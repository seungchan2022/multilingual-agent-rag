"""희토류 원소 코퍼스의 정보 상자 줄과 마크다운 표에 적힌 값을 모두 모아 values.json에 쓴다(이슈 #7, 값 목록 1단계).

실행: .venv/bin/python research_notes/stage2_values_rare_earth/extract.py
결과: 같은 폴더의 values.json. 본문 문단의 값은 여기서 다루지 않는다(뒤 단계).

자리(place)는 한 곳에 적힌 값 하나다. 자리마다 대상(object), 양(quantity), 조건(condition)을 단다.
이름과 열쇠는 vocab.json(읽기만 한다)에서 찾고, 없으면 만들지 않고 빠진 것으로 적은 뒤 실패한다.
숫자를 읽는 규칙은 src/domain_select/quantities.py의 read를 그대로 쓴다.

덮임 검사(coverage): 문서 전체에 read를 돌려, 정보 상자 줄과 표 줄에 있는 숫자 항목이 모두
  - 자리 하나의 범위 안이거나
  - 값이 아닌 것(이름·제목·구조 이름·덧붙인 말·머리글·대상 칸·되풀이 칸)으로 표시한 범위 안인지 센다.
못 덮은 것이 하나라도 있으면 목록을 찍고 종료 코드 1로 끝낸다.
"""
import bisect
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "src" / "domain_select"))
import quantities as Q  # noqa: E402

MD_DIR = ROOT / "data" / "corpus" / "markdown"
SKIP = Q.SKIP

# 값이 아닌 범위의 이유
R_LABEL = "정보 상자 이름"
R_TITLE = "제목 줄"
R_STRUCT = "구조 이름"
R_NOTE = "덧붙인 말"
R_HEADER = "머리글"
R_OBJECT = "대상 칸"
R_REPEAT = "되풀이 칸"
R_ROWLABEL = "표 줄 이름"

# 칸의 값이 늘 낱말인 양(스핀·붕괴 방식처럼 숫자가 들어 있어도 이름표인 것)
WORD_QUANTITIES = {"decay_mode", "daughter", "spin_parity", "accelerator_product", "delivery_agent_dose",
                   "patients_and_trial_years", "clinical_status", "listed_boron_agent"}

# 사마륨-코발트 자석 표의 열 머리글 -> 대상
MAGNET_OBJECT = {"Neodymium": "sintered neodymium magnet", "Sm-Co": "sintered samarium-cobalt magnet"}

SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
ISO_RE = re.compile(r"^([⁰¹²³⁴⁵⁶⁷⁸⁹]+)(?:ᵐ([⁰¹²³⁴⁵⁶⁷⁸⁹]*))?([A-Z][a-z]?)$")


def isotope_key(cell):
    """'¹⁶⁷Tm' -> 'Tm-167', '⁸⁷ᵐY' -> 'Y-87m', '⁸⁵ᵐ¹Y' -> 'Y-85m1'. 모양이 다르면 None."""
    m = ISO_RE.match(cell.strip())
    if not m:
        return None
    iso = "" if m.group(2) is None else "m" + m.group(2).translate(SUP)
    return f"{m.group(3)}-{m.group(1).translate(SUP)}{iso}"


# --- 숫자 모양 ---------------------------------------------------------------
_SIGN = r"[+\-−–]?"
_BASE = r"\d[\d,]*(?:\.\d+)?"
_EXP = r"(?:\s?×\s?10(?:[⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\^\{?[+−-]?\d+\}?)|[eE][+\-]?\d+)"
NUM_RE = re.compile(_SIGN + _BASE + _EXP + "?")
EXP_RE = re.compile(_EXP)
UNC_RE = re.compile(r"(?:\([+\-−]?\d+(?:\.\d+)?(?:[+\-−]\d+(?:\.\d+)?)?\)|\s?±\s?" + _BASE + ")")
APPROX_RE = re.compile(r"(est\.|ca\.|about|~|≈|약|<|>|≥|≤)\s?")
RANGE_RE = re.compile(r"(?:\s?[–-]\s?|\.\.|\s+to\s+)")
PAREN_RANGE_RE = re.compile(rf"\((?P<a>{_BASE})[–-](?P<b>{_BASE})\)(?P<exp>{_EXP})")
FALLBACK_UNIT_RE = re.compile(r"\s?(%|°[CF]?|[A-Za-zµμΩ][A-Za-zµμΩ³²⁻¹/·⋅]*)")
BRACKET_RE = re.compile(r"\[[^\[\]]*\]")
PREFIX_RE = re.compile(r"([^:=()]+?): ")
LATTICE_RE = re.compile(r"([A-Za-zα-ωΑ-Ω]+) = ")
TRAILING_PAREN_RE = re.compile(r"\(([^()]*)\)\s*$")
HAS_DIGIT = re.compile(r"\d")


def _num_part(s, p):
    """p에서 숫자 하나(부호, 지수, 오차, #)를 읽는다. (num, unc, est, 끝) 또는 None."""
    m = NUM_RE.match(s, p)
    if not m:
        return None
    num, e, unc = m.group(0), m.end(), ""
    u = UNC_RE.match(s, e)
    if u:
        unc, e = u.group(0).strip(), u.end()
        x = EXP_RE.match(s, e)             # 2.29(16)×10¹⁵: 오차 뒤의 지수는 수에 붙인다
        if x and not EXP_RE.search(num):
            num, e = num + x.group(0), x.end()
    est = s.startswith("#", e)
    return num, unc, est, e + 1 if est else e


def parse_rep(s, p, value_of=None):
    """s의 p에서 표기 하나(숫자 [범위] [오차] [단위])를 읽는다. 읽을 수 없으면 None.
    돌려주는 값: (rep dict, 끝). value_of(시작, 끝)은 quantities.read의 값(없으면 None)을 찾는 함수다."""
    a = APPROX_RE.match(s, p)
    approx, q = (a.group(1), a.end()) if a else ("", p)
    pr = PAREN_RANGE_RE.match(s, q)
    if pr:                                   # (3–4)×10⁻⁶: 지수는 두 끝에 함께 붙는다
        num, range_to, unc, est, e = pr.group("a") + pr.group("exp"), pr.group("b") + pr.group("exp"), "", False, pr.end()
    else:
        n = _num_part(s, q)
        if not n:
            return None
        num, unc, est, e = n
        range_to = None
        r = RANGE_RE.match(s, e)
        n2 = _num_part(s, r.end()) if r else None
        if n2:
            range_to, e = n2[0], n2[3]
            est = est or n2[2]
    unit, ue = "", e
    u = Q.find_unit(s, e)
    if u:
        unit, ue = u[0], u[2]
    else:
        f = FALLBACK_UNIT_RE.match(s, e)
        if f:
            unit, ue = f.group(1), f.end()
    rep = {"text": s[q:ue], "num": num, "unc": unc, "unit": unit, "range_to": range_to, "approx": approx,
           "est_mark": est, "value": value_of(q, ue) if value_of else None}
    return rep, ue


def parse_numeric(s, value_of=None):
    """표 칸 글 s가 표기 하나 이상(' / '로 이음)과 끝의 [..] 덧붙임으로만 이루어졌는지 본다.
    돌려주는 값: (reps, 표기가 끝난 자리, 덧붙임 글 또는 None). 아니면 None."""
    reps, p = [], 0
    while True:
        r = parse_rep(s, p, value_of)
        if not r:
            return None
        reps.append(r[0])
        p = r[1]
        if s.startswith(" / ", p):
            p += 3
            continue
        break
    rest = s[p:].strip()
    if not rest:
        return reps, p, None
    if BRACKET_RE.fullmatch(rest):
        return reps, p, rest
    return None


# --- 한 줄의 글 -------------------------------------------------------------
class Line:
    """줄 하나. quote는 원문 줄, c는 건너뛰는 글자(U+200B, 소프트 하이픈 등)를 뺀 줄이다.
    자리와 값이 아닌 범위는 quote 안의 자리로 적는다(idx가 c의 자리를 quote의 자리로 바꾼다)."""

    def __init__(self, doc, no, quote, items):
        self.doc, self.no, self.quote = doc, no, quote
        self.idx = [i for i, ch in enumerate(quote) if ch not in SKIP]
        self.c = "".join(quote[i] for i in self.idx)
        inv, kept = [], 0                       # quote의 i번째 글자 앞에 남은 글자 수 = 그 글자의 c 자리
        for ch in quote:
            inv.append(kept)
            kept += ch not in SKIP
        inv.append(kept)
        self.items = [{**it, "s": inv[it["start"]], "e": inv[it["end"] - 1] + 1} for it in items]
        self.places, self.nonvalue = [], []

    def orig(self, a, b):
        return self.idx[a], self.idx[b - 1] + 1

    def mark(self, a, b, reason):
        """c의 [a, b)를 값이 아닌 범위로 표시한다."""
        if b > a:
            self.nonvalue.append((*self.orig(a, b), reason))

    def value_of(self, a, b):
        """c의 [a, b) 안에서 처음 나오는 '양' 항목의 값. 없으면 None."""
        for it in self.items:
            if it["kind"] == "양" and a <= it["s"] < b:
                return it["value"]
        return None

    def item_spans(self, a, b):
        return [(it["s"], it["e"]) for it in self.items if a <= it["s"] and it["e"] <= b]


class Builder:
    def __init__(self, vocab):
        self.v = vocab
        self.records = []
        self.missing = []           # 빠진 사전 항목
        self.problems = []          # 규칙대로 읽지 못한 것
        self.fallback_words = []    # 숫자 규칙에 안 맞아 낱말이 된 칸 (문서, 줄, 양, 글)

    # --- 사전과 기록 ---
    def need(self, table, key, ln):
        tab = self.v[table]
        if key in tab:
            return tab[key]
        self.missing.append((table, key, f"{ln.doc.id}:{ln.no}"))
        return None

    def problem(self, ln, msg):
        self.problems.append(f"{ln.doc.id}:{ln.no}: {msg}")

    def add(self, ln, a, b, where, obj, quantity, condition, notes, label, kind, reps, multi=False):
        """c의 [a, b)를 자리로 적는다."""
        start, end = ln.orig(a, b)
        rec = {
            "id": "", "doc_id": ln.doc.id, "lang": ln.doc.lang, "topic": ln.doc.topic, "branch": ln.doc.branch,
            "line": ln.no, "where": where, "quote": ln.quote, "raw": ln.quote[start:end], "start": start, "end": end,
            "object": obj, "quantity": quantity, "condition": condition, "note": notes, "label": label,
            "kind": kind, "reps": reps if reps is not None else [{"text": ln.quote[start:end]}],
        }
        if multi:
            rec["multi"] = True
        ln.places.append(rec)
        self.records.append(rec)

    # --- 정보 상자 ---
    def infobox_line(self, ln, state):
        c = ln.c
        if not c.strip() or c.startswith("|"):
            return
        m1 = re.match(r"^  - ", c)
        m0 = re.match(r"^- ", c)
        if not (m1 or m0):
            self.problem(ln, "정보 상자 줄의 모양을 모른다: " + c[:60])
            return
        start = (m1 or m0).end()
        text = c[start:]
        obj = self.v["topic_object"].get(ln.doc.topic)
        if obj is None:
            self.missing.append(("topic_object", ln.doc.topic, ln.doc.id))
            return
        if ": " in text:
            k = text.index(": ")
            label, va = text[:k], start + k + 2
            ln.mark(start, start + len(label), R_LABEL)
            if m0:
                state["group"] = text
            ent = self.need("infobox_label", label, ln)
            if ent is None:
                return
            self.value(ln, va, len(c.rstrip()), ent["quantity"], ent.get("whole", False), obj, label)
            return
        if m0:
            state["group"] = text
            ln.mark(start, len(c.rstrip()), R_TITLE)
            return
        if text in self.v["infobox_title"]:
            ln.mark(start, len(c.rstrip()), R_TITLE)
            return
        for gk, ent in self.v["infobox_group_label"].items():
            if state["group"].startswith(gk):
                self.value(ln, start, len(c.rstrip()), ent["quantity"], ent.get("whole", False), obj, state["group"])
                return
        self.missing.append(("infobox_title", text, f"{ln.doc.id}:{ln.no}"))

    def value(self, ln, va, vb, quantity, whole, obj, label):
        if vb <= va:
            return
        if whole:
            self.add(ln, va, vb, "정보 상자", obj, quantity, "", [], label, "낱말", None)
            return
        for a, b in self.split_pieces(ln, va, vb):
            self.piece(ln, a, b, quantity, obj, label)

    def split_pieces(self, ln, va, vb):
        """값 글을 ' / '(늘)와 ', '(뒤가 구조 이름 '이름: ' 이거나 '(이름)'으로 끝날 때만)로 가른다. 괄호 안은 가르지 않는다."""
        c, struct = ln.c, self.v["structural_condition"]
        cuts, depth, i = [], 0, va
        while i < vb:
            ch = c[i]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif depth == 0 and c.startswith(" / ", i):
                cuts.append((i, i + 3))
            i += 1
        bounds, pos = [], va
        for ca, cb in cuts:
            bounds.append((pos, ca))
            pos = cb
        bounds.append((pos, vb))
        out = []
        for a, b in bounds:
            pa, depth, i = a, 0, a
            while i < b:
                ch = c[i]
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                elif depth == 0 and c.startswith(", ", i):
                    rest = c[i + 2:b]
                    pm = PREFIX_RE.match(rest)
                    tm = TRAILING_PAREN_RE.search(rest)
                    if (pm and pm.group(1) in struct) or (tm and tm.group(1) in struct):
                        out.append((pa, i))
                        pa = i + 2
                        i += 1
                i += 1
            out.append((pa, b))
        return [(a, b) for a, b in out if c[a:b].strip()]

    def piece(self, ln, a, b, quantity, obj, label):
        c, struct = ln.c, self.v["structural_condition"]
        while a < b and c[a] == " ":
            a += 1
        while b > a and c[b - 1] == " ":
            b -= 1
        conds, notes, blanks = [], [], []     # blanks: (시작, 끝, 이유)
        p = a
        pm = PREFIX_RE.match(c, a, b)
        if pm and (pm.group(1) in struct or not HAS_DIGIT.search(pm.group(1))):
            x = pm.group(1)
            if x in struct:
                conds.append(struct[x])
                blanks.append((a, pm.end(), R_STRUCT))
            else:
                notes.append(x)
                blanks.append((a, pm.end(), R_NOTE))
            p = pm.end()
        else:
            lm = LATTICE_RE.match(c, a, b)
            if lm:
                x = lm.group(1)
                if x in struct:
                    conds.append(struct[x])
                else:
                    self.missing.append(("structural_condition", x, f"{ln.doc.id}:{ln.no}"))
                blanks.append((a, lm.end(), R_STRUCT))
                p = lm.end()
        spans = ln.item_spans(p, b)
        groups, i = [], p
        while i < b:
            if c[i] == "(" and (i == p or c[i - 1] == " ") and not any(s <= i < e for s, e in spans):
                depth, j = 0, i
                while j < b:
                    depth += (c[j] == "(") - (c[j] == ")")
                    j += 1
                    if depth == 0:
                        break
                if depth != 0:
                    self.problem(ln, "괄호가 닫히지 않았다: " + c[a:b])
                    return
                groups.append((i, j))
                i = j
            else:
                i += 1
        main = next((it for it in ln.items if it["kind"] == "양" and p <= it["s"] < b
                     and not any(g0 <= it["s"] < g1 for g0, g1 in groups)), None)
        main_dim = main["dim"] if main else None
        conv = []                              # 단위를 바꿔 적은 괄호 (시작, 끝)
        for g0, g1 in groups:
            inner = c[g0 + 1:g1 - 1]
            if inner in struct:
                conds.append(struct[inner])
                blanks.append((g0, g1, R_STRUCT))
                continue
            gi = [it for it in ln.items if g0 <= it["s"] and it["e"] <= g1]
            parts = inner.split(", ")
            ok = main_dim is not None and gi and all(it["kind"] == "양" and it["dim"] == main_dim for it in gi)
            if ok:
                for part in parts:
                    r = parse_rep(part, 0)
                    ok = ok and r is not None and r[1] == len(part)
            if ok:
                conv.append((g0, g1))
            else:
                notes.append(c[g0:g1])
                blanks.append((g0, g1, R_NOTE))
        if len(set(conds)) > 1:
            self.problem(ln, f"조건이 둘 이상이다: {conds}")
            return
        res = list(c)
        for s, e, _ in blanks:
            res[s:e] = " " * (e - s)
        res = "".join(res)
        cs = next((k for k in range(a, b) if res[k] != " "), None)
        if cs is None:
            self.problem(ln, "값이 비었다: " + c[a:b])
            return
        ce = max(k for k in range(a, b) if res[k] != " ") + 1
        for s, e, why in blanks:
            ln.mark(s, e, why)
        cond = conds[0] if conds else ""
        core = res[cs:ce]
        if not HAS_DIGIT.search(core):
            self.add(ln, cs, ce, "정보 상자", obj, quantity, cond, notes, label, "낱말", None)
            return
        r = parse_rep(res, cs, ln.value_of)
        if not r:
            self.problem(ln, f"숫자를 읽지 못했다: {core!r}")
            return
        reps, q = [r[0]], r[1]
        while q < ce:
            if res[q] == " ":
                q += 1
                continue
            g = next(((g0, g1) for g0, g1 in conv if g0 == q), None)
            if not g:
                self.problem(ln, f"읽고 남은 글이 있다: {res[q:ce]!r} (값 {core!r})")
                return
            for part, off in self.parts(c, g[0] + 1, g[1] - 1):
                rr = parse_rep(part, 0, lambda s, e, off=off: ln.value_of(off + s, off + e))
                reps.append(rr[0])
            q = g[1]
        self.add(ln, cs, ce, "정보 상자", obj, quantity, cond, notes, label, "수", reps)

    @staticmethod
    def parts(c, a, b):
        """괄호 안 글을 ', '로 가른 (글, 시작 자리)."""
        out, pos = [], a
        for m in re.finditer(", ", c[a:b]):
            out.append((c[pos:a + m.start()], pos))
            pos = a + m.end()
        out.append((c[pos:b], pos))
        return out

    # --- 표 ---
    @staticmethod
    def cells(c):
        """표 줄 c의 칸마다 (내용 시작, 내용 끝). 앞뒤 공백을 뺀다."""
        pipes = [i for i, ch in enumerate(c) if ch == "|" and (i == 0 or c[i - 1] != "\\")]
        out = []
        for k in range(len(pipes) - 1):
            a, b = pipes[k] + 1, pipes[k + 1]
            while a < b and c[a] == " ":
                a += 1
            while b > a and c[b - 1] == " ":
                b -= 1
            out.append((a, b))
        return out

    def table_cell(self, ln, a, b, quantity, obj, label, unit_default="", extra_notes=()):
        """데이터 칸 하나를 자리로 적는다. 칸이 비었거나 '-'이면 적지 않는다."""
        text = ln.c[a:b]
        if text in ("", "-"):
            return
        if quantity not in WORD_QUANTITIES:
            res = parse_numeric(text, lambda s, e: ln.value_of(a + s, a + e))
        else:
            res = None
        if res:
            reps, end, note = res
            notes = list(extra_notes)
            if note:
                notes.append(note)
                ln.mark(a + len(text) - len(text[end:].lstrip()), b, R_NOTE)
            for r in reps:
                if not r["unit"] and unit_default:
                    r["unit"] = unit_default
            self.add(ln, a, a + end, "표", obj, quantity, "", notes, label, "수", reps, multi=len(reps) > 1)
        else:
            if quantity not in WORD_QUANTITIES and HAS_DIGIT.search(text):
                self.fallback_words.append((ln.doc.id, ln.no, quantity, text))
            self.add(ln, a, b, "표", obj, quantity, "", list(extra_notes), label, "낱말", None)

    def table(self, doc, t, lines):
        """표 하나를 읽는다. 돌려주는 값: (머리글 줄 번호 목록, 데이터 줄 번호 목록) (0부터 센 md_lines 번호)."""
        n0 = t["md_line_no"] - 1
        L = [lines[n0 + k] for k in range(len(t["md_lines"]))]
        top = t["top_th_rows"]
        first = [x.strip() for x in L[0].strip().strip("|").split("|")]
        name = f"{doc.id}:{t['md_line_no']}"
        if first[0] in ("압력 (Pa)", "P (Pa)"):
            return "증기 압력", self.vapor(doc, t, L, n0, lines)
        header_idx = [0, 1] + ([2] if top == 2 else [])
        rows0 = [x.strip() for x in L[0].strip().strip("|").split("|")]
        rows2 = [x.strip() for x in L[2].strip().strip("|").split("|")] if top == 2 else None
        if "핵자 수" in rows0 or "Nuclide" in rows0:
            return "동위 원소 목록", self.isotope_table(doc, t, L, n0, rows0, rows2, True)
        if (top == 1 and "동위체" in rows0) or (top == 2 and "Isotope" in rows2):
            return "주요 동위원소", self.isotope_table(doc, t, L, n0, rows2 or rows0, None, False)
        if doc.id == "wiki-en-samarium-cobalt-magnet":
            return "그 밖의 표", self.magnet_table(doc, t, L, n0)
        if doc.id == "wiki-en-neutron-capture-therapy":
            return "그 밖의 표", self.nct_table(doc, t, L, n0, rows0, top)
        self.problems.append(f"{name}: 표 모양을 분류하지 못했다")
        return "분류 못함", (header_idx, [])

    def mark_header_lines(self, doc, n0, idxs):
        for k in idxs:
            ln = doc.line(n0 + k)
            ln.mark(0, len(ln.c), R_HEADER)

    def vapor(self, doc, t, L, n0, lines):
        """압력 줄(머리글)과 온도 줄. 온도 칸마다 자리 하나: 조건은 압력(Pa)."""
        self.mark_header_lines(doc, n0, [0, 1])
        lp, lt = doc.line(n0), doc.line(n0 + 2)
        pcells, tcells = self.cells(lp.c), self.cells(lt.c)
        if len(pcells) != 7 or len(tcells) != 7:
            self.problem(lt, "증기 압력 표의 칸 수가 7이 아니다")
            return [0, 1], []
        label = lt.c[tcells[0][0]:tcells[0][1]]
        um = re.search(r"\(([^()]*)\)\s*$", label)
        unit = um.group(1) if um else ""
        lt.mark(*tcells[0], R_ROWLABEL)
        above = ""
        k = n0 - 1
        while k >= 0 and not doc.lines[k].strip():
            k -= 1
        if k >= 0:
            above = "".join(ch for ch in doc.lines[k] if ch not in SKIP).strip()
            above = above[2:].strip() if above.startswith("- ") else above
        base_notes = ["extrapolated"] if above == "Vapor pressure (extrapolated)" else []
        for (pa, pb), (ta, tb) in zip(pcells[1:], tcells[1:]):
            ptxt = lp.c[pa:pb]
            pm = re.fullmatch(r"(\d+)( k)?", ptxt)
            if not pm:
                self.problem(lp, "압력 칸을 읽지 못했다: " + ptxt)
                continue
            pressure = str(int(pm.group(1)) * (1000 if pm.group(2) else 1))
            ttxt = lt.c[ta:tb]
            tm = re.fullmatch(r"\(?(\d+(?:\.\d+)?)\)?", ttxt)
            if not tm:
                self.problem(lt, "온도 칸을 읽지 못했다: " + ttxt)
                continue
            notes = list(base_notes) + (["괄호 값"] if ttxt.startswith("(") else [])
            rep = {"text": ttxt, "num": tm.group(1), "unc": "", "unit": unit, "range_to": None, "approx": "",
                   "est_mark": False, "value": lt.value_of(ta, tb)}
            self.add(lt, ta, tb, "표", self.v["topic_object"][doc.topic], "vapor_pressure_temperature",
                     f"P={pressure}", notes, label, "수", [rep])
        return [0, 1], [2]

    def data_rows(self, t, top):
        """md_lines에서 데이터 줄 번호와 머리글 줄 번호."""
        n = len(t["md_lines"])
        if top == 0:
            return [0] + list(range(2, n)), [1]
        return list(range(top + 1, n)), list(range(0, top + 1))

    def columns(self, ln, names):
        """names(머리글 글)를 vocab의 양으로 바꾼다. 빠진 이름은 기록한다."""
        return [self.need("table_column", nm, ln) for nm in names]

    def isotope_table(self, doc, t, L, n0, names, names2, is_list):
        top = t["top_th_rows"]
        data, header = self.data_rows(t, top)
        self.mark_header_lines(doc, n0, header)
        hl = doc.line(n0)
        names1 = [x.replace("­", "").strip() for x in names]
        q1 = self.columns(hl, names1)
        q2 = None
        if is_list:
            nm2 = [x.replace("­", "").strip() for x in names2]
            q2 = self.columns(hl, nm2)
        for k in data:
            ln = doc.line(n0 + k)
            cells = self.cells(ln.c)
            if len(cells) != len(names1):
                self.problem(ln, f"칸 수가 머리글과 다르다 ({len(cells)} / {len(names1)})")
                continue
            oi = q1.index("@object") if "@object" in q1 else None
            if oi is None:
                self.problem(ln, "대상 열이 없다")
                continue
            oa, ob = cells[oi]
            otext = ln.c[oa:ob]
            obj = isotope_key(otext)
            if obj is None:
                self.problem(ln, "동위체 칸을 읽지 못했다: " + otext)
                continue
            ln.mark(oa, ob, R_OBJECT)
            isomer = is_list and "ᵐ" in otext
            qs, nms = (q2, nm2) if isomer else (q1, names1)
            seen_exc = None
            for ci, ((a, b), q) in enumerate(zip(cells, qs)):
                if ci == oi or q is None:
                    continue
                if q == "excitation_energy":
                    if seen_exc is None:
                        seen_exc = ln.c[a:b]
                    else:
                        if ln.c[a:b] != seen_exc:
                            self.problem(ln, "들뜬 에너지 칸 셋이 같지 않다")
                        ln.mark(a, b, R_REPEAT)
                        continue
                self.table_cell(ln, a, b, q, obj, nms[ci])
        return header, data

    def magnet_table(self, doc, t, L, n0):
        data, header = self.data_rows(t, t["top_th_rows"])
        self.mark_header_lines(doc, n0, header)
        names = [x.strip() for x in L[0].strip().strip("|").split("|")]
        for k in data:
            ln = doc.line(n0 + k)
            cells = self.cells(ln.c)
            if len(cells) != 3:
                self.problem(ln, "칸 수가 3이 아니다")
                continue
            label = ln.c[cells[0][0]:cells[0][1]]
            ln.mark(*cells[0], R_ROWLABEL)
            lm = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", label)
            base, unit = (lm.group(1), lm.group(2)) if lm else (label, "")
            quantity = base.lower().replace(" ", "_")
            unit = "" if unit == "–" else unit
            for (a, b), nm in zip(cells[1:], names[1:]):
                obj = MAGNET_OBJECT.get(nm)
                if obj is None:
                    self.missing.append(("magnet_object", nm, f"{doc.id}:{ln.no}"))
                    continue
                self.table_cell(ln, a, b, quantity, obj, label, unit_default=unit)
        return header, data

    def nct_table(self, doc, t, L, n0, rows0, top):
        data, header = self.data_rows(t, top)
        self.mark_header_lines(doc, n0, header)
        if top == 0:                           # 이름 목록: 칸마다 화합물 이름 하나
            for k in data:
                ln = doc.line(n0 + k)
                for a, b in self.cells(ln.c):
                    if ln.c[a:b]:
                        self.add(ln, a, b, "표", ln.c[a:b], "listed_boron_agent", "", [], "", "낱말", None)
            return header, data
        hl = doc.line(n0)
        qs = self.columns(hl, rows0)
        oi = qs.index("@object") if "@object" in qs else None
        for k in data:
            ln = doc.line(n0 + k)
            cells = self.cells(ln.c)
            if len(cells) != len(rows0) or oi is None:
                self.problem(ln, "칸 수가 머리글과 다르다")
                continue
            oa, ob = cells[oi]
            obj = ln.c[oa:ob]
            ln.mark(oa, ob, R_OBJECT)
            for ci, ((a, b), q) in enumerate(zip(cells, qs)):
                if ci != oi and q is not None:
                    self.table_cell(ln, a, b, q, obj, rows0[ci])
        return header, data


class Doc:
    def __init__(self, meta):
        self.id, self.lang, self.topic, self.branch = meta["doc_id"], meta["language"], meta["topic"], meta["branch"]
        self.text = (MD_DIR / f"{self.id}.md").read_text(encoding="utf-8")
        self.lines = self.text.split("\n")
        starts, pos = [], 0
        for ln in self.lines:
            starts.append(pos)
            pos += len(ln) + 1
        self.starts = starts
        self.q_items = defaultdict(list)
        for it in Q.read(self.text):
            ls = starts[it["line"]]
            self.q_items[it["line"]].append({**it, "start": it["start"] - ls, "end": it["end"] - ls})
        self._lines = {}

    def line(self, i):
        """0부터 센 줄 번호 i의 Line."""
        if i not in self._lines:
            self._lines[i] = Line(self, i + 1, self.lines[i], self.q_items.get(i, []))
        return self._lines[i]


def infobox_end(lines):
    """정보 상자 끝: 2번째 줄부터 처음 나오는 본문 문단 줄의 0부터 센 번호."""
    for i in range(1, len(lines)):
        s = lines[i].strip()
        if s == "" or s.startswith("- ") or lines[i].startswith("|") or lines[i].startswith("#"):
            continue
        return i
    return len(lines)


def load_tables():
    all_t = json.loads((ROOT / "research_notes/stage2_table_shapes_rare_earth/tables.json").read_text(encoding="utf-8"))
    tables = [t for t in all_t if t["md_line_no"] is not None]      # 나머지는 마크다운에 남지 않은 안내 상자다
    return tables


def build():
    vocab = json.loads((HERE / "vocab.json").read_text(encoding="utf-8"))
    metas = yaml.safe_load((ROOT / "data/corpus/documents.yaml").read_text(encoding="utf-8"))["documents"]
    tables = load_tables()
    b = Builder(vocab)
    docs = [Doc(m) for m in metas]
    result = {"builder": b, "docs": docs, "table_kinds": Counter(), "scope": {}, "tables": []}
    assert len(tables) == 37, len(tables)
    for t in tables:
        d = next(x for x in docs if x.id == t["doc_id"])
        n0 = t["md_line_no"] - 1
        assert d.lines[n0:n0 + len(t["md_lines"])] == t["md_lines"], (t["doc_id"], t["md_line_no"])
    for d in docs:
        end = infobox_end(d.lines)
        scope = set()
        state = {"group": ""}
        for i in range(1, end):
            scope.add(i)
            b.infobox_line(d.line(i), state)
        d_tables = sorted((t for t in tables if t["doc_id"] == d.id), key=lambda t: t["md_line_no"])
        for t in d_tables:
            kind, (header, data) = b.table(d, t, d.lines)
            result["table_kinds"][kind] += 1
            n0 = t["md_line_no"] - 1
            for k in range(len(t["md_lines"])):
                scope.add(n0 + k)
            result["tables"].append((d, t, header, data))
        for i, s in enumerate(d.lines):
            if s.startswith("|") and i not in scope:
                b.problems.append(f"{d.id}:{i + 1}: tables.json에 없는 표 줄")
        result["scope"][d.id] = scope
    # 줄마다 순번과 id를 단다
    for d in docs:
        for i in sorted(d._lines):
            ln = d._lines[i]
            ln.places.sort(key=lambda r: r["start"])
            for n, r in enumerate(ln.places):
                r["id"] = f"{d.id}:{ln.no}:{n}"
                assert r["quote"][r["start"]:r["end"]] == r["raw"]
    b.records.sort(key=lambda r: ([m["doc_id"] for m in metas].index(r["doc_id"]), r["line"], r["start"]))
    return result


def coverage(result):
    """정보 상자 줄과 표 줄의 숫자 항목이 자리 또는 값이 아닌 범위 안에 있는지 센다."""
    out = {"checked": 0, "place": 0, "nonvalue": Counter(), "uncovered": [], "overlap": [], "cells": []}
    for d in result["docs"]:
        for i in sorted(result["scope"][d.id]):
            ln = d.line(i)
            spans = sorted((r["start"], r["end"]) for r in ln.places)
            for (s1, e1), (s2, e2) in zip(spans, spans[1:]):
                if s2 < e1:
                    out["overlap"].append((d.id, ln.no, ln.quote[s1:e1], ln.quote[s2:e2]))
            for it in d.q_items.get(i, []):
                out["checked"] += 1
                a, b = it["start"], it["end"]
                if any(s <= a and b <= e for s, e in spans):
                    out["place"] += 1
                    continue
                why = next((w for s, e, w in ln.nonvalue if s <= a and b <= e), None)
                if why:
                    out["nonvalue"][why] += 1
                else:
                    out["uncovered"].append((d.id, ln.no, it["raw"]))
    for d, t, header, data in result["tables"]:
        n0 = t["md_line_no"] - 1
        for k in data:
            ln = d.line(n0 + k)
            ok_spans = [(r["start"], r["end"]) for r in ln.places] + [(s, e) for s, e, w in ln.nonvalue if w in (R_OBJECT, R_REPEAT, R_NOTE, R_ROWLABEL)]
            for a, b in Builder.cells(ln.quote):
                if ln.quote[a:b] in ("", "-"):
                    continue
                if not any(s <= a and b <= e for s, e in ok_spans):
                    # 칸이 자리 + 덧붙임으로 나뉘어 덮였는지 본다
                    cover = sorted((max(s, a), min(e, b)) for s, e in ok_spans if s < b and a < e)
                    pos = a
                    for s, e in cover:
                        while pos < b and ln.quote[pos] == " ":
                            pos += 1
                        if s <= pos:
                            pos = max(pos, e)
                    if pos < b:
                        out["cells"].append((d.id, ln.no, ln.quote[a:b]))
    return out


def write(result):
    recs = result["builder"].records
    body = ",\n".join(json.dumps(r, ensure_ascii=False) for r in recs)
    (HERE / "values.json").write_text("[\n" + body + "\n]\n", encoding="utf-8")


def main():
    result = build()
    b = result["builder"]
    cov = coverage(result)
    write(result)
    recs = b.records
    print(f"문서 {len(result['docs'])}개, 자리 {len(recs)}개")
    print("표 모양:", dict(result["table_kinds"]))
    wc = Counter(r["where"] for r in recs)
    print("자리 (where별):", dict(wc))
    for d in result["docs"]:
        c = Counter(r["where"] for r in recs if r["doc_id"] == d.id)
        print(f"  {d.id}: 정보 상자 {c['정보 상자']}, 표 {c['표']}")
    print("자리 (kind별):", dict(Counter(r["kind"] for r in recs)))
    print(f"덮임 검사: 항목 {cov['checked']}개 = 자리 안 {cov['place']} + 값이 아닌 범위 {sum(cov['nonvalue'].values())} "
          f"{dict(cov['nonvalue'])} + 못 덮음 {len(cov['uncovered'])}")
    bad = False
    if cov["uncovered"]:
        bad = True
        print("못 덮은 항목:")
        for x in cov["uncovered"]:
            print("  ", x)
    if cov["overlap"]:
        bad = True
        print("겹친 자리:", cov["overlap"])
    if cov["cells"]:
        bad = True
        print("자리도 표시도 없는 표 칸:", cov["cells"])
    else:
        print("표 데이터 칸 검사: 비지 않은 모든 칸이 자리 또는 표시로 덮였다")
    if b.missing:
        bad = True
        print("vocab에 없는 것:")
        for x in sorted(set(b.missing)):
            print("  ", x)
    if b.problems:
        bad = True
        print("규칙대로 읽지 못한 것:")
        for x in b.problems:
            print("  ", x)
    print(f"숫자 규칙에 안 맞아 낱말이 된 칸(숫자가 든 것): {len(b.fallback_words)}개")
    for x in b.fallback_words:
        print("  ", x)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
