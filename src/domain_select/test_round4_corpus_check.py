"""round4_corpus_check.py 시험. 네트워크를 쓰지 않는다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import round4_corpus_check as rc


def page(body):
    return f'<div class="mw-parser-output">{body}</div>'


INFOBOX = ('<table class="infobox"><tr><th>이름</th><td><a href="/wiki/원자_번호">원자 번호</a> 63</td></tr>'
           '<tr><td colspan="2"><table><tr><td><a href="/wiki/수소">수소</a></td></tr></table></td></tr></table>')


class Links(unittest.TestCase):
    def links(self, body, **kw):
        return rc.collect_links(page(body), **kw)

    def test_namespaces_dropped(self):
        body = ('<p><a href="/wiki/%EB%B6%84%EB%A5%98:%ED%99%94%ED%95%99">분류</a><a href="/wiki/%ED%8B%80:X">틀</a>'
                '<a href="/wiki/%ED%8C%8C%EC%9D%BC:A.png">파일</a><a href="/wiki/Category:X">c</a><a href="/wiki/Help:X">h</a>'
                '<a href="/wiki/Wikipedia:X">w</a><a href="/wiki/Star_Wars:_A">sw</a><a href="/wiki/Iron">철</a></p>')
        self.assertEqual(self.links(body), ["Star Wars: A", "Iron"])      # 콜론이 있어도 이름공간 접두어가 아니면 남는다

    def test_fragment_underscore_external_and_red_links(self):
        body = ('<p><a href="/wiki/Rare-earth_element#Uses">a</a><a href="https://x.org/">e</a>'
                '<a href="/w/index.php?title=Z&amp;redlink=1" class="new">r</a><a href="/wiki/Q" class="new">q</a></p>')
        self.assertEqual(self.links(body), ["Rare-earth element"])

    def test_footnotes_navbox_hatnote_dropped(self):
        body = ('<p>글<a href="/wiki/Keep">k</a><sup class="reference"><a href="/wiki/Ref">r</a></sup></p>'
                '<div class="navbox"><a href="/wiki/Nav">n</a></div><div class="hatnote"><a href="/wiki/Hat">h</a></div>'
                '<ol class="references"><li><a href="/wiki/Cite">c</a></li></ol>')
        self.assertEqual(self.links(body), ["Keep"])

    def test_dropped_sections(self):
        body = ('<p><a href="/wiki/A">a</a></p><div class="mw-heading mw-heading2"><h2>같이 보기</h2></div>'
                '<ul><li><a href="/wiki/B">b</a></li></ul><div class="mw-heading mw-heading3"><h3>소항목</h3></div>'
                '<p><a href="/wiki/C">c</a></p><div class="mw-heading mw-heading2"><h2>역사</h2></div><p><a href="/wiki/D">d</a></p>')
        self.assertEqual(self.links(body), ["A", "D"])    # 같이 보기 절(소항목 포함)은 빠지고 다음 같은 높이 제목에서 다시 센다

    def test_infobox_counted_but_its_grid_is_optional(self):
        self.assertEqual(self.links(INFOBOX), ["원자 번호"])
        self.assertEqual(self.links(INFOBOX, infobox_grid=True), ["원자 번호", "수소"])

    def test_duplicates_kept(self):
        self.assertEqual(self.links('<p><a href="/wiki/A">a</a> <a href="/wiki/A">a</a></p>'), ["A", "A"])


class Resolve(unittest.TestCase):
    def fake_api(self, calls):
        def api(lang, **p):
            calls.append((lang, p["titles"]))
            return {"query": {
                "normalized": [{"from": "iron", "to": "Iron"}],
                "redirects": [{"from": "Fe", "to": "Iron"}],
                "pages": [{"title": "Iron", "ns": 0, "langlinks": [{"lang": "ko", "title": "철"}]},
                          {"title": "Mercury", "ns": 0, "pageprops": {"disambiguation": ""}},
                          {"title": "Nope", "ns": 0, "missing": True}]}}
        return api

    def test_redirect_normalize_langlink_disamb_missing(self):
        calls, store = [], {}
        rc.resolve("en", ["iron", "Fe", "Mercury", "Nope"], "ko", store, api=self.fake_api(calls))
        self.assertEqual(store["iron"]["title"], "Iron")
        self.assertEqual(store["Fe"]["title"], "Iron")
        self.assertEqual(store["Fe"]["other"], "철")
        self.assertTrue(store["Mercury"]["disamb"])
        self.assertTrue(store["Nope"]["missing"])
        rc.resolve("en", ["iron", "Fe"], "ko", store, api=self.fake_api(calls))
        self.assertEqual(len(calls), 1)      # 이미 푼 제목은 다시 묻지 않는다

    def test_batches_of_50(self):
        calls = []
        rc.resolve("en", [f"T{i}" for i in range(120)], "ko", {}, api=self.fake_api(calls))
        self.assertEqual([len(c[1].split("|")) for c in calls], [50, 50, 20])


def rec(title, other=None, ns=0, missing=False, disamb=False):
    return {"title": title, "ns": ns, "missing": missing, "other": other, "disamb": disamb}


class Topics(unittest.TestCase):
    def setUp(self):
        # 한국어: 철(영어 Iron), 구리(Copper), 2005년, 나라(영어 없음). 영어: Iron -> 철, Copper(redirect Cu) -> 구리
        self.ko = {"철": rec("철", "Iron"), "구리": rec("구리", "Copper"), "2005년": rec("2005년", "2005"),
                   "나라": rec("나라", None), "동음": rec("동음", "Disamb"), "유로퓸": rec("유로퓸", "Europium"), "금": rec("금", "Gold")}
        self.en = {"Iron": rec("Iron", "철"), "Cu": rec("Copper", "구리"), "Copper": rec("Copper", "구리"), "Noko": rec("Noko", None),
                   "Europium": rec("Europium", "유로퓸"), "Gold": rec("Gold", "금"), "2005": rec("2005", "2005년"),
                   "Disamb": rec("Disamb", "동음", disamb=True)}

    def occ(self, *rows):
        return [{"target": t, "lang": l, "title": x} for t, l, x in rows]

    def test_two_languages_of_same_target_count_once_and_en_links_map_by_langlink(self):
        occ = self.occ(("A", "ko", "철"), ("A", "en", "Iron"), ("B", "en", "Iron"), ("B", "ko", "구리"), ("A", "en", "Cu"),
                       ("A", "en", "Noko"))
        topics, unpaired = rc.build_topics(occ, self.ko, self.en)
        self.assertEqual(topics["철"]["targets"], {"A", "B"})
        self.assertEqual((topics["철"]["ko_links"], topics["철"]["en_links"]), (1, 2))
        self.assertEqual(topics["구리"]["targets"], {"A", "B"})       # 영어 Cu(넘겨주기)가 구리로 묶인다
        self.assertEqual(sum(unpaired.values()), 1)                   # 한국어 언어 링크가 없는 영어 링크

    def test_rank_order_and_exclusions(self):
        occ = self.occ(("A", "ko", "철"), ("B", "ko", "철"), ("A", "ko", "구리"), ("A", "ko", "구리"), ("B", "ko", "구리"),
                       ("A", "ko", "금"), ("A", "ko", "나라"), ("A", "ko", "2005년"), ("A", "ko", "동음"), ("A", "ko", "유로퓸"))
        topics, _ = rc.build_topics(occ, self.ko, self.en)
        kept, dropped = rc.rank(topics, self.en, {"유로퓸"}, {"Europium"})
        # 철과 구리는 대상 2개씩이고 링크 수 합이 구리(3)가 철(2)보다 크다. 금은 대상 1개
        self.assertEqual([r["ko_title"] for r in kept], ["구리", "철", "금"])
        why = {r["ko_title"]: r["reason"] for r in dropped}
        self.assertIn("영어 문서 없음", why["나라"])
        self.assertEqual(why["2005년"], "연도·날짜 문서")
        self.assertEqual(why["동음"], "동음이의 문서")
        self.assertEqual(why["유로퓸"], "대상 10개 자신")

    def test_tie_goes_to_korean_title_order(self):
        occ = self.occ(("A", "ko", "철"), ("A", "ko", "구리"))
        topics, _ = rc.build_topics(occ, self.ko, self.en)
        kept, _ = rc.rank(topics, self.en, set(), set())
        self.assertEqual([r["ko_title"] for r in kept], ["구리", "철"])      # 대상 수·링크 수 합이 같으면 가나다 순


class DateTitles(unittest.TestCase):
    def test_dates(self):
        for t in ("2005년", "10월 28일", "1990년대", "기원전 500년", "2005", "1990s", "March 5", "March", "March 2005", "AD 100"):
            self.assertTrue(rc.is_date(t), t)

    def test_not_dates(self):
        for t in ("20세기", "Kepler-22b", "3월 혁명 기념", "Mars", "1997 XF11", "100 Hz", "목성"):
            self.assertFalse(rc.is_date(t), t)


TABLE_HTML = page(
    '<table class="infobox"><tr><th>녹는점</th><td>1099 K</td></tr></table>'
    '<p>본문에서 질량 3.5 kg 이고 길이 12 m 이다.</p>'
    '<table class="wikitable"><tr><th>이름</th><th>값</th></tr><tr><td>A</td><td>77 km</td></tr><tr><td>B</td><td>88 km</td></tr></table>'
    '<table class="wikitable"><tr><th>한 줄</th></tr></table>'
    '<table class="navbox"><tr><td>99 kg</td><td>x</td></tr><tr><td>y</td><td>z</td></tr></table>')


class TableNumbers(unittest.TestCase):
    def test_only_rule_passing_tables_marked(self):
        plain, tagged, same, n = rc.doc_markdown("문서", TABLE_HTML)
        self.assertTrue(same)
        self.assertEqual(n, 1)         # 위키표 하나만(정보 상자·한 칸짜리·둘러보기는 표 규칙 밖)
        self.assertEqual(plain.count(rc.SENT), 0)
        flags = {i["raw"]: i["in_table"] for i in rc.doc_items(tagged)}
        self.assertEqual(flags, {"1099 K": False, "3.5 kg": False, "12 m": False, "77 km": True, "88 km": True})

    def test_items_equal_to_whole_text_extract(self):
        plain, tagged, _, _ = rc.doc_markdown("문서", TABLE_HTML)
        self.assertEqual([i["raw"] for i in rc.doc_items(tagged)], [i["raw"] for i in rc.rm.extract(plain)])

    def test_marks_match_measure_count(self):
        self.assertEqual(rc.tag_tables(TABLE_HTML)[1], len(rc.sc.measure(TABLE_HTML)["tables"]))


def items_of(text, in_table=False):
    out = rc.rm.extract(text)
    for i in out:
        i["in_table"] = in_table
    return out


class CorpusJudgment(unittest.TestCase):
    def judge(self, mine, theirs):
        """mine: [(문서 번호, 글, 표 안인가)] 한 언어, theirs: [(문서 번호, 글)] 반대 언어"""
        groups = rc.pool_groups([(d, items_of(t, tab)) for d, t, tab in mine])
        rc.judge_groups(groups, [(d, t, items_of(t)) for d, t in theirs])
        return {g["mentions"][0]["raw"]: g for g in groups}

    def test_found_in_any_opposite_doc_by_digits_or_conversion(self):
        g = self.judge([(0, "질량 77 kg 이고 길이 5 km 이고 온도 9 K", False)],
                       [(10, "다른 글"), (11, "무게 77 파운드 아님. 길이는 5000 m 이다.")])
        self.assertEqual(g["77 kg"]["verdict"]["reason"], "a")           # 같은 숫자 글자 77
        self.assertEqual(g["77 kg"]["verdict"]["found_doc"], 11)         # 두 번째 문서에서 찾았다
        self.assertEqual(g["5 km"]["verdict"]["reason"], "b")            # 5 km = 5000 m
        self.assertEqual(g["9 K"]["verdict"], "그 언어에만")

    def test_same_value_in_other_same_language_doc_counts_once(self):
        groups = rc.pool_groups([(0, items_of("5 km")), (1, items_of("5000 m 와 5.02 km")), (2, items_of("9 km"))])
        self.assertEqual(len(groups), 2)                       # 5 km, 5000 m, 5.02 km(±1%)는 한 값, 9 km는 다른 값
        self.assertEqual(sorted(m["doc"] for m in groups[0]["mentions"]), [0, 1, 1])

    def test_table_origin_if_any_mention_in_table(self):
        groups = rc.pool_groups([(0, items_of("5 km", False)), (1, items_of("5 km", True))])
        self.assertTrue(any(m["in_table"] for m in groups[0]["mentions"]))


class Lines(unittest.TestCase):
    def res(self, ko, en, ko_tab, en_tab):
        def groups(prefix, n, tab):
            return [{"id": f"{prefix}{i}", "verdict": "그 언어에만", "in_table": i < tab} for i in range(n)]
        g = {"ko": groups("ko", ko, ko_tab), "en": groups("en", en, en_tab)}
        return {"domain": "rare_earth", "groups": g, "docs": []}

    def test_both_lines_needed(self):
        s = rc.summarize(self.res(36, 36, 3, 3))
        self.assertTrue(s["line_a"] and s["line_b"] and s["passed"])
        self.assertFalse(rc.summarize(self.res(35, 36, 3, 3))["passed"])      # 선 가는 36 이상
        self.assertFalse(rc.summarize(self.res(36, 36, 2, 3))["passed"])      # 선 나는 3 이상
        s = rc.summarize(self.res(40, 40, 5, 0))
        self.assertTrue(s["line_a"])
        self.assertFalse(s["line_b"])                                         # 한쪽이 0이면 못 넘는다

    def test_non_only_groups_not_counted(self):
        r = self.res(1, 1, 1, 1)
        r["groups"]["ko"][0]["verdict"] = {"reason": "a", "found": "5", "found_doc": 3}
        s = rc.summarize(r)
        self.assertEqual((s["ko_only"], s["ko_only_table"]), (0, 0))


class Inputs(unittest.TestCase):
    def test_every_domain_has_20_target_docs_on_disk(self):
        for dom in rc.DOMAINS:
            docs = rc.target_docs(dom)
            self.assertEqual(sum(d["lang"] == "ko" for d in docs), 10, dom)
            self.assertEqual(len({d["target"] for d in docs}), 10, dom)
            for d in docs:
                self.assertTrue(d["html"].exists(), (dom, d["html"]))


if __name__ == "__main__":
    unittest.main()
