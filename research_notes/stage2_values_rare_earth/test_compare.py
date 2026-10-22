"""compare.py 시험. 골든 사례(C1~C12)는 extract.py가 만든 실제 values.json으로, 비교 함수는 손으로 만든 값으로 확인한다.

실행: .venv/bin/python -m unittest discover -s research_notes/stage2_values_rare_earth -p "test_*.py"
"""
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare as cp  # noqa: E402

RESULT = None
GROUPS = {}


def setUpModule():
    global RESULT
    records = json.loads((HERE / "values.json").read_text(encoding="utf-8"))
    RESULT = cp.run(records)
    for g in RESULT["groups"]:
        GROUPS[(g["object"], g["quantity"], g["condition"])] = g


def rep(num, unit="", **kw):
    r = {"text": f"{num} {unit}".strip(), "num": num, "unc": "", "unit": unit, "range_to": None, "approx": "", "est_mark": False, "value": None}
    r.update(kw)
    return r


def key(num, unit="", raw="", **kw):
    return cp.member(rep(num, unit, **kw), "수", raw)["key"]


def classes(group, doc, where_not="본문"):
    return {p["class"] for p in group["places"] if p["doc_id"] == doc and p["where"] != where_not}


def place(group, doc, first_line=None, where_not="본문"):
    got = [p for p in group["places"] if p["doc_id"] == doc and p["where"] != where_not and (first_line is None or p["lines"][0] == first_line)]
    assert len(got) == 1, (doc, first_line, [p["place"] for p in group["places"]])
    return got[0]


def same_class(group, a, b):
    return place(group, *a)["class"] == place(group, *b)["class"]


class PureCompare(unittest.TestCase):
    def test_c11_units_exact(self):
        self.assertEqual(key("1000", "m"), key("1", "km"))
        self.assertNotEqual(key("2.67", "d"), key("64.053", "h"))          # 64.053/24 = 2.668875
        self.assertEqual(key("2", "d"), key("48", "h"))
        self.assertEqual(key("5.1×10⁻⁶", "/K"), key("5.1", "µm/(m·K)"))      # 둘 다 열팽창 차원
        self.assertEqual(cp.unit_info("/K")[0], cp.unit_info("µm/(m·K)")[0])

    def test_temperature_exact(self):
        self.assertEqual(key("1545", "°C"), key("1818.15", "K"))
        self.assertNotEqual(key("1545", "°C"), key("1818", "K"))
        self.assertEqual(key("2813", "°F"), key("1545", "°C"))             # (2813-32)×5/9 = 1545 정확히
        self.assertNotEqual(key("100", "°F"), key("37.78", "°C"))

    def test_writing_only_differences(self):
        self.assertEqual(key("9.32", "g/cm³"), key("9.320", "g/cm³"))
        self.assertEqual(key("1,654", "K"), key("1654", "K"))
        self.assertEqual(key("58.51", "d", unc="(6)"), key("58.51", "d"))
        self.assertEqual(key("168.934219", unc="±0.000005"), key("168.934219", unc="(5)"))
        self.assertEqual(key("100", "ns", est_mark=True), key("100", "ns"))              # 끝의 #는 무시
        self.assertEqual(key("+25500×10⁻⁶"), key("0.0255"))
        self.assertEqual(cp.parse_num("3.0E+6"), Fraction(3000000))
        self.assertEqual(cp.parse_num("−0.09"), Fraction(-9, 100))
        self.assertEqual(cp.parse_num("2×10¹⁵"), Fraction(2 * 10 ** 15))

    def test_different_writings(self):
        self.assertNotEqual(key("58.5", "d"), key("58.51", "d"))
        self.assertNotEqual(key("13.9", "W/(m·K)", approx="est."), key("13.9", "W/(m·K)"))
        self.assertNotEqual(key("22", "kJ/mol", approx="약"), key("22", "kJ/mol"))
        self.assertEqual(key("22", "kJ/mol", approx="약"), key("22", "kJ/mol", approx="about"))     # 어림 말끼리는 같은 어림
        self.assertNotEqual(key("470", "MPa", range_to="650"), key("520", "MPa"))
        self.assertNotEqual(key("470", "MPa", range_to="650"), key("470", "MPa", range_to="900"))
        self.assertEqual(key("470", "MPa", range_to="650"), key("0.47", "GPa", range_to="0.65"))
        self.assertNotEqual(key("5", "s", approx="<"), key("5", "s", approx=">"))
        self.assertEqual(key("5", "s", approx="less than"), key("5", "s", approx="<"))

    def test_units_aliases(self):
        self.assertEqual(key("180", "a"), key("180", "y"))                               # a는 해
        self.assertEqual(key("75.95845", "u"), key("75.95845", "Da"))
        self.assertEqual(key("1", "keV"), key("1000", "eV"))
        self.assertNotEqual(key("5", "cm³/mol"), key("5", "m"))                          # 바꿀 수 없는 단위
        self.assertEqual(cp.header_unit("DE (MeV)"), "MeV")
        self.assertEqual(cp.header_unit("동위 원소 질량 (u)"), "Da")
        self.assertEqual(cp.header_unit("Median survival time (months)"), "months")
        self.assertEqual(cp.header_unit("Z(p)"), "")
        self.assertEqual(cp.header_unit("자연계에 존재하는 동위 원소 범위 (몰 분율)"), "")

    def test_year_suffix_is_a_date(self):
        self.assertEqual(key("1879", "년"), key("1879"))
        self.assertNotEqual(key("100", "년"), key("100"))                                # 연도가 아닌 기간은 단위다

    def test_magnitude_words(self):
        k1 = cp.member(rep("38", approx="about"), "수", "about 38 billion years")["key"]
        k2 = cp.member(rep("380", approx="약"), "수", "약 380억년")["key"]
        self.assertEqual(k1, k2)
        self.assertEqual(k1[2], Fraction(38 * 10 ** 9) * 31557600)                       # 단위(years)도 낱말 뒤에서 얻는다
        k3 = cp.member(rep("2", approx="약"), "수", "약 2백만 톤")["key"]
        self.assertEqual(k3[1], "질량")
        self.assertEqual(k3[2], Fraction(2 * 10 ** 6) * 1000)
        self.assertNotEqual(k3, cp.member(rep("2", approx="약"), "수", "약 2 톤")["key"])
        self.assertEqual(cp.member(rep("5"), "수", "5만큼")["key"][2], Fraction(5))        # '만큼'은 큰 수 낱말이 아니다

    def test_words(self):
        w = lambda t: cp.member({"text": t}, "낱말")["key"]
        self.assertEqual(w("β-"), w("β⁻"))
        self.assertEqual(w("β−"), w("β⁻"))
        self.assertEqual(w("안정"), w("stable"))
        self.assertEqual(w("Stable"), w("stable"))
        self.assertEqual(w("합성"), w("synth"))
        self.assertEqual(w("인공"), w("synth"))
        self.assertEqual(w("1/2-"), w("1/2−"))
        self.assertEqual(w("a­b​c  d"), w("abc d"))
        self.assertNotEqual(w("ε"), w("β⁺"))
        self.assertNotEqual(w("100"), key("100"))

    def test_places_as_sets(self):
        def mk(doc, lang, vals, kind="수", **kw):
            members = [cp.member(v if isinstance(v, dict) else rep(v, "d"), kind) for v in vals]
            keys = frozenset(m["key"] for m in members)
            p = {"doc_id": doc, "lang": lang, "where": "표", "members": members, "keys": keys, "notes": [], "uncertain": False,
                 "partial": False, "word_digits": False}
            p.update(kw)
            return p
        a, b, c = mk("d1", "ko", ["3.35"]), mk("d2", "ko", ["3.35", "3.35"]), mk("d3", "en", ["3.35", "4"])
        j = cp.judge_group([a, b, c])
        self.assertEqual(j["verdict"], "다름")
        self.assertEqual(j["classes"][0], j["classes"][1])
        self.assertNotEqual(j["classes"][0], j["classes"][2])
        self.assertEqual(set(j["scopes"]), {cp.SCOPE_OTHER_LANG})
        self.assertIn("여러 값", j["reasons"])
        self.assertEqual(cp.judge_group([a, b])["verdict"], "같음")

    def test_cannot_convert_reason(self):
        def mk(doc, unit):
            m = cp.member(rep("5", unit), "수")
            return {"doc_id": doc, "lang": "en", "where": "표", "members": [m], "keys": frozenset([m["key"]]), "notes": [],
                    "uncertain": False, "partial": False, "word_digits": False}
        j = cp.judge_group([mk("a", "m"), mk("b", "kg")])
        self.assertEqual(j["verdict"], "다름")
        self.assertIn("단위를 못 바꿈", j["reasons"])

    def test_condition_variants(self):
        def mk(doc, cond):
            return {"doc_id": doc, "object": "X", "quantity": "q", "condition": cond}
        self.assertEqual(len(cp.condition_variants([mk("a", ""), mk("b", "poly")])), 1)
        self.assertEqual(len(cp.condition_variants([mk("a", "empirical"), mk("a", "calculated"), mk("b", "empirical")])), 0)
        self.assertEqual(len(cp.condition_variants([mk("a", ""), mk("b", "")])), 0)


class Golden(unittest.TestCase):
    def test_c1(self):
        g = GROUPS[("Tm", "heat_of_vaporization", "")]
        self.assertEqual((g["verdict"], g["scopes"]), ("다름", ["반대 언어"]))

    def test_c2(self):
        g = GROUPS[("Tm", "atomic_radius", "empirical")]
        self.assertEqual((g["verdict"], g["scopes"]), ("다름", ["반대 언어"]))
        self.assertNotIn(("Tm", "atomic_radius", "calculated"), GROUPS)              # 곳이 하나뿐인 묶음은 쓰지 않는다

    def test_c3(self):
        g = GROUPS[("Tm", "density", "")]              # 이 묶음에는 본문 곳도 있어 묶음 판정은 다를 수 있다. 정보 상자 둘은 같아야 한다.
        self.assertTrue(same_class(g, ("wiki-ko-thulium",), ("wiki-en-thulium",)))

    def test_c4(self):
        g = GROUPS[("Tm", "melting_point", "")]
        self.assertEqual(g["verdict"], "같음")

    def test_c5(self):
        g = GROUPS[("Tm", "vickers_hardness", "")]
        self.assertEqual(g["verdict"], "다름")

    def test_c6(self):
        for p in (1, 10, 100, 1000, 10000, 100000):
            g = GROUPS[("Tm", "vapor_pressure_temperature", f"P={p}")]
            self.assertEqual(g["verdict"], "같음", p)

    def test_c7(self):
        g = GROUPS[("Tm-168", "decay_mode", "")]
        self.assertEqual(g["verdict"], "다름")
        self.assertEqual(sorted(v for p in g["places"] for v in p["values"]), ["β⁺", "ε"])

    def test_c8(self):
        g = GROUPS[("Y-91", "half_life", "")]
        self.assertEqual(g["verdict"], "다름")
        ko_y = place(g, "wiki-ko-yttrium")
        ko_i = place(g, "wiki-ko-isotopes-of-yttrium", 50)
        en_main = place(g, "wiki-en-isotopes-of-yttrium", 10)
        en_list = place(g, "wiki-en-isotopes-of-yttrium", 70)
        self.assertEqual(ko_y["values"], ["58.5 d"])
        self.assertEqual({p["class"] for p in (ko_y, ko_i, en_main, en_list)}.__len__(), 2)
        self.assertEqual({ko_i["class"], en_main["class"], en_list["class"]}.__len__(), 1)
        self.assertNotEqual(ko_y["class"], ko_i["class"])
        self.assertIn(cp.SCOPE_SAME_LANG, g["scopes"])
        self.assertIn(cp.SCOPE_OTHER_LANG, g["scopes"])
        self.assertNotEqual(en_main["place"], en_list["place"])              # 같은 문서의 다른 표는 다른 곳

    def test_c9(self):
        g = GROUPS[("Y-90", "half_life", "")]
        ko_y = place(g, "wiki-ko-yttrium")
        ko_i = place(g, "wiki-ko-isotopes-of-yttrium", 47)
        self.assertEqual((ko_y["values"], ko_i["values"]), (["2.67 d"], ["64.053 h"]))
        self.assertNotEqual(ko_y["class"], ko_i["class"])

    def test_c10(self):
        for cond in ("", "abridged"):
            g = GROUPS[("Tm", "standard_atomic_weight", cond)]
            self.assertEqual(g["verdict"], "같음", cond)

    def test_c12(self):
        g = GROUPS[("Y-87", "decay_mode", "")]
        p = place(g, "wiki-ko-yttrium")
        self.assertEqual(p["values"], ["ε", "γ"])
        self.assertEqual(p["lines"], [57, 58])
        self.assertIn("여러 값", g["reasons"])

    def test_alias_and_override(self):
        g = GROUPS[("Yb", "number_of_nuclear_isomers", "")]
        ko = [p for p in g["places"] if p["place"].startswith("wiki-ko-ytterbium:117:")]
        en = [p for p in g["places"] if p["place"].startswith("wiki-en-ytterbium:119:")]
        self.assertTrue(any("12개의 준안정 상태" in r for p in ko for r in p["raws"]))
        self.assertTrue(any("18 meta states" in r for p in en for r in p["raws"]))
        self.assertEqual(g["verdict"], "다름")
        given = [p["given"] for p in g["places"] if p.get("given")]
        self.assertIn("number_of_meta_states", {x["quantity"] for x in given})
        # 덮어쓰기: 자리 id로 조건·양을 바꾸고 원래 열쇠를 남긴다
        rows = [{"id": "d:1:0", "object": "A", "quantity": "q1", "condition": ""}, {"id": "d:1:1", "object": "A", "quantity": "q2", "condition": ""}]
        out = cp.apply_keys(rows, {"place_override": {"d:1:0": {"condition": "c"}}, "quantity_alias": {"A|q2": "B|q3"}})
        self.assertEqual((out[0]["condition"], out[0]["given"]["condition"]), ("c", ""))
        self.assertEqual((out[1]["object"], out[1]["quantity"], out[1]["given"]["quantity"]), ("B", "q3", "q2"))
        self.assertEqual(rows[0]["condition"], "")                                  # 원본은 그대로
        with self.assertRaises(ValueError):
            cp.apply_keys(rows, {"place_override": {"d:9:9": {"condition": "c"}}})
        with self.assertRaises(ValueError):
            cp.apply_keys(rows, {"quantity_alias": {"A|nope": "B|q"}})

    def test_body_rules(self):
        for g in RESULT["groups"]:
            has_body = any(p["where"] == "본문" for p in g["places"])
            if g["verdict"] == "다름" and has_body:
                self.assertTrue(g["review"] and "본문 값" in g["reasons"], g["object"])
            if g["verdict"] == "같음":
                self.assertFalse(g["review"])
            if any(p["where"] == "본문" and p["uncertain_reason"] for p in g["places"]) and g["verdict"] == "다름":
                self.assertIn("불확실 표시", g["reasons"])

    def test_counts_consistent(self):
        c = RESULT["counts"]
        self.assertEqual(c["same"] + c["different"], c["groups_2plus"])
        self.assertEqual(c["groups_2plus"] + c["singletons"], c["groups"])
        self.assertEqual(c["review"] + c["different_no_review"], c["different"])
        for g in RESULT["groups"]:
            self.assertGreaterEqual(len(g["places"]), 2)
            self.assertEqual(g["verdict"] == "같음", len({p["class"] for p in g["places"]}) == 1)


if __name__ == "__main__":
    unittest.main()
