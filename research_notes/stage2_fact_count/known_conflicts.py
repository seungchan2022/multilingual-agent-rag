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


def verbatim(doc, quotes):
    """인용이 모두 그 문서 마크다운에 글자 그대로 있어야 한다. 아니면 멈춘다."""
    md = (MARKDOWN / f"{doc}.md").read_text(encoding="utf-8")
    for q in quotes:
        if q not in md:
            raise SystemExit(f"{doc}.md에 글자 그대로 없는 인용: {q}")
    return quotes


# S2: (도시, what) -> (한국어 문서의 자리들, 영어 문서의 자리들). 자리마다 원문 글자 그대로. 산문은 값이 든 문장(또는 그 부분), 표는 값이 든 행 한 줄, 목록은 줄마다.
S2_PLACES = {
    ("jeonju", "6월 역대 최고 기온"): (
        ["| 역대 최고 기온 °C (°F) | 18.3 (64.9) | 22.9 (73.2) | 29.6 (85.3) | 31.2 (88.2) | 35.1 (95.2) | 36.5 (97.7) | 38.6 (101.5) | 38.9 (102.0) | 35.5 (95.9) | 31.5 (88.7) | 28.0 (82.4) | 23.0 (73.4) | 38.9 (102.0) |"],
        ["| Record high °C (°F) | 18.3 (64.9) | 22.9 (73.2) | 29.6 (85.3) | 31.2 (88.2) | 35.1 (95.2) | 35.8 (96.4) | 38.6 (101.5) | 38.9 (102.0) | 35.5 (95.9) | 31.5 (88.7) | 28.0 (82.4) | 23.0 (73.4) | 38.9 (102.0) |"]),
    ("jeonju", "전주한옥마을의 한옥 수"): (
        ["전주한옥마을은 경기전 앞을 지나는 길인 태조로를 중심으로 교동과 풍남동 일대의 도심지에 650여채의 한옥들이 군락을 이루고 있는 곳이다."],
        ["The Jeonju Hanok Village (Hanok Maeul) is a traditional-style village in the heart of Jeonju, housing over 800 traditional \"hanok\" style buildings."]),
    ("jeonju", "전주 전동성당의 사적 번호"): (
        ["호남지역 서양식 근대건축물로써는 가장 오래된 건축물로 사적 제228호에 지정되었다."],
        ["This Byzantine and Romanesque church has been designated historic site No. 288."]),
    ("jeonju", "1182년 봉기가 이어진 기간"): (
        ["1182년(무신 정권 시기) : 관노비와 군인들이 합세해서 전주성을 점령하고 여러 달 동안 저항하였다."],
        ["The rebellion was soon suppressed forty days after it began."]),
    ("jeonju", "후백제가 끝난 해"): (
        ["후백제가 망한 936년까지 수도(首都)였다."],
        ["However, Wang Geon and his forces invaded Later Baekje in 934 and Jeonju surrendered to him in 935."]),
    ("jeonju", "자매 도시 수"): (
        ["- 미국 샌디에고 (1983. 05. 20 ~ )",
         "- 중국 쑤저우시 (1996. 03. 21 ~ )",
         "- 일본 가나자와시 (2002. 04. 30 ~ )",
         "- 튀르키예 안탈리아 (2013. 07. 04 ~ )",
         "- 미국 호놀룰루 (2004. 12. 20 ~ )",
         "- 중국 선양시 (2006. 07. 17 ~ )",
         "- 중국 창춘시 (2006. 07. 18 ~ )",
         "- 이탈리아 피렌체 (2007. 03. 28 ~ )",
         "- 중국 시닝시 (2012. 06. 11 ~ )"],
        ["- San Diego, California, United States",
         "- Suzhou, Jiangsu, China",
         "- Huế, Vietnam",
         "- Kanazawa, Ishikawa, Japan",
         "- Edmonton, Canada",
         "- Antalya, Turkey",
         "- Mokpo, South Korea",
         "- Zugló, Hungary"]),
    ("jeonju", "동(행정동) 수"): (
        ["행정 구역: 2구 35행정동 82법정동",
         "행정 구역은 2구(완산구, 덕진구) 35행정동 82법정동이다.",
         "전주시의 행정 구역은 2구 35행정동 82법정동으로 구성되어 있다."],
        ["Administrative divisions: 2 Gu, 40 dong",
         "Jeonju is divided into two wards, Deokjin District and Wansan District that, in turn, are divided into approximately 40 neighborhoods."]),
    ("cheonan", "천안시 면적"): (
        ["면적: 636.2 km2",
         "천안시의 면적은 636.07 km2이고, 2018년 9월 주민등록 인구는 669,928명이다.",
         "| 총계 | 총계 | 683,453 | 255,696 | 636.2 |"],
        ["Total: 636.25 km2 (245.66 sq mi)"]),
    ("cheonan", "천안시 행정동 수"): (
        ["행정 구역: 2구 4읍 8면 19행정동 30법정동",
         "행정구역은 2구 4읍 8면 19행정동이고, 시청 소재지는 불당동이다.",
         "불당동이 불당1동과 불당2동으로 분동되었다.(2구 4읍 8면 19행정동)",
         "천안시의 행정구역은 2구, 4읍, 8면, 19행정동이다."],
        ["Administrative divisions: 2 gu, 16 legal dong, 4 eup, 8 myeon",
         "Cheonan is divided into 2 gu, and 16 administrative dong (subdivided into 30 distinct legal dong), 4 eup and 8 myeon."]),
    ("cheonan", "12월 역대 최고 기온"): (
        ["| 역대 최고 기온 °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.7 (80.1) | 31.2 (88.2) | 33.9 (93.0) | 34.8 (94.6) | 37.7 (99.9) | 37.8 (100.0) | 34.1 (93.4) | 28.7 (83.7) | 25.3 (77.5) | 19.1 (66.4) | 37.8 (100.0) |"],
        ["| Record high °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.9 (80.4) | 31.2 (88.2) | 33.9 (93.0) | 34.8 (94.6) | 37.7 (99.9) | 37.8 (100.0) | 34.1 (93.4) | 28.7 (83.7) | 25.3 (77.5) | 18.5 (65.3) | 37.8 (100.0) |"]),
    ("cheonan", "3월 역대 최고 기온"): (
        ["| 역대 최고 기온 °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.7 (80.1) | 31.2 (88.2) | 33.9 (93.0) | 34.8 (94.6) | 37.7 (99.9) | 37.8 (100.0) | 34.1 (93.4) | 28.7 (83.7) | 25.3 (77.5) | 19.1 (66.4) | 37.8 (100.0) |"],
        ["| Record high °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.9 (80.4) | 31.2 (88.2) | 33.9 (93.0) | 34.8 (94.6) | 37.7 (99.9) | 37.8 (100.0) | 34.1 (93.4) | 28.7 (83.7) | 25.3 (77.5) | 18.5 (65.3) | 37.8 (100.0) |"]),
    ("cheonan", "태조산 높이"): (
        ["천안시 중앙을 남북으로 가로지르는 차령산맥의 태조산(424m) 줄기를 중심으로 동서측으로 지역이 분리되어 있다."],
        ["Some of the mountains in the city's vicinity include Malloesan (611m), Seonggeosan (579m), Taejosan (422m), Heukseongsan (519m), Gwangdeoksan (699m), and Manggyeongsan (600m)."]),
    ("cheongju", "3월 역대 최고 기온(°C)"): (
        ["| 역대 최고 기온 °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 25.9 (78.6) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 36.2 (97.2) | 30.6 (87.1) | 26.5 (79.7) | 19.6 (67.3) | 39.1 (102.4) |"],
        ["| Record high °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 28.2 (82.8) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 34.7 (94.5) | 30.6 (87.1) | 25.1 (77.2) | 19.3 (66.7) | 39.1 (102.4) |"]),
    ("cheongju", "9월 역대 최고 기온(°C)"): (
        ["| 역대 최고 기온 °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 25.9 (78.6) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 36.2 (97.2) | 30.6 (87.1) | 26.5 (79.7) | 19.6 (67.3) | 39.1 (102.4) |"],
        ["| Record high °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 28.2 (82.8) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 34.7 (94.5) | 30.6 (87.1) | 25.1 (77.2) | 19.3 (66.7) | 39.1 (102.4) |"]),
    ("cheongju", "11월 역대 최고 기온(°C)"): (
        ["| 역대 최고 기온 °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 25.9 (78.6) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 36.2 (97.2) | 30.6 (87.1) | 26.5 (79.7) | 19.6 (67.3) | 39.1 (102.4) |"],
        ["| Record high °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 28.2 (82.8) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 34.7 (94.5) | 30.6 (87.1) | 25.1 (77.2) | 19.3 (66.7) | 39.1 (102.4) |"]),
    ("cheongju", "12월 역대 최고 기온(°C)"): (
        ["| 역대 최고 기온 °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 25.9 (78.6) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 36.2 (97.2) | 30.6 (87.1) | 26.5 (79.7) | 19.6 (67.3) | 39.1 (102.4) |"],
        ["| Record high °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 28.2 (82.8) | 31.3 (88.3) | 34.5 (94.1) | 36.3 (97.3) | 37.8 (100.0) | 39.1 (102.4) | 34.7 (94.5) | 30.6 (87.1) | 25.1 (77.2) | 19.3 (66.7) | 39.1 (102.4) |"]),
    ("cheongju", "충북선 개통 연도"): (
        ["1920년 충북선이 개통되었다."],
        ["The opening of the Chungbuk-line in 1926 sparked regional development."]),
    ("cheongju", "자매도시 수와 구성"): (
        ["| 대한민국 | 서울특별시 | 용산구 |",
         "| 대한민국 | 경상남도 | 사천시 |",
         "| 미국 | 워싱턴주 | 벨링헴 |",
         "| 아랍에미리트 | 아부다비 토후국 | 아부다비 |",
         "| 에콰도르 | 피친차주 | 키토 |",
         "| 일본 | 돗토리현 | 돗토리시 |",
         "| 일본 | 야마나시현 | 고후시 |",
         "| 캐나다 | 온타리오주 | 오타와 시 |"],
        ["| Tottori | Tottori Prefecture | Japan | 1991 |",
         "| Wuhan | Hubei | China | 2000 |",
         "| Bellingham | Washington | United States | 2008 |",
         "| Rostov-on-Don | Rostov oblast | Russia | 1999 |",
         "| Wrocław | Lower Silesian Voivodeship | Poland | 2023 |"]),
    ("chuncheon", "춘천시의 전체 면적"): (
        ["면적: 1,116.35km2",
         "면적은 1,116.35 km2이고, 이 중 시내 동 면적은 52.66 km2이다.",
         "| 합계 | 합계 | 1,163.35 | 116,273 | 282,439 |"],
        ["Total: 1,166.8 km2 (450.5 sq mi)",
         "| Total | Total | 1,166.8 | 290,281 |"]),
    ("chuncheon", "춘천시 2015년 인구(첫 번째 인구 표)"): (
        ["| 2015 | 281,725 | +3.3% |"],
        ["| 2015 | 281,005 | +3.0% |"]),
    ("chuncheon", "춘천시 2020년 인구(첫 번째 인구 표)"): (
        ["| 2020 | 284,645 | +1.0% |"],
        ["| 2020 | 284,489 | +1.2% |"]),
    ("chuncheon", "3월 역대 최고 기온"): (
        ["| 역대 최고 기온 °C (°F) | 12.7 (54.9) | 19.9 (67.8) | 24.9 (76.8) | 32.0 (89.6) | 34.0 (93.2) | 36.4 (97.5) | 37.2 (99.0) | 39.5 (103.1) | 34.7 (94.5) | 28.5 (83.3) | 25.5 (77.9) | 16.6 (61.9) | 39.5 (103.1) |"],
        ["| Record high °C (°F) | 12.7 (54.9) | 19.9 (67.8) | 23.5 (74.3) | 32.0 (89.6) | 34.0 (93.2) | 36.4 (97.5) | 37.2 (99.0) | 39.5 (103.1) | 34.7 (94.5) | 28.5 (83.3) | 24.8 (76.6) | 16.6 (61.9) | 39.5 (103.1) |"]),
    ("chuncheon", "11월 역대 최고 기온"): (
        ["| 역대 최고 기온 °C (°F) | 12.7 (54.9) | 19.9 (67.8) | 24.9 (76.8) | 32.0 (89.6) | 34.0 (93.2) | 36.4 (97.5) | 37.2 (99.0) | 39.5 (103.1) | 34.7 (94.5) | 28.5 (83.3) | 25.5 (77.9) | 16.6 (61.9) | 39.5 (103.1) |"],
        ["| Record high °C (°F) | 12.7 (54.9) | 19.9 (67.8) | 23.5 (74.3) | 32.0 (89.6) | 34.0 (93.2) | 36.4 (97.5) | 37.2 (99.0) | 39.5 (103.1) | 34.7 (94.5) | 28.5 (83.3) | 24.8 (76.6) | 16.6 (61.9) | 39.5 (103.1) |"]),
    ("chuncheon", "연 강수량"): (
        ["| 평균 강수량 mm (인치) | 18.6 (0.73) | 27.6 (1.09) | 33.5 (1.32) | 71.5 (2.81) | 99.4 (3.91) | 122.9 (4.84) | 398.2 (15.68) | 319.9 (12.59) | 128.1 (5.04) | 49.3 (1.94) | 48.3 (1.90) | 24.2 (0.95) | 1,341.5 (52.81) |"],
        ["The annual precipitation is an average of 1347.3 mm.",
         "| Average precipitation mm (inches) | 18.6 (0.73) | 27.6 (1.09) | 33.5 (1.32) | 71.5 (2.81) | 99.4 (3.91) | 122.9 (4.84) | 398.2 (15.68) | 319.9 (12.59) | 128.1 (5.04) | 49.3 (1.94) | 48.3 (1.90) | 24.2 (0.95) | 1,341.5 (52.81) |"]),
    ("chuncheon", "효자2동 면적"): (
        ["| 효자2동 | 孝子2洞 | 1.16 | 6,783 | 12,183 |"],
        ["| Hyoja-2-dong | 효자2동 | 1.9 | 12,067 |"]),
    ("chuncheon", "효자3동 면적"): (
        ["| 효자3동 | 孝子3洞 | 0.85 | 2,676 | 5,070 |"],
        ["| Hyoja-3-dong | 효자3동 | 0.4 | 4,232 |"]),
    ("chuncheon", "1950년 춘천 전투에서 국군 6사단이 버틴 기간"): (
        ["국군 6사단은 3일간 적군과 대치하며 춘천을 확보했으나 육군본부 명령에 따라 충주로 철수하면서 인민군은 27일 저녁 10시가 되어서야 춘천을 점령할 수 있었다."],
        ["During the Battle of Chuncheon in 1950, the 6th Infantry Division of South Korea conducted a defense war for six days in Chuncheon and Hongcheon, delaying II Corps of North Korea's advance to the areas."]),
    ("chuncheon", "하이원 아이스하키단의 현재 상태"): (
        ["하이원 아이스하키단: 프로 아이스하키팀으로 아시아리그에 참가하며 춘천 의암실내빙상장을 홈구장으로 사용한다."],
        ["The club was a member of the Asia League Ice Hockey between 2005 and 2019. Founded in 2004, it was dissolved in 2023."]),
}
# S1: 사실 id -> 이유 글에 적힌 다른 쪽 자리들(사실 자신의 인용에 더한다). 읍면동·구별·산업별 합처럼 계산한 값은 원문에 없어 넣지 않았다.
S1_PLACES = {
    "부산광역시_en_01": ["It decreased from 3,513,777 in 2015 to 3,266,598 in 2024."],
    "부산광역시_en_12": ["Pusan National University Hospital with 1,300 beds in Ami-dong"],
    "부산광역시_en_13": ["Dong-A University Hospital with 999 beds in Dongdaesin-dong"],
    "강릉시_en_01": ["Total: 208,161",
        "| Gangneung-si | 강릉시 | 1,040 | 217,986 | 90,891 |"],
    "제주시_en_01": ["Total: 488,844",
        "(244,468 men and 245,136 women, May 2024)"],
    "천안시_ko_02": ["| 총계 | 총계 | 683,453 | 255,696 | 636.2 |"],
    "청주시_ko_06": ["| 총합계 | 총합계 | 380,651 | 846,691 | 940.33 | 4구 | 3읍 10면 30행정동 82법정동 |"],
    "광주광역시_ko_02": ["면적: 500.9 km2"],
    "경주시_ko_03": ["면적: 1,324.95km2"],
    "세종특별자치시_ko_01": ["인구: 392,230명(2025년)"],
    "세종특별자치시_ko_02": ["면적: 465.96 km2"],
    "세종특별자치시_ko_04": ["행정 구역: 1읍 9면 15행정동 23법정동",
        "행정구역은 1읍 9면 14 행정동 23 법정동이다."],
    "수원시_ko_01": ["| 수원시 | 水原市 | 121.05 | 1,209,169 |"],
    "수원시_ko_04": ["| 일일 평균 기온 °C (°F) | −2.1 (28.2) | 0.3 (32.5) | 5.7 (42.3) | 12.0 (53.6) | 17.6 (63.7) | 22.2 (72.0) | 25.3 (77.5) | 26.0 (78.8) | 21.4 (70.5) | 14.6 (58.3) | 7.2 (45.0) | 0.1 (32.2) | 12.5 (54.5) |"],
    "수원시_ko_05": ["연평균 강수량은 13,996.5 mm이다."],
    "수원시_ko_17": ["백운산(566 m)~광교산(581 m)을 비롯한 수원 북부 산악지대에 분포하며"],
    "전주시_ko_01": ["동경 126°59′∼127°14′, 북위 35°43′∼35°53′에 위치하고 있으며 면적은 206 km2이다."],
    "경주시_ko_06": ["| 평균 강수량 mm (인치) | 34.4 (1.35) | 45.2 (1.78) | 63.8 (2.51) | 82.9 (3.26) | 71.6 (2.82) | 128.8 (5.07) | 195.4 (7.69) | 172.7 (6.80) | 154.7 (6.09) | 63.3 (2.49) | 51.9 (2.04) | 26.2 (1.03) | 1,090.9 (42.93) |"],
    "세종특별자치시_ko_11": ["2023년 기준 인구는 약 38만 명에 이르렀으며, 2025년 기준으로 약 38만~39만 명 수준에서 유지되고 있다."],
    "광주광역시_ko_03": ["1986년 광주는 직할시로 승격되었으며, 1995년 지방자치제 실시와 함께 광역시로 전환되었다."],
    "세종특별자치시_ko_09": ["2015년경에는 인구가 약 20만 명을 돌파하였으며, 2017년에는 30만 명을 넘어섰고, 2020년에는 34만 명을 상회하였다."],
    "강릉시_en_03": ["As merger with Myeongju area: January 1, 1995"],
    "세종특별자치시_ko_03": ["세종특별자치시는 2012년 7월 충청남도 연기군 전체 지역, 공주시 장기면과 의당면·반포면의 일부, 충청북도 청원군 부용면을 관할로 설치되었다."],
}
used_s2 = set()


def places(city, what):
    """S2 항목의 (한국어 자리들, 영어 자리들). 둘 중 하나라도 비면 멈춘다."""
    used_s2.add((city, what))
    ko, en = S2_PLACES.get((city, what), ([], []))
    if not ko or not en:
        raise SystemExit(f"S2 항목({city}, {what})의 한국어·영어 자리가 비어 있음")
    return ko, en


for i, why in excluded.items():
    x = by_id[i]
    doc = f"wiki-{x['lang']}-{DOC[x['city']]}"
    add(S1, f"`{doc}`: {x['fact']} — {why}",
        doc_id=doc, quotes=[located(doc, x["quote"])] + verbatim(doc, S1_PLACES.get(i, [])), values=numbers(" ".join(x.get("keys_num", []))))
for f in sorted((HERE / "facts").glob("*_pair.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    city = DOC[d["city"]]
    for c in d.get("conflict", []):
        add(S2, f"`wiki-ko-{city}`와 `wiki-en-{city}`: {c['what']} — 한국어 {c['ko']}, 영어 {c['en']}",
            targets=[{"doc_id": f"wiki-{lang}-{city}", "values": numbers(str(c[lang])), "quotes": verbatim(f"wiki-{lang}-{city}", quotes)}
                     for lang, quotes in zip(("ko", "en"), places(city, c["what"]))])
if set(S2_PLACES) - used_s2 or set(S1_PLACES) - set(excluded):
    raise SystemExit(f"쓰이지 않은 키: {sorted(set(S2_PLACES) - used_s2)} {sorted(set(S1_PLACES) - set(excluded))}")
# 손으로 적은 줄: (문서, 줄 글, 줄에 인용된 원문 문장들, 값을 뽑을 글들[화씨·인치 환산 값과 덧붙인 날짜·메모는 뺀다])
OUTSIDE = [
    ("wiki-en-cheonan", "연평균 기온과 역대 최고·최저 기온 — 본문 \"The average temperature in the city is 12.5 °C, with a recorded high of 34.2 °C and a low of -13.4 °C.\", 기후 표 연평균 12.0 °C, 역대 최고 37.8 °C, 역대 최저 −23.9 °C (미정 목록 \"질문을 만들 때 지킬 것\" ②의 천안 연평균 기온)",
     ["The average temperature in the city is 12.5 °C, with a recorded high of 34.2 °C and a low of -13.4 °C.",
      "| Record high °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.9 (80.4) | 31.2 (88.2) | 33.9 (93.0) | 34.8 (94.6) | 37.7 (99.9) | 37.8 (100.0) | 34.1 (93.4) | 28.7 (83.7) | 25.3 (77.5) | 18.5 (65.3) | 37.8 (100.0) |",
      "| Daily mean °C (°F) | −2.4 (27.7) | 0.0 (32.0) | 5.3 (41.5) | 11.7 (53.1) | 17.5 (63.5) | 21.8 (71.2) | 24.9 (76.8) | 25.2 (77.4) | 20.2 (68.4) | 13.4 (56.1) | 6.5 (43.7) | −0.2 (31.6) | 12.0 (53.6) |",
      "| Record low °C (°F) | −23.9 (−11.0) | −19.9 (−3.8) | −10.4 (13.3) | −5.2 (22.6) | 2.0 (35.6) | 6.9 (44.4) | 12.5 (54.5) | 12.1 (53.8) | 3.0 (37.4) | −4.3 (24.3) | −10.4 (13.3) | −18.7 (−1.7) | −23.9 (−11.0) |"],
     ["12.5 °C", "34.2 °C", "13.4 °C", "12.0 °C", "37.8 °C", "23.9 °C"]),
    ("wiki-en-jeju", "6~9월 강수량 — 본문 \"more than 180 millimetres (7.1 in) of rain falling in each month from June to September\", 일도1동 기후 표의 6월 171.2 mm (2026-10-14 같은 문서 안의 다른 값을 찾던 서브에이전트가 사실 밖에서 본 것)",
     ["more than 180 millimetres (7.1 in) of rain falling in each month from June to September",
      "| Average precipitation mm (inches) | 67.5 (2.66) | 57.2 (2.25) | 90.6 (3.57) | 89.7 (3.53) | 95.6 (3.76) | 171.2 (6.74) | 210.2 (8.28) | 272.3 (10.72) | 227.8 (8.97) | 95.1 (3.74) | 69.5 (2.74) | 55.6 (2.19) | 1,502.3 (59.15) |"],
     ["180 millimetres", "171.2 mm"]),
    ("wiki-ko-gyeongju", "달마다의 평균 최고 기온 범위 — 본문 \"연평균 최고 기온은 8.6–31.1 °C (47–88 °F)이다\", 기후 표의 일평균 최고 기온은 가장 높은 달(8월)이 29.7 °C (같은 서브에이전트들이 사실 밖에서 본 것)",
     ["연평균 최고 기온은 8.6–31.1 °C (47–88 °F)이다",
      "| 일평균 최고 기온 °C (°F) | 5.7 (42.3) | 7.3 (45.1) | 11.9 (53.4) | 17.8 (64.0) | 22.8 (73.0) | 25.1 (77.2) | 28.7 (83.7) | 29.7 (85.5) | 25.1 (77.2) | 20.9 (69.6) | 14.6 (58.3) | 8.6 (47.5) | 18.2 (64.7) |"],
     ["8.6–31.1 °C", "29.7 °C"]),
    ("wiki-en-gangneung", "시로 설치된 해 — 정보 상자 \"City established: September 1, 1955\", 본문 \"Gangneung City was established in 1995 as the areas of Gangneung and Myeongju merged\" (2026-10-14 Codex 2차 지적 1)",
     ["City established: September 1, 1955", "Gangneung City was established in 1995 as the areas of Gangneung and Myeongju merged"],
     ["September 1, 1955", "in 1995"]),
    ("wiki-en-gangneung", "면적 — 정보 상자·표 1,040 km2, 본문 \"about 1,040.4 km2\" (2026-10-14, 반올림·어림도 다른 값으로 본다)",
     ["about 1,040.4 km2", "Total: 1,040 km2 (400 sq mi)", "| Gangneung-si | 강릉시 | 1,040 | 217,986 | 90,891 |"],
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
