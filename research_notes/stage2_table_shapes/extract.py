"""조사용: 마크다운 코퍼스의 표 100개를 원문 HTML 표와 짝지어 구조를 있는 그대로 적는다. 분류하지 않는다.

실행: uv run python research_notes/stage2_table_shapes/extract.py
결과: 같은 폴더의 tables.json, tables_dump.md
줄 번호(full_width_rows 등)는 원문 표의 줄을 1부터 센 값이다.
"""
import json
import re
import sys
from pathlib import Path

import yaml
from bs4 import NavigableString

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src" / "corpus"))
import build  # noqa: E402

CORPUS = ROOT / "data" / "corpus"


def frags(cell):
    """칸의 글자를 <br>과 직접 자식 <p>로 나눈 조각들. 빈 조각은 뺀다."""
    out, buf = [], []

    def flush():
        t = build.inline(buf)
        buf.clear()
        if t:
            out.append(t)

    def rec(node):
        for ch in node.children:
            if isinstance(ch, NavigableString):
                buf.append(ch)
            elif ch.name == "br":
                flush()
            elif ch.name == "p" and ch.parent is cell:
                flush()
                rec(ch)
                flush()
            elif ch.find("br"):
                rec(ch)
            else:
                buf.append(ch)

    rec(cell)
    flush()
    return out


def own(table, tag_names, cell):
    """칸 안의 tag_names 요소 가운데 이 표 자신의 것(겹친 표 안의 것이 아닌 것)."""
    return [x for x in cell.find_all(tag_names) if x.find_parent("table") is table]


def html_section(table):
    sub = None
    for h in table.find_all_previous(re.compile(r"^h[23]$")):
        t = build.inline(h)
        if h.name == "h3" and sub is None:
            sub = t
        elif h.name == "h2":
            return " / ".join(x for x in (f"## {t}", f"### {sub}" if sub else "") if x)
    return f"### {sub}" if sub else ""


def structure(table):
    rows = build.own_rows(table)
    grid, all_th, row_texts, row_spans, *_ = build.grid_of(table)
    cols = len(grid[0]) if grid else 0
    cells_by_row = [build.own_cells(tr) for tr in rows]
    full = [len(sp) == 1 and sp[0] > 1 and sp[0] >= cols for sp in row_spans]
    lead = 0
    while lead < len(rows) and full[lead]:
        lead += 1
    top = 0
    while lead + top < len(rows) and all_th[lead + top]:
        top += 1
    mid = [i + 1 for i in range(lead + top + 1, len(rows)) if all_th[i]]
    row_header = sum(1 for i, cs in enumerate(cells_by_row) if cs and not all_th[i] and cs[0].name == "th")
    rowspan = [build.inline(c)[:30] for cs in cells_by_row for c in cs if build.span(c, "rowspan") > 1]
    colspan = [build.inline(c)[:30] for i, cs in enumerate(cells_by_row) if not full[i]
               for c in cs if build.span(c, "colspan") > 1]
    br_ex, list_ex, pairs = [], [], []
    for i, cs in enumerate(cells_by_row):
        per_cell = []
        for c in cs:
            f = frags(c)
            per_cell.append(f)
            has_br = bool(own(table, "br", c))
            ps = c.find_all("p", recursive=False)
            if has_br or len(ps) >= 2:
                br_ex.append(" ⏎ ".join(f))
            if own(table, ["ul", "ol"], c):
                list_ex.append(build.inline(c))
        counts = [len(f) for f in per_cell if len(f) >= 2]
        if any(counts.count(n) >= 2 for n in set(counts)):
            pairs.append({"row": i + 1, "cells": per_cell})
    caption = table.find("caption")
    return {
        "rows": len(rows), "cols": cols,
        "class": table.get("class", []),
        "caption": build.inline(caption) if caption else None,
        "full_width_rows": [i + 1 for i, f in enumerate(full) if f],
        "top_th_rows": top,
        "mid_th_rows": mid,
        "row_header_rows": row_header,
        "rowspan_cells": {"count": len(rowspan), "texts": rowspan},
        "colspan_cells": {"count": len(colspan), "texts": colspan},
        "br_cells": {"count": len(br_ex), "examples": [e[:200] for e in br_ex[:3]]},
        "list_cells": {"count": len(list_ex), "examples": [e[:200] for e in list_ex[:3]]},
        "nested": table.find("table") is not None,
        "pair_rows": pairs,
        "first_cells": [build.inline(cs[0])[:80] for cs in cells_by_row[:5] if cs],
    }


def md_groups(lines):
    """파일에서 '|'로 시작하는 줄이 이어진 묶음: (시작 줄 번호(1부터), 줄 목록)."""
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


def md_section(lines, line_no):
    h2 = h3 = None
    for l in reversed(lines[:line_no - 1]):
        if h3 is None and l.startswith("### "):
            h3 = l
        if l.startswith("## "):
            h2 = l
            break
    return " / ".join(x for x in (h2, h3) if x)


def convert_wiki_traced(d, raw):
    calls, stack = [], []
    original = build.table_items

    def wrapper(table):
        rec = {"doc_id": d["doc_id"], "n": len(calls) + 1,
               "parent": stack[-1]["n"] if stack else None}
        rec.update({"_struct": structure(table), "_frame": build.is_frame(table),
                    "_section_html": html_section(table)})
        calls.append(rec)
        stack.append(rec)
        try:
            result = original(table)
        finally:
            stack.pop()
        rec["_result"] = result
        return result

    build.table_items = wrapper
    try:
        text = build.convert_wiki(d, raw)
    finally:
        build.table_items = original
    return text, calls


def finish(rec, md_lines_file, occurrence):
    result = rec.pop("_result")
    struct = rec.pop("_struct")
    frame = rec.pop("_frame")
    section_html = rec.pop("_section_html")
    idx = next((i for i, it in enumerate(result) if it[0] == "b" and it[1] and it[1][0].startswith("| ")), None)
    out = {"doc_id": rec["doc_id"], "n": rec["n"], "parent": rec["parent"]}
    if frame:
        out["outcome"] = "frame"
    elif idx is not None:
        out["outcome"] = "markdown"
    else:
        out["outcome"] = "empty"
    if out["outcome"] == "markdown":
        out["md_lines"] = result[idx][1]
        out["md_above"] = [l for it in result[:idx] if it[0] == "b" for l in it[1]]
        out["md_below"] = [l for it in result[idx + 1:] if it[0] == "b" for l in it[1]]
        key = tuple(out["md_lines"])
        starts = [s for s, g in md_groups(md_lines_file) if tuple(g) == key]
        k = occurrence.get(key, 0)
        occurrence[key] = k + 1
        out["md_line_no"] = starts[k] if k < len(starts) else None
    else:
        out["md_lines"], out["md_above"], out["md_below"], out["md_line_no"] = [], [], [], None
    if out["md_line_no"]:
        out["section"], out["section_source"] = md_section(md_lines_file, out["md_line_no"]), "md"
    else:
        out["section"], out["section_source"] = section_html, "html"
    out.update(struct)
    return out


def run():
    docs = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
    collected = {c["doc_id"]: c for c in yaml.safe_load((CORPUS / "collected.yaml").read_text(encoding="utf-8"))["documents"]}
    tables, problems, per_doc, kto_tables = [], [], [], {}
    for d in docs:
        did = d["doc_id"]
        md_bytes = (CORPUS / "markdown" / f"{did}.md").read_bytes()
        md_lines = md_bytes.decode("utf-8").split("\n")
        file_tables = len(md_groups(md_lines))
        if did.startswith("wiki-"):
            raw = (CORPUS / collected[did]["raw_file"]).read_bytes()
            text, calls = convert_wiki_traced(d, raw)
            if text.encode("utf-8") != md_bytes:
                problems.append(f"{did}: 다시 만든 글이 마크다운 파일과 다르다")
            occ = {}
            items = [finish(c, md_lines, occ) for c in calls]
            tables.extend(items)
            per_doc.append({"doc_id": did, "calls": len(items), "file_tables": file_tables,
                            **{o: sum(1 for t in items if t["outcome"] == o) for o in ("markdown", "frame", "empty")}})
        elif did.startswith("portal-"):
            g = md_groups(md_lines)
            lines = g[0][1] if g else []
            ncols = len(re.split(r"(?<!\\)\|", lines[0])) - 2 if lines else 0
            tables.append({"doc_id": did, "n": 1, "parent": None, "outcome": "markdown",
                           "md_lines": lines, "md_above": [], "md_below": [],
                           "md_line_no": g[0][0] if g else None,
                           "section": md_section(md_lines, g[0][0]) if g else "", "section_source": "md",
                           "rows": len(lines) - 1, "cols": ncols, "html": None})
            per_doc.append({"doc_id": did, "calls": 1, "file_tables": file_tables,
                            "markdown": 1, "frame": 0, "empty": 0})
        elif file_tables:
            kto_tables[did] = file_tables
    return tables, per_doc, kto_tables, problems


def fmt_md(t):
    lines = t["md_lines"]
    if len(lines) > 14:
        lines = lines[:12] + [f"… ({len(lines) - 14}줄 뺌)"] + lines[-2:]
    return lines


def dump(tables, per_doc, kto_tables, problems):
    o = ["# 표 구조 덤프", "", "줄 번호는 원문 표의 줄을 1부터 센 값.", "", "## 합계", "",
         "| 문서 | 호출 | markdown | frame | empty | 파일의 표 | markdown=파일 표 |", "|---|---|---|---|---|---|---|"]
    tot = {"calls": 0, "markdown": 0, "frame": 0, "empty": 0, "file_tables": 0}
    for p in per_doc:
        o.append(f"| {p['doc_id']} | {p['calls']} | {p['markdown']} | {p['frame']} | {p['empty']} | {p['file_tables']} | "
                 f"{'같다' if p['markdown'] == p['file_tables'] else '다르다'} |")
        for k in tot:
            tot[k] += p[k]
    o.append(f"| 전체 | {tot['calls']} | {tot['markdown']} | {tot['frame']} | {tot['empty']} | {tot['file_tables']} | "
             f"{'같다' if tot['markdown'] == tot['file_tables'] else '다르다'} |")
    o += ["", f"표 줄이 있는 그 밖의 문서: {kto_tables or '없음'}",
          f"원본 대조 문제: {problems or '없음'}", ""]
    for t in tables:
        parent = f" (parent {t['parent']})" if t["parent"] else ""
        md = f"md {t['md_line_no']}줄" if t["md_line_no"] else "md 줄 없음"
        sec = t["section"] + ("" if t["section_source"] == "md" else " [원문 제목]")
        o += ["", f"### {t['doc_id']} #{t['n']} [{t['outcome']}]{parent} — {md} — {sec}"]
        if "html" in t:
            o.append(f"구조: {t['rows']}줄×{t['cols']}열 (통계 표, 원문 HTML 없음)")
        else:
            o.append("구조: {rows}×{cols}, top_th_rows {top}, mid_th_rows {mid}, row_header_rows {rh}, "
                     "rowspan {rs}, colspan {cs}, br {br}, list {ls}, nested {ne}, caption {ca}, class {cl}, "
                     "full_width_rows {fw}".format(
                         rows=t["rows"], cols=t["cols"], top=t["top_th_rows"], mid=t["mid_th_rows"],
                         rh=t["row_header_rows"], rs=t["rowspan_cells"]["count"], cs=t["colspan_cells"]["count"],
                         br=t["br_cells"]["count"], ls=t["list_cells"]["count"], ne=t["nested"],
                         ca=repr(t["caption"]), cl=t["class"], fw=t["full_width_rows"]))
            for label, items in (("br 예", t["br_cells"]["examples"]), ("list 예", t["list_cells"]["examples"])):
                if items:
                    o.append(f"{label}: " + " | ".join(items))
            for label, key in (("rowspan 글자", "rowspan_cells"), ("colspan 글자", "colspan_cells")):
                tx = t[key]["texts"]
                if tx:
                    o.append(f"{label}: " + " | ".join(tx[:10]) + (f" … 외 {len(tx) - 10}" if len(tx) > 10 else ""))
            if t["pair_rows"]:
                o.append(f"pair_rows ({len(t['pair_rows'])}줄):")
                for p in t["pair_rows"][:5]:
                    o.append(f"  줄 {p['row']}: " + " || ".join(" ¦ ".join(c) for c in p["cells"]))
        if t["outcome"] == "markdown":
            if t["md_above"]:
                o.append("표 위: " + " / ".join(t["md_above"]))
            o += ["마크다운:"] + ["    " + l for l in fmt_md(t)]
            if t["md_below"]:
                o.append("표 아래: " + " / ".join(t["md_below"]))
        else:
            o.append("첫 칸들: " + " | ".join(t["first_cells"]))
    return "\n".join(o) + "\n"


def main():
    tables, per_doc, kto_tables, problems = run()
    (HERE / "tables.json").write_text(json.dumps(tables, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "tables_dump.md").write_text(dump(tables, per_doc, kto_tables, problems), encoding="utf-8")
    print(f"표 호출 {len(tables)}개, 문제 {problems or '없음'}")


if __name__ == "__main__":
    main()
