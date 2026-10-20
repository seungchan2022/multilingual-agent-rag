"""2단계 분야 고르기(STEPPER 기준)에 쓰는 숫자를 재는 프로그램.

세 분야(rare_earth, exoplanets, moons)의 대상 30개마다 한국어·영어 위키백과 문서의 본문 길이와 표의 수를 센다.
세는 규칙은 research_notes/stage2_domain_survey/measure.py의 measure(html)을 경로로 불러와 그대로 쓴다.

  python3 stepper_check.py targets   네트워크 없이 대상 30개를 출력한다
  python3 stepper_check.py fetch     한국어는 판을 고정해, 영어는 지금 판을 받아 cache/에 둔다
  python3 stepper_check.py count     받아 둔 HTML 전부를 다시 세어 results.json을 새로 쓴다
  python3 stepper_check.py summary   results.json으로 분야마다 숫자와 선의 통과 여부를 summary.md에 쓴다
"""
import importlib.util
import json
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUND2 = ROOT / "research_notes" / "stage2_stem_select" / "round2"
OUT = ROUND2 / "stepper_check"
DOMAINS = ("rare_earth", "exoplanets", "moons")
UA = {"User-Agent": "MultilingualAgentRAG-corpus/1.0 (https://github.com/seungchan2022/multilingual-agent-rag)"}
PAUSE = 1.5
WAITS = (10, 30, 60, 120)


def _load_measure():
    path = ROOT / "research_notes" / "stage2_domain_survey" / "measure.py"
    spec = importlib.util.spec_from_file_location("survey_measure", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.measure


measure = _load_measure()


def load_targets(round2=ROUND2):
    """대상 30개를 [{domain, target, ko_title, ko_revid, en_title}]로 돌려준다. 못 찾으면 SystemExit."""
    langlinks = json.loads((round2 / "criterion4_langlinks.json").read_text(encoding="utf-8"))
    rows, missing = [], []
    for dom in DOMAINS:
        qs = json.loads((round2 / dom / "questions.json").read_text(encoding="utf-8"))
        docs = json.loads((round2 / dom / "docs.json").read_text(encoding="utf-8"))
        for q in qs:
            title = q["evidence_quotes"][0]["doc"]
            revid = (docs.get(title) or {}).get("revid")
            en = (langlinks.get(dom) or {}).get(title)
            if not revid:
                missing.append(f"{dom} {q['target']}: docs.json에 '{title}'의 revid가 없다")
            if not en:
                missing.append(f"{dom} {q['target']}: criterion4_langlinks.json에 '{title}'의 영어 제목이 없다")
            rows.append({"domain": dom, "target": q["target"], "ko_title": title, "ko_revid": revid, "en_title": en})
    if missing:
        raise SystemExit("대상을 맞추지 못했다:\n" + "\n".join(missing))
    return rows


def cmd_targets():
    rows = load_targets()
    for r in rows:
        print(f"{r['domain']} | {r['target']} | {r['ko_title']} | {r['ko_revid']} | {r['en_title']}")
    print(f"대상 {len(rows)}개")


def api(lang, **p):
    p.update(format="json", formatversion=2)
    url = f"https://{lang}.wikipedia.org/w/api.php?{urllib.parse.urlencode(p)}"
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


def cmd_fetch():
    rows = load_targets()
    cache = OUT / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    log = OUT / "fetched.jsonl"
    done = set()
    if log.exists():
        done = {(r["domain"], r["target"], r["lang"]) for r in map(json.loads, log.read_text(encoding="utf-8").splitlines())}
    for r in rows:
        for lang in ("ko", "en"):
            key = (r["domain"], r["target"], lang)
            if key in done:
                continue
            if lang == "ko":
                d = api("ko", action="parse", oldid=r["ko_revid"], prop="text|revid")
            else:
                d = api("en", action="parse", page=r["en_title"], prop="text|revid", redirects=1)
            if "parse" not in d:
                raise RuntimeError(f"{key}: {d.get('error')}")
            p = d["parse"]
            (cache / f"{lang}_{p['revid']}.html").write_text(p["text"], encoding="utf-8")
            rec = {"domain": r["domain"], "target": r["target"], "lang": lang, "title": p["title"], "revid": p["revid"],
                   "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
            with log.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"{r['domain']} | {r['target']} | {lang} | {p['title']} | {p['revid']}", flush=True)


def cmd_count():
    cache = OUT / "cache"
    log = OUT / "fetched.jsonl"
    recs = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()]
    rows = []
    for r in recs:
        m = measure((cache / f"{r['lang']}_{r['revid']}.html").read_text(encoding="utf-8"))
        rows.append({"domain": r["domain"], "target": r["target"], "lang": r["lang"], "title": r["title"],
                     "revid": r["revid"], "chars": m["chars"], "table_count": len(m["tables"]), "tables": m["tables"]})
    (OUT / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("센 문서", len(rows))


def summarize(rows):
    """results 행 목록에서 분야마다 숫자와 선의 통과 여부를 계산한다. 고르는 규칙은 계산하지 않는다."""
    out = []
    for dom in DOMAINS:
        rs = [r for r in rows if r["domain"] == dom]
        if not rs:
            continue
        ko = [r for r in rs if r["lang"] == "ko"]
        en = [r for r in rs if r["lang"] == "en"]
        med = lambda l: int(statistics.median([r["chars"] for r in l])) if l else 0
        tab = lambda l: sum(1 for r in l if r["table_count"] >= 1)
        s = {"domain": dom, "ko_docs": len(ko), "en_docs": len(en),
             "ko_median": med(ko), "en_median": med(en), "ko_tables": tab(ko), "en_tables": tab(en)}
        s["line1"] = s["ko_median"] >= 5000 and s["en_median"] >= 5000
        s["line2"] = s["en_tables"] >= 4
        s["line3"] = s["ko_tables"] >= 4
        s["passed"] = sum([s["line1"], s["line2"], s["line3"]])
        s["out"] = s["ko_tables"] == 0 or s["en_tables"] == 0
        out.append(s)
    return out


def render(summ):
    yn = lambda v: "넘음" if v else "못 넘음"
    lines = ["| 분야 | 한국어 문서 수 | 영어 문서 수 | 한국어 본문 중앙값 | 영어 본문 중앙값 | 표 있는 한국어 문서 | 표 있는 영어 문서 | 선 1 | 선 2 | 선 3 | 넘은 선 | 탈락 표시 |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in summ:
        lines.append(f"| {s['domain']} | {s['ko_docs']} | {s['en_docs']} | {s['ko_median']:,} | {s['en_median']:,} | "
                     f"{s['ko_tables']} | {s['en_tables']} | {yn(s['line1'])} | {yn(s['line2'])} | {yn(s['line3'])} | "
                     f"{s['passed']} | {'탈락' if s['out'] else '-'} |")
    lines += ["", "선 1: 한국어 중앙값 5000 이상이고 영어 중앙값 5000 이상. 선 2: 표 있는 영어 문서 4개 이상. "
              "선 3: 표 있는 한국어 문서 4개 이상. 탈락 표시: 표 있는 한국어 문서 0개이거나 표 있는 영어 문서 0개."]
    return "\n".join(lines) + "\n"


def cmd_summary():
    rows = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
    text = render(summarize(rows))
    (OUT / "summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"targets": cmd_targets, "fetch": cmd_fetch, "count": cmd_count, "summary": cmd_summary}.get(cmd)
    if not fn:
        raise SystemExit(__doc__)
    fn()
