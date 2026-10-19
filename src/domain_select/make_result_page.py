"""첫 번째 재기(이슈 #6)의 결과를 HTML 한 장으로 만든다.

  python3 src/domain_select/make_result_page.py [<stage2_stem_select 폴더> [<출력 html>]]

폴더 안의 <주제>/questions.json과 <주제>/results/*.jsonl, criterion4_langlinks.json을 읽기만 한다.
결과 폴더에는 아무것도 쓰지 않는다. 실행할 때마다 원본 기록에서 모든 숫자를 새로 계산한다.
숫자 규칙은 summarize.py와 같다. 통과 문제는 10번 중 6번 이상 맞은 문제다.
"""
import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_BASE = Path(__file__).resolve().parents[2] / "research_notes" / "stage2_stem_select"
TOPICS = [("chem", "화학 원소"), ("solar", "태양계 천체"), ("mineral", "광물")]
CITY = ("city_v1", "어제 도시 10문제")
PASS_AT = 6  # summarize.py와 같다
SEEDS = 10  # 질문 하나를 돌린 횟수
A_RANGE = (20, 40)  # 기준 ①: A의 맞은 답이 이 범위 안
C_GAIN = 40  # 기준 ③: C − A가 이 값 이상

e = html.escape


def read_jsonl(path):
    """파일이 없으면 빈 목록. 쓰는 중이라 마지막 줄이 덜 쓰였으면 그 줄은 건너뛴다."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def load_topic(base, folder, name):
    d = base / folder
    qs = json.loads((d / "questions.json").read_text(encoding="utf-8")) if (d / "questions.json").exists() else []
    res = d / "results"
    refine = read_jsonl(res / "refine_merged.jsonl") or read_jsonl(res / "refine.jsonl")
    return {"folder": folder, "name": name, "qs": qs,
            "A": read_jsonl(res / "base.jsonl"), "B": refine, "C": read_jsonl(res / "context.jsonl")}


def per_question(rows):
    c = defaultdict(lambda: [0, 0])
    for r in rows:
        c[r["id"]][0] += bool(r["correct"])
        c[r["id"]][1] += 1
    return c


def score(rows, qs):
    """맞은 답, 전체, 통과 문제. summarize.py의 계산과 같다."""
    pq = per_question(rows)
    ok = sum(v[0] for v in pq.values())
    n = sum(v[1] for v in pq.values())
    passed = sum(1 for q in qs if q["id"] in pq and pq[q["id"]][0] >= PASS_AT)
    return {"ok": ok, "n": n, "passed": passed, "pq": pq}


def judgement(rows):
    """B의 1회차만 본다. 처음 답이 맞았나 × judgement가 통과시켰나."""
    m = Counter()
    for r in rows:
        first = r["rounds"][0]
        m[(bool(first["draft_correct"]), bool(first["passed"]))] += 1
    change = Counter((bool(r["rounds"][0]["draft_correct"]), bool(r["correct"])) for r in rows)
    return {
        "맞음_통과": m[(True, True)], "맞음_불통과": m[(True, False)],
        "틀림_통과": m[(False, True)], "틀림_불통과": m[(False, False)],
        "고쳐짐": change[(False, True)], "망가짐": change[(True, False)],
        "서버오류": sum(1 for r in rows if any("error" in rd["judge"] for rd in r["rounds"])),
        "judge_null": sum(1 for r in rows for rd in r["rounds"] if rd["judge"].get("parsed") is None),
    }


def null_counts(t):
    """생성 출력을 JSON으로 읽지 못한 수. A, C, B의 모든 회차 초안."""
    return {
        "A": sum(1 for r in t["A"] if r["gen"]["parsed"] is None),
        "C": sum(1 for r in t["C"] if r["gen"]["parsed"] is None),
        "B": sum(1 for r in t["B"] for rd in r["rounds"] if rd["draft"]["parsed"] is None),
    }


def full(rows, qs):
    return bool(qs) and len(rows) == len(qs) * SEEDS


def verdict(ok):
    return "✓" if ok else "✗"


def criteria(t, sa, sc, links):
    """① ③ ④의 칸 글자. ②는 v2를 잰 뒤에만 판정한다."""
    qs = t["qs"]
    out = {"②": "v2를 잰 뒤 판정"}
    if full(t["A"], qs):
        lo, hi = A_RANGE
        out["①"] = f"{verdict(lo <= sa['ok'] <= hi)} (A {sa['ok']})"
    else:
        out["①"] = "아직"
    if full(t["A"], qs) and full(t["C"], qs):
        d = sc["ok"] - sa["ok"]
        out["③"] = f"{verdict(d >= C_GAIN)} (C−A {d:+d})"
    else:
        out["③"] = "아직"
    mine = links.get(t["folder"])
    if mine is None:
        out["④"] = "아직"
    else:
        missing = [k for k, v in mine.items() if v is None]
        out["④"] = f"{verdict(not missing)} (영어 글 없는 것 {len(missing)}개)"
    return out


def cell(rows, s, qs):
    if not rows:
        return "아직 없음"
    tag = "" if full(rows, qs) else " (진행 중)"
    return f"{s['ok']}/{s['n']} · 통과 {s['passed']}/{len(qs)}{tag}"


def diff(rows1, s1, rows0, s0, qs):
    if full(rows1, qs) and full(rows0, qs):
        return f"{s1['ok'] - s0['ok']:+d}"
    return "아직"


def table(head, body, cls=""):
    th = "".join(f"<th>{e(h)}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in body)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def pill(kind, text):
    """색이 있는 작은 이름표. 상태는 색뿐 아니라 글자로도 적는다."""
    return f'<span class="pill p-{kind}">{e(text)}</span>'


def mark(v):
    return pill("ok", "맞음") if v else pill("bad", "틀림")


def pass_pill(v):
    return pill("pass", "통과") if v else pill("fail", "불통과")


def multi_rows(t):
    out = []
    for key, label in (("A", "A"), ("B", "B-v1"), ("C", "C")):
        for r in t[key]:
            g = r.get("grade", {})
            if g.get("multi"):
                out.append([label, e(r["id"]), str(r["seed"]), e(str(r["final_answer"])),
                            f"<code>{e(str(g.get('picked')))}</code>", mark(r["correct"])])
    return out


def seed_rows(rows):
    return {(r["id"], r["seed"]): r for r in rows}


def change_of(r):
    """처음 답(1회차 초안)과 최종 답을 견줘 '고쳐짐' 또는 '망가짐'. 둘 다 아니면 None."""
    first, last = bool(r["rounds"][0]["draft_correct"]), bool(r["correct"])
    if not first and last:
        return "고쳐짐"
    if first and not last:
        return "망가짐"
    return None


def raw_toggle(text):
    """원문을 접어 둔다. 글자는 모두 escape한다."""
    return f'<details class="raw"><summary>원문 JSON 보기</summary><pre>{e(text or "")}</pre></details>'


def grade_sentence(grade):
    """채점 결과를 한 문장으로 쓴다. 여러 숫자가 있으면 그 목록과 고른 값을 함께 적는다."""
    if not grade:
        return ""
    if grade.get("picked") is None:
        return "답에서 숫자를 찾지 못했다."
    s = f"정답 {e(str(grade.get('answer_key')))}와 {e(str(grade.get('diff_pct')))}% 차이."
    if grade.get("multi"):
        nums = ", ".join(e(str(x)) for x in grade.get("numbers", []))
        s += f" 답에 숫자가 여러 개다({nums}). 마지막 숫자 {e(str(grade.get('picked')))}를 골랐다."
    return s


GEN_KEYS = ("answer", "reason")
JUDGE_KEYS = ("pass", "issues", "revision_instruction")


def key(k):
    """JSON 키 이름을 그대로 작은 mono 글씨로 붙인다."""
    return f'<code class="key">{e(k)}</code>'


def key_notes(parsed, expected):
    """기대한 키가 빠졌거나 정해지지 않은 키가 있으면 그 사실을 한 줄로 적는다."""
    notes = [f"{key(k)} 칸이 없음" for k in expected if k not in parsed]
    extra = [k for k in parsed if k not in expected]
    if extra:
        notes.append("정해지지 않은 칸: " + ", ".join(key(k) for k in extra))
    return f'<p class="keynote">{"; ".join(notes)}</p>' if notes else ""


def gen_block(gen, correct, grade, title="최종 답"):
    """모델 출력 하나. 답, 판정, 채점 한 문장, 풀이, 원문 순서."""
    p = gen.get("parsed") if gen else None
    text = (gen or {}).get("text", "")
    if p is None:
        return (f'<div class="out"><p class="ans-line"><span class="lbl">{e(title)}</span> {mark(correct)}</p>'
                f'<p class="bad">JSON으로 읽지 못함. 아래는 모델이 낸 원문이다.</p><pre>{e(text)}</pre></div>')
    g = grade_sentence(grade)
    return (f'<div class="out"><p class="ans-line"><span class="lbl">{e(title)} {key("answer")}</span> '
            f'<span class="ans">{e(str(p.get("answer", "")))}</span> {mark(correct)}</p>'
            + (f'<p class="grade">{g}</p>' if g else "")
            + f'<p class="lbl">풀이 {key("reason")}</p><p class="reason">{e(str(p.get("reason", "")))}</p>'
            + key_notes(p, GEN_KEYS) + raw_toggle(text) + "</div>")


def judge_block(rd):
    """judgement 한 번. 통과 여부, 지적, 고칠 지시, 원문."""
    j = rd["judge"]
    jp = j.get("parsed")
    head = f'<p class="lbl">{rd["round"]}회차 judgement</p>'
    if "error" in j:
        return f'<div class="out">{head}<p class="bad">서버 오류로 멈춤: {e(str(j["error"]))}</p></div>'
    if jp is None:
        return (f'<div class="out">{head}<p class="bad">JSON으로 읽지 못함. 아래는 judgement가 낸 원문이다.</p>'
                f'<pre>{e(j.get("text", ""))}</pre></div>')
    issues = "".join(f"<li>{e(str(x))}</li>" for x in jp.get("issues", [])) or "<li>없음</li>"
    return (f'<div class="out">{head}<p class="ans-line"><span class="lbl">통과 여부 {key("pass")}</span> {pass_pill(rd["passed"])}</p>'
            f'<p class="lbl">지적 {key("issues")}</p><ul class="issues">{issues}</ul>'
            f'<p class="lbl">고칠 지시 {key("revision_instruction")}</p><p class="reason">{e(str(jp.get("revision_instruction", "")))}</p>'
            + key_notes(jp, JUDGE_KEYS) + raw_toggle(j.get("text", "")) + "</div>")


def refine_block(r):
    """B-v1을 회차 순서로 세로로 늘어놓고, 끝에 최종 답 줄을 둔다."""
    steps = []
    for rd in r["rounds"]:
        steps.append(f'<li class="step"><p class="round">{rd["round"]}회차</p>'
                     + gen_block(rd["draft"], rd["draft_correct"], rd.get("draft_grade"), title=f'{rd["round"]}회차 답')
                     + judge_block(rd) + "</li>")
    final = (f'<div class="final"><span class="lbl">최종 답</span> <span class="ans">{e(str(r["final_answer"]))}</span> '
             f'{mark(r["correct"])}</div>')
    return f'<ol class="tl">{"".join(steps)}</ol>{final}'


def seed_summary(s, a, b, c):
    """씨앗 한 줄 요약. 씨앗 · A · B-v1(몇 회차에 끝났나) · C."""
    parts = [f"씨앗 {s}"]
    parts.append("A " + (mark(a["correct"]) if a else "아직 없음"))
    if b:
        last = b["rounds"][-1]
        ended = pill("grey", str(len(b["rounds"])) + "회차에서 끝남")
        end = f"{ended} 마지막 judgement {pass_pill(True)}" if last["passed"] else f"{ended} 끝까지 {pass_pill(False)}"
        parts.append(f"B-v1 {mark(b['correct'])} ({end})")
        ch = change_of(b)
        if ch:
            parts.append(pill("fix" if ch == "고쳐짐" else "break", ch))
    else:
        parts.append("B-v1 아직 없음")
    parts.append("C " + (mark(c["correct"]) if c else "아직 없음"))
    return " · ".join(parts)


def section(title, inner):
    return f'<section class="part"><h5>{e(title)}</h5>{inner}</section>'


def question_ref(q):
    """질문 맨 위에 둘 정답, 해설, 근거 글. 모델 풀이와 견주어 보는 기준이다."""
    steps = "".join(f"<li>{e(str(x))}</li>" for x in q.get("steps", [])) or "<li>없음</li>"
    quotes = "".join(f'<li>[{e(str(x.get("doc", "")))}] {e(str(x.get("quote", "")))}</li>'
                     for x in q.get("evidence_quotes", [])) or "<li>없음</li>"
    return (f'<div class="ref"><p><span class="lbl">정답</span> <span class="ans">{e(str(q.get("answer", "")))}</span></p>'
            f'<p class="lbl">해설</p><ol>{steps}</ol><p class="lbl">근거 글</p><ul>{quotes}</ul></div>')


def detail(t, q):
    a, b, c = seed_rows(t["A"]), seed_rows(t["B"]), seed_rows(t["C"])
    seeds = sorted({s for (i, s) in list(a) + list(b) + list(c) if i == q["id"]})
    body = []
    for s in seeds:
        k = (q["id"], s)
        inner = (section("A", gen_block(a[k]["gen"], a[k]["correct"], a[k].get("grade")) if k in a else "<p>아직 없음</p>")
                 + section("B-v1", refine_block(b[k]) if k in b else "<p>아직 없음</p>")
                 + section("C", gen_block(c[k]["gen"], c[k]["correct"], c[k].get("grade")) if k in c else "<p>아직 없음</p>"))
        body.append(f'<details class="seed"><summary>{seed_summary(s, a.get(k), b.get(k), c.get(k))}</summary>{inner}</details>')
    pa, pb, pc = (per_question(t[x]).get(q["id"], [0, 0])[0] for x in "ABC")
    changes = Counter(change_of(r) for r in t["B"] if r["id"] == q["id"])
    return (f'<details><summary><span class="qid">{e(q["id"])}</span> {e(q["question"])} '
            f'<span class="sm">A {pa} · B-v1 {pb} · C {pc} · 고쳐짐 {changes["고쳐짐"]} · 망가짐 {changes["망가짐"]}</span></summary>'
            f'{question_ref(q)}<div class="seeds">{"".join(body) or "<p>아직 없음</p>"}</div></details>')


CSS = """
:root {
  color-scheme: light;
  --bg: #fafbfc; --paper: #ffffff; --ink: #1a2330; --muted: #566273; --line: #dde3ea; --soft: #f3f6f9;
  --accent: #1d5fd1; --accent-soft: #e6eefb;
  --ok: #14532d; --ok-bg: #dcf5e4; --bad: #991b1b; --bad-bg: #fde3e3;
  --pass: #1e3a8a; --pass-bg: #dbe8ff; --fail: #9a3412; --fail-bg: #ffe8d2;
  --grey: #475569; --grey-bg: #edf0f4;
  --fix: #ffffff; --fix-bg: #15803d; --break: #ffffff; --break-bg: #b91c1c;
  --sans: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.7; }
.wrap { max-width: 1100px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 20px; }
h1 { font-size: 1.6rem; margin: 0; text-wrap: balance; }
h2 { font-size: 1.2rem; margin: 8px 0 0; }
h3 { font-size: 1rem; margin: 6px 0 0; }
h5 { font-size: .85rem; margin: 0 0 6px; color: var(--accent); }
.where { font-family: var(--mono); font-size: .85rem; color: var(--muted); }
.box { background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px; display: grid; gap: 10px; }
.box p, .box ol, .box ul { margin: 0; }
.box ol, .box ul { padding-left: 1.4em; }
.guide { background: var(--accent-soft); border-color: #b9cdf0; }
.guide h2 { margin: 0; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; font-size: .88rem; }
.tw { overflow-x: auto; background: var(--paper); border: 1px solid var(--line); border-radius: 8px; }
table { border-collapse: collapse; width: 100%; font-size: .88rem; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: .75rem; color: var(--muted); font-weight: 500; }
td:not(:first-child) { font-family: var(--mono); }
.note { font-size: .88rem; color: var(--muted); margin: 0; }
details { background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 8px 14px; }
summary { cursor: pointer; font-weight: 500; overflow-wrap: anywhere; }
.qlist { display: grid; gap: 10px; }
.seeds { display: grid; gap: 8px; margin-top: 10px; }
details.seed { background: var(--soft); }
details.raw { background: transparent; border: 0; padding: 0; margin-top: 6px; }
details.raw summary { font-size: .8rem; font-weight: 400; color: var(--accent); }
pre { white-space: pre-wrap; overflow-wrap: anywhere; font-family: var(--mono); font-size: .8rem; background: var(--soft);
  border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; margin: 6px 0 0; }
.qid { font-family: var(--mono); font-size: .8rem; color: var(--accent); background: var(--accent-soft); padding: 2px 8px; border-radius: 4px; }
.sm { font-family: var(--mono); font-size: .8rem; color: var(--muted); }
.pill { display: inline-block; font-size: .78rem; font-weight: 500; line-height: 1.5; padding: 0 9px; border-radius: 999px; white-space: nowrap; }
.p-ok { color: var(--ok); background: var(--ok-bg); }
.p-bad { color: var(--bad); background: var(--bad-bg); }
.p-pass { color: var(--pass); background: var(--pass-bg); }
.p-fail { color: var(--fail); background: var(--fail-bg); }
.p-grey { color: var(--grey); background: var(--grey-bg); }
.p-fix { color: var(--fix); background: var(--fix-bg); }
.p-break { color: var(--break); background: var(--break-bg); }
.ref { background: var(--accent-soft); border-radius: 8px; padding: 10px 14px; margin-top: 10px; }
.ref p { margin: 2px 0; }
.ref ol, .ref ul { margin: 2px 0 6px; padding-left: 1.4em; max-width: 70ch; }
.part { border-top: 1px solid var(--line); margin-top: 10px; padding-top: 10px; }
.out { background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; margin: 6px 0; overflow-wrap: anywhere; }
.out p { margin: 2px 0; }
.lbl { font-size: .78rem; color: var(--muted); letter-spacing: .04em; }
.ans { font-family: var(--mono); font-size: 1.15rem; font-weight: 500; }
.ans-line { display: flex; flex-wrap: wrap; gap: 4px 10px; align-items: baseline; }
.key { font-size: .72rem; color: var(--muted); background: var(--soft); padding: 0 5px; border-radius: 4px; margin-left: 4px; }
.keynote { font-size: .85rem; color: var(--fail); }
.grade { font-size: .88rem; color: var(--muted); }
.reason { max-width: 70ch; }
.issues { margin: 2px 0 6px; padding-left: 1.4em; max-width: 70ch; }
.bad { color: var(--bad); }
.tl { list-style: none; margin: 0; padding: 0 0 0 14px; border-left: 3px solid var(--accent-soft); }
.step { margin: 0 0 8px; padding-left: 10px; }
.round { font-size: .8rem; font-weight: 700; color: var(--accent); margin: 4px 0 0; }
.final { display: flex; flex-wrap: wrap; gap: 4px 10px; align-items: baseline; background: var(--accent-soft);
  border-radius: 8px; padding: 8px 12px; margin-top: 6px; }
code { font-family: var(--mono); font-size: .85em; }
summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
"""


def build(base, out):
    base = Path(base)
    links_path = base / "criterion4_langlinks.json"
    links = json.loads(links_path.read_text(encoding="utf-8")) if links_path.exists() else {}
    topics = [load_topic(base, f, n) for f, n in TOPICS]
    city = load_topic(base, *CITY)
    everyone = topics + [city]
    sc = {t["folder"]: {x: score(t[x], t["qs"]) for x in "ABC"} for t in everyone}

    # 2. 요약 표
    body = []
    for t in everyone:
        s, qs = sc[t["folder"]], t["qs"]
        if t is city:
            crit = {k: "-" for k in "①②③④"}
        else:
            crit = criteria(t, s["A"], s["C"], links)
        body.append([e(t["name"]), cell(t["A"], s["A"], qs), cell(t["B"], s["B"], qs), cell(t["C"], s["C"], qs),
                     diff(t["B"], s["B"], t["A"], s["A"], qs), diff(t["C"], s["C"], t["A"], s["A"], qs),
                     crit["①"], crit["②"], crit["③"], crit["④"]])
    summary = table(["", "A", "B-v1", "C", "B-v1 − A", "C − A", "① A 20~40", "② B−A ≥ 20", "③ C−A ≥ 40", "④ 영어 글"], body)

    # 3. judgement 표
    jrows = []
    for t in everyone:
        nulls = null_counts(t)
        if t["B"]:
            j = judgement(t["B"])
            jrows.append([e(t["name"]), str(len(t["B"])), str(j["맞음_통과"]), str(j["맞음_불통과"]), str(j["틀림_통과"]),
                          str(j["틀림_불통과"]), str(j["고쳐짐"]), str(j["망가짐"]), str(j["서버오류"]), str(j["judge_null"]),
                          f'A {nulls["A"]} · B {nulls["B"]} · C {nulls["C"]}'])
        else:
            jrows.append([e(t["name"]), "아직 없음"] + ["-"] * 8 + [f'A {nulls["A"]} · C {nulls["C"]}'])
    judge = table(["", "B-v1 답 수", "처음 답 맞음 · 통과", "맞음 · 불통과(맞는 답을 떨어뜨림)", "틀림 · 통과", "틀림 · 불통과",
                   "고쳐짐(처음 틀림 → 최종 맞음)", "망가짐(처음 맞음 → 최종 틀림)", "서버 오류로 멈춘 답",
                   "judgement 출력을 못 읽음", "생성 출력을 못 읽음"], jrows)

    # 4. 숫자가 둘 이상인 답
    multi_html = []
    for t in everyone:
        m = multi_rows(t)
        has_grade = any("grade" in r for x in "ABC" for r in t[x])
        if m:
            multi_html.append(f"<h3>{e(t['name'])}</h3>" + table(["조건", "id", "씨앗", "최종 답", "고른 값", "채점"], m))
        elif has_grade:
            multi_html.append(f"<h3>{e(t['name'])}</h3><p class='note'>없음</p>")
        else:
            multi_html.append(f"<h3>{e(t['name'])}</h3><p class='note'>아직 없음 (옛 채점은 이 값을 기록하지 않음)</p>")

    # 5. 질문별 표, 6. 씨앗별 자세히
    perq, details = [], []
    for t in topics:
        if not t["qs"]:
            perq.append(f"<h3>{e(t['name'])}</h3><p class='note'>질문 파일 없음</p>")
            continue
        pqs = {x: sc[t["folder"]][x]["pq"] for x in "ABC"}
        rows = []
        for q in t["qs"]:
            cells = []
            for x in "ABC":
                v = pqs[x].get(q["id"])
                cells.append(f"{v[0]}/{v[1]}" if v else "아직 없음")
            rows.append([e(q["id"]), e(q["question"]), e(q["answer"])] + cells)
        perq.append(f"<h3>{e(t['name'])}</h3>" + table(["id", "질문", "정답", "A", "B-v1", "C"], rows))
        details.append(f"<h3>{e(t['name'])}</h3><div class=\"qlist\">" + "".join(detail(t, q) for q in t["qs"]) + "</div>")

    page = f"""<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>첫 번째 재기 결과</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <div class="where">2단계 &gt; 도메인 다시 고르기(#6) &gt; 3. 첫 번째 재기 &gt; 결과</div>
  <h1>첫 번째 재기 결과</h1>
  <div class="box">
    <p>A는 문서 없이 바로 답한 것입니다. B-v1은 A의 답을 judgement가 보고 generate가 고쳐 쓴 것입니다(어제 프롬프트). C는 근거 글을 넣고 답한 것입니다.</p>
    <p>100은 질문 10개 × 10번입니다. 숫자는 저장된 원본 기록에서 이 페이지를 만들 때마다 새로 계산합니다. 통과 문제는 10번 중 6번 이상 맞은 질문입니다.</p>
    <p>기준 ②는 B-v2를 잰 뒤에 판정합니다. 지금은 B-v1 − A만 참고로 보입니다. 기록이 100개가 안 되면 ①③과 차이 칸은 &quot;아직&quot;입니다.</p>
  </div>
  <div class="box guide">
    <h2>읽는 법</h2>
    <ol>
      <li>요약 표에서 후보마다 A, B-v1, C의 점수를 봅니다.</li>
      <li>질문별 표에서 어느 질문이 맞고 어느 질문이 틀렸는지 봅니다.</li>
      <li>아래 &quot;씨앗별 자세히&quot;에서 질문을 펼쳐 정답과 해설을 먼저 읽습니다.</li>
      <li>씨앗 하나를 펼쳐 A, B-v1, C 순서로 따라갑니다. B-v1은 회차마다 초안, 그다음 judgement 순서입니다.</li>
      <li>특히 &quot;고쳐짐&quot;(처음 틀림, 최종 맞음)과 &quot;망가짐&quot;(처음 맞음, 최종 틀림) 씨앗을 봅니다.</li>
    </ol>
    <p class="note">씨앗은 같은 질문을 다시 돌릴 때 붙인 번호입니다. 질문 하나를 씨앗 1~10으로 10번 돌렸습니다. 이름표의 뜻은 아래와 같습니다.</p>
    <div class="legend">
      <span><span class="pill p-ok">맞음</span> 모델의 최종 답이 정답</span>
      <span><span class="pill p-bad">틀림</span> 최종 답이 정답이 아님</span>
      <span><span class="pill p-pass">통과</span> judgement가 답을 통과시킴</span>
      <span><span class="pill p-fail">불통과</span> judgement가 고치라고 함</span>
      <span><span class="pill p-fix">고쳐짐</span> 처음 틀림, 최종 맞음</span>
      <span><span class="pill p-break">망가짐</span> 처음 맞음, 최종 틀림</span>
      <span><span class="pill p-grey">3회차에서 끝남</span> 부가 정보</span>
    </div>
  </div>
  <h2>요약</h2>
  {summary}
  <h2>judgement가 한 일</h2>
  <p class="note">B-v1의 1회차만 봅니다. 처음 답은 1회차 초안이고, 최종 답은 마지막 회차 뒤의 답입니다.</p>
  {judge}
  <h2>숫자가 둘 이상인 답</h2>
  <p class="note">채점은 답의 마지막 숫자를 씁니다. 숫자가 둘 이상이면 사용자가 고른 값이 맞는지 볼 수 있게 모두 적습니다.</p>
  {''.join(multi_html)}
  <h2>질문별 맞은 횟수</h2>
  {''.join(perq)}
  <h2>씨앗별 자세히</h2>
  <p class="note">질문을 눌러 펼치고, 그 안에서 씨앗을 눌러 펼칩니다.</p>
  {''.join(details)}
</div>
"""
    out = Path(out)
    out.write_text(page, encoding="utf-8")
    return out, len(page)


if __name__ == "__main__":
    b = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BASE
    o = Path(sys.argv[2]) if len(sys.argv) > 2 else b / "round1_results.html"
    print(*build(b, o))
