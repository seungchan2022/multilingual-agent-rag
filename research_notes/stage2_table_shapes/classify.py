"""마크다운 표 100개를 모양별로 나눠 센다(이슈 #4 ⑤).

  uv run python research_notes/stage2_table_shapes/classify.py

extract.py가 만든 tables.json을 읽는다. 모양은 두 가지로 판정한다.
- 기계 판정: 원문 HTML 표의 구조(합친 칸, 칸 안의 줄바꿈 등)와 마크다운 줄에서 바로 정해지는 것.
- 읽어서 판정: AI가 tables_dump.md의 표 100개를 전부 읽고 고른 표. 아래 MANUAL에 표마다 이유를 적었다.
결과: shapes.json(모양마다 표 목록), shapes.md(사람이 읽는 보고). 처리 방법은 4단계에서 정한다.
"""
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TABLES = json.loads((HERE / "tables.json").read_text(encoding="utf-8"))
TABLES = TABLES["tables"] if isinstance(TABLES, dict) else TABLES
URL = {r["doc_id"]: r["source_url"]
       for r in yaml.safe_load((ROOT / "data/corpus/collected.yaml").read_text(encoding="utf-8"))["documents"]}


def key(doc, n):
    return f"{doc}#{n}"


def body_rows(t):
    return [[c.strip() for c in l.strip()[1:-1].split(" | ")] for l in t["md_lines"][2:]]


def count(v):
    return v.get("count", 0) if isinstance(v, dict) else (len(v) if isinstance(v, list) else (v or 0))


# 읽어서 판정한 모양. (모양 이름, 쉬운 뜻, {표: 이유})
MANUAL = [
    ("머리글 줄이 없는 표",
     "원문에 제목 줄이 없어, 첫 줄(내용)이 마크다운 표의 머리글 자리에 놓였다",
     {key("wiki-ko-cheongju", 3): "고속철도 노선과 역", key("wiki-ko-cheongju", 4): "일반철도 노선과 역",
      key("wiki-ko-cheongju", 5): "고속도로 이름과 나들목", key("wiki-ko-cheongju", 6): "일반 도로 번호와 도로 이름",
      key("wiki-ko-cheongju", 7): "버스 터미널과 운행", key("wiki-ko-chuncheon", 8): "철도 노선과 역",
      key("wiki-ko-chuncheon", 9): "고속도로 이름과 나들목", key("wiki-ko-chuncheon", 10): "일반 도로 번호와 도로 이름",
      key("wiki-ko-chuncheon", 11): "버스 터미널과 운행", key("wiki-ko-chuncheon", 13): "대학 종류와 학교 이름",
      key("wiki-ko-chuncheon", 14): "고등학교 종류와 학교 이름(세로로 긴 '고등학교' 칸만 있던 첫 줄을 지운 뒤)",
      key("wiki-en-gangneung", 4): "철도 노선과 역"}),
    ("한 줄에 여러 대상이 옆으로 놓인 표",
     "한 줄에 서로 다른 대상 여럿이 나란히 있어, 줄 하나가 대상 하나가 아니다",
     {key("wiki-ko-cheongju", 6): "도로 번호·도로 이름 짝 4개가 한 줄에",
      key("wiki-ko-cheongju", 7): "터미널·운행 짝 2개가 한 줄에",
      key("wiki-ko-chuncheon", 10): "도로 번호·도로 이름 짝 3개가 한 줄에",
      key("wiki-ko-chuncheon", 11): "터미널·운행 짝 2개가 한 줄에",
      key("wiki-ko-chuncheon", 13): "같은 종류의 학교 이름이 여러 열에 흩어짐",
      key("wiki-ko-chuncheon", 14): "같은 종류의 학교 이름이 여러 열에 흩어짐"}),
    ("머리글이 두 줄인 표",
     "제목 줄이 두 줄이라, 마크다운에서는 둘째 제목 줄이 내용 줄처럼 놓였다",
     {key("wiki-en-gangneung", 3): "1줄: 국가 지정/도 지정, 2줄: 국보·보물 등"}),
    ("같은 머리글이 여러 열에 붙은 표",
     "가로로 합친 제목 칸이 펴져, 서로 다른 열이 같은 이름을 가졌다",
     {key("wiki-en-gangneung", 3): "State-designated heritage가 9열, Province-designated heritage가 5열",
      key("wiki-ko-suwon", 6): "지방자치단체 2열(국내 도시는 시·도와 시·군, 외국 도시는 나라와 도시)",
      key("wiki-ko-cheongju", 8): "도시 2열(시·도·주와 시·군·구)",
      key("wiki-ko-sejong", 4): "구분 2열(이전 단계와 분야)"}),
    ("머리글 칸이 일부만 찬 표",
     "제목 줄의 칸 대부분이 비어 있다 (2026-10-14 변환 규칙을 고쳐 춘천 고등학교 표의 그 줄을 지웠다. 지금은 없다)",
     {}),
    ("표 중간에 머리글이 다시 나오는 표",
     "표 중간에 제목 줄이 한 번 더 있어, 그 아래 줄은 첫 제목이 아니라 새 제목에 속한다",
     {key("wiki-ko-gwangju", 14): "박물관 6줄 뒤에 '미술관 | 주소 | 홈페이지' 줄"}),
    ("합계 줄이 있는 표",
     "대상 줄들의 앞이나 사이나 끝에 그 합계 줄이 있다",
     {key("wiki-ko-jeonju", 2): "끝 줄 전주시", key("wiki-ko-cheongju", 2): "끝 줄 총합계",
      key("wiki-ko-chuncheon", 3): "끝 줄 합계", key("wiki-en-chuncheon", 3): "끝 줄 Total",
      key("wiki-ko-cheonan", 2): "구 소계 2줄과 끝 줄 총계", key("wiki-ko-suwon", 5): "끝 줄 수원시",
      key("wiki-ko-gyeongju", 4): "끝 줄 경주시", key("wiki-ko-sejong", 1): "끝 줄 세종특별자치시",
      key("wiki-ko-gwangju", 2): "끝 줄 광주광역시", key("wiki-en-gangneung", 2): "끝 줄 Gangneung-si",
      key("wiki-ko-sejong", 4): "첫 줄 36개 기관", key("wiki-ko-gwangju", 10): "첫 줄 합계",
      key("wiki-ko-gwangju", 7): "매출액 합계, 수출액 합계 줄"}),
    ("줄의 소속이 순서로만 드러나는 표",
     "줄 이름만으로는 무엇에 속한 줄인지 알 수 없고, 위나 아래의 줄을 봐야 안다",
     {key("wiki-ko-cheonan", 2): "동 줄들 뒤에 그 동들이 속한 구의 소계 줄(서북구, 동남구)",
      key("wiki-ko-gwangju", 7): "'완성차'·'부품' 줄이 두 번 나오고, 위의 합계 줄(매출액, 수출액)에 따라 뜻이 갈린다"}),
    ("줄 이름이 없는 표",
     "줄마다 무엇을 센 값인지 적힌 칸이 없다",
     {key("wiki-ko-gyeongju", 8): "학생 수 줄과 교직원 수 줄에 이름이 없고, 표 위 제목('학생 · 교직원 현황')으로만 짐작된다"}),
    ("열이 달·해·종류로 나뉜 표",
     "맨 윗줄이 달·해·종류처럼 한 항목을 나눈 칸이고, 맨 왼쪽 열은 무엇을 센 값인지를 적는다. 그래서 값 하나의 뜻에 줄 이름과 열 이름이 둘 다 필요하다",
     {**{key(d, n): "기후 표" for d, n in [
         ("wiki-ko-jeonju", 1), ("wiki-en-jeonju", 1), ("wiki-ko-cheongju", 1), ("wiki-en-cheongju", 1),
         ("wiki-ko-chuncheon", 1), ("wiki-en-chuncheon", 4), ("wiki-ko-cheonan", 1), ("wiki-en-cheonan", 1),
         ("wiki-en-busan", 1), ("wiki-en-jeju", 2), ("wiki-en-jeju", 3), ("wiki-en-jeju", 4), ("wiki-en-jeju", 5),
         ("wiki-en-andong", 2), ("wiki-en-gangneung", 1), ("wiki-ko-suwon", 1), ("wiki-ko-gyeongju", 2),
         ("wiki-ko-gwangju", 1)]},
      key("wiki-ko-suwon", 3): "산업별 사업체 수(2009년, 2018년, 증감율)",
      key("wiki-ko-gyeongju", 7): "의료시설 건수·병상수", key("wiki-ko-gyeongju", 8): "학생·교직원 수",
      key("wiki-ko-gwangju", 7): "자동차 생산·매출·수출", key("wiki-ko-gwangju", 10): "기업 수",
      key("wiki-ko-gwangju", 11): "제조업체 수", key("wiki-ko-gwangju", 12): "고용·업체·매출",
      key("wiki-ko-gwangju", 13): "고용·기업체·매출"}),
]

# 기계 판정. (모양 이름, 쉬운 뜻, 판정 함수)
AUTO = [
    ("세로로 합친 칸이 있는 표", "칸 하나가 아래로 여러 줄에 걸쳐 있었다. 마크다운에서는 같은 글자가 줄마다 되풀이된다",
     lambda t: count(t["rowspan_cells"]) > 0),
    ("가로로 합친 칸이 있는 표", "칸 하나가 옆으로 여러 칸에 걸쳐 있었다(표 전체 너비의 줄은 뺀다)",
     lambda t: count(t["colspan_cells"]) > 0),
    ("칸 안에 줄바꿈이 있는 표", "칸 하나 안에서 줄이 바뀌었다. 마크다운에서는 빈칸 하나가 된다",
     lambda t: count(t["br_cells"]) > 0),
    ("칸 안에 목록이 있는 표", "칸 하나 안에 점 목록이 있었다. 마크다운에서는 쉼표로 이어진다",
     lambda t: count(t["list_cells"]) > 0),
    ("내용 줄이 없는 표", "마크다운 표가 머리글 자리 한 줄뿐이다",
     lambda t: len(t["md_lines"]) <= 2),
    ("모든 칸이 빈 줄이 있는 표", "내용 줄 가운데 모든 칸이 빈 줄이 있다",
     lambda t: any(all(c == "" for c in r) for r in body_rows(t))),
    ("통계 표", "공공데이터포털의 CSV를 옮긴 표(원문 HTML이 없다)",
     lambda t: t["doc_id"].startswith("portal-")),
]

md = [t for t in TABLES if t["outcome"] == "markdown"]
by = {key(t["doc_id"], t["n"]): t for t in md}
for name, _, items in MANUAL:
    missing = [k for k in items if k not in by]
    assert not missing, f"{name}: 마크다운 표가 아님 {missing}"

shapes = []
for name, meaning, items in MANUAL:
    shapes.append({"shape": name, "meaning": meaning, "how": "읽어서 판정",
                   "tables": [{"table": k, "note": v} for k, v in items.items()]})
for name, meaning, f in AUTO:
    wiki_only = name != "통계 표"
    pool = [t for t in md if (not wiki_only or t["doc_id"].startswith("wiki-"))]
    shapes.append({"shape": name, "meaning": meaning, "how": "기계 판정",
                   "tables": [{"table": key(t["doc_id"], t["n"]), "note": ""} for t in pool if f(t)]})

plain = [key(t["doc_id"], t["n"]) for t in md if key(t["doc_id"], t["n"]) not in
         {x["table"] for s in shapes for x in s["tables"]}]
shapes.append({"shape": "위 모양이 하나도 없는 표", "meaning": "제목 줄 한 줄, 줄마다 대상 하나인 표",
               "how": "기계 판정(위 목록의 나머지)", "tables": [{"table": k, "note": ""} for k in plain]})

# 지난 세션의 HTML 수(116, 52, 30, 17, 7)와 견주려고, 원문 표 전체(위키백과 HTML 표와 통계 표 CSV, 틀로 풀린 표 포함)에서도 센다.
all_calls = {
    "table_items가 받은 위키백과 원문 HTML 표": sum(t["doc_id"].startswith("wiki-") for t in TABLES),
    "table_items가 받은 통계 표(CSV)": sum(t["doc_id"].startswith("portal-") for t in TABLES),
    "마크다운 표가 됨": sum(t["outcome"] == "markdown" for t in TABLES),
    "틀로 풀림": sum(t["outcome"] == "frame" for t in TABLES),
    "비어서 빠짐": sum(t["outcome"] == "empty" for t in TABLES),
    "칸을 합친 표(세로나 가로)": sum(count(t.get("rowspan_cells")) + count(t.get("colspan_cells")) > 0 for t in TABLES),
    "칸 안에 줄바꿈이 있는 표": sum(count(t.get("br_cells")) > 0 for t in TABLES),
    "칸 안에 목록이 있는 표": sum(count(t.get("list_cells")) > 0 for t in TABLES),
    "표 안에 표가 있는 것": sum(bool(t.get("nested")) for t in TABLES),
    "칸을 합쳤거나 표 전체 너비의 줄이 있는 표": sum(
        count(t.get("rowspan_cells")) + count(t.get("colspan_cells")) > 0 or bool(t.get("full_width_rows")) for t in TABLES),
}

# 사용자가 2026-10-12에 짚은 모양(한 칸에 값이 둘 들어 줄끼리 짝을 이루는 표. 예: `축구 \n 농구`, `11 \n 5`).
# extract.py가 고른 후보(한 줄에서 칸 둘 이상이 같은 수의 조각으로 나뉜 줄이 있는 표)를 AI가 전부 읽은 결과.
CLIMATE = {k for k, v in MANUAL[-1][2].items() if v == "기후 표"}
PAIR_NOTES = {
    key("wiki-en-chuncheon", 3): "제목 칸 안의 단위 줄(Area / (km2))",
    key("wiki-ko-gyeongju", 8): "제목 칸 안의 구분 줄(고등학교 / (일반계))",
    key("wiki-ko-gwangju", 7): "제목 칸 안의 구분 줄(2013 / (추정))",
    key("wiki-ko-gwangju", 8): "한 칸의 설명 글이 줄을 넘긴 것. 옆 칸과 짝을 이루지 않는다",
    key("wiki-ko-gwangju", 12): "제목 칸 안의 구분 줄(1999년 / (육성이전))",
}
pair = []
for t in md:
    if not count(t.get("pair_rows")):
        continue
    k = key(t["doc_id"], t["n"])
    note = "같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다" if k in CLIMATE else PAIR_NOTES[k]
    pair.append({"table": k, "note": note})

out = {"markdown_tables": len(md), "shapes": shapes, "all_source_tables": all_calls,
       "pair_candidates": pair, "pair_found": 0}
(HERE / "shapes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# 영어 절 이름의 한국어 뜻(사용자가 영어를 읽지 않는다).
KO = {"Administrative divisions": "행정 구역", "Climate": "기후", "Culture": "문화", "Heritage": "문화유산",
      "Culture and attractions": "문화와 명소", "Festivals": "축제", "Media": "언론", "Demographics": "인구",
      "Festivals and events": "축제와 행사", "Geography": "지리",
      "Geography and administrative divisions": "지리와 행정 구역", "Medical facilities": "의료 시설",
      "Major medical centers": "주요 병원", "Population": "인구", "Sister cities": "자매 도시", "Sports": "스포츠",
      "Transportation": "교통", "Trains": "철도", "Twin towns – sister cities": "자매 도시"}


def where(k):
    t = by[k]
    parts = [s.lstrip("# ") for s in (t.get("section") or "").split(" / ") if s]
    sec = " / ".join(f"{s}({KO[s]})" if s in KO else s for s in parts)
    return f"`data/corpus/markdown/{t['doc_id']}.md` {t['md_line_no']}번째 줄 · 원문 {URL[t['doc_id']]} · 절: {sec}"


lines = ["# 마크다운 표의 모양", "",
         "`classify.py`가 `tables.json`에서 만든다. 표 하나가 여러 모양에 들 수 있다. 처리 방법은 4단계에서 정한다.", "",
         f"마크다운 표 {len(md)}개(위키백과 {sum(t['doc_id'].startswith('wiki-') for t in md)}, 통계 표 {sum(t['doc_id'].startswith('portal-') for t in md)}).", "",
         "| 모양 | 판정 | 표 수 |", "|---|---|---|"]
lines += [f"| {s['shape']} | {s['how']} | {len(s['tables'])} |" for s in shapes]
lines += ["", "## 원문 표 전체(틀로 풀린 표 포함)", "",
          "변환 코드가 받은 원문 표 가운데 마크다운 표가 되지 않은 것: 틀로 풀린 표는 목록이나 표를 옆으로 나란히 놓으려고 "
          "표의 틀만 빌린 것이라, 표로 옮기지 않고 칸의 내용을 위에서 아래로 적었다(`decisions/stage2.md` 2026-10-14 "
          "표 규칙 ㉣㉤). 비어서 빠진 표는 글자가 없는 표다(춘천 한국어 문서 '교육 기관' 절).", "",
          "| 항목 | 수 |", "|---|---|"]
lines += [f"| {k} | {v} |" for k, v in all_calls.items()]
lines += ["", f"## 한 칸에 값이 둘 들어 줄끼리 짝을 이루는 표 (0개)", "",
          f"후보 표 {len(pair)}개(한 줄에서 칸 둘 이상이 같은 수의 조각으로 나뉜 줄이 있는 표)를 AI가 전부 읽었다. 짝을 이루는 표는 없었다.", ""]
lines += [f"- {x['table']} — {x['note']}" for x in pair]
for s in shapes:
    lines += ["", f"## {s['shape']} ({len(s['tables'])}개)", "", s["meaning"] + ".", ""]
    lines += [f"- {x['table']}" + (f" — {x['note']}" if x["note"] else "") + f"  \n  {where(x['table'])}" for x in s["tables"]]
(HERE / "shapes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines[:len(shapes) + 20]))
