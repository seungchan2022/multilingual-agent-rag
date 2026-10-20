"""새 후보 분야 세 곳(decisions/stage2.md 2026-10-20 "새 후보 분야 여섯을 문서 측정부터 거른다"의 2 대상 고르기)의 대상 10개를 고정하고,
3 문단 읽기에 쓸 첫 본문 단락을 뽑는다. make_short_test.py와 같은 방법이다.

  .venv/bin/python src/domain_select/make_round3_targets.py [폴더 ...]   (기본: kr_satellites probes kr_bridges)

round3/survey/survey.json에서 그 분야의 정한 값에 대해 셈한 대상(영어 링크 있음, kind 하나, 단위 환산 가능)을 survey.json에 적힌 차례로
가져와 make_short_test.shuffled(씨앗 20261019)로 섞는다. 섞은 차례대로 한국어 문서를 받아(판 revid를 docs.json에 남김) 정보 상자 줄에서
값을 읽고, survey.json의 값과 같은지 확인하고, 영어 위키백과의 같은 문서(langlink)의 정보 상자 칸에서 값을 읽어 단위를 맞춘 뒤
1% 안에서 맞으면 쓴다. 아니면 이유를 적고 건너뛴다. 10개가 되면 멈춘다. 10개를 못 채우면 questions.json 없이 selection.json만 남긴다.
영어 문서는 받는 때의 판이고 revid를 selection.json의 en_docs에 남긴다. 영어 위키 글은 en/에 둔다(4 문서 측정에서 쓴다).
questions.json이 이미 있으면 멈춘다. 끝나면 questions.json이 있는 분야의 첫째 대상 한국어 문서에서 첫 본문 단락을 뽑아 round3/paragraphs.md에 쓴다.

한국어 값 읽기는 survey3.py와 같다: 칸 이름은 survey.json에 적힌 칸(survey3.py의 정규식이 고른 칸)이고 단위 표 MASS, LEN_M도 survey3.py의 것을 쓴다.
survey3.py의 kind가 하나라도 값 글자가 둘이거나 어림인 것(예: "1,400kg 내외", "3,625 kg (발사), 1,593 kg")은 질문의 답이 하나로 정해지지 않으므로
make_short_test와 같은 규칙으로 건너뛰고 이유를 적는다.
"""
import importlib.util, json, re, sys, time, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import make_short_test as mst  # noqa: E402
from make_short_test import GAP, N, SEED, TOL_PCT, UA, get  # noqa: E402

ROUND3 = ROOT / "research_notes" / "stage2_stem_select" / "round3"
SURVEY = ROUND3 / "survey" / "survey.json"
PARAGRAPHS = ROUND3 / "paragraphs.md"

_spec = importlib.util.spec_from_file_location("survey3", ROUND3 / "survey" / "survey3.py")
survey3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(survey3)  # survey3.MASS, survey3.LEN_M (main()은 실행되지 않는다)

# 영어 위키백과 단위(소문자) -> 질문 단위로 곱할 값. 이 표에 없으면 비교할 수 없다. "ton"·"tons"는 short ton(907 kg)인지 tonne인지 알 수 없어 뺀다.
EN_KG = {"kg": 1, "kilogram": 1, "kilograms": 1, "g": 1e-3, "gram": 1e-3, "grams": 1e-3,
         "lb": 0.45359237, "lbs": 0.45359237, "lb.": 0.45359237, "pound": 0.45359237, "pounds": 0.45359237,
         "t": 1e3, "tonne": 1e3, "tonnes": 1e3}
EN_M = {"m": 1, "metre": 1, "metres": 1, "meter": 1, "meters": 1, "km": 1e3, "kilometre": 1e3, "kilometres": 1e3,
        "kilometer": 1e3, "kilometers": 1e3, "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
        "mi": 1609.344, "mile": 1609.344, "miles": 1609.344}

# 영어 칸은 아래 근거 문서의 영어 위키 글(Infobox spaceflight / Infobox bridge)에서 `| 칸 = 값` 줄의 이름을 센 표를 보고 2026-10-20 돌리기 전에 정했다.
# 칸이 여럿이면 한국어 값과 1% 안에서 맞는 칸이 하나라도 있으면 맞음으로 하고 어느 칸인지 남긴다(읽는 차례가 아니라 맞는 칸).
#  - 인공위성(survey 대상 18개의 영어 글): launch_mass 16, dry_mass 6, landing_mass 1. 본 문서: OSSI-1, STSat-1, Koreasat 1, KOMPSAT-3, KITSAT-1
#  - 탐사선(65개): launch_mass 60, dry_mass 47, payload_mass 26, landing_mass 14, bol_mass 9, mass 1(대문자 Mass, 달 광물 지도 작성기). 본 문서: Magellan,
#    Venus Express, Juno, New Horizons, Mars Express(launch_mass와 dry_mass가 다른 값), Moon Mineralogy Mapper(Mass). payload·landing·bol(수명 초 질량)은
#    탐사선 전체 질량이 아니라 쓰지 않는다
#  - 교량(17개): length 9, mainspan 8, spans 8. total_length 칸은 하나도 없었다(본 문서: Incheon Bridge, Busan Harbor Bridge, Seohae Bridge,
#    Yi Sun-sin Bridge는 length에 총길이). mainspan·spans는 주경간이라 쓰지 않는다. total_length는 없어도 읽도록 뒤에 둔다
FIELDS = [
    {"dir": "kr_satellites", "prefix": "ks", "field": "한국의 인공위성", "value": "질량(kg)", "unit_out": "kg",
     "ko_units": survey3.MASS, "en_keys": ["launch_mass", "dry_mass", "mass"], "en_units": EN_KG,
     "q": "인공위성 {이름}의 질량은 몇 kg인가?", "a": "{값} kg"},
    {"dir": "probes", "prefix": "pr", "field": "태양계 탐사선", "value": "질량(kg)", "unit_out": "kg",
     "ko_units": survey3.MASS, "en_keys": ["launch_mass", "dry_mass", "mass"], "en_units": EN_KG,
     "q": "탐사선 {이름}의 질량은 몇 kg인가?", "a": "{값} kg"},
    {"dir": "kr_bridges", "prefix": "kb", "field": "한국의 교량", "value": "총길이(m)", "unit_out": "m",
     "ko_units": survey3.LEN_M, "en_keys": ["length", "total_length"], "en_units": EN_M,
     "q": "{이름}의 총길이는 몇 m인가?", "a": "{값} m"},
]


def candidates(survey_field, value):
    """survey.json에서 그 값에 대해 셈한 대상(kind 하나, 단위 환산 가능, 영어 링크 있음)을 survey.json의 차례 그대로. [(한국어 제목, 영어 제목, 대상 기록)]"""
    en = {d["ko"]: d["en"] for d in survey_field["docs"]}
    return [(t["title"], en[t["title"]], t) for t in survey_field["values"][value]["targets"]
            if t["kind"] == "하나" and t["base_value"] is not None and en.get(t["title"])]


def one_paren(rest):
    """단위 뒤에 남은 글이 없거나, 괄호 하나뿐인지. make_short_test.only_paren은 "(가), 2 (나)"도 받아서 괄호가 하나인지 따로 본다."""
    rest = rest.strip()
    return rest == "" or re.fullmatch(r"\([^()]*\)", rest) is not None


def format_value(v):
    """답에 적을 숫자 글자. 소수 여섯 자리까지, 끝의 0은 뗀다(0.95, 38.011041, 1770)."""
    return ("%.6f" % v).rstrip("0").rstrip(".")


def find_ko(cell, units, md, survey_base):
    """한국어 마크다운의 정보 상자 줄에서 survey가 읽은 칸의 값을 찾는다. (quote, 숫자 글자, 한국어 값 글자, 질문 단위로 바꾼 값, 이유).
    못 찾거나 survey 값과 다르거나 값이 하나로 정해지지 않으면 값이 None이고 이유가 있다."""
    label = r"\s*".join(map(re.escape, cell.replace(" ", "")))
    head = re.compile(rf"^\s*- ({label})\s*(?:\([^)]*\))?\s*[:：]?\s*(.+)$")
    reason = "정보 상자 줄 없음"
    for line in md.splitlines():
        m = head.match(line)
        if not m:
            continue
        quote = line.strip()[2:]
        num_text, value, tail, why = mst.parse_number(m.group(2))
        if why:
            reason = f"숫자 하나가 아님({why}): {quote}"
            continue
        tok = re.match(r"[^\s(]*", tail).group()
        if tok.lower() not in units:
            reason = f"단위를 바꿀 수 없음: {quote}"
            continue
        if not one_paren(tail[len(tok):]):
            reason = f"값 뒤에 더 있음(값이 둘이거나 어림): {quote}"
            continue
        base = value * units[tok.lower()]
        if abs(base - survey_base) > 1e-9 * abs(survey_base):
            reason = f"survey 값과 다름: survey {survey_base:g}, 문서 {quote!r}"
            continue
        return quote, num_text, f"{num_text} {tok}".strip(), base, None
    return None, None, None, None, reason


def en_cells(keys, units, wikitext):
    """영어 위키 글에서 keys의 칸(대소문자 무시, 같은 이름이 여러 번 나오면 모두)을 읽는다. [(칸, 원래 글, 질문 단위로 바꾼 값 또는 None, 이유 또는 None)].
    비어 있는 칸(주석뿐)은 없는 것으로 본다."""
    out = []
    for key in keys:
        pat = re.compile(r"^\s*\|\s*" + re.escape(key).replace("_", r"[_ ]") + r"\s*=(.*)$", re.I | re.M)
        for m in pat.finditer(wikitext):
            raw = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()
            if not raw:
                continue
            text = mst.clean_en(raw)
            num_text, value, tail, why = mst.parse_number(text)
            if why:
                out.append((key, raw[:80], None, f"{why}: {text}"))
                continue
            tok = re.match(r"[^\s(]*", tail).group().lower()
            if not one_paren(tail[len(tok):]):
                out.append((key, raw[:80], None, f"값 뒤에 더 있음: {text}"))
            elif tok not in units:
                out.append((key, raw[:80], None, f"단위 {tok or '없음'}: {text}"))
            else:
                out.append((key, raw[:80], value * units[tok], None))
    return out


def en_match(ko_value, cells):
    """한국어 값(질문 단위)과 영어 칸들을 견준다. 1% 안에서 맞는 칸이 하나라도 있으면 영어 값에 가장 가까운 칸을 (칸, 원래 글, 영어 값, 차이 %, None)으로,
    아니면 (None, None, None, None, 이유)로 돌려준다. 차이는 영어 값 기준 퍼센트(make_short_test와 같다)."""
    ok = [(abs(ko_value - v) / abs(v) * 100, k, raw, v) for k, raw, v, why in cells if v is not None]
    hit = sorted(d for d in ok if d[0] <= TOL_PCT)
    if hit:
        d, k, raw, v = hit[0]
        return k, raw, v, d, None
    if ok:
        return None, None, None, None, f"영어 값과 다름: 한국어 {ko_value:g}, 영어 " + ", ".join(f"{k}={v:g}" for _, k, _, v in ok)
    if cells:
        return None, None, None, None, "영어 값 비교 불가: " + "; ".join(f"{k}: {why}" for k, _, _, why in cells)
    return None, None, None, None, "영어 값 없음: 영어 글에 읽을 칸이 없음"


def fetch_en(titles):
    """영어 위키 글을 제목을 묶어 받는다(50개씩). 제목 -> (실제 제목, 위키 글, revid). 없는 글은 (제목, None, None). revid를 남기는 것이 make_short_test.fetch_en과 다르다."""
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({
            "action": "query", "titles": "|".join(chunk), "prop": "revisions", "rvprop": "ids|content", "rvslots": "main",
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
            out[t] = (real, p["revisions"][0]["slots"]["main"]["content"], p["revisions"][0]["revid"]) if ok else (real, None, None)
    return out


def first_paragraph(md):
    """마크다운의 첫 본문 단락. 제목(#), 정보 상자 줄(- 로 시작), 표(|), 틀({{)·그림·목록·인용 표시로 시작하는 덩어리는 건너뛴다."""
    for block in re.split(r"\n\s*\n", md):
        b = block.strip()
        if not b or b[0] in "#-*|{![>:;=":
            continue
        return b
    return None


def make_field(f, survey, fetched):
    out = ROUND3 / f["dir"]
    if (out / "questions.json").exists():
        sys.exit(f"{out / 'questions.json'}이 이미 있다. 고른 대상이 바뀌지 않게 멈춘다")
    for d in ("raw", "md", "en"):
        (out / d).mkdir(parents=True, exist_ok=True)
    docs = {}
    cands = {ko: (en, rec) for ko, en, rec in candidates(survey["fields"][f["field"]], f["value"])}
    order = mst.shuffled(list(cands))
    en_texts = fetch_en([cands[ko][0] for ko in order])
    results = {ko: {"result": "unvisited"} for ko in order}
    en_docs = {}
    questions = []
    for ko in order:
        en_title, rec = cands[ko]
        doc, md = mst.fetch_doc(out, ko, docs)
        if doc is None:
            results[ko] = {"result": "skipped", "reason": "없는 문서"}
            continue
        quote, num_text, ko_text, ko_value, reason = find_ko(rec["cell"], f["ko_units"], md, rec["base_value"])
        if reason:
            results[ko] = {"result": "skipped", "reason": reason}
            continue
        real, en_wiki, en_revid = en_texts[en_title]
        if en_wiki is None:
            results[ko] = {"result": "skipped", "reason": "영어 값 없음: 영어 글 없음"}
            continue
        (out / "en" / f"{real.replace('/', '_')}.wikitext").write_text(en_wiki, encoding="utf-8")
        en_docs[ko] = {"en_title": real, "revid": en_revid, "fetched_utc": fetched}
        key, en_text, ev, diff, reason = en_match(ko_value, en_cells(f["en_keys"], f["en_units"], en_wiki))
        if reason:
            results[ko] = {"result": "skipped", "reason": reason}
            continue
        mst.check_quote(md, quote, num_text)
        n = len(questions) + 1
        name = mst.strip_paren(ko)
        questions.append({
            "id": f"{f['prefix']}-{n:02d}", "kind": "값", "subject": f["field"], "target": name,
            "question": f["q"].format(이름=name), "answer": f["a"].format(값=format_value(ko_value)),
            "value": ko_value, "unit": f["unit_out"], "evidence_quotes": [{"doc": doc, "quote": quote}],
            "en_check": {"en_title": real, "en_revid": en_revid, "en_key": key, "en_value": ev, "en_text": en_text, "diff_pct": round(diff, 4)}})
        results[ko] = {"result": "used", "id": questions[-1]["id"], "doc": doc, "ko_text": ko_text, "en_key": key}
        print(f"{f['dir']} {questions[-1]['id']} {name} 한국어 {ko_text} = {ko_value:g} {f['unit_out']} 영어 {key} {ev:g} 차이 {diff:.4f}%")
        if len(questions) == N:
            break
    sel = {"seed": SEED, "survey_fetched_utc": survey["fetched_utc"], "order": order, "results": results, "en_docs": en_docs}
    (out / "selection.json").write_text(json.dumps(sel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if len(questions) < N:
        print(f"{f['dir']}: 대상 {N}개를 못 채웠다({len(questions)}개). selection.json을 본다", file=sys.stderr)
        return False
    (out / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def write_paragraphs():
    """questions.json이 있는 분야마다 첫째로 쓴 대상의 한국어 문서(docs.json의 판)에서 첫 본문 단락을 뽑아 paragraphs.md에 쓴다."""
    L = ["# 3 문단 읽기용 첫 본문 단락", "",
         "분야마다 고른 10개 가운데 섞은 차례의 첫째 대상(질문 -01)의 한국어 문서(docs.json의 판)에서 정보 상자·표·틀이 아닌 첫 문단을 그대로 옮겼다.", ""]
    for f in FIELDS:
        out = ROUND3 / f["dir"]
        if not (out / "questions.json").exists():
            continue
        q = json.loads((out / "questions.json").read_text(encoding="utf-8"))[0]
        doc = q["evidence_quotes"][0]["doc"]
        revid = json.loads((out / "docs.json").read_text(encoding="utf-8"))[doc]["revid"]
        para = first_paragraph((out / "md" / f"{doc}.md").read_text(encoding="utf-8"))
        L += [f"## {f['field']}", "", f"- 분야: {f['field']}", f"- 대상: {q['target']} ({q['id']})", f"- 문서 제목: {doc}", f"- revid: {revid}", "",
              para or "(첫 본문 단락을 찾지 못했다)", ""]
    PARAGRAPHS.write_text("\n".join(L), encoding="utf-8")


def main():
    survey = json.loads(SURVEY.read_text(encoding="utf-8"))
    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    only = sys.argv[1:]
    failed = [f["dir"] for f in FIELDS if (not only or f["dir"] in only) and not make_field(f, survey, fetched)]
    write_paragraphs()
    if failed:
        sys.exit(f"못 채운 분야: {', '.join(failed)}")


if __name__ == "__main__":
    main()
