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

    def go(self, memo=None):
        cmd = [sys.executable, str(PROGRAM), str(self.src), str(self.out)] + (["--memo", str(memo)] if memo else [])
        self.proc = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
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
        self.assertIn("- `term`(찾을 말) `1969`:", i5)
        self.assertIn("걸린 곳 1: [wiki-en-chuncheon.md", i5)
        self.assertIn(f" · 원문 주소(앞뒤 문맥을 볼 때): {URLS['wiki-en-chuncheon']}", i5)
        self.assertIn(f"    > {hit}", i5)
        self.assertIn("Gemini의 판단: 같은 사실 아님 — 기온 날짜", i5)
        self.assertIn("- `passage`(근거 구절):", t)
        self.assertIn("  - 사실 1의 근거 1: [wiki-ko-chuncheon.md", t)

    def test_kto_document_shows_no_api_url(self):
        ex = "Samaksan Mountain Lake Cable Car is the longest cable car in Korea"
        oc = [{"term": "longest cable car", "hits": [{"doc_id": "kto-en-chuncheon-samaksan-cable-car", "excerpt": ex, "same_fact": False, "why": "시험"}]}]
        r = Run(self, [candidate(oc=oc)]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
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

    def test_en_evidence_same_city_docs_are_korean(self):
        r = Run(self, [candidate(doc="wiki-en-jeonju", el="en")]).go()
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
        raw = "- id: c-001\n  question: q\n  question_language: ko\n  evidence_language: ko\n  type: single_fact\n  answer: a\n  required_facts:\n    - fact: f\n      evidence: []\n  opposite_check:\n    - term: 1969\n      hits: []\n"
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))
        src = tmp / "b.yaml"
        src.write_text(raw, encoding="utf-8")
        r = Run(self, src=src).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        self.assertIn("`1969`: 영어 문서 어디에도 없다", item_text(r.text, 5))

    def test_no_hits_at_all(self):
        oc = [{"term": "alpha", "hits": []}, {"term": "beta", "hits": []}]
        r = Run(self, [candidate(oc=oc)]).go()
        i5 = item_text(r.text, 5)
        self.assertIn("Gemini가 찾은 말 `alpha`, `beta`: 영어 문서 어디에도 없다(검사 프로그램이 확인함). 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.", i5)
        self.assertIn("읽을 것이 없으니", i5)
        self.assertIn("- Gemini가 찾은 말: `alpha`, `beta`", item_text(r.text, 6))

    def test_numbers_from_answer_in_item3(self):
        c = candidate()
        c["answer"] = "1,234명과 12.5%, 1969년"
        r = Run(self, [c]).go()
        self.assertIn("정답과 근거 구절에서 뽑은 숫자: `1,234`, `12.5`, `1969`", item_text(r.text, 3))
        r2 = Run(self, [candidate()]).go()
        self.assertIn("정답과 근거 구절에서 뽑은 숫자:", item_text(r2.text, 3))

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
        r = Run(self, [candidate(oc=[{"term": "x", "hits": []}])]).go()
        details = r.text.split("<details>")[1].split("</details>")[0]
        self.assertIn("opposite_check:", details)
        self.assertIn("```yaml", details)

    def test_labels_appear_in_candidate_block_first(self):
        hit = "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969)"
        oc = [{"term": "1969", "hits": [{"doc_id": "wiki-en-chuncheon", "excerpt": hit, "same_fact": False, "why": "기온 날짜"}]}]
        r = Run(self, [candidate(oc=oc), candidate(cid="c-002", doc="wiki-en-jeonju", el="en", oc=oc)]).go()
        self.assertEqual(r.proc.returncode, 0, r.proc.stderr)
        cards = split_cards(r.text)
        self.assertEqual(len(cards), 2)
        for card in cards:
            check_labels(self, card)

    def slc(self, el, doc, terms):
        """same_language_check 시험 후보: terms는 [(term, [doc_id,...])]. 걸린 곳 글은 각 문서의 산문 줄."""
        sc = [{"term": t, "hits": [{"doc_id": d, "excerpt": prose(d)[0], "same_fact": False, "why": "시험 이유"} for d in ds]}
              for t, ds in terms]
        c = candidate(doc=doc, el=el)
        c["same_language_check"] = sc
        return c

    def test_same_language_hits_split_between_item3_and_item4(self):
        c = self.slc("ko", "wiki-ko-chuncheon", [("가", ["wiki-ko-chuncheon", "wiki-ko-jeonju"]), ("나", ["wiki-ko-jeonju"]), ("다", [])])
        t = Run(self, [c]).go().text
        i3, i4 = item_text(t, 3), item_text(t, 4)
        e, o = prose("wiki-ko-chuncheon")[0], prose("wiki-ko-jeonju")[0]
        self.assertIn(f"    > {e}", i3)
        self.assertNotIn(o, i3)
        self.assertIn(f"    > {o}", i4)
        self.assertNotIn(e, i4)
        self.assertIn("- `term`(찾을 말) `가`:", i3)
        self.assertNotIn("`나`:", i3)
        self.assertIn("찾을 말 `나`, `다`: 근거 문서 안에서는 걸린 곳이 없다", i3)
        self.assertIn("Gemini의 판단: 같은 것 아님 — 시험 이유", i3)
        self.assertIn("걸린 곳 1: [wiki-ko-jeonju.md", i4)
        self.assertLess(i4.index("Cmd+Shift+F"), i4.index("Gemini가"))
        self.assertIn("3번의 찾을 말로 찾는다.", i4)
        self.assertIn("Cmd+클릭", i3)
        self.assertNotIn("번역", i3 + i4)

    def test_item5_unchanged_by_same_language_check(self):
        hit = "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969)"
        oc = [{"term": "1969", "hits": [{"doc_id": "wiki-en-chuncheon", "excerpt": hit, "same_fact": False, "why": "기온 날짜"}]}]
        plain = candidate(oc=oc)
        with_slc = self.slc("ko", "wiki-ko-chuncheon", [("가", ["wiki-ko-chuncheon"])])
        with_slc["opposite_check"], with_slc["required_facts"] = oc, plain["required_facts"]
        a = item_text(Run(self, [plain]).go().text, 5)
        b = item_text(Run(self, [with_slc]).go().text, 5)
        self.assertEqual(a, b)
        self.assertIn("Gemini의 판단: 같은 사실 아님 — 기온 날짜", a)

    def test_en_evidence_item3_and_item4_use_translation(self):
        c = self.slc("en", "wiki-en-jeonju", [("가", ["wiki-en-jeonju"]), ("나", ["kto-en-jeonju-hanok-village"])])
        t = Run(self, [c]).go().text
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
        c = self.slc("en", kto, [])
        i3 = item_text(Run(self, [c]).go().text, 3)
        self.assertIn("내용 전체를 번역기에 붙여 읽는다", i3)

    def test_ko_evidence_wording_unchanged_without_field(self):
        t = Run(self, [candidate()]).go().text
        i3, i4 = item_text(t, 3), item_text(t, 4)
        self.assertNotIn("Gemini", i3 + i4)
        self.assertIn("- 할 일: 위 근거 문서 링크를 `Cmd+클릭`해 열고", i3)
        self.assertTrue(i4.split("\n", 1)[1].startswith("- 할 일: `Cmd+Shift+F`"))
        self.assertIn("3번의 찾을 말로 찾는다.\n", i4)

    def test_no_field_means_no_gemini_block_en(self):
        t = Run(self, [candidate(doc="wiki-en-jeonju", el="en")]).go().text
        self.assertNotIn("검사 프로그램이 확인함", item_text(t, 3) + item_text(t, 4))

    def test_field_without_hits_in_group_says_not_found(self):
        c = self.slc("ko", "wiki-ko-chuncheon", [("가", ["wiki-ko-jeonju"]), ("나", [])])
        t = Run(self, [c]).go().text
        i3, i4 = item_text(t, 3), item_text(t, 4)
        self.assertIn("- Gemini가 찾은 말 `가`, `나`: 근거 문서 안에서는 걸린 곳이 없다(검사 프로그램이 확인함). 위 직접 찾기는 그대로 해야 한다.", i3)
        self.assertNotIn("`term`", i3)
        self.assertIn("`term`(찾을 말) `가`:", i4)
        c2 = self.slc("ko", "wiki-ko-chuncheon", [("가", ["wiki-ko-chuncheon"])])
        i4b = item_text(Run(self, [c2]).go().text, 4)
        self.assertIn("- Gemini가 찾은 말 `가`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다(검사 프로그램이 확인함). 위 직접 찾기는 그대로 해야 한다.", i4b)
        self.assertNotIn("`[x]`", i4b)

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
        hit = "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969)"
        oc = [{"term": "1969", "hits": [{"doc_id": "wiki-en-chuncheon", "excerpt": hit, "same_fact": False, "why": "시험"}]}]
        t = Run(self, [candidate(oc=oc)]).go().text
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


if __name__ == "__main__":
    unittest.main()
