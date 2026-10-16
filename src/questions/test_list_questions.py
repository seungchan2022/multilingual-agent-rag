"""list_questions.py를 시험하는 프로그램.

  uv run python -m unittest src/questions/test_list_questions.py
"""
import subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "src" / "questions" / "list_questions.py"


def run(tmp, files):
    paths = []
    for n, text in enumerate(files):
        p = Path(tmp) / f"batch{n}.yaml"
        p.write_text(text, encoding="utf-8")
        paths.append(str(p))
    out = Path(tmp) / "previous.md"
    r = subprocess.run([sys.executable, str(PROGRAM), str(out), *paths], capture_output=True, text=True, cwd=ROOT)
    return r, (out.read_text(encoding="utf-8") if out.exists() else None)


class ListQuestionsTest(unittest.TestCase):
    def test_questions_in_order_from_several_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            r, out = run(tmp, ["```yaml\n- id: c-001\n  question: 비밀질문 하나\n- id: c-002\n  question: 비밀질문 둘\n```\n메모\n",
                               "- id: c-013\n  question: Secret three\n"])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(out, "비밀질문 하나\n비밀질문 둘\nSecret three\n")
            self.assertEqual(r.stdout.strip(), f"질문 3개를 씀: {Path(tmp) / 'previous.md'}")
            self.assertNotIn("비밀", r.stdout + r.stderr)

    def test_broken_yaml_hides_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            r, out = run(tmp, ["- id: c-001\n  question: \"비밀질문\n  answer: x\n"])
            self.assertEqual(r.returncode, 1)
            self.assertIn("YAML을 읽지 못함", r.stderr)
            self.assertNotIn("비밀", r.stdout + r.stderr)
            self.assertIsNone(out)


if __name__ == "__main__":
    unittest.main()
