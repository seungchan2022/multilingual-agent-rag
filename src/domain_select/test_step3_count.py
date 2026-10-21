"""step3_count.py 시험. 네트워크와 저장된 결과 파일을 쓰지 않는다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import step3_count as s3

SENT = s3.rc.SENT
SMALL = {"side": 2, "sum": 4, "table": 1, "model": 2}      # 시험용으로 줄인 필요한 수


def doc(i, lang, branch, text, outside=False, tagged=None):
    return {"id": i, "lang": lang, "title": f"문서{i}", "branch": branch, "outside_target": outside, "plain": text,
            "tagged": tagged if tagged is not None else text}


class Analyze(unittest.TestCase):
    def docs(self):
        ko_tab = "| 길이 | 7 m |"
        return [doc(0, "ko", s3.BOTH, "지름은 5 km 이다.\n질량은 3 kg 이다."),
                doc(1, "ko", s3.KO_ONLY, f"지름은 5 km 이다.\n{ko_tab}\n거리는 12345 m 이다.", outside=True,
                    tagged=f"지름은 5 km 이다.\n| {SENT}길이 | {SENT}7 m |\n거리는 12345 m 이다."),
                doc(2, "en", s3.BOTH, "The radius is 5 km."),
                doc(3, "en", s3.EN_ONLY, "It weighs 3 kg.\nCode 12345 zz.")]

    def test_groups_are_separate_per_side(self):
        r = s3.analyze(self.docs())
        self.assertEqual({lang: {s: len(g) for s, g in sides.items()} for lang, sides in r.items()},
                         {"ko": {"both": 2, "one": 3}, "en": {"both": 1, "one": 1}})
        five = [g for s in s3.SIDES for g in r["ko"][s] if g["mentions"][0]["raw"] == "5 km"]
        self.assertEqual(len(five), 2)                                   # 같은 값이 두 쪽에 다 있으면 쪽마다 하나씩
        self.assertEqual({g["side"] for g in five}, {"both", "one"})

    def test_judge_uses_all_opposite_docs(self):
        r = s3.analyze(self.docs())
        kg = next(g for g in r["ko"]["both"] if g["mentions"][0]["raw"] == "3 kg")
        self.assertEqual(kg["verdict"], s3.SAME)             # 영어 영어만 갈래 문서의 3 kg과도 견준다
        self.assertEqual(kg["found"]["doc"], 3)
        km = next(g for g in r["ko"]["both"] if g["mentions"][0]["raw"] == "5 km")
        self.assertEqual(km["found"]["doc"], 2)

    def test_not_compared_with_docs_outside_corpus(self):
        r = s3.analyze(self.docs()[:2])                      # 반대 언어 문서가 코퍼스에 없으면 견줄 곳이 없다
        self.assertTrue(all(g["verdict"] == s3.ONLY for sides in r["ko"].values() for g in sides))

    def test_maybe_is_not_candidate(self):
        r = s3.analyze(self.docs())
        m = next(g for g in r["ko"]["one"] if g["mentions"][0]["raw"] == "12345 m")
        self.assertEqual(m["verdict"], s3.MAYBE)
        orders = s3.make_orders(r["ko"], {d["id"]: d["title"] for d in self.docs()})
        ids = {g["id"] for name in orders for g in orders[name]}
        self.assertNotIn(m["id"], ids)

    def test_table_and_outside_flags(self):
        r = s3.analyze(self.docs())
        seven = next(g for g in r["ko"]["one"] if g["mentions"][0]["raw"] == "7 m")
        self.assertTrue(seven["in_table"])
        self.assertTrue(seven["outside_target"])
        three = next(g for g in r["ko"]["both"] if g["mentions"][0]["raw"] == "3 kg")
        self.assertFalse(three["in_table"] or three["outside_target"])

    def test_line_count_mismatch_stops(self):
        d = doc(0, "ko", s3.BOTH, "a 5 km\nb", tagged="a 5 km")
        with self.assertRaises(SystemExit):
            s3.analyze([d])


def grp(gid, side, doc_id, line, start, table=False, outside=False):
    return {"id": gid, "side": side, "verdict": s3.ONLY, "in_table": table, "outside_target": outside,
            "mentions": [{"doc": doc_id, "line": line, "start": start}]}


class Orders(unittest.TestCase):
    def groups(self):
        return {"both": [grp("b0", "both", 0, 3, 0), grp("b1", "both", 0, 1, 0, table=True), grp("b2", "both", 1, 0, 5)],
                "one": [grp(f"o{i}", "one", 2, i, 0, table=i % 2 == 0, outside=i % 3 == 0) for i in range(8)]}

    def test_same_input_same_order_whatever_the_input_order(self):
        titles = {0: "나", 1: "가", 2: "다"}
        a = s3.make_orders(self.groups(), titles)
        g = self.groups()
        g = {s: list(reversed(v)) for s, v in g.items()}
        b = s3.make_orders(g, titles)
        self.assertEqual({k: [x["id"] for x in v] for k, v in a.items()}, {k: [x["id"] for x in v] for k, v in b.items()})

    def test_four_orders_hold_the_right_candidates(self):
        o = s3.make_orders(self.groups(), {0: "나", 1: "가", 2: "다"})
        self.assertEqual(sorted(g["id"] for g in o["both"]), ["b0", "b1", "b2"])
        self.assertEqual(sorted(g["id"] for g in o["table"]), ["b1", "o0", "o2", "o4", "o6"])
        self.assertEqual(sorted(g["id"] for g in o["model"]), ["o0", "o3", "o6"])

    def test_shuffle_follows_the_sorted_list(self):
        titles = {0: "나", 1: "가", 2: "다"}
        o = s3.make_orders(self.groups(), titles)
        want = s3.shuffled(sorted(self.groups()["one"], key=lambda g: (titles[g["mentions"][0]["doc"]], g["mentions"][0]["line"], 0, g["id"])))
        self.assertEqual([g["id"] for g in o["one"]], [g["id"] for g in want])

    def test_confirm_numbers_follow_side_orders(self):
        o = s3.make_orders(self.groups(), {0: "나", 1: "가", 2: "다"})
        es = s3.make_confirm("rare_earth", "en", o)
        self.assertEqual([e["no"] for e in es], [f"R-en-{i:03d}" for i in range(1, 12)])
        self.assertEqual([e["group"] for e in es[:3]], [g["id"] for g in o["both"]])
        self.assertEqual([e["side"] for e in es], ["both"] * 3 + ["one"] * 8)
        self.assertEqual([e["order_side"] for e in es], [1, 2, 3] + list(range(1, 9)))
        by = {e["group"]: e for e in es}
        self.assertEqual(sorted(e["order_table"] for e in es if e["order_table"]), [1, 2, 3, 4, 5])
        self.assertEqual(by["o1"]["order_table"], None)
        self.assertEqual(by["o3"]["order_model"] is not None, True)
        self.assertTrue(all(e["read_ok"] is None and e["truth"] is None and e["note"] is None for e in es))


def E(no, side="both", os=None, ot=None, om=None, state="u", field="exoplanets", lang="ko", table=False):
    e = {"no": no, "field": field, "lang": lang, "side": side, "group": no, "in_table": table, "outside_target": om is not None,
         "order_side": os, "order_table": ot, "order_model": om, "read_ok": None, "truth": None, "note": None}
    if state == "c":
        e["read_ok"], e["truth"] = True, s3.ONLY
    elif state == "w":
        e["read_ok"], e["truth"] = True, "반대 언어에 있음"
    elif state == "r":
        e["read_ok"], e["truth"] = False, s3.ONLY
    return e


def cfg(field, lang, one="cc"):
    """통과하는 모양(SMALL 기준). 두 언어 쪽 c w c u, 한쪽 언어 쪽 one, 표 1개(맞음), 모델 시험 둘(맞음)."""
    p = f"{field[0]}{lang}"
    es = [E(p + "1", "both", os=1, ot=1, om=1, state="c", field=field, lang=lang, table=True),
          E(p + "2", "both", os=2, state="w", field=field, lang=lang),
          E(p + "3", "both", os=3, state="c", field=field, lang=lang),
          E(p + "4", "both", os=4, field=field, lang=lang)]
    for i, ch in enumerate(one, 1):
        es.append(E(f"{p}x{i}", "one", os=i, om=2 if i == 1 else None, state=ch, field=field, lang=lang))
    return es


class Status(unittest.TestCase):
    def test_empty_confirm(self):
        s = s3.make_status([E("a1", os=1), E("a2", os=2)], SMALL)["exoplanets"]["ko"]["both"]
        self.assertEqual((s["correct"], s["filled"], s["total"], s["stopped"], s["exhausted"]), (0, 0, 2, False, False))
        self.assertEqual(s["next"], ["a1", "a2"])

    def test_gap_is_reported(self):
        order = [E("a1", os=1, state="c"), E("a2", os=2), E("a3", os=3, state="w"), E("a4", os=4)]
        s = s3.quota(order, 2)
        self.assertEqual(s["gaps"], ["a2"])
        self.assertEqual((s["prefix"], s["prefix_correct"]), (1, 1))
        self.assertEqual(s["next"], ["a2", "a4"])

    def test_stops_when_side_reaches_need(self):
        order = [E("a1", os=1, state="c"), E("a2", os=2, state="r"), E("a3", os=3, state="c"), E("a4", os=4)]
        s = s3.quota(order, 2)
        self.assertEqual((s["correct"], s["stopped"], s["exhausted"], s["next"]), (2, True, False, []))   # read_ok가 false면 맞은 것이 아니다

    def test_exhausted(self):
        s = s3.quota([E("a1", os=1, state="w"), E("a2", os=2, state="r")], 2)
        self.assertEqual((s["correct"], s["stopped"], s["exhausted"]), (0, False, True))

    def test_table_counts_filled_in_other_order(self):
        es = [E("a1", os=1, ot=2, table=True, state="c"), E("a2", os=2, ot=1, table=True)]       # 표 차례의 첫 자리는 비었고 둘째는 쪽 차례에서 채움
        s = s3.make_status(es, SMALL)["exoplanets"]["ko"]
        self.assertEqual((s["table"]["correct"], s["table"]["stopped"], s["table"]["next"]), (1, True, []))
        s = s3.make_status(es, {**SMALL, "table": 2})["exoplanets"]["ko"]["table"]
        self.assertEqual((s["stopped"], s["next"], s["gaps"]), (False, ["a2"], ["a2"]))

    def test_model_values_stop_at_five_style_need(self):
        es = [E(f"m{i}", os=i, om=i, state="c" if i != 2 else "w") for i in range(1, 4)]
        s = s3.make_status(es, SMALL)["exoplanets"]["ko"]["model"]
        self.assertEqual((s["correct"], s["stopped"]), (2, True))

    def test_out_of_range_value_stops(self):
        bad = E("a1", os=1)
        bad["truth"] = "아무 말"
        with self.assertRaises(SystemExit):
            s3.check_confirm([bad])

    def test_unfinished_lists_open_quotas_and_gaps(self):
        es = [e for f in s3.FIELDS for lang in s3.LANGS for e in cfg(f, lang)]
        self.assertEqual(s3.unfinished(s3.make_status(es, SMALL)), [])
        es[0]["read_ok"] = es[0]["truth"] = None                         # 첫 번호를 비우면 두 언어 쪽이 멈추지 않고 표와 모델도 영향을 받는다
        self.assertTrue(s3.unfinished(s3.make_status(es, SMALL)))


class Judge(unittest.TestCase):
    def test_pass_and_estimates_by_hand(self):
        es = [e for f in s3.FIELDS for lang in s3.LANGS for e in cfg(f, lang)]
        r = s3.judge_all(s3.make_status(es, SMALL), SMALL)["exoplanets"]
        ko = r["quotas"]["ko"]
        self.assertAlmostEqual(ko["both"]["estimate"], 4 * 2 / 3)        # 후보 4 × 앞 3개 가운데 맞은 2
        self.assertAlmostEqual(ko["one"]["estimate"], 2.0)
        self.assertAlmostEqual(ko["sum"]["estimate"], 4 * 2 / 3 + 2)
        self.assertEqual((ko["sum"]["correct"], ko["sum"]["need"]), (4, 4))
        self.assertAlmostEqual(ko["table"]["estimate"], 1.0)
        self.assertTrue(r["passed"])
        self.assertAlmostEqual(r["reserve"], 1.0)                        # 여덟 몫의 어림÷필요 가운데 가장 낮은 것(한쪽 언어 쪽 2÷2, 표 1÷1)

    def test_fail_when_one_quota_is_short(self):
        es = [e for f in s3.FIELDS for lang in s3.LANGS for e in cfg(f, lang, one="c" if (f, lang) == ("rare_earth", "ko") else "cc")]
        status = s3.make_status(es, SMALL)
        self.assertEqual(s3.unfinished(status), [])                      # 후보가 다 떨어졌으므로 judge를 할 수 있다
        res = s3.judge_all(status, SMALL)
        self.assertTrue(res["exoplanets"]["passed"])
        r = res["rare_earth"]
        self.assertFalse(r["passed"])
        ko = r["quotas"]["ko"]
        self.assertEqual((ko["one"]["ok"], ko["sum"]["ok"], ko["both"]["ok"], ko["table"]["ok"]), (False, False, True, True))
        self.assertAlmostEqual(ko["sum"]["estimate"], 4 * 2 / 3 + 1)
        self.assertAlmostEqual(r["reserve"], 0.5)                        # 한쪽 언어 쪽 1÷2

    def test_model_values_first_n_correct(self):
        res_field = {"docs": [{"id": 0, "title": "대상 문서", "outside_target": False}, {"id": 1, "title": "②문서", "outside_target": True}],
                     "groups": {"ko": {"both": [], "one": [
                         {"id": f"g{i}", "mentions": [{"doc": 0, "raw": "a", "line": 1}, {"doc": 1, "raw": f"{i} km", "line": i}]} for i in range(4)]}, "en": {"both": [], "one": []}}}
        order = [E(f"n{i}", os=i, om=i, state="w" if i == 1 else "c") for i in range(4)]
        for e in order:
            e["group"] = f"g{e['order_model']}"
        v = s3.model_values(order, res_field, 2)
        self.assertEqual([x["no"] for x in v], ["n0", "n2"])
        self.assertEqual(v[1], {"no": "n2", "title": "②문서", "raw": "2 km", "line": 2})


if __name__ == "__main__":
    unittest.main()
