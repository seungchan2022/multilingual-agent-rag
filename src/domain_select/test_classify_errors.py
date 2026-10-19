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

    def test_unit_per_question_factor(self):
        # 값 5.0, 그 문제의 바꾸기가 60(s<->min)이면 x60, 1000 단계 실수를 겹친 x60/10^3, 나누기 /60가 단위 오류다
        for picked, k, e in [(300.0, 0, 1), (0.3, -3, 1), (5 / 60, 0, -1), (300000.0, 3, 1)]:
            labels, d = ce.classify(row("값 10 에서 결과 %s" % picked, picked), 5.0, [[10]], None, [60])
            self.assertIn(ce.BAD_UNIT, labels)
            self.assertEqual((d[ce.BAD_UNIT]["t"], d[ce.BAD_UNIT]["k"], d[ce.BAD_UNIT]["e"]), (60, k, e))

    def test_unit_factor_not_allowed_for_other_question(self):
        # 같은 답이라도 60 바꾸기가 없는 문제에서는 단위 오류가 아니다
        labels, _ = ce.classify(row("값 10 에서 결과 300", 300.0), 5.0, [[10]])
        self.assertEqual(labels, [ce.BAD_CALC])
        # 3600 바꾸기가 있는 문제에서 60은 단위 오류가 아니다
        labels, _ = ce.classify(row("값 10 에서 결과 300", 300.0), 5.0, [[10]], None, [3600])
        self.assertEqual(labels, [ce.BAD_CALC])
        labels, _ = ce.classify(row("값 10 에서 결과 18000", 18000.0), 5.0, [[10]], None, [3600])
        self.assertIn(ce.BAD_UNIT, labels)

    def test_unit_only_one_factor_at_a_time(self):
        # 60과 3600을 함께 곱한 값(216000)은 두 바꾸기를 겹친 것이라 세지 않는다
        labels, _ = ce.classify(row("값 10 에서 결과 1080000", 1080000.0), 5.0, [[10]], None, [60, 3600])
        self.assertEqual(labels, [ce.BAD_CALC])

    def test_unit_kelvin_offset(self):
        labels, d = ce.classify(row("값 10 에서 결과 2.0", 2.0), -271.15, [[10]], None, ["offset"])
        self.assertIn(ce.BAD_UNIT, labels)
        self.assertEqual(d[ce.BAD_UNIT]["종류"], "더하기")
        self.assertAlmostEqual(d[ce.BAD_UNIT]["차이"], 273.15)
        labels, d = ce.classify(row("값 10 에서 결과 1000", 1000.0), 1273.15, [[10]], None, ["offset"])
        self.assertEqual(d[ce.BAD_UNIT]["차이"], -273.15)
        # offset이 없는 문제에서는 더하기를 보지 않는다
        labels, _ = ce.classify(row("값 10 에서 결과 2.0", 2.0), -271.15, [[10]])
        self.assertEqual(labels, [ce.BAD_CALC])

    def test_unit_non_conversion_ratio_is_bad_calc(self):
        labels, _ = ce.classify(row("값 10 에서 결과 2.5", 2.5), 5.0, [[10]])
        self.assertEqual(labels, [ce.BAD_CALC])

    def test_unit_picks_closest_factor(self):
        # 100은 10^2 (t=1)로 정확히 맞는다
        _, d = ce.classify(row("값 10 에서 결과 500", 500.0), 5.0, [[10]])
        self.assertEqual((d[ce.BAD_UNIT]["k"], d[ce.BAD_UNIT]["t"]), (2, 1))

    def test_bad_calc(self):
        labels, _ = ce.classify(row("값 10 에 3을 곱해 30", 30.0), 5.0, [[10]])
        self.assertEqual(labels, [ce.BAD_CALC])

    def test_multi_label(self):
        labels, _ = ce.classify(row("값 1 에서", 500.0), 5.0, [[10]])
        self.assertEqual(labels, [ce.BAD_INPUT, ce.NO_CALC, ce.BAD_UNIT])


class Tolerance(unittest.TestCase):
    def test_product_gets_one_percent(self):
        self.assertEqual(ce.tolerance_of("2 * 5 * 22.61 / 1000", 22.61), 0.01)

    def test_subtraction_is_tighter(self):
        # 100 - (370.944 - 273.15) = 2.206, 허용 변화는 0.01*2.206 = 0.02206 이므로 r = 0.02206/370.944
        t = ce.tolerance_of("100 - (370.944 - 273.15)", 370.944)
        self.assertLess(t, 0.01)
        self.assertAlmostEqual(t, 0.02206 / 370.944, delta=2e-7)

    def test_all_occurrences_change_together(self):
        # m-01: 28.085가 분자와 분모에 함께 들어 있어도 모두 같이 바꿔 계산해 1%로 나온다
        t = ce.tolerance_of("1000 * 28.085 / (28.085 + 2 * 15.999)", 28.085)
        self.assertEqual(t, 0.01)

    def test_primary_must_be_literal(self):
        with self.assertRaises(AssertionError):
            ce.tolerance_of("2 * 3", 5.0)

    def test_offset_matching(self):
        alts = [[3695, ce.Offset(3421.85)]]
        # 차이 대안은 기본 값 3695의 1% = 36.95 만큼의 절대 폭, 배수 없음
        self.assertNotIn(ce.BAD_INPUT, ce.classify(row("끓는점 3450 에서 3", 3.0), 77, alts)[0])
        self.assertIn(ce.BAD_INPUT, ce.classify(row("끓는점 3500 에서 3", 3.0), 77, alts)[0])
        # 좁은 허용폭이면 절대 폭도 좁아진다
        self.assertIn(ce.BAD_INPUT, ce.classify(row("끓는점 3450 에서 3", 3.0), 77, alts, [0.001])[0])
        # 차이 대안에는 단위 배수를 적용하지 않는다
        self.assertIn(ce.BAD_INPUT, ce.classify(row("끓는점 3.42185 에서 3", 3.0), 77, alts)[0])

    def test_scale_matching_with_tolerance(self):
        alts = [[22.61]]
        self.assertNotIn(ce.BAD_INPUT, ce.classify(row("값 22.7 로 3", 3.0), 77, alts, [0.01])[0])
        self.assertIn(ce.BAD_INPUT, ce.classify(row("값 22.7 로 3", 3.0), 77, alts, [0.001])[0])
        self.assertNotIn(ce.BAD_INPUT, ce.classify(row("값 22610 로 3", 3.0), 77, alts, [0.001])[0])

    def test_detail_records_tolerance_and_match(self):
        _, d = ce.classify(row("값 20 에서 3", 3.0), 77, [[22.61], [5]], [0.01, 0.002])
        chk = d[ce.BAD_INPUT]["재료 값 대조"]
        self.assertEqual([c["허용폭"] for c in chk], [0.01, 0.002])
        self.assertEqual([c["맞은 풀이 숫자"] for c in chk], [None, None])


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
        # 0.76 = 12.672 x 60 x 10^-3: s-01은 60 바꾸기가 있고 1000 단계 실수를 겹친 값과 ±1% 안이라 둘 다 붙는다
        self.assertEqual(self.get("solar", "C", "s-01", 1)["labels"], [ce.NO_CALC, ce.BAD_UNIT])
        r = self.get("solar", "C", "s-05", 1)["labels"]
        self.assertIn(ce.BAD_UNIT, r)
        self.assertNotIn(ce.NO_CALC, r)
        self.assertIn(ce.BAD_UNIT, self.get("solar", "C", "s-08", 1)["labels"])
        self.assertEqual(self.get("mineral", "C", "m-06", 3)["labels"], [ce.BAD_CALC])
        self.assertIn(ce.BAD_INPUT, self.get("mineral", "C", "m-02", 1)["labels"])
        self.assertEqual(self.get("chem", "C", "c-10", 2)["labels"], [ce.NO_CALC])

    def test_s01_forgot_minutes(self):
        r = self.get("solar", "A", "s-01", 1)
        self.assertIn(ce.BAD_UNIT, r["labels"])
        self.assertNotIn(ce.BAD_CALC, r["labels"])

    def test_m10_190_5_is_not_unit(self):
        # m-10에는 시간 바꾸기가 없으므로 190.5는 단위 오류가 아니다
        for seed in range(1, 11):
            for r in self.recs:
                if (r["topic"], r["cond"], r["id"], r["seed"]) == ("mineral", "A", "m-10", seed):
                    self.assertNotIn(ce.BAD_UNIT, r["labels"])

    def test_c06_material_is_root_cause(self):
        # 97.72는 문서의 97.794와 0.08%만 달라도 두 수를 빼는 c-06에서는 답이 3% 움직인다
        for seed in (1, 3, 4):
            self.assertEqual(self.get("chem", "A", "c-06", seed)["labels"], [ce.BAD_INPUT])


if __name__ == "__main__":
    unittest.main()
