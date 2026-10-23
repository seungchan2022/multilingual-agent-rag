"""표 청크 확인(이슈 #10. 미정 목록 "만들어진 표 청크를 전부 열어, 행마다 값이 맞는 머리글과 짝지어졌는지 확인한다").

  .venv/bin/python research_notes/stage5_table_chunks/check.py

값과 머리글의 짝이 깨질 수 있는 곳은 둘이라 둘 다 본다.
가. 변환(원문 HTML → 마크다운 표 37개): 변환이 받은 원문 표(지울 것을 지운 뒤)를 붙잡아, 합친 칸을 이 프로그램이 따로 편 격자와
    마크다운 표를 칸마다 견준다. 마크다운의 열은 왼쪽부터, 모든 줄의 글자가 같은 첫 HTML 열에 짝짓는다. 모든 마크다운 열이
    짝을 찾고, 짝이 없는 HTML 열이 값이 빈 열이거나 왼쪽 열의 되풀이(가로로 합친 칸을 편 것)이면, 마크다운의 값은 모두 원문과
    같은 머리글 아래에 있다. 칸 글자는 build.inline으로 읽는다(글자 꼴이 아니라 자리를 보는 확인이다).
나. 청크(묶음 4개의 표가 든 청크 전부): 청크마다 그 표의 머리글 줄이 전부 원문 그대로 붙었는지, 표 제목·표 이름 줄(있으면)이
    머리글 바로 위에 있는지, 행이 그 표의 원문 줄 그대로 원문 순서로 머리글 아래 이어지는지, 줄마다 칸 수가 머리글과 같은지,
    정보 상자 청크는 묶음 이름 줄로 시작하는지 본다. 묶음마다 표의 행이 정확히 한 청크에 드는지(빠짐·겹침 없음)도 본다.
    표 예외 1(목록으로 바꾼 표)과 예외 2(첫 열을 네 열로 나눈 표)는 원문에서 따로 기대값을 만들어 견준다.
결과: 같은 폴더의 verdicts.jsonl(청크마다 판정), tables.json(표마다 판정과 행 모양), output.txt(요약).
"""
import copy
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src" / "corpus"))
import build  # noqa: E402

CORPUS = ROOT / "data" / "corpus"
CHUNKS = ROOT / "data" / "minimal" / "chunks"
SETS = ["size128_notitle", "size128_title", "size256_notitle", "size256_title"]
EX1 = ("wiki-en-neutron-capture-therapy", 56)   # 표 예외 1: 머리글 없는 목록 표(표 제목 54줄)
EX2 = ("wiki-en-neutron-capture-therapy", 187)  # 표 예외 2: 첫 열에 네 가지가 붙은 표
EX2_HEAD = ["Manufacturer", "Product", "Reaction", "Accelerator type"]


# ---------------------------------------------------------------- 가. 변환

def traced(d, raw):
    """변환을 돌리며 표마다 (변환이 받은 원문 표의 사본, 변환 결과 항목)을 모은다."""
    calls, original = [], build.table_items

    def wrap(table):
        snap = copy.copy(table)  # 변환 전의 모습. bs4의 copy는 자식까지 복사한다
        result = original(table)
        calls.append((snap, result))
        return result

    build.table_items = wrap
    try:
        text = build.convert_wiki(d, raw)
    finally:
        build.table_items = original
    return text, calls


def own_rows(t):
    return [tr for tr in t.find_all("tr") if tr.find_parent("table") is t]


def own_cells(tr):
    return tr.find_all(["th", "td"], recursive=False)


def spanv(cell, attr):
    v = cell.get(attr, "")
    return int(v) if v.isdigit() and int(v) > 0 else 1


def expand(t):
    """합친 칸을 편 격자. 칸마다 (원래 칸의 번호, 글자, th인가). 원래 칸이 없는 자리는 (None, '', False)."""
    rows = own_rows(t)
    occ, n = {}, 0
    for r, tr in enumerate(rows):
        c = 0
        for cell in own_cells(tr):
            while (r, c) in occ:
                c += 1
            n += 1
            rs, cs = spanv(cell, "rowspan"), spanv(cell, "colspan")
            for dr in range(rs):
                for dc in range(cs):
                    if r + dr < len(rows):
                        occ.setdefault((r + dr, c + dc), (n, build.inline(cell), cell.name == "th"))
            c += cs
    ncols = max((c for _, c in occ), default=-1) + 1
    grid = [[occ.get((r, c), (None, "", False)) for c in range(ncols)] for r in range(len(rows))]
    return rows, grid, ncols


def md_cells(line):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)[1:-1]]


def md_groups(lines):
    """'|'로 시작하는 줄이 이어진 묶음: [(시작 줄 번호, 줄 목록)]."""
    groups, cur = [], None
    for i, l in enumerate(lines, 1):
        if l.startswith("|"):
            if cur is None:
                cur = (i, [])
                groups.append(cur)
            cur[1].append(l)
        else:
            cur = None
    return groups


def check_table(snap, md_start, md_lines):
    """원문 표와 마크다운 표(md_lines, 둘째 줄은 구분 줄)를 견준다."""
    rows, grid, ncols = expand(snap)
    full = [len(own_cells(tr)) == 1 and spanv(own_cells(tr)[0], "colspan") > 1
            and spanv(own_cells(tr)[0], "colspan") >= ncols for tr in rows]
    spanned = [bool(own_cells(tr)) and all(spanv(c, "rowspan") > 1 for c in own_cells(tr)) for tr in rows]
    kept = [r for r in range(len(rows)) if not full[r] and not spanned[r]]
    md = [md_cells(md_lines[0])] + [md_cells(l) for l in md_lines[2:]]
    md_no = [md_start] + list(range(md_start + 2, md_start + len(md_lines)))
    rec = {"html_rows": len(rows), "html_cols": ncols, "kept_rows": len(kept), "md_rows": len(md),
           "md_cols": len(md[0]), "moved_rows": [r + 1 for r in range(len(rows)) if full[r]],
           "spanned_rows": [r + 1 for r in range(len(rows)) if spanned[r]], "problems": []}
    if len(kept) != len(md):
        rec["problems"].append(f"줄 수가 다르다: 원문(뺀 줄 제외) {len(kept)}, 마크다운 {len(md)}")
        return rec, None
    bad = [i for i, cs in enumerate(md) if len(cs) != len(md[0])]
    if bad:
        rec["problems"].append(f"칸 수가 머리글과 다른 마크다운 줄: {[md_no[i] for i in bad]}")
        return rec, None
    # 마크다운 열마다, 모든 줄의 글자가 같은 첫 HTML 열(앞 열의 짝보다 오른쪽)을 짝으로 삼는다
    mapping, prev = [], -1
    for j in range(len(md[0])):
        c = next((c for c in range(prev + 1, ncols)
                  if all(md[i][j] == grid[kept[i]][c][1] for i in range(len(kept)))), None)
        if c is None:
            # 어느 줄에서 어긋나는지 남긴다: 다음 HTML 열과 견준 첫 어긋남
            c2 = prev + 1
            diff = [(md_no[i], md[i][j], grid[kept[i]][c2][1] if c2 < ncols else None)
                    for i in range(len(kept)) if c2 >= ncols or md[i][j] != grid[kept[i]][c2][1]][:3]
            rec["problems"].append(f"마크다운 {j + 1}열의 짝 HTML 열이 없다. 다음 열과의 어긋남(줄, 마크다운, 원문): {diff}")
            return rec, None
        mapping.append(c)
        prev = c
    head_th = all(x.name == "th" for x in own_cells(rows[kept[0]])) if own_cells(rows[kept[0]]) else False
    value_rows = kept[1:] if head_th else kept
    dropped = []
    for c in range(ncols):
        if c in mapping:
            continue
        if c > 0 and all(grid[r][c][0] == grid[r][c - 1][0] for r in kept):
            dropped.append((c + 1, "왼쪽 열의 되풀이"))
        elif all(grid[r][c][1] == "" for r in value_rows if not grid[r][c][2]):
            dropped.append((c + 1, "값이 빈 열"))
        else:
            dropped.append((c + 1, "값이 있는데 빠짐"))
            rec["problems"].append(f"원문 {c + 1}열이 값이 있는데 마크다운에 없다")
    rec["mapping"] = [c + 1 for c in mapping]
    rec["dropped"] = dropped
    # 머리글 줄 수: 첫 줄부터 이어진, 자기 칸이 모두 th인 남은 줄
    top = 0
    while top < len(kept) and own_cells(rows[kept[top]]) and all(x.name == "th" for x in own_cells(rows[kept[top]])):
        top += 1
    rec["header_rows"] = top
    # 행 모양: 값 줄마다 같은 원래 칸에서 나온 이웃 마크다운 열의 길이. 1만 있으면 보통 줄
    shapes = Counter()
    examples = {}
    for i in range(top, len(kept)):
        r = kept[i]
        runs, j = [], 0
        while j < len(mapping):
            k = j
            while k + 1 < len(mapping) and grid[r][mapping[k + 1]][0] is not None \
                    and grid[r][mapping[k + 1]][0] == grid[r][mapping[j]][0]:
                k += 1
            runs.append(k - j + 1)
            j = k + 1
        key = tuple(runs)
        shapes[key] += 1
        examples.setdefault(key, md_no[i])
    rec["row_shapes"] = [{"runs": list(k), "count": v, "example_line": examples[k]} for k, v in shapes.items()]
    return rec, {"rows": rows, "grid": grid, "kept": kept, "mapping": mapping, "md_no": md_no, "top": top}


# ---------------------------------------------------------------- 나. 청크

def ex2_expected(snap, info, md_file):
    """예외 2의 기대 행: 원문 첫 열 칸의 <p> 조각(네 가지)과 마크다운의 나머지 칸."""
    out, problems = {}, []
    for i, r in enumerate(info["kept"][1:], start=1):
        line = info["md_no"][i]
        cid = info["grid"][r][info["mapping"][0]][0]
        cell = next(c for tr in info["rows"] for c in own_cells(tr) if id_of(info, c) == cid)
        # 첫 조각(제조사)은 <p> 밖에서 칸을 여는 글자이고, 나머지는 <p>마다 하나다
        lead = []
        for ch in cell.children:
            if getattr(ch, "name", None) == "p":
                break
            lead.append(ch)
        frags = [build.inline(lead)] + [build.inline(p) for p in cell.find_all("p", recursive=False)]
        frags = [f for f in frags if f]
        first = md_cells(md_file[line - 1])[0]
        if " ".join(frags) != first:
            problems.append(f"{line}줄: 원문 조각 {frags}을 이은 글이 마크다운 첫 칸 {first!r}와 다르다")
        out[line] = {"frags": frags, "rest": md_cells(md_file[line - 1])[1:]}
    return out, problems


def id_of(info, cell):
    # expand가 매긴 번호를 칸에서 다시 얻는다: 줄과 칸 순서로 센다
    if "_ids" not in info:
        ids, n = {}, 0
        for tr in info["rows"]:
            for c in own_cells(tr):
                n += 1
                ids[id(c)] = n
        info["_ids"] = ids
    return info["_ids"][id(cell)]


def main():
    docs = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
    collected = {c["doc_id"]: c for c in yaml.safe_load((CORPUS / "collected.yaml").read_text(encoding="utf-8"))["documents"]}
    md = {}
    tables = {}      # (doc_id, 시작 줄) -> 표 정보
    infos = {}
    out_lines = []
    for d in docs:
        did = d["doc_id"]
        md_bytes = (CORPUS / "markdown" / f"{did}.md").read_bytes()
        lines = md_bytes.decode("utf-8").split("\n")
        md[did] = lines
        raw = (CORPUS / collected[did]["raw_file"]).read_bytes()
        text, calls = traced(d, raw)
        if text.encode("utf-8") != md_bytes:
            sys.exit(f"{did}: 다시 만든 글이 마크다운 파일과 다르다")
        groups = md_groups(lines)
        occ = Counter()
        found = set()
        for snap, result in calls:
            idx = next((i for i, it in enumerate(result) if it[0] == "b" and it[1] and it[1][0].startswith("| ")), None)
            if idx is None:
                continue
            key = tuple(result[idx][1])
            starts = [s for s, g in groups if tuple(g) == key]
            k = occ[key]
            occ[key] += 1
            if k >= len(starts):
                continue  # 변환 뒤 정리(prune)에서 빠져 마크다운에 없는 표. 마크다운 표가 모두 짝지어졌는지는 아래에서 본다
            start = starts[k]
            rec, info = check_table(snap, start, list(key))
            above = [l for it in result[:idx] if it[0] == "b" for l in it[1]]
            rec.update({"doc_id": did, "md_line": start, "md_end": start + len(key) - 1, "caption_line": None})
            if above:  # 표 제목(caption)은 변환이 표 바로 위에 한 줄로 적는다
                cap = above[-1]
                rec["caption_line"] = next(i for i in range(start - 1, 0, -1) if lines[i - 1] == cap)
            tables[(did, start)] = rec
            infos[(did, start)] = (snap, info)
            found.add(start)
        missing = [s for s, _ in groups if s not in found]
        if missing:
            sys.exit(f"{did}: 원문 표와 짝짓지 못한 마크다운 표 {missing}")

    # 표 제목과 머리글 줄 수를 2단계 조사(tables.json)와 견준다
    survey = json.loads((ROOT / "research_notes/stage2_table_shapes_rare_earth/tables.json").read_text(encoding="utf-8"))
    for s in survey:
        if not s["md_line_no"]:
            continue
        rec = tables[(s["doc_id"], s["md_line_no"])]
        if rec.get("header_rows") is not None and rec["header_rows"] != s["top_th_rows"]:
            rec["problems"].append(f"머리글 줄 수 {rec['header_rows']}가 2단계 조사 {s['top_th_rows']}와 다르다")
        if bool(s["caption"]) != (rec["caption_line"] is not None):
            rec["problems"].append("표 제목 유무가 2단계 조사와 다르다")

    # 정보 상자 구간(3줄부터 목록 줄·표 줄·빈 줄이 이어지는 곳)과, 그 안의 표마다 묶음 이름 줄·표 이름 줄
    # (표 이름 줄: 빈 줄 하나 건너 바로 아래 표가 오는 항목 줄. decisions/stage4.md 2026-10-23 "표 이름" 줄)
    box_end = {}
    for did, lines in md.items():
        i = 3
        while i <= len(lines) and (lines[i - 1] == "" or lines[i - 1].startswith(("- ", "  - ", "|"))):
            i += 1
        box_end[did] = i - 1
    for (did, start), rec in tables.items():
        lines = md[did]
        rec["header_lines"] = [start, start + 1] + list(range(start + 2, start + 1 + (rec.get("header_rows") or 1)))
        rec["name_line"] = rec["group_line"] = None
        up = start - 2  # 표 바로 위 빈 줄의 위 줄(1부터)
        if start <= box_end[did] and up >= 1 and lines[start - 2] == "":
            l = lines[up - 1]
            if l.startswith("  - "):
                rec["name_line"] = up
                rec["group_line"] = next(i for i in range(up - 1, 0, -1) if lines[i - 1].startswith("- "))
            elif l.startswith("- "):
                rec["group_line"] = up

    # 예외 2의 기대값
    ex2_snap, ex2_info = infos[EX2]
    ex2_rows, ex2_problems = ex2_expected(ex2_snap, ex2_info, md[EX2[0]])
    tables[EX2]["problems"] += ex2_problems
    tables[EX2]["ex2_frags"] = {str(k): v["frags"] for k, v in ex2_rows.items()}

    # 예외 1의 기대값: 마크다운 표의 이름을 왼쪽 열부터 위에서 아래로
    ex1 = tables[EX1]
    ex1_rows = [ex1["md_line"]] + list(range(ex1["md_line"] + 2, ex1["md_end"] + 1))
    ex1_names = [(l, md_cells(md[EX1[0]][l - 1])[j]) for j in range(2) for l in ex1_rows]
    ex1_names = [(l, n) for l, n in ex1_names if n]

    verdicts = []
    counts = {}
    for name in SETS:
        chunks = [json.loads(l) for l in (CHUNKS / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
        seen_rows = defaultdict(Counter)   # 표 -> 행 줄 -> 든 청크 수
        ex1_seq = []
        n_checked = n_bad = 0
        for c in chunks:
            did, ls = c["doc_id"], set(c["lines"])
            touched = [k for k in tables if k[0] == did and any(tables[k]["md_line"] <= l <= tables[k]["md_end"] for l in ls)]
            if not touched:
                continue
            n_checked += 1
            text = c["text"].split("\n")
            problems = []
            if c["title"]:
                if text[0] != c["path"]:
                    problems.append("맨 윗줄이 붙인 제목이 아니다")
                body = text[1:]
            else:
                body = text
            src = md[did]
            for key in touched:
                t = tables[key]
                rows_in = sorted(l for l in ls if t["md_line"] <= l <= t["md_end"] and l not in t["header_lines"])
                for l in rows_in:
                    seen_rows[key][l] += 1
                if key == EX1:
                    # 한 원문 줄에 이름이 둘이라 조각이 나뉘면 한 줄이 두 조각에 걸칠 수 있다. 빠짐·겹침은 이름 순서로 본다
                    if body[0] != src[t["caption_line"] - 1]:
                        problems.append("예외 1 조각이 표 제목으로 시작하지 않는다")
                    if not {t["caption_line"], t["md_line"], t["md_line"] + 1} <= ls:
                        problems.append("예외 1 조각의 줄 목록에 표 제목·머리글·구분 줄이 없다")
                    line_of = dict((n, l) for l, n in ex1_names)
                    for n in body[1:]:
                        if n not in line_of:
                            problems.append(f"예외 1 조각에 원문 표에 없는 이름 {n!r}")
                        elif line_of[n] not in ls:
                            problems.append(f"예외 1 조각의 이름 {n!r}이 나온 {line_of[n]}줄이 줄 목록에 없다")
                    ex1_seq += body[1:]
                    continue
                missing_head = [l for l in t["header_lines"] if l not in ls]
                if missing_head:
                    problems.append(f"표 {key[1]}: 머리글 줄 {missing_head}이 줄 목록에 없다")
                if key == EX2:
                    head = md_cells(src[t["md_line"] - 1])
                    want = ["| " + " | ".join(EX2_HEAD + head[1:]) + " |", "|" + "---|" * (len(head) + 3)]
                    for l in rows_in:
                        e = ex2_rows[l]
                        # 세 조각인 줄은 제품 칸이 빈 것으로 기대한다(None. 아래에서 따로 판정. 어느 조각이 빠졌는지는 원문을 읽어 확인한다)
                        want.append(build.md_row(e["frags"] + e["rest"]) if len(e["frags"]) == 4 else None)
                    i = next((i for i, x in enumerate(body) if x == want[0]), None)
                    if i is None:
                        problems.append("예외 2: 네 열로 나눈 머리글이 없다")
                        continue
                    for k, w in enumerate(want):
                        got = body[i + k] if i + k < len(body) else None
                        if w is None:
                            fr = ex2_rows[rows_in[k - 2]]["frags"]
                            gc = md_cells(got) if got else []
                            ok = (len(gc) == 7 and gc[1] == "" and [gc[0], gc[2], gc[3]] == fr
                                  and gc[4:] == ex2_rows[rows_in[k - 2]]["rest"])
                            if not ok:
                                problems.append(f"예외 2 {rows_in[k - 2]}줄: 세 조각 줄이 기대(제품 칸만 빔)와 다르다: {got!r}")
                        elif got != w:
                            problems.append(f"예외 2 {(rows_in[k - 2] if k >= 2 else '머리글')}: 기대 {w!r}, 실제 {got!r}")
                    continue
                block = [src[l - 1].rstrip() for l in t["header_lines"]] + [src[l - 1].rstrip() for l in rows_in]
                i = next((i for i in range(len(body)) if body[i:i + len(block)] == block), None)
                if i is None:
                    problems.append(f"표 {key[1]}: 머리글 + 행이 원문 그대로 이어진 덩어리가 청크 글에 없다")
                else:
                    before = body[i - 1] if i > 0 else None
                    for what in ("caption_line", "name_line"):
                        if t[what]:
                            if t[what] not in ls:
                                problems.append(f"표 {key[1]}: {what} {t[what]}줄이 줄 목록에 없다")
                            if before != src[t[what] - 1].rstrip():
                                problems.append(f"표 {key[1]}: 머리글 바로 위가 {what}이 아니다: {before!r}")
                    if t["group_line"] and not t["name_line"] and before != src[t["group_line"] - 1].rstrip():
                        problems.append(f"표 {key[1]}: 머리글 바로 위가 묶음 이름 줄이 아니다: {before!r}")
                    after = body[i + len(block)] if i + len(block) < len(body) else None
                    if after is not None and after.startswith("|"):
                        problems.append(f"표 {key[1]}: 덩어리 뒤에 다른 표 줄이 붙어 있다")
                n0 = len(md_cells(src[t["md_line"] - 1]))
                wrong = [l for l in t["header_lines"] + rows_in if len(md_cells(src[l - 1])) != n0]
                if wrong:
                    problems.append(f"표 {key[1]}: 칸 수가 머리글과 다른 줄 {wrong}")
                if t["problems"]:
                    problems.append(f"표 {key[1]}: 변환 확인에서 문제 {len(t['problems'])}개")
            if c["kind"] == "infobox":
                g = next((tables[k]["group_line"] for k in touched if tables[k]["group_line"]), None)
                if g is None or body[0] != src[g - 1] or g not in ls:
                    problems.append("정보 상자 청크가 그 표의 묶음 이름 줄로 시작하지 않는다")
            verdict = "맞음" if not problems else "틀림"
            n_bad += bool(problems)
            verdicts.append({"set": name, "chunk_id": c["chunk_id"], "doc_id": did, "kind": c["kind"],
                             "tables": [k[1] for k in touched], "rows": sorted(l for k in touched for l in ls
                                                                           if tables[k]["md_line"] <= l <= tables[k]["md_end"]
                                                                           and l not in tables[k]["header_lines"]),
                             "verdict": verdict, "problems": problems})
        # 묶음 전체: 표의 행이 정확히 한 청크에 드는가
        part = []
        for key, t in tables.items():
            if key == EX1:
                continue  # 이름 순서로 따로 본다(아래)
            want = [l for l in range(t["md_line"], t["md_end"] + 1) if l not in t["header_lines"]]
            bad = [l for l in want if seen_rows[key][l] != 1]
            if bad:
                part.append(f"{key[0]}:{key[1]} 행 {bad[:10]}의 든 청크 수 {[seen_rows[key][l] for l in bad[:10]]}")
        if ex1_seq != [n for _, n in ex1_names]:
            part.append(f"예외 1 이름 순서가 기대와 다르다: {ex1_seq[:5]} …")
        counts[name] = {"checked": n_checked, "bad": n_bad, "partition_problems": part}

    (HERE / "verdicts.jsonl").write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in verdicts), encoding="utf-8")
    (HERE / "tables.json").write_text(json.dumps(
        [dict(v, key=f"{k[0]}:{k[1]}") for k, v in sorted(tables.items())], ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    out = ["가. 변환(마크다운 표 37개와 원문 HTML)"]
    for k, t in sorted(tables.items()):
        shapes = ", ".join(f"{'·'.join(map(str, s['runs'])) if any(x > 1 for x in s['runs']) else '보통'} {s['count']}"
                           for s in t.get("row_shapes", []))
        out.append(f"{k[0]}:{k[1]}  원문 {t['html_rows']}줄×{t['html_cols']}열 → 마크다운 {t['md_rows']}줄×{t['md_cols']}열, "
                   f"머리글 {t.get('header_rows')}줄, 뺀 열 {t.get('dropped')}, 행 모양 [{shapes}], "
                   f"문제 {t['problems'] or '없음'}")
    out.append("")
    out.append("나. 청크")
    for name in SETS:
        cnt = counts[name]
        out.append(f"{name}: 표가 든 청크 {cnt['checked']}, 틀림 {cnt['bad']}, 행 빠짐·겹침 {cnt['partition_problems'] or '없음'}")
    (HERE / "output.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
