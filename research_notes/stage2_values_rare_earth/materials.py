"""언어마다 질문 재료(여러 문서 연결 쌍, 표·수치·조건 단독)를 정해진 순서로 제안한다(이슈 #7).

실행: .venv/bin/python research_notes/stage2_values_rare_earth/materials.py [부딪히는 값 목록 경로]
      (경로를 주지 않으면 data/questions/known_conflicts.json)
읽는 것(읽기만 한다): values.json, vocab.json, data/corpus/documents.yaml, data/corpus/markdown/*.md, 부딪히는 값 목록
쓰는 것: materials.json, materials.md

이 프로그램은 후보를 정해진 순서로 내놓을 뿐이다. 원문 확인은 사람이 한다.

풀: values.json의 숫자 자리(kind == "수", multi 아님) 가운데 한 언어 주제 문서(documents.yaml의 branch가 "한국어만"/"영어만")의 것.
적격인 자리:
  1) 열쇠는 compare.apply_keys를 거친 (대상, 양, 조건).
  2) 그 묶음에 반대 언어의 자리가 없다(종류와 상관없이 values.json 전체 자리로 묶는다).
  3) known_conflicts의 자리(문서, 줄, raw)가 아니고, 그 줄이 recheck_step3.blocked_B에 안 막힌다.
  4) 어림 말(approx)도 추정 표시(est_mark)도 없다(reps 전부).
표시(제외하지 않는다): 같은 숫자(쉼표와 끝의 "(6)" 같은 오차를 뗀 것)가 반대 언어 문서 어디에든 있으면 문서:줄을 적는다.

A) 여러 문서 연결 쌍: 적격인 서로 다른 문서의 두 자리, 대상이 다르고 양과 조건이 같고, 단위를 바꿀 수 있고(compare.member가 같은 차원으로 읽음),
   범위가 아니고, 값이 다르다. 더 큰 쪽을 정확한 분수로 정한다. 순서: 양 열쇠를 정렬해 양마다 돌아가며, 양 안에서는 (문서 쌍, 줄) 순으로
   두 자리가 아직 안 쓰인 다음 쌍을 하나씩 가져간다. 언어마다 24쌍까지, 자리는 한 쌍에만 나온다.
B) 표·수치·조건 단독: 적격인 자리 가운데 표 칸이거나, 같은 문서에 같은 (대상, 양)이면서 조건이 다른 자리(적격 여부와 상관없이)가 있는 것.
   A에 쓰인 자리는 뺀다. 순서: 문서(정렬)마다 돌아가며, 문서 안에서는 양 열쇠를 정렬해 양마다 돌아가며(양 안은 줄 순). 언어마다 12개까지.
"""
import json
import re
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import compare as cp  # noqa: E402
import recheck_step3 as rc  # noqa: E402

VALUES = HERE / "values.json"
VOCAB = HERE / "vocab.json"
DOCS_YAML = ROOT / "data" / "corpus" / "documents.yaml"
MD_DIR = ROOT / "data" / "corpus" / "markdown"
OUT_JSON = HERE / "materials.json"
OUT_MD = HERE / "materials.md"
DEFAULT_CONFLICTS = rc.DEFAULT_CONFLICTS

MAX_A = 24
MAX_B = 12
BRANCH = {"ko": "한국어만", "en": "영어만"}
LANG_NAME = {"ko": "한국어", "en": "영어"}
TOKEN = re.compile(r"(?<!\d)(?<!\d\.)\d+(?:\.\d+)?(?!\d)(?!\.\d)")       # 검사기의 값 규칙과 같은 경계
QUOTE_AROUND = 100


# --- 입력 -------------------------------------------------------------------
def corpus_docs():
    return yaml.safe_load(DOCS_YAML.read_text(encoding="utf-8"))["documents"]


def md_lines(doc_id, cache={}):
    if doc_id not in cache:
        cache[doc_id] = (MD_DIR / f"{doc_id}.md").read_text(encoding="utf-8").split("\n")
    return cache[doc_id]


def pool_docs(docs):
    """언어 -> 한 언어 주제 문서 doc_id 목록(정렬)."""
    return {lang: sorted(d["doc_id"] for d in docs if d["language"] == lang and d["branch"] == BRANCH[lang]) for lang in BRANCH}


def opposite_index(docs):
    """언어 -> {숫자 글자: [(문서, 줄)]}: 그 언어의 *반대* 언어 문서 전부에서, 쉼표를 뗀 줄에 있는 숫자(경계 규칙은 검사기와 같다)."""
    by_lang = {}
    for lang in BRANCH:
        idx = defaultdict(list)
        for d in docs:
            if d["language"] == lang:
                continue
            for n, line in enumerate(md_lines(d["doc_id"]), 1):
                for tok in dict.fromkeys(TOKEN.findall(line.replace(",", ""))):
                    idx[tok].append(f"{d['doc_id']}:{n}")
        by_lang[lang] = idx
    return by_lang


def number_texts(rec):
    """자리의 숫자 글자들: 각 rep의 num과 range_to에서 쉼표와 끝의 오차 "(6)"을 뗀 것."""
    out = []
    for rep in rec["reps"]:
        for s in (rep["num"], rep.get("range_to")):
            if s:
                t = re.sub(r"\(\d+\)$", "", s.replace(",", ""))
                if t not in out:
                    out.append(t)
    return out


# --- 적격 --------------------------------------------------------------------
def build(records, docs, targets):
    """적격 자리와 필요한 색인. 돌려주는 값: {pool, keyed(키 적용한 전체 자리), eligible{언어: [자리]}}."""
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    keyed = cp.apply_keys(records, vocab)
    langs_of = defaultdict(set)
    for r in keyed:
        langs_of[(r["object"], r["quantity"], r["condition"])].add(r["lang"])
    pool = pool_docs(docs)
    opp = opposite_index(docs)
    eligible = {lang: [] for lang in BRANCH}
    for r in keyed:
        lang = r["lang"]
        if r["doc_id"] not in pool[lang] or r["kind"] != "수" or r.get("multi"):
            continue
        if langs_of[(r["object"], r["quantity"], r["condition"])] != {lang}:
            continue
        if any(rep.get("approx") or rep.get("est_mark") for rep in r["reps"]):
            continue
        line = md_lines(r["doc_id"])[r["line"] - 1]
        if rc.blocked_A(r["doc_id"], r["line"], r, targets) or rc.blocked_B(r["doc_id"], line, targets):
            continue
        m = cp.member(r["reps"][0], r["kind"], r["raw"], cp.header_unit(r["label"]) if r["where"] == "표" else "")
        flags = {"opposite_number": [{"number": t, "at": opp[lang][t]} for t in number_texts(r) if t in opp[lang]]}
        if r.get("uncertain"):
            flags["uncertain"] = r.get("uncertain_reason", "")
        eligible[lang].append({
            "id": r["id"], "doc_id": r["doc_id"], "line": r["line"], "raw": r["raw"], "object": r["object"], "quantity": r["quantity"],
            "condition": r["condition"], "where": r["where"], "quote": line, "start": r["start"], "end": r["end"], "value": m["text"],
            "flags": flags,
            # 아래는 쌍을 정하는 데 쓰는 계산값이고 JSON에는 적지 않는다.
            "_dim": m["dim"] if m["key"][0] == "n" and m["key"][3] is None else None,
            "_lo": m["key"][2] if m["key"][0] == "n" and m["key"][3] is None else None,
        })
    return {"pool": pool, "keyed": keyed, "eligible": eligible}


# --- A: 쌍 -------------------------------------------------------------------
def comparable(a, b):
    return (a["doc_id"] != b["doc_id"] and a["object"] != b["object"] and a["quantity"] == b["quantity"] and a["condition"] == b["condition"]
            and a["_dim"] is not None and a["_dim"] == b["_dim"] and a["_lo"] != b["_lo"])


def pick_pairs(places, limit=MAX_A):
    """양 열쇠를 정렬해 양마다 돌아가며, 양 안에서는 (문서 쌍, 줄) 순으로 두 자리가 아직 안 쓰인 다음 쌍을 가져간다."""
    by_q = defaultdict(list)
    for p in places:
        if p["_dim"] is not None:
            by_q[p["quantity"]].append(p)
    queues = {}
    for q in sorted(by_q):
        ps = sorted(by_q[q], key=lambda p: (p["doc_id"], p["line"], p["id"]))
        pairs = [(a, b) for i, a in enumerate(ps) for b in ps[i + 1:] if comparable(a, b)]
        pairs.sort(key=lambda ab: (ab[0]["doc_id"], ab[1]["doc_id"], ab[0]["line"], ab[1]["line"], ab[0]["id"], ab[1]["id"]))
        queues[q] = [0, pairs]
    used, out = set(), []
    progress = True
    while len(out) < limit and progress:
        progress = False
        for q in sorted(queues):
            if len(out) >= limit:
                break
            pos, pairs = queues[q]
            while pos < len(pairs) and (pairs[pos][0]["id"] in used or pairs[pos][1]["id"] in used):
                pos += 1
            queues[q][0] = pos
            if pos < len(pairs):
                a, b = pairs[pos]
                used.update((a["id"], b["id"]))
                out.append({"quantity": q, "condition": a["condition"], "a": a, "b": b, "larger": "a" if a["_lo"] > b["_lo"] else "b"})
                queues[q][0] = pos + 1
                progress = True
    return out


# --- B: 단독 -----------------------------------------------------------------
def has_sibling_condition(keyed):
    """(문서, 대상, 양) -> 조건 집합(적격 여부와 상관없이 values.json 전체 자리)."""
    out = defaultdict(set)
    for r in keyed:
        out[(r["doc_id"], r["object"], r["quantity"])].add(r["condition"])
    return out


def pick_singles(places, conds, pool_docs_, used, limit=MAX_B):
    """문서(정렬)마다 돌아가며, 문서 안에서는 양 열쇠를 정렬해 양마다 돌아가며(양 안은 줄 순) 하나씩."""
    per_doc = {}
    for d in pool_docs_:
        by_q = defaultdict(list)
        for p in places:
            if p["doc_id"] != d or p["id"] in used:
                continue
            if p["where"] == "표" or len(conds[(d, p["object"], p["quantity"])]) >= 2:
                by_q[p["quantity"]].append(p)
        qs = sorted(by_q)
        for q in qs:
            by_q[q].sort(key=lambda p: (p["line"], p["id"]))
        order = []
        for i in range(max((len(v) for v in by_q.values()), default=0)):
            order += [by_q[q][i] for q in qs if i < len(by_q[q])]
        per_doc[d] = order
    out = []
    for i in range(max((len(v) for v in per_doc.values()), default=0)):
        for d in pool_docs_:
            if i < len(per_doc[d]) and len(out) < limit:
                out.append(per_doc[d][i])
    return out


def run(records=None, docs=None, targets=None):
    records = records if records is not None else json.loads(VALUES.read_text(encoding="utf-8"))
    docs = docs if docs is not None else corpus_docs()
    targets = targets if targets is not None else rc.load_conflicts(DEFAULT_CONFLICTS)
    b = build(records, docs, targets)
    conds = has_sibling_condition(b["keyed"])
    result = {}
    for lang in BRANCH:
        el = b["eligible"][lang]
        pairs = pick_pairs(el)
        used = {p["id"] for pr in pairs for p in (pr["a"], pr["b"])}
        singles = pick_singles(el, conds, b["pool"][lang], used)
        result[lang] = {"pool_docs": b["pool"][lang], "eligible": len(el), "A": pairs, "B": singles}
    return result


# --- 출력 --------------------------------------------------------------------
def public(p):
    return {k: v for k, v in p.items() if not k.startswith("_")}


def to_json(result):
    out = {}
    for lang, r in result.items():
        out[lang] = {
            "pool_docs": r["pool_docs"], "eligible": r["eligible"],
            "A": [{"rank": i, "quantity": x["quantity"], "condition": x["condition"], "larger": x["larger"],
                   "a": public(x["a"]), "b": public(x["b"])} for i, x in enumerate(r["A"], 1)],
            "B": [dict(public(p), rank=i) for i, p in enumerate(r["B"], 1)],
        }
    return out


def cut(p):
    """줄을 raw 둘레 약 200자로 자른다."""
    line, s, e = p["quote"], p["start"], p["end"]
    a, z = max(0, s - QUOTE_AROUND), min(len(line), e + QUOTE_AROUND)
    return ("…" if a else "") + line[a:z] + ("…" if z < len(line) else "")


def flag_text(p, show=5):
    parts = []
    for f in p["flags"]["opposite_number"]:
        at = f["at"]
        parts.append(f"반대 언어에 같은 숫자 {f['number']}: " + ", ".join(at[:show]) + (f" 외 {len(at) - show}곳" if len(at) > show else ""))
    if "uncertain" in p["flags"]:
        parts.append("불확실: " + p["flags"]["uncertain"])
    return "; ".join(parts)


def place_md(p, label):
    lines = [f"- {label + ' ' if label else ''}`{p['doc_id']}:{p['line']}` {cp.span(p['raw'])} = {p['value']} ({p['where']}) 대상 {p['object']}, 양 {p['quantity']}" + (f", 조건 {p['condition']}" if p["condition"] else "")]
    lines.append(f"  - 줄: {cp.span(cut(p))}")
    ft = flag_text(p)
    if ft:
        lines.append(f"  - 표시: {ft}")
    return lines


def counts_line(result):
    return "; ".join(f"{LANG_NAME[l]} 적격 자리 {r['eligible']}, 쌍 {len(r['A'])}, 단독 {len(r['B'])}(표 칸 {sum(p['where'] == '표' for p in r['B'])})"
                     for l, r in result.items())


def to_md(result, conflicts_path):
    out = ["# 질문 재료 후보 (materials.py)", "",
           f"부딪히는 값 목록: `{conflicts_path}`. 후보는 정해진 순서로 낸 것이고 원문 확인은 사람이 한다.", "",
           "- " + counts_line(result), ""]
    for lang, r in result.items():
        out += [f"## {LANG_NAME[lang]}", "", f"문서: {', '.join(r['pool_docs'])}", "", f"### A 여러 문서 연결 쌍 ({len(r['A'])})", ""]
        for i, x in enumerate(r["A"], 1):
            big = x["a"] if x["larger"] == "a" else x["b"]
            out += [f"{i}. 양 {x['quantity']}" + (f", 조건 {x['condition']}" if x["condition"] else "") + f" - 큰 쪽 {big['object']} ({big['value']})"]
            out += place_md(x["a"], "가") + place_md(x["b"], "나") + [""]
        out += [f"### B 표·수치·조건 단독 ({len(r['B'])})", ""]
        for i, p in enumerate(r["B"], 1):
            out += [f"{i}. " + ("표 칸" if p["where"] == "표" else "본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음")]
            out += place_md(p, "") + [""]
    return "\n".join(out) + "\n"


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_CONFLICTS
    result = run(targets=rc.load_conflicts(path))
    OUT_JSON.write_text(json.dumps({"conflicts": str(path), "limits": {"A": MAX_A, "B": MAX_B}, "languages": to_json(result)}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_MD.write_text(to_md(result, path), encoding="utf-8")
    print(f"부딪히는 값 목록: {path}")
    print(counts_line(result))
    print(f"쓴 파일: {OUT_JSON}, {OUT_MD}")


if __name__ == "__main__":
    main(sys.argv)
