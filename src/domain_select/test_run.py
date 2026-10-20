# run.py의 숫자 채점 규칙과 근거 글 만들기를 확인한다. 모델 서버는 부르지 않는다.
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run

CITY = Path(__file__).parents[2] / "research_notes/stage2_stem_select/city_v1/questions.json"


def vq(value):
    return {"answer": "정답", "value": value}


class NumericGrade(unittest.TestCase):
    def test_last_number_is_used(self):
        self.assertTrue(run.grade_record(vq(12.672), "760초, 즉 12.67분")["correct"])
        r = run.grade_record(vq(12.672), "12.67분, 약 13분")
        self.assertFalse(r["correct"])
        self.assertEqual(r["picked"], 13.0)

    def test_commas_removed(self):
        self.assertTrue(run.grade_record(vq(838400), "838,400 m")["correct"])

    def test_one_percent_boundary(self):
        self.assertTrue(run.grade_record(vq(100), "101")["correct"])
        self.assertFalse(run.grade_record(vq(100), "101.5")["correct"])
        self.assertTrue(run.grade_record(vq(100), "99")["correct"])

    def test_no_number(self):
        r = run.grade_record(vq(100), "모르겠다")
        self.assertFalse(r["correct"])
        self.assertIsNone(r["picked"])
        self.assertIsNone(r["diff_pct"])

    def test_multi_flag(self):
        self.assertTrue(run.grade_record(vq(100), "50, 100")["multi"])
        self.assertFalse(run.grade_record(vq(100), "100")["multi"])

    def test_record_fields(self):
        r = run.grade_record({"answer": "12.67분", "value": 12.672}, "12.7")
        self.assertEqual(r["answer_key"], "12.67분")
        self.assertEqual(r["numbers"], [12.7])
        self.assertEqual(r["diff_pct"], round(abs(12.7 - 12.672) / 12.672 * 100, 4))


class OldQuestion(unittest.TestCase):
    def test_old_rule_kept(self):
        q = next(x for x in json.loads(CITY.read_text(encoding="utf-8")) if "keys" in x)
        good = " ".join(q["keys"])
        self.assertEqual(run.grade_record(q, good), {"correct": run.grade(q, good)})
        self.assertEqual(run.grade_record(q, "전혀 다른 답"), {"correct": False})
        self.assertEqual(run.evidence_of(q), q["evidence"])


class Evidence(unittest.TestCase):
    def test_from_quotes(self):
        q = {"evidence_quotes": [{"doc": "A", "quote": "가"}, {"doc": "B", "quote": "나"}]}
        self.assertEqual(run.evidence_of(q), "[A] 가\n[B] 나")


class JudgePrompt(unittest.TestCase):
    def test_v1_file_equals_code(self):
        v1 = Path(__file__).parent / "judge_prompts" / "v1.txt"
        self.assertEqual(v1.read_text(encoding="utf-8"), run.JUDGE_SYSTEM)

    def _judge_systems(self, *extra):
        """가짜 chat으로 run_refine을 돌려 판정 모델 호출에 넘어온 system을 모은다."""
        seen = []

        def fake_chat(model, system, user, temperature, seed):
            if model == run.JUDGE_MODEL:
                seen.append(system)
            return {"text": "", "parsed": {"pass": True}, "seconds": 0, "gen_tokens": 0}

        base_rows = [{"id": "q1", "seed": 1, "gen": {"text": "답", "parsed": {"answer": "1"}}}]
        qs = [{"id": "q1", "kind": "k", "question": "질문", "answer": "1", "value": 1}]
        orig = run.chat
        run.chat = fake_chat
        try:
            with tempfile.TemporaryDirectory() as d:
                run.run_refine(qs, Path(d) / "out.jsonl", base_rows, [1], *extra)
        finally:
            run.chat = orig
        return seen

    def test_default_uses_judge_system(self):
        self.assertEqual(self._judge_systems(), [run.JUDGE_SYSTEM])

    def test_given_prompt_is_used(self):
        self.assertEqual(self._judge_systems("다른 프롬프트"), ["다른 프롬프트"])


if __name__ == "__main__":
    unittest.main()
