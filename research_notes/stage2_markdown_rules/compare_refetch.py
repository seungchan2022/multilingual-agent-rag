"""2026-10-14에 수집 코드로 받은 위키백과 원본을, 2026-10-13에 같은 판 번호로 받아 둔 HTML과 견준다.

  uv run python research_notes/stage2_markdown_rules/compare_refetch.py

같은 판을 다시 받으면 같은 바이트가 오는지를 본다(이슈 #4 ④의 재료). 결과는 compare_refetch.json에 쓴다.
어제 받은 HTML은 stage2_domain_survey/cache/에 있고 저장소에는 없다.
"""
import json, re
from pathlib import Path

import yaml

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
strip = lambda s: re.sub(r"<!--.*?-->", "", s, flags=re.S)  # HTML 주석(문서를 그리는 데 걸린 시간 등이 적힌다)

rows = []
for d in yaml.safe_load((ROOT / "data/corpus/documents.yaml").read_text(encoding="utf-8"))["documents"]:
    if not d["doc_id"].startswith("wiki-"):
        continue
    new = (ROOT / f"data/corpus/raw/{d['doc_id']}.html").read_text(encoding="utf-8")
    old = (HERE.parent / f"stage2_domain_survey/cache/{d['language']}_{d['version'].split()[-1]}.html").read_text(encoding="utf-8")
    rows.append({"doc_id": d["doc_id"], "same_bytes": new == old, "same_without_comments": strip(new) == strip(old)})
total = {"documents": len(rows), "same_bytes": sum(r["same_bytes"] for r in rows), "same_without_comments": sum(r["same_without_comments"] for r in rows)}
(HERE / "compare_refetch.json").write_text(json.dumps({"total": total, "documents": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
print(total)
