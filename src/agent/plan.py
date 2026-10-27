"""검색 계획 쓰기의 요청 글과 요청 본문, 모델 답의 꼴 검사(이슈 #14).

규칙은 decisions/stage6.md의 2026-10-26 줄(검색 계획의 칸과 요청 글 / 계획 요청 글에 reason을 더하고 계획 검사의 기준과 요청 글을 정한다 /
모델 답의 꼴 검사)과 2026-10-27 줄(계획 쓰기의 온도 / 저지먼트·리파이먼트를 뺀다)에 있다.
요청 글(PLAN_SYSTEM)은 결정 줄에 적힌 전문과 글자가 같다. 한 글자도 바꾸지 않는다(test_plan.py가 전문을 따로 적어 견준다).
저지먼트·리파이먼트를 뺐으므로 판정 요청 글(JUDGE_SYSTEM)과 고치기 요청 글, 판정 코드는 이 파일에 없다. 그 요청 글의 전문은 decisions/stage6.md에 그대로 남아 있다.
이 파일은 모델을 부르지 않는다. 요청은 src/minimal/generate.py의 send로 보낸다.
계획 쓰기의 설정은 답 쓰기(generate.request_body)와 같고 온도만 0이다(decisions/stage6.md 2026-10-27 "계획 쓰기의 온도" 줄).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
import generate  # noqa: E402

PLAN_VERSION = "plan-en-v1"

PLAN_SYSTEM = "\n".join([
    "You prepare a document search for the question. Do not answer the question.",
    "Answer only in the JSON format below.",
    '{"reason": "...", "targets": [{"fact": "...", "condition": "...", "unit": "..."}], "korean_question": "...", "english_question": "..."}',
    "reason: before the plan, write how you found the facts to look up and anything that was hard to translate.",
    "targets: every fact that must be looked up in documents to answer the question, one item per fact. Write them in the language of the question.",
    "fact: the fact to look up.",
    'condition: conditions attached to that fact, such as time, place, or state. Write "" if there are none.',
    'unit: the unit of that fact. Write "" if there is none.',
    "korean_question: the whole question written in Korean. If the question is already in Korean, copy it as it is.",
    "english_question: the whole question written in English. If the question is already in English, copy it as it is.",
    "For korean_question and english_question: write common words such as element names in that language. "
    "Keep numbers, symbols, abbreviations, units, and names of people and organizations as they are. Do not add, drop, shorten, or answer anything.",
])


def plan_body(user_message, seed):
    """계획 쓰기의 요청 본문. 답 쓰기의 설정에서 온도만 0으로 바꾼다. 옮겨 쓰기에 무작위성이 들면 드문 글자가 깨졌다."""
    body = generate.request_body(PLAN_SYSTEM, user_message, seed)
    body["options"]["temperature"] = 0
    return body


def parse_object(output):
    """(읽은 객체, 어긋난 까닭 목록). JSON으로 읽히지 않거나 객체(dict)가 아니면 객체는 None이다."""
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as e:
        return None, [f"JSON으로 읽히지 않음: {e}"]
    if not isinstance(parsed, dict):
        return None, [f"JSON 객체가 아님: {type(parsed).__name__}"]
    return parsed, []


def check_plan(output):
    """계획 꼴 검사. (읽은 계획 또는 None, 어긋난 까닭 목록). 빈 목록이면 통과다.
    reason·korean_question·english_question이 글자이고 두 판은 빈칸만이 아니다. targets는 항목이 하나 이상인 목록이고,
    항목마다 객체이며 fact(글자, 빈칸만이 아님)·condition(글자)·unit(글자)이 있다."""
    plan, problems = parse_object(output)
    if plan is None:
        return None, problems
    for key in ("reason", "korean_question", "english_question"):
        if not isinstance(plan.get(key), str):
            problems.append(f"{key}가 없거나 글자가 아님")
    for key in ("korean_question", "english_question"):
        if isinstance(plan.get(key), str) and plan[key].strip() == "":
            problems.append(f"{key}가 빈칸뿐임")
    targets = plan.get("targets")
    if not isinstance(targets, list) or not targets:
        problems.append("targets가 없거나 항목이 하나 이상인 목록이 아님")
    else:
        for i, item in enumerate(targets):
            if not isinstance(item, dict):
                problems.append(f"targets[{i}]가 객체가 아님")
                continue
            for key in ("fact", "condition", "unit"):
                if not isinstance(item.get(key), str):
                    problems.append(f"targets[{i}].{key}가 없거나 글자가 아님")
            if isinstance(item.get("fact"), str) and item["fact"].strip() == "":
                problems.append(f"targets[{i}].fact가 빈칸뿐임")
    return plan, problems
