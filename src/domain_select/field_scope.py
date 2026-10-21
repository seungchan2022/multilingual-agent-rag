"""분야 문서 보기(decisions/stage2.md 2026-10-21 "1 문서 보기의 범위" 줄)에서 범위 안의 문서를 모으고 구조를 기록하는 프로그램.

  .venv/bin/python src/domain_select/field_scope.py tree [분야]       한국어 위키백과 분류를 깊이 2까지 걷는다(네트워크). tree.json을 쓴다
  .venv/bin/python src/domain_select/field_scope.py scope [분야]      tree.json에 더하고 빼는 규칙을 적용해 scope.json을 쓴다
  .venv/bin/python src/domain_select/field_scope.py langlinks [분야]  범위 문서의 영어 짝을 찾는다(네트워크). langlinks.json을 쓴다
  .venv/bin/python src/domain_select/field_scope.py fetch [분야]      한·영 문서를 parse로 받아 gzip으로 cache/에 둔다(네트워크)
  .venv/bin/python src/domain_select/field_scope.py count [분야]      받은 문서를 읽어 results.json을 쓴다
  .venv/bin/python src/domain_select/field_scope.py summary           results.json·scope.json으로 summary.md, 분야별 docs.md, summary_numbers.json을 쓴다
  .venv/bin/python src/domain_select/field_scope.py verify            summary_numbers.json과 두 마크다운을 다시 계산해 맞춘다

분야를 안 쓰면 exoplanets, rare_earth 차례로 둘 다 한다.

범위 규칙:
  - 출발 분류의 깊이는 0, 그 하위 분류는 1, 그 아래는 2다. 분류에 바로 든 본 이름공간 문서는 그 분류의 깊이를 얻는다.
    깊이 2 분류의 하위 분류는 보지 않는다. 한 분류는 한 번만 보고(가장 얕은 깊이), 한 문서는 가장 얕은 깊이를 갖는다.
    그 깊이로 들어온 분류를 모두 via에 적는다.
  - 더하는 것은 깊이를 null로 적고 via에 "더함: ..."을 적는다. 이미 들어온 문서면 깊이는 그대로 두고 via에 이어 붙인다.
  - 빼는 것은 제목이 정규식에 맞는 문서이고 이유와 함께 scope.json의 excluded에 둔다.
  - 영어는 범위에 든 한국어 문서의 언어 링크(영어)만 본다. 짝이 없는 문서도 범위에 둔다(en_title null).

이 프로그램은 숫자를 뽑지 않는다. 문서의 구조(영어 짝, 본문 길이, 표)만 적는다. 한쪽 언어에만 있는 숫자는 여기서 세지 않는다.
요청은 한 번에 하나씩 보내고 코퍼스 프로그램의 get(쉬기·다시 하기)을 쓴다.
"""
import gzip
import json
import re
import statistics
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "corpus"))
import stepper_check as sc  # noqa: E402  measure(본문 길이·표), load_targets(대상 10개)
from fetch import UA, GAP, get, wait_from  # noqa: E402

ROOT = sc.ROOT
ROUND5 = ROOT / "research_notes" / "stage2_stem_select" / "round5"
HEADERS = {"User-Agent": UA, "Accept-Encoding": "gzip"}
MAX_DEPTH = 2
BATCH = 50
FIELDS = {
    "exoplanets": {"ko_name": "외계 행성", "roots": ["분류:외계 행성"], "add_categories": ["분류:외계행성학"], "add_pages": [],
                   "exclude": None},
    "rare_earth": {"ko_name": "희토류 원소", "roots": ["분류:란타넘족", "분류:스칸듐", "분류:이트륨"],
                   "add_categories": ["분류:희토류 합금"], "add_pages": ["희토류 원소"],
                   "exclude": {"regex": r"^\S+-\d+m?\d*$", "reason": "동위 원소 하나를 다룬 문서(제목이 원소 이름-질량수 꼴)"}},
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


# --- 요청 ---------------------------------------------------------------------

def busy(body, h):
    """서버가 바쁘다(maxlag)는 응답이면 쉴 초를, 아니면 None. fetch.fetch_wiki와 같은 규칙."""
    try:
        e = json.loads(body).get("error")
    except ValueError:
        return None
    return wait_from(h, 5) if e and e.get("code") == "maxlag" else None


def api(lang, **p):
    """Action API를 한 번 부르고 GAP초 쉰다. 모든 주소에 maxlag=5를 붙인다."""
    url = f"https://{lang}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({**p, "format": "json", "formatversion": 2, "maxlag": 5})
    body = get(url, HEADERS, busy)
    time.sleep(GAP)
    return json.loads(body)


# --- 1 분류 걷기 ---------------------------------------------------------------

def members(api, cat, cmtype, namespace=None):
    """분류에 바로 든 항목의 제목을 continue를 끝까지 따라가며 모은다."""
    p = dict(action="query", list="categorymembers", cmtitle=cat, cmtype=cmtype, cmlimit="max")
    if namespace is not None:
        p["cmnamespace"] = namespace
    out, more = [], {}
    while True:
        d = api("ko", **p, **more)
        if "error" in d:
            raise RuntimeError(f"{cat}: {d['error']}")
        out += [m["title"] for m in d.get("query", {}).get("categorymembers", [])]
        if "continue" not in d:
            return out
        more = d["continue"]


def walk(roots, api, max_depth=MAX_DEPTH):
    """{분류: {depth, pages, subcats}}. 너비 우선이라 분류는 가장 얕은 깊이에서 한 번만 보인다(순환·두 번 닿는 분류 포함).
    max_depth 분류의 하위 분류는 보지 않는다(subcats null)."""
    cats, level = {}, list(dict.fromkeys(roots))
    for depth in range(max_depth + 1):
        nxt = []
        for c in level:
            subs = members(api, c, "subcat") if depth < max_depth else None
            cats[c] = {"depth": depth, "pages": members(api, c, "page", 0), "subcats": subs}
            nxt += subs or []
        level = [c for c in dict.fromkeys(nxt) if c not in cats]
    return cats


def cmd_tree(field, api=api, out=ROUND5):
    cfg = FIELDS[field]
    cats = walk(cfg["roots"], api)
    added = {c: members(api, c, "page", 0) for c in cfg["add_categories"]}    # 더하는 분류는 바로 든 문서만 본다
    tree = {"field": field, "fetched_at": now(), "roots": cfg["roots"], "max_depth": MAX_DEPTH, "categories": cats,
            "additions": {"categories": added, "pages": cfg["add_pages"]}}
    write_json(out / field / "tree.json", tree)
    per = [sum(1 for c in cats.values() if c["depth"] == d) for d in range(MAX_DEPTH + 1)]
    print(field, "분류", len(cats), "(깊이별", per, ")", "더하는 분류의 문서", {c: len(p) for c, p in added.items()})


# --- 2 범위 정하기 ---------------------------------------------------------------

def build_scope(tree, exclude, target_titles):
    """tree(tree.json)에 더하고 빼는 규칙을 적용한 scope. exclude는 {regex, reason} 또는 None. 네트워크를 쓰지 않는다."""
    found = {}
    for cat, c in tree["categories"].items():
        for t in c["pages"]:
            cur = found.get(t)
            if cur is None or c["depth"] < cur["depth"]:
                found[t] = {"depth": c["depth"], "via": [cat]}
            elif c["depth"] == cur["depth"]:
                cur["via"].append(cat)
    for cur in found.values():
        cur["via"].sort()
    labels = [(f"더함: {cat}", pages) for cat, pages in tree["additions"]["categories"].items()]
    labels.append(("더함: 문서", tree["additions"]["pages"]))
    for label, pages in labels:
        for t in pages:
            cur = found.setdefault(t, {"depth": None, "via": []})
            if label not in cur["via"]:
                cur["via"].append(label)
    included, excluded = [], []
    for t, cur in found.items():
        if exclude and re.search(exclude["regex"], t):
            excluded.append({"ko_title": t, "reason": exclude["reason"]})
        else:
            included.append({"ko_title": t, **cur})
    included.sort(key=lambda r: (r["depth"] is None, r["depth"] or 0, r["ko_title"]))
    excluded.sort(key=lambda r: r["ko_title"])
    have = {r["ko_title"] for r in included}
    return {"field": tree["field"], "included": included, "excluded": excluded,
            "missing_targets": [t for t in target_titles if t not in have]}


def cmd_scope(field, out=ROUND5, targets=None):
    tree = read_json(out / field / "tree.json")
    if targets is None:
        targets = [r["ko_title"] for r in sc.load_targets() if r["domain"] == field]
    scope = build_scope(tree, FIELDS[field]["exclude"], targets)
    write_json(out / field / "scope.json", scope)
    print(field, "범위 안", len(scope["included"]), "뺀 것", len(scope["excluded"]), "대상 중 범위 밖", scope["missing_targets"])


# --- 3 영어 짝 --------------------------------------------------------------------

def lang_pairs(titles, api):
    """한국어 제목 -> 영어 제목(없으면 None). 50개씩 묻고, 응답의 normalized·redirects를 따라 요청한 제목으로 되돌린다."""
    out = {}
    for i in range(0, len(titles), BATCH):
        chunk = titles[i:i + BATCH]
        params = dict(action="query", titles="|".join(chunk), prop="langlinks", lllang="en", lllimit="max", redirects=1)
        mapping, pages, more = {}, {}, {}
        while True:
            d = api("ko", **params, **more)
            if "error" in d:
                raise RuntimeError(f"langlinks: {d['error']}")
            q = d.get("query", {})
            for n in q.get("normalized", []) + q.get("redirects", []):
                mapping[n["from"]] = n["to"]
            for p in q.get("pages", []):
                cur = pages.setdefault(p["title"], None)
                for ll in p.get("langlinks") or []:
                    cur = cur or ll["title"]
                pages[p["title"]] = cur
            if "continue" not in d:
                break
            more = d["continue"]
        for t in chunk:
            f = t
            for _ in range(6):
                if f in mapping and mapping[f] != f:
                    f = mapping[f]
                else:
                    break
            out[t] = pages.get(f)
    return out


def cmd_langlinks(field, api=api, out=ROUND5):
    titles = [r["ko_title"] for r in read_json(out / field / "scope.json")["included"]]
    pairs = lang_pairs(titles, api)
    write_json(out / field / "langlinks.json", {"fetched_at": now(), "pairs": pairs})
    print(field, "영어 짝 있음", sum(1 for v in pairs.values() if v), "없음", sum(1 for v in pairs.values() if not v))


# --- 4 받기 -----------------------------------------------------------------------

def read_log(path):
    """fetched.jsonl의 줄. 같은 (언어, 요청한 제목)이 여러 번이면 마지막 줄이 이긴다."""
    if not path.exists():
        return {}
    recs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
    return {(r["lang"], r["title_requested"]): r for r in recs}


def cmd_fetch(field, api=api, out=ROUND5):
    base = out / field
    (base / "cache").mkdir(parents=True, exist_ok=True)
    titles = [r["ko_title"] for r in read_json(base / "scope.json")["included"]]
    pairs = read_json(base / "langlinks.json")["pairs"]
    if [t for t in titles if t not in pairs]:
        raise SystemExit(f"{field}: langlinks를 먼저 한다(scope.json과 langlinks.json의 문서가 다르다)")
    jobs = list(dict.fromkeys([("ko", t) for t in titles] + [("en", pairs[t]) for t in titles if pairs[t]]))
    log = base / "fetched.jsonl"
    done = {k for k, r in read_log(log).items() if "error" not in r}      # 오류로 끝난 것은 다시 받아 본다
    for lang, title in jobs:
        if (lang, title) in done:
            continue
        d = api(lang, action="parse", page=title, prop="text|revid", redirects=1)
        if "parse" not in d:
            rec = {"lang": lang, "title_requested": title, "error": (d.get("error") or {}).get("code") or "parse 없음", "fetched_at": now()}
        else:
            p = d["parse"]
            file = f"cache/{lang}_{p['revid']}.html.gz"
            (base / file).write_bytes(gzip.compress(p["text"].encode("utf-8")))
            rec = {"lang": lang, "title_requested": title, "title": p["title"], "revid": p["revid"], "fetched_at": now(), "file": file}
        with log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{field} | {lang} | {title} | {rec.get('revid') or 'error: ' + rec['error']}", flush=True)


# --- 5 세기 -----------------------------------------------------------------------

def side(base, rec):
    """받은 문서 한 쪽의 {revid, chars, n_tables, tables}와 오류 글(없으면 None)."""
    empty = {"revid": None, "chars": None, "n_tables": None, "tables": None}
    if rec is None:
        return empty, "받지 않음"
    if "error" in rec:
        return empty, rec["error"]
    m = sc.measure(gzip.decompress((base / rec["file"]).read_bytes()).decode("utf-8"))
    return {"revid": rec["revid"], "chars": m["chars"], "n_tables": len(m["tables"]), "tables": m["tables"]}, None


def cmd_count(field, out=ROUND5):
    base = out / field
    scope = read_json(base / "scope.json")
    pairs = read_json(base / "langlinks.json")["pairs"]
    log = read_log(base / "fetched.jsonl")
    rows = []
    for r in scope["included"]:
        en_title = pairs[r["ko_title"]]
        ko, ko_err = side(base, log.get(("ko", r["ko_title"])))
        en, en_err = side(base, log.get(("en", en_title))) if en_title else (side(base, None)[0], None)
        errors = [f"{lang}: {e}" for lang, e in (("ko", ko_err), ("en", en_err)) if e]
        rows.append({"ko_title": r["ko_title"], "depth": r["depth"], "via": r["via"], "en_title": en_title,
                     **{f"ko_{k}": v for k, v in ko.items()}, **{f"en_{k}": v for k, v in en.items()}, "errors": errors})
    write_json(base / "results.json", rows)
    print(field, "센 문서", len(rows), "오류", sum(len(r["errors"]) for r in rows))


# --- 6 summary ----------------------------------------------------------------------

def numbers(rows, scope):
    """results 행과 scope에서 계산한 값만 돌려준다."""
    pairs = [r for r in rows if r["en_title"]]
    chars = lambda key: [r[key] for r in rows if r[key] is not None]
    med = lambda l: (int(statistics.median(l)) if statistics.median(l) % 1 == 0 else statistics.median(l)) if l else None    # 딱 떨어지면 정수로
    n = {"ko_pages": len(rows)}
    for d in (0, 1, 2):
        n[f"depth_{d}"] = sum(1 for r in rows if r["depth"] == d)
    n.update(added=sum(1 for r in rows if r["depth"] is None), excluded=len(scope["excluded"]),
             en_yes=len(pairs), en_no=len(rows) - len(pairs),
             ko_with_table=sum(1 for r in rows if (r["ko_n_tables"] or 0) >= 1), ko_tables=sum(r["ko_n_tables"] or 0 for r in rows),
             en_with_table=sum(1 for r in pairs if (r["en_n_tables"] or 0) >= 1), en_tables=sum(r["en_n_tables"] or 0 for r in pairs),
             ko_median=med(chars("ko_chars")), en_median=med(chars("en_chars")),
             fetch_errors=sum(len(r["errors"]) for r in rows), missing_targets=scope["missing_targets"])
    return n


def load_field(field, out):
    rows, scope = read_json(out / field / "results.json"), read_json(out / field / "scope.json")
    if [r["ko_title"] for r in rows] != [r["ko_title"] for r in scope["included"]]:
        raise SystemExit(f"{field}: results.json과 scope.json의 문서가 다르다(count를 다시 한다)")
    return rows, scope


LABELS = [("ko_pages", "범위 안 한국어 문서"), ("depth_0", "깊이 0"), ("depth_1", "깊이 1"), ("depth_2", "깊이 2"),
          ("added", "더한 문서(깊이 null)"), ("excluded", "뺀 문서"), ("en_yes", "영어 짝 있음"), ("en_no", "영어 짝 없음"),
          ("ko_with_table", "표가 1개 이상인 한국어 문서"), ("ko_tables", "한국어 표 수 합"),
          ("en_with_table", "표가 1개 이상인 영어 짝"), ("en_tables", "영어 표 수 합"),
          ("ko_median", "한국어 본문 길이 중앙값"), ("en_median", "영어 짝 본문 길이 중앙값"), ("fetch_errors", "받기 오류")]


def render_summary(nums):
    L = ["# 분야 문서 보기 (1 문서 보기)", "",
         "규칙: decisions/stage2.md 2026-10-21 \"1 문서 보기의 범위\" 줄. 숫자는 results.json과 scope.json에서 계산했다. 한쪽 언어에만 있는 숫자는 세지 않는다.", ""]
    for field, n in nums.items():
        L += [f"## {FIELDS[field]['ko_name']} ({field})", "", "| 항목 | 값 |", "|---|---|"]
        L += [f"| {name} | {'없음' if n[k] is None else format(n[k], ',')} |" for k, name in LABELS]
        L += ["", "시험 대상 10개 가운데 범위 밖: " + (", ".join(n["missing_targets"]) if n["missing_targets"] else "없음"), ""]
    return "\n".join(L)


def render_docs(field, rows):
    L = [f"# {FIELDS[field]['ko_name']} ({field}) 문서 목록", "",
         "| 제목 | 깊이 | 들어온 분류 | 영어 짝 | 한국어 길이 | 한국어 표 수 | 영어 길이 | 영어 표 수 | 한국어 표 head |", "|---|---|---|---|---|---|---|---|---|"]
    cell = lambda v: "" if v is None else format(v, ",")
    for r in sorted(rows, key=lambda r: (r["depth"] is None, r["depth"] or 0, r["ko_title"])):
        heads = "; ".join(t["head"] for t in r["ko_tables"] or []).replace("|", "\\|")
        L.append(f"| {r['ko_title']} | {'더함' if r['depth'] is None else r['depth']} | {r['via'][0]} | {r['en_title'] or '없음'} | "
                 f"{cell(r['ko_chars'])} | {cell(r['ko_n_tables'])} | {cell(r['en_chars'])} | {cell(r['en_n_tables'])} | {heads} |")
    return "\n".join(L) + "\n"


def compute_all(out):
    loaded = {f: load_field(f, out) for f in FIELDS}
    return {f: numbers(*loaded[f]) for f in FIELDS}, {f: render_docs(f, loaded[f][0]) for f in FIELDS}


def cmd_summary(out=ROUND5):
    nums, docs = compute_all(out)
    write_json(out / "summary_numbers.json", nums)
    (out / "summary.md").write_text(render_summary(nums), encoding="utf-8")
    for f, text in docs.items():
        (out / f / "docs.md").write_text(text, encoding="utf-8")
    print(render_summary(nums))


def cmd_verify(out=ROUND5):
    """results.json·scope.json에서 다시 계산한 값이 저장된 summary_numbers.json, summary.md, docs.md와 같은지 본다."""
    nums, docs = compute_all(out)
    bad = []
    if read_json(out / "summary_numbers.json") != json.loads(json.dumps(nums)):
        bad.append("summary_numbers.json")
    if (out / "summary.md").read_text(encoding="utf-8") != render_summary(nums):
        bad.append("summary.md")
    bad += [f"{f}/docs.md" for f, text in docs.items() if (out / f / "docs.md").read_text(encoding="utf-8") != text]
    print("불일치: " + ", ".join(bad) if bad else "일치")
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    per_field = {"tree": cmd_tree, "scope": cmd_scope, "langlinks": cmd_langlinks, "fetch": cmd_fetch, "count": cmd_count}
    if cmd in per_field:
        fields = sys.argv[2:] or list(FIELDS)
        if [f for f in fields if f not in FIELDS]:
            raise SystemExit(f"분야는 {list(FIELDS)} 가운데 하나다")
        for f in fields:
            per_field[cmd](f)
    elif cmd == "summary":
        cmd_summary()
    elif cmd == "verify":
        sys.exit(0 if cmd_verify() else 1)
    else:
        raise SystemExit(__doc__)
