"""src/agent/graph.py(1단계 고리 그래프)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama와 실제 데이터베이스를 쓰지 않는다. urlopen을 FakeOllama로 바꿔 모델 요청마다 정해 둔 글을 돌려주고, 검색은 가짜로 바꾼다(fakes.py).
요청 본문을 모두 붙잡아 어느 칸이 어떤 글과 설정으로 몇 번 불렀는지 본다.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402
import graph  # noqa: E402
import plan  # noqa: E402
from fakes import TIMES, FakeOllama, FakeResponse, found_row, patched, plan_output, question  # noqa: E402

Q = "반감기는 몇 시간인가?"
SEED = 3
TIME_KEYS = ("prompt_eval_seconds", "eval_seconds", "load_seconds")


def searches():
    table = {Q: [found_row(f"o{i}", text=f"o{i} 글") for i in range(1, 17)]}
    table["한국어판1"] = [found_row(f"k1-{i}", text=f"k1-{i} 글") for i in range(1, 5)]
    table["english1"] = [found_row(f"e1-{i}", text=f"e1-{i} 글") for i in range(1, 5)]
    return table


def run_graph(ollama, q=None, seed=SEED):
    with patched(ollama, searches()) as calls:
        state = graph.build(None, None).invoke(graph.initial_state(q or question(text=Q), seed))
    return state, calls


class PlanThenSearchTest(unittest.TestCase):
    """계획을 한 번 쓰고 바로 검색하고 답한다. 판정·다시 쓰기 요청은 없다."""

    def setUp(self):
        self.ollama = FakeOllama(plans=[plan_output("한국어판1", "english1")])
        self.state, self.calls = run_graph(self.ollama)

    def test_request_order(self):
        self.assertEqual(self.ollama.roles(), ["plan", "answer"])

    def test_node_names_are_exactly_generate_search_answer(self):
        self.assertEqual(set(graph.build(None, None).get_graph().nodes) - {"__start__", "__end__"}, {"generate", "search", "answer"})
        self.assertEqual([t["node"] for t in self.state["node_times"]], ["generate", "search", "answer"])

    def test_state_has_no_judgment_fields(self):
        for key in ("user_message", "judgments", "n_judgments", "n_refinements", "plan_passed", "first_plan", "plan_steps"):
            self.assertNotIn(key, self.state)

    def test_plan_and_step(self):
        s = self.state
        self.assertEqual((s["shape_error"], s["plan"]["korean_question"], s["plan"]["reason"]), (None, "한국어판1", "생각"))
        step = s["plan_step"]
        self.assertEqual((step["user_message"], step["output"], step["problems"], step["aborted"], step["abort_reason"]),
                         (Q, plan_output("한국어판1", "english1"), [], False, None))
        self.assertEqual((step["gen_tokens"], step["prompt_tokens"]), (12, 345))
        self.assertEqual(step["plan"], s["plan"])
        self.assertIsInstance(step["gen_seconds"], float)

    def test_plan_request_is_the_generation_request(self):
        role, body = self.ollama.requests[0]
        self.assertEqual(body, plan.plan_body(Q, SEED))
        self.assertEqual(body["options"]["temperature"], 0)
        self.assertEqual(body["messages"][1]["content"], Q)

    def test_search_uses_original_korean_and_english(self):
        self.assertEqual(self.calls, [(Q, 8), ("한국어판1", 4), ("english1", 4)])
        self.assertEqual(self.state["search"]["n_chunks"], 16)

    def test_answer_uses_merged_chunks_in_order(self):
        _, body = self.ollama.requests[1]
        system_message = body["messages"][0]["content"]
        self.assertTrue(system_message.startswith(generate.SYSTEM_EN + generate.CONTEXT_EN.split("{")[0]))
        order = [system_message.index(f"{cid} 글") for cid in
                 [f"o{i}" for i in range(1, 9)] + [f"k1-{i}" for i in range(1, 5)] + [f"e1-{i}" for i in range(1, 5)]]
        self.assertEqual(order, sorted(order))
        self.assertEqual(body["messages"][1]["content"], Q)
        answer = self.state["answer"]
        self.assertEqual((answer["system_message"], answer["user_message"], answer["output"]), (system_message, Q, self.ollama.answer))
        self.assertEqual((answer["correct"], answer["parsed_ok"], answer["aborted"]), (True, True, False))
        self.assertEqual(body["options"], generate.request_body("", "", SEED)["options"])

    def test_every_request_uses_the_seed_of_the_run(self):
        self.assertEqual([body["options"]["seed"] for _, body in self.ollama.requests], [SEED] * 2)


class NodeTimesTest(unittest.TestCase):
    def test_nodes_in_order_with_ordered_times(self):
        state, _ = run_graph(FakeOllama(plans=[plan_output("한국어판1", "english1")]))
        times = state["node_times"]
        self.assertEqual([t["node"] for t in times], ["generate", "search", "answer"])
        for t in times:
            self.assertEqual(set(t), {"node", "start", "end"})
            self.assertGreaterEqual(t["start"], 0)
            self.assertLessEqual(t["start"], t["end"])
            self.assertEqual((t["start"], t["end"]), (round(t["start"], 3), round(t["end"], 3)))
        for before, after in zip(times, times[1:]):
            self.assertLessEqual(before["end"], after["start"])

    def test_timed_wraps_any_node_and_measures_from_the_start_of_the_run(self):
        node = graph.timed("anything", lambda state: {"plan": {"x": 1}})
        state = graph.initial_state(question(text=Q), SEED)
        update = node(state)
        self.assertEqual(update["plan"], {"x": 1})
        self.assertEqual([t["node"] for t in update["node_times"]], ["anything"])
        self.assertLessEqual(update["node_times"][0]["start"], update["node_times"][0]["end"])

    def test_request_records_carry_the_three_ollama_times(self):
        state, _ = run_graph(FakeOllama(plans=[plan_output("한국어판1", "english1")]))
        for record in (state["plan_step"], state["answer"]):
            self.assertEqual({key: record[key] for key in TIME_KEYS}, TIMES)

    def test_shape_error_run_has_only_the_generate_node(self):
        state, _ = run_graph(FakeOllama(plans=["이건 JSON이 아니다"]))
        self.assertEqual([t["node"] for t in state["node_times"]], ["generate"])


class ShapeErrorTest(unittest.TestCase):
    """꼴 오류 → 검색·답 없이 멈추고 원문이 기록됨"""

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
        self.assertEqual(state["plan"], None)
        self.assertEqual(state["plan_step"]["problems"], error["problems"])

    def test_plan_with_empty_targets(self):
        ollama = FakeOllama(plans=[plan_output("한국어판1", "english1", targets=[])])
        state, calls = run_graph(ollama)
        self.assertEqual(ollama.roles(), ["plan"])
        self.assertIn("targets", state["shape_error"]["problems"][0])

    def test_token_repeat_limit_is_recorded_with_its_reason(self):
        abort = "prediction aborted, token repeat limit reached"
        partial = '{"reason": "r", "targets": [{"fact": "f", "cond'
        ollama = FakeOllama(plans=[FakeResponse(partial, error=abort)])
        state, _ = run_graph(ollama)
        step = state["plan_step"]
        self.assertEqual((step["output"], step["aborted"], step["abort_reason"], step["gen_tokens"], step["prompt_tokens"]), (partial, True, abort, None, None))
        self.assertEqual({key: step[key] for key in TIME_KEYS}, {key: None for key in TIME_KEYS})
        self.assertEqual((state["shape_error"]["stage"], state["shape_error"]["output"]), ("generate", partial))


class OllamaErrorTest(unittest.TestCase):
    def test_other_error_stops_with_the_node(self):
        ollama = FakeOllama(plans=[FakeResponse("앞 글", error="model runner has unexpectedly stopped")])
        with self.assertRaises(RuntimeError) as cm:
            run_graph(ollama)
        self.assertIn("generate에서 멈춤", str(cm.exception))
        self.assertIn("model runner has unexpectedly stopped", str(cm.exception))

    def test_answer_error_names_the_answer_node(self):
        ollama = FakeOllama(plans=[plan_output("한국어판1", "english1")], answer=FakeResponse("", error="boom"))
        with self.assertRaises(RuntimeError) as cm:
            run_graph(ollama)
        self.assertIn("answer에서 멈춤", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
