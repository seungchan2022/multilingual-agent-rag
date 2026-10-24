"""Baseline(문서 없이 답)과 최소판(검색 한 번 + 가져온 청크로 답)으로 질문 38개를 씨앗 1~5로 돌려 실행 기록을 남기는 프로그램(이슈 #12).

  .venv/bin/python src/minimal/generate.py        # 38 × 5 × 2 = 380번 → data/minimal/generation/runs.jsonl

규칙은 decisions/stage4.md의 2026-10-23 줄(생성 설정 / 다시 돌려 같은 글이 나오는지는 확인 조건으로 두지 않고 실행 조건을 고정 /
Baseline과 최소판의 지시문은 영어 지시문 하나 / 가져온 청크를 넣는 부분도 영어로 / 실행 기록)과 decisions/stage5.md의 2026-10-23 줄(최소판의 조합)에 있다.
순서는 시스템(baseline → minimal) → 씨앗(1 → 5) → 질문(파일 순서)이고, 요청은 한 번에 하나씩 보낸다. 시작할 때 몸풀기 호출을 한 번 하고 기록하지 않는다.
실행 기록 파일이 이미 있으면 덮어쓰지 않고 멈춘다(점수는 첫 실행의 기록에서만 계산하기 때문이다). 요약·비교 계산은 이 프로그램에 없다.
"""
import importlib.util
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_retrieval import parse_chunk_set, result_row  # noqa: E402
from index import DSN, QUESTIONS, ROOT, load_model  # noqa: E402
from search import embed_query, search  # noqa: E402

OUT_DIR = ROOT / "data" / "minimal" / "generation"
RUNS = OUT_DIR / "runs.jsonl"
URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:8b"
SEEDS = (1, 2, 3, 4, 5)
SYSTEMS = ("baseline", "minimal")
CHUNK_SET = "size128_title"   # 최소판의 조합(decisions/stage5.md 2026-10-23)
EMBED_MODEL = "bge-m3"
K = 8
PROMPT_VERSION = {"baseline": "en-v1", "minimal": "en-v1+ctx-en-v1"}

# 아래 SYSTEM_EN과 CONTEXT_EN은 research_notes/stage4_answer_language/check_language.py의 같은 이름 상수와 글자가 같다.
# 그 글로 답 언어 확인 38/38을 통과했으므로 한 글자도 바꾸지 않는다(test_generate.py가 두 파일의 글이 같은지 본다).
SYSTEM_EN = (
    "You are an assistant that answers questions. Answer only in the JSON format below.\n"
    '{"reason": "Write the reasoning that leads to the answer, step by step", "answer": "Write only the final answer, briefly"}\n'
    "If a calculation is needed, write the formula in reason, write the unit conversion step (e.g., g → kg) separately, "
    "and then check the calculation once more.\n"
    "Answer in the same language as the question. If the question is in Korean, write reason and answer in Korean; "
    "if it is in English, write them in English."
)
CONTEXT_EN = "\n\nAnswer based on the reference passages below.\nReference passages:\n{passages}"
WARMUP_USER = "안녕"   # 몸풀기 호출의 사용자 메시지(check_language.py와 같다)


def _load_grade_record():
    """채점 규칙은 도메인 고르기 실험의 grade_record(src/domain_select/run.py)를 그대로 쓴다. 파일 이름이 흔한 run이라 경로로 불러온다."""
    spec = importlib.util.spec_from_file_location("domain_select_run", ROOT / "src" / "domain_select" / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.grade_record


grade_record = _load_grade_record()


def passages_of(found):
    """가져온 청크(search의 결과 줄, 순위 순)를 '[순위] 문서 ID (lines 첫 줄-끝 줄)\\n청크 글'로 적어 빈 줄로 잇는다."""
    return "\n\n".join(f"[{rank}] {doc_id} (lines {line_start}-{line_end})\n{text}"
                       for rank, (_, _, doc_id, _, text, _, _, line_start, line_end) in enumerate(found, 1))


def messages_of(system, question, found=None):
    """(시스템 메시지, 사용자 메시지). baseline은 지시문과 질문 글만, minimal은 지시문 끝에 가져온 청크를 붙인다."""
    if system == "baseline":
        return SYSTEM_EN, question["question"]
    return SYSTEM_EN + CONTEXT_EN.format(passages=passages_of(found)), question["question"]


def request_body(system_message, user_message, seed):
    options = {"temperature": 0.7, "top_p": 0.8, "top_k": 20, "min_p": 0, "num_predict": 2048, "num_ctx": 32768, "seed": seed}
    body = {"model": MODEL, "messages": [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}],
            "stream": False, "think": False, "format": "json", "options": options}
    return body


def chat(system_message, user_message, seed):
    """Ollama에 요청 하나를 보내 (모델이 돌려준 글, 걸린 시간, eval_count, prompt_eval_count)를 돌려준다."""
    body = request_body(system_message, user_message, seed)
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        res = json.loads(r.read())
    return res["message"]["content"], round(time.time() - t0, 2), res.get("eval_count"), res.get("prompt_eval_count")


def language_of(text):
    """한글 음절이 로마자보다 같거나 많으면 ko, 적으면 en. (언어, 한글 수, 로마자 수)."""
    hangul = len(re.findall(r"[가-힣]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return ("ko" if hangul >= latin else "en"), hangul, latin


def graded(question, output):
    """모델이 돌려준 글을 읽어 reason·answer와 채점 칸을 만든다. JSON이 아니거나 dict가 아니면 reason·answer는 빈 글, 맞음은 false, 답 언어는 null이다."""
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError:
        parsed = None
    ok = isinstance(parsed, dict)
    reason, answer = (parsed.get("reason", ""), parsed.get("answer", "")) if ok else ("", "")
    grade = grade_record(question, answer)
    answer_lang, hangul, latin = language_of(f"{reason} {answer}") if ok else (None, None, None)
    return {"parsed_ok": ok, "reason": reason, "answer": answer,
            "numbers": grade["numbers"], "picked": grade["picked"], "value": question["value"], "correct": grade["correct"],
            "answer_lang": answer_lang, "hangul": hangul, "latin": latin, "lang_ok": answer_lang == question["lang"]}


def git_state():
    """(HEAD 커밋, 작업 트리에 커밋되지 않은 변경이 있는지). 새 파일도 변경으로 센다."""
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return commit, bool(status.strip())


def check_new(path):
    if path.exists():
        raise FileExistsError(f"{path}가 이미 있다. 점수는 첫 실행의 기록에서만 계산하므로 덮어쓰지 않는다")


def retrieve(conn, model, question):
    """질문 글을 그대로 검색 쿼리로 써서 검색 한 번. (결과 줄 목록, 임베딩 시간, 검색 시간)."""
    start = time.perf_counter()
    vector = embed_query(model, question["question"])
    embed_seconds = time.perf_counter() - start
    start = time.perf_counter()
    found = search(conn, CHUNK_SET, EMBED_MODEL, vector, K)
    return found, embed_seconds, time.perf_counter() - start


def retrieval_fields(question, found, embed_seconds, search_seconds):
    """검색 기록 칸. compare_retrieval.result_row와 같은 칸 이름·계산이다."""
    row = result_row(CHUNK_SET, EMBED_MODEL, question, found, embed_seconds, search_seconds)
    size, title = parse_chunk_set(CHUNK_SET)
    return {"chunk_set": CHUNK_SET, "embedding_model": EMBED_MODEL, "chunk_size": size, "title": title, "query": row["query"], "k": K,
            "retrieved": row["retrieved"], "retrieved_tokens": row["retrieved_tokens"], "hit": row["hit"], "hit_ranks": row["hit_ranks"],
            "embed_seconds": row["embed_seconds"], "search_seconds": row["search_seconds"]}


NO_RETRIEVAL = {key: None for key in ("chunk_set", "embedding_model", "chunk_size", "title", "query", "k", "retrieved", "retrieved_tokens", "hit", "hit_ranks",
                                      "embed_seconds", "search_seconds")}


def run(questions, path, conn, model, seeds=SEEDS, systems=SYSTEMS):
    """몸풀기 호출 한 번 뒤에 시스템 → 씨앗 → 질문 순서로 하나씩 돌려 한 줄씩 path에 쓴다. 쓴 줄 수를 돌려준다."""
    check_new(path)
    commit, dirty = git_state()
    run_id = time.strftime("%Y%m%dT%H%M%S")
    path.parent.mkdir(parents=True, exist_ok=True)
    chat(SYSTEM_EN, WARMUP_USER, seeds[0])  # 몸풀기 호출. 결과는 쓰지 않는다.
    n = 0
    with open(path, "x", encoding="utf-8") as out:
        for system in systems:
            for seed in seeds:
                for q in questions:
                    if system == "minimal":
                        found, embed_seconds, search_seconds = retrieve(conn, model, q)
                        search_part = retrieval_fields(q, found, embed_seconds, search_seconds)
                    else:
                        found, search_part = None, NO_RETRIEVAL
                    system_message, user_message = messages_of(system, q, found)
                    output, seconds, tokens, prompt_tokens = chat(system_message, user_message, seed)
                    row = {"run_id": run_id, "system": system, "question_id": q["id"], "lang": q["lang"], "branch": q["branch"], "seed": seed,
                           "model": MODEL, "options": request_body(system_message, user_message, seed)["options"],
                           "prompt_version": PROMPT_VERSION[system], "code_commit": commit, "code_dirty": dirty,
                           **search_part, "system_message": system_message, "user_message": user_message, "output": output,
                           **graded(q, output), "gen_seconds": seconds, "gen_tokens": tokens, "prompt_tokens": prompt_tokens}
                    out.write(json.dumps(row, ensure_ascii=False) + "\n")
                    out.flush()
                    n += 1
                    print(f'{system} 씨앗{seed} {q["id"]} {"맞음" if row["correct"] else "틀림"} {seconds}s', flush=True)
    return n


def main():
    import psycopg
    check_new(RUNS)
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    model = load_model(EMBED_MODEL)
    with psycopg.connect(DSN) as conn:
        n = run(questions, RUNS, conn, model)
    print(f"\n{n}줄 씀: {RUNS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
