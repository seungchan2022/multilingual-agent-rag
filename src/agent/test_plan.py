"""src/agent/plan.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

Ollama도 데이터베이스도 쓰지 않는다. 요청 글이 결정 줄의 전문과 글자까지 같은지, 요청 본문, 꼴 검사를 본다.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import plan  # noqa: E402
from fakes import plan_output  # noqa: E402

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

def a_plan(**changes):
    return {**json.loads(plan_output()), **changes}


class ConstantsTest(unittest.TestCase):
    def test_plan_system_is_the_decided_text(self):
        self.assertEqual(plan.PLAN_SYSTEM, PLAN_SYSTEM_TEXT)

    def test_version(self):
        self.assertEqual(plan.PLAN_VERSION, "plan-en-v1")

    def test_judgment_and_refinement_are_gone(self):
        for name in ("JUDGE_MODEL", "MAX_JUDGMENTS", "JUDGE_VERSION", "REFINE_VERSION", "CHECKS", "JUDGE_SYSTEM", "plan_json", "judge_user_message",
                     "failed_checks", "refine_user_message", "judge_body", "check_judgment", "passed"):
            self.assertFalse(hasattr(plan, name), name)

    def test_plan_body_is_answer_settings_with_temperature_zero(self):
        body = plan.plan_body("질문", 3)
        expected = plan.generate.request_body(plan.PLAN_SYSTEM, "질문", 3)
        expected["options"]["temperature"] = 0
        self.assertEqual(body, expected)
        self.assertEqual(plan.generate.request_body("", "", 3)["options"]["temperature"], 0.7)


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


if __name__ == "__main__":
    unittest.main()
