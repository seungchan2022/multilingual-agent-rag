"""check_read_test.py를 시험하는 프로그램.

  uv run python src/questions/test_check_read_test.py

답 파일을 임시 폴더에 쓰고 검사 프로그램을 하위 프로세스로 실행해, 종료 코드와 출력 글자만 본다.
검사 프로그램을 불러 쓰지 않고, 올바른 답과 말뭉치 기준값은 이 파일의 코드로 따로 만든다.
"""
import copy, subprocess, sys, tempfile, unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "src" / "questions" / "check_read_test.py"
CORPUS = ROOT / "data" / "corpus"
DOC_IDS = [d["doc_id"] for d in yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]]


def lines_of(doc_id):
    """문서의 줄들. 줄 끝 공백은 뗀다."""
    return [l.rstrip() for l in (CORPUS / "markdown" / f"{doc_id}.md").read_text(encoding="utf-8").split("\n")]


def big_headings(doc_id):
    return [l for l in lines_of(doc_id) if l.startswith("## ")]


def nonempty(ls):
    return [l for l in ls if l.strip()]


def first_after(ls, i):
    rest = nonempty(ls[i + 1:])
    return rest[0] if rest else None


def correct_entry(doc_id):
    """시험 안에서 따로 만든 올바른 답 항목. 앞부분은 30글자다."""
    ls = lines_of(doc_id)
    heads = [i for i, l in enumerate(ls) if l.startswith("## ")]
    if heads:
        return {"doc_id": doc_id, "sections": [{"heading": ls[i], "next_line": first_after(ls, i)[:30]} for i in heads]}
    body = nonempty(ls)
    return {"doc_id": doc_id, "first_line": body[1][:30], "last_line": body[-1][:30]}


def correct_answer():
    return [correct_entry(d) for d in DOC_IDS]


def entry(answer, doc_id):
    return next(e for e in answer if e["doc_id"] == doc_id)


def dump(answer):
    return yaml.safe_dump(answer, allow_unicode=True, sort_keys=False, width=10000)


def run(text, tmp):
    """답 글자를 파일에 쓰고 검사 프로그램을 돌려 (종료 코드, 출력)을 돌려준다."""
    path = Path(tmp) / "answer.yaml"
    path.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, str(CHECKER), str(path)], capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


def failed_ids(output):
    return [l.split()[1] for l in output.splitlines() if l.startswith("실패  ") and len(l.split()) > 1]


class Anchors(unittest.TestCase):
    """말뭉치에 대해 사람이 확인한 값. 어긋나면 기준을 고치지 말고 알린다."""

    def test_big_heading_counts(self):
        with_heads = [d for d in DOC_IDS if big_headings(d)]
        self.assertEqual(len(with_heads), 16)
        self.assertEqual(len(DOC_IDS) - len(with_heads), 12)

    def test_andong(self):
        h = big_headings("wiki-en-andong")
        self.assertEqual(len(h), 14)
        self.assertEqual(h[-1], "## People from Andong")

    def test_jeonju(self):
        h = big_headings("wiki-en-jeonju")
        self.assertEqual(len(h), 7)
        self.assertEqual(h[-1], "## Sister cities")

    def test_cheongnamdae(self):
        self.assertEqual(big_headings("kto-ko-cheongju-cheongnamdae"), [])
        self.assertTrue(nonempty(lines_of("kto-ko-cheongju-cheongnamdae"))[-1].startswith("청남대는 대청호반에 자리 잡고"))

    def test_suwon_population(self):
        self.assertEqual(big_headings("portal-ko-suwon-population"), [])
        self.assertTrue(nonempty(lines_of("portal-ko-suwon-population"))[-1].startswith("| 영통구 | 광교2동 |"))


class CheckReadTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        self.ans = correct_answer()

    def check(self, answer_or_text):
        text = answer_or_text if isinstance(answer_or_text, str) else dump(answer_or_text)
        return run(text, self.tmp)

    def assertFailsFor(self, doc_id, answer_or_text):
        code, out = self.check(answer_or_text)
        self.assertEqual(code, 1, out)
        self.assertIn(doc_id, failed_ids(out), out)
        return out

    def sections_with_long_next(self, doc_id, need=30):
        """next_line 실제 줄이 need글자 이상인 (구역 번호, 실제 줄)을 돌려준다."""
        ls = lines_of(doc_id)
        heads = [i for i, l in enumerate(ls) if l.startswith("## ")]
        return [(k, first_after(ls, i)) for k, i in enumerate(heads) if first_after(ls, i) and len(first_after(ls, i)) >= need]

    # 1
    def test_01_correct_answer_passes(self):
        code, out = self.check(self.ans)
        self.assertEqual(code, 0, out)
        self.assertIn("문서 28개 가운데 28개 통과", out)

    # 2
    def test_02_fenced_answer_passes(self):
        text = "아래가 답입니다.\n\n```yaml\n" + dump(self.ans) + "```\n\n이상입니다. 더 필요하면 말씀하세요.\n"
        code, out = self.check(text)
        self.assertEqual(code, 0, out)
        self.assertIn("문서 28개 가운데 28개 통과", out)

    # 3
    def test_03_missing_doc(self):
        self.ans.remove(entry(self.ans, "wiki-ko-sejong"))
        self.assertFailsFor("wiki-ko-sejong", self.ans)

    # 4
    def test_04_duplicated_doc(self):
        self.ans.append(copy.deepcopy(entry(self.ans, "wiki-en-busan")))
        self.assertFailsFor("wiki-en-busan", self.ans)

    # 5
    def test_05_extra_doc(self):
        self.ans.append({"doc_id": "wiki-ko-seoul", "first_line": "가", "last_line": "나"})
        code, out = self.check(self.ans)
        self.assertEqual(code, 1, out)
        self.assertIn("wiki-ko-seoul", failed_ids(out), out)

    # 6
    def test_06_status_unread(self):
        self.ans[self.ans.index(entry(self.ans, "portal-ko-suwon-population"))] = {
            "doc_id": "portal-ko-suwon-population", "status": "읽지 못함"}
        self.assertFailsFor("portal-ko-suwon-population", self.ans)

    # 7
    def test_07_last_section_removed(self):
        entry(self.ans, "wiki-en-busan")["sections"].pop()
        self.assertFailsFor("wiki-en-busan", self.ans)

    # 8
    def test_08_first_two_sections_swapped(self):
        s = entry(self.ans, "wiki-en-andong")["sections"]
        s[0], s[1] = s[1], s[0]
        self.assertFailsFor("wiki-en-andong", self.ans)

    # 9
    def test_09_heading_one_char_changed(self):
        s = entry(self.ans, "wiki-ko-jeonju")["sections"][0]
        s["heading"] = s["heading"][:-1] + ("X" if s["heading"][-1] != "X" else "Y")
        self.assertFailsFor("wiki-ko-jeonju", self.ans)

    # 10
    def test_10_inserted_h3_section(self):
        h3 = next(l for l in lines_of("wiki-en-jeonju") if l.startswith("### "))
        s = entry(self.ans, "wiki-en-jeonju")["sections"]
        s.insert(2, {"heading": h3, "next_line": "x" * 20})
        self.assertFailsFor("wiki-en-jeonju", self.ans)

    # 11
    def test_11_next_lines_swapped(self):
        s = entry(self.ans, "wiki-en-cheonan")["sections"]
        pair = next((a, b) for a in range(len(s)) for b in range(a + 1, len(s))
                    if s[a]["next_line"][:20] != s[b]["next_line"][:20])
        a, b = pair
        s[a]["next_line"], s[b]["next_line"] = s[b]["next_line"], s[a]["next_line"]
        self.assertFailsFor("wiki-en-cheonan", self.ans)

    # 12
    def test_12_next_line_cut_to_10(self):
        doc = "wiki-en-busan"
        k, actual = self.sections_with_long_next(doc)[0]
        entry(self.ans, doc)["sections"][k]["next_line"] = actual[:10]
        self.assertFailsFor(doc, self.ans)

    # 13
    def test_13_next_line_middle_char_replaced(self):
        doc = "wiki-en-busan"
        k, actual = self.sections_with_long_next(doc)[0]
        g = actual[:30]
        g = g[:15] + ("X" if g[15] != "X" else "Y") + g[16:]
        entry(self.ans, doc)["sections"][k]["next_line"] = g
        self.assertFailsFor(doc, self.ans)

    # 14
    def test_14_next_line_not_from_beginning(self):
        doc = "wiki-en-busan"
        k, actual = self.sections_with_long_next(doc, need=35)[0]
        g = actual[5:35]
        self.assertFalse(actual.startswith(g))
        entry(self.ans, doc)["sections"][k]["next_line"] = g
        self.assertFailsFor(doc, self.ans)

    # 15
    def test_15_last_line_is_second_to_last(self):
        doc = "portal-ko-jeonju-population"
        body = nonempty(lines_of(doc))
        g = body[-2][:30]
        self.assertNotEqual(g, body[-1][:30])
        entry(self.ans, doc)["last_line"] = g
        self.assertFailsFor(doc, self.ans)

    # 16
    def test_16_first_line_is_title(self):
        doc = "kto-ko-cheongju-cheongnamdae"
        title = lines_of(doc)[0]
        self.assertTrue(title.startswith("# "))
        entry(self.ans, doc)["first_line"] = title[:30]
        self.assertFailsFor(doc, self.ans)

    # 17
    def test_17_short_lines(self):
        """실제 줄이 20글자보다 짧은 자리를 찾아, 줄 전체는 통과하고 끝 글자 하나를 뺀 것은 실패하는지 본다."""
        found = None
        for d in DOC_IDS:
            ls = lines_of(d)
            heads = [i for i, l in enumerate(ls) if l.startswith("## ")]
            if heads:
                for k, i in enumerate(heads):
                    n = first_after(ls, i)
                    if n and len(n) < 20:
                        found = (d, ("sections", k, "next_line"), n)
                        break
            else:
                body = nonempty(ls)
                for key, n in (("first_line", body[1]), ("last_line", body[-1])):
                    if len(n) < 20:
                        found = (d, (key,), n)
                        break
            if found:
                break
        if not found:
            self.skipTest("말뭉치에 20글자보다 짧은 기대 줄(큰 제목 아래 첫 줄, 첫 줄, 마지막 줄)이 없어 시험하지 못함")
        doc, where, actual = found

        def put(value):
            a = copy.deepcopy(self.ans)
            e = entry(a, doc)
            if where[0] == "sections":
                e["sections"][where[1]][where[2]] = value
            else:
                e[where[0]] = value
            return a
        code, out = self.check(put(actual))
        self.assertEqual(code, 0, out)
        self.assertFailsFor(doc, put(actual[:-1]))

    # 18
    def test_18_broken_yaml(self):
        code, out = self.check('- doc_id: wiki-en-busan\n  sections:\n    - heading: "## Hist\n')
        self.assertEqual(code, 1, out)
        self.assertIn("YAML을 읽지 못함", out)
        self.assertNotIn("Traceback", out)

    # 19
    def test_19_top_level_mapping(self):
        code, out = self.check({"documents": self.ans})
        self.assertEqual(code, 1, out)
        self.assertNotIn("Traceback", out)

    # 20
    def test_20_first_last_instead_of_sections(self):
        doc = "wiki-en-gangneung"
        self.assertTrue(big_headings(doc))
        self.ans[self.ans.index(entry(self.ans, doc))] = {"doc_id": doc, "first_line": "Gangneung is a city", "last_line": "x" * 20}
        self.assertFailsFor(doc, self.ans)


if __name__ == "__main__":
    unittest.main(verbosity=2)
