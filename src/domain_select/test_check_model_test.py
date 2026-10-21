import unittest

import check_model_test as c


def q(**kw):
    base = {"id": "E-ko-1", "kind": "한국어 문서", "lang": "ko", "subject": "s", "target": "t",
            "question": "표면 기압은 몇 기압인가?", "answer": "35 기압", "value": 35, "unit": "기압",
            "evidence_quotes": [{"doc": "D", "quote": "기압은 35 기압으로 추정."}]}
    base.update(kw)
    return base


VALUES = [{"no": "E-ko-1", "lang": "ko", "raw": "35 기압"}]
TEXTS = {("ko", "D"): "앞 글. 기압은 35 기압으로 추정. 뒤 글."}


def run(questions, values=VALUES, texts=TEXTS):
    return c.check_field(questions, values, texts)


class Check1(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(run([q()]), [])

    def test_missing_field(self):
        d = q()
        del d["unit"]
        self.assertTrue(any("unit" in p for p in run([d])))

    def test_empty_text(self):
        self.assertTrue(any("question" in p for p in run([q(question=" ")])))

    def test_bad_lang_and_kind(self):
        self.assertTrue(any("lang" in p for p in run([q(lang="fr")])))
        self.assertTrue(any("kind" in p for p in run([q(kind="영어 문서")])))

    def test_value_not_number(self):
        self.assertTrue(any("value" in p for p in run([q(value="35")])))
        self.assertTrue(any("value" in p for p in run([q(value=True)])))

    def test_empty_evidence(self):
        self.assertTrue(any("evidence_quotes" in p for p in run([q(evidence_quotes=[])])))
        self.assertTrue(any("evidence_quotes" in p for p in run([q(evidence_quotes=[{"doc": "D", "quote": ""}])])))


class Check2(unittest.TestCase):
    def test_duplicate_id(self):
        self.assertTrue(any("겹친다" in p for p in run([q(), q()])))

    def test_missing_question(self):
        vals = VALUES + [{"no": "E-ko-2", "lang": "ko", "raw": "1 K"}]
        self.assertTrue(any("E-ko-2" in p and "빠졌다" in p for p in run([q()], vals)))

    def test_extra_question(self):
        self.assertTrue(any("E-ko-9" in p and "없는 번호" in p for p in run([q(), q(id="E-ko-9")])))

    def test_lang_differs_from_judge(self):
        vals = [{"no": "E-ko-1", "lang": "en", "raw": "35 기압"}]
        self.assertTrue(any("판정 문서의 언어" in p for p in run([q()], vals)))


class Check3(unittest.TestCase):
    def test_quote_not_in_text(self):
        d = q(evidence_quotes=[{"doc": "D", "quote": "기압은 36 기압"}])
        self.assertTrue(any("원문에 없다" in p for p in run([d])))

    def test_doc_missing(self):
        d = q(evidence_quotes=[{"doc": "X", "quote": "35 기압"}])
        self.assertTrue(any("코퍼스에 없다" in p for p in run([d])))

    def test_doc_wrong_lang(self):
        self.assertTrue(any("코퍼스에 없다" in p for p in run([q()], texts={("en", "D"): "x"})))


class Check4(unittest.TestCase):
    def test_raw_not_in_quote(self):
        vals = [{"no": "E-ko-1", "lang": "ko", "raw": "40 기압"}]
        self.assertTrue(any("근거 문장에 없다" in p for p in run([q(value=40)], vals)))

    def test_raw_in_second_quote(self):
        d = q(evidence_quotes=[{"doc": "D", "quote": "앞 글."}, {"doc": "D", "quote": "기압은 35 기압으로 추정."}])
        self.assertEqual(run([d]), [])


class Check5(unittest.TestCase):
    def one(self, raw, value, qtext="값은 얼마인가?"):
        vals = [{"no": "E-ko-1", "lang": "ko", "raw": raw}]
        texts = {("ko", "D"): raw}
        d = q(value=value, question=qtext, evidence_quotes=[{"doc": "D", "quote": raw}])
        return run([d], vals, texts)

    def test_comma(self):
        self.assertEqual(self.one("4,040 °F", 4040), [])

    def test_uncertainty_paren(self):
        self.assertEqual(self.one("621.4(11) keV", 621.4), [])

    def test_uncertainty_plus_minus(self):
        self.assertEqual(self.one("4.71+0.38 −0.27 L☉", 4.71), [])

    def test_mismatch(self):
        self.assertTrue(any("첫 수" in p for p in self.one("4,040 °F", 4.04)))

    def test_no_number(self):
        self.assertTrue(any("수가 없다" in p for p in self.one("many", 1)))


class Check6(unittest.TestCase):
    def test_leak(self):
        self.assertTrue(any("드러난다" in p for p in run([q(question="35 기압이 맞는가?")])))

    def test_leak_decimal(self):
        vals = [{"no": "E-ko-1", "lang": "ko", "raw": "621.4(11) keV"}]
        texts = {("ko", "D"): "621.4(11) keV"}
        d = q(value=621.4, question="621.4는 얼마인가?", evidence_quotes=[{"doc": "D", "quote": "621.4(11) keV"}])
        self.assertTrue(any("드러난다" in p for p in run([d], vals, texts)))

    def test_inside_other_number_ok(self):
        self.assertEqual(run([q(question="135 기압과 비교하면 몇 기압인가?")]), [])
        self.assertEqual(run([q(question="3.5 기압과 비교하면 몇 기압인가?")]), [])


if __name__ == "__main__":
    unittest.main()
