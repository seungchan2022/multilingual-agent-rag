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


def mark(v):
    return "맞음" if v else "틀림"


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


def gen_block(gen, correct, grade):
    p = gen.get("parsed") if gen else None
    if p is None:
        return f'<p class="bad">JSON으로 읽지 못함. 원문: {e((gen or {}).get("text", ""))}</p>'
    g = ""
    if grade and "picked" in grade:
        g = (f' · 숫자 <code>{e(str(grade.get("numbers")))}</code> · 고른 값 <code>{e(str(grade.get("picked")))}</code>'
             f' · 차이 <code>{e(str(grade.get("diff_pct")))}%</code>')
    return (f'<p>답 <code>{e(str(p.get("answer", "")))}</code> · {mark(correct)}{g}</p>'
            f'<p class="reason">{e(str(p.get("reason", "")))}</p>')


def refine_block(r):
    parts = []
    for rd in r["rounds"]:
        j = rd["judge"]
        jp = j.get("parsed")
        parts.append(f'<h5>{rd["round"]}회차 초안</h5>' + gen_block(rd["draft"], rd["draft_correct"], rd.get("draft_grade")))
        if "error" in j:
            parts.append(f'<p class="bad">judgement 서버 오류: {e(str(j["error"]))}</p>')
        elif jp is None:
            parts.append(f'<p class="bad">judgement 출력을 JSON으로 읽지 못함. 원문: {e(j.get("text", ""))}</p>')
        else:
            issues = "".join(f"<li>{e(str(x))}</li>" for x in jp.get("issues", []))
            parts.append(f'<h5>{rd["round"]}회차 judgement</h5><p>통과: <code>{e(str(jp.get("pass")))}</code></p>'
                         f'<ul>{issues}</ul><p class="reason">고칠 지시: {e(str(jp.get("revision_instruction", "")))}</p>')
    parts.append(f'<p><b>최종 답</b> <code>{e(str(r["final_answer"]))}</code> · {mark(r["correct"])}</p>')
    return "".join(parts)


def detail(t, q):
    a, b, c = seed_rows(t["A"]), seed_rows(t["B"]), seed_rows(t["C"])
    seeds = sorted({s for (i, s) in list(a) + list(b) + list(c) if i == q["id"]})
    body = []
    for s in seeds:
        k = (q["id"], s)
        sec = [f"<h4>씨앗 {s}</h4>"]
        sec.append("<h5>A</h5>" + (gen_block(a[k]["gen"], a[k]["correct"], a[k].get("grade")) if k in a else "<p>아직 없음</p>"))
        sec.append("<h5>B-v1</h5>" + (refine_block(b[k]) if k in b else "<p>아직 없음</p>"))
        sec.append("<h5>C</h5>" + (gen_block(c[k]["gen"], c[k]["correct"], c[k].get("grade")) if k in c else "<p>아직 없음</p>"))
        body.append(f'<div class="seed">{"".join(sec)}</div>')
    pa, pb, pc = (per_question(t[x]).get(q["id"], [0, 0])[0] for x in "ABC")
    return (f'<details><summary><span class="qid">{e(q["id"])}</span> {e(q["question"])} '
            f'<span class="sm">A {pa} · B-v1 {pb} · C {pc}</span></summary>{"".join(body) or "<p>아직 없음</p>"}</details>')


CSS = """
:root {
  --bg: #f3f5f7; --paper: #ffffff; --ink: #1c2530; --muted: #5b6876; --line: #d5dbe1;
  --accent: #1f5fa8; --accent-soft: #e3ecf7; --warn: #8a5a00; --warn-soft: #fbf1dc;
  --ok: #1d6b3a; --bad: #a22a2a;
  --sans: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #12171d; --paper: #1a2129; --ink: #e4e9ee; --muted: #9aa7b4; --line: #2c3743;
  --accent: #7fb0ea; --accent-soft: #1d2d40; --warn: #e2b764; --warn-soft: #33290f;
  --ok: #6cc58a; --bad: #e88a8a; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #12171d; --paper: #1a2129; --ink: #e4e9ee; --muted: #9aa7b4; --line: #2c3743;
  --accent: #7fb0ea; --accent-soft: #1d2d40; --warn: #e2b764; --warn-soft: #33290f;
  --ok: #6cc58a; --bad: #e88a8a; color-scheme: dark; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.65; }
.wrap { max-width: 1100px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 20px; }
h1 { font-size: 1.6rem; margin: 0; text-wrap: balance; }
h2 { font-size: 1.2rem; margin: 8px 0 0; }
h3 { font-size: 1rem; margin: 6px 0 0; }
h4 { font-size: .9rem; margin: 12px 0 2px; color: var(--accent); }
h5 { font-size: .75rem; letter-spacing: .06em; color: var(--muted); font-weight: 500; margin: 8px 0 2px; }
.where { font-family: var(--mono); font-size: .85rem; color: var(--muted); }
.box { background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 16px 18px; display: grid; gap: 10px; }
.box p { margin: 0; }
.tw { overflow-x: auto; background: var(--paper); border: 1px solid var(--line); border-radius: 6px; }
table { border-collapse: collapse; width: 100%; font-size: .88rem; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: .75rem; color: var(--muted); font-weight: 500; white-space: nowrap; }
td:not(:first-child) { font-family: var(--mono); }
.note { font-size: .85rem; color: var(--muted); margin: 0; }
details { background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 8px 14px; }
summary { cursor: pointer; font-weight: 500; overflow-wrap: anywhere; }
.qid { font-family: var(--mono); font-size: .8rem; color: var(--accent); background: var(--accent-soft); padding: 2px 8px; border-radius: 4px; }
.sm { font-family: var(--mono); font-size: .8rem; color: var(--muted); }
.seed { border-top: 1px solid var(--line); margin-top: 8px; padding-top: 4px; }
.seed p { margin: 2px 0; overflow-wrap: anywhere; }
.reason { font-size: .85rem; color: var(--muted); }
.bad { color: var(--bad); }
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
        details.append(f"<h3>{e(t['name'])}</h3>" + "".join(detail(t, q) for q in t["qs"]))

    page = f"""<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
  <p class="note">질문을 눌러 펼칩니다.</p>
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
