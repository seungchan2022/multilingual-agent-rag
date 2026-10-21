"""이슈 #6의 3 세기: 분야마다 정해 둔 문서 20개(코퍼스)에서 한쪽 언어 문서에만 있는 사실(단위가 붙은 수)을 센다
(decisions/stage2.md 2026-10-21 "2 규칙 정하기 ①~⑥", "두 언어 문서가 같은 것을 서로 다른 값으로 적은 사실은 … 세지 않는다",
"3 세기는 … AI가 원문과 대조해 확인한 수로 판정한다" ㉠~㉧,
"3 세기에서 두 언어 주제 쪽의 필요한 수(18)는 통과 판정에서 빼고 …" ㉠~㉥).

  .venv/bin/python src/domain_select/step3_count.py count    코퍼스를 읽어 세고 results.json, summary.md, md/를 쓴다(네트워크 없음)
  .venv/bin/python src/domain_select/step3_count.py sheet    대조할 차례와 읽을 종이를 만든다: confirm.json(AI가 채울 판정 파일의 틀), sheet.md
  .venv/bin/python src/domain_select/step3_count.py status   AI가 채운 confirm.json이 어디까지 왔고 다음에 무엇을 볼지 status.md에 쓴다
  .venv/bin/python src/domain_select/step3_count.py judge    몫을 다 채웠는지(넘음, 탈락)와 어림을 judge.md, judge.json에 쓴다

판정은 프로그램이 센 수로 하지 않는다. 프로그램이 "그 언어에만"으로 센 묶음은 후보일 뿐이고("있을 수 있음"은 있음으로 보아 후보가 아니다),
AI가 후보를 정한 차례로 원문과 대조해 맞은 수로 판정한다(read_ok가 true이고 truth가 "그 언어에만"인 것).
두 언어 쪽은 판정에 쓰지 않는다(위 "두 언어 주제 쪽의 필요한 수(18)는 통과 판정에서 빼고" 줄). 넘음과 여유는 언어마다 한쪽 언어 쪽과 표 넷으로 보고,
두 언어 쪽은 맞은 수, 채운 수, 후보 수만 참고로 적는다.

코퍼스: 분야마다 문서 20개(한국어 10, 영어 10). 갈래는 "두 언어"(한·영 문서 둘 다 있는 주제 5개), "한국어만"(한국어 문서만 5개),
"영어만"(영어 문서만 5개)이다. 들어온 곳: "대상"(앞 단계에서 판을 고정한 문서), "②", "③"(round5 results.json에서 찾은 문서).
②·③은 시험 대상 밖 문서다(outside_target).
쪽: 근거 언어마다 "both"(그 언어의 두 언어 갈래 문서 5개)와 "one"(그 언어의 한쪽 언어 갈래 문서 5개) 둘이다. 사실은 그 사실이 든 문서의
쪽으로 센다(결정 ① ㉣). 그래서 묶기(group)는 (분야, 언어, 쪽)마다 따로 하고, 판정(judge)은 그 분야 코퍼스의 반대 언어 문서 10개 전부와 견준다.
차례(분야·언어마다 넷): both(두 언어 쪽 후보), one(한쪽 언어 쪽 후보), table(두 쪽의 후보 가운데 표 안), model(두 쪽의 후보 가운데
outside_target). 각 목록은 (첫 언급의 문서 title, line, start)로 정렬한 뒤 make_short_test.shuffled로 섞는다. 차례의 "자리"는 1부터 센다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import round4_corpus_check as rc  # noqa: E402
import count_rule_check as cc  # noqa: E402
import quantities as q  # noqa: E402
from make_short_test import shuffled  # noqa: E402

BASE = cc.BASE
OUT = BASE / "step3"
FIELDS = ("exoplanets", "rare_earth")
LANGS = ("ko", "en")
SIDES = ("both", "one")
SIDE_NAME = {"both": "두 언어 쪽", "one": "한쪽 언어 쪽"}
BOTH, KO_ONLY, EN_ONLY = "두 언어", "한국어만", "영어만"
ONLY, SAME, MAYBE, TRUTH_ONLY = cc.ONLY, cc.SAME, cc.MAYBE, cc.TRUTH_ONLY
CTX, CTX_SMALL, NEAR, LIMIT_NEAR, LIMIT_DIGITS = cc.CTX, cc.CTX_SMALL, cc.NEAR, cc.LIMIT_NEAR, cc.LIMIT_DIGITS
NEED = {"side": 18, "table": 3, "model": 5}      # 쪽마다, 표, 모델 시험 값(결정 ④ ⑥)
NEXT_MAX = 10

# 갈래, 들어온 곳, 주제(한국어 제목). 분야마다 갈래 쪽 주제는 5개다(두 언어는 한·영 문서 둘, 한쪽 언어는 그 언어 문서 하나).
CORPUS = {
    "exoplanets": [
        (BOTH, "대상", ["케플러-16b", "COROT-7b", "목동자리 타우 b", "글리제 1214 b"]), (BOTH, "③", ["KOI-4878.01"]),
        (KO_ONLY, "대상", ["글리제 581 c", "글리제 436 b", "센타우루스자리 프록시마 b"]), (KO_ONLY, "②", ["지구 유사도 지수", "HD 20367 b"]),
        (EN_ONLY, "대상", ["KELT-9b", "로스 128 b", "케플러-22b"]), (EN_ONLY, "②", ["토끼자리 제타", "TOI-2109b"])],
    "rare_earth": [
        (BOTH, "대상", ["툴륨", "디스프로슘", "이터븀", "루테튬"]), (BOTH, "③", ["이트륨 동위 원소"]),
        (KO_ONLY, "대상", ["어븀", "사마륨", "이트륨"]), (KO_ONLY, "②", ["터븀 동위 원소", "네오디뮴 동위 원소"]),
        (EN_ONLY, "대상", ["란타넘", "유로퓸", "프라세오디뮴"]), (EN_ONLY, "②", ["중성자 포획 치료", "사마륨-코발트 자석"])],
}


def side_of(doc):
    return "both" if doc["branch"] == BOTH else "one"


# --- 코퍼스 -----------------------------------------------------------------------------

def corpus_rows(field):
    """CORPUS 표대로 문서 20개의 줄을 모은다(html은 아직 읽지 않는다). 주제를 못 찾거나 20개(한국어 10, 영어 10)가 아니면 멈춘다.
    [{field, lang, topic, title, revid, branch, entered, outside_target, html: 읽을 곳}]"""
    targets = {(r["target"], r["lang"]): r for r in rc.target_docs(field)}
    r5 = {r["ko_title"]: r for r in cc.read_json(cc.ROUND5 / field / "results.json")}
    rows, missing = [], []
    for branch, entered, topics in CORPUS[field]:
        langs = LANGS if branch == BOTH else (("ko",) if branch == KO_ONLY else ("en",))
        for topic in topics:
            for lang in langs:
                if entered == "대상":
                    t = targets.get((topic, lang))
                    if not t:
                        missing.append(f"{topic}({lang}, 대상)")
                        continue
                    title, revid, html = t["title"], t["revid"], t["html"]
                else:
                    r = r5.get(topic)
                    if not r or not r.get(f"{lang}_revid") or not r.get(f"{lang}_title"):
                        missing.append(f"{topic}({lang}, {entered})")
                        continue
                    title, revid, html = r[f"{lang}_title"], r[f"{lang}_revid"], None
                rows.append({"field": field, "lang": lang, "topic": topic, "title": title, "revid": revid, "branch": branch,
                             "entered": entered, "outside_target": entered != "대상", "html": html})
    if missing:
        raise SystemExit(f"{field}: 찾지 못한 주제 {missing}")
    n = {lang: sum(1 for r in rows if r["lang"] == lang) for lang in LANGS}
    if len(rows) != 20 or n != {"ko": 10, "en": 10}:
        raise SystemExit(f"{field}: 문서가 {len(rows)}개(한국어 {n['ko']}, 영어 {n['en']})다. 20개(10, 10)여야 한다")
    for i, r in enumerate(rows):
        r["id"] = i
    pair = {(r["topic"], r["lang"]): r["id"] for r in rows if r["branch"] == BOTH}
    for r in rows:
        r["pair"] = pair[(r["topic"], "en" if r["lang"] == "ko" else "ko")] if r["branch"] == BOTH else None
    return rows


def read_html(row):
    if row["html"] is not None:
        return row["html"].read_text(encoding="utf-8")
    return cc.r5_html(row["field"], row["lang"], row["revid"])


def md_path(field, lang, revid):
    return OUT / "md" / f"{field}_{lang}_{revid}.md"


# --- 세기 -------------------------------------------------------------------------------

def analyze(docs):
    """docs: [{id, lang, title, branch, outside_target, plain, tagged}]. 문서마다 plain을 read()로 읽고(표 안 표시는 tagged 줄에서),
    (언어, 쪽)마다 양을 group()으로 묶어 그 분야의 반대 언어 문서 전부와 judge()한다.
    돌려주는 값: {lang: {side: [묶음]}}. 묶음: {id, lang, side, dim, base, verdict, found, in_table, outside_target, mentions}"""
    for d in docs:
        d["items"] = q.read(d["plain"])
        plain_lines, tagged_lines = d["plain"].split("\n"), d["tagged"].split("\n")
        if len(plain_lines) != len(tagged_lines):
            raise SystemExit(f"{d['title']}: 줄 수가 다르다(표시 없음 {len(plain_lines)}, 표시 있음 {len(tagged_lines)})")
        for it in d["items"]:
            it["in_table"] = rc.SENT in tagged_lines[it["line"]]
    by_id = {d["id"]: d for d in docs}
    out = {}
    for lang, other in (("ko", "en"), ("en", "ko")):
        others = [(d["id"], d["items"]) for d in docs if d["lang"] == other]
        out[lang] = {}
        for side in SIDES:
            mine = [{**it, "doc": d["id"]} for d in docs if d["lang"] == lang and side_of(d) == side
                    for it in d["items"] if it["kind"] == "양"]
            res = []
            for k, g in enumerate(q.judge(q.group(mine), others)):
                res.append({"id": f"{lang}-{side}-{k:03d}", "lang": lang, "side": side, "dim": g["dim"], "base": g["base"],
                            "verdict": g["verdict"], "found": cc.locate_found(g, by_id),
                            "in_table": any(m["in_table"] for m in g["mentions"]),
                            "outside_target": any(by_id[m["doc"]]["outside_target"] for m in g["mentions"]),
                            "mentions": [{"doc": m["doc"], "raw": m["raw"], "line": m["line"], "start": m["start"], "end": m["end"],
                                          "how": m["how"], "digits": m["digits"], "in_table": m["in_table"]} for m in g["mentions"]]})
            out[lang][side] = res
    return out


def count_field(field):
    rows = corpus_rows(field)
    docs = []
    for r in rows:
        plain, tagged, same, _ = rc.doc_markdown(r["title"], read_html(r))
        md_path(field, r["lang"], r["revid"]).parent.mkdir(parents=True, exist_ok=True)
        md_path(field, r["lang"], r["revid"]).write_text(plain, encoding="utf-8")
        docs.append({**r, "plain": plain, "tagged": tagged})
    groups = analyze(docs)
    meta = [{"id": d["id"], "field": field, "lang": d["lang"], "topic": d["topic"], "title": d["title"], "revid": d["revid"],
             "branch": d["branch"], "entered": d["entered"], "outside_target": d["outside_target"], "pair": d["pair"],
             "chars": len(d["plain"])} for d in docs]
    return {"docs": meta, "groups": groups}


def counts(groups):
    c = {"n": len(groups), SAME: 0, MAYBE: 0, ONLY: 0, "only_table": 0}
    for g in groups:
        c[g["verdict"]] += 1
        c["only_table"] += g["verdict"] == ONLY and g["in_table"]
    return c


def render_summary(res):
    L = ["# 3 세기: 세는 규칙의 결과 (count)", "",
         "숫자는 results.json에서 계산했다. 묶음 수는 (분야, 언어, 쪽) 안에서 같은 차원, 1% 안의 값을 하나로 센 수다. "
         "\"그 언어에만\"이 후보이고 \"있을 수 있음\"은 있음으로 본다. 표 안은 후보 가운데 언급 하나라도 표 안인 것이다. "
         "필요한 수는 AI가 대조해 맞은 수로 채울 몫이라 후보 수가 이보다 적으면 그 몫은 못 채운다.", "",
         "| 분야 | 언어 | 쪽 | 묶음 수 | 있음 | 있을 수 있음 | 그 언어에만(후보) | 그 가운데 표 안 | 필요한 수 |", "|---|---|---|---|---|---|---|---|---|"]
    for field in FIELDS:
        for lang in LANGS:
            tot = {"n": 0, SAME: 0, MAYBE: 0, ONLY: 0, "only_table": 0}
            for side in SIDES:
                c = counts(res["fields"][field]["groups"][lang][side])
                tot = {k: tot[k] + c[k] for k in tot}
                L.append(f"| {field} | {lang} | {SIDE_NAME[side]} | {c['n']} | {c[SAME]} | {c[MAYBE]} | {c[ONLY]} | {c['only_table']} | {NEED['side']} |")
            L.append(f"| {field} | {lang} | 두 쪽 합 | {tot['n']} | {tot[SAME]} | {tot[MAYBE]} | {tot[ONLY]} | {tot['only_table']} | "
                     f"표 {NEED['table']} |")
    L.append("")
    return "\n".join(L)


def cmd_count():
    res = {"fields": {}}
    for field in FIELDS:
        res["fields"][field] = count_field(field)
        print(field, {lang: {s: len(g) for s, g in sides.items()} for lang, sides in res["fields"][field]["groups"].items()})
    cc.write_json(OUT / "results.json", res)
    text = render_summary(res)
    (OUT / "summary.md").write_text(text, encoding="utf-8")
    print(text)


# --- sheet ------------------------------------------------------------------------------

def make_orders(groups, titles):
    """한 분야·한 언어의 groups({side: [묶음]})에서 후보로 네 차례를 만든다. titles: {문서 id: title}.
    각 목록은 (첫 언급의 문서 title, line, start)로 정렬한 뒤 shuffled로 섞는다. 돌려주는 값: {both, one, table, model: [묶음]}"""
    def key(g):
        m = g["mentions"][0]
        return (titles[m["doc"]], m["line"], m["start"], g["id"])

    cand = {s: [g for g in groups[s] if g["verdict"] == ONLY] for s in SIDES}
    both = cand["both"] + cand["one"]
    return {"both": shuffled(sorted(cand["both"], key=key)), "one": shuffled(sorted(cand["one"], key=key)),
            "table": shuffled(sorted([g for g in both if g["in_table"]], key=key)),
            "model": shuffled(sorted([g for g in both if g["outside_target"]], key=key))}


def make_confirm(field, lang, orders):
    """번호는 (두 언어 쪽 차례, 한쪽 언어 쪽 차례) 순서로 매긴다. 돌려주는 값: confirm.json의 항목 목록"""
    entries = {}
    for side in SIDES:
        for g in orders[side]:
            entries[g["id"]] = {"no": f"{field[0].upper()}-{lang}-{len(entries) + 1:03d}", "field": field, "lang": lang, "side": side,
                                "group": g["id"], "in_table": g["in_table"], "outside_target": g["outside_target"],
                                "order_side": orders[side].index(g) + 1, "order_table": None, "order_model": None,
                                "read_ok": None, "truth": None, "note": None}
    for name in ("table", "model"):
        for i, g in enumerate(orders[name], 1):
            entries[g["id"]][f"order_{name}"] = i
    return list(entries.values())


CRITERIA = """## 판정 기준 (이 종이를 읽는 AI가 지킨다)

- read_ok: 값과 단위를 문서대로 읽었는가(true/false).
- truth(셋 가운데 하나): "그 언어에만" = 코퍼스 안의 반대 언어 문서에 같은 값도, 같은 대상의 같은 양이 다른 값으로 적힌 것(서로 어긋남)도 없다.
  "반대 언어에 있음" = 둘 가운데 하나가 있다. "세는 범위의 수가 아님" = 연도·이름·오차 폭 등.
- 같은 값: ±1% 안이거나, 더 정밀한 값을 덜 정밀한 값의 마지막 자리로 반올림해 같은 것(괄호 안의 환산과 낱말 숫자도 견준다. 정수 끝의 0은 유효 자릿수로 보지 않는다).
- 묶음에 언급이 여럿이면, 바르게 읽은 "그 언어에만"인 사실이 하나라도 있으면 그 묶음은 맞은 것(read_ok true, truth "그 언어에만")이다.
- 견주는 문서는 코퍼스 안의 반대 언어 문서뿐이다.
- 판정은 차례의 앞에서부터 빈틈없이 채운다. 그 쪽 차례로 맞은 것이 18개가 되면 그 쪽은 멈춘다(`status`가 알려 준다). 두 언어 쪽은 2026-10-21 "3 세기에서 두 언어 주제 쪽의 필요한 수(18)는 통과 판정에서 빼고" 결정으로 더 대조하지 않는다.
- 칸은 confirm.json에 채운다: read_ok(true/false), truth, note(글).
"""


def context_of(text, m, n=CTX):
    return cc.context(text, m["start"], m["end"], n)


def near_groups(res_field, lang, g):
    """(가) 반대 언어 묶음(두 쪽 모두) 가운데 같은 dim이고 기준 값이 NEAR 안인 것, 가까운 차례로 LIMIT_NEAR개.
    두 쪽에 같은 값이 따로 있으면 하나로 본다(서로 close인 것은 앞의 것만)."""
    other = "en" if lang == "ko" else "ko"
    c = [(abs(o["base"] - g["base"]) / max(abs(o["base"]), abs(g["base"]), 1e-300), o)
         for s in SIDES for o in res_field["groups"][other][s] if o["dim"] == g["dim"]]
    out = []
    for diff, o in sorted([x for x in c if x[0] <= NEAR], key=lambda x: (x[0], x[1]["id"])):
        if not any(p["dim"] == o["dim"] and q.close(p["base"], o["base"]) for p in out):
            out.append(o)
    return out[:LIMIT_NEAR]


def digit_places(field, res_field, texts, lang, g):
    """(나) 반대 언어 문서에서 언급의 digits 글자가 나오는 자리 LIMIT_DIGITS개. 앞뒤가 숫자인 곳은 뺀다."""
    wanted = []
    for m in g["mentions"]:
        wanted += [x for x in m["digits"] if x not in wanted]
    out = []
    for d in res_field["docs"]:
        if d["lang"] == lang:
            continue
        text = texts[d["id"]]
        for w in wanted:
            for m in re.finditer(r"(?<![0-9])" + re.escape(w) + r"(?![0-9])", text):
                out.append((d["title"], w, cc.context(text, m.start(), m.end(), CTX_SMALL)))
                if len(out) >= LIMIT_DIGITS:
                    return out
    return out


def render_candidate(entry, g, res_field, texts):
    docs = {d["id"]: d for d in res_field["docs"]}
    lang = entry["lang"]
    L = [f"### {entry['no']}", "",
         f"- 분야 {entry['field']}, 언어 {lang}, 쪽 {SIDE_NAME[g['side']]}, dim {g['dim']}, base {g['base']:.6g}, "
         f"표 안 {'예' if g['in_table'] else '아니오'}, 시험 대상 밖 {'예' if g['outside_target'] else '아니오'}", "- 언급:"]
    for m in g["mentions"]:
        d = docs[m["doc"]]
        pair = f" (같은 주제의 반대 언어 문서: {docs[d['pair']]['title']})" if d["pair"] is not None else ""
        L.append(f"  - [{d['title']}]{pair} raw `{m['raw']}` (줄 {m['line']}, {m['how']}): {context_of(texts[m['doc']], m)}")
    near = near_groups(res_field, lang, g)
    L.append(f"- (가) 반대 언어의 같은 dim이고 기준 값이 {int(NEAR * 100)}% 안인 양 {len(near)}개(가까운 차례):")
    for o in near:
        m = o["mentions"][0]
        L.append(f"  - base {o['base']:.6g}: [{docs[m['doc']]['title']}] raw `{m['raw']}` (줄 {m['line']}, {SIDE_NAME[o['side']]}): "
                 f"{context_of(texts[m['doc']], m, CTX_SMALL)}")
    places = digit_places(entry["field"], res_field, texts, lang, g)
    L.append(f"- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 {len(places)}개:")
    for title, w, c in places:
        L.append(f"  - [{title}] `{w}`: {c}")
    L.append("")
    return L


def cmd_sheet():
    res = cc.read_json(OUT / "results.json")
    old = OUT / "confirm.json"
    if old.exists() and any(e["read_ok"] is not None or e["truth"] is not None for e in cc.read_json(old)):
        raise SystemExit("confirm.json에 AI가 채운 판정이 있다. 덮어쓰지 않는다")
    confirm, L = [], ["# 3 세기: 후보 대조 종이 (sheet)", "", CRITERIA, "## 차례별 목록 (번호만)", ""]
    detail = []
    for field in FIELDS:
        rf = res["fields"][field]
        titles = {d["id"]: d["title"] for d in rf["docs"]}
        texts = {d["id"]: md_path(field, d["lang"], d["revid"]).read_text(encoding="utf-8") for d in rf["docs"]}
        for lang in LANGS:
            orders = make_orders(rf["groups"][lang], titles)
            entries = make_confirm(field, lang, orders)
            confirm += entries
            no_of = {e["group"]: e["no"] for e in entries}
            L.append(f"### {field} {lang}")
            for name, label in (("both", "두 언어 쪽 차례"), ("one", "한쪽 언어 쪽 차례"), ("table", "표 차례"), ("model", "모델 시험 차례(결정 ⑥)")):
                L.append(f"- {label} ({len(orders[name])}개): " + (", ".join(no_of[g["id"]] for g in orders[name]) or "없음"))
            L.append("")
            by_group = {g["id"]: g for s in SIDES for g in rf["groups"][lang][s]}
            detail += [(e, by_group[e["group"]], rf, texts) for e in entries]
    L += ["## 후보", ""]
    for e, g, rf, texts in detail:
        L += render_candidate(e, g, rf, texts)
    cc.write_json(OUT / "confirm.json", confirm)
    (OUT / "sheet.md").write_text("\n".join(L), encoding="utf-8")
    print("후보", len(confirm), {(f, lang): sum(1 for e in confirm if e["field"] == f and e["lang"] == lang) for f in FIELDS for lang in LANGS})


# --- status -----------------------------------------------------------------------------

def is_filled(e):
    return e["read_ok"] is not None and e["truth"] is not None


def is_correct(e):
    return is_filled(e) and e["read_ok"] is True and e["truth"] == ONLY


def check_confirm(entries):
    """칸 값이 틀린 번호를 알린다(read_ok는 true/false/null, truth는 TRUTH_ONLY 또는 null)."""
    bad = [e["no"] for e in entries if e["read_ok"] not in (True, False, None) or (e["truth"] is not None and e["truth"] not in TRUTH_ONLY)]
    if bad:
        raise SystemExit("칸 값이 틀린 번호: " + ", ".join(bad))


def quota(order, need, by_prefix=False):
    """order: 한 차례의 confirm 항목(차례 순). 몫 하나의 상태. by_prefix: 멈춤을 앞에서부터 빈틈없이 채운 부분의 맞은 수로 본다(모델 시험 몫).
    correct 맞은 수, filled 그 차례에서 채운 수, total 후보 수, stopped, exhausted(후보가 다 떨어짐), gaps(채운 것보다 앞인데 비어 있는 번호),
    next(아직 채우지 않은 앞의 번호, 멈추지 않았을 때), prefix(앞에서부터 빈틈없이 채운 수), prefix_correct(그 가운데 맞은 수)"""
    filled = [e for e in order if is_filled(e)]
    prefix = 0
    while prefix < len(order) and is_filled(order[prefix]):
        prefix += 1
    last = max((i for i, e in enumerate(order) if is_filled(e)), default=-1)
    correct = sum(1 for e in order if is_correct(e))
    prefix_correct = sum(1 for e in order[:prefix] if is_correct(e))
    stopped = (prefix_correct if by_prefix else correct) >= need
    return {"need": need, "correct": correct, "filled": len(filled), "total": len(order), "stopped": stopped,
            "exhausted": len(filled) == len(order),
            "gaps": [e["no"] for i, e in enumerate(order) if i < last and not is_filled(e)],
            "next": [] if stopped else [e["no"] for e in order if not is_filled(e)][:NEXT_MAX],
            "prefix": prefix, "prefix_correct": prefix_correct}


def ordered(entries, key, **where):
    """key 자리가 null이 아닌 항목을 그 자리 순으로. where: 다른 칸이 이 값인 것만."""
    return sorted([e for e in entries if e[key] is not None and all(e[k] == v for k, v in where.items())], key=lambda e: e[key])


def make_status(entries, need=NEED):
    """돌려주는 값: {분야: {언어: {both, one, table, model: quota}}}"""
    out = {}
    for field in FIELDS:
        out[field] = {}
        for lang in LANGS:
            es = [e for e in entries if e["field"] == field and e["lang"] == lang]
            out[field][lang] = {"both": quota(ordered(es, "order_side", side="both"), need["side"]),
                                "one": quota(ordered(es, "order_side", side="one"), need["side"]),
                                "table": quota(ordered(es, "order_table"), need["table"]),
                                "model": quota(ordered(es, "order_model"), need["model"], by_prefix=True)}
    return out


QUOTA_NAME = {"both": "두 언어 쪽", "one": "한쪽 언어 쪽", "table": "표", "model": "모델 시험 값"}


def unfinished(status):
    """멈추지도 후보가 다 떨어지지도 않은 몫과 빈틈이 있는 쪽을 글로 돌려준다(두 언어 쪽은 판정에 쓰지 않아 알리지 않고, 표와 모델 시험 몫의 빈틈은 알리지 않는다).
    비어 있으면 judge를 해도 된다."""
    out = []
    for field, langs in status.items():
        for lang, qs in langs.items():
            for name, s in qs.items():
                if name == "both":
                    continue
                if not (s["stopped"] or s["exhausted"]):
                    got = s["prefix_correct"] if name == "model" else s["correct"]
                    out.append(f"{field} {lang} {QUOTA_NAME[name]}: 맞은 수 {got}/{s['need']}, 다음 {', '.join(s['next'][:NEXT_MAX])}")
                elif name not in ("table", "model") and s["gaps"]:
                    out.append(f"{field} {lang} {QUOTA_NAME[name]}: 빈틈 {', '.join(s['gaps'])}")
    return out


def render_status(status):
    L = ["# 3 세기: 대조 상태 (status)", "",
         "숫자는 confirm.json에서 계산했다. 맞은 것 = read_ok가 true이고 truth가 \"그 언어에만\"인 것. 채운 것 = read_ok와 truth가 둘 다 채워진 것. "
         "두 언어 쪽은 판정에 쓰지 않는다(결정 \"3 세기에서 두 언어 주제 쪽의 필요한 수(18)는 통과 판정에서 빼고\"). 표의 맞은 수는 어느 차례에서 채웠든 센다. 모델 시험 값은 차례의 앞에서부터 빈틈없이 채운 부분에서 맞은 것을 쓴다(이미 채운 판정도 그 부분에 들면 쓴다).", ""]
    for field, langs in status.items():
        for lang, qs in langs.items():
            L += [f"## {field} {lang}", "",
                  "| 몫 | 필요한 수 | 맞은 수 | 그 차례에서 채운 수 | 후보 수 | 멈췄는가 | 후보가 다 떨어졌는가 | 빈틈 | 다음에 볼 번호 |", "|---|---|---|---|---|---|---|---|---|"]
            for name, s in qs.items():
                right = f"앞부분 {s['prefix_correct']} (모두 {s['correct']})" if name == "model" else s["correct"]
                label = QUOTA_NAME[name] + (" (판정에 쓰지 않음)" if name == "both" else "")
                L.append(f"| {label} | {s['need']} | {right} | {s['filled']} | {s['total']} | {'예' if s['stopped'] else '아니오'} | "
                         f"{'예' if s['exhausted'] else '아니오'} | {', '.join(s['gaps']) or '없음'} | {', '.join(s['next']) or '없음'} |")
            L.append("")
    todo = unfinished(status)
    L += ["남은 몫: " + ("없음. judge를 돌릴 수 있다." if not todo else ""), *[f"- {t}" for t in todo], ""]
    return "\n".join(L)


def cmd_status():
    entries = cc.read_json(OUT / "confirm.json")
    check_confirm(entries)
    text = render_status(make_status(entries))
    (OUT / "status.md").write_text(text, encoding="utf-8")
    print(text)


# --- judge ------------------------------------------------------------------------------

def estimate(s, name):
    """어림 = 프로그램이 센 후보 수 × 확인한 것 가운데 맞은 비율. 쪽 몫은 그 차례의 앞에서부터 채운 부분의 비율이고(쪽 차례는 빈틈이 없어야 judge를 한다),
    표 몫은 그 차례에서 채운 것 전체의 비율이다(표 차례에는 빈틈이 남는다). 후보가 없을 때만 0이다."""
    if s["total"] == 0:
        return 0.0
    if name == "table":
        return s["total"] * s["correct"] / s["filled"]
    return s["total"] * s["prefix_correct"] / s["prefix"]


def judge_all(status, need=NEED):
    """분야마다 언어마다 몫 둘(한쪽 언어 쪽, 표)의 맞은 수와 어림, 넘음/탈락, 여유를 계산한다. 두 언어 쪽은 판정에 쓰지 않고 참고로만 남긴다.
    돌려주는 값: {분야: {quotas: {언어: {몫: {need, correct, estimate, ok}}}, reference: {언어: {correct, filled, total}}, passed, reserve}}"""
    out = {}
    for field, langs in status.items():
        quotas, reference, ratios = {}, {}, []
        for lang, qs in langs.items():
            b, o, t = qs["both"], qs["one"], qs["table"]
            quotas[lang] = {
                "one": {"need": o["need"], "correct": o["correct"], "estimate": estimate(o, "one")},
                "table": {"need": t["need"], "correct": t["correct"], "estimate": estimate(t, "table")}}
            reference[lang] = {"correct": b["correct"], "filled": b["filled"], "total": b["total"]}
            for v in quotas[lang].values():
                v["ok"] = v["correct"] >= v["need"]
                ratios.append(v["estimate"] / v["need"])
        out[field] = {"quotas": quotas, "reference": reference, "passed": all(v["ok"] for qs in quotas.values() for v in qs.values()),
                      "reserve": min(ratios)}
    return out


def model_values(order, res_field, n=NEED["model"]):
    """모델 시험 차례의 앞에서부터 빈틈없이 채운 부분에서 맞은 것 앞의 n개: 번호, 문서 제목, raw, 줄(첫 언급 가운데 시험 대상 밖 문서의 것)."""
    docs = {d["id"]: d for d in res_field["docs"]}
    by_group = {g["id"]: g for lang in LANGS for s in SIDES for g in res_field["groups"][lang][s]}
    out = []
    prefix = 0
    while prefix < len(order) and is_filled(order[prefix]):
        prefix += 1
    for e in [e for e in order[:prefix] if is_correct(e)][:n]:
        m = next(m for m in by_group[e["group"]]["mentions"] if docs[m["doc"]]["outside_target"])
        out.append({"no": e["no"], "title": docs[m["doc"]]["title"], "raw": m["raw"], "line": m["line"]})
    return out


def render_judge(result, values):
    L = ["# 3 세기: 판정과 어림 (judge)", "",
         "숫자는 confirm.json과 results.json에서 계산했다. 넘음 = 언어마다 한쪽 언어 쪽과 표, 모두 넷을 맞은 수로 채움. "
         "어림 = 프로그램이 센 후보 수 × 확인한 것 가운데 맞은 비율(한쪽 언어 쪽은 그 차례의 앞에서부터 채운 부분의 비율, 표는 표 차례에서 채운 것 전체의 비율). "
         "여유 = 그 넷의 어림 ÷ 필요한 수 가운데 가장 낮은 값이고, 두 분야가 다 넘을 때만 쓰는 값이다. "
         "두 언어 쪽은 판정에 쓰지 않고 참고로 적는다(결정 \"3 세기에서 두 언어 주제 쪽의 필요한 수(18)는 통과 판정에서 빼고\").", ""]
    names = {"one": "한쪽 언어 쪽", "table": "표"}
    for field, r in result.items():
        L += [f"## {field}: {'넘음' if r['passed'] else '탈락'} (여유 {r['reserve']:.3f})", "",
              "| 언어 | 몫 | 필요한 수 | 맞은 수 | 어림 | 채웠는가 |", "|---|---|---|---|---|---|"]
        for lang, qs in r["quotas"].items():
            for name, v in qs.items():
                L.append(f"| {lang} | {names[name]} | {v['need']} | {v['correct']} | {v['estimate']:.2f} | {'예' if v['ok'] else '아니오'} |")
        L.append("")
        for lang, ref in r["reference"].items():
            L.append(f"- 참고(판정에 쓰지 않음) {lang} 두 언어 쪽: 맞은 수 {ref['correct']}, 채운 수 {ref['filled']}, 후보 수 {ref['total']}")
        L.append("")
        for lang in LANGS:
            L += [f"### {field} {lang} 모델 시험 값 (결정 ⑥)", ""]
            L += [f"- {v['no']} | {v['title']} | `{v['raw']}` | 줄 {v['line']}" for v in values[field][lang]] or ["- 없음"]
            L.append("")
    return "\n".join(L)


def cmd_judge():
    entries = cc.read_json(OUT / "confirm.json")
    check_confirm(entries)
    res = cc.read_json(OUT / "results.json")
    for field in FIELDS:
        for lang in LANGS:
            n_conf = sum(1 for e in entries if e["field"] == field and e["lang"] == lang)
            n_res = sum(1 for s in SIDES for g in res["fields"][field]["groups"][lang][s] if g["verdict"] == ONLY)
            if n_conf != n_res:
                raise SystemExit(f"{field} {lang}: confirm.json의 후보 {n_conf}개와 results.json의 후보 {n_res}개가 다르다")
    status = make_status(entries)
    todo = unfinished(status)
    if todo:
        raise SystemExit("아직 judge를 못 한다. 남은 몫:\n" + "\n".join(todo))
    result = judge_all(status)
    values = {f: {lang: model_values(ordered([e for e in entries if e["field"] == f and e["lang"] == lang], "order_model"), res["fields"][f])
                  for lang in LANGS} for f in FIELDS}
    cc.write_json(OUT / "judge.json", {"need": NEED, "fields": result, "model_values": values})
    text = render_judge(result, values)
    (OUT / "judge.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fns = {"count": cmd_count, "sheet": cmd_sheet, "status": cmd_status, "judge": cmd_judge}
    if cmd not in fns:
        raise SystemExit(__doc__)
    fns[cmd]()
