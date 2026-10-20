# make_round3_targets.py의 네트워크 없는 함수를 확인한다.
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_round3_targets as m

KG, M = m.EN_KG, m.EN_M


def cells(keys, units, text):
    return m.en_cells(keys, units, text)


class Order(unittest.TestCase):
    def test_same_seed_same_order(self):
        titles = [f"대상{i}" for i in range(18)]
        self.assertEqual(m.mst.shuffled(titles), m.mst.shuffled(titles))
        self.assertEqual(m.mst.shuffled(titles), [titles[i] for i in m.mst.shuffled(list(range(18)))])

    def test_pinned_order_for_seed(self):
        # 씨앗 20261019로 0..9를 섞은 차례. 씨앗이나 섞는 방법이 바뀌면 깨진다
        self.assertEqual(m.mst.SEED, 20261019)
        self.assertEqual(m.mst.shuffled(list(range(10))), [8, 0, 6, 2, 4, 3, 7, 1, 5, 9])


class Candidates(unittest.TestCase):
    def test_survey_order_and_filter(self):
        field = {"docs": [{"ko": "가", "en": "A"}, {"ko": "나", "en": None}, {"ko": "다", "en": "C"}, {"ko": "라", "en": "D"}],
                 "values": {"질량(kg)": {"targets": [
                     {"title": "다", "kind": "하나", "base_value": 5.0},
                     {"title": "나", "kind": "하나", "base_value": 1.0},    # 영어 링크 없음
                     {"title": "가", "kind": "하나", "base_value": 2.0},
                     {"title": "라", "kind": "범위", "base_value": None}]}}}
        self.assertEqual([c[0] for c in m.candidates(field, "질량(kg)")], ["다", "가"])


class KoLine(unittest.TestCase):
    def read(self, line, cell="중량", base=None, units=None):
        units = units or m.survey3.MASS
        return m.find_ko(cell, units, line, base)

    def test_plain(self):
        q, num, text, val, why = self.read("- 중량: 106 kg", base=106.0)
        self.assertEqual((num, val, why), ("106", 106.0, None))

    def test_ton_and_gram(self):
        self.assertAlmostEqual(self.read("- 중량: 4.5톤", base=4500.0)[3], 4500.0)
        self.assertAlmostEqual(self.read("- 중량: 950g", base=0.95)[3], 0.95)

    def test_thousand_separator_and_kg_sign(self):
        self.assertEqual(self.read("- 중량: 1,464㎏", base=1464.0)[3], 1464.0)

    def test_one_paren_ok(self):
        self.assertEqual(self.read("- 중량: 370 kg (발사 시)", base=370.0)[3], 370.0)

    def test_two_values_skipped(self):
        why = self.read("- 중량: 3,625 kg (발사), 1,593 kg", base=3625.0)[4]
        self.assertIn("값 뒤에 더 있음", why)
        why = self.read("- 중량: 1,380kg(이륙시), 675kg (달궤도)", base=1380.0)[4]
        self.assertIn("값 뒤에 더 있음", why)  # make_short_test.only_paren은 이것을 받는다

    def test_approx_skipped(self):
        self.assertIn("값 뒤에 더 있음", self.read("- 중량: 1,400kg 내외", base=1400.0)[4])
        self.assertIn("어림", self.read("- 중량: 약 100 kg", base=100.0)[4])

    def test_label_not_number(self):
        self.assertIn("숫자로 시작하지 않음", self.read("- 총길이: 연장21.38 km", cell="총길이", base=21380.0, units=m.survey3.LEN_M)[4])

    def test_differs_from_survey(self):
        self.assertIn("survey 값과 다름", self.read("- 중량: 99 kg", base=106.0)[4])

    def test_missing_line_and_spaced_label(self):
        self.assertEqual(self.read("- 발사일: 1999", base=1.0)[4], "정보 상자 줄 없음")
        self.assertEqual(self.read("- 총 길이: 1,770m", cell="총길이", base=1770.0, units=m.survey3.LEN_M)[3], 1770.0)


class EnUnits(unittest.TestCase):
    def one(self, wiki, keys=("launch_mass",), units=KG):
        return cells(list(keys), units, wiki)

    def test_cvt_kg(self):
        self.assertEqual(self.one("| launch_mass = {{cvt|106|kg}}")[0][2], 106.0)

    def test_convert_with_second_unit_and_abbr(self):
        self.assertEqual(self.one("| launch_mass = {{convert|1,123|kg|lb|0|abbr=on}}<ref name=a/>")[0][2], 1123.0)

    def test_lb_to_kg(self):
        self.assertAlmostEqual(self.one("| launch_mass = {{convert|83.8|lb}}")[0][2], 83.8 * 0.45359237)
        self.assertAlmostEqual(self.one("| launch_mass = {{convert|1071|lb|kg|order=flip|abbr=on}}")[0][2], 1071 * 0.45359237)

    def test_tonne_and_gram(self):
        self.assertEqual(self.one("| launch_mass = 4.5 t")[0][2], 4500.0)
        self.assertAlmostEqual(self.one("| launch_mass = 950g<ref name=\"nasa\"/>")[0][2], 0.95)

    def test_ambiguous_ton_not_comparable(self):
        self.assertIn("단위 ton", self.one("| launch_mass = 2 tons")[0][3])

    def test_comment_only_cell_is_absent(self):
        self.assertEqual(self.one("| dry_mass = <!--spacecraft mass in orbit without fuel-->", keys=("dry_mass",)), [])

    def test_approx_and_trailing_text_not_comparable(self):
        self.assertIn("어림", self.one("| launch_mass = ≈3,939 kg<!--x-->")[0][3])
        self.assertIn("값 뒤에 더 있음", self.one("| launch_mass = {{convert|13.5|kg|abbr=on}} each")[0][3])

    def test_case_insensitive_key_and_repeated_key(self):
        c = self.one("| Mass = {{convert|8.2|kg|abbr=on}}", keys=("mass",))
        self.assertEqual((c[0][0], c[0][2]), ("mass", 8.2))
        c = self.one("| launch_mass = 381 kg\n| launch_mass = 381 kg<ref/>")
        self.assertEqual(len(c), 2)

    def test_length_units(self):
        self.assertEqual(self.one("| length = {{convert|3368|m}}", ("length",), M)[0][2], 3368.0)
        self.assertEqual(self.one("| length = {{convert|21.38|km|mi|abbr=on}}", ("length",), M)[0][2], 21380.0)
        self.assertAlmostEqual(self.one("| length = {{convert|5,000|ft}}", ("length",), M)[0][2], 1524.0)
        self.assertAlmostEqual(self.one("| length = {{convert|2|mi}}", ("length",), M)[0][2], 3218.688)
        self.assertEqual(self.one("| length = 1,941m", ("length",), M)[0][2], 1941.0)

    def test_other_keys_not_read(self):
        self.assertEqual(self.one("| mainspan = {{convert|1150|m}}\n| payload_mass = 5 kg", ("length", "launch_mass")), [])


class Match(unittest.TestCase):
    C = [("launch_mass", "x", 3445.0, None), ("dry_mass", "y", 1035.0, None)]

    def test_within_one_percent_boundary(self):
        # 차이는 영어 값 기준 퍼센트다
        self.assertIsNone(m.en_match(1000.0, [("launch_mass", "x", 1010.0, None)])[4])      # 0.99%
        self.assertIsNotNone(m.en_match(1000.0, [("launch_mass", "x", 1011.0, None)])[4])   # 1.09%
        self.assertIsNotNone(m.en_match(1011.0, [("launch_mass", "x", 1000.0, None)])[4])   # 1.1%

    def test_any_cell_matches(self):
        key, raw, ev, diff, why = m.en_match(1035.0, self.C)
        self.assertEqual((key, ev, why), ("dry_mass", 1035.0, None))
        self.assertEqual(diff, 0.0)

    def test_no_cell_matches_lists_all(self):
        why = m.en_match(1200.0, self.C)[4]
        self.assertIn("launch_mass=3445", why)
        self.assertIn("dry_mass=1035", why)

    def test_none_comparable_and_absent(self):
        self.assertIn("비교 불가", m.en_match(1.0, [("launch_mass", "x", None, "단위 없음: 5")])[4])
        self.assertIn("영어 값 없음", m.en_match(1.0, [])[4])

    def test_closest_cell_is_reported(self):
        key = m.en_match(100.0, [("launch_mass", "a", 100.9, None), ("dry_mass", "b", 100.1, None)])[0]
        self.assertEqual(key, "dry_mass")


class Format(unittest.TestCase):
    def test_format_value(self):
        self.assertEqual(m.format_value(1770.0), "1770")
        self.assertEqual(m.format_value(0.95), "0.95")
        self.assertEqual(m.format_value(260.68), "260.68")
        self.assertEqual(m.format_value(21380.0), "21380")


class Paragraph(unittest.TestCase):
    MD = ("# 마젤란 (우주선)\n\n- 마젤란\n- 임무 기간\n- 중량: 1,035kg\n\n"
          "{{틀}}\n\n![그림](a.png)\n\n| 표 | 값 |\n|---|---|\n\n"
          "마젤란은 미국의 금성 탐사선이다. 1989년에 발사되었다.\n\n둘째 단락이다.\n")

    def test_skips_infobox_template_image_table(self):
        self.assertEqual(m.first_paragraph(self.MD), "마젤란은 미국의 금성 탐사선이다. 1989년에 발사되었다.")

    def test_none_when_no_body(self):
        self.assertIsNone(m.first_paragraph("# 제목\n\n- 줄\n"))


if __name__ == "__main__":
    unittest.main()
