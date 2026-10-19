"""짧은 시험(이슈 #6)의 질문 파일을 만든다. 분야마다 대상 10개를 무작위로 골라, 값 하나를 계산 없이 묻는다.

  .venv/bin/python src/domain_select/make_short_test.py [폴더 ...]   (기본: 분야 6개 모두)

survey.json에서 씨앗 SEED로 섞은 차례대로 한국어 위키백과 문서를 받아, 정보 상자 줄에서 값을 뽑을 수 있고 영어 위키백과의
같은 값과 1% 안에서 맞으면 쓰고, 아니면 이유를 적고 건너뛴다. 쓴 대상이 10개가 되면 멈춘다. 받는 방식은 fetch_docs.py와 같다.
값 읽기 규칙은 field_survey/survey.py의 kind와 같다(자릿수 띄어쓰기, ± 오차, 값 뒤 괄호는 하나로 본다).
<폴더>/에 questions.json, selection.json, docs.json, raw/, md/, en/을 쓴다. questions.json이 이미 있으면 멈춘다.
10개를 못 채운 분야는 questions.json 없이 selection.json만 남기고, 나머지 분야는 계속 만든다.
"""
import json, random, re, sys, time, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from fetch_docs import GAP, api, to_markdown  # noqa: E402
from fetch import UA, get  # noqa: E402

BASE = ROOT / "research_notes" / "stage2_stem_select"
SURVEY = BASE / "field_survey" / "survey.json"
OUT = BASE / "short_test"
SEED = 20261019
N = 10
TOL_PCT = 1.0  # 한국어 값과 영어 값이 이 퍼센트 안이어야 쓴다

# 영어 위키백과 단위 → 한국어 쪽 단위로 바꾸는 곱. 이 표에 없으면 비교할 수 없다
DAY = {"d": 1, "day": 1, "days": 1, "일": 1, "yr": 365.25, "y": 365.25, "a": 365.25, "year": 365.25, "years": 365.25}
AU = {"au": 1, "gm": 1 / 149.5978707, "km": 1 / 149597870.7}
GCM3 = {"g/cm3": 1, "g/cm³": 1}
CELSIUS = {"°c": 1, "c": 1, "℃": 1}
SOLAR = {"m☉": 1, "m⊙": 1}

# unit: 한국어 값 뒤 글자가 이 식으로 시작해야 받는다. empty: 단위가 없어도 받는지. sign: 값 앞 부호를 공전 방향으로 보고 뗄지.
# en_keys: 영어 위키 글에서 읽을 칸 이름 (칸, 단위가 없어도 되는지). en_units: 영어 단위 표. en_template: 원소 정보 틀을 읽는지
FIELDS = [
    {"dir": "rare_earth", "prefix": "re", "field": "희토류 원소", "value": "밀도", "label": r"밀도",
     "unit": r"g\s*/\s*cm(?:3|³)", "unit_out": "g/cm³", "empty": False,
     "en_keys": [("density gpcm3nrt", True), ("density", False)], "en_units": GCM3, "en_template": True,
     "q": "{이름}의 상온 근처 밀도는 몇 g/cm³인가?", "a": "{값} g/cm³"},
    {"dir": "organic", "prefix": "or", "field": "유기 화합물", "value": "끓는점", "label": r"끓는점",
     "unit": r"[°º]\s*C|℃", "unit_out": "°C", "empty": False,
     "en_keys": [("BoilingPtC", True), ("BoilingPt", False)], "en_units": CELSIUS, "en_template": False,
     "q": "{이름}의 끓는점은 몇 °C인가?", "a": "{값} °C"},
    {"dir": "minor_bodies", "prefix": "mb", "field": "왜행성·소행성", "value": "긴반지름", "label": r"(?:궤도\s*)?긴반지름",
     "unit": r"AU\b", "unit_out": "AU", "empty": True,
     "en_keys": [("semimajor", False)], "en_units": AU, "en_template": False,
     "q": "천체 {이름}의 궤도 긴반지름은 몇 AU인가?", "a": "{값} AU"},
    {"dir": "moons", "prefix": "mo", "field": "덜 알려진 위성", "value": "공전 주기", "label": r"공전\s*주기",
     "unit": r"일|d\b", "unit_out": "일", "empty": False, "sign": True,
     "en_keys": [("period", False)], "en_units": DAY, "en_template": False,
     "q": "위성 {이름}의 공전 주기는 며칠인가?", "a": "{값}일"},
    {"dir": "stars", "prefix": "st", "field": "가까운 항성", "value": "질량", "label": r"질량",
     "unit": r"M\s*[☉⊙]", "unit_out": "M☉", "empty": False,
     "en_keys": [("mass", True)], "en_units": SOLAR, "en_template": False,
     "q": "항성 {이름}의 질량은 태양 질량의 몇 배인가?", "a": "{값}배"},
    {"dir": "exoplanets", "prefix": "ex", "field": "외계 행성", "value": "공전주기", "label": r"공전\s*주기",
     "unit": r"일|d\b", "unit_out": "일", "empty": False, "sign": True,
     "en_keys": [("period", False)], "en_units": DAY, "en_template": False,
     "q": "외계 행성 {이름}의 공전 주기는 며칠인가?", "a": "{값}일"},
]

# 숫자 하나: 정수부의 세 자리 띄어쓰기, 소수부의 띄어쓴 자릿수 묶음("79.321 5")을 한 수로 읽는다
NUM = r"-?\d[\d,]*(?:\s\d{3}(?!\d))*(?:\.\d+(?:\s\d+(?!\d))*)?"
# ± 오차(영어 글의 +/-도), 위아래가 다른 오차("+0.001 −0.002"), "(+0.23, -0.20)"는 가운데 값 하나로 보고 버린다
ERR = re.compile(r"\s*(?:(?:±|\+/-)\s*\d[\d,.]*|[+＋]\s*\d[\d.]*\s*[-−–]\s*\d[\d.]*|\(\s*\+[\d.]+\s*,\s*[-−–][\d.]+\s*\))")
APPROX = re.compile(r"약|~|≈|≥|≤|>|<|\?|추정")


def shuffled(rows, seed=SEED):
    """분야마다 새 Random을 같은 씨앗으로 만들어 섞는다. 이 차례가 고르는 차례다."""
    rows = list(rows)
    random.Random(seed).shuffle(rows)
    return rows


def strip_paren(title):
    """문서 제목 끝의 괄호 설명을 뗀다. "미란다 (위성)" → "미란다"."""
    return re.sub(r"\s*\([^)]*\)\s*$", "", title)


def to_float(num_text):
    return float(re.sub(r"[\s,]", "", num_text))


def parse_number(text, sign=False):
    """값 글자에서 숫자 하나를 읽어 (숫자 글자, 값, 뒤 글자, 이유)를 돌려준다. 못 읽으면 이유가 있다.
    범위, 두 값, 어림, 숫자로 시작하지 않는 글은 받지 않는다.
    sign이면 앞의 부호(+, −, -)는 공전 방향 표시로 보고 떼어 크기만 읽는다."""
    s = text.strip()
    if sign:
        s = re.sub(r"^[+−–-]\s*(?=\d)", "", s)
    if APPROX.search(re.sub(r"\([^)]*\)", "", s)):
        return None, None, None, "어림"
    m = re.match(NUM, s)
    if not m:
        return None, None, None, "숫자로 시작하지 않음"
    rest = s[m.end():]
    e = ERR.match(rest)
    if e:
        rest = rest[e.end():]
    tail = rest.strip()
    if re.match(r"[-–~−×/\d]", tail):
        return None, None, None, "범위나 두 값"
    return m.group(), to_float(m.group()), tail, None


def only_paren(rest):
    """단위 뒤에 남은 글이 없거나, 같은 값을 다른 단위로 다시 적은 괄호뿐인지."""
    rest = rest.strip()
    return rest == "" or (rest.startswith("(") and rest.endswith(")"))


def find_line(f, md):
    """마크다운에서 정보 상자 줄을 찾아 (quote, 숫자 글자, 값, 이유)를 돌려준다. 못 찾거나 못 받으면 숫자 글자가 None이다."""
    head = re.compile(rf"^\s*- ({f['label']})\s*(?:\([^)]*\))?\s*[:：]?\s*(.+)$")
    unit = re.compile(f["unit"])
    reason = "정보 상자 줄 없음"
    for line in md.splitlines():
        m = head.match(line)
        if not m:
            continue
        quote = line.strip()[2:]
        num_text, value, tail, why = parse_number(m.group(2), f.get("sign"))
        if why:
            reason = f"숫자 하나가 아님({why}): {quote}"
            continue
        u = unit.match(tail)
        if not (u or (f["empty"] and only_paren(tail))):
            reason = f"단위가 맞지 않음: {quote}"
            continue
        return quote, num_text, value, None
    return None, None, None, reason


def check_quote(md, quote, num_text):
    """quote가 문서에 글자 그대로 있고 값의 숫자 글자가 들어 있는지 확인한다."""
    assert quote in md, f"quote가 문서에 없다: {quote}"
    assert num_text in quote, f"quote에 값 {num_text}이 없다: {quote}"


def en_template(m):
    """영어 위키 틀 하나를 글자로 바꾼다. 값 틀(val, convert, cvt)만 살리고 나머지(출처, 각주)는 지운다."""
    parts = [s.strip() for s in m.group(1).split("|")]
    named = {a.split("=", 1)[0].strip(): a.split("=", 1)[1] for a in parts[1:] if re.match(r"[\w ]+=", a)}
    pos = [a for a in parts[1:] if not re.match(r"[\w ]+=", a)]
    name = parts[0].lower()
    if name == "val":
        if not pos:
            return ""
        num = pos[0] + (f"×10^{named['e']}" if "e" in named else "")
        return f"{named.get('p', '')}{num} {named.get('u') or named.get('ul') or ''}".strip()
    if name in ("convert", "cvt"):
        out = []
        for a in pos:  # 숫자, ± 오차, 단위까지만. 바꿀 단위는 버린다
            out.append(a)
            if re.search(r"[A-Za-z°℃]", a) and a.lower() not in ("to", "and", "or", "by"):
                break
        return " ".join(out)
    if name in ("nowrap", "nobr", "sigfig"):  # sigfig는 어림하지 않은 앞 값을 쓴다
        return pos[0] if pos else ""
    return ""


def clean_en(raw):
    """영어 위키 칸의 값 글을 읽을 글자로 바꾼다(survey.py의 clean과 같은 순서)."""
    s = re.sub(r"<ref[^>]*/>", "", raw)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*>.*$", "", s)
    s = re.sub(r"<br\s*/?>", " / ", s)
    s = re.sub(r"</?[A-Za-z][^>]*>", "", s)
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", s)
    for _ in range(3):  # 안쪽 틀부터
        s = re.sub(r"\{\{([^{}]*)\}\}", en_template, s)
    for a, b in (("&nbsp;", " "), ("&thinsp;", " "), ("&minus;", "−"), ("&plusmn;", "±"), ("&ndash;", "–")):
        s = s.replace(a, b)
    s = re.sub(r"'{2,}", "", s)
    return re.sub(r"\s+", " ", s).strip()


def en_value(f, wikitext):
    """영어 위키 글에서 칸을 읽어 (값, 칸의 원래 글, 이유)를 돌려준다. 값은 한국어 쪽 단위로 바꾼 것이다.
    칸이 없으면 이유가 "영어 값 없음", 읽거나 단위를 맞출 수 없으면 "영어 값 비교 불가: ..."이다."""
    for key, implicit in f["en_keys"]:
        pat = re.compile(r"^\s*\|\s*" + key.replace(" ", r"\s+") + r"\s*=(.*)$", re.I | re.M)
        for m in pat.finditer(wikitext):
            raw = m.group(1).strip()
            if not raw:
                continue
            text = clean_en(raw)
            num_text, value, tail, why = parse_number(text, f.get("sign"))
            if why:
                return None, raw[:80], f"영어 값 비교 불가: {why}: {text}"
            tok = re.match(r"[^\s(]*", tail).group().lower()
            if not only_paren(tail[len(tok):]):
                return None, raw[:80], f"영어 값 비교 불가: 값 뒤에 더 있음: {text}"
            if tok == "" and implicit:
                return value, raw[:80], None
            if tok not in f["en_units"]:
                return None, raw[:80], f"영어 값 비교 불가: 단위 {tok or '없음'}: {text}"
            return value * f["en_units"][tok], raw[:80], None
    return None, "", "영어 값 없음"


def fetch_en(titles):
    """영어 위키 글을 제목을 묶어 받는다(50개씩). 제목 → (실제 제목, 위키 글). 없는 글은 (제목, None)."""
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "titles": "|".join(chunk), "prop": "revisions", "rvprop": "content", "rvslots": "main",
            "redirects": 1, "format": "json", "formatversion": 2})
        q = json.loads(get(url, {"User-Agent": UA, "Accept-Encoding": "gzip"}))["query"]
        time.sleep(GAP)
        norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
        redir = {r["from"]: r["to"] for r in q.get("redirects", [])}
        pages = {p["title"]: p for p in q["pages"]}
        for t in chunk:
            real = redir.get(norm.get(t, t), norm.get(t, t))
            p = pages.get(real)
            ok = p and not p.get("missing") and "revisions" in p
            out[t] = (real, p["revisions"][0]["slots"]["main"]["content"] if ok else None)
    return out


def fetch_doc(out, title, docs):
    """문서 하나를 받아 raw/md에 쓰고 (문서 제목, 마크다운)을 돌려준다. fetch_docs.main과 같은 순서다. 없는 문서면 None."""
    page = api({"action": "query", "titles": title, "prop": "revisions", "rvprop": "ids", "redirects": 1})["query"]["pages"][0]
    if "missing" in page:
        return None, None
    revid = page["revisions"][0]["revid"]
    time.sleep(GAP)
    r = api({"action": "parse", "oldid": revid, "prop": "text|revid"})["parse"]
    assert r["revid"] == revid, title
    raw = r["text"].encode("utf-8")
    (out / "raw" / f"{page['title']}.html").write_bytes(raw)
    md = to_markdown(page["title"], raw)
    (out / "md" / f"{page['title']}.md").write_text(md, encoding="utf-8")
    docs[page["title"]] = {"revid": revid, "url": f"https://ko.wikipedia.org/w/index.php?oldid={revid}"}
    (out / "docs.json").write_text(json.dumps(docs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    time.sleep(GAP)
    return page["title"], md


def en_title_of(f, row):
    """영어 쪽에서 읽을 글 제목. 원소는 원소 정보 틀이다."""
    return f"Template:Infobox {row['en'].lower()}" if f["en_template"] else row["en"]


def make_field(f, rows):
    """분야 하나를 만든다. 10개를 채우면 True, 못 채우면 questions.json 없이 selection.json만 남기고 False."""
    out = OUT / f["dir"]
    if (out / "questions.json").exists():
        sys.exit(f"{out / 'questions.json'}이 이미 있다. 고른 대상이 바뀌지 않게 멈춘다")
    for d in ("raw", "md", "en"):
        (out / d).mkdir(parents=True, exist_ok=True)
    docs = {}
    cands = [r for r in rows if r.get("ko") and r.get("values", {}).get(f["value"], {}).get("kind") == "하나"]
    order = shuffled(cands)
    en_texts = fetch_en([en_title_of(f, r) for r in order])
    results = {r["ko"]: {"result": "unvisited"} for r in order}
    questions = []
    for r in order:
        ko = r["ko"]
        doc, md = fetch_doc(out, ko, docs)
        if doc is None:
            results[ko] = {"result": "skipped", "reason": "없는 문서"}
            continue
        quote, num_text, value, reason = find_line(f, md)
        if num_text is not None:
            survey_text = r["values"][f["value"]]["text"]
            sv = parse_number(survey_text, f.get("sign"))[1]
            if sv != value:
                reason = f"survey 값과 다름: survey {survey_text!r}, 문서 {quote!r}"
        if reason:
            results[ko] = {"result": "skipped", "reason": reason}
            continue
        en_title, en_wiki = en_texts[en_title_of(f, r)]
        if en_wiki is None:
            results[ko] = {"result": "skipped", "reason": "영어 값 없음: 영어 글 없음"}
            continue
        (out / "en" / f"{en_title.replace('/', '_')}.wikitext").write_text(en_wiki, encoding="utf-8")
        ev, en_text, reason = en_value(f, en_wiki)
        if reason:
            results[ko] = {"result": "skipped", "reason": reason}
            continue
        diff = abs(value - ev) / abs(ev) * 100
        if diff > TOL_PCT:
            results[ko] = {"result": "skipped", "reason": f"영어 값과 다름: 한국어 {value:g}, 영어 {ev:g}"}
            continue
        check_quote(md, quote, num_text)
        n = len(questions) + 1
        name = strip_paren(ko)
        questions.append({
            "id": f"{f['prefix']}-{n:02d}", "kind": "값", "subject": f["field"], "target": name,
            "question": f["q"].format(이름=name), "answer": f["a"].format(값=re.sub(r"\s", "", num_text)),
            "value": value, "unit": f["unit_out"], "evidence_quotes": [{"doc": doc, "quote": quote}],
            "en_check": {"en_title": en_title, "en_value": ev, "en_text": en_text, "diff_pct": round(diff, 4)}})
        results[ko] = {"result": "used", "id": questions[-1]["id"], "doc": doc}
        print(f"{f['dir']} {questions[-1]['id']} {name} 한국어 {value:g} 영어 {ev:g} 차이 {diff:.4f}% {f['unit_out']}")
        if len(questions) == N:
            break
    sel = {"seed": SEED, "order": [r["ko"] for r in order], "results": results}
    (out / "selection.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if len(questions) < N:
        print(f"{f['dir']}: 대상 {N}개를 못 채웠다({len(questions)}개). selection.json을 본다", file=sys.stderr)
        return False
    (out / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def main():
    survey = json.loads(SURVEY.read_text(encoding="utf-8"))
    warm = OUT / "warmup.json"
    if not warm.exists():
        OUT.mkdir(parents=True, exist_ok=True)
        warm.write_text(json.dumps([{"id": "warmup", "kind": "준비", "question": "1 더하기 1은?", "answer": "2", "value": 2}],
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    only = sys.argv[1:]
    failed = [f["dir"] for f in FIELDS if (not only or f["dir"] in only) and not make_field(f, survey[f["field"]])]
    if failed:
        sys.exit(f"못 채운 분야: {', '.join(failed)}")


if __name__ == "__main__":
    main()
