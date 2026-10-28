"""1단계 고리를 LangGraph 그래프로 만든다(이슈 #14): 생성(검색 계획 쓰기) → 검색 → 답.

규칙은 decisions/stage6.md의 2026-10-26 줄(1단계 고리의 칸이 맡는 일 / 1단계 고리부터 LangGraph로 짠다 / 청크 합치기 / 모델 답의 꼴 검사)과
2026-10-27 줄(저지먼트·리파이먼트를 뺀다 / 시간 기록)에 있다.
칸(node)은 전체 그림의 칸 이름을 영어로 쓴 generate, search, answer다.
  시작 → generate → (꼴 오류면 끝) → search → answer → 끝
저지먼트(계획 검사)와 리파이먼트(계획 고치기)는 190번을 재 보고 뺐다(결정 줄 "저지먼트·리파이먼트를 뺀다"). 생성이 처음 쓴 계획으로 바로 search한다.
generate는 계획 쓰기(요청 한 번)이고, 사용자 메시지는 질문 글, 시스템 메시지는 PLAN_SYSTEM이다.
모델 요청은 src/minimal/generate.py의 send(계획 쓰기 plan.plan_body)와 chat(답 쓰기)으로 보낸다. LangChain의 모델 연결은 쓰지 않는다.
계획이 꼴 검사(plan.py)에 걸리면 그 실행만 search 전에 멈추고(그래프가 끝으로 감) 까닭과 요청·원문을 shape_error에 남긴다. 처리는 만들지 않았다.
시간 기록: 모든 칸은 timed로 감싸서 붙인다. node_times에 지나간 순서대로 칸 이름과 실행 시작부터 잰 시작·끝(초, 소수 셋째 자리)이 남는다.
모델 요청마다의 읽기·쓰기·모델 올리기 시간은 reply_fields가 요청 기록에 넣는다(send가 돌려준다).
"""
import sys
import time
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
import answer  # noqa: E402
import generate  # noqa: E402
import merge  # noqa: E402
import plan  # noqa: E402


class State(TypedDict):
    question: dict
    seed: int
    started_at: float          # 실행 시작 시각(time.perf_counter()). 칸 시간을 재는 데만 쓰고 기록에는 쓰지 않는다
    node_times: list           # 지나간 칸마다 {"node", "start", "end"}. start·end는 실행 시작부터 잰 초
    plan_step: dict | None     # 계획 요청 하나의 기록
    plan: dict | None          # 꼴 검사를 통과한 계획
    shape_error: dict | None
    search: dict | None        # 청크 합치기 기록
    merged_found: list | None  # 합친 청크(search 결과 줄). 답 쓰기에 넘기며 기록에는 쓰지 않는다
    answer: dict | None


def initial_state(question, seed):
    return {"question": question, "seed": seed, "started_at": time.perf_counter(), "node_times": [], "plan_step": None, "plan": None,
            "shape_error": None, "search": None, "merged_found": None, "answer": None}


def timed(name, fn):
    """칸 fn을 감싸 칸이 도는 동안의 시작·끝을 node_times에 더한다. 그래프에 칸을 붙일 때는 모두 이것을 지나간다."""
    def wrapped(state):
        start = time.perf_counter() - state["started_at"]
        update = fn(state)
        end = time.perf_counter() - state["started_at"]
        return {**update, "node_times": state["node_times"] + [{"node": name, "start": round(start, 3), "end": round(end, 3)}]}
    return wrapped


def ask(label, send, *args):
    """요청 하나를 보낸다. Ollama 오류(RuntimeError)는 어느 칸의 요청이었는지 붙여 다시 던진다."""
    try:
        return send(*args)
    except RuntimeError as e:
        raise RuntimeError(f"{label}에서 멈춤: {e}") from e


def reply_fields(output, seconds, tokens, prompt_tokens, abort_reason, times):
    return {"output": output, "gen_seconds": seconds, "gen_tokens": tokens, "prompt_tokens": prompt_tokens,
            "aborted": abort_reason is not None, "abort_reason": abort_reason, **times}


def answer_of(question, found, seed, label="answer"):
    """합친 청크로 최소판과 같은 답 쓰기를 하고 채점 칸을 만든다. 시스템·사용자 메시지, 원문, graded의 칸, 시간, 토큰, 끊김."""
    system_message, user_message = generate.messages_of("minimal", question, found)
    reply = ask(label, generate.chat, system_message, user_message, seed)
    return {"system_message": system_message, "user_message": user_message, **reply_fields(*reply), **generate.graded(question, reply[0])}


def cite_answer_of(version, question, found, seed, hit_ranks, label="answer"):
    """합친 청크로 근거 칸이 있는 답 쓰기(answer.py의 지시문 판 version)를 하고 기록을 만든다. 요청은 generate.send로 보내고 format만 틀이다."""
    system_message, user_message = answer.messages_of(version, question, found)
    reply = ask(label, generate.send, answer.request_body(system_message, user_message, seed, len(found)))
    return answer.record_of(question, found, hit_ranks, system_message, user_message, reply_fields(*reply))


def shape_error_of(stage, index, problems, body, output):
    """꼴 오류 기록: 어느 칸(generate)의 몇 번째 요청인지, 까닭 목록, 그 요청의 시스템·사용자 메시지·모델·설정, 받은 원문."""
    system_message, user_message = (m["content"] for m in body["messages"])
    return {"stage": stage, "index": index, "problems": problems, "system_message": system_message, "user_message": user_message,
            "model": body["model"], "options": body["options"], "output": output}


def build(conn, model, answer_version=None):
    """conn(데이터베이스 연결)과 model(임베딩 모델)을 쥐고 1단계 고리 그래프를 만들어 컴파일해 돌려준다.
    answer_version이 None이면 답 쓰기는 최소판(answer_of)이고, 판 이름(answer.SYSTEMS의 키)을 주면 근거 칸이 있는 답 쓰기(cite_answer_of)다.
    graph.invoke(initial_state(질문, 씨앗))이 실행 하나를 돌려 마지막 상태를 돌려준다."""

    def generate_node(state):
        question, seed = state["question"], state["seed"]
        user_message = question["question"]
        body = plan.plan_body(user_message, seed)
        reply = ask("generate", generate.send, body)
        parsed, problems = plan.check_plan(reply[0])
        update = {"plan_step": {"user_message": user_message, **reply_fields(*reply), "plan": parsed, "problems": problems}}
        if problems:
            update["shape_error"] = shape_error_of("generate", 1, problems, body, reply[0])
        else:
            update["plan"] = parsed
        return update

    def search_node(state):
        final = state["plan"]
        record, found = merge.merge_search(conn, model, state["question"],
                                           [("korean", final["korean_question"]), ("english", final["english_question"])])
        return {"search": record, "merged_found": found}

    def answer_node(state):
        if answer_version is None:
            return {"answer": answer_of(state["question"], state["merged_found"], state["seed"])}
        return {"answer": cite_answer_of(answer_version, state["question"], state["merged_found"], state["seed"], state["search"]["hit_ranks"])}

    def after_generate(state):
        return END if state["shape_error"] else "search"

    graph = StateGraph(State)
    for name, node in (("generate", generate_node), ("search", search_node), ("answer", answer_node)):
        graph.add_node(name, timed(name, node))
    graph.add_edge(START, "generate")
    graph.add_conditional_edges("generate", after_generate, {"search": "search", END: END})
    graph.add_edge("search", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
