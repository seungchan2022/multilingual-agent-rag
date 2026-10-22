"""recheck_step3.py 시험. 수는 파일에서 세고, 부딪히는 값 목록은 임시 파일로 만든다.

실행: .venv/bin/python -m unittest discover -s research_notes/stage2_values_rare_earth -p "test_*.py"
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recheck_step3 as rc  # noqa: E402

MD_DIR = rc.MD_DIR
KO_DYS = "wiki-ko-dysprosium"


def md_lines(doc_id):
    return rc.read_text(MD_DIR / f"{doc_id}.md").split("\n")


def run_with(entries, more=None):
    """항목들(대상 목록)로 임시 목록 파일을 만들어 재확인을 돌린다. {사실 번호: 결과}.
    more가 None이면 없는 confirm_more 파일을 가리킨다(진짜 confirm_more.json이 생겨도 시험이 흔들리지 않게). 리스트면 임시 파일로 쓴다."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "conflicts.json"
        path.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
        more_path = Path(tmp) / "confirm_more.json"
        if more is not None:
            more_path.write_text(json.dumps(more, ensure_ascii=False), encoding="utf-8")
        return {r["no"]: r for r in rc.run(path, more_path)}


def confirm_rows():
    return json.loads((rc.STEP3 / "confirm.json").read_text(encoding="utf-8"))


def more_record(base, **kw):
    """confirm.json 기록 base를 확인한 것으로 채운 confirm_more 기록."""
    m = {k: base[k] for k in ("no", "field", "lang", "side", "group", "in_table", "order_side")}
    m.update(read_ok=True, truth="그 언어에만", note="시험용 메모")
    m.update(kw)
    return m


def unconfirmed(lang="en"):
    """3 세기 때 확인하지 못한 희토류 한 쪽 기록 가운데 첫째."""
    return next(r for r in confirm_rows() if r["field"] == "rare_earth" and r["lang"] == lang and r["side"] == "one" and r["read_ok"] is None)


def entry(doc_id, places, quotes, values):
    return {"section": "시험", "text": "시험", "object": "x", "quantity": "x", "condition": "",
            "targets": [{"doc_id": doc_id, "quotes": quotes, "values": values, "places": places}]}


def dys_line():
    """디스프로슘의 "228 pm"과 "(계산값)"이 함께 있는 줄(1부터)과 그 글."""
    hits = [(i + 1, l) for i, l in enumerate(md_lines(KO_DYS)) if "228 pm" in l and "(계산값)" in l]
    assert len(hits) == 1, hits
    return hits[0]


class MappingTest(unittest.TestCase):
    def test_r_ko_010_maps_to_today_line(self):
        r = run_with([])["R-ko-010"]
        self.assertEqual(len(r["mentions"]), 1)
        m = r["mentions"][0]
        line, text = dys_line()
        self.assertEqual((m["status"], m["doc_id"], m["line"]), ("찾음", KO_DYS, line))
        self.assertIn("(계산값)", m["new_line"])
        self.assertEqual(m["new_line"], text)
        self.assertEqual(m["how"], "뒤 창")                       # 옛 줄에는 " / "가 없어 줄 전체는 맞지 않는다
        self.assertNotEqual(m["slot"], rc.NO_SLOT)

    def test_values_json_line_is_one_based_and_offsets_are_in_line(self):
        records = json.loads(rc.VALUES.read_text(encoding="utf-8"))
        cache = {}
        for r in records:
            lines = cache.setdefault(r["doc_id"], md_lines(r["doc_id"]))
            self.assertEqual(lines[r["line"] - 1][r["start"]:r["end"]], r["raw"], r["id"])

    def test_exact_line_and_window_and_missing(self):
        old = "가나다\n  - 길이: 175 pm (실험값) 228 pm (계산값)\n끝"
        start = old.index("228 pm")
        m = {"raw": "228 pm", "start": start, "end": start + 6, "line": 1}
        same = "머리\n  - 길이: 175 pm (실험값) 228 pm (계산값)\n끝"
        line, off, how = rc.locate(m, old, same)
        self.assertEqual((line, how), (2, "줄"))
        self.assertEqual(same.split("\n")[1][off:off + 6], "228 pm")
        changed = "머리\n  - 길이: 175 pm (실험값) / 228 pm (계산값)\n끝"
        line, off, how = rc.locate(m, old, changed)
        self.assertEqual((line, how), (2, "뒤 창"))
        self.assertEqual(changed.split("\n")[1][off:off + 6], "228 pm")
        twice = changed + "\n228 pm (계산값)"
        self.assertIsNone(rc.locate(m, old, twice)[0])            # 창이 두 번 나오면 짐작하지 않는다
        self.assertIsNone(rc.locate(m, old, "아무 상관 없는 글")[0])


class BlockingTest(unittest.TestCase):
    def test_baseline_without_conflicts_is_usable(self):
        r = run_with([])["R-ko-010"]
        self.assertTrue(r["A"] and r["B"])

    def test_fact_in_a_conflict_is_unusable_under_A_and_B(self):
        line, text = dys_line()
        e = entry(KO_DYS, [{"line": line, "label": "원자 반지름", "raw": "228 pm"}], [text], ["228"])
        r = run_with([e])["R-ko-010"]
        self.assertFalse(r["A"])
        self.assertFalse(r["B"])
        m = r["mentions"][0]
        self.assertEqual((m["A"], m["B"]), (rc.BLOCKED, rc.BLOCKED))

    def test_shared_value_only_blocks_B(self):
        # 같은 숫자 228만 가진 다른 줄을 대상으로 삼는다. 자리(places)와 quotes는 이 줄과 겹치지 않는다.
        line, _ = dys_line()
        e = entry(KO_DYS, [{"line": line + 1000, "label": "다른 곳", "raw": "228 pm"}], ["이 문서에 없는 줄"], ["228"])
        r = run_with([e])["R-ko-010"]
        self.assertTrue(r["A"])
        self.assertFalse(r["B"])
        self.assertEqual(r["mentions"][0]["B_reasons"], ["항목 1 값 228"])

    def test_B_value_rule_ignores_digit_neighbors(self):
        # 2288이나 22.8, 228.5 안의 228은 걸리지 않는다(원래 검사기의 정규식).
        self.assertEqual(rc.blocked_B("d", "값 2288 pm", [{"entry": 1, "doc_id": "d", "quotes": [], "values": ["228"]}]), [])
        self.assertEqual(rc.blocked_B("d", "값 228.5 pm", [{"entry": 1, "doc_id": "d", "quotes": [], "values": ["228"]}]), [])
        self.assertEqual(rc.blocked_B("d", "값 1,228 pm", [{"entry": 1, "doc_id": "d", "quotes": [], "values": ["1228"]}]), [(1, "값 1228")])
        self.assertEqual(rc.blocked_B("d", "줄  ", [{"entry": 2, "doc_id": "d", "quotes": ["줄"], "values": []}]), [(2, "자리")])
        self.assertEqual(rc.blocked_B("x", "줄", [{"entry": 2, "doc_id": "d", "quotes": ["줄"], "values": []}]), [])


class CountTest(unittest.TestCase):
    def test_confirmed_one_side_counts_match_confirm_json(self):
        rows = json.loads((rc.STEP3 / "confirm.json").read_text(encoding="utf-8"))
        results = run_with([])
        for lang in ("ko", "en"):
            want = [r for r in rows if r["field"] == "rare_earth" and r["lang"] == lang and r["side"] == "one"
                    and r["read_ok"] is True and r["truth"] == "그 언어에만"]
            got = rc.summarize(list(results.values()), lang)["확인됨"]
            self.assertEqual(got["사실"], len(want))
            self.assertEqual(got["표"], sum(1 for r in want if r["in_table"]))
            self.assertGreater(len(want), 0)

    def test_every_confirmed_fact_is_in_results(self):
        rows = json.loads((rc.STEP3 / "confirm.json").read_text(encoding="utf-8"))
        want = {r["no"] for r in rows if r["field"] == "rare_earth" and r["read_ok"] is True and r["truth"] == "그 언어에만"}
        self.assertEqual(set(run_with([])), want)


class ConfirmMoreTest(unittest.TestCase):
    def test_extra_record_adds_one_confirmed_fact(self):
        base = unconfirmed("en")
        before = run_with([])
        after = run_with([], [more_record(base)])
        self.assertEqual(len(after), len(before) + 1)
        self.assertEqual(set(after) - set(before), {base["no"]})
        self.assertEqual(after[base["no"]]["source"], rc.SRC_MORE)
        self.assertEqual(after[base["no"]]["note"], "시험용 메모")
        self.assertTrue(all(r["source"] == rc.SRC_STEP3 for no, r in after.items() if no != base["no"]))
        s0, s1 = rc.summarize(list(before.values()), "en"), rc.summarize(list(after.values()), "en")
        self.assertEqual(s1["확인됨"]["사실"], s0["확인됨"]["사실"] + 1)
        self.assertEqual(s1["확인됨"]["표"], s0["확인됨"]["표"] + int(base["in_table"]))
        self.assertEqual(s1["confirm_more 출처"]["사실"], 1)
        self.assertEqual(s0["confirm_more 출처"]["사실"], 0)
        self.assertEqual(rc.summarize(list(after.values()), "ko"), rc.summarize(list(before.values()), "ko"))

    def test_record_not_confirmed_true_is_not_counted(self):
        base = unconfirmed("en")
        after = run_with([], [more_record(base, read_ok=True, truth="반대 언어에 있음")])
        self.assertNotIn(base["no"], after)

    def test_missing_file_gives_same_counts(self):
        rows = [r for r in confirm_rows() if r["field"] == "rare_earth" and r["read_ok"] is True and r["truth"] == "그 언어에만"]
        self.assertEqual({r["no"] for r in rows}, {r["no"] for r in rc.confirmed_facts(HERE / "no_such_file.json")})

    def test_already_filled_record_is_error(self):
        filled = next(r for r in confirm_rows() if r["field"] == "rare_earth" and r["read_ok"] is True and r["side"] == "one")
        with self.assertRaises(SystemExit) as cm:
            run_with([], [more_record(filled)])
        self.assertIn(filled["no"], str(cm.exception))

    def test_unknown_no_is_error(self):
        with self.assertRaises(SystemExit) as cm:
            run_with([], [more_record(unconfirmed(), no="R-en-99999")])
        self.assertIn("R-en-99999", str(cm.exception))

    def test_changed_group_or_duplicate_is_error(self):
        base = unconfirmed()
        with self.assertRaises(SystemExit) as cm:
            run_with([], [more_record(base, group="en-one-xxx")])
        self.assertIn(base["no"], str(cm.exception))
        with self.assertRaises(SystemExit) as cm:
            run_with([], [more_record(base), more_record(base)])
        self.assertIn(base["no"], str(cm.exception))


if __name__ == "__main__":
    unittest.main()
