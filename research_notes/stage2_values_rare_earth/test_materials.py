"""materials.py 시험. 실제 파일로 확인하고 수는 파일에서 센다.

실행: .venv/bin/python -m unittest discover -s research_notes/stage2_values_rare_earth -p "test_*.py"
"""
import json
import re
import sys
import unittest
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compare as cp  # noqa: E402
import materials as mt  # noqa: E402
import recheck_step3 as rc  # noqa: E402

RESULT = None
RECORDS = None
KEYED = None
DOCS = None
TARGETS = None
GROUP_LANGS = {}


def setUpModule():
    global RESULT, RECORDS, KEYED, DOCS, TARGETS
    RECORDS = json.loads(mt.VALUES.read_text(encoding="utf-8"))
    DOCS = mt.corpus_docs()
    TARGETS = rc.load_conflicts(mt.DEFAULT_CONFLICTS)
    RESULT = mt.run(RECORDS, DOCS, TARGETS)
    KEYED = {r["id"]: r for r in cp.apply_keys(RECORDS, json.loads(mt.VOCAB.read_text(encoding="utf-8")))}
    # 반대 언어 자리가 있는 묶음을 compare.run으로 따로 구한다(두 자리 이상인 묶음만 나오고, 한 자리 묶음은 반대 언어가 있을 수 없다).
    for g in cp.run(RECORDS)["groups"]:
        GROUP_LANGS[(g["object"], g["quantity"], g["condition"])] = {p["lang"] for p in g["places"]}


def all_places(lang):
    r = RESULT[lang]
    out = [p for x in r["A"] for p in (x["a"], x["b"])] + list(r["B"])
    return out


def value_blocked(doc_id, line):
    """검사기 값 규칙과 자리 규칙을 시험 안에서 따로 쓴다(recheck_step3.blocked_B를 부르지 않고)."""
    flat = line.replace(",", "")
    for t in TARGETS:
        if t["doc_id"] != doc_id:
            continue
        if line.rstrip() in [q.rstrip() for q in t["quotes"]]:
            return True
        for v in t["values"]:
            if re.search(r"(?<!\d)(?<!\d\.)" + re.escape(v.replace(",", "")) + r"(?!\d)(?!\.\d)", flat):
                return True
    return False


class PoolTest(unittest.TestCase):
    def test_pool_comes_from_documents_yaml(self):
        for lang, name in mt.BRANCH.items():
            want = sorted(d["doc_id"] for d in DOCS if d["language"] == lang and d["branch"] == name)
            self.assertEqual(RESULT[lang]["pool_docs"], want)
            self.assertGreater(len(want), 0)
            for p in all_places(lang):
                self.assertIn(p["doc_id"], want)
                self.assertTrue(p["doc_id"].startswith(f"wiki-{lang}-"))

    def test_eligible_counts_are_consistent(self):
        for lang in mt.BRANCH:
            r = RESULT[lang]
            self.assertGreaterEqual(r["eligible"], len({p["id"] for p in all_places(lang)}))
            self.assertLessEqual(len(r["A"]), mt.MAX_A)
            self.assertLessEqual(len(r["B"]), mt.MAX_B)
            j = mt.to_json(RESULT)[lang]
            self.assertEqual((len(j["A"]), len(j["B"]), j["eligible"]), (len(r["A"]), len(r["B"]), r["eligible"]))


class EligibilityTest(unittest.TestCase):
    def test_no_conflict_place_or_blocked_line(self):
        conflict_places = {(t["doc_id"], p["line"], p["raw"]) for t in TARGETS for p in t["places"]}
        for lang in mt.BRANCH:
            for p in all_places(lang):
                self.assertNotIn((p["doc_id"], p["line"], p["raw"]), conflict_places, p["id"])
                line = mt.md_lines(p["doc_id"])[p["line"] - 1]
                self.assertEqual(line, p["quote"])
                self.assertFalse(value_blocked(p["doc_id"], line), p["id"])

    def test_no_place_whose_group_has_opposite_language(self):
        for lang in mt.BRANCH:
            for p in all_places(lang):
                langs = GROUP_LANGS.get((p["object"], p["quantity"], p["condition"]), {lang})
                self.assertEqual(langs, {lang}, p["id"])

    def test_no_approximation_or_estimate(self):
        for lang in mt.BRANCH:
            for p in all_places(lang):
                rec = KEYED[p["id"]]
                self.assertEqual(rec["kind"], "수")
                self.assertFalse(rec.get("multi"))
                for rep in rec["reps"]:
                    self.assertFalse(rep["approx"] or rep["est_mark"], p["id"])

    def test_keys_are_the_applied_keys(self):
        for lang in mt.BRANCH:
            for p in all_places(lang):
                rec = KEYED[p["id"]]
                self.assertEqual((p["object"], p["quantity"], p["condition"]), (rec["object"], rec["quantity"], rec["condition"]))

    def test_opposite_number_flag_is_true(self):
        for lang in mt.BRANCH:
            for p in all_places(lang):
                for f in p["flags"]["opposite_number"]:
                    self.assertTrue(f["at"])
                    for at in f["at"]:
                        doc_id, n = at.rsplit(":", 1)
                        self.assertFalse(doc_id.startswith(f"wiki-{lang}-"))
                        self.assertIn(f["number"], mt.TOKEN.findall(mt.md_lines(doc_id)[int(n) - 1].replace(",", "")))


class PairTest(unittest.TestCase):
    def test_every_pair_is_valid(self):
        for lang in mt.BRANCH:
            self.assertGreater(len(RESULT[lang]["A"]), 0)
            for x in RESULT[lang]["A"]:
                a, b = x["a"], x["b"]
                self.assertNotEqual(a["doc_id"], b["doc_id"])
                self.assertNotEqual(a["object"], b["object"])
                self.assertEqual(a["quantity"], b["quantity"])
                self.assertEqual(a["condition"], b["condition"])
                ma, mb = [self.member(KEYED[p["id"]]) for p in (a, b)]
                self.assertEqual(ma["key"][1], mb["key"][1])           # 같은 차원
                self.assertIsNone(ma["key"][3])
                self.assertNotEqual(ma["key"][2], mb["key"][2])
                big = a if ma["key"][2] > mb["key"][2] else b
                self.assertEqual(x["larger"], "a" if big is a else "b")

    @staticmethod
    def member(rec):
        return cp.member(rec["reps"][0], rec["kind"], rec["raw"], cp.header_unit(rec["label"]) if rec["where"] == "표" else "")

    def test_no_place_twice_across_A_and_B(self):
        for lang in mt.BRANCH:
            ids = [p["id"] for p in all_places(lang)]
            self.assertEqual(len(ids), len(set(ids)))

    def test_pairs_follow_round_robin_order(self):
        for lang in mt.BRANCH:
            qs = [x["quantity"] for x in RESULT[lang]["A"]]
            first = []
            for q in qs:
                if q not in first:
                    first.append(q)
            self.assertEqual(first, sorted(first))                      # 양이 처음 나오는 순서는 정렬 순서

    def test_pick_pairs_on_toy_places(self):
        def pl(i, doc, line, obj, q, lo, cond=""):
            return {"id": i, "doc_id": doc, "line": line, "object": obj, "quantity": q, "condition": cond, "_dim": "길이", "_lo": Fraction(lo)}
        places = [pl("a1", "d1", 1, "A", "x", 1), pl("a2", "d2", 1, "B", "x", 2), pl("a3", "d2", 2, "C", "x", 3),
                  pl("b1", "d1", 5, "A", "y", 5), pl("b2", "d2", 5, "B", "y", 4), pl("same", "d3", 1, "A", "x", 1)]
        out = mt.pick_pairs(places)
        ids = [i for x in out for i in (x["a"]["id"], x["b"]["id"])]
        self.assertEqual(len(ids), len(set(ids)))                       # 자리는 한 쌍에만
        self.assertEqual([x["quantity"] for x in out][:2], ["x", "y"])  # 양마다 돌아가며
        self.assertEqual((out[0]["a"]["id"], out[0]["b"]["id"]), ("a1", "a2"))
        self.assertEqual(out[1]["larger"], "a")                         # b1(5) > b2(4)
        self.assertNotIn(("a1", "same"), [(x["a"]["id"], x["b"]["id"]) for x in out])   # 같은 대상, 같은 값은 쌍이 아니다


class SingleTest(unittest.TestCase):
    def test_every_single_is_table_cell_or_has_sibling_condition(self):
        by = defaultdict(set)
        for r in KEYED.values():
            by[(r["doc_id"], r["object"], r["quantity"])].add(r["condition"])
        for lang in mt.BRANCH:
            self.assertGreater(len(RESULT[lang]["B"]), 0)
            for p in RESULT[lang]["B"]:
                self.assertTrue(p["where"] == "표" or len(by[(p["doc_id"], p["object"], p["quantity"])]) >= 2, p["id"])

    def test_every_language_has_a_table_single(self):
        for lang in mt.BRANCH:
            self.assertTrue(any(p["where"] == "표" for p in RESULT[lang]["B"]))

    def test_deterministic(self):
        again = mt.run(RECORDS, DOCS, TARGETS)
        self.assertEqual(mt.to_json(again), mt.to_json(RESULT))


if __name__ == "__main__":
    unittest.main()
