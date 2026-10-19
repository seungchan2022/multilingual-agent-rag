"""check_questions.py 검사 ⑥ 시험. 임시 폴더에 가짜 질문과 문서를 만들어 쓴다."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_questions as cq

QUOTE = "밀도 (상온 근처): 5.244 g/cm3"


def question(qid="re-01", target="유로퓸", ingredient=5.244, calc="3 * 4 * 5 * 5.244 / 1000"):
    return {"id": qid, "kind": "값 + 계산", "subject": "희토류 원소", "target": target, "unit_factor": "1000",
            "question": "질문", "answer": "0.31464 kg", "value": 0.31464, "calc": calc, "steps": [],
            "evidence_quotes": [{"doc": "문서", "quote": QUOTE}], "ingredient": ingredient}


def short(qid="re-01", target="유로퓸", value=5.244):
    return {"id": qid, "target": target, "value": value}


class Check6(unittest.TestCase):
    def run_check(self, qs, shorts=None):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "md").mkdir()
            (d / "md" / "문서.md").write_text(QUOTE, encoding="utf-8")
            (d / "questions.json").write_text(json.dumps(qs, ensure_ascii=False), encoding="utf-8")
            st = None
            if shorts is not None:
                st = d / "short.json"
                st.write_text(json.dumps(shorts, ensure_ascii=False), encoding="utf-8")
            return cq.find_problems(d, st)[1]

    def test_ok(self):
        self.assertEqual(self.run_check([question()], [short()]), [])

    def test_ok_without_short_test(self):
        self.assertEqual(self.run_check([question()]), [])

    def test_ingredient_not_in_calc(self):
        p = self.run_check([question(ingredient=5.2)], [short(value=5.2)])
        self.assertEqual(len(p), 1)
        self.assertIn("⑥", p[0])

    def test_value_differs_from_short_test(self):
        p = self.run_check([question()], [short(value=5.245)])
        self.assertEqual(len(p), 1)
        self.assertIn("ⓒ", p[0])

    def test_target_differs(self):
        p = self.run_check([question()], [short(target="루테튬")])
        self.assertEqual(len(p), 1)
        self.assertIn("ⓒ", p[0])

    def test_short_test_target_missing(self):
        p = self.run_check([question()], [short(), short("re-02", "루테튬", 9.841)])
        self.assertEqual(len(p), 1)
        self.assertIn("ⓓ", p[0])

    def test_no_ingredient_field(self):
        q = question()
        del q["ingredient"]
        p = self.run_check([q], [short()])
        self.assertEqual(len(p), 1)
        self.assertIn("ⓐ", p[0])

    def test_unknown_id(self):
        p = self.run_check([question("re-09")], [short()])
        self.assertTrue(any("ⓑ" in x for x in p))


if __name__ == "__main__":
    unittest.main()
