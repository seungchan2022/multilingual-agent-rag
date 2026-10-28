"""⑧ 기록의 청크로 답 쓰기만 다시 돌려 근거 칸이 있는 답(판 1·판 2)의 실행 기록을 남기는 프로그램(이슈 #15).

  .venv/bin/python src/agent/run_answer.py --version cite-en-v1     # 190번 → data/agent/answer_cite/runs_v1.jsonl
  .venv/bin/python src/agent/run_answer.py --version cite-en-v2     # 190번 → data/agent/answer_cite/runs_v2.jsonl
  .venv/bin/python src/agent/run_answer.py --version cite-en-v1 --check-only     # 참고 글 대조만 하고 모델은 부르지 않음
  .venv/bin/python src/agent/run_answer.py --version cite-en-v1 --questions q01-ko --seeds 1 --out <경로>     # 짧은 확인용

규칙은 decisions/stage6.md의 2026-10-28 줄(④의 실행 방법과 기록 경로 / 판 0 고르기 / 지시문 두 판 / 근거 칸의 공통 검사)과
2026-10-27 줄(시간 기록)에 있다. 계획 쓰기와 검색은 다시 하지 않는다. ⑧ 기록(data/agent/plan_search/runs.jsonl)의 줄마다 판 0의 청크 목록을
데이터베이스(chunks 표)에서 순위대로 가져와 답 쓰기만 다시 돌린다. ⑧ 기록과 ⑧ 프로그램(run.py, graph.build의 기본 동작)은 바꾸지 않는다.
판 0: 줄에 first_plan_search가 있으면 first_plan_search·first_plan_answer(base_kind "first_plan"), 없으면 search·answer(base_kind "final").
돌리기 전에 ⑧ 기록이 190줄이고 모든 줄의 code_commit이 369d74d로 시작하며 code_dirty가 false인지, 다시 만든 참고 글이 판 0 답의 system_message와
글자까지 같은지 본다. 하나라도 어긋나면 모델을 부르기 전에 멈춘다.
돌리는 순서는 ⑧ 기록의 줄 순서(씨앗 1 → 5, 질문 파일 순서)이고, 요청은 한 번에 하나씩 보내며 줄마다 바로 써서 flush한다.
시작 때 생성 모델을 메모리에서 내리고 몸풀기 호출을 한 번 한다. 몸풀기는 기록하지 않는다.
Ollama의 그 밖의 오류(token repeat limit이 아닌 error, HTTP 오류)는 어느 씨앗·질문이었는지와 함께 RuntimeError로 멈춘다.
기록 파일이 이미 있으면 덮어쓰지 않고 멈춘다. --questions나 --seeds를 주면 --out이 반드시 있어야 하고, 기본 경로에는 쓰지 못한다.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import answer  # noqa: E402
import generate  # noqa: E402
import graph  # noqa: E402
from index import DSN, QUESTIONS, ROOT  # noqa: E402

BASE_RUNS = ROOT / "data" / "agent" / "plan_search" / "runs.jsonl"
OUT_DIR = ROOT / "data" / "agent" / "answer_cite"
RUNS = {"cite-en-v1": OUT_DIR / "runs_v1.jsonl", "cite-en-v1b": OUT_DIR / "runs_v1b.jsonl", "cite-en-v2": OUT_DIR / "runs_v2.jsonl"}
BASE_ROWS = 190
BASE_COMMIT = "369d74d"
SEEDS = generate.SEEDS
WARMUP_SEED = 1
CHUNK_SQL = "SELECT chunk_id, doc_id, lines, text, tokens, language, line_start, line_end FROM chunks WHERE chunk_set = %s AND chunk_id = ANY(%s)"


def pick_base(row):
    """⑧ 기록의 줄에서 판 0의 (검색 기록, 답, base_kind). first_plan_search가 있으면 처음 계획의 것, 없으면 search·answer."""
    if row.get("first_plan_search") is not None:
        return row["first_plan_search"], row["first_plan_answer"], "first_plan"
    return row["search"], row["answer"], "final"


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def check_base(rows, expected=None):
    """⑧ 기록이 온전한지 본다: 줄 수(기본 BASE_ROWS), code_commit이 369d74d로 시작, code_dirty가 false, 판 0의 검색 기록이 있음. 어긋나면 ValueError."""
    expected = BASE_ROWS if expected is None else expected
    if len(rows) != expected:
        raise ValueError(f"⑧ 기록이 {len(rows)}줄이다({expected}줄이어야 한다)")
    wrong_commit = sorted({r["code_commit"] for r in rows if not r["code_commit"].startswith(BASE_COMMIT)})
    if wrong_commit:
        raise ValueError(f"⑧ 기록의 code_commit이 {BASE_COMMIT}로 시작하지 않는 줄이 있다: {wrong_commit}")
    dirty = [(r["question_id"], r["seed"]) for r in rows if r["code_dirty"]]
    if dirty:
        raise ValueError(f"⑧ 기록에 code_dirty가 true인 줄이 있다: {dirty}")
    no_search = [(r["question_id"], r["seed"]) for r in rows if pick_base(r)[0] is None]
    if no_search:
        raise ValueError(f"⑧ 기록에 판 0의 검색 기록이 없는 줄(꼴 오류 줄)이 있다: {no_search}")


def fetch_chunks(conn, ids):
    """chunks 표에서 chunk_id마다 search 결과 줄 (chunk_id, None, doc_id, lines, text, tokens, language, line_start, line_end)을 가져온다.
    거리는 이 프로그램이 검색하지 않으므로 None이다. 표에 없는 chunk_id가 있으면 ValueError."""
    ids = sorted(set(ids))
    got = {row[0]: (row[0], None, *row[1:]) for row in conn.execute(CHUNK_SQL, (generate.CHUNK_SET, ids)).fetchall()}
    missing = [chunk_id for chunk_id in ids if chunk_id not in got]
    if missing:
        raise ValueError(f"chunks 표({generate.CHUNK_SET})에 없는 chunk_id: {missing}")
    return got


def prepare(conn, base_rows, questions, expected_rows=None):
    """⑧ 기록을 확인하고 줄마다 판 0의 청크 목록을 데이터베이스에서 다시 만든다. 다시 만든 참고 글(시스템 메시지)이 판 0 답의 것과
    글자까지 같은 줄 수를 출력하고, 하나라도 다르면 ValueError로 멈춘다. 줄마다 {row, search, base_kind, found, question}를 기록 순서대로 돌려준다."""
    check_base(base_rows, expected_rows)
    by_id = {q["id"]: q for q in questions}
    picked = [pick_base(r) for r in base_rows]
    chunks = fetch_chunks(conn, [c["chunk_id"] for search, _, _ in picked for c in search["merged"]])
    items, different = [], []
    for row, (search, base_answer, kind) in zip(base_rows, picked):
        question = by_id[row["question_id"]]
        found = [chunks[c["chunk_id"]] for c in search["merged"]]
        if generate.messages_of("minimal", question, found)[0] != base_answer["system_message"]:
            different.append((row["question_id"], row["seed"]))
        items.append({"row": row, "search": search, "base_kind": kind, "found": found, "question": question})
    print(f"참고 글 대조: {len(items) - len(different)}/{len(items)}줄이 판 0 답의 system_message와 글자까지 같다", flush=True)
    if different:
        raise ValueError(f"다시 만든 참고 글이 판 0 답과 다른 줄이 {len(different)}개 있어 멈춘다: {different}")
    return items


def warm_up():
    """생성 모델을 메모리에서 내리고 몸풀기 호출을 한 번 한다. 결과는 쓰지 않는다."""
    generate.unload_model()
    print("모델을 메모리에서 내리고 시작한다(몸풀기 호출 한 번, 기록하지 않음)", flush=True)
    generate.chat(generate.SYSTEM_EN, generate.WARMUP_USER, WARMUP_SEED)


def flags_of(record):
    """공통 검사에 걸린 것의 이름 목록."""
    checks, flags = record["checks"], []
    if not checks["shape_ok"]:
        flags.append("꼴 오류")
    if checks["cites_evidence"] is False:
        flags.append("근거 청크 안 가리킴")
    if checks["wrong_attached"]:
        flags.append(f'잘못 붙은 인용 {checks["wrong_attached"]}')
    if checks["citation_missing"]:
        flags.append("인용 누락")
    if checks["aborted"]:
        flags.append("끊김")
    if any(item["invalid_chunks"] for item in record["cited"] or []):
        flags.append("목록에 없는 번호")
    return flags


def source_path():
    try:
        return str(BASE_RUNS.relative_to(ROOT))
    except ValueError:
        return str(BASE_RUNS)


def run(version, items, path):
    """몸풀기 뒤에 items의 순서대로 답 쓰기만 하나씩 돌려 한 줄씩 path에 쓴다. 쓴 줄 수를 돌려준다."""
    generate.check_new(path)
    commit, dirty = generate.git_state()
    run_id = time.strftime("%Y%m%dT%H%M%S")
    path.parent.mkdir(parents=True, exist_ok=True)
    warm_up()
    n = 0
    with open(path, "x", encoding="utf-8") as out:
        for item in items:
            base, search, question, seed = item["row"], item["search"], item["question"], item["row"]["seed"]
            start = time.perf_counter()
            try:
                record = graph.cite_answer_of(version, question, item["found"], seed, search["hit_ranks"])
            except RuntimeError as e:
                raise RuntimeError(f'씨앗{seed} {question["id"]}에서 멈춤: {e}') from e
            run_seconds = round(time.perf_counter() - start, 3)
            row = {"run_id": run_id, "question_id": question["id"], "lang": question["lang"], "seed": seed,
                   "generate_model": generate.MODEL, "answer_options": generate.request_body("", "", seed)["options"], "answer_format": "schema",
                   "prompt_version": answer.prompt_version(version), "code_commit": commit, "code_dirty": dirty,
                   "source": {"path": source_path(), "run_id": base["run_id"], "base_kind": item["base_kind"]},
                   "n_chunks": search["n_chunks"], "hit": search["hit"], "hit_ranks": search["hit_ranks"],
                   "chunks": [{key: c[key] for key in ("rank", "chunk_id", "doc_id", "line_start", "line_end")} for c in search["merged"]],
                   "run_seconds": run_seconds, "answer": record}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            n += 1
            n_facts = "-" if record["cited"] is None else len(record["cited"])
            flags = flags_of(record)
            print(f'씨앗{seed} {question["id"]} {"맞음" if record["correct"] else "틀림"} 사실 {n_facts}개 '
                  f'검사 {", ".join(flags) if flags else "걸린 것 없음"} {run_seconds}s', flush=True)
    return n


def main(argv=None):
    parser = argparse.ArgumentParser(description="⑧ 기록의 청크로 근거 칸이 있는 답 쓰기만 다시 돌려 실행 기록을 남긴다")
    parser.add_argument("--version", choices=sorted(answer.SYSTEMS), required=True, help="답 쓰기 지시문 판")
    parser.add_argument("--questions", help="돌릴 질문 ID를 쉼표로 이은 것(짧은 확인용). 주면 --out이 필요하다")
    parser.add_argument("--seeds", help="돌릴 씨앗을 쉼표로 이은 것(짧은 확인용). 주면 --out이 필요하다")
    parser.add_argument("--out", type=Path, help="기록 파일 경로(기본 data/agent/answer_cite/runs_v1.jsonl 또는 runs_v2.jsonl). 기본 경로에는 전체 190번만 쓴다")
    parser.add_argument("--check-only", action="store_true", help="⑧ 기록과 참고 글 대조만 하고 모델은 부르지 않는다")
    args = parser.parse_args(argv)
    partial = args.questions is not None or args.seeds is not None
    if partial and args.out is None:
        parser.error("--questions나 --seeds를 주면 --out을 반드시 함께 줘야 한다(짧은 확인이 기본 경로에 쓰이지 않게)")
    default = RUNS[args.version]
    path = args.out or default
    if partial and path.resolve() == default.resolve():
        parser.error("--questions나 --seeds를 준 짧은 확인은 기본 경로에 쓰지 못한다")
    if not args.check_only:
        generate.check_new(path)
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    wanted = None
    if args.questions is not None:
        wanted = args.questions.split(",")
        unknown = [qid for qid in wanted if qid not in {q["id"] for q in questions}]
        if unknown:
            parser.error(f"질문 파일에 없는 질문 ID: {unknown}")
    seeds = SEEDS
    if args.seeds is not None:
        seeds = tuple(int(s) for s in args.seeds.split(","))
        if any(s not in SEEDS for s in seeds):
            parser.error(f"씨앗은 {SEEDS} 가운데서만 고른다: {seeds}")
    import psycopg
    with psycopg.connect(DSN) as conn:
        items = prepare(conn, read_jsonl(BASE_RUNS), questions)
    if args.check_only:
        print("대조만 하고 끝낸다(--check-only)")
        return
    items = [i for i in items if i["row"]["seed"] in seeds and (wanted is None or i["question"]["id"] in wanted)]
    n = run(args.version, items, path)
    print(f"\n{n}줄 씀: {path}")


if __name__ == "__main__":
    main()
