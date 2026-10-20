"""위성 분야를 고르기 전에 확인할 두 기준(decisions/stage2.md 마지막 줄)의 숫자를 재는 프로그램.

  .venv/bin/python moons_check.py infobox   기준 ①: 대상 10개 문서의 정보 상자에서 '이름 칸과 값 칸이 모두 있는 줄'을 센다(네트워크 없음)
  .venv/bin/python moons_check.py lists     기준 ②: 네 목록 문서를 받아 표에 대상 위성이 값과 함께 나오는지 센다(네트워크 씀)
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
ROUND2 = ROOT / "research_notes" / "stage2_stem_select" / "round2"
SRC = ROUND2 / "stepper_check"
OUT = ROUND2 / "moons_check"
UA = {"User-Agent": "MultilingualAgentRAG-corpus/1.0 (https://github.com/seungchan2022/multilingual-agent-rag)"}
PAUSE = 1.5
WAITS = (10, 30, 60, 120)
INFOBOX_LINE_MIN = 36
LIST_MOON_MIN = 3
LIST_TITLES = ("토성의 위성", "목성의 위성", "천왕성의 위성", "해왕성의 위성")
TABLE_CLASS = re.compile(r"wikitable|toccolours|sortable|table-pale")
SKIP_CLASS = re.compile(r"infobox|navbox|sidebar|metadata|ambox")


def text_of(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


def own_rows(table):
    """겹친 표의 줄을 빼고 이 표의 줄만 돌려준다."""
    return [tr for tr in table.find_all("tr") if tr.find_parent("table") is table]


def cells_of(tr):
    return tr.find_all(["th", "td"], recursive=False)


def infobox_lines(html):
    """첫 infobox 표에서 th 하나와 td 하나가 모두 있고 둘 다 글자가 있는 줄의 (이름, 값) 목록."""
    soup = BeautifulSoup(html, "html.parser")
    box = soup.find(lambda t: t.name == "table" and "infobox" in " ".join(t.get("class", [])))
    if box is None:
        return []
    out = []
    for tr in own_rows(box):
        ths = tr.find_all("th", recursive=False)
        tds = tr.find_all("td", recursive=False)
        if len(ths) == 1 and len(tds) == 1:
            name, value = text_of(ths[0]), text_of(tds[0])
            if name and value:
                out.append((name, value))
    return out


def pick_tables(html):
    """목록 문서에서 셀 수 기준을 통과한 표만 돌려준다."""
    soup = BeautifulSoup(html, "html.parser")
    picked = []
    for table in soup.find_all("table"):
        cls = " ".join(table.get("class", []))
        if not TABLE_CLASS.search(cls):
            continue
        if any(SKIP_CLASS.search(" ".join(p.get("class", []))) for p in table.parents if hasattr(p, "get")):
            continue
        rows = [cells_of(tr) for tr in own_rows(table)]
        if sum(1 for r in rows if len(r) >= 2) >= 2:
            picked.append(table)
    return picked


def match_rows(table, targets):
    """표에서 {위성: 그 줄의 글자} — 이름이 나온 칸 말고 다른 칸에 숫자가 있는 줄만."""
    found = {}
    for tr in own_rows(table):
        cells = cells_of(tr)
        if len(cells) < 2:
            continue
        texts = [text_of(c) for c in cells]
        for name in targets:
            pat = re.compile(rf"(?<![가-힣]){re.escape(name)}(?![가-힣])")
            has = [bool(pat.search(t)) for t in texts]
            if any(has) and any(re.search(r"\d", t) for t, h in zip(texts, has) if not h):
                found.setdefault(name, " | ".join(texts)[:120])
    return found


def load_targets():
    rows = [json.loads(l) for l in (SRC / "fetched.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return [r for r in rows if r["domain"] == "moons" and r["lang"] == "ko"]


def cmd_infobox():
    docs, total = [], 0
    for r in load_targets():
        lines = infobox_lines((SRC / "cache" / f"ko_{r['revid']}.html").read_text(encoding="utf-8"))
        total += len(lines)
        docs.append({"target": r["target"], "revid": r["revid"], "count": len(lines),
                     "lines": [{"name": n, "value": v} for n, v in lines]})
    res = {"docs": docs, "total": total, "threshold": INFOBOX_LINE_MIN, "pass": total >= INFOBOX_LINE_MIN}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "infobox.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    for d in docs:
        print(f"{d['target']} (revid {d['revid']}): {d['count']}줄")
        for l in d["lines"]:
            print(f"   {l['name']}: {l['value'][:30]}")
    print(f"합 {total}, 기준 ① 넘음: {res['pass']}")


def api(**p):
    p.update(format="json", formatversion=2)
    url = f"https://ko.wikipedia.org/w/api.php?{urllib.parse.urlencode(p)}"
    err = None
    for wait in (0,) + WAITS:
        time.sleep(wait)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as resp:
                d = json.load(resp)
            time.sleep(PAUSE)
            return d
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                raise
            err = e
        except urllib.error.URLError as e:
            err = e
    raise RuntimeError(f"요청 실패: {err}")


def fetch_list_docs():
    """네 문서를 받아 [{title, got_title, revid}]를 돌려준다. 문서가 없으면 revid가 None."""
    cache = OUT / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    log = OUT / "fetched.jsonl"
    done = {}
    if log.exists():
        for l in log.read_text(encoding="utf-8").splitlines():
            if l.strip():
                r = json.loads(l)
                done[r["title"]] = r
    docs = []
    for title in LIST_TITLES:
        if title not in done:
            d = api(action="parse", page=title, prop="text|revid", redirects=1)
            if "error" in d:
                rec = {"title": title, "got_title": None, "revid": None, "error": d["error"].get("code"),
                       "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            else:
                p = d["parse"]
                (cache / f"ko_{p['revid']}.html").write_text(p["text"], encoding="utf-8")
                rec = {"title": title, "got_title": p["title"], "revid": p["revid"],
                       "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            with log.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            done[title] = rec
        docs.append(done[title])
    return docs


def cmd_lists():
    targets = [r["target"] for r in load_targets()]
    out = []
    for rec in fetch_list_docs():
        if rec["revid"] is None:
            out.append({"title": rec["title"], "revid": None, "status": "없음", "tables": 0, "found": {}, "count": 0})
            continue
        html = (OUT / "cache" / f"ko_{rec['revid']}.html").read_text(encoding="utf-8")
        tables = pick_tables(html)
        found = {}
        for t in tables:
            for k, v in match_rows(t, targets).items():
                found.setdefault(k, v)
        out.append({"title": rec["title"], "got_title": rec["got_title"], "revid": rec["revid"], "tables": len(tables),
                    "found": found, "count": len(found)})
    res = {"docs": out, "threshold": LIST_MOON_MIN, "pass": any(d["count"] >= LIST_MOON_MIN for d in out)}
    (OUT / "lists.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    for d in out:
        print(f"{d['title']} (받은 제목 {d.get('got_title')}, revid {d['revid'] or '없음'}): 고른 표 {d['tables']}, 대상 위성 {d['count']}")
        for k, v in d["found"].items():
            print(f"   {k}: {v}")
    print(f"기준 ② 넘음: {res['pass']}")


if __name__ == "__main__":
    cmds = {"infobox": cmd_infobox, "lists": cmd_lists}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    cmds[sys.argv[1]]()
