"""src/agent/compare_answer.py(답 쓰기 판끼리 견주기)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

가짜 기록만 쓴다. 파일은 임시 폴더에 쓴다(data/agent/에는 쓰지 않는다).
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare_answer  # noqa: E402
from fakes import question  # noqa: E402

QUESTIONS = {qid: question(qid, "ko", f"{qid} 질문") for qid in ("q01-ko", "q02-ko")}   # 정답 값은 모두 17.7
ORDER = [("q01-ko", 1), ("q01-ko", 2), ("q02-ko", 1), ("q02-ko", 2)]


def reply(text, reason="읽는다", lang_ok=True, aborted=False):
    return {"answer": text, "reason": reason, "lang_ok": lang_ok, "aborted": aborted, "user_message": "질문 글"}


def base_row(qid, seed, hit, text, reason="읽는다", first=None, **kw):
    """⑧ 기록 꼴의 줄. first=(hit, 답 글)을 주면 처음 계획 기록(first_plan_search·first_plan_answer)이 따로 있는 줄이다."""
    row = {"question_id": qid, "seed": seed, "search": {"hit": hit, "hit_ranks": [1] if hit else [], "merged": [{"chunk_id": "c1"}]},
           "answer": reply(text, reason, **kw),
           "first_plan_search": None, "first_plan_answer": None}
    if first:
        row["first_plan_search"] = {"hit": first[0], "hit_ranks": [1] if first[0] else [], "merged": [{"chunk_id": "c1"}]}
        row["first_plan_answer"] = reply(first[1])
    return row


def checks(**kw):
    return {"shape_ok": True, "cites_evidence": True, "wrong_attached": 0, "no_number_facts": 0, "facts_without_chunks": 0, "citation_missing": False, "aborted": False, **kw}


def new_row(qid, seed, hit, text, reason="읽는다", cited=(), base_kind="final", check=None, **kw):
    return {"question_id": qid, "seed": seed, "hit": hit, "hit_ranks": [1] if hit else [], "source": {"path": "x", "run_id": "r", "base_kind": base_kind},
            "chunks": [{"chunk_id": "c1"}],
            "answer": {**reply(text, reason, **kw), "cited": list(cited), "checks": check or checks()}}


def base_world():
    return [base_row("q01-ko", 1, True, "17.7 kg", "3 × 4 = 12"), base_row("q01-ko", 2, True, "5 kg"),
            base_row("q02-ko", 1, False, "5 kg", lang_ok=False), base_row("q02-ko", 2, True, "17.7 kg", aborted=True)]


def new_world():
    return [new_row("q01-ko", 1, True, "17.7 kg", "6.145*60 = 368.7"), new_row("q01-ko", 2, True, "17.7 kg", "2 g × 3"),
            new_row("q02-ko", 1, False, "5 kg"), new_row("q02-ko", 2, True, "9 kg", check=checks(cites_evidence=False, wrong_attached=2, no_number_facts=1, facts_without_chunks=1))]


class SameInputsTest(unittest.TestCase):
    def setUp(self):
        self.base, self.new = compare_answer.cells_of(base_world()), compare_answer.cells_of(new_world())
        self.keys = compare_answer.pair_up(self.base, self.new, 4)

    def test_same_inputs_pass(self):
        compare_answer.check_same_inputs(self.base, self.new, self.keys)

    def test_different_inputs_stop(self):
        for field, value in (("chunk_ids", ["c2"]), ("hit_ranks", [9]), ("base_kind", "first_plan")):
            new = {k: dict(v) for k, v in self.new.items()}
            new[("q01-ko", 1)][field] = value
            with self.assertRaises(ValueError, msg=field):
                compare_answer.check_same_inputs(self.base, new, self.keys)
        new = {k: dict(v) for k, v in self.new.items()}
        new[("q01-ko", 1)]["answer"] = {**new[("q01-ko", 1)]["answer"], "user_message": "다른 질문"}
        with self.assertRaises(ValueError):
            compare_answer.check_same_inputs(self.base, new, self.keys)


class HitFixedTest(unittest.TestCase):
    def test_only_wrong_answers_that_had_evidence_are_counted(self):
        # base: q1s2(근거 찾음, 틀림) → new 맞음은 셈. q2s1(근거 못 찾음, 틀림) → new 맞음이어도 세지 않음
        base_rows = base_world()
        new_rows = new_world()
        new_rows[2] = new_row("q02-ko", 1, False, "17.7 kg")
        base, new = compare_answer.cells_of(base_rows), compare_answer.cells_of(new_rows)
        keys = compare_answer.pair_up(base, new, 4)
        b, w = compare_answer.side_counts(base, keys, QUESTIONS), compare_answer.side_counts(new, keys, QUESTIONS)
        fixed, _ = compare_answer.changes(base, new, keys, b, w)
        self.assertEqual(len(fixed), 2)
        self.assertEqual(compare_answer.hit_fixed(base, keys, b, w), 1)


class CellsTest(unittest.TestCase):
    def test_base_from_plan_search_picks_the_first_plan_when_it_exists(self):
        rows = [base_row("q01-ko", 1, False, "최종 답", first=(True, "처음 계획 답")), base_row("q01-ko", 2, True, "최종 답")]
        cells = compare_answer.cells_of(rows)
        self.assertEqual((cells[("q01-ko", 1)]["base_kind"], cells[("q01-ko", 1)]["hit"], cells[("q01-ko", 1)]["answer"]["answer"]), ("first_plan", True, "처음 계획 답"))
        self.assertEqual((cells[("q01-ko", 2)]["base_kind"], cells[("q01-ko", 2)]["hit"], cells[("q01-ko", 2)]["answer"]["answer"]), ("final", True, "최종 답"))

    def test_record_of_this_form_is_taken_as_it_is(self):
        cells = compare_answer.cells_of([new_row("q01-ko", 1, True, "17.7", base_kind="first_plan")])
        self.assertEqual((cells[("q01-ko", 1)]["base_kind"], cells[("q01-ko", 1)]["hit"], cells[("q01-ko", 1)]["answer"]["answer"]), ("first_plan", True, "17.7"))

    def test_repeated_pair_stops(self):
        with self.assertRaises(ValueError):
            compare_answer.cells_of([new_row("q01-ko", 1, True, "a"), new_row("q01-ko", 1, True, "b")])


class PairUpTest(unittest.TestCase):
    def cells(self, pairs):
        return compare_answer.cells_of([new_row(q, s, True, "17.7") for q, s in pairs])

    def test_matching_pairs_in_base_order(self):
        self.assertEqual(compare_answer.pair_up(self.cells(ORDER), self.cells(reversed(ORDER)), 4), ORDER)

    def test_missing_pair_stops(self):
        with self.assertRaises(ValueError) as cm:
            compare_answer.pair_up(self.cells(ORDER), self.cells(ORDER[:3]), 4)
        self.assertIn("q02-ko", str(cm.exception))

    def test_same_count_but_different_pairs_stops(self):
        with self.assertRaises(ValueError):
            compare_answer.pair_up(self.cells(ORDER), self.cells(ORDER[:3] + [("q03-ko", 1)]), 4)

    def test_default_is_190_pairs(self):
        self.assertEqual(compare_answer.EXPECTED_PAIRS, 190)
        with self.assertRaises(ValueError):
            compare_answer.pair_up(self.cells(ORDER), self.cells(ORDER))


class CalculationTest(unittest.TestCase):
    def test_pattern(self):
        search = compare_answer.CALCULATION.search
        for text in ("3 × 4", "6.145*60", "10 ÷ 4", "1 + 2", "5 − 1", "계산: 1,000 × 0.5", "5.246 g/cm³ × 60 cm³", "9.841 g/cm³ − 9.32"):
            self.assertTrue(search(text), text)
        for text in ("읽는다", "숫자 12", "17.7 시간", "× 4", "3 ×", "공식을 쓴다", "2 x 3", "1/2", "5 - 1", "2.5·4", "Tb-144", "6.145 g/cm³",
                     "Volume = width × length × height"):
            self.assertFalse(search(text), text)


class CountsTest(unittest.TestCase):
    def setUp(self):
        self.base, self.new = compare_answer.cells_of(base_world()), compare_answer.cells_of(new_world())
        self.keys = compare_answer.pair_up(self.base, self.new, 4)
        self.b = compare_answer.side_counts(self.base, self.keys, QUESTIONS)
        self.w = compare_answer.side_counts(self.new, self.keys, QUESTIONS)

    def test_both_sides_counts(self):
        # base: 근거 찾음 3, 맞음 2(q1s1, q2s2), 찾고도 틀림 1(q1s2), 언어 같음 3, 끊김 1, 계산 1(3 × 4)
        self.assertEqual({k: v for k, v in self.b.items() if k != "correct_by"},
                         {"hit": 3, "correct": 2, "hit_wrong": 1, "lang_ok": 3, "aborted": 1, "calculation": 1})
        # new: 근거 찾음 3, 맞음 2(q1s1, q1s2), 찾고도 틀림 1(q2s2), 언어 같음 4, 끊김 0, 계산 2
        self.assertEqual({k: v for k, v in self.w.items() if k != "correct_by"},
                         {"hit": 3, "correct": 2, "hit_wrong": 1, "lang_ok": 4, "aborted": 0, "calculation": 2})

    def test_correct_is_regraded_from_the_answer_text_not_the_stored_flag(self):
        rows = new_world()
        for r in rows:
            r["answer"]["correct"] = True
        counts = compare_answer.side_counts(compare_answer.cells_of(rows), self.keys, QUESTIONS)
        self.assertEqual(counts["correct"], 2)

    def test_changes_lists_both_directions_with_both_answer_texts(self):
        fixed, broken = compare_answer.changes(self.base, self.new, self.keys, self.b, self.w)
        self.assertEqual(fixed, [("q01-ko", 2, "5 kg", "17.7 kg")])
        self.assertEqual(broken, [("q02-ko", 2, "17.7 kg", "9 kg")])

    def test_new_side_common_checks(self):
        rows = new_world()
        rows[0]["answer"]["checks"] = checks(citation_missing=True)
        rows[1]["answer"]["checks"] = checks(shape_ok=False, cites_evidence=None, wrong_attached=None, no_number_facts=None, facts_without_chunks=None, citation_missing=None)
        rows[2]["answer"]["cited"] = [{"invalid_chunks": [9]}, {"invalid_chunks": []}]
        c = compare_answer.new_checks(compare_answer.cells_of(rows), self.keys)
        self.assertEqual(c["shape_errors"], [("q01-ko", 2)])
        self.assertEqual((c["hit_cites"], c["n_hit"]), (1, 3))   # 근거를 찾은 실행 셋: q1s1 true, q1s2 null(꼴 오류), q2s2 false
        self.assertEqual(c["cites_false"], [("q02-ko", 2)])
        self.assertEqual((c["wrong_attached_sum"], c["wrong_attached"]), (2, [(("q02-ko", 2), 2)]))
        self.assertEqual(c["no_number_facts"], 1)
        self.assertEqual(c["facts_without_chunks"], [(("q02-ko", 2), 1)])
        self.assertEqual(c["citation_missing"], [("q01-ko", 1)])
        self.assertEqual(c["invalid_chunks"], [(("q02-ko", 1), [9])])


class RenderTest(unittest.TestCase):
    def render(self, base=None, new=None):
        return compare_answer.render(compare_answer.cells_of(base or base_world()), compare_answer.cells_of(new or new_world()),
                                     Path("base.jsonl"), Path("new.jsonl"), QUESTIONS, 4)

    def test_tables_lists_and_checks(self):
        text = self.render()
        for part in ("| 근거를 찾음 | 3/4 | 3/4 |", "| 맞음 | 2/4 | 2/4 |", "| 근거를 찾고도 틀림 | 1/3 | 1/3 |", "| 답 언어가 질문과 같음 | 3/4 | 4/4 |",
                     "| 끊김 | 1/4 | 0/4 |", "| 생각 과정에 숫자 계산을 씀 | 1/4 | 2/4 |",
                     "## 틀림 → 맞음 (1개)", "q01-ko 씨앗2", "## 맞음 → 틀림 (1개)", "q02-ko 씨앗2",
                     "- 꼴 오류: 0개", "cites_evidence가 false인 실행: 1개", "wrong_attached 합: 2 (1개 실행)", "no_number_facts 합: 1",
                     "citation_missing인 실행: 0개", "invalid_chunks)가 있는 실행: 0개", "짝지은 실행: 4쌍"):
            self.assertIn(part, text)

    def test_base_kind_counts_are_shown(self):
        rows = base_world()
        rows[0] = base_row("q01-ko", 1, False, "17.7 kg", first=(True, "17.7 kg"))
        new = new_world()
        new[0] = new_row("q01-ko", 1, True, "17.7 kg", base_kind="first_plan")   # 판 0 고르기가 같아야 짝이 된다
        self.assertIn("처음 계획 1줄, 최종 3줄", self.render(base=rows, new=new))

    def test_no_change_prints_none(self):
        text = self.render(base=[base_row(q, s, True, "17.7 kg") for q, s in ORDER], new=[new_row(q, s, True, "17.7 kg") for q, s in ORDER])
        self.assertIn("## 틀림 → 맞음 (0개)\n\n- 그 가운데 base에서 근거를 찾고도 틀렸던 답: 0개\n\n- 없음", text)
        self.assertIn("## 맞음 → 틀림 (0개)\n\n- 없음", text)

    def test_missing_pair_stops_the_summary(self):
        with self.assertRaises(ValueError):
            self.render(new=new_world()[:3])

    def test_comparing_two_cite_records_works(self):
        base = [new_row(q, s, h, "5 kg") for (q, s), h in zip(ORDER, (True, True, False, True))]   # 입력(hit_ranks)은 new_world와 같게
        self.assertIn("| 맞음 | 0/4 | 2/4 |", self.render(base=base))

    def test_same_records_give_the_same_summary(self):
        self.assertEqual(self.render(), self.render())


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.base, self.new, self.out = root / "base.jsonl", root / "new.jsonl", root / "out" / "summary.md"
        self.base.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in base_world()), encoding="utf-8")
        self.new.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in new_world()), encoding="utf-8")
        self.questions = root / "questions.json"
        self.questions.write_text(json.dumps(list(QUESTIONS.values()), ensure_ascii=False), encoding="utf-8")

    def call_main(self, argv):
        with mock.patch.object(compare_answer, "QUESTIONS", self.questions), mock.patch.object(compare_answer, "EXPECTED_PAIRS", 4), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            compare_answer.main(argv)

    def args(self):
        return ["--base", str(self.base), "--new", str(self.new), "--out", str(self.out)]

    def test_writes_the_summary(self):
        self.call_main(self.args())
        self.assertIn("| 맞음 | 2/4 | 2/4 |", self.out.read_text(encoding="utf-8"))

    def test_existing_summary_stops_and_is_kept(self):
        self.out.parent.mkdir()
        self.out.write_text("이미 있음\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            self.call_main(self.args())
        self.assertEqual(self.out.read_text(encoding="utf-8"), "이미 있음\n")

    def test_missing_arguments_are_refused(self):
        with self.assertRaises(SystemExit):
            self.call_main(["--base", str(self.base), "--new", str(self.new)])

    def test_unpaired_records_stop_without_writing(self):
        self.new.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in new_world()[:3]), encoding="utf-8")
        with self.assertRaises(ValueError):
            self.call_main(self.args())
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
