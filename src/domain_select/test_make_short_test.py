# make_short_test.py의 네트워크 없는 함수를 확인한다.
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_short_test as m

F = {f["dir"]: f for f in m.FIELDS}


def found(dir_, line):
    quote, num_text, value, reason = m.find_line(F[dir_], line)
    return num_text, value, reason


class Order(unittest.TestCase):
    def test_same_seed_same_order(self):
        rows = [{"ko": str(i)} for i in range(20)]
        self.assertEqual(m.shuffled(rows), m.shuffled(rows))
        self.assertNotEqual(m.shuffled(rows), rows)
        self.assertEqual(rows[0], {"ko": "0"})  # 원래 목록은 그대로

    def test_other_seed_other_order(self):
        rows = [{"ko": str(i)} for i in range(20)]
        self.assertNotEqual(m.shuffled(rows, 1), m.shuffled(rows, 2))


class Title(unittest.TestCase):
    def test_strip_paren(self):
        self.assertEqual(m.strip_paren("미란다 (위성)"), "미란다")
        self.assertEqual(m.strip_paren("세레스 (왜행성)"), "세레스")
        self.assertEqual(m.strip_paren("요소 (화학)"), "요소")
        self.assertEqual(m.strip_paren("바너드별"), "바너드별")


class Lines(unittest.TestCase):
    def test_density(self):
        self.assertEqual(found("rare_earth", "- 밀도 (상온 근처): 7.90 g/cm3"), ("7.90", 7.9, None))
        self.assertEqual(found("rare_earth", "- 밀도 2.17 g/cm3")[1], 2.17)

    def test_indented_line(self):
        self.assertEqual(found("rare_earth", "  - 밀도 (상온 근처): 9.841 g/cm3"), ("9.841", 9.841, None))

    def test_density_no_line(self):
        self.assertIsNotNone(found("rare_earth", "- 녹는점 1585 K")[2])

    def test_boiling(self):
        self.assertEqual(found("organic", "- 끓는점 250 °C (482 °F; 523 K)"), ("250", 250.0, None))
        self.assertEqual(found("organic", "- 끓는점 1,465 °C (2,669 °F)")[1], 1465.0)

    def test_boiling_condition_after_unit(self):
        self.assertEqual(found("organic", "- 끓는점 341.3 °C (646.3 °F; 614.5 K) at 760 mmHg")[1], 341.3)

    def test_boiling_range_rejected(self):
        self.assertIsNone(found("organic", "- 끓는점 113-115 °C")[0])
        self.assertIsNone(found("organic", "- 끓는점 113–115 °C")[0])

    def test_boiling_kelvin_rejected(self):
        self.assertIsNone(found("organic", "- 끓는점 523 K")[0])

    def test_minor_bodies(self):
        self.assertEqual(found("minor_bodies", "- 궤도 긴반지름(a): 2.765926424"), ("2.765926424", 2.765926424, None))
        self.assertEqual(found("minor_bodies", "- 궤도 긴반지름 2.77 AU")[1], 2.77)

    def test_minor_bodies_km_rejected(self):
        self.assertIsNone(found("minor_bodies", "- 긴반지름 129390 km")[0])

    def test_moons(self):
        self.assertEqual(found("moons", "- 공전 주기(P): 1.413479 일"), ("1.413479", 1.413479, None))
        self.assertEqual(found("moons", "- 공전 주기 2.52 d")[1], 2.52)

    def test_moons_range_and_unit_rejected(self):
        self.assertIsNone(found("moons", "- 공전 주기(P): 1.4-1.5 일")[0])
        self.assertIsNone(found("moons", "- 공전 주기(P): 1.4 시간")[0])

    def test_stars(self):
        self.assertEqual(found("stars", "- 질량: 0.15 M☉"), ("0.15", 0.15, None))

    def test_stars_pm_takes_center(self):
        self.assertEqual(found("stars", "- 질량: 0.168±0.017 M☉"), ("0.168", 0.168, None))
        self.assertEqual(found("stars", "- 질량 0.168 ± 0.017 M☉")[1], 0.168)

    def test_pm_taken_everywhere(self):
        self.assertEqual(found("moons", "- 공전 주기(P): 1.4±0.1 일")[:2], ("1.4", 1.4))

    def test_exoplanets(self):
        self.assertEqual(found("exoplanets", "- 공전주기: 2.643904 일"), ("2.643904", 2.643904, None))

    def test_exoplanets_year_rejected(self):
        self.assertIsNone(found("exoplanets", "- 공전주기: 11.86 년")[0])

    def test_comma_removed(self):
        self.assertEqual(found("exoplanets", "- 공전주기: 1,234.5 일")[1], 1234.5)


class SurveyRules(unittest.TestCase):
    def test_digit_groups(self):
        self.assertEqual(found("moons", "- 공전 주기(P): 79.321 5 일")[:2], ("79.321 5", 79.3215))
        self.assertEqual(found("moons", "- 공전 주기(P): 550.564 636 일")[1], 550.564636)
        self.assertEqual(m.parse_number("12 955 759")[1], 12955759.0)
        self.assertEqual(m.parse_number("1,078 ± 2")[1], 1078.0)

    def test_pm(self):
        self.assertEqual(found("exoplanets", "- 공전주기: 1095.0 ± 2.9 일")[1], 1095.0)
        self.assertEqual(found("moons", "- 공전 주기(P): 0.49817943±0.00000007 d (11 h, 57 min, 23 s)")[1], 0.49817943)

    def test_asymmetric_error(self):
        self.assertEqual(found("exoplanets", "- 공전주기: 11.186+0.001 −0.002 일")[1], 11.186)

    def test_paren_after_value_ignored(self):
        self.assertEqual(found("exoplanets", "- 공전주기: 1.5803925 ± 0.0000117 일(37.92942 시간)")[1], 1.5803925)
        self.assertEqual(found("exoplanets", "- 공전주기: 36.562 ± 0.052 일(0.1년)")[1], 36.562)

    def test_still_rejected(self):
        self.assertIsNone(found("moons", "- 공전 주기(P): 0.70/0.63 일")[0])
        self.assertIsNone(found("moons", "- 공전 주기(P): 약 3 일")[0])
        self.assertIsNone(found("moons", "- 공전 주기(P): ~3 일")[0])
        self.assertIsNone(found("moons", "- 공전 주기(P): ≥3 일")[0])
        self.assertIsNone(found("moons", "- 공전 주기(P): A: 3 일 B: 4 일")[0])
        self.assertIsNone(found("exoplanets", "- 공전주기: 0.1668446년")[0])
        self.assertIsNone(found("exoplanets", "- 공전주기: 2.81705 ± 0.0001")[0])

    def test_survey_text_same_rule(self):
        self.assertEqual(m.parse_number("1095.0 ± 2.9 일")[1], 1095.0)
        self.assertEqual(m.parse_number("2.520")[1], 2.52)
        self.assertEqual(m.parse_number("0.1221 태양질량")[1], 0.1221)
        self.assertIsNone(m.parse_number("")[1])


def en(dir_, wikitext):
    ev, text, reason = m.en_value(F[dir_], wikitext)
    return ev, reason


class English(unittest.TestCase):
    def test_ascii_plus_minus(self):
        self.assertEqual(en("organic", "|BoilingPt = 341.3 +/- 0.4 C"), (341.3, None))

    def test_orbit_sign(self):
        self.assertEqual(en("moons", "| period = +248.29 d"), (248.29, None))
        self.assertEqual(en("moons", "| period = −550.31 d"), (550.31, None))
        self.assertEqual(en("moons", "| period = -550.31 d"), (550.31, None))
        self.assertEqual(en("exoplanets", "| period = {{val|−3.5|u=d}}"), (3.5, None))

    def test_sign_only_for_periods(self):
        self.assertIn("비교 불가", en("minor_bodies", "| semimajor = +2.5 AU")[1])
        self.assertIn("비교 불가", en("organic", "|BoilingPtC = +5")[1])

    def test_ko_sign(self):
        self.assertEqual(found("moons", "- 공전 주기(P): −550.564 636 일")[1], 550.564636)
        self.assertIsNone(found("organic", "- 끓는점 −5 °C")[0])

    def test_val_unit(self):
        self.assertEqual(en("moons", "| period = {{val|1.413479|u=d}}"), (1.413479, None))
        self.assertEqual(en("exoplanets", "| period = {{val|289.863876|0.000013|ul=d}}"), (289.863876, None))
        self.assertEqual(en("exoplanets", "| period = {{val|61.1057|0.0074|u=days}}"), (61.1057, None))

    def test_convert_and_plain(self):
        self.assertEqual(en("minor_bodies", "| semimajor = {{convert|2.861|AU|m|abbr=on}}"), (2.861, None))
        self.assertEqual(en("exoplanets", "| period = 32<ref name=\"v\"/> [[day|d]]"), (32.0, None))

    def test_nested_sigfig(self):
        self.assertEqual(en("minor_bodies", "| semimajor = {{Convert|{{sigfig|2.76604|3}}|AU|e6km|abbr=unit}}"), (2.76604, None))

    def test_year_to_days(self):
        ev, _ = en("exoplanets", "| period = {{val|2|u=yr}}")
        self.assertAlmostEqual(ev, 730.5)

    def test_au_units(self):
        self.assertAlmostEqual(en("minor_bodies", "| semimajor = {{val|149.5978707|u=Gm}}")[0], 1.0)
        self.assertAlmostEqual(en("minor_bodies", "| semimajor = {{val|149597870.7|u=km}}")[0], 1.0)

    def test_unit_unknown_or_missing(self):
        self.assertIn("비교 불가", en("minor_bodies", "| semimajor = {{val|5|u=m}}")[1])
        self.assertIn("비교 불가", en("exoplanets", "| period = {{val|5}}")[1])

    def test_star_mass_implicit_unit(self):
        self.assertEqual(en("stars", "| mass = {{val|0.1221|0.0022}}<ref name=a/>"), (0.1221, None))

    def test_boiling_keys(self):
        self.assertEqual(en("organic", "|BoilingPtC = 110.60\n|BoilingPt_ref = x"), (110.6, None))
        self.assertEqual(en("organic", "|BoilingPtC =\n|BoilingPt = {{convert|115.2|C|F}}"), (115.2, None))

    def test_element_density_fallback(self):
        t = "|density=7.899&nbsp;g/cm<sup>3</sup>&thinsp;<ref name=\"A\" />\n|density gpcm3nrt="
        self.assertEqual(en("rare_earth", t), (7.899, None))
        self.assertEqual(en("rare_earth", "|density gpcm3nrt=6.5\n|density=7 g/cm3"), (6.5, None))
        self.assertIn("비교 불가", en("rare_earth", "|density=β-Ce: 6.689 g/cm<sup>3</sup><br />γ-Ce: 6.769 g/cm<sup>3</sup>")[1])

    def test_no_value(self):
        self.assertEqual(en("moons", "| mass = 5"), (None, "영어 값 없음"))
        self.assertEqual(en("exoplanets", "| mass = \n| period = "), (None, "영어 값 없음"))

    def test_first_nonempty_line_wins(self):
        self.assertEqual(en("exoplanets", "| period = {{val|5|u=d}}\n| period = {{val|9|u=d}}")[0], 5.0)

    def test_multiple_values_rejected(self):
        self.assertIn("비교 불가", en("exoplanets", "| period = 1,078 ± 2 [[day|d]]<br>~2.95 [[year|y]]")[1])


class Tolerance(unittest.TestCase):
    def diff(self, ko, en_):
        return abs(ko - en_) / abs(en_) * 100

    def test_within_and_over_one_percent(self):
        self.assertLessEqual(self.diff(7.90, 7.899), m.TOL_PCT)
        self.assertGreater(self.diff(2.7659, 2.861), m.TOL_PCT)
        self.assertLessEqual(self.diff(100.9, 100), m.TOL_PCT)
        self.assertGreater(self.diff(101.1, 100), m.TOL_PCT)


class Quote(unittest.TestCase):
    md = "# x\n\n- 밀도 (상온 근처): 7.90 g/cm3\n"

    def test_ok(self):
        m.check_quote(self.md, "밀도 (상온 근처): 7.90 g/cm3", "7.90")

    def test_quote_not_in_doc(self):
        with self.assertRaises(AssertionError):
            m.check_quote(self.md, "밀도 (상온 근처): 7.9 g/cm3", "7.9")

    def test_number_not_in_quote(self):
        with self.assertRaises(AssertionError):
            m.check_quote(self.md, "밀도 (상온 근처): 7.90 g/cm3", "8.2")


if __name__ == "__main__":
    unittest.main()
