"""src/agent/merge.py(청크 합치기)를 검사하는 시험.

  .venv/bin/python -m unittest discover -s src/agent

실제 데이터베이스와 임베딩 모델은 쓰지 않는다. 검색어 글이 곧 가짜 벡터이고 검색어마다 정해 둔 청크 줄을 돌려준다(fakes.py).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import merge  # noqa: E402
from fakes import found_row, patched, question  # noqa: E402

ORIGINAL = "반감기는 몇 시간인가?"


def rows(prefix, n, evidence_at=()):
    return [found_row(f"{prefix}{i}", text=f"{prefix}{i} 글", evidence=i in evidence_at) for i in range(1, n + 1)]


def search_tables(**extra):
    return {ORIGINAL: rows("o", 16), **extra}


def merge_with(searches, others, q=None):
    with patched(None, searches) as calls:
        record, found = merge.merge_search(None, None, q or question(text=ORIGINAL), others)
    return record, found, calls


class MergeTest(unittest.TestCase):
    def test_original_eight_are_all_kept(self):
        record, found, calls = merge_with(search_tables(), [])
        self.assertEqual([c["chunk_id"] for c in record["merged"]], [f"o{i}" for i in range(1, 9)])
        self.assertEqual([r[0] for r in found], [f"o{i}" for i in range(1, 9)])
        self.assertEqual((record["n_chunks"], calls), (8, [(ORIGINAL, 8)]))

    def test_overlap_is_removed_and_not_refilled(self):
        # 한국어판 위 4개: o2(겹침), k1, k2, k3. k4 이후로 내려가 채우지 않는다
        searches = search_tables(**{"한국어판": [found_row("o2")] + rows("k", 5)})
        record, found, calls = merge_with(searches, [("korean", "한국어판")])
        self.assertEqual([c["chunk_id"] for c in record["merged"]][8:], ["k1", "k2", "k3"])
        self.assertEqual(record["n_chunks"], 11)
        self.assertEqual(calls, [(ORIGINAL, 8), ("한국어판", 4)])
        self.assertEqual([r[0] for r in found], [c["chunk_id"] for c in record["merged"]])

    def test_order_original_then_korean_then_english(self):
        searches = search_tables(**{"한국어판": rows("k", 4), "english version": rows("e", 4)})
        record, found, _ = merge_with(searches, [("korean", "한국어판"), ("english", "english version")])
        self.assertEqual([c["chunk_id"] for c in record["merged"]],
                         [f"o{i}" for i in range(1, 9)] + ["k1", "k2", "k3", "k4", "e1", "e2", "e3", "e4"])
        self.assertEqual([c["rank"] for c in record["merged"]], list(range(1, 17)))
        self.assertEqual([c["source"] for c in record["merged"]], ["original"] * 8 + ["korean"] * 4 + ["english"] * 4)
        self.assertEqual([c["source_rank"] for c in record["merged"]], [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 1, 2, 3, 4])
        self.assertEqual(record["n_chunks"], 16)   # 최대 16개

    def test_english_overlaps_with_korean_and_original(self):
        searches = search_tables(**{"한국어판": rows("k", 4), "english version": [found_row("k1"), found_row("o3"), found_row("e1"), found_row("e2"), found_row("e3")]})
        record, _, _ = merge_with(searches, [("korean", "한국어판"), ("english", "english version")])
        self.assertEqual([c["chunk_id"] for c in record["merged"]][12:], ["e1", "e2"])
        self.assertEqual([c["source_rank"] for c in record["merged"]][12:], [3, 4])

    def test_same_text_as_original_is_skipped(self):
        # 앞뒤 빈칸이 달라도 같은 글이다. 건너뛴 검색어는 검색하지 않는다
        searches = search_tables(**{"english version": rows("e", 4)})
        record, _, calls = merge_with(searches, [("korean", "  " + ORIGINAL + "\n"), ("english", "english version")])
        korean = record["queries"][1]
        self.assertEqual((korean["name"], korean["skipped"], korean["retrieved"], korean["embed_seconds"], korean["search_seconds"]),
                         ("korean", True, [], None, None))
        self.assertEqual(korean["text"], "  " + ORIGINAL + "\n")
        self.assertEqual(calls, [(ORIGINAL, 8), ("english version", 4)])
        self.assertEqual(record["n_chunks"], 12)   # 한 언어로만 쓴 질문은 검색 두 번, 최대 12개

    def test_both_skipped(self):
        record, _, calls = merge_with(search_tables(), [("korean", ORIGINAL), ("english", ORIGINAL)])
        self.assertEqual((record["n_chunks"], calls, [q["skipped"] for q in record["queries"]]), (8, [(ORIGINAL, 8)], [False, True, True]))

    def test_query_records(self):
        searches = search_tables(**{"한국어판": rows("k", 4)})
        record, _, _ = merge_with(searches, [("korean", "한국어판")])
        original, korean = record["queries"]
        self.assertEqual((original["name"], original["text"], original["skipped"], len(original["retrieved"])), ("original", ORIGINAL, False, 8))
        self.assertEqual((korean["name"], korean["text"], korean["skipped"], len(korean["retrieved"])), ("korean", "한국어판", False, 4))
        self.assertIsInstance(korean["embed_seconds"], float)
        self.assertIsInstance(korean["search_seconds"], float)
        self.assertEqual(set(korean["retrieved"][0]),
                         {"rank", "chunk_id", "doc_id", "language", "distance", "lines", "line_start", "line_end", "tokens", "evidence"})
        # 가져온 목록은 겹침을 빼기 전 그대로이고, 순위는 그 검색어 안의 순위다
        self.assertEqual([c["rank"] for c in korean["retrieved"]], [1, 2, 3, 4])

    def test_hit_is_by_the_merged_list(self):
        # 근거 청크가 한국어판 3등: 원래 8개에는 없지만 합친 목록의 11번째(원래 8개 다음 한국어판 1, 2, 3등)에 든다
        searches = search_tables(**{"한국어판": rows("k", 4, evidence_at=(3,))})
        record, _, _ = merge_with(searches, [("korean", "한국어판")])
        self.assertEqual((record["hit"], record["hit_ranks"]), (True, [11]))
        self.assertEqual(record["merged"][10]["evidence"], [0])
        self.assertFalse(any(c["evidence"] for c in record["queries"][0]["retrieved"]))

    def test_evidence_below_the_top_four_is_not_hit(self):
        searches = search_tables(**{"한국어판": rows("k", 6, evidence_at=(5,))})
        record, _, _ = merge_with(searches, [("korean", "한국어판")])
        self.assertEqual((record["hit"], record["hit_ranks"]), (False, []))

    def test_evidence_in_original_is_hit_with_original_rank(self):
        searches = {ORIGINAL: rows("o", 16, evidence_at=(2,))}
        record, _, _ = merge_with(searches, [])
        self.assertEqual((record["hit"], record["hit_ranks"]), (True, [2]))

    def test_evidence_chunk_already_chosen_counts_once_at_original_rank(self):
        searches = {ORIGINAL: rows("o", 16, evidence_at=(2,)), "한국어판": [found_row("o2", evidence=True), found_row("k1")]}
        record, _, _ = merge_with(searches, [("korean", "한국어판")])
        self.assertEqual(record["hit_ranks"], [2])
        self.assertEqual(record["n_chunks"], 9)

    def test_evidence_is_counted_with_the_original_questions_evidence(self):
        # 한국어판 검색어로 가져와도 근거 번호는 원래 질문의 evidence로 매긴다
        searches = search_tables(**{"한국어판": [found_row("k1", evidence=True)]})
        record, _, _ = merge_with(searches, [("korean", "한국어판")])
        self.assertEqual(record["queries"][1]["retrieved"][0]["evidence"], [0])

    def test_comparison_retrieved_is_top_sixteen_of_the_original_question(self):
        with patched(None, search_tables()) as calls:
            rows16 = merge.comparison_retrieved(None, None, question(text=ORIGINAL))
        self.assertEqual(calls, [(ORIGINAL, 16)])
        self.assertEqual([c["chunk_id"] for c in rows16], [f"o{i}" for i in range(1, 17)])
        self.assertTrue(all("evidence" in c for c in rows16))


if __name__ == "__main__":
    unittest.main()
