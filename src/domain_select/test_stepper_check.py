"""stepper_check.py 시험. 네트워크를 쓰지 않는다."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stepper_check as sc

SURVEY = sc.ROOT / "research_notes" / "stage2_domain_survey"


class Regression(unittest.TestCase):
    def test_same_as_survey_results(self):
        rows = json.loads((SURVEY / "results.json").read_text(encoding="utf-8"))
        picked = []
        for r in rows:
            for lang in ("ko", "en"):
                d = r.get(lang)
                if d and (SURVEY / "cache" / f"{lang}_{d['revid']}.html").exists() and len(picked) < 3 \
                        and d["title"] not in [p[1]["title"] for p in picked] and len(picked) == len({p[1]["title"] for p in picked}):
                    picked.append((lang, d))
                    break
            if len(picked) == 3:
                break
        self.assertEqual(len(picked), 3)
        for lang, d in picked:
            m = sc.measure((SURVEY / "cache" / f"{lang}_{d['revid']}.html").read_text(encoding="utf-8"))
            self.assertEqual(m["chars"], d["chars"], d["title"])
            self.assertEqual(len(m["tables"]), len(d["tables"]), d["title"])


def row(dom, lang, chars, tables):
    return {"domain": dom, "lang": lang, "chars": chars, "table_count": tables}


def build(ko_chars, en_chars, ko_tab, en_tab, dom="moons"):
    rows = [row(dom, "ko", c, 1 if i < ko_tab else 0) for i, c in enumerate(ko_chars)]
    rows += [row(dom, "en", c, 1 if i < en_tab else 0) for i, c in enumerate(en_chars)]
    return sc.summarize(rows)[0]


class Summary(unittest.TestCase):
    def test_median_floor(self):
        s = build([1, 2, 3, 4], [10, 20], 0, 0)
        self.assertEqual(s["ko_median"], 2)  # 2.5 -> 2
        self.assertEqual(s["en_median"], 15)

    def test_line1_boundary(self):
        self.assertTrue(build([5000] * 3, [5000] * 3, 0, 0)["line1"])
        self.assertFalse(build([4999] * 3, [5000] * 3, 0, 0)["line1"])
        self.assertFalse(build([5000] * 3, [4999] * 3, 0, 0)["line1"])

    def test_line2_line3_boundary(self):
        s = build([1] * 10, [1] * 10, 4, 3)
        self.assertTrue(s["line3"])
        self.assertFalse(s["line2"])
        s = build([1] * 10, [1] * 10, 3, 4)
        self.assertTrue(s["line2"])
        self.assertFalse(s["line3"])

    def test_passed_count(self):
        self.assertEqual(build([5000] * 10, [5000] * 10, 4, 4)["passed"], 3)
        self.assertEqual(build([5000] * 10, [5000] * 10, 3, 3)["passed"], 1)
        self.assertEqual(build([1] * 10, [1] * 10, 1, 1)["passed"], 0)

    def test_out_flag(self):
        self.assertTrue(build([5000] * 10, [5000] * 10, 0, 9)["out"])
        self.assertTrue(build([5000] * 10, [5000] * 10, 9, 0)["out"])
        self.assertFalse(build([5000] * 10, [5000] * 10, 1, 1)["out"])

    def test_render_has_table(self):
        text = sc.render([build([5000] * 10, [5000] * 10, 4, 4)])
        self.assertIn("| moons |", text)


class Targets(unittest.TestCase):
    def test_thirty_no_blank(self):
        rows = sc.load_targets()
        self.assertEqual(len(rows), 30)
        for r in rows:
            for k in ("domain", "target", "ko_title", "ko_revid", "en_title"):
                self.assertTrue(r[k], (r, k))
        self.assertEqual(len({(r["domain"], r["target"]) for r in rows}), 30)


if __name__ == "__main__":
    unittest.main()
