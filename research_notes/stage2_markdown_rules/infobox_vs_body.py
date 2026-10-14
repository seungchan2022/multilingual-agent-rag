"""정보 상자의 면적·인구·행정 구역 값과, 본문에서 같은 종류로 뽑아 둔 사실의 값을 문서마다 나란히 적는다.

  uv run python research_notes/stage2_markdown_rules/infobox_vs_body.py

정보 상자를 코퍼스에 남기면서 한 문서 안에 같은 것의 값이 둘이 되는 곳을 찾으려는 것이다(이슈 #4의 ③-2).
같은지 다른지는 프로그램이 판정하지 않는다. 나란히 적은 것을 사람이 읽는다. 결과는 infobox_vs_body.json.
본문 쪽 값은 stage2_fact_count/checked_markdown.json의 사실(문서마다 20개까지만 뽑은 것)이라 본문의 값 전부가 아니다.
"""
import json, re
from pathlib import Path

import yaml

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
KIND = {"area": ("면적", "Area"), "population": ("인구", "Population"), "districts_count": ("행정 구역", "법정동", "Administrative divisions", "Districts")}

facts = json.loads((HERE.parent / "stage2_fact_count" / "checked_markdown.json").read_text(encoding="utf-8"))
rows = []
for d in yaml.safe_load((ROOT / "data/corpus/documents.yaml").read_text(encoding="utf-8"))["documents"]:
    if not d["doc_id"].startswith("wiki-"):
        continue
    lines = (ROOT / "data/corpus/markdown" / (d["doc_id"] + ".md")).read_text(encoding="utf-8").split("\n")[2:]
    box, group = {}, ""
    for l in lines:
        if not l.strip():
            break  # 정보 상자는 제목 다음의 첫 목록이다
        if l.startswith("- "):
            group = l[2:].split(":")[0]
        for kind, names in KIND.items():
            label = l.strip()[2:].split(":")[0]
            if ":" in l and (label.startswith(names) or (l.startswith("  - ") and group.startswith(names) and label in ("Total", "Metropolitan city"))):
                box.setdefault(kind, []).append(l.strip()[2:])
    body = {k: [f"{x['value']} ← {x['quote'][:70]}" for x in facts if x["city"] == d["city"] and x["lang"] == d["language"] and x["kind"] == k] for k in KIND}
    rows.append({"doc_id": d["doc_id"], "infobox": box, "body_facts": body})
(HERE / "infobox_vs_body.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
for r in rows:
    print("==", r["doc_id"])
    for k in KIND:
        print("  ", k, "| 상자:", r["infobox"].get(k), "| 본문:", [b[:60] for b in r["body_facts"][k]])
