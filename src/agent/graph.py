"""1단계 고리를 LangGraph 그래프로 만든다(이슈 #14): 생성(검색 계획 쓰기) → 저지먼트(계획 검사) → 리파이먼트(문제를 모아 생성으로) → 검색 → 답.

규칙은 decisions/stage6.md의 2026-10-26 줄(1단계 고리의 칸이 맡는 일 / 1단계 고리부터 LangGraph로 짠다 / 1단계 고리의 반복 한도 /
청크 합치기 / 모델 답의 꼴 검사 / 1단계 고리의 사용자 메시지 모양과 판정 모델 설정)에 있다.
칸(node)은 전체 그림의 칸 이름을 영어로 쓴 generate, judgment, refinement, search, answer다.
  시작 → generate → (꼴 오류면 끝) → judgment → (꼴 오류면 끝) → 통과 또는 3번째 검사면 search, 아니면 refinement → generate
  search → answer → 끝
generate는 계획 쓰기(요청 한 번)이고, 사용자 메시지로 리파이먼트가 만든 글이 있으면 그것을, 없으면 질문 글을 쓴다. 시스템 메시지는 늘 PLAN_SYSTEM이다.
judgment는 판정 모델(gemma3:4b)에게 계획을 검사시키고, 통과는 코드가 정한다(세 칸이 모두 true). refinement는 모델을 부르지 않고 코드가
앞 계획·떨어진 검사 이름·판정 모델이 적은 문제를 모아 다시 쓰기 메시지를 만든다. 검사는 최대 3번, 다시 쓰기는 최대 2번이고,
3번째 검사에서도 떨어지면 마지막 계획 그대로 search로 가며 plan_passed가 false로 남는다.
모델 요청은 src/minimal/generate.py의 send(계획 쓰기 plan.plan_body, 판정 plan.judge_body)와 chat(답 쓰기)으로 보낸다. LangChain의 모델 연결은 쓰지 않는다.
계획이나 판정이 꼴 검사(plan.py)에 걸리면 그 실행만 search 전에 멈추고(그래프가 끝으로 감) 까닭과 요청·원문을 shape_error에 남긴다. 처리는 만들지 않았다.
"""
import sys
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
import generate  # noqa: E402
import merge  # noqa: E402
import plan  # noqa: E402


class State(TypedDict):
    question: dict
    seed: int
    user_message: str | None   # 리파이먼트가 만든 다시 쓰기 메시지. 없으면(None) generate가 질문 글을 쓴다
    plan: dict | None          # 가장 최근에 꼴 검사를 통과한 계획
    first_plan: dict | None
    plan_steps: list           # 계획 요청마다(처음·다시 쓰기)의 기록
    judgments: list            # 판정마다의 기록
    n_judgments: int
    n_refinements: int
    plan_passed: bool | None   # 가장 최근 판정에서 통과했는지. 판정 전에는 None
    shape_error: dict | None
    search: dict | None        # 청크 합치기 기록
    merged_found: list | None  # 합친 청크(search 결과 줄). 답 쓰기에 넘기며 기록에는 쓰지 않는다
    answer: dict | None


def initial_state(question, seed):
    return {"question": question, "seed": seed, "user_message": None, "plan": None, "first_plan": None, "plan_steps": [], "judgments": [],
            "n_judgments": 0, "n_refinements": 0, "plan_passed": None, "shape_error": None, "search": None, "merged_found": None, "answer": None}


def ask(label, send, *args):
    """요청 하나를 보낸다. Ollama 오류(RuntimeError)는 어느 칸의 몇 번째 요청이었는지 붙여 다시 던진다."""
    try:
        return send(*args)
    except RuntimeError as e:
        raise RuntimeError(f"{label}에서 멈춤: {e}") from e


def reply_fields(output, seconds, tokens, prompt_tokens, abort_reason):
    return {"output": output, "gen_seconds": seconds, "gen_tokens": tokens, "prompt_tokens": prompt_tokens,
            "aborted": abort_reason is not None, "abort_reason": abort_reason}


def answer_of(question, found, seed, label="answer"):
    """합친 청크로 최소판과 같은 답 쓰기를 하고 채점 칸을 만든다. 시스템·사용자 메시지, 원문, graded의 칸, 시간, 토큰, 끊김."""
    system_message, user_message = generate.messages_of("minimal", question, found)
    reply = ask(label, generate.chat, system_message, user_message, seed)
    return {"system_message": system_message, "user_message": user_message, **reply_fields(*reply), **generate.graded(question, reply[0])}


def shape_error_of(stage, index, problems, body, output):
    """꼴 오류 기록: 어느 칸(generate/judgment)의 몇 번째 요청인지, 까닭 목록, 그 요청의 시스템·사용자 메시지·모델·설정, 받은 원문."""
    system_message, user_message = (m["content"] for m in body["messages"])
    return {"stage": stage, "index": index, "problems": problems, "system_message": system_message, "user_message": user_message,
            "model": body["model"], "options": body["options"], "output": output}


def build(conn, model):
    """conn(데이터베이스 연결)과 model(임베딩 모델)을 쥐고 1단계 고리 그래프를 만들어 컴파일해 돌려준다.
    graph.invoke(initial_state(질문, 씨앗))이 실행 하나를 돌려 마지막 상태를 돌려준다."""

    def generate_node(state):
        question, seed = state["question"], state["seed"]
        user_message = state["user_message"] or question["question"]
        n = len(state["plan_steps"]) + 1
        body = plan.plan_body(user_message, seed)
        reply = ask(f"generate {n}번째 요청", generate.send, body)
        parsed, problems = plan.check_plan(reply[0])
        step = {"user_message": user_message, **reply_fields(*reply), "plan": parsed, "problems": problems}
        update = {"plan_steps": state["plan_steps"] + [step]}
        if problems:
            update["shape_error"] = shape_error_of("generate", n, problems, body, reply[0])
        else:
            update["plan"] = parsed
            if state["first_plan"] is None:
                update["first_plan"] = parsed
        return update

    def judgment_node(state):
        question, seed = state["question"], state["seed"]
        user_message = plan.judge_user_message(question["question"], state["plan"])
        body = plan.judge_body(user_message, seed)
        n = len(state["judgments"]) + 1
        reply = ask(f"judgment {n}번째 요청", generate.send, body)
        parsed, problems = plan.check_judgment(reply[0])
        passed = None if problems else plan.passed(parsed)
        step = {"user_message": user_message, **reply_fields(*reply), "judgment": parsed, "problems": problems, "passed": passed}
        update = {"judgments": state["judgments"] + [step], "n_judgments": n}
        if problems:
            update["shape_error"] = shape_error_of("judgment", n, problems, body, reply[0])
        else:
            update["plan_passed"] = passed
        return update

    def refinement_node(state):
        judgment = state["judgments"][-1]["judgment"]
        return {"n_refinements": state["n_refinements"] + 1,
                "user_message": plan.refine_user_message(state["question"]["question"], state["plan"], judgment)}

    def search_node(state):
        final = state["plan"]
        record, found = merge.merge_search(conn, model, state["question"],
                                           [("korean", final["korean_question"]), ("english", final["english_question"])])
        return {"search": record, "merged_found": found}

    def answer_node(state):
        return {"answer": answer_of(state["question"], state["merged_found"], state["seed"])}

    def after_generate(state):
        return END if state["shape_error"] else "judgment"

    def after_judgment(state):
        if state["shape_error"]:
            return END
        if state["plan_passed"] or state["n_judgments"] >= plan.MAX_JUDGMENTS:
            return "search"
        return "refinement"

    graph = StateGraph(State)
    for name, node in (("generate", generate_node), ("judgment", judgment_node), ("refinement", refinement_node),
                       ("search", search_node), ("answer", answer_node)):
        graph.add_node(name, node)
    graph.add_edge(START, "generate")
    graph.add_conditional_edges("generate", after_generate, {"judgment": "judgment", END: END})
    graph.add_conditional_edges("judgment", after_judgment, {"search": "search", "refinement": "refinement", END: END})
    graph.add_edge("refinement", "generate")
    graph.add_edge("search", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
