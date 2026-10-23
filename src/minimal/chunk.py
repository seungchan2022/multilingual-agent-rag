"""코퍼스 마크다운 20개를 청크로 나누는 프로그램. 청크 묶음 4개(크기 128·256 × 제목 붙임·붙이지 않음)를 만든다.

  uv run python src/minimal/chunk.py

규칙은 decisions/stage4.md의 2026-10-22·23 줄(청크는 문서 구조를 따라 나눈다 / 표 규칙 / 가장 작은 단위 / 줄 번호 목록)에 있다.
크기는 글자 수가 아니라 BAAI/bge-m3 토크나이저의 토큰 수다. gte-multilingual-base는 코퍼스 모든 줄에서 같은 토큰을 내므로 두 모델이 묶음을 함께 쓴다.
모델은 캐시에서만 읽는다(HF_HUB_OFFLINE=1). 시계, 무작위, 인터넷을 쓰지 않아 같은 입력에서는 바이트까지 같은 파일이 나온다.
표의 둘째 머리글 줄은 마크다운만 보고 가를 수 없어 research_notes/stage2_table_shapes_rare_earth/tables.json에서 읽고,
표 두 개(neutron-capture-therapy 56줄, 187줄)는 청크 글만 바꿔 쓴다(코퍼스 파일은 고치지 않는다).
동위 원소 표 4개는 들뜬 상태 행에 둘째 머리글 줄의 이름을 붙이고 그 둘째 줄을 청크에 붙이지 않는다(decisions/stage4.md 마지막 줄).
규칙이 맞지 않는 모양을 만나면 예외를 던지고 멈춘다(규칙을 고쳐서 맞추지 않는다).
"""
import json
import os
import re
import sys
from collections import namedtuple
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"  # transformers를 불러오기 전에 켠다. 모델을 캐시에서만 읽는다

ROOT = Path(__file__).resolve().parents[2]
MARKDOWN = ROOT / "data" / "corpus" / "markdown"
RAW = ROOT / "data" / "corpus" / "raw"
TABLES = ROOT / "research_notes" / "stage2_table_shapes_rare_earth" / "tables.json"
OUT_DIR = ROOT / "data" / "minimal" / "chunks"
MODEL = "BAAI/bge-m3"
SIZES = (128, 256)

NCT = "wiki-en-neutron-capture-therapy"
EXC_NAMES = (NCT, 56)   # 표 예외 1: 머리글이 없는 목록 표(Table 1). 이름을 한 줄에 하나씩 쓴다
EXC_ACCEL = (NCT, 187)  # 표 예외 2: 첫 열에 네 가지가 붙은 가속기 설치 현황 표. 네 열로 나눈다

# 문장 경계로 보지 않는 마침표 앞의 낱말(소문자). 한 글자 머리글자(H. J. Taylor)와 U.S.·e.g. 꼴은 아래 정규식이 맡는다
ABBREVIATIONS = {"dr", "mr", "mrs", "prof", "st", "vs", "fig", "figs", "no", "nos", "approx", "ca", "cf", "al",
                 "inc", "ltd", "co", "jr", "sr", "eq", "vol", "ref", "ph.d"}
CLOSING_QUOTES = "\"'”’»"
OPENING = "([{（"
CLOSING = ")]}）"

Piece = namedtuple("Piece", "text lines")        # 청크 글의 한 줄과, 그 줄이 나온 원문 줄 번호들
Group = namedtuple("Group", "key ctx rows")      # 같이 두는 줄 묶음. ctx는 key가 처음 나올 때 앞에 붙는 줄(표 이름·제목·머리글)
Unit = namedtuple("Unit", "lineno sep text")     # 글의 문장 하나(또는 목록 항목 줄 하나). sep은 같은 줄 앞 문장과의 사이 공백
Block = namedtuple("Block", "pieces units")      # 빈 줄로 나뉜 글 덩어리 하나. pieces는 원문 줄 그대로, units는 문장으로 나눈 것
Table = namedtuple("Table", "fixed groups")      # 표(또는 정보 상자 묶음). fixed는 조각마다 맨 위에 붙는 줄


class Counter:
    """청크 글의 토큰 수를 센다. 모델은 처음 셀 때 불러오고, 센 글은 기억해 둔다."""

    def __init__(self):
        self.tok = None
        self.cache = {}

    def __call__(self, text):
        n = self.cache.get(text)
        if n is None:
            if self.tok is None:
                from transformers import AutoTokenizer
                self.tok = AutoTokenizer.from_pretrained(MODEL)
            n = len(self.tok.encode(text, add_special_tokens=False))
            self.cache[text] = n
        return n


class TableMeta:
    """tables.json에서 읽은 표 정보. 둘째 머리글 줄 수와 표 제목 줄 여부는 마크다운만으로 알 수 없다."""

    def __init__(self, entries):
        self.th_rows = {}   # (doc_id, 표 첫 줄) -> 머리글 줄 수(top_th_rows)
        self.captions = {}  # (doc_id, 표 첫 줄) -> 표 제목 글
        self.starts = {}    # doc_id -> 표 첫 줄 집합
        for e in entries:
            if e["md_line_no"] is None:  # 지운 절에 있던 표
                continue
            k = (e["doc_id"], e["md_line_no"])
            self.th_rows[k] = e["top_th_rows"]
            if e["caption"]:
                self.captions[k] = e["caption"]
            self.starts.setdefault(e["doc_id"], set()).add(e["md_line_no"])

    @classmethod
    def load(cls):
        return cls(json.loads(TABLES.read_text(encoding="utf-8")))


# ---------------------------------------------------------------- 문장 나누기

def split_sentences(line):
    """줄 하나를 문장으로 나눈다. (앞 문장과의 사이 공백, 문장 글) 목록을 돌려준다.

    . ! ? 뒤에 (닫는 따옴표를 건너) 공백이 오고 그 다음 글자가 영어 소문자가 아니면 문장 끝이다. 아래는 끝으로 보지 않는다.
    괄호 안의 마침표(문장 전체가 괄호 하나로 싸인 "(…끝.) 다음"만 괄호를 닫은 뒤를 끝으로 본다), 한 글자 머리글자(H. J. Taylor, 숫자 뒤의 91 K.는 제외),
    U.S.·e.g. 꼴, ABBREVIATIONS의 낱말. 소수점(9.84)은 뒤에 공백이 없어 저절로 빠진다. 한국어는 "다. 다음"처럼 한글이 소문자가 아니라 그대로 나뉜다.
    """
    out = []
    start, depth, open_at, i, n = 0, 0, -1, 0, len(line)
    sep = ""
    while i < n:
        c = line[i]
        if c in OPENING:
            if depth == 0:
                open_at = i
            depth += 1
        elif c in CLOSING:
            depth = max(0, depth - 1)
        elif c in ".!?":
            j = i
            while j + 1 < n and line[j + 1] in ".!?":
                j += 1
            # 문장이 괄호 하나로 통째로 싸인 꼴 "(…끝.) 다음"은 괄호를 닫은 뒤를 끝으로 본다
            whole = depth == 1 and open_at == start and j + 1 < n and line[j + 1] in CLOSING
            if depth == 0 or whole:
                k = j + 2 if whole else j + 1
                while k < n and line[k] in CLOSING_QUOTES:
                    k += 1
                if k < n and line[k].isspace():
                    m = k
                    while m < n and line[m].isspace():
                        m += 1
                    if m < n and not line[m].islower() and not (j == i and c == "." and is_abbreviation(line, i)):
                        out.append((sep, line[start:k]))
                        sep, start, depth = line[k:m], m, 0
                        i = m
                        continue
            i = j
        i += 1
    if start < n:
        out.append((sep, line[start:]))
    return out


def is_abbreviation(line, i):
    """line[i]의 마침표 바로 앞 낱말이 문장 끝이 아닌 줄임 꼴인지. 한 글자는 머리글자로 보되, 숫자 낱말 뒤(91 K.)는 단위라 문장 끝으로 본다."""
    a = i
    while a > 0 and not line[a - 1].isspace() and line[a - 1] not in OPENING + CLOSING_QUOTES:
        a -= 1
    word = line[a:i]
    if re.fullmatch(r"[A-Za-z]", word):
        before = line[:a].rstrip()
        return not (before and before[-1].isdigit())
    return bool(re.fullmatch(r"(?:[A-Za-z]\.)+[A-Za-z]", word) or word.lower() in ABBREVIATIONS)


def is_item_line(text):
    """목록 항목 줄(- 로 시작하거나 1. 꼴)은 문장 나누기 없이 한 문장으로 본다."""
    return bool(re.match(r"\s*- |\d+\. ", text))


def make_block(lines):
    """빈 줄로 나뉜 글 덩어리 하나. lines는 (줄 번호, 줄 글) 목록."""
    pieces, units = [], []
    for no, text in lines:
        pieces.append(Piece(text, (no,)))
        if is_item_line(text):
            units.append(Unit(no, "", text))
        else:
            units += [Unit(no, sep, s) for sep, s in split_sentences(text)]
    return Block(pieces, units)


def pieces_of(units):
    """문장들을 청크 글의 줄로 잇는다. 같은 줄의 문장은 원래 공백으로, 다른 줄은 줄바꿈으로 나뉜다."""
    out = []
    for u in units:
        if out and out[-1][1] == u.lineno:
            out[-1][0] += u.sep + u.text
        else:
            out.append([u.text, u.lineno])
    return [Piece(t, (no,)) for t, no in out]


# ---------------------------------------------------------------- 표 읽기

def cells_of(line):
    return [c.strip() for c in line.strip()[1:-1].split("|")]


def table_end(ls, i):
    """ls[i]에서 시작하는 이어진 표 줄의 끝(포함) 인덱스."""
    j = i
    while j + 1 < len(ls) and ls[j + 1].startswith("|"):
        j += 1
    return j


def piece_at(ls, k):
    """1부터 세는 줄 번호 k의 원문 줄."""
    return Piece(ls[k - 1].rstrip(), (k,))


def name_spans(head1, head2):
    """둘째 머리글 줄에서 같은 이름이 이웃한 열 둘 이상에 이어지고 그 열들의 첫째 머리글 이름이 서로 다른 구간 [(처음 열, 끝 열(미포함))] 목록.
    (들뜬 에너지가 Z(p)·N(n)·동위 원소 질량 세 열에 걸친 꼴. Main isotopes 표는 둘째 줄에 같은 이름이 이어지지 않아 빈 목록이다.)"""
    spans, i = [], 0
    while i < len(head2):
        j = i + 1
        while j < len(head2) and head2[j] == head2[i]:
            j += 1
        if j - i >= 2 and len(set(head1[i:j])) == j - i:
            spans.append((i, j))
        i = j
    return spans


def named_row(line, n, spans, names):
    """들뜬 상태 행(이름 구간의 칸이 모두 같은 글자이고 비어 있지 않음)이면 구간의 첫 칸에 '이름 값'을 쓰고 나머지 칸을 비운 줄을, 아니면 None을 돌려준다."""
    cells = cells_of(line)
    if len(cells) != n:
        raise ValueError(f"칸 수가 머리글과 다름: {len(cells)} / {n}: {line!r}")
    changed = False
    for a, b in spans:
        if cells[a] and all(c == cells[a] for c in cells[a:b]):
            cells[a:b] = [f"{names[a]} {cells[a]}"] + [""] * (b - a - 1)
            changed = True
    return "| " + " | ".join(cells) + " |" if changed else None


def group_rows(ls, rows, key, ctx, spans=(), head2=()):
    """표 행(줄 번호 목록)을, 첫 칸이 같은 이어진 행끼리 묶는다. spans가 있으면 들뜬 상태 행은 이름을 붙인 꼴로 쓴다."""
    groups = []
    for k in rows:
        first = cells_of(ls[k - 1])[0]
        piece = piece_at(ls, k)
        if spans:
            named = named_row(ls[k - 1], len(head2), spans, head2)
            if named is not None:
                piece = Piece(named, (k,))
        if groups and groups[-1][0] == first:
            groups[-1][1].append(piece)
        else:
            groups.append((first, [piece]))
    return [Group(key, tuple(ctx), rows_) for _, rows_ in groups]


def normal_table(ls, doc_id, first, last, meta, ctx_prefix):
    """보통 표. first·last는 1부터 세는 줄 번호. 머리글 = 첫 줄 + 구분 줄 + 그 아래 (top_th_rows - 1)줄.
    머리글이 두 줄 이상이고 둘째 줄에 이름 구간이 있으면(name_spans) 들뜬 상태 행에 이름을 붙이고 둘째 머리글 줄은 붙이지 않는다.
    둘째 줄이 구간 밖에서 첫째 줄과 다르면 멈춘다."""
    th = meta.th_rows.get((doc_id, first), 1)
    header_len = 1 + max(th, 1)
    if not re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", ls[first].strip()):
        raise ValueError(f"{doc_id}:{first}: 둘째 줄이 구분 줄이 아님")
    if last - first + 1 <= header_len:
        raise ValueError(f"{doc_id}:{first}: 표에 행이 없음")
    head_nos = list(range(first, first + header_len))
    spans, head2 = [], []
    if th >= 2:
        head1, head2 = cells_of(ls[first - 1]), cells_of(ls[first + 1])
        spans = name_spans(head1, head2) if len(head1) == len(head2) else []
        if spans:
            inside = {c for a, b in spans for c in range(a, b)}
            if any(h1 != h2 for c, (h1, h2) in enumerate(zip(head1, head2)) if c not in inside):
                raise ValueError(f"{doc_id}:{first + 2}: 둘째 머리글 줄이 이름 구간 밖에서 첫째 줄과 다름")
            head_nos.remove(first + 2)
    ctx = list(ctx_prefix) + [piece_at(ls, k) for k in head_nos]
    return Table([], group_rows(ls, range(first + header_len, last + 1), first, ctx, spans, head2))


def names_table(ls, doc_id, first, last, title_no):
    """표 예외 1(neutron-capture-therapy Table 1). 표 대신 표 제목 아래에 이름을 한 줄에 하나씩 쓴다.
    왼쪽 열을 위에서 아래로, 이어서 오른쪽 열. 이름 23개(빈 칸 제외). 조각마다 표 제목을 붙이고, 원래 표의 머리글·구분 줄(56·57)은 줄 목록에 넣는다."""
    cols = [[], []]
    for k in range(first, last + 1):
        if k == first + 1:
            continue
        cells = cells_of(ls[k - 1])
        if len(cells) != 2:
            raise ValueError(f"{NCT}:{k}: 열이 둘이 아님")
        for c in (0, 1):
            if cells[c]:
                cols[c].append(Piece(cells[c], (k,)))
    if len(cols[0]) + len(cols[1]) != 23:
        raise ValueError(f"{NCT}: 표 1의 이름이 23개가 아님: {len(cols[0]) + len(cols[1])}")
    ctx = (Piece(ls[title_no - 1].rstrip(), (title_no, first, first + 1)),)
    return Table([], [Group(first, ctx, [p]) for p in cols[0] + cols[1]])


SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def accel_first_cells():
    """원본 HTML에서 가속기 표의 머리글과 값 행(14개)의 첫 칸을 <p> 경계로 나눈 조각 목록을 읽는다.
    칸 글자 변환은 마크다운과 같게 맞춘다(인용 번호는 지우고 위첨자는 유니코드로). 첫 칸이 rowspan인 행은 위 칸을 이어 쓴다."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup((RAW / f"{NCT}.html").read_text(encoding="utf-8"), "html.parser")
    tables = [t for t in soup.find_all("table") if t.find("tr") and t.find("tr").get_text().strip().startswith("Manufacturer")]
    if len(tables) != 1:
        raise ValueError(f"{NCT}: 가속기 표를 하나로 못 찾음: {len(tables)}")

    def segments(cell):
        for s in cell.find_all("sup", class_="reference"):
            s.decompose()
        for s in cell.find_all("sup"):
            s.string = s.get_text().translate(SUPERSCRIPT)
        direct = "".join(str(x) for x in cell.children if isinstance(x, str))
        return [" ".join(direct.split())] + [" ".join(p.get_text().split()) for p in cell.find_all("p", recursive=False)]

    trs = tables[0].find_all("tr")
    header = segments(trs[0].find_all(["th", "td"], recursive=False)[0])
    rows, pending, left = [], None, 0
    for tr in trs[1:]:
        cells = tr.find_all(["th", "td"], recursive=False)
        if left > 0:
            first, rest, left = pending, cells, left - 1
        else:
            first, rest = cells[0], cells[1:]
            if int(first.get("rowspan", 1)) > 1:
                pending, left = first, int(first["rowspan"]) - 1
        if len(rest) != 3:
            raise ValueError(f"{NCT}: 가속기 표 행의 나머지 칸이 3개가 아님")
        rows.append(segments(first))
    return header, rows


def split_four(segs, md_cell):
    """첫 칸 조각을 네 열(Manufacturer, Product, Reaction, Accelerator type)로 놓는다.
    조각이 셋이면 제품 이름이 원본에 없는 행이다(Product 칸을 비운다). 이어 붙인 글이 마크다운 첫 칸과 다르면 멈춘다."""
    if " ".join(s for s in segs if s) != md_cell:
        raise ValueError(f"{NCT}: 원본 칸 조각을 이으면 마크다운 첫 칸과 다름: {segs!r} / {md_cell!r}")
    if len(segs) == 4:
        return segs
    if len(segs) == 3:
        return [segs[0], ""] + segs[1:]
    raise ValueError(f"{NCT}: 첫 칸 조각이 {len(segs)}개: {segs!r}")


def accel_table(ls, first, last):
    """표 예외 2(neutron-capture-therapy 187~202줄). 머리글 187줄, 구분 188줄, 값 행 189~202줄 14행."""
    header, rows = accel_first_cells()
    if last - first - 1 != len(rows):
        raise ValueError(f"{NCT}: 가속기 표 행 수가 원본과 다름: {last - first - 1} / {len(rows)}")
    md_head = cells_of(ls[first - 1])
    head = split_four(header, md_head[0]) + md_head[1:]
    sep = "|" + "---|" * len(head)
    ctx = (Piece("| " + " | ".join(head) + " |", (first,)), Piece(sep, (first + 1,)))
    groups = []
    for k, segs in zip(range(first + 2, last + 1), rows):
        cells = cells_of(ls[k - 1])
        row = split_four(segs, cells[0]) + cells[1:]
        piece = Piece("| " + " | ".join(row) + " |", (k,))
        if groups and groups[-1][0] == cells[0]:
            groups[-1][1].append(piece)
        else:
            groups.append((cells[0], [piece]))
    return Table([], [Group(first, ctx, rows_) for _, rows_ in groups])


# ---------------------------------------------------------------- 문서 읽기

def infobox_region(ls):
    """정보 상자가 있을 수 있는 구간 [3줄, 처음으로 목록·표·빈 줄이 아닌 줄)의 인덱스(0부터)."""
    j = 2
    while j < len(ls) and (ls[j] == "" or ls[j].startswith(("- ", "  - ", "|"))):
        j += 1
    return 2, j


def infobox_end(ls):
    """정보 상자가 끝난 줄 번호(1부터, 마지막으로 글이 있는 줄). 정보 상자(`- ` 줄)가 없으면 None."""
    a, b = infobox_region(ls)
    if not any(l.startswith("- ") for l in ls[a:b]):
        return None
    while ls[b - 1] == "":
        b -= 1
    return b


def parse_infobox(doc_id, ls, meta, starts):
    """정보 상자 구간을 (묶음 앞에 놓인 표 목록, 묶음 목록)으로 읽는다. 첫 묶음 앞의 표는 본문 표로 다룬다.
    묶음 하나는 (이름 줄 번호, Table). 이름 줄 아래 표가 없고 항목 줄만 있으면 Table의 fixed가 이름 줄이다."""
    a, b = infobox_region(ls)
    bundles, orphans = [], []
    i = a
    while i < b:
        line = ls[i]
        if line.startswith("- "):
            bundles.append({"name": i, "elems": []})
            i += 1
        elif line.startswith("  - "):
            bundles[-1]["elems"].append(("line", i))
            i += 1
        elif line.startswith("|"):
            j = table_end(ls, i)
            starts.append(i + 1)
            if not bundles:
                orphans.append((i + 1, j + 1))
            else:
                bundles[-1]["elems"].append(("table", i, j))
            i = j + 1
        else:
            i += 1

    out = []
    for bd in bundles:
        name = bd["name"]
        # 표 이름 줄: 빈 줄 하나를 건너 바로 아래에 표가 오는 항목 줄. 묶음 이름 줄 바로 아래 표는 묶음 이름 줄이 그 역할이다
        table_names = {e[1] - 2 for e in bd["elems"] if e[0] == "table" and e[1] >= 2 and ls[e[1] - 1] == ""
                       and ls[e[1] - 2].startswith("  - ")}
        groups = []
        seen_table = False
        for e in bd["elems"]:
            if e[0] == "line":
                if e[1] in table_names:
                    continue
                if seen_table:
                    raise ValueError(f"{doc_id}:{e[1] + 1}: 정보 상자 표 뒤에 항목 줄이 있음(규칙이 가리키지 않는 모양)")
                groups.append(Group(None, (), [piece_at(ls, e[1] + 1)]))
            else:
                seen_table = True
                prefix = [piece_at(ls, e[1] - 1)] if e[1] - 2 in table_names else []
                groups += normal_table(ls, doc_id, e[1] + 1, e[2] + 1, meta, prefix).groups
        out.append((name + 1, ls[name][2:], Table([piece_at(ls, name + 1)], groups)))
    return orphans, out


def parse_body(doc_id, ls, start, meta, starts):
    """본문을 절 목록 [(절 경로의 제목들, [요소...])]로 읽는다. 요소는 ("text", Block) 또는 ("table", Table).
    start는 본문이 시작하는 인덱스(0부터). 제목 줄(##~####)마다 새 절이 시작한다. 표 제목 줄은 표에 붙인다."""
    sections = [([], [])]
    stack = []
    i = start
    while i < len(ls):
        line = ls[i]
        m = re.match(r"(#{2,4}) (.*)", line)
        if m:
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, m.group(2)))
            sections.append(([t for _, t in stack], []))
            i += 1
        elif line == "":
            i += 1
        elif line.startswith("|"):
            j = table_end(ls, i)
            starts.append(i + 1)
            sections[-1][1].append(("table", body_table(doc_id, ls, i + 1, j + 1, meta, sections[-1][1])))
            i = j + 1
        else:
            j = i
            while j + 1 < len(ls) and ls[j + 1] != "" and not ls[j + 1].startswith(("|", "#")):
                j += 1
            if j + 1 < len(ls) and ls[j + 1].startswith("|"):
                raise ValueError(f"{doc_id}:{j + 2}: 글과 표가 빈 줄 없이 붙어 있음")
            sections[-1][1].append(("text", make_block([(k + 1, ls[k].rstrip()) for k in range(i, j + 1)])))
            i = j + 1
    return [s for s in sections if s[1]]


def body_table(doc_id, ls, first, last, meta, elements):
    """본문 표 하나. 표 제목 줄이 있는 표(tables.json의 caption)는 바로 앞 글 덩어리를 가져와 표에 붙인다."""
    key = (doc_id, first)
    title_no = None
    if key in meta.captions:
        title_no = first - 2
        prev = elements.pop() if elements else None
        if (prev is None or prev[0] != "text" or len(prev[1].pieces) != 1 or prev[1].pieces[0].lines != (title_no,)
                or ls[first - 2] != "" or prev[1].pieces[0].text != meta.captions[key]):
            raise ValueError(f"{doc_id}:{first}: 표 제목 줄이 표 바로 위(빈 줄 하나 건너)에 없음")
    if key == EXC_NAMES:
        return names_table(ls, doc_id, first, last, title_no)
    if key == EXC_ACCEL:
        return accel_table(ls, first, last)
    prefix = [piece_at(ls, title_no)] if title_no else []
    return normal_table(ls, doc_id, first, last, meta, prefix)


# ---------------------------------------------------------------- 청크 만들기

class Chunker:
    """크기와 제목 붙임 여부 하나에 대한 청크 만들기. 한도 안에 드는지는 늘 청크 글 전체를 한 번에 세어 본다."""

    def __init__(self, count, size, title):
        self.count, self.size, self.title = count, size, title

    def render(self, path, pieces):
        text = "\n".join(p.text for p in pieces)
        return path + "\n" + text if self.title else text

    def fits(self, path, pieces):
        return self.count(self.render(path, pieces)) <= self.size

    def pack(self, path, table):
        """표(또는 정보 상자 묶음)를 조각으로 나눈다. 줄 묶음(첫 칸이 같은 이어진 행)을 앞에서부터 한도까지 채운다.
        묶음이 지금 조각에 안 들어가면 새 조각에서 시작하고, 새 조각에도 안 들어가면 행 하나씩으로 풀어 채운다.
        조각마다 fixed(묶음 이름 줄)와, 표가 시작하는 곳에 ctx(표 이름 줄·표 제목·머리글)가 붙는다.
        가장 작은 단위(fixed + ctx + 행 하나)는 한도를 넘어도 자르지 않는다."""
        def assemble(groups):
            pieces, last = list(table.fixed), None
            for g in groups:
                if g.key is not None and g.key != last:
                    pieces += g.ctx
                last = g.key
                pieces += g.rows
            return pieces

        if not table.groups:  # 항목 줄이 없는 정보 상자 묶음(이름 줄만 있다)
            return [list(table.fixed)]
        chunks, cur, todo = [], [], list(table.groups)
        while todo:
            g = todo.pop(0)
            if cur and self.fits(path, assemble(cur + [g])):
                cur.append(g)
                continue
            if len(g.rows) > 1 and not self.fits(path, assemble([g])):
                todo[0:0] = [Group(g.key, g.ctx, [r]) for r in g.rows]
                continue
            if cur:
                chunks.append(assemble(cur))
            cur = [g]
        if cur:
            chunks.append(assemble(cur))
        return chunks

    def split_units(self, path, units):
        """한도를 넘는 문단을 문장 경계에서 나눈다. 앞 조각의 마지막 문장 하나를 다음 조각 맨 앞에 다시 넣되,
        겹친 문장과 다음 문장이 한도 안에 들 때만 넣는다. 조각마다 새 문장이 적어도 하나 든다."""
        chunks, i, prev = [], 0, None
        while i < len(units):
            cur = []
            if prev is not None and self.fits(path, pieces_of([prev, units[i]])):
                cur = [prev]
            cur.append(units[i])
            i += 1
            while i < len(units) and self.fits(path, pieces_of(cur + [units[i]])):
                cur.append(units[i])
                i += 1
            chunks.append(pieces_of(cur))
            prev = cur[-1]
        return chunks

    def text_chunks(self, path, blocks):
        """한 절의 글 덩어리들(사이에 표가 없는 이어진 것)을 청크로 만든다. 앞에서부터 한도까지 합치고,
        한도를 넘는 문단은 혼자 문장 경계에서 나눈다(조각이 이웃 문단을 끌어들이지 않는다)."""
        out, cur = [], []
        for b in blocks:
            if cur and self.fits(path, [p for c in cur for p in c.pieces] + b.pieces):
                cur.append(b)
                continue
            if cur:
                out.append([p for c in cur for p in c.pieces])
                cur = []
            if self.fits(path, b.pieces):
                cur = [b]
            else:
                out += self.split_units(path, b.units)
        if cur:
            out.append([p for c in cur for p in c.pieces])
        return out

    def doc_chunks(self, doc_id, ls, meta):
        """문서 하나의 청크 목록(chunk_id 앞의 순번 없이). 문서 안 등장 순서대로."""
        if not ls[0].startswith("# ") or ls[1] != "":
            raise ValueError(f"{doc_id}: 1줄이 '# 제목', 2줄이 빈 줄이 아님")
        doc_title = ls[0][2:]
        starts = []
        orphans, bundles = parse_infobox(doc_id, ls, meta, starts)
        a, b = infobox_region(ls)
        sections = parse_body(doc_id, ls, b, meta, starts)
        want = meta.starts.get(doc_id)
        if want is not None and set(starts) != want:
            raise ValueError(f"{doc_id}: 표 첫 줄이 tables.json과 다름: {sorted(set(starts) ^ want)}")

        out = []

        def emit(kind, path, pieces):
            text = self.render(path, pieces)
            tokens = self.count(text)
            lines = sorted({n for p in pieces for n in p.lines})
            out.append({"doc_id": doc_id, "language": doc_id.split("-")[1], "size": self.size, "title": self.title,
                        "kind": kind, "path": path, "text": text, "line_start": lines[0], "line_end": lines[-1],
                        "lines": lines, "tokens": tokens, "over_limit": tokens > self.size})

        # 첫 묶음 앞의 표(en-isotopes-of-yttrium 3줄)는 본문 표다(머리말 절)
        for first, last in orphans:
            table = normal_table(ls, doc_id, first, last, meta, [])
            for pieces in self.pack(doc_title, table):
                emit("table", doc_title, pieces)
        for _, name, table in bundles:
            path = f"{doc_title} > {name}"
            for pieces in self.pack(path, table):
                emit("infobox", path, pieces)
        for headings, elements in sections:
            path = " > ".join([doc_title] + headings)
            run = []
            for kind, el in elements + [("end", None)]:
                if kind == "text":
                    run.append(el)
                    continue
                for pieces in self.text_chunks(path, run):
                    emit("text", path, pieces)
                run = []
                if kind == "table":
                    for pieces in self.pack(path, el):
                        emit("table", path, pieces)
        for n, c in enumerate(out, 1):
            c["chunk_id"] = f"{doc_id}#{n:04d}"
        # JSON 칸 순서를 정해 둔다
        order = ["chunk_id", "doc_id", "language", "size", "title", "kind", "path", "text",
                 "line_start", "line_end", "lines", "tokens", "over_limit"]
        return [{k: c[k] for k in order} for c in out]


def load_docs():
    """코퍼스 마크다운을 파일 이름 순으로 읽는다. {doc_id: 줄 목록}."""
    return {p.stem: p.read_text(encoding="utf-8").split("\n") for p in sorted(MARKDOWN.glob("*.md"))}


def build_all(out_dir=OUT_DIR, count=None):
    """청크 묶음 4개를 out_dir에 쓰고, 묶음별 (파일 이름, 청크 수, 한도를 넘은 수, 가장 긴 토큰 수) 목록을 돌려준다."""
    count = count or Counter()
    meta = TableMeta.load()
    docs = load_docs()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stats = []
    for size in SIZES:
        for title in (False, True):
            chunker = Chunker(count, size, title)
            rows = []
            for doc_id, ls in docs.items():
                rows += chunker.doc_chunks(doc_id, ls, meta)
            name = f"size{size}_{'title' if title else 'notitle'}.jsonl"
            text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
            with open(out_dir / name, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            stats.append((name, len(rows), sum(r["over_limit"] for r in rows), max(r["tokens"] for r in rows)))
    return stats


def main(out_dir=OUT_DIR):
    for name, n, over, longest in build_all(out_dir):
        print(f"{name}: 청크 {n}개, 한도를 넘은 청크 {over}개, 가장 긴 청크 {longest}토큰")


if __name__ == "__main__":
    main(*sys.argv[1:2])
