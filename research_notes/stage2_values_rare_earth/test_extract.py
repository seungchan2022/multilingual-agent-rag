"""extract.py 시험. 실제 마크다운 파일을 읽어 골든 사례(E1~E15)를 확인한다.

실행: .venv/bin/python -m unittest discover -s research_notes/stage2_values_rare_earth -p "test_*.py"
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import extract as ex  # noqa: E402

RESULT = None
BY_LINE = {}


def setUpModule():
    global RESULT
    RESULT = ex.build()
    for r in RESULT["builder"].records:
        BY_LINE.setdefault((r["doc_id"], r["line"]), []).append(r)


def at(doc, line):
    return sorted(BY_LINE.get((doc, line), []), key=lambda r: r["start"])


def one(doc, line):
    got = at(doc, line)
    assert len(got) == 1, (doc, line, len(got))
    return got[0]


def pick(doc, line, quantity):
    return [r for r in at(doc, line) if r["quantity"] == quantity]


class IsotopeKey(unittest.TestCase):
    def test_keys(self):
        self.assertEqual(ex.isotope_key("¹⁶⁷Tm"), "Tm-167")
        self.assertEqual(ex.isotope_key("⁸⁷ᵐY"), "Y-87m")
        self.assertEqual(ex.isotope_key("⁸⁵ᵐ¹Y"), "Y-85m1")
        self.assertEqual(ex.isotope_key("¹⁶⁸Tm"), "Tm-168")
        self.assertEqual(ex.isotope_key("¹³³ᵐ²Nd"), "Nd-133m2")
        self.assertIsNone(ex.isotope_key("Tm"))


class Infobox(unittest.TestCase):
    def test_e1_heat_of_vaporization(self):
        for doc, num in (("wiki-ko-thulium", "247"), ("wiki-en-thulium", "191")):
            r = one(doc, 22)
            self.assertEqual((r["object"], r["quantity"], r["condition"]), ("Tm", "heat_of_vaporization", ""))
            self.assertEqual((r["reps"][0]["num"], r["reps"][0]["unit"]), (num, "kJ/mol"))

    def test_e2_atomic_radius(self):
        a, b = at("wiki-ko-thulium", 34)
        self.assertEqual((a["quantity"], a["condition"], a["reps"][0]["num"], a["reps"][0]["unit"]), ("atomic_radius", "empirical", "175", "pm"))
        self.assertEqual((b["quantity"], b["condition"], b["reps"][0]["num"], b["reps"][0]["unit"]), ("atomic_radius", "calculated", "222", "pm"))
        r = one("wiki-en-thulium", 35)
        self.assertEqual((r["quantity"], r["condition"], r["reps"][0]["num"]), ("atomic_radius", "empirical", "176"))
        self.assertIn("empirical", r["quote"])

    def test_e3_density(self):
        r = one("wiki-ko-thulium", 19)
        self.assertEqual((r["quantity"], r["condition"], r["reps"][0]["num"], r["reps"][0]["unit"]), ("density", "", "9.32", "g/cm³"))
        r = one("wiki-en-thulium", 19)
        self.assertEqual((r["quantity"], r["condition"], r["reps"][0]["num"], r["reps"][0]["unit"]), ("density", "", "9.320", "g/cm³"))

    def test_e4_melting_point(self):
        r = one("wiki-ko-thulium", 17)
        self.assertEqual((r["quantity"], r["condition"], len(r["reps"])), ("melting_point", "", 1))
        self.assertEqual((r["reps"][0]["num"], r["reps"][0]["unit"]), ("1818", "K"))
        r = one("wiki-en-thulium", 17)       # 줄에 U+200B가 끼어 있다
        self.assertEqual([(x["num"], x["unit"]) for x in r["reps"]], [("1818", "K"), ("1545", "°C"), ("2813", "°F")])
        self.assertEqual(r["quote"][r["start"]:r["end"]], r["raw"])
        self.assertTrue(r["raw"].startswith("1818 K") and r["raw"].endswith("°F)"))

    def test_e5_vickers(self):
        r = one("wiki-ko-thulium", 45)
        self.assertEqual((r["quantity"], r["condition"], r["reps"][0]["num"], r["reps"][0]["unit"]), ("vickers_hardness", "", "520", "MPa"))
        r = one("wiki-en-thulium", 50)
        rep = r["reps"][0]
        self.assertEqual((r["quantity"], rep["num"], rep["range_to"], rep["unit"]), ("vickers_hardness", "470", "650", "MPa"))

    def test_e11_ionization(self):
        for doc, line in (("wiki-ko-thulium", 33), ("wiki-en-thulium", 34)):
            got = at(doc, line)
            self.assertEqual([r["condition"] for r in got], ["1st", "2nd", "3rd"])
            self.assertEqual([r["reps"][0]["num"] for r in got], ["596.7", "1160", "2285"])
            self.assertTrue(all(r["quantity"] == "ionization_energy" for r in got))

    def test_e12_standard_atomic_weight(self):
        a, b = at("wiki-ko-thulium", 5)
        self.assertEqual((a["quantity"], a["condition"], a["reps"][0]["num"], a["reps"][0]["unc"]), ("standard_atomic_weight", "", "168.934219", "(5)"))
        self.assertEqual((b["quantity"], b["condition"], b["reps"][0]["num"], b["reps"][0]["unc"]), ("standard_atomic_weight", "abridged", "168.93", "± 0.01"))
        self.assertEqual(a["note"], [])
        a, b = at("wiki-en-thulium", 7)
        self.assertEqual((a["quantity"], a["condition"], a["reps"][0]["num"], a["reps"][0]["unc"]), ("standard_atomic_weight", "", "168.934219", "±0.000005"))
        self.assertEqual((b["quantity"], b["condition"], b["reps"][0]["num"], b["reps"][0]["unc"]), ("standard_atomic_weight", "abridged", "168.93", "±0.01"))

    def test_e13_notes(self):
        r = one("wiki-en-thulium", 41)
        self.assertEqual((r["quantity"], r["condition"]), ("thermal_expansion", ""))
        self.assertIn("poly", r["note"])
        self.assertIn("(at r.t.)", r["note"])
        r = one("wiki-ko-thulium", 38)
        self.assertEqual((r["quantity"], r["condition"]), ("thermal_expansion", ""))
        self.assertEqual(r["note"], ["(실온)", "(poly)"])

    def test_e14_whole_word(self):
        r = one("wiki-en-thulium", 55)
        self.assertEqual((r["quantity"], r["kind"], r["raw"]), ("discovery", "낱말", "Per Teodor Cleve (1879)"))

    def test_lattice_and_exponent(self):
        a, b = at("wiki-ko-thulium", 37)
        self.assertEqual((a["condition"], b["condition"]), ("a", "c"))
        self.assertEqual(a["note"], [])
        self.assertEqual(b["note"], ["(20 °C에서)"])
        r = one("wiki-en-thulium", 45)       # 단위를 모르는 수: 단위 글자는 수 뒤의 글에서 얻는다
        self.assertEqual((r["reps"][0]["num"], r["reps"][0]["unit"]), ("+25500×10⁻⁶", "cm³/mol"))
        self.assertEqual(r["note"], ["(291 K)"])


class Tables(unittest.TestCase):
    def test_e6_vapor_pressure(self):
        for doc, line in (("wiki-ko-thulium", 28), ("wiki-en-thulium", 29)):
            got = at(doc, line)
            self.assertEqual([r["condition"] for r in got], ["P=1", "P=10", "P=100", "P=1000", "P=10000", "P=100000"])
            self.assertEqual([r["reps"][0]["num"] for r in got], ["1117", "1235", "1381", "1570", "1821", "2217"])
            self.assertTrue(all(r["reps"][0]["unit"] == "K" and r["quantity"] == "vapor_pressure_temperature" and r["object"] == "Tm" for r in got))
            self.assertEqual([r["note"] for r in got], [[], [], [], [], ["괄호 값"], ["괄호 값"]])
            self.assertEqual(len(BY_LINE.get((doc, line - 2), [])) + len(BY_LINE.get((doc, line - 1), [])), 0)
        # 길이가 같은 두 언어 파일에서 6칸씩
        self.assertEqual(sum(len(at("wiki-en-lanthanum", n)) for n in (27, 28, 29, 30)), 6)
        self.assertTrue(all(r["note"][0] == "extrapolated" for r in at("wiki-en-lanthanum", 29)))

    def test_e7_main_isotopes(self):
        (r,) = pick("wiki-ko-thulium", 57, "decay_mode")
        self.assertEqual((r["object"], r["kind"], r["raw"]), ("Tm-168", "낱말", "ε"))
        (r,) = pick("wiki-en-thulium", 63, "decay_mode")
        self.assertEqual((r["object"], r["raw"]), ("Tm-168", "β⁺"))
        for n in (59, 60, 61):
            self.assertEqual(at("wiki-en-thulium", n), [])
        got = {r["quantity"]: r for r in at("wiki-en-thulium", 62)}
        self.assertEqual(got["abundance"]["raw"], "synth")
        self.assertEqual((got["half_life"]["reps"][0]["num"], got["half_life"]["reps"][0]["unit"]), ("9.25", "d"))
        self.assertEqual(got["decay_mode"]["raw"], "ε")
        self.assertEqual(got["daughter"]["raw"], "¹⁶⁷Er")
        self.assertEqual(set(got), {"abundance", "half_life", "decay_mode", "daughter"})

    def test_e8_isomer_row(self):
        doc = "wiki-ko-isotopes-of-yttrium"
        got = at(doc, 40)
        by = {r["quantity"]: r for r in got}
        self.assertEqual([r["quantity"] for r in got].count("excitation_energy"), 1)
        for q in ("proton_number", "neutron_number", "isotopic_mass"):
            self.assertNotIn(q, by)
        e = by["excitation_energy"]
        self.assertEqual(e["object"], "Y-87m")
        rep = e["reps"][0]
        self.assertEqual((rep["num"], rep["unc"], rep["unit"]), ("380.82", "(7)", "keV"))
        self.assertEqual((by["half_life"]["reps"][0]["num"], by["half_life"]["reps"][0]["unit"]), ("13.37", "h"))
        self.assertEqual(by["decay_mode"]["raw"], "IT (98.43%)")
        self.assertEqual(by["daughter"]["raw"], "⁸⁷Y")
        self.assertEqual(by["spin_parity"]["raw"], "9/2+")
        # 같은 글이 세 번 나오는 줄: 자리는 첫 칸이고 나머지 둘은 서로 다른 되풀이 범위다
        ln = RESULT["docs"][[d.id for d in RESULT["docs"]].index(doc)].line(39)
        repeats = sorted((s, e2) for s, e2, why in ln.nonvalue if why == ex.R_REPEAT)
        self.assertEqual(len(repeats), 2)
        self.assertEqual(len(set(repeats)), 2)
        self.assertLess(e["end"], repeats[0][0])
        self.assertLess(repeats[0][1], repeats[1][0])

    def test_e9_half_life_y91(self):
        cases = (("wiki-ko-yttrium", 64, "58.5d"), ("wiki-ko-isotopes-of-yttrium", 50, "58.51(6) d"),
                 ("wiki-en-isotopes-of-yttrium", 10, "58.51 d"), ("wiki-en-isotopes-of-yttrium", 70, "58.51(6) d"))
        for doc, line, raw in cases:
            got = pick(doc, line, "half_life")
            self.assertEqual(len(got), 1, (doc, line))
            self.assertEqual((got[0]["object"], got[0]["raw"]), ("Y-91", raw), (doc, line))

    def test_e10_two_rows(self):
        doc = "wiki-ko-yttrium"
        a, b = at(doc, 57), at(doc, 58)
        self.assertEqual([r["raw"] for r in a if r["quantity"] == "decay_mode"], ["ε"])
        self.assertEqual([r["raw"] for r in b if r["quantity"] == "decay_mode"], ["γ"])
        self.assertEqual([r["raw"] for r in a + b if r["quantity"] == "half_life"], ["3.35d", "3.35d"])
        self.assertTrue(all(r["object"] == "Y-87" for r in a + b))
        e = pick(doc, 58, "decay_energy")
        self.assertEqual(len(e), 1)
        self.assertTrue(e[0]["multi"])
        self.assertEqual([x["num"] for x in e[0]["reps"]], ["0.48", "0.38"])
        self.assertEqual(pick(doc, 57, "decay_energy"), [])          # '-' 칸은 자리를 만들지 않는다

    def test_other_tables(self):
        doc = "wiki-en-samarium-cobalt-magnet"
        got = at(doc, 24)
        self.assertEqual([(r["object"], r["quantity"]) for r in got],
                         [("sintered neodymium magnet", "remanence"), ("sintered samarium-cobalt magnet", "remanence")])
        self.assertEqual([(r["reps"][0]["num"], r["reps"][0]["range_to"], r["reps"][0]["unit"]) for r in got],
                         [("1", "1.5", "T"), ("0.8", "1.16", "T")])
        got = at(doc, 26)
        self.assertEqual(got[0]["reps"][0]["unit"], "")              # '(–)'는 단위 없음
        nct = "wiki-en-neutron-capture-therapy"
        boric = [r for r in BY_LINE_ALL(nct) if r["quantity"] == "listed_boron_agent"]
        self.assertEqual(len(boric), 23)
        self.assertEqual(boric[0]["object"], "Boric acid")
        self.assertTrue(all(r["kind"] == "낱말" for r in boric))
        reactor = [r for r in at(nct, 143)]
        self.assertEqual(reactor[0]["object"], "BMRR, US")
        self.assertEqual([r["quantity"] for r in reactor], ["patients_and_trial_years", "delivery_agent_dose", "median_survival_months"])
        host = at(nct, 189)
        self.assertEqual(host[0]["object"], "Particle Radiation Oncology Research Center, Kyoto University, Kumatori, Japan")


def BY_LINE_ALL(doc):
    return [r for r in RESULT["builder"].records if r["doc_id"] == doc]


class Integrity(unittest.TestCase):
    def test_quote_and_spans(self):
        for r in RESULT["builder"].records:
            self.assertEqual(r["quote"][r["start"]:r["end"]], r["raw"], r["id"])
        ids = [r["id"] for r in RESULT["builder"].records]
        self.assertEqual(len(ids), len(set(ids)))

    def test_e15_coverage(self):
        cov = ex.coverage(RESULT)
        self.assertEqual(cov["uncovered"], [])
        self.assertEqual(cov["overlap"], [])
        self.assertEqual(cov["cells"], [])
        self.assertGreater(cov["checked"], 0)
        b = RESULT["builder"]
        self.assertEqual(b.missing, [])
        self.assertEqual(b.problems, [])
        self.assertEqual(sum(RESULT["table_kinds"].values()), 37)
        self.assertEqual(dict(RESULT["table_kinds"]), {"증기 압력": 14, "주요 동위원소": 15, "동위 원소 목록": 4, "그 밖의 표": 4})


if __name__ == "__main__":
    unittest.main()
