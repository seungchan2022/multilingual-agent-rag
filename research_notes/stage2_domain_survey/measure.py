"""2단계 도메인 후보를 재는 프로그램.

기준은 decisions/stage2.md의 2026-10-13 "도메인 후보를 재는 방법과 통과선" 줄과 그 아래 보충 줄에 있다.

  python measure.py fetch <캐시 폴더> [분야 ...]   위키백과 문서를 받아 캐시에 두고 fetched.jsonl에 적는다
  python measure.py count <캐시 폴더>              캐시 전체를 다시 세어 results.json을 새로 쓴다
  python measure.py judge                          results.json과 portal.json으로 통과 여부 표를 낸다

받는 일과 세는 일을 나눈 까닭: 세는 규칙을 고치면 옛 규칙의 숫자와 새 규칙의 숫자가 섞이지 않게
전부 다시 세기 위해서다. 받은 문서의 판 번호(revid)는 fetched.jsonl에 남는다.
"""
import json, re, statistics, sys, time, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
UA = {"User-Agent": "MultilingualAgentRAG-survey/0.3 (study project)"}
SKIP = re.compile(r"infobox|navbox|sidebar|metadata|ambox|reflist|references|mw-editsection|catlinks|toc\b|noprint|hatnote|sistersitebox|authority-control|portalbox|mw-empty-elt|navigation-not-searchable|side-box|thumbcaption")
TABLE = re.compile(r"wikitable|toccolours|sortable|table-pale")
# 기후 자료 틀과 인구 변화 틀. 두 언어 문서에 같은 값으로 들어가는 일이 많아 참고 칸에서 따로 센다.
TEMPLATE_TABLE = re.compile(r"Climate data|기후 자료|Historical population|인구 변화")
VOID = {"br", "img", "hr", "input", "meta", "link", "col", "wbr", "source", "area", "base", "embed", "param", "track"}


def api(lang, **p):
    p.update(format="json", formatversion=2, redirects=1)
    url = f"https://{lang}.wikipedia.org/w/api.php?{urllib.parse.urlencode(p)}"
    err = None
    for wait in (0, 10, 30, 60, 120):
        time.sleep(wait)
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))
            time.sleep(1.5)
            return d
        except Exception as e:
            err = e
    raise RuntimeError(f"요청 실패: {err}")


class Body(HTMLParser):
    """본문 글자와 표를 센다. SKIP에 걸린 상자와 각주 표시는 통째로 건너뛴다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # (tag, skip 여부, 표 여부)
        self.skip = 0
        self.text = []
        self.tables = []
        self.cur = []        # 열려 있는 표의 기록(겹친 표는 바깥 것만 센다)
        self.in_head = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        cls = dict(attrs).get("class") or ""
        skip = bool(SKIP.search(cls)) or tag in ("style", "script") or (tag == "sup" and "reference" in cls)
        # 표는 일단 전부 열어 두고, 닫을 때 아래 두 조건을 다 채운 것만 센다.
        #  1) 표 모양의 class가 있거나 머리글 칸(th)이 있다
        #     (class만 보면 인구 변화 틀처럼 class 이름이 다른 표가 빠진다)
        #  2) 칸이 2개 이상인 줄이 2줄 이상이다
        #     (글을 여러 단으로 나누려고 쓴 표를 빼기 위해서다)
        is_table = tag == "table" and not skip and not self.skip
        self.stack.append((tag, skip, is_table))
        if skip:
            self.skip += 1
        if is_table:
            self.cur.append({"rows": 0, "wide": 0, "cells": 0, "head": "", "ok": bool(TABLE.search(cls))})
        if self.cur and not self.skip:
            t = self.cur[0]
            if tag == "tr":
                if t["cells"] >= 2:
                    t["wide"] += 1
                t["rows"] += 1
                t["cells"] = 0
            if tag in ("td", "th"):
                t["cells"] += 1
            if tag == "th":
                t["ok"] = True
            if tag in ("caption", "th") and len(t["head"]) < 80:
                self.in_head += 1

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, skip, is_table = self.stack.pop()
            if skip:
                self.skip -= 1
            if is_table:
                rec = self.cur.pop()
                if rec["cells"] >= 2:
                    rec["wide"] += 1
                if not self.cur and rec["ok"] and rec["wide"] >= 2:
                    self.tables.append(rec)
            if t in ("caption", "th") and self.in_head:
                self.in_head -= 1
                if self.cur:
                    self.cur[0]["head"] += " | "
            if t == tag:
                break

    def handle_data(self, data):
        if self.skip:
            return
        self.text.append(data)
        if self.cur and self.in_head and len(self.cur[0]["head"]) < 80:
            self.cur[0]["head"] += data.strip()


def measure(html):
    b = Body()
    b.feed(html)
    b.close()
    text = re.sub(r"\s+", " ", "".join(b.text)).strip()
    tables = [{"rows": t["rows"], "head": re.sub(r"\s+", " ", t["head"])[:80]} for t in b.tables]
    return {"chars": len(text), "tables": tables}


def resolve(title):
    d = api("ko", action="query", titles=title, prop="langlinks|pageprops", lllang="en", ppprop="disambiguation")
    pg = (d.get("query", {}).get("pages") or [{}])[0]
    how = "제목 그대로"
    if pg.get("missing") or "title" not in pg:
        s = api("ko", action="query", list="search", srsearch=title, srlimit=1).get("query", {}).get("search") or []
        if not s:
            return None, None, "한국어 문서를 찾지 못함"
        d = api("ko", action="query", titles=s[0]["title"], prop="langlinks|pageprops", lllang="en", ppprop="disambiguation")
        pg = d["query"]["pages"][0]
        how = "검색으로 찾음"
    if "disambiguation" in (pg.get("pageprops") or {}):
        how += " · 동음이의 문서"
    en = (pg.get("langlinks") or [{}])[0].get("title")
    return pg["title"], en, how


def name(lang, revid):
    return f"{lang}_{revid}.html"


def fetch(cache, want):
    cache.mkdir(parents=True, exist_ok=True)
    subjects = json.loads((HERE / "subjects.json").read_text(encoding="utf-8"))
    out = HERE / "fetched.jsonl"
    done = set()
    if out.exists():
        done = {(r["domain"], r["subject"]) for r in map(json.loads, out.read_text(encoding="utf-8").splitlines())}
    for dom in want or list(subjects):
        for sub in subjects[dom]:
            if (dom, sub) in done:
                continue
            ko, en, how = resolve(sub)
            rec = {"domain": dom, "subject": sub, "resolved": how, "ko": None, "en": None}
            for lang, title in (("ko", ko), ("en", en)):
                if not title:
                    continue
                p = api(lang, action="parse", page=title, prop="text|revid")["parse"]
                (cache / name(lang, p["revid"])).write_text(p["text"], encoding="utf-8")
                rec[lang] = {"title": p["title"], "revid": p["revid"]}
            with out.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f2 = lambda r: "없음" if not r else r["title"]
            print(f"{dom} | {sub} [{how}] | 한 {f2(rec['ko'])} | 영 {f2(rec['en'])}", flush=True)


def count(cache):
    rows = []
    for r in map(json.loads, (HERE / "fetched.jsonl").read_text(encoding="utf-8").splitlines()):
        for lang in ("ko", "en"):
            if r[lang]:
                r[lang].update(measure((cache / name(lang, r[lang]["revid"])).read_text(encoding="utf-8")))
        rows.append(r)
    (HERE / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("센 대상", len(rows))


def judge():
    rows = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    portal = {}
    if (HERE / "portal.json").exists():
        portal = json.loads((HERE / "portal.json").read_text(encoding="utf-8"))
    doms = {}
    for r in rows:
        doms.setdefault(r["domain"], []).append(r)
    print("| 분야 | 잰 대상 | ① 두 언어 다 있음 | ② 한국어 중앙값 | ② 영어 중앙값 | ③ 표 있는 영어 문서 | ④ 표 있는 한국어 문서 | 포털: 통계 표 | ⑤ 포털: 대상 자료 | 1차 | 참고: 틀 말고 표가 있는 영어 문서 |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for dom, rs in doms.items():
        both = sum(1 for r in rs if r["ko"] and r["en"])
        # ② 중앙값은 있는 문서만으로 낸다. 없는 문서는 ①이 따진다.
        med = lambda l: int(statistics.median([r[l]["chars"] for r in rs if r[l]])) if any(r[l] for r in rs) else 0
        tab = lambda l: sum(1 for r in rs if r[l] and r[l]["tables"])
        other = sum(1 for r in rs if r["en"] and any(not TEMPLATE_TABLE.search(t["head"]) for t in r["en"]["tables"]))
        p = portal.get(dom, {})
        stat, subj = p.get("stat_table"), p.get("subject_data")
        c = [both >= 6, med("ko") >= 5000 and med("en") >= 5000, tab("en") >= 3, tab("ko") >= 3 or bool(stat), bool(subj)]
        if stat is None or subj is None:
            verdict = "포털 확인 전" if all(c[:3]) else "탈락"
        else:
            verdict = "통과" if all(c) else "탈락"
        yn = lambda v: "미확인" if v is None else ("있음" if v else "없음")
        print(f"| {dom} | {len(rs)} | {both} | {med('ko'):,} | {med('en'):,} | {tab('en')} | {tab('ko')} | {yn(stat)} | {yn(subj)} | {verdict} | {other} |")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(Path(sys.argv[2]), sys.argv[3:])
    elif cmd == "count":
        count(Path(sys.argv[2]))
    elif cmd == "judge":
        judge()
