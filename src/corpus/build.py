"""받아 둔 원본에서 마크다운을 만드는 프로그램.

  uv run python src/corpus/build.py                       원본이 있는 문서를 모두 바꾼다
  uv run python src/corpus/build.py --only <doc_id> ...   그 문서만 바꾼다

data/corpus/raw/<doc_id>.html을 읽어 data/corpus/markdown/<doc_id>.md를 쓰고,
마크다운의 해시를 data/corpus/collected.yaml에 적는다. 인터넷과 시계를 쓰지 않는다.
같은 원본에서는 항상 글자 하나까지 같은 마크다운이 나온다.
규칙은 decisions/stage2.md의 2026-10-14 줄(남기는 것과 지우는 것 / 표를 옮기는 규칙 / 제목)에 있다.
지금은 위키백과(wiki-) 문서만 바꾼다. 관광공사(kto-)와 통계 표(portal-)는 CONVERT에 함수를 더하면 된다.
"""
import argparse, hashlib, re, sys
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
    "style", "script", "link", "meta",
    ".geo-nondefault", ".geo-multi-punct", ".geo-inline-hidden",
]
DISPLAY_NONE = re.compile(r"display\s*:\s*none", re.I)
ROAD_SIGN = re.compile(r"/(Korean_(?:Highway|National_Route|Local_Route)[^/]*)")
FOLD_NOTICE = "이 글을 보려면 오른쪽 ‘펼치기’ 버튼 클릭"  # 접힌 상자를 여는 안내문. 본문이 아니다.
INFOBOX_SKIP_LABELS = {"웹사이트", "Website"}

BLOCK = {"p", "div", "li", "dt", "dd", "dl", "ul", "ol", "tr", "td", "th", "table", "caption",
         "blockquote", "h1", "h2", "h3", "h4", "h5", "h6"}


def norm(s):
    """공백(줄바꿈, 띄어쓰기 없는 공백 포함)을 하나로 줄이고 앞뒤를 자른다."""
    return re.sub(r"\s+", " ", s).strip()


def inline(nodes):
    """노드(또는 노드 목록)의 글자. <br>과 칸 안의 문단은 빈칸 하나로, 목록은 ', '로 잇는다."""
    if not isinstance(nodes, list):
        nodes = [nodes]
    parts = []

    def rec(n):
        if isinstance(n, NavigableString):
            parts.append(str(n))
        elif n.name == "br":
            parts.append(" ")
        elif n.name in ("ul", "ol"):
            items = [inline(li) for li in n.find_all("li", recursive=False)]
            parts.append(" " + ", ".join(i for i in items if i) + " ")
        elif n.name in BLOCK:
            parts.append(" ")
            for c in n.children:
                rec(c)
            parts.append(" ")
        else:
            for c in n.children:
                rec(c)

    for n in nodes:
        rec(n)
    return norm("".join(parts))


# ---------------------------------------------------------------- 지우기

def prepare(root):
    """HTML 나무에서 지울 것을 지우고, 그 자리에 남길 글자(도로 표지, 원그래프)를 넣는다."""
    for c in root.find_all(string=lambda t: isinstance(t, Comment)):
        c.extract()
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
    """문서 맨 위의 정보 상자 하나를 찾아 이미지가 든 줄을 지우고 돌려준다. 나머지 infobox 표는 지운다.

    이미지가 든 줄에는 그 이미지의 설명이 같이 들어 있으므로 줄째로 지운다. 이 일은
    이미지를 지우기 전에 해야 한다. 국기 아이콘(.flagicon)은 장식이라 줄을 지우는 근거로 쓰지 않는다.
    """
    top = root.find("table", class_="infobox", recursive=False)
    for t in root.find_all("table", class_="infobox"):
        if t is not top:
            t.decompose()
    for tr in own_rows(top):
        for fl in tr.select(".flagicon"):
            fl.decompose()
        if tr.select("img, figure, .mw-kartographer-map"):
            tr.decompose()
    return top


def infobox_lines(box):
    """정보 상자에서 글자로 된 줄을 '- ...'로 뽑는다.

    웹사이트 줄만 화면의 글자 대신 바깥 링크의 주소를 값으로 적는다(링크가 없으면 화면의 글자).
    아래에 줄이 하나도 남지 않는 묶음 제목(infobox-header)은 지운다.
    """
    items = []  # (묶음 제목인가, 줄)
    for tr in own_rows(box):
        cells = own_cells(tr)
        texts = [inline(c) for c in cells]
        if len(cells) == 2 and cells[0].name == "th" and cells[1].name == "td":
            value = texts[1]
            if texts[0] in INFOBOX_SKIP_LABELS:
                link = cells[1].find("a", class_="external")
                if link and link.get("href"):
                    value = link["href"].strip()
            if not value:
                continue
            items.append((False, f"- {texts[0]}: {value}" if texts[0] else f"- {value}"))
        else:
            text = norm(" ".join(t for t in texts if t))
            if text:
                head = len(cells) == 1 and cells[0].name == "th" and "infobox-header" in cells[0].get("class", [])
                items.append((head, f"- {text}"))
    return [line for i, (head, line) in enumerate(items)
            if not head or (i + 1 < len(items) and not items[i + 1][0])]


# ---------------------------------------------------------------- 표

def grid_of(table):
    """칸을 합친 표를 폈을 때의 (칸 글자 격자, 줄마다 모두 th인지, 줄의 원래 칸 글자, 줄의 원래 colspan, 칸의 출처)."""
    cells, origin = {}, {}
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
    return grid, all_th, row_texts, row_spans, src


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

    grid, all_th, row_texts, row_spans, src = grid_of(table)
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
    rows = [i for i in range(lead, len(grid)) if not full[i]]
    if not rows:
        return out + below
    # 이웃한 두 열이 모든 줄에서 같은 원래 칸에서 나왔으면(가로로 합친 칸을 편 것) 하나로 합친다.
    cols = [0]
    for c in range(1, ncols):
        if not all(src[i] is None or src[i][c] == src[i][c - 1] for i in rows):
            cols.append(c)
    head, body = [grid[rows[0]][c] for c in cols], [[grid[i][c] for c in cols] for i in rows[1:]]
    # 머리글 줄을 뺀 모든 줄에서 글자가 없는 열은 머리글까지 지운다.
    # 머리글 줄밖에 없는 표는 줄이 없어 모든 열이 비게 되므로, 머리글 칸이 빈 열만 지운다.
    keep = [c for c in range(len(head)) if any(r[c] for r in body)] if body else [c for c in range(len(head)) if head[c]]
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
    soup = BeautifulSoup(raw.decode("utf-8"), "html.parser")
    root = soup.find("div", class_="mw-parser-output")
    prepare(root)
    box = mark_infobox(root)
    drop_all(root)
    info = infobox_lines(box)
    box.decompose()
    items = []
    walk(root, items)
    return render(d["title"], info, prune(items))


# 출처마다 바꾸는 함수. 관광공사(kto)와 통계 표(portal)는 여기에 함수를 더한다.
CONVERT = {"wiki": convert_wiki}


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


def main():
    ap = argparse.ArgumentParser(description="받아 둔 원본에서 마크다운을 만든다.")
    ap.add_argument("--only", nargs="+", metavar="DOC_ID", help="그 문서만 바꾼다")
    args = ap.parse_args()

    docs = yaml.safe_load(DOCS.read_text(encoding="utf-8"))["documents"]
    if args.only:
        unknown = set(args.only) - {d["doc_id"] for d in docs}
        if unknown:
            sys.exit(f"documents.yaml에 없는 doc_id: {sorted(unknown)}")
    rows = load_collected()
    done = {r["doc_id"]: r for r in rows}
    MARKDOWN.mkdir(parents=True, exist_ok=True)

    made, skipped = 0, 0
    for d in docs:
        doc_id = d["doc_id"]
        if args.only and doc_id not in args.only:
            continue
        kind = doc_id.split("-")[0]
        if kind not in CONVERT:
            continue  # 아직 바꾸는 함수가 없는 출처
        row = done.get(doc_id)
        raw_path = CORPUS / row["raw_file"] if row and row.get("raw_file") else None
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
    save_collected(docs, rows)

    print(f"\n만듦 {made}, 건너뜀 {skipped}")


if __name__ == "__main__":
    main()
