"""src/agent/answer.py(근거 칸이 있는 답 쓰기)와 graph.build(conn, model, answer_version)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama와 실제 데이터베이스를 쓰지 않는다. urlopen과 검색을 가짜로 바꾼다(fakes.py).
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import answer  # noqa: E402
import generate  # noqa: E402
import graph  # noqa: E402
from fakes import TIMES, FakeOllama, FakeResponse, found_row, patched, plan_output, question  # noqa: E402

# 결정 줄(decisions/stage6.md 2026-10-28 "④ 답 쓰기 지시문 두 판의 전문")의 글을 이 시험에 따로 적었다. 두 글이 글자까지 같아야 한다.
LINE_1 = "You are an assistant that answers questions. Answer only in the JSON format below."
LINE_2 = ('{"reason": "Write the reasoning that leads to the answer, step by step", "answer": "Write only the final answer, briefly", '
          '"citations": [{"fact": "A fact from the reference passages that you used", "chunks": [the number of the passage that contains it]}]}')
CALC_V1 = ("If a calculation is needed, write the formula in reason, write the unit conversion step (e.g., g → kg) separately, "
           "and then check the calculation once more.")
CALC_V2_A = ("If a calculation is needed, do it in reason with the actual numbers from the question and the passages, one step at a time "
             "(e.g., 2.5 × 4 = 10). Do not only describe the steps in words.")
CALC_V2_B = ("Write the unit conversion (e.g., g → kg) as a step with numbers too, check the calculation once more, "
             "and write the final result of the calculation in answer.")
LINE_CITATIONS = ("In citations, list every fact from the reference passages that you used for the answer, one item per fact, "
                  "with the number of each passage that contains it. Do not write passage numbers in reason or answer.")
LINE_NONE = ("If the reference passages do not contain the facts needed to answer, write in answer that the question cannot be answered from the passages, "
             "and write [] for citations.")
LINE_LANG = ("Answer in the same language as the question. If the question is in Korean, write reason, answer, and fact in Korean; "
             "if it is in English, write them in English.")
# 판 1′·판 2(decisions/stage6.md 2026-10-28 "판 1′을 둔다"): 답 꼴 줄의 칸 순서를 바꾸고 문서 ID 확인 줄을 넣는다
LINE_2B = ('{"citations": [{"fact": "A fact from the reference passages that you used", "chunks": [the number of the passage that contains it]}], '
           '"reason": "Write the reasoning that leads to the answer, step by step", "answer": "Write only the final answer, briefly"}')
LINE_ID = ("Each reference passage starts with its document ID, and the ID contains the English name of what the document is about "
           "(for example, wiki-ko-<English name>). Before you use a value, check with the ID that the passage is about the same thing the question asks about.")
V1_TEXT = "\n".join([LINE_1, LINE_2, CALC_V1, LINE_CITATIONS, LINE_NONE, LINE_LANG])
V1B_TEXT = "\n".join([LINE_1, LINE_2B, CALC_V1, LINE_CITATIONS, LINE_ID, LINE_NONE, LINE_LANG])
V2_TEXT = "\n".join([LINE_1, LINE_2B, CALC_V2_A, CALC_V2_B, LINE_CITATIONS, LINE_ID, LINE_NONE, LINE_LANG])

Q = "반감기는 몇 시간인가?"
SEED = 3


def found_list():
    """청크 3개: 1번(doc-b, 숫자 6.145 있음), 2번(doc-b, 숫자 없음), 3번(doc-a 5줄, 근거 17.7 있음)."""
    return [found_row("c1", text="밀도는 6.145 이다"), found_row("c2", text="숫자 없는 글"), found_row("c3", evidence=True)]


def fields(output, aborted=False):
    return graph.reply_fields(output, 4.5, 12, 345, "token repeat limit" if aborted else None, TIMES)


def cite_output(answer_text="17.7 시간", citations=(), reason="읽는다"):
    return json.dumps({"reason": reason, "answer": answer_text, "citations": list(citations)}, ensure_ascii=False)


def record(output, hit_ranks=(3,), aborted=False, q=None):
    q = q or question(text=Q)
    found = found_list()
    return answer.record_of(q, found, list(hit_ranks), "SYS", Q, fields(output, aborted))


class InstructionTest(unittest.TestCase):
    def test_v1_text_is_the_decided_text(self):
        self.assertEqual(answer.CITE_V1, V1_TEXT)

    def test_v2_text_is_the_decided_text(self):
        self.assertEqual(answer.CITE_V2, V2_TEXT)

    def test_v1b_text_is_the_decided_text(self):
        self.assertEqual(answer.CITE_V1B, V1B_TEXT)

    def test_v2_differs_from_v1b_only_in_the_calculation_lines(self):
        v1b, v2 = answer.CITE_V1B.split("\n"), answer.CITE_V2.split("\n")
        self.assertEqual((v1b[:2], v1b[3:]), (v2[:2], v2[4:]))
        self.assertEqual((len(v1b), len(v2)), (7, 8))

    def test_schema_order_follows_the_version(self):
        self.assertEqual(list(answer.schema(3)["properties"]), ["reason", "answer", "citations"])
        for version in ("cite-en-v1b", "cite-en-v2"):
            s = answer.schema(3, answer.ORDERS[version])
            self.assertEqual((list(s["properties"]), s["required"]), (["citations", "reason", "answer"], ["citations", "reason", "answer"]))
            self.assertEqual(s["properties"]["citations"], answer.schema(3)["properties"]["citations"])

    def test_versions_and_prompt_version(self):
        self.assertEqual(set(answer.SYSTEMS), {"cite-en-v1", "cite-en-v1b", "cite-en-v2"})
        self.assertEqual(answer.prompt_version("cite-en-v1"), "cite-en-v1+ctx-en-v1")

    def test_minimal_instruction_is_untouched(self):
        self.assertNotIn("citations", generate.SYSTEM_EN)
        self.assertEqual(generate.request_body("s", "u", 1)["format"], "json")

    def test_messages_are_version_text_plus_context_and_the_question(self):
        found = found_list()
        for version, text in (("cite-en-v1", V1_TEXT), ("cite-en-v1b", V1B_TEXT), ("cite-en-v2", V2_TEXT)):
            system_message, user_message = answer.messages_of(version, question(text=Q), found)
            self.assertEqual(system_message, text + generate.CONTEXT_EN.format(passages=generate.passages_of(found)))
            self.assertEqual(user_message, Q)
        self.assertIn("[1] doc-b (lines 1-1)\n밀도는 6.145 이다", system_message)
        self.assertTrue(system_message.endswith("[3] doc-a (lines 5-5)\n반감기는 17.7 시간이다 무관한 글"))


class SchemaAndBodyTest(unittest.TestCase):
    def test_schema_shape_and_required(self):
        s = answer.schema(4)
        self.assertEqual((s["type"], s["required"]), ("object", ["reason", "answer", "citations"]))
        self.assertEqual([s["properties"][k]["type"] for k in ("reason", "answer", "citations")], ["string", "string", "array"])
        item = s["properties"]["citations"]["items"]
        self.assertEqual((item["type"], item["required"]), ("object", ["fact", "chunks"]))
        self.assertEqual(item["properties"]["fact"], {"type": "string"})
        self.assertEqual((item["properties"]["chunks"]["type"], item["properties"]["chunks"]["items"]["type"]), ("array", "integer"))

    def test_enum_is_one_to_n(self):
        for n in (1, 8, 13):
            enum = answer.schema(n)["properties"]["citations"]["items"]["properties"]["chunks"]["items"]["enum"]
            self.assertEqual(enum, list(range(1, n + 1)))

    def test_request_body_changes_only_format(self):
        body = answer.request_body("SYS", "USER", SEED, 5)
        plain = generate.request_body("SYS", "USER", SEED)
        self.assertEqual(body["format"], answer.schema(5))
        self.assertEqual({k: v for k, v in body.items() if k != "format"}, {k: v for k, v in plain.items() if k != "format"})
        self.assertEqual(body["options"]["temperature"], 0.7)


class CitedTest(unittest.TestCase):
    def test_numbers_become_documents(self):
        out = cite_output(citations=[{"fact": "반감기는 17.7 시간", "chunks": [3]}, {"fact": "밀도 6.145", "chunks": [1, 3]}])
        r = record(out)
        first, second = r["cited"]
        self.assertEqual(first["mapped"], [{"rank": 3, "chunk_id": "c3", "doc_id": "doc-a", "line_start": 5, "line_end": 5}])
        self.assertEqual(first["numbers"], [17.7])
        self.assertEqual(first["checks"], [{"rank": 3, "missing_numbers": []}])
        self.assertEqual([m["chunk_id"] for m in second["mapped"]], ["c1", "c3"])
        self.assertEqual(second["checks"], [{"rank": 1, "missing_numbers": []}, {"rank": 3, "missing_numbers": [6.145]}])
        self.assertEqual(r["citations"], [{"fact": "반감기는 17.7 시간", "chunks": [3]}, {"fact": "밀도 6.145", "chunks": [1, 3]}])

    def test_wrong_attached_counts_fact_chunk_pairs_whose_number_is_missing(self):
        # 6.145는 1번 청크에만 있다. 2번(숫자 없는 청크)과 3번에 붙이면 둘 다 센다. 1번은 안 센다
        r = record(cite_output(citations=[{"fact": "밀도 6.145", "chunks": [1, 2, 3]}]))
        self.assertEqual(r["checks"]["wrong_attached"], 2)

    def test_wrong_attached_is_zero_when_all_numbers_are_in_the_chunks(self):
        r = record(cite_output(citations=[{"fact": "반감기는 17.7 시간", "chunks": [3]}]))
        self.assertEqual(r["checks"]["wrong_attached"], 0)

    def test_one_missing_number_among_several_counts_the_pair(self):
        r = record(cite_output(citations=[{"fact": "17.7 시간과 99 개", "chunks": [3]}]))
        self.assertEqual(r["cited"][0]["checks"][0]["missing_numbers"], [99.0])
        self.assertEqual(r["checks"]["wrong_attached"], 1)

    def test_hyphen_before_a_number_is_not_a_sign(self):
        # numbers_of는 "Tb-144"를 -144로 읽는다. 청크에 "144"가 있으면 같은 숫자로 본다
        found = [("c1", 0.1, "doc-a", [5], "터븀 144 동위 원소의 반감기는 1 s", 9, "ko", 5, 5)]
        r = answer.record_of(question(), found, [1], "SYS", "USER",
                             graph.reply_fields(cite_output(citations=[{"fact": "Tb-144의 반감기 1 s", "chunks": [1]}]), 1.0, 10, 20, None, TIMES))
        self.assertEqual(r["cited"][0]["checks"][0]["missing_numbers"], [])

    def test_a_real_minus_sign_is_kept(self):
        # 청크에는 -0.05인데 사실에 0.05로 적으면 숫자가 없는 것으로 센다
        found = [("c1", 0.1, "doc-a", [5], "온도 계수는 -0.05%/°C 이다", 9, "ko", 5, 5)]
        r = answer.record_of(question(), found, [1], "SYS", "USER",
                             graph.reply_fields(cite_output(citations=[{"fact": "온도 계수 0.05%/°C", "chunks": [1]}]), 1.0, 10, 20, None, TIMES))
        self.assertEqual(r["cited"][0]["checks"][0]["missing_numbers"], [0.05])

    def test_numbers_are_compared_by_value(self):
        r = record(cite_output(citations=[{"fact": "6.1450", "chunks": [1]}]))
        self.assertEqual((r["cited"][0]["numbers"], r["checks"]["wrong_attached"]), ([6.145], 0))

    def test_facts_without_numbers_are_counted_apart_and_never_wrong(self):
        r = record(cite_output(citations=[{"fact": "원소 이름은 터븀", "chunks": [2]}, {"fact": "또 다른 이름", "chunks": [1]},
                                           {"fact": "반감기는 17.7 시간", "chunks": [3]}]))
        self.assertEqual((r["checks"]["no_number_facts"], r["checks"]["wrong_attached"]), (2, 0))

    def test_facts_without_chunks_are_counted(self):
        # 참고 글 밖의 지식(예: 단위 환산)을 청크 번호 없이 적은 사실
        r = record(cite_output(citations=[{"fact": "1 g/cm³ = 1000 kg/m³", "chunks": []}, {"fact": "반감기는 17.7 시간", "chunks": [3]}]))
        self.assertEqual((r["checks"]["facts_without_chunks"], r["checks"]["wrong_attached"]), (1, 0))

    def test_citation_missing_when_a_number_was_picked_but_citations_are_empty(self):
        r = record(cite_output(answer_text="17.7 시간", citations=[]))
        self.assertTrue(r["checks"]["citation_missing"])
        self.assertEqual(r["cited"], [])

    def test_citation_missing_is_false_when_no_number_was_picked_or_citations_exist(self):
        refusal = record(cite_output(answer_text="참고 글로는 답할 수 없다", citations=[]))
        self.assertFalse(refusal["checks"]["citation_missing"])
        cited = record(cite_output(answer_text="17.7 시간", citations=[{"fact": "17.7", "chunks": [3]}]))
        self.assertFalse(cited["checks"]["citation_missing"])

    def test_cites_evidence_overlap(self):
        r = record(cite_output(citations=[{"fact": "밀도 6.145", "chunks": [1]}, {"fact": "17.7", "chunks": [2, 3]}]), hit_ranks=(3, 5))
        self.assertIs(r["checks"]["cites_evidence"], True)

    def test_cites_evidence_no_overlap(self):
        r = record(cite_output(citations=[{"fact": "밀도 6.145", "chunks": [1]}]), hit_ranks=(3,))
        self.assertIs(r["checks"]["cites_evidence"], False)

    def test_cites_evidence_is_false_for_empty_citations_when_evidence_exists(self):
        r = record(cite_output(citations=[]), hit_ranks=(3,))
        self.assertIs(r["checks"]["cites_evidence"], False)

    def test_cites_evidence_is_null_without_hit_ranks(self):
        r = record(cite_output(citations=[{"fact": "17.7", "chunks": [3]}]), hit_ranks=())
        self.assertIsNone(r["checks"]["cites_evidence"])

    def test_numbers_not_in_the_list_are_kept_apart_as_invalid_chunks(self):
        r = record(cite_output(citations=[{"fact": "17.7", "chunks": [3, 7, 0]}]))
        item = r["cited"][0]
        self.assertEqual(([m["rank"] for m in item["mapped"]], item["invalid_chunks"]), ([3], [7, 0]))
        self.assertEqual(r["checks"]["wrong_attached"], 0)
        self.assertTrue(r["checks"]["shape_ok"])


class ShapeTest(unittest.TestCase):
    def assert_unreadable(self, r):
        self.assertFalse(r["checks"]["shape_ok"])
        self.assertIsNone(r["cited"])
        for key in ("cites_evidence", "wrong_attached", "no_number_facts", "facts_without_chunks", "citation_missing"):
            self.assertIsNone(r["checks"][key], key)

    def test_not_json(self):
        r = record("이건 JSON이 아니다")
        self.assert_unreadable(r)
        self.assertIsNone(r["citations"])
        self.assertEqual((r["parsed_ok"], r["correct"]), (False, False))

    def test_json_but_not_an_object(self):
        r = record("[1, 2]")
        self.assert_unreadable(r)
        self.assertIsNone(r["citations"])

    def test_missing_citations(self):
        r = record(json.dumps({"reason": "r", "answer": "17.7"}))
        self.assert_unreadable(r)
        self.assertIsNone(r["citations"])
        self.assertTrue(r["correct"])   # 채점은 answer 칸만 본다

    def test_citations_not_a_list(self):
        r = record(json.dumps({"reason": "r", "answer": "17.7", "citations": "3번"}))
        self.assert_unreadable(r)
        self.assertEqual(r["citations"], "3번")   # 모델이 쓴 원본을 그대로 남긴다

    def test_item_without_fact_or_with_bad_chunks(self):
        for item in ({"chunks": [1]}, {"fact": "f"}, {"fact": 3, "chunks": [1]}, {"fact": "f", "chunks": "1"}, {"fact": "f", "chunks": [1.5]},
                     {"fact": "f", "chunks": [True]}, {"fact": "f", "chunks": ["1"]}, "문자열"):
            r = record(json.dumps({"reason": "r", "answer": "17.7", "citations": [item]}))
            self.assert_unreadable(r)

    def test_missing_reason_or_answer(self):
        for body in ({"answer": "a", "citations": []}, {"reason": "r", "citations": []}, {"reason": "r", "answer": 3, "citations": []}):
            self.assert_unreadable(record(json.dumps(body)))

    def test_aborted_partial_output_is_a_shape_error_with_aborted_true(self):
        r = record('{"reason": "앞 글', aborted=True)
        self.assert_unreadable(r)
        self.assertTrue(r["checks"]["aborted"])
        self.assertTrue(r["aborted"])

    def test_empty_citations_list_is_a_good_shape(self):
        r = record(cite_output(citations=[]))
        self.assertTrue(r["checks"]["shape_ok"])
        self.assertEqual((r["citations"], r["cited"]), ([], []))


class RecordFieldsTest(unittest.TestCase):
    def test_columns(self):
        r = record(cite_output(citations=[{"fact": "17.7", "chunks": [3]}]))
        self.assertEqual((r["system_message"], r["user_message"]), ("SYS", Q))
        # graph.reply_fields와 같은 칸(글, 시간, 토큰, 끊김, 시간 셋)
        self.assertEqual({k: r[k] for k in fields("x")}, {**fields("x"), "output": r["output"]})
        for key in ("output", "gen_seconds", "gen_tokens", "prompt_tokens", "aborted", "abort_reason", "prompt_eval_seconds", "eval_seconds", "load_seconds"):
            self.assertIn(key, r)
        # generate.graded의 칸
        for key in ("parsed_ok", "reason", "answer", "numbers", "picked", "value", "correct", "unit", "answer_lang", "hangul", "latin", "lang_ok"):
            self.assertIn(key, r)
        self.assertEqual((r["answer"], r["picked"], r["correct"], r["parsed_ok"]), ("17.7 시간", 17.7, True, True))
        self.assertEqual(set(r["checks"]), {"shape_ok", "cites_evidence", "wrong_attached", "no_number_facts", "facts_without_chunks", "citation_missing", "aborted"})

    def test_grading_ignores_citations(self):
        # 근거 칸의 숫자(번호 3)가 있어도 채점은 answer 칸의 마지막 숫자만 본다
        r = record(cite_output(answer_text="17.7 시간", citations=[{"fact": "99", "chunks": [3]}]))
        self.assertEqual((r["numbers"], r["correct"]), ([17.7], True))


def searches():
    table = {Q: [found_row(f"o{i}", text=f"o{i} 글", evidence=(i == 2)) for i in range(1, 17)]}
    table["한국어판1"] = [found_row(f"k1-{i}", text=f"k1-{i} 글") for i in range(1, 5)]
    table["english1"] = [found_row(f"e1-{i}", text=f"e1-{i} 글") for i in range(1, 5)]
    return table


def run_graph(ollama, answer_version=None):
    with patched(ollama, searches()):
        return graph.build(None, None, answer_version).invoke(graph.initial_state(question(text=Q), SEED))


class GraphAnswerVersionTest(unittest.TestCase):
    def cite(self):
        return cite_output(citations=[{"fact": "반감기는 17.7 시간", "chunks": [2]}])

    def test_with_a_version_the_answer_node_uses_the_new_function(self):
        ollama = FakeOllama(plans=[plan_output("한국어판1", "english1")], answer=self.cite())
        state = run_graph(ollama, "cite-en-v2")
        self.assertEqual(ollama.roles(), ["plan", "answer"])
        _, body = ollama.requests[1]
        self.assertEqual(body["format"], answer.schema(16, answer.ORDERS["cite-en-v2"]))
        self.assertEqual(body["messages"][0]["content"].split("\n\nAnswer based on")[0], V2_TEXT)
        a = state["answer"]
        self.assertEqual(a["system_message"], body["messages"][0]["content"])
        self.assertEqual([m["chunk_id"] for m in a["cited"][0]["mapped"]], ["o2"])
        self.assertEqual((a["checks"]["shape_ok"], a["checks"]["cites_evidence"]), (True, True))   # hit_ranks는 state["search"]의 것 [2]
        self.assertEqual(state["search"]["hit_ranks"], [2])
        self.assertEqual({k: a[k] for k in TIMES}, TIMES)
        self.assertEqual([t["node"] for t in state["node_times"]], ["generate", "search", "answer"])
        self.assertEqual(body["options"], generate.request_body("", "", SEED)["options"])

    def test_without_a_version_the_answer_is_the_minimal_one_as_before(self):
        ollama = FakeOllama(plans=[plan_output("한국어판1", "english1")])
        state = run_graph(ollama)
        _, body = ollama.requests[1]
        self.assertEqual(body["format"], "json")
        self.assertTrue(body["messages"][0]["content"].startswith(generate.SYSTEM_EN))
        for key in ("citations", "cited", "checks"):
            self.assertNotIn(key, state["answer"])
        self.assertEqual(state["answer"]["output"], ollama.answer)

    def test_answer_error_names_the_answer_node(self):
        ollama = FakeOllama(plans=[plan_output("한국어판1", "english1")], answer=FakeResponse("", error="boom"))
        with self.assertRaises(RuntimeError) as cm:
            run_graph(ollama, "cite-en-v1")
        self.assertIn("answer에서 멈춤", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
