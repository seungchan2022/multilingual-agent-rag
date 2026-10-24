"""실행 기록의 answer 글을 채점하는 규칙: 숫자 꺼내기, 맞음, 단위 확인.

숫자와 맞음은 도메인 고르기 실험의 규칙(src/domain_select/run.py의 numbers_of, grade_record)과 같다: answer에서 쉼표를 지우고
숫자를 모두 꺼내, 마지막 숫자가 정답 값의 ±1% 안이면 맞음이다. 하나만 더했다: 숫자 바로 뒤에 붙은 괄호 안 정수(오차 표기, 예: 621.4(11))는
숫자로 세지 않는다. 괄호 앞에 빈칸이 있으면(621.4 (11)) 센다. 단위 확인은 맞음·틀림을 바꾸지 않고 따로 알려 주기만 한다.
"""
import re

NUMBER = re.compile(r"(-?\d+(?:\.\d+)?)(?:\(\d+\))?")   # 뒤의 괄호 묶음은 꺼내는 숫자에 넣지 않고 지나간다
UNIT_WORD = re.compile(r"\s*([A-Za-z가-힣]+)")
TOLERANCE = 0.01
# 같은 단위로 보는 표기(로마자는 소문자로 견준다). 질문의 unit이 든 묶음이 그 질문의 단위다.
UNIT_GROUPS = [{"kg", "킬로그램", "kilogram", "kilograms"}, {"kev"}, {"분", "min", "mins", "minute", "minutes"},
               {"초", "s", "sec", "secs", "second", "seconds"}, {"일", "day", "days"}, {"개월", "달", "month", "months"}]


def scan(answer):
    """(쉼표를 지운 글, [(숫자, 그 숫자와 뒤에 붙은 괄호 묶음이 끝나는 자리), …])."""
    text = str(answer).replace(",", "")
    return text, [(float(m.group(1)), m.end()) for m in NUMBER.finditer(text)]


def numbers_of(answer):
    """answer에서 쉼표를 지우고 숫자를 모두 뽑는다. 숫자 바로 뒤에 붙은 괄호 안 정수는 세지 않는다."""
    return [value for value, _ in scan(answer)[1]]


def grade(question, answer):
    """마지막 숫자가 정답 값의 ±1% 안이면 맞음. {numbers, picked, correct}."""
    numbers = numbers_of(answer)
    picked = numbers[-1] if numbers else None
    value = question["value"]
    return {"numbers": numbers, "picked": picked, "correct": picked is not None and abs(picked - value) <= abs(value) * TOLERANCE}


def unit_check(question, answer):
    """고른 숫자(마지막 숫자) 바로 뒤(빈칸 0개 이상)의 글자 덩어리를 단위로 읽어 질문의 unit과 같은 단위인지 본다.
    덩어리가 같은 단위 표기 가운데 하나로 시작하면 '같음', 아니면 '다름', 숫자나 덩어리가 없으면 '없음'."""
    text, found = scan(answer)
    if not found:
        return "없음"
    word = UNIT_WORD.match(text, found[-1][1])
    if not word:
        return "없음"
    unit = question["unit"].lower()
    group = next((g for g in UNIT_GROUPS if unit in g), None)
    if group is None:
        raise ValueError(f"{question['id']}: 단위 {question['unit']!r}가 같은 단위 표기 목록에 없다")
    return "같음" if any(word.group(1).lower().startswith(alias) for alias in group) else "다름"
