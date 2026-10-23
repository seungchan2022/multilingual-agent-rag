"""PostgreSQL(pgvector)에 넣은 청크에서 질의와 가까운 청크를 찾는 함수. 청크를 넣는 프로그램은 src/minimal/index.py다.

규칙은 decisions/stage4.md의 2026-10-23 줄(벡터 스토어는 PostgreSQL + pgvector / Codex 1차 검토 ㉥ / MiniLM은 비교에서 재기 전에 뺀다 ㉣)에 있다.
근사 인덱스(HNSW, IVFFlat)를 쓰지 않고 한 묶음·한 모델의 모든 청크와 코사인 거리(<=>)를 잰다. 순서는 거리 오름차순이고, 같은 거리는 청크 ID 오름차순이다.
청크 ID는 바이트 순서(COLLATE "C")로 비교한다. 데이터베이스의 기본 정렬 규칙에 따라 같은 거리의 순서가 달라지지 않게 하려는 것이다.
"""

SQL = """
SELECT c.chunk_id, e.embedding <=> %s::vector AS distance, c.doc_id, c.lines, c.text, c.tokens,
       c.language, c.line_start, c.line_end
FROM chunk_embeddings e JOIN chunks c ON c.chunk_set = e.chunk_set AND c.chunk_id = e.chunk_id
WHERE e.chunk_set = %s AND e.model = %s
ORDER BY distance, c.chunk_id COLLATE "C"
LIMIT %s
"""


def vector_literal(vector):
    """벡터를 pgvector가 읽는 글자 '[0.1,0.2,…]'로 바꾼다. 유효숫자 9자리는 32비트 실수를 되돌려 읽어도 같은 값이 나오는 길이다."""
    return "[" + ",".join(f"{float(x):.9g}" for x in vector) + "]"


def embed_query(model, text):
    """질의 문장 하나를 L2 정규화한 벡터로 바꾼다. 청크와 같게 지시문을 붙이지 않고, 장치는 모델을 불러올 때 정한 CPU다."""
    return model.encode([text], normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)[0]


def search(conn, chunk_set, model_name, query_vector, k):
    """chunk_set·model_name의 청크에서 상위 k개를 (chunk_id, distance, doc_id, lines, text, tokens, language, line_start, line_end) 목록으로 돌려준다.
    뒤의 셋(문서 언어, 원문 첫 줄·끝 줄)은 chunks 표의 칸이고, 검색 기록(compare_retrieval.py)이 쓴다."""
    return conn.execute(SQL, (vector_literal(query_vector), chunk_set, model_name, k)).fetchall()
