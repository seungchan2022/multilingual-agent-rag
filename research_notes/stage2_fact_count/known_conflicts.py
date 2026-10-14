"""최종 평가셋 진행 안내(data/questions/final_set_guide.md)의 "알려진 부딪히는 값" 목록을 만든다(2026-10-14).

  uv run python -I research_notes/stage2_fact_count/known_conflicts.py

출처는 셋이다. excluded.json(질문에 쓰지 않기로 한 사실 29개와 이유), facts/*_pair.json의 conflict(두 언어 도시에서
두 언어 문서가 서로 어긋나는 값), DECISIONS.md 미정 목록 "질문을 만들 때 지킬 것" ⑤(한국어 전주·춘천 문서의 두 인구 표에서 값이 다른 해).
뽑아 둔 사실에서 찾은 것뿐이라 문서의 모든 값을 본 것이 아니다. 출력한 마크다운을 안내서 끝에 붙인다.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
facts = json.loads((HERE / "checked_markdown.json").read_text(encoding="utf-8"))
excluded = json.loads((HERE / "excluded.json").read_text(encoding="utf-8"))
DOC = {"전주시": "jeonju", "청주시": "cheongju", "춘천시": "chuncheon", "천안시": "cheonan", "부산광역시": "busan",
       "제주시": "jeju", "안동시": "andong", "강릉시": "gangneung", "수원시": "suwon", "경주시": "gyeongju",
       "세종특별자치시": "sejong", "광주광역시": "gwangju"}
by_id = {x["id"]: x for x in facts}

print("### 같은 문서 안에서, 또는 두 언어 문서의 목록에서 값이 부딪히는 사실\n")
for i, why in excluded.items():
    x = by_id[i]
    print(f"- `wiki-{x['lang']}-{DOC[x['city']]}`: {x['fact']} — {why}")
print("\n### 같은 도시의 두 언어 문서가 서로 어긋나는 값\n")
for f in sorted((HERE / "facts").glob("*_pair.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    city = DOC[d["city"]]
    for c in d.get("conflict", []):
        print(f"- `wiki-ko-{city}`와 `wiki-en-{city}`: {c['what']} — 한국어 {c['ko']}, 영어 {c['en']}")
print("\n### 뽑아 둔 사실 밖에서 본 것\n")
print("- `wiki-en-cheonan`: 연평균 기온과 역대 최고·최저 기온 — 본문 \"The average temperature in the city is 12.5 °C, with a recorded high of 34.2 °C and a low of -13.4 °C.\", 기후 표 연평균 12.0 °C, 역대 최고 37.8 °C, 역대 최저 −23.9 °C (미정 목록 \"질문을 만들 때 지킬 것\" ②의 천안 연평균 기온)")
print("- `wiki-en-jeju`: 6~9월 강수량 — 본문 \"more than 180 millimetres (7.1 in) of rain falling in each month from June to September\", 일도1동 기후 표의 6월 171.2 mm (2026-10-14 같은 문서 안의 다른 값을 찾던 서브에이전트가 사실 밖에서 본 것)")
print("- `wiki-ko-gyeongju`: 달마다의 평균 최고 기온 범위 — 본문 \"연평균 최고 기온은 8.6–31.1 °C (47–88 °F)이다\", 기후 표의 일평균 최고 기온은 가장 높은 달(8월)이 29.7 °C (같은 서브에이전트들이 사실 밖에서 본 것)")
print("- `wiki-en-gangneung`: 시로 설치된 해 — 정보 상자 \"City established: September 1, 1955\", 본문 \"Gangneung City was established in 1995 as the areas of Gangneung and Myeongju merged\" (명주 지역과 합친 해 1995년은 두 곳이 같아 쓸 수 있다. 2026-10-14 Codex 2차 지적 1)")
print("- `wiki-en-gangneung`: 면적 — 정보 상자·표 1,040 km2, 본문 \"about 1,040.4 km2\" (2026-10-14, 반올림·어림도 다른 값으로 본다)")
print("\n### 한 문서에 인구 표가 둘 있고 같은 해의 값이 다른 곳\n")
print("- `wiki-ko-jeonju`: 1955, 1960, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015년의 인구")
print("- `wiki-ko-chuncheon`: 1995, 2000, 2005, 2010, 2015, 2020년의 인구")
