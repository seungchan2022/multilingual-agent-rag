"""짝 질문으로 검색한 결과를 질문마다 남기는 프로그램(이슈 #14). 모델은 쓰지 않고 검색만 한다.

  .venv/bin/python src/agent/pair_search.py     # 질문 38개 → data/agent/plan_search/pair_search.jsonl

규칙은 decisions/stage6.md의 2026-10-26 줄(남길 기준의 하나 / 다른 판 검색을 남길지와 번역을 고칠지는 한 표로 정한다 / 비교용이 넘기는 청크 수를 실행마다 맞춘다)에 있다.
짝 질문은 질문 파일에서 pair_id로 가리키는 질문(같은 사실을 다른 언어로 사람이 쓴 것)이다. 청크 합치기는 시스템과 같은 규칙이다:
원래 질문으로 8개를 모두 두고, 짝 질문으로 가져온 위쪽 4개 중 겹치지 않는 것을 더한다(짝 질문 글이 원래 질문과 같을 일은 없지만 같으면 건너뛴다).
근거는 원래 질문의 evidence로 센다. 모델을 쓰지 않으므로 씨앗마다 결과가 같고, 질문마다 한 줄만 남긴다. 견주는 쪽(compare.py)이 씨앗 5개에 똑같이 센다.
질문마다 비교용 재료(원래 질문으로 k = 16 검색)도 함께 남긴다. 기록 파일이 이미 있으면 덮어쓰지 않고 멈춘다.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402
import merge  # noqa: E402
from index import DSN, QUESTIONS, ROOT, load_model  # noqa: E402

PAIR_SEARCH = ROOT / "data" / "agent" / "plan_search" / "pair_search.jsonl"


def run(questions, path, conn, model):
    """질문마다 한 줄씩 path에 쓴다. 쓴 줄 수를 돌려준다."""
    generate.check_new(path)
    commit, dirty = generate.git_state()
    by_id = {q["id"]: q for q in questions}
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(path, "x", encoding="utf-8") as out:
        for q in questions:
            pair = by_id[q["pair_id"]]
            record, _ = merge.merge_search(conn, model, q, [("pair", pair["question"])])
            row = {"question_id": q["id"], "lang": q["lang"], "branch": q["branch"], "pair_id": q["pair_id"],
                   "code_commit": commit, "code_dirty": dirty, "search": record,
                   "comparison_retrieved": merge.comparison_retrieved(conn, model, q)}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            n += 1
            print(f'{q["id"]} 짝 {q["pair_id"]} 청크 {record["n_chunks"]}개 근거 {"찾음" if record["hit"] else "못 찾음"}', flush=True)
    return n


def main():
    generate.check_new(PAIR_SEARCH)
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    import psycopg
    model = load_model(generate.EMBED_MODEL)
    with psycopg.connect(DSN) as conn:
        n = run(questions, PAIR_SEARCH, conn, model)
    print(f"\n{n}줄 씀: {PAIR_SEARCH}")


if __name__ == "__main__":
    main()
