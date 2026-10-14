"""같은 것이 다른 모양(반올림·버림·어림)으로 적힌 곳을 찾은 답(form/<doc_id>.answer.json)이 빠짐없고 인용이 맞는지 검사한다.

  uv run python -I research_notes/stage2_fact_count/within_doc/form/check_form.py

targets.json(문서마다 볼 사실 목록)의 사실 번호가 답에 꼭 한 번씩 있는가, 판정이 정한 세 값 가운데 하나인가,
"다른 모양 없음"이 아닌 답의 인용(quotes)이 그 문서의 마크다운에 글자 그대로 있는가(공백만 하나로 줄여 견준다)를 본다.
문서마다 문제를 한 줄씩 출력하고, 문제가 있으면 종료 코드 1로 끝낸다.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
MARKDOWN = HERE.parents[3] / "data" / "corpus" / "markdown"
VERDICTS = {"다른 모양 없음", "다른 모양 있음"}
norm = lambda s: re.sub(r"\s+", " ", s).strip()

targets = json.loads((HERE / "targets.json").read_text(encoding="utf-8"))
bad = 0
for doc, facts in sorted(targets.items()):
    path = HERE / f"{doc}.answer.json"
    if not path.exists():
        print(f"{doc}: 답 파일 없음")
        bad += 1
        continue
    text = norm((MARKDOWN / f"{doc}.md").read_text(encoding="utf-8"))
    answers = json.loads(path.read_text(encoding="utf-8"))
    want = [f["id"] for f in facts]
    got = [a.get("id") for a in answers]
    problems = [f"빠진 번호 {i}" for i in want if i not in got]
    problems += [f"목록에 없는 번호 {i}" for i in got if i not in want]
    problems += [f"두 번 나온 번호 {i}" for i in set(got) if got.count(i) > 1]
    for a in answers:
        if a.get("verdict") not in VERDICTS:
            problems.append(f"{a.get('id')}: 판정 '{a.get('verdict')}'이 정한 값이 아님")
        elif a["verdict"] != "다른 모양 없음":
            quotes = a.get("quotes") or []
            if not quotes:
                problems.append(f"{a['id']}: 인용이 없음")
            problems += [f"{a['id']}: 인용이 문서에 없음: {q[:50]}" for q in quotes if norm(q) not in text]
    counts = {v: sum(1 for a in answers if a.get("verdict") == v) for v in sorted(VERDICTS)}
    print(f"{doc}: 사실 {len(want)}, 답 {len(answers)}, {counts}" + ("" if not problems else f", 문제 {len(problems)}"))
    for p in problems:
        print(f"    {p}")
    bad += bool(problems)
sys.exit(1 if bad else 0)
