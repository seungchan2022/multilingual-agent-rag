# classify_errors.py의 다섯 갈래 조건을 확인한다. 실제 결과는 읽기만 한다.
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import classify_errors as ce


def row(reason, picked, answer="x", parsed=True):
    gen = {"text": "", "parsed": {"reason": reason, "answer": answer} if parsed else None}
    return {"gen": gen, "grade": {"picked": picked}}


class Numbers(unittest.TestCase):
    def test_scientific(self):
        self.assertEqual(ce.numbers_of("광속 3 × 10⁸ m/s"), [3e8])
        self.assertEqual(ce.numbers_of("2.998×10^8"), [2.998e8])
        self.assertEqual(ce.numbers_of("6.022e23"), [6.022e23])
        self.assertEqual(ce.numbers_of("1.6 x 10^-19"), [1.6e-19])
        self.assertEqual(ce.numbers_of("1.6 × 10⁻¹⁹"), [1.6e-19])

    def test_comma(self):
        self.assertEqual(ce.numbers_of("227,939,200 km"), [227939200.0])


class Labels(unittest.TestCase):
    def test_no_number_skips_others(self):
        labels, _ = ce.classify(row("없음", None), 10, [[99.0]])
        self.assertEqual(labels, [ce.NO_NUM])
        labels, _ = ce.classify(row("", None, parsed=False), 10, [[99.0]])
        self.assertEqual(labels, [ce.NO_NUM])

    def test_bad_input(self):
        labels, d = ce.classify(row("밀도 20 이고 5를 곱해 7", 7.0), 100, [[22.61]])
        self.assertIn(ce.BAD_INPUT, labels)
        self.assertEqual(d[ce.BAD_INPUT]["빠진 재료 값"], [[22.61]])

    def test_scaling_satisfies(self):
        labels, _ = ce.classify(row("밀도 22,610 kg/m³ 에 2를 곱해 45220", 45220.0), 99999, [[22.61]])
        self.assertNotIn(ce.BAD_INPUT, labels)

    def test_scientific_satisfies(self):
        labels, _ = ce.classify(row("광속 3 × 10⁸ 로 나눠 5", 5.0), 77, [[299792458]])
        self.assertNotIn(ce.BAD_INPUT, labels)

    def test_kelvin_or_celsius(self):
        labels, _ = ce.classify(row("끓는점 3421.85 에서 3", 3.0), 77, [[3695, 3421.85]])
        self.assertNotIn(ce.BAD_INPUT, labels)

    def test_tolerance_one_percent(self):
        self.assertNotIn(ce.BAD_INPUT, ce.classify(row("값 22.7 로 3", 3.0), 77, [[22.61]])[0])
        self.assertIn(ce.BAD_INPUT, ce.classify(row("값 23.5 로 3", 3.0), 77, [[22.61]])[0])

    def test_no_calc(self):
        labels, _ = ce.classify(row("값 10 과 2", 0.76), 50, [[10]])
        self.assertIn(ce.NO_CALC, labels)
        labels, _ = ce.classify(row("값 10 에서 결과 0.76", 0.76), 50, [[10]])
        self.assertNotIn(ce.NO_CALC, labels)

    def test_bad_unit(self):
        labels, d = ce.classify(row("값 10 에서 결과 500", 500.0), 5.0, [[10]])
        self.assertIn(ce.BAD_UNIT, labels)
        self.assertEqual(d[ce.BAD_UNIT]["k"], 2)
        self.assertNotIn(ce.BAD_UNIT, ce.classify(row("값 10 결과 5.02", 5.02), 5.0, [[10]])[0])
        self.assertNotIn(ce.BAD_UNIT, ce.classify(row("값 10 결과 7", 7.0), 5.0, [[10]])[0])

    def test_bad_calc(self):
        labels, _ = ce.classify(row("값 10 에 3을 곱해 30", 30.0), 5.0, [[10]])
        self.assertEqual(labels, [ce.BAD_CALC])

    def test_multi_label(self):
        labels, _ = ce.classify(row("값 1 에서", 500.0), 5.0, [[10]])
        self.assertEqual(labels, [ce.BAD_INPUT, ce.NO_CALC, ce.BAD_UNIT])


class RealData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs = ce.collect()

    def get(self, topic, cond, qid, seed):
        for r in self.recs:
            if (r["topic"], r["cond"], r["id"], r["seed"]) == (topic, cond, qid, seed):
                return r
        self.fail(f"{topic} {cond} {qid} {seed} 없음")

    def test_totals(self):
        a = [r for r in self.recs if r["cond"] == "A"]
        c = [r for r in self.recs if r["cond"] == "C"]
        self.assertEqual(len(a), 152)
        self.assertEqual(len(c), 64)
        for t, na, nc in [("chem", 30, 3), ("solar", 59, 35), ("mineral", 63, 26)]:
            self.assertEqual(sum(1 for r in a if r["topic"] == t), na)
            self.assertEqual(sum(1 for r in c if r["topic"] == t), nc)
        self.assertEqual(sum(1 for r in self.recs if not r["labels"]), 0)

    def test_seed_cases(self):
        self.assertEqual(self.get("solar", "C", "s-01", 1)["labels"], [ce.NO_CALC])
        r = self.get("solar", "C", "s-05", 1)["labels"]
        self.assertIn(ce.BAD_UNIT, r)
        self.assertNotIn(ce.NO_CALC, r)
        self.assertIn(ce.BAD_UNIT, self.get("solar", "C", "s-08", 1)["labels"])
        self.assertEqual(self.get("mineral", "C", "m-06", 3)["labels"], [ce.BAD_CALC])
        self.assertIn(ce.BAD_INPUT, self.get("mineral", "C", "m-02", 1)["labels"])
        self.assertEqual(self.get("chem", "C", "c-10", 2)["labels"], [ce.NO_CALC])


if __name__ == "__main__":
    unittest.main()
