"""check_candidates.py를 시험하는 프로그램.

  uv run python src/questions/test_check_candidates.py

후보 파일을 임시 폴더에 쓰고 검사 프로그램을 하위 프로세스로 실행해, 종료 코드와 출력 글자만 본다.
검사 프로그램을 불러 쓰지 않고, 올바른 묶음은 이 파일의 코드로 실제 말뭉치 글자에서 따로 만든다.
"""
import copy, re, subprocess, sys, tempfile, unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "src" / "questions" / "check_candidates.py"
CORPUS = ROOT / "data" / "corpus"
DOCS = {d["doc_id"]: d["language"] for d in yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]}
# 앞 넷은 두 언어 도시의 문서, 뒤 넷은 그 언어만 넣는 도시의 문서
KO_POOL = ["wiki-ko-jeonju", "wiki-ko-cheongju", "wiki-ko-chuncheon", "wiki-ko-cheonan", "wiki-ko-suwon", "wiki-ko-gyeongju", "wiki-ko-sejong", "wiki-ko-gwangju"]
EN_POOL = ["wiki-en-jeonju", "wiki-en-cheongju", "wiki-en-chuncheon", "wiki-en-cheonan", "wiki-en-andong", "wiki-en-busan", "wiki-en-gangneung", "wiki-en-jeju"]
START = {"ko-ko": 1, "en-en": 13, "ko-en": 25, "en-ko": 37, "no-answer": 49}


class Block(str):
    """YAML에서 |로 쓸 글자."""


yaml.SafeDumper.add_representer(Block, lambda d, v: d.represent_scalar("tag:yaml.org,2002:str", str(v), style="|"))


def text_of(doc_id):
    return (CORPUS / "markdown" / f"{doc_id}.md").read_text(encoding="utf-8")


def lines_of(doc_id):
    return text_of(doc_id).split("\n")


def prose(doc_id):
    """문서에서 한 줄짜리 산문으로 쓸 만한 줄들(30~150글자, 문서에 한 번만 나옴)."""
    t = text_of(doc_id)
    return [l for l in lines_of(doc_id)
            if 30 <= len(l) <= 150 and l == l.strip() and l[0] not in "#|-*!<>[" and t.count(l) == 1]


def tables_of(doc_id):
    """문서의 표들. 시험 안에서 따로 찾는다: 다음 줄이 구분선인 | 줄에서 시작해 | 줄이 이어지는 만큼."""
    ls = lines_of(doc_id)
    out = []
    for i in range(len(ls) - 1):
        if ls[i].startswith("|") and re.fullmatch(r"\|[-|: ]+", ls[i + 1]) and "-" in ls[i + 1]:
            j = i
            while j < len(ls) and ls[j].startswith("|"):
                j += 1
            out.append(ls[i:j])
    return out


def table_doc(pool):
    """표(머리글, 구분선, 데이터 줄 2개 이상)가 있는 첫 문서."""
    return next(d for d in pool if any(len(t) >= 4 for t in tables_of(d)))


def table_passage(doc_id, row):
    t = next(t for t in tables_of(doc_id) if len(t) >= 4 + row)
    return t[0] + "\n" + t[2 + row] + "\n"


class Pool:
    """문서 여러 개에서 겹치지 않는 (문서, 줄)을 차례로 꺼낸다."""
    def __init__(self, docs, shift):
        self.docs, self.shift, self.k = docs, shift, 0

    def take(self):
        doc = self.docs[self.k % len(self.docs)]
        idx = self.shift + self.k // len(self.docs)
        self.k += 1
        return doc, prose(doc)[idx]


def ev(doc, passage, loc="고유위치"):
    return {"doc_id": doc, "location": loc, "passage": passage}


def answered(cid, typ, ql, el, evs, tag):
    """답 있는 후보. evs는 [(doc, passage), ...]이고 둘 이상이면 사실을 나누고 결론 사실을 하나 더 붙인다."""
    facts = [{"fact": f"사실 {cid}-{i}", "evidence": [ev(d, p, f"고유위치 {cid}-{i}")]} for i, (d, p) in enumerate(evs)]
    if len(evs) > 1:
        facts.append({"fact": f"사실 {cid}-결론", "evidence": []})
    return {"id": cid, "question": f"{tag} 질문 {cid}", "question_language": ql, "evidence_language": el, "type": typ,
            "answer": f"{tag} 정답 {cid}", "required_facts": facts}


def make_batch(batch, shift=0, table_row=0, with_table=True, both=6):
    """실제 말뭉치 글자로 올바른 묶음을 만든다. 앞에서부터 짝수 번째(0부터) 후보 가운데 both개는 두 언어 도시, 나머지는 그 언어만 넣는 도시의 문서를 쓴다."""
    ql, el = batch.split("-")
    docs = KO_POOL if el == "ko" else EN_POOL
    pools = [Pool(docs[:4], shift), Pool(docs[4:], shift)]   # 두 언어 도시, 그 언어만 넣는 도시
    two = set(range(0, 12, 2)[:both])
    tag = "한국어" if ql == "ko" else "english"
    types = ["single_fact"] * 2 + ["table_numeric"] * 2 + ["multi_doc"] * 4 + ["paraphrase"] * 4
    out = []
    for k, typ in enumerate(types):
        cid = f"c-{START[batch] + k:03d}"
        pool = pools[0 if k in two else 1]
        if typ == "table_numeric" and k == 2 and with_table:
            d = table_doc(["portal-ko-jeonju-population"] if el == "ko" else docs[:4])
            evs = [(d, Block(table_passage(d, table_row)))]
        elif typ == "multi_doc":
            evs = [pool.take(), pool.take()]
        else:
            evs = [pool.take()]
        out.append(answered(cid, typ, ql, el, evs, tag))
    return out


def make_no_answer(rebuttal_doc="wiki-ko-jeonju", shift=0):
    out = []
    for k in range(12):
        cid = f"c-{49 + k:03d}"
        ql = "ko" if k < 6 else "en"
        rb = []
        if k == 1:
            rb = [ev(rebuttal_doc, prose(rebuttal_doc)[shift], f"고유위치 {cid}")]
        out.append({"id": cid, "question": f"없는 {cid} 질문", "question_language": ql, "evidence_language": None, "type": "no_answer",
                    "answer": None, "required_facts": [], "expected_refusal": f"거절 {cid}", "no_answer_reason": f"이유 {cid}", "rebuttal": rb})
    return out


def dump(items, fence=False):
    s = yaml.dump(items, Dumper=yaml.SafeDumper, allow_unicode=True, sort_keys=False, width=10 ** 6)
    return f"```yaml\n{s}```\n" if fence else s


def first_ev(c, i=0):
    return c["required_facts"][i]["evidence"][0]


def failed_names(output):
    return [l[4:].strip() for l in output.splitlines() if l.startswith("실패  ")]


class CheckCandidatesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.n = 0

    def write(self, text_or_items, fence=False):
        self.n += 1
        text = text_or_items if isinstance(text_or_items, str) else dump(text_or_items, fence)
        p = self.tmp / f"f{self.n}.yaml"
        p.write_text(text, encoding="utf-8")
        return str(p)

    def run_check(self, items, batch="ko-ko", previous=(), hide=False, fence=False):
        args = [sys.executable, str(CHECKER), self.write(items, fence), "--batch", batch]
        for pv in previous:
            args += ["--previous", self.write(pv)]
        if hide:
            args.append("--hide")
        r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
        return r.returncode, r.stdout + r.stderr

    def assertPasses(self, *a, **kw):
        code, out = self.run_check(*a, **kw)
        self.assertEqual(code, 0, out)
        return out

    def assertFailsFor(self, name, *a, **kw):
        code, out = self.run_check(*a, **kw)
        self.assertEqual(code, 1, out)
        self.assertIn(name, failed_names(out), out)
        return out

    # ---- 올바른 묶음 ----

    def test_01_valid_ko_ko(self):
        out = self.assertPasses(make_batch("ko-ko"), fence=True)
        self.assertIn("후보 12개 가운데 12개 통과, 묶음 구성 통과", out)

    def test_02_valid_no_answer(self):
        self.assertPasses(make_no_answer(), "no-answer")

    def test_03_valid_en_ko_with_previous(self):
        self.assertPasses(make_batch("en-ko", shift=6, table_row=1), "en-ko", previous=[make_batch("ko-ko")])

    # ---- 구절이 원문과 다름 ----

    def test_04_changed_char(self):
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        m = len(e["passage"]) // 2
        e["passage"] = e["passage"][:m] + "☃" + e["passage"][m + 1:]
        out = self.assertFailsFor("c-001", b)
        self.assertIn("글자까지는 원문에 있고", out)
        self.assertIn(f"앞에서 {m}글자까지는", out)

    def test_05_only_in_other_document(self):
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        other = next(d for d in KO_POOL if d != e["doc_id"] and e["passage"] not in text_of(d))
        e["doc_id"] = other
        self.assertFailsFor("c-001", b)

    def test_06_middle_removed(self):
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        p = e["passage"]
        e["passage"] = p[:10] + p[22:]
        self.assertNotIn(e["passage"], text_of(e["doc_id"]))
        self.assertFailsFor("c-001", b)

    def test_07_row_from_other_table(self):
        found = None
        for d in KO_POOL:
            ts = tables_of(d)
            for t1 in ts:
                for t2 in ts:
                    if t1[0] == t2[0]:
                        continue
                    row = next((r for r in t2[2:] if r not in t1), None)
                    if row:
                        found = (d, t1[0], row)
                        break
                if found:
                    break
            if found:
                break
        if not found:
            self.skipTest("표가 둘 이상이고 머리글이 다른 한국어 문서가 없어 건너뜀")
        d, header, row = found
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        e["doc_id"], e["passage"] = d, header + "\n" + row + "\n"
        out = self.assertFailsFor("c-001", b)
        self.assertIn("같은 머리글의 표에 없음", out)

    def test_08_separator_included(self):
        b = make_batch("ko-ko")
        d = "portal-ko-jeonju-population"
        t = tables_of(d)[0]
        first_ev(b[2])["passage"] = Block(t[0] + "\n" + t[1] + "\n" + t[2] + "\n")
        out = self.assertFailsFor("c-003", b)
        self.assertIn("구분선", out)

    def test_09_banned_documents(self):
        b = make_batch("en-en")
        e = first_ev(b[0])
        e["doc_id"], e["passage"] = "kto-en-jeonju-hanok-village", prose("kto-en-jeonju-hanok-village")[0]
        out = self.assertFailsFor("c-013", b, "en-en")
        self.assertIn("쓰면 안 되는 영어 소개 글", out)
        na = make_no_answer()
        na[1]["rebuttal"] = [ev("kto-en-cheonan-samgeori-park", prose("kto-en-cheonan-samgeori-park")[0])]
        out = self.assertFailsFor("c-050", na, "no-answer")
        self.assertIn("쓰면 안 되는 영어 소개 글", out)

    def test_10_english_doc_in_ko_ko(self):
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        e["doc_id"], e["passage"] = "wiki-en-jeonju", prose("wiki-en-jeonju")[0]
        out = self.assertFailsFor("c-001", b)
        self.assertIn("evidence_language와 다름", out)

    def test_11_unknown_doc_id(self):
        b = make_batch("ko-ko")
        first_ev(b[0])["doc_id"] = "wiki-ko-seoul"
        self.assertFailsFor("c-001", b)

    # ---- 묶음 구성 ----

    def test_12_counts(self):
        b = make_batch("ko-ko")
        self.assertFailsFor("묶음 구성", b[:11])
        b = make_batch("ko-ko")
        b[3]["type"] = "single_fact"   # 단일 사실 3, 표 숫자 1
        out = self.assertFailsFor("묶음 구성", b)
        self.assertIn("type single_fact가 3개", out)

    def test_13_ids(self):
        b = make_batch("ko-ko")
        for k, c in enumerate(b):
            c["id"] = f"c-{k + 2:03d}"
        self.assertFailsFor("묶음 구성", b)
        b = make_batch("ko-ko")
        b[1]["id"] = "c-001"
        out = self.assertFailsFor("묶음 구성", b)
        self.assertIn("id가 겹침", out)

    def test_14_wrong_question_language(self):
        b = make_batch("ko-ko")
        b[4]["question_language"] = "en"
        self.assertFailsFor("c-005", b)

    # ---- 칸 ----

    def test_15_missing_answer_and_empty_question(self):
        b = make_batch("ko-ko")
        del b[0]["answer"]
        out = self.assertFailsFor("c-001", b)
        self.assertIn("answer", out)
        b = make_batch("ko-ko")
        b[1]["question"] = ""
        self.assertFailsFor("c-002", b)

    def test_16_no_answer_with_answer_or_facts(self):
        na = make_no_answer()
        na[0]["answer"] = "답이 있음"
        self.assertFailsFor("c-049", na, "no-answer")
        na = make_no_answer()
        na[2]["required_facts"] = [{"fact": "사실", "evidence": []}]
        self.assertFailsFor("c-051", na, "no-answer")

    def test_17_all_evidence_empty(self):
        b = make_batch("ko-ko")
        b[0]["required_facts"][0]["evidence"] = []
        out = self.assertFailsFor("c-001", b)
        self.assertIn("근거(evidence)가 있는 사실이 하나도 없음", out)

    def test_18_no_table_passage(self):
        b = make_batch("ko-ko", with_table=False)
        code, out = self.run_check(b)
        self.assertEqual(code, 1, out)
        self.assertIn("묶음 구성", failed_names(out), out)
        self.assertNotIn("c-003", failed_names(out), out)

    # ---- 앞 묶음 ----

    def test_19_previous(self):
        prev = make_batch("ko-ko")
        # id 다시 씀
        b = make_batch("en-ko", shift=6, table_row=1)
        b[0]["id"] = "c-001"
        self.assertFailsFor("c-001", b, "en-ko", previous=[prev])
        # 같은 질문
        b = make_batch("en-ko", shift=6, table_row=1)
        b[2]["question"] = prev[2]["question"]
        self.assertFailsFor("c-039", b, "en-ko", previous=[prev])
        # 같은 (문서, 구절)을 다른 id가 씀: 주의만 하고 통과
        b = make_batch("en-ko", shift=6, table_row=1)
        src = first_ev(prev[0])
        e = first_ev(b[0])
        e["doc_id"], e["passage"] = src["doc_id"], src["passage"]
        out = self.assertPasses(b, "en-ko", previous=[prev])
        self.assertIn("주의  c-037", out)

    # ---- --hide ----

    def test_20_hide(self):
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        m = len(e["passage"]) // 2
        e["passage"] = e["passage"][:m] + "☃" + e["passage"][m + 1:]
        e3 = first_ev(b[2], 0)
        e3["doc_id"], e3["passage"] = "kto-en-jeonju-hanok-village", prose("kto-en-jeonju-hanok-village")[0]
        secrets = []
        for c in b:
            secrets += [c["question"], c["answer"]]
            for f in c["required_facts"]:
                secrets.append(f["fact"])
                for x in f["evidence"]:
                    secrets += [x["location"], x["passage"], x["passage"][:10]]
        b = b[:11]
        code, out = self.run_check(b, hide=True)
        self.assertEqual(code, 1, out)
        names = failed_names(out)
        for n in ("c-001", "c-003", "묶음 구성"):
            self.assertIn(n, names, out)
        self.assertIn("required_facts[0].evidence[0].passage", out)
        self.assertIn("원문에 글자 그대로 없음", out)
        self.assertIn("글자까지 원문과 같음", out)
        for s in secrets:
            self.assertNotIn(s.strip(), out)
        self.assertNotIn("☃", out)
        # 답 없는 묶음도 마찬가지
        na = make_no_answer()
        na[1]["rebuttal"][0]["passage"] += "다름"
        code, out = self.run_check(na, "no-answer", hide=True)
        self.assertEqual(code, 1, out)
        for c in na:
            for s in (c["question"], c["expected_refusal"], c["no_answer_reason"]):
                self.assertNotIn(s, out)
        self.assertNotIn(na[1]["rebuttal"][0]["passage"][:10], out)
        self.assertIn("rebuttal[0].passage", out)

    def test_21_broken_yaml(self):
        text = '- id: c-001\n  question: "비밀질문 [\n  type: ?: ]\n'
        code, out = self.run_check(text)
        self.assertEqual(code, 1, out)
        self.assertIn("YAML을 읽지 못함", out)
        self.assertNotIn("Traceback", out)
        code, out = self.run_check(text, hide=True)
        self.assertEqual(code, 1, out)
        self.assertIn("YAML을 읽지 못함", out)
        self.assertNotIn("Traceback", out)
        self.assertNotIn("비밀질문", out)

    # ---- 여러 줄과 블록 글자 ----

    def test_22_multiline_non_table(self):
        found = None
        for d in KO_POOL:
            ls = lines_of(d)
            for i in range(len(ls) - 2):
                t = ls[i:i + 3]
                if all(x.strip() and x == x.rstrip() and not x.startswith("|") for x in t):
                    found = (d, t)
                    break
            if found:
                break
        self.assertIsNotNone(found, "연달아 놓인 비지 않은 줄 셋을 찾지 못함")
        d, (a, b_, c_) = found
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        e["doc_id"], e["passage"] = d, a + "\n" + b_
        self.assertPasses(b)
        e["passage"] = a + "\n" + c_   # 가운데 줄을 건너뜀
        self.assertNotIn(e["passage"], text_of(d))
        self.assertFailsFor("c-001", b)

    def test_23_block_scalar(self):
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        e["passage"] = Block(e["passage"] + "\n")
        text = dump(b)
        self.assertIn("passage: |", text)
        self.assertPasses(text)

    # ---- 도시 묶음 ----

    def test_24_city_imbalance(self):
        b = make_batch("ko-ko", both=3)
        out = self.assertFailsFor("묶음 구성", b)
        self.assertIn("두 언어 도시 3개", out)
        self.assertIn("한국어 도시 9개 (기대 6개씩)", out)
        self.assertIn("도시 묶음  두 언어 도시 3개, 한국어 도시 9개", out)

    def test_25_mixed_candidate_counts_as_two_language(self):
        b = make_batch("ko-ko")
        c = b[4]   # multi_doc, 두 언어 도시 후보
        self.assertEqual(c["type"], "multi_doc")
        doc = KO_POOL[4]   # 한국어만 넣는 도시
        c["required_facts"][1]["evidence"] = [ev(doc, prose(doc)[5], "고유위치 섞음")]
        self.assertEqual(DOCS[first_ev(c, 0)["doc_id"]], "ko")
        out = self.assertPasses(b)
        self.assertIn("도시 묶음  두 언어 도시 6개, 한국어 도시 6개", out)

    def test_26_valid_en_en_city_line(self):
        out = self.assertPasses(make_batch("en-en"), "en-en")
        self.assertIn("도시 묶음  두 언어 도시 6개, 영어 도시 6개", out)
        out = self.assertPasses(make_batch("en-en"), "en-en", hide=True)
        self.assertIn("도시 묶음  두 언어 도시 6개, 영어 도시 6개", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
