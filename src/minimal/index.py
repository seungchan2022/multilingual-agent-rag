"""청크 묶음 4개를 두 임베딩 모델로 벡터로 바꿔 PostgreSQL(pgvector)에 넣는 프로그램. 조합 8개(묶음 4개 × 모델 2개)를 넣고 확인한다.

  uv run python src/minimal/index.py

규칙은 decisions/stage4.md의 2026-10-23 줄(벡터 스토어는 PostgreSQL + pgvector / Codex 1차 검토 ㉥ / MiniLM은 비교에서 재기 전에 뺀다 ㉣)과
decisions/stage5.md의 2026-10-23 줄(PostgreSQL 18 / 두 모델이 청크 묶음 4개를 함께 쓴다)에 있다. 찾는 함수는 src/minimal/search.py다.
임베딩할 글은 청크의 text 칸 그대로이고, 두 모델 모두 지시문을 붙이지 않는다. 벡터는 L2 정규화한다.
같은 입력에서 같은 벡터가 나오게 장치는 CPU, 배치 크기는 상수, 청크는 파일의 순서대로 넣는다. 모델은 캐시에서만 읽는다(HF_HUB_OFFLINE=1).
다시 돌리면 표 두 개를 지우고 처음부터 다시 만든다. 다 넣은 뒤 조합마다 확인하고, 어긋나면 멈춘다.
"""
import json
import os
import sys
import time
from importlib.metadata import version
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"  # sentence_transformers를 불러오기 전에 켠다. 모델을 캐시에서만 읽는다

import psycopg  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search import embed_query, search, vector_literal  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CHUNKS = ROOT / "data" / "minimal" / "chunks"
QUESTIONS = ROOT / "data" / "minimal" / "questions.json"
DSN = "dbname=multilingual_rag"
CHUNK_SETS = ("size128_notitle", "size128_title", "size256_notitle", "size256_title")
MODELS = {  # 표에 적는 이름 -> (불러오는 이름, 벡터 차원, trust_remote_code)
    "bge-m3": ("BAAI/bge-m3", 1024, False),
    "gte-multilingual-base": ("Alibaba-NLP/gte-multilingual-base", 768, True),
}
BATCH_SIZE = 16     # 배치 크기도 벡터에 영향을 주므로(길이를 맞추는 채움) 고정한다
NORM_TOLERANCE = 1e-5
COLUMNS = ["chunk_id", "doc_id", "language", "size", "title", "kind", "path", "text",
           "line_start", "line_end", "lines", "tokens", "over_limit"]

SCHEMA = """
DROP TABLE IF EXISTS chunk_embeddings, chunks;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE chunks (
    chunk_set text NOT NULL,
    chunk_id text NOT NULL,
    doc_id text NOT NULL,
    language text NOT NULL,
    size integer NOT NULL,
    title boolean NOT NULL,
    kind text NOT NULL,
    path text NOT NULL,
    text text NOT NULL,
    line_start integer NOT NULL,
    line_end integer NOT NULL,
    lines integer[] NOT NULL,
    tokens integer NOT NULL,
    over_limit boolean NOT NULL,
    PRIMARY KEY (chunk_set, chunk_id)
);
CREATE TABLE chunk_embeddings (
    chunk_set text NOT NULL,
    chunk_id text NOT NULL,
    model text NOT NULL,
    embedding vector NOT NULL,
    PRIMARY KEY (chunk_set, chunk_id, model),
    FOREIGN KEY (chunk_set, chunk_id) REFERENCES chunks (chunk_set, chunk_id)
);
"""


def load_model(key):
    """모델을 CPU로 불러온다. search.embed_query가 같은 모델을 받는다."""
    from sentence_transformers import SentenceTransformer
    name, _, trust = MODELS[key]
    return SentenceTransformer(name, device="cpu", trust_remote_code=trust)


def read_chunks(path):
    """청크 JSONL을 파일의 순서대로 읽는다."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def embed_texts(model, texts):
    """글 목록을 L2 정규화한 벡터로 바꾼다. 순서는 입력과 같다."""
    return model.encode(texts, batch_size=BATCH_SIZE, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)


def create_schema(conn):
    """표 두 개를 지우고 새로 만든다."""
    conn.execute(SCHEMA)
    conn.commit()


def insert_chunks(conn, chunk_set, rows):
    marks = ", ".join(["%s"] * (len(COLUMNS) + 1))
    with conn.cursor() as cur:
        cur.executemany(f"INSERT INTO chunks (chunk_set, {', '.join(COLUMNS)}) VALUES ({marks})",
                        [[chunk_set] + [r[c] for c in COLUMNS] for r in rows])
    conn.commit()


def insert_embeddings(conn, chunk_set, model_key, rows, vectors):
    with conn.cursor() as cur:
        cur.executemany("INSERT INTO chunk_embeddings (chunk_set, chunk_id, model, embedding) VALUES (%s, %s, %s, %s::vector)",
                        [(chunk_set, r["chunk_id"], model_key, vector_literal(v)) for r, v in zip(rows, vectors)])
    conn.commit()


def check_stored(conn, chunk_set, model_key, expected_rows, dim):
    """저장된 행 수·벡터 차원·벡터 길이를 확인한다. (행 수, 가장 먼 길이 차이)를 돌려주고, 어긋나면 ValueError를 던진다."""
    n, wrong_dim, deviation = conn.execute(
        "SELECT count(*), count(*) FILTER (WHERE vector_dims(embedding) <> %s), max(abs(vector_norm(embedding) - 1)) "
        "FROM chunk_embeddings WHERE chunk_set = %s AND model = %s", (dim, chunk_set, model_key)).fetchone()
    if n != expected_rows:
        raise ValueError(f"{chunk_set} × {model_key}: 저장된 행 {n}개, 청크 파일 {expected_rows}줄")
    if wrong_dim:
        raise ValueError(f"{chunk_set} × {model_key}: 차원이 {dim}이 아닌 벡터 {wrong_dim}개")
    if deviation is None or deviation > NORM_TOLERANCE:
        raise ValueError(f"{chunk_set} × {model_key}: 벡터 길이가 1에서 {deviation} 벗어남(허용 {NORM_TOLERANCE})")
    return n, deviation


def check_repeat(conn, model, chunk_set, model_key, question, k=8):
    """같은 질의를 두 번(질의 벡터도 두 번 만들어) 검색해 같은 청크가 같은 순서·같은 거리로 나오는지 본다. 어긋나면 ValueError."""
    runs = [[(r[0], r[1]) for r in search(conn, chunk_set, model_key, embed_query(model, question), k)] for _ in range(2)]
    if runs[0] != runs[1] or len(runs[0]) != k:
        raise ValueError(f"{chunk_set} × {model_key}: 같은 질의의 두 검색 결과가 다름: {runs[0]} / {runs[1]}")
    return runs[0][0]


def main():
    started = time.time()
    chunk_rows = {s: read_chunks(CHUNKS / f"{s}.jsonl") for s in CHUNK_SETS}
    models = {key: load_model(key) for key in MODELS}
    seconds = {}
    with psycopg.connect(DSN) as conn:
        create_schema(conn)
        for s in CHUNK_SETS:
            insert_chunks(conn, s, chunk_rows[s])
        for key, model in models.items():
            for s in CHUNK_SETS:
                t = time.time()
                insert_embeddings(conn, s, key, chunk_rows[s], embed_texts(model, [r["text"] for r in chunk_rows[s]]))
                seconds[(s, key)] = time.time() - t
                print(f"넣음: {s} × {key}: {len(chunk_rows[s])}행, {seconds[(s, key)]:.1f}초", flush=True)

        question = json.loads(QUESTIONS.read_text(encoding="utf-8"))[0]["question"]
        print(f"\n확인(질의: {question})")
        for s in CHUNK_SETS:
            n_chunks = conn.execute("SELECT count(*) FROM chunks WHERE chunk_set = %s", (s,)).fetchone()[0]
            if n_chunks != len(chunk_rows[s]):
                raise ValueError(f"{s}: chunks 표 {n_chunks}행, 청크 파일 {len(chunk_rows[s])}줄")
            for key, model in models.items():
                n, deviation = check_stored(conn, s, key, len(chunk_rows[s]), MODELS[key][1])
                first_id, first_distance = check_repeat(conn, model, s, key, question)
                print(f"{s} × {key}: 행 {n}개, 차원 {MODELS[key][1]}, 길이 오차 최대 {deviation:.2e}, "
                      f"두 검색 같음(1위 {first_id}, 거리 {first_distance:.6f})")

    print("\n조합마다 행 수와 임베딩·저장에 걸린 시간")
    for key in MODELS:
        for s in CHUNK_SETS:
            print(f"{s} × {key}: 행 {len(chunk_rows[s])}개, {seconds[(s, key)]:.1f}초")
    print(f"전체 {time.time() - started:.1f}초")
    print("판: " + ", ".join(f"{p} {version(p)}" for p in ("torch", "sentence-transformers", "transformers")))


if __name__ == "__main__":
    main()
