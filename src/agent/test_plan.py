"""src/agent/plan.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama도 데이터베이스도 쓰지 않는다. 요청 글이 결정 줄의 전문과 글자까지 같은지, 사용자 메시지의 모양, 꼴 검사를 본다.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan  # noqa: E402
from fakes import judge_output, plan_output  # noqa: E402

# decisions/stage6.md 2026-10-26 줄의 전문을 이 시험에 따로 적었다. plan.py의 상수와 한 글자도 다르면 안 된다(줄바꿈 \n, 맨 끝에 줄바꿈 없음).
PLAN_SYSTEM_TEXT = '''You prepare a document search for the question. Do not answer the question.
Answer only in the JSON format below.
{"reason": "...", "targets": [{"fact": "...", "condition": "...", "unit": "..."}], "korean_question": "...", "english_question": "..."}
reason: before the plan, write how you found the facts to look up and anything that was hard to translate.
targets: every fact that must be looked up in documents to answer the question, one item per fact. Write them in the language of the question.
fact: the fact to look up.
condition: conditions attached to that fact, such as time, place, or state. Write "" if there are none.
unit: the unit of that fact. Write "" if there is none.
korean_question: the whole question written in Korean. If the question is already in Korean, copy it as it is.
english_question: the whole question written in English. If the question is already in English, copy it as it is.
For korean_question and english_question: write common words such as element names in that language. Keep numbers, symbols, abbreviations, units, and names of people and organizations as they are. Do not add, drop, shorten, or answer anything.'''

JUDGE_SYSTEM_TEXT = '''You check a search plan written for a question. Do not answer the question.
The plan has targets (facts to look up, each with a condition and a unit), korean_question, and english_question.
Check three things.
targets_ok: targets include every fact needed to answer the question, and each condition and unit matches the question.
korean_ok: korean_question is written in Korean and asks exactly the same thing as the question: the same numbers, names, symbols, conditions, and units, with nothing added or dropped.
english_ok: english_question is written in English and asks exactly the same thing as the question, in the same way.
reason: before deciding, compare the plan with the question item by item and write what matches and what differs.
For every check that fails, write one problem: what is wrong and how to fix it.
Answer only in the JSON format below.
{"reason": "...", "targets_ok": true, "korean_ok": true, "english_ok": true, "problems": ["..."]}'''


def a_plan(**changes):
    return {**json.loads(plan_output()), **changes}


class ConstantsTest(unittest.TestCase):
    def test_plan_system_is_the_decided_text(self):
        self.assertEqual(plan.PLAN_SYSTEM, PLAN_SYSTEM_TEXT)

    def test_judge_system_is_the_decided_text(self):
        self.assertEqual(plan.JUDGE_SYSTEM, JUDGE_SYSTEM_TEXT)

    def test_versions_and_limits(self):
        self.assertEqual((plan.PLAN_VERSION, plan.JUDGE_VERSION, plan.REFINE_VERSION), ("plan-en-v1", "judge-en-v2", "refine-en-v1"))
        self.assertEqual((plan.JUDGE_MODEL, plan.MAX_JUDGMENTS), ("gemma3:4b", 3))

    def test_plan_body_is_answer_settings_with_temperature_zero(self):
        body = plan.plan_body("질문", 3)
        expected = plan.generate.request_body(plan.PLAN_SYSTEM, "질문", 3)
        expected["options"]["temperature"] = 0
        self.assertEqual(body, expected)
        self.assertEqual(plan.generate.request_body("", "", 3)["options"]["temperature"], 0.7)


class MessageTest(unittest.TestCase):
    def test_plan_json_drops_reason_and_extra_fields_and_fixes_order(self):
        messy = {"english_question": "E?", "extra": 1, "reason": "생각", "korean_question": "한?",
                 "targets": [{"unit": "h", "note": "x", "condition": "c", "fact": "f"}, {"fact": "g", "condition": "", "unit": ""}]}
        self.assertEqual(plan.plan_json(messy),
                         '{"targets": [{"fact": "f", "condition": "c", "unit": "h"}, {"fact": "g", "condition": "", "unit": ""}], '
                         '"korean_question": "한?", "english_question": "E?"}')

    def test_plan_json_keeps_korean_as_it_is(self):
        self.assertIn("한국어판", plan.plan_json(a_plan()))
        self.assertNotIn("\\u", plan.plan_json(a_plan()))
        self.assertNotIn("\n", plan.plan_json(a_plan()))

    def test_judge_user_message(self):
        p = a_plan()
        self.assertEqual(plan.judge_user_message("질문 글", p), "Question:\n질문 글\n\nSearch plan:\n" + plan.plan_json(p))
        self.assertNotIn("생각", plan.judge_user_message("질문 글", p))   # reason은 판정 모델에게 보여 주지 않는다

    def test_failed_checks_in_fixed_order(self):
        judgment = json.loads(judge_output(targets_ok=False, korean_ok=True, english_ok=False, problems=["a"]))
        self.assertEqual(plan.failed_checks(judgment), ["targets_ok", "english_ok"])

    def test_refine_user_message(self):
        p = a_plan()
        judgment = json.loads(judge_output(korean_ok=False, english_ok=False, problems=["숫자가 빠짐: 고쳐라", "second problem"]))
        self.assertEqual(plan.refine_user_message("질문 글", p, judgment),
                         "질문 글\n\nYour previous plan:\n" + plan.plan_json(p) + "\nFailed checks: korean_ok, english_ok"
                         "\nProblems found in the plan:\n- 숫자가 빠짐: 고쳐라\n- second problem"
                         "\nWrite the whole plan again in the same JSON format. Fix every problem. Keep the parts without problems as they are.")

    def test_refine_user_message_has_no_reason(self):
        judgment = json.loads(judge_output(targets_ok=False, problems=["p"]))
        self.assertNotIn("생각", plan.refine_user_message("질문", a_plan(), judgment))

    def test_judge_body_matches_spec(self):
        body = plan.judge_body("사용자 글", 4)
        self.assertEqual(body, {"model": "gemma3:4b",
                                "messages": [{"role": "system", "content": plan.JUDGE_SYSTEM}, {"role": "user", "content": "사용자 글"}],
                                "stream": True, "format": "json",
                                "options": {"temperature": 0, "top_p": 0.8, "top_k": 20, "min_p": 0, "num_predict": 2048, "num_ctx": 8192, "seed": 4}})
        self.assertNotIn("think", body)


class CheckPlanTest(unittest.TestCase):
    def check(self, **changes):
        return plan.check_plan(json.dumps(a_plan(**changes), ensure_ascii=False))

    def test_good_plan_passes(self):
        parsed, problems = plan.check_plan(plan_output())
        self.assertEqual(problems, [])
        self.assertEqual(parsed["korean_question"], "한국어판")

    def test_empty_condition_and_unit_are_fine(self):
        self.assertEqual(self.check(targets=[{"fact": "f", "condition": "", "unit": ""}])[1], [])

    def test_missing_fields(self):
        for key in ("reason", "korean_question", "english_question", "targets"):
            data = a_plan()
            del data[key]
            parsed, problems = plan.check_plan(json.dumps(data))
            self.assertTrue(problems and any(key in p for p in problems), key)

    def test_targets_empty_list(self):
        self.assertTrue(any("targets" in p for p in self.check(targets=[])[1]))

    def test_targets_not_a_list(self):
        self.assertTrue(any("targets" in p for p in self.check(targets={"fact": "f"})[1]))

    def test_target_item_not_object(self):
        self.assertTrue(any("targets[0]" in p for p in self.check(targets=["f"])[1]))

    def test_target_missing_fact_condition_or_unit(self):
        for key in ("fact", "condition", "unit"):
            item = {"fact": "f", "condition": "", "unit": ""}
            del item[key]
            self.assertTrue(any(f"targets[0].{key}" in p for p in self.check(targets=[item])[1]), key)

    def test_target_value_not_text(self):
        self.assertTrue(any("targets[0].unit" in p for p in self.check(targets=[{"fact": "f", "condition": "", "unit": 3}])[1]))

    def test_fact_blank_only(self):
        problems = self.check(targets=[{"fact": " \n ", "condition": "", "unit": ""}])[1]
        self.assertTrue(any("targets[0].fact" in p and "빈칸" in p for p in problems))

    def test_second_item_is_numbered(self):
        problems = self.check(targets=[{"fact": "f", "condition": "", "unit": ""}, {"fact": "", "condition": "", "unit": ""}])[1]
        self.assertTrue(any("targets[1].fact" in p for p in problems))

    def test_blank_versions(self):
        self.assertTrue(any("korean_question" in p and "빈칸" in p for p in self.check(korean_question="  ")[1]))
        self.assertTrue(any("english_question" in p and "빈칸" in p for p in self.check(english_question="")[1]))

    def test_versions_not_text(self):
        self.assertTrue(any("korean_question" in p for p in self.check(korean_question=["한"])[1]))

    def test_reason_not_text(self):
        self.assertTrue(any("reason" in p for p in self.check(reason=None)[1]))

    def test_not_json(self):
        parsed, problems = plan.check_plan('{"reason": "r", "targets": [')
        self.assertIsNone(parsed)
        self.assertTrue(problems and "JSON" in problems[0])

    def test_json_list_is_not_an_object(self):
        parsed, problems = plan.check_plan('[{"fact": "f"}]')
        self.assertIsNone(parsed)
        self.assertTrue(problems and "객체" in problems[0])

    def test_empty_output(self):
        self.assertIsNone(plan.check_plan("")[0])
        self.assertTrue(plan.check_plan("")[1])

    def test_all_problems_are_listed(self):
        problems = self.check(targets=[], korean_question="", english_question=" ")[1]
        self.assertEqual(len(problems), 3)


class CheckJudgmentTest(unittest.TestCase):
    def check(self, **changes):
        data = {**json.loads(judge_output()), **changes}
        return plan.check_judgment(json.dumps(data, ensure_ascii=False))

    def test_all_true_passes_with_empty_problems(self):
        parsed, problems = plan.check_judgment(judge_output())
        self.assertEqual(problems, [])
        self.assertTrue(plan.passed(parsed))

    def test_false_with_problems_is_good_shape_but_not_passed(self):
        parsed, problems = plan.check_judgment(judge_output(korean_ok=False, problems=["p"]))
        self.assertEqual(problems, [])
        self.assertFalse(plan.passed(parsed))

    def test_text_true_is_wrong(self):
        self.assertTrue(any("targets_ok" in p for p in self.check(targets_ok="true")[1]))

    def test_number_one_is_wrong(self):
        self.assertTrue(any("korean_ok" in p for p in self.check(korean_ok=1)[1]))

    def test_missing_check(self):
        data = json.loads(judge_output())
        del data["english_ok"]
        self.assertTrue(any("english_ok" in p for p in plan.check_judgment(json.dumps(data))[1]))

    def test_false_with_empty_problems(self):
        problems = self.check(english_ok=False, problems=[])[1]
        self.assertEqual(len(problems), 1)
        self.assertIn("problems", problems[0])

    def test_problems_with_non_text_item(self):
        self.assertTrue(any("problems" in p for p in self.check(korean_ok=False, problems=["p", 3])[1]))

    def test_problems_not_a_list(self):
        self.assertTrue(any("problems" in p for p in self.check(problems="p")[1]))

    def test_reason_not_text(self):
        self.assertTrue(any("reason" in p for p in self.check(reason=5)[1]))

    def test_not_json(self):
        parsed, problems = plan.check_judgment('{"reason": "r", "targets_ok": tr')
        self.assertIsNone(parsed)
        self.assertTrue(problems)

    def test_json_list(self):
        self.assertIsNone(plan.check_judgment("[true]")[0])

    def test_passed_needs_all_three(self):
        for name in plan.CHECKS:
            parsed = json.loads(judge_output(**{name: False}, problems=["p"]))
            self.assertFalse(plan.passed(parsed), name)


if __name__ == "__main__":
    unittest.main()
