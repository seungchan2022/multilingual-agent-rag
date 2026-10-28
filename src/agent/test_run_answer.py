"""src/agent/run_answer.py(⑧ 기록의 청크로 답 쓰기만 다시 돌림)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama와 실제 데이터베이스를 쓰지 않는다. urlopen과 chunks 표를 가짜로 바꾸고(fakes.py), 파일은 임시 폴더에 쓴다(data/agent/에는 쓰지 않는다).
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import answer  # noqa: E402
import generate  # noqa: E402
import run_answer  # noqa: E402
from fakes import TIMES, FakeOllama, FakeResponse, found_row, patched, question  # noqa: E402

Q1, Q2 = "반감기는 몇 시간인가?", "다른 질문인가?"
COMMIT = "369d74dabcdef0123456789abcdef0123456789a"


def table_row(chunk_id, evidence=False):
    """chunks 표의 행 (chunk_id, doc_id, lines, text, tokens, language, line_start, line_end). found_row와 같은 내용이다."""
    row = found_row(chunk_id, text=f"{chunk_id} 글", evidence=evidence)
    return (row[0], *row[2:])


def chunk_table():
    ids = [f"a{i}" for i in range(1, 7)] + [f"b{i}" for i in range(1, 7)] + [f"f{i}" for i in range(1, 5)]
    return {cid: table_row(cid, evidence=(cid in ("a3", "f2"))) for cid in ids}


class FakeConn:
    """psycopg 연결을 대신한다. chunks 표 질의의 chunk_id 목록에 맞는 행만 돌려주고 질의를 calls에 쌓는다."""

    def __init__(self, table):
        self.table, self.calls = table, []

    def execute(self, sql, params):
        self.calls.append((sql, params))
        chunk_set, ids = params
        rows = [self.table[cid] for cid in ids if cid in self.table]
        return mock.Mock(fetchall=lambda: rows)


def merged_of(chunk_ids):
    return [{"rank": i, "chunk_id": cid, "doc_id": "d", "language": "en", "distance": 0.1, "lines": [1], "line_start": 1, "line_end": 1, "tokens": 9,
             "evidence": False, "source": "original", "source_rank": i} for i, cid in enumerate(chunk_ids, 1)]


def search_of(table, chunk_ids, hit_ranks):
    merged = merged_of(chunk_ids)
    for m in merged:   # DB 행의 doc_id·줄을 기록에도 같게 적는다
        m["doc_id"], m["line_start"], m["line_end"] = table[m["chunk_id"]][1], table[m["chunk_id"]][6], table[m["chunk_id"]][7]
    return {"queries": [], "merged": merged, "n_chunks": len(merged), "hit": bool(hit_ranks), "hit_ranks": hit_ranks}


def base_answer(q, table, search):
    found = [(c["chunk_id"], None, *table[c["chunk_id"]][1:]) for c in search["merged"]]
    return {"system_message": generate.messages_of("minimal", q, found)[0], "user_message": q["question"], "answer": "17.7 kg", "reason": "읽는다"}


def base_rows(table, questions, seeds=(1, 2)):
    """⑧ 기록 꼴의 줄. (q01-ko, 씨앗 1)만 처음 계획 기록(first_plan_search)이 따로 있다: 최종 검색은 b1..b6, 처음 검색은 f1..f4."""
    rows = []
    for seed in seeds:
        for q in questions:
            final = search_of(table, [f"a{i}" for i in range(1, 7)] if q["id"] == "q02-ko" else [f"b{i}" for i in range(1, 7)], [3] if q["id"] == "q02-ko" else [])
            first = None
            if (q["id"], seed) == ("q01-ko", 1):
                first = search_of(table, ["f1", "f2", "f3", "f4"], [2])
            rows.append({"run_id": "20261028T100000", "question_id": q["id"], "seed": seed, "code_commit": COMMIT, "code_dirty": False,
                         "search": final, "answer": base_answer(q, table, final), "first_plan_search": first,
                         "first_plan_answer": base_answer(q, table, first) if first else None})
    return rows


def cite_answer(citations):
    return json.dumps({"reason": "읽는다", "answer": "17.7 시간", "citations": citations}, ensure_ascii=False)


class WorldMixin:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.table = chunk_table()
        self.conn = FakeConn(self.table)
        self.questions = [question("q01-ko", "ko", Q1), question("q02-ko", "ko", Q2)]
        self.rows = base_rows(self.table, self.questions)


class PickBaseTest(WorldMixin, unittest.TestCase):
    def test_first_plan_when_it_exists(self):
        search, ans, kind = run_answer.pick_base(self.rows[0])   # q01-ko 씨앗 1
        self.assertEqual((kind, [c["chunk_id"] for c in search["merged"]], search["hit_ranks"]), ("first_plan", ["f1", "f2", "f3", "f4"], [2]))
        self.assertIs(ans, self.rows[0]["first_plan_answer"])

    def test_final_when_there_is_no_first_plan(self):
        for row in self.rows[1:]:
            search, ans, kind = run_answer.pick_base(row)
            self.assertEqual(kind, "final")
            self.assertIs(search, row["search"])
            self.assertIs(ans, row["answer"])


class PrepareTest(WorldMixin, unittest.TestCase):
    def prepare(self, rows=None, expected=4):
        with redirect_stdout(io.StringIO()) as printed:
            try:
                return run_answer.prepare(self.conn, rows or self.rows, self.questions, expected)
            finally:
                self.printed = printed.getvalue()

    def test_chunks_are_rebuilt_in_search_row_form_and_in_rank_order(self):
        items = self.prepare()
        first = items[0]
        self.assertEqual(first["base_kind"], "first_plan")
        self.assertEqual(first["found"][1], ("f2", None, "doc-a", [5], "반감기는 17.7 시간이다 f2 글", 9, "en", 5, 5))
        self.assertEqual([r[0] for r in first["found"]], ["f1", "f2", "f3", "f4"])   # 판 0은 처음 계획의 청크
        self.assertEqual(len(first["found"][0]), 9)
        self.assertIsNone(first["found"][0][1])
        self.assertEqual([r[0] for r in items[1]["found"]], [f"a{i}" for i in range(1, 7)])
        self.assertEqual([i["row"]["seed"] for i in items], [1, 1, 2, 2])
        self.assertIn("4/4", self.printed)

    def test_one_query_for_all_chunks(self):
        self.prepare()
        self.assertEqual(len(self.conn.calls), 1)
        self.assertEqual(self.conn.calls[0][1][0], generate.CHUNK_SET)

    def test_mismatching_passages_stop_and_name_the_row(self):
        self.rows[1]["answer"]["system_message"] += " 다름"
        with self.assertRaises(ValueError) as cm:
            self.prepare()
        self.assertIn("q02-ko", str(cm.exception))
        self.assertIn("3/4", self.printed)

    def test_first_plan_passages_are_compared_with_the_first_plan_answer(self):
        # 처음 계획 줄의 최종 답 글이 달라도(고친 계획의 참고 글) 판 0은 처음 계획의 답이므로 통과한다
        self.rows[0]["answer"]["system_message"] = "다른 글"
        self.prepare()
        self.rows[0]["first_plan_answer"]["system_message"] += "x"
        with self.assertRaises(ValueError):
            self.prepare()

    def test_row_count_commit_and_dirty_are_checked(self):
        with self.assertRaises(ValueError):
            self.prepare(self.rows[:3])
        self.rows[2]["code_commit"] = "ac09906" + COMMIT[7:]
        with self.assertRaises(ValueError):
            self.prepare()
        self.rows[2]["code_commit"] = COMMIT
        self.rows[3]["code_dirty"] = True
        with self.assertRaises(ValueError):
            self.prepare()

    def test_missing_chunk_in_table_stops(self):
        del self.table["a4"]
        with self.assertRaises(ValueError) as cm:
            self.prepare()
        self.assertIn("a4", str(cm.exception))

    def test_default_expected_rows_is_190(self):
        self.assertEqual(run_answer.BASE_ROWS, 190)
        with self.assertRaises(ValueError):
            run_answer.check_base(self.rows)


class RunTest(WorldMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.path = Path(self.tmp.name) / "answer_cite" / "runs_v1.jsonl"
        with redirect_stdout(io.StringIO()):
            self.items = run_answer.prepare(self.conn, self.rows, self.questions, 4)

    def go(self, ollama, version="cite-en-v1", items=None):
        with patched(ollama, {}) as _, redirect_stdout(io.StringIO()) as printed:
            try:
                n = run_answer.run(version, items or self.items, self.path)
            finally:
                self.printed = printed.getvalue()
        return n, [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]

    def test_warmup_then_one_request_per_row_in_base_order(self):
        ollama = FakeOllama(answer=cite_answer([{"fact": "17.7", "chunks": [1]}]))
        n, rows = self.go(ollama)
        self.assertEqual((n, len(rows)), (4, 4))
        self.assertEqual([(r["seed"], r["question_id"]) for r in rows], [(1, "q01-ko"), (1, "q02-ko"), (2, "q01-ko"), (2, "q02-ko")])
        self.assertEqual(ollama.calls[0], (generate.GENERATE_URL, {"model": "qwen3:8b", "keep_alive": 0}))
        self.assertEqual(ollama.roles(), ["warmup"] + ["answer"] * 4)
        self.assertEqual(len([c for c in ollama.calls if c[0] == generate.GENERATE_URL]), 1)
        self.assertEqual([body["options"]["seed"] for _, body in ollama.requests[1:]], [1, 1, 2, 2])
        self.assertEqual(len(self.printed.strip().splitlines()), 1 + 4)
        self.assertEqual(len({r["run_id"] for r in rows}), 1)

    def test_request_is_the_schema_request_of_the_version_on_the_base_chunks(self):
        ollama = FakeOllama(answer=cite_answer([]))
        _, rows = self.go(ollama, version="cite-en-v2")
        _, body = ollama.requests[1]   # 첫 줄: q01-ko 씨앗 1, 처음 계획의 청크 4개
        self.assertEqual(body["format"], answer.schema(4))
        system_message, user_message = answer.messages_of("cite-en-v2", self.questions[0], self.items[0]["found"])
        self.assertEqual([m["content"] for m in body["messages"]], [system_message, user_message])
        self.assertEqual(ollama.requests[2][1]["format"], answer.schema(6))
        self.assertEqual(rows[0]["prompt_version"], "cite-en-v2+ctx-en-v1")

    def test_row_fields(self):
        ollama = FakeOllama(answer=cite_answer([{"fact": "17.7", "chunks": [2]}]))
        _, rows = self.go(ollama)
        r = rows[0]
        self.assertEqual((r["question_id"], r["lang"], r["seed"], r["generate_model"], r["answer_format"]), ("q01-ko", "ko", 1, "qwen3:8b", "schema"))
        self.assertEqual(r["answer_options"], generate.request_body("", "", 1)["options"])
        self.assertEqual(r["prompt_version"], "cite-en-v1+ctx-en-v1")
        self.assertEqual(len(r["code_commit"]), 40)
        self.assertIsInstance(r["code_dirty"], bool)
        self.assertEqual({k: r["source"][k] for k in ("run_id", "base_kind")}, {"run_id": "20261028T100000", "base_kind": "first_plan"})
        self.assertTrue(r["source"]["path"].endswith("runs.jsonl"))
        self.assertEqual(rows[1]["source"]["base_kind"], "final")
        self.assertEqual((r["n_chunks"], r["hit"], r["hit_ranks"]), (4, True, [2]))
        self.assertEqual([c["chunk_id"] for c in r["chunks"]], ["f1", "f2", "f3", "f4"])
        self.assertEqual(set(r["chunks"][0]), {"rank", "chunk_id", "doc_id", "line_start", "line_end"})
        self.assertEqual((rows[1]["n_chunks"], rows[1]["hit"], rows[1]["hit_ranks"]), (6, True, [3]))
        self.assertIsInstance(r["run_seconds"], float)
        a = r["answer"]
        self.assertEqual({k: a[k] for k in TIMES}, TIMES)
        self.assertEqual((a["user_message"], a["correct"], a["checks"]["cites_evidence"]), (Q1, True, True))   # 근거 칸 2번이 hit_ranks [2]
        self.assertEqual(a["cited"][0]["mapped"][0]["chunk_id"], "f2")
        self.assertNotIn("search", r)
        self.assertNotIn("plan", r)

    def test_stdout_line_shows_result_facts_flags_and_seconds(self):
        ollama = FakeOllama(answer=cite_answer([{"fact": "99", "chunks": [1]}]))
        self.go(ollama)
        line = self.printed.strip().splitlines()[1]
        for part in ("씨앗1 q01-ko", "맞음", "사실 1개", "근거 청크 안 가리킴", "잘못 붙은 인용 1", "s"):
            self.assertIn(part, line)

    def test_bad_shape_is_recorded_and_the_run_continues(self):
        n, rows = self.go(FakeOllama(answer="이건 JSON이 아니다"))
        self.assertEqual(n, 4)
        self.assertFalse(rows[0]["answer"]["checks"]["shape_ok"])
        self.assertIn("꼴 오류", self.printed)

    def test_other_ollama_error_stops_with_seed_and_question(self):
        with self.assertRaises(RuntimeError) as cm:
            self.go(FakeOllama(answer=FakeResponse("앞 글", error="model runner has unexpectedly stopped")))
        for part in ("씨앗1", "q01-ko", "answer에서 멈춤", "model runner has unexpectedly stopped"):
            self.assertIn(part, str(cm.exception))

    def test_token_repeat_limit_is_recorded_not_stopped(self):
        n, rows = self.go(FakeOllama(answer=FakeResponse('{"reason": "앞', error="token repeat limit reached")))
        self.assertEqual(n, 4)
        self.assertTrue(rows[0]["answer"]["aborted"])
        self.assertTrue(rows[0]["answer"]["checks"]["aborted"])

    def test_existing_file_stops_before_any_request_and_is_kept(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("첫 실행의 기록\n", encoding="utf-8")
        ollama = FakeOllama()
        with self.assertRaises(FileExistsError):
            self.go(ollama)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "첫 실행의 기록\n")
        self.assertEqual(ollama.calls, [])


class MainTest(WorldMixin, unittest.TestCase):
    """명령 인자, 기록 경로, 시작 전 확인을 본다. 데이터베이스 연결은 가짜로 바꾼다."""

    def setUp(self):
        super().setUp()
        root = Path(self.tmp.name)
        self.base = root / "plan_search" / "runs.jsonl"
        self.base.parent.mkdir()
        self.base.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in self.rows), encoding="utf-8")
        self.questions_path = root / "questions.json"
        self.questions_path.write_text(json.dumps(self.questions, ensure_ascii=False), encoding="utf-8")
        self.default = root / "answer_cite" / "runs_v1.jsonl"
        self.ollama = FakeOllama(answer=cite_answer([{"fact": "17.7", "chunks": [1]}]))

    def call_main(self, argv):
        runs = {"cite-en-v1": self.default, "cite-en-v2": self.default.with_name("runs_v2.jsonl")}
        with mock.patch.object(run_answer, "BASE_RUNS", self.base), mock.patch.object(run_answer, "QUESTIONS", self.questions_path), \
                mock.patch.object(run_answer, "RUNS", runs), mock.patch.object(run_answer, "BASE_ROWS", 4), \
                mock.patch.object(psycopg, "connect", lambda dsn: mock.MagicMock(__enter__=lambda s: self.conn)), \
                patched(self.ollama, {}), redirect_stdout(io.StringIO()) as printed, redirect_stderr(io.StringIO()):
            try:
                run_answer.main(argv)
            finally:
                self.printed = printed.getvalue()

    def written(self, path=None):
        return [json.loads(line) for line in (path or self.default).read_text(encoding="utf-8").splitlines()]

    def test_real_default_paths(self):
        self.assertEqual(run_answer.RUNS["cite-en-v1"], run_answer.ROOT / "data" / "agent" / "answer_cite" / "runs_v1.jsonl")
        self.assertEqual(run_answer.RUNS["cite-en-v2"], run_answer.ROOT / "data" / "agent" / "answer_cite" / "runs_v2.jsonl")
        self.assertEqual(run_answer.BASE_RUNS, run_answer.ROOT / "data" / "agent" / "plan_search" / "runs.jsonl")

    def test_version_is_required_and_must_be_known(self):
        for argv in ([], ["--version", "cite-en-v9"]):
            with self.assertRaises(SystemExit):
                self.call_main(argv)

    def test_full_run_writes_all_rows_at_the_default_path_of_the_version(self):
        self.call_main(["--version", "cite-en-v1"])
        self.assertEqual(len(self.written()), 4)
        self.assertEqual(self.ollama.roles(), ["warmup"] + ["answer"] * 4)
        self.call_main(["--version", "cite-en-v2"])
        self.assertEqual(len(self.written(self.default.with_name("runs_v2.jsonl"))), 4)
        self.assertEqual(self.written(self.default.with_name("runs_v2.jsonl"))[0]["prompt_version"], "cite-en-v2+ctx-en-v1")

    def test_questions_or_seeds_without_out_is_refused(self):
        for extra in (["--questions", "q01-ko"], ["--seeds", "1"], ["--questions", "q01-ko", "--seeds", "1"]):
            with self.assertRaises(SystemExit) as cm:
                self.call_main(["--version", "cite-en-v1", *extra])
            self.assertEqual(cm.exception.code, 2, extra)
        self.assertEqual(self.ollama.calls, [])

    def test_partial_run_cannot_write_to_the_default_path(self):
        with self.assertRaises(SystemExit):
            self.call_main(["--version", "cite-en-v1", "--questions", "q01-ko", "--out", str(self.default)])
        self.assertEqual(self.ollama.calls, [])

    def test_partial_run_with_out_keeps_base_order_and_checks_all_base_rows(self):
        out = Path(self.tmp.name) / "short.jsonl"
        self.call_main(["--version", "cite-en-v1", "--questions", "q02-ko,q01-ko", "--seeds", "2", "--out", str(out)])
        self.assertEqual([(r["seed"], r["question_id"]) for r in self.written(out)], [(2, "q01-ko"), (2, "q02-ko")])
        self.assertIn("4/4", self.printed)   # 대조는 ⑧ 기록 전체에 한다

    def test_unknown_question_and_seed_are_refused(self):
        out = Path(self.tmp.name) / "short.jsonl"
        for extra in (["--questions", "q99-xx"], ["--seeds", "7"]):
            with self.assertRaises(SystemExit):
                self.call_main(["--version", "cite-en-v1", *extra, "--out", str(out)])
        self.assertEqual(self.ollama.calls, [])

    def test_existing_out_file_is_refused_before_any_request(self):
        out = Path(self.tmp.name) / "short.jsonl"
        out.write_text("x\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.call_main(["--version", "cite-en-v1", "--questions", "q01-ko", "--out", str(out)])
        self.assertEqual(self.ollama.calls, [])

    def test_existing_default_file_is_refused_before_any_request(self):
        self.default.parent.mkdir()
        self.default.write_text("첫 실행의 기록\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.call_main(["--version", "cite-en-v1"])
        self.assertEqual(self.default.read_text(encoding="utf-8"), "첫 실행의 기록\n")
        self.assertEqual(self.ollama.calls, [])

    def test_mismatching_passages_stop_before_the_model_is_called(self):
        self.rows[1]["answer"]["system_message"] += " 다름"
        self.base.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in self.rows), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.call_main(["--version", "cite-en-v1"])
        self.assertEqual(self.ollama.calls, [])
        self.assertFalse(self.default.exists())

    def test_wrong_row_count_stops_before_the_model_is_called(self):
        self.base.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in self.rows[:3]), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.call_main(["--version", "cite-en-v1"])
        self.assertEqual(self.ollama.calls, [])

    def test_check_only_compares_and_never_calls_the_model_or_writes(self):
        self.call_main(["--version", "cite-en-v1", "--check-only"])
        self.assertEqual(self.ollama.calls, [])
        self.assertFalse(self.default.exists())
        self.assertIn("4/4", self.printed)


if __name__ == "__main__":
    unittest.main()
