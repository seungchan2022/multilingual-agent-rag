"""field_scope.py 시험. 네트워크를 쓰지 않는다(api·get을 가짜로 바꾼다)."""
import gzip
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import field_scope as fs


# --- 분류 걷기 ---------------------------------------------------------------------

GRAPH = {
    "분류:R": {"page": ["a"], "subcat": ["분류:S1", "분류:S2"]},
    "분류:S1": {"page": ["b", "c"], "subcat": ["분류:T"]},
    "분류:S2": {"page": ["c"], "subcat": ["분류:T", "분류:R"]},      # R로 되돌아가는 순환
    "분류:T": {"page": ["d", "b"], "subcat": ["분류:U"]},            # 깊이 2. 하위 분류 U는 보지 않는다
    "분류:U": {"page": ["z"], "subcat": []},
    "분류:ADD": {"page": ["x", "a"], "subcat": ["분류:ADD2"]},
    "분류:ADD2": {"page": ["w"], "subcat": []},
}


def graph_api(calls):
    """항목을 한 번에 하나씩만 주고 continue로 잇는 가짜 API."""
    def api(lang, **p):
        calls.append(p)
        items = GRAPH[p["cmtitle"]][p["cmtype"]]
        i = int(p.get("cmcontinue", 0))
        d = {"query": {"categorymembers": [{"title": items[i]}] if items else []}}
        if i + 1 < len(items):
            d["continue"] = {"cmcontinue": str(i + 1), "continue": "-||"}
        return d
    return api


class Walk(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.cats = fs.walk(["분류:R"], graph_api(self.calls))

    def test_depths_and_cycle_visited_once(self):
        self.assertEqual({c: v["depth"] for c, v in self.cats.items()}, {"분류:R": 0, "분류:S1": 1, "분류:S2": 1, "분류:T": 2})
        self.assertEqual(sum(1 for p in self.calls if p["cmtitle"] == "분류:R" and p["cmtype"] == "page"), 1)

    def test_no_subcategory_listing_below_depth_2(self):
        self.assertIsNone(self.cats["분류:T"]["subcats"])
        self.assertFalse(any(p["cmtitle"] == "분류:U" for p in self.calls))
        self.assertFalse(any(p["cmtitle"] == "분류:T" and p["cmtype"] == "subcat" for p in self.calls))
        self.assertTrue(any(p["cmtitle"] == "분류:T" and p["cmtype"] == "page" for p in self.calls))    # 깊이 2의 문서는 본다

    def test_continue_followed_to_the_end(self):
        self.assertEqual(self.cats["분류:S1"]["pages"], ["b", "c"])
        self.assertEqual(self.cats["분류:R"]["subcats"], ["분류:S1", "분류:S2"])

    def test_only_main_namespace_pages(self):
        pages = [p for p in self.calls if p["cmtype"] == "page"]
        self.assertTrue(pages and all(p["cmnamespace"] == 0 for p in pages))
        self.assertTrue(all("cmnamespace" not in p for p in self.calls if p["cmtype"] == "subcat"))

    def test_api_error_raises(self):
        with self.assertRaises(RuntimeError):
            fs.members(lambda lang, **p: {"error": {"code": "x"}}, "분류:R", "page", 0)


# --- 범위 ---------------------------------------------------------------------------

def tree_of(cats, add_cats=None, add_pages=None):
    return {"field": "f", "categories": cats, "additions": {"categories": add_cats or {}, "pages": add_pages or []}}


class Scope(unittest.TestCase):
    def tree(self, **kw):
        cats = fs.walk(["분류:R"], graph_api([]))
        return tree_of(cats, **kw)

    def by_title(self, scope):
        return {r["ko_title"]: r for r in scope["included"]}

    def test_smallest_depth_and_via(self):
        s = self.by_title(fs.build_scope(self.tree(), None, []))
        self.assertEqual((s["b"]["depth"], s["b"]["via"]), (1, ["분류:S1"]))              # 깊이 1과 2에 있으면 1
        self.assertEqual((s["c"]["depth"], s["c"]["via"]), (1, ["분류:S1", "분류:S2"]))   # 같은 깊이의 분류는 모두 적는다
        self.assertEqual((s["a"]["depth"], s["a"]["via"]), (0, ["분류:R"]))
        self.assertEqual((s["d"]["depth"], s["d"]["via"]), (2, ["분류:T"]))

    def test_order_depth_then_title(self):
        sc_ = fs.build_scope(self.tree(add_pages=["가"]), None, [])
        self.assertEqual([r["ko_title"] for r in sc_["included"]], ["a", "b", "c", "d", "가"])

    def test_addition_new_page_and_existing_page(self):
        s = self.by_title(fs.build_scope(self.tree(add_cats={"분류:ADD": ["x", "a"]}, add_pages=["희토류"]), None, []))
        self.assertEqual((s["x"]["depth"], s["x"]["via"]), (None, ["더함: 분류:ADD"]))
        self.assertEqual((s["a"]["depth"], s["a"]["via"]), (0, ["분류:R", "더함: 분류:ADD"]))    # 이미 있으면 깊이는 그대로
        self.assertEqual((s["희토류"]["depth"], s["희토류"]["via"]), (None, ["더함: 문서"]))
        self.assertNotIn("w", s)                                                                  # 더하는 분류의 하위 분류는 안 본다

    def test_addition_label_not_repeated(self):
        s = self.by_title(fs.build_scope(self.tree(add_cats={"분류:ADD": ["x", "x"]}), None, []))
        self.assertEqual(s["x"]["via"], ["더함: 분류:ADD"])

    def test_exclusion_regex_examples(self):
        ex = fs.FIELDS["rare_earth"]["exclude"]
        drop = ["유로퓸-152", "가돌리늄-141m", "터븀-154m2"]
        keep = ["유로퓸 동위 원소", "사마륨-코발트 자석", "아연-세륨 전지", "이트륨 바륨 구리 산화물"]
        s = fs.build_scope(tree_of({"분류:R": {"depth": 0, "pages": drop + keep, "subcats": []}}), ex, [])
        self.assertEqual([r["ko_title"] for r in s["excluded"]], sorted(drop))
        self.assertTrue(all(r["reason"] == ex["reason"] for r in s["excluded"]))
        self.assertEqual(sorted(r["ko_title"] for r in s["included"]), sorted(keep))

    def test_exclusion_applies_to_added_pages_and_not_to_exoplanets(self):
        tree = tree_of({"분류:R": {"depth": 0, "pages": ["케플러-22", "A-1"], "subcats": []}}, add_pages=["유로퓸-152"])
        self.assertEqual(len(fs.build_scope(tree, fs.FIELDS["rare_earth"]["exclude"], [])["excluded"]), 3)
        self.assertIsNone(fs.FIELDS["exoplanets"]["exclude"])
        s = fs.build_scope(tree, fs.FIELDS["exoplanets"]["exclude"], [])
        self.assertEqual((len(s["included"]), s["excluded"]), (3, []))

    def test_config_regex_is_the_spec_regex(self):
        self.assertEqual(fs.FIELDS["rare_earth"]["exclude"]["regex"], r"^\S+-\d+m?\d*$")

    def test_missing_targets_reported_not_crashing(self):
        tree = tree_of({"분류:R": {"depth": 0, "pages": ["a", "유로퓸-152"], "subcats": []}})
        s = fs.build_scope(tree, fs.FIELDS["rare_earth"]["exclude"], ["a", "유로퓸-152", "없는 문서"])
        self.assertEqual(s["missing_targets"], ["유로퓸-152", "없는 문서"])     # 범위 밖이거나 뺀 대상도 보고한다

    def test_cmd_tree_and_scope_files(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            cfg = {"ko_name": "시험", "roots": ["분류:R"], "add_categories": ["분류:ADD"], "add_pages": ["문서"], "exclude": None}
            calls = []
            with mock.patch.dict(fs.FIELDS, {"t": cfg}):
                fs.cmd_tree("t", api=graph_api(calls), out=out)
                tree = fs.read_json(out / "t" / "tree.json")
                self.assertEqual((tree["roots"], tree["max_depth"], tree["additions"]["categories"]), (["분류:R"], 2, {"분류:ADD": ["x", "a"]}))
                self.assertRegex(tree["fetched_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00$")
                self.assertFalse(any(p["cmtitle"] == "분류:ADD" and p["cmtype"] == "subcat" for p in calls))
                fs.cmd_scope("t", out=out, targets=["a", "없음"])
            scope = fs.read_json(out / "t" / "scope.json")
            self.assertEqual(scope["missing_targets"], ["없음"])
            self.assertEqual({r["ko_title"] for r in scope["included"]}, {"a", "b", "c", "d", "x", "문서"})


# --- 영어 짝 ------------------------------------------------------------------------

class LangPairs(unittest.TestCase):
    def test_batches_of_50(self):
        calls = []

        def api(lang, **p):
            calls.append(p)
            return {"query": {"pages": [{"title": t, "langlinks": [{"lang": "en", "title": "E " + t}]} for t in p["titles"].split("|")]}}
        titles = [f"T{i}" for i in range(120)]
        pairs = fs.lang_pairs(titles, api)
        self.assertEqual([len(p["titles"].split("|")) for p in calls], [50, 50, 20])
        self.assertTrue(all(p["lllang"] == "en" and p["prop"] == "langlinks" and p["redirects"] == 1 for p in calls))
        self.assertEqual(pairs["T119"], "E T119")
        self.assertEqual(len(pairs), 120)

    def test_normalized_redirect_missing_and_no_langlink(self):
        resp = {"query": {"normalized": [{"from": "가_나", "to": "가 나"}], "redirects": [{"from": "가 나", "to": "다"}],
                          "pages": [{"title": "다", "langlinks": [{"lang": "en", "title": "Da"}]},
                                    {"title": "없음", "missing": True}, {"title": "짝없음"}]}}
        pairs = fs.lang_pairs(["가_나", "없음", "짝없음", "다"], lambda lang, **p: resp)
        self.assertEqual(pairs, {"가_나": "Da", "없음": None, "짝없음": None, "다": "Da"})

    def test_langlinks_continue_followed(self):
        seq = [{"query": {"pages": [{"title": "가"}]}, "continue": {"llcontinue": "x", "continue": "||"}},
               {"query": {"pages": [{"title": "가", "langlinks": [{"lang": "en", "title": "Ga"}]}]}}]
        calls = []

        def api(lang, **p):
            calls.append(p)
            return seq[len(calls) - 1]
        self.assertEqual(fs.lang_pairs(["가"], api), {"가": "Ga"})
        self.assertEqual(calls[1]["llcontinue"], "x")


# --- 요청 머리 ----------------------------------------------------------------------

class Requests(unittest.TestCase):
    def test_headers_url_and_gap(self):
        seen = {}

        def fake_get(url, headers, busy=None):
            seen.update(url=url, headers=headers, busy=busy)
            return b'{"query": {}}'
        with mock.patch.object(fs, "get", fake_get), mock.patch.object(fs.time, "sleep") as sleep:
            fs.api("en", action="parse", page="Europium")
        self.assertEqual(seen["headers"], {"User-Agent": fs.UA, "Accept-Encoding": "gzip"})
        self.assertEqual(fs.UA, "MultilingualAgentRAG-corpus/1.0 (https://github.com/seungchan2022/multilingual-agent-rag)")
        self.assertTrue(seen["url"].startswith("https://en.wikipedia.org/w/api.php?"))
        self.assertIn("maxlag=5", seen["url"])
        self.assertIs(seen["busy"], fs.busy)
        self.assertNotIn("@", seen["url"] + "".join(seen["headers"].values()))
        sleep.assert_called_once_with(fs.GAP)

    def test_busy_only_for_maxlag(self):
        self.assertEqual(fs.busy(b'{"error": {"code": "maxlag"}}', {"Retry-After": "7"}), 7)
        self.assertEqual(fs.busy(b'{"error": {"code": "maxlag"}}', {}), 5)
        self.assertIsNone(fs.busy(b'{"error": {"code": "missingtitle"}}', {}))
        self.assertIsNone(fs.busy(b'{"parse": {}}', {}))
        self.assertIsNone(fs.busy(b"<html>", {}))


# --- 받기와 세기 ---------------------------------------------------------------------

HTML = ('<div class="mw-parser-output"><p>본문 글</p><table class="wikitable"><tr><th>머리</th><th>값</th></tr>'
        '<tr><td>1</td><td>2</td></tr></table></div>')
HTML_EN = '<div class="mw-parser-output"><p>abcde</p></div>'


def parse_api(calls, bad=("Bad",)):
    revs = {"Good": 11, "Good-en": 12, "Bad": 13}

    def api(lang, **p):
        calls.append((lang, p["page"]))
        assert p["action"] == "parse" and p["prop"] == "text|revid" and p["redirects"] == 1
        t = p["page"]
        if t in bad:
            return {"error": {"code": "missingtitle"}}
        return {"parse": {"title": t + " (넘겨받음)", "revid": revs[t], "text": HTML if lang == "ko" else HTML_EN}}
    return api


def prepare(out, field="t"):
    base = out / field
    fs.write_json(base / "scope.json", {"field": field, "included": [
        {"ko_title": "Good", "depth": 0, "via": ["분류:R"]}, {"ko_title": "Bad", "depth": 1, "via": ["분류:S"]}], "excluded": [],
        "missing_targets": []})
    fs.write_json(base / "langlinks.json", {"fetched_at": "x", "pairs": {"Good": "Good-en", "Bad": None}})
    return base


class FetchCount(unittest.TestCase):
    def test_fetch_log_cache_resume_and_error_continue(self):
        with tempfile.TemporaryDirectory() as d:
            base = prepare(Path(d))
            calls = []
            fs.cmd_fetch("t", api=parse_api(calls), out=Path(d))
            self.assertEqual(calls, [("ko", "Good"), ("ko", "Bad"), ("en", "Good-en")])     # 오류 뒤에도 계속한다
            recs = [json.loads(l) for l in (base / "fetched.jsonl").read_text(encoding="utf-8").splitlines()]
            self.assertEqual([(r["lang"], r["title_requested"]) for r in recs], [("ko", "Good"), ("ko", "Bad"), ("en", "Good-en")])
            self.assertEqual((recs[0]["title"], recs[0]["revid"], recs[0]["file"]), ("Good (넘겨받음)", 11, "cache/ko_11.html.gz"))
            self.assertEqual(set(recs[0]), {"lang", "title_requested", "title", "revid", "fetched_at", "file"})
            self.assertEqual(recs[1]["error"], "missingtitle")
            self.assertEqual(gzip.decompress((base / "cache" / "ko_11.html.gz").read_bytes()).decode("utf-8"), HTML)
            calls2 = []
            fs.cmd_fetch("t", api=parse_api(calls2), out=Path(d))
            self.assertEqual(calls2, [("ko", "Bad")])       # 받은 것은 건너뛰고 오류였던 것만 다시 받는다
            self.assertEqual(len((base / "fetched.jsonl").read_text(encoding="utf-8").splitlines()), 4)

    def test_fetch_needs_langlinks_for_every_page(self):
        with tempfile.TemporaryDirectory() as d:
            base = prepare(Path(d))
            fs.write_json(base / "langlinks.json", {"fetched_at": "x", "pairs": {"Good": None}})
            with self.assertRaises(SystemExit):
                fs.cmd_fetch("t", api=parse_api([]), out=Path(d))

    def test_count_reads_gzip_cache_and_calls_measure(self):
        with tempfile.TemporaryDirectory() as d:
            base = prepare(Path(d))
            fs.cmd_fetch("t", api=parse_api([]), out=Path(d))
            fs.cmd_count("t", out=Path(d))
            good, bad = fs.read_json(base / "results.json")
            self.assertEqual(list(good), ["ko_title", "depth", "via", "en_title", "ko_revid", "ko_chars", "ko_n_tables", "ko_tables",
                                          "en_revid", "en_chars", "en_n_tables", "en_tables", "errors"])
            m = fs.sc.measure(HTML)
            self.assertEqual((good["ko_revid"], good["ko_chars"], good["ko_n_tables"], good["ko_tables"]), (11, m["chars"], 1, m["tables"]))
            self.assertEqual((good["en_title"], good["en_revid"], good["en_chars"], good["en_n_tables"]), ("Good-en", 12, 5, 0))
            self.assertEqual(good["errors"], [])
            self.assertEqual((bad["ko_revid"], bad["ko_chars"], bad["ko_tables"], bad["errors"]), (None, None, None, ["ko: missingtitle"]))
            self.assertEqual((bad["en_title"], bad["en_chars"], bad["errors"]), (None, None, ["ko: missingtitle"]))

    def test_count_marks_unfetched(self):
        with tempfile.TemporaryDirectory() as d:
            base = prepare(Path(d))
            fs.cmd_count("t", out=Path(d))
            good = fs.read_json(base / "results.json")[0]
            self.assertEqual(good["errors"], ["ko: 받지 않음", "en: 받지 않음"])


# --- summary와 verify ---------------------------------------------------------------

def row(title, depth, en, kc, kt, ec, et, errors=(), heads=()):
    return {"ko_title": title, "depth": depth, "via": ["분류:R"], "en_title": en, "ko_revid": 1, "ko_chars": kc, "ko_n_tables": kt,
            "ko_tables": None if kt is None else [{"rows": 2, "head": h, "cls": "wikitable"} for h in heads],
            "en_revid": 2 if ec is not None else None, "en_chars": ec, "en_n_tables": et, "en_tables": None, "errors": list(errors)}


ROWS = [row("A", 0, "A-en", 100, 1, 200, 2, heads=["머리 | 값"]), row("B", 1, "B-en", 300, 0, 400, 0), row("C", 2, None, 500, 0, None, None),
        row("D", None, "D-en", 700, 3, None, None, errors=["en: 받지 않음"], heads=["x", "y", "z"])]
SCOPE = {"field": "t", "included": [{"ko_title": r["ko_title"]} for r in ROWS], "excluded": [{"ko_title": "e1"}, {"ko_title": "e2"}],
         "missing_targets": ["X"]}


class Summary(unittest.TestCase):
    def test_numbers_hand_computed(self):
        n = fs.numbers(ROWS, SCOPE)
        self.assertEqual(n, {"ko_pages": 4, "depth_0": 1, "depth_1": 1, "depth_2": 1, "added": 1, "excluded": 2, "en_yes": 3, "en_no": 1,
                             "ko_with_table": 2, "ko_tables": 4, "en_with_table": 1, "en_tables": 2,
                             "ko_median": 400, "en_median": 300, "fetch_errors": 1, "missing_targets": ["X"]})

    def test_median_none_when_no_pairs(self):
        n = fs.numbers([row("A", 0, None, 100, 0, None, None)], {"excluded": [], "missing_targets": []})
        self.assertEqual((n["en_median"], n["en_yes"], n["en_no"]), (None, 0, 1))
        self.assertIn("| 영어 짝 본문 길이 중앙값 | 없음 |", fs.render_summary({"exoplanets": n}))

    def write_both(self, out, rows=ROWS):
        for f in fs.FIELDS:
            fs.write_json(out / f / "results.json", rows)
            fs.write_json(out / f / "scope.json", SCOPE)

    def test_summary_files_and_verify_detects_change(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            self.write_both(out)
            with mock.patch("builtins.print"):
                fs.cmd_summary(out)
                self.assertTrue(fs.cmd_verify(out))
            text = (out / "summary.md").read_text(encoding="utf-8")
            self.assertIn("| 범위 안 한국어 문서 | 4 |", text)
            self.assertIn("| 한국어 본문 길이 중앙값 | 400 |", text)
            self.assertIn("시험 대상 10개 가운데 범위 밖: X", text)
            docs = (out / "exoplanets" / "docs.md").read_text(encoding="utf-8").splitlines()
            self.assertEqual(docs[4], "| A | 0 | 분류:R | A-en | 100 | 1 | 200 | 2 | 머리 \\| 값 |")
            self.assertEqual([l.split(" | ")[0] for l in docs[4:]], ["| A", "| B", "| C", "| D"])    # 깊이 차례, 더한 문서는 맨 뒤
            self.assertIn("| C | 2 | 분류:R | 없음 | 500 | 0 |  |  | ", "\n".join(docs))
            nums = fs.read_json(out / "summary_numbers.json")
            self.assertEqual(nums["rare_earth"]["ko_tables"], 4)
            nums["rare_earth"]["ko_tables"] = 5                              # 숫자 하나를 손으로 바꾼다
            fs.write_json(out / "summary_numbers.json", nums)
            with mock.patch("builtins.print") as pr:
                self.assertFalse(fs.cmd_verify(out))
            self.assertIn("summary_numbers.json", pr.call_args[0][0])

    def test_verify_detects_changed_results_and_markdown(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            self.write_both(out)
            with mock.patch("builtins.print"):
                fs.cmd_summary(out)
                text = (out / "summary.md").read_text(encoding="utf-8")
                (out / "summary.md").write_text(text.replace("| 4 |", "| 5 |", 1), encoding="utf-8")
                self.assertFalse(fs.cmd_verify(out))
                fs.cmd_summary(out)
                changed = [dict(r) for r in ROWS]
                changed[0]["ko_chars"] = 9999
                fs.write_json(out / "exoplanets" / "results.json", changed)
                self.assertFalse(fs.cmd_verify(out))

    def test_results_and_scope_must_list_same_pages(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            self.write_both(out, ROWS[:3])
            with self.assertRaises(SystemExit):
                fs.cmd_summary(out)


class Config(unittest.TestCase):
    def test_fields_match_decision_line(self):
        self.assertEqual(list(fs.FIELDS), ["exoplanets", "rare_earth"])
        self.assertEqual(fs.FIELDS["exoplanets"]["roots"], ["분류:외계 행성"])
        self.assertEqual(fs.FIELDS["rare_earth"]["roots"], ["분류:란타넘족", "분류:스칸듐", "분류:이트륨"])
        self.assertEqual(fs.FIELDS["exoplanets"]["add_categories"], ["분류:외계행성학"])
        self.assertEqual((fs.FIELDS["rare_earth"]["add_categories"], fs.FIELDS["rare_earth"]["add_pages"]), (["분류:희토류 합금"], ["희토류 원소"]))
        self.assertEqual(fs.MAX_DEPTH, 2)


if __name__ == "__main__":
    unittest.main()
