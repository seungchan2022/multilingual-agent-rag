"""make_result_page.py 시험. 가짜 폴더를 만들어 쓰고 실제 결과는 건드리지 않는다."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_result_page as m

QIDS = [f"q-{i:02d}" for i in range(10)]


def questions():
    return [{"id": i, "kind": "값", "question": f"질문 {i} <b>", "answer": "1 kg", "value": 1.0} for i in QIDS]


def grade(correct, multi=False):
    return {"answer_key": "1 kg", "value": 1.0, "numbers": [1.0, 2.0] if multi else [1.0],
            "picked": 1.0 if correct else 5.0, "diff_pct": 0.0, "multi": multi, "correct": correct}


def gen(ans="1"):
    return {"text": "{}", "parsed": {"reason": "이유 <x>", "answer": ans}, "seconds": 1, "gen_tokens": 1}


def simple(cond, qid, seed, correct, multi=False):
    return {"cond": cond, "id": qid, "seed": seed, "kind": "값", "gen": gen(), "final_answer": "1",
            "correct": correct, "grade": grade(correct, multi)}


def counts_rows(cond, per_q):
    """per_q[i]는 질문 i에서 맞은 횟수. 씨앗 1..10."""
    return [simple(cond, qid, s, s <= per_q[i]) for i, qid in enumerate(QIDS) for s in range(1, 11)]


def refine_row(qid, seed, d_ok, passed, f_ok, error=False, judge_null=False):
    judge = {"text": "", "parsed": None if judge_null else {"issues": ["문제 <i>"], "pass": passed,
                                                           "revision_instruction": "고쳐라"}, "seconds": 1, "gen_tokens": 1}
    if error:
        judge["error"] = "HTTP 500"
    rd = {"round": 1, "draft": gen(), "draft_answer": "1", "draft_correct": d_ok, "draft_grade": grade(d_ok),
          "judge": judge, "passed": passed}
    return {"cond": "refine", "id": qid, "seed": seed, "kind": "값", "rounds": [rd],
            "final_answer": "1", "correct": f_ok, "grade": grade(f_ok)}


def write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def make_tree(root, topics):
    """topics: {폴더: {'A': 행들, 'B': 행들, 'C': 행들}}. 도시 폴더는 비워 둔다."""
    for folder in ("chem", "solar", "mineral", "city_v1"):
        (root / folder).mkdir(parents=True, exist_ok=True)
        write_q = json.dumps(questions(), ensure_ascii=False)
        (root / folder / "questions.json").write_text(write_q, encoding="utf-8")
    for folder, d in topics.items():
        for key, name in (("A", "base"), ("B", "refine"), ("C", "context")):
            if key in d:
                write(root / folder / "results" / f"{name}.jsonl", d[key])
    links = {"chem": {"a": "A"}, "solar": {"b": None}, "mineral": {"c": "C"}}
    (root / "criterion4_langlinks.json").write_text(json.dumps(links), encoding="utf-8")


def build(topics):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    make_tree(root, topics)
    out, _ = m.build(root, root / "out.html")
    return tmp, out.read_text(encoding="utf-8")


def row_of(page, name):
    """요약 표에서 이름으로 시작하는 줄의 칸 글자 목록."""
    for tr in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        cells = re.findall(r"<td>(.*?)</td>", tr, re.S)
        if cells and cells[0] == name:
            return cells
    raise AssertionError(name)


class Tests(unittest.TestCase):
    def test_counts_and_pass(self):
        # 맞은 답 = 6+5+10+0+3+3+3+3+3+4 = 40, 통과 문제 = 6과 10 두 개
        pq = [6, 5, 10, 0, 3, 3, 3, 3, 3, 4]
        tmp, page = build({"chem": {"A": counts_rows("base", pq)}})
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "화학 원소")
        self.assertIn("40/100 · 통과 2/10", cells[1])
        s = m.score(counts_rows("base", pq), questions())
        self.assertEqual((s["ok"], s["n"], s["passed"]), (40, 100, 2))

    def test_criterion1_boundaries(self):
        for a, expect in ((20, "✓"), (40, "✓"), (41, "✗"), (19, "✗")):
            pq = [a // 10 + (1 if i < a % 10 else 0) for i in range(10)]
            tmp, page = build({"chem": {"A": counts_rows("base", pq)}})
            self.addCleanup(tmp.cleanup)
            self.assertTrue(row_of(page, "화학 원소")[6].startswith(expect), (a, row_of(page, "화학 원소")[6]))

    def test_criterion3_boundaries(self):
        a = [2] * 10  # A = 20
        for c_total, expect in ((60, "✓"), (59, "✗")):
            pq = [c_total // 10 + (1 if i < c_total % 10 else 0) for i in range(10)]
            tmp, page = build({"chem": {"A": counts_rows("base", a), "C": counts_rows("context", pq)}})
            self.addCleanup(tmp.cleanup)
            self.assertTrue(row_of(page, "화학 원소")[8].startswith(expect), (c_total, row_of(page, "화학 원소")[8]))

    def test_criterion2_never_judged(self):
        a = [2] * 10
        b = [refine_row(q, s, True, True, True) for q in QIDS for s in range(1, 11)]
        tmp, page = build({"chem": {"A": counts_rows("base", a), "B": b, "C": counts_rows("context", [10] * 10)}})
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "화학 원소")
        self.assertEqual(cells[7], "v2를 잰 뒤 판정")
        self.assertEqual(cells[4], "+80")  # B-v1 − A는 참고 숫자로만 나온다

    def test_criterion4(self):
        tmp, page = build({})
        self.addCleanup(tmp.cleanup)
        self.assertTrue(row_of(page, "화학 원소")[9].startswith("✓"))
        self.assertTrue(row_of(page, "태양계 천체")[9].startswith("✗"))

    def test_incomplete_topic(self):
        tmp, page = build({"solar": {"A": counts_rows("base", [10] * 10)[:50]}})
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "태양계 천체")
        self.assertIn("(진행 중)", cells[1])
        self.assertEqual(cells[6], "아직")
        self.assertEqual(cells[8], "아직")
        self.assertEqual(cells[2], "아직 없음")
        self.assertEqual(cells[4], "아직")
        self.assertEqual(row_of(page, "광물")[1], "아직 없음")

    def test_judgement_counts(self):
        rows = []
        spec = [(True, True, True, 4), (True, False, False, 3), (False, True, False, 2),
                (False, False, True, 5), (False, False, False, 6)]
        i = 0
        for d_ok, passed, f_ok, n in spec:
            for _ in range(n):
                rows.append(refine_row(QIDS[i // 10], i % 10 + 1, d_ok, passed, f_ok))
                i += 1
        rows.append(refine_row(QIDS[9], 9, True, False, True, error=True))
        rows.append(refine_row(QIDS[9], 10, True, False, True, judge_null=True))
        j = m.judgement(rows)
        self.assertEqual((j["맞음_통과"], j["맞음_불통과"], j["틀림_통과"], j["틀림_불통과"]), (4, 3 + 2, 2, 5 + 6))
        self.assertEqual(j["고쳐짐"], 5)  # 처음 틀림 → 최종 맞음
        self.assertEqual(j["망가짐"], 3)  # 처음 맞음 → 최종 틀림
        self.assertEqual(j["서버오류"], 1)
        self.assertEqual(j["judge_null"], 1)

    def test_multi_list(self):
        a = counts_rows("base", [5] * 10)
        a[3] = simple("base", a[3]["id"], a[3]["seed"], False, multi=True)
        tmp, page = build({"chem": {"A": a}})
        self.addCleanup(tmp.cleanup)
        self.assertIn(f"<td>{a[3]['id']}</td>", page)
        self.assertEqual(len(m.multi_rows({"A": a, "B": [], "C": []})), 1)

    def test_html_escaped_and_details(self):
        tmp, page = build({"chem": {"A": counts_rows("base", [5] * 10), "B": [refine_row(QIDS[0], 1, False, False, True)]}})
        self.addCleanup(tmp.cleanup)
        self.assertNotIn("<b>", page.replace("<b>최종 답</b>", ""))
        self.assertIn("질문 q-00 &lt;b&gt;", page)
        self.assertIn("<details>", page)
        self.assertNotIn("<details open", page)

    def test_readability_parts(self):
        b = refine_row(QIDS[0], 1, False, False, True)
        b["rounds"][0]["draft"]["parsed"]["note"] = "덤 <n>"  # 정해지지 않은 키
        del b["rounds"][0]["judge"]["parsed"]["revision_instruction"]  # 빠진 키
        qs = questions()
        qs[0].update({"steps": ["단계 <1>"], "evidence_quotes": [{"doc": "문서", "quote": "글 <q>"}]})
        tmp, root = tempfile.TemporaryDirectory(), None
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        make_tree(root, {"chem": {"A": counts_rows("base", [5] * 10), "B": [b]}})
        (root / "chem" / "questions.json").write_text(json.dumps(qs, ensure_ascii=False), encoding="utf-8")
        page = m.build(root, root / "o.html")[0].read_text(encoding="utf-8")
        self.assertIn("읽는 법", page)
        self.assertIn("p-fix", page)  # 처음 틀림 → 최종 맞음
        self.assertIn("고쳐짐 1 · 망가짐 0", page)
        self.assertIn("단계 &lt;1&gt;", page)
        self.assertIn("[문서] 글 &lt;q&gt;", page)
        self.assertIn("1회차에서 끝남", page)
        self.assertIn("원문 JSON 보기", page)
        self.assertIn('<code class="key">answer</code>', page)
        self.assertIn("정해지지 않은 칸: <code", page)
        self.assertIn("칸이 없음", page)
        self.assertNotIn("prefers-color-scheme: dark", page)

    def test_unparsed_output(self):
        html_ = m.gen_block({"text": "깨짐 <x>", "parsed": None}, False, None)
        self.assertIn("JSON으로 읽지 못함", html_)
        self.assertIn("깨짐 &lt;x&gt;", html_)

    def test_multi_sentence(self):
        s = m.grade_sentence(grade(True, multi=True))
        self.assertIn("마지막 숫자", s)
        self.assertIn("정답 1 kg와", s)


if __name__ == "__main__":
    unittest.main()
