# 틀린 답을 다섯 갈래로 나눈다. 모델 서버는 부르지 않고 저장된 원본 결과만 읽는다.
#   한 답이 여러 갈래에 들 수 있다. 갈래마다 자기 조건으로 따로 판단한다.
#   결과: research_notes/stage2_stem_select/round1_error_types.jsonl 과 요약표
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parents[2] / "research_notes/stage2_stem_select"
TOPICS = ["chem", "solar", "mineral"]
CONDS = [("A", "base.jsonl"), ("C", "context.jsonl")]
OUT_NAME = "round1_error_types.jsonl"

NO_NUM = "숫자 없는 답"
BAD_INPUT = "재료 값이 틀림"
NO_CALC = "계산 없이 답함"
BAD_UNIT = "단위를 잘못 바꿈"
BAD_CALC = "계산이 틀림"
LABELS = [NO_NUM, BAD_INPUT, NO_CALC, BAD_UNIT, BAD_CALC]

SCALES = [10.0 ** k for k in (-9, -6, -3, 0, 3, 6, 9)]

# 문제마다 풀이에 꼭 들어가야 하는 재료 값. 각 문제의 근거 글에서 뽑았고,
# 센 숫자를 보기 전에 정했다(decisions/stage2.md 2026-10-19).
# 요구 하나는 대안 값 목록이다. 풀이에 그중 하나라도 있으면 채운 것이다.
# 예: K와 °C 둘 다 인정하려고 {3695, 3421.85}처럼 적는다.
REQUIREMENTS = {
    "c-01": [[22.61]],
    "c-02": [[3695, 3421.85], [1811, 1537.85]],
    "c-03": [[196.97]],
    "c-04": [[0.534]],
    "c-05": [[13.546]],
    "c-06": [[370.944, 97.794]],
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


def near(x, y):
    """x가 y의 ±1% 안인가."""
    return abs(x - y) <= 0.01 * abs(y)


def matches_scaled(nums, alt):
    """풀이 숫자 중 하나가 alt에 단위 배수(10의 ±3, 6, 9승)를 곱한 값과 ±1% 안에서 맞는가."""
    for n in nums:
        for sc in SCALES:
            if near(n, alt * sc):
                return n
    return None


def reason_of(row):
    parsed = row["gen"]["parsed"]
    if isinstance(parsed, dict):
        return str(parsed.get("reason", ""))
    return ""


def classify(row, value, reqs):
    """틀린 답 하나를 받아 (갈래 목록, 갈래별 근거)를 돌려준다."""
    picked = row["grade"]["picked"]
    if row["gen"]["parsed"] is None or picked is None:
        return [NO_NUM], {NO_NUM: {"parsed가 null": row["gen"]["parsed"] is None,
                                   "picked": picked}}
    nums = numbers_of(reason_of(row))
    labels, detail = [], {}

    missing, found = [], []
    for alts in reqs:
        hit = None
        for a in alts:
            hit = matches_scaled(nums, a)
            if hit is not None:
                found.append({"대안": alts, "맞은 풀이 숫자": hit})
                break
        if hit is None:
            missing.append(alts)
    if missing:
        labels.append(BAD_INPUT)
        detail[BAD_INPUT] = {"빠진 재료 값": missing, "맞은 재료 값": found}

    if not any(near(n, picked) for n in nums):
        labels.append(NO_CALC)
        detail[NO_CALC] = {"풀이 숫자": nums, "picked": picked}

    for k in range(-12, 13):
        if k != 0 and near(picked, value * 10.0 ** k):
            labels.append(BAD_UNIT)
            detail[BAD_UNIT] = {"picked": picked, "value": value,
                                "비율": picked / value, "k": k}
            break

    if not labels:
        labels.append(BAD_CALC)
        detail[BAD_CALC] = {"풀이 숫자": nums, "picked": picked, "value": value}
    return labels, detail


def collect(base=BASE):
    """틀린 답을 모두 분류한다. 순서는 주제, 문제 순서, 씨앗이다."""
    base = Path(base)
    recs = []
    for topic in TOPICS:
        qs = json.loads((base / topic / "questions.json").read_text(encoding="utf-8"))
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
                labels, detail = classify(r, q["value"], REQUIREMENTS[r["id"]])
                recs.append({"topic": topic, "cond": cond, "id": r["id"], "seed": r["seed"],
                             "final_answer": r["final_answer"], "picked": r["grade"]["picked"],
                             "value": q["value"], "labels": labels, "detail": detail})
    return recs


def show_detail(rec):
    return json.dumps(rec["detail"], ensure_ascii=False)


def summarize(recs, out=print):
    out("== 1. 주제 x 조건 x 갈래 (한 답은 가진 갈래마다 한 번씩 센다) ==")
    out("주제 | 조건 | 틀린 답 | " + " | ".join(LABELS) + " | 갈래 2개 이상인 답")
    totals = {}
    for topic in TOPICS:
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
    for topic in TOPICS:
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


def main():
    base = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE
    recs = collect(base)
    nowhere = sum(1 for r in recs if not r["labels"])
    assert nowhere == 0, f"어디에도 안 들어간 답이 {nowhere}개"
    with open(base / OUT_NAME, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    summarize(recs)
    print(f"\n{len(recs)}줄을 {base / OUT_NAME}에 썼다.")


if __name__ == "__main__":
    main()
