"""src/agent/compare.py(견주기)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

작은 가짜 기록(질문 2개 × 씨앗 2개 = 4번)으로 센다. 파일을 읽거나 쓰지 않는다. 기대하는 수는 손으로 센 값이다.
"""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare  # noqa: E402

SEEDS = (1, 2)
QUESTIONS = [{"id": "q1", "value": 10.0}, {"id": "q2", "value": 20.0}]
ORIGINAL = [f"x{i}" for i in range(1, 9)]
# 비교용 재료(원래 질문 k = 16): q1의 근거는 10등, q2의 근거는 9등(원래 8개 밖)
EVIDENCE_RANK = {"q1": 10, "q2": 9}


def comparison(qid):
    return [{"chunk_id": f"x{i}", "evidence": [0] if i == EVIDENCE_RANK[qid] else []} for i in range(1, 17)]


def search(n_chunks, hit):
    merged = [{"chunk_id": cid, "source": "original"} for cid in ORIGINAL] + \
             [{"chunk_id": f"extra{i}", "source": "korean"} for i in range(n_chunks - 8)]
    return {"merged": merged, "n_chunks": n_chunks, "hit": hit}


def answer(text):
    return {"answer": text}


def run_row(qid, seed, fixed, first=None, answer_text="10", first_text="10", passed=True, refined=False):
    return {"run_id": "R", "question_id": qid, "seed": seed, "code_commit": "c" * 40, "code_dirty": False, "langgraph_version": "1.2.17",
            "n_refinements": int(refined), "plan_passed": passed, "shape_error": None, "search": fixed,
            "comparison_retrieved": comparison(qid), "first_plan_search": first, "answer": answer(answer_text),
            "first_plan_answer": answer(first_text) if refined else None}


def minimal_row(qid, seed, hit, answer_text):
    return {"question_id": qid, "seed": seed, "hit": hit, "answer": answer_text, "code_commit": "m" * 40, "retrieved": [{"chunk_id": cid} for cid in ORIGINAL]}


def pair_row(qid, n_chunks, hit):
    return {"question_id": qid, "code_commit": "p" * 40, "search": search(n_chunks, hit), "comparison_retrieved": comparison(qid)}


def world():
    """손으로 센 기록. 실행: q1 s1 (안 고침, 12개, 근거 찾음) / q1 s2 (고침, 처음 8개 못 찾음 → 고친 13개 찾음: 나아짐) /
    q2 s1 (고침, 처음 12개 찾음 → 고친 9개 못 찾음: 나빠짐, 계획 불통과) / q2 s2 (안 고침, 8개, 못 찾음)."""
    runs = [run_row("q1", 1, search(12, True)),
            run_row("q1", 2, search(13, True), first=search(8, False), refined=True, answer_text="10", first_text="3"),
            run_row("q2", 1, search(9, False), first=search(12, True), refined=True, passed=False, answer_text="1", first_text="20"),
            run_row("q2", 2, search(8, False), answer_text="7")]
    pairs = [pair_row("q1", 12, False), pair_row("q2", 10, True)]
    minimal = [minimal_row("q1", 1, True, "10"), minimal_row("q1", 2, True, "11"), minimal_row("q2", 1, False, "20"), minimal_row("q2", 2, False, "3")]
    return runs, pairs, minimal


class CheckRunsTest(unittest.TestCase):
    def test_good_records_pass(self):
        runs, pairs, minimal = world()
        compare.check_runs(runs, QUESTIONS, SEEDS)
        compare.check_shape_errors(runs)
        compare.check_pair_rows(pairs, QUESTIONS)
        compare.check_original_eight(runs, pairs, minimal)

    def test_wrong_line_count(self):
        runs, _, _ = world()
        with self.assertRaisesRegex(ValueError, "3줄이다"):
            compare.check_runs(runs[:3], QUESTIONS, SEEDS)

    def test_missing_and_repeated_pair(self):
        runs, _, _ = world()
        runs[3] = copy.deepcopy(runs[0])
        with self.assertRaisesRegex(ValueError, "빠짐.*겹침"):
            compare.check_runs(runs, QUESTIONS, SEEDS)

    def test_two_commits(self):
        runs, _, _ = world()
        runs[2]["code_commit"] = "d" * 40
        with self.assertRaisesRegex(ValueError, "code_commit이 하나가 아니다"):
            compare.check_runs(runs, QUESTIONS, SEEDS)

    def test_dirty(self):
        runs, _, _ = world()
        runs[1]["code_dirty"] = True
        with self.assertRaisesRegex(ValueError, "code_dirty"):
            compare.check_runs(runs, QUESTIONS, SEEDS)

    def test_shape_error_row_stops_and_lists_it(self):
        runs, _, _ = world()
        runs[2]["shape_error"] = {"stage": "judgment", "index": 2, "problems": ["targets_ok가 없거나 참·거짓 값이 아님"]}
        with self.assertRaises(ValueError) as cm:
            compare.check_shape_errors(runs)
        message = str(cm.exception)
        for part in ("q2", "씨앗1", "judgment", "2번째", "targets_ok", "1개"):
            self.assertIn(part, message)

    def test_pair_rows_must_be_one_per_question(self):
        _, pairs, _ = world()
        with self.assertRaisesRegex(ValueError, "질문마다 한 줄이 아니다"):
            compare.check_pair_rows(pairs[:1], QUESTIONS)
        with self.assertRaisesRegex(ValueError, "겹침"):
            compare.check_pair_rows(pairs + [pairs[0]], QUESTIONS)

    def test_original_eight_differs_from_minimal_is_code_breakage(self):
        runs, pairs, minimal = world()
        minimal[1]["retrieved"][3] = {"chunk_id": "other"}
        with self.assertRaisesRegex(ValueError, "코드 고장.*q1 씨앗2"):
            compare.check_original_eight(runs, pairs, minimal)

    def test_original_eight_differs_from_comparison_is_code_breakage(self):
        runs, pairs, minimal = world()
        runs[3]["comparison_retrieved"][0] = {"chunk_id": "other", "evidence": []}
        with self.assertRaisesRegex(ValueError, "코드 고장.*q2 씨앗2"):
            compare.check_original_eight(runs, pairs, minimal)

    def test_original_eight_of_pair_search_is_checked_too(self):
        runs, pairs, minimal = world()
        pairs[1]["search"]["merged"][0]["chunk_id"] = "other"
        with self.assertRaisesRegex(ValueError, "코드 고장.*q2"):
            compare.check_original_eight(runs, pairs, minimal)

    def test_order_of_original_eight_matters(self):
        runs, pairs, minimal = world()
        merged = runs[0]["search"]["merged"]
        merged[0], merged[1] = merged[1], merged[0]
        with self.assertRaisesRegex(ValueError, "코드 고장"):
            compare.check_original_eight(runs, pairs, minimal)


class CountTest(unittest.TestCase):
    def setUp(self):
        runs, pairs, minimal = world()
        self.t = compare.totals(compare.per_run(runs, pairs, minimal, QUESTIONS))

    def test_hit_counts(self):
        t = self.t
        self.assertEqual((t["n"], t["current_hit"]), (4, 2))
        # 고친 계획: q1s1 O, q1s2 O, q2s1 X, q2s2 X. 처음 계획: q1s1 O(안 고침), q1s2 X, q2s1 O, q2s2 X
        self.assertEqual((t["fixed_hit"], t["first_hit"]), (2, 2))
        self.assertEqual(t["pair_hit"], 2)   # 질문마다 결과를 씨앗 2개에 똑같이 셈: q1 X × 2, q2 O × 2

    def test_comparison_is_cut_at_the_number_the_other_side_passed(self):
        t = self.t
        # 고친 계획의 수: q1s1 12(근거 10등 안 O), q1s2 13 O, q2s1 9(근거 9등 O), q2s2 8(X) → 3
        self.assertEqual(t["cmp_fixed"], 3)
        # 처음 계획의 수: q1s1 12 O, q1s2 8 X, q2s1 12 O, q2s2 8 X → 2
        self.assertEqual(t["cmp_first"], 2)
        # 짝 질문의 수: q1 12 O × 2, q2 10(근거 9등 안) O × 2 → 4
        self.assertEqual(t["cmp_pair"], 4)

    def test_differences(self):
        t = self.t
        self.assertEqual((t["diff_fixed"], t["diff_first"], t["diff_pair"]), (2 - 3, 2 - 2, 2 - 4))

    def test_refinements(self):
        t = self.t
        self.assertEqual((t["refined"], t["improved"], t["worsened"], t["plan_failed"]), (2, 1, 1, 1))

    def test_answers_are_regraded_from_the_stored_answer_text(self):
        t = self.t
        # 지금 시스템: "10"(q1 정답 10) O, "11" X(±1% 밖), "20"(q2 정답 20) O, "3" X → 2. 근거를 찾은 실행(q1 두 번) 가운데 맞은 것 1
        self.assertEqual((t["current_correct"], t["current_hit"], t["current_hit_correct"]), (2, 2, 1))
        # 고친 계획의 답: q1s1 "10" O, q1s2 "10" O, q2s1 "1" X, q2s2 "7" X → 2. 근거를 찾은 실행(q1s1, q1s2) 가운데 2
        self.assertEqual((t["fixed_correct"], t["fixed_hit_correct"]), (2, 2))
        # 처음 계획의 답: 안 고친 실행은 answer, 고친 실행은 first_plan_answer: q1s1 "10" O, q1s2 "3" X, q2s1 "20" O, q2s2 "7" X → 2. 근거를 찾은 실행(q1s1, q2s1) 가운데 2
        self.assertEqual((t["first_correct"], t["first_hit_correct"]), (2, 2))

    def test_record_correct_field_is_not_used(self):
        runs, pairs, minimal = world()
        for r in runs:
            r["answer"]["correct"] = True
        for r in minimal:
            r["correct"] = True
        t = compare.totals(compare.per_run(runs, pairs, minimal, QUESTIONS))
        self.assertEqual((t["current_correct"], t["fixed_correct"]), (2, 2))


class NextStepsTest(unittest.TestCase):
    def t(self, refined, improved, worsened, diff_fixed, diff_pair, fixed_hit=150, pair_hit=150, diff_first=None, first_hit=None):
        return {"refined": refined, "improved": improved, "worsened": worsened, "diff_fixed": diff_fixed, "diff_pair": diff_pair,
                "fixed_hit": fixed_hit, "pair_hit": pair_hit,
                "diff_first": diff_fixed if diff_first is None else diff_first, "first_hit": fixed_hit if first_hit is None else first_hit}

    def test_fewer_than_ten_refinements_cannot_be_measured(self):
        first, second = compare.next_steps(self.t(9, 5, 0, 11, 0))
        self.assertEqual(first, "계획 검사와 고치기: 이 질문으로는 잴 수 없음(남겨 둠). 새 시스템은 고친 계획으로 센다")
        self.assertTrue(second.startswith("다른 판 검색 남김"))

    def test_ten_refinements_and_more_improved_keeps(self):
        first, _ = compare.next_steps(self.t(10, 3, 2, 0, 0))
        self.assertEqual(first, "계획 검사와 고치기: 남김. 새 시스템은 고친 계획으로 센다")

    def test_not_more_improved_needs_cause_analysis_and_shows_the_second_line_for_both_outcomes(self):
        for improved, worsened in ((2, 2), (1, 3)):
            first, second = compare.next_steps(self.t(10, improved, worsened, 5, 0, diff_first=20))
            self.assertEqual(first, "계획 검사와 고치기: 원인 가르기 필요(판정·다시 쓰기 기록을 읽음)")
            self.assertEqual(second, "가.가 정해진 뒤. 가.에서 남기면(고친 계획으로 셈): 다른 판 검색 뺌 (새 시스템 − 비교용 = 5, 짝 질문으로 검색 − 비교용 = 0)"
                                     " / 가.에서 빼면(처음 계획으로 셈): 다른 판 검색 남김 (새 시스템 − 비교용 = 20, 짝 질문으로 검색 − 비교용 = 0)")

    def test_new_system_eleven_more_keeps_other_version_search(self):
        _, second = compare.next_steps(self.t(0, 0, 0, 11, 0))
        self.assertTrue(second.startswith("다른 판 검색 남김"))
        self.assertNotIn("기록만", second)

    def test_keeps_and_only_records_when_pair_search_is_higher_than_the_new_system(self):
        _, second = compare.next_steps(self.t(0, 0, 0, 11, 30, fixed_hit=180, pair_hit=181))
        self.assertTrue(second.startswith("다른 판 검색 남김"))
        self.assertIn("기록만", second)

    def test_no_record_only_note_when_pair_search_is_not_higher_even_if_its_difference_is_large(self):
        # 새 시스템 180 − 비교용 169 = 11, 짝 질문 178 − 비교용 150 = 28이어도 짝 질문으로 검색(178)이 새 시스템(180)보다 낮다
        _, second = compare.next_steps(self.t(0, 0, 0, 11, 28, fixed_hit=180, pair_hit=178))
        self.assertTrue(second.startswith("다른 판 검색 남김"))
        self.assertNotIn("기록만", second)

    def test_ten_or_less_and_pair_eleven_more_means_translation_problem(self):
        _, second = compare.next_steps(self.t(0, 0, 0, 10, 11))
        self.assertTrue(second.startswith("번역이 문제: 계획 요청 글을 고쳐 다시 잼"))

    def test_both_ten_or_less_drops_it(self):
        for diff_fixed, diff_pair in ((10, 10), (-5, 0), (0, -20)):
            _, second = compare.next_steps(self.t(0, 0, 0, diff_fixed, diff_pair))
            self.assertTrue(second.startswith("다른 판 검색 뺌"), (diff_fixed, diff_pair))


class SummaryTest(unittest.TestCase):
    def setUp(self):
        runs, pairs, minimal = world()
        self.text = compare.build_summary(runs, pairs, minimal, QUESTIONS, SEEDS)

    def test_tables_show_numerator_and_denominator(self):
        for line in ("| 지금 시스템 (원래 질문 8개) | 2/4 |", "| 새 시스템 (고친 계획) | 2/4 |", "| 새 시스템 (처음 계획) | 2/4 |",
                     "| 짝 질문으로 검색 | 2/4 |", "| 비교용 (고친 계획이 넘긴 수에 맞춤) | 3/4 |", "| 비교용 (처음 계획이 넘긴 수에 맞춤) | 2/4 |",
                     "| 비교용 (짝 질문으로 검색이 넘긴 수에 맞춤) | 4/4 |",
                     "| 새 시스템(고친 계획) − 비교용 | 2 − 3 = -1 |", "| 짝 질문으로 검색 − 비교용 | 2 − 4 = -2 |",
                     "| 다시 쓰기가 일어난 실행 | 2/4 |", "| 나아짐 (처음 계획 hit 아님 → 고친 계획 hit) | 1/2 |",
                     "| 나빠짐 (처음 계획 hit → 고친 계획 hit 아님) | 1/2 |", "| 계획 검사 불통과 (`plan_passed` false) | 1/4 |",
                     "| 맞은 답 | 2/4 | 2/4 | 2/4 |", "| 근거를 찾은 실행 가운데 맞은 답 | 1/2 | 2/2 | 2/2 |"):
            self.assertIn(line, self.text)

    def test_pair_search_is_counted_for_every_seed(self):
        self.assertIn("씨앗 2개에 똑같이 셈해 4번으로 센다", self.text)

    def test_chunk_count_distribution(self):
        # 고친 계획: 12, 13, 9, 8 각 1번. 처음 계획: 12, 8, 12, 8. 짝 질문: q1 12 × 2, q2 10 × 2
        for line in ("| 8 | 1 | 2 | 0 |", "| 9 | 1 | 0 | 0 |", "| 10 | 0 | 0 | 2 |", "| 12 | 1 | 2 | 2 |", "| 13 | 1 | 0 | 0 |"):
            self.assertIn(line, self.text)

    def test_per_question_table(self):
        self.assertIn("| q1 | 2/2 | 2/2 | 1/2 | 0/2 | 2/2 | 1/2 | 2/2 |", self.text)
        self.assertIn("| q2 | 0/2 | 0/2 | 1/2 | 2/2 | 1/2 | 1/2 | 2/2 |", self.text)

    def test_next_steps_lines(self):
        # 다시 쓰기 2번(10번 미만)이라 잴 수 없음. 새 시스템 − 비교용 = -1, 짝 질문 − 비교용 = -2라 둘 다 10번 이하
        self.assertIn("- 가. 계획 검사와 고치기: 이 질문으로는 잴 수 없음(남겨 둠)", self.text)
        self.assertIn("- 나. 다른 판 검색 뺌", self.text)

    def test_sources(self):
        self.assertIn("`" + "c" * 40 + "`", self.text)
        self.assertIn("langgraph 1.2.17", self.text)

    def test_same_records_give_the_same_summary(self):
        runs, pairs, minimal = world()
        self.assertEqual(self.text, compare.build_summary(runs, pairs, minimal, QUESTIONS, SEEDS))

    def test_records_are_not_changed(self):
        runs, pairs, minimal = world()
        before = copy.deepcopy((runs, pairs, minimal))
        compare.build_summary(runs, pairs, minimal, QUESTIONS, SEEDS)
        self.assertEqual((runs, pairs, minimal), before)


if __name__ == "__main__":
    unittest.main()
