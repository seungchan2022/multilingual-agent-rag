"""희토류 원소 값 목록(values.json)에서 같은 것을 말하는 자리끼리 묶어 값이 같은지 다른지 가른다(이슈 #7, 값 목록 2단계).

실행: .venv/bin/python research_notes/stage2_values_rare_earth/compare.py
읽는 것: values.json, vocab.json(둘 다 읽기만 한다). 쓰는 것: compare.json, review.md.

묶는 틀: (대상, 양, 조건)이 같은 자리끼리 한 묶음이다. 비교하는 단위는 "곳"이다.
  - 정보 상자 자리와 본문 자리는 하나가 곳 하나다.
  - 표에서는 같은 문서, 같은 표(|로 시작하는 줄이 이어진 덩어리), 같은 (대상, 양, 조건)의 자리를 한 곳으로 합치고 곳의 값은 값의 집합이다.
    multi 자리는 reps마다 집합의 한 원소가 된다. 한 곳에 함께 적은 단위 환산(reps의 둘째부터)은 같은 곳이라 비교하지 않는다.
두 곳의 값이 같은 것은 두 집합의 원소가 서로 하나씩 짝지어 같을 때(집합이 같을 때)뿐이다.

"같은 값"의 규칙(사용자와 정한 것, 구현은 이 규칙 그대로다):
  - 같다: 숫자가 정확히 같고 적는 방식만 다를 때(쉼표, 끝의 0, 오차 표기, 끝의 #).
  - 다르다: 반올림·어림 표기(est. 약 ~ about), 범위와 그 안의 한 값, 끝이 하나라도 다른 두 범위, 다른 부등호.
  - 단위가 다르면 정확한 분수(fractions.Fraction)로 바꿔 정확히 같을 때만 같다. 허용 오차도 반올림도 없다.
    (Decimal은 5/9처럼 끝없는 수에서 반올림하므로 분수를 쓴다. 적힌 십진수는 그대로 정확한 분수가 된다.)
  - 낱말은 다듬은 글(공백, U+00AD, 영 너비 글자, 라틴 대소문자, vocab["word"], 마이너스 기호)이 같을 때 같고 숫자 값과는 늘 다르다.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "src" / "domain_select"))
import quantities as Q  # noqa: E402

MD_DIR = ROOT / "data" / "corpus" / "markdown"
SKIP = Q.SKIP
SUP = {c: str(i) for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}

SCOPE_SAME_DOC = "같은 문서"
SCOPE_SAME_LANG = "같은 언어의 다른 문서"
SCOPE_OTHER_LANG = "반대 언어"


# --- 단위와 숫자 -------------------------------------------------------------
def _exact(f):
    """quantities.UNITS의 곱(float)을 적힌 십진수 그대로의 정확한 분수로."""
    return Fraction(Decimal(repr(f))) if isinstance(f, float) else Fraction(f)


YEAR_UNITS = {"년", "year", "years", "yr"}
UNIT_ALIAS = {"a": "y", "u": "Da"}                     # a는 해(annum), u는 Da와 같은 단위
CELSIUS_OFFSET = Fraction(27315, 100)


def clean_unit(unit):
    """단위 글자를 다듬는다: 영 너비 글자를 빼고, 가운뎃점·µ를 quantities.norm대로 맞추고, 별칭(a→y, u→Da)을 적용한다."""
    u = "".join(ch for ch in unit if ch not in SKIP).strip()
    u = Q.norm(u)
    return UNIT_ALIAS.get(u, u)


def unit_info(unit):
    """(차원, 곱 또는 None). 모르는 단위는 ('?'+글자, 1)이라 글자가 같을 때만 같은 차원이다. 빈 단위의 차원은 ''."""
    if not unit:
        return "", Fraction(1)
    if unit in Q.UNITS:
        dim, f = Q.UNITS[unit]
        return dim, _exact(f)
    return "?" + unit, Fraction(1)


def to_base(x, unit):
    """수 x(Fraction)를 단위 unit에서 기준 단위로. 온도는 K로(K = °C + 273.15, °C = (°F - 32) × 5/9)."""
    if unit in Q.CELSIUS:
        return x + CELSIUS_OFFSET
    if unit in Q.FAHRENHEIT:
        return (x - 32) * Fraction(5, 9) + CELSIUS_OFFSET
    return x * unit_info(unit)[1]


NUM_RE = re.compile(r"^([+\-−–]?)(\d[\d,]*(?:\.\d+)?)(?:\s?×\s?10(?:([⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)|\^\{?([+−-]?\d+)\}?)|[eE]([+\-]?\d+))?$")


def parse_num(s):
    """적힌 수를 정확한 분수로. 읽을 수 없으면 None. 쉼표를 빼고 부호(− –)와 지수(×10⁻⁶, ×10^3, E+6)를 읽는다."""
    m = NUM_RE.match(s.strip())
    if not m:
        return None
    sign, base, sup, car, e = m.groups()
    x = Fraction(Decimal(base.replace(",", "")))
    exp = 0
    if sup:
        exp = int("".join(SUP.get(ch, "") for ch in sup)) * (-1 if sup.startswith("⁻") else 1)
    elif car:
        exp = int(car.replace("−", "-"))
    elif e:
        exp = int(e)
    x *= Fraction(10) ** exp
    return -x if sign in ("-", "−", "–") else x


EN_MAG = {"thousand": 3, "million": 6, "billion": 9, "trillion": 12}
EN_MAG_RE = re.compile(r"\s?(thousand|million|billion|trillion)(?![A-Za-z])", re.I)
KO_MAG_RE = re.compile(r"((?:천|백)?(?:조|억|만)?)(?!큼)")
KO_TIER = {"천": 1000, "백": 100, "조": 10 ** 12, "억": 10 ** 8, "만": 10 ** 4}


def magnitude(raw, rep):
    """rep의 숫자 바로 뒤에 영어(million 등)나 한국어(백만, 억, 만) 큰 수 낱말이 있으면 (곱, 낱말 뒤 단위 또는 '').
    rep["text"]는 낱말 앞에서 끝나므로 raw에서 text 뒤를 본다. 없으면 (1, '')."""
    pos = raw.find(rep["text"]) if raw else -1
    if pos < 0:
        return Fraction(1), ""
    end = pos + len(rep["text"])
    m = EN_MAG_RE.match(raw, end)
    if m:
        mult = Fraction(10) ** EN_MAG[m.group(1).lower()]
    else:
        m = KO_MAG_RE.match(raw, end)
        if not m or not m.group(1):
            return Fraction(1), ""
        mult = Fraction(1)
        for ch in m.group(1):
            mult *= KO_TIER[ch]
    u = Q.find_unit(raw, m.end())
    return mult, (u[0] if u else "")


APPROX_CLASS = {}
for _w in ("about", "approximately", "approx.", "around", "roughly", "nearly", "almost", "ca.", "c.", "est.", "~", "≈",
           "약", "대략", "거의", "some"):
    APPROX_CLASS[_w] = "≈"
for _w in ("over", "more than", ">", "초과", "above"):
    APPROX_CLASS[_w] = ">"
for _w in ("at least", "≥", "이상"):
    APPROX_CLASS[_w] = "≥"
for _w in ("under", "less than", "<", "미만", "below"):
    APPROX_CLASS[_w] = "<"
for _w in ("at most", "≤", "이하", "up to"):
    APPROX_CLASS[_w] = "≤"


def approx_class(a):
    """어림 말·부등호를 같은 뜻끼리 한 기호로. 없으면 ''. 모르는 말은 소문자 글자 그대로."""
    a = " ".join(a.split()).lower()
    return APPROX_CLASS.get(a, a)


def num_text(x):
    """분수를 읽기 쉬운 십진수 글자로(끝나지 않는 분수는 분수 그대로)."""
    d = Decimal(x.numerator) / Decimal(x.denominator)
    if Fraction(d) != x:
        return f"{x.numerator}/{x.denominator}"
    s = format(d.normalize(), "f")
    return s


def member(rep, kind, raw="", unit_default=""):
    """곳의 값 집합의 원소 하나. rep는 values.json의 rep. 돌려주는 값: {key, text, approx(적힌 그대로), est, word}.
    같은 값인지는 key가 같은지로 가른다."""
    if kind == "낱말":
        return {"key": ("w", WORD(rep["text"])), "text": rep["text"], "approx": "", "est": False, "word": True, "dim": None}
    unit = clean_unit(rep.get("unit", ""))
    mult, tail_unit = magnitude(raw, rep)
    if not unit and tail_unit:
        unit = clean_unit(tail_unit)
    if not unit and unit_default:
        unit = clean_unit(unit_default)
    lo = parse_num(rep["num"])
    hi = parse_num(rep["range_to"]) if rep.get("range_to") else None
    if unit in YEAR_UNITS and lo is not None and hi is None and mult == 1 and lo.denominator == 1 and 1000 <= lo <= 2100:
        unit = ""                     # 1886년은 연도(날짜)이지 1886년 동안이 아니다. quantities.read도 날짜로 읽는다.
    if lo is None or (rep.get("range_to") and hi is None):
        return {"key": ("x", rep["text"]), "text": rep["text"], "approx": rep.get("approx", ""), "est": rep.get("est_mark", False),
                "word": False, "dim": "?읽지 못함"}
    dim = unit_info(unit)[0]
    lo = to_base(lo * mult, unit)
    hi = to_base(hi * mult, unit) if hi is not None else None
    ac = approx_class(rep.get("approx", ""))
    shown = num_text(parse_num(rep["num"]) * mult)
    if hi is not None:
        shown += "–" + num_text(parse_num(rep["range_to"]) * mult)
    shown = ((rep.get("approx", "") + " ") if rep.get("approx") else "") + shown + (" " + unit if unit else "")
    return {"key": ("n", dim, lo, hi, ac), "text": shown, "approx": rep.get("approx", ""), "est": rep.get("est_mark", False),
            "word": False, "dim": dim}


def same_member(a, b):
    return a["key"] == b["key"]


# --- 낱말 ---------------------------------------------------------------------
_VOCAB = json.loads((HERE / "vocab.json").read_text(encoding="utf-8"))
WORD_MAP = {k.lower(): v for k, v in _VOCAB["word"].items()}
WORD_SYMBOLS = sorted((k for k in WORD_MAP if not k.isalpha()), key=len, reverse=True)


def WORD(text):
    """낱말을 비교하기 좋게: 영 너비 글자·소프트 하이픈을 빼고, 공백을 하나로, 소문자로, 마이너스 기호를 -로 맞춘 뒤
    vocab["word"]로 글 전체를, 안 맞으면 기호(β- 등)를 낱말 경계에서 바꾼다."""
    s = "".join(ch for ch in text if ch not in SKIP)
    s = " ".join(s.split()).lower().replace("−", "-").replace("–", "-")
    if s in WORD_MAP:
        return WORD_MAP[s]
    for sym in WORD_SYMBOLS:
        s = re.sub(r"(?<![\w])" + re.escape(sym) + r"(?![\w])", WORD_MAP[sym], s)
    return s


# --- 곳 ---------------------------------------------------------------------
def header_unit(label):
    """표 열 머리글의 끝 괄호 글이 단위이면 그 단위, 아니면 ''. 예: 'DE (MeV)' -> 'MeV', 'Z(p)' -> ''."""
    m = re.search(r"\(([^()]*)\)\s*$", label)
    if not m:
        return ""
    u = clean_unit(m.group(1))
    return u if (u in Q.UNITS or u == "Da") else ""


def table_ids(doc_id, cache={}):
    """문서의 줄 번호(1부터) -> 그 줄이 든 표 덩어리의 첫 줄 번호(|로 시작하는 줄이 이어진 덩어리)."""
    if doc_id not in cache:
        out, start = {}, None
        for i, ln in enumerate((MD_DIR / f"{doc_id}.md").read_text(encoding="utf-8").split("\n"), 1):
            if ln.startswith("|"):
                start = start or i
                out[i] = start
            else:
                start = None
        cache[doc_id] = out
    return cache[doc_id]


NUMTOK = re.compile(r"\d[\d,]*(?:\.\d+)?")


def partial_body(rec):
    """본문 자리의 raw에 reps가 담지 못한 숫자나 범위 끝이 있는가(그러면 첫 값만 비교되어 다르게 나올 수 있다)."""
    raw = rec["raw"]
    have = Counter()
    for r in rec["reps"]:
        for t in NUMTOK.findall(r["text"] + " " + (r.get("range_to") or "")):
            have[t.replace(",", "")] += 1
    need = Counter(t.replace(",", "") for t in NUMTOK.findall(raw))
    if need - have:
        return True
    if len(rec["reps"]) > 1 and not rec.get("multi"):
        for r in rec["reps"][1:]:
            p = raw.find(r["text"])
            if p < 0 or raw.rfind("(", 0, p) <= raw.rfind(")", 0, p):       # 괄호 안에 적힌 환산이 아님
                return True
    return False


def build_places(records):
    """자리 목록을 곳으로 합친다. 돌려주는 값: 곳 dict 목록."""
    buckets = {}
    for r in records:
        if r["where"] == "표":
            key = (r["doc_id"], "t", table_ids(r["doc_id"])[r["line"]], r["object"], r["quantity"], r["condition"])
        else:
            key = (r["doc_id"], "p", r["id"], r["object"], r["quantity"], r["condition"])
        buckets.setdefault(key, []).append(r)
    places = []
    for recs in buckets.values():
        first = recs[0]
        members, notes, raws, quotes = [], [], [], {}
        partial = False
        for r in recs:
            unit_default = header_unit(r["label"]) if r["where"] == "표" else ""
            reps = r["reps"] if (r.get("multi") and r["kind"] == "수") else r["reps"][:1]
            for rep in reps:
                members.append(member(rep, r["kind"], r["raw"], unit_default))
            for n in r["note"]:
                if n not in notes:
                    notes.append(n)
            raws.append(r["raw"])
            quotes[r["line"]] = r["quote"]
            if r["where"] == "본문" and partial_body(r):
                partial = True
        uniq = {}
        for m in members:
            uniq.setdefault(m["key"], m)
        places.append({
            "place": f"{first['doc_id']}:{first['line']}:{first['quantity']}", "doc_id": first["doc_id"], "lang": first["lang"],
            "where": first["where"], "lines": sorted(quotes), "members": list(uniq.values()), "keys": frozenset(uniq),
            "raws": raws, "notes": notes, "quotes": quotes, "uncertain": any(r.get("uncertain") for r in recs),
            "uncertain_reason": next((r["uncertain_reason"] for r in recs if r.get("uncertain")), ""),
            "partial": partial, "given": next((r["given"] for r in recs if "given" in r), None), "object": first["object"], "quantity": first["quantity"], "condition": first["condition"],
            "word_digits": any(m["word"] and re.search(r"\d", m["text"]) for m in members),
        })
    return places


# --- 묶음 -------------------------------------------------------------------
def scope_of(a, b):
    if a["doc_id"] == b["doc_id"]:
        return SCOPE_SAME_DOC
    return SCOPE_SAME_LANG if a["lang"] == b["lang"] else SCOPE_OTHER_LANG


def judge_group(places):
    """한 (대상, 양, 조건) 묶음의 판정. 돌려주는 값: {verdict, scopes, review, reasons, classes(곳마다 번호)}."""
    n = len(places)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if places[i]["keys"] == places[j]["keys"]:
                parent[find(i)] = find(j)
    roots = sorted({find(i) for i in range(n)}, key=lambda r: min(i for i in range(n) if find(i) == r))
    cls = [roots.index(find(i)) for i in range(n)]
    verdict = "같음" if len(roots) == 1 else "다름"
    scopes = set()
    for i in range(n):
        for j in range(i + 1, n):
            if cls[i] != cls[j]:
                scopes.add(scope_of(places[i], places[j]))
    reasons = []
    if verdict == "다름":
        if any(p["word_digits"] for p in places):
            reasons.append("줄 전체 값")
        wp = [(p, cls[i]) for i, p in enumerate(places) if any(m["word"] for m in p["members"])]
        if any(a["lang"] != b["lang"] and ca != cb for a, ca in wp for b, cb in wp):
            reasons.append("두 언어 낱말")
        if any(frozenset(places[i]["notes"]) != frozenset(places[j]["notes"])
               for i in range(n) for j in range(i + 1, n) if cls[i] != cls[j]):
            reasons.append("덧붙인 말 다름")
        marks = {(m["approx"], m["est"]) for p in places for m in p["members"] if not m["word"]}
        if len(marks) > 1:
            reasons.append("어림 표시")
        if any(len(p["members"]) > 1 for p in places):
            reasons.append("여러 값")
        dims = {m["dim"] for p in places for m in p["members"] if not m["word"]}
        if len(dims) > 1:
            reasons.append("단위를 못 바꿈")
        if any(m["dim"] == "?읽지 못함" for p in places for m in p["members"]):
            reasons.append("숫자를 못 읽음")
        if any(p["where"] == "본문" for p in places):
            reasons.append("본문 값")
            if any(p["uncertain"] for p in places if p["where"] == "본문"):
                reasons.append("불확실 표시")
            if any(p["partial"] for p in places):
                reasons.append("본문 값의 일부만 비교")
    return {"verdict": verdict, "scopes": sorted(scopes), "review": bool(reasons), "reasons": reasons, "classes": cls}


def condition_variants(places):
    """(대상, 양)이 두 조건 이상으로 놓였고, 서로 다른 두 문서가 각자 상대에 없는 조건을 갖는 것."""
    by = defaultdict(lambda: defaultdict(set))          # (대상, 양) -> 문서 -> 조건 집합
    for p in places:
        by[(p["object"], p["quantity"])][p["doc_id"]].add(p["condition"])
    out = []
    for (obj, qty), docs in sorted(by.items()):
        names = sorted(docs)
        hit = None
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if docs[a] - docs[b] and docs[b] - docs[a]:
                    hit = (a, b)
                    break
            if hit:
                break
        if hit:
            out.append({"object": obj, "quantity": qty, "conditions_by_doc": {d: sorted(c) for d, c in sorted(docs.items())},
                        "example_docs": list(hit)})
    return out


def apply_keys(records, vocab):
    """묶기 전에 vocab["place_override"](자리 id -> 바꿀 object/quantity/condition)를 먼저, 이어서 vocab["quantity_alias"]
    ("대상|양" -> "대상|양")를 적용한다. 바뀐 자리에는 원래 열쇠를 given으로 남긴다. values.json은 고치지 않고 복사본을 쓴다.
    덮어쓸 id나 바꿀 열쇠가 어느 자리에도 맞지 않으면 ValueError(오타가 조용히 지나가지 않게)."""
    out = [dict(r) for r in records]
    by_id = {r["id"]: r for r in out}
    bad = [i for i in vocab.get("place_override", {}) if i not in by_id]
    for i, change in vocab.get("place_override", {}).items():
        r = by_id.get(i)
        if r is None:
            continue
        if not set(change) <= {"object", "quantity", "condition"}:
            bad.append(f"{i}: 알 수 없는 칸 {sorted(set(change) - {'object', 'quantity', 'condition'})}")
        r.setdefault("given", {"object": r["object"], "quantity": r["quantity"], "condition": r["condition"]})
        r.update({k: v for k, v in change.items() if k in ("object", "quantity", "condition")})
    present = {f"{r['object']}|{r['quantity']}" for r in out}
    bad += [f"별칭 원본 {src}" for src in vocab.get("quantity_alias", {}) if src not in present]
    for src, dst in vocab.get("quantity_alias", {}).items():
        obj, qty = dst.split("|", 1)
        for r in out:
            if f"{r['object']}|{r['quantity']}" == src:
                r.setdefault("given", {"object": r["object"], "quantity": r["quantity"], "condition": r["condition"]})
                r["object"], r["quantity"] = obj, qty
    if bad:
        raise ValueError(f"vocab의 place_override나 quantity_alias가 맞는 자리를 못 찾았다: {bad}")
    for r in out:
        if "given" in r and all(r["given"][k] == r[k] for k in ("object", "quantity", "condition")):
            del r["given"]
    return out


def run(records, vocab=None):
    vocab = vocab or json.loads((HERE / "vocab.json").read_text(encoding="utf-8"))
    places = build_places(apply_keys(records, vocab))
    groups = defaultdict(list)
    for p in places:
        groups[(p["object"], p["quantity"], p["condition"])].append(p)
    out, singletons = [], 0
    for key in sorted(groups):
        ps = groups[key]
        if len(ps) == 1:
            singletons += 1
            continue
        j = judge_group(ps)
        out.append({
            "object": key[0], "quantity": key[1], "condition": key[2], "verdict": j["verdict"], "scopes": j["scopes"],
            "review": j["review"], "reasons": j["reasons"],
            "places": [{"place": p["place"], "doc_id": p["doc_id"], "lang": p["lang"], "where": p["where"], "lines": p["lines"],
                        "values": [m["text"] for m in p["members"]], "raws": p["raws"], "notes": p["notes"], "class": c,
                        "uncertain_reason": p["uncertain_reason"], "quotes": {str(k): v for k, v in p["quotes"].items()},
                        **({"given": p["given"]} if p["given"] else {})}
                       for p, c in zip(ps, j["classes"])],
        })
    counts = {"places": len(places), "groups": len(groups), "singletons": singletons, "groups_2plus": len(out),
              "same": sum(g["verdict"] == "같음" for g in out), "different": sum(g["verdict"] == "다름" for g in out),
              "review": sum(g["review"] for g in out), "different_no_review": sum(g["verdict"] == "다름" and not g["review"] for g in out),
              "by_scope": {s: sum(s in g["scopes"] for g in out) for s in (SCOPE_SAME_DOC, SCOPE_SAME_LANG, SCOPE_OTHER_LANG)},
              "reasons": dict(Counter(r for g in out for r in g["reasons"]).most_common())}
    variants = condition_variants(places)
    counts["condition_variants"] = len(variants)
    return {"counts": counts, "groups": out, "condition_variants": variants}


# --- review.md ---------------------------------------------------------------
def span(text):
    fence = "`" * (max((len(m) for m in re.findall(r"`+", text)), default=0) + 1)
    return f"{fence} {text} {fence}" if "`" in text else f"`{text}`"


def review_md(result):
    c = result["counts"]
    lines = ["# 값 비교 검토", "",
             f"- 곳 {c['places']}개, 묶음 {c['groups']}개 (곳이 하나뿐인 묶음 {c['singletons']}개는 비교하지 않음)",
             f"- 곳이 둘 이상인 묶음 {c['groups_2plus']}개: 같음 {c['same']}, 다름 {c['different']} (읽을 것 {c['review']}, 안 읽어도 됨 {c['different_no_review']})",
             "- 다름 묶음의 범위: " + ", ".join(f"{k} {v}" for k, v in c["by_scope"].items()),
             "- 읽을 이유: " + ", ".join(f"{k} {v}" for k, v in c["reasons"].items()),
             f"- 조건 갈림 후보 {c['condition_variants']}개 (compare.json의 condition_variants)", ""]

    def section(g, short):
        out = [f"## {g['object']} / {g['quantity']} / {g['condition'] or '(조건 없음)'}  [{g['verdict']}; {', '.join(g['scopes'])}]"]
        if g["reasons"]:
            out.append("이유: " + ", ".join(g["reasons"]))
        for p in g["places"]:
            vals = " | ".join(p["values"])
            head = f"- 묶음{p['class']} {p['doc_id']}:{','.join(map(str, p['lines']))} ({p['where']}) 값 {vals}"
            if short:
                out.append(head + "  raw " + " / ".join(span(r) for r in p["raws"]))
                continue
            out.append(head)
            for ln, q in p["quotes"].items():
                out.append(f"  - 줄 {ln}: {span(q)}")
            out.append("  - raw: " + " / ".join(span(r) for r in p["raws"]))
            if p["notes"]:
                out.append("  - 덧붙인 말: " + "; ".join(p["notes"]))
            if p["uncertain_reason"]:
                out.append("  - 불확실: " + p["uncertain_reason"])
        out.append("")
        return out

    lines += ["# 읽을 묶음", ""]
    for g in result["groups"]:
        if g["review"]:
            lines += section(g, False)
    lines += ["# 다름이지만 읽지 않아도 되는 묶음", ""]
    for g in result["groups"]:
        if g["verdict"] == "다름" and not g["review"]:
            lines += section(g, True)
    return "\n".join(lines) + "\n"


def main():
    records = json.loads((HERE / "values.json").read_text(encoding="utf-8"))
    result = run(records)
    (HERE / "compare.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "review.md").write_text(review_md(result), encoding="utf-8")
    c = result["counts"]
    print(f"곳 {c['places']}개, 묶음 {c['groups']}개, 곳이 하나뿐인 묶음 {c['singletons']}개")
    print(f"곳이 둘 이상인 묶음 {c['groups_2plus']}개: 같음 {c['same']}, 다름 {c['different']} (읽을 것 {c['review']}, 안 읽어도 됨 {c['different_no_review']})")
    print("다름 묶음의 범위:", c["by_scope"])
    print("읽을 이유:", c["reasons"])
    print(f"조건 갈림 후보: {c['condition_variants']}개")


if __name__ == "__main__":
    main()
