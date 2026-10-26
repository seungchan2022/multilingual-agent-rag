"""1단계 고리(검색 계획 쓰기 → 계획 검사 → 계획 다시 쓰기 → 청크 합치기 → 답)로 질문 38개를 씨앗 1~5로 돌려 실행 기록을 남기는 프로그램(이슈 #14).

  .venv/bin/python src/agent/run.py     # 38 × 5 = 190번 → data/agent/plan_search/runs.jsonl
  .venv/bin/python src/agent/run.py --questions q01-ko,q03-en --seeds 1 --out <경로>     # 짧은 확인용

규칙은 decisions/stage6.md의 2026-10-26 줄(재는 법의 첫째 / 비교용이 넘기는 청크 수를 실행마다 맞춘다 / 남길 기준의 둘 / 모델 답의 꼴 검사 /
리파이먼트가 일어난 실행에서는 처음 계획으로도 답을 써 둔다 / 1단계 고리의 사용자 메시지 모양과 판정 모델 설정)에 있다. 그래프는 src/agent/graph.py다.
모델 설정은 생성 모델(qwen3:8b)의 답 쓰기가 src/minimal/generate.py의 request_body와 같고 계획 쓰기는 온도만 0인 plan.plan_body이며, 판정 모델(gemma3:4b)은 src/agent/plan.py의 judge_body다. 씨앗은 그 실행의 씨앗이다.
실행 시작 때 두 모델을 메모리에서 내리고 몸풀기 호출을 모델마다 한 번 한다. 몸풀기는 기록하지 않는다.
순서는 씨앗(1 → 5) → 질문(파일 순서)이고, 요청은 한 번에 하나씩 보내며 줄마다 바로 써서 flush한다.
시스템의 흐름 밖에서 이 파일이 덧붙이는 것(그래프에는 넣지 않았다): ① 원래 질문으로 k = 16 검색한 비교용 재료(comparison_retrieved)
② 다시 쓰기가 한 번이라도 일어난 실행에서만, 처음 계획의 두 판으로 같은 청크 합치기를 하고 그 청크로 같은 답 쓰기를 해 채점한 것(first_plan_search, first_plan_answer).
①②는 시스템의 검색과 답이 아니다. 꼴 오류로 멈춘 실행은 ①②도 하지 않는다. 다른 실행은 이어 간다.
Ollama의 그 밖의 오류(token repeat limit이 아닌 error, HTTP 오류)는 어느 씨앗·질문·칸이었는지와 함께 RuntimeError로 전체 실행을 멈춘다.
기록 파일이 이미 있으면 덮어쓰지 않고 멈춘다. --questions나 --seeds를 주면 --out이 반드시 있어야 하고, 기본 경로에는 쓰지 못한다.
"""
import argparse
import json
import sys
import time
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402
import graph  # noqa: E402
import merge  # noqa: E402
import plan  # noqa: E402
from index import DSN, QUESTIONS, ROOT, load_model  # noqa: E402

OUT_DIR = ROOT / "data" / "agent" / "plan_search"
RUNS = OUT_DIR / "runs.jsonl"
SEEDS = generate.SEEDS
WARMUP_SEED = 1
PROMPT_VERSION = {"plan": plan.PLAN_VERSION, "judge": plan.JUDGE_VERSION, "refine": plan.REFINE_VERSION, "answer": generate.PROMPT_VERSION["minimal"]}


def warm_up():
    """두 모델을 메모리에서 내리고 몸풀기 호출을 모델마다 한 번 한다. 결과는 쓰지 않는다."""
    generate.unload_model()
    generate.unload_model(plan.JUDGE_MODEL)
    print("두 모델을 메모리에서 내리고 시작한다(몸풀기 호출 모델마다 한 번, 기록하지 않음)", flush=True)
    generate.send(plan.plan_body(generate.WARMUP_USER, WARMUP_SEED))
    body = plan.judge_body(generate.WARMUP_USER, WARMUP_SEED)
    generate.send(body)


def run_one(compiled, conn, model, question, seed):
    """실행 하나. 그래프를 돌린 마지막 상태에, 꼴 오류가 없으면 비교용 재료와(다시 쓰기가 있었다면) 처음 계획의 검색·답을 덧붙여 (상태, 덧붙인 칸)을 돌려준다."""
    state = compiled.invoke(graph.initial_state(question, seed))
    extra = {"comparison_retrieved": None, "first_plan_search": None, "first_plan_answer": None}
    if state["shape_error"]:
        return state, extra
    extra["comparison_retrieved"] = merge.comparison_retrieved(conn, model, question)
    if state["n_refinements"] > 0:
        first = state["first_plan"]
        record, found = merge.merge_search(conn, model, question, [("korean", first["korean_question"]), ("english", first["english_question"])])
        extra["first_plan_search"] = record
        extra["first_plan_answer"] = {**graph.answer_of(question, found, seed, label="first_plan_answer"), "system_answer": False}
    return state, extra


def run(questions, path, conn, model, seeds=SEEDS):
    """몸풀기 뒤에 씨앗 → 질문 순서로 하나씩 돌려 한 줄씩 path에 쓴다. 쓴 줄 수를 돌려준다."""
    generate.check_new(path)
    commit, dirty = generate.git_state()
    run_id = time.strftime("%Y%m%dT%H%M%S")
    path.parent.mkdir(parents=True, exist_ok=True)
    compiled = graph.build(conn, model)
    warm_up()
    n = 0
    with open(path, "x", encoding="utf-8") as out:
        for seed in seeds:
            for q in questions:
                try:
                    state, extra = run_one(compiled, conn, model, q, seed)
                except RuntimeError as e:
                    raise RuntimeError(f'씨앗{seed} {q["id"]}에서 멈춤: {e}') from e
                error = state["shape_error"]
                row = {"run_id": run_id, "question_id": q["id"], "lang": q["lang"], "branch": q["branch"], "seed": seed,
                       "generate_model": generate.MODEL, "plan_options": plan.plan_body("", seed)["options"],
                       "answer_options": generate.request_body("", "", seed)["options"],
                       "judge_model": plan.JUDGE_MODEL, "judge_options": plan.judge_body("", seed)["options"],
                       "prompt_version": PROMPT_VERSION, "code_commit": commit, "code_dirty": dirty, "langgraph_version": version("langgraph"),
                       "plan_steps": state["plan_steps"], "judgments": state["judgments"],
                       "first_plan": state["first_plan"], "final_plan": None if error else state["plan"],
                       "n_judgments": state["n_judgments"], "n_refinements": state["n_refinements"], "plan_passed": state["plan_passed"],
                       "shape_error": error, "search": state["search"], **extra, "answer": state["answer"]}
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()
                n += 1
                if error:
                    print(f'씨앗{seed} {q["id"]} 꼴 오류({error["stage"]} {error["index"]}번째): {"; ".join(error["problems"])}', flush=True)
                else:
                    print(f'씨앗{seed} {q["id"]} 판정 {row["n_judgments"]}번 통과 {"예" if row["plan_passed"] else "아니오"} '
                          f'청크 {row["search"]["n_chunks"]}개 근거 {"찾음" if row["search"]["hit"] else "못 찾음"} '
                          f'{"맞음" if row["answer"]["correct"] else "틀림"}', flush=True)
    return n


def main(argv=None):
    parser = argparse.ArgumentParser(description="1단계 고리로 질문 38개를 씨앗 1~5로 돌려 실행 기록을 남긴다")
    parser.add_argument("--questions", help="돌릴 질문 ID를 쉼표로 이은 것(짧은 확인용). 주면 --out이 필요하다")
    parser.add_argument("--seeds", help="돌릴 씨앗을 쉼표로 이은 것(짧은 확인용). 주면 --out이 필요하다")
    parser.add_argument("--out", type=Path, help="기록 파일 경로(기본 data/agent/plan_search/runs.jsonl). 기본 경로에는 전체 190번만 쓴다")
    args = parser.parse_args(argv)
    partial = args.questions is not None or args.seeds is not None
    if partial and args.out is None:
        parser.error("--questions나 --seeds를 주면 --out을 반드시 함께 줘야 한다(짧은 확인이 기본 경로 runs.jsonl에 쓰이지 않게)")
    path = args.out or RUNS
    if partial and path.resolve() == RUNS.resolve():
        parser.error("--questions나 --seeds를 준 짧은 확인은 기본 경로 runs.jsonl에 쓰지 못한다")
    generate.check_new(path)
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    if args.questions is not None:
        wanted = args.questions.split(",")
        unknown = [qid for qid in wanted if qid not in {q["id"] for q in questions}]
        if unknown:
            parser.error(f"질문 파일에 없는 질문 ID: {unknown}")
        questions = [q for q in questions if q["id"] in wanted]
    seeds = SEEDS
    if args.seeds is not None:
        seeds = tuple(int(s) for s in args.seeds.split(","))
        if any(s not in SEEDS for s in seeds):
            parser.error(f"씨앗은 {SEEDS} 가운데서만 고른다: {seeds}")
    import psycopg
    model = load_model(generate.EMBED_MODEL)
    with psycopg.connect(DSN) as conn:
        n = run(questions, path, conn, model, seeds=seeds)
    print(f"\n{n}줄 씀: {path}")


if __name__ == "__main__":
    main()
