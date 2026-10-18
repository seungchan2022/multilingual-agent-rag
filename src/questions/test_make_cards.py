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
REAL_MEMO = ROOT / "research_notes" / "stage3_dev" / "chat3" / "batch1_ko-ko_full.md"
REAL_TYPES = ROOT / "research_notes" / "stage3_dev" / "chat3" / "type_check_batch1_answer4.md"
REAL2_BATCH = ROOT / "research_notes" / "stage3_dev" / "chat4" / "batch2_en-en.yaml"
REAL2_MEMO = ROOT / "research_notes" / "stage3_dev" / "chat4" / "batch2_en-en_full.md"
REAL2_TYPES = ROOT / "research_notes" / "stage3_dev" / "chat4" / "type_check_batch2_en-en_answer.md"


def lines_of(doc_id):
    return (MARKDOWN / f"{doc_id}.md").read_text(encoding="utf-8").split("\n")


def prose(doc_id):
    """문서에서 한 줄짜리 산문으로 쓸 만한 줄(30~150글자, 문서에 한 번만 나옴)과 그 줄 번호(1부터)."""
    ls = lines_of(doc_id)
    for n, l in enumerate(ls, 1):
        if 30 <= len(l) <= 150 and not l.startswith(("|", "#", "-")) and ls.count(l) == 1:
            return l, n
    raise AssertionError(doc_id)


def candidate(cid="c-001", doc="wiki-ko-chuncheon", passage=None, el="ko", ctype="single_fact", evidence=None, oc=None, question="가 나"):
    passage = passage if passage is not None else prose(doc)[0]
    ev = [{"doc_id": doc, "location": "경제", "passage": passage}] if evidence is None else evidence
    return {"id": cid, "question": question, "question_language": el, "evidence_language": el, "type": ctype,
            "answer": "시험 정답", "required_facts": [{"fact": "시험 사실", "evidence": ev}], "opposite_check": oc or []}


def count_in(doc_ids, term):
    """문서들에서 term이 나오는 곳 수(대소문자 무시, 겹치지 않게). 프로그램과 따로 센다."""
    return sum(len(re.findall(re.escape(term), "\n".join(lines_of(d)), re.I)) for d in doc_ids)


def docs_of(lang):
    return [d for d in URLS if f"-{lang}-" in d]


def hit_count(block):
    return len(re.findall(r"^  - 걸린 곳 \d+: ", block, re.M))


def split_cards(text):
    return [c for c in text.split("\n---\n") if c.startswith("\n## c-")]


def item_text(text, n):
    """첫 카드의 n번 칸 글자(다음 칸 또는 '적기' 앞까지)."""
    return re.split(r"\n#### ", text.split(f"#### {n}. ")[1])[0]


def check_labels(tc, card):
    """칸들에서 쓴 `이름`(뜻) 이름표는 **후보** 블록(첫 칸 앞)에 이미 나와 있어야 한다. 찾을 말 목록의 `term`은 정의라 뺀다."""
    head, rest = card.split("#### 1. ", 1)
    items = rest.split("#### 적기")[0]
    used = 0
    for line in items.split("\n"):
        if line.startswith("- `term`(찾을 말)"):
            continue
        for label in re.findall(r"`[a-z_]+`\([^)]+\)", line):
            used += 1
            tc.assertIn(label, head, f"{label} 이(가) 후보 블록에 없음: {line}")
    tc.assertGreater(used, 0)


def rerequest_of(stdout):
    """출력에서 가로줄 두 개 사이의 재요청 글."""
    parts = stdout.split("-" * 60 + "\n")
    return parts[1] if len(parts) >= 3 else ""


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

    def go(self, memo=None, types=None):
        cmd = [sys.executable, str(PROGRAM), str(self.src), str(self.out)] + (["--memo", str(memo)] if memo else []) + (["--types", str(types)] if types else [])
        self.proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        return self

    @property
    def text(self):
        return self.out.read_text(encoding="utf-8")


class MakeCardsTest(unittest.TestCase):
    def test_ko_ko_card_with_links_and_hit(self):
        passage, line_no = prose("wiki-ko-chuncheon")
        hit = "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969)"
        hit_line = next(n for n, l in enumerate(lines_of("wiki-en-chuncheon"), 1) if hit in l)
        r = Run(self, [candidate(passage=passage, oc=["1969"])]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        t = r.text
        self.assertIn("## c-001 · `type`(유형): single_fact(단일 사실) · 도시 갈래: 두 언어 도시(춘천시)", t)
        m = re.search(r"\[wiki-ko-chuncheon\.md (\d+)줄\]\(([^)]+)#L(\d+)\)", t)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), m.group(3))
        self.assertEqual(int(m.group(1)), line_no)
        self.assertEqual((r.out.parent / m.group(2)).resolve(), (MARKDOWN / "wiki-ko-chuncheon.md").resolve())
        self.assertTrue(lines_of("wiki-ko-chuncheon")[int(m.group(1)) - 1].startswith(passage[:20]))
        self.assertIn(URLS["wiki-en-chuncheon"], t)
        same = item_text(t, 7)
        self.assertIn("wiki-en-chuncheon", same)
        self.assertIn("kto-en-chuncheon-samaksan-cable-car.md", same)
        self.assertIn("한국어로 번역", same)
        i5 = item_text(t, 5)
        self.assertIn("프로그램이 영어 문서 14개에서 찾은 걸린 곳 전부다.", i5)
        self.assertIn("- `term`(찾을 말) `1969`:", i5)
        self.assertEqual(hit_count(i5), count_in(docs_of("en"), "1969"))
        self.assertIn(f"걸린 곳 1: [wiki-en-chuncheon.md {hit_line}줄]", i5)
        self.assertIn(f"wiki-en-chuncheon.md#L{hit_line})", i5)
        self.assertIn(f" · 원문 주소(앞뒤 문맥을 볼 때): {URLS['wiki-en-chuncheon']}", i5)
        self.assertIn("    > …west measured temperature was −27.9 °C (−18 °F) (6 February [1969]), and the highest was 39.5 °C", i5)
        self.assertNotIn("Gemini의 판단", i5)
        self.assertIn("- `passage`(근거 구절):", t)
        self.assertIn("  - 사실 1의 근거 1: [wiki-ko-chuncheon.md", t)

    def test_snippet_is_cut_at_line_boundaries(self):
        ls = lines_of("wiki-en-busan")
        n = next(i for i, l in enumerate(ls) if l.startswith("- Kim Wonhae (born 1969)"))
        r = Run(self, [candidate(oc=["Wonhae"])]).go()
        i5 = item_text(r.text, 5)
        self.assertIn(f"wiki-en-busan.md {n + 1}줄]", i5)
        self.assertIn("    > - Kim [Wonhae] (born 1969), actor and comedian\n", i5)
        self.assertNotIn("…", i5.split("[Wonhae]")[0].split("> ")[-1])

    def test_kto_document_shows_no_api_url(self):
        r = Run(self, [candidate(oc=["longest cable car"])]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn("kto-en-chuncheon-samaksan-cable-car.md", item_text(r.text, 5))
        self.assertIn("[longest cable car]", item_text(r.text, 5))
        self.assertNotIn("apis.data.go.kr", r.text)
        self.assertIn("내용 전체를 번역기에 붙여 읽는다. 짧은 글이다.", item_text(r.text, 7))
        self.assertIn(URLS["wiki-en-chuncheon"], r.text)

    def test_korean_only_city(self):
        r = Run(self, [candidate(doc="wiki-ko-sejong")]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn("한국어 도시(세종특별자치시)", r.text)
        self.assertIn("세종특별자치시는 영어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.", item_text(r.text, 7))

    def test_table_passage_points_to_header_row(self):
        ls = lines_of("wiki-ko-sejong")
        n = next(i for i, l in enumerate(ls) if l.startswith("| 읍·면·행정동") and ls[i + 1].startswith("|---"))
        passage = ls[n] + "\n" + ls[n + 2] + "\n"
        r = Run(self, [candidate(doc="wiki-ko-sejong", passage=passage, ctype="table_numeric")]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn(f"wiki-ko-sejong.md#L{n + 1})", r.text)
        self.assertIn(f"{n + 1}줄]", r.text)
        self.assertIn(f"    > {ls[n]}\n    > {ls[n + 2]}\n", r.text)

    def test_empty_evidence(self):
        c = candidate()
        c["required_facts"].append({"fact": "결론", "evidence": []})
        r = Run(self, [c]).go()
        self.assertIn("`fact`(사실) 2: 결론 (근거 없음 — 다른 사실들에서 나오는 결론이라 문서에 이 문장이 없다. 채점 때 답에 이 결론이 들어 있는지 본다)", r.text)

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
        self.assertIn("#### 1. 문서 전체에서 한국어 표현과 영어 표현으로 찾아봐도 답이 없다", t)
        self.assertIn("#### 2. 문서를 보지 않고 일반 지식으로도 답할 수 없다", t)
        self.assertIn("- `no_answer_reason`(답이 없다고 본 까닭): 찾아도 없음", t)
        self.assertIn(f"  - [wiki-ko-sejong.md {line_no}줄]", t)
        self.assertIn(f"    > {passage}", t)
        self.assertIn("- `rebuttal`(반박 구절):\n  - 없음", t)
        self.assertIn("#### 3. 전제가 너무 뻔하게 틀리지 않았다", t)
        self.assertNotIn("같은 도시", t)

    def test_english_reading_line(self):
        # 영어인 칸만 이름을 들어 번역기로 읽게 하고, 한국어 카드에는 넣지 않는다
        ko = Run(self, [candidate()]).go()
        self.assertNotIn("영어 읽는 법", ko.text)
        q_en = candidate()
        q_en["question_language"] = "en"
        e_en = candidate(cid="c-002", doc="wiki-en-jeonju", el="en")
        e_en["question_language"] = "ko"
        r = Run(self, [q_en, e_en]).go(types=self._any_types())
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        cards = split_cards(r.text)
        self.assertIn("**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실). ", cards[0])
        self.assertIn("**영어 읽는 법** — 영어로 적힌 칸: `passage`(근거 구절). ", cards[1])
        for card in cards:
            self.assertIn("옮긴 글로 칸 1~8을 판단한다", card)
            self.assertIn("칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다", card)
            self.assertTrue(card.index("영어 읽는 법") < card.index("#### 1."))
        na = {"id": "c-049", "question": "No such thing?", "question_language": "en", "evidence_language": None, "type": "no_answer",
              "answer": None, "required_facts": [], "expected_refusal": "Says none", "no_answer_reason": "Not found",
              "rebuttal": [{"doc_id": "wiki-en-jeonju", "location": "top", "passage": prose("wiki-en-jeonju")[0]}]}
        t = Run(self, [na]).go().text
        self.assertIn("`question`(질문), `expected_refusal`(기대하는 거절), `no_answer_reason`(답이 없다고 본 까닭), `rebuttal`(반박 구절). ", t)
        self.assertIn("옮긴 글로 칸 1~3을 판단한다", t)
        self.assertNotIn("칸 9", t)

    def test_en_evidence_same_city_docs_are_korean(self):
        r = Run(self, [candidate(doc="wiki-en-jeonju", el="en")]).go(types=self._any_types())
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        same = item_text(r.text, 7)
        self.assertIn("wiki-ko-jeonju.md", same)
        self.assertIn("3번의 찾을 말로 `Cmd+F` 하고", same)
        self.assertNotIn("wiki-en-", same)
        self.assertNotIn("번역", item_text(r.text, 5) + item_text(r.text, 6) + same)
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
        raw = "- id: c-001\n  question: q\n  question_language: ko\n  evidence_language: ko\n  type: single_fact\n  answer: a\n  required_facts:\n    - fact: f\n      evidence: []\n  opposite_check:\n    - 1969\n    - yyyy\n    - zzzz\n"
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        src = tmp / "b.yaml"
        src.write_text(raw, encoding="utf-8")
        r = Run(self, src=src).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        i5 = item_text(r.text, 5)
        self.assertIn("- `term`(찾을 말) `1969`:", i5)
        self.assertIn("[1969]", i5)
        self.assertIn("찾을 말 `yyyy`, `zzzz`: 걸린 곳이 없다.", i5)

    def test_old_shape_records_use_term_only(self):
        c = candidate(oc=[{"term": "1969", "hits": [{"doc_id": "wiki-en-busan", "excerpt": "엉뚱한 글", "same_fact": True, "why": "엉뚱"}]}])
        i5 = item_text(Run(self, [c]).go().text, 5)
        self.assertIn("[1969]", i5)
        self.assertNotIn("엉뚱", i5)

    def test_no_hits_at_all(self):
        r = Run(self, [candidate(oc=["alphaxyz", "betaxyz"])]).go()
        i5 = item_text(r.text, 5)
        self.assertIn("Gemini가 고른 찾을 말 `alphaxyz`, `betaxyz`: 프로그램이 영어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.", i5)
        self.assertNotIn("`term`", i5)
        self.assertIn("- Gemini가 고른 찾을 말: `alphaxyz`, `betaxyz`", item_text(r.text, 6))

    def test_numbers_from_answer_in_item3(self):
        c = candidate()
        c["answer"] = "1,234명과 12.5%, 1969년"
        r = Run(self, [c]).go()
        self.assertIn("정답과 사실에서 뽑은 숫자: `1,234`, `12.5`, `1969`", item_text(r.text, 3))
        r2 = Run(self, [candidate()]).go()
        self.assertIn("정답과 사실에서 뽑은 숫자:", item_text(r2.text, 3))

    def test_numbers_from_answer_and_facts_not_passage(self):
        d = ROOT / "research_notes" / "stage3_dev" / "chat3"
        r = Run(self, src=d / "batch1_ko-ko_newshape.yaml").go(memo=d / "batch1_ko-ko_full.md")
        cards = {re.match(r"\n## (c-\d+)", c).group(1): c for c in split_cards(r.text)}
        i3 = lambda cid: re.split(r"\n#### ", cards[cid].split("#### 3. ")[1])[0]
        self.assertIn("정답과 사실에서 뽑은 숫자: `45,860`, `120,107`, `87,514`, `178,735`, `148,252`", i3("c-007"))
        self.assertIn("정답과 사실에서 뽑은 숫자: `1342`, `2026`, `3`, `17`, `18`, `890`, `452`", i3("c-008"))
        self.assertIn("정답과 사실에서 뽑은 숫자: 없음", i3("c-009"))

    def test_answer_value_in_item3(self):
        c = candidate()
        c["answer"] = "파랑새이다"
        self.assertIn("정답의 값: `파랑새` · 정답과", item_text(Run(self, [c]).go().text, 3))
        c["answer"] = "1969년"
        self.assertIn("정답의 값: `1969년` · 정답과", item_text(Run(self, [c]).go().text, 3))
        c["answer"] = "가나다라마바사아자차카타파하 " * 3
        i3 = item_text(Run(self, [c]).go().text, 3)
        self.assertIn("정답의 값: 위 `answer`(정답)에서 값마다 골라 찾는다 · 정답과", i3)
        self.assertNotIn("가나다라마바사아자차카타파하 가나다", i3)

    def test_item6_has_search_line_and_verdict_does_not(self):
        t = Run(self, [candidate()]).go().text
        i6 = item_text(t, 6)
        self.assertTrue(i6.rstrip().endswith("- 더 찾아본 말과 걸린 곳:\n- [ ] 확인함"))
        self.assertNotIn("맨 아래", i6)
        self.assertNotIn("더 찾아본 말과 걸린 곳", t.split("#### 적기")[1])

    def test_details_block_has_raw_yaml(self):
        r = Run(self, [candidate(oc=["x"])]).go()
        details = r.text.split("<details>")[1].split("</details>")[0]
        self.assertIn("opposite_check:", details)
        self.assertIn("```yaml", details)

    def test_labels_appear_in_candidate_block_first(self):
        oc = ["1969"]
        r = Run(self, [candidate(oc=oc), candidate(cid="c-002", doc="wiki-en-jeonju", el="en", oc=["Jeonju"])]).go(types=self._any_types())
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        cards = split_cards(r.text)
        self.assertEqual(len(cards), 2)
        for card in cards:
            check_labels(self, card)

    def slc(self, el, doc, terms, passage=None):
        """same_language_check 시험 후보: terms는 찾을 말 글자 목록."""
        c = candidate(doc=doc, el=el, passage=passage)
        c["same_language_check"] = terms
        return c

    def test_same_language_hits_split_between_item3_and_item4(self):
        # 근거 문서 안의 산문 줄 하나가 근거 구절이다. 그 줄 안의 걸린 곳은 빼고, 나머지는 문서가 같은지로 3번/4번에 나뉜다.
        passage, line_no = prose("wiki-ko-chuncheon")
        term = "춘천"
        own_in_passage = passage.count(term)
        c = self.slc("ko", "wiki-ko-chuncheon", [term, "존재하지않는말"], passage)
        t = Run(self, [c]).go().text
        i3, i4 = item_text(t, 3), item_text(t, 4)
        self.assertGreater(own_in_passage, 0)
        self.assertEqual(hit_count(i3), count_in(["wiki-ko-chuncheon"], term) - own_in_passage)
        self.assertEqual(hit_count(i4), count_in([d for d in docs_of("ko") if d != "wiki-ko-chuncheon"], term))
        self.assertGreater(hit_count(i3), 0)
        self.assertGreater(hit_count(i4), 0)
        self.assertNotIn("wiki-ko-jeonju", i3)
        self.assertNotIn(f"wiki-ko-chuncheon.md {line_no}줄]", i3)
        self.assertNotIn("wiki-ko-chuncheon", i4)
        self.assertRegex(i3, r"\n    > .*\[춘천\]")
        self.assertIn("찾을 말 `존재하지않는말`: 근거 문서 안에서는 걸린 곳이 없다.", i3)
        self.assertIn("찾을 말 `존재하지않는말`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다.", i4)
        self.assertIn("프로그램이 한국어 문서에서 찾은", i3)
        self.assertNotIn("Gemini의 판단", i3 + i4)
        self.assertLess(i4.index("Cmd+Shift+F"), i4.index("Gemini가"))
        self.assertIn("3번의 찾을 말로 찾는다.", i4)
        self.assertIn("Cmd+클릭", i3)
        self.assertNotIn("번역", i3 + i4)

    def test_same_language_excludes_own_passage_entirely(self):
        passage, _ = prose("wiki-ko-chuncheon")
        term = passage[5:11]
        self.assertEqual(count_in(["wiki-ko-chuncheon"], term), passage.count(term))
        c = self.slc("ko", "wiki-ko-chuncheon", [term], passage)
        i3 = item_text(Run(self, [c]).go().text, 3)
        self.assertIn(f"- Gemini가 고른 찾을 말 `{term}`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.", i3)

    def test_item5_unchanged_by_same_language_check(self):
        plain = candidate(oc=["1969"])
        with_slc = self.slc("ko", "wiki-ko-chuncheon", ["춘천"])
        with_slc["opposite_check"], with_slc["required_facts"] = ["1969"], plain["required_facts"]
        a = item_text(Run(self, [plain]).go().text, 5)
        b = item_text(Run(self, [with_slc]).go().text, 5)
        self.assertEqual(a, b)
        self.assertIn("[1969]", a)

    def test_en_evidence_item3_and_item4_use_translation(self):
        c = self.slc("en", "wiki-en-jeonju", ["Jeonju", "hanok"])
        t = Run(self, [c]).go(types=self._any_types()).text
        i3, i4 = item_text(t, 3), item_text(t, 4)
        self.assertIn(URLS["wiki-en-jeonju"], i3)
        self.assertIn("한국어로 번역", i3)
        self.assertIn("위 찾을 말(한국어)과 숫자", i3)
        self.assertNotIn("Cmd+클릭", i3)
        self.assertIn("번역기에 붙여 읽는다", i3)
        self.assertIn("번역기로 영어로 옮긴 말과 숫자", i4)
        self.assertIn("번역기에 붙여 읽는다", i4)
        self.assertIn("`data/corpus/markdown/*-en-*`", i4)

    def test_en_evidence_kto_doc_pasted_whole(self):
        kto = next(d for d in URLS if d.startswith("kto-en-"))
        c = self.slc("en", kto, ["Jeonju"])
        i3 = item_text(Run(self, [c]).go(types=self._any_types()).text, 3)
        self.assertIn("내용 전체를 번역기에 붙여 읽는다", i3)

    def test_ko_evidence_wording_unchanged_without_field(self):
        t = Run(self, [candidate()]).go().text
        i3, i4 = item_text(t, 3), item_text(t, 4)
        self.assertNotIn("Gemini", i3 + i4)
        self.assertIn("- 할 일: 위 근거 문서 링크를 `Cmd+클릭`해 열고", i3)
        self.assertTrue(i4.split("\n", 1)[1].startswith("- 할 일: `Cmd+Shift+F`"))
        self.assertIn("3번의 찾을 말로 찾는다.\n", i4)

    def test_no_field_means_no_gemini_block_en(self):
        t = Run(self, [candidate(doc="wiki-en-jeonju", el="en")]).go(types=self._any_types()).text
        self.assertNotIn("검사 프로그램이 확인함", item_text(t, 3) + item_text(t, 4))

    def test_real_batch(self):
        r = Run(self, src=REAL_BATCH).go(memo=REAL_MEMO)
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        cards = split_cards(r.text)
        self.assertEqual(len(cards), 12)
        self.assertEqual(len(re.findall(r"^## c-\d{3} · ", r.text, re.M)), 12)
        for card in cards:
            check_labels(self, card)
        self.assertNotIn("apis.data.go.kr", r.text)
        self.assertNotIn("원문에서 찾지 못함", r.text)

    def test_multi_doc_meaning_mentions_table_comparison(self):
        t = Run(self, [candidate(ctype="multi_doc")]).go().text
        self.assertIn("(비교, 집계, 여러 단계). 표의 값이나 수치를 비교하는 질문도 여기다.", item_text(t, 9))

    def test_judging_questions_pass_on_yes(self):
        t = Run(self, [candidate(oc=["1969"])]).go().text
        self.assertIn("- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?", item_text(t, 5))
        self.assertIn("- 판단할 질문: 영어 문서 어디에도 같은 사실이 다른 표현으로 없는가?", item_text(t, 6))
        self.assertIn("- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?", item_text(t, 7))

    def test_item1_has_premise_question(self):
        i1 = item_text(Run(self, [candidate()]).go().text, 1)
        self.assertIn("- 판단할 질문: 이 구절만 받은 사람이", i1)
        self.assertIn("- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 \"5개 자치구 중\"이면 근거 문서에 자치구가 5개인지 본다.", i1)

    def _memo_file(self, body):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(d, ignore_errors=True))
        f = d / "full.md"
        f.write_text(body, encoding="utf-8")
        return f

    def test_paraphrase_card_has_table_and_memo(self):
        memo = self._memo_file("설명\n```yaml\n- id: c-001\n  note: c-001: 코드 안 줄\n```\n\n- c-001: \"가\"를 \"나\"로 바꿈\n* c-002: \"다\"를 \"라\"로 바꿈\n")
        items = [candidate(cid="c-001", ctype="paraphrase"), candidate(cid="c-002", ctype="paraphrase"),
                 candidate(cid="c-003", ctype="paraphrase"), candidate(cid="c-004", ctype="single_fact")]
        r = Run(self, items).go(memo=memo)
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        cards = split_cards(r.text)
        i9 = [item_text(c.replace("\n---\n", ""), 9) for c in cards]
        for k in range(3):
            self.assertIn("`질문 조각 → 근거 구절의 짝 (같은 말 / 바꾼 말 / 이름)`", i9[k])
            self.assertEqual(i9[k].count("\n- 짝 목록:\n  - \n  - \n  - \n  - \n"), 1)
            self.assertIn("<details><summary>Gemini가 적은 바꾼 말(짝 목록을 채운 뒤 펼친다)</summary>", i9[k])
            self.assertIn("- 판단할 질문: \"바꾼 말\" 줄이 하나 이상 있는가?", i9[k])
            self.assertIn("표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).", i9[k])
        self.assertIn("\n\"가\"를 \"나\"로 바꿈\n", i9[0])
        self.assertNotIn("코드 안 줄", r.text.split("<details>")[1])
        self.assertIn("\n\"다\"를 \"라\"로 바꿈\n", i9[1])
        self.assertNotIn("\"가\"를 \"나\"로 바꿈", i9[1])
        self.assertIn("\nGemini가 적은 바꾼 말이 없다.\n", i9[2])
        for bad in ("질문 조각", "<details>", "바꾼 말"):
            self.assertNotIn(bad, i9[3])
        self.assertIn("- 판단할 질문: 이 후보가 이 뜻에 맞는가?", i9[3])

    def test_paraphrase_without_memo_fails(self):
        r = Run(self, [candidate(ctype="paraphrase")]).go()
        self.assertEqual(r.proc.returncode, 1)
        self.assertIn("사용법", r.proc.stdout)
        self.assertFalse(r.out.exists())

    def test_no_paraphrase_needs_no_memo(self):
        r = Run(self, [candidate()]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)

    def _any_types(self):
        """영어 후보 시험용: --types 필수 규칙만 넘기는 빈 구역 답 파일."""
        line = "- \"가\" → \"나\"(나) · 같은 말 · 핵심 낱말 예 · 까닭\n- \"나\" → \"나\"(나) · 같은 말 · 핵심 낱말 예 · 까닭\n"
        return self._memo_file("## c-001\n" + line + "## c-002\n" + line)

    TYPES_HEADER = "- 질문 조각 → 근거 구절의 짝 · 가름 · 핵심 낱말 예/아니오 · 까닭"
    DETAILS = "<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>"
    SF_Q = "- 판단할 질문: ChatGPT 목록에서 \"핵심 낱말 예\"인 줄에 \"바꾼 말\"이 없는가? (있으면 단일 사실이 아니다)"
    PA_Q = "- 판단할 질문: ChatGPT 목록에서 \"핵심 낱말 예\"인 줄에 \"바꾼 말\"이 하나 이상 있는가?"
    MEANING_Q = "- 판단할 질문: ChatGPT 목록에서 \"가르기 어려움\"이나 \"짝 없음\"인 줄마다, 그 조각의 뜻이 문서에 있는가? "

    def _types_text(self):
        return ("앞 설명\n```text\n## c-001\n" + self.TYPES_HEADER + "\n- \"가\" → \"A\"(에이) · 같은 말 · 핵심 낱말 예 · 까닭1\n"
                "- \"나\" → \"B\"(비) · 바꾼 말 · 핵심 낱말 예 · 까닭2\n\n## c-002\n" + self.TYPES_HEADER + "\n- \"다\" → 없음 · 짝 없음 · 핵심 낱말 아니오 · 까닭3\n```\n뒤 설명\n- 코드 밖 줄\n")

    def test_read_types_fenced_and_unfenced(self):
        import importlib.util
        sys.path.insert(0, str(PROGRAM.parent))
        self.addCleanup(sys.path.remove, str(PROGRAM.parent))
        spec = importlib.util.spec_from_file_location("make_cards", PROGRAM)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        fenced = mod.read_types(self._memo_file(self._types_text()))
        self.assertEqual(list(fenced), ["c-001", "c-002"])
        self.assertEqual(fenced["c-001"], ['- "가" → "A"(에이) · 같은 말 · 핵심 낱말 예 · 까닭1', '- "나" → "B"(비) · 바꾼 말 · 핵심 낱말 예 · 까닭2'])
        self.assertEqual(fenced["c-002"], ['- "다" → 없음 · 짝 없음 · 핵심 낱말 아니오 · 까닭3'])
        plain = mod.read_types(self._memo_file("## c-005\n" + self.TYPES_HEADER + "\n- 줄 하나\n## c-006\n- 줄 둘\n- 줄 셋\n"))
        self.assertEqual(plain, {"c-005": ["- 줄 하나"], "c-006": ["- 줄 둘", "- 줄 셋"]})

    def test_types_block_in_item9_single_fact_and_paraphrase(self):
        items = [candidate(cid="c-001"), candidate(cid="c-002", ctype="paraphrase", question="다"), candidate(cid="c-003", ctype="multi_doc"),
                 candidate(cid="c-004", ctype="table_numeric")]
        r = Run(self, items).go(memo=self._memo_file("- c-002: 바꿈\n"), types=self._memo_file(self._types_text()))
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        i9 = [item_text(c.replace("\n---\n", ""), 9) for c in split_cards(r.text)]
        self.assertIn(self.DETAILS + '\n\n- "가" → "A"(에이) · 같은 말 · 핵심 낱말 예 · 까닭1\n- "나" → "B"(비) · 바꾼 말 · 핵심 낱말 예 · 까닭2\n\n</details>', i9[0])
        self.assertNotIn(self.TYPES_HEADER, i9[0])
        self.assertIn("- 판단할 질문: 이 후보가 이 뜻에 맞는가?\n\n" + self.DETAILS, i9[0])
        self.assertTrue(i9[0].index(self.DETAILS) < i9[0].index(self.SF_Q))
        self.assertNotIn(self.PA_Q, i9[0])
        gem = i9[1].index("<details><summary>Gemini가")
        self.assertTrue(gem < i9[1].index(self.DETAILS) < i9[1].index(self.PA_Q))
        self.assertIn('\n- "다" → 없음 · 짝 없음 · 핵심 낱말 아니오 · 까닭3\n', i9[1])
        self.assertNotIn(self.SF_Q, i9[1])
        # 뜻이 문서에 있는지 묻는 질문은 ChatGPT 목록 바로 뒤, 유형 질문보다 먼저 온다
        self.assertTrue(i9[0].index(self.DETAILS) < i9[0].index(self.MEANING_Q) < i9[0].index(self.SF_Q))
        self.assertTrue(i9[1].index(self.DETAILS) < i9[1].index(self.MEANING_Q) < i9[1].index(self.PA_Q))
        for k in (2, 3):
            for bad in ("ChatGPT", "<details>"):
                self.assertNotIn(bad, i9[k])
        self.assertNotIn("주의", r.proc.stdout)

    def test_types_missing_id_stops_with_rerequest(self):
        items = [candidate(cid="c-001"), candidate(cid="c-007"), candidate(cid="c-008", ctype="paraphrase"), candidate(cid="c-009", ctype="multi_doc")]
        r = Run(self, items).go(memo=self._memo_file("- c-008: 바꿈\n"), types=self._memo_file(self._types_text()))
        self.assertEqual(r.proc.returncode, 1)
        self.assertFalse(r.out.exists())
        out = r.proc.stdout
        self.assertIn("아래 후보들의 목록에 문제가 있다. 이 후보들만 지시문 4번 형식대로, 질문 전체를 빠짐없이 조각으로 나눠 다시 써라. 코드 블록 하나에 넣는다.\n- c-007: 이 후보의 목록이 없다\n- c-008: 이 후보의 목록이 없다\n", out)
        self.assertNotIn("c-009", out)
        self.assertNotIn("c-001", out)
        self.assertNotIn("가 나", out)

    def test_types_missing_multi_doc_is_fine(self):
        items = [candidate(cid="c-001"), candidate(cid="c-009", ctype="multi_doc")]
        r = Run(self, items).go(types=self._memo_file(self._types_text()))
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)

    def test_types_bad_lines_stop(self):
        cases = {
            "칸 수": ('- "가" → "A"(에이) · 같은 말 · 핵심 낱말 예', "칸 수가 4가 아님"),
            "가름 값": ('- "가" → "A"(에이) · 비슷한 말 · 핵심 낱말 예 · 까닭', "가름이 다섯 값"),
            "핵심 낱말": ('- "가" → "A"(에이) · 같은 말 · 핵심 어휘 예 · 까닭', "셋째 칸"),
            "없음 짝": ('- "가" → 없음 · 같은 말 · 핵심 낱말 예 · 까닭', "서로 맞지 않음"),
            "짝 없음 가름인데 짝이 있음": ('- "가" → "A"(에이) · 짝 없음 · 핵심 낱말 예 · 까닭', "서로 맞지 않음"),
            "빈 까닭": ('- "가" → "A"(에이) · 같은 말 · 핵심 낱말 예 · ', "칸 수가 4가 아님"),
            "화살표 없음": ('- "가" "A" · 같은 말 · 핵심 낱말 예 · 까닭', "→ 가 없음"),
            "영어 조각 뜻 없음": ('- "founded" → "창단" · 바꾼 말 · 핵심 낱말 예 · 까닭', "한국어 뜻 괄호가 없음"),
            "영어 짝 뜻 없음": ('- "가" → "founded" · 바꾼 말 · 핵심 낱말 예 · 까닭', "한국어 뜻 괄호가 없음"),
            "영어 뜻 괄호에 한글 없음": ('- "가" → "founded"(abc) · 바꾼 말 · 핵심 낱말 예 · 까닭', "한국어 뜻 괄호가 없음"),
        }
        for name, (line, problem) in cases.items():
            c = candidate(cid="c-001", doc="wiki-en-chuncheon", el="en")
            if name.startswith("영어 조각"):
                c["evidence_language"] = "ko"
            elif name.startswith("영어 짝") or name.startswith("영어 뜻"):
                c["question_language"] = "ko"
            elif name in ("칸 수", "가름 값", "핵심 낱말", "없음 짝", "짝 없음 가름인데 짝이 있음", "빈 까닭", "화살표 없음"):
                c["question_language"] = c["evidence_language"] = "ko"
            r = Run(self, [c]).go(types=self._memo_file("## c-001\n" + line + "\n"))
            self.assertEqual(r.proc.returncode, 1, name)
            self.assertFalse(r.out.exists(), name)
            self.assertIn("c-001", r.proc.stdout, name)
            self.assertIn(problem, r.proc.stdout, name)
            self.assertRegex(rerequest_of(r.proc.stdout), rf"- c-001: 1번째 줄: .*{re.escape(problem)}", name)

    def test_types_korean_piece_needs_no_paren(self):
        c = candidate(cid="c-001", doc="wiki-en-chuncheon", el="en", question="창단")
        c["question_language"] = "ko"
        r = Run(self, [c]).go(types=self._memo_file('## c-001\n- "창단" → "founded"(창단된) · 같은 말 · 핵심 낱말 예 · 까닭\n'))
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)

    def test_types_duplicate_section_uses_later(self):
        first = '## c-001\n- "앞" → "A" · 같은 말 · 핵심 낱말 예\n'
        second = '```text\n## c-001\n- "뒤" → "B" · 바꾼 말 · 핵심 낱말 예 · 뒤의 까닭\n```\n'
        r = Run(self, [candidate(question="뒤")]).go(types=self._memo_file("```text\n" + first + "```\n" + second))
        self.assertEqual(r.proc.returncode, 0, r.proc.stdout)
        self.assertIn("뒤의 까닭", r.text)
        self.assertNotIn('"앞"', r.text)

    def test_old_shape_terms_stop_with_message(self):
        c = candidate(oc=[{"doc_id": "wiki-en-busan", "excerpt": "엉뚱한 글"}])
        r = Run(self, [c]).go()
        self.assertEqual(r.proc.returncode, 1)
        self.assertIn("찾기 기록이 예전 모양이다. 후보 검사(check_candidates.py)를 먼저 통과시킨다", r.proc.stdout)
        self.assertNotIn("Traceback", r.proc.stderr)
        self.assertFalse(r.out.exists())
        c = candidate(oc=[["중첩"]])
        r = Run(self, [c]).go()
        self.assertEqual(r.proc.returncode, 1)
        self.assertNotIn("Traceback", r.proc.stderr)

    def test_types_file_unreadable(self):
        r = Run(self, [candidate()]).go(types=self.tmp_missing())
        self.assertEqual(r.proc.returncode, 1)
        self.assertIn("ChatGPT 답 파일을 읽지 못함", r.proc.stdout)

    def tmp_missing(self):
        return Path(tempfile.gettempdir()) / "no-such-types-answer.md"

    def test_real_answer4_makes_cards(self):
        r = Run(self, src=REAL_BATCH).go(memo=REAL_MEMO, types=REAL_TYPES)
        self.assertEqual(r.proc.returncode, 0, r.proc.stdout)
        self.assertEqual(len(split_cards(r.text)), 12)

    def _real_with(self, edit):
        text = edit(REAL_TYPES.read_text(encoding="utf-8"))
        return Run(self, src=REAL_BATCH).go(memo=REAL_MEMO, types=self._memo_file(text))

    def test_real_answer4_missing_piece_line_stops(self):
        r = self._real_with(lambda t: "\n".join(l for l in t.split("\n") if not l.startswith('- "전소된"')))
        self.assertEqual(r.proc.returncode, 1)
        self.assertFalse(r.out.exists())
        self.assertIn("ChatGPT 답의 문제  c-010", r.proc.stdout)
        self.assertIn("질문에서 조각으로 덮이지 않은 부분이 있음", r.proc.stdout)
        self.assertNotIn("전소", r.proc.stdout.replace(rerequest_of(r.proc.stdout), ""))
        self.assertIn('\n- c-010: 어느 조각에도 들어 있지 않은 질문 글자: "전소된"\n', rerequest_of(r.proc.stdout))

    def test_real_batch2_rerequest_names_missing_pieces(self):
        r = Run(self, src=REAL2_BATCH).go(memo=REAL2_MEMO, types=REAL2_TYPES)
        self.assertEqual(r.proc.returncode, 1, r.proc.stdout)
        self.assertFalse(r.out.exists())
        re_text = rerequest_of(r.proc.stdout)
        self.assertIn('- c-013: 어느 조각에도 들어 있지 않은 질문 글자: "in"', re_text)
        self.assertIn('- c-021: 어느 조각에도 들어 있지 않은 질문 글자: "a", "that is"', re_text)
        self.assertIn('- c-022: 어느 조각에도 들어 있지 않은 질문 글자: "the"', re_text)
        # 화면 문제 목록(가로줄 밖)에는 질문의 글자가 나오지 않는다
        screen = r.proc.stdout.replace(re_text, "")
        self.assertIn("ChatGPT 답의 문제  c-021", screen)
        self.assertNotIn("that is", screen)
        self.assertNotIn('"in"', screen)

    def test_real_answer4_broken_lines_stop(self):
        bad = {
            "따옴표 없는 조각과 영어 뜻 없음": ('- "전소된" → "불태우고" · 가르기 어려움', '- founded → founded · 같은 말 · 핵심 낱말 예 · 까닭', "조각이 큰따옴표로 감싼 비지 않은 글이 아님"),
            "빈 조각과 빈 짝": ('- "전소된" → "불태우고" · 가르기 어려움', '- "" →  · 같은 말 · 핵심 낱말 예 · 까닭', "조각이 큰따옴표로 감싼 비지 않은 글이 아님"),
            "빈 짝": ('- "전소된" → "불태우고" · 가르기 어려움', '- "전소된" →  · 같은 말 · 핵심 낱말 예 · 까닭', "짝이 큰따옴표로 감싼 비지 않은 글"),
            "질문에 없는 조각": ('- "전소된" → "불태우고" · 가르기 어려움', '- "불에 탄" → "불태우고" · 바꾼 말 · 핵심 낱말 예 · 까닭', "조각이 질문에 없음"),
        }
        for name, (start, line, problem) in bad.items():
            def edit(t):
                out = []
                for l in t.split("\n"):
                    out.append(line if l.startswith(start) else l)
                return "\n".join(out)
            r = self._real_with(edit)
            self.assertEqual(r.proc.returncode, 1, name)
            self.assertIn("ChatGPT 답의 문제  c-010", r.proc.stdout, name)
            self.assertIn(problem, r.proc.stdout, name)
            self.assertFalse(r.out.exists(), name)

    def test_types_piece_not_in_question_stops(self):
        c = candidate(question="가 나")
        r = Run(self, [c]).go(types=self._memo_file('## c-001\n- "가" → "A" · 같은 말 · 핵심 낱말 예 · 까닭\n- "나" → "B" · 같은 말 · 핵심 낱말 예 · 까닭\n- "다" → 없음 · 짝 없음 · 핵심 낱말 아니오 · 까닭\n'.replace('"A"', '"A"(에이)').replace('"B"', '"B"(비)')))
        self.assertEqual(r.proc.returncode, 1, r.proc.stdout)
        self.assertIn("3번째 줄: 조각이 질문에 없음", r.proc.stdout)
        self.assertIn('- c-001: 3번째 줄의 조각이 질문에 없다: "다"', rerequest_of(r.proc.stdout))

    def test_types_english_pieces_ignore_case(self):
        c = candidate(doc="wiki-en-chuncheon", el="en", question="When Was Chuncheon founded?")
        t = ('## c-001\n- "when was"(언제였나) → 없음 · 짝 없음 · 핵심 낱말 아니오 · 까닭\n'
             '- "Chuncheon"(춘천) → "Chuncheon"(춘천) · 이름 · 핵심 낱말 아니오 · 까닭\n'
             '- "founded"(설립) → "founded"(설립) · 같은 말 · 핵심 낱말 예 · 까닭\n')
        r = Run(self, [c]).go(types=self._memo_file(t))
        self.assertEqual(r.proc.returncode, 0, r.proc.stdout)

    def test_types_required_for_english(self):
        for ctype in ("single_fact", "paraphrase"):
            for qa in ("question", "evidence"):
                c = candidate(doc="wiki-en-chuncheon", el="en", ctype=ctype)
                if qa == "question":
                    c["evidence_language"] = "ko"
                else:
                    c["question_language"] = "ko"
                r = Run(self, [c]).go(memo=self._memo_file("- c-001: 바꿈\n"))
                self.assertEqual(r.proc.returncode, 1, (ctype, qa))
                self.assertIn("--types", r.proc.stdout)
                self.assertFalse(r.out.exists())
        ok = Run(self, [candidate(doc="wiki-en-chuncheon", el="en", ctype="multi_doc")]).go()
        self.assertEqual(ok.proc.returncode, 0, ok.proc.stderr)
        ok = Run(self, [candidate(doc="wiki-en-chuncheon", el="en")]).go(types=self._memo_file(self._types_text()))
        self.assertEqual(ok.proc.returncode, 0, ok.proc.stderr)

    def test_types_optional_for_ko_ko(self):
        r = Run(self, [candidate(), candidate(cid="c-002", ctype="paraphrase")]).go(memo=self._memo_file("- c-002: 바꿈\n"))
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertNotIn("ChatGPT", r.text)

    def test_no_types_option_output_unchanged_on_real_batch(self):
        r = Run(self, src=REAL_BATCH).go(memo=REAL_MEMO)
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertNotIn("ChatGPT", r.text)
        self.assertNotIn("주의", r.proc.stdout)
        t = Run(self, src=REAL_BATCH).go(memo=REAL_MEMO, types=REAL_TYPES)
        self.assertEqual(t.proc.returncode, 0, t.proc.stderr)
        self.assertEqual(t.text.count(self.DETAILS), 6)
        self.assertNotIn("이 후보가 없다", t.text)
        for cid in ("c-001", "c-002", "c-009", "c-010", "c-011", "c-012"):
            card = [c for c in split_cards(t.text) if c.startswith(f"\n## {cid} ")][0]
            self.assertIn(self.DETAILS, card)


if __name__ == "__main__":
    unittest.main()
