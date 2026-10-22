"""받아 둔 원본에서 마크다운을 만드는 프로그램.

  uv run python src/corpus/build.py                       원본이 있는 문서를 모두 바꾼다
  uv run python src/corpus/build.py --only <doc_id> ...   그 문서만 바꾼다

collected.yaml의 raw_file(data/corpus/raw/)을 읽어 data/corpus/markdown/<doc_id>.md를 쓰고,
마크다운의 해시를 data/corpus/collected.yaml에 적는다. 인터넷과 시계를 쓰지 않는다.
같은 원본에서는 항상 글자 하나까지 같은 마크다운이 나온다.
documents.yaml에 converter_commit이 있으면 코퍼스가 그 커밋의 변환에 묶인 것이다. 만들기는 아무것도 쓰지 않고
알리며 끝나고(종료 코드 1), --verify는 그 커밋의 build.py로 검사한다.
규칙은 decisions/stage2.md의 2026-10-14 줄(남기는 것과 지우는 것 / 표를 옮기는 규칙 / 제목)에 있다.
위첨자와 수식은 decisions/stage2.md 2026-10-21 '세는 규칙 보완: 변환의 적는 방식과 세는 범위' 줄에 있다.
doc_id 앞머리(wiki, kto, portal)마다 바꾸는 함수가 CONVERT에 있다.
"""
import argparse, csv, hashlib, html, io, json, re, subprocess, sys, tempfile
from pathlib import Path

import yaml
from bs4 import BeautifulSoup, Comment, NavigableString

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
RAW = CORPUS / "raw"
MARKDOWN = CORPUS / "markdown"
DOCS = CORPUS / "documents.yaml"
COLLECTED = CORPUS / "collected.yaml"
HEADER = "# 수집 기록. src/corpus/fetch.py가 원본을 받을 때 쓴다. 마크다운의 해시는 src/corpus/build.py가 채운다.\n"

# 이름으로 지우는 절. 다른 이름을 더하지 않는다(영어 문서의 Notable people 등은 글이 있어 남는다).
DROP_SECTIONS = {"같이 보기", "외부 링크", "각주", "내용주", "참고 문헌",
                 "See also", "External links", "References", "Notes"}

# 통째로 지우는 요소. 이미지, 각주, 다른 곳으로 가는 길, 편집자용 표시.
DROP_SELECTORS = [
    "img", "figure", ".thumb", ".gallery", ".mod-gallery", ".thumbcaption", "figcaption",
    ".mw-kartographer-map", ".ext-phonos",
    "sup.reference", ".reflist", "ol.references", ".mw-references-wrap",
    ".hatnote", ".navbox", ".navbox-styles", ".sistersitebox", ".side-box", ".authority-control",
    ".portalbox", ".catlinks",
    ".mw-editsection", "sup.noprint", "span.noprint", "sup.Inline-Template", ".ambox", "a.autonumber",
    ".infobox-below", ".infobox .navbar",
    "style", "script", "link", "meta",
    ".geo-nondefault", ".geo-multi-punct", ".geo-inline-hidden",
]
DISPLAY_NONE = re.compile(r"display\s*:\s*none", re.I)
ROAD_SIGN = re.compile(r"/(Korean_(?:Highway|National_Route|Local_Route)[^/]*)")
FOLD_NOTICE = "이 글을 보려면 오른쪽 ‘펼치기’ 버튼 클릭"  # 접힌 상자를 여는 안내문. 본문이 아니다.
INFOBOX_SKIP_LABELS = {"웹사이트", "Website"}
SWATCH = re.compile(r"color\s*:\s*transparent")  # 주기율표 그림의 원소 한 칸: 링크 안에 글자색이 투명한 span이 든다
PERIODIC_TABLE_MIN = 100  # 원소는 118개다. 줄 하나에 투명한 칸이 이만큼 이상이면 주기율표 그림이다.

# 위첨자 글자. 여기 없는 글자(한글, †, 점 등)는 그대로 둔다.
SUPERSCRIPT = str.maketrans(
    "0123456789+-\u2212=()"
    "abcdefghijklmnoprstuvwxyz"
    "ABDEGHIJKLMNOPRTUVW",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁼⁽⁾"
    "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ"
    "ᴬᴮᴰᴱᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᴿᵀᵁⱽᵂ")

BLOCK = {"p", "div", "li", "dt", "dd", "dl", "ul", "ol", "tr", "td", "th", "table", "caption",
         "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"}


def norm(s):
    """공백(줄바꿈, 띄어쓰기 없는 공백 포함)을 하나로 줄이고 앞뒤를 자른다."""
    return re.sub(r"\s+", " ", s).strip()


def inline(nodes):
    """노드(또는 노드 목록)의 글자. <br>과 칸 안의 문단은 빈칸 하나로, 목록은 ', '로 잇는다. (값 칸의 <br>은 prepare가 먼저 ' / '로 바꿔 둔다.)"""
    if not isinstance(nodes, list):
        nodes = [nodes]
    parts = []

    def rec(n, up=False):
        if isinstance(n, NavigableString):
            parts.append(str(n).translate(SUPERSCRIPT) if up else str(n))
        elif n.name == "br":
            parts.append(" ")
        elif n.name in ("ul", "ol"):
            items = [inline(li) for li in n.find_all("li", recursive=False)]
            parts.append(" " + ", ".join(i for i in items if i) + " ")
        elif n.name in BLOCK:
            parts.append(" ")
            for c in n.children:
                rec(c, up)
            parts.append(" ")
        else:
            for c in n.children:
                rec(c, up or n.name == "sup")

    for n in nodes:
        rec(n)
    return norm("".join(parts))


# ---------------------------------------------------------------- 지우기

def tex_of(el):
    """수식 요소의 TeX 글. <math>의 alttext, 없으면 수식 그림의 alt. 글 전체가 {\\displaystyle …}이면 껍데기만 벗긴다. 못 찾으면 None."""
    math = el.find("math")
    tex = math.get("alttext") if math else None
    if not tex:
        img = el.find("img", class_=lambda c: c and c.startswith("mwe-math-fallback-image"))
        tex = img.get("alt") if img else None
    if not tex:
        return None
    if tex.startswith("{\\displaystyle") and tex.endswith("}"):
        depth = 0
        for i, ch in enumerate(tex):
            if i and tex[i - 1] == "\\":  # \{ 와 \} 는 짝을 이루는 괄호가 아니다
                continue
            depth += (ch == "{") - (ch == "}")
            if depth == 0:
                break
        if i == len(tex) - 1:  # 첫 {가 마지막 }에서 닫힐 때만 전체를 감싼 껍데기다
            tex = tex[len("{\\displaystyle"):-1]
            tex = tex[1:] if tex.startswith(" ") else tex  # 껍데기의 띄어쓰기 하나만 벗긴다
    return tex


def prepare(root):
    """HTML 나무에서 지울 것을 지우고, 그 자리에 남길 글자(도로 표지, 원그래프, 수식의 TeX 글)를 넣는다."""
    for c in root.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
    # 수식: display:none 지우기와 이미지 지우기에서 사라지기 전에 TeX 글로 바꾼다. TeX 글이 없으면 지워지게 둔다.
    for el in root.find_all(class_="mwe-math-element"):
        tex = tex_of(el)
        if tex:
            block = "mwe-math-element-block" in el.get("class", [])
            el.replace_with(NavigableString(f"\\[{tex}\\]" if block else f"\\({tex}\\)"))
    # 도로 표지: 그림을 지우고 그 자리에 대체 글자를 넣는다. 다른 이미지의 대체 글자는 넣지 않는다.
    for img in root.find_all("img"):
        if ROAD_SIGN.search(img.get("src", "")) and img.get("alt"):
            img.replace_with(NavigableString(img["alt"]))
    for el in root.select(".mw-collapsible > div"):
        if norm(el.get_text()) == FOLD_NOTICE:
            el.decompose()
    for el in root.find_all(style=DISPLAY_NONE):
        el.decompose()
    # 원그래프: 원은 지우고 제목 한 줄과 범례의 값 줄만 남긴다. .thumb 안에 있어 먼저 꺼낸다.
    for pie in root.select(".smooth-pie-container"):
        box = pie.find_parent(class_="thumb") or pie
        new = root.new_tag("div")
        caption = pie.select_one(".smooth-pie-caption")
        if caption:
            p = root.new_tag("p")
            p.extend(list(caption.children))
            new.append(p)
        legend = root.new_tag("ul")
        for label in pie.select(".smooth-pie-legend .l-label"):
            li = root.new_tag("li")
            li.extend(list(label.children))
            legend.append(li)
        new.append(legend)
        box.replace_with(new)
    # 화학식 틀(.chemf): 위첨자와 아래첨자를 위아래로 쌓느라 사이에 <br>이 든다. 빈칸이 되면 La2O3이 'La 2O 3'으로 끊기므로 값 칸 규칙보다 먼저 없앤다.
    for br in root.select(".chemf br"):
        br.decompose()
    split_value_breaks(root)


def only_parens(text):
    """글이 통째로 괄호 묶음뿐인가. 예: '(실온) (poly)'."""
    return bool(re.fullmatch(r"(\([^()]*\)\s*)+", text))


def split_value_breaks(root):
    """값 칸(td)의 <br>을 ' / '로 바꾼다. <br>이 서로 다른 두 값을 가르는데 빈칸이면 한 값으로 읽히기 때문이다(0.48 0.38D).
    가장 가까운 칸이 th(머리글 칸)이면 그대로 둔다. <br> 바로 앞이나 뒤 조각이 통째로 괄호면 값이 아니라 조건·설명을 떼는 줄바꿈이라 빈칸으로 둔다."""
    swaps = []
    for br in root.find_all("br"):
        cell = br.find_parent(["th", "td"])
        if cell is None or cell.name == "th":
            continue
        before, after = [], []
        for s in br.previous_siblings:
            if getattr(s, "name", None) == "br":
                break
            before.insert(0, s)
        for s in br.next_siblings:
            if getattr(s, "name", None) == "br":
                break
            after.append(s)
        swaps.append((br, " " if only_parens(inline(before)) or only_parens(inline(after)) else " / "))
    for br, text in swaps:  # 조각 글자는 <br>이 그대로일 때 재야 하므로 다 잰 뒤에 바꾼다
        br.replace_with(NavigableString(text))


def drop_all(root):
    for sel in DROP_SELECTORS:
        for el in root.select(sel):
            el.decompose()


# ---------------------------------------------------------------- 정보 상자

def own_rows(table):
    """겹친 표의 줄을 빼고 이 표의 줄만."""
    return [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]


def own_cells(tr):
    return tr.find_all(["th", "td"], recursive=False)


def mark_infobox(root):
    """문서 맨 위의 정보 상자 하나를 찾아 이미지가 든 줄과 주기율표 그림 줄을 지우고 돌려준다. 나머지 infobox 표는 지운다.

    칸이 둘(이름표 th, 값 td)인 줄의 이미지는 값 옆의 장식이라 줄은 두고 이미지만 지운다(뒤의 drop_all).
    그 밖의 모양의 줄에 든 글자는 이미지의 설명이므로 줄째로 지운다. 이 일은
    이미지를 지우기 전에 해야 한다. 국기 아이콘(.flagicon)은 장식이라 줄을 지우는 근거로 쓰지 않는다.

    주기율표 그림 줄은 한국어와 영어 상자에 모두 있고 원소 118개를 작은 링크로 이은 격자다. 화면에는 색 칸이지만
    글로는 원소 이름이 이어져 읽을 수 없다. 클래스 이름은 두 언어가 달라서(영어만 periodic-table-32-micro) 쓰지 않고,
    줄 하나 안에 글자색이 투명한 span(원소 한 칸)이 PERIODIC_TABLE_MIN개 이상 든 줄을 지운다. 묶음 제목과 다른 줄은 둔다.
    """
    top = root.find("table", class_="infobox", recursive=False)
    for t in root.find_all("table", class_="infobox"):
        if t is not top:
            t.decompose()
    for tr in own_rows(top):
        for fl in tr.select(".flagicon"):
            fl.decompose()
        cells = own_cells(tr)
        is_row = len(cells) == 2 and cells[0].name == "th" and cells[1].name == "td"
        if not is_row and tr.select("img, figure, .mw-kartographer-map"):
            tr.decompose()
        elif len(tr.find_all("span", style=SWATCH)) >= PERIODIC_TABLE_MIN:
            tr.decompose()
    return top


def infobox_lines(box):
    """정보 상자에서 글자로 된 줄을 '- ...'로 뽑는다.

    웹사이트 줄만 화면의 글자 대신 바깥 링크의 주소를 값으로 적는다(링크가 없으면 화면의 글자).
    묶음 제목(th.infobox-header)에 딸린 줄은 두 칸 들여 쓴다. 딸린 줄은 이렇게 정한다.
      - 제목 바로 다음 줄의 이름표가 '•'로 시작하면(영어): '•'로 시작하는 줄이 이어지는 동안.
      - 아니면(한국어 상자, 영어의 Korean name 상자): 다음 묶음 제목이나 상자의 끝까지.
    딸린 줄 앞의 '•'는 뺀다. 딸린 줄이 하나도 없는 묶음 제목은 지운다.
    줄의 칸에 자료 표(증기 압력, 주요 동위원소)가 들어 있으면 표는 마크다운 표로 그 자리에 둔다(cell_parts).
    표 앞에 칸의 글자(표의 이름)가 있으면 그 글자가 목록 줄이 되고, 목록은 빈 줄로 끊겼다가 표 뒤에서 이어진다.
    """
    entries = []  # (종류: head/row/text/table, 이름표가 •로 시작하는가, 글자 또는 table의 조각들)
    for tr in own_rows(box):
        cells = own_cells(tr)
        if any(data_tables(c) for c in cells):
            entries.append(("table", False, [p for c in cells for p in cell_parts(c)]))
            continue
        texts = [inline(c) for c in cells]
        if len(cells) == 2 and cells[0].name == "th" and cells[1].name == "td":
            value = texts[1]
            if texts[0] in INFOBOX_SKIP_LABELS:
                link = cells[1].find("a", class_="external")
                if link and link.get("href"):
                    value = link["href"].strip()
            if not value:
                continue
            bullet = texts[0].startswith("•")
            label = re.sub(r"^•\s*", "", texts[0])
            entries.append(("row", bullet, f"{label}: {value}" if label else value))
        else:
            text = norm(" ".join(t for t in texts if t))
            if text:
                head = len(cells) == 1 and cells[0].name == "th" and "infobox-header" in cells[0].get("class", [])
                entries.append(("head" if head else "text", False, text))
    lines, i = [], 0
    while i < len(entries):
        kind, _, text = entries[i]
        if kind != "head":
            lines += entry_lines(entries[i], "")
            i += 1
            continue
        j = i + 1
        if j < len(entries) and entries[j][0] == "row" and entries[j][1]:
            while j < len(entries) and entries[j][0] == "row" and entries[j][1]:
                j += 1
        else:
            while j < len(entries) and entries[j][0] != "head":
                j += 1
        if j > i + 1:
            lines.append(f"- {text}")
            for e in entries[i + 1:j]:
                lines += entry_lines(e, "  ")
        i = j
    while lines and not lines[-1]:  # 표 앞뒤의 빈 줄이 맨 앞이나 맨 끝에 남으면 뺀다
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return lines


def data_tables(cell):
    """칸 안의 자료 표: 겹친 표 가운데 가장 바깥의 것. 한 줄짜리 배치용 표(table.infobox-subbox)는 자료 표가 아니다."""
    tables = []
    for t in cell.find_all("table"):
        outer = t.find_parent("table")
        if "infobox-subbox" not in t.get("class", []) and not (outer is not None and cell in outer.parents):
            tables.append(t)
    return tables


def cell_parts(cell):
    """칸을 차례대로 읽어 [('text', 글자) 또는 ('table', 표의 항목들)]로. 자료 표는 table_items로 바꾼다.

    표 자리에 표시 글자를 넣고 칸의 글자를 읽은 뒤 표시 글자에서 잘라, 표 앞뒤의 글자(표의 이름)가 제자리에 남게 한다.
    """
    marks = [(t, table_items(t)) for t in data_tables(cell)]
    for n, (t, _) in enumerate(marks):
        t.replace_with(NavigableString(f"\ue000{n}\ue000"))
    parts = []
    for k, piece in enumerate(re.split("\ue000(\\d+)\ue000", inline(cell))):
        if k % 2:
            parts.append(("table", marks[int(piece)][1]))
        elif norm(piece):
            parts.append(("text", norm(piece)))
    return parts


def entry_lines(entry, indent):
    """정보 상자 항목 하나의 줄. 표는 앞뒤를 빈 줄로 띄운다(마크다운은 목록 안에 표를 둘 수 없다)."""
    kind, _, text = entry
    if kind != "table":
        return [f"{indent}- {text}"]
    lines = []
    for k, piece in text:
        if k == "text":
            lines.append(f"{indent}- {piece}")
        else:
            for it in piece:
                lines += ["", *it[1], ""] if it[0] == "b" else []
    return lines


# ---------------------------------------------------------------- 표

def grid_of(table):
    """칸을 합친 표를 폈을 때의 (칸 글자 격자, 줄마다 모두 th인지, 줄의 원래 칸 글자, 줄의 원래 colspan, 칸의 출처, th에서 나온 칸).

    th에서 나온 칸: 칸마다 th에서 나왔는지의 격자. 줄이 짧아 채운 빈 자리는 th가 아니다.
    """
    cells, origin, from_th = {}, {}, {}
    all_th, row_texts, row_spans = [], [], []
    rows = own_rows(table)
    for r, tr in enumerate(rows):
        c = 0
        row_cells = own_cells(tr)
        all_th.append(bool(row_cells) and all(x.name == "th" for x in row_cells))
        row_texts.append([inline(x) for x in row_cells])
        row_spans.append([span(x, "colspan") for x in row_cells])
        for cell in row_cells:
            while (r, c) in cells:
                c += 1
            text = inline(cell)
            rs, cs = span(cell, "rowspan"), span(cell, "colspan")
            for dr in range(rs):
                for dc in range(cs):
                    cells.setdefault((r + dr, c + dc), text)
                    origin.setdefault((r + dr, c + dc), id(cell))
                    from_th.setdefault((r + dr, c + dc), cell.name == "th")
            c += cs
    nrows = len(rows)
    ncols = max((c for _, c in cells), default=-1) + 1
    grid = [[cells.get((r, c), "") for c in range(ncols)] for r in range(nrows)]
    # 칸이 어느 원래 칸에서 나왔는지. 줄이 짧아 채운 빈 자리는 왼쪽 칸에서 나온 것으로 본다. 원래 칸이 없는 줄은 None.
    src = []
    for r in range(nrows):
        row, last = [], None
        for c in range(ncols):
            last = origin.get((r, c), last)
            row.append(last)
        src.append(row if own_cells(rows[r]) else None)
    th_grid = [[from_th.get((r, c), False) for c in range(ncols)] for r in range(nrows)]
    return grid, all_th, row_texts, row_spans, src, th_grid


def span(cell, attr):
    v = cell.get(attr, "")
    return int(v) if v.isdigit() and int(v) > 0 else 1


def is_frame(table):
    """틀로만 쓰인 표인가: 표 안에 표가 있거나, th가 없고 칸 안에 목록이나 작은 제목이 든 표."""
    if table.find("table"):
        return True
    cells = [c for tr in own_rows(table) for c in own_cells(tr)]
    if any(c.name == "th" for c in cells):
        return False
    return any(c.find(["ul", "ol", "h3", "h4", "h5"]) for c in cells)


def esc(s):
    return s.replace("|", "\\|")


def md_row(cells):
    return "| " + " | ".join(esc(c) for c in cells) + " |"


def table_items(table):
    """표 하나를 항목(제목, 글 덩어리)으로 바꾼다."""
    out = []
    if is_frame(table):
        # 틀을 푼다: 칸의 내용을 왼쪽 칸부터 위에서 아래로. th 줄은 아래 칸의 이름으로 그 칸 내용 바로 위에 한 줄로 적는다.
        heads, shown = {}, set()
        for tr in own_rows(table):
            cells = own_cells(tr)
            col = 0
            only_th = bool(cells) and all(c.name == "th" for c in cells)
            for cell in cells:
                span_c = span(cell, "colspan")
                if only_th:
                    heads[col] = (id(cell), inline(cell))
                else:
                    if cell.name == "th":
                        text = inline(cell)
                        if text:
                            out.append(("b", [text]))
                    else:
                        h = heads.get(col)
                        if h and h[1] and h[0] not in shown:
                            shown.add(h[0])
                            out.append(("b", [h[1]]))
                        walk(cell, out)
                col += span_c
        return out

    grid, all_th, row_texts, row_spans, src, th_grid = grid_of(table)
    if not grid:
        return out
    caption = table.find("caption")
    if caption and inline(caption):
        out.append(("b", [inline(caption)]))
    # 표 전체에 걸친 한 칸짜리 줄은 표 밖으로 뺀다. 머리글보다 앞에 있으면 표 위에, 뒤에 있으면 표 바로 아래에
    # 한 줄씩 적는다. 머리글은 그 뒤의 첫 줄이다(머리글이 아예 없는 표이면 첫 줄이 머리글 자리다).
    ncols = len(grid[0])
    full = [len(sp) == 1 and sp[0] > 1 and sp[0] >= ncols for sp in row_spans]
    lead = 0
    while lead < len(grid) and full[lead]:
        if row_texts[lead][0]:
            out.append(("b", [row_texts[lead][0]]))
        lead += 1
    if lead >= len(grid) or not any(any(r) for r in grid):
        return out
    below = [("b", [row_texts[i][0]]) for i in range(lead, len(grid)) if full[i] and row_texts[i][0]]
    # 자기 칸이 모두 아래 줄로 걸친(rowspan>1) 줄은 표에서 뺀다. 그 칸의 글자는 걸친 아래 줄마다 이미 되풀이되어 있어
    # 잃는 것이 없고, 두면 칸이 빈 줄이 따로 남는다. 빼고 나면 다음 줄이 첫 줄(머리글 자리)이 된다.
    own_rs = [[span(c, "rowspan") for c in own_cells(tr)] for tr in own_rows(table)]
    spanned = [bool(rs) and all(n > 1 for n in rs) for rs in own_rs]
    rows = [i for i in range(lead, len(grid)) if not full[i] and not spanned[i]]
    if not rows:
        return out + below
    # 이웃한 두 열이 모든 줄에서 같은 원래 칸에서 나왔으면(가로로 합친 칸을 편 것) 하나로 합친다.
    cols = [0]
    for c in range(1, ncols):
        if not all(src[i] is None or src[i][c] == src[i][c - 1] for i in rows):
            cols.append(c)
    head, body = [grid[rows[0]][c] for c in cols], [[grid[i][c] for c in cols] for i in rows[1:]]
    # 값 칸(td)이 모두 빈 열은 머리글까지 지운다. th는 머리글로 보고 값으로 세지 않는다(머리글 줄을 아래로 되풀이한 칸이
    # 글자를 가져도 값이 아니다). 첫 줄이 머리글(th)이 아닌 표는 첫 줄도 내용 줄이므로 값 칸에 넣는다(마크다운
    # 머리글 자리에는 그대로 첫 줄을 쓴다). 값 칸이 아예 없는 열(줄 이름표 열, 머리글 줄밖에 없는 표)은 칸에 글자가
    # 있으면 남긴다.
    check = rows[1:] if all_th[rows[0]] else rows

    def keep_col(k):
        values = [grid[i][cols[k]] for i in check if not th_grid[i][cols[k]]]
        return any(values) if values else bool(head[k] or any(r[k] for r in body))

    keep = [k for k in range(len(head)) if keep_col(k)]
    head, body = [head[c] for c in keep], [[r[c] for c in keep] for r in body]
    if not head:
        return out + below
    lines = [md_row(head), "|" + "---|" * len(head)] + [md_row(r) for r in body]
    out.append(("b", lines))
    return out + below


# ---------------------------------------------------------------- 본문

def list_lines(lst, depth=0):
    lines, n = [], 0
    for li in lst.children:
        if isinstance(li, NavigableString):
            continue
        if li.name in ("ul", "ol"):
            lines += list_lines(li, depth + 1)
            continue
        if li.name != "li":
            continue
        own = [c for c in li.children if not (not isinstance(c, NavigableString) and c.name in ("ul", "ol"))]
        text = inline(own)
        if text:
            n += 1
            mark = f"{n}. " if lst.name == "ol" else "- "
            lines.append("  " * depth + mark + text)
        for sub in li.find_all(["ul", "ol"], recursive=False):
            lines += list_lines(sub, depth + 1)
    return lines


def walk(node, out):
    """node의 자식을 차례로 읽어 항목을 out에 더한다. 항목: ('h', 높이, 글자) 또는 ('b', [줄...])."""
    buf = []

    def flush():
        text = inline(buf)
        buf.clear()
        if text:
            out.append(("b", [text]))

    for ch in node.children:
        if isinstance(ch, NavigableString):
            buf.append(ch)
            continue
        name = ch.name
        if name == "div" and "mw-heading" in ch.get("class", []):
            flush()
            h = ch.find(re.compile(r"h[1-6]$"))
            text = inline(h) if h else ""
            if text:
                out.append(("h", int(h.name[1]), text))
        elif re.fullmatch(r"h[1-6]", name):
            flush()
            text = inline(ch)
            if text:
                out.append(("h", int(name[1]), text))
        elif name in ("ul", "ol"):
            flush()
            lines = list_lines(ch)
            if lines:
                out.append(("b", lines))
        elif name == "dl":
            flush()
            lines = [t for t in (inline(x) for x in ch.find_all(["dt", "dd"])) if t]
            if lines:
                out.append(("b", lines))
        elif name == "table":
            flush()
            out.extend(table_items(ch))
        elif name == "p":
            flush()
            text = inline(ch)
            if text:
                out.append(("b", [text]))
        elif name in ("div", "blockquote", "section", "center"):
            flush()
            walk(ch, out)
        elif name == "hr":
            flush()
        else:
            buf.append(ch)
    flush()


def has_text(item):
    return item[0] == "b" and any(norm(l) for l in item[1])


def prune(items):
    """이름으로 지우는 절을 지우고, 글자가 하나도 남지 않은 절은 제목도 지운다."""
    kept, i = [], 0
    while i < len(items):
        it = items[i]
        if it[0] == "h" and it[2] in DROP_SECTIONS:
            level = it[1]
            i += 1
            while i < len(items) and not (items[i][0] == "h" and items[i][1] <= level):
                i += 1
            continue
        kept.append(it)
        i += 1
    result = []
    for i, it in enumerate(kept):
        if it[0] == "h":
            j, found = i + 1, False
            while j < len(kept) and not (kept[j][0] == "h" and kept[j][1] <= it[1]):
                if has_text(kept[j]):
                    found = True
                    break
                j += 1
            if not found:
                continue
        elif not has_text(it):
            continue
        result.append(it)
    return result


def render(title, info, items):
    blocks = [f"# {title}"]
    if info:
        blocks.append("\n".join(info))
    for it in items:
        if it[0] == "h":
            blocks.append("#" * it[1] + " " + it[2])
        else:
            blocks.append("\n".join(it[1]))
    text = "\n\n".join(blocks)
    text = "\n".join(l.rstrip() for l in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def convert_wiki(d, raw):
    """정보 상자가 맨 위에 없는 문서(동위 원소 문서 등)는 정보 상자 줄 없이 본문만 옮긴다."""
    soup = BeautifulSoup(raw.decode("utf-8"), "html.parser")
    root = soup.find("div", class_="mw-parser-output")
    has_box = root.find("table", class_="infobox", recursive=False) is not None
    prepare(root)
    info = []
    if has_box:
        box = mark_infobox(root)
        drop_all(root)
        info = infobox_lines(box)
        box.decompose()
    else:
        drop_all(root)
    items = []
    walk(root, items)
    return render(d["title"], info, prune(items))


def convert_kto(d, raw):
    """관광공사 명소 소개 글: 제목, 주소 줄, 홈페이지 줄, 소개 글. 쓰는 칸은 title, addr1, homepage, overview뿐이다."""
    item = json.loads(raw.decode("utf-8"))["response"]["body"]["items"]["item"]
    item = item[0] if isinstance(item, list) else item
    en = d["language"] == "en"
    blocks = [f"# {item['title'].strip()}"]
    homepage = (item.get("homepage") or "").strip()
    if "<" in homepage:  # <a …>주소</a>: 화면에 보이는 글자만
        homepage = norm(BeautifulSoup(homepage, "html.parser").get_text())
    for label, value in (("Address" if en else "주소", (item.get("addr1") or "").strip()),
                         ("Homepage" if en else "홈페이지", homepage)):
        if value:
            blocks.append(f"{label}: {value}")
    # <br>만 줄바꿈으로 바꾼다. <…> 모양을 통째로 지우지 않는다(<기생충>처럼 꺾쇠로 적은 글자가 남아야 한다).
    text = re.sub(r"<br\s*/?>", "\n", item.get("overview") or "", flags=re.I)
    text = html.unescape(text).replace("\xa0", " ")
    paragraphs = [re.sub(r"[ \t]+", " ", l).strip() for l in re.split(r"\r\n|\r|\n", text)]
    blocks += [p for p in paragraphs if p]
    return "\n\n".join(blocks) + "\n"


def convert_portal(d, raw):
    """통계 표: CSV를 칸 이름과 값을 바꾸지 않고 마크다운 표로 옮긴다."""
    rows = [[c.strip() for c in r] for r in csv.reader(io.StringIO(raw.decode("cp949"), newline="")) if r]
    lines = [md_row(rows[0]), "|" + "---|" * len(rows[0])] + [md_row(r) for r in rows[1:]]
    return "\n".join([f"# {d['title']}", ""] + lines) + "\n"


# 출처마다 바꾸는 함수.
CONVERT = {"wiki": convert_wiki, "kto": convert_kto, "portal": convert_portal}


# ---------------------------------------------------------------- collected.yaml

def load_collected():
    if not COLLECTED.exists():
        return []
    return (yaml.safe_load(COLLECTED.read_text(encoding="utf-8")) or {}).get("documents") or []


def save_collected(docs, rows):
    """documents.yaml의 순서로 쓴다. 목록에 없는 줄은 뒤에 둔다. fetch.py와 같은 모양."""
    order = {d["doc_id"]: i for i, d in enumerate(docs)}
    rows = sorted(rows, key=lambda r: order.get(r["doc_id"], len(order)))
    text = yaml.safe_dump({"documents": rows}, allow_unicode=True, sort_keys=False)
    COLLECTED.write_text(HEADER + text, encoding="utf-8")


def verify_with_commit(commit, only):
    """묶인 커밋의 build.py로 --verify를 돌려 출력을 그대로 내고 종료 코드를 돌려준다."""
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:src/corpus/build.py"], capture_output=True)
    if r.returncode != 0:
        sys.exit(f"커밋 {commit}의 build.py를 꺼내지 못함: {r.stderr.decode().strip()}")
    with tempfile.TemporaryDirectory() as tmp:
        script = Path(tmp) / "src" / "corpus" / "build.py"
        script.parent.mkdir(parents=True)
        script.write_bytes(r.stdout)
        (Path(tmp) / "data").symlink_to(ROOT / "data")  # 옛 build.py는 자기 위치에서 ROOT를 정한다
        cmd = [sys.executable, str(script), "--verify"] + (["--only", *only] if only else [])
        return subprocess.run(cmd).returncode


def main():
    ap = argparse.ArgumentParser(description="받아 둔 원본에서 마크다운을 만든다.")
    ap.add_argument("--only", nargs="+", metavar="DOC_ID", help="그 문서만 바꾼다")
    ap.add_argument("--verify", action="store_true",
                    help="파일과 기록을 쓰지 않고, 다시 만든 마크다운의 해시를 기록과 견준다")
    args = ap.parse_args()

    config = yaml.safe_load(DOCS.read_text(encoding="utf-8"))
    commit = config.get("converter_commit")
    if commit:
        if args.verify:
            sys.exit(verify_with_commit(commit, args.only))
        sys.exit(f"이 코퍼스는 커밋 {commit}의 변환에 묶여 있어 지금 변환으로 다시 만들지 않는다. --verify만 쓸 수 있다.")
    docs = config["documents"]
    if args.only:
        unknown = set(args.only) - {d["doc_id"] for d in docs}
        if unknown:
            sys.exit(f"documents.yaml에 없는 doc_id: {sorted(unknown)}")
    rows = load_collected()
    done = {r["doc_id"]: r for r in rows}
    if not args.verify:
        MARKDOWN.mkdir(parents=True, exist_ok=True)

    made, skipped = 0, 0
    same, differ, missing = 0, 0, 0
    for d in docs:
        doc_id = d["doc_id"]
        if args.only and doc_id not in args.only:
            continue
        kind = doc_id.split("-")[0]
        if kind not in CONVERT:
            continue  # 아직 바꾸는 함수가 없는 출처
        row = done.get(doc_id)
        raw_path = CORPUS / row["raw_file"] if row and row.get("raw_file") else None
        if args.verify:
            if raw_path is None or not raw_path.is_file() or not row.get("markdown_sha256"):
                missing += 1
                print(f"{doc_id}  없음")
                continue
            digest = hashlib.sha256(CONVERT[kind](d, raw_path.read_bytes()).encode("utf-8")).hexdigest()
            if digest == row["markdown_sha256"]:
                same += 1
                print(f"{doc_id}  같음")
            else:
                differ += 1
                print(f"{doc_id}  다름")
            continue
        if raw_path is None or not raw_path.is_file():
            skipped += 1
            print(f"{doc_id}  건너뜀: 원본이 없음")
            continue
        text = CONVERT[kind](d, raw_path.read_bytes())
        body = text.encode("utf-8")
        (MARKDOWN / f"{doc_id}.md").write_bytes(body)
        row["markdown_file"] = f"markdown/{doc_id}.md"
        row["markdown_sha256"] = hashlib.sha256(body).hexdigest()
        made += 1
        print(f"{doc_id}  만듦  {len(text)}글자")
    if args.verify:
        print(f"\n같음 {same}, 다름 {differ}, 없음 {missing}")
        sys.exit(1 if differ or missing else 0)
    save_collected(docs, rows)

    print(f"\n만듦 {made}, 건너뜀 {skipped}")


if __name__ == "__main__":
    main()
