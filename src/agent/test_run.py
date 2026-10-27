"""src/agent/run.py(190번 실행)와 src/agent/pair_search.py(짝 질문 검색)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama와 실제 데이터베이스를 쓰지 않는다. urlopen과 검색을 가짜로 바꾸고(fakes.py), 파일은 임시 폴더에 쓴다(data/agent/에는 쓰지 않는다).
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
import generate  # noqa: E402
import pair_search  # noqa: E402
import plan  # noqa: E402
import run  # noqa: E402
from fakes import TIMES, FakeOllama, FakeResponse, found_row, patched, plan_output, question  # noqa: E402

Q1, Q2 = "반감기는 몇 시간인가?", "다른 질문인가?"
Q1_EN = "What is the half-life in hours?"


def plan_n(n):
    return plan_output(f"한국어판{n}", f"english{n}")


def searches():
    table = {text: [found_row(f"{tag}{i}", text=f"{tag}{i} 글", evidence=(tag == "a" and i == 3)) for i in range(1, 17)]
             for tag, text in (("o", Q1), ("a", Q2))}
    table["한국어판1"] = [found_row(f"k1-{i}", text=f"k1-{i} 글") for i in range(1, 5)]
    table["english1"] = [found_row(f"e1-{i}", text=f"e1-{i} 글") for i in range(1, 5)]
    return table


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "plan_search" / "runs.jsonl"
        self.questions = [question("q01-ko", "ko", Q1), question("q02-ko", "ko", Q2)]

    def go(self, ollama, seeds=(1,), questions=None):
        with patched(ollama, searches()) as calls, redirect_stdout(io.StringIO()) as printed:
            try:
                n = run.run(questions or self.questions, self.path, None, None, seeds=seeds)
            finally:
                self.calls, self.printed = calls, printed.getvalue()
        return n, [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]

    def test_warmup_order_and_count(self):
        ollama = FakeOllama(plans=[plan_n(1)] * 4)
        n, rows = self.go(ollama, seeds=(1, 2))
        self.assertEqual((n, len(rows)), (4, 4))
        self.assertEqual([(r["seed"], r["question_id"]) for r in rows], [(1, "q01-ko"), (1, "q02-ko"), (2, "q01-ko"), (2, "q02-ko")])
        # 생성 모델을 내리고, 몸풀기 호출을 한 번(씨앗 1): PLAN_SYSTEM + 안녕. 판정 모델은 없다
        self.assertEqual(ollama.calls[0], (generate.GENERATE_URL, {"model": "qwen3:8b", "keep_alive": 0}))
        self.assertEqual(ollama.calls[1][1], plan.plan_body("안녕", 1))
        self.assertEqual(len(ollama.requests), 1 + 4 * 2)   # 몸풀기 하나 + 실행 4번 × (계획, 답)
        self.assertEqual(len([c for c in ollama.calls if c[0] == generate.GENERATE_URL]), 1)
        self.assertNotIn("안녕", [r["plan_step"]["user_message"] for r in rows])
        # 요청은 한 번에 하나씩, 씨앗 1의 실행 둘 다음에 씨앗 2의 실행 둘 순서이고 모든 요청이 그 실행의 씨앗을 쓴다
        self.assertEqual([body["options"]["seed"] for _, body in ollama.requests[1:]], [1] * 4 + [2] * 4)
        self.assertEqual(len(self.printed.strip().splitlines()), 1 + 4)
        self.assertEqual(len({r["run_id"] for r in rows}), 1)

    def test_row_fields(self):
        ollama = FakeOllama(plans=[plan_n(1)])
        _, rows = self.go(ollama, questions=self.questions[:1])
        r = rows[0]
        self.assertEqual((r["question_id"], r["lang"], r["branch"], r["seed"]), ("q01-ko", "ko", "한국어만", 1))
        self.assertEqual(r["generate_model"], "qwen3:8b")
        self.assertEqual(r["plan_options"], plan.plan_body("", 1)["options"])
        self.assertEqual(r["plan_options"]["temperature"], 0)
        self.assertEqual(r["answer_options"], generate.request_body("", "", 1)["options"])
        self.assertEqual(r["prompt_version"], {"plan": "plan-en-v1", "answer": "en-v1+ctx-en-v1"})
        self.assertEqual(len(r["code_commit"]), 40)
        self.assertIsInstance(r["code_dirty"], bool)
        self.assertRegex(r["langgraph_version"], r"^\d+\.\d+")
        self.assertIsNone(r["shape_error"])
        self.assertEqual(r["plan"], r["plan_step"]["plan"])
        self.assertEqual(r["plan"]["reason"], "생각")
        self.assertEqual((r["search"]["n_chunks"], r["search"]["hit"]), (16, False))
        self.assertEqual([q["name"] for q in r["search"]["queries"]], ["original", "korean", "english"])
        self.assertEqual(len(r["comparison_retrieved"]), 16)
        self.assertEqual([c["chunk_id"] for c in r["comparison_retrieved"][:8]], [c["chunk_id"] for c in r["search"]["merged"][:8]])
        self.assertEqual((r["answer"]["user_message"], r["answer"]["correct"]), (Q1, True))
        self.assertNotIn("merged_found", r)
        self.assertNotIn("started_at", r)

    def test_row_has_no_judgment_fields(self):
        _, rows = self.go(FakeOllama(plans=[plan_n(1)]), questions=self.questions[:1])
        for key in ("judge_model", "judge_options", "judgments", "n_judgments", "n_refinements", "plan_passed", "first_plan", "final_plan",
                    "plan_steps", "first_plan_search", "first_plan_answer"):
            self.assertNotIn(key, rows[0], key)

    def test_row_has_run_seconds_node_times_and_request_times(self):
        _, rows = self.go(FakeOllama(plans=[plan_n(1)]), questions=self.questions[:1])
        r = rows[0]
        self.assertIsInstance(r["run_seconds"], float)
        self.assertEqual([t["node"] for t in r["node_times"]], ["generate", "search", "answer"])
        self.assertGreaterEqual(r["run_seconds"], r["node_times"][-1]["end"])   # invoke 한 번이 칸들을 모두 품는다
        for record in (r["plan_step"], r["answer"]):
            self.assertEqual({key: record[key] for key in ("prompt_eval_seconds", "eval_seconds", "load_seconds")}, TIMES)

    def test_comparison_uses_evidence_of_the_original_question(self):
        # q02의 원래 질문 3등이 근거다. 비교용 16개에 근거 번호가 매겨지고 합친 목록도 hit다
        ollama = FakeOllama(plans=[plan_n(1)])
        _, rows = self.go(ollama, questions=self.questions[1:])
        r = rows[0]
        self.assertEqual([c["rank"] for c in r["comparison_retrieved"] if c["evidence"]], [3])
        self.assertEqual((r["search"]["hit"], r["search"]["hit_ranks"]), (True, [3]))

    def test_shape_error_run_stops_and_next_run_continues(self):
        ollama = FakeOllama(plans=["이건 JSON이 아니다", plan_n(1)])
        n, rows = self.go(ollama)
        self.assertEqual(n, 2)
        bad, good = rows
        self.assertEqual((bad["question_id"], bad["shape_error"]["stage"], bad["shape_error"]["output"]), ("q01-ko", "generate", "이건 JSON이 아니다"))
        self.assertEqual(bad["shape_error"]["system_message"], plan.PLAN_SYSTEM)
        for key in ("search", "answer", "comparison_retrieved", "plan"):
            self.assertIsNone(bad[key], key)
        self.assertEqual([t["node"] for t in bad["node_times"]], ["generate"])   # 꼴 오류 실행은 search·answer 칸을 지나가지 않았다
        self.assertIsInstance(bad["run_seconds"], float)
        self.assertEqual(ollama.roles()[1:], ["plan", "plan", "answer"])
        self.assertIsNone(good["shape_error"])
        self.assertEqual(len(good["comparison_retrieved"]), 16)
        self.assertEqual([c[0] for c in self.calls], [Q2, "한국어판1", "english1", Q2])   # 꼴 오류 실행은 검색(비교용 포함)을 하지 않았다
        self.assertIn("꼴 오류", self.printed)

    def test_other_ollama_error_stops_whole_run_with_where(self):
        ollama = FakeOllama(plans=[plan_n(1), FakeResponse("앞 글", error="model runner has unexpectedly stopped")])
        with self.assertRaises(RuntimeError) as cm:
            self.go(ollama)
        message = str(cm.exception)
        for part in ("씨앗1", "q02-ko", "generate에서 멈춤", "model runner has unexpectedly stopped"):
            self.assertIn(part, message)
        rows = self.path.read_text(encoding="utf-8").splitlines()
        self.assertEqual([json.loads(line)["question_id"] for line in rows], ["q01-ko"])   # 끝난 줄은 이미 쓰여 있다

    def test_existing_file_stops_and_is_kept(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("첫 실행의 기록\n", encoding="utf-8")
        ollama = FakeOllama()
        with self.assertRaises(FileExistsError):
            self.go(ollama)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "첫 실행의 기록\n")
        self.assertEqual(ollama.calls, [])   # 모델 내리기도 몸풀기도 하지 않는다


class MainTest(unittest.TestCase):
    """명령 인자와 기록 경로 규칙을 본다. run, 모델 불러오기, DB 연결은 가짜로 바꿔 불린 것만 센다."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.default = Path(self.tmp.name) / "runs.jsonl"

    def call_main(self, argv):
        calls = []
        fake_run = lambda questions, path, conn, model, **kw: calls.append(("run", [q["id"] for q in questions], path, kw)) or 0
        with mock.patch.object(run, "RUNS", self.default), mock.patch.object(run, "run", fake_run), \
                mock.patch.object(run, "load_model", lambda key: calls.append(("load_model", key)) or "MODEL"), \
                mock.patch.object(psycopg, "connect", lambda dsn: calls.append(("connect", dsn)) or mock.MagicMock()), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            run.main(argv)
        return calls

    def test_real_default_path(self):
        self.assertEqual(run.RUNS, run.ROOT / "data" / "agent" / "plan_search" / "runs.jsonl")

    def test_full_run_uses_all_questions_and_seeds_at_default_path(self):
        calls = self.call_main([])
        self.assertEqual([c[0] for c in calls], ["load_model", "connect", "run"])
        _, ids, path, kw = calls[2]
        self.assertEqual((len(ids), path, kw), (38, self.default, {"seeds": (1, 2, 3, 4, 5)}))

    def test_default_path_is_refused_when_file_exists_before_loading_anything(self):
        self.default.write_text("첫 실행의 기록\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.call_main([])
        self.assertEqual(self.default.read_text(encoding="utf-8"), "첫 실행의 기록\n")

    def test_existing_out_file_is_refused(self):
        out = Path(self.tmp.name) / "short.jsonl"
        out.write_text("x\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.call_main(["--questions", "q01-ko", "--out", str(out)])

    def test_questions_or_seeds_without_out_is_refused(self):
        for argv in (["--questions", "q01-ko"], ["--seeds", "1"], ["--questions", "q01-ko", "--seeds", "1"]):
            with self.assertRaises(SystemExit) as cm:
                self.call_main(argv)
            self.assertEqual(cm.exception.code, 2, argv)

    def test_partial_run_cannot_write_to_the_default_path(self):
        with self.assertRaises(SystemExit):
            self.call_main(["--questions", "q01-ko", "--out", str(self.default)])

    def test_partial_run_with_out(self):
        out = Path(self.tmp.name) / "short" / "runs.jsonl"
        calls = self.call_main(["--questions", "q03-en,q01-ko", "--seeds", "1", "--out", str(out)])
        _, ids, path, kw = calls[-1]
        self.assertEqual((ids, path, kw), (["q01-ko", "q03-en"], out, {"seeds": (1,)}))   # 질문은 파일의 순서

    def test_unknown_question_and_seed_are_refused(self):
        out = Path(self.tmp.name) / "short.jsonl"
        for argv in (["--questions", "q99-xx", "--out", str(out)], ["--seeds", "7", "--out", str(out)]):
            with self.assertRaises(SystemExit):
                self.call_main(argv)


class PairSearchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "pair_search.jsonl"
        self.questions = [question("q01-ko", "ko", Q1, "q01-en"), question("q01-en", "en", Q1_EN, "q01-ko")]

    def go(self, table):
        with patched(None, table) as calls, redirect_stdout(io.StringIO()):
            n = pair_search.run(self.questions, self.path, None, None)
        return n, [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()], calls

    def test_one_row_per_question_with_pair_merge(self):
        # 영어 질문의 짝은 한국어 질문이다. 영어 질문의 원래 8개는 Q1_EN 검색 결과의 위 8개
        table = {Q1: [found_row(f"o{i}", text=f"o{i} 글") for i in range(1, 17)],
                 Q1_EN: [found_row("o2"), found_row("p1", evidence=True), found_row("p2"), found_row("p3"), found_row("p4")]
                 + [found_row(f"q{i}") for i in range(1, 12)]}
        n, rows, calls = self.go(table)
        self.assertEqual((n, [r["question_id"] for r in rows], [r["pair_id"] for r in rows]), (2, ["q01-ko", "q01-en"], ["q01-en", "q01-ko"]))
        ko = rows[0]
        # 한국어 질문: 원래 8개 + 영어 짝 질문 위 4개(o2, p1, p2, p3) 중 겹치지 않는 p1, p2, p3. 근거는 원래 질문의 evidence로 센다
        self.assertEqual([c["chunk_id"] for c in ko["search"]["merged"]], [f"o{i}" for i in range(1, 9)] + ["p1", "p2", "p3"])
        self.assertEqual([q["name"] for q in ko["search"]["queries"]], ["original", "pair"])
        self.assertEqual((ko["search"]["n_chunks"], ko["search"]["hit"], ko["search"]["hit_ranks"]), (11, True, [9]))
        self.assertEqual(len(ko["comparison_retrieved"]), 16)
        self.assertEqual((ko["lang"], ko["branch"], len(ko["code_commit"])), ("ko", "한국어만", 40))
        self.assertIsInstance(ko["code_dirty"], bool)
        self.assertEqual(calls[:3], [(Q1, 8), (Q1_EN, 4), (Q1, 16)])

    def test_same_text_as_pair_is_skipped(self):
        self.questions = [question("q01-ko", "ko", Q1, "q01-en"), question("q01-en", "en", " " + Q1 + " ", "q01-ko")]
        table = {Q1: [found_row(f"o{i}") for i in range(1, 17)], " " + Q1 + " ": [found_row(f"o{i}") for i in range(1, 17)]}
        _, rows, calls = self.go(table)
        self.assertTrue(rows[0]["search"]["queries"][1]["skipped"])
        self.assertEqual(rows[0]["search"]["n_chunks"], 8)

    def test_existing_file_stops(self):
        self.path.write_text("첫 기록\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.go({})
        self.assertEqual(self.path.read_text(encoding="utf-8"), "첫 기록\n")


if __name__ == "__main__":
    unittest.main()
