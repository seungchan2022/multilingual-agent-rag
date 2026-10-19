"""make_round2.py 시험. 질문 만들기와 results/ 멈춤만 본다(파일은 임시 폴더에 쓴다)."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_round2 as m
from check_questions import evaluate


def short(target, value, field):
    return {"id": "x-01", "subject": "분야", "target": target, "value": value,
            "evidence_quotes": [{"doc": target, "quote": "인용"}]}


class Josa(unittest.TestCase):
    def test_rules(self):
        self.assertEqual(m.josa("유로퓸"), "이")
        self.assertEqual(m.josa("미마스"), "가")
        self.assertEqual(m.josa("COROT-7b"), "가")
        self.assertEqual(m.josa("글리제 581 c"), "가")

    def test_other_char_raises(self):
        with self.assertRaises(ValueError):
            m.josa("케플러-16d")
        with self.assertRaises(ValueError):
            m.josa("HD 189733 B")


class Make(unittest.TestCase):
    def test_calc_gives_value_and_ingredient_in_calc(self):
        for field, target, v in [("rare_earth", "유로퓸", 5.244), ("exoplanets", "글리제 1214 b", 1.5803925),
                                 ("moons", "미마스", 0.942)]:
            q = m.make_question(field, short(target, v, field))
            got, _, nums = evaluate(q["calc"])
            self.assertEqual(round(got, 10), q["value"])
            self.assertIn(q["ingredient"], nums)
            self.assertIn(float(q["unit_factor"]), nums)

    def test_shown_numbers(self):
        q = m.make_question("rare_earth", short("유로퓸", 5.244, "rare_earth"))
        self.assertEqual(q["answer"], "0.31464 kg")
        self.assertEqual(q["requirements"], [[5.244, 5244.0]])
        q = m.make_question("exoplanets", short("글리제 1214 b", 1.5803925, "exoplanets"))
        self.assertEqual(q["answer"], "113.788시간")
        self.assertEqual(q["unit_conv"], [24])

    def test_stops_when_results_exist(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "moons" / "results").mkdir(parents=True)
            with self.assertRaises(SystemExit) as cm:
                m.stop_if_results(root)
            self.assertEqual(cm.exception.code, 1)
            self.assertFalse((root / "rare_earth").exists())

    def test_passes_without_results(self):
        with tempfile.TemporaryDirectory() as d:
            m.stop_if_results(Path(d))


if __name__ == "__main__":
    unittest.main()
