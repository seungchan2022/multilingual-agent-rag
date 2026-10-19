"""make_result_page.py 시험. 가짜 폴더를 만들어 쓰고 실제 결과는 건드리지 않는다."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import make_result_page as m
import run

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


def error_row(folder, cond, row, labels):
    return {"topic": folder, "cond": cond, "id": row["id"], "seed": row["seed"], "labels": labels}


def make_tree(root, topics, errors=None):
    """topics: {폴더: {'A': 행들, 'B': 행들, 'C': 행들}}. 도시 폴더는 비워 둔다.
    errors: 오류 유형 줄 목록. None이면 틀린 A, C 답마다 '재료 값이 틀림'을 붙인다. False면 파일을 만들지 않는다."""
    for folder in ("chem", "solar", "mineral", "city_v1"):
        (root / folder).mkdir(parents=True, exist_ok=True)
        write_q = json.dumps(questions(), ensure_ascii=False)
        (root / folder / "questions.json").write_text(write_q, encoding="utf-8")
    for folder, d in topics.items():
        for key, name in (("A", "base"), ("B", "refine"), ("C", "context")):
            if key in d:
                write(root / folder / "results" / f"{name}.jsonl", d[key])
    if errors is None:
        errors = [error_row(f, c, r, ["재료 값이 틀림"]) for f, d in topics.items()
                  for c in "AC" if c in d for r in d[c] if not r["correct"]]
    if errors is not False:
        write(root / "round1_error_types.jsonl", errors)
    links = {"chem": {"a": "A"}, "solar": {"b": None}, "mineral": {"c": "C"}}
    (root / "criterion4_langlinks.json").write_text(json.dumps(links), encoding="utf-8")


def build(topics, errors=None):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    make_tree(root, topics, errors)
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
            self.assertTrue(row_of(page, "화학 원소")[8].startswith(expect), (a, row_of(page, "화학 원소")[8]))

    def test_criterion3_boundaries(self):
        a = [2] * 10  # A = 20
        for c_total, expect in ((60, "✓"), (59, "✗")):
            pq = [c_total // 10 + (1 if i < c_total % 10 else 0) for i in range(10)]
            tmp, page = build({"chem": {"A": counts_rows("base", a), "C": counts_rows("context", pq)}})
            self.addCleanup(tmp.cleanup)
            self.assertTrue(row_of(page, "화학 원소")[10].startswith(expect), (c_total, row_of(page, "화학 원소")[10]))

    def material_page(self, labels_for_wrong, errors=None):
        """A는 10문제 × 1번 맞고 9번 틀림(맞은 답 10). 틀린 A 답마다 labels_for_wrong을 붙인다. C는 모두 맞음."""
        a = counts_rows("base", [1] * 10)
        errs = [error_row("chem", "A", r, labels_for_wrong) for r in a if not r["correct"]] if errors is None else errors
        tmp, page = build({"chem": {"A": a, "C": counts_rows("context", [10] * 10)}}, errs)
        self.addCleanup(tmp.cleanup)
        return row_of(page, "화학 원소")

    def test_material_counts_calc_only_error_as_known(self):
        cells = self.material_page(["계산 없이 답함"])
        self.assertEqual(cells[4], "100")  # 틀려도 재료는 맞았다
        self.assertTrue(cells[8].startswith("✗"), cells[8])  # A 재료 100은 20~40 밖

    def test_material_counts_wrong_material_as_unknown(self):
        for labels in (["재료 값이 틀림"], ["계산이 틀림", "재료 값이 틀림"], ["숫자 없는 답"]):
            cells = self.material_page(labels)
            self.assertEqual(cells[4], "10", labels)
            self.assertTrue(cells[8].startswith("✗"), cells[8])

    def test_material_criteria_use_material_not_final(self):
        # 최종 답 A 20(통과 20~40), 틀린 답 중 40개는 계산만 틀림 → 재료 60 → ① ✗
        a = counts_rows("base", [2] * 10)
        wrong = [r for r in a if not r["correct"]]
        errs = [error_row("chem", "A", r, ["계산 없이 답함"] if i < 40 else ["재료 값이 틀림"]) for i, r in enumerate(wrong)]
        c = counts_rows("context", [10] * 10)
        tmp, page = build({"chem": {"A": a, "C": c}}, errs)
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "화학 원소")
        self.assertIn("20/100", cells[1])
        self.assertEqual((cells[4], cells[5], cells[7]), ("60", "100", "+40"))
        self.assertTrue(cells[8].startswith("✗"))
        self.assertTrue(cells[10].startswith("✓"))  # 재료 C − A = 40
        self.assertEqual(cells[6], "아직")  # B가 없다

    def test_material_missing_errors_file_is_pending(self):
        tmp, page = build({"chem": {"A": counts_rows("base", [2] * 10), "C": counts_rows("context", [10] * 10)}}, False)
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "화학 원소")
        self.assertEqual((cells[4], cells[5], cells[7], cells[8], cells[10]), ("아직",) * 5)

    def test_criterion2_never_judged(self):
        a = [2] * 10
        b = [refine_row(q, s, True, True, True) for q in QIDS for s in range(1, 11)]
        tmp, page = build({"chem": {"A": counts_rows("base", a), "B": b, "C": counts_rows("context", [10] * 10)}})
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "화학 원소")
        self.assertEqual(cells[9], "v2를 잰 뒤 판정")
        self.assertEqual(cells[6], "+80")  # B-v1 − A는 참고 숫자로만 나온다

    def test_criterion4(self):
        tmp, page = build({})
        self.addCleanup(tmp.cleanup)
        self.assertTrue(row_of(page, "화학 원소")[11].startswith("✓"))
        self.assertTrue(row_of(page, "태양계 천체")[11].startswith("✗"))

    def test_incomplete_topic(self):
        tmp, page = build({"solar": {"A": counts_rows("base", [10] * 10)[:50]}})
        self.addCleanup(tmp.cleanup)
        cells = row_of(page, "태양계 천체")
        self.assertIn("(진행 중)", cells[1])
        self.assertEqual(cells[8], "아직")
        self.assertEqual(cells[10], "아직")
        self.assertEqual(cells[2], "아직 없음")
        self.assertEqual(cells[6], "아직")
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

    def two_round_row(self, second_answer):
        r = refine_row(QIDS[0], 1, False, False, True)
        r["rounds"][0]["draft"]["text"] = "첫 글 <t>"
        r["rounds"][0]["judge"]["parsed"]["issues"] = ["한글 지적 <i>"]
        r["rounds"][0]["judge"]["parsed"]["revision_instruction"] = "다시 <풀어>"
        r["rounds"].append(dict(r["rounds"][0], round=2, draft_answer=second_answer, draft={**gen(), "text": "둘째 글"},
                                passed=True))
        return r

    def page_of(self, row):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        make_tree(root, {"chem": {"A": counts_rows("base", [5] * 10), "B": [row]}})
        return m.build(root, root / "o.html")[0].read_text(encoding="utf-8")

    def test_refine_request_between_rounds(self):
        import html
        page = self.page_of(self.two_round_row("1"))
        want = run.REFINE_USER.format(question="질문 q-00 <b>", draft="첫 글 <t>",
                                      issues=json.dumps(["한글 지적 <i>"], ensure_ascii=False), instruction="다시 <풀어>")
        self.assertIn(html.escape(want), page)
        self.assertIn("2회차 고쳐 쓰기 요청 (generate에게 보낸 글)", page)
        self.assertIn("2회차 고쳐 쓰기 요청 보기", page)
        self.assertIn("white-space:pre-wrap", page)
        self.assertEqual(page.count("고쳐 쓰기 요청 (generate에게 보낸 글)"), 1)  # 1회차 앞에는 없다
        order = [page.index(x) for x in ("1회차 judgement", "2회차 고쳐 쓰기 요청 (", "2회차 답")]
        self.assertEqual(order, sorted(order))

    def test_answer_changed_label(self):
        same = self.page_of(self.two_round_row(" 1 "))
        self.assertIn("답이 그대로</span>", same.split("<h2>씨앗별 자세히</h2>")[1])
        self.assertNotIn("답이 바뀜</span>", same.split("<h2>씨앗별 자세히</h2>")[1])
        diff = self.page_of(self.two_round_row("2"))
        self.assertIn("답이 바뀜</span>", diff.split("<h2>씨앗별 자세히</h2>")[1])
        self.assertNotIn("답이 그대로</span>", diff.split("<h2>씨앗별 자세히</h2>")[1])

    def test_seed_has_sticky_reference_box(self):
        page = self.page_of(self.two_round_row("2"))
        seeds = page.split('<details class="seed">')[1:]
        self.assertTrue(seeds)
        for sd in seeds:
            self.assertEqual(sd.count('<div class="std">'), 1)
            box = sd.split('<div class="std">')[1].split("</div>")[0]
            self.assertIn("기준 · 질문", box)
            self.assertIn('<span class="ans">1 kg</span>', box)
            self.assertIn("해설 보기", box)
            self.assertIn("근거 글 보기", box)
            self.assertLess(sd.index('class="std"'), sd.index("<h5>A</h5>"))
        self.assertIn("position: sticky", page)
        self.assertIn("max-width: 699px", page)
        self.assertIn("min-width: 1000px", page)
        # 정답이 A, 두 회차 답, 최종 답 옆에 한 줄로 붙는다. 이 씨앗에는 C가 없다.
        self.assertEqual(seeds[0].count('class="keyans"'), 4)
        self.assertEqual(seeds[0].count('<div class="pair">'), 2)

    def test_unparsed_output(self):
        html_ = m.gen_block({"text": "깨짐 <x>", "parsed": None}, False, None)
        self.assertIn("JSON으로 읽지 못함", html_)
        self.assertIn("깨짐 &lt;x&gt;", html_)

    def test_multi_sentence(self):
        s = m.grade_sentence(grade(True, multi=True))
        self.assertIn("마지막 숫자", s)
        self.assertIn("정답 1 kg와", s)


class Round2(unittest.TestCase):
    """--round 2: 분야 셋, 도시 줄 없음, B는 돌리지 않음. 임시 폴더의 가짜 데이터만 쓴다."""

    def page(self, a_ok, c_ok, wrong_label="계산 없이 답함"):
        """희토류 원소만 A, C를 채운다. 맞은 답 수는 a_ok, c_ok(질문마다 균등, 10의 배수 아님도 허용)."""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for f in ("rare_earth", "exoplanets", "moons"):
            (root / f).mkdir()
            (root / f / "questions.json").write_text(json.dumps(questions()), encoding="utf-8")

        def rows(cond, n_ok):
            return [simple(cond, qid, s, i * 10 + s - 1 < n_ok) for i, qid in enumerate(QIDS) for s in range(1, 11)]
        a, c = rows("base", a_ok), rows("context", c_ok)
        write(root / "rare_earth" / "results" / "base.jsonl", a)
        write(root / "rare_earth" / "results" / "context.jsonl", c)
        errs = [error_row("rare_earth", cond, r, [wrong_label]) for cond, rs in (("A", a), ("C", c)) for r in rs if not r["correct"]]
        write(root / "error_types.jsonl", errs)
        write(root / "round1_error_types.jsonl", [])  # round 2는 이 파일을 보지 않는다
        (root / "criterion4_langlinks.json").write_text(json.dumps({"rare_earth": {"가": "A"}, "moons": {"나": None}}), encoding="utf-8")
        out, _ = m.build(root, root / "results.html", 2)
        return out.read_text(encoding="utf-8")

    def test_summary_row(self):
        page = self.page(30, 80)
        cells = row_of(page, "희토류 원소")
        # 틀린 답은 모두 '계산 없이 답함'이라 재료는 다 맞은 것으로 센다: A 재료 100, C 재료 100
        self.assertEqual((cells[4], cells[5], cells[7]), ("100", "100", "+0"))
        self.assertTrue(cells[8].startswith("✗"))  # ① A 재료 100은 20~40 밖
        self.assertTrue(cells[10].startswith("✗"))  # ③ C−A 0

    def test_criteria_pass(self):
        page = self.page(30, 80, "재료 값이 틀림")
        cells = row_of(page, "희토류 원소")
        self.assertEqual((cells[4], cells[5], cells[7]), ("30", "80", "+50"))
        self.assertTrue(cells[8].startswith("✓"), cells[8])
        self.assertTrue(cells[10].startswith("✓"), cells[10])

    def test_no_city_and_b_not_run(self):
        page = self.page(30, 80)
        names = [re.findall(r"<td>(.*?)</td>", tr, re.S)[0] for tr in re.findall(r"<tr>(.*?)</tr>", page, re.S)
                 if "<td>" in tr]
        self.assertNotIn("어제 도시 10문제", page)
        self.assertEqual(names[:3], ["희토류 원소", "외계 행성", "덜 알려진 위성"])
        cells = row_of(page, "희토류 원소")
        self.assertEqual((cells[2], cells[9]), ("돌리지 않음", "B를 돌릴 때 판정"))
        self.assertIn("기준 ①③④를 넘는 분야가 둘 이상일 때만", page)
        self.assertNotIn("어제 프롬프트", page)

    def test_no_b_in_questions_and_seeds(self):
        page = self.page(30, 80)
        body = page.split("<h2>질문별 맞은 횟수</h2>")[1]
        self.assertNotIn("B-v1", body)
        self.assertNotIn("고쳐짐", body)
        self.assertIn("A 10 · C 10", body)
        self.assertIn("<th>C</th>", body)
        self.assertNotIn("<h5>B-v1</h5>", body)
        self.assertIn("<h5>C</h5>", body)

    def test_criterion4_and_pending(self):
        page = self.page(30, 80)
        self.assertTrue(row_of(page, "희토류 원소")[11].startswith("✓"))
        self.assertTrue(row_of(page, "덜 알려진 위성")[11].startswith("✗"))
        self.assertEqual(row_of(page, "외계 행성")[11], "아직")
        self.assertEqual(row_of(page, "외계 행성")[8], "아직")


if __name__ == "__main__":
    unittest.main()
