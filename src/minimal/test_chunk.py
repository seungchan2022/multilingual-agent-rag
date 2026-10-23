"""src/minimal/chunk.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

규칙(decisions/stage4.md 2026-10-22·23 줄, 지시서의 규칙 1~11)마다 작은 가짜 마크다운으로 만든 시험과,
실제 코퍼스로 만든 청크 묶음 4개를 보는 시험을 둔다. 실제 코퍼스 시험은 청크 프로그램을 임시 폴더에 두 번 돌려 쓰고,
data/minimal/chunks/에 있는 파일이 그 결과와 바이트까지 같은지도 본다. 토큰은 시험이 따로 불러온 토크나이저로 센다.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ["HF_HUB_OFFLINE"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chunk  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MARKDOWN = ROOT / "data" / "corpus" / "markdown"
QUESTIONS = ROOT / "data" / "minimal" / "questions.json"
COMMITTED = ROOT / "data" / "minimal" / "chunks"
NAMES = ["size128_notitle", "size128_title", "size256_notitle", "size256_title"]
NCT = "wiki-en-neutron-capture-therapy"

COUNT = chunk.Counter()
META = chunk.TableMeta.load()
LS = {p.stem: p.read_text(encoding="utf-8").split("\n") for p in sorted(MARKDOWN.glob("*.md"))}
EMPTY = chunk.TableMeta([])


def run(md, size, title=False, meta=EMPTY, doc_id="wiki-en-fake"):
    """가짜 마크다운 글(줄바꿈으로 끝나도 된다)을 청크로 나눈다."""
    return chunk.Chunker(COUNT, size, title).doc_chunks(doc_id, md.split("\n"), meta)


def texts(chunks):
    return [c["text"] for c in chunks]


def body(c):
    """청크 글에서 붙인 제목 줄을 뺀 글."""
    return c["text"].split("\n", 1)[1] if c["title"] else c["text"]


# ---------------------------------------------------------------- 가짜 마크다운 시험

class TestFakeUnits(unittest.TestCase):
    """규칙 1·3: 단위(정보 상자 묶음, 절 안의 문단, 표)와 문단 합치기."""

    MD = """# Doc

- Bundle A
  - a1: 1
  - a2: 2
- Bundle B
  - b1: 3

Intro one.

## Sec1

Para one. Short.

Para two.

| h1 | h2 |
|---|---|
| x | 1 |
| y | 2 |

Para three.

## Sec2

Para four.
"""

    def test_units_and_merging(self):
        out = run(self.MD, 1000)
        self.assertEqual([c["kind"] for c in out], ["infobox", "infobox", "text", "text", "table", "text", "text"])
        self.assertEqual(out[0]["text"], "- Bundle A\n  - a1: 1\n  - a2: 2")
        self.assertEqual(out[1]["text"], "- Bundle B\n  - b1: 3")
        self.assertEqual(out[2]["text"], "Intro one.")
        # 같은 절 안의 이웃 문단은 한도까지 합친다. 표와 정보 상자는 문단과 합치지 않고, 절을 넘어 합치지 않는다
        self.assertEqual(out[3]["text"], "Para one. Short.\nPara two.")
        self.assertEqual(out[4]["text"], "| h1 | h2 |\n|---|---|\n| x | 1 |\n| y | 2 |")
        self.assertEqual(out[5]["text"], "Para three.")
        self.assertEqual(out[6]["text"], "Para four.")
        self.assertEqual([c["chunk_id"] for c in out], [f"wiki-en-fake#{i:04d}" for i in range(1, 8)])

    def test_merge_up_to_limit_in_order(self):
        md = "# Doc\n\nAlpha beta gamma delta.\n\nEpsilon zeta eta theta.\n\nIota kappa lambda mu.\n"
        a, b, c = "Alpha beta gamma delta.", "Epsilon zeta eta theta.", "Iota kappa lambda mu."
        size = COUNT(a + "\n" + b)
        self.assertGreater(COUNT(a + "\n" + b + "\n" + c), size)
        self.assertEqual(texts(run(md, size)), [a + "\n" + b, c])  # 앞에서부터 차례로 채운다
        self.assertEqual(texts(run(md, COUNT(c) - 1)), [a, b, c])  # 한도를 넘는 문단은 합치지 않는다(가장 작은 단위)

    def test_oversize_paragraph_does_not_absorb_neighbors(self):
        small, big = "Tiny one.", "First long sentence is here today. Second long sentence is here today. Third long sentence is here today."
        md = f"# Doc\n\n{small}\n\n{big}\n\n{small}\n"
        size = COUNT("First long sentence is here today. Second long sentence is here today.")
        out = run(md, size)
        self.assertEqual(out[0]["text"], small)
        self.assertEqual(out[-1]["text"], small)
        self.assertTrue(all(small not in c["text"] for c in out[1:-1]))

    def test_headings_make_paths_and_scopes(self):
        md = "# Doc\n\nP0.\n\n## A\n\nP1.\n\n### B\n\nP2.\n\n#### C\n\nP3.\n\n### D\n\nP4.\n\n## E\n\nP5.\n"
        out = run(md, 1000, title=True)
        self.assertEqual([c["path"] for c in out], ["Doc", "Doc > A", "Doc > A > B", "Doc > A > B > C", "Doc > A > D", "Doc > E"])
        self.assertEqual([c["text"].split("\n")[1] for c in out], ["P0.", "P1.", "P2.", "P3.", "P4.", "P5."])  # 절마다 따로


class TestFakeInfobox(unittest.TestCase):
    """규칙 2·2-1: 정보 상자의 표 이름 줄, 묶음 나누기."""

    TABLE_BUNDLE = """# Doc

- Physical
  - density: 5
  - Vapor pressure

| P (Pa) | 1 | 10 | 100 |
|---|---|---|---|
| T (K) | 1117 | 1235 | 1381 |
| U (K) | 2117 | 2235 | 2381 |
| V (K) | 3117 | 3235 | 3381 |
- Atomic
  - Z: 69

Body.
"""

    def test_table_name_line_stays_with_table(self):
        out = run(self.TABLE_BUNDLE, 1000)
        self.assertEqual(out[0]["text"].split("\n")[:5], ["- Physical", "  - density: 5", "  - Vapor pressure",
                                                           "| P (Pa) | 1 | 10 | 100 |", "|---|---|---|---|"])
        self.assertEqual(len(out), 3)  # 묶음마다 한 청크 + 본문

    def test_split_bundle_repeats_bundle_name_and_table_name(self):
        head = "- Physical\n  - Vapor pressure\n| P (Pa) | 1 | 10 | 100 |\n|---|---|---|---|\n"
        size = COUNT(head + "| T (K) | 1117 | 1235 | 1381 |") + 3  # 표 이름 줄 + 머리글 + 행 한 개씩만 들어간다
        out = [c for c in run(self.TABLE_BUNDLE, size) if c["kind"] == "infobox" and c["line_start"] < 12]
        self.assertGreater(len(out), 2)
        self.assertEqual(out[0]["text"].split("\n")[:2], ["- Physical", "  - density: 5"])
        for c in out:
            lines = c["text"].split("\n")
            self.assertEqual(lines[0], "- Physical")
            if any(l.startswith("| ") and "(K)" in l for l in lines):
                i = lines.index("|---|---|---|---|")
                self.assertEqual(lines[i - 2:i], ["  - Vapor pressure", "| P (Pa) | 1 | 10 | 100 |"])
        rows = [l for c in out for l in c["text"].split("\n") if "(K)" in l]
        self.assertEqual(rows, ["| T (K) | 1117 | 1235 | 1381 |", "| U (K) | 2117 | 2235 | 2381 |", "| V (K) | 3117 | 3235 | 3381 |"])

    def test_bundles_are_not_merged_and_split_at_lines(self):
        md = "# Doc\n\n- A\n  - a1: x\n- B\n  - b1: y\n  - b2: z\n  - b3: w\n"
        self.assertEqual(texts(run(md, 1000)), ["- A\n  - a1: x", "- B\n  - b1: y\n  - b2: z\n  - b3: w"])
        size = COUNT("- B\n  - b1: y\n  - b2: z")
        out = run(md, size)
        self.assertEqual(texts(out), ["- A\n  - a1: x", "- B\n  - b1: y\n  - b2: z", "- B\n  - b3: w"])  # 나뉜 조각마다 묶음 이름 줄

    def test_bundle_with_name_line_only_and_end_line(self):
        md = "# Doc\n\n- Only name\n- Second\n\nBody text.\n"
        self.assertEqual(texts(run(md, 1000)), ["- Only name", "- Second", "Body text."])
        self.assertEqual(chunk.infobox_end(md.split("\n")), 4)
        self.assertIsNone(chunk.infobox_end("# Doc\n\nBody.\n".split("\n")))


class TestFakeTables(unittest.TestCase):
    """규칙 4·5: 표 나누기, 머리글 다시 붙이기, 같은 첫 칸의 행, 가장 작은 단위."""

    MD = """# Doc

| Name | Val | Unit |
|---|---|---|
| a | 1 | kg |
| b | 2 | kg |
| b | 3 | kg |
| c | 4 | kg |
| d | 5 | kg |
"""
    HEAD = "| Name | Val | Unit |\n|---|---|---|\n"

    def test_whole_table_when_fits(self):
        out = run(self.MD, 1000)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["text"], self.HEAD + "\n".join(f"| {r} |" for r in
                                                              ["a | 1 | kg", "b | 2 | kg", "b | 3 | kg", "c | 4 | kg", "d | 5 | kg"]))
        self.assertEqual(out[0]["lines"], [3, 4, 5, 6, 7, 8, 9])

    def test_split_by_rows_repeats_header(self):
        size = COUNT(self.HEAD + "| a | 1 | kg |\n| b | 2 | kg |\n| b | 3 | kg |")
        out = run(self.MD, size)
        self.assertEqual(len(out), 2)
        for c in out:
            self.assertTrue(c["text"].startswith(self.HEAD))
            self.assertLessEqual(c["tokens"], size)
        self.assertEqual(out[0]["lines"], [3, 4, 5, 6, 7])
        self.assertEqual(out[1]["lines"], [3, 4, 8, 9])

    def test_same_first_cell_rows_stay_together_if_fit(self):
        # 행 2개(a, b)까지는 들어가지만 b b 세 행은 안 들어가는 크기: b 두 행은 한 조각에 둔다
        size = COUNT(self.HEAD + "| b | 2 | kg |\n| b | 3 | kg |\n| c | 4 | kg |")
        out = run(self.MD, size)
        groups = [[l for l in c["lines"] if l > 4] for c in out]
        self.assertTrue(any({6, 7} <= set(g) for g in groups), groups)  # 6·7줄(b 두 행)이 같은 조각
        self.assertFalse(any((6 in g) != (7 in g) for g in groups))
        # 그 두 행 + 머리글이 한도를 넘으면 행 경계에서 나눈다
        size2 = COUNT(self.HEAD + "| b | 2 | kg |")
        out2 = run(self.MD, size2)
        self.assertFalse(any(6 in c["lines"] and 7 in c["lines"] for c in out2))

    def test_two_row_header_from_meta(self):
        md = "# Doc\n\n| Top | Top | X |\n|---|---|---|\n| sub1 | sub2 | sub3 |\n| a | 1 | 2 |\n| b | 3 | 4 |\n"
        meta = chunk.TableMeta([{"doc_id": "wiki-en-fake", "md_line_no": 3, "top_th_rows": 2, "caption": None}])
        head = "| Top | Top | X |\n|---|---|---|\n| sub1 | sub2 | sub3 |\n"
        size = COUNT(head + "| a | 1 | 2 |")
        out = run(md, size, meta=meta)
        self.assertEqual(len(out), 2)
        for c in out:
            self.assertTrue(c["text"].startswith(head))
        self.assertEqual(out[1]["lines"], [3, 4, 5, 7])
        # 머리글 줄 수를 모르는 표(top_th_rows 1)는 첫 줄 + 구분 줄만 머리글이다
        out1 = run(md, 1000)
        self.assertEqual(len(out1), 1)

    def test_caption_line_belongs_to_table(self):
        md = "# Doc\n\nIntro.\n\nTable 1. Caption here\n\n| h | v |\n|---|---|\n| a | 1 |\n| b | 2 |\n"
        meta = chunk.TableMeta([{"doc_id": "wiki-en-fake", "md_line_no": 7, "top_th_rows": 1, "caption": "Table 1. Caption here"}])
        out = run(md, 1000, meta=meta)
        self.assertEqual([c["kind"] for c in out], ["text", "table"])  # 표 제목 줄은 따로 문단이 되지 않는다
        self.assertEqual(out[1]["text"], "Table 1. Caption here\n| h | v |\n|---|---|\n| a | 1 |\n| b | 2 |")
        self.assertEqual(out[1]["lines"], [5, 7, 8, 9, 10])
        size = COUNT("Table 1. Caption here\n| h | v |\n|---|---|\n| a | 1 |")
        out2 = run(md, size, meta=meta)
        self.assertEqual([c["lines"] for c in out2[1:]], [[5, 7, 8, 9], [5, 7, 8, 10]])  # 조각마다 표 제목

    def test_smallest_unit_is_not_cut(self):
        out = run(self.MD, 1)
        self.assertEqual(len(out), 5)  # 행마다 한 조각(b 두 행도 한도를 넘으니 갈린다)
        for c, row in zip(out, [5, 6, 7, 8, 9]):
            self.assertEqual(c["lines"], [3, 4, row])
            self.assertTrue(c["over_limit"])

    def test_smallest_unit_text_and_infobox(self):
        md = "# Doc\n\n- B\n  - first item line\n  - second item line\n\nOne long sentence. Another long sentence.\n"
        out = run(md, 1)
        self.assertEqual(texts(out), ["- B\n  - first item line", "- B\n  - second item line", "One long sentence.", "Another long sentence."])
        self.assertTrue(all(c["over_limit"] for c in out))  # 겹침 없음: 겹친 문장 + 다음 문장이 한도를 넘으므로 넣지 않는다


class TestFakeParagraphSplit(unittest.TestCase):
    """규칙 3: 한도를 넘는 문단은 문장 경계에서 나누고 마지막 문장 하나를 다음 조각 맨 앞에 다시 넣는다."""

    S = ["The cat sat on the mat today.", "A dog ran in the park today.", "Birds sing at dawn each day.", "Fish swim in the lake now."]

    def test_overlap(self):
        md = "# Doc\n\n" + " ".join(self.S) + "\n"
        pairs = [COUNT(self.S[i] + " " + self.S[i + 1]) for i in range(3)]
        size = max(pairs)  # 문장 둘은 들어가고 셋은 안 들어가는 크기
        self.assertTrue(all(COUNT(" ".join(self.S[i:i + 3])) > size for i in range(2)))
        out = run(md, size)
        self.assertEqual(texts(out), [self.S[0] + " " + self.S[1], self.S[1] + " " + self.S[2], self.S[2] + " " + self.S[3]])
        for c in out:
            self.assertLessEqual(c["tokens"], size)
            self.assertEqual(c["lines"], [3])  # 겹친 문장도 같은 줄 번호

    def test_overlap_only_when_it_fits(self):
        long3 = "Birds sing very loudly at dawn each day in the old tall green trees by the river."
        md = "# Doc\n\n" + " ".join([self.S[0], self.S[1], long3]) + "\n"
        size = COUNT(long3) + 1
        self.assertGreater(COUNT(self.S[1] + " " + long3), size)
        self.assertGreater(COUNT(" ".join([self.S[0], self.S[1], long3])), size)
        out = run(md, size)
        self.assertEqual(texts(out), [self.S[0] + " " + self.S[1], long3])  # 겹친 문장이 들어가면 넘치므로 겹치지 않는다

    def test_every_fragment_adds_a_new_sentence(self):
        md = "# Doc\n\n" + " ".join(self.S) + "\n"
        out = run(md, 1)
        self.assertEqual(texts(out), self.S)

    def test_multiline_block_and_list_items(self):
        md = "# Doc\n\nEq one → x\nEq two → y\nEq three → z\n\n- item one. still item one.\n- item two\n"
        out = run(md, COUNT("Eq one → x\nEq two → y"))
        self.assertEqual(texts(out)[0], "Eq one → x\nEq two → y")  # 줄바꿈이 문장 경계
        self.assertIn("Eq three → z", texts(out)[1])
        # 목록 항목 줄은 문장 하나다(안에 마침표가 있어도 나누지 않는다)
        out2 = run("# Doc\n\n- item one. still item one.\n- item two\n", 1)
        self.assertEqual(texts(out2), ["- item one. still item one.", "- item two"])


class TestFakeTitleAndLines(unittest.TestCase):
    """규칙 9·11: 제목 붙임, 빈 줄 없음, 줄 번호 목록."""

    MD = "# Doc Title\n\n- Box\n  - k: v\n\nIntro text.\n\n## Sec A\n\n### Sub B\n\nBody here.\n\n| h | v |\n|---|---|\n| a | 1 |\n"

    def test_title_line(self):
        out = run(self.MD, 1000, title=True)
        self.assertEqual([c["text"].split("\n")[0] for c in out], ["Doc Title > Box", "Doc Title", "Doc Title > Sec A > Sub B", "Doc Title > Sec A > Sub B"])
        self.assertEqual([c["path"] for c in out], [c["text"].split("\n")[0] for c in out])
        plain = run(self.MD, 1000, title=False)
        self.assertEqual([c["path"] for c in plain], [c["path"] for c in out])  # 붙이지 않는 쪽에도 path는 남긴다
        for c in plain:
            self.assertFalse(c["text"].startswith(("#", "Doc Title")))
        # 붙인 제목 줄은 원문 줄이 아니라 lines에 넣지 않는다
        self.assertEqual(out[0]["lines"], [3, 4])
        self.assertEqual(out[1]["lines"], [6])
        self.assertEqual(out[3]["lines"], [14, 15, 16])

    def test_title_counts_toward_limit(self):
        md = "# Doc Title\n\n## Sec A\n\nBody one is here.\n\nBody two is here.\n"
        size = COUNT("Body one is here.\nBody two is here.")
        self.assertEqual(len(run(md, size, title=False)), 1)
        out = run(md, size, title=True)
        self.assertEqual(len(out), 2)  # 제목까지 세면 두 문단이 같이 들어가지 않는다
        for c in out:
            self.assertEqual(c["tokens"], COUNT(c["text"]))
            self.assertFalse(c["over_limit"])
        # 제목을 붙여 넘쳐도 가장 작은 단위는 자르지 않는다
        out2 = run(md, COUNT("Body one is here."), title=True)
        self.assertTrue(all(c["over_limit"] for c in out2))
        self.assertEqual([body(c) for c in out2], ["Body one is here.", "Body two is here."])

    def test_no_blank_lines_and_fields(self):
        out = run(self.MD, 1000)
        for c in out:
            self.assertNotIn("", c["text"].split("\n"))
            self.assertEqual(list(c), ["chunk_id", "doc_id", "language", "size", "title", "kind", "path", "text",
                                       "line_start", "line_end", "lines", "tokens", "over_limit"])
            self.assertEqual(c["language"], "en")
            self.assertEqual(c["lines"], sorted(set(c["lines"])))
            self.assertEqual((c["line_start"], c["line_end"]), (c["lines"][0], c["lines"][-1]))
        self.assertEqual(run("# Doc\n\nBody.\n", 100, doc_id="wiki-ko-fake")[0]["language"], "ko")

    def test_unexpected_shapes_stop(self):
        with self.assertRaises(ValueError):  # 글과 표가 빈 줄 없이 붙음
            run("# Doc\n\nText line\n| h | v |\n|---|---|\n| a | 1 |\n", 100)
        with self.assertRaises(ValueError):  # 정보 상자 표 뒤에 항목 줄
            run("# Doc\n\n- B\n  - n\n\n| h | v |\n|---|---|\n| a | 1 |\n  - after\n", 100)
        with self.assertRaises(ValueError):  # tables.json과 표 줄 번호가 다름
            run("# Doc\n\n| h | v |\n|---|---|\n| a | 1 |\n", 100,
                meta=chunk.TableMeta([{"doc_id": "wiki-en-fake", "md_line_no": 9, "top_th_rows": 1, "caption": None}]))


class TestSentences(unittest.TestCase):
    """규칙 10: 문장 경계. 소수점, 줄임말, 괄호 안 마침표를 자르지 않는다."""

    def sents(self, line):
        return [s for _, s in chunk.split_sentences(line)]

    def test_plain_english_and_korean(self):
        self.assertEqual(self.sents("It is a metal. It melts at 1925 K. Is it rare? Yes!"),
                         ["It is a metal.", "It melts at 1925 K.", "Is it rare?", "Yes!"])
        self.assertEqual(self.sents("루테튬은 금속이다. 밀도는 9.841 g/cm³이다. 다음 문장이다."),
                         ["루테튬은 금속이다.", "밀도는 9.841 g/cm³이다.", "다음 문장이다."])

    def test_decimal_and_numbers(self):
        self.assertEqual(self.sents("Density is 9.84 g/cm³ and 0.5 more. Next one."), ["Density is 9.84 g/cm³ and 0.5 more.", "Next one."])
        self.assertEqual(self.sents("Value 12.4 min. Then 3.5."), ["Value 12.4 min.", "Then 3.5."])

    def test_abbreviations(self):
        for text in ["Metals, e.g. copper and iron, conduct.", "Use a fluid, i.e. a liquid, here.", "Dr. Smith saw St. Louis.",
                     "Data from the U.S. Geological Survey.", "Albert K. Levine and H. J. Taylor wrote it.",
                     "Savolainen et al. A team of authors.", "That is, approx. 128 kg."]:
            self.assertEqual(len(self.sents(text)), 1, text)
        # 숫자 뒤의 한 글자(켈빈 K, 볼트 V)는 단위라 문장 끝이다
        self.assertEqual(self.sents("It boils below 91 K. In compounds it is +3."), ["It boils below 91 K.", "In compounds it is +3."])
        self.assertEqual(self.sents("The couple is −2.35 V. However, it varies."), ["The couple is −2.35 V.", "However, it varies."])

    def test_period_inside_parentheses(self):
        self.assertEqual(len(self.sents("It is stable (see Fig. 2. Another note). It is also hard.")), 2)
        self.assertEqual(self.sents("It is stable (see Fig. 2. Another note) and hard. Next."), ["It is stable (see Fig. 2. Another note) and hard.", "Next."])
        self.assertEqual(self.sents("(Europium has lower melting points.) This chemical matters."),
                         ["(Europium has lower melting points.)", "This chemical matters."])
        self.assertEqual(self.sents("이다. (괄호 문장이다.) 다음 문장이다."), ["이다.", "(괄호 문장이다.)", "다음 문장이다."])

    def test_lowercase_after_period_is_not_a_boundary(self):
        self.assertEqual(len(self.sents("See no. 5 and vs. the rest, etc. and so on.")), 1)

    def test_pieces_rejoin_exactly(self):
        line = "First one.  Second one (a. b). Third? Fourth!"
        self.assertEqual("".join(sep + s for sep, s in chunk.split_sentences(line)), line)


# ---------------------------------------------------------------- 실제 코퍼스 시험

TMP = None
CHUNKS = {}
TOKENIZER = None


def setUpModule():
    global TMP, TOKENIZER
    from transformers import AutoTokenizer
    TOKENIZER = AutoTokenizer.from_pretrained("BAAI/bge-m3")
    TMP = tempfile.TemporaryDirectory()
    for n in ("a", "b"):
        chunk.build_all(Path(TMP.name) / n, COUNT)
    for name in NAMES:
        CHUNKS[name] = [json.loads(l) for l in (Path(TMP.name) / "a" / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]


def tearDownModule():
    TMP.cleanup()


def infobox_region_lines(ls):
    """시험이 따로 적은 정보 상자 구간: 3줄부터 처음으로 목록·표·빈 줄이 아닌 줄 앞까지(줄 번호, 1부터)."""
    j = 3
    while j <= len(ls) and (ls[j - 1] == "" or ls[j - 1].startswith(("- ", "  - ", "|"))):
        j += 1
    return range(3, j)


def structure_lines(doc_id):
    """청크마다 다시 붙는 구조 줄의 번호: 묶음 이름 줄, 표 이름 줄, 표 제목 줄, 표 머리글 줄."""
    ls = LS[doc_id]
    s = set()
    for n in infobox_region_lines(ls):
        if ls[n - 1].startswith("- "):
            s.add(n)
        if ls[n - 1].startswith("  - ") and n + 1 <= len(ls) and ls[n] == "" and n + 2 <= len(ls) and ls[n + 1].startswith("|"):
            s.add(n)
    for (d, first), th in META.th_rows.items():
        if d != doc_id:
            continue
        if (d, first) == chunk.EXC_NAMES:
            s |= {first - 2, first, first + 1}
        elif (d, first) == chunk.EXC_ACCEL:
            s |= {first, first + 1}
        else:
            s |= set(range(first, first + 1 + max(th, 1)))
        if (d, first) in META.captions:
            s.add(first - 2)
    return s


def table_ranges(doc_id):
    """(첫 줄, 마지막 줄, 머리글 줄 번호 집합) 목록."""
    ls = LS[doc_id]
    out = []
    for (d, first), th in sorted(META.th_rows.items()):
        if d != doc_id:
            continue
        last = first
        while last < len(ls) and ls[last].startswith("|"):
            last += 1
        if (d, first) == chunk.EXC_NAMES:
            head = {first - 2, first, first + 1}
        elif (d, first) == chunk.EXC_ACCEL:
            head = {first, first + 1}
        else:
            head = set(range(first, first + 1 + max(th, 1)))
            if (d, first) in META.captions:
                head.add(first - 2)
        out.append((first, last, head))
    return out


EXCEPTION_RANGES = [(54, 68), (187, 202)]


def in_exception(c):
    return c["doc_id"] == NCT and any(a <= c["line_start"] and c["line_end"] <= b for a, b in EXCEPTION_RANGES)


class TestCorpusShape(unittest.TestCase):
    def test_four_files_and_fields(self):
        for name in NAMES:
            rows = CHUNKS[name]
            size = int(name[4:7])
            title = name.endswith("_title")
            counters = {}
            prev_doc = None
            for r in rows:
                self.assertEqual(list(r), ["chunk_id", "doc_id", "language", "size", "title", "kind", "path", "text",
                                           "line_start", "line_end", "lines", "tokens", "over_limit"])
                self.assertEqual((r["size"], r["title"]), (size, title))
                self.assertIn(r["kind"], ("infobox", "text", "table"))
                self.assertEqual(r["language"], r["doc_id"].split("-")[1])
                counters[r["doc_id"]] = counters.get(r["doc_id"], 0) + 1
                self.assertEqual(r["chunk_id"], f"{r['doc_id']}#{counters[r['doc_id']]:04d}")
                self.assertEqual(r["lines"], sorted(set(r["lines"])))
                self.assertEqual((r["line_start"], r["line_end"]), (r["lines"][0], r["lines"][-1]))
                self.assertEqual(r["tokens"], len(TOKENIZER.encode(r["text"], add_special_tokens=False)), r["chunk_id"])
                self.assertEqual(r["over_limit"], r["tokens"] > size)
                self.assertNotIn("", r["text"].split("\n"), r["chunk_id"])
                if title:
                    self.assertEqual(r["text"].split("\n")[0], r["path"])
                else:
                    self.assertFalse(r["text"].startswith("#"))
            self.assertEqual(sorted(set(r["doc_id"] for r in rows)), sorted(LS))
            docs_in_order = [r["doc_id"] for r in rows]
            self.assertEqual(docs_in_order, sorted(docs_in_order))  # 문서는 파일 이름 순

    def test_chunk_order_follows_the_document(self):
        for name in NAMES:
            last = {}
            for r in CHUNKS[name]:
                # 정보 상자(맨 앞)와 본문은 줄 번호 순서로 놓인다. 다만 정보 상자 묶음 앞의 표(en-isotopes-of-yttrium 3줄)는 앞에 온다
                self.assertGreaterEqual(r["line_start"], last.get(r["doc_id"], 0), f"{name} {r['chunk_id']}")
                last[r["doc_id"]] = r["line_start"]

    def test_title_paths(self):
        for r in CHUNKS["size256_title"]:
            title = LS[r["doc_id"]][0][2:]
            self.assertEqual(r["path"].split(" > ")[0], title)
            if r["kind"] == "infobox":
                first = LS[r["doc_id"]][r["line_start"] - 1]
                self.assertEqual(r["path"], f"{title} > {first[2:]}")
        sample = [r for r in CHUNKS["size256_title"] if r["doc_id"] == NCT and r["kind"] == "text" and r["line_start"] == 14][0]
        self.assertEqual(sample["path"], "Neutron capture therapy of cancer > Boron neutron capture therapy > History")
        intro = [r for r in CHUNKS["size256_title"] if r["doc_id"] == NCT and r["line_start"] == 6][0]
        self.assertEqual(intro["path"], "Neutron capture therapy of cancer")  # 머리말 절은 문서 제목만


class TestCorpusLines(unittest.TestCase):
    def test_each_line_text_is_in_the_chunk(self):
        for name in NAMES:
            for r in CHUNKS[name]:
                if in_exception(r):
                    continue
                ls = LS[r["doc_id"]]
                pieces = body(r).split("\n")
                self.assertEqual(len(pieces), len(r["lines"]), r["chunk_id"])  # 청크 글의 줄 하나가 원문 줄 하나
                for piece, n in zip(pieces, r["lines"]):
                    line = ls[n - 1].strip()
                    self.assertTrue(line, f"{r['chunk_id']} 빈 줄 {n}")
                    if line in r["text"]:
                        self.assertEqual(piece.strip(), line, r["chunk_id"])
                    else:  # 예외 (가): 문장 경계에서 나뉜 글 조각은 원문 줄의 일부만 담는다
                        self.assertEqual(r["kind"], "text", f"{r['chunk_id']} 줄 {n}")
                        self.assertIn(piece, line, r["chunk_id"])
                self.assertEqual(len(set(r["lines"])), len(r["lines"]))

    def test_no_line_is_missing(self):
        for name in NAMES:
            covered = {}
            for r in CHUNKS[name]:
                covered.setdefault(r["doc_id"], set()).update(r["lines"])
            for doc_id, ls in LS.items():
                want = {i + 1 for i, l in enumerate(ls) if l.strip() and not l.startswith("#")}
                self.assertEqual(want - covered[doc_id], set(), f"{name} {doc_id} 빠진 줄")
                self.assertEqual(covered[doc_id] - want, set(), f"{name} {doc_id} 원문에 없는 줄")

    def test_tables_always_carry_their_header(self):
        for name in NAMES:
            for r in CHUNKS[name]:
                for first, last, head in table_ranges(r["doc_id"]):
                    rows = set(r["lines"]) & set(range(first, last + 1)) - head
                    if rows or (set(r["lines"]) & head):
                        self.assertLessEqual(head, set(r["lines"]), f"{r['chunk_id']} 머리글이 빠짐")
                if r["kind"] == "infobox":
                    self.assertTrue(LS[r["doc_id"]][r["line_start"] - 1].startswith("- "), r["chunk_id"])  # 묶음 이름 줄이 맨 위

    def test_over_limit_chunks_hold_one_smallest_unit(self):
        total = 0
        for name in NAMES:
            for r in CHUNKS[name]:
                if not r["over_limit"]:
                    continue
                total += 1
                struct = structure_lines(r["doc_id"])
                pieces = body(r).split("\n")
                if r["doc_id"] == NCT and set(r["lines"]) & {54}:  # 표 예외 1: 표 제목 + 이름 하나
                    self.assertEqual(len(pieces), 2)
                    continue
                content = [n for n in r["lines"] if n not in struct]
                self.assertEqual(len(content), 1, f"{name} {r['chunk_id']} {r['lines']}")
                if r["kind"] == "text":
                    self.assertEqual(len(pieces), 1)  # 겹침 없음, 문장 하나
                    sents = chunk.split_sentences(pieces[0])
                    self.assertTrue(chunk.is_item_line(pieces[0]) or len(sents) == 1, r["chunk_id"])
        self.assertGreater(total, 100)

    def test_smaller_size_never_has_fewer_chunks(self):
        self.assertGreater(len(CHUNKS["size128_notitle"]), len(CHUNKS["size256_notitle"]))
        self.assertGreater(len(CHUNKS["size128_title"]), len(CHUNKS["size256_title"]))

    def test_infobox_end_lines(self):
        ends = {d: chunk.infobox_end(ls) for d, ls in LS.items()}
        self.assertEqual(ends["wiki-ko-lutetium"], 59)
        self.assertEqual(ends["wiki-en-thulium"], 66)
        self.assertEqual(ends[NCT], 4)
        self.assertEqual(ends["wiki-en-isotopes-of-yttrium"], 13)
        for d in ("wiki-ko-isotopes-of-terbium", "wiki-ko-isotopes-of-neodymium", "wiki-ko-isotopes-of-yttrium", "wiki-en-samarium-cobalt-magnet"):
            self.assertIsNone(ends[d])


class TestCorpusRules(unittest.TestCase):
    def test_table_list_matches_tables_json(self):
        self.assertEqual(sum(len(v) for v in META.starts.values()), 37)
        two = {(d, n) for (d, n), th in META.th_rows.items() if th == 2}
        self.assertEqual(two, {("wiki-en-thulium", 59), ("wiki-en-dysprosium", 60), ("wiki-en-ytterbium", 60), ("wiki-en-lutetium", 59),
                               ("wiki-ko-isotopes-of-yttrium", 9), ("wiki-en-isotopes-of-yttrium", 3), ("wiki-en-isotopes-of-yttrium", 23),
                               ("wiki-ko-isotopes-of-terbium", 9), ("wiki-ko-isotopes-of-neodymium", 11), ("wiki-en-lanthanum", 60),
                               ("wiki-en-europium", 58), ("wiki-en-praseodymium", 59)})
        self.assertEqual(sorted(META.captions), [(NCT, 56), (NCT, 141), ("wiki-en-samarium-cobalt-magnet", 22)])
        for doc_id, ls in LS.items():  # 마크다운에서 센 표 덩어리의 첫 줄이 모두 tables.json과 맞는다
            starts = {i + 1 for i, l in enumerate(ls) if l.startswith("|") and (i == 0 or not ls[i - 1].startswith("|"))}
            self.assertEqual(starts, META.starts.get(doc_id, set()), doc_id)

    def test_terbium_128_tables_carry_lines_9_to_11(self):
        for name in ("size128_notitle", "size128_title"):
            tab = [r for r in CHUNKS[name] if r["doc_id"] == "wiki-ko-isotopes-of-terbium" and r["kind"] == "table"]
            self.assertGreater(len(tab), 50)
            for r in tab:
                self.assertLessEqual({9, 10, 11}, set(r["lines"]), r["chunk_id"])
                self.assertEqual(len(r["lines"]), 4, r["chunk_id"])  # 머리글 + 행 하나
                self.assertTrue(r["over_limit"])
        # ¹⁴⁴ᵐ¹Tb 세 행(31~33줄)은 머리글과 334토큰이라 256에서도 갈린다
        for name in ("size256_notitle", "size256_title"):
            hit = [r for r in CHUNKS[name] if r["doc_id"] == "wiki-ko-isotopes-of-terbium" and set(r["lines"]) & {31, 32, 33}]
            self.assertEqual(sorted(sum((r["lines"][3:] for r in hit), [])), [31, 32, 33])
            self.assertGreater(len(hit), 1)
        # 같은 첫 칸의 이어진 행은 머리글과 함께 한도(256) 안에 들 때 한 조각에 둔다. 넘으면 갈린다(¹³⁸Tb 두 행은 머리글과 257토큰)
        ls = LS["wiki-ko-isotopes-of-terbium"]
        tab = [r for r in CHUNKS["size256_notitle"] if r["doc_id"] == "wiki-ko-isotopes-of-terbium" and r["kind"] == "table"]
        head = "\n".join(ls[8:11])
        kept = split = 0
        k = 12
        while k <= 98:
            if not ls[k - 1].startswith("|"):
                break
            first = ls[k - 1].split("|")[1]
            j = k
            while j + 1 <= 98 and ls[j].startswith("|") and ls[j].split("|")[1] == first:
                j += 1
            if j > k:
                fits = COUNT(head + "\n" + "\n".join(ls[k - 1:j])) <= 256
                together = any({k, j} <= set(r["lines"]) for r in tab)
                self.assertEqual(together, fits, f"{k}~{j}줄")
                kept += fits
                split += not fits
            k = j + 1
        self.assertGreater(kept, 0)
        self.assertGreater(split, 0)

    def test_exception_1_names_table(self):
        ls = LS[NCT]
        rows = [[c.strip() for c in ls[k - 1].strip()[1:-1].split("|")] for k in [56] + list(range(58, 69))]
        left = [(r[0], k) for r, k in zip(rows, [56] + list(range(58, 69))) if r[0]]
        right = [(r[1], k) for r, k in zip(rows, [56] + list(range(58, 69))) if r[1]]
        want = left + right
        self.assertEqual(len(want), 23)
        for name in NAMES:
            ex = [r for r in CHUNKS[name] if r["doc_id"] == NCT and r["line_end"] <= 68 and r["line_start"] >= 54 and r["kind"] == "table"]
            got = []
            for r in ex:
                self.assertLessEqual({54, 56, 57}, set(r["lines"]))
                pieces = body(r).split("\n")
                self.assertEqual(pieces[0], ls[53].strip())  # 조각마다 표 제목
                for p in pieces[1:]:
                    self.assertNotIn("|", p)
                got += pieces[1:]
            self.assertEqual(got, [n for n, _ in want], name)
            if len(ex) == 1:
                self.assertEqual(ex[0]["lines"], [54] + list(range(56, 69)))
            for r in ex:  # 조각의 lines = 표 제목, 머리글·구분 줄, 그 조각의 이름이 나온 표 줄
                names = body(r).split("\n")[1:]
                lines = {k for n, k in want if n in names} | {54, 56, 57}
                self.assertEqual(set(r["lines"]), lines)

    def test_exception_2_accelerator_table(self):
        ls = LS[NCT]

        def cells(s):
            return [c.strip() for c in s.strip()[1:-1].split("|")]
        head = ["Manufacturer", "Product", "Reaction", "Accelerator type", "Host institution", "First clinical use", "Status"]
        for name in NAMES:
            ex = [r for r in CHUNKS[name] if r["doc_id"] == NCT and r["line_start"] >= 187 and r["kind"] == "table"]
            rows_seen = []
            for r in ex:
                self.assertEqual(r["lines"][:2], [187, 188])
                pieces = body(r).split("\n")
                self.assertEqual(cells(pieces[0]), head)
                self.assertEqual(pieces[1], "|---|---|---|---|---|---|---|")
                for p, n in zip(pieces[2:], r["lines"][2:]):
                    c = cells(p)
                    md = cells(ls[n - 1])
                    self.assertEqual(len(c), 7)
                    self.assertEqual(" ".join(x for x in c[:4] if x), md[0], n)  # 네 조각을 이으면 마크다운 첫 칸
                    self.assertEqual(c[4:], md[1:], n)
                    rows_seen.append(n)
            self.assertEqual(rows_seen, list(range(189, 203)), name)
            if len(ex) == 1:
                self.assertEqual(ex[0]["lines"], list(range(187, 203)))
        # 원본의 네 조각을 이은 글이 다르면 멈춘다. 조각이 셋이면 제품 칸이 빈다
        with self.assertRaises(ValueError):
            chunk.split_four(["A", "B", "C", "D"], "A B C X")
        self.assertEqual(chunk.split_four(["A", "C", "D"], "A C D"), ["A", "", "C", "D"])
        self.assertEqual(chunk.split_four(["A", "B", "C", "D"], "A B C D"), ["A", "B", "C", "D"])
        # 원본 HTML 칸에서 읽은 14행이 마크다운 값 행 14개와 맞다(위첨자 변환 포함)
        _, seg_rows = chunk.accel_first_cells()
        self.assertEqual(len(seg_rows), 14)
        self.assertEqual(seg_rows[0], ["Sumitomo Heavy Industries", "NeuCure", "⁹Be(p,n)⁹B", "Cyclotron"])
        self.assertEqual(seg_rows[4], ["Cancer Intelligence Care Systems", "⁷Li(p,n)⁷Be", "RFQ"])

    def test_corpus_files_are_untouched_by_exceptions(self):
        # 예외 1·2는 청크 글만 바꾼다: 코퍼스 마크다운의 해당 줄은 그대로 남아 있다
        ls = LS[NCT]
        self.assertTrue(ls[55].startswith("| Boric acid | Boronated unnatural amino acids |"))
        self.assertTrue(ls[186].startswith("| Manufacturer Product Reaction Accelerator type | Host institution |"))


class TestCorpusEvidence(unittest.TestCase):
    def test_every_evidence_is_retrievable_in_all_four(self):
        qs = json.loads(QUESTIONS.read_text(encoding="utf-8"))
        evidence = [e for q in qs for e in q["evidence"]]
        self.assertEqual(len(evidence), 64)
        for name in NAMES:
            for e in evidence:
                hit = [r for r in CHUNKS[name] if r["doc_id"] == e["doc_id"] and e["line"] in r["lines"] and e["value_text"] in r["text"]]
                self.assertTrue(hit, f"{name} {e['doc_id']}:{e['line']} {e['value_text']}")


class TestDeterminism(unittest.TestCase):
    def test_two_runs_give_the_same_bytes(self):
        for name in NAMES:
            a = (Path(TMP.name) / "a" / f"{name}.jsonl").read_bytes()
            b = (Path(TMP.name) / "b" / f"{name}.jsonl").read_bytes()
            self.assertEqual(a, b, name)
            self.assertTrue(a.endswith(b"\n"))
            self.assertNotIn(b"\r", a)

    def test_committed_files_match_a_fresh_run(self):
        for name in NAMES:
            fresh = (Path(TMP.name) / "a" / f"{name}.jsonl").read_bytes()
            self.assertTrue((COMMITTED / f"{name}.jsonl").is_file(), f"{name}.jsonl이 data/minimal/chunks/에 없음")
            self.assertEqual((COMMITTED / f"{name}.jsonl").read_bytes(), fresh, f"{name}.jsonl이 프로그램 결과와 다름. chunk.py를 다시 돌린다")
        self.assertEqual(sorted(p.name for p in COMMITTED.iterdir()), sorted(f"{n}.jsonl" for n in NAMES))


if __name__ == "__main__":
    unittest.main()
