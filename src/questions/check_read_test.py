"""웹 AI의 읽기 시험 답을 원문과 대조하는 프로그램.

  uv run python src/questions/check_read_test.py <답 파일>

답 파일은 AI가 낸 YAML 코드 블록을 옮겨 적은 파일이다. ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고,
없으면 파일 전체를 읽는다. data/corpus/markdown/의 글자에서 기대값을 직접 계산해 문서마다 통과/실패를 한 줄씩 출력하고,
하나라도 실패하면 종료 코드 1로 끝낸다.
맨 마지막 줄은 언제나 전체 판정이다(일찍 끝나는 경우도 같다. 사용법 오류만 뺀다): 종료 코드가 0이면 `전체 검사: 통과`,
아니면 `전체 검사: 실패 (위의 실패 줄을 본다)`. 그 앞의 `문서 28개 가운데 N개 통과` 줄은 개수를 보는 정보 줄이다.
글자는 그대로 견준다(유니코드 정규화, 공백 합치기, 대소문자 맞추기를 하지 않는다). 줄 끝 공백만 떼고 견준다.
"앞부분" 값은 실제 줄이 그 값으로 시작해야 하고, 길이가 min(20, 실제 줄 길이) 이상이어야 한다(요청은 30글자지만 글자 수를 세는 오차를 받아 20글자까지 받는다).
다만 그 값이 기대한 줄의 중간부터 옮긴 것이고(기대한 줄 안에 글자 그대로 한 번 있고), 그 문서의 다른 값이 모두 통과했으면
"통과(줄 중간부터 옮김)"으로 센다. 줄의 시작을 다르게 본 것이라 읽기 실패로 보지 않는다(decisions/stage3.md 2026-10-15).
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
    """problems가 비면 통과, 줄 중간부터 옮긴 값 하나뿐이면 통과(줄 중간부터 옮김), 아니면 실패하고 이유를 들여 써서 보인다."""
    mid = len(problems) == 1 and isinstance(problems[0], MidLine)
    results.append(not problems or mid)
    print(f"{'통과' if not problems else '통과(줄 중간부터 옮김)' if mid else '실패'}  {name}")
    for p in problems[:10]:
        print(f"      {p}")
    if len(problems) > 10:
        print(f"      ... 외 {len(problems) - 10}건")


def finish():
    """맨 마지막 줄에 전체 판정을 보이고 종료 코드를 돌려준다. 판정과 종료 코드는 results 하나에서 나온다."""
    ok = all(results)
    print("전체 검사: 통과" if ok else "전체 검사: 실패 (위의 실패 줄을 본다)")
    return 0 if ok else 1


def show(s):
    """이유에 넣을 글자를 60자까지만 보인다."""
    s = repr(s) if not isinstance(s, str) else s
    return "'" + (s if len(s) <= 60 else s[:60] + "...") + "'"


def diff_at(expected, given):
    """처음 다른 글자의 자리(1부터)와 앞뒤 10글자를 보여 주는 글. 한쪽이 먼저 끝나면 그쪽 칸은 비어 있다."""
    n = 0
    for a, b in zip(expected, given):
        if a != b:
            break
        n += 1
    flat = lambda t: t.replace("\n", "↵")
    before = flat(expected[max(0, n - 10):n])
    side = lambda t: f"…{before}[{flat(t[n:n + 1])}]{flat(t[n + 1:n + 11])}…"
    return f"{n + 1}번째 글자부터 다름: 기대 {side(expected)}, 답 {side(given)}"


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


class MidLine(str):
    """기대한 줄의 중간부터 옮긴 값(그 문서의 다른 값이 모두 통과했을 때만 통과로 센다)."""


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
        if len(given) >= min(MIN_LEN, len(actual)) and actual.count(given) == 1:
            return MidLine(f"{label}: 기대한 줄 안에 글자 그대로 한 번 있음")
        return f"{label}: 줄의 앞부분이 아님. 기대 {show(actual)}, 답 {show(given)}. {diff_at(actual, given)}"
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
                bad.append(f"{i}번째 heading이 다름. 기대 {show(h)}, 답 {show(g)}" + (f". {diff_at(h, g.rstrip())}" if isinstance(g, str) else ""))
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
    mid = [b for b in bad if isinstance(b, MidLine)]
    if len(mid) == 1 and len(bad) == 1:
        return mid
    return [b if not isinstance(b, MidLine) else f"{b} (그러나 이 문서의 다른 값도 틀려 통과로 보지 않음)" for b in bad]


def main():
    if len(sys.argv) != 2:
        print("사용법: uv run python src/questions/check_read_test.py <답 파일>")
        return 1
    if not Path(sys.argv[1]).is_file():
        print(f"실패  답 파일이 없음: {sys.argv[1]}")
        results.append(False)
        return finish()
    try:
        data = yaml.safe_load(read_answer(sys.argv[1]))
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None)
        where = f" ({mark.line + 1}줄 {mark.column + 1}칸)" if mark else ""
        print(f"실패  YAML을 읽지 못함{where}")
        print(f"      {str(getattr(err, 'problem', None) or err).splitlines()[0]}")
        results.append(False)
        return finish()
    if not isinstance(data, list):
        print("실패  맨 위가 목록이 아님 (doc_id 묶음의 목록이어야 함)")
        results.append(False)
        return finish()
    by, top = {}, []
    for n, item in enumerate(data, 1):
        if not isinstance(item, dict) or not isinstance(item.get("doc_id"), str):
            top.append(f"{n}번째 항목이 doc_id가 있는 키와 값 묶음이 아님")
        else:
            by.setdefault(item["doc_id"], []).append(item)
    if top:
        report("답의 항목 모양", top)
    passed, mids = 0, 0
    for doc_id in DOC_IDS:
        problems = check_doc(doc_id, by.get(doc_id, []))
        report(doc_id, problems)
        mids += bool(problems) and results[-1]
        passed += results[-1]
    for doc_id in by:
        if doc_id not in DOC_IDS:
            report(doc_id, ["문서 28개에 없는 doc_id"])
    print(f"문서 {len(DOC_IDS)}개 가운데 {passed}개 통과" + (f" (그 가운데 {mids}개는 줄 중간부터 옮김)" if mids else ""))
    return finish()


sys.exit(main())
