"""src/agent/graph.py(1단계 고리 그래프)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama와 실제 데이터베이스를 쓰지 않는다. urlopen을 FakeOllama로 바꿔 모델 요청마다 정해 둔 글을 돌려주고, 검색은 가짜로 바꾼다(fakes.py).
요청 본문을 모두 붙잡아 어느 칸이 어떤 글과 설정으로 몇 번 불렀는지 본다.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402
import graph  # noqa: E402
import plan  # noqa: E402
from fakes import FakeOllama, FakeResponse, found_row, judge_output, patched, plan_output, question  # noqa: E402

Q = "반감기는 몇 시간인가?"
SEED = 3


def plan_n(n, **kw):
    return plan_output(f"한국어판{n}", f"english{n}", **kw)


def plan_json_n(n):
    return ('{"targets": [{"fact": "half-life", "condition": "", "unit": "h"}], '
            f'"korean_question": "한국어판{n}", "english_question": "english{n}"}}')


def searches():
    table = {Q: [found_row(f"o{i}", text=f"o{i} 글") for i in range(1, 17)]}
    for n in (1, 2, 3):
        table[f"한국어판{n}"] = [found_row(f"k{n}-{i}", text=f"k{n}-{i} 글") for i in range(1, 5)]
        table[f"english{n}"] = [found_row(f"e{n}-{i}", text=f"e{n}-{i} 글") for i in range(1, 5)]
    return table


def run_graph(ollama, q=None, seed=SEED):
    with patched(ollama, searches()) as calls:
        state = graph.build(None, None).invoke(graph.initial_state(q or question(text=Q), seed))
    return state, calls


def user_messages(ollama, role):
    return [body["messages"][1]["content"] for r, body in ollama.requests if r == role]


class PassFirstTest(unittest.TestCase):
    """① 첫 판정 통과 → 다시 쓰기 0"""

    def setUp(self):
        self.ollama = FakeOllama(plans=[plan_n(1)], judges=[judge_output()])
        self.state, self.calls = run_graph(self.ollama)

    def test_request_order(self):
        self.assertEqual(self.ollama.roles(), ["plan", "judge", "answer"])

    def test_counts_and_flags(self):
        s = self.state
        self.assertEqual((s["n_judgments"], s["n_refinements"], s["plan_passed"], s["shape_error"]), (1, 0, True, None))
        self.assertEqual((len(s["plan_steps"]), len(s["judgments"])), (1, 1))
        self.assertEqual(s["first_plan"], s["plan"])
        self.assertEqual(s["plan"]["korean_question"], "한국어판1")

    def test_plan_request_is_the_generation_request(self):
        role, body = self.ollama.requests[0]
        self.assertEqual(body, plan.plan_body(Q, SEED))
        self.assertEqual(body["options"]["temperature"], 0)
        self.assertEqual(body["messages"][1]["content"], Q)

    def test_judge_request(self):
        _, body = self.ollama.requests[1]
        self.assertEqual(body, plan.judge_body("Question:\n" + Q + "\n\nSearch plan:\n" + plan_json_n(1), SEED))

    def test_records(self):
        step, judgment = self.state["plan_steps"][0], self.state["judgments"][0]
        self.assertEqual((step["user_message"], step["output"], step["problems"], step["aborted"], step["abort_reason"]), (Q, plan_n(1), [], False, None))
        self.assertEqual((step["gen_tokens"], step["prompt_tokens"]), (12, 345))
        self.assertEqual(step["plan"]["reason"], "생각")   # 생성 모델의 reason도 읽은 계획에 남는다
        self.assertEqual((judgment["output"], judgment["problems"], judgment["passed"]), (judge_output(), [], True))
        self.assertTrue(judgment["user_message"].startswith("Question:\n" + Q))
        self.assertIsInstance(judgment["gen_seconds"], float)

    def test_search_uses_original_korean_and_english(self):
        self.assertEqual(self.calls, [(Q, 8), ("한국어판1", 4), ("english1", 4)])
        self.assertEqual(self.state["search"]["n_chunks"], 16)

    def test_answer_uses_merged_chunks_in_order(self):
        _, body = self.ollama.requests[2]
        system_message = body["messages"][0]["content"]
        self.assertTrue(system_message.startswith(generate.SYSTEM_EN + generate.CONTEXT_EN.split("{")[0]))
        order = [system_message.index(f"{cid} 글") for cid in
                 [f"o{i}" for i in range(1, 9)] + [f"k1-{i}" for i in range(1, 5)] + [f"e1-{i}" for i in range(1, 5)]]
        self.assertEqual(order, sorted(order))
        self.assertTrue(system_message.index("[16] ") > system_message.index("[1] "))
        self.assertEqual(body["messages"][1]["content"], Q)
        answer = self.state["answer"]
        self.assertEqual((answer["system_message"], answer["user_message"], answer["output"]), (system_message, Q, self.ollama.answer))
        self.assertEqual((answer["correct"], answer["parsed_ok"], answer["aborted"]), (True, True, False))
        self.assertEqual(body["options"], generate.request_body("", "", SEED)["options"])

    def test_every_request_uses_the_seed_of_the_run(self):
        self.assertEqual([body["options"]["seed"] for _, body in self.ollama.requests], [SEED] * 3)


class RefineOnceTest(unittest.TestCase):
    """② 한 번 떨어지고 통과 → 다시 쓰기 1"""

    def setUp(self):
        self.ollama = FakeOllama(plans=[plan_n(1), plan_n(2)],
                                 judges=[judge_output(korean_ok=False, english_ok=False, problems=["숫자가 빠짐: 고쳐라", "second"]), judge_output()])
        self.state, self.calls = run_graph(self.ollama)

    def test_request_order(self):
        self.assertEqual(self.ollama.roles(), ["plan", "judge", "plan", "judge", "answer"])

    def test_counts(self):
        s = self.state
        self.assertEqual((s["n_judgments"], s["n_refinements"], s["plan_passed"], s["shape_error"]), (2, 1, True, None))
        self.assertEqual((len(s["plan_steps"]), len(s["judgments"])), (2, 2))
        self.assertEqual([j["passed"] for j in s["judgments"]], [False, True])

    def test_rewrite_message_matches_the_previous_judgment(self):
        first, second = user_messages(self.ollama, "plan")
        self.assertEqual(first, Q)
        self.assertEqual(second, Q + "\n\nYour previous plan:\n" + plan_json_n(1) + "\nFailed checks: korean_ok, english_ok"
                         "\nProblems found in the plan:\n- 숫자가 빠짐: 고쳐라\n- second"
                         "\nWrite the whole plan again in the same JSON format. Fix every problem. Keep the parts without problems as they are.")
        self.assertEqual(self.state["plan_steps"][1]["user_message"], second)
        # 시스템 메시지는 늘 PLAN_SYSTEM이다
        self.assertEqual([body["messages"][0]["content"] for role, body in self.ollama.requests if role == "plan"], [plan.PLAN_SYSTEM] * 2)

    def test_second_judgment_sees_the_rewritten_plan(self):
        self.assertTrue(user_messages(self.ollama, "judge")[1].endswith(plan_json_n(2)))

    def test_first_plan_is_kept_and_final_plan_is_the_rewrite(self):
        self.assertEqual(self.state["first_plan"]["korean_question"], "한국어판1")
        self.assertEqual(self.state["plan"]["korean_question"], "한국어판2")

    def test_search_uses_the_rewritten_plan(self):
        self.assertEqual(self.calls, [(Q, 8), ("한국어판2", 4), ("english2", 4)])

    def test_every_request_uses_the_seed_of_the_run(self):
        self.assertEqual({body["options"]["seed"] for _, body in self.ollama.requests}, {SEED})


class FailThreeTimesTest(unittest.TestCase):
    """③ 세 번 모두 떨어짐 → 판정 3, 다시 쓰기 2, plan_passed false, 마지막 계획으로 검색"""

    def setUp(self):
        self.ollama = FakeOllama(plans=[plan_n(1), plan_n(2), plan_n(3)],
                                 judges=[judge_output(targets_ok=False, problems=[f"problem {n}"]) for n in (1, 2, 3)])
        self.state, self.calls = run_graph(self.ollama)

    def test_request_order_stops_after_three_judgments(self):
        self.assertEqual(self.ollama.roles(), ["plan", "judge", "plan", "judge", "plan", "judge", "answer"])

    def test_counts(self):
        s = self.state
        self.assertEqual((s["n_judgments"], s["n_refinements"], s["plan_passed"], s["shape_error"]), (3, 2, False, None))
        self.assertEqual((len(s["plan_steps"]), len(s["judgments"])), (3, 3))

    def test_search_and_answer_use_the_last_plan(self):
        self.assertEqual(self.calls, [(Q, 8), ("한국어판3", 4), ("english3", 4)])
        self.assertIsNotNone(self.state["answer"])
        self.assertEqual(self.state["first_plan"]["korean_question"], "한국어판1")

    def test_third_rewrite_message_has_only_the_latest_problems(self):
        third = user_messages(self.ollama, "plan")[2]
        self.assertIn("- problem 2", third)
        self.assertNotIn("problem 1", third)
        self.assertIn(plan_json_n(2), third)
        self.assertNotIn(plan_json_n(1), third)
        self.assertIn("Failed checks: targets_ok\n", third)


class ShapeErrorTest(unittest.TestCase):
    """④ 꼴 오류 → 검색·답 없이 멈추고 원문이 기록됨"""

    def assert_stopped_before_search(self, state, calls):
        self.assertEqual((state["search"], state["answer"], state["merged_found"], calls), (None, None, None, []))

    def test_plan_not_json(self):
        ollama = FakeOllama(plans=['{"reason": "r", "targets": ['])
        state, calls = run_graph(ollama)
        self.assertEqual(ollama.roles(), ["plan"])
        self.assert_stopped_before_search(state, calls)
        error = state["shape_error"]
        self.assertEqual((error["stage"], error["index"], error["output"]), ("generate", 1, '{"reason": "r", "targets": ['))
        self.assertTrue(error["problems"])
        self.assertEqual((error["system_message"], error["user_message"], error["model"]), (plan.PLAN_SYSTEM, Q, "qwen3:8b"))
        self.assertEqual(error["options"], plan.plan_body("", SEED)["options"])
        self.assertEqual((state["first_plan"], state["plan"], state["n_judgments"]), (None, None, 0))
        self.assertEqual(state["plan_steps"][0]["problems"], error["problems"])

    def test_plan_with_empty_targets(self):
        ollama = FakeOllama(plans=[plan_n(1, targets=[])])
        state, calls = run_graph(ollama)
        self.assertEqual(ollama.roles(), ["plan"])
        self.assertIn("targets", state["shape_error"]["problems"][0])

    def test_judgment_with_text_true(self):
        bad = json.dumps({"reason": "r", "targets_ok": "true", "korean_ok": True, "english_ok": True, "problems": []})
        ollama = FakeOllama(plans=[plan_n(1)], judges=[bad])
        state, calls = run_graph(ollama)
        self.assertEqual(ollama.roles(), ["plan", "judge"])
        self.assert_stopped_before_search(state, calls)
        error = state["shape_error"]
        self.assertEqual((error["stage"], error["index"], error["output"], error["model"]), ("judgment", 1, bad, "gemma3:4b"))
        self.assertEqual((error["system_message"], error["options"]), (plan.JUDGE_SYSTEM, plan.judge_body("", SEED)["options"]))
        self.assertTrue(error["user_message"].startswith("Question:\n"))
        self.assertEqual((state["judgments"][0]["passed"], state["plan_passed"], state["n_judgments"]), (None, None, 1))

    def test_judgment_false_without_problems(self):
        ollama = FakeOllama(plans=[plan_n(1)], judges=[judge_output(korean_ok=False)])
        state, _ = run_graph(ollama)
        self.assertEqual(state["shape_error"]["stage"], "judgment")

    def test_error_in_a_rewrite_is_numbered_by_its_request(self):
        ollama = FakeOllama(plans=[plan_n(1), "not json"], judges=[judge_output(korean_ok=False, problems=["p"])])
        state, calls = run_graph(ollama)
        self.assertEqual(ollama.roles(), ["plan", "judge", "plan"])
        self.assert_stopped_before_search(state, calls)
        error = state["shape_error"]
        self.assertEqual((error["stage"], error["index"], state["n_refinements"]), ("generate", 2, 1))
        self.assertTrue(error["user_message"].startswith(Q + "\n\nYour previous plan:\n"))
        self.assertEqual(state["first_plan"]["korean_question"], "한국어판1")

    def test_token_repeat_limit_is_recorded_with_its_reason(self):
        abort = "prediction aborted, token repeat limit reached"
        partial = '{"reason": "r", "targets": [{"fact": "f", "cond'
        ollama = FakeOllama(plans=[FakeResponse(partial, error=abort)])
        state, _ = run_graph(ollama)
        step = state["plan_steps"][0]
        self.assertEqual((step["output"], step["aborted"], step["abort_reason"], step["gen_tokens"], step["prompt_tokens"]), (partial, True, abort, None, None))
        self.assertEqual((state["shape_error"]["stage"], state["shape_error"]["output"]), ("generate", partial))

    def test_aborted_judgment_is_recorded(self):
        abort = "prediction aborted, token repeat limit reached"
        ollama = FakeOllama(plans=[plan_n(1)], judges=[FakeResponse('{"reason": "r", "targets_ok": tru', error=abort)])
        state, _ = run_graph(ollama)
        judgment = state["judgments"][0]
        self.assertEqual((judgment["aborted"], judgment["abort_reason"]), (True, abort))
        self.assertEqual(state["shape_error"]["stage"], "judgment")


class OllamaErrorTest(unittest.TestCase):
    def test_other_error_stops_with_the_node_and_request_number(self):
        ollama = FakeOllama(plans=[plan_n(1)], judges=[FakeResponse("앞 글", error="model runner has unexpectedly stopped")])
        with self.assertRaises(RuntimeError) as cm:
            run_graph(ollama)
        self.assertIn("judgment 1번째 요청", str(cm.exception))
        self.assertIn("model runner has unexpectedly stopped", str(cm.exception))

    def test_answer_error_names_the_answer_node(self):
        ollama = FakeOllama(plans=[plan_n(1)], judges=[judge_output()], answer=FakeResponse("", error="boom"))
        with self.assertRaises(RuntimeError) as cm:
            run_graph(ollama)
        self.assertIn("answer에서 멈춤", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
