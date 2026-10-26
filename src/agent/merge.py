"""검색어 여러 개로 검색해 청크 목록을 합치는 함수(이슈 #14). 합친 청크가 답 쓰기로 넘어간다.

규칙은 decisions/stage6.md의 2026-10-26 줄(청크 합치기 / 비교용이 넘기는 청크 수를 실행마다 맞춘다)에 있다.
원래 질문으로 가져온 8개를 모두 두고, 다른 검색어(한국어판, 영어판)마다 위쪽 4개를 이미 고른 청크(chunk_id)와 겹치지 않게 더한다.
4개를 채우려고 더 아래로 내려가지 않는다. 다른 검색어의 글이 원래 질문과 같으면(앞뒤 빈칸을 뺀 글자가 같으면) 그 검색은 하지 않는다.
합친 목록의 순서는 원래 질문 → 첫째 다른 검색어에서 더한 것 → 둘째 다른 검색어에서 더한 것이고, 이 순서가 답 쓰기의 [순위] 번호가 된다.
근거를 찾았는지(hit)는 compare_retrieval.matched_evidence로 청크마다 매긴 근거 번호가 합친 목록에 하나라도 있는지다.
검색 한 번은 src/minimal/generate.retrieve와 같은 방식이다(청크 묶음 size128_title, 모델 bge-m3, 질문 글을 그대로 검색어로 씀).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
from compare_retrieval import result_row  # noqa: E402
from generate import CHUNK_SET, EMBED_MODEL, K  # noqa: E402
from search import embed_query, search  # noqa: E402

K_OTHER = 4        # 다른 검색어에서 가져와 더하는 수(원래 질문 k = 8의 절반)
K_COMPARISON = 16  # 비교용 재료: 원래 질문 검색을 이만큼 가져와 기록한다(원래 8개 + 다른 검색어 둘의 4개씩)


def fetch(conn, model, question, text, k):
    """text를 검색어로 검색 한 번. (search 결과 줄 목록, 기록용 청크 목록, 임베딩 시간, 검색 시간).
    기록용 청크는 순위, chunk_id, doc_id, language, distance, lines, line_start, line_end, tokens, evidence(원래 질문의 근거 번호)다."""
    start = time.perf_counter()
    vector = embed_query(model, text)
    embed_seconds = time.perf_counter() - start
    start = time.perf_counter()
    found = search(conn, CHUNK_SET, EMBED_MODEL, vector, k)
    search_seconds = time.perf_counter() - start
    rows = result_row(CHUNK_SET, EMBED_MODEL, {**question, "question": text}, found, embed_seconds, search_seconds)["retrieved"]
    return found, rows, embed_seconds, search_seconds


def comparison_retrieved(conn, model, question):
    """비교용 재료: 원래 질문 글로 k = 16 검색한 청크 16개를 근거 번호와 함께(기록용 청크 목록). 시스템의 흐름에는 들어가지 않는다."""
    return fetch(conn, model, question, question["question"], K_COMPARISON)[1]


def merge_search(conn, model, question, others):
    """원래 질문으로 K개를 검색하고, others([(이름, 검색어 글), …])의 순서대로 위쪽 K_OTHER개를 겹치지 않게 더한다.
    (검색 기록, 합친 search 결과 줄 목록)을 돌려준다. 합친 줄 목록은 답 쓰기에 넘기는 것이고 기록에는 쓰지 않는다(글이 길다).
    검색 기록: queries(검색어마다 name, text, skipped, retrieved, embed_seconds, search_seconds), merged(청크마다 순위와 source, source_rank),
    n_chunks, hit, hit_ranks(합친 목록의 순위). 건너뛴 검색어는 retrieved가 빈 목록이고 시간이 None이다."""
    found, rows, embed_seconds, search_seconds = fetch(conn, model, question, question["question"], K)
    queries = [{"name": "original", "text": question["question"], "skipped": False, "retrieved": rows,
                "embed_seconds": embed_seconds, "search_seconds": search_seconds}]
    merged_found, merged_rows = list(found), [{**row, "source": "original", "source_rank": row["rank"]} for row in rows]
    chosen = {row["chunk_id"] for row in rows}
    for name, text in others:
        if text.strip() == question["question"].strip():
            queries.append({"name": name, "text": text, "skipped": True, "retrieved": [], "embed_seconds": None, "search_seconds": None})
            continue
        found, rows, embed_seconds, search_seconds = fetch(conn, model, question, text, K_OTHER)
        queries.append({"name": name, "text": text, "skipped": False, "retrieved": rows,
                        "embed_seconds": embed_seconds, "search_seconds": search_seconds})
        for line, row in zip(found, rows):
            if row["chunk_id"] not in chosen:
                chosen.add(row["chunk_id"])
                merged_found.append(line)
                merged_rows.append({**row, "source": name, "source_rank": row["rank"]})
    for rank, row in enumerate(merged_rows, 1):
        row["rank"] = rank
    hit_ranks = [row["rank"] for row in merged_rows if row["evidence"]]
    record = {"queries": queries, "merged": merged_rows, "n_chunks": len(merged_rows), "hit": bool(hit_ranks), "hit_ranks": hit_ranks}
    return record, merged_found
