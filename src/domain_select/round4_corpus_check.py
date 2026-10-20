"""코퍼스 단위 검사(decisions/stage2.md 2026-10-20 "코퍼스 단위 검사의 규칙" 줄)의 2 함께 넣을 문서 고르기와 3 검사 다.

  .venv/bin/python src/domain_select/round4_corpus_check.py select [분야]   링크를 모아 주제를 묶고 고른다(네트워크). added.json을 쓴다
        select 분야 --with-infobox-grid  정보 상자 안의 표(주기율표 격자 등)의 링크도 센 경우를 added_with_infobox_grid.json에 쓴다(참고용)
  .venv/bin/python src/domain_select/round4_corpus_check.py fetch [분야]    고른 5개 주제의 한·영 문서를 parse로 받는다(네트워크)
  .venv/bin/python src/domain_select/round4_corpus_check.py count [분야]    코퍼스 30개를 읽어 results.json을 쓴다
  .venv/bin/python src/domain_select/round4_corpus_check.py summary         results.json으로 summary.md를 쓴다
  .venv/bin/python src/domain_select/round4_corpus_check.py verify          summary.md의 숫자를 results.json에서 다시 계산해 맞춘다

링크 판단 규칙(2 함께 넣을 문서):
  - 링크는 코퍼스에 들어가는 마크다운 본문에서 센다. 그래서 마크다운 변환(src/corpus/build.py)이 지우는 것은 링크로도 세지 않는다:
    각주·참고 문헌 표시, 둘러보기 상자(navbox), 위쪽 안내(hatnote), 이미지·썸네일 설명, 편집 링크, 분류 상자와
    이름으로 지우는 절(같이 보기·외부 링크·각주·내용주·참고 문헌 / See also·External links·References·Notes).
  - 정보 상자(맨 위 것) 안의 링크는 센다(정보 상자도 문서 내용). 이미지가 든 줄은 변환이 지우므로 그 줄의 링크는 뺀다.
  - /wiki/제목 형태의 링크만 센다(외부 링크는 /wiki/가 아니라 저절로 빠진다). #절 표시는 떼고, 붉은 링크(class new)는 뺀다.
  - 이름공간 접두어(틀·분류·파일·도움말·위키백과·특수·포털·사용자·Template·Category·File·Help·Wikipedia·Special·Portal·User 등)가 붙은
    링크는 뺀다. 접두어 목록에 없는 경우는 API가 알려주는 이름공간 번호(ns)가 0이 아니면 뺀다.
  - 링크 수는 <a> 태그의 수다(같은 문서가 같은 주제를 여러 번 링크하면 여러 번). 링크한 대상의 수는 대상(10개) 가운데
    한 언어 문서라도 그 주제를 링크한 대상의 수다.

숫자가 표 안에서 나왔는지 가리는 방법(3 검사 다 선 나):
  HTML에서 2026-10-13 표 규칙(research_notes/stage2_domain_survey/measure.py의 Body)으로 센 표만 골라, 그 표 안의 칸(td·th)과
  칸 안의 문단·목록 항목 맨 앞에 눈에 안 보이는 표시 글자(U+E000)를 넣은 HTML을 같은 변환(fetch_docs.to_markdown)에 넣는다.
  표시가 든 마크다운 줄에서 나온 숫자는 "표 안", 아닌 줄은 "표 밖"이다. 표시를 지운 마크다운은 표시를 넣지 않고 변환한
  것과 같아야 하며(표시 뒤 공백 하나까지 지운다)(같지 않으면 results.json의 md_same이 false), 정보 상자·둘러보기 상자 같은 표는 표 규칙에서 빠져 표시가 안 붙는다.
  그 언어에만 있는 숫자 하나(같은 값으로 묶은 것)는 언급 가운데 하나라도 표 안이면 "표 안"으로 센다.
"""
import importlib.util
import json
import re
import sys
import urllib.parse
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stepper_check as sc  # noqa: E402  api(User-Agent·쉬기·429 다시 해 보기)
import round3_measure as rm  # noqa: E402  숫자 뽑기·같은 값 판정
from fetch_docs import to_markdown  # noqa: E402  마크다운 변환(import하면 src/corpus가 경로에 든다)
from build import DROP_SECTIONS, drop_all, inline, mark_infobox, norm, prepare  # noqa: E402
from bs4 import BeautifulSoup, NavigableString  # noqa: E402

ROOT = sc.ROOT
ROUND4 = ROOT / "research_notes" / "stage2_stem_select" / "round4"
STEPPER_OUT = sc.OUT
DOMAINS = {"rare_earth": "희토류 원소", "exoplanets": "외계 행성"}
N_PICK = 5
N_CAND = 20
ONLY_MIN = 36        # 선 가: 그 언어에만 있는 숫자(한국어·영어 각각)
TABLE_ONLY_MIN = 3   # 선 나: 그 가운데 표 안에서 나온 것(한국어·영어 각각)
SENT = ""      # 표 안 표시

# --- 링크 모으기 -----------------------------------------------------------

NS_PREFIX = {p.lower() for p in (
    "틀", "분류", "파일", "도움말", "위키백과", "특수", "포털", "사용자", "모듈", "미디어위키", "토론", "그림", "이미지", "위키프로젝트",
    "Template", "Category", "File", "Help", "Wikipedia", "Special", "Portal", "User", "Module", "MediaWiki", "Talk", "Draft",
    "Image", "Media", "TimedText", "WP", "WT", "Project", "Template talk", "Category talk", "User talk", "Help talk",
    "Wikipedia talk", "Portal talk", "File talk")}


def link_title(href):
    """/wiki/ 링크의 문서 제목. 본 이름공간 문서가 아닌 것(이름공간 접두어)이거나 /wiki/가 아니면 None."""
    if not href.startswith("/wiki/"):
        return None
    t = urllib.parse.unquote(href[len("/wiki/"):]).split("#")[0].split("?")[0].replace("_", " ").strip()
    if not t:
        return None
    if ":" in t and t.split(":", 1)[0].strip().lower() in NS_PREFIX:
        return None
    return t


def _blocks(node):
    """build.walk와 같은 순서로 (제목) 또는 (덩어리 요소)를 차례로 낸다."""
    for ch in node.children:
        if isinstance(ch, NavigableString):
            continue
        if ch.name == "div" and "mw-heading" in (ch.get("class") or []):
            h = ch.find(re.compile(r"h[1-6]$"))
            text = inline(h) if h else ""
            if text:
                yield ("h", int(h.name[1]), text)
        elif re.fullmatch(r"h[1-6]", ch.name):
            text = inline(ch)
            if text:
                yield ("h", int(ch.name[1]), text)
        elif ch.name in ("div", "blockquote", "section", "center"):
            yield from _blocks(ch)
        else:
            yield ("b", ch)


def collect_links(html, infobox_grid=False):
    """문서 본문의 위키 링크 제목을 문서 차례대로 모두(같은 것도 여러 번) 돌려준다. 규칙은 파일 머리말.
    infobox_grid=False(기본)이면 정보 상자 칸 안에 든 표(원소 정보 상자의 주기율표 전체 격자처럼 문서마다 같은 이동 격자)의
    링크는 뺀다. 정보 상자의 글자 줄이 아니라 둘러보기 상자와 같은 역할이라 보기 때문이다. True면 센다(규칙을 글자 그대로 읽은 경우)."""
    soup = BeautifulSoup(html, "html.parser")
    root = soup.find("div", class_="mw-parser-output")
    prepare(root)
    if root.find("table", class_="infobox", recursive=False):
        top = mark_infobox(root)
        if not infobox_grid:
            for t in top.find_all("table"):
                if not getattr(t, "decomposed", False):
                    t.decompose()
    drop_all(root)
    out, dropping = [], None
    for it in _blocks(root):
        if it[0] == "h":
            if dropping is not None and it[1] <= dropping:
                dropping = None
            if dropping is None and it[2] in DROP_SECTIONS:
                dropping = it[1]
            continue
        if dropping is not None:
            continue
        el = it[1]
        for a in ([el] if el.name == "a" else []) + el.find_all("a", href=True):
            if "new" in (a.get("class") or []) or not a.get("href"):
                continue
            t = link_title(a["href"])
            if t:
                out.append(t)
    return out


# --- 제목을 실제 문서로 풀기(API) --------------------------------------------

def resolve(lang, titles, other, store, api=sc.api):
    """titles를 lang 위키백과에서 한꺼번에 50개씩 물어 넘겨주기를 푼 실제 제목·이름공간·동음이의·other 언어 제목을 store에 쌓는다.
    store[입력 제목] = {title, ns, missing, other, disamb}. 이미 store에 있는 제목은 다시 묻지 않는다."""
    todo = [t for t in dict.fromkeys(titles) if t not in store]
    for i in range(0, len(todo), 50):
        batch = todo[i:i + 50]
        params = dict(action="query", titles="|".join(batch), redirects=1, prop="langlinks|pageprops", lllang=other,
                      lllimit="max", ppprop="disambiguation")
        pages, mapping, more = {}, {}, {}
        while True:
            d = api(lang, **{**params, **more})
            q = d.get("query", {})
            for n in q.get("normalized", []) + q.get("redirects", []):
                mapping[n["from"]] = n["to"]
            for p in q.get("pages", []):
                cur = pages.setdefault(p["title"], {"ns": p.get("ns"), "missing": bool(p.get("missing") or p.get("invalid")),
                                                    "other": None, "disamb": False})
                for ll in p.get("langlinks") or []:
                    cur["other"] = cur["other"] or ll["title"]
                if "disambiguation" in (p.get("pageprops") or {}):
                    cur["disamb"] = True
            if "continue" not in d:
                break
            more = d["continue"]
        for t in batch:
            f = t
            for _ in range(6):
                if f in mapping and mapping[f] != f:
                    f = mapping[f]
                else:
                    break
            p = pages.get(f) or {"ns": None, "missing": True, "other": None, "disamb": False}
            store[t] = {"title": f, **p}


# --- 주제 묶기와 고르기 -------------------------------------------------------

MONTHS_EN = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_RES = [re.compile(p) for p in (
    r"(기원전 )?\d{1,4}년( \d{1,2}월( \d{1,2}일)?)?", r"(기원전 )?\d{1,4}년대", r"\d{1,2}월( \d{1,2}일)?",
    r"(AD )?\d{1,4}( BC| AD)?", r"\d{1,4}s( BC)?", rf"({MONTHS_EN})( \d{{1,2}}| \d{{4}})?")]


def is_date(title):
    """연도·연대·월·날짜 문서인가(2005년, 1990년대, 10월 28일, 2005, 1990s, March 5). 세기(20세기)는 날짜로 치지 않는다."""
    return any(r.fullmatch(title) for r in DATE_RES)


def build_topics(occ, store_ko, store_en):
    """링크 발생(occ: {target, lang, title}) 목록을 한국어 제목 기준 주제로 묶는다.
    돌려주는 값: {ko_title: {ko_title, en_other, ko_rec, targets:set, ko_links, en_links}}와 못 묶은 발생의 수(이유별).
    영어 링크는 영어 문서의 한국어 언어 링크로 한국어 제목에 맞추고(없으면 못 묶음), 한국어 링크는 그 문서의 영어 언어 링크로 짝을 짓는다."""
    topics, unpaired = {}, defaultdict(int)
    for o in occ:
        if o["lang"] == "ko":
            rec = store_ko[o["title"]]
        else:
            r_en = store_en[o["title"]]
            if r_en["missing"] or r_en["ns"] != 0 or not r_en["other"]:
                unpaired["영어 문서에 한국어 언어 링크 없음(또는 없는 문서·본 이름공간 아님)"] += 1
                continue
            rec = store_ko[r_en["other"]]
        if rec["missing"] or rec["ns"] != 0:
            unpaired["한국어 문서 없음 또는 본 이름공간 아님"] += 1
            continue
        t = topics.setdefault(rec["title"], {"ko_title": rec["title"], "ko_rec": rec, "en_other": rec["other"], "targets": set(),
                                             "ko_links": 0, "en_links": 0})
        t["targets"].add(o["target"])
        t["ko_links" if o["lang"] == "ko" else "en_links"] += 1
    return topics, dict(unpaired)


def exclusion(t, store_en, target_ko, target_en):
    """주제를 빼는 이유(없으면 None). 차례대로 본다."""
    if not t["en_other"]:
        return "영어 문서 없음(한국어 문서에 영어 언어 링크가 없다)"
    en = store_en[t["en_other"]]
    if en["missing"] or en["ns"] != 0:
        return "영어 문서 없음(언어 링크가 가리키는 문서가 없거나 본 이름공간이 아니다)"
    t["en_title"] = en["title"]
    if t["ko_title"] in target_ko or en["title"] in target_en:
        return "대상 10개 자신"
    if t["ko_rec"]["disamb"] or en["disamb"]:
        return "동음이의 문서"
    if is_date(t["ko_title"]) or is_date(en["title"]):
        return "연도·날짜 문서"
    return None


def rank(topics, store_en, target_ko, target_en):
    """(고를 수 있는 주제를 차례로, 뺀 주제 목록). 차례: 링크한 대상 수 큰 순, 두 언어 링크 수 합 큰 순, 한국어 제목."""
    kept, dropped = [], []
    for t in topics.values():
        why = exclusion(t, store_en, target_ko, target_en)
        row = {"ko_title": t["ko_title"], "en_title": t.get("en_title") or t["en_other"], "targets_linked": len(t["targets"]),
               "ko_links": t["ko_links"], "en_links": t["en_links"], "links_sum": t["ko_links"] + t["en_links"],
               "linked_by": sorted(t["targets"])}
        (dropped if why else kept).append({**row, "reason": why} if why else row)
    kept.sort(key=lambda r: (-r["targets_linked"], -r["links_sum"], r["ko_title"]))
    dropped.sort(key=lambda r: (-r["targets_linked"], -r["links_sum"], r["ko_title"]))
    for i, r in enumerate(kept, 1):
        r["rank"] = i
        r["why_ranked"] = (f"링크한 대상 {r['targets_linked']}개, 링크 수 합 {r['links_sum']}"
                           f"(한국어 {r['ko_links']}, 영어 {r['en_links']})")
    return kept, dropped


# --- 대상 문서와 받은 판 -------------------------------------------------------

def target_docs(dom):
    """stepper_check가 받아 둔 대상 10개의 한·영 문서. [{kind, lang, target, title, revid, html}]"""
    recs = [json.loads(l) for l in (STEPPER_OUT / "fetched.jsonl").read_text(encoding="utf-8").splitlines()]
    rows = [{"kind": "대상", "lang": r["lang"], "target": r["target"], "title": r["title"], "revid": r["revid"],
             "html": STEPPER_OUT / "cache" / f"{r['lang']}_{r['revid']}.html"} for r in recs if r["domain"] == dom]
    assert len(rows) == 20, (dom, len(rows))
    return rows


def added_docs(dom):
    """고른 5개 주제의 받은 한·영 문서. fetch가 끝난 뒤에만 있다."""
    base = ROUND4 / dom
    added = json.loads((base / "added.json").read_text(encoding="utf-8"))
    rows = []
    for lang in ("ko", "en"):
        for s in added["selected"]:
            if not s.get(f"{lang}_revid"):
                raise SystemExit(f"{dom}: fetch를 먼저 한다({s['ko_title']})")
            rows.append({"kind": "함께 넣은 것", "lang": lang, "target": s["ko_title"], "title": s[f"{lang}_fetched_title"],
                         "revid": s[f"{lang}_revid"], "html": base / "cache" / f"{lang}_{s[f'{lang}_revid']}.html"})
    return rows


def cmd_select(dom, infobox_grid=False):
    base = ROUND4 / dom
    cache = base / "cache"
    cache.mkdir(parents=True, exist_ok=True)

    def load(name):
        p = cache / name
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    def save(name, obj):
        (cache / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")

    docs = target_docs(dom)
    occ = []
    for d in docs:
        for t in collect_links(d["html"].read_text(encoding="utf-8"), infobox_grid):
            occ.append({"target": d["target"], "lang": d["lang"], "title": t})
    store_ko, store_en = load("resolve_ko.json"), load("resolve_en.json")
    resolve("ko", [o["title"] for o in occ if o["lang"] == "ko"], "en", store_ko)
    resolve("en", [o["title"] for o in occ if o["lang"] == "en"], "ko", store_en)
    save("resolve_ko.json", store_ko), save("resolve_en.json", store_en)
    others = [store_en[o["title"]]["other"] for o in occ if o["lang"] == "en"
              if store_en[o["title"]]["ns"] == 0 and not store_en[o["title"]]["missing"] and store_en[o["title"]]["other"]]
    resolve("ko", others, "en", store_ko)
    save("resolve_ko.json", store_ko)
    topics, unpaired = build_topics(occ, store_ko, store_en)
    resolve("en", [t["en_other"] for t in topics.values() if t["en_other"]], "ko", store_en)
    save("resolve_en.json", store_en)
    target_ko = {d["title"] for d in docs if d["lang"] == "ko"}
    target_en = {d["title"] for d in docs if d["lang"] == "en"}
    kept, dropped = rank(topics, store_en, target_ko, target_en)
    reasons = defaultdict(int)
    for r in dropped:
        reasons[r["reason"]] += 1
    added = {
        "domain": dom, "rule": "링크한 대상 수 큰 순 -> 두 언어 링크 수 합 큰 순 -> 한국어 제목 차례. 위 5개",
        "link_occurrences": len(occ), "distinct_topics_with_ko_page": len(topics), "unpaired_occurrences": unpaired,
        "excluded_counts": dict(reasons),
        "targets": sorted({d["target"] for d in docs}),
        "candidates_top20": kept[:N_CAND], "selected": [dict(r) for r in kept[:N_PICK]],
        "excluded": [r for r in dropped if r["reason"] != "영어 문서 없음(한국어 문서에 영어 언어 링크가 없다)" or r["targets_linked"] >= 3],
        "selected_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    added["infobox_grid_counted"] = infobox_grid
    out_name = "added_with_infobox_grid.json" if infobox_grid else "added.json"
    (base / out_name).write_text(json.dumps(added, ensure_ascii=False, indent=1), encoding="utf-8")
    print(dom, out_name, "링크", len(occ), "주제", len(topics), "고를 수 있는 것", len(kept), "뺀 것", dict(reasons))
    for r in kept[:N_CAND]:
        print(f"  {r['rank']:>2} {r['ko_title']} | {r['en_title']} | {r['why_ranked']}")


def cmd_fetch(dom):
    base = ROUND4 / dom
    added = json.loads((base / "added.json").read_text(encoding="utf-8"))
    (base / "cache").mkdir(parents=True, exist_ok=True)
    log = base / "fetched.jsonl"
    for s in added["selected"]:
        for lang, title in (("ko", s["ko_title"]), ("en", s["en_title"])):
            if s.get(f"{lang}_revid"):
                continue
            d = sc.api(lang, action="parse", page=title, prop="text|revid", redirects=1)
            if "parse" not in d:
                raise RuntimeError(f"{dom} {title} {lang}: {d.get('error')}")
            p = d["parse"]
            (base / "cache" / f"{lang}_{p['revid']}.html").write_text(p["text"], encoding="utf-8")
            s[f"{lang}_revid"], s[f"{lang}_fetched_title"] = p["revid"], p["title"]
            s[f"{lang}_fetched_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            with log.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"domain": dom, "topic": s["ko_title"], "lang": lang, "title": p["title"], "revid": p["revid"],
                                    "fetched_at": s[f"{lang}_fetched_at"]}, ensure_ascii=False) + "\n")
            (base / "added.json").write_text(json.dumps(added, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{dom} | {s['ko_title']} | {lang} | {p['title']} | {p['revid']}", flush=True)


# --- 표 안 숫자 가리기 ---------------------------------------------------------

def _load_survey():
    spec = importlib.util.spec_from_file_location("survey_measure", ROOT / "research_notes" / "stage2_domain_survey" / "measure.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sv = _load_survey()


class TableBody(sv.Body):
    """measure의 Body와 같은 규칙으로 표를 세면서, 겹치지 않은 후보 표(둘러보기·정보 상자 같은 skip 밖)마다 표 규칙을 넘었는지 남긴다."""

    def __init__(self):
        super().__init__()
        self.cands = []

    def handle_starttag(self, tag, attrs):
        outer = False
        if tag not in sv.VOID:
            cls = dict(attrs).get("class") or ""
            skip = bool(sv.SKIP.search(cls)) or tag in ("style", "script") or (tag == "sup" and "reference" in cls)
            outer = tag == "table" and not skip and not self.skip and not self.cur
        super().handle_starttag(tag, attrs)
        if outer:
            self.cur[0]["idx"] = len(self.cands)
            self.cands.append(None)

    def handle_endtag(self, tag):
        rec = self.cur[0] if tag == "table" and self.stack and self.stack[-1][2] and len(self.cur) == 1 else None
        n = len(self.tables)
        super().handle_endtag(tag)
        if rec is not None and "idx" in rec:
            self.cands[rec["idx"]] = len(self.tables) > n


def _is_candidate(t):
    """TableBody의 후보 표와 같은 조건: 안 겹치고, 자기와 윗대 가운데 skip class가 없다."""
    if t.find_parent("table"):
        return False
    for n in [t] + list(t.parents):
        cls = " ".join(n.get("class") or []) if hasattr(n, "get") else ""
        if cls and sv.SKIP.search(cls):
            return False
    return True


def tag_tables(html):
    """표 규칙을 넘은 표의 칸(td·th)과 칸 안 문단·목록 항목 맨 앞에 SENT를 넣은 HTML과 표의 수를 돌려준다."""
    b = TableBody()
    b.feed(html)
    b.close()
    soup = BeautifulSoup(html, "html.parser")
    cands = [t for t in soup.find_all("table") if _is_candidate(t)]
    assert len(cands) == len(b.cands) and None not in b.cands, (len(cands), b.cands.count(None), len(b.cands))
    n, els = 0, []
    for t, ok in zip(cands, b.cands):
        if not ok:
            continue
        n += 1
        for el in t.find_all(["td", "th", "p", "li", "dd", "dt"]):
            el["data-r4id"] = str(len(els))
            els.append(el)
    # 변환이 지우는 것(숨긴 글, 이미지 줄 등)을 지운 복사본에서, 변환이 보는 글자가 남는 요소에만 표시를 넣는다.
    # 글자가 없는 칸에 표시를 넣으면 변환 결과의 구조가 달라지기 때문이다.
    copy = BeautifulSoup(str(soup), "html.parser")
    croot = copy.find("div", class_="mw-parser-output")
    prepare(croot)
    drop_all(croot)
    visible = {el["data-r4id"] for el in croot.find_all(attrs={"data-r4id": True}) if inline(el)}
    for el in els:
        if el["data-r4id"] in visible:
            el.insert(0, NavigableString(SENT))
        del el["data-r4id"]
    return str(soup), n


def doc_markdown(title, html):
    """(표시 없이 변환한 마크다운, 표시가 든 마크다운, 표시를 지우면(표시와 뒤따르는 공백 하나) 표시 없이 변환한 것과 글자까지 같은가, 표 규칙을 넘은 표의 수)"""
    tagged_html, n = tag_tables(html)
    tagged = to_markdown(title, tagged_html.encode("utf-8"))
    plain = to_markdown(title, html.encode("utf-8"))      # 코퍼스에 들어갈 마크다운은 표시를 안 넣고 변환한 것이다
    return plain, tagged, re.sub(SENT + " ?", "", tagged) == plain, n


def doc_items(tagged_md):
    """마크다운 줄마다 숫자를 뽑는다. 항목에 in_table(그 줄이 표 안 표시를 가졌는가)을 붙인다."""
    items = []
    for line in tagged_md.split("\n"):
        tab = SENT in line
        for it in rm.extract(re.sub(SENT + " ?", "", line)):
            it["in_table"] = tab
            items.append(it)
    return items


# --- 코퍼스 단위 판정 -----------------------------------------------------------

def pool_groups(per_doc):
    """한 언어 문서들의 숫자를 한 묶음으로 모아 같은 값(같은 차원 ±1%, rm.dedupe와 같은 방식)을 하나로 센다.
    per_doc: [(doc 번호, items)]. 돌려주는 값: [{dim, base, digits_all, unit, mentions:[{doc, raw, in_table}]}]"""
    flat = [(d, it) for d, items in per_doc for it in items]
    flat.sort(key=lambda x: (x[1]["dim"], x[1]["base"]))
    groups = []
    for d, it in flat:
        m = {"doc": d, "raw": it["raw"], "digits": it["digits"], "in_table": it["in_table"], "value": it["value"], "unit": it["unit"]}
        for g in groups:
            if g["dim"] == it["dim"] and rm.close(g["base"], it["base"]):
                g["mentions"].append(m)
                g["digits_all"].append(it["digits"])
                it["group_ref"] = g
                break
        else:
            g = {"dim": it["dim"], "base": it["base"], "digits_all": [it["digits"]], "mentions": [m]}
            groups.append(g)
            it["group_ref"] = g     # 항목이 어느 묶음에 들었는지(문서별 숫자 목록을 만들 때 쓴다)
    return groups


def judge_groups(groups, other_docs):
    """각 묶음이 반대 언어 문서들 어디에 있는가. other_docs: [(doc 번호, 마크다운, items)].
    묶음마다 verdict를 단다: '그 언어에만' 또는 {reason: a|b, found, found_doc}. 문서 차례대로 보아 처음 찾은 것."""
    prepared = [(d, rm.number_tokens(md), items) for d, md, items in other_docs]
    for g in groups:
        g["verdict"] = "그 언어에만"
        for d, tokens, items in prepared:
            hit = rm.find_in_other(g, tokens, items)
            if hit:
                g["verdict"] = {**hit, "found_doc": d}
                break
    return groups


def count_domain(dom):
    docs = target_docs(dom) + added_docs(dom)
    base = ROUND4 / dom
    (base / "cache" / "md").mkdir(parents=True, exist_ok=True)
    for i, d in enumerate(docs):
        html = d["html"].read_text(encoding="utf-8")
        m = sc.measure(html)
        plain, tagged, same, n_tab = doc_markdown(d["title"], html)
        assert n_tab == len(m["tables"]), (d["title"], n_tab, len(m["tables"]))
        (base / "cache" / "md" / f"{d['lang']}_{d['revid']}.md").write_text(plain, encoding="utf-8")
        d.update(id=i, chars=m["chars"], table_count=len(m["tables"]), md_same=same, plain=plain, items=doc_items(tagged))
        assert len(d["items"]) == len(rm.extract(plain)), d["title"]  # 줄마다 뽑은 것과 통째로 뽑은 것이 같다
    pools = {}
    for lang, other in (("ko", "en"), ("en", "ko")):
        mine = [(d["id"], d["items"]) for d in docs if d["lang"] == lang]
        theirs = [(d["id"], d["plain"], d["items"]) for d in docs if d["lang"] == other]
        pools[lang] = judge_groups(pool_groups(mine), theirs)
    for lang, groups in pools.items():
        for k, g in enumerate(groups):
            g["id"] = f"{lang}{k}"
    out_docs = []
    for d in docs:
        nums = [{"raw": it["raw"], "value": it["value"], "unit": it["unit"], "in_table": it["in_table"],
                 "group": it["group_ref"]["id"], "judgment": it["group_ref"]["verdict"]} for it in d["items"]]
        out_docs.append({"id": d["id"], "kind": d["kind"], "lang": d["lang"], "target": d["target"], "title": d["title"],
                         "revid": d["revid"], "chars": d["chars"], "table_count": d["table_count"], "md_same": d["md_same"],
                         "numbers": nums})
    out_groups = {lang: [{"id": g["id"], "dim": g["dim"], "base": g["base"], "verdict": g["verdict"],
                          "in_table": any(m["in_table"] for m in g["mentions"]),
                          "mentions": [{k: m[k] for k in ("doc", "raw", "value", "unit", "in_table")} for m in g["mentions"]]}
                         for g in groups] for lang, groups in pools.items()}
    res = {"domain": dom, "docs": out_docs, "groups": out_groups}
    (base / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


def cmd_count(dom):
    res = count_domain(dom)
    s = summarize(res)
    print(dom, {k: s[k] for k in ("ko_only", "en_only", "ko_only_table", "en_only_table", "line_a", "line_b", "passed")},
          "md_same 아닌 문서", [d["title"] for d in res["docs"] if not d["md_same"]])


# --- 선 판정과 summary ------------------------------------------------------------

def summarize(res):
    """results에서 계산한 값만 돌려준다."""
    s = {"domain": res["domain"]}
    for lang in ("ko", "en"):
        only = [g for g in res["groups"][lang] if g["verdict"] == "그 언어에만"]
        s[f"{lang}_only"] = len(only)
        s[f"{lang}_only_table"] = sum(1 for g in only if g["in_table"])
    s["line_a"] = s["ko_only"] >= ONLY_MIN and s["en_only"] >= ONLY_MIN
    s["line_b"] = s["ko_only_table"] >= TABLE_ONLY_MIN and s["en_only_table"] >= TABLE_ONLY_MIN
    s["passed"] = s["line_a"] and s["line_b"]
    only_ids = {g["id"] for lang in ("ko", "en") for g in res["groups"][lang] if g["verdict"] == "그 언어에만"}
    in_tab = {g["id"] for lang in ("ko", "en") for g in res["groups"][lang] if g["in_table"]}
    rows = []
    for d in res["docs"]:
        ids = {n["group"] for n in d["numbers"] if n["group"] in only_ids}
        tab = {n["group"] for n in d["numbers"] if n["group"] in only_ids and n["in_table"]}
        rows.append({"id": d["id"], "lang": d["lang"], "title": d["title"], "kind": d["kind"], "chars": d["chars"],
                     "table_count": d["table_count"], "only": len(ids), "only_table": len(tab)})
    s["docs"] = rows
    return s


def render_domain(res, added):
    s = summarize(res)
    yn = lambda v: "넘음" if v else "못 넘음"
    L = [f"## {DOMAINS[s['domain']]} ({s['domain']})", "", "고른 5개 주제(링크한 대상 수, 두 언어 링크 수 합):", ""]
    for r in added["selected"]:
        L.append(f"- {r['ko_title']} / {r['en_title']}: 링크한 대상 {r['targets_linked']}개, 링크 수 합 {r['links_sum']}"
                 f"(한국어 {r['ko_links']}, 영어 {r['en_links']})")
    L += ["", "| 구분 | 한국어 | 영어 | 통과선 |", "|---|---|---|---|",
          f"| 선 가: 그 언어에만 있는 숫자 | {s['ko_only']} | {s['en_only']} | 각각 {ONLY_MIN} 이상 ({yn(s['line_a'])}) |",
          f"| 선 나: 그 가운데 표 안에서 나온 것 | {s['ko_only_table']} | {s['en_only_table']} | 각각 {TABLE_ONLY_MIN} 이상 ({yn(s['line_b'])}) |",
          "", f"판정(두 선 모두 넘어야 통과): **{'통과' if s['passed'] else '탈락'}**", "",
          "문서별(그 언어에만 숫자 수는 그 문서에 한 번이라도 나온 \"그 언어에만\" 숫자의 수라, 같은 숫자가 여러 문서에 있으면 "
          "문서마다 한 번씩 세어 합이 위 총수보다 클 수 있다):", "",
          "| 언어 | 제목 | 구분 | 길이(chars) | 표 수 | 그 언어에만 숫자 수 | 그 가운데 표 안 |", "|---|---|---|---|---|---|---|"]
    for r in s["docs"]:
        L.append(f"| {r['lang']} | {r['title']} | {r['kind']} | {r['chars']:,} | {r['table_count']} | {r['only']} | {r['only_table']} |")
    L.append("")
    return "\n".join(L)


def cmd_summary():
    L = ["# 코퍼스 단위 검사 (2 함께 넣을 문서 + 3 검사 다)", "",
         "규칙: decisions/stage2.md 2026-10-20 \"코퍼스 단위 검사의 규칙\" 줄. 한 언어 문서의 숫자가 반대 언어 문서 15개 어디에도 없으면 "
         "\"그 언어에만\"(같은 숫자 글자 또는 같은 차원 환산값 ±1%). 언어마다 서로 다른 값으로 센다. 숫자는 results.json에서 계산했다.", ""]
    for dom in DOMAINS:
        res = json.loads((ROUND4 / dom / "results.json").read_text(encoding="utf-8"))
        added = json.loads((ROUND4 / dom / "added.json").read_text(encoding="utf-8"))
        L.append(render_domain(res, added))
    (ROUND4 / "summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


def cmd_verify():
    """summary.md의 숫자를 results.json의 숫자 목록(문서별 numbers)에서 따로 다시 계산해 맞춘다."""
    text = (ROUND4 / "summary.md").read_text(encoding="utf-8")
    ok = True
    for dom in DOMAINS:
        res = json.loads((ROUND4 / dom / "results.json").read_text(encoding="utf-8"))
        langs = {}
        for lang in ("ko", "en"):
            seen = {}
            for d in res["docs"]:
                if d["lang"] != lang:
                    continue
                for n in d["numbers"]:
                    cur = seen.setdefault(n["group"], {"only": n["judgment"] == "그 언어에만", "tab": False})
                    cur["tab"] = cur["tab"] or n["in_table"]
            langs[lang] = (sum(v["only"] for v in seen.values()), sum(v["only"] and v["tab"] for v in seen.values()))
        sec = text.split(f"({dom})")[1].split("\n## ")[0]
        a = re.search(r"\| 선 가[^|]*\| (\d+) \| (\d+) \|", sec)
        b = re.search(r"\| 선 나[^|]*\| (\d+) \| (\d+) \|", sec)
        got = {"ko_only": int(a[1]), "en_only": int(a[2]), "ko_tab": int(b[1]), "en_tab": int(b[2])}
        want = {"ko_only": langs["ko"][0], "en_only": langs["en"][0], "ko_tab": langs["ko"][1], "en_tab": langs["en"][1]}
        good = got == want
        # 문서별 줄도 다시 센다
        for r in summarize(res)["docs"]:
            d = res["docs"][r["id"]]
            ids = {n["group"] for n in d["numbers"] if n["judgment"] == "그 언어에만"}
            tab = {n["group"] for n in d["numbers"] if n["judgment"] == "그 언어에만" and n["in_table"]}
            row = f"| {r['lang']} | {r['title']} | {r['kind']} | {r['chars']:,} | {r['table_count']} | {len(ids)} | {len(tab)} |"
            if row not in sec:
                good = False
                print("문서 줄 불일치", dom, row)
        ok = ok and good
        print(dom, "summary", got, "다시 계산", want, "일치" if good else "불일치")
    print("전체", "일치" if ok else "불일치")
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    doms = args if args else list(DOMAINS)
    if cmd in ("select", "fetch", "count"):
        for dom in doms:
            if cmd == "select" and "--with-infobox-grid" in sys.argv:
                cmd_select(dom, infobox_grid=True)
            else:
                {"select": cmd_select, "fetch": cmd_fetch, "count": cmd_count}[cmd](dom)
    elif cmd == "summary":
        cmd_summary()
    elif cmd == "verify":
        sys.exit(0 if cmd_verify() else 1)
    else:
        raise SystemExit(__doc__)
