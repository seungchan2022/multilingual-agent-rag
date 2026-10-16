"""최종 평가셋 진행 안내(data/questions/final_set_guide.md)의 "알려진 부딪히는 값" 목록을 만든다(2026-10-14).

  uv run python -I research_notes/stage2_fact_count/known_conflicts.py

출처는 셋이다. excluded.json(질문에 쓰지 않기로 한 사실과 이유), facts/*_pair.json의 conflict(두 언어 도시에서
두 언어 문서가 서로 어긋나는 값), DECISIONS.md 미정 목록 "질문을 만들 때 지킬 것" ⑤(한국어 전주·춘천 문서의 두 인구 표에서 값이 다른 해).
뽑아 둔 사실에서 찾은 것뿐이라 문서의 모든 값을 본 것이 아니다. 출력한 마크다운을 안내서 끝에 붙인다.
같은 항목들을 기계가 읽을 JSON으로도 data/questions/known_conflicts.json에 쓴다(src/questions/check_candidates.py가 읽는다).
"""
import json, pathlib, re

HERE = pathlib.Path(__file__).parent
facts = json.loads((HERE / "checked_markdown.json").read_text(encoding="utf-8"))
excluded = json.loads((HERE / "excluded.json").read_text(encoding="utf-8"))
DOC = {"전주시": "jeonju", "청주시": "cheongju", "춘천시": "chuncheon", "천안시": "cheonan", "부산광역시": "busan",
       "제주시": "jeju", "안동시": "andong", "강릉시": "gangneung", "수원시": "suwon", "경주시": "gyeongju",
       "세종특별자치시": "sejong", "광주광역시": "gwangju"}
by_id = {x["id"]: x for x in facts}
ROOT = HERE.parents[1]
OUT = ROOT / "data" / "questions" / "known_conflicts.json"
MARKDOWN = ROOT / "data" / "corpus" / "markdown"
S1 = "같은 문서 안에서, 또는 두 언어 문서의 목록에서 값이 부딪히는 사실"
S2 = "같은 도시의 두 언어 문서가 서로 어긋나는 값"
S3 = "뽑아 둔 사실 밖에서 본 것"
S4 = "한 문서에 인구 표가 둘 있고 같은 해의 값이 다른 곳"
items = []   # (소제목, 줄 글, 견줄 거리)


def numbers(s):
    """글에서 숫자열(쉼표·소수점 포함)을 뽑는다. 음수 부호는 뗀다. 쉼표·소수점을 뺀 자릿수가 2자리 미만인 것은 뺀다."""
    return [n for n in re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", s) if len(re.sub(r"[,.]", "", n)) >= 2]


def add(section, text, **rest):
    items.append((section, text, rest))


def located(doc, quote):
    """인용이 원문에 글자 그대로 없고 끝에 빈 표 칸(' |')이 하나 더 붙은 것이면 떼어 돌려준다(청주 영어 자매도시 두 줄)."""
    md = (MARKDOWN / f"{doc}.md").read_text(encoding="utf-8")
    if quote not in md and quote.endswith(" |") and quote[:-2] in md:
        return quote[:-2]
    return quote


for i, why in excluded.items():
    x = by_id[i]
    doc = f"wiki-{x['lang']}-{DOC[x['city']]}"
    add(S1, f"`{doc}`: {x['fact']} — {why}",
        doc_id=doc, quotes=[located(doc, x["quote"])], values=numbers(" ".join(x.get("keys_num", []))))
for f in sorted((HERE / "facts").glob("*_pair.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    city = DOC[d["city"]]
    for c in d.get("conflict", []):
        add(S2, f"`wiki-ko-{city}`와 `wiki-en-{city}`: {c['what']} — 한국어 {c['ko']}, 영어 {c['en']}",
            targets=[{"doc_id": f"wiki-ko-{city}", "values": numbers(str(c["ko"]))},
                     {"doc_id": f"wiki-en-{city}", "values": numbers(str(c["en"]))}])
# 손으로 적은 줄: (문서, 줄 글, 줄에 인용된 원문 문장들, 값을 뽑을 글들[화씨·인치 환산 값과 덧붙인 날짜·메모는 뺀다])
OUTSIDE = [
    ("wiki-en-cheonan", "연평균 기온과 역대 최고·최저 기온 — 본문 \"The average temperature in the city is 12.5 °C, with a recorded high of 34.2 °C and a low of -13.4 °C.\", 기후 표 연평균 12.0 °C, 역대 최고 37.8 °C, 역대 최저 −23.9 °C (미정 목록 \"질문을 만들 때 지킬 것\" ②의 천안 연평균 기온)",
     ["The average temperature in the city is 12.5 °C, with a recorded high of 34.2 °C and a low of -13.4 °C."],
     ["12.5 °C", "34.2 °C", "13.4 °C", "12.0 °C", "37.8 °C", "23.9 °C"]),
    ("wiki-en-jeju", "6~9월 강수량 — 본문 \"more than 180 millimetres (7.1 in) of rain falling in each month from June to September\", 일도1동 기후 표의 6월 171.2 mm (2026-10-14 같은 문서 안의 다른 값을 찾던 서브에이전트가 사실 밖에서 본 것)",
     ["more than 180 millimetres (7.1 in) of rain falling in each month from June to September"],
     ["180 millimetres", "171.2 mm"]),
    ("wiki-ko-gyeongju", "달마다의 평균 최고 기온 범위 — 본문 \"연평균 최고 기온은 8.6–31.1 °C (47–88 °F)이다\", 기후 표의 일평균 최고 기온은 가장 높은 달(8월)이 29.7 °C (같은 서브에이전트들이 사실 밖에서 본 것)",
     ["연평균 최고 기온은 8.6–31.1 °C (47–88 °F)이다"],
     ["8.6–31.1 °C", "29.7 °C"]),
    ("wiki-en-gangneung", "시로 설치된 해 — 정보 상자 \"City established: September 1, 1955\", 본문 \"Gangneung City was established in 1995 as the areas of Gangneung and Myeongju merged\" (2026-10-14 Codex 2차 지적 1)",
     ["City established: September 1, 1955", "Gangneung City was established in 1995 as the areas of Gangneung and Myeongju merged"],
     ["September 1, 1955", "in 1995"]),
    ("wiki-en-gangneung", "면적 — 정보 상자·표 1,040 km2, 본문 \"about 1,040.4 km2\" (2026-10-14, 반올림·어림도 다른 값으로 본다)",
     ["about 1,040.4 km2"],
     ["1,040 km2", "1,040.4 km2"]),
]
for doc, text, quotes, vsrc in OUTSIDE:
    md = (MARKDOWN / f"{doc}.md").read_text(encoding="utf-8")
    for q in quotes:
        if q not in md:
            raise SystemExit(f"{doc}.md에 글자 그대로 없는 인용: {q}")
    add(S3, f"`{doc}`: {text}", doc_id=doc, quotes=quotes, values=numbers(" ".join(vsrc)))
YEARS = [("wiki-ko-jeonju", "1955, 1960, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015"),
         ("wiki-ko-chuncheon", "1995, 2000, 2005, 2010, 2015, 2020")]
for doc, years in YEARS:
    add(S4, f"`{doc}`: {years}년의 인구", doc_id=doc, table_years=years.split(", "))

printed = None
for section, text, rest in items:
    if section != printed:
        print(("\n" if printed else "") + f"### {section}\n")
        printed = section
    print(f"- {text}")
OUT.write_text(json.dumps([{"section": s, "text": t, **r} for s, t, r in items], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
