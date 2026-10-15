"""웹 AI가 낸 평가 질문 후보를 형식과 원문 대조로 검사하는 프로그램(형식 검사의 첫 판).

  uv run python src/questions/check_candidates.py <후보 파일> --batch <ko-ko|en-en|ko-en|en-ko|no-answer> [--previous <앞 묶음 파일> ...] [--hide]

후보 파일은 AI가 낸 YAML 코드 블록을 옮겨 적은 파일이다. ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고,
없으면 파일 전체를 읽는다. --previous 파일도 같은 방식으로 읽으며, 앞 묶음과 겹치는지 보는 데만 쓰고 그 자체는 검사하지 않는다.
묶음 이름은 <질문 언어>-<근거 문서 언어>이고 no-answer는 답 없는 질문 묶음이다. 한 묶음은 후보 12개이고 id는 묶음마다 정해진 번호부터 차례로 붙는다.
후보마다 통과/실패를 한 줄씩 보이고, 이어서 묶음 구성, 주의(경고) 줄, 마지막 요약 줄을 출력한다. 하나라도 실패하면 종료 코드 1로 끝낸다.
passage는 data/corpus/markdown/의 글자와 그대로 견준다(유니코드 정규화, 공백 합치기, 대소문자 맞추기를 하지 않는다).
YAML 블록 글자(|)가 붙이는 맨 끝 줄바꿈 하나, 그리고 표 줄의 줄 끝 공백만 뗀다.
표 구절(비어 있지 않은 줄이 모두 |로 시작하는 구절)은 첫 줄이 원문 표의 머리글 행이고 나머지 줄이 같은 표의 줄이어야 한다.
구분선 행은 '|'와 '-'를 함께 쓴 줄(|---|---| 꼴)로 본다.
--hide를 주면 후보와 원문의 글자(질문, 답, 사실, 구절, 위치 등)를 출력에 넣지 않고 id, 칸 경로, doc_id, 개수, 규칙 이름만 보인다.
"""
import re, sys
from functools import cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"

DOC_LANG = {d["doc_id"]: d["language"] for d in yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]}
BANNED = {"kto-en-jeonju-hanok-village", "kto-en-cheonan-samgeori-park"}
LANGS = {"ko", "en"}
TYPES = {"single_fact", "table_numeric", "multi_doc", "paraphrase", "no_answer"}
ID_RE = re.compile(r"c-\d{3}")
# 묶음 이름: (질문 언어, 근거 문서 언어, 첫 id 번호)
BATCHES = {"ko-ko": ("ko", "ko", 1), "en-en": ("en", "en", 13), "ko-en": ("ko", "en", 25), "en-ko": ("en", "ko", 37), "no-answer": (None, None, 49)}
COUNT = 12
ANSWERED_TYPE_COUNTS = {"single_fact": 2, "table_numeric": 2, "multi_doc": 4, "paraphrase": 4}
USAGE = "사용법: uv run python src/questions/check_candidates.py <후보 파일> --batch <ko-ko|en-en|ko-en|en-ko|no-answer> [--previous <파일> ...] [--hide]"

HIDE = False
results = []


def report(name, problems):
    """problems가 비면 통과, 아니면 실패하고 이유를 들여 써서 보인다."""
    results.append(not problems)
    print(f"{'통과' if not problems else '실패'}  {name}")
    for p in problems[:10]:
        print(f"      {p}")
    if len(problems) > 10:
        print(f"      ... 외 {len(problems) - 10}건")


def val(x):
    """이유에 덧붙일 값. --hide에서는 값을 보이지 않는다."""
    if HIDE:
        return ""
    s = x if isinstance(x, str) else repr(x)
    return f" ({s[:40]}{'...' if len(s) > 40 else ''})"


def doc_label(doc):
    """doc_id를 이유에 보인다. --hide에서는 id처럼 생긴 짧은 값만 보인다."""
    if isinstance(doc, str) and (not HIDE or re.fullmatch(r"[A-Za-z0-9_-]{1,60}", doc)):
        return f" ({doc})"
    return ""


def around(s, n):
    """s의 n번째(0부터) 글자를 [ ]로 싸고 앞뒤 10글자를 붙인다."""
    flat = lambda t: t.replace("\n", "↵")
    return f"…{flat(s[max(0, n - 10):n])}[{flat(s[n:n + 1])}]{flat(s[n + 1:n + 11])}…"


def common_len(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


# ---------- 읽기 ----------

def read_block(path):
    """후보 파일에서 YAML 글자를 꺼낸다. ``` 줄이 있으면 첫 번째와 그다음 ``` 줄 사이만 쓴다. (글자, 앞에서 뗀 줄 수)를 돌려준다."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    fences = [i for i, l in enumerate(lines) if l.lstrip().startswith("```")]
    skipped = 0
    if fences:
        end = fences[1] if len(fences) > 1 else len(lines)
        lines = lines[fences[0] + 1:end]
        skipped = fences[0] + 1
    return "\n".join(lines), skipped


def load(path):
    """(데이터, 실패 이유 목록). 읽지 못하면 데이터는 None이다."""
    try:
        text, skipped = read_block(path)
    except (OSError, UnicodeDecodeError):
        return None, ["파일을 읽지 못함"]
    try:
        data = yaml.safe_load(text)
    except (yaml.YAMLError, ValueError) as err:
        mark = getattr(err, "problem_mark", None)
        where = f" ({mark.line + 1 + skipped}줄 {mark.column + 1}칸)" if mark else ""
        why = [] if HIDE else [str(getattr(err, "problem", None) or err).splitlines()[0]]
        return None, [f"YAML을 읽지 못함{where}"] + why
    if not isinstance(data, list):
        return None, ["맨 위가 목록이 아님 (후보 묶음의 목록이어야 함)"]
    return data, []


# ---------- 원문 ----------

@cache
def doc_text(doc_id):
    return (MARKDOWN / f"{doc_id}.md").read_text(encoding="utf-8")


@cache
def doc_tables(doc_id):
    """문서의 표들. 머리글 행(다음 줄이 구분선인 | 줄)에서 시작해 | 줄이 이어지는 동안의 줄 목록을 모은다."""
    ls = [l.rstrip() for l in doc_text(doc_id).split("\n")]
    tables = []
    for i in range(len(ls) - 1):
        if ls[i].startswith("|") and is_separator(ls[i + 1]):
            j = i
            while j < len(ls) and ls[j].startswith("|"):
                j += 1
            tables.append(ls[i:j])
    return tables


def is_separator(line):
    line = line.rstrip()
    return line.startswith("|") and "-" in line and re.fullmatch(r"[|\-: ]+", line) is not None


def normalize(passage):
    """YAML 블록 글자가 붙이는 맨 끝 줄바꿈 하나를 뗀다."""
    return passage[:-1] if passage.endswith("\n") else passage


def is_table_passage(passage):
    nonempty = [l for l in normalize(passage).split("\n") if l.strip()]
    return bool(nonempty) and all(l.startswith("|") for l in nonempty)


def longest_prefix_in(text, p):
    """p의 앞부분 가운데 text의 부분 문자열인 가장 긴 것의 길이."""
    lo, hi = 0, len(p)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if p[:mid] in text:
            lo = mid
        else:
            hi = mid - 1
    return lo


def diff_note(s, n, ref):
    """s가 n글자까지 ref와 같고 그다음이 다르다는 안내 글(--hide에서는 개수만)."""
    if HIDE:
        return f"{n}글자까지 {ref}과 같음"
    if n == 0:
        return f"시작부터 {ref}에 없음"
    if n >= len(s):
        return f"앞의 {n}글자는 {ref}에 있으나 {ref}의 줄이 더 길어 여기서 끝남"
    return f"앞에서 {n}글자까지는 {ref}에 있고, 그다음이 다름: {around(s, n)}"


def verbatim_problem(doc_id, passage):
    """passage가 원문에 글자 그대로 있는지 본다. 있으면 None, 없으면 이유 글."""
    p = normalize(passage)
    if is_table_passage(passage):
        return table_problem(doc_id, p.split("\n"))
    text = doc_text(doc_id)
    if p in text:
        return None
    n = longest_prefix_in(text, p)
    if HIDE:
        return f"원문에 글자 그대로 없음 ({n}글자까지 원문과 같음)"
    if n == 0:
        return "원문에 글자 그대로 없음. 구절의 시작이 원문에 없음"
    return f"원문에 글자 그대로 없음. {diff_note(p, n, '원문')}"


def table_problem(doc_id, L):
    L = [l.rstrip() for l in L]
    seps = [i + 1 for i, l in enumerate(L) if is_separator(l)]
    if seps:
        return f"원문에 글자 그대로 없음 (구분선 행을 넣음: {seps[0]}번째 줄)"
    tables = doc_tables(doc_id)
    if not tables:
        return "원문에 글자 그대로 없음 (이 문서에는 표가 없음)"
    same = [t for t in tables if t[0] == L[0]]
    if not same:
        best = max((t[0] for t in tables), key=lambda h: common_len(L[0], h))
        n = common_len(L[0], best)
        return f"원문에 글자 그대로 없음 (표의 첫 줄이 어떤 표의 머리글 행과도 같지 않음. {diff_note(L[0], n, '머리글 행')})"
    worst = None   # 모든 표 가운데 가장 멀리까지 맞은 것: (처음 틀린 줄 번호, 표)
    for t in same:
        rows = set(t)
        bad = next((j for j in range(1, len(L)) if L[j] not in rows), None)
        if bad is None:
            return None
        if worst is None or bad > worst[0]:
            worst = (bad, t)
    bad, t = worst
    n = max(common_len(L[bad], r) for r in t)
    return f"원문에 글자 그대로 없음 (표의 {bad + 1}번째 줄이 같은 머리글의 표에 없음. {diff_note(L[bad], n, '같은 표의 줄')})"


# ---------- 후보 하나 ----------

def nonempty_str(c, key, problems, path=None):
    path = path or key
    v = c.get(key)
    if not isinstance(v, str) or not v.strip():
        problems.append(f"{path}: 비었거나 없거나 글자가 아님")
        return False
    return True


def check_item(item, path, language, problems, info, is_evidence):
    """근거(evidence) 항목이나 반박(rebuttal) 항목 하나를 본다."""
    if not isinstance(item, dict):
        problems.append(f"{path}: 키와 값 묶음이 아님")
        return
    doc = item.get("doc_id")
    known = isinstance(doc, str) and doc in DOC_LANG
    if not known:
        problems.append(f"{path}.doc_id: 28개 문서에 없는 doc_id{doc_label(doc) or val(doc)}")
    elif doc in BANNED:
        problems.append(f"{path}.doc_id: 쓰면 안 되는 영어 소개 글 ({doc})")
    if known and language and DOC_LANG[doc] != language:
        problems.append(f"{path}.doc_id: 근거 문서 언어({DOC_LANG[doc]})가 evidence_language와 다름 ({doc})")
    nonempty_str(item, "location", problems, f"{path}.location")
    if nonempty_str(item, "passage", problems, f"{path}.passage") and known:
        passage = item["passage"]
        why = verbatim_problem(doc, passage)
        if why:
            problems.append(f"{path}.passage: {why}")
        info["pairs"].append((doc, normalize(passage)))
        if is_evidence and is_table_passage(passage):
            info["table"] = True


def check_candidate(c, batch):
    """후보 하나의 실패 이유 목록과, 묶음 검사에 쓸 정보를 돌려준다."""
    problems = []
    info = {"table": False, "pairs": []}
    if not isinstance(c, dict):
        return ["항목이 키와 값 묶음이 아님"], info
    if not (isinstance(c.get("id"), str) and ID_RE.fullmatch(c["id"])):
        problems.append("id: c-000 꼴이 아님")
    nonempty_str(c, "question", problems)
    ql, typ = c.get("question_language"), c.get("type")
    if ql not in LANGS:
        problems.append(f"question_language: ko나 en이 아님{val(ql)}")
    if typ not in TYPES:
        problems.append(f"type: 정해진 다섯 가지가 아님{val(typ)}")
    bql, bel, _ = BATCHES[batch]
    if typ == "no_answer":
        check_no_answer(c, problems, info)
    else:
        check_answered(c, problems, info)
    # 묶음과의 일치
    if batch == "no-answer":
        if typ != "no_answer":
            problems.append("type: 답 없는 질문 묶음인데 no_answer가 아님")
    else:
        if typ == "no_answer":
            problems.append(f"type: {batch} 묶음인데 no_answer임")
        if ql in LANGS and ql != bql:
            problems.append(f"question_language: {batch} 묶음인데 {bql}가 아님{val(ql)}")
        if c.get("evidence_language") in LANGS and c["evidence_language"] != bel:
            problems.append(f"evidence_language: {batch} 묶음인데 {bel}이 아님{val(c['evidence_language'])}")
    return problems, info


def check_answered(c, problems, info):
    el = c.get("evidence_language")
    if el not in LANGS:
        problems.append(f"evidence_language: ko나 en이 아님{val(el)}")
        el = None
    nonempty_str(c, "answer", problems)
    facts = c.get("required_facts")
    if not isinstance(facts, list) or not facts:
        problems.append("required_facts: 비었거나 없거나 목록이 아님")
        return
    with_evidence = 0
    for i, f in enumerate(facts):
        p = f"required_facts[{i}]"
        if not isinstance(f, dict):
            problems.append(f"{p}: 키와 값 묶음이 아님")
            continue
        nonempty_str(f, "fact", problems, f"{p}.fact")
        ev = f.get("evidence")
        if not isinstance(ev, list):
            problems.append(f"{p}.evidence: 없거나 목록이 아님")
            continue
        with_evidence += bool(ev)
        for j, item in enumerate(ev):
            check_item(item, f"{p}.evidence[{j}]", el, problems, info, True)
    if not with_evidence:
        problems.append("required_facts: 근거(evidence)가 있는 사실이 하나도 없음")


def check_no_answer(c, problems, info):
    if "evidence_language" not in c or c["evidence_language"] is not None:
        problems.append("evidence_language: null이어야 함")
    if "answer" not in c or c["answer"] is not None:
        problems.append("answer: null이어야 함")
    if c.get("required_facts") != []:
        problems.append("required_facts: 빈 목록([])이어야 함")
    nonempty_str(c, "expected_refusal", problems)
    nonempty_str(c, "no_answer_reason", problems)
    rb = c.get("rebuttal")
    if not isinstance(rb, list):
        problems.append("rebuttal: 없거나 목록이 아님 (없으면 [])")
        return
    for j, item in enumerate(rb):
        check_item(item, f"rebuttal[{j}]", None, problems, info, False)


# ---------- 묶음 ----------

def label(c, n):
    """보고에 쓸 이름. 쓸 수 있는 id가 없으면 'N번째 항목'."""
    if isinstance(c, dict) and isinstance(c.get("id"), str) and ID_RE.fullmatch(c["id"]):
        return c["id"]
    return f"{n}번째 항목"


def batch_problems(items, infos, batch):
    problems = []
    cands = [c for c in items if isinstance(c, dict)]
    if len(items) != COUNT:
        problems.append(f"후보가 {len(items)}개임 (기대 {COUNT}개)")
    first = BATCHES[batch][2]
    want = [f"c-{first + k:03d}" for k in range(COUNT)]
    got = [c["id"] for c in cands if isinstance(c.get("id"), str)]
    dup = sorted({i for i in got if got.count(i) > 1})
    if dup:
        problems.append("id가 겹침: " + ", ".join(i if ID_RE.fullmatch(i) else "(c-000 꼴이 아닌 id)" for i in dup))
    missing = [i for i in want if i not in got]
    if missing:
        problems.append("없는 id: " + ", ".join(missing))
    extra = [i for i in got if i not in want]
    if extra:
        shown = [i for i in extra if ID_RE.fullmatch(i)]
        problems.append(f"기대한 id({want[0]}~{want[-1]})가 아닌 id {len(extra)}개" + (": " + ", ".join(shown) if shown else ""))
    if not missing and not extra and not dup and got != want and len(got) == len(want):
        problems.append(f"id가 {want[0]}부터 차례로 놓이지 않음")
    types = [c.get("type") for c in cands]
    if batch == "no-answer":
        other = sum(t != "no_answer" for t in types)
        if other:
            problems.append(f"no_answer가 아닌 후보가 {other}개 있음")
        for lang in ("ko", "en"):
            n = sum(c.get("question_language") == lang for c in cands)
            if n != 6:
                problems.append(f"question_language {lang}가 {n}개임 (기대 6개)")
    else:
        for t, want_n in ANSWERED_TYPE_COUNTS.items():
            n = types.count(t)
            if n != want_n:
                problems.append(f"type {t}가 {n}개임 (기대 {want_n}개)")
        if not any(info["table"] for c, info in zip(items, infos) if isinstance(c, dict) and c.get("type") == "table_numeric"):
            problems.append("table_numeric 후보 가운데 표 구절(근거 구절이 | 줄로만 이뤄진 것)을 가진 것이 없음")
    return problems


# ---------- 실행 ----------

def parse_args(argv):
    """(후보 파일, 묶음 이름, 앞 묶음 파일들, --hide) 또는 None."""
    path, batch, prev, hide = None, None, [], False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--hide":
            hide = True
        elif a in ("--batch", "--previous"):
            if i + 1 >= len(argv):
                return None
            i += 1
            if a == "--batch":
                batch = argv[i]
            else:
                prev.append(argv[i])
        elif a.startswith("--") or path is not None:
            return None
        else:
            path = a
        i += 1
    if path is None or batch not in BATCHES:
        return None
    return path, batch, prev, hide


def main():
    global HIDE
    args = parse_args(sys.argv[1:])
    if args is None:
        print(USAGE)
        return 1
    path, batch, prev_paths, HIDE = args

    # 앞 묶음
    prev_ids, prev_q, users = set(), {}, {}
    for pp in prev_paths:
        data, why = load(pp)
        if why:
            report(f"앞 묶음 {Path(pp).name}", why)
            continue
        for n, c in enumerate(data, 1):
            if not isinstance(c, dict):
                continue
            lab = label(c, n)
            if isinstance(c.get("id"), str):
                prev_ids.add(c["id"])
            if isinstance(c.get("question"), str):
                prev_q.setdefault(c["question"], lab)
            for pair in collect_pairs(c):
                users.setdefault(pair, []).append(lab)

    data, why = load(path)
    if why:
        print("실패  " + why[0])
        for w in why[1:]:
            print(f"      {w}")
        return 1

    infos, warnings, seen_q = [], [], {}
    passed = 0
    for n, c in enumerate(data, 1):
        problems, info = check_candidate(c, batch)
        infos.append(info)
        lab = label(c, n)
        if isinstance(c, dict):
            if isinstance(c.get("id"), str) and c["id"] in prev_ids:
                problems.append("id: 앞 묶음에서 이미 쓴 id")
            q = c.get("question")
            if isinstance(q, str):
                other = prev_q.get(q) or seen_q.get(q)
                if other:
                    problems.append(f"question: {other}의 질문과 글자 그대로 같음")
                else:
                    seen_q[q] = lab
            others = []
            for pair in dict.fromkeys(info["pairs"]):
                others += [u for u in users.get(pair, []) if u != lab and u not in others]
            if others:
                warnings.append(f"주의  {lab}: {', '.join(others)}와 같은 문서·구절을 씀. 같은 사실을 물었을 수 있음")
            for pair in dict.fromkeys(info["pairs"]):
                users.setdefault(pair, []).append(lab)
        report(lab, problems)
        passed += not problems

    bp = batch_problems(data, infos, batch)
    report("묶음 구성", bp)
    for w in warnings:
        print(w)
    print(f"후보 {len(data)}개 가운데 {passed}개 통과, 묶음 구성 {'통과' if not bp else '실패'}")
    return 0 if all(results) else 1


def collect_pairs(c):
    """앞 묶음 후보에서 (doc_id, 구절) 쌍을 모은다. 모양이 틀려도 터지지 않게 읽는다."""
    out = []
    groups = [c.get("rebuttal")] + [f.get("evidence") for f in (c.get("required_facts") if isinstance(c.get("required_facts"), list) else []) if isinstance(f, dict)]
    for g in groups:
        for item in g if isinstance(g, list) else []:
            if isinstance(item, dict) and isinstance(item.get("doc_id"), str) and isinstance(item.get("passage"), str):
                out.append((item["doc_id"], normalize(item["passage"])))
    return out


if __name__ == "__main__":
    sys.exit(main())
