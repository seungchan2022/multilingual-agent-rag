"""quantities.py 시험. 네트워크를 쓰지 않는다. 규칙 절(1~9)마다 받는 예와 받지 않는 예를 둔다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import quantities as qt
from fetch_docs import to_markdown

CACHE = Path(__file__).resolve().parents[2] / "research_notes" / "stage2_stem_select" / "round2" / "stepper_check" / "cache"
NB, THIN, NNB = " ", " ", " "


def qs(text):
    """양 항목을 (raw, value, unit)로."""
    return [(i["raw"], i["value"], i["unit"]) for i in qt.quantities(text)]


def vals(text):
    return [i["value"] for i in qt.quantities(text)]


def bases(text):
    return [i["base"] for i in qt.quantities(text)]


def kinds(text):
    return [(i["kind"], i["raw"]) for i in qt.read(text)]


def unk(text):
    return [i["digits"] for i in qt.read(text) if i["kind"] == "모르는 숫자"]


def near(test, a, b, rel=1e-9):
    test.assertAlmostEqual(a / b, 1.0, delta=rel)


class Common(unittest.TestCase):
    """공통 칸과 건너뛰는 글자."""

    def test_common_fields(self):
        text = "첫 줄\n질량 12 kg"
        it = qt.read(text)[0]
        self.assertEqual((it["kind"], it["raw"], it["start"], it["end"], it["line"]), ("양", "12 kg", 7, 12, 1))
        self.assertEqual(text[it["start"]:it["end"]], it["raw"])

    def test_skipped_characters_keep_original_positions(self):
        text = "1097 K ​(824 °C, ​1515 °F)"
        its = qt.read(text)
        self.assertEqual([i["value"] for i in its], [1097.0, 824.0, 1515.0])
        for i in its:
            self.assertEqual(text[i["start"]:i["end"]], i["raw"])
        self.assertEqual(its[2]["raw"], "1515 °F")

    def test_each_skipped_char(self):
        for ch in "​‌‍⁠﻿­":
            its = qt.read(f"1{ch}2 kg")
            self.assertEqual([i["value"] for i in its], [12.0], repr(ch))
            self.assertEqual(its[0]["raw"], f"1{ch}2 kg")


class Number(unittest.TestCase):
    """1. 숫자의 모양."""

    def test_integer_decimal(self):
        self.assertEqual(qs("12 km"), [("12 km", 12.0, "km")])
        self.assertEqual(vals("0.073 AU"), [0.073])

    def test_comma_group(self):
        self.assertEqual(vals("1,316 km 와 15,000 km"), [1316.0, 15000.0])
        self.assertEqual(unk("1,316"), ["1316"])

    def test_comma_not_group(self):
        # 세 자리씩이 아니면 묶음이 아니다
        self.assertEqual(unk("1,3160"), ["1", "3160"])
        self.assertEqual(unk("2, 8, 18"), ["2", "8", "18"])

    def test_space_group(self):
        for sp in (NB, THIN, NNB):
            t = f"149{sp}597{sp}870{sp}700 m"
            self.assertEqual(vals(t), [149597870700.0], repr(sp))
        self.assertEqual(unk(f"0.002{THIN}569"), ["0.002569"])
        self.assertEqual(unk(f"12{NB}34"), ["12", "34"])           # 뒤 묶음이 세 자리가 아니면 묶음이 아니다

    def test_plain_space_not_group(self):
        self.assertEqual(unk("149 597 870"), ["149", "597", "870"])

    def test_sign(self):
        self.assertEqual(vals("(−60–28 °C)"), [-60.0, 28.0])
        self.assertEqual(vals("x: -5 K, +3 K, ;−2 K, ~−1 K"), [-5.0, 3.0, -2.0, -1.0])
        self.assertEqual(vals("a/-4 K"), [-4.0])

    def test_sign_not_after_letter_or_digit(self):
        self.assertEqual(vals("T−5 K"), [5.0])
        self.assertEqual(vals("5−3 K"), [3.0])            # 숫자 뒤의 −는 부호가 아니다(범위의 줄도 아니다)
        self.assertEqual(vals("2 K−3 K"), [2.0, 3.0])

    def test_sign_at_line_start(self):
        self.assertEqual(vals("−5 K"), [-5.0])
        self.assertEqual(vals("x\n−5 K"), [-5.0])

    def test_decor_not_in_value(self):
        for t in ("≥1.40 M🜨", "≤1.40 M🜨", ">1.40 M🜨", "<1.40 M🜨", "≈1.40 M🜨", "~1.40 M🜨", "약 1.40 M🜨",
                  "about 1.40 M🜨", "c. 1.40 M🜨", "ca. 1.40 M🜨"):
            self.assertEqual(vals(t), [1.40], t)
        it = qt.quantities("≥1.40±0.13 M🜨")[0]
        self.assertEqual(it["value"], 1.40)
        self.assertEqual(it["raw"], "1.40±0.13 M🜨")

    def test_exponent_forms(self):
        for t in ("8.06×10²⁴ kg", "8.06 × 10²⁴ kg", "8.06·10²⁴ kg", "8.06⋅10²⁴ kg", "8.06×10^24 kg"):
            it = qt.quantities(t)
            self.assertEqual(len(it), 1, t)
            near(self, it[0]["value"], 8.06e24)
            near(self, it[0]["base"], 8.06e24)
            self.assertEqual(it[0]["raw"], t)

    def test_exponent_negative_and_pure_power(self):
        near(self, vals("2×10⁻³ kg")[0], 2e-3)
        near(self, vals("2×10⁺³ kg")[0], 2e3)
        it = qt.quantities("거리 10⁸ km")
        near(self, it[0]["value"], 1e8)
        near(self, it[0]["base"], 1e11)
        self.assertEqual(it[0]["raw"], "10⁸ km")

    def test_exponent_unknown_keeps_mantissa_digits(self):
        its = qt.read("자기 감수율 24.31×10⁻⁶ cgs")          # cgs는 단위 표에 없다
        self.assertEqual([(i["kind"], i["digits"], i["raw"]) for i in its], [("모르는 숫자", "24.31", "24.31×10⁻⁶")])
        self.assertEqual(unk("10⁸ 개"), ["10"])

    def test_not_exponent(self):
        # 10 뒤에 위첨자가 없으면 지수가 아니다
        self.assertEqual(qs("5×10 km"), [("10 km", 10.0, "km")])
        self.assertEqual(unk("5×10 개"), ["5", "10"])
        self.assertEqual(unk("5² 개"), ["5"])          # 10ⁿ이 아닌 위첨자는 지수가 아니다

    def test_superscripts_not_numbers(self):
        self.assertEqual(qs("¹⁶⁶Yb 인공 56.7 h"), [("56.7 h", 56.7, "h")])
        self.assertEqual(kinds("¹⁶⁶Yb"), [])
        self.assertEqual(qs("[Xe] 4f¹⁴ 6s²"), [])
        self.assertEqual(qs("넓이 km²"), [])

    def test_ko_big_words(self):
        cases = {"4561만 km": 4561e4, "1억 4960만 km": 149600000, "26만 5천 km": 265000, "8천만 km": 80000000,
                 "40조 km": 4e13, "46억 km": 4.6e9, "4.6억 km": 4.6e8, "1억4960만km": 149600000, "3천 km": 3000}
        for t, v in cases.items():
            it = qt.quantities(t)
            self.assertEqual(len(it), 1, t)
            near(self, it[0]["value"], v)
            self.assertEqual(it[0]["raw"], t)

    def test_en_big_words(self):
        near(self, vals("6.9 million km")[0], 6.9e6)
        near(self, vals("194 trillion km")[0], 1.94e14)
        near(self, vals("3 thousand km")[0], 3e3)
        near(self, vals("2 billion years")[0], 2e9)
        near(self, vals("180 million years")[0], 1.8e8)

    def test_big_words_unit_decides(self):
        # 단위가 없으면 모르는 숫자, 단위가 붙으면 양
        self.assertEqual(unk("6.9 million"), ["6.9"])
        self.assertEqual(qs("6.9 million"), [])
        self.assertEqual(unk("4561만"), ["4561"])
        self.assertEqual(unk("5만큼"), ["5"])       # 만 뒤에 조사가 아닌 한글이 오면 큰 수 낱말이 아니다
        self.assertEqual(len(qs("46억 년")), 1)
        near(self, bases("46억 년")[0], 4.6e9 * 31557600)

    def test_big_word_not_mi(self):
        self.assertEqual(qs("5 million"), [])
        self.assertEqual(unk("5 million"), ["5"])

    def test_tolerance(self):
        cases = [("0.0718+0.0008 −0.0009 AU", 0.0718, "AU"), ("279±4 K", 279.0, "K"), ("0.049640±0.000004 AU", 0.049640, "AU"),
                 ("187±8 pm", 187.0, "pm"), ("9.8556+0.0012 −0.0011 d", 9.8556, "d"), ("279 ± 4 K", 279.0, "K"),
                 ("0.0718+0.0008 -0.0009 AU", 0.0718, "AU")]
        for t, v, u in cases:
            it = qt.quantities(t)
            self.assertEqual(len(it), 1, t)
            self.assertEqual((it[0]["value"], it[0]["unit"], it[0]["raw"]), (v, u, t), t)

    def test_tolerance_paren(self):
        self.assertEqual(unk("173.045(10)"), ["173.045"])
        self.assertEqual(vals("173.045(10) km"), [173.045])
        self.assertEqual(unk("1047 (1266)"), ["1047", "1266"])      # 띄어 쓴 괄호는 오차 폭이 아니다
        self.assertEqual(unk("5(a)"), ["5"])

    def test_tolerance_no_item(self):
        self.assertEqual(unk("173.045±0.010, 173.05±0.02 (abridged)"), ["173.045", "173.05"])

    def test_ranges(self):
        self.assertEqual(qs("213–301 K"), [("213", 213.0, "K"), ("301 K", 301.0, "K")])
        self.assertEqual(vals("−60–28 °C"), [-60.0, 28.0])
        self.assertEqual(vals("−76–82 °F"), [-76.0, 82.0])
        self.assertEqual(vals("5-10 km"), [5.0, 10.0])
        self.assertEqual(vals("5 ~ 10 km"), [5.0, 10.0])
        self.assertEqual(vals("5∼10 km"), [5.0, 10.0])
        self.assertEqual(vals("5 to 10 km"), [5.0, 10.0])
        self.assertEqual(vals("5 – 10 km"), [5.0, 10.0])
        self.assertEqual(vals("5~−10 km"), [5.0, -10.0])
        self.assertEqual([i["dim"] for i in qt.quantities("213–301 K")], ["온도", "온도"])
        near(self, bases("−60–28 °C")[0], 213.15)

    def test_range_needs_unit(self):
        self.assertEqual(qs("5–10 개"), [])
        self.assertEqual(unk("5–10 개"), ["5", "10"])
        self.assertEqual(unk("1990–2000"), ["1990", "2000"])

    def test_range_not_when_a_has_unit(self):
        self.assertEqual(qs("5 km – 10 km"), [("5 km", 5.0, "km"), ("10 km", 10.0, "km")])

    def test_fraction(self):
        self.assertEqual(unk("3분의 1"), ["3", "1"])
        self.assertEqual(qs("3분의 1"), [])


class Names(unittest.TestCase):
    """2. 이름(숫자 글자이지만 값이 아닌 것). 이름은 양도 모르는 숫자도 아니다."""

    def names(self, text):
        return [i["raw"] for i in qt.read(text) if i["kind"] == "이름"]

    def only_names(self, text, expect):
        self.assertEqual(self.names(text), expect, text)
        self.assertEqual([i for i in qt.read(text) if i["kind"] != "이름"], [], text)

    def test_letter_before(self):
        self.only_names("G9 형 별", ["9"])
        self.only_names("M4.5 지진", ["4.5"])
        self.only_names("Eu2O3", ["2", "3"])

    def test_letter_after_not_unit(self):
        self.only_names("22b", ["22"])
        self.only_names("4f 6s²", ["4", "6"])
        self.only_names("6s²", ["6"])
        self.only_names("390Lb", ["390"])
        self.only_names("4f¹⁴ 6s²", ["4", "6"])

    def test_hyphen_before(self):
        self.only_names("Kepler-22b", ["22"])
        self.only_names("COROT-7b", ["7"])
        self.only_names("OGLE-2003-BLG-235L b", ["2003", "235"])
        self.only_names("케플러-22b", ["22"])

    def test_hyphen_chain_of_numbers(self):
        self.only_names("CAS 7440-64-4", ["7440", "64", "4"])
        self.only_names("1-2-3", ["1", "2", "3"])

    def test_ordinals(self):
        self.only_names("1st 2nd 3rd 4th 21st", ["1", "2", "3", "4", "21"])
        self.only_names("제22호", ["22"])
        self.only_names("40번째", ["40"])
        self.only_names("1차 2차", ["1", "2"])

    def test_not_names(self):
        self.assertEqual(qs("12m"), [("12m", 12.0, "m")])
        self.assertEqual(qs("3t짜리"), [("3t", 3.0, "t")])
        self.assertEqual(qs("5 km"), [("5 km", 5.0, "km")])
        self.assertEqual(self.names("5 개, 10-20 km"), [])
        self.assertEqual(self.names("a 5"), [])

    def test_names_not_counted(self):
        self.assertEqual(unk("Kepler-22b 7 개"), ["7"])
        self.assertEqual(qs("Kepler-22b 5 km"), [("5 km", 5.0, "km")])


class Units(unittest.TestCase):
    """3. 숫자 뒤의 단위와 경계."""

    def test_every_listed_unit_is_read(self):
        for key in qt.UNITS:
            its = qt.quantities(f"5 {key}")
            self.assertEqual([(i["unit"], i["value"]) for i in its], [(key, 5.0)], key)

    def test_gap_between_number_and_unit(self):
        for gap in ("", " ", NB, THIN, NNB):
            self.assertEqual(vals(f"12{gap}km"), [12.0], repr(gap))
        self.assertEqual(vals("12  km"), [])

    def test_longest_unit(self):
        self.assertEqual(qs("7.5 km/s"), [("7.5 km/s", 7.5, "km/s")])
        self.assertEqual(qs("38.5 W/(m⋅K)"), [("38.5 W/(m⋅K)", 38.5, "W/(m⋅K)")])
        self.assertEqual(qs("0.25 µΩ⋅m")[0][2], "µΩ⋅m")
        self.assertEqual(qs("0.25 μ Ω·m")[0][2], "μ Ω·m")
        self.assertEqual([i["dim"] for i in qt.quantities("5 km/s 5 km 5 °C")], ["속도", "길이", "온도"])
        self.assertEqual(qs("154.522 J/(kg·K)")[0][2], "J/(kg·K)")
        self.assertEqual(qs("5 W/m·K")[0][2], "W/m·K")

    def test_boundary_rejects_longer_word_or_other_unit(self):
        self.assertEqual(qs("1515 °F"), [("1515 °F", 1515.0, "°F")])
        self.assertEqual(qs("0.00362 L☉"), [("0.00362 L☉", 0.00362, "L☉")])
        self.assertEqual([i["dim"] for i in qt.quantities("0.00362 L☉")], ["출력"])
        self.assertEqual(qs("5 million"), [])
        self.assertEqual(qs("6 KB"), [])
        for t in ("5 m/s3", "5 km²x", "5 km^2", "5 km_s", "5 kg·m", "5 m′", "5 m″", "5 mm2x"):
            self.assertEqual(qs(t), [], t)

    def test_boundary_letters_digits_and_superscripts(self):
        self.assertEqual(qs("5 mile"), [("5 mile", 5.0, "mile")])
        self.assertEqual(qs("5 miles."), [("5 miles", 5.0, "miles")])
        self.assertEqual(qs("5 mi2"), [])
        self.assertEqual(qs("5 km²"), [("5 km²", 5.0, "km²")])
        self.assertEqual(qs("5 km2"), [("5 km2", 5.0, "km2")])
        self.assertEqual(qs("5 km³"), [("5 km³", 5.0, "km³")])

    def test_unlisted_unit_is_unknown_number(self):
        self.assertEqual(qs("5 foo"), [])
        self.assertEqual(unk("5 foo, 6 barish"), ["5", "6"])

    def test_two_meaning_symbols_not_units(self):
        for u in ("MJ", "도", "a", "in", "A", "V", "u", "줄"):
            self.assertEqual(qs(f"5 {u}"), [], u)
            self.assertEqual(unk(f"5 {u}"), ["5"], u)

    def test_korean_unit_with_particle(self):
        for t in ("4일에", "3년간", "3일째", "5 km를", "3t짜리", "4일 동안", "6 km는"):
            self.assertEqual(len(qs(t)), 1, t)

    def test_korean_unit_without_particle(self):
        for t in ("60년대", "3분기", "1일차", "5초기", "6주기"):
            self.assertEqual(qs(t), [], t)
        self.assertEqual(len(qs("6주")), 1)
        self.assertEqual(len(qs("5초")), 1)

    def test_year_before_year_unit_is_a_date(self):
        for t, raw in (("2005 years ago", "2005 years"), ("2007년에", "2007년"), ("1000 yr", "1000 yr"), ("2100 year", "2100 year"),
                       ("2007 년", "2007 년")):
            self.assertEqual([(i["kind"], i["raw"]) for i in qt.read(t)], [("날짜", raw)], t)
        for t in ("999 years", "2101 years", "1500.5 years", "5 년"):
            self.assertEqual(len(qs(t)), 1, t)
        self.assertEqual(len(qs("1500 km")), 1)

    def test_degree_c_with_space(self):
        its = qt.quantities("Density (at 20° C): 6.967 g/cm³ (5° F)")
        self.assertEqual([(i["raw"], i["dim"]) for i in its], [("20° C", "온도"), ("6.967 g/cm³", "밀도"), ("5° F", "온도")])
        near(self, its[0]["base"], 293.15)

    def test_conversions(self):
        near(self, bases("1 AU")[0], 1.495978707e11)
        near(self, bases("1 ly")[0], 9.4607304725808e15)
        near(self, bases("2 mi")[0], 3218.688)
        near(self, bases("1 km/h")[0], 1 / 3.6)
        near(self, bases("1 eV")[0], 1.602176634e-19)
        near(self, bases("1097 K")[0], 1097.0)
        near(self, bases("1515 °F")[0], 1097.0388888888888)
        near(self, bases("824 ℃")[0], 1097.15)
        near(self, bases("1 d")[0], 86400.0)
        near(self, bases("1 년")[0], 31557600.0)
        near(self, bases("6.26 파섹")[0], 6.26 * 3.0856775814913673e16)
        near(self, bases("1 g/cm³")[0], 1000.0)
        near(self, bases("1 rad")[0], 57.29577951308232)
        self.assertEqual([i["dim"] for i in qt.quantities("1 d 1 년 1 ha 1 L 1 atm 1 kcal 1 J/mol 1 mas 1 GHz 1 g/mol")],
                         ["시간", "시간", "넓이", "부피", "압력", "에너지", "몰 에너지", "각도", "진동수", "몰 질량"])


class Prefix(unittest.TestCase):
    """4. 앞에 오는 말."""

    def one(self, text):
        its = qt.quantities(text)
        self.assertEqual(len(its), 1, text)
        return its[0]

    def test_speed(self):
        it = self.one("초속 11.2 km")
        self.assertEqual((it["raw"], it["value"], it["unit"], it["dim"], it["how"]), ("초속 11.2 km", 11.2, "km", "속도", "앞"))
        near(self, it["base"], 11200.0)
        it = self.one("시속 100 km로")
        self.assertEqual((it["dim"], it["how"]), ("속도", "앞"))
        near(self, it["base"], 100 / 3.6)
        near(self, self.one("초속 340 m")["base"], 340.0)
        near(self, self.one("초속 2 mi")["base"], 2 * 1609.344)

    def test_speed_needs_length_unit(self):
        it = self.one("초속 5 kg")
        self.assertEqual((it["dim"], it["how"], it["raw"]), ("질량", "뒤", "5 kg"))
        self.assertEqual(qs("초속 5 개"), [])
        self.assertEqual(unk("초속 5 개"), ["5"])

    def test_celsius_fahrenheit_do(self):
        it = self.one("섭씨 29도에서")
        self.assertEqual((it["raw"], it["value"], it["unit"], it["dim"], it["how"]), ("섭씨 29도", 29.0, "도", "온도", "앞"))
        near(self, it["base"], 302.15)
        it = self.one("화씨 84도")
        near(self, it["base"], (84 - 32) * 5 / 9 + 273.15)
        self.assertEqual(it["how"], "앞")

    def test_below_zero(self):
        for t in ("영하 5도", "영하 5 °C", "영하 5 ℃", "섭씨 영하 5도", "섭씨 영하 5 °C", "영하 5°C"):
            it = self.one(t)
            self.assertEqual(it["value"], -5.0, t)
            near(self, it["base"], 268.15)
            self.assertEqual(it["raw"], t, t)
        self.assertEqual(self.one("영하 5도")["how"], "앞")
        self.assertEqual(self.one("영하 5 °C")["how"], "뒤")
        near(self, self.one("화씨 영하 4도")["base"], (-4 - 32) * 5 / 9 + 273.15)

    def test_explicit_unit_wins(self):
        it = self.one("섭씨 100 °C")
        self.assertEqual((it["raw"], it["how"]), ("100 °C", "뒤"))

    def test_do_without_prefix_is_not_a_unit(self):
        self.assertEqual(qs("29도"), [])
        self.assertEqual(unk("29도"), ["29"])
        self.assertEqual(unk("섭씨 29도시"), ["29"])
        self.assertEqual(unk("가섭씨 29 개"), ["29"])


class Dates(unittest.TestCase):
    """5. 날짜는 세지 않고 같은 값 판정의 근거로도 쓰지 않는다. 모르는 숫자도 아니다."""

    def only_date(self, text, raw=None):
        self.assertEqual([(i["kind"], i["raw"]) for i in qt.read(text)], [("날짜", raw or text)], text)

    def test_korean_forms(self):
        for t in ("2007년 3월 5일", "2007년 3월", "3월 5일", "2007년", "2007 년", "1990년대", "20세기", "2007년3월5일", "8월 11일"):
            self.only_date(t)
        self.only_date("2007년 3월 5일에", "2007년 3월 5일")

    def test_english_and_numeric_forms(self):
        for t in ("2007-04-05", "4 April 2007", "April 4, 2007", "April 2007", "4 April", "Jan. 5, 2007", "4 Dec.", "15 May 1990",
                  "1990s", "21st century", f"4{NB}April 2007"):
            self.only_date(t)

    def test_date_inside_text(self):
        its = qt.read("Discovery date: 4 April 2007; 12.932 일")
        self.assertEqual([(i["kind"], i["raw"]) for i in its], [("날짜", "4 April 2007"), ("양", "12.932 일")])

    def test_not_dates(self):
        self.assertEqual(unk("발견: 1878"), ["1878"])
        self.assertEqual(unk("Discovery: Jean Charles Galissard de Marignac (1878)"), ["1878"])
        self.assertEqual(unk("T (K) 736 813 910 1047 (1266) (1465)"), ["736", "813", "910", "1047", "1266", "1465"])
        self.assertEqual(unk("April 4"), ["4"])
        self.assertEqual(unk("3월에"), ["3"])
        self.assertEqual(unk("4 Mars"), ["4"])
        self.assertEqual(unk("60년대"), ["60"])
        self.assertEqual([i["kind"] for i in qt.read("2007-13-05")], ["이름"] * 3)     # 달이 아니면 날짜가 아니라 숫자-숫자-숫자 이름이다
        self.assertEqual(qs("4일에 한 바퀴"), [("4일", 4.0, "일")])
        self.assertEqual(unk("1990 개"), ["1990"])

    def test_dates_do_not_leak_digits(self):
        t = "2007년 3월 5일, 4 April 2007, 1990s, 21st century"
        self.assertEqual([i["kind"] for i in qt.read(t)], ["날짜"] * 4)


class MultiPart(unittest.TestCase):
    """6. 여러 칸 표기는 한 값이다."""

    def one(self, text):
        its = qt.read(text)
        self.assertEqual(len(its), 1, text)
        return its[0]

    def test_right_ascension(self):
        for t, deg in (("15h 19m 26s", 15 * 15 + 19 * 0.25 + 26 / 240), ("15ʰ 19ᵐ 26ˢ", 15 * 15 + 19 * 0.25 + 26 / 240),
                       ("15ʰ 19ᵐ 26.8ˢ", 15 * 15 + 19 * 0.25 + 26.8 / 240)):
            it = self.one(t)
            self.assertEqual((it["kind"], it["dim"], it["how"], it["raw"]), ("양", "각도", "여러 칸", t), t)
            near(self, it["base"], deg)
            near(self, it["value"], deg)

    def test_degrees_minutes_seconds(self):
        for t, deg in (("−07° 43′ 20″", -(7 + 43 / 60 + 20 / 3600)), ("-07° 43′ 20″", -(7 + 43 / 60 + 20 / 3600)),
                       ("+17° 27′ 22″", 17 + 27 / 60 + 22 / 3600), ("43° 15′", 43.25), ("43°15′20″", 43 + 15 / 60 + 20 / 3600)):
            it = self.one(t)
            self.assertEqual((it["kind"], it["dim"], it["how"], it["raw"]), ("양", "각도", "여러 칸", t), t)
            near(self, it["base"], deg)

    def test_degree_alone_and_hour_alone(self):
        it = self.one("43°")
        self.assertEqual((it["dim"], it["how"]), ("각도", "뒤"))
        it = self.one("15h")
        self.assertEqual((it["dim"], it["how"]), ("시간", "뒤"))
        self.assertEqual(qs("19m"), [("19m", 19.0, "m")])

    def test_same_dimension_big_to_small(self):
        for t, secs in (("3 days 7.5 hours", 3.3125 * 86400), ("3일 7시간", 3 * 86400 + 7 * 3600), ("1 h 30 min", 5400.0),
                        ("2년 3개월", 2 * 31557600 + 3 * 2629746), ("1 km 20 m", 1020.0), ("2 kg 500 g", 2.5)):
            it = self.one(t)
            self.assertEqual((it["kind"], it["how"], it["raw"]), ("양", "여러 칸", t), t)
            near(self, it["base"], secs)
        it = self.one("3 days 7.5 hours")
        self.assertEqual((it["value"], it["unit"], it["dim"]), (3.3125, "days", "시간"))

    def test_not_merged(self):
        self.assertEqual(vals("1097 K (824 °C, 1515 °F)"), [1097.0, 824.0, 1515.0])
        self.assertEqual(vals("1 h, 30 min"), [1.0, 30.0])
        self.assertEqual(vals("1 h (30 min)"), [1.0, 30.0])
        self.assertEqual(vals("5 km 3 km"), [5.0, 3.0])               # 작아지지 않으면 잇지 않는다
        self.assertEqual(vals("3 hours 7.5 days"), [3.0, 7.5])        # 작은 것부터는 잇지 않는다
        self.assertEqual(vals("3 days 5 km"), [3.0, 5.0])             # 차원이 다르면 잇지 않는다
        self.assertEqual(vals("20 °C 5 °C"), [20.0, 5.0])
        self.assertEqual(vals("3 days; 7 hours"), [3.0, 7.0])
        self.assertEqual([i["how"] for i in qt.quantities("1 h, 30 min")], ["뒤", "뒤"])


class ContextUnit(unittest.TestCase):
    """7. 이름 칸과 머리글의 단위."""

    def test_infobox_name_unit(self):
        it = qt.quantities("- 평균거리(AU): 0.073")
        self.assertEqual([(i["raw"], i["value"], i["unit"], i["dim"], i["how"]) for i in it], [("0.073", 0.073, "AU", "길이", "이름 칸")])
        near(self, it[0]["base"], 0.073 * 1.495978707e11)
        self.assertEqual([i["how"] for i in qt.quantities("  - 반지름[km]: 6,371")], ["이름 칸"])
        self.assertEqual(vals("  - 온도 (K): 1097"), [1097.0])
        self.assertEqual(vals("- 거리(AU): 0.04–0.05"), [0.04, 0.05])
        self.assertEqual([i["how"] for i in qt.quantities("- 거리(AU): 0.04–0.05")], ["이름 칸", "이름 칸"])

    def test_infobox_name_not_unit(self):
        self.assertEqual(qs("- 밀도 (상온 근처): 12"), [])
        self.assertEqual(unk("- 밀도 (상온 근처): 12"), ["12"])
        self.assertEqual(unk("- 전기 음성도 (폴링 척도): 1.1"), ["1.1"])
        self.assertEqual(unk("- 값 (MJ): 3"), ["3"])

    def test_infobox_only_value_part_and_only_bullets(self):
        self.assertEqual(unk("평균거리(AU): 0.073"), ["0.073"])          # 목록 줄이 아니다
        self.assertEqual(unk("- 평균거리(AU) 0.073"), ["0.073"])         # 이름: 값 모양이 아니다
        self.assertEqual(vals("- 2번 (AU): 0.5"), [0.5])

    def test_year_in_year_column_is_a_date(self):
        self.assertEqual([i["kind"] for i in qt.read("- 발견(년): 1995")], ["날짜"])
        self.assertEqual(vals("- 주기(년): 12"), [12.0])

    def test_explicit_unit_first(self):
        its = qt.quantities("- 평균거리(AU): 5 km")
        self.assertEqual([(i["unit"], i["how"]) for i in its], [("km", "뒤")])

    def test_not_unit_values_in_infobox(self):
        its = qt.read("- 지름(km): Kepler-22b, 2007년, 22b, 3분의 1")
        self.assertEqual([i["kind"] for i in its], ["이름", "날짜", "이름", "모르는 숫자", "모르는 숫자"])

    TABLE = "| 이름 | 질량 (kg) | 반지름 [km] | 비고 (표) |\n|---|---|---|---|\n| A | 5.97 | 6371 | 3 |\n| B | 2 g | 2,000 m | 4 |\n"

    def test_table_header_unit(self):
        its = qt.quantities(self.TABLE)
        self.assertEqual([(i["raw"], i["unit"], i["how"]) for i in its],
                         [("5.97", "kg", "머리글"), ("6371", "km", "머리글"), ("2 g", "g", "뒤"), ("2,000 m", "m", "뒤")])
        self.assertEqual(unk(self.TABLE), ["3", "4"])

    def test_table_pipe_escape_and_extent(self):
        t = "| 값 (km) | 메모 |\n|---|---|\n| 5 \\| 7 | 9 |\n"
        self.assertEqual(qs(t), [("5", 5.0, "km"), ("7", 7.0, "km")])
        self.assertEqual(unk(t), ["9"])
        # 머리글 칸 자체와 표가 끝난 뒤의 줄은 단위를 받지 않는다
        t = "| 값 (km) 3 |\n|---|\n| 5 |\n\n6\n"
        self.assertEqual(unk(t), ["3", "6"])
        self.assertEqual(vals(t), [5.0])

    def test_not_a_table_without_separator(self):
        t = "| 값 (km) |\n| 5 |\n"
        self.assertEqual(qs(t), [])

    def test_table_cell_does_not_cross_pipe(self):
        t = "| 값 (km) | 메모 |\n|---|---|\n| 5 | km |\n"
        self.assertEqual(qs(t), [("5", 5.0, "km")])


class Formula(unittest.TestCase):
    """8. 수식 안에서는 단위를 읽지 않고, 위·아래 첨자 자리의 숫자는 숫자로 보지 않는다."""

    def test_example(self):
        t = r"\(M_{\rm {J}}=1.8986\times 10^{27}{\mbox{ kg}}\)"
        its = qt.read(t)
        self.assertEqual([(i["kind"], i["digits"], i["raw"]) for i in its], [("모르는 숫자", "1.8986", "1.8986"), ("모르는 숫자", "10", "10")])
        self.assertEqual(t[its[0]["start"]:its[0]["end"]], "1.8986")
        self.assertEqual(qs(t), [])

    def test_units_not_read_inside(self):
        self.assertEqual(qs(r"\(5 km\)"), [])
        self.assertEqual(unk(r"\(5 km\)"), ["5"])
        self.assertEqual(unk(r"\[ T = 273.15 \, \mathrm{K} \]"), ["273.15"])

    def test_super_and_subscript_digits_skipped(self):
        self.assertEqual(unk(r"\(x_{12}^2 + 5 y_3 - z^{-4}\)"), ["5"])
        self.assertEqual(unk(r"\(a^{b_{1}} + 7\)"), ["7"])
        self.assertEqual(unk(r"\(e^\circ + 2\)"), ["2"])

    def test_text_outside_is_read_normally(self):
        its = qt.read(r"질량 5 kg \(x=3\) 와 7 km")
        self.assertEqual([(i["kind"], i["raw"]) for i in its], [("양", "5 kg"), ("모르는 숫자", "3"), ("양", "7 km")])

    def test_unit_does_not_cross_formula_edge(self):
        self.assertEqual(qs(r"5 \(km\)"), [])
        self.assertEqual(unk(r"5 \(km\)"), ["5"])

    def test_display_formula_over_lines(self):
        t = "앞 3 m\n\\[\n a = 5\n   + 6 \\cdot 2\n\\]\n뒤 4 m"
        its = qt.read(t)
        self.assertEqual([(i["kind"], i["raw"]) for i in its],
                         [("양", "3 m"), ("모르는 숫자", "5"), ("모르는 숫자", "6"), ("모르는 숫자", "2"), ("양", "4 m")])
        self.assertEqual([i["line"] for i in its], [0, 2, 3, 3, 5])
        for i in its:
            self.assertEqual(t[i["start"]:i["end"]], i["raw"])

    def test_command_names_are_not_letters(self):
        self.assertEqual(unk(r"\(\sqrt2 + \frac{1}{2}\)"), ["2", "1", "2"])

    def test_letter_digit_names_inside(self):
        self.assertEqual([i["kind"] for i in qt.read(r"\(Eu2O3\)")], ["이름", "이름"])


class Others(unittest.TestCase):
    """9. 그 밖: 백분율은 비율이고, 배는 단위가 아니다."""

    def test_percent(self):
        for t in ("47.8%", "85 %", f"85{NB}%", "0.126%", "47.8±0.2%"):
            self.assertEqual([(i["kind"], i["raw"]) for i in qt.read(t)], [("비율", t)], t)
        its = qt.read("0.126% stable 14.2159999999% 32.014 d")
        self.assertEqual([i["kind"] for i in its], ["비율", "비율", "양"])

    def test_percent_before_context_unit(self):
        self.assertEqual([i["kind"] for i in qt.read("- 비율(km): 5%")], ["비율"])

    def test_percent_after_range_is_not_a_quantity_range(self):
        self.assertEqual([(i["kind"], i["raw"]) for i in qt.read("10–20%")], [("모르는 숫자", "10"), ("비율", "20%")])

    def test_times_is_not_a_unit(self):
        self.assertEqual(qs("1.5배"), [])
        self.assertEqual(unk("1.5배"), ["1.5"])
        self.assertEqual(unk("지구의 3배 크다"), ["3"])

    def test_no_overlap_and_order(self):
        text = ("Kepler-22b 0.073+0.0008 −0.0009 AU 213–301 K 8.06×10²⁴ kg 7440-64-4 3 days 7.5 hours 15ʰ 19ᵐ 26ˢ 47.8% 3분의 1 "
                "2007년 3월 5일 \\(x=3\\) 영하 5도 초속 11.2 km")
        its = qt.read(text)
        spans = [(i["start"], i["end"]) for i in its]
        self.assertEqual(spans, sorted(spans))
        for (a1, b1), (a2, b2) in zip(spans, spans[1:]):
            self.assertLessEqual(b1, a2)
        for i in its:
            self.assertEqual(text[i["start"]:i["end"]], i["raw"])

    def test_unknown_digits_set(self):
        self.assertEqual(qt.unknown_digits("1,316 0.002 569 5 km 2007년 6주기 6주기"), {"1316", "0.002569", "6"})
        self.assertEqual(qt.unknown_digits(""), set())


class RealDocs(unittest.TestCase):
    """저장된 실제 문서를 to_markdown으로 바꾼 글을 읽는다(파일은 읽기만 한다)."""

    @classmethod
    def doc(cls, name, title):
        path = CACHE / name
        if not path.exists():
            raise unittest.SkipTest(f"{path} 없음")
        return to_markdown(title, path.read_bytes())

    @staticmethod
    def line(md, head):
        found = [ln for ln in md.split("\n") if ln.startswith(("- ", "  - ")) and ln.lstrip(" -").startswith(head)]
        assert len(found) == 1, (head, found)
        return found[0]

    def test_ytterbium_en(self):
        md = self.doc("en_1380332337.html", "Ytterbium")
        its = qt.quantities(self.line(md, "Melting point"))
        self.assertEqual([(i["unit"], i["dim"]) for i in its], [("K", "온도"), ("°C", "온도"), ("°F", "온도")])
        for i in its:
            self.assertLess(abs(i["base"] / 1097 - 1), 0.01, i["raw"])
        its = qt.quantities(self.line(md, "Density"))
        self.assertEqual([(i["raw"], i["dim"]) for i in its], [("20° C", "온도"), ("6.967 g/cm³", "밀도")])
        self.assertEqual(qt.quantities(self.line(md, "Electron configuration")), [])
        self.assertEqual([i["kind"] for i in qt.read(self.line(md, "Electron configuration"))], ["이름", "이름"])

    def test_ross_128_b_en(self):
        md = self.doc("en_1378593358.html", "Ross 128 b")
        its = qt.quantities(self.line(md, "Mass: ≥1.40"))
        self.assertEqual(its[0]["raw"], "1.40±0.13 M🜨")
        self.assertEqual(its[0]["value"], 1.40)
        self.assertEqual(len(its), 2)
        its = qt.quantities(self.line(md, "Semi-major axis"))
        self.assertEqual([(i["value"], i["unit"]) for i in its], [(0.04964, "AU")])
        its = qt.quantities(self.line(md, "Temperature"))
        self.assertEqual([(i["value"], i["unit"]) for i in its],
                         [(213.0, "K"), (301.0, "K"), (-60.0, "°C"), (28.0, "°C"), (-76.0, "°F"), (82.0, "°F")])
        near(self, its[2]["base"], 213.15)
        its = [i for i in qt.quantities(md) if i["raw"] == "8.06×10²⁴ kg"]
        self.assertEqual(len(its), 1)
        near(self, its[0]["base"], 8.06e24)

    def test_gliese_581_c_ko(self):
        md = self.doc("ko_42643352.html", "글리제 581 c")

        def one(head):
            its = qt.read(self.line(md, head))
            self.assertEqual(len(its), 1, head)
            return its[0]
        it = one("적경")
        near(self, it["base"], 229.858333, 1e-7)
        self.assertEqual((it["dim"], it["how"]), ("각도", "여러 칸"))
        near(self, one("적위")["base"], -7.722222, 1e-6)
        its = qt.quantities(self.line(md, "거리"))
        self.assertEqual([(i["unit"], i["dim"]) for i in its], [("파섹", "길이"), ("광년", "길이")])
        it = one("평균거리")
        self.assertEqual((it["value"], it["unit"], it["how"]), (0.073, "AU", "이름 칸"))
        self.assertEqual((one("공전주기")["dim"], one("공전주기")["unit"]), ("시간", "일"))
        self.assertEqual(one("각거리")["dim"], "각도")
        self.assertEqual(one("질량")["kind"], "모르는 숫자")
        self.assertEqual(one("발견일")["kind"], "날짜")

    def test_ytterbium_ko(self):
        md = self.doc("ko_42388980.html", "이터븀")
        its = qt.read(self.line(md, "녹는점"))
        self.assertEqual([(i["kind"], i["dim"]) for i in its], [("양", "온도")])
        self.assertEqual(qt.quantities(self.line(md, "주기:")), [])
        self.assertEqual([(i["kind"], i["digits"]) for i in qt.read(self.line(md, "주기:"))], [("모르는 숫자", "6")])
        self.assertEqual([(i["kind"], i["digits"]) for i in qt.read(self.line(md, "발견"))], [("모르는 숫자", "1878")])
        its = [i for i in qt.read(self.line(md, "동위체")) if i["raw"] == "56.7 h"]
        self.assertEqual(len(its), 1)
        self.assertNotIn("166", qt.unknown_digits(self.line(md, "동위체")))
        self.assertEqual([i["kind"] for i in qt.read(self.line(md, "CAS 번호"))], ["이름"] * 3)


class UnitTable(unittest.TestCase):
    """단위 표를 일반 목록으로 채운 것(decisions/stage2.md 2026-10-21 "세는 규칙 보완의 방향" 줄 ㉡)."""

    def one(self, text):
        its = qt.quantities(text)
        self.assertEqual(len(its), 1, its)
        return its[0]

    def check(self, text, dim, base, unit=None):
        it = self.one(text)
        self.assertEqual(it["dim"], dim, text)
        near(self, it["base"], base)
        if unit:
            self.assertEqual(it["unit"], unit)

    # 1. 이미 있는 단위의 영어 이름과 한국어 이름
    def test_english_names_of_existing_units(self):
        text = "Launch mass: 115 kilograms (254 lb)"
        self.assertEqual(qs(text), [("115 kilograms", 115.0, "kilograms"), ("254 lb", 254.0, "lb")])
        self.assertEqual([i["dim"] for i in qt.quantities(text)], ["질량", "질량"])
        self.assertEqual(bases(text)[0], 115.0)
        text = "Perigee altitude: 800 kilometres (500 mi)"
        its = qt.quantities(text)
        self.assertEqual([(i["raw"], i["dim"]) for i in its], [("800 kilometres", "길이"), ("500 mi", "길이")])
        near(self, its[0]["base"], 8e5)
        text = "Length: 0.75 metres (2.5 ft)"
        its = qt.quantities(text)
        self.assertEqual([(i["raw"], i["dim"]) for i in its], [("0.75 metres", "길이"), ("2.5 ft", "길이")])
        near(self, its[0]["base"], 0.75)

    def test_spellings_and_plurals(self):
        for t in ("3 meter", "3 meters", "3 metre", "3 metres"):
            self.check(t, "길이", 3)
        for t in ("2 kilometers", "2 kilometre"):
            self.check(t, "길이", 2e3)
        self.check("5 micron", "길이", 5e-6)
        self.check("5 angstroms", "길이", 5e-10)
        self.check("2 astronomical units", "길이", 2 * 1.495978707e11)
        self.check("3 megaparsecs", "길이", 3 * 3.0856775814913673e22)
        self.check("4 metric tons", "질량", 4e3)
        self.check("4 milligrams", "질량", 4e-6)
        self.check("7 nanoseconds", "시간", 7e-9)
        self.check("8 square kilometres", "넓이", 8e6)
        self.check("8 square miles", "넓이", 8 * 2589988.110336)
        self.check("3 hectares", "넓이", 3e4)
        self.check("9 cubic centimeters", "부피", 9e-6)
        self.check("9 millilitres", "부피", 9e-6)
        self.check("90 atmospheres", "압력", 90 * 101325)
        self.check("3 millibars", "압력", 300)
        self.check("3 bars", "압력", 3e5)
        self.check("2 kilowatt-hours", "에너지", 7.2e6)
        self.check("2 gigaelectronvolts", "에너지", 2 * 1.602176634e-10)
        self.check("2 electron volts", "에너지", 2 * 1.602176634e-19)
        self.check("3 kilocalories", "에너지", 3 * 4184)
        self.check("2 terawatts", "출력", 2e12)
        self.check("3 megahertz", "진동수", 3e6)
        self.check("3 THz", "진동수", 3e12)

    def test_angle_and_temperature_names(self):
        it = self.one("Inclination: 5 degrees (planned)")
        self.assertEqual((it["dim"], it["value"], it["base"]), ("각도", 5.0, 5.0))
        it = self.one("heated to 1,000 degrees Celsius")
        self.assertEqual((it["dim"], it["unit"]), ("온도", "degrees Celsius"))
        near(self, it["base"], 1273.15)
        near(self, self.one("212 degrees Fahrenheit")["base"], 373.15)
        self.check("300 kelvin", "온도", 300)
        self.check("2 arcseconds", "각도", 2 / 3600)
        self.check("2 arc-minutes", "각도", 2 / 60)
        self.check("5 milliarcseconds", "각도", 5 / 3.6e6)
        self.check("2 radians", "각도", 2 * 57.29577951308232)

    def test_korean_names_of_existing_units(self):
        self.check("5 밀리초", "시간", 5e-3)
        self.check("5 제곱센티미터", "넓이", 5e-4)
        self.check("5 세제곱킬로미터", "부피", 5e9)
        self.check("1,013 헥토파스칼", "압력", 101300)
        self.check("5 킬로줄", "에너지", 5e3)
        self.check("5 킬로와트시", "에너지", 5 * 3.6e6)
        self.check("5 킬로칼로리", "에너지", 5 * 4184)
        self.check("5 기가전자볼트", "에너지", 5 * 1.602176634e-10)
        self.check("5 테라와트", "출력", 5e12)
        self.check("5 라디안", "각도", 5 * 57.29577951308232)
        self.check("5 기가헤르츠", "진동수", 5e9)

    # 2. 새 차원
    def test_new_dimensions(self):
        self.check("20 kV", "전압", 2e4)
        self.check("0.5 mSv", "선량당량", 5e-4)
        self.check("2 mol", "물질량", 2)
        self.check("3 newtons", "힘", 3)
        self.check("3 kN", "힘", 3e3)
        self.check("12 volts", "전압", 12)
        self.check("5 mA", "전류", 5e-3)
        self.check("5 µA", "전류", 5e-6)
        self.check("4.7 kΩ", "전기 저항", 4.7e3)
        self.check("4.7 ohms", "전기 저항", 4.7)
        self.check("2 coulombs", "전하", 2)
        self.check("2 gauss", "자기장", 2e-4)
        self.check("3 nT", "자기장", 3e-9)
        self.check("5 mCi", "방사능", 5 * 3.7e7)
        self.check("2 Ci", "방사능", 2 * 3.7e10)
        self.check("3 TBq", "방사능", 3e12)
        self.check("4 mGy", "흡수선량", 4e-3)
        self.check("4 sieverts", "선량당량", 4)
        self.check("4 µmol", "물질량", 4e-6)
        self.check("4 candelas", "광도", 4)
        self.check("4 lumens", "광선속", 4)
        self.check("4 lux", "조도", 4)
        self.check("4 pF", "전기 용량", 4e-12)
        self.check("4 Wb", "자기 선속", 4)
        self.check("4 henries", "인덕턴스", 4)
        self.check("4 siemens", "전기 전도도", 4)
        self.check("1 Da", "질량", 1.66053906660e-27)
        self.check("5 kDa", "질량", 5 * 1.66053906660e-24)
        self.check("5 달톤", "질량", 5 * 1.66053906660e-27)
        for t, d, b in (("5 뉴턴", "힘", 5), ("5 볼트", "전압", 5), ("5 암페어", "전류", 5), ("5 옴", "전기 저항", 5),
                        ("5 쿨롱", "전하", 5), ("5 테슬라", "자기장", 5), ("5 베크렐", "방사능", 5), ("5 퀴리", "방사능", 5 * 3.7e10),
                        ("5 그레이", "흡수선량", 5), ("5 밀리시버트", "선량당량", 5e-3), ("5 몰", "물질량", 5), ("5 칸델라", "광도", 5),
                        ("5 루멘", "광선속", 5), ("5 럭스", "조도", 5), ("5 패럿", "전기 용량", 5), ("5 웨버", "자기 선속", 5),
                        ("5 헨리", "인덕턴스", 5), ("5 지멘스", "전기 전도도", 5), ("5 가우스", "자기장", 5e-4)):
            self.check(t, d, b)

    def test_new_dimension_boundaries(self):
        self.assertEqual(qs("5 metresX"), [])
        self.assertEqual(unk("5 metresX"), ["5"])
        self.assertEqual(qs("5 몰디브"), [])
        self.assertEqual(unk("5 몰디브"), ["5"])
        self.assertEqual(qs("5 뉴턴의"), [("5 뉴턴", 5.0, "뉴턴")])
        self.assertEqual(qs("5 mTorr"), [])

    # 3. 천문 단위의 이름
    def test_astronomical_names(self):
        it = self.one("Mass: 6.81 Earth masses")
        self.assertEqual((it["dim"], it["value"]), ("질량", 6.81))
        near(self, it["base"], 6.81 * 5.9722e24)
        self.check("2 Jupiter masses", "질량", 2 * 1.89813e27)
        self.check("2 Jovian mass", "질량", 2 * 1.89813e27)
        self.check("2 MJup", "질량", 2 * 1.89813e27)
        self.check("2 M♃", "질량", 2 * 1.89813e27)
        self.check("3 solar masses", "질량", 3 * 1.98847e30)
        self.check("1.5 Jupiter radii", "길이", 1.5 * 7.1492e7)
        self.check("1.5 RJup", "길이", 1.5 * 7.1492e7)
        self.check("0.9 Earth radius", "길이", 0.9 * 6.3781e6)
        self.check("0.9 solar radii", "길이", 0.9 * 6.957e8)
        self.check("2 solar luminosities", "출력", 2 * 3.828e26)
        self.check("5 지구 질량", "질량", 5 * 5.9722e24)
        self.check("5 태양질량", "질량", 5 * 1.98847e30)
        self.check("5 지구 반지름", "길이", 5 * 6.3781e6)
        self.check("5 목성 반지름", "길이", 5 * 7.1492e7)
        self.check("5 태양 반지름", "길이", 5 * 6.957e8)
        self.check("5 태양 광도", "출력", 5 * 3.828e26)
        its = qt.quantities("질량: >7.80±0.35 목성질량(2,480 지구질량)")
        self.assertEqual([(i["raw"], i["unit"], i["dim"]) for i in its],
                         [("7.80±0.35 목성질량", "목성질량", "질량"), ("2,480 지구질량", "지구질량", "질량")])
        near(self, its[0]["base"], 7.80 * 1.89813e27)
        near(self, its[1]["base"], 2480 * 5.9722e24)
        self.assertEqual(qt.UNITS["RJup"], qt.UNITS["RJ"])

    # 4. 음의 지수로 적은 합친 단위
    def test_negative_exponent_units(self):
        it = self.one("530±0.15 kg m⁻³")
        self.assertEqual((it["dim"], it["value"], it["unit"]), ("밀도", 530.0, "kg m⁻³"))
        near(self, it["base"], 530)
        self.check("1.2 g·cm⁻³", "밀도", 1200)
        self.check("1.2 g cm⁻³", "밀도", 1200)
        self.check("20 m s⁻¹", "속도", 20)
        self.check("20 km·s⁻¹", "속도", 2e4)
        self.check("36 km h⁻¹", "속도", 10)
        self.check("9.8 m·s⁻²", "가속도", 9.8)
        self.check("40 kJ mol⁻¹", "몰 에너지", 4e4)
        self.check("10 kcal·mol⁻¹", "몰 에너지", 41840)
        self.check("18 g mol⁻¹", "몰 질량", 0.018)
        self.check("0.018 kg·mol⁻¹", "몰 질량", 0.018)
        self.check("401 W m⁻¹ K⁻¹", "열전도율", 401)
        self.check("401 W·m⁻¹·K⁻¹", "열전도율", 401)
        self.check("25 J mol⁻¹ K⁻¹", "몰 열용량", 25)
        self.check("25 J/mol·K", "몰 열용량", 25)
        self.check("4.18 J g⁻¹ K⁻¹", "비열", 4180)
        self.check("900 J kg⁻¹ K⁻¹", "비열", 900)
        self.check("900 J/kg·K", "비열", 900)
        self.check("4.18 J/g·K", "비열", 4180)

    def test_thermal_expansion(self):
        its = qt.quantities("Thermal expansion: 4.5×10⁻⁶/K (at 20 °C)")
        self.assertEqual([(i["raw"], i["dim"]) for i in its], [("4.5×10⁻⁶/K", "열팽창"), ("20 °C", "온도")])
        near(self, its[0]["base"], 4.5e-6)
        near(self, its[1]["base"], 293.15)
        near(self, self.one("23×10⁻⁶ K⁻¹")["base"], 23e-6)
        near(self, self.one("1.2×10⁻⁵ 1/K")["base"], 1.2e-5)
        near(self, self.one("1.2×10⁻⁵ °C⁻¹")["base"], 1.2e-5)
        near(self, self.one("1.2×10⁻⁵/°C")["base"], 1.2e-5)

    # 5. 뜻이 둘인 기호는 읽지 않는다
    def test_ambiguous_symbols_stay_unknown(self):
        for t, d in (("3 MJ", "3"), ("5 N", "5"), ("12 V", "12"), ("2 tons", "2"), ("2 ton", "2"), ("4 A", "4"), ("4 C", "4"),
                     ("4 F", "4"), ("4 S", "4"), ("4 H", "4"), ("4 T", "4"), ("4 cd", "4"), ("4 lm", "4"), ("4 sr", "4"),
                     ("4 G", "4"), ("4 도", "4"), ("4 줄", "4"), ("4 바", "4")):
            self.assertEqual(qs(t), [], t)
            self.assertEqual(unk(t), [d], t)
        for sym in ("N", "V", "A", "C", "F", "S", "H", "T", "MJ", "cd", "lm", "sr", "G", "ton", "tons", "도", "줄", "바"):
            self.assertNotIn(sym, qt.UNITS)


class Digits(unittest.TestCase):
    """양 항목의 digits(목록): 적힌 값의 숫자 글자."""

    def d(self, text):
        return [i["digits"] for i in qt.quantities(text)]

    def test_plain_and_comma(self):
        self.assertEqual(self.d("질량 12 kg"), [["12"]])
        self.assertEqual(self.d("1,316 km"), [["1316"]])
        self.assertEqual(self.d("1316.0 km"), [["1316.0"]])

    def test_sign_and_tolerance_not_in_digits(self):
        self.assertEqual(self.d("-5 °C"), [["5"]])
        self.assertEqual(self.d("12.5 ± 0.3 kg"), [["12.5"]])

    def test_exponent_uses_leading_number(self):
        self.assertEqual(self.d("8.06×10²⁴ kg"), [["8.06"]])

    def test_big_word(self):
        self.assertEqual(self.d("4561만년"), [["4561"]])
        self.assertEqual(self.d("1억 4960만 km"), [["1", "4960"]])
        self.assertEqual(self.d("5 million km"), [["5"]])

    def test_multi_cell(self):
        self.assertEqual(self.d("3 days 7.5 hours"), [["3", "7.5"]])
        self.assertEqual(self.d("적경 15h 19m 26s"), [["15", "19", "26"]])

    def test_range_each_end(self):
        self.assertEqual(self.d("3–5 km"), [["3"], ["5"]])

    def test_unknown_digits_stay_string(self):
        self.assertEqual(unk("4 of the 15 lanthanides"), ["4", "15"])


class Close(unittest.TestCase):
    def test_close(self):
        self.assertTrue(qt.close(100, 100.9))
        self.assertTrue(qt.close(0, 0))
        self.assertFalse(qt.close(100, 102))
        self.assertFalse(qt.close(0.048, 0.05))


def verdicts(ko, en, ko_docs=None):
    """한국어 글(들)의 양 묶음마다 (raw들, 판정을 단 묶음)을 반대 언어 글 en(들)에 대해."""
    kos = [ko] if isinstance(ko, str) else ko
    ens = [en] if isinstance(en, str) else en
    items = []
    for k, t in enumerate(kos):
        for it in qt.quantities(t):
            items.append({**it, "doc": f"ko{k}"})
    groups = qt.judge(qt.group(items), [(f"en{k}", qt.read(t)) for k, t in enumerate(ens)])
    return [([m["raw"] for m in g["mentions"]], g) for g in groups]


class Group(unittest.TestCase):
    def test_same_dim_close_joined(self):
        its = [{**i, "doc": "a"} for i in qt.quantities("1316 km")] + [{**i, "doc": "b"} for i in qt.quantities("1,316 km")]
        gs = qt.group(its)
        self.assertEqual(len(gs), 1)
        self.assertEqual((gs[0]["dim"], gs[0]["base"]), ("길이", 1316e3))
        self.assertEqual([m["doc"] for m in gs[0]["mentions"]], ["a", "b"])

    def test_other_dim_or_far_not_joined(self):
        its = [{**i, "doc": "a"} for i in qt.quantities("4500 m, 4500 kg, 4600 m")]
        self.assertEqual(len(qt.group(its)), 3)


class Judge(unittest.TestCase):
    def one(self, ko, en):
        v = verdicts(ko, en)
        self.assertEqual(len(v), 1, v)
        return v[0][1]

    def test_date_is_not_evidence(self):
        v = self.one("공전 주기는 4일이다", "Discovery date: 4 April 2007")
        self.assertEqual((v["verdict"], v["found"]), ("그 언어에만", None))

    def test_unknown_number_same_digits_maybe(self):
        v = verdicts("공전 주기는 4일이다", "4 of the 15 lanthanides")[0][1]
        self.assertEqual(v["verdict"], "있을 수 있음")
        self.assertEqual((v["found"]["doc"], v["found"]["digits"]), ("en0", "4"))

    def test_fahrenheit_celsius_present(self):
        v = self.one("824 °C", "melts at 1515 °F")
        self.assertEqual(v["verdict"], "있음")
        self.assertEqual((v["found"]["doc"], v["found"]["raw"]), ("en0", "1515 °F"))

    def test_tonnes_kg(self):
        self.assertEqual(self.one("4.5톤", "4,500 kg")["verdict"], "있음")

    def test_dimension_mismatch(self):
        self.assertEqual(self.one("길이 4500 m", "mass 4,500 kg")["verdict"], "그 언어에만")

    def test_rounding_difference_stays_only(self):
        self.assertEqual(self.one("0.05 AU", "0.048 AU")["verdict"], "그 언어에만")

    def test_formula_digits_maybe(self):
        v = self.one("8.06×10²⁴ kg", r"\(M=8.06\times 10^{24}\)")
        self.assertEqual(v["verdict"], "있을 수 있음")
        self.assertEqual(v["found"]["digits"], "8.06")

    def test_parsec_and_lightyear(self):
        v = verdicts("거리: 6.26 파섹 (20.55 광년)", "20.55 light-years")
        # 6.26 pc(20.42 ly)와 20.55 ly는 0.6% 차이라 한 묶음이고, 그 묶음이 있음이다
        self.assertEqual([(raws, g["verdict"]) for raws, g in v], [(["6.26 파섹", "20.55 광년"], "있음")])

    def test_comma_is_same(self):
        self.assertEqual(self.one("1,316 km", "1316 km")["verdict"], "있음")

    def test_decimal_text_must_match(self):
        self.assertEqual(self.one("1316.0 km", "the number 1316")["verdict"], "그 언어에만")

    def test_unit_vs_unitless_maybe(self):
        self.assertEqual(self.one("1316 km", "the number 1316")["verdict"], "있을 수 있음")

    def test_any_mention_with_evidence_decides(self):
        v = verdicts(["질량 1316 kg", "mass 1,316 kg"], "1316 kg")
        self.assertEqual(len(v), 1)
        self.assertEqual(len(v[0][0]), 2)
        self.assertEqual(v[0][1]["verdict"], "있음")

    def test_second_other_doc_found(self):
        v = self.one("12 kg", ["nothing", "weighs 12 kg"])
        self.assertEqual((v["verdict"], v["found"]["doc"]), ("있음", "en1"))

    def test_first_found_in_doc_order(self):
        v = self.one("12 kg", ["12 kg", "12 kg"])
        self.assertEqual(v["found"]["doc"], "en0")

    def test_ratio_and_name_not_evidence(self):
        self.assertEqual(self.one("12 kg", "12% of Kepler-12")["verdict"], "그 언어에만")


if __name__ == "__main__":
    unittest.main()
