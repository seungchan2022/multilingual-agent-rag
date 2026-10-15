"""make_cards.py를 시험하는 프로그램.

  uv run python src/questions/test_make_cards.py

후보 묶음을 임시 폴더에 쓰고 카드 프로그램을 하위 프로세스로 실행해, 종료 코드와 출력 파일의 글자만 본다.
카드 프로그램을 불러 쓰지 않고, 후보는 이 파일의 코드로 실제 말뭉치 글자에서 따로 만든다.
"""
import os, re, subprocess, sys, tempfile, unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "src" / "questions" / "make_cards.py"
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"
URLS = {d["doc_id"]: d["url"] for d in yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]}
REAL_BATCH = ROOT / "research_notes" / "stage3_dev" / "chat3" / "batch1_ko-ko.yaml"


def lines_of(doc_id):
    return (MARKDOWN / f"{doc_id}.md").read_text(encoding="utf-8").split("\n")


def prose(doc_id):
    """문서에서 한 줄짜리 산문으로 쓸 만한 줄(30~150글자, 문서에 한 번만 나옴)과 그 줄 번호(1부터)."""
    ls = lines_of(doc_id)
    for n, l in enumerate(ls, 1):
        if 30 <= len(l) <= 150 and not l.startswith(("|", "#", "-")) and ls.count(l) == 1:
            return l, n
    raise AssertionError(doc_id)


def candidate(cid="c-001", doc="wiki-ko-chuncheon", passage=None, el="ko", ctype="single_fact", evidence=None, oc=None):
    passage = passage if passage is not None else prose(doc)[0]
    ev = [{"doc_id": doc, "location": "경제", "passage": passage}] if evidence is None else evidence
    return {"id": cid, "question": "시험 질문", "question_language": el, "evidence_language": el, "type": ctype,
            "answer": "시험 정답", "required_facts": [{"fact": "시험 사실", "evidence": ev}], "opposite_check": oc or []}


class Run:
    """후보 목록을 임시 폴더의 파일로 쓰고 프로그램을 실행한다."""

    def __init__(self, tc, items=None, src=None, out_name="out/cards.md"):
        self.tmp = Path(tempfile.mkdtemp(dir=None))
        tc.addCleanup(lambda: __import__("shutil").rmtree(self.tmp, ignore_errors=True))
        if src is None:
            src = self.tmp / "batch.yaml"
            src.write_text("```yaml\n" + yaml.safe_dump(items, allow_unicode=True) + "```\n", encoding="utf-8")
        self.src = src
        self.out = self.tmp / out_name

    def go(self):
        self.proc = subprocess.run([sys.executable, str(PROGRAM), str(self.src), str(self.out)], capture_output=True, text=True, cwd=ROOT)
        return self

    @property
    def text(self):
        return self.out.read_text(encoding="utf-8")


class MakeCardsTest(unittest.TestCase):
    def test_ko_ko_card_with_links_and_hit(self):
        passage, line_no = prose("wiki-ko-chuncheon")
        hit = "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969)"
        self.assertTrue(any(hit in l for l in lines_of("wiki-en-chuncheon")))
        oc = [{"term": "1969", "hits": [{"doc_id": "wiki-en-chuncheon", "excerpt": hit, "same_fact": False, "why": "기온 날짜"}]}]
        r = Run(self, [candidate(passage=passage, oc=oc)]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        t = r.text
        self.assertIn("## c-001 · `type`(유형): single_fact(단일 사실) · 도시 묶음: 두 언어 도시(춘천시)", t)
        m = re.search(r"\[wiki-ko-chuncheon\.md (\d+)줄\]\(([^)]+)#L(\d+)\)", t)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), m.group(3))
        self.assertEqual(int(m.group(1)), line_no)
        self.assertEqual((r.out.parent / m.group(2)).resolve(), (MARKDOWN / "wiki-ko-chuncheon.md").resolve())
        self.assertTrue(lines_of("wiki-ko-chuncheon")[int(m.group(1)) - 1].startswith(passage[:20]))
        self.assertIn(URLS["wiki-en-chuncheon"], t)
        same = t.split("같은 도시의 반대 언어 문서")[1].split("`opposite_check`")[0]
        self.assertIn("wiki-en-chuncheon.md", same)
        self.assertIn("kto-en-chuncheon-samaksan-cable-car.md", same)
        self.assertIn("(통째로 번역해 읽는다)", same)
        self.assertIn("`hits`(걸린 곳) 1곳", t)
        self.assertIn("`passage`(근거 구절):", t)
        self.assertIn("`excerpt`(걸린 구절):", t)
        self.assertIn("`same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 기온 날짜", t)

    def test_kto_document_shows_no_api_url(self):
        ex = "Samaksan Mountain Lake Cable Car is the longest cable car in Korea"
        oc = [{"term": "longest cable car", "hits": [{"doc_id": "kto-en-chuncheon-samaksan-cable-car", "excerpt": ex, "same_fact": False, "why": "시험"}]}]
        r = Run(self, [candidate(oc=oc)]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertNotIn("apis.data.go.kr", r.text)
        self.assertGreaterEqual(r.text.count("짧은 문서라 파일 내용을 그대로 번역기에 붙인다"), 2)
        self.assertIn(URLS["wiki-en-chuncheon"], r.text)

    def test_korean_only_city(self):
        r = Run(self, [candidate(doc="wiki-ko-sejong")]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn("한국어 도시(세종특별자치시)", r.text)
        self.assertIn("없음(한국어 도시)", r.text)

    def test_table_passage_points_to_header_row(self):
        ls = lines_of("wiki-ko-sejong")
        n = next(i for i, l in enumerate(ls) if l.startswith("| 읍·면·행정동") and ls[i + 1].startswith("|---"))
        passage = ls[n] + "\n" + ls[n + 2] + "\n"
        r = Run(self, [candidate(doc="wiki-ko-sejong", passage=passage, ctype="table_numeric")]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn(f"wiki-ko-sejong.md#L{n + 1})", r.text)
        self.assertIn(f"{n + 1}줄]", r.text)
        self.assertIn(f"      > {ls[n]}\n      > {ls[n + 2]}\n", r.text)

    def test_empty_evidence(self):
        c = candidate()
        c["required_facts"].append({"fact": "결론", "evidence": []})
        r = Run(self, [c]).go()
        self.assertIn("`evidence`(근거): 없음 — 다른 사실에서 나오는 결론", r.text)

    def test_no_answer(self):
        passage, line_no = prose("wiki-ko-sejong")
        c = {"id": "c-049", "question": "없는 질문", "question_language": "ko", "evidence_language": None, "type": "no_answer",
             "answer": None, "required_facts": [], "expected_refusal": "없다고 답한다", "no_answer_reason": "찾아도 없음",
             "rebuttal": [{"doc_id": "wiki-ko-sejong", "location": "첫 부분", "passage": passage}]}
        c2 = dict(c, id="c-050", rebuttal=[])
        r = Run(self, [c, c2]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        t = r.text
        self.assertIn("## c-049 · `type`(유형): no_answer(답 없음) · 질문 언어 ko", t)
        self.assertIn("- `expected_refusal`(기대하는 거절): 없다고 답한다", t)
        self.assertIn("- `no_answer_reason`(답이 없다고 본 까닭): 찾아도 없음", t)
        self.assertIn(f"- `doc_id`(문서): [wiki-ko-sejong.md {line_no}줄]", t)
        self.assertIn(f"    > {passage}", t)
        self.assertIn("### `rebuttal`(반박 구절)\n없음", t)
        self.assertIn("- [ ] 3. 전제가 너무 뻔하게 틀리지 않았다", t)
        self.assertNotIn("반대 언어 문서 확인 재료", t)

    def test_en_evidence_same_city_docs_are_korean(self):
        r = Run(self, [candidate(doc="wiki-en-jeonju", el="en")]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        same = r.text.split("같은 도시의 반대 언어 문서")[1].split("`opposite_check`")[0]
        self.assertIn("(직접 읽는다)", same)
        self.assertIn("wiki-ko-jeonju.md", same)
        self.assertNotIn("wiki-en-", same)
        self.assertIn("`data/corpus/markdown/*-ko-*`", r.text)

    def test_refuses_to_overwrite(self):
        r = Run(self, [candidate()])
        r.out.parent.mkdir(parents=True)
        r.out.write_text("내가 채운 답", encoding="utf-8")
        r.go()
        self.assertEqual(r.proc.returncode, 1)
        self.assertEqual(r.text, "내가 채운 답")
        self.assertIn("덮어쓰지 않음", r.proc.stdout)

    def test_unquoted_numeric_term(self):
        raw = "- id: c-001\n  question: q\n  question_language: ko\n  evidence_language: ko\n  type: single_fact\n  answer: a\n  required_facts:\n    - fact: f\n      evidence: []\n  opposite_check:\n    - term: 1969\n      hits: []\n"
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        src = tmp / "b.yaml"
        src.write_text(raw, encoding="utf-8")
        r = Run(self, src=src).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn("`term`(찾을 말) `1969` → `hits`(걸린 곳) 없음", r.text)

    def test_look_at_labels_appear_earlier_in_card(self):
        hit = "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969)"
        oc = [{"term": "1969", "hits": [{"doc_id": "wiki-en-chuncheon", "excerpt": hit, "same_fact": False, "why": "기온 날짜"}]}]
        r = Run(self, [candidate(oc=oc), candidate(cid="c-002", doc="wiki-en-jeonju", el="en", oc=oc)]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        cards = [c for c in r.text.split("\n---\n") if c.startswith("\n## c-")]
        self.assertEqual(len(cards), 2)
        for card in cards:
            body, checklist = card.split("### 판정")
            checked = 0
            for line in checklist.split("\n"):
                if "볼 곳:" not in line:
                    continue
                for label in re.findall(r"`[^`]+`\([^)]+\)", line.split("볼 곳:")[1]):
                    checked += 1
                    self.assertIn(label, body, f"{label} 이(가) 위에 없음: {line}")
            self.assertGreaterEqual(checked, 8)

    def test_real_batch(self):
        r = Run(self, src=REAL_BATCH).go()
        # 실제 묶음의 카드마다 "볼 곳"에 나오는 이름이 그 카드 위쪽에 있다(걸린 곳이 없는 카드 포함)
        for card in [c for c in r.text.split("\n---\n") if c.startswith("\n## c-")]:
            body, checklist = card.split("### 판정")
            for line in checklist.split("\n"):
                if "볼 곳:" in line or "해당 없음:" in line:
                    for label in re.findall(r"`[^`]+`\([^)]+\)", line.split(":", 1)[1]):
                        self.assertIn(label, body, f"{label} 이(가) 위에 없음: {line}")
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertEqual(len(re.findall(r"^## c-\d{3} · ", r.text, re.M)), 12)
        self.assertNotIn("apis.data.go.kr", r.text)
        self.assertNotIn("원문에서 찾지 못함", r.text)


if __name__ == "__main__":
    unittest.main()
