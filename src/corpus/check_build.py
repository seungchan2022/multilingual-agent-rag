"""build.py가 만든 마크다운 28개를 검사하는 프로그램.

  uv run python src/corpus/check_build.py

data/corpus/markdown/의 글자를 읽어 항목마다 통과/실패를 한 줄씩 출력하고, 실패가 있으면 종료 코드 1로 끝낸다.
변환 코드(build.py)를 불러 쓰지 않는다. 글자를 찾고 줄을 찾는 단순한 검사만 한다.
마지막 항목만 build.py를 하위 프로세스로 두 번 실행해 결과 파일의 해시를 견준다.
"""
import csv, hashlib, html, io, itertools, json, re, subprocess, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"

DOCS = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
WIKI = [d for d in DOCS if d["doc_id"].startswith("wiki-")]
TEXT = {}   # doc_id -> 마크다운 글자 (없으면 빠짐)
for d in DOCS:
    p = MARKDOWN / f"{d['doc_id']}.md"
    if p.is_file():
        TEXT[d["doc_id"]] = p.read_text(encoding="utf-8")
LINES = {k: v.split("\n") for k, v in TEXT.items()}

results = []


def report(name, problems):
    """problems가 비면 통과, 아니면 실패하고 이유를 들여 써서 보인다."""
    results.append(not problems)
    print(f"{'통과' if not problems else '실패'}  {name}")
    for p in problems[:10]:
        print(f"      {p}")
    if len(problems) > 10:
        print(f"      ... 외 {len(problems) - 10}건")


def next_line(doc, i):
    """i번째 줄 다음의 빈 줄이 아닌 줄."""
    for l in LINES[doc][i + 1:]:
        if l.strip():
            return l
    return ""


def has_line(doc, prefix):
    return any(l.startswith(prefix) for l in LINES.get(doc, []))


# 1
bad = []
for d in WIKI:
    t = TEXT.get(d["doc_id"])
    if t is None:
        bad.append(f"{d['doc_id']}: 파일이 없음")
    elif t.split("\n")[0] != f"# {d['title']}":
        bad.append(f"{d['doc_id']}: 첫 줄이 '# {d['title']}'가 아님")
report(f"1. 파일 {len(WIKI)}개가 모두 있고 첫 줄이 '# 제목'", bad)

# 2
BANNED = ["[편집", "[edit", "원본 편집", "출처 필요", "citation needed", "<img", "<br", "<td", "<table",
          "http://", "https://"]
# 주소 글자를 허용하는 곳: 표의 칸 전체가 주소인 곳(광주 한국어 박물관·미술관 표의 '홈페이지' 열)과
# 정보 상자의 '- 웹사이트:' / '- Website:' 줄, 관광공사 글의 '홈페이지:' / 'Homepage:' 줄. 그 밖의 주소는 실패다.
URL_CELL = re.compile(r"\|\s*https?://\S*\s*(?=\|)")
SITE_LINE = re.compile(r"^((  )?- (웹사이트|Website)|홈페이지|Homepage): https?://\S+$")
bad = [f"{k}:{n} '{w}'" for k, ls in LINES.items() for n, l in enumerate(ls, 1)
       if not SITE_LINE.match(l) for w in BANNED if w in URL_CELL.sub("|", l)]
report("2. 편집 표시, 태그 찌꺼기, 주소가 없다 (표 칸 전체가 주소인 곳, 정보 상자 웹사이트 줄, 관광공사 홈페이지 줄은 제외)", bad)

# 3
HEADS = ["같이 보기", "외부 링크", "각주", "내용주", "참고 문헌", "See also", "External links", "References",
         "Notes", "출신 인물", "갤러리"]
bad = [f"{k}:{n} '{l}'" for k, ls in LINES.items() for n, l in enumerate(ls, 1) if l in {f"## {h}" for h in HEADS}]
report("3. 지우기로 한 절 제목이 없다", bad)

# 4
bad = []
for d in WIKI:
    if d["language"] != "en" or d["doc_id"] not in TEXT:
        continue
    raw = (CORPUS / "raw" / f"{d['doc_id']}.html").read_text(encoding="utf-8")
    if not re.search(r"<h[2-6][^>]*>(?:<[^>]*>)*Notable people", raw):
        continue
    ls = LINES[d["doc_id"]]
    idx = [i for i, l in enumerate(ls) if re.match(r"#+ Notable people", l)]
    if not idx:
        bad.append(f"{d['doc_id']}: Notable people 절이 없음")
    else:
        level = len(ls[idx[0]].split(" ")[0])
        body = []
        for l in ls[idx[0] + 1:]:
            if l.startswith("#") and len(l.split(" ")[0]) <= level:
                break
            if l.strip() and not l.startswith("#"):
                body.append(l)
        if not body:
            bad.append(f"{d['doc_id']}: Notable people 아래에 글이 없음")
report("4. 영어 문서의 Notable people 절이 글과 함께 남아 있다", bad)


# 5
def cells(line):
    return len(re.split(r"(?<!\\)\|", line)) - 2


bad = []
for k, ls in LINES.items():
    head = None
    for n, l in enumerate(ls, 1):
        if l.startswith("|"):
            if head is None:
                head = cells(l)
            elif cells(l) != head:
                bad.append(f"{k}:{n} 열 {cells(l)}개, 머리글은 {head}개")
        else:
            head = None
report("5. 표의 모든 줄이 머리글 줄과 열 수가 같다", bad)

# 6
doc = "wiki-ko-jeonju"
EXPECT = ["- 전주시 全州市", "- 행정", "  - 행정 구역: 2구 35행정동 82법정동",
          "  - 청사 소재지: 전북특별자치도 전주시 완산구 노송광장로 10", "  - 단체장: 조지훈(더불어민주당)",
          "  - 국회의원: 갑: 김윤덕(더불어민주당) 을: 이성윤(더불어민주당) 병: 정동영(더불어민주당)",
          "- 지리", "  - 면적: 205.5 km2", "- 인문", "  - 인구: 655,879명(2022년 3월년)", "- 상징",
          "  - 시목: 은행나무", "  - 시화: 개나리", "  - 시조: 까치", "  - 동물: 독수리", "- 지역 부호",
          "  - 웹사이트: https://www.jeonju.go.kr/"]
t = TEXT.get(doc, "")
bad = [] if LINES.get(doc, [])[2:2 + len(EXPECT)] == EXPECT else ["정보 상자 줄이 들여 쓰기까지 기대와 같지 않음"]
bad += [f"있으면 안 되는 글자: {w}" for w in ["휘장", "전주시의 위치"] if w in t]
if "  - 웹사이트: https://www.jeonju.go.kr/" not in LINES.get(doc, []):
    bad.append("'  - 웹사이트: https://www.jeonju.go.kr/' 줄이 없음")
if not has_line(doc, "| 1949년 | 100,624명 |"):
    bad.append("'| 1949년 | 100,624명 |'로 시작하는 줄이 없음")
elif cells(next(l for l in LINES[doc] if l.startswith("| 1949년 | 100,624명 |"))) != 3:
    bad.append("1949년 줄의 열이 3개가 아님")
if not has_line(doc, "| 1950 | 83,000 |"):
    bad.append("'| 1950 | 83,000 |'로 시작하는 줄이 없음")
if "## 국제 교류" not in LINES.get(doc, []):
    bad.append("'## 국제 교류'가 없음")
if re.search(r"전북대학교병원\s*\[a\]", t):
    bad.append("전북대학교병원 뒤에 [a]가 있음")
report("6. 전주 한국어: 정보 상자, 인구 표 둘, 국제 교류, 각주 글자 표시", bad)

# 7
doc = "wiki-ko-cheongju"
ls = LINES.get(doc, [])
bad = []
if not any("17 국도 제17호선" in l and "청남로, 상당로, 공항로" in l for l in ls):
    bad.append("'17 국도 제17호선'과 '청남로, 상당로, 공항로'가 든 줄이 없음")
if not any("고속국도 제1호선" in l and "경부고속도로" in l for l in ls):
    bad.append("'고속국도 제1호선'과 '경부고속도로'가 든 줄이 없음")
report("7. 청주 한국어: 도로 표지의 대체 글자가 표 줄에 있다", bad)

# 8
doc = "wiki-ko-chuncheon"
ls = LINES.get(doc, [])
bad = []
for head, item in [("#### 유원지/휴양지", "- 강원숲체험장"), ("#### 섬/호수", "- 남이섬")]:
    if head not in ls:
        bad.append(f"'{head}'가 없음")
    elif not next_line(doc, ls.index(head)).startswith(item):
        bad.append(f"'{head}' 다음이 '{item}'이 아님")
if "지방도 제403호선" not in TEXT.get(doc, ""):
    bad.append("'지방도 제403호선'이 없음")
report("8. 춘천 한국어: 틀로 쓰인 표가 제목과 목록으로 풀렸고 도로 표지가 있다", bad)

# 9
doc = "wiki-ko-suwon"
ls = LINES.get(doc, [])
bad = []
row = "| 자매도시 | 독일 | 프라이부르크시 |"
if row not in ls:
    bad.append(f"'{row}' 줄이 없음")
else:
    i = ls.index(row)
    while i > 0 and ls[i - 1].startswith("|"):
        i -= 1
    if ls[i] != "| 자매결연도시 | 지방자치단체 | 지방자치단체 |":
        bad.append(f"그 표의 머리글 줄이 '{ls[i]}'")
report("9. 수원 한국어: 칸을 합친 교류 도시 표", bad)

# 10
doc = "wiki-ko-gyeongju"
t = TEXT.get(doc, "")
s = "경운기 전용 도로가 설치되어 있다."
bad = []
if s not in t:
    bad.append(f"'{s}'가 없음")
elif any(t[m.end():m.end() + 1] == "[" for m in re.finditer(re.escape(s), t)):
    bad.append("그 문장 뒤에 '['가 붙어 있음")
report("10. 경주 한국어: 문장 뒤의 각주 글자 표시가 없다", bad)

# 11
doc = "wiki-ko-sejong"
t, ls = TEXT.get(doc, ""), LINES.get(doc, [])
bad = []
if "출처가 분명하지 않습니다" in t:
    bad.append("'출처가 분명하지 않습니다'가 있음")
bad += [f"'{h}'가 있음" for h in ["## 국회의원", "## 교육감"] if h in ls]
if "## 인구" not in ls:
    bad.append("'## 인구'가 없음")
report("11. 세종 한국어: 알림 상자 글, 빈 절이 없고 인구 절이 있다", bad)

# 12
doc = "wiki-ko-gwangju"
ls = LINES.get(doc, [])
bad = []
for h in ["자매도시", "우호도시"]:
    if h not in ls:
        bad.append(f"'{h}' 한 줄이 없음")
    elif not next_line(doc, ls.index(h)).startswith("| 국가 | 도시 |"):
        bad.append(f"'{h}' 다음이 '| 국가 | 도시 |' 표가 아님")
report("12. 광주 한국어: 겹친 표를 풀어 머리글을 안의 표 위에 적었다", bad)

# 13
doc = "wiki-en-busan"
t, ls = TEXT.get(doc, ""), LINES.get(doc, [])
bad = [f"없어야 하는 글자: {w}" for w in ["Climate chart", "Interactive map", "Wordmark"] if w in t]
bad += [f"있어야 하는 글자: {w}" for w in ["Climate data for Busan", "Religion in Busan (2024)",
                                       "Not religious (45.0%)"] if w not in t]
coords = [l for l in ls if "Coordinates:" in l]
if not coords:
    bad.append("Coordinates: 줄이 없음")
for l in coords:
    if l.count("°") != 2 or "/" in l:
        bad.append(f"좌표 표기가 한 벌이 아님: {l}")
report("13. 부산 영어: 기후 도표, 정보 상자 이름표가 없고 원그래프 글, 좌표 한 벌이 있다", bad)

# 14
doc = "wiki-en-jeonju"
first = next((l for l in LINES.get(doc, [])[1:] if l.strip() and not l.startswith(("-", "#", " "))), "")
report("14. 전주 영어: 첫 문단에 발음 기호가 있다",
       [] if "Korean pronunciation: [t͡ɕʌɲ.d͡ʑu]" in first else ["첫 문단에 'Korean pronunciation: [t͡ɕʌɲ.d͡ʑu]'가 없음"])


# 16
bad = []
for k, ls in LINES.items():
    for n, l in enumerate(ls, 1):
        if not l.startswith("|"):
            continue
        cs = [c.strip() for c in re.split(r"(?<!\\)\|", l)[1:-1]]
        run = max((sum(1 for _ in g) for _, g in itertools.groupby(cs) if _), default=0)
        if run >= 3 and re.match(r"\| ?(출처|Source|자료|의료인력)", l):
            bad.append(f"{k}:{n} {l[:60]}")
doc = "wiki-ko-jeonju"
ls = LINES.get(doc, [])
src = "출처: 기상청 (평년값: 1991년~2020년, 극값: 1918년~현재)"
last = max((i for i, l in enumerate(ls) if l.startswith("| 평균 월간 일조시간 |")), default=-1)
if src not in ls:
    bad.append(f"{doc}: 보통 줄 '{src}'가 없음")
elif last < 0 or ls.index(src) <= last:
    bad.append(f"{doc}: '{src}'가 기후 표의 마지막 줄보다 뒤에 있지 않음")
report("16. 표 줄에 출처·자료 줄이 열마다 되풀이되지 않고, 전주 한국어는 기후 표 아래에 보통 줄로 있다", bad)

# 17
bad = []
ls = LINES.get("wiki-ko-gyeongju", [])
heads = [l for l in ls if l.startswith("| 구분 | 종합병원 |")]
if not heads:
    bad.append("경주: '| 구분 | 종합병원 |' 머리글 줄이 없음")
elif not heads[0].endswith("| 합계 |"):
    bad.append(f"경주: 머리글 줄이 '| 합계 |'로 끝나지 않음: {heads[0][-30:]}")
if "| 자치구 | 공원명 | 주소 |" not in LINES.get("wiki-ko-gwangju", []):
    bad.append("광주: '| 자치구 | 공원명 | 주소 |' 줄이 없음")
report("17. 경주 의료시설 표의 빈 열이 사라졌고 광주 공원 표의 같은 열이 합쳐졌다", bad)

# 18
report("18. 부산 영어에 웹사이트 주소 줄이 있다",
       [] if "- Website: https://www.busan.go.kr/eng/index" in LINES.get("wiki-en-busan", []) else
       ["'- Website: https://www.busan.go.kr/eng/index' 줄이 없음"])

# 19
bad = []
for d in DOCS:
    t = TEXT.get(d["doc_id"])
    if t is None:
        bad.append(f"{d['doc_id']}: 파일이 없음")
    elif t.split("\n")[0] != f"# {d['title']}":
        bad.append(f"{d['doc_id']}: 첫 줄이 '# {d['title']}'가 아님")
report(f"19. 파일 {len(DOCS)}개가 모두 있고 첫 줄이 '# 제목'", bad)

# 관광공사 글 10개: 원본 JSON에서 칸을 따로 읽는다(변환 코드를 부르지 않는다).
KTO = {}
for d in DOCS:
    if d["doc_id"].startswith("kto-"):
        it = json.loads((CORPUS / "raw" / f"{d['doc_id']}.json").read_text(encoding="utf-8"))["response"]["body"]["items"]["item"]
        KTO[d["doc_id"]] = it[0] if isinstance(it, list) else it


def kto_head(d, it):
    """원본 칸에서 기대하는 주소 줄과 홈페이지 줄."""
    en = d["language"] == "en"
    hp = (it.get("homepage") or "").strip()
    if "<" in hp:
        hp = re.sub(r"<[^>]*>", "", hp).strip()  # 이 원본에서 태그는 <a>뿐이다
    return [("Address" if en else "주소", (it.get("addr1") or "").strip()),
            ("Homepage" if en else "홈페이지", hp)]


# 20
bad = []
for d in DOCS:
    if d["doc_id"] not in KTO:
        continue
    ls = LINES.get(d["doc_id"], [])
    for label, value in kto_head(d, KTO[d["doc_id"]]):
        if value and f"{label}: {value}" not in ls:
            bad.append(f"{d['doc_id']}: '{label}: {value}' 줄이 없음")
        if not value and any(l.startswith(f"{label}:") for l in ls):
            bad.append(f"{d['doc_id']}: 원본 칸이 비었는데 '{label}:' 줄이 있음")
    t = TEXT.get(d["doc_id"], "")
    bad += [f"{d['doc_id']}: '{w}'가 있음" for w in ["<br", "&nbsp;", "&ldquo;", "<a "] if w in t]
report("20. 관광공사 10개: 주소·홈페이지 줄이 원본 칸과 맞고 태그, 문자 참조가 없다", bad)

# 21
doc = "kto-en-jeju-ara-dong-trail"
ls, t = LINES.get(doc, []), TEXT.get(doc, "")
bad = []
if "Homepage: https://visitjeju.net/kr/" not in ls:
    bad.append("'Homepage: https://visitjeju.net/kr/' 줄이 없음")
if any(l.startswith("Address:") for l in ls):
    bad.append("'Address:' 줄이 있음")
if "“Crash Landing on You (2019).”" not in t:
    bad.append("'“Crash Landing on You (2019).”'가 없음")
a = [i for i, l in enumerate(ls) if l.endswith("Songaksan Mountain Cave Fortification.")]
b = [i for i, l in enumerate(ls) if l.startswith("The area around Kaldaripokpo Falls")]
if not a or not b or set(a) & set(b):
    bad.append("두 문장이 서로 다른 줄에 있지 않음")
report("21. 제주 아라동 영어: 홈페이지 줄, 주소 줄 없음, 인용 글자, 문단 나뉨", bad)

# 22
doc = "kto-ko-cheonan-samgeori-park"
report("22. 천안삼거리공원 한국어: 제목과 소개 글", [] if LINES.get(doc, [""])[0] == "# 천안삼거리공원"
       and "1970년대 조성한 공원이다" in TEXT.get(doc, "") else ["첫 줄이 '# 천안삼거리공원'이 아니거나 문장이 없음"])

# 23
bad = []
for d in DOCS:
    if d["doc_id"] not in KTO:
        continue
    ov = re.sub(r"<br\s*/?>", "", KTO[d["doc_id"]].get("overview") or "", flags=re.I)
    want = re.sub(r"\s+", "", html.unescape(ov))
    heads = {f"{label}: {value}" for label, value in kto_head(d, KTO[d["doc_id"]]) if value}
    rest = [l for l in LINES.get(d["doc_id"], [])[1:] if l not in heads]
    got = re.sub(r"\s+", "", "".join(rest))
    if want != got:
        bad.append(f"{d['doc_id']}: 소개 글 글자가 다름(원본 {len(want)}자, 마크다운 {len(got)}자)")
report("23. 관광공사 10개: 소개 글의 글자가 빠지거나 더해지지 않았다", bad)

# 24
bad = []
for d in DOCS:
    if not d["doc_id"].startswith("portal-"):
        continue
    raw = (CORPUS / "raw" / f"{d['doc_id']}.csv").read_bytes().decode("cp949")
    rows = [[c.strip() for c in r] for r in csv.reader(io.StringIO(raw, newline="")) if r]
    md = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l)[1:-1]]
          for l in LINES.get(d["doc_id"], []) if l.startswith("|")]
    if len(md) < 2:
        bad.append(f"{d['doc_id']}: 표가 없음")
        continue
    data = md[2:]  # 0: 머리글, 1: |---|
    if len(data) != len(rows) - 1:
        bad.append(f"{d['doc_id']}: 자료 줄 {len(data)}개, CSV는 {len(rows) - 1}개")
    if md[0] != rows[0]:
        bad.append(f"{d['doc_id']}: 머리글 칸이 CSV 첫 줄과 다름")
    for i, (a, b) in enumerate(zip(data, rows[1:]), 1):
        if a != b:
            bad.append(f"{d['doc_id']}: 자료 {i}번째 줄이 CSV와 다름")
            break
report("24. 통계 표 2개: 줄 수, 머리글, 모든 값이 CSV와 같다", bad)

# 25
bad = []
rows = (yaml.safe_load((CORPUS / "collected.yaml").read_text(encoding="utf-8")) or {}).get("documents") or []
by = {r["doc_id"]: r for r in rows}
for d in DOCS:
    r = by.get(d["doc_id"])
    p = MARKDOWN / f"{d['doc_id']}.md"
    if not r or not r.get("markdown_file") or not r.get("markdown_sha256"):
        bad.append(f"{d['doc_id']}: markdown_file/markdown_sha256이 없음")
    elif not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != r["markdown_sha256"]:
        bad.append(f"{d['doc_id']}: 해시가 파일과 다름")
report(f"25. collected.yaml의 {len(DOCS)}줄에 마크다운 파일과 해시가 있고 맞다", bad)

# 26
bad = []
ls = LINES.get("wiki-en-busan", [])
for head, nxt in [("- Area", "  - Metropolitan city: 770.04 km2 (297.31 sq mi)"),
                  ("- Population (January 2026)", "  - Metropolitan city: 3,285,147")]:
    if head not in ls:
        bad.append(f"'{head}' 줄이 없음")
    elif ls[ls.index(head) + 1] != nxt:
        bad.append(f"'{head}' 다음 줄이 '{nxt}'이 아님")
bad += [f"{k}:{n} '{l[:30]}'" for k, v in LINES.items() for n, l in enumerate(v, 1) if l.startswith(("- •", "  - •"))]
report("26. 부산 영어 정보 상자의 묶음이 들여 쓰였고 어느 파일에도 '•'로 시작하는 목록 줄이 없다", bad)

# 15
def hashes():
    return {d["doc_id"]: hashlib.sha256((MARKDOWN / f"{d['doc_id']}.md").read_bytes()).hexdigest()
            for d in DOCS if (MARKDOWN / f"{d['doc_id']}.md").is_file()}


runs = []
bad = []
for _ in range(2):
    r = subprocess.run([sys.executable, str(ROOT / "src" / "corpus" / "build.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        bad.append(f"build.py가 실패함: {r.stderr[-200:]}")
    runs.append(hashes())
if len(runs[0]) != len(DOCS):
    bad.append(f"해시를 낸 파일이 {len(runs[0])}개")
bad += [f"{k}: 두 번의 해시가 다름" for k in runs[0] if runs[0][k] != runs[1].get(k)]
report("15. build.py를 두 번 돌려도 28개 파일의 해시가 같다", bad)

sys.exit(0 if all(results) else 1)
