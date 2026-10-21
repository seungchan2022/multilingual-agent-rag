"""count_rule_check.py 시험. 네트워크와 저장된 결과 파일을 쓰지 않는다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import count_rule_check as cc
import make_short_test as mst


def cands(n):
    return [{"ko_title": f"주제{i:02d}", "en_title": f"T{i}"} for i in range(n)]


class Select(unittest.TestCase):
    def test_three_exclusions_and_counts(self):
        c = cands(20)
        new = {"주제00", "주제01"}
        prev = {"주제01", "주제02"}          # 주제01은 새 코퍼스에 먼저 걸려 한 번만 센다
        math = {"주제02", "주제03"}
        picked, dropped, skipped = cc.pick_heldout(c, new, prev, math)
        self.assertEqual(dropped, {"새 코퍼스의 주제": 2, "지난번 코퍼스의 주제": 1, "수식이 든 문서": 1})
        self.assertEqual(len(picked), 5)
        self.assertEqual(skipped, [])
        left = {x["ko_title"] for x in picked}
        self.assertFalse(left & (new | prev | math))

    def test_order_is_shuffled_sorted_titles(self):
        c = cands(12)
        picked, _, _ = cc.pick_heldout(list(reversed(c)), set(), set(), set())      # 들어온 차례가 달라도 같다
        want = mst.shuffled(sorted(c, key=lambda r: r["ko_title"]))[:5]
        self.assertEqual([x["ko_title"] for x in picked], [x["ko_title"] for x in want])

    def test_fewer_than_n_left(self):
        picked, _, _ = cc.pick_heldout(cands(3), set(), set(), set())
        self.assertEqual(len(picked), 3)


def fake_docs():
    ko = "지름은 5 km 이고 질량은 3 kg 이다.\n| 길이 | 7 m |"
    en = "The radius is 5 km.\nIt weighs 40 kg."
    sent = cc.rc.SENT
    return [{"id": 0, "lang": "ko", "title": "가", "revid": 1, "plain": ko, "tagged": ko.replace("| 길이 | 7 m |", f"| {sent}길이 | {sent}7 m |")},
            {"id": 1, "lang": "en", "title": "A", "revid": 2, "plain": en, "tagged": en}]


class Analyze(unittest.TestCase):
    def test_verdicts_and_table_flag(self):
        r = cc.analyze(fake_docs())
        ko = {g["mentions"][0]["raw"]: g for g in r["groups"]["ko"]}
        self.assertEqual(ko["5 km"]["verdict"], cc.SAME)
        self.assertEqual(ko["5 km"]["found"]["doc"], 1)
        self.assertEqual(ko["5 km"]["found"]["line"], 0)
        self.assertEqual(ko["3 kg"]["verdict"], cc.ONLY)
        self.assertFalse(ko["3 kg"]["in_table"])
        self.assertEqual(ko["7 m"]["verdict"], cc.ONLY)
        self.assertTrue(ko["7 m"]["in_table"])
        self.assertEqual(r["docs"][0]["chars"], len(fake_docs()[0]["plain"]))

    def test_line_count_mismatch_stops(self):
        d = fake_docs()
        d[0]["tagged"] += "\n추가"
        with self.assertRaises(SystemExit):
            cc.analyze(d)


def fake_res(n_ko_only, n_ko_present):
    def grp(lang, k, verdict):
        return {"id": f"{lang}{k}", "lang": lang, "verdict": verdict}
    groups = {"ko": [grp("ko", k, cc.ONLY) for k in range(n_ko_only)] + [grp("ko", n_ko_only + k, cc.SAME) for k in range(n_ko_present)],
              "en": [grp("en", k, cc.ONLY) for k in range(60)] + [grp("en", 60 + k, cc.MAYBE) for k in range(30)]}
    docs = [{"id": 0, "lang": "ko", "chars": 100}, {"id": 1, "lang": "ko", "chars": cc.FULL_MAX_CHARS + 1},
            {"id": 2, "lang": "en", "chars": cc.FULL_MAX_CHARS}, {"id": 3, "lang": "en", "chars": cc.FULL_MAX_CHARS + 1}]
    return {"bundles": {"A": {"x": {"groups": groups, "docs": docs}}, "B": {"y": {"groups": groups, "docs": docs}}}}


class Sample(unittest.TestCase):
    def test_same_input_same_sample(self):
        res = fake_res(60, 40)
        self.assertEqual(cc.draw(res), cc.draw(res))
        a = cc.draw(res)
        self.assertEqual(sum(1 for e in a["groups"] if e["stratum"] == "ko A 그 언어에만"), 25)
        self.assertEqual(sum(1 for e in a["groups"] if e["stratum"] == "ko B 있음 쪽"), 12)
        self.assertEqual(len(a["docs"]), 4)                              # 언어마다 묶음마다 하나
        self.assertEqual(a["shortage"], [])
        self.assertEqual([(d["stratum"], d["doc"]) for d in a["docs"]],     # 20,000자를 넘는 문서는 뽑히지 않고, 언어가 맞는 문서만
                         [("ko 문서 A", 0), ("ko 문서 B", 0), ("en 문서 A", 2), ("en 문서 B", 2)])

    def test_different_seed_differs(self):
        res = fake_res(60, 40)
        self.assertNotEqual(cc.draw(res)["groups"], cc.draw(res, seed=1)["groups"])

    def test_shortage_takes_all(self):
        res = fake_res(10, 5)
        a = cc.draw(res)
        ko_a = [e for e in a["groups"] if e["stratum"] == "ko A 그 언어에만"]
        self.assertEqual(len(ko_a), 10)
        self.assertEqual(sorted(e["group"] for e in ko_a), sorted(f"ko{k}" for k in range(10)))
        self.assertTrue(any("ko A 그 언어에만" in s for s in a["shortage"]))
        self.assertTrue(any("ko A 있음 쪽" in s for s in a["shortage"]))      # 5개뿐(13개를 못 채움)

    def test_order_in_sample_matches_declared(self):
        a = cc.draw(fake_res(60, 40))
        seen = []
        for e in a["groups"] + a["docs"]:
            if e["stratum"] not in seen:
                seen.append(e["stratum"])
        self.assertEqual(seen, list(cc.SAMPLE_ORDER))


class Rates(unittest.TestCase):
    def test_wilson_matches_hand_value(self):
        lo, hi = cc.wilson(5, 10)          # 손으로 계산: 중심 0.5, 구간 0.2366~0.7634
        self.assertAlmostEqual(lo, 0.2366, 3)
        self.assertAlmostEqual(hi, 0.7634, 3)
        lo, hi = cc.wilson(0, 10)          # 0/10: 0 ~ 0.2775
        self.assertAlmostEqual(lo, 0.0, 6)
        self.assertAlmostEqual(hi, 0.2775, 3)
        self.assertEqual(cc.wilson(0, 0), (None, None))

    def test_rates_rows(self):
        def only(no, lang, bundle, ok, truth):
            return {"no": no, "type": "only", "lang": lang, "bundle": bundle, "verdict": cc.ONLY, "read_ok": ok, "truth": truth, "note": ""}

        def present(no, lang, bundle, verdict, truth):
            return {"no": no, "type": "present", "lang": lang, "bundle": bundle, "verdict": verdict, "read_ok": True, "truth": truth, "note": ""}
        rows = [only("S1", "ko", "A", True, "그 언어에만"), only("S2", "ko", "A", False, "그 언어에만"),
                only("S3", "ko", "B", True, "반대 언어에 있음"), only("S4", "en", "A", True, "세는 범위의 수가 아님"),
                present("S5", "ko", "A", cc.SAME, "반대 언어에 없음"), present("S6", "ko", "A", cc.MAYBE, "같은 사실이 반대 언어에 있음"),
                present("S7", "en", "B", cc.MAYBE, "반대 언어에 없음")]
        st = cc.rates_rows(rows)
        self.assertEqual(st[("ko", "A")]["only"], (1, 2))        # read_ok false 하나
        self.assertEqual(st[("ko", "합")]["only"], (2, 3))       # + truth가 다른 것 하나
        self.assertEqual(st[("합", "합")]["only"], (3, 4))
        self.assertEqual(st[("ko", "A")]["present"], (1, 2))
        self.assertEqual(st[("ko", "A")]["by_verdict"], {cc.SAME: (1, 1), cc.MAYBE: (0, 1)})
        self.assertEqual(st[("합", "합")]["present"], (2, 3))
        self.assertEqual(st[("en", "B")]["by_verdict"][cc.MAYBE], (1, 1))

    def test_blank_stops(self):
        rows = [{"no": "S1", "type": "only", "read_ok": None, "truth": None, "note": None},
                {"no": "S2", "type": "present", "read_ok": True, "truth": "반대 언어에 없음", "note": ""},
                {"no": "S3", "type": "only", "read_ok": True, "truth": "엉뚱한 값", "note": ""},
                {"no": "D1", "type": "doc", "ai_list": None},
                {"no": "D2", "type": "doc", "ai_list": []}]
        self.assertEqual(cc.check_filled(rows), ["S1", "S3", "D1"])

    def test_compare_doc(self):
        rule = [{"line": 1, "raw": "5 km", "value": 5.0, "unit": "km", "dim": "길이"},
                {"line": 2, "raw": "3 kg", "value": 3.0, "unit": "kg", "dim": "질량"},
                {"line": 4, "raw": "9 m", "value": 9.0, "unit": "m", "dim": "길이"}]
        ai = [{"line": 1, "raw": "5 km", "value": 5.02, "unit": "km"},       # 1% 안: 맞음
              {"line": 2, "raw": "3 m", "value": 3.0, "unit": "m"},          # dim이 다름: 놓침
              {"line": 7, "raw": "8 s", "value": 8.0, "unit": "s"}]          # 규칙에 없음: 놓침
        matched, missed, wrong = cc.compare_doc(rule, ai)
        self.assertEqual(matched, 1)
        self.assertEqual([m["line"] for m in missed], [2, 7])
        self.assertEqual([w["line"] for w in wrong], [2, 4])


if __name__ == "__main__":
    unittest.main()
