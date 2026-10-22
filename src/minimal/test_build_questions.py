"""data/minimal/questions.json을 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

결과 파일과 코퍼스를 따로 읽어서 견준다. build_questions는 마지막 시험(다시 만들어 바이트를 견주기)에서만 불러 쓴다.
"""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "minimal" / "questions.json"
MARKDOWN = ROOT / "data" / "corpus" / "markdown"
SRC_A = "research_notes/stage2_stem_select/round2/rare_earth/questions.json"
SRC_B = "research_notes/stage2_stem_select/step4/rare_earth/questions.json"

QS = json.loads(OUT.read_text(encoding="utf-8"))
BY_ID = {q["id"]: q for q in QS}
LANG = {d["doc_id"]: d["language"] for d in
        yaml.safe_load((ROOT / "data" / "corpus" / "documents.yaml").read_text(encoding="utf-8"))["documents"]}
SRC = {f: {q["id"]: q for q in json.loads((ROOT / f).read_text(encoding="utf-8"))} for f in (SRC_A, SRC_B)}
KO = [q for q in QS if q["lang"] == "ko"]


def numbers(text):
    return [float(m) for m in re.findall(r"\d+(?:\.\d+)?", text)]


def within(x, value):
    return abs(x - value) <= abs(value) * 0.01


class TestQuestions(unittest.TestCase):
    def test_1_ids(self):
        want = [f"q{i:02d}-{l}" for i in range(1, 20) for l in ("ko", "en")]
        self.assertEqual(len(QS), 38)
        self.assertEqual([q["id"] for q in QS], want)
        self.assertEqual(len(BY_ID), 38)
        self.assertEqual(sum(q["lang"] == "ko" for q in QS), 19)
        self.assertEqual(sum(q["lang"] == "en" for q in QS), 19)

    def test_2_pairs(self):
        for q in QS:
            twin = BY_ID[q["pair_id"]]
            self.assertEqual(twin["pair_id"], q["id"])
            self.assertNotEqual(twin["lang"], q["lang"])
            for k in ("source", "value", "evidence", "branch", "one_language_basis"):
                self.assertEqual(twin[k], q[k], f"{q['id']} {k}")

    def test_3_evidence_text(self):
        for q in QS:
            is_a = q["source"]["file"] == SRC_A
            self.assertTrue(q["evidence"], q["id"])
            for e in q["evidence"]:
                line = (MARKDOWN / f"{e['doc_id']}.md").read_text(encoding="utf-8").split("\n")[e["line"] - 1]
                self.assertEqual(e["text"], line, f"{q['id']} {e['doc_id']}:{e['line']}")
                if is_a:  # 밀도 x 60 cm3 / 1000 = kg
                    ok = any(within(d * 60 / 1000, q["value"]) for d in numbers(line))
                else:
                    ok = any(within(x, q["value"]) for x in numbers(line))
                self.assertTrue(ok, f"{q['id']} {e['doc_id']}:{e['line']} 값 {q['value']}에 맞는 숫자가 없음")

    def test_4_language_and_branch(self):
        for q in QS:
            langs = set()
            for e in q["evidence"]:
                self.assertEqual(e["language"], LANG[e["doc_id"]], q["id"])
                langs.add(e["language"])
            want = "한국어만" if langs == {"ko"} else "영어만" if langs == {"en"} else "두 언어"
            self.assertEqual(q["branch"], want, q["id"])
            self.assertEqual(q["one_language_basis"] is None, want == "두 언어", q["id"])

    def test_5_branch_counts(self):
        counts = {}
        for q in KO:
            counts[q["branch"]] = counts.get(q["branch"], 0) + 1
        self.assertEqual(counts, {"한국어만": 8, "영어만": 8, "두 언어": 3})

    def test_6_korean_text_and_source(self):
        used = []
        for q in KO:
            src = SRC[q["source"]["file"]][q["source"]["id"]]
            self.assertEqual(q["question"], src["question"])
            self.assertEqual(q["answer"], src["answer"])
            self.assertEqual(q["value"], src["value"])
            used.append(q["source"]["id"])
        self.assertNotIn("re-03", used)
        self.assertEqual(len(set(used)), 19)

    def test_7_table_header_line(self):
        for q in QS:
            for e in q["evidence"]:
                ls = (MARKDOWN / f"{e['doc_id']}.md").read_text(encoding="utf-8").split("\n")
                h = e["table_header_line"]
                if not ls[e["line"] - 1].startswith("|"):
                    self.assertIsNone(h, q["id"])
                else:
                    self.assertTrue(ls[h - 1].startswith("|"), q["id"])
                    self.assertTrue(h == 1 or not ls[h - 2].startswith("|"), q["id"])
                    self.assertLessEqual(h, e["line"])
                    self.assertTrue(all(l.startswith("|") for l in ls[h - 1:e["line"]]), q["id"])

    def test_8_deterministic(self):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import build_questions
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "q.json"
            build_questions.main(p)
            self.assertEqual(p.read_bytes(), OUT.read_bytes())


if __name__ == "__main__":
    unittest.main()
