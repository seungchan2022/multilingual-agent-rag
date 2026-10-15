"""웹 AI의 읽기 시험 답을 원문과 대조하는 프로그램.

  uv run python src/questions/check_read_test.py <답 파일>

답 파일은 AI가 낸 YAML 코드 블록을 옮겨 적은 파일이다. ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고,
없으면 파일 전체를 읽는다. data/corpus/markdown/의 글자에서 기대값을 직접 계산해 문서마다 통과/실패를 한 줄씩 출력하고,
하나라도 실패하면 종료 코드 1로 끝낸다.
글자는 그대로 견준다(유니코드 정규화, 공백 합치기, 대소문자 맞추기를 하지 않는다). 줄 끝 공백만 떼고 견준다.
"앞부분" 값은 실제 줄이 그 값으로 시작해야 하고, 길이가 min(20, 실제 줄 길이) 이상이어야 한다(요청은 30글자지만 글자 수를 세는 오차를 받아 20글자까지 받는다).
"""
import re, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"
MIN_LEN = 20   # 앞부분으로 받는 최소 글자 수(줄이 이보다 짧으면 줄 전체)

DOC_IDS = [d["doc_id"] for d in yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]]

results = []


def report(name, problems):
    """problems가 비면 통과, 아니면 실패하고 이유를 들여 써서 보인다."""
    results.append(not problems)
    print(f"{'통과' if not problems else '실패'}  {name}")
    for p in problems[:10]:
        print(f"      {p}")
    if len(problems) > 10:
        print(f"      ... 외 {len(problems) - 10}건")


def show(s):
    """이유에 넣을 글자를 60자까지만 보인다."""
    s = repr(s) if not isinstance(s, str) else s
    return "'" + (s if len(s) <= 60 else s[:60] + "...") + "'"


def read_answer(path):
    """답 파일에서 YAML 글자를 꺼낸다. ``` 줄이 있으면 첫 번째와 그다음 ``` 줄 사이만 쓴다."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    fences = [i for i, l in enumerate(lines) if l.lstrip().startswith("```")]
    if fences:
        end = fences[1] if len(fences) > 1 else len(lines)
        lines = lines[fences[0] + 1:end]
    return "\n".join(lines)


def expected(doc_id):
    """문서의 기대값. 큰 제목이 있으면 [(제목, 아래 첫 줄 또는 None), ...], 없으면 (첫 줄, 마지막 줄)."""
    ls = [l.rstrip() for l in (MARKDOWN / f"{doc_id}.md").read_text(encoding="utf-8").split("\n")]
    heads = [i for i, l in enumerate(ls) if re.match(r"## ", l)]
    if heads:
        return [(ls[i], next((l for l in ls[i + 1:] if l.strip()), None)) for i in heads]
    body = [l for l in ls[1:] if l.strip()]
    return (body[0] if body else None, [l for l in ls if l.strip()][-1])


def begins(label, actual, given):
    """앞부분 규칙을 어기면 이유 글, 지키면 None."""
    if actual is None:
        if given is None or given == "":
            return None
        return f"{label}: 아래에 줄이 없는데 {show(given)}를 적음"
    if not isinstance(given, str) or given.rstrip() == "":
        return f"{label}: 값이 비었거나 글자가 아님 (기대 {show(actual)})"
    given = given.rstrip()
    if not actual.startswith(given):
        return f"{label}: 줄의 앞부분이 아님. 기대 {show(actual)}, 답 {show(given)}"
    if len(given) < min(MIN_LEN, len(actual)):
        return f"{label}: {len(given)}글자로 너무 짧음 (최소 {min(MIN_LEN, len(actual))}글자). 기대 {show(actual)}, 답 {show(given)}"
    return None


def check_doc(doc_id, entries):
    if not entries:
        return ["답에 이 문서가 없음"]
    if len(entries) > 1:
        return [f"답에 {len(entries)}번 나옴"]
    e = entries[0]
    if "status" in e:
        s = e["status"]
        return ["읽지 못함이라고 답함"] if s == "읽지 못함" else [f"status를 답함: {show(s)}"]
    exp = expected(doc_id)
    bad = []
    if isinstance(exp, list):
        if "first_line" in e or "last_line" in e:
            bad.append("큰 제목이 있는 문서인데 first_line/last_line으로 답함")
        secs = e.get("sections")
        if not isinstance(secs, list):
            return bad + ["sections가 없거나 목록이 아님"]
        if len(secs) != len(exp):
            bad.append(f"큰 제목 수가 다름. 기대 {len(exp)}개, 답 {len(secs)}개")
        for i, ((h, nxt), s) in enumerate(zip(exp, secs), 1):
            if not isinstance(s, dict):
                bad.append(f"{i}번째: 항목이 키와 값 묶음이 아님")
                continue
            g = s.get("heading")
            if not isinstance(g, str) or g.rstrip() != h:
                bad.append(f"{i}번째 heading이 다름. 기대 {show(h)}, 답 {show(g)}")
            r = begins(f"{i}번째 next_line", nxt, s.get("next_line"))
            if r:
                bad.append(r)
    else:
        if "sections" in e:
            bad.append("큰 제목이 없는 문서인데 sections로 답함")
        for key, actual in zip(("first_line", "last_line"), exp):
            if key not in e:
                bad.append(f"{key}가 없음")
                continue
            r = begins(key, actual, e[key])
            if r:
                bad.append(r)
    return bad


def main():
    if len(sys.argv) != 2:
        print("사용법: uv run python src/questions/check_read_test.py <답 파일>")
        return 1
    try:
        data = yaml.safe_load(read_answer(sys.argv[1]))
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None)
        where = f" ({mark.line + 1}줄 {mark.column + 1}칸)" if mark else ""
        print(f"실패  YAML을 읽지 못함{where}")
        print(f"      {str(getattr(err, 'problem', None) or err).splitlines()[0]}")
        return 1
    if not isinstance(data, list):
        print("실패  맨 위가 목록이 아님 (doc_id 묶음의 목록이어야 함)")
        return 1
    by, top = {}, []
    for n, item in enumerate(data, 1):
        if not isinstance(item, dict) or not isinstance(item.get("doc_id"), str):
            top.append(f"{n}번째 항목이 doc_id가 있는 키와 값 묶음이 아님")
        else:
            by.setdefault(item["doc_id"], []).append(item)
    if top:
        report("답의 항목 모양", top)
    passed = 0
    for doc_id in DOC_IDS:
        problems = check_doc(doc_id, by.get(doc_id, []))
        report(doc_id, problems)
        passed += not problems
    for doc_id in by:
        if doc_id not in DOC_IDS:
            report(doc_id, ["문서 28개에 없는 doc_id"])
    print(f"문서 {len(DOC_IDS)}개 가운데 {passed}개 통과")
    return 0 if all(results) else 1


sys.exit(main())
