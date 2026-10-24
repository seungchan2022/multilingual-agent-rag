"""src/minimal/generate.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

Ollama를 부르지 않는다. 요청을 보내는 urllib.request.urlopen을 가짜로 바꿔 끼우고, 보낸 요청 본문을 붙잡아 본다.
실행 순서 시험은 실제 multilingual_rag를 건드리지 않게 시험용 데이터베이스 multilingual_rag_test를 만들어 쓰고 끝나면 지운다.
모델은 불러오지 않고 embed_query를 고정 벡터를 돌려주는 함수로 바꾼다. 파일을 쓰는 시험은 임시 폴더에 쓴다(data/minimal/generation/에는 쓰지 않는다).
"""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import numpy as np
import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402
import index  # noqa: E402

ADMIN_DSN = "dbname=multilingual_rag"  # 시험용 데이터베이스를 만들고 지우는 연결(실제 표는 건드리지 않는다)
TEST_DB = "multilingual_rag_test"
DIM = 8


def found_row(n, doc_id="doc-a", text="청크 글", lines=(3, 4)):
    """search가 돌려주는 한 줄 (chunk_id, distance, doc_id, lines, text, tokens, language, line_start, line_end)."""
    return (f"{doc_id}#{n:04d}", 0.1 * n, doc_id, list(lines), text, 50, "en", min(lines), max(lines))


def question(qid="q01-ko", lang="ko", value=17.7, text="반감기는 몇 시간인가?"):
    return {"id": qid, "lang": lang, "branch": "한국어만", "question": text, "value": value, "unit": "kg", "answer": f"{value} kg",
            "evidence": [{"doc_id": "doc-a", "line": 5, "value_text": "17.7"}]}


class FakeResponse:
    """stream 응답 하나. 줄 단위로 읽힌다. 글은 두 조각으로 나눠 오고, 끝에 done 줄이 온다. error를 주면 done 줄 대신 error 줄이 온다."""

    def __init__(self, content, eval_count=12, prompt_eval_count=345, error=None):
        cut = len(content) // 2
        lines = [{"message": {"role": "assistant", "content": piece}, "done": False} for piece in (content[:cut], content[cut:]) if piece]
        lines.append({"error": error} if error else
                     {"message": {"role": "assistant", "content": ""}, "done": True, "eval_count": eval_count, "prompt_eval_count": prompt_eval_count})
        self.lines = [(json.dumps(line, ensure_ascii=False) + "\n").encode() for line in lines]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def __iter__(self):
        return iter(self.lines)

    def read(self):
        return b'{"done": true}'


class FakeOllama:
    """urlopen을 대신한다. 모든 요청을 순서대로 calls에, 채팅 요청 본문만 requests에 쌓고, 정해진 글을 돌려준다.
    responses는 {채팅 요청 번호(0이 몸풀기): FakeResponse}로, 그 번호의 요청에만 다른 응답을 준다."""

    def __init__(self, content='{"reason": "계산", "answer": "17.7 시간"}', responses=None):
        self.content = content
        self.responses = responses or {}
        self.requests = []
        self.calls = []

    def __call__(self, req, timeout=None):
        body = json.loads(req.data)
        self.calls.append((req.full_url, body))
        if req.full_url == g.GENERATE_URL:
            return FakeResponse("")
        assert req.full_url == "http://localhost:11434/api/chat", req.full_url
        self.requests.append(body)
        return self.responses.get(len(self.requests) - 1) or FakeResponse(self.content)


def http_error(code=500, body="model runner has unexpectedly stopped".encode()):
    return g.urllib.error.HTTPError(g.URL, code, "Internal Server Error", {}, io.BytesIO(body))


class MessagesTest(unittest.TestCase):
    def test_baseline_has_only_instruction_and_question(self):
        system, user = g.messages_of("baseline", question())
        self.assertEqual(system, g.SYSTEM_EN)
        self.assertEqual(user, "반감기는 몇 시간인가?")
        self.assertNotIn("Reference passages", system + user)
        self.assertNotIn("청크 글", system + user)

    def test_minimal_passages_format(self):
        found = [found_row(1, "doc-a", "첫 청크\n둘째 줄", (3, 4, 9)), found_row(2, "doc-b", "다른 청크", (7,))]
        system, user = g.messages_of("minimal", question(), found)
        expected = ("[1] doc-a (lines 3-9)\n첫 청크\n둘째 줄\n\n"
                    "[2] doc-b (lines 7-7)\n다른 청크")
        self.assertEqual(g.passages_of(found), expected)
        self.assertEqual(system, g.SYSTEM_EN + "\n\nAnswer based on the reference passages below.\nReference passages:\n" + expected)
        self.assertEqual(user, "반감기는 몇 시간인가?")

    def test_minimal_uses_chunk_columns_for_lines_not_lines_list(self):
        # 표 조각처럼 줄이 끊긴 청크: lines 표시는 line_start-line_end(9-40)이지 줄 목록이 아니다
        found = [(f"x#1", 0.1, "doc-a", [9, 10, 11, 40], "머리글 행", 20, "ko", 9, 40)]
        self.assertTrue(g.passages_of(found).startswith("[1] doc-a (lines 9-40)\n"))

    def test_constants_match_check_language(self):
        spec = importlib.util.spec_from_file_location("check_language", g.ROOT / "research_notes" / "stage4_answer_language" / "check_language.py")
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        self.assertEqual(g.SYSTEM_EN, old.SYSTEM_EN)
        self.assertEqual(g.CONTEXT_EN, old.CONTEXT_EN)


class RequestTest(unittest.TestCase):
    def test_body_matches_spec(self):
        fake = FakeOllama()
        with mock.patch.object(g.urllib.request, "urlopen", fake):
            content, seconds, tokens, prompt_tokens, abort_reason = g.chat("지시문", "질문", 3)
        self.assertEqual((content, tokens, prompt_tokens, abort_reason), ('{"reason": "계산", "answer": "17.7 시간"}', 12, 345, None))
        body = fake.requests[0]
        self.assertEqual(body["model"], "qwen3:8b")
        self.assertIs(body["think"], False)
        self.assertEqual(body["format"], "json")
        self.assertIs(body["stream"], True)
        self.assertEqual(body["options"], {"temperature": 0.7, "top_p": 0.8, "top_k": 20, "min_p": 0, "num_predict": 2048,
                                           "num_ctx": 32768, "seed": 3})
        self.assertEqual(body["messages"], [{"role": "system", "content": "지시문"}, {"role": "user", "content": "질문"}])
        self.assertNotIn("tools", body)


    def test_http_error_becomes_runtime_error_with_code_and_body(self):
        def fail(req, timeout=None):
            raise http_error(500, "모델 오류 {\"error\": \"runner stopped\"}".encode())
        with mock.patch.object(g.urllib.request, "urlopen", fail), self.assertRaises(RuntimeError) as cm:
            g.chat("지시문", "질문", 1)
        self.assertEqual(str(cm.exception), 'Ollama HTTP 500: 모델 오류 {"error": "runner stopped"}')
        self.assertIsInstance(cm.exception.__cause__, g.urllib.error.HTTPError)

    def test_undecodable_body_is_replaced(self):
        def fail(req, timeout=None):
            raise http_error(500, b"bad \xff byte")
        with mock.patch.object(g.urllib.request, "urlopen", fail), self.assertRaises(RuntimeError) as cm:
            g.chat("지시문", "질문", 1)
        self.assertIn("HTTP 500: bad \ufffd byte", str(cm.exception))


    def test_stream_pieces_are_joined(self):
        with mock.patch.object(g.urllib.request, "urlopen", FakeOllama("가나다라마바사")):
            content, _, tokens, prompt_tokens, abort_reason = g.chat("지시문", "질문", 1)
        self.assertEqual((content, tokens, prompt_tokens, abort_reason), ("가나다라마바사", 12, 345, None))

    def test_token_repeat_limit_returns_partial_text(self):
        fake = FakeOllama(responses={0: FakeResponse('{"reason": "r", "answer": "0.0000000', error="prediction aborted, token repeat limit reached")})
        with mock.patch.object(g.urllib.request, "urlopen", fake):
            content, _, tokens, prompt_tokens, abort_reason = g.chat("지시문", "질문", 1)
        self.assertEqual(content, '{"reason": "r", "answer": "0.0000000')
        self.assertEqual((tokens, prompt_tokens, abort_reason), (None, None, "prediction aborted, token repeat limit reached"))

    def test_other_error_line_stops(self):
        fake = FakeOllama(responses={0: FakeResponse("앞 글", error="model runner has unexpectedly stopped")})
        with mock.patch.object(g.urllib.request, "urlopen", fake), self.assertRaises(RuntimeError) as cm:
            g.chat("지시문", "질문", 1)
        self.assertEqual(str(cm.exception), "Ollama 오류: model runner has unexpectedly stopped")

    def test_unload_request(self):
        fake = FakeOllama()
        with mock.patch.object(g.urllib.request, "urlopen", fake):
            g.unload_model()
        self.assertEqual(fake.calls, [("http://localhost:11434/api/generate", {"model": "qwen3:8b", "keep_alive": 0})])


class LanguageTest(unittest.TestCase):
    def test_hangul_more_is_ko(self):
        self.assertEqual(g.language_of("계산 결과 17.7 h"), ("ko", 4, 1))

    def test_latin_more_is_en(self):
        self.assertEqual(g.language_of("The answer is 17.7 시간"), ("en", 2, 11))

    def test_equal_is_ko(self):
        self.assertEqual(g.language_of("가나 ab"), ("ko", 2, 2))

    def test_no_letters_is_ko(self):
        self.assertEqual(g.language_of("17.7"), ("ko", 0, 0))


def graded(answer, value=17.7, lang="ko", reason="풀이", raw=None):
    output = raw if raw is not None else json.dumps({"reason": reason, "answer": answer}, ensure_ascii=False)
    return g.graded(question(value=value, lang=lang), output)


class GradeTest(unittest.TestCase):
    def test_last_number_is_picked(self):
        r = graded("17.7 시간이 아니라 18 시간 중 17.7")
        self.assertEqual((r["numbers"], r["picked"], r["correct"]), ([17.7, 18.0, 17.7], 17.7, True))
        r = graded("17.7 시간이 아니라 5")
        self.assertEqual((r["picked"], r["correct"]), (5.0, False))

    def test_comma_is_removed(self):
        r = graded("1,234.5 g", value=1234.5)
        self.assertEqual((r["numbers"], r["correct"]), ([1234.5], True))

    def test_one_percent_boundary(self):
        self.assertTrue(graded("100.9", value=100)["correct"])
        self.assertTrue(graded("99.1", value=100)["correct"])
        self.assertTrue(graded("101", value=100)["correct"])   # 경계는 안이다
        self.assertFalse(graded("101.01", value=100)["correct"])
        self.assertFalse(graded("98.9", value=100)["correct"])

    def test_negative_number(self):
        r = graded("-3.5", value=-3.5)
        self.assertEqual((r["picked"], r["correct"]), (-3.5, True))

    def test_no_number(self):
        r = graded("모른다")
        self.assertEqual((r["numbers"], r["picked"], r["correct"], r["value"]), ([], None, False, 17.7))

    def test_broken_json(self):
        r = graded(None, raw='{"reason": "풀이", "answer": "17.')
        self.assertEqual((r["parsed_ok"], r["reason"], r["answer"], r["numbers"], r["picked"], r["correct"]), (False, "", "", [], None, False))
        self.assertEqual(r["unit"], "없음")
        self.assertEqual((r["answer_lang"], r["hangul"], r["latin"], r["lang_ok"]), (None, None, None, False))

    def test_json_but_not_dict(self):
        r = graded(None, raw="[17.7]")
        self.assertEqual((r["parsed_ok"], r["correct"], r["answer_lang"]), (False, False, None))

    def test_missing_keys_are_empty(self):
        r = graded(None, raw='{"answer": "17.7"}')
        self.assertEqual((r["parsed_ok"], r["reason"], r["correct"]), (True, "", True))

    def test_error_notation_is_correct_in_record(self):
        # 오차 표기(621.4(11))를 숫자로 세지 않으므로 마지막 숫자가 621.4다(예전 규칙은 11을 골라 틀렸다)
        r = g.graded(question(value=621.4), json.dumps({"reason": "읽는다", "answer": "621.4(11) keV"}, ensure_ascii=False))
        self.assertEqual((r["numbers"], r["picked"], r["correct"]), ([621.4], 621.4, True))
        self.assertEqual(r["unit"], "다름")   # 이 시험의 질문 단위는 kg라 keV와 다르다

    def test_unit_field(self):
        self.assertEqual(graded("17.7 kg")["unit"], "같음")
        self.assertEqual(graded("17.7 kg입니다")["unit"], "같음")
        self.assertEqual(graded("17.7 g")["unit"], "다름")
        self.assertEqual(graded("17.7")["unit"], "없음")
        self.assertTrue(graded("17.7 g")["correct"])   # 단위는 맞음을 바꾸지 않는다

    def test_language_fields(self):
        r = graded("17.7 시간", reason="반감기를 읽는다", lang="ko")
        self.assertEqual((r["answer_lang"], r["lang_ok"]), ("ko", True))
        self.assertGreater(r["hangul"], r["latin"])
        r = graded("17.7 hours", reason="Read the half-life", lang="ko")
        self.assertEqual((r["answer_lang"], r["lang_ok"]), ("en", False))
        r = graded("17.7 hours", reason="Read the half-life", lang="en")
        self.assertTrue(r["lang_ok"])


class MainTest(unittest.TestCase):
    """명령 인자에 따라 기록 파일과 시스템이 갈리는지 본다. run, 모델 불러오기, DB 연결은 가짜로 바꿔 불린 것만 센다."""

    def call_main(self, argv):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        paths = {s: Path(self.tmp.name) / f"runs_{s}.jsonl" for s in g.SYSTEMS}
        calls = []
        fake_run = lambda questions, path, conn, model, **kw: calls.append(("run", path, conn, model, kw)) or 190
        with mock.patch.dict(g.RUNS, paths), mock.patch.object(g, "run", fake_run), \
                mock.patch.object(g, "load_model", lambda key: calls.append(("load_model", key)) or "MODEL"), \
                mock.patch.object(psycopg, "connect", lambda dsn: calls.append(("connect", dsn)) or mock.MagicMock()), \
                redirect_stdout(io.StringIO()):
            g.main(argv)
        return paths, calls

    def test_real_paths_are_per_system(self):
        self.assertEqual({s: p.name for s, p in g.RUNS.items()}, {"baseline": "runs_baseline.jsonl", "minimal": "runs_minimal.jsonl"})
        self.assertEqual({p.parent for p in g.RUNS.values()}, {g.ROOT / "data" / "minimal" / "generation"})

    def test_baseline_loads_no_model_and_no_db(self):
        paths, calls = self.call_main(["--system", "baseline"])
        self.assertEqual([c[0] for c in calls], ["run"])
        _, path, conn, model, kw = calls[0]
        self.assertEqual((path, conn, model, kw), (paths["baseline"], None, None, {"systems": ("baseline",)}))

    def test_minimal_loads_model_and_connects(self):
        paths, calls = self.call_main(["--system", "minimal"])
        self.assertEqual([c[0] for c in calls], ["load_model", "connect", "run"])
        self.assertEqual(calls[0][1], "bge-m3")
        _, path, conn, model, kw = calls[2]
        self.assertEqual((path, model, kw), (paths["minimal"], "MODEL", {"systems": ("minimal",)}))

    def test_system_is_required_and_checked(self):
        for argv in ([], ["--system", "other"]):
            with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
                self.call_main(argv)

    def test_existing_file_stops_before_loading_anything(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name) / "runs_minimal.jsonl"
        path.write_text("첫 실행의 기록\n", encoding="utf-8")
        calls = []
        with mock.patch.dict(g.RUNS, {"minimal": path}), mock.patch.object(g, "load_model", lambda key: calls.append(key)), \
                self.assertRaises(FileExistsError):
            g.main(["--system", "minimal"])
        self.assertEqual(calls, [])


class RunTest(unittest.TestCase):
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
        vectors = rng.normal(size=(3, DIM)).astype(np.float32)
        vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
        self.query_vector = vectors[1]   # 두 번째 청크와 같은 벡터라 1위가 된다
        rows = [{"chunk_id": f"doc-a#{n}", "doc_id": "doc-a", "language": "en", "size": 128, "title": True, "kind": "text", "path": "A",
                 "text": text, "line_start": 4, "line_end": 6, "lines": [4, 5, 6], "tokens": 9, "over_limit": False}
                for n, text in enumerate(["무관한 글", "반감기는 17.7 시간이다", "또 무관한 글"], 1)]
        self.conn = psycopg.connect(f"dbname={TEST_DB}")
        self.addCleanup(self.conn.close)
        index.create_schema(self.conn)
        index.insert_chunks(self.conn, g.CHUNK_SET, rows)
        index.insert_embeddings(self.conn, g.CHUNK_SET, g.EMBED_MODEL, rows, vectors)
        self.questions = [question("q01-ko", "ko"), question("q01-en", "en", text="What is the half-life in hours?")]
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "generation" / "runs.jsonl"

    def run_small(self, fake, seeds=(1, 2)):
        with mock.patch.object(g.urllib.request, "urlopen", fake), \
                mock.patch.object(g, "embed_query", lambda model, text: self.query_vector), \
                mock.patch.object(g, "K", 2), redirect_stdout(io.StringIO()) as printed:
            n = g.run(self.questions, self.path, self.conn, None, seeds=seeds)
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]
        return n, rows, printed.getvalue()

    def test_order_count_and_warmup(self):
        fake = FakeOllama()
        n, rows, printed = self.run_small(fake)
        self.assertEqual((n, len(rows)), (8, 8))   # 질문 2 × 씨앗 2 × 시스템 2
        self.assertEqual([(r["system"], r["seed"], r["question_id"]) for r in rows],
                         [(s, seed, q) for s in ("baseline", "minimal") for seed in (1, 2) for q in ("q01-ko", "q01-en")])
        # 요청은 몸풀기 1 + 8번이고, 몸풀기는 맨 앞이며 기록에 들어가지 않는다
        self.assertEqual(len(fake.requests), 9)
        # 모델 내리기 요청이 몸풀기보다 먼저 가고, 기록에는 없다
        self.assertEqual(fake.calls[0], (g.GENERATE_URL, {"model": "qwen3:8b", "keep_alive": 0}))
        self.assertEqual(fake.calls[1][1]["messages"][1]["content"], g.WARMUP_USER)
        self.assertEqual(len(fake.calls), 10)
        self.assertTrue(all(r["aborted"] is False and r["abort_reason"] is None for r in rows))
        self.assertEqual(fake.requests[0]["messages"][1]["content"], g.WARMUP_USER)
        self.assertNotIn(g.WARMUP_USER, [r["user_message"] for r in rows])
        self.assertEqual([r["options"]["seed"] for r in rows], [req["options"]["seed"] for req in fake.requests[1:]])
        self.assertEqual(len(printed.strip().splitlines()), 9)   # 모델 내림 알림 1줄 + 진행 8줄
        self.assertEqual(len({r["run_id"] for r in rows}), 1)

    def test_baseline_and_minimal_rows(self):
        fake = FakeOllama()
        _, rows, _ = self.run_small(fake)
        base, mini = rows[0], rows[4]
        for r in (base, mini):
            self.assertEqual((r["model"], r["output"], r["gen_tokens"], r["parsed_ok"], r["correct"]), ("qwen3:8b", fake.content, 12, True, True))
            self.assertEqual(r["options"]["num_ctx"], 32768)
            self.assertIsInstance(r["code_dirty"], bool)
            self.assertEqual(len(r["code_commit"]), 40)
        self.assertEqual((base["prompt_version"], mini["prompt_version"]), ("en-v1", "en-v1+ctx-en-v1"))
        for key in g.NO_RETRIEVAL:
            self.assertIsNone(base[key], key)
        self.assertIsNone(base["retrieved_tokens"])
        self.assertEqual(mini["retrieved_tokens"], sum(r["tokens"] for r in mini["retrieved"]))
        self.assertEqual(mini["retrieved_tokens"], 18)   # 가져온 청크 2개 × 9토큰
        self.assertEqual((base["prompt_tokens"], mini["prompt_tokens"]), (345, 345))
        self.assertEqual(base["system_message"], g.SYSTEM_EN)
        # 최소판: 질문 글이 검색 쿼리이고, 청크가 순위대로 지시문에 들어 있고, 근거가 든 청크(1위)가 ✔다
        self.assertEqual((mini["chunk_set"], mini["embedding_model"], mini["chunk_size"], mini["title"], mini["k"]),
                         ("size128_title", "bge-m3", 128, True, 2))
        self.assertEqual(mini["query"], "반감기는 몇 시간인가?")
        self.assertEqual([r["chunk_id"] for r in mini["retrieved"]][0], "doc-a#2")
        self.assertEqual((mini["hit"], mini["hit_ranks"]), (True, [1]))
        self.assertEqual(mini["retrieved"][0]["evidence"], [0])
        self.assertIn("[1] doc-a (lines 4-6)\n반감기는 17.7 시간이다", mini["system_message"])
        self.assertTrue(mini["system_message"].startswith(g.SYSTEM_EN))
        self.assertEqual(mini["user_message"], "반감기는 몇 시간인가?")
        self.assertIsInstance(mini["embed_seconds"], float)
        self.assertIsInstance(mini["search_seconds"], float)

    def test_http_error_stops_with_request_identified_and_no_error_line(self):
        calls = []

        def flaky(req, timeout=None):
            if req.full_url == g.GENERATE_URL:
                return FakeResponse("")
            calls.append(json.loads(req.data))
            if len(calls) == 4:   # 몸풀기 1 + baseline 씨앗 1의 2개 + 다음 요청(baseline 씨앗 2, q01-ko)
                raise http_error(500)
            return FakeResponse('{"reason": "r", "answer": "17.7"}')
        with mock.patch.object(g.urllib.request, "urlopen", flaky), redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError) as cm:
            g.run(self.questions, self.path, self.conn, None, seeds=(1, 2), systems=("baseline",))
        message = str(cm.exception)
        for part in ("baseline", "씨앗2", "q01-ko", "HTTP 500", "model runner has unexpectedly stopped"):
            self.assertIn(part, message)
        self.assertEqual(len(calls), 4)   # 재시도하지 않는다
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([(r["seed"], r["question_id"]) for r in rows], [(1, "q01-ko"), (1, "q01-en")])   # 오류 줄은 쓰지 않는다

    def test_token_repeat_limit_is_recorded_and_run_continues(self):
        abort = "prediction aborted, token repeat limit reached"
        partial = '{"reason": "r", "answer": "0.000000'
        # 채팅 요청 번호: 0 몸풀기, 1~2 baseline 씨앗 1(q01-ko, q01-en). 1번을 끊는다
        fake = FakeOllama(responses={1: FakeResponse(partial, error=abort)})
        n, rows, printed = self.run_small(fake, seeds=(1,))
        self.assertEqual(n, 4)   # 끊겨도 멈추지 않고 나머지를 돈다
        cut, ok = rows[0], rows[1]
        self.assertEqual((cut["question_id"], cut["output"], cut["aborted"], cut["abort_reason"]), ("q01-ko", partial, True, abort))
        self.assertEqual((cut["gen_tokens"], cut["prompt_tokens"]), (None, None))
        self.assertEqual((cut["parsed_ok"], cut["correct"], cut["answer_lang"], cut["reason"], cut["answer"]), (False, False, None, "", ""))
        self.assertEqual((ok["aborted"], ok["abort_reason"], ok["gen_tokens"], ok["prompt_tokens"], ok["correct"]), (False, None, 12, 345, True))
        self.assertIn("q01-ko 틀림 (끊김)", printed)

    def test_other_error_line_stops_run_with_request_identified(self):
        fake = FakeOllama(responses={2: FakeResponse("앞 글", error="model runner has unexpectedly stopped")})
        with mock.patch.object(g.urllib.request, "urlopen", fake), redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError) as cm:
            g.run(self.questions, self.path, self.conn, None, seeds=(1,), systems=("baseline",))
        for part in ("baseline", "씨앗1", "q01-en", "model runner has unexpectedly stopped"):
            self.assertIn(part, str(cm.exception))
        rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["question_id"] for r in rows], ["q01-ko"])

    def test_existing_file_stops_and_is_kept(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text("첫 실행의 기록\n", encoding="utf-8")
        fake = FakeOllama()
        with mock.patch.object(g.urllib.request, "urlopen", fake), self.assertRaises(FileExistsError):
            g.run(self.questions, self.path, self.conn, None, seeds=(1,))
        self.assertEqual(self.path.read_text(encoding="utf-8"), "첫 실행의 기록\n")
        self.assertEqual((fake.requests, fake.calls), ([], []))   # 모델 내리기도 몸풀기도 하지 않는다


if __name__ == "__main__":
    unittest.main()
