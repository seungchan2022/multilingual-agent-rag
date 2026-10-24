"""src/minimal/compare_generation.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

실제 기록 파일(data/minimal/generation/)을 읽지 않는다. 질문 3개 × 씨앗 2의 손으로 만든 기록으로, 표마다 손으로 센 값과 견준다.
파일을 쓰는 시험은 임시 폴더에 쓴다.

가짜 기록(맞음 ○/×, 줄 순서는 씨앗 1의 a, b, c, 씨앗 2의 a, b, c):
  질문   언어 갈래      Baseline 씨앗1,2   최소판 씨앗1,2   검색(hit_ranks)
  a-ko   ko   한국어만   ○ ○               ○ ×              ✔ [2]
  b-en   en   영어만     × ○               ○ ○              ✔ [1, 3]
  c-ko   ko   영어만     ○ ×(끊김)          × ×              ✘ []
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare_generation as cg  # noqa: E402

SEEDS = (1, 2)
QUESTIONS = [{"id": "a-ko", "lang": "ko", "branch": "한국어만"}, {"id": "b-en", "lang": "en", "branch": "영어만"},
             {"id": "c-ko", "lang": "ko", "branch": "영어만"}]
CORRECT = {"baseline": {("a-ko", 1): True, ("a-ko", 2): True, ("b-en", 1): False, ("b-en", 2): True, ("c-ko", 1): True, ("c-ko", 2): False},
           "minimal": {("a-ko", 1): True, ("a-ko", 2): False, ("b-en", 1): True, ("b-en", 2): True, ("c-ko", 1): False, ("c-ko", 2): False}}
HIT = {"a-ko": [2], "b-en": [1, 3], "c-ko": []}


def make_rows(system):
    rows = []
    for seed in SEEDS:
        for q in QUESTIONS:
            n = len(rows) + 1
            correct = CORRECT[system][(q["id"], seed)]
            row = {"run_id": f"run-{system}", "system": system, "question_id": q["id"], "lang": q["lang"], "branch": q["branch"], "seed": seed,
                   "code_commit": "c" * 40, "correct": correct, "lang_ok": True, "parsed_ok": True, "picked": 1.0, "aborted": False,
                   "gen_seconds": float(n) if system == "baseline" else 10.0 * n, "prompt_tokens": 100 * n if system == "baseline" else 1000 + n}
            if system == "minimal":
                row.update({"hit": bool(HIT[q["id"]]), "hit_ranks": HIT[q["id"]]})
            rows.append(row)
    if system == "baseline":
        rows[1]["lang_ok"] = False                                  # 씨앗 1의 b-en: 답 언어가 다름
        rows[5].update({"aborted": True, "parsed_ok": False, "picked": None, "lang_ok": False, "prompt_tokens": None})   # 씨앗 2의 c-ko: 끊김
    else:
        rows[2]["picked"] = None                                    # 씨앗 1의 c-ko: 숫자를 못 꺼냄
        rows[0]["parsed_ok"] = False                                # 씨앗 1의 a-ko: JSON이 읽히지 않음
    return rows


def make_runs():
    return {system: make_rows(system) for system in cg.SYSTEMS}


class StatsTest(unittest.TestCase):
    def test_system_stats(self):
        base, mini = (cg.system_stats(rows) for rows in make_runs().values())
        self.assertEqual((base["n"], base["correct"], base["lang_ok"], base["not_parsed"], base["no_number"], base["aborted"]), (6, 4, 4, 1, 1, 1))
        self.assertEqual((mini["n"], mini["correct"], mini["lang_ok"], mini["not_parsed"], mini["no_number"], mini["aborted"]), (6, 3, 6, 1, 1, 0))

    def test_medians_and_null_tokens_are_dropped(self):
        base, mini = (cg.system_stats(rows) for rows in make_runs().values())
        self.assertEqual(base["gen_seconds"], 3.5)                   # 1..6
        self.assertEqual((base["prompt_tokens"], base["prompt_tokens_n"]), (300, 5))   # 100..500, 끊긴 답의 null(600 자리)은 뺀다
        self.assertEqual(mini["gen_seconds"], 35.0)                  # 10..60
        self.assertEqual((mini["prompt_tokens"], mini["prompt_tokens_n"]), (1003.5, 6))

    def test_all_prompt_tokens_null(self):
        rows = make_rows("baseline")
        for r in rows:
            r["prompt_tokens"] = None
        self.assertEqual(cg.system_stats(rows)["prompt_tokens"], None)


class GroupTest(unittest.TestCase):
    def test_group_counts(self):
        runs = make_runs()
        base = cg.group_counts(runs["baseline"], QUESTIONS, SEEDS)
        mini = cg.group_counts(runs["minimal"], QUESTIONS, SEEDS)
        self.assertEqual(base[("ko", "한국어만")], (2, 2))
        self.assertEqual(base[("ko", "영어만")], (1, 2))
        self.assertEqual(base[("en", "영어만")], (1, 2))
        self.assertEqual(mini[("ko", "한국어만")], (1, 2))
        self.assertEqual(mini[("ko", "영어만")], (0, 2))
        self.assertEqual(mini[("en", "영어만")], (2, 2))
        # 질문 언어만, 갈래만으로 합친 줄
        self.assertEqual((base[("ko", None)], base[("en", None)]), ((3, 4), (1, 2)))
        self.assertEqual((mini[("ko", None)], mini[("en", None)]), ((1, 4), (2, 2)))
        self.assertEqual((base[(None, "영어만")], mini[(None, "영어만")]), ((2, 4), (2, 4)))
        self.assertEqual((base[(None, "한국어만")], mini[(None, "한국어만")]), ((2, 2), (1, 2)))

    def test_empty_group_is_zero_over_zero(self):
        base = cg.group_counts(make_runs()["baseline"], QUESTIONS, SEEDS)
        self.assertEqual((base[("en", "두 언어")], base[(None, "두 언어")]), ((0, 0), (0, 0)))

    def test_group_sums_equal_total(self):
        for rows in make_runs().values():
            counts = cg.group_counts(rows, QUESTIONS, SEEDS)
            six = [counts[key] for key in cg.GROUPS]
            self.assertEqual((sum(c for c, _ in six), sum(n for _, n in six)), (sum(r["correct"] for r in rows), len(rows)))
            for part in ([("ko", None), ("en", None)], [(None, b) for b in ("한국어만", "영어만", "두 언어")]):
                self.assertEqual((sum(counts[k][0] for k in part), sum(counts[k][1] for k in part)), (sum(c for c, _ in six), len(rows)))


class PairTest(unittest.TestCase):
    def test_four_cells(self):
        pairs = cg.pair_counts(make_runs())
        # 짝: a1 둘 다 / a2 Baseline만 / b1 최소판만 / b2 둘 다 / c1 Baseline만 / c2 둘 다 틀림
        self.assertEqual(pairs, {"both": 2, "baseline_only": 2, "minimal_only": 1, "neither": 1, "pairs": 6})
        self.assertEqual(pairs["both"] + pairs["baseline_only"] + pairs["minimal_only"] + pairs["neither"], pairs["pairs"])


class RetrievalTest(unittest.TestCase):
    def test_hit_by_correct(self):
        cells = cg.hit_by_correct(make_runs()["minimal"])
        # ✔ 질문 a-ko(○ ×), b-en(○ ○) → 맞음 3, 틀림 1. ✘ 질문 c-ko(× ×) → 맞음 0, 틀림 2
        self.assertEqual(cells, {(True, True): 3, (True, False): 1, (False, True): 0, (False, False): 2})
        self.assertEqual(sum(cells.values()), 6)

    def test_question_retrieval(self):
        self.assertEqual(cg.question_retrieval(make_runs()["minimal"], QUESTIONS),
                         {"a-ko": (True, (2,)), "b-en": (True, (1, 3)), "c-ko": (False, ())})

    def test_retrieval_differing_between_seeds_stops(self):
        rows = make_runs()["minimal"]
        rows[3].update({"hit": False, "hit_ranks": []})   # 씨앗 2의 a-ko만 다르게
        with self.assertRaises(ValueError):
            cg.question_retrieval(rows, QUESTIONS)


class DistributionTest(unittest.TestCase):
    def test_distribution(self):
        runs = make_runs()
        per_question = {s: cg.correct_per_question(runs[s], QUESTIONS) for s in cg.SYSTEMS}
        self.assertEqual(per_question["baseline"], {"a-ko": 2, "b-en": 1, "c-ko": 1})
        self.assertEqual(per_question["minimal"], {"a-ko": 1, "b-en": 2, "c-ko": 0})
        base, mini = (cg.distribution(per_question[s], SEEDS) for s in cg.SYSTEMS)
        self.assertEqual(base, {2: 1, 1: 2, 0: 0})
        self.assertEqual(mini, {2: 1, 1: 1, 0: 1})
        self.assertEqual((sum(base.values()), sum(mini.values())), (3, 3))

    def test_aborted_list(self):
        runs = make_runs()
        self.assertEqual(cg.aborted_list(runs["baseline"]), {"c-ko": [2]})
        self.assertEqual(cg.aborted_list(runs["minimal"]), {})


class CheckTest(unittest.TestCase):
    def test_good_records_pass(self):
        cg.check_runs(make_runs(), QUESTIONS, SEEDS)

    def test_wrong_line_count(self):
        runs = make_runs()
        runs["minimal"].pop()
        with self.assertRaises(ValueError):
            cg.check_runs(runs, QUESTIONS, SEEDS)

    def test_unmatched_pair_stops(self):
        runs = make_runs()
        runs["minimal"][5]["question_id"] = "d-ko"   # 줄 수는 같지만 짝이 맞지 않는다
        with self.assertRaisesRegex(ValueError, "짝"):
            cg.check_runs(runs, QUESTIONS, SEEDS)

    def test_duplicated_pair_stops(self):
        runs = make_runs()
        runs["baseline"][5] = copy.deepcopy(runs["baseline"][4])   # 같은 짝이 두 번, 한 짝이 빠짐
        with self.assertRaisesRegex(ValueError, "짝"):
            cg.check_runs(runs, QUESTIONS, SEEDS)

    def test_several_code_commits_stop(self):
        runs = make_runs()
        runs["baseline"][2]["code_commit"] = "d" * 40
        with self.assertRaisesRegex(ValueError, "code_commit"):
            cg.check_runs(runs, QUESTIONS, SEEDS)

    def test_different_commits_between_files_are_allowed(self):
        runs = make_runs()
        for r in runs["minimal"]:
            r["code_commit"] = "e" * 40
        cg.check_runs(runs, QUESTIONS, SEEDS)

    def test_other_system_line_stops(self):
        runs = make_runs()
        runs["baseline"][0]["system"] = "minimal"
        with self.assertRaises(ValueError):
            cg.check_runs(runs, QUESTIONS, SEEDS)


class SummaryTest(unittest.TestCase):
    def test_summary_shows_hand_counted_cells(self):
        text = cg.build_summary(make_runs(), QUESTIONS, SEEDS)
        for expected in ("| 맞은 답 | 4/6 | 3/6 |", "| 되풀이로 끊긴 답(`aborted`) | 1/6 | 0/6 |",
                         "| 생성 시간 중앙값(초) | 3.50 | 35.00 |", "| 300 (5/6줄) | 1003.5 (6/6줄) |",
                         "| 질문 언어 ko | 2 | 3/4 | 1/4 |", "| en·두 언어 | 0 | 0/0 | 0/0 |",
                         "| 둘 다 맞음 | 2/6 |", "| Baseline만 맞음 | 2/6 |", "| 최소판만 맞음 | 1/6 |", "| 둘 다 틀림 | 1/6 |",
                         "| ✔ | 3 | 1 | 4/6 |", "| ✘ | 0 | 2 | 2/6 |", "검색 ✔인 질문이 2/3개",
                         "| 2/2 | 1/3 | 1/3 |", "| 1/2 | 2/3 | 1/3 |", "| 0/2 | 0/3 | 1/3 |",
                         "| a-ko | ko | 한국어만 | 2/2 | 1/2 | ✔ 2 | - |", "| b-en | en | 영어만 | 1/2 | 2/2 | ✔ 1, 3 | - |",
                         "| c-ko | ko | 영어만 | 1/2 | 0/2 | ✘ | Baseline 씨앗 2 |",
                         "- Baseline: `data/minimal/generation/runs_baseline.jsonl` 6줄, code_commit `" + "c" * 40 + "`, run_id `run-baseline`"):
            self.assertIn(expected, text)

    def test_same_records_same_text(self):
        self.assertEqual(cg.build_summary(make_runs(), QUESTIONS, SEEDS), cg.build_summary(make_runs(), QUESTIONS, SEEDS))

    def test_summary_changes_when_records_change(self):
        runs = make_runs()
        runs["minimal"][0]["correct"] = False
        self.assertNotEqual(cg.build_summary(runs, QUESTIONS, SEEDS), cg.build_summary(make_runs(), QUESTIONS, SEEDS))

    def test_read_runs_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "runs.jsonl"
            rows = make_rows("baseline")
            path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
            self.assertEqual(cg.read_runs(path), rows)

    def test_real_questions_group_sizes(self):
        questions = json.loads(cg.QUESTIONS.read_text(encoding="utf-8"))
        self.assertEqual(len(questions), 38)
        rows = [{"question_id": q["id"], "correct": True} for q in questions for _ in range(5)]
        counts = cg.group_counts(rows, questions)
        self.assertEqual(sum(n for key, (_, n) in counts.items() if key in cg.GROUPS), 190)


if __name__ == "__main__":
    unittest.main()
