"""src/minimal/compare_retrieval.py를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/minimal

실제 질문 38개로 검색을 돌리지 않는다. DB와 모델 없이, 손으로 만든 질문·청크·결과 줄로 ✔ 판정, 세기, 고르기, 요약을 본다.
파일을 쓰는 시험은 임시 폴더에 쓴다(data/minimal/retrieval/에는 쓰지 않는다).
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compare_retrieval as cr  # noqa: E402

QUESTIONS = json.loads(cr.QUESTIONS.read_text(encoding="utf-8"))


def evidence(doc_id, line, value_text):
    return {"doc_id": doc_id, "line": line, "value_text": value_text}


def question(qid="q01-ko", lang="ko", branch="한국어만", evid=None):
    return {"id": qid, "lang": lang, "branch": branch, "evidence": evid or [evidence("doc-a", 5, "17.7")]}


def chunk(doc_id="doc-a", lines=(4, 5, 9), text="반감기는 17.7 시간이다"):
    return {"doc_id": doc_id, "lines": list(lines), "text": text}


class MatchedEvidenceTest(unittest.TestCase):
    def test_all_conditions_met(self):
        self.assertEqual(cr.matched_evidence(question(), chunk()), [0])

    def test_line_in_list_but_value_missing(self):
        self.assertEqual(cr.matched_evidence(question(), chunk(text="반감기는 18.1 시간이다")), [])

    def test_value_present_but_line_not_in_list(self):
        self.assertEqual(cr.matched_evidence(question(), chunk(lines=(4, 6, 9))), [])

    def test_different_doc(self):
        self.assertEqual(cr.matched_evidence(question(), chunk(doc_id="doc-b")), [])

    def test_one_of_two_evidence_is_enough(self):
        q = question(evid=[evidence("doc-a", 5, "17.7"), evidence("doc-b", 7, "99")])
        self.assertEqual(cr.matched_evidence(q, chunk()), [0])
        self.assertEqual(cr.matched_evidence(q, chunk(doc_id="doc-b", lines=(7,), text="값 99")), [1])

    def test_line_inside_range_but_not_in_list(self):
        # 표 조각: 머리글(4)과 행(9)만 있고 5~8줄은 없다. 줄 범위는 4~9지만 5는 목록에 없다.
        self.assertEqual(cr.matched_evidence(question(), chunk(lines=(4, 9), text="머리글 17.7 행")), [])

    def test_empty_value_text_stops(self):
        with self.assertRaises(ValueError):
            cr.matched_evidence(question(evid=[evidence("doc-a", 5, "")]), chunk())


def found_row(n, doc_id="doc-x", lines=(1,), text="무관", tokens=100):
    """search가 돌려주는 한 줄 (chunk_id, distance, doc_id, lines, text, tokens)."""
    return (f"{doc_id}#{n:04d}", 0.1 * n, doc_id, list(lines), text, tokens)


class ResultRowTest(unittest.TestCase):
    def test_row_fields(self):
        found = [found_row(1, tokens=100), found_row(2, "doc-a", (5,), "17.7 값", 80), found_row(3, tokens=60),
                 found_row(4, "doc-a", (5,), "17.7", 40)]
        row = cr.result_row("size256_title", "bge-m3", question(), found)
        self.assertEqual((row["chunk_set"], row["model"], row["k"], row["question_id"]), ("size256_title", "bge-m3", 4, "q01-ko"))
        self.assertEqual((row["lang"], row["branch"], row["cross"]), ("ko", "한국어만", False))
        self.assertTrue(row["hit"])
        self.assertEqual(row["hit_ranks"], [2, 4])
        self.assertEqual(row["retrieved_tokens"], 280)
        self.assertEqual([r["rank"] for r in row["retrieved"]], [1, 2, 3, 4])
        self.assertEqual([r["evidence"] for r in row["retrieved"]], [[], [0], [], [0]])
        self.assertEqual(set(row["retrieved"][1]), {"rank", "chunk_id", "doc_id", "distance", "lines", "tokens", "evidence"})

    def test_miss(self):
        row = cr.result_row("size128_notitle", "gte-multilingual-base", question(), [found_row(1)])
        self.assertEqual((row["hit"], row["hit_ranks"], row["k"]), (False, [], 8))

    def test_chunk_set_name(self):
        self.assertEqual(cr.parse_chunk_set("size128_notitle"), (128, False))
        self.assertEqual(cr.parse_chunk_set("size256_title"), (256, True))


class CountTest(unittest.TestCase):
    def test_cross_is_only_two_of_six_groups(self):
        crosses = {(lang, branch): cr.is_cross(question(lang=lang, branch=branch)) for lang, branch in cr.GROUPS}
        self.assertEqual({g for g, v in crosses.items() if v}, {("ko", "영어만"), ("en", "한국어만")})

    def test_real_questions_group_sizes(self):
        sizes = {g: sum(1 for q in QUESTIONS if (q["lang"], q["branch"]) == g) for g in cr.GROUPS}
        self.assertEqual(list(sizes.values()), [8, 8, 3, 8, 8, 3])
        self.assertEqual(sum(cr.is_cross(q) for q in QUESTIONS), 16)

    def test_counts_by_group_and_cross(self):
        rows = [row("a", "bge-m3", lang, branch, hit) for lang, branch, hit in [
            ("ko", "한국어만", True), ("ko", "한국어만", False), ("ko", "영어만", True), ("en", "한국어만", True),
            ("en", "영어만", False), ("en", "두 언어", True)]]
        c = cr.combo_counts(rows)[("a", "bge-m3")]
        self.assertEqual((c["total"], c["n"], c["cross"], c["cross_n"]), (4, 6, 2, 2))
        self.assertEqual(c["groups"][("ko", "한국어만")], (1, 2))
        self.assertEqual(c["groups"][("ko", "영어만")], (1, 1))
        self.assertEqual(c["groups"][("en", "두 언어")], (1, 1))
        self.assertNotIn(("ko", "두 언어"), c["groups"])


def row(chunk_set, model, lang, branch, hit, tokens=100, qid="q"):
    return {"chunk_set": chunk_set, "model": model, "k": 8, "question_id": qid, "lang": lang, "branch": branch,
            "cross": (lang, branch) in (("ko", "영어만"), ("en", "한국어만")), "hit": hit, "hit_ranks": [1] if hit else [],
            "retrieved": [], "retrieved_tokens": tokens}


GTE = "gte-multilingual-base"
BGE = "bge-m3"


def counts_of(spec):
    """{(chunk_set, model): (전체 ✔, 다른 언어 ✔)} -> choose가 받는 모양."""
    return {combo: {"total": total, "n": 38, "groups": {}, "cross": cross, "cross_n": 16, "tokens": [0]} for combo, (total, cross) in spec.items()}


class ChooseTest(unittest.TestCase):
    def test_gap_2_is_tied_and_3_is_not(self):
        spec = {("size128_notitle", GTE): (31, 8), ("size128_title", GTE): (29, 8), ("size256_title", GTE): (28, 8)}
        picked = cr.choose(counts_of(spec))
        self.assertEqual(picked["best"], 31)
        self.assertEqual([combo for combo, _ in picked["tied"]], [("size128_notitle", GTE), ("size128_title", GTE)])

    def test_step1_cross_decides_even_if_total_is_lower(self):
        spec = {("size128_notitle", GTE): (30, 5), ("size256_notitle", BGE): (29, 6)}
        picked = cr.choose(counts_of(spec))
        self.assertEqual(picked["chosen"], ("size256_notitle", BGE))
        self.assertEqual(len(picked["steps"]), 1)

    def test_step2_gte_decides_when_step1_equal(self):
        spec = {("size128_notitle", BGE): (30, 6), ("size256_title", GTE): (30, 6)}
        picked = cr.choose(counts_of(spec))
        self.assertEqual(picked["chosen"], ("size256_title", GTE))
        self.assertEqual([s["name"][:2] for s in picked["steps"]], ["1.", "2."])
        self.assertEqual(len(picked["steps"][0]["remaining"]), 2)

    def test_step3_no_title_decides(self):
        spec = {("size128_title", GTE): (30, 6), ("size256_notitle", GTE): (30, 6)}
        self.assertEqual(cr.choose(counts_of(spec))["chosen"], ("size256_notitle", GTE))

    def test_step4_small_size_decides(self):
        spec = {("size256_notitle", GTE): (30, 6), ("size128_notitle", GTE): (30, 6)}
        picked = cr.choose(counts_of(spec))
        self.assertEqual(picked["chosen"], ("size128_notitle", GTE))
        self.assertEqual(len(picked["steps"]), 4)

    def test_single_tied_combo_is_chosen_without_steps(self):
        spec = {("size256_title", BGE): (31, 3), ("size128_notitle", GTE): (20, 9)}
        picked = cr.choose(counts_of(spec))
        self.assertEqual(picked["chosen"], ("size256_title", BGE))
        self.assertEqual(picked["steps"], [])

    def test_earlier_step_beats_later_step(self):
        # 2칸(gte)에서는 B가 앞서지만 1칸(다른 언어 ✔)에서 A가 앞서므로 A다.
        spec = {("size128_notitle", BGE): (30, 7), ("size128_notitle", GTE): (30, 6)}
        self.assertEqual(cr.choose(counts_of(spec))["chosen"], ("size128_notitle", BGE))


class SummaryTest(unittest.TestCase):
    CHUNK_ROWS = [
        {"doc_id": "d1", "tokens": 50, "over_limit": False}, {"doc_id": "d1", "tokens": 100, "over_limit": False},
        {"doc_id": "d2", "tokens": 120, "over_limit": False}, {"doc_id": "d2", "tokens": 130, "over_limit": True},
        {"doc_id": "d2", "tokens": 200, "over_limit": True}, {"doc_id": "d3", "tokens": 170, "over_limit": True}]

    def sample_rows(self):
        rows = []
        for chunk_set, model, hits in [("size128_notitle", GTE, 3), ("size256_title", BGE, 2)]:
            for i, (lang, branch) in enumerate(cr.GROUPS):
                rows.append(row(chunk_set, model, lang, branch, i < hits, tokens=100 + i))
        return rows

    def stats(self):
        return {"size128_notitle": cr.chunk_stats(self.CHUNK_ROWS), "size256_title": cr.chunk_stats(self.CHUNK_ROWS[:2])}

    def test_chunk_stats(self):
        s = cr.chunk_stats(self.CHUNK_ROWS)
        self.assertEqual(s["n"], 6)
        self.assertEqual(s["tokens"], (50, 125.0, 200, 200))   # 중앙값 (120 + 130) / 2, 90%는 6 × 0.9 = 5.4 → 6번째
        self.assertEqual((s["over_n"], s["over"]), (3, (130, 170, 200)))
        self.assertEqual(s["per_doc"], {"d2": 2, "d3": 1})
        self.assertIsNone(cr.chunk_stats(self.CHUNK_ROWS[:2])["over"])

    def test_summary_numbers_come_from_results(self):
        text = cr.build_summary(self.sample_rows(), self.stats())
        self.assertIn("| size128_notitle | gte-multilingual-base | 8 | 3/6 |", text)
        self.assertIn("| size256_title | bge-m3 | 4 | 2/6 |", text)
        self.assertIn("고른 조합: size128_notitle × gte-multilingual-base", text)   # 전체 ✔ 3 대 2: 차이 1이라 비김 → 1칸 다른 언어 ✔는 1 대 1로 같고 → 2칸 gte
        self.assertIn("| size128_notitle | 6 | 50 | 125 | 200 | 200 | 3 | 130 | 170 | 200 |", text)
        self.assertIn("- size128_notitle: d2 2, d3 1", text)
        self.assertIn("- size256_title: 없음", text)

    def test_summary_changes_when_results_change(self):
        rows = self.sample_rows()
        before = cr.build_summary(rows, self.stats())
        rows[0]["hit"] = False
        self.assertNotEqual(before, cr.build_summary(rows, self.stats()))

    def test_same_file_gives_same_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.jsonl"
            cr.write_results(path, self.sample_rows())
            first = cr.build_summary(cr.read_results(path), self.stats()).encode("utf-8")
            second = cr.build_summary(cr.read_results(path), self.stats()).encode("utf-8")
            self.assertEqual(first, second)
            Path(tmp, "summary.md").write_bytes(first)
            self.assertEqual(Path(tmp, "summary.md").read_bytes(), second)

    def test_write_read_roundtrip(self):
        rows = self.sample_rows()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sub" / "results.jsonl"
            cr.write_results(path, rows)
            self.assertEqual(cr.read_results(path), rows)
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), len(rows))


if __name__ == "__main__":
    unittest.main()
