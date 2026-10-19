"""후보 고르기 실험(이슈 #6)의 질문 파일을 검사한다.

  .venv/bin/python src/domain_select/check_questions.py <후보 폴더> [--short-test <짧은 시험 questions.json>]

<후보 폴더>/questions.json의 질문마다 본다(규칙은 decisions/stage2.md의 2026-10-19 줄들).
  ① 근거 글(evidence_quotes)이 <후보 폴더>/md/<문서>.md에 글자 그대로 있다
  ② 계산식(calc)을 다시 계산하면 value와 0.1% 안에서 같다
  ③ 정답(answer)의 숫자가 value와 ±1% 안이다(채점 규칙과 같은 폭)
  ④ 계산식에 연산이 두 개 이상이다
  ⑤ 계산식에 단위 바꾸기가 있다: 질문의 unit_factor(예: 1000, 273.15, 3600)가 계산식의 숫자로 들어 있다
  ⑥ 질문에 ingredient(재료 값)가 있으면 계산식의 숫자 가운데 하나와 정확히 같다
--short-test를 주면 추가로 본다.
  ⓐ 질문마다 ingredient 칸이 있다
  ⓑ 같은 id의 짧은 시험 질문이 있다
  ⓒ 그 짧은 시험 질문의 value가 ingredient와 같고 target이 같다
  ⓓ 짧은 시험의 id가 모두 정식 질문에 있다(빠진 대상이 없다)
걸린 것은 질문 번호와 함께 모두 출력하고 종료 코드 1로 끝낸다.
"""
import ast, json, re, sys
from pathlib import Path


def evaluate(expr):
    """숫자와 + - * / 괄호만 있는 식을 계산하고 연산의 수와 식에 든 숫자들을 함께 돌려준다."""
    ops, nums = 0, []

    def ev(n):
        nonlocal ops
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            nums.append(n.value)
            return n.value
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            ops += 1
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b else float("nan")}[type(n.op)]
        raise ValueError(f"계산식에 쓸 수 없는 것: {ast.dump(n)}")

    value = ev(ast.parse(expr, mode="eval"))
    return value, ops, nums


def first_number(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s.replace(",", ""))
    return float(m.group()) if m else None


def find_problems(folder, short_test=None):
    """질문 파일을 검사해 (질문 수, 걸린 것 목록)을 돌려준다. short_test는 짧은 시험 questions.json 경로."""
    qs = json.loads((folder / "questions.json").read_text(encoding="utf-8"))
    problems = []
    for q in qs:
        for e in q["evidence_quotes"]:
            md = folder / "md" / f"{e['doc']}.md"
            if not md.exists():
                problems.append(f"{q['id']} ① 문서가 없음: {e['doc']}")
            elif e["quote"] not in md.read_text(encoding="utf-8"):
                problems.append(f"{q['id']} ① 근거 글이 {e['doc']} 문서에 그대로 없음: {e['quote']}")
        got, ops, nums = evaluate(q["calc"])
        if abs(got - q["value"]) > abs(q["value"]) * 0.001:
            problems.append(f"{q['id']} ② 계산식 {q['calc']} = {got}, value {q['value']}와 다름")
        a = first_number(q["answer"])
        if a is None or abs(a - q["value"]) > abs(q["value"]) * 0.01:
            problems.append(f"{q['id']} ③ 정답 {q['answer']}의 숫자가 value {q['value']}와 ±1% 밖")
        if ops < 2:
            problems.append(f"{q['id']} ④ 계산식의 연산이 {ops}개")
        if "unit_factor" not in q or float(q["unit_factor"]) not in nums:
            problems.append(f"{q['id']} ⑤ 단위 바꾸기 unit_factor({q.get('unit_factor')})가 계산식의 숫자에 없음")
        if "ingredient" in q and float(q["ingredient"]) not in nums:
            problems.append(f"{q['id']} ⑥ ingredient {q['ingredient']}가 계산식 {q['calc']}의 숫자에 없음")
    if short_test:
        short = {s["id"]: s for s in json.loads(Path(short_test).read_text(encoding="utf-8"))}
        ids = {q["id"] for q in qs}
        for q in qs:
            if "ingredient" not in q:
                problems.append(f"{q['id']} ⑥ⓐ ingredient 칸이 없음")
            s = short.get(q["id"])
            if s is None:
                problems.append(f"{q['id']} ⑥ⓑ 같은 id의 짧은 시험 질문이 없음")
            elif "ingredient" in q:
                if s["value"] != q["ingredient"]:
                    problems.append(f"{q['id']} ⑥ⓒ ingredient {q['ingredient']}가 짧은 시험 value {s['value']}와 다름")
                if s["target"] != q.get("target"):
                    problems.append(f"{q['id']} ⑥ⓒ target {q.get('target')}이 짧은 시험 target {s['target']}과 다름")
        for sid in short:
            if sid not in ids:
                problems.append(f"{sid} ⑥ⓓ 짧은 시험 질문이 정식 질문에 없음")
    return len(qs), problems


def main():
    args = sys.argv[1:]
    short_test = None
    if "--short-test" in args:
        i = args.index("--short-test")
        short_test = args[i + 1]
        del args[i:i + 2]
    n, problems = find_problems(Path(args[0]), short_test)
    for p in problems:
        print(p)
    print(f"질문 {n}개, 걸린 것 {len(problems)}개")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
