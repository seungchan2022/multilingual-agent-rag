# results/의 원본 기록에서 점수를 계산한다. 숫자는 모두 여기서 나온 값만 쓴다.
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
QS = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
ORDER = [q["id"] for q in QS]
KIND = {q["id"]: q["kind"] for q in QS}
KINDS = ["일반 지식", "추론", "문서 속 세부 사실"]
PASS_AT = 6  # 10번 중 6번 이상 맞으면 통과


def load(name):
    p = HERE / "results" / f"{name}.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def per_question(rows):
    c = defaultdict(lambda: [0, 0])
    for r in rows:
        c[r["id"]][0] += r["correct"]
        c[r["id"]][1] += 1
    return c


def report(name, rows):
    pq = per_question(rows)
    print(f"\n## {name}  (답 {len(rows)}개)")
    print("| id | 종류 | 맞은 수/돌린 수 | 통과 |")
    print("|---|---|---|---|")
    for qid in ORDER:
        if qid in pq:
            ok, n = pq[qid]
            print(f"| {qid} | {KIND[qid]} | {ok}/{n} | {'통과' if ok >= PASS_AT else '-'} |")
    passed = sum(1 for qid in ORDER if qid in pq and pq[qid][0] >= PASS_AT)
    ok_all = sum(v[0] for v in pq.values())
    n_all = sum(v[1] for v in pq.values())
    print(f"통과한 문제: {passed}/{len(pq)} · 맞은 답: {ok_all}/{n_all}")
    for k in KINDS:
        ids = [q for q in ORDER if KIND[q] == k and q in pq]
        p = sum(1 for q in ids if pq[q][0] >= PASS_AT)
        ok = sum(pq[q][0] for q in ids)
        n = sum(pq[q][1] for q in ids)
        print(f"  {k}: 통과 {p}/{len(ids)} · 맞은 답 {ok}/{n}")
    return pq


def judge_report(rows):
    """처음 답(1번째 판정)에 대한 판정 모델의 통과·실패를 실제 정답 여부와 맞춰 본다."""
    m = Counter()
    for r in rows:
        first = r["rounds"][0]
        m[(first["draft_correct"], first["passed"])] += 1
    print("\n## 판정 모델: 처음 답에 대한 판정 (정답 여부는 채점 규칙으로 본 것)")
    print(f"맞는 답을 통과: {m[(True, True)]} · 맞는 답을 실패로 봄: {m[(True, False)]}")
    print(f"틀린 답을 실패로 봄: {m[(False, False)]} · 틀린 답을 통과: {m[(False, True)]}")
    change = Counter()
    rounds = Counter(len(r["rounds"]) for r in rows)
    for r in rows:
        before, after = r["rounds"][0]["draft_correct"], r["correct"]
        change[(before, after)] += 1
    print("\n## 판정 고리 전후 (같은 씨앗의 처음 답과 최종 답)")
    print(f"틀림→맞음: {change[(False, True)]} · 맞음→틀림: {change[(True, False)]} · "
          f"맞음 유지: {change[(True, True)]} · 틀림 유지: {change[(False, False)]}")
    print("판정 횟수 분포:", dict(sorted(rounds.items())))
    unparsed = sum(1 for r in rows for rd in r["rounds"] if rd["judge"]["parsed"] is None)
    print("판정 출력을 JSON으로 읽지 못한 수:", unparsed)


base, refine, context = load("base"), load("refine_merged"), load("context")
report("기준 (문서 없이)", base)
if refine:
    report("판정 고리 (플로우 PDF 1단계)", refine)
    judge_report(refine)
if context:
    report("맞는 글 넣기", context)
for name, rows in (("base", base), ("context", context)):
    bad = sum(1 for r in rows if r["gen"]["parsed"] is None)
    print(f"{name}: 생성 출력을 JSON으로 읽지 못한 수 {bad}")
