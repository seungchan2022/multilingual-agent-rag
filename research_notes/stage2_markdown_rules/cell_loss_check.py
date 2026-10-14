"""표 칸의 글자가 마크다운에 남았는지 견준다(2026-10-14, Codex 1차 지적 1을 고친 뒤).

  uv run python -I research_notes/stage2_markdown_rules/cell_loss_check.py

build.py의 table_items를 감싸, 표마다 원본의 글자가 table_items가 낸 항목에 있는지 본다.
틀이 아닌 표는 칸을 편 격자의 칸 글자 전체를, 틀로 풀린 표는 표 안의 두 글자 이상인 글자 조각(공백을 뺀 것)을 찾는다.
위키백과 문서 16개만 본다(통계 표는 check_build.py 24번이 CSV와 모든 값을 견준다).
"""
import pathlib, re, sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = ROOT / "src" / "corpus" / "build.py"
g = {"__file__": str(BUILD), "__name__": "build"}
sys.argv = ["build"]
exec(compile(BUILD.read_text(encoding="utf-8"), str(BUILD), "exec"), g)

orig = g["table_items"]
cur, n = [None], {"표": 0, "틀": 0}
lost = {"표": [], "틀": []}
squash = lambda s: re.sub(r"\s+", "", s)


def wrapped(table):
    frame = g["is_frame"](table)
    grid = None if frame else g["grid_of"](table)[0]
    out = orig(table)
    text = "".join(map(str, out))
    if frame:
        n["틀"] += 1
        flat = squash(text)
        for s in table.find_all(string=True):
            t = squash(str(s))
            if len(t) >= 2 and t not in flat:
                lost["틀"].append((cur[0], n["틀"], str(s).strip()[:60]))
    else:
        n["표"] += 1
        seen = set()
        for row in grid:
            for cell in row:
                if cell and cell not in text and cell not in seen:
                    seen.add(cell)
                    lost["표"].append((cur[0], n["표"], cell[:60]))
    return out


g["table_items"] = wrapped
for d in yaml.safe_load((ROOT / "data" / "corpus" / "documents.yaml").read_text(encoding="utf-8"))["documents"]:
    if d["doc_id"].startswith("wiki-"):
        cur[0] = d["doc_id"]
        g["convert_wiki"](d, (ROOT / "data" / "corpus" / "raw" / f"{d['doc_id']}.html").read_bytes())

print(f"틀이 아닌 표 {n['표']}개, 사라진 칸 {len(lost['표'])}개")
for x in lost["표"]:
    print("  ", *x)
print(f"틀로 풀린 표 {n['틀']}개, 사라진 글자 조각 {len(lost['틀'])}개")
for x in lost["틀"]:
    print("  ", *x)
