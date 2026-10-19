# 틀린 답을 다섯 갈래로 나눈다. 모델 서버는 부르지 않고 저장된 원본 결과만 읽는다.
#   한 답이 여러 갈래에 들 수 있다. 갈래마다 자기 조건으로 따로 판단한다.
#   결과: research_notes/stage2_stem_select/round1_error_types.jsonl 과 요약표
# 갈래 조건(답 하나마다 따로 본다):
#   숫자 없는 답     parsed가 null이거나 고른 숫자(picked)가 없다. 이 답은 다른 갈래를 보지 않는다.
#   재료 값이 틀림   풀이에 꼭 있어야 할 재료 값이 없다. 있다고 보는 폭은 요구마다 달라서,
#                    그 값을 바꿔도 답이 ±1% 안에 남는 가장 큰 폭(최대 1%)이다.
#   계산 없이 답함   풀이의 어떤 숫자도 picked의 ±1% 안이 아니다(단위 배수 없음).
#   단위를 잘못 바꿈 아래 셋 중 하나다. 모두 picked가 그 수의 ±1% 안이다.
#                    1) 자리수: value x 10^k (k는 0이 아닌 정수, -12~12)
#                    2) 그 문제가 직접 하는 소수점 아닌 단위 바꾸기(UNIT_CONV): 문제마다 정한 수 t 하나를
#                       곱하거나 나눈 값, 거기에 1000 단계 실수를 겹친 값. value x t^e x 10^k (e는 -1, +1; k는 -3, 0, 3)
#                    3) UNIT_CONV에 "offset"이 적힌 문제만: value +- 273.15 (K와 °C)
#   계산이 틀림      위 넷 중 어느 것도 아니다.
import ast
import argparse
import json
import re
from pathlib import Path

BASE = Path(__file__).parents[2] / "research_notes/stage2_stem_select"
TOPICS = ["chem", "solar", "mineral"]
CONDS = [("A", "base.jsonl"), ("C", "context.jsonl")]
OUT_NAME = "round1_error_types.jsonl"
BASE2 = BASE / "round2"
TOPICS2 = ["rare_earth", "exoplanets", "moons"]
OUT_NAME2 = "error_types.jsonl"

NO_NUM = "숫자 없는 답"
BAD_INPUT = "재료 값이 틀림"
NO_CALC = "계산 없이 답함"
BAD_UNIT = "단위를 잘못 바꿈"
BAD_CALC = "계산이 틀림"
LABELS = [NO_NUM, BAD_INPUT, NO_CALC, BAD_UNIT, BAD_CALC]

SCALES = [10.0 ** k for k in (-9, -6, -3, 0, 3, 6, 9)]
TOL_MAX = 0.01   # 재료 값 허용폭의 위쪽 끝(±1%)
ANS_TOL = 0.01   # 이 폭 안이면 답이 맞다고 보는 채점 폭(±1%)
KELVIN = 273.15


class Offset(float):
    """같은 양을 다른 기준으로 잰 값(K와 °C). 단위 배수가 아니라 차이로 맞춘다."""

# 문제마다 풀이에 꼭 들어가야 하는 재료 값. 각 문제의 근거 글에서 뽑았고,
# 센 숫자를 보기 전에 정했다(decisions/stage2.md 2026-10-19).
# 요구 하나는 대안 값 목록이다. 풀이에 그중 하나라도 있으면 채운 것이다.
# 첫 대안이 기본 값이고 계산식(calc)에 숫자 그대로 들어 있어야 한다.
# 나머지 대안은 두 종류다. 종류를 적지 않은 것은 "배수"(같은 양을 다른 단위로 쓰거나 합친 값),
#   Offset(...)은 "차이"(K와 °C처럼 기본 값에서 273.15를 뺀 값)다.
# 예: K와 °C 둘 다 인정하려고 [3695, Offset(3421.85)]처럼 적는다.
REQUIREMENTS = {
    "c-01": [[22.61]],
    "c-02": [[3695, Offset(3421.85)], [1811, Offset(1537.85)]],
    "c-03": [[196.97]],
    "c-04": [[0.534]],
    "c-05": [[13.546]],
    "c-06": [[370.944, Offset(97.794)]],
    "c-07": [[107.87]],
    "c-08": [[7.87]],
    "c-09": [[8.96], [2.70]],
    "c-10": [[58.443]],
    "s-01": [[227939200], [299792458]],
    "s-02": [[2575.5], [1737.1]],
    "s-03": [[9.639], [384400]],
    "s-04": [[2413402], [1.022]],
    "s-05": [[4498252900], [299792458]],
    "s-06": [[9.925]],
    "s-07": [[2870972220, 19.19126393], [1426725413, 9.53707032]],
    "s-08": [[24.077]],
    "s-09": [[149597870700], [299792458]],
    "s-10": [[17.334], [1.769137786]],
    "m-01": [[28.085], [15.999, 60.083]],
    "m-02": [[40.078], [12.011, 100.086], [15.999, 100.086]],
    "m-03": [[26.982], [15.999, 101.961]],
    "m-04": [[32.06], [55.845, 119.965]],
    "m-05": [[47.867], [15.999, 79.865]],
    "m-06": [[18.998], [40.078, 78.074]],
    "m-07": [[3.52]],
    "m-08": [[4.02], [3.52]],
    "m-09": [[2.17]],
    "m-10": [[2.23], [3.52]],
}

# 문제마다 그 문제의 계산식(calc)과 풀이 단계가 직접 하는 소수점 아닌 단위 바꾸기.
# 센 숫자를 다시 보기 전에 고정했다(decisions/stage2.md 2026-10-19). 적히지 않은 문제는 그런 바꾸기가 없다.
# 숫자는 곱하거나 나누는 수(60은 s<->min, 3600은 s<->h, 86400은 day<->s, 149597870.7은 AU<->km),
# "offset"은 K<->°C(273.15)다. 다른 문제에서 쓰는 바꾸기는 허용하지 않는다.
UNIT_CONV = {
    "c-02": ["offset"], "c-06": ["offset"],
    "s-01": [60], "s-03": [3600], "s-04": [86400], "s-05": [3600], "s-06": [60],
    "s-07": [149597870.7], "s-08": [3600], "s-09": [60], "s-10": [86400],
}

SUP = {c: str(i) for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
SUP["⁻"] = "-"
NUM = r"-?\d+(?:\.\d+)?"
SUPCH = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
# 3 × 10⁸, 3×10^8, 3 x 10^-19, 6.022e23
SCI = re.compile(
    rf"({NUM})\s*[×xX*]\s*10\s*(?:\^\s*\(?\s*(-?\d+)\s*\)?|([{SUPCH}]+))"
    rf"|({NUM})[eE]([+-]?\d+)"
)


def numbers_of(text):
    """풀이에서 쉼표를 지우고 숫자를 모두 뽑는다. 과학 표기는 숫자 하나로 센다."""
    s = str(text).replace(",", "").replace(" ", "")
    out = []

    def sci(m):
        if m.group(1) is not None:
            exp = m.group(2) if m.group(2) is not None else "".join(SUP[c] for c in m.group(3))
            out.append(float(f"{m.group(1)}e{int(exp)}"))
        else:
            out.append(float(f"{m.group(4)}e{int(m.group(5))}"))
        return " "

    rest = SCI.sub(sci, s)
    out += [float(x) for x in re.findall(NUM, rest)]
    return out


def near(x, y, tol=ANS_TOL):
    """x가 y의 ±tol 안인가."""
    return abs(x - y) <= tol * abs(y)


def matches_alt(nums, alt, primary, tol):
    """풀이 숫자 중 하나가 대안 alt와 맞는가. 맞은 풀이 숫자를 돌려주고 없으면 None.
    배수 대안: alt에 단위 배수(10의 ±3, 6, 9승)를 곱한 값의 ±tol 안.
    차이 대안: alt에서 기본 값(primary)의 ±tol 만큼(기본 값과 같은 절대 폭) 안, 배수 없음."""
    for n in nums:
        if isinstance(alt, Offset):
            if abs(n - alt) <= tol * abs(primary):
                return n
        else:
            for sc in SCALES:
                if near(n, alt * sc, tol):
                    return n
    return None


def eval_calc(expr, target=None, factor=1.0):
    """숫자와 + - * / 괄호만 있는 식을 계산한다(check_questions.py와 같은 방식).
    target과 같은 숫자는 식 어디에 있든 모두 factor배 해서 계산한다. 식에 든 target의 개수도 돌려준다."""
    count = 0

    def ev(n):
        nonlocal count
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            if target is not None and n.value == target:
                count += 1
                return n.value * factor
            return n.value
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b}[type(n.op)]
        raise ValueError(f"계산식에 쓸 수 없는 것: {ast.dump(n)}")

    return ev(ast.parse(expr, mode="eval")), count


def tolerance_of(calc, primary):
    """기본 값 primary를 ±r만큼 바꿔도(식의 같은 숫자를 모두 함께) 답이 ±1% 안에 남는 가장 큰 r(0~1%).
    위로 바꾸는 쪽과 아래로 바꾸는 쪽을 따로 이분법(정밀도 1e-7)으로 찾아 작은 쪽을 쓴다."""
    base, count = eval_calc(calc, primary)
    assert count >= 1, f"기본 값 {primary}가 계산식 {calc}에 숫자 그대로 없다"

    def ok(r, sign):
        v, _ = eval_calc(calc, primary, 1 + sign * r)
        return abs(v - base) <= ANS_TOL * abs(base)

    best = TOL_MAX
    for sign in (1, -1):
        if ok(TOL_MAX, sign):
            continue
        lo, hi = 0.0, TOL_MAX
        while hi - lo > 1e-7:
            mid = (lo + hi) / 2
            if ok(mid, sign):
                lo = mid
            else:
                hi = mid
        best = min(best, lo)
    return best


def tolerances_of(q, reqs=REQUIREMENTS):
    """문제 q의 요구마다 재료 값 허용폭(기본 값 기준)을 돌려준다. reqs는 문제 id별 요구 목록."""
    return [tolerance_of(q["calc"], alts[0]) for alts in reqs[q["id"]]]


def unit_factors(conv):
    """문제의 UNIT_CONV(conv)가 허용하는 곱하기 후보를 (f, k, t, e) 목록으로 돌려준다.
    자리수 후보(t=1, e=0)와, 숫자 t마다 t^e x 10^k(e -1/+1, k -3/0/3)를 함께 담는다."""
    out = [(10.0 ** k, k, 1, 0) for k in range(-12, 13) if k != 0]
    for t in conv:
        if t == "offset":
            continue
        out += [(t ** e * 10.0 ** k, k, t, e) for e in (-1, 1) for k in (-3, 0, 3)]
    return out


def unit_match(picked, value, conv=()):
    """picked가 value에 단위 바꾸기를 한 값인지 본다. 맞으면 근거 dict, 아니면 None.
    허용하는 바꾸기는 unit_factors(conv)와, conv에 "offset"이 있을 때의 value +- 273.15뿐이다.
    여럿 맞으면 |picked - value*f|가 가장 작은 것(같으면 자리수, 그다음 |k|가 작은 것)을 쓴다."""
    best = None
    for f, k, t, e in unit_factors(conv):
        if abs(f - 1) <= 1e-9:
            continue
        if near(picked, value * f):
            key = (abs(picked - value * f), e != 0, abs(k))
            if best is None or key < best[0]:
                best = (key, {"종류": "곱하기", "k": k, "t": t, "e": e, "f": f})
    if best is not None:
        return best[1]
    if "offset" in conv:
        for off in (KELVIN, -KELVIN):
            if near(picked, value + off):
                return {"종류": "더하기", "차이": off}
    return None


def candidate_count(conv):
    """문제 하나에서 단위를 잘못 바꿈으로 칠 수 있는 후보 수(곱하기 후보 + 더하기 2개)."""
    n = len(unit_factors(conv))
    return n + (2 if "offset" in conv else 0)


def reason_of(row):
    parsed = row["gen"]["parsed"]
    if isinstance(parsed, dict):
        return str(parsed.get("reason", ""))
    return ""


def classify(row, value, reqs, tols=None, conv=()):
    """틀린 답 하나를 받아 (갈래 목록, 갈래별 근거)를 돌려준다.
    tols는 요구마다의 재료 값 허용폭이다. 없으면 모두 ±1%.
    conv는 그 문제의 UNIT_CONV 목록이다. 없으면 자리수 바꾸기만 본다."""
    if tols is None:
        tols = [TOL_MAX] * len(reqs)
    picked = row["grade"]["picked"]
    if row["gen"]["parsed"] is None or picked is None:
        return [NO_NUM], {NO_NUM: {"parsed가 null": row["gen"]["parsed"] is None,
                                   "picked": picked}}
    nums = numbers_of(reason_of(row))
    labels, detail = [], {}

    missing, found, check = [], [], []
    for alts, tol in zip(reqs, tols):
        hit = None
        for a in alts:
            hit = matches_alt(nums, a, alts[0], tol)
            if hit is not None:
                found.append({"대안": alts, "맞은 풀이 숫자": hit})
                break
        if hit is None:
            missing.append(alts)
        check.append({"대안": alts, "허용폭": tol, "맞은 풀이 숫자": hit})
    if missing:
        labels.append(BAD_INPUT)
        detail[BAD_INPUT] = {"빠진 재료 값": missing, "맞은 재료 값": found, "재료 값 대조": check}

    if not any(near(n, picked) for n in nums):
        labels.append(NO_CALC)
        detail[NO_CALC] = {"풀이 숫자": nums, "picked": picked}

    um = unit_match(picked, value, conv)
    if um is not None:
        labels.append(BAD_UNIT)
        detail[BAD_UNIT] = {"picked": picked, "value": value, "비율": picked / value, **um}

    if not labels:
        labels.append(BAD_CALC)
        detail[BAD_CALC] = {"풀이 숫자": nums, "picked": picked, "value": value}
    return labels, detail


def round2_tables(base, topics=TOPICS2):
    """round 2는 요구와 단위 바꾸기가 질문 파일에 있다. 문제 id별 (요구, 단위 바꾸기) 사전을 돌려준다."""
    reqs, conv = {}, {}
    for topic in topics:
        for q in json.loads((Path(base) / topic / "questions.json").read_text(encoding="utf-8")):
            reqs[q["id"]] = q["requirements"]
            conv[q["id"]] = q["unit_conv"]
    return reqs, conv


def collect(base=BASE, topics=TOPICS, reqs=REQUIREMENTS, conv=UNIT_CONV):
    """틀린 답을 모두 분류한다. 순서는 주제, 문제 순서, 씨앗이다."""
    base = Path(base)
    recs = []
    for topic in topics:
        qs = json.loads((base / topic / "questions.json").read_text(encoding="utf-8"))
        tols = {q["id"]: tolerances_of(q, reqs) for q in qs}
        for cond, fname in CONDS:
            rows = [json.loads(l) for l in
                    (base / topic / "results" / fname).read_text(encoding="utf-8").splitlines() if l.strip()]
            order = {q["id"]: i for i, q in enumerate(qs)}
            qmap = {q["id"]: q for q in qs}
            rows.sort(key=lambda r: (order[r["id"]], r["seed"]))
            for r in rows:
                if r["correct"]:
                    continue
                q = qmap[r["id"]]
                labels, detail = classify(r, q["value"], reqs[r["id"]], tols[r["id"]],
                                          conv.get(r["id"], ()))
                recs.append({"topic": topic, "cond": cond, "id": r["id"], "seed": r["seed"],
                             "final_answer": r["final_answer"], "picked": r["grade"]["picked"],
                             "value": q["value"], "labels": labels, "detail": detail})
    return recs


def show_detail(rec):
    return json.dumps(rec["detail"], ensure_ascii=False)


def summarize(recs, out=print, topics=TOPICS):
    out("== 1. 주제 x 조건 x 갈래 (한 답은 가진 갈래마다 한 번씩 센다) ==")
    out("주제 | 조건 | 틀린 답 | " + " | ".join(LABELS) + " | 갈래 2개 이상인 답")
    totals = {}
    for topic in topics:
        for cond, _ in CONDS:
            rs = [r for r in recs if r["topic"] == topic and r["cond"] == cond]
            cnt = [sum(1 for r in rs if lab in r["labels"]) for lab in LABELS]
            multi = sum(1 for r in rs if len(r["labels"]) >= 2)
            out(f"{topic} | {cond} | {len(rs)} | " + " | ".join(map(str, cnt)) + f" | {multi}")
            totals[cond] = totals.get(cond, 0) + len(rs)
    out(f"틀린 답 합계: A {totals.get('A', 0)}, C {totals.get('C', 0)}")
    nowhere = sum(1 for r in recs if not r["labels"])
    out(f"어디에도 안 들어감: {nowhere}")

    out("")
    out("== 2. A에서 재료 값은 맞았는데 틀린 답 (A 틀린 답 중 '재료 값이 틀림'이 없는 것) ==")
    for topic in topics:
        rs = [r for r in recs if r["topic"] == topic and r["cond"] == "A"]
        n = sum(1 for r in rs if BAD_INPUT not in r["labels"])
        out(f"{topic}: {n} / A 틀린 답 {len(rs)}")

    out("")
    out("== 3. 직접 확인할 목록 (조건 x 갈래마다 앞에서 3개) ==")
    for cond, _ in CONDS:
        for lab in LABELS:
            rs = [r for r in recs if r["cond"] == cond and lab in r["labels"]][:3]
            out(f"-- 조건 {cond} / {lab} (앞 {len(rs)}개) --")
            for r in rs:
                out(f"{r['topic']} {r['id']} 씨앗 {r['seed']} | 최종 답: {r['final_answer']} | "
                    f"갈래: {', '.join(r['labels'])}")
                out(f"    근거: {json.dumps(r['detail'].get(lab), ensure_ascii=False)}")


def sensitive_rows(base=BASE, topics=TOPICS, reqs=REQUIREMENTS):
    """허용폭이 1%보다 작은 요구를 (주제, 문제, 기본 값, 허용폭)으로 돌려준다."""
    rows = []
    for topic in topics:
        qs = json.loads((Path(base) / topic / "questions.json").read_text(encoding="utf-8"))
        for q in qs:
            for alts, tol in zip(reqs[q["id"]], tolerances_of(q, reqs)):
                if tol < TOL_MAX:
                    rows.append((topic, q["id"], float(alts[0]), tol))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base", nargs="?", help="기준 폴더(round 1 기본값은 stage2_stem_select)")
    ap.add_argument("--round", type=int, choices=(1, 2), default=1)
    args = ap.parse_args()
    if args.round == 2:
        base, topics, out_name = Path(args.base) if args.base else BASE2, TOPICS2, OUT_NAME2
        reqs, conv = round2_tables(base, topics)
    else:
        base, topics, out_name = Path(args.base) if args.base else BASE, TOPICS, OUT_NAME
        reqs, conv = REQUIREMENTS, UNIT_CONV
    recs = collect(base, topics, reqs, conv)
    nowhere = sum(1 for r in recs if not r["labels"])
    assert nowhere == 0, f"어디에도 안 들어간 답이 {nowhere}개"
    with open(base / out_name, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summarize(recs, topics=topics)
    print("\n== 4. 재료 값 허용폭이 1%보다 작은 요구 (이 문제들은 재료 값이 조금만 달라도 답이 1%를 넘게 움직인다) ==")
    print("주제 | 문제 | 기본 값 | 허용폭(%)")
    for topic, qid, prim, tol in sensitive_rows(base, topics, reqs):
        print(f"{topic} | {qid} | {prim} | {tol * 100:.4f}")
    print("\n== 5. 문제마다 단위를 잘못 바꿈 후보 수 (우연히 맞을 가능성을 가늠하는 값) ==")
    print("후보 하나는 답의 ±1%(로그 폭 약 0.0087 자리) 구간이다. 후보가 많을수록 우연히 걸리기 쉽다.")
    for n in sorted({candidate_count(conv.get(qid, ())) for qid in reqs}):
        ids = [qid for qid in reqs if candidate_count(conv.get(qid, ())) == n]
        print(f"후보 {n}개: {', '.join(ids)}")
    print(f"\n{len(recs)}줄을 {base / out_name}에 썼다.")


if __name__ == "__main__":
    main()
