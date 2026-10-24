"""src/minimal/scoring.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

DB도 Ollama도 쓰지 않는다. 괄호 오차 표기 빼기, 예전 규칙과 같은 경우, 단위 확인을 손으로 만든 글로 본다.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scoring  # noqa: E402
from generate import grade_record  # noqa: E402  (예전 규칙: src/domain_select/run.py의 grade_record)
from index import QUESTIONS  # noqa: E402


def q(value=621.4, unit="keV"):
    return {"id": "q", "value": value, "unit": unit, "answer": f"{value} {unit}"}


class NumbersTest(unittest.TestCase):
    def test_attached_parenthesis_integer_is_dropped(self):
        self.assertEqual(scoring.numbers_of("621.4(11) keV"), [621.4])
        self.assertEqual(scoring.numbers_of("476.2(5)"), [476.2])
        self.assertEqual(scoring.numbers_of("12.4(6) 분"), [12.4])
        self.assertEqual(scoring.numbers_of("10(2)"), [10.0])

    def test_space_before_parenthesis_counts(self):
        self.assertEqual(scoring.numbers_of("621.4 (11) keV"), [621.4, 11.0])

    def test_only_integers_inside_parenthesis(self):
        self.assertEqual(scoring.numbers_of("621.4(1.5) keV"), [621.4, 1.5])
        self.assertEqual(scoring.numbers_of("621.4(abc)"), [621.4])
        self.assertEqual(scoring.numbers_of("621.4(11 keV)"), [621.4, 11.0])   # 닫는 괄호가 정수 바로 뒤가 아니다

    def test_parenthesis_not_after_a_number_counts(self):
        self.assertEqual(scoring.numbers_of("값(11) 621.4"), [11.0, 621.4])

    def test_two_values_with_errors(self):
        self.assertEqual(scoring.numbers_of("621.4(11)와 476.2(5)"), [621.4, 476.2])

    def test_comma_and_negative(self):
        self.assertEqual(scoring.numbers_of("1,234.5(3) g"), [1234.5])
        self.assertEqual(scoring.numbers_of("-3.5(2)"), [-3.5])

    def test_same_as_old_rule_without_parenthesis_errors(self):
        samples = ["0.31464 kg", "1,234.5 g", "17.7 시간이 아니라 5", "모른다", "", "약 3 또는 4", "-3.5", "5 (3)", "a 12 b (7) c", "1e3", "0.000000000"]
        for text in samples:
            old = grade_record({"value": 17.7, "answer": "x"}, text)
            new = scoring.grade({"value": 17.7}, text)
            self.assertEqual((new["numbers"], new["picked"], new["correct"]), (old["numbers"], old["picked"], old["correct"]), text)

    def test_non_string_answer(self):
        self.assertEqual(scoring.numbers_of(17.7), [17.7])
        self.assertEqual(scoring.numbers_of(None), [])


class GradeTest(unittest.TestCase):
    def test_error_notation_answer_is_correct(self):
        r = scoring.grade(q(621.4), "621.4(11) keV")
        self.assertEqual((r["numbers"], r["picked"], r["correct"]), ([621.4], 621.4, True))
        r = scoring.grade(q(476.2), "476.2(5)")
        self.assertEqual((r["picked"], r["correct"]), (476.2, True))

    def test_old_rule_got_it_wrong(self):
        old = grade_record({"value": 621.4, "answer": "x"}, "621.4(11) keV")
        self.assertEqual((old["picked"], old["correct"]), (11.0, False))

    def test_last_number_and_one_percent(self):
        self.assertTrue(scoring.grade(q(100), "101")["correct"])
        self.assertFalse(scoring.grade(q(100), "101.01")["correct"])
        self.assertTrue(scoring.grade(q(100), "99")["correct"])
        self.assertFalse(scoring.grade(q(100), "98.9")["correct"])
        self.assertEqual(scoring.grade(q(100), "100 아니라 5")["picked"], 5.0)

    def test_no_number(self):
        r = scoring.grade(q(100), "모른다")
        self.assertEqual((r["numbers"], r["picked"], r["correct"]), ([], None, False))


class UnitTest(unittest.TestCase):
    def check(self, unit, answer):
        return scoring.unit_check(q(0.5592, unit), answer)

    def test_same_unit(self):
        self.assertEqual(self.check("kg", "0.5592 kg"), "같음")
        self.assertEqual(self.check("kg", "0.5592kg"), "같음")
        self.assertEqual(self.check("kg", "0.5592 kg입니다"), "같음")
        self.assertEqual(self.check("kg", "0.5592 킬로그램"), "같음")
        self.assertEqual(self.check("kg", "0.5592 kilograms"), "같음")
        self.assertEqual(self.check("min", "12.4 분"), "같음")
        self.assertEqual(self.check("분", "2.11분"), "같음")
        self.assertEqual(self.check("분", "2.11분입니다"), "같음")
        self.assertEqual(self.check("분", "2.11 minutes"), "같음")
        self.assertEqual(self.check("months", "10.8 months"), "같음")
        self.assertEqual(self.check("개월", "10.8 개월"), "같음")
        self.assertEqual(self.check("개월", "10.8 달"), "같음")
        self.assertEqual(self.check("s", "3 seconds"), "같음")
        self.assertEqual(self.check("초", "3 s"), "같음")
        self.assertEqual(self.check("days", "3 일"), "같음")
        self.assertEqual(self.check("일", "3 day"), "같음")
        self.assertEqual(self.check("keV", "621.4(11) keV"), "같음")

    def test_different_unit(self):
        self.assertEqual(self.check("kg", "0.5592 g"), "다름")
        self.assertEqual(self.check("kg", "0.5592 톤"), "다름")
        self.assertEqual(self.check("분", "2.11 초"), "다름")
        self.assertEqual(self.check("min", "2 hours"), "다름")
        self.assertEqual(self.check("keV", "621.4 MeV"), "다름")
        self.assertEqual(self.check("개월", "10.8 days"), "다름")

    def test_no_unit(self):
        self.assertEqual(self.check("kg", "0.5592"), "없음")
        self.assertEqual(self.check("kg", "0.5592."), "없음")
        self.assertEqual(self.check("kg", "0.5592 (약)"), "없음")
        self.assertEqual(self.check("kg", "모른다"), "없음")
        self.assertEqual(self.check("kg", ""), "없음")

    def test_unit_follows_the_picked_number_only(self):
        self.assertEqual(self.check("kg", "5 g 중 0.5592 kg"), "같음")
        self.assertEqual(self.check("kg", "0.5592 kg 아니라 5 g"), "다름")

    def test_unit_is_not_a_grade(self):
        # 단위가 달라도 맞음은 숫자로만 정한다
        self.assertTrue(scoring.grade(q(0.5592, "kg"), "0.5592 g")["correct"])

    def test_all_question_units_are_known(self):
        questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
        for question in questions:
            self.assertEqual(scoring.unit_check(question, f"1 {question['unit']}"), "같음", question["id"])

    def test_unknown_question_unit_stops(self):
        with self.assertRaises(ValueError):
            scoring.unit_check(q(1, "furlong"), "1 furlong")


if __name__ == "__main__":
    unittest.main()
