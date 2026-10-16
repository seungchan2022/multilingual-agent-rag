"""check_candidates.py를 시험하는 프로그램.

  uv run python src/questions/test_check_candidates.py

후보 파일을 임시 폴더에 쓰고 검사 프로그램을 하위 프로세스로 실행해, 종료 코드와 출력 글자만 본다.
검사 프로그램을 불러 쓰지 않고, 올바른 묶음과 찾을 말이 나오는 곳의 수는 이 파일의 코드로 실제 말뭉치 글자에서 따로 만든다.
"""
import copy, json, re, subprocess, sys, tempfile, unittest
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


CONFLICTS = json.loads((ROOT / "data" / "questions" / "known_conflicts.json").read_text(encoding="utf-8"))


def conflict_entries(doc_id):
    """doc_id를 가리키는 알려진 부딪히는 값 항목들."""
    return [e for e in CONFLICTS if e.get("doc_id") == doc_id or doc_id in [t["doc_id"] for t in e.get("targets", [])]]


def touches_conflict(doc_id, line):
    """줄이 알려진 부딪히는 값 항목과 겹칠 수 있는지. 값이 홀로 선 숫자로 들어 있거나 인용과 줄이 포함 관계이면 참."""
    flat = line.replace(",", "")
    for e in conflict_entries(doc_id):
        vals = e.get("values", []) + [v for x in e.get("targets", []) if x["doc_id"] == doc_id for v in x["values"]]
        if any(re.search(r"(?<!\d)(?<!\d\.)" + re.escape(v.replace(",", "")) + r"(?!\d)(?!\.\d)", flat) for v in vals):
            return True
        for q in e.get("quotes", []):
            if q in line or line in q:
                return True
    return False


def prose(doc_id):
    """문서에서 한 줄짜리 산문으로 쓸 만한 줄들(30~150글자, 문서에 한 번만 나옴, 알려진 부딪히는 값과 겹치지 않음)."""
    t = text_of(doc_id)
    return [l for l in lines_of(doc_id)
            if 30 <= len(l) <= 150 and l == l.strip() and l[0] not in "#|-*!<>[" and t.count(l) == 1 and not touches_conflict(doc_id, l)]


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


def clean_rows(doc_id, t):
    """표 t의 데이터 줄 가운데 알려진 부딪히는 값과 겹치지 않는 것."""
    return [r for r in t[2:] if not touches_conflict(doc_id, r)]


def table_doc(pool):
    """표(머리글, 구분선, 겹치지 않는 데이터 줄 2개 이상)가 있는 첫 문서."""
    return next(d for d in pool if any(len(clean_rows(d, t)) >= 2 for t in tables_of(d)))


def table_passage(doc_id, row):
    t = next(t for t in tables_of(doc_id) if len(clean_rows(doc_id, t)) >= 2 + row)
    return t[0] + "\n" + clean_rows(doc_id, t)[row] + "\n"


class Pool:
    """문서 여러 개에서 겹치지 않는 (문서, 줄)을 차례로 꺼낸다."""
    def __init__(self, docs, shift):
        self.docs, self.shift, self.k = docs, shift, 0

    def take(self):
        doc = self.docs[self.k % len(self.docs)]
        idx = self.shift + self.k // len(self.docs)
        self.k += 1
        return doc, prose(doc)[idx]


# 반대 언어에서 찾을 말: (실제로 나오는 말, 어디에도 없는 지어낸 말, 어디에도 없는 말)
TERMS = {"ko": ["flower", "zqxwv", "peach"], "en": ["벚꽃", "쿼쿼쿼", "쌍무지개"]}
# 같은 언어에서 찾을 말: (실제로 나오는 말, 어디에도 없는 말, 어디에도 없는 말)
SAME_TERMS = {"ko": ["한옥마을", "쿼쿼쿼", "쌍무지개"], "en": ["flower", "zqxwv", "peach"]}
MAX_HITS = 10
OLD_SHAPE_MSG = "찾을 말만 글자로 적는다(걸린 곳은 적지 않는다. 프로그램이 찾는다)"


def own_spans(c):
    """후보 자신의 근거 구절이 원문에서 덮는 구간. 표 구절은 구절의 줄과 같은 문서의 모든 줄, 나머지는 구절이 나오는 모든 곳."""
    out = {}
    for f in c["required_facts"]:
        for e in f["evidence"]:
            d, ps, t = e["doc_id"], e["passage"].rstrip("\n"), text_of(e["doc_id"])
            if ps.startswith("|"):
                rows, at = set(ps.split("\n")), 0
                for line in t.split("\n"):
                    if line in rows:
                        out.setdefault(d, []).append((at, at + len(line)))
                    at += len(line) + 1
            else:
                out.setdefault(d, []).extend((m.start(), m.end()) for m in re.finditer(re.escape(ps), t))
    return out


def count_hits(c, field, term, skip_own=True):
    """찾을 말이 field의 문서들에 나오는 곳의 수(대소문자 무시). same_language_check는 후보 자신의 근거 구절 안을 뺀다(skip_own이 거짓이면 빼지 않는다). 검사 프로그램과 따로 센다."""
    el, same = c["evidence_language"], field == "same_language_check"
    skip = own_spans(c) if same and skip_own else {}
    n = 0
    for d, lang in DOCS.items():
        if (lang == el) != same:
            continue
        for m in re.finditer(re.escape(term), text_of(d), re.IGNORECASE):
            if not any(x <= m.start() and m.end() <= y for x, y in skip.get(d, [])):
                n += 1
    return n


def ev(doc, passage, loc="고유위치"):
    return {"doc_id": doc, "location": loc, "passage": passage}


def answered(cid, typ, ql, el, evs, tag):
    """답 있는 후보. evs는 [(doc, passage), ...]이고 둘 이상이면 사실을 나누고 결론 사실을 하나 더 붙인다."""
    facts = [{"fact": f"사실 {cid}-{i}", "evidence": [ev(d, p, f"고유위치 {cid}-{i}")]} for i, (d, p) in enumerate(evs)]
    if len(evs) > 1:
        facts.append({"fact": f"사실 {cid}-결론", "evidence": []})
    c = {"id": cid, "question": f"{tag} 질문 {cid}", "question_language": ql, "evidence_language": el, "type": typ,
            "answer": f"{tag} 정답 {cid}", "required_facts": facts, "opposite_check": list(TERMS[el]), "same_language_check": list(SAME_TERMS[el])}
    return c


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

    # ---- 도시 갈래 ----

    def test_24_city_imbalance(self):
        b = make_batch("ko-ko", both=3)
        out = self.assertFailsFor("묶음 구성", b)
        self.assertIn("두 언어 도시 3개", out)
        self.assertIn("한국어 도시 9개 (기대 6개씩)", out)
        self.assertIn("도시 갈래  두 언어 도시 3개, 한국어 도시 9개", out)

    def test_25_mixed_candidate_counts_as_two_language(self):
        b = make_batch("ko-ko")
        c = b[4]   # multi_doc, 두 언어 도시 후보
        self.assertEqual(c["type"], "multi_doc")
        doc = KO_POOL[4]   # 한국어만 넣는 도시
        c["required_facts"][1]["evidence"] = [ev(doc, prose(doc)[5], "고유위치 섞음")]
        self.assertEqual(DOCS[first_ev(c, 0)["doc_id"]], "ko")
        out = self.assertPasses(b)
        self.assertIn("도시 갈래  두 언어 도시 6개, 한국어 도시 6개", out)

    def test_26_valid_en_en_city_line(self):
        out = self.assertPasses(make_batch("en-en"), "en-en")
        self.assertIn("도시 갈래  두 언어 도시 6개, 영어 도시 6개", out)
        out = self.assertPasses(make_batch("en-en"), "en-en", hide=True)
        self.assertIn("도시 갈래  두 언어 도시 6개, 영어 도시 6개", out)


    # ---- 찾기 기록(opposite_check, same_language_check): 찾을 말만 적는다 ----

    def test_27_missing_or_not_list(self):
        for field in ("opposite_check", "same_language_check"):
            b = make_batch("ko-ko")
            del b[0][field]
            out = self.assertFailsFor("c-001", b)
            self.assertIn(f"{field}: 없거나 목록이 아님", out)
            self.assertNotIn("c-002", failed_names(out))
            b = make_batch("ko-ko")
            b[0][field] = "없음"
            out = self.assertFailsFor("c-001", b)
            self.assertIn(f"{field}: 없거나 목록이 아님", out)

    def test_28_fewer_than_three_terms(self):
        for field in ("opposite_check", "same_language_check"):
            b = make_batch("ko-ko")
            b[0][field] = b[0][field][:2]
            out = self.assertFailsFor("c-001", b)
            self.assertIn(f"{field}: 찾을 말이 2개임 (3개 이상이어야 함)", out)

    def test_29_old_shape_mapping_item(self):
        # 옛 모양({term, hits})은 걸린 곳을 적지 말라고 알리며 실패한다
        for field in ("opposite_check", "same_language_check"):
            b = make_batch("ko-ko")
            b[0][field][1] = {"term": b[0][field][1], "hits": []}
            out = self.assertFailsFor("c-001", b)
            self.assertIn(f"{field}[1]: {OLD_SHAPE_MSG}", out)
            self.assertNotIn("c-002", failed_names(out))

    def test_30_blank_or_non_text_item(self):
        for field in ("opposite_check", "same_language_check"):
            for bad in ("  ", None, True, ["a"]):
                b = make_batch("ko-ko")
                b[0][field][2] = bad
                out = self.assertFailsFor("c-001", b)
                self.assertIn(f"{field}[2]: 비었거나 없거나 글자가 아님", out)

    def test_31_term_language(self):
        b = make_batch("ko-ko")
        b[0]["opposite_check"][0] = "전주"
        out = self.assertFailsFor("c-001", b)
        self.assertIn("opposite_check[0]: 찾을 말이 반대 언어가 아님 (전주)", out)
        b = make_batch("en-en")
        b[0]["opposite_check"][0] = "flower"
        out = self.assertFailsFor("c-013", b, "en-en")
        self.assertIn("opposite_check[0]: 찾을 말이 반대 언어가 아님 (flower)", out)
        b = make_batch("ko-ko")
        b[0]["same_language_check"][0] = "flower"
        out = self.assertFailsFor("c-001", b)
        self.assertIn("same_language_check[0]: 찾을 말이 근거 문서의 언어가 아님 (flower)", out)
        b = make_batch("en-en")
        b[0]["same_language_check"][0] = "벚꽃"
        out = self.assertFailsFor("c-013", b, "en-en")
        self.assertIn("same_language_check[0]: 찾을 말이 근거 문서의 언어가 아님 (벚꽃)", out)

    def test_32_number_term(self):
        # 숫자만 있는 말은 두 언어 모두에서 허용하고, 따옴표 없이 적은 숫자(YAML이 숫자로 읽음)도 글자로 바꿔 받는다
        for batch in ("ko-ko", "en-en"):
            for number in ("1969", 1969):
                b = make_batch(batch)
                b[0]["opposite_check"][1] = number
                b[0]["same_language_check"][1] = number
                for field in ("opposite_check", "same_language_check"):
                    self.assertLessEqual(count_hits(b[0], field, "1969"), MAX_HITS)
                self.assertPasses(b, batch)

    def test_33_too_many_hits(self):
        # 경계: 10곳은 받고 11곳은 받지 않는다. 같은 언어는 근거 구절 안을 세지 않고, 반대 언어는 그대로 센다.
        b = make_batch("ko-ko")
        self.assertEqual(count_hits(b[0], "opposite_check", "2005"), 10)
        self.assertEqual(count_hits(b[0], "opposite_check", "1970"), 11)
        self.assertEqual(count_hits(b[0], "same_language_check", "1991"), 10)
        self.assertEqual(count_hits(b[0], "same_language_check", "1949"), 11)
        b[0]["opposite_check"][1] = "2005"
        b[0]["same_language_check"][1] = "1991"
        self.assertPasses(b)
        b[0]["opposite_check"][1] = "1970"
        b[0]["same_language_check"][1] = "1949"
        out = self.assertFailsFor("c-001", b)
        msg = "찾을 말이 11곳에 나옴 (10곳까지 받는다). 그 사실을 가려내는 더 구체적인 말(이름, 숫자가 붙은 말)로 바꾼다"
        self.assertIn(f"opposite_check[1]: {msg} (1970)", out)
        self.assertIn(f"same_language_check[1]: {msg} (1949)", out)
        # 아주 흔한 말
        b = make_batch("ko-ko")
        b[0]["opposite_check"][1] = "city"
        n = count_hits(b[0], "opposite_check", "city")
        self.assertGreater(n, MAX_HITS)
        out = self.assertFailsFor("c-001", b)
        self.assertIn(f"opposite_check[1]: 찾을 말이 {n}곳에 나옴 (10곳까지 받는다)", out)

    def test_34_case_insensitive(self):
        # 대문자로 적어도 같은 곳을 센다
        b = make_batch("ko-ko")
        b[0]["opposite_check"][0] = "FLOWER"
        self.assertEqual(count_hits(b[0], "opposite_check", "FLOWER"), count_hits(b[0], "opposite_check", "flower"))
        n = count_hits(b[0], "opposite_check", "flower") + count_hits(b[0], "opposite_check", "peach") + count_hits(b[0], "opposite_check", "zqxwv")
        out = self.assertPasses(b)
        self.assertIn(f"      찾은 기록: 찾을 말 3개, 걸린 곳 {n}곳", out)

    def test_35_same_inside_own_non_table_passage(self):
        # 찾을 말 하나가 근거 문서들에 11곳 나오지만 그중 1곳이 이 후보의 근거 구절 안이면 10곳이므로 받는다
        b = make_batch("ko-ko")
        c = b[1]
        self.assertIn("이를", first_ev(c)["passage"])
        self.assertEqual(count_hits(c, "same_language_check", "이를", skip_own=False), 11)
        self.assertEqual(count_hits(c, "same_language_check", "이를"), 10)
        c["same_language_check"][1] = "이를"
        self.assertPasses(b)
        # 다른 후보에서는 근거 구절 밖이므로 11곳으로 세어 받지 않는다
        b[0]["same_language_check"][1] = "이를"
        self.assertEqual(count_hits(b[0], "same_language_check", "이를"), 11)
        out = self.assertFailsFor("c-001", b)
        self.assertIn("same_language_check[1]: 찾을 말이 11곳에 나옴", out)
        self.assertNotIn("c-002", failed_names(out))

    def test_36_same_inside_own_table_passage(self):
        # 표 구절은 구절의 줄과 글자가 같은 문서의 모든 줄을 뺀다: 표의 머리글 낱말이 문서에서 16곳이지만 표 줄 안은 빼면 4곳
        b = make_batch("ko-ko")
        c = b[2]
        self.assertTrue(first_ev(c)["passage"].startswith("|"))
        self.assertGreater(count_hits(c, "same_language_check", "인구수", skip_own=False), MAX_HITS)
        self.assertLessEqual(count_hits(c, "same_language_check", "인구수"), MAX_HITS)
        c["same_language_check"][1] = "인구수"
        self.assertPasses(b)

    def test_37_info_line_counts_program_hits(self):
        b = make_batch("ko-ko")
        b[0]["opposite_check"][1] = "2005"
        b[0]["same_language_check"][1] = "1991"
        n_o = sum(count_hits(b[0], "opposite_check", t) for t in b[0]["opposite_check"])
        n_s = sum(count_hits(b[0], "same_language_check", t) for t in b[0]["same_language_check"])
        self.assertGreater(n_o, 10)
        self.assertGreater(n_s, 10)
        for hide in (False, True):
            out = self.assertPasses(b, hide=hide)
            self.assertIn(f"      찾은 기록: 찾을 말 3개, 걸린 곳 {n_o}곳\n      같은 언어 찾은 기록: 찾을 말 3개, 걸린 곳 {n_s}곳\n", out)
        # 답 없는 묶음에는 두 줄 모두 없다
        self.assertNotIn("찾은 기록", self.assertPasses(make_no_answer(), "no-answer"))

    def test_38_numeric_text_field(self):
        # 따옴표 없이 적은 숫자 글자 칸(예: answer: 2007.)은 숫자로 읽혔다고 알린다. 글자가 아닌 다른 값은 옛 말을 쓴다.
        msg = "따옴표 없이 적어 숫자로 읽힘. 큰따옴표로 감싼다"
        b = make_batch("ko-ko")
        b[0]["answer"] = 2007.0
        b[1]["question"] = 2007
        b[2]["required_facts"][0]["fact"] = 3.5
        first_ev(b[3])["location"] = 12
        out = self.assertFailsFor("c-001", b)
        self.assertIn(f"answer: {msg}", out)
        self.assertIn(f"question: {msg}", out)
        self.assertIn(f"required_facts[0].fact: {msg}", out)
        self.assertIn(f"required_facts[0].evidence[0].location: {msg}", out)
        b = make_batch("ko-ko")
        b[0]["answer"] = True
        out = self.assertFailsFor("c-001", b)
        self.assertIn("answer: 비었거나 없거나 글자가 아님", out)
        na = make_no_answer()
        na[0]["expected_refusal"] = 2007
        out = self.assertFailsFor("c-049", na, "no-answer")
        self.assertIn(f"expected_refusal: {msg}", out)

    def test_39_hide_terms(self):
        # --hide에서는 찾을 말 글자를 보이지 않는다
        b = make_batch("ko-ko")
        b[0]["opposite_check"][1] = "city"                       # 너무 많이 나옴
        b[1]["opposite_check"][0] = "전주"                       # 언어가 다름
        b[2]["same_language_check"][1] = {"term": "쿼쿼쿼", "hits": []}   # 옛 모양
        n = count_hits(b[0], "opposite_check", "city")
        code, out = self.run_check(b, hide=True)
        self.assertEqual(code, 1, out)
        for name in ("c-001", "c-002", "c-003"):
            self.assertIn(name, failed_names(out))
        self.assertIn(f"opposite_check[1]: 찾을 말이 {n}곳에 나옴 (10곳까지 받는다). 그 사실을 가려내는 더 구체적인 말(이름, 숫자가 붙은 말)로 바꾼다\n", out)
        self.assertIn("opposite_check[0]: 찾을 말이 반대 언어가 아님\n", out)
        self.assertIn(f"same_language_check[1]: {OLD_SHAPE_MSG}", out)
        for s_ in ("city", "전주", "쿼쿼쿼", "flower", "한옥마을"):
            self.assertNotIn(s_, out)
        # 숨기지 않으면 찾을 말이 보인다
        code, out = self.run_check(b)
        self.assertIn("(city)", out)


    def test_42_table_row_without_header(self):
        # 머리글 행 없이 표의 줄 하나만 적으면, 머리글 행이 없다고 알린다
        b = make_batch("ko-ko")
        c = next(x for x in b if x["type"] == "table_numeric" and "|" in first_ev(x)["passage"])
        rows = [l for l in first_ev(c)["passage"].rstrip("\n").split("\n") if l.strip()]
        first_ev(c)["passage"] = rows[-1]
        out = self.assertFailsFor(c["id"], b)
        self.assertIn("머리글 행이 없음", out)

    # ---- 알려진 부딪히는 값 ----

    def conflict_batch(self, doc, passage):
        """첫 후보의 근거 구절을 (doc, passage)로 바꾼 묶음. ko-ko 묶음에서 doc은 한국어 문서여야 한다."""
        b = make_batch("ko-ko")
        e = first_ev(b[0])
        e["doc_id"], e["passage"] = doc, passage
        return b

    def place_case(self):
        """(항목 번호, doc_id, 줄): 인용이 문서의 한 줄 안에 있는 한국어 문서 항목과 그 줄 전체."""
        for n, e in enumerate(CONFLICTS, 1):
            d = e.get("doc_id", "")
            if d.startswith("wiki-ko-") and e.get("quotes"):
                line = next((l for l in lines_of(d) if e["quotes"][0] in l and not l.startswith("|")), None)
                if line:
                    return n, d, line
        self.fail("인용이 문서의 한 줄 안에 있는 한국어 문서 항목이 없음")

    def test_43_conflict_place(self):
        # 목록 항목의 인용과 같은 자리의 줄이면 걸린다
        n, d, line = self.place_case()
        out = self.assertFailsFor("c-001", self.conflict_batch(d, line))
        self.assertIn('"알려진 부딪히는 값"의 항목과 겹친다(자리', out)

    def test_44_conflict_value(self):
        # 자리는 다르고 값만 같은 줄이면 걸리고, 값이 다른 숫자의 일부이면 걸리지 않는다
        b = self.conflict_batch("wiki-ko-jeonju", "전주 이야기 — 한옥 650여 채")
        e = first_ev(b[0])
        self.assertNotIn(e["passage"], text_of("wiki-ko-jeonju"))   # 값 규칙만 시험하는 글이라 원문과 다르다
        out = self.assertFailsFor("c-001", b)
        self.assertIn("겹친다(값 650)", out)
        e["passage"] = "전주 이야기 — 한옥 6500여 채와 1650채"
        out = self.assertFailsFor("c-001", b)
        self.assertNotIn("겹친다", out)

    def test_45_conflict_year(self):
        # 인구 표가 둘인 문서의 표 줄 가운데 첫 칸이 목록의 해이면 걸린다
        d = "wiki-ko-chuncheon"
        t = next(t for t in tables_of(d) if any(r.split("|")[1].strip() in ("2000", "2000년") for r in t[2:]))
        row = next(r for r in t[2:] if r.split("|")[1].strip() in ("2000", "2000년"))
        b = self.conflict_batch(d, Block(t[0] + "\n" + row + "\n"))
        out = self.assertFailsFor("c-001", b)
        self.assertIn("겹친다(", out)
        self.assertIn("해 2000", out)

    def test_46_conflict_header_only(self):
        # 머리글 행만 같고 데이터 행은 목록과 겹치지 않으면 걸리지 않는다
        d = "wiki-ko-chuncheon"
        t = next(t for t in tables_of(d) if any(r.split("|")[1].strip() in ("2000", "2000년") for r in t[2:]))
        other = next(r for r in t[2:] if r.split("|")[1].strip() not in ("1995", "1995년", "2000", "2000년", "2005", "2005년", "2010", "2010년", "2015", "2015년", "2020", "2020년"))
        b = self.conflict_batch(d, Block(t[0] + "\n" + other + "\n"))
        out = self.assertPasses(b) if not touches_conflict(d, other) else None
        if out is None:
            self.skipTest("머리글 행만 다른 데이터 행이 모두 목록과 겹쳐 건너뜀")

    def test_47_conflict_hide(self):
        # --hide에서는 원문·후보 글자 없이 번호, doc_id, 규칙 이름만 보인다
        n, d, line = self.place_case()
        out = self.assertFailsFor("c-001", self.conflict_batch(d, line), hide=True)
        self.assertIn(f'"알려진 부딪히는 값" {n}번째 항목({d})과 겹친다(자리', out)
        self.assertNotIn(line, out)
        self.assertNotIn(CONFLICTS[n - 1]["quotes"][0], out)
        self.assertNotIn(CONFLICTS[n - 1]["text"], out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
