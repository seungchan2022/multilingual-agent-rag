"""make_type_check.py를 시험하는 프로그램.

  uv run python -m unittest src/questions/test_make_type_check.py

후보 묶음을 임시 폴더에 쓰고 프로그램을 하위 프로세스로 실행해, 종료 코드와 화면 글자와 출력 파일의 글자만 본다.
"""
import subprocess, sys, tempfile, unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "src" / "questions" / "make_type_check.py"
TABLE = "| 연도 | 인구 |\n|---|---|\n| 2000 | 100 |\n| 2010 | 120 |"


def candidate(cid, ctype="single_fact", passages=("근거 하나입니다.",)):
    return {"id": cid, "question": f"질문{cid}", "question_language": "ko", "evidence_language": "en", "type": ctype,
            "answer": f"정답{cid}",
            "required_facts": [{"fact": f"사실문장{cid}", "evidence": [{"doc_id": f"문서-{cid}", "location": f"위치{cid}", "passage": p} for p in passages]}],
            "opposite_check": [{"term": f"반대말{cid}", "hits": []}], "same_language_check": [{"term": f"같은말{cid}", "hits": []}]}


def run(test, data, raw=None):
    tmp = Path(tempfile.mkdtemp())
    src, dest = tmp / "in.yaml", tmp / "out" / "out.md"
    src.write_text(raw if raw is not None else "```yaml\n" + yaml.safe_dump(data, allow_unicode=True) + "```\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(PROGRAM), str(src), str(dest)], capture_output=True, text=True, cwd=ROOT)
    return proc, (dest.read_text(encoding="utf-8") if dest.exists() else None)


class MakeTypeCheckTest(unittest.TestCase):
    def test_only_single_fact_and_paraphrase(self):
        data = [candidate("c-001"), candidate("c-002", "multi_hop"), candidate("c-003", "paraphrase"), candidate("c-004", "cross_lingual")]
        proc, out = run(self, data)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(out.startswith("후보 2개다. 아래 후보마다 지시문 4번의 형식으로 답하라.\n\n## c-001"))
        self.assertIn("## c-003", out)
        self.assertNotIn("c-002", out)
        self.assertNotIn("c-004", out)
        self.assertLess(out.index("c-001"), out.index("c-003"))

    def test_fields_and_forbidden_content(self):
        proc, out = run(self, [candidate("c-001", "paraphrase")])
        self.assertIn("## c-001\n- 질문 언어: ko\n- 근거 구절 언어: en\n- 질문: 질문c-001\n- 정답: 정답c-001\n- 근거 구절 1:\n> 근거 하나입니다.", out)
        for banned in ("single_fact", "paraphrase", "type", "사실문장", "문서-c-001", "위치c-001", "반대말", "같은말", "opposite_check", "same_language_check"):
            self.assertNotIn(banned, out)

    def test_table_passage_line_for_line(self):
        _, out = run(self, [candidate("c-001", passages=(TABLE + "\n",))])
        self.assertIn("- 근거 구절 1:\n" + "\n".join("> " + l for l in TABLE.split("\n")) + "\n", out)

    def test_passages_numbered(self):
        _, out = run(self, [candidate("c-001", passages=("첫째", "둘째", "셋째"))])
        self.assertIn("- 근거 구절 1:\n> 첫째\n- 근거 구절 2:\n> 둘째\n- 근거 구절 3:\n> 셋째", out)

    def test_stdout_has_no_question_text(self):
        proc, _ = run(self, [candidate("c-001")])
        self.assertTrue(proc.stdout.startswith("후보 1개를 씀: "))
        self.assertNotIn("질문", proc.stdout)
        self.assertNotIn("정답", proc.stdout)

    def test_zero_candidates(self):
        proc, out = run(self, [candidate("c-001", "multi_hop")])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(out, "후보 0개다. 아래 후보마다 지시문 4번의 형식으로 답하라.\n")
        self.assertTrue(proc.stdout.startswith("후보 0개를 씀: "))

    def test_unreadable_yaml(self):
        proc, out = run(self, None, raw="```yaml\n- id: c-001\n  question: \"비밀질문\n  answer: x\n```\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("후보 파일의 YAML을 읽지 못함", proc.stderr)
        self.assertNotIn("비밀질문", proc.stderr)
        self.assertEqual(proc.stdout, "")
        self.assertIsNone(out)


if __name__ == "__main__":
    unittest.main()
