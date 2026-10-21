"""고친 세는 규칙(quantities.py)이 얼마나 틀리는지 재는 표본 읽기(decisions/stage2.md 2026-10-21 "세는 규칙 보완: 표본 읽기의 크기와 잴 문서" 줄 ㉠~㉤).

  .venv/bin/python src/domain_select/count_rule_check.py select   새 시험 묶음(분야마다 5개 주제)을 골라 heldout.json을 쓴다(네트워크 없음)
  .venv/bin/python src/domain_select/count_rule_check.py count    두 묶음의 문서에 규칙을 돌려 results.json, summary.md, md/를 쓴다
  .venv/bin/python src/domain_select/count_rule_check.py sample   표본을 뽑아 sample.json, sheet.md, verdicts.json(빈칸)을 쓴다
  .venv/bin/python src/domain_select/count_rule_check.py rates    AI가 채운 verdicts.json으로 틀린 비율을 rates.md에 쓴다

묶음 A: 지난번 코퍼스(round4_corpus_check의 대상 문서 + 함께 넣은 문서, 분야 넷, 분야마다 30개).
묶음 B: 새 시험 묶음(heldout.json의 분야 둘, 주제마다 한·영 문서, 분야마다 10개).
판정은 묶음 안, 분야 안에서 한다: 한 언어 문서들의 양을 group()으로 묶고, 반대 언어 문서들과 judge()로 견준다.
표 안 여부는 round4_corpus_check.doc_markdown의 표시(U+E000)가 든 줄에서 읽힌 항목인가로 가린다.

새 시험 묶음에서 빼는 주제(한국어 제목으로 맞춘다. 한 주제가 여럿에 걸리면 아래 차례의 첫 까닭으로 센다):
  1 새 코퍼스의 주제(분야마다 15개)  2 지난번 코퍼스의 주제  3 수식이 든 문서(한국어나 영어 HTML에 mwe-math-element)
남은 후보를 한국어 제목의 sorted로 늘어놓고 make_short_test.shuffled(씨앗 SEED)로 섞어 앞에서부터 5개를 고른다.

표본 뽑기: 모은 목록은 (묶음, 분야, 그룹 id)로 정렬하고, random.Random(SEED) 하나로 SAMPLE_ORDER의 차례대로 뽑는다.
"""
import gzip
import json
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stepper_check as sc  # noqa: E402
import round4_corpus_check as rc  # noqa: E402
import quantities as q  # noqa: E402
from make_short_test import SEED, shuffled  # noqa: E402

ROOT = sc.ROOT
BASE = ROOT / "research_notes" / "stage2_stem_select"
ROUND5 = BASE / "round5"
OUT = BASE / "count_rule_check"
HELDOUT_DOMAINS = ("exoplanets", "rare_earth")
N_PICK = 5
FULL_MAX_CHARS = 20000      # 끝까지 읽는 문서는 plain이 이 글자 수 이하인 것 가운데서 뽑는다(AI가 끝까지 읽을 수 있는 길이)
CTX = 150                   # 언급 앞뒤로 보이는 글자 수
CTX_SMALL = 80
NEAR = 0.10                 # (가) 기준 값이 이 비율 안인 반대 언어 묶음
LIMIT_NEAR = 5
LIMIT_DIGITS = 5

# 새 코퍼스의 주제 가운데 시험 대상 10개 밖의 5개(decisions/stage2.md "2 규칙 정하기 ②", "③")
NEW_CORPUS_EXTRA = {
    "exoplanets": ["지구 유사도 지수", "HD 20367 b", "토끼자리 제타", "TOI-2109b", "KOI-4878.01"],
    "rare_earth": ["터븀 동위 원소", "네오디뮴 동위 원소", "중성자 포획 치료", "사마륨-코발트 자석", "이트륨 동위 원소"],
}

ONLY = "그 언어에만"
SAME = "있음"
MAYBE = "있을 수 있음"
TRUTH_ONLY = ("그 언어에만", "반대 언어에 있음", "세는 범위의 수가 아님")
TRUTH_PRESENT = ("같은 사실이 반대 언어에 있음", "반대 언어에 없음", "세는 범위의 수가 아님")

# 표본의 수: (그 언어에만 A, B), (있음·있을 수 있음 A, B), 끝까지 읽는 문서 (A, B)
N_ONLY = {"A": 25, "B": 25}
N_PRESENT = {"A": 13, "B": 12}
N_DOC = {"A": 1, "B": 1}
SAMPLE_ORDER = ("ko A 그 언어에만", "ko B 그 언어에만", "ko A 있음 쪽", "ko B 있음 쪽",
                "en A 그 언어에만", "en B 그 언어에만", "en A 있음 쪽", "en B 있음 쪽",
                "ko 문서 A", "ko 문서 B", "en 문서 A", "en 문서 B")


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


# --- select -----------------------------------------------------------------------------

def pick_heldout(cands, new_corpus, prev_corpus, has_math, n=N_PICK):
    """후보(ko_title이 있는 줄)에서 세 규칙으로 주제를 빼고 섞은 차례에서 앞 n개를 고른다.
    돌려주는 값: (고른 줄, 빠진 수 {까닭: 수}, 건너뛴 주제 [{ko_title, reason}]).
    건너뛰는 일은 빼기를 먼저 하므로 지금은 생기지 않는다(섞은 차례의 앞 n개를 그대로 쓴다)."""
    dropped = {"새 코퍼스의 주제": 0, "지난번 코퍼스의 주제": 0, "수식이 든 문서": 0}
    kept = []
    for c in cands:
        t = c["ko_title"]
        if t in new_corpus:
            dropped["새 코퍼스의 주제"] += 1
        elif t in prev_corpus:
            dropped["지난번 코퍼스의 주제"] += 1
        elif t in has_math:
            dropped["수식이 든 문서"] += 1
        else:
            kept.append(c)
    order = shuffled(sorted(kept, key=lambda c: c["ko_title"]))
    return order[:n], dropped, []


def r5_html(dom, lang, revid):
    return gzip.open(ROUND5 / dom / "cache" / f"{lang}_{revid}.html.gz", "rt", encoding="utf-8").read()


def cmd_select():
    targets = sc.load_targets()
    heldout = {"seed": SEED, "rule": __doc__.split("새 시험 묶음에서 빼는 주제")[1].split("표본 뽑기")[0].strip(), "domains": {}}
    for dom in HELDOUT_DOMAINS:
        rows = read_json(ROUND5 / dom / "results.json")
        cands = [r for r in rows if r.get("en_title")]
        titles = {c["ko_title"] for c in cands}
        target_titles = {t["ko_title"] for t in targets if t["domain"] == dom}
        new_corpus = target_titles | set(NEW_CORPUS_EXTRA[dom])
        missing = sorted(t for t in new_corpus if t not in titles)
        if len(new_corpus) != 15 or missing:
            raise SystemExit(f"{dom}: 새 코퍼스의 주제 {len(new_corpus)}개, 후보에 없는 것 {missing}")
        added = read_json(rc.ROUND4 / dom / "added.json")
        prev_corpus = target_titles | {s["ko_title"] for s in added["selected"]}
        has_math = set()
        for c in cands:
            if any("mwe-math-element" in r5_html(dom, lang, c[f"{lang}_revid"]) for lang in ("ko", "en")):
                has_math.add(c["ko_title"])
        picked, dropped, skipped = pick_heldout(cands, new_corpus, prev_corpus, has_math)
        heldout["domains"][dom] = {
            "candidates": len(cands), "dropped": dropped, "skipped": skipped,
            "picked": [{"ko_title": c["ko_title"], "en_title": c["en_title"], "ko_revid": c["ko_revid"], "en_revid": c["en_revid"]}
                       for c in picked]}
        print(dom, f"후보 {len(cands)}", "빠짐", dropped, "고른 것", [c["ko_title"] for c in picked], "건너뜀", skipped)
        if len(picked) < N_PICK:
            raise SystemExit(f"{dom}: 고른 주제가 {len(picked)}개뿐이다")
    write_json(OUT / "heldout.json", heldout)


# --- count ------------------------------------------------------------------------------

def docs_a(dom):
    docs = []
    for i, d in enumerate(rc.target_docs(dom) + rc.added_docs(dom)):
        docs.append({"id": i, "lang": d["lang"], "title": d["title"], "revid": d["revid"],
                     "html": d["html"].read_text(encoding="utf-8")})
    return docs


def docs_b(dom, heldout):
    docs = []
    for lang in ("ko", "en"):
        for p in heldout["domains"][dom]["picked"]:
            docs.append({"id": len(docs), "lang": lang, "title": p[f"{lang}_title"], "revid": p[f"{lang}_revid"],
                         "html": r5_html(dom, lang, p[f"{lang}_revid"])})
    return docs


def md_name(bundle, dom, d):
    return f"{bundle}_{dom}_{d['lang']}_{d['revid']}.md"


def analyze(docs):
    """docs: [{id, lang, title, revid, plain, tagged}]. 문서마다 plain을 read()로 읽고, 언어마다 양을 group()으로 묶어
    반대 언어 문서들과 judge()한다. 돌려주는 값: {docs: [...], groups: {lang: [...]}}"""
    for d in docs:
        d["items"] = q.read(d["plain"])
        plain_lines, tagged_lines = d["plain"].split("\n"), d["tagged"].split("\n")
        if len(plain_lines) != len(tagged_lines):
            raise SystemExit(f"{d['title']}: 줄 수가 다르다(표시 없음 {len(plain_lines)}, 표시 있음 {len(tagged_lines)})")
        for it in d["items"]:
            it["in_table"] = rc.SENT in tagged_lines[it["line"]]
    out = {"docs": [{"id": d["id"], "lang": d["lang"], "title": d["title"], "revid": d["revid"], "chars": len(d["plain"])}
                    for d in docs],
           "groups": {}}
    by_id = {d["id"]: d for d in docs}
    for lang, other in (("ko", "en"), ("en", "ko")):
        mine = [{**it, "doc": d["id"]} for d in docs if d["lang"] == lang for it in d["items"] if it["kind"] == "양"]
        groups = q.judge(q.group(mine), [(d["id"], d["items"]) for d in docs if d["lang"] == other])
        res = []
        for k, g in enumerate(groups):
            res.append({"id": f"{lang}{k}", "lang": lang, "dim": g["dim"], "base": g["base"], "verdict": g["verdict"],
                        "found": locate_found(g, by_id), "in_table": any(m["in_table"] for m in g["mentions"]),
                        "mentions": [{"doc": m["doc"], "raw": m["raw"], "line": m["line"], "start": m["start"], "end": m["end"],
                                      "how": m["how"], "digits": m["digits"], "in_table": m["in_table"]} for m in g["mentions"]]})
        out["groups"][lang] = res
    return out


def locate_found(g, by_id):
    """judge가 돌려준 found에 그 자리(start, end, line)를 더한다. judge와 같은 조건의 첫 항목이다."""
    f = g["found"]
    if not f:
        return None
    items = by_id[f["doc"]]["items"]
    if g["verdict"] == SAME:
        hit = next(i for i in items if i["kind"] == "양" and i["dim"] == g["dim"] and q.close(g["base"], i["base"]) and i["raw"] == f["raw"])
    else:
        hit = next(i for i in items if i["kind"] == "모르는 숫자" and i["digits"] == f["digits"])
    return {**f, "start": hit["start"], "end": hit["end"], "line": hit["line"]}


def load_bundles():
    heldout = read_json(OUT / "heldout.json")
    out = []
    for dom in rc.DOMAINS:
        out.append(("A", dom, docs_a(dom)))
    for dom in HELDOUT_DOMAINS:
        out.append(("B", dom, docs_b(dom, heldout)))
    return out


def cmd_count():
    res = {"bundles": {"A": {}, "B": {}}}
    (OUT / "md").mkdir(parents=True, exist_ok=True)
    for bundle, dom, docs in load_bundles():
        for d in docs:
            d["plain"], d["tagged"], same, _ = rc.doc_markdown(d["title"], d.pop("html"))
            (OUT / "md" / md_name(bundle, dom, d)).write_text(d["plain"], encoding="utf-8")
        res["bundles"][bundle][dom] = analyze(docs)
        print(bundle, dom, {lang: len(g) for lang, g in res["bundles"][bundle][dom]["groups"].items()})
    write_json(OUT / "results.json", res)
    cmd_summary(res)


def counts(groups):
    c = {"n": len(groups), SAME: 0, MAYBE: 0, ONLY: 0, "only_table": 0}
    for g in groups:
        c[g["verdict"]] += 1
        c["only_table"] += g["verdict"] == ONLY and g["in_table"]
    return c


def old_counts(dom, lang):
    """옛 규칙으로 센 수(round4/<분야>/results.json): 그 언어에만, 그 가운데 표 안."""
    only = [g for g in read_json(rc.ROUND4 / dom / "results.json")["groups"][lang] if g["verdict"] == ONLY]
    return len(only), sum(1 for g in only if g["in_table"])


def render_summary(res):
    L = ["# 세는 규칙 보완: 표본 읽기 전의 규칙 결과 (count)", "",
         "규칙: decisions/stage2.md 2026-10-21 \"세는 규칙 보완: 표본 읽기의 크기와 잴 문서\" 줄 ㉡. 숫자는 results.json에서 계산했다. "
         "묶음 수는 언어 안에서 같은 차원, 1% 안의 값을 하나로 센 수다. 표 안은 \"그 언어에만\" 묶음 가운데 언급 하나라도 표 안인 것이다.", ""]
    for bundle, name in (("A", "묶음 A: 지난번 코퍼스"), ("B", "묶음 B: 새 시험 묶음")):
        head = "| 분야 | 언어 | 묶음 수 | 있음 | 있을 수 있음 | 그 언어에만 | 그 가운데 표 안 |"
        sep = "|---|---|---|---|---|---|---|"
        if bundle == "A":
            head += " 옛 규칙: 그 언어에만 | 옛 규칙: 그 가운데 표 안 |"
            sep += "---|---|"
        L += [f"## {name}", "", head, sep]
        for dom, r in res["bundles"][bundle].items():
            for lang in ("ko", "en"):
                c = counts(r["groups"][lang])
                row = f"| {dom} | {lang} | {c['n']} | {c[SAME]} | {c[MAYBE]} | {c[ONLY]} | {c['only_table']} |"
                if bundle == "A":
                    row += " %d | %d |" % old_counts(dom, lang)
                L.append(row)
        L.append("")
    return "\n".join(L)


def cmd_summary(res=None):
    res = res or read_json(OUT / "results.json")
    text = render_summary(res)
    (OUT / "summary.md").write_text(text, encoding="utf-8")
    print(text)


# --- sample -----------------------------------------------------------------------------

def pools_for(res):
    """뽑을 목록. 키: (언어, 묶음, 'only' | 'present'), 값: (묶음, 분야, 그룹 id)로 정렬한 그룹 목록."""
    pools = {}
    for bundle, doms in res["bundles"].items():
        for dom, r in doms.items():
            for lang, groups in r["groups"].items():
                for g in groups:
                    kind = "only" if g["verdict"] == ONLY else "present"
                    pools.setdefault((lang, bundle, kind), []).append((bundle, dom, g["id"]))
    return {k: sorted(v) for k, v in pools.items()}


def draw(res, seed=SEED):
    """SAMPLE_ORDER의 차례대로 random.Random(seed) 하나로 뽑는다. 모자라면 있는 만큼 뽑고 shortage에 적는다.
    돌려주는 값: {groups: [{stratum, bundle, domain, group}], docs: [{bundle, domain, doc}], shortage: [...], pools: {...}}"""
    rng = random.Random(seed)
    pools = pools_for(res)
    out = {"groups": [], "docs": [], "shortage": [], "pools": {}}

    def take(label, items, n):
        k = min(n, len(items))
        if k < n:
            out["shortage"].append(f"{label}: {n}개를 뽑아야 하는데 {len(items)}개뿐이라 {k}개를 뽑았다")
        out["pools"][label] = len(items)
        return rng.sample(items, k)

    for lang in ("ko", "en"):
        for kind, n in (("only", N_ONLY), ("present", N_PRESENT)):
            for bundle in ("A", "B"):
                label = f"{lang} {bundle} " + ("그 언어에만" if kind == "only" else "있음 쪽")
                for b, dom, gid in take(label, pools.get((lang, bundle, kind), []), n[bundle]):
                    out["groups"].append({"stratum": label, "bundle": b, "domain": dom, "group": gid})
    for lang in ("ko", "en"):      # 끝까지 읽는 문서도 언어마다 묶음마다 뽑는다(결정 줄 ㉢의 "언어마다 … 문서 2개")
        for bundle in ("A", "B"):
            cand = sorted((bundle, dom, d["id"]) for dom, r in res["bundles"][bundle].items() for d in r["docs"]
                          if d["lang"] == lang and d["chars"] <= FULL_MAX_CHARS)
            for b, dom, did in take(f"{lang} 문서 {bundle}", cand, N_DOC[bundle]):
                out["docs"].append({"stratum": f"{lang} 문서 {bundle}", "bundle": b, "domain": dom, "doc": did})
    return out


def find_group(res, bundle, dom, gid):
    return next(g for g in res["bundles"][bundle][dom]["groups"][gid[:2]] if g["id"] == gid)


def plain_of(res, bundle, dom, doc_id):
    d = res["bundles"][bundle][dom]["docs"][doc_id]
    return (OUT / "md" / md_name(bundle, dom, d)).read_text(encoding="utf-8")


def context(text, start, end, n=CTX):
    """언급 자리 앞뒤 n글자(그 줄 안에서만). 언급은 【】로 싼다."""
    ls = text.rfind("\n", 0, start) + 1
    le = text.find("\n", end)
    le = len(text) if le < 0 else le
    a, b = max(ls, start - n), min(le, end + n)
    return ("…" if a > ls else "") + text[a:start] + "【" + text[start:end] + "】" + text[end:b] + ("…" if b < le else "")


def near_groups(res, bundle, dom, g):
    """(가) 반대 언어 묶음 가운데 같은 dim이고 기준 값이 NEAR 안인 것, 가까운 차례로 LIMIT_NEAR개."""
    other = "en" if g["lang"] == "ko" else "ko"
    c = [(abs(o["base"] - g["base"]) / max(abs(o["base"]), abs(g["base"]), 1e-300), o)
         for o in res["bundles"][bundle][dom]["groups"][other] if o["dim"] == g["dim"]]
    c = sorted([x for x in c if x[0] <= NEAR], key=lambda x: (x[0], x[1]["id"]))
    return [o for _, o in c[:LIMIT_NEAR]]


def digit_places(res, bundle, dom, g):
    """(나) 반대 언어 plain에서 언급의 digits 글자가 나오는 자리 LIMIT_DIGITS개. 앞뒤가 숫자인 곳은 뺀다."""
    other = "en" if g["lang"] == "ko" else "ko"
    wanted = []
    for m in g["mentions"]:
        wanted += [x for x in m["digits"] if x not in wanted]
    out = []
    for d in res["bundles"][bundle][dom]["docs"]:
        if d["lang"] != other:
            continue
        text = plain_of(res, bundle, dom, d["id"])
        for w in wanted:
            for m in re.finditer(r"(?<![0-9])" + re.escape(w) + r"(?![0-9])", text):
                out.append((d["title"], w, context(text, m.start(), m.end(), CTX_SMALL)))
                if len(out) >= LIMIT_DIGITS:
                    return out
    return out


def render_group(no, entry, res):
    bundle, dom, g = entry["bundle"], entry["domain"], find_group(res, entry["bundle"], entry["domain"], entry["group"])
    docs = res["bundles"][bundle][dom]["docs"]
    L = [f"### {no} (묶음 {bundle}, {dom}, {g['lang']}, 그룹 {g['id']})", "",
         f"- verdict: {g['verdict']}, dim: {g['dim']}, base: {g['base']:.6g}, 표 안: {'예' if g['in_table'] else '아니오'}", "- 언급:"]
    for m in g["mentions"]:
        d = docs[m["doc"]]
        L.append(f"  - [{d['title']}] raw `{m['raw']}` (줄 {m['line']}, {m['how']}): {context(plain_of(res, bundle, dom, m['doc']), m['start'], m['end'])}")
    f = g["found"]
    if f:
        d = docs[f["doc"]]
        what = f"raw `{f['raw']}`" if g["verdict"] == SAME else f"숫자 글자 `{f['digits']}`"
        L.append(f"- found: [{d['title']}] {what} (줄 {f['line']}): {context(plain_of(res, bundle, dom, f['doc']), f['start'], f['end'])}")
    else:
        near = near_groups(res, bundle, dom, g)
        L.append(f"- (가) 반대 언어의 같은 dim이고 기준 값이 {int(NEAR * 100)}% 안인 양 {len(near)}개(가까운 차례):")
        for o in near:
            m = o["mentions"][0]
            d = docs[m["doc"]]
            L.append(f"  - base {o['base']:.6g}: [{d['title']}] raw `{m['raw']}` (줄 {m['line']}): "
                     f"{context(plain_of(res, bundle, dom, m['doc']), m['start'], m['end'], CTX_SMALL)}")
        places = digit_places(res, bundle, dom, g)
        L.append(f"- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 {len(places)}개:")
        for title, w, c in places:
            L.append(f"  - [{title}] `{w}`: {c}")
    L.append("")
    return L


def render_doc(no, entry, res):
    bundle, dom = entry["bundle"], entry["domain"]
    d = res["bundles"][bundle][dom]["docs"][entry["doc"]]
    text = plain_of(res, bundle, dom, entry["doc"])
    L = [f"### {no} (끝까지 읽는 문서: 묶음 {bundle}, {dom}, {d['lang']}, {d['title']}, {d['chars']}자)", "",
         "줄 번호는 0부터 센다. 규칙이 읽은 양의 목록 뒤에 줄 번호를 붙인 글 전체가 있다.", "", "규칙이 읽은 양(줄, raw, value, unit, dim):", ""]
    for r in entry["rule_list"]:
        L.append(f"- {r['line']} | `{r['raw']}` | {r['value']} | {r['unit']} | {r['dim']}")
    L += ["", "```"] + [f"{i}: {ln}" for i, ln in enumerate(text.split("\n"))] + ["```", ""]
    return L


def cmd_sample():
    res = read_json(OUT / "results.json")
    picked = draw(res)
    entries = []
    for i, e in enumerate(picked["groups"], 1):
        g = find_group(res, e["bundle"], e["domain"], e["group"])
        entries.append({"no": f"S{i:03d}", "type": "only" if g["verdict"] == ONLY else "present", "lang": g["lang"], "verdict": g["verdict"], **e})
    for i, e in enumerate(picked["docs"], 1):
        rule = [{"line": it["line"], "raw": it["raw"], "value": it["value"], "unit": it["unit"], "dim": it["dim"]}
                for it in q.quantities(plain_of(res, e["bundle"], e["domain"], e["doc"]))]
        d = res["bundles"][e["bundle"]][e["domain"]]["docs"][e["doc"]]
        entries.append({"no": f"D{i}", "type": "doc", "lang": d["lang"], "title": d["title"], "rule_list": rule, **e})
    sample = {"seed": SEED, "order": list(SAMPLE_ORDER),
              "order_note": "정렬한 목록(묶음, 분야, 그룹 id)에서 random.Random(seed) 하나로 order의 차례대로 random.sample로 뽑는다. "
                            "수는 그 언어에만 A 25, B 25, 있음 쪽(있음, 있을 수 있음) A 13, B 12(언어마다), 문서 A 1, B 1이다.",
              "doc_condition": f"끝까지 읽는 문서는 plain이 {FULL_MAX_CHARS:,}자 이하인 문서 가운데서 뽑는다(AI가 끝까지 읽을 수 있는 길이로 정했다).",
              "pools": picked["pools"], "shortage": picked["shortage"], "entries": entries}
    write_json(OUT / "sample.json", sample)
    L = ["# 표본 읽기 종이", "",
         "읽는 방법: decisions/stage2.md 2026-10-21 \"세는 규칙 보완: 표본 읽기의 크기와 잴 문서\" 줄 ㉣. 항목마다 verdicts.json에 판정을 적는다.",
         "- \"그 언어에만\": read_ok(값과 단위를 문서대로 읽었는가)와 truth(" + " / ".join(TRUTH_ONLY) + ")",
         "- \"있음\"·\"있을 수 있음\": read_ok와 truth(" + " / ".join(TRUTH_PRESENT) + ")",
         f"- 끝까지 읽는 문서: ai_list(세는 범위의 수: 줄, raw, value, unit). 조건: {sample['doc_condition']}",
         f"- 언급 옆의 글은 그 줄 안에서 앞뒤 {CTX}자이고 언급은 【】로 싼다.", "",
         "표본의 수: " + ", ".join(f"{k} {v}개 중 {sum(1 for e in picked['groups'] + picked['docs'] if e['stratum'] == k)}개 뽑음"
                                 for k, v in picked["pools"].items()),
         *(["모자란 곳: " + "; ".join(picked["shortage"])] if picked["shortage"] else []), ""]
    blank = []
    for e in entries:
        if e["type"] == "doc":
            L += render_doc(e["no"], e, res)
            blank.append({"no": e["no"], "type": "doc", "bundle": e["bundle"], "domain": e["domain"], "lang": e["lang"], "doc": e["doc"],
                          "ai_list": None})
        else:
            L += render_group(e["no"], e, res)
            blank.append({"no": e["no"], "type": e["type"], "bundle": e["bundle"], "domain": e["domain"], "lang": e["lang"],
                          "group": e["group"], "verdict": e["verdict"], "read_ok": None, "truth": None, "note": None})
    (OUT / "sheet.md").write_text("\n".join(L), encoding="utf-8")
    write_json(OUT / "verdicts.json", blank)
    print("표본", len(picked["groups"]), "그룹", len(picked["docs"]), "문서", "모자란 곳", picked["shortage"] or "없음")
    print({k: v for k, v in picked["pools"].items()})


# --- rates ------------------------------------------------------------------------------

def wilson(k, n, z=1.959964):
    """윌슨 95% 구간 (아래, 위). n이 0이면 (None, None)."""
    if n == 0:
        return None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def fmt_rate(k, n):
    if n == 0:
        return "0/0"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {k / n * 100:.1f}% [{lo * 100:.1f}, {hi * 100:.1f}]"


def check_filled(rows):
    """빈칸이 남은 번호를 돌려준다."""
    bad = []
    for r in rows:
        if r["type"] == "doc":
            ok = isinstance(r["ai_list"], list) and all(isinstance(x, dict) and {"line", "raw", "value", "unit"} <= set(x) for x in r["ai_list"])
        else:
            allowed = TRUTH_ONLY if r["type"] == "only" else TRUTH_PRESENT
            ok = isinstance(r["read_ok"], bool) and r["truth"] in allowed and isinstance(r["note"], str)
        if not ok:
            bad.append(r["no"])
    return bad


def compare_doc(rule_list, ai_list):
    """AI 목록과 규칙 목록을 하나씩 짝짓는다(같은 줄, 값이 1% 안, 같은 dim). 돌려주는 값: (맞춘 수, 규칙이 놓친 AI 항목, 규칙이 잘못 읽은 항목)"""
    left = list(rule_list)
    matched, missed = 0, []
    for a in ai_list:
        key = q.norm(str(a["unit"]))
        dim = q.UNITS[key][0] if key in q.UNITS else None
        hit = next((r for r in left if r["line"] == a["line"] and dim is not None and r["dim"] == dim and q.close(r["value"], a["value"])), None)
        if hit:
            left.remove(hit)
            matched += 1
        else:
            missed.append(a)
    return matched, missed, left


def rates_rows(rows):
    """verdicts.json의 줄에서 (언어 또는 합, 묶음 또는 합)마다 센 값을 돌려준다."""
    out = {}
    for lang in ("ko", "en", "합"):
        for bundle in ("A", "B", "합"):
            sel = [r for r in rows if r["type"] != "doc" and lang in (r["lang"], "합") and bundle in (r["bundle"], "합")]
            only = [r for r in sel if r["type"] == "only"]
            present = [r for r in sel if r["type"] == "present"]
            wrong_only = sum(1 for r in only if not r["read_ok"] or r["truth"] != ONLY)
            by_verdict = {v: (sum(1 for r in present if r["verdict"] == v and r["truth"] == "반대 언어에 없음"),
                              sum(1 for r in present if r["verdict"] == v)) for v in (SAME, MAYBE)}
            out[(lang, bundle)] = {"only": (wrong_only, len(only)),
                                   "present": (sum(1 for r in present if r["truth"] == "반대 언어에 없음"), len(present)),
                                   "by_verdict": by_verdict,
                                   "truth_only": {t: sum(1 for r in only if r["truth"] == t) for t in TRUTH_ONLY},
                                   "unread_only": sum(1 for r in only if not r["read_ok"]),
                                   "truth_present": {t: sum(1 for r in present if r["truth"] == t) for t in TRUTH_PRESENT}}
    return out


def render_rates(rows, sample):
    st = rates_rows(rows)
    names = {"ko": "한국어", "en": "영어", "합": "합쳐서"}
    L = ["# 틀린 비율 (rates)", "",
         "숫자는 verdicts.json(AI의 판정)과 sample.json(규칙이 읽은 양의 목록)에서 계산했다. 칸은 `틀린 수/표본 수 = 비율 [윌슨 95% 구간]`이다.", "",
         "## \"그 언어에만\" 표본의 틀린 비율(많이 세는 오차)", "",
         "틀림 = read_ok가 false이거나 truth가 \"그 언어에만\"이 아닌 것.", "",
         "| 언어 | 묶음 A | 묶음 B | 합쳐서 |", "|---|---|---|---|"]
    for lang in ("ko", "en", "합"):
        L.append(f"| {names[lang]} | " + " | ".join(fmt_rate(*st[(lang, b)]["only"]) for b in ("A", "B", "합")) + " |")
    L += ["", "## \"있음\"·\"있을 수 있음\" 표본의 틀린 비율(적게 세는 오차)", "", "틀림 = truth가 \"반대 언어에 없음\"인 것.", "",
          "| 언어 | verdict | 묶음 A | 묶음 B | 합쳐서 |", "|---|---|---|---|---|"]
    for lang in ("ko", "en", "합"):
        L.append(f"| {names[lang]} | 둘 합쳐서 | " + " | ".join(fmt_rate(*st[(lang, b)]["present"]) for b in ("A", "B", "합")) + " |")
        for v in (SAME, MAYBE):
            L.append(f"| {names[lang]} | {v} | " + " | ".join(fmt_rate(*st[(lang, b)]["by_verdict"][v]) for b in ("A", "B", "합")) + " |")
    L += ["", "## 판정의 갈래별 수(위 비율의 바탕)", "", "| 언어 | 묶음 | 표본 | 그 언어에만 truth별 | read_ok가 false | 있음 쪽 truth별 |", "|---|---|---|---|---|---|"]
    for lang in ("ko", "en", "합"):
        for b in ("A", "B", "합"):
            s = st[(lang, b)]
            L.append(f"| {names[lang]} | {b} | 그 언어에만 {s['only'][1]}, 있음 쪽 {s['present'][1]} | "
                     + ", ".join(f"{t} {n}" for t, n in s["truth_only"].items()) + f" | {s['unread_only']} | "
                     + ", ".join(f"{t} {n}" for t, n in s["truth_present"].items()) + " |")
    L += ["", "## 끝까지 읽은 문서", ""]
    rule_by_no = {e["no"]: e["rule_list"] for e in sample["entries"] if e["type"] == "doc"}
    tot = [0, 0, 0, 0]
    for r in rows:
        if r["type"] != "doc":
            continue
        matched, missed, wrong = compare_doc(rule_by_no[r["no"]], r["ai_list"])
        tot = [tot[0] + len(r["ai_list"]), tot[1] + matched, tot[2] + len(missed), tot[3] + len(wrong)]
        L += [f"### {r['no']} (묶음 {r['bundle']}, {r['domain']}, {r['lang']})", "",
              f"- AI 목록 {len(r['ai_list'])}개, 규칙이 읽은 것 {matched}개, 규칙이 놓친 것 {len(missed)}개, 규칙이 읽었지만 AI 목록에 없는 것(잘못 읽음) {len(wrong)}개",
              f"- 규칙이 읽은 수 {len(rule_by_no[r['no']])}개, 규칙이 읽은 것 가운데 AI 목록과 맞은 비율 {fmt_rate(len(rule_by_no[r['no']]) - len(wrong), len(rule_by_no[r['no']]))}",
              f"- AI 목록 가운데 규칙이 읽은 비율 {fmt_rate(matched, len(r['ai_list']))}", "- 규칙이 놓친 것:"]
        L += [f"  - 줄 {a['line']} | `{a['raw']}` | {a['value']} | {a['unit']}" for a in missed] or ["  - 없음"]
        L.append("- 규칙이 읽었지만 AI 목록에 없는 것:")
        L += [f"  - 줄 {a['line']} | `{a['raw']}` | {a['value']} | {a['unit']} | {a['dim']}" for a in wrong] or ["  - 없음"]
        L.append("")
    L += [f"합쳐서: AI 목록 {tot[0]}개 가운데 규칙이 읽은 것 {tot[1]}개, 놓친 것 {tot[2]}개, 잘못 읽은 것 {tot[3]}개", ""]
    return "\n".join(L)


def cmd_rates():
    rows = read_json(OUT / "verdicts.json")
    bad = check_filled(rows)
    if bad:
        raise SystemExit("빈칸이 남았다: " + ", ".join(bad))
    text = render_rates(rows, read_json(OUT / "sample.json"))
    (OUT / "rates.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fns = {"select": cmd_select, "count": cmd_count, "sample": cmd_sample, "rates": cmd_rates}
    if cmd not in fns:
        raise SystemExit(__doc__)
    fns[cmd]()
