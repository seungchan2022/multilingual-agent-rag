"""검색 계획 쓰기·계획 검사(판정)·계획 다시 쓰기의 요청 글과 사용자 메시지, 모델 답의 꼴 검사(이슈 #14).

규칙은 decisions/stage6.md의 2026-10-26 줄(검색 계획의 칸과 요청 글 / 계획 요청 글에 reason을 더하고 계획 검사의 기준과 요청 글을 정한다 /
계획 고치기의 요청 글 / 1단계 고리의 사용자 메시지 모양과 판정 모델 설정 / 모델 답의 꼴 검사)에 있다.
요청 글(PLAN_SYSTEM, JUDGE_SYSTEM)은 결정 줄에 적힌 전문과 글자가 같다. 한 글자도 바꾸지 않는다(test_plan.py가 전문을 따로 적어 견준다).
이 파일은 모델을 부르지 않는다. 요청은 src/minimal/generate.py의 chat(생성 모델)과 send(판정 모델)로 보낸다.
"""
import json

JUDGE_MODEL = "gemma3:4b"
MAX_JUDGMENTS = 3   # 계획 검사 최대 3번, 계획 다시 쓰기 최대 2번(decisions/stage6.md 2026-10-26 1단계 고리의 반복 한도)
PLAN_VERSION = "plan-en-v1"
JUDGE_VERSION = "judge-en-v1"
REFINE_VERSION = "refine-en-v1"
CHECKS = ("targets_ok", "korean_ok", "english_ok")

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

JUDGE_SYSTEM = "\n".join([
    "You check a search plan written for a question. Do not answer the question.",
    "The plan has targets (facts to look up, each with a condition and a unit), korean_question, and english_question.",
    "Check three things.",
    "targets_ok: targets include every fact needed to answer the question, and each condition and unit matches the question.",
    "korean_ok: korean_question is written in Korean and asks exactly the same thing as the question: "
    "the same numbers, names, symbols, conditions, and units, with nothing added or dropped.",
    "english_ok: english_question is written in English and asks exactly the same thing as the question, in the same way.",
    "reason: before deciding, compare the plan with the question item by item and write what matches and what differs.",
    "For every check that fails, write one problem: what is wrong and how to fix it.",
    "Answer only in the JSON format below.",
    '{"reason": "...", "targets_ok": true, "korean_ok": true, "english_ok": true, "problems": []}',
])


def plan_json(plan):
    """판정과 다시 쓰기에 넣는 계획 JSON. 생성 모델의 reason과 모델이 더 쓴 칸은 빼고,
    targets(fact, condition, unit) → korean_question → english_question 순서로 새로 만들어 한 줄로 적는다."""
    clean = {"targets": [{"fact": t["fact"], "condition": t["condition"], "unit": t["unit"]} for t in plan["targets"]],
             "korean_question": plan["korean_question"], "english_question": plan["english_question"]}
    return json.dumps(clean, ensure_ascii=False)


def judge_user_message(question_text, plan):
    return "Question:\n" + question_text + "\n\nSearch plan:\n" + plan_json(plan)


def failed_checks(judgment):
    """판정에서 false인 검사 이름(targets_ok, korean_ok, english_ok 순서)."""
    return [name for name in CHECKS if judgment[name] is False]


def refine_user_message(question_text, plan, judgment):
    """계획 다시 쓰기의 사용자 메시지: 질문 글, 앞 계획(reason 뺀 JSON), 떨어진 검사 이름, 판정 모델이 적은 문제 줄들, 다시 쓰라는 글."""
    problems = "\n".join("- " + problem for problem in judgment["problems"])
    return (question_text + "\n\nYour previous plan:\n" + plan_json(plan) + "\nFailed checks: " + ", ".join(failed_checks(judgment))
            + "\nProblems found in the plan:\n" + problems
            + "\nWrite the whole plan again in the same JSON format. Fix every problem. Keep the parts without problems as they are.")


def judge_body(user_message, seed):
    """판정 모델(gemma3:4b)의 요청 본문. 설정을 모두 적어 보낸다(Ollama 기본값이 바뀌어도 같은 요청이 되게). think 칸은 보내지 않는다."""
    options = {"temperature": 0, "top_p": 0.8, "top_k": 20, "min_p": 0, "num_predict": 2048, "num_ctx": 8192, "seed": seed}
    return {"model": JUDGE_MODEL, "messages": [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user_message}],
            "stream": True, "format": "json", "options": options}


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


def check_judgment(output):
    """판정 꼴 검사. (읽은 판정 또는 None, 어긋난 까닭 목록). 빈 목록이면 통과다.
    reason이 글자, targets_ok·korean_ok·english_ok가 참·거짓 값(글자 "true"와 숫자 1은 어긋남), problems가 글자 목록이다.
    셋 가운데 하나라도 false면 problems가 비어 있지 않아야 한다."""
    judgment, problems = parse_object(output)
    if judgment is None:
        return None, problems
    if not isinstance(judgment.get("reason"), str):
        problems.append("reason이 없거나 글자가 아님")
    for name in CHECKS:
        if not isinstance(judgment.get(name), bool):
            problems.append(f"{name}가 없거나 참·거짓 값이 아님")
    listed = judgment.get("problems")
    if not isinstance(listed, list) or not all(isinstance(p, str) for p in listed):
        problems.append("problems가 없거나 글자 목록이 아님")
    elif all(isinstance(judgment.get(name), bool) for name in CHECKS) and not all(judgment[name] for name in CHECKS) and not listed:
        problems.append("검사가 false인데 problems가 비어 있음")
    return judgment, problems


def passed(judgment):
    """판정 통과는 코드가 정한다: 세 칸이 모두 true."""
    return all(judgment[name] is True for name in CHECKS)
