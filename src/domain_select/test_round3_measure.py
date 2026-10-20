"""round3_measure.py 시험. 네트워크를 쓰지 않는다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import round3_measure as rm


def raws(text):
    return [i["raw"] for i in rm.extract(text)]


class Extract(unittest.TestCase):
    def test_basic_units(self):
        self.assertEqual(raws("질량 48.6 kg, 높이 12m, 속도 7.5 km/s"), ["48.6 kg", "12m", "7.5 km/s"])

    def test_comma_and_space(self):
        it = rm.extract("고도 1,316.0 km 와 2,000kg")
        self.assertEqual([i["digits"] for i in it], ["1316.0", "2000"])
        self.assertEqual(it[0]["value"], 1316.0)

    def test_variants(self):
        it = rm.extract("110 Kg, 5㎏, 3t짜리, 4.5톤")
        self.assertEqual([i["base"] for i in it], [110.0, 5.0, 3000.0, 4500.0])

    def test_year_excluded(self):
        self.assertEqual(raws("1992년 8월 11일 발사, 2005 years ago, 1990s"), [])

    def test_year_not_excluded_when_small_or_other_unit(self):
        self.assertEqual(raws("5년 동안, 12 years, 3000 years"), ["5년", "12 years", "3000 years"])

    def test_not_a_unit(self):
        self.assertEqual(raws("5 million, 3 to 4, 제22호, KITSAT-1 10 meters"), [])

    def test_celsius_and_angle(self):
        it = rm.extract("20 °C 와 66.0°와 300 K")
        self.assertEqual([i["unit"] for i in it], ["°C", "°", "K"])
        self.assertAlmostEqual(it[0]["base"], 293.15)

    def test_decade_and_quarter_excluded(self):
        self.assertEqual(raws("60년대 3분기"), [])


class Convert(unittest.TestCase):
    def test_conversions(self):
        self.assertEqual(rm.to_base(4.5, "톤"), ("질량", 4500.0))
        self.assertAlmostEqual(rm.to_base(107, "lb")[1], 48.53, places=1)
        self.assertEqual(rm.to_base(1, "일")[1], 86400.0)
        self.assertEqual(rm.to_base(2, "km/s")[1], 2000.0)

    def test_close(self):
        self.assertTrue(rm.close(100, 100.9))
        self.assertFalse(rm.close(100, 102))
        self.assertTrue(rm.close(0, 0))


class Dedupe(unittest.TestCase):
    def test_same_value_other_unit_grouped(self):
        g = rm.dedupe(rm.extract("48.6 kg 이고 107 lb 이며 48.6 kg"))
        # 107 lb(=48.53 kg)는 48.6 kg의 ±1% 안이라 한 값이다
        self.assertEqual(len(g), 1)
        self.assertEqual(len(g[0]["mentions"]), 3)

    def test_far_values_not_grouped(self):
        self.assertEqual(len(rm.dedupe(rm.extract("48.6 kg, 50 kg"))), 2)

    def test_different_dimension_not_grouped(self):
        g = rm.dedupe(rm.extract("5 kg, 5 km"))
        self.assertEqual(len(g), 2)

    def test_mentions_kept(self):
        g = rm.dedupe(rm.extract("10 m 와 10 m"))
        self.assertEqual(len(g), 1)
        self.assertEqual(g[0]["mentions"], ["10 m", "10 m"])


class OtherLang(unittest.TestCase):
    def test_a_same_digits_without_unit(self):
        r = rm.only_numbers("무게 48.6 kg", "mass was 48.6 and more")
        self.assertEqual(r[0]["other_lang"], {"reason": "a", "found": "48.6"})

    def test_a_comma_removed(self):
        r = rm.only_numbers("고도 1,316 km", "altitude 1316 meters")
        self.assertEqual(r[0]["other_lang"]["reason"], "a")
        r = rm.only_numbers("고도 1316 km", "altitude 1,316 meters")
        self.assertEqual(r[0]["other_lang"]["reason"], "a")

    def test_a_not_substring(self):
        r = rm.only_numbers("무게 6 kg", "mass 48.6 and 16")
        self.assertEqual(r[0]["other_lang"], "그 언어에만")

    def test_a_decimal_kept(self):
        r = rm.only_numbers("고도 1316.0 km", "altitude 1316 here")
        self.assertEqual(r[0]["other_lang"], "그 언어에만")

    def test_b_unit_converted(self):
        r = rm.only_numbers("무게 4.5톤", "mass 4,500 kg")
        self.assertEqual(r[0]["other_lang"]["reason"], "b")
        self.assertEqual(r[0]["other_lang"]["found"], "4,500 kg")

    def test_b_other_dim_not_matched(self):
        r = rm.only_numbers("길이 4500 m", "mass 4,500 kg")
        self.assertEqual(r[0]["other_lang"]["reason"], "a")   # 숫자 글자는 같다
        r = rm.only_numbers("길이 4500.5 m", "mass 4,500.5 kg")
        self.assertEqual(r[0]["other_lang"]["reason"], "a")
        r = rm.only_numbers("길이 4400 m", "mass 4,500 kg")
        self.assertEqual(r[0]["other_lang"], "그 언어에만")

    def test_only(self):
        r = rm.only_numbers("임무 5년, 무게 48.6 kg", "mass 48.6 kg")
        self.assertEqual([x["other_lang"] == "그 언어에만" for x in r], [True, False])


class Lines(unittest.TestCase):
    def row(self, dom, i, lang, chars, tables, only):
        return {"domain": dom, "id": i, "lang": lang, "chars": chars, "table_count": tables, "infobox_lines": 3, "only_count": only}

    def rows(self, chars, tables, only, n=10):
        out = []
        for i in range(n):
            for lang in ("ko", "en"):
                out.append(self.row("kr_satellites", i, lang, chars, 1 if i < tables else 0, only))
        return out

    def test_all_pass(self):
        s = rm.summarize(self.rows(5000, 4, 4))[0]   # 4*10 = 40
        self.assertTrue(s["passed"])
        self.assertEqual((s["ko_only"], s["en_only"]), (40, 40))

    def test_each_line_fails_alone(self):
        self.assertFalse(rm.summarize(self.rows(4999, 4, 4))[0]["line1"])
        self.assertFalse(rm.summarize(self.rows(5000, 3, 4))[0]["line2"])
        self.assertFalse(rm.summarize(self.rows(5000, 3, 4))[0]["line3"])
        s = rm.summarize(self.rows(5000, 4, 3, n=10))[0]     # 30 < 36
        self.assertFalse(s["line4"])
        self.assertFalse(s["passed"])

    def test_line4_boundary(self):
        rows = self.rows(5000, 4, 3)
        rows[0]["only_count"] = 9      # ko 합 36
        rows[1]["only_count"] = 9      # en 합 36
        s = rm.summarize(rows)[0]
        self.assertEqual((s["ko_only"], s["en_only"]), (36, 36))
        self.assertTrue(s["line4"])

    def test_md_infobox_count(self):
        md = "# T\n\n- 가: 1\n- 나\n  - 다: 2\n\n본문 - 라: 3\n"
        self.assertEqual(rm.md_infobox_count(md.replace("# T\n\n", "# T\n")), 2)


if __name__ == "__main__":
    unittest.main()
