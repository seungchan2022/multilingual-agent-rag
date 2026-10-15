"""shared_names.json을 맡을 문서별로 60개 이하의 묶음으로 나눈다. 결과: batches/<번호>.json"""
import json
from pathlib import Path
HERE = Path(__file__).parent
items = json.loads((HERE / "shared_names.json").read_text(encoding="utf-8"))
ORDER = ["wiki-ko-suwon", "portal-ko-suwon-population", "wiki-ko-gyeongju", "wiki-ko-sejong", "wiki-ko-gwangju",
         "wiki-ko-jeonju", "kto-ko-jeonju-hanok-village", "portal-ko-jeonju-population",
         "wiki-ko-cheongju", "kto-ko-cheongju-cheongnamdae", "wiki-ko-chuncheon",
         "kto-ko-chuncheon-samaksan-cable-car", "wiki-ko-cheonan", "kto-ko-cheonan-samgeori-park"]
SMALL = 30  # 이보다 적은 문서는 모아서 한 묶음으로
out = HERE / "batches"; out.mkdir(exist_ok=True)
for f in out.glob("*.json"): f.unlink()
groups, rest = [], []
for d in ORDER:
    mine = [x for x in items if x["owner"] == d]
    if len(mine) < SMALL:
        rest += mine; continue
    n = -(-len(mine) // 60); size = -(-len(mine) // n)
    groups += [mine[i:i + size] for i in range(0, len(mine), size)]
if rest: groups.append(rest)
for i, g in enumerate(groups, 1):
    (out / f"{i:02d}.json").write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
assert sum(len(g) for g in groups) == len(items)
print([(i, len(g), sorted({x['owner'] for x in g})) for i, g in enumerate(groups, 1)])
