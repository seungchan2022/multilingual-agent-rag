"""후보 고르기 실험(이슈 #6)의 질문 파일을 검사한다.

  .venv/bin/python src/domain_select/check_questions.py <후보 폴더>

<후보 폴더>/questions.json의 질문마다 본다(규칙은 decisions/stage2.md의 2026-10-19 줄들).
  ① 근거 글(evidence_quotes)이 <후보 폴더>/md/<문서>.md에 글자 그대로 있다
  ② 계산식(calc)을 다시 계산하면 value와 0.1% 안에서 같다
  ③ 정답(answer)의 숫자가 value와 ±1% 안이다(채점 규칙과 같은 폭)
  ④ 계산식에 연산이 두 개 이상이다
  ⑤ 계산식에 단위 바꾸기가 있다: 1000(g과 kg, cm³와 L) 또는 273.15(K와 °C)
걸린 것은 질문 번호와 함께 모두 출력하고 종료 코드 1로 끝낸다.
"""
import ast, json, re, sys
from pathlib import Path

UNIT = ("1000", "273.15")


def evaluate(expr):
    """숫자와 + - * / 괄호만 있는 식을 계산하고 연산의 수를 함께 돌려준다."""
    ops = 0

    def ev(n):
        nonlocal ops
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            ops += 1
            a, b = ev(n.left), ev(n.right)
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b else float("nan")}[type(n.op)]
        raise ValueError(f"계산식에 쓸 수 없는 것: {ast.dump(n)}")

    return ev(ast.parse(expr, mode="eval")), ops


def first_number(s):
    m = re.search(r"-?\d+(?:\.\d+)?", s.replace(",", ""))
    return float(m.group()) if m else None


def main():
    folder = Path(sys.argv[1])
    qs = json.loads((folder / "questions.json").read_text(encoding="utf-8"))
    problems = []
    for q in qs:
        for e in q["evidence_quotes"]:
            md = folder / "md" / f"{e['doc']}.md"
            if not md.exists():
                problems.append(f"{q['id']} ① 문서가 없음: {e['doc']}")
            elif e["quote"] not in md.read_text(encoding="utf-8"):
                problems.append(f"{q['id']} ① 근거 글이 {e['doc']} 문서에 그대로 없음: {e['quote']}")
        got, ops = evaluate(q["calc"])
        if abs(got - q["value"]) > abs(q["value"]) * 0.001:
            problems.append(f"{q['id']} ② 계산식 {q['calc']} = {got}, value {q['value']}와 다름")
        a = first_number(q["answer"])
        if a is None or abs(a - q["value"]) > abs(q["value"]) * 0.01:
            problems.append(f"{q['id']} ③ 정답 {q['answer']}의 숫자가 value {q['value']}와 ±1% 밖")
        if ops < 2:
            problems.append(f"{q['id']} ④ 계산식의 연산이 {ops}개")
        if not any(u in q["calc"] for u in UNIT):
            problems.append(f"{q['id']} ⑤ 계산식에 단위 바꾸기(1000, 273.15)가 없음")
    for p in problems:
        print(p)
    print(f"질문 {len(qs)}개, 걸린 것 {len(problems)}개")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
