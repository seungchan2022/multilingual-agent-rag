"""찾을 낱말이 없어 대조 없이 통과하던 사실 9개(cleared.json)를 사람이 읽어 확인할 자리를 뽑는다(2026-10-14, Codex 1차 지적 2).

  uv run python -I research_notes/stage2_fact_count/no_key_city_mentions.py

사실의 도시 이름이 반대 언어 마크다운(위키백과와 포털 문서 전부)에 나오는 자리를 앞뒤 120자와 함께 모두 적는다.
같은 사실이 반대 언어 문서에 있다면 그 도시 이름이 함께 나오므로, 이 자리를 다 읽으면 된다고 본다.
글자로 찾으므로 다른 낱말의 일부(예: "성안동"의 "안동")도 나온다. 판정은 decisions/judgments.md 2026-10-14 줄에 있다.
"""
import pathlib, re

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
docs = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
text = {d["doc_id"]: (CORPUS / "markdown" / f"{d['doc_id']}.md").read_text(encoding="utf-8") for d in docs}
lang = {d["doc_id"]: d["language"] for d in docs}
# 사실 9개의 도시: 강릉 en 07·10, 부산 en 02, 안동 en 02·03, 제주 en 11 → 한국어 문서에서 찾는다
#                 경주 ko 05·07, 세종 ko 14 → 영어 문서에서 찾는다
NAMES = {"강릉": ("ko", ["강릉"]), "부산": ("ko", ["부산"]), "안동": ("ko", ["안동"]), "제주": ("ko", ["제주"]),
         "경주": ("en", ["Gyeongju", "Kyongju", "Kyŏngju"]), "세종": ("en", ["Sejong"])}
for city, (want, keys) in NAMES.items():
    found = [(did, m) for did, t in text.items() if lang[did] == want for k in keys for m in re.finditer(k, t)]
    print(f"## {city}: {want} 문서에서 {len(found)}곳")
    for did, m in found:
        t = text[did]
        print(f"- {did}: …{t[max(0, m.start() - 120): m.end() + 120]}…".replace("\n", " ⏎ "))
    print()
