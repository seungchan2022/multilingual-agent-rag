"""위키백과 표의 줄 두 가지를 센다(2026-10-14, Codex 1차 지적 1과 그 뒤의 고침).

  uv run python -I research_notes/stage2_markdown_rules/table_row_scans.py [build.py 경로]

① 빈 열 지우기로 첫 줄의 글자가 사라진 표: 표마다 첫 줄이 전부 머리글 칸(th)인지와 사라진 글자를 적는다.
② 원본 줄의 칸이 전부 아래로 걸친 칸(rowspan 2 이상)뿐인 줄.
build.py 경로를 주면 그 판으로 센다. 고치기 전 판은 git show 8a7f2e3^:src/corpus/build.py > 파일 로 꺼낸다
(그 판으로 ①은 표 11개, 그중 첫 줄이 th가 아닌 표 2개(청주 일반 도로, 춘천 교육 기관)가 나온다).
"""
import pathlib, sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "src" / "corpus" / "build.py"
src = BUILD.read_text(encoding="utf-8")
hook = "    head, body = [head[c] for c in keep], [[r[c] for c in keep] for r in body]\n"
assert src.count(hook) == 1, "build.py의 빈 열 지우기 줄을 찾지 못함"
src = src.replace(hook, "    LOST.append((CUR[0], [head[c] for c in range(len(head)) if c not in keep and head[c]], all_th[rows[0]]))\n" + hook)
g = {"__file__": str(ROOT / "src" / "corpus" / "build.py"), "__name__": "build", "LOST": [], "CUR": [None]}
sys.argv = ["build"]
exec(compile(src, str(BUILD), "exec"), g)

orig, spanned, n = g["table_items"], [], [0]


def wrapped(table):
    if not g["is_frame"](table):
        n[0] += 1
        for r, tr in enumerate(g["own_rows"](table)):
            cells = g["own_cells"](tr)
            if cells and all(g["span"](c, "rowspan") > 1 for c in cells):
                spanned.append((g["CUR"][0], n[0], r, [g["inline"](c)[:30] for c in cells]))
    return orig(table)


g["table_items"] = wrapped
for d in yaml.safe_load((ROOT / "data" / "corpus" / "documents.yaml").read_text(encoding="utf-8"))["documents"]:
    if d["doc_id"].startswith("wiki-"):
        g["CUR"][0] = d["doc_id"]
        g["convert_wiki"](d, (ROOT / "data" / "corpus" / "raw" / f"{d['doc_id']}.html").read_bytes())

lost = [x for x in g["LOST"] if x[1]]
print(f"build.py: {BUILD}")
print(f"① 빈 열 지우기로 첫 줄의 글자가 사라진 표 {len(lost)}개, 그중 첫 줄이 th가 아닌 표 {sum(1 for x in lost if not x[2])}개")
for doc, cells, th in lost:
    print(f"   {doc} {'첫 줄 전부 th' if th else '첫 줄 th 아님'} {cells}")
print(f"② 틀이 아닌 표 {n[0]}개에서 칸이 전부 아래로 걸친 줄 {len(spanned)}개")
for x in spanned:
    print("  ", *x)
