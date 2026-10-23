"""src/minimal/index.py와 src/minimal/search.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

실제 multilingual_rag를 건드리지 않게 시험용 데이터베이스 multilingual_rag_test를 만들어 쓰고 끝나면 지운다
(CREATE EXTENSION vector는 index.create_schema가 한다). 모델은 불러오지 않고, 시험이 만든 작은 가짜 청크와 벡터를 쓴다.
시험마다 표를 새로 만들어 서로 영향을 주지 않는다.
"""
import sys
import unittest
from pathlib import Path

import numpy as np
import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent))
import index  # noqa: E402
from search import search, vector_literal  # noqa: E402

ADMIN_DSN = "dbname=multilingual_rag"  # 시험용 데이터베이스를 만들고 지우는 연결(실제 표는 건드리지 않는다)
TEST_DB = "multilingual_rag_test"
DIM = 8
SET = "size128_title"
MODEL = "bge-m3"
# 바이트 순서(C)와 이 데이터베이스의 기본 정렬 규칙(en_US.UTF-8)이 서로 다르게 놓는 ID 쌍 둘: 대문자·소문자, '#'·'-'
TIES = [("tie#a", "tie#B"), ("tie#9", "tie-1")]


def unit(rng, n=1):
    v = rng.normal(size=(n, DIM)).astype(np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def fake_row(chunk_id, text):
    return {"chunk_id": chunk_id, "doc_id": chunk_id.split("#")[0], "language": "en", "size": 128, "title": True,
            "kind": "text", "path": "Fake", "text": text, "line_start": 3, "line_end": 5, "lines": [3, 4, 5],
            "tokens": 7, "over_limit": False}


class IndexTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with psycopg.connect(ADMIN_DSN, autocommit=True) as admin:
            admin.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
            admin.execute(f"CREATE DATABASE {TEST_DB}")

    @classmethod
    def tearDownClass(cls):
        with psycopg.connect(ADMIN_DSN, autocommit=True) as admin:
            admin.execute(f"DROP DATABASE IF EXISTS {TEST_DB} WITH (FORCE)")

    def setUp(self):
        rng = np.random.default_rng(0)
        self.tie_vectors = unit(rng, len(TIES))   # 쌍마다 같은 벡터(거리가 같다)
        self.rows, vectors = [], []
        for n, vec in enumerate(unit(rng, 5), 1):
            self.rows.append(fake_row(f"fake#{n:04d}", f"글 {n}"))
            vectors.append(vec)
        for pair, vec in zip(TIES, self.tie_vectors):
            for chunk_id in pair:                 # 정렬 규칙을 잘못 쓰면 뒤집히도록 사전 순서로 먼저 오는 것부터 넣는다
                self.rows.append(fake_row(chunk_id, "같은 글"))
                vectors.append(vec)
        self.vectors = np.array(vectors)
        self.conn = psycopg.connect(f"dbname={TEST_DB}")
        self.addCleanup(self.conn.close)
        index.create_schema(self.conn)
        index.insert_chunks(self.conn, SET, self.rows)
        index.insert_embeddings(self.conn, SET, MODEL, self.rows, self.vectors)

    def test_rows_dimension_and_length(self):
        n, deviation = index.check_stored(self.conn, SET, MODEL, len(self.rows), DIM)
        self.assertEqual(n, len(self.rows))
        self.assertLess(deviation, index.NORM_TOLERANCE)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM chunks").fetchone()[0], len(self.rows))
        # 어긋나면 멈춘다: 행 수, 차원, 길이
        with self.assertRaises(ValueError):
            index.check_stored(self.conn, SET, MODEL, len(self.rows) + 1, DIM)
        with self.assertRaises(ValueError):
            index.check_stored(self.conn, SET, MODEL, len(self.rows), DIM + 1)
        index.insert_chunks(self.conn, "other", [fake_row("long#1", "긴 벡터")])
        index.insert_embeddings(self.conn, "other", MODEL, [fake_row("long#1", "")], self.vectors[:1] * 2)
        with self.assertRaises(ValueError):
            index.check_stored(self.conn, "other", MODEL, 1, DIM)

    def test_chunk_columns_are_stored(self):
        row = self.conn.execute("SELECT chunk_set, doc_id, lines, tokens, over_limit, title FROM chunks WHERE chunk_id = 'fake#0001'").fetchone()
        self.assertEqual(row, (SET, "fake", [3, 4, 5], 7, False, True))

    def test_same_distance_orders_by_chunk_id_bytes(self):
        for pair, vec in zip(TIES, self.tie_vectors):
            # 시험이 쓸모 있으려면 데이터베이스의 기본 정렬 규칙이 바이트 순서와 달라야 한다
            default = [r[0] for r in self.conn.execute("SELECT x FROM unnest(%s::text[]) x ORDER BY x", (list(pair),))]
            bytewise = [r[0] for r in self.conn.execute('SELECT x FROM unnest(%s::text[]) x ORDER BY x COLLATE "C"', (list(pair),))]
            self.assertNotEqual(default, bytewise)
            result = search(self.conn, SET, MODEL, vec, 2)
            self.assertEqual([r[0] for r in result], bytewise)
            self.assertEqual(result[0][1], result[1][1])

    def test_same_query_same_result(self):
        query = unit(np.random.default_rng(1))[0]
        first = search(self.conn, SET, MODEL, query, len(self.rows))
        second = search(self.conn, SET, MODEL, query, len(self.rows))
        self.assertEqual(first, second)
        self.assertEqual([r[1] for r in first], sorted(r[1] for r in first))

    def test_distance_matches_python_cosine_distance(self):
        query = unit(np.random.default_rng(2))[0]
        by_id = {r["chunk_id"]: v for r, v in zip(self.rows, self.vectors)}
        result = search(self.conn, SET, MODEL, query, len(self.rows))
        self.assertEqual(len(result), len(self.rows))
        for chunk_id, distance, doc_id, lines, text, tokens in result:
            expected = 1 - float(np.dot(by_id[chunk_id].astype(np.float64), query.astype(np.float64)))
            self.assertAlmostEqual(distance, expected, delta=1e-5)
        best = next(r for r in result if r[0] == "fake#0001")
        self.assertEqual(best[2:], ("fake", [3, 4, 5], "글 1", 7))

    def test_search_stays_within_chunk_set_and_model_and_limit(self):
        query = self.vectors[0]
        self.assertEqual(len(search(self.conn, SET, MODEL, query, 3)), 3)
        self.assertEqual(search(self.conn, SET, "gte-multilingual-base", query, 3), [])
        self.assertEqual(search(self.conn, "size256_title", MODEL, query, 3), [])

    def test_rebuild_starts_from_empty(self):
        index.create_schema(self.conn)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM chunks").fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM chunk_embeddings").fetchone()[0], 0)

    def test_vector_literal_round_trips_float32(self):
        for v in unit(np.random.default_rng(3), 50):
            back = np.array([float(x) for x in vector_literal(v)[1:-1].split(",")], dtype=np.float32)
            self.assertTrue(np.array_equal(back, v))


if __name__ == "__main__":
    unittest.main()
