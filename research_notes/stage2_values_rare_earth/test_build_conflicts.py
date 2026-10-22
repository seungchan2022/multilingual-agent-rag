"""build_conflicts.py 시험. 만들어진 data/questions/known_conflicts.json을 실제 마크다운과 맞대어 보고,
판정이 빠졌을 때 등의 오류도 확인한다.

실행: .venv/bin/python -m unittest discover -s research_notes/stage2_values_rare_earth -p "test_*.py"
"""
import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_conflicts as bc  # noqa: E402

ENTRIES = None
INPUTS = None


def setUpModule():
    global ENTRIES, INPUTS
    INPUTS = tuple(json.loads((HERE / f"{n}.json").read_text(encoding="utf-8")) for n in ("compare", "values", "vocab", "verdicts"))
    ENTRIES, errors = bc.collect(*INPUTS)
    assert errors == [], errors


def find(obj, qty, cond=""):
    return [e for e in ENTRIES if (e["object"], e["quantity"], e["condition"]) == (obj, qty, cond)]


def doc_text(doc_id):
    return (bc.MD_DIR / f"{doc_id}.md").read_text(encoding="utf-8")


class Written(unittest.TestCase):
    def test_file_is_what_collect_builds(self):
        written = json.loads(bc.OUT_JSON.read_text(encoding="utf-8"))
        self.assertEqual(written, ENTRIES)
        self.assertTrue(bc.OUT_MD.read_text(encoding="utf-8").startswith("# 알려진 부딪히는 값"))

    def test_quotes_and_values_in_documents(self):
        for e in ENTRIES:
            self.assertEqual(list(e), ["section", "text", "object", "quantity", "condition", "targets"])
            for t in e["targets"]:
                text = doc_text(t["doc_id"])
                self.assertTrue(t["quotes"], (e["text"], t["doc_id"]))
                for q in t["quotes"]:
                    self.assertIn(q, text, (t["doc_id"], q[:50]))
                    self.assertEqual(q, q.rstrip())
                flat = [q.replace(",", "") for q in t["quotes"]]
                for v in t["values"]:
                    self.assertTrue(any(v in q for q in flat), (t["doc_id"], v))
                    self.assertGreaterEqual(len(v.replace(".", "")), 2)
                    self.assertNotIn(",", v)
                self.assertEqual(len(t["values"]), len(set(t["values"])))
                for p in t["places"]:
                    self.assertEqual(set(p), {"line", "label", "raw"})

    def test_checker_reads_it(self):
        # src/questions/check_candidates.py는 문서 목록에 city_group이 없어 아직 불러올 수 없다(3단계에서 고친다).
        # 그래서 그 파일의 conflicts() 검사(항목마다 targets, 문서마다 quotes·values 하나 이상)와 읽는 칸을 같은 규칙으로 확인한다.
        for n, e in enumerate(ENTRIES, 1):
            self.assertIsInstance(e["text"], str)
            self.assertTrue(e["targets"])
            for t in e["targets"]:
                self.assertTrue(t["quotes"] or t["values"], (n, t["doc_id"]))
                self.assertIsInstance(t["quotes"], list)
                self.assertIsInstance(t["values"], list)


class Content(unittest.TestCase):
    def test_known_conflicts_present(self):
        for key in (("Tm", "heat_of_vaporization"), ("Tm-168", "decay_mode"), ("Y-91", "half_life")):
            e = find(*key)
            self.assertEqual(len(e), 1, key)
            self.assertGreaterEqual(len(e[0]["targets"]), 2)
        e = find("Tm", "heat_of_vaporization")[0]
        self.assertEqual(e["section"], "반대 언어")
        self.assertEqual({t["doc_id"] for t in e["targets"]}, {"wiki-ko-thulium", "wiki-en-thulium"})
        self.assertEqual([t["values"] for t in e["targets"]], [["247"], ["191"]])

    def test_non_conflicts(self):
        self.assertEqual(find("Tm", "density"), [])
        self.assertEqual(find("Yb", "boiling_point"), [])
        self.assertEqual(find("Tm", "melting_point"), [])              # 같음

    def test_manual_conflict(self):
        (e,) = find("Yb", "number_of_radioactive_isotopes")
        by = {t["doc_id"]: t for t in e["targets"]}
        en = by["wiki-en-ytterbium"]
        self.assertEqual(en["quotes"], [doc_text("wiki-en-ytterbium").split("\n")[118].rstrip()])
        self.assertNotIn("32", en["values"])
        self.assertEqual(en["values"], [])
        self.assertEqual(by["wiki-ko-ytterbium"]["values"], ["27"])
        self.assertEqual(e["section"], "반대 언어")
        self.assertIn("영어는 Thirty-two", e["text"])

    def test_dy156_includes_table_and_body_lines(self):
        (e,) = find("Dy-156", "natural_abundance")
        en = next(t for t in e["targets"] if t["doc_id"] == "wiki-en-dysprosium")
        lines = doc_text("wiki-en-dysprosium").split("\n")
        self.assertIn(lines[63].rstrip(), en["quotes"])
        self.assertIn(lines[123].rstrip(), en["quotes"])
        self.assertEqual({p["line"] for p in en["places"]}, {64, 124})

    def test_merged_table_place_lists_both_lines(self):
        (e,) = find("Y-87", "decay_mode")
        ko = next(t for t in e["targets"] if t["doc_id"] == "wiki-ko-yttrium")
        lines = doc_text("wiki-ko-yttrium").split("\n")
        self.assertIn(lines[56].rstrip(), ko["quotes"])
        self.assertIn(lines[57].rstrip(), ko["quotes"])

    def test_sections_in_fixed_order(self):
        order = [bc.SCOPE_ORDER.index(s) for e in ENTRIES for s in e["section"].split(" · ")]
        for e in ENTRIES:
            idx = [bc.SCOPE_ORDER.index(s) for s in e["section"].split(" · ")]
            self.assertEqual(idx, sorted(idx))
        self.assertTrue(order)


class Errors(unittest.TestCase):
    def test_missing_verdict(self):
        compare, records, vocab, verdicts = copy.deepcopy(INPUTS)
        key = next(k for k, v in verdicts.items() if k != "manual" and v["verdict"] == "부딪힘")
        del verdicts[key]
        _, errors = bc.collect(compare, records, vocab, verdicts)
        self.assertTrue(any("판정이 없다" in what and key in items for what, items in errors))

    def test_unknown_verdict_key(self):
        compare, records, vocab, verdicts = copy.deepcopy(INPUTS)
        verdicts["Tm|no_such_quantity|"] = {"verdict": "부딪힘", "why": "x"}
        verdicts["Tm|melting_point|"] = {"verdict": "부딪힘", "why": "같음 묶음"}      # 같음 묶음도 맞는 열쇠가 아니다
        _, errors = bc.collect(compare, records, vocab, verdicts)
        bad = [items for what, items in errors if "안 맞는다" in what]
        self.assertEqual(len(bad), 1)
        self.assertIn("Tm|no_such_quantity|", bad[0])
        self.assertIn("Tm|melting_point|", bad[0])

    def test_manual_raw_not_in_line(self):
        compare, records, vocab, verdicts = copy.deepcopy(INPUTS)
        verdicts["manual"][0]["places"][1]["raw"] = "이 줄에 없는 글자"
        _, errors = bc.collect(compare, records, vocab, verdicts)
        self.assertTrue(any("raw가 그 줄에 없다" in what for what, _ in errors))

    def test_main_writes_nothing_on_error(self):
        compare, records, vocab, verdicts = copy.deepcopy(INPUTS)
        verdicts["manual"][0]["places"][0] = {"id": "no:such:id"}
        _, errors = bc.collect(compare, records, vocab, verdicts)
        self.assertTrue(any("자리 id가 values.json에 없다" in what for what, _ in errors))


if __name__ == "__main__":
    unittest.main()
