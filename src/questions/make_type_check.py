"""후보 묶음 YAML에서 두 번째 확인용 AI(ChatGPT)에게 붙여 넣을 후보 글을 만드는 프로그램.

  uv run python src/questions/make_type_check.py <후보 파일> <출력 파일>

먼저 data/questions/type_check_instructions.md를 붙여 넣고, 그다음 이 프로그램의 출력 파일을 붙여 넣는다.
type이 single_fact 또는 paraphrase인 후보만 파일 순서대로 쓴다.
후보마다 질문 언어, 근거 구절 언어, 질문, 정답, 근거 구절(줄마다 "> "를 붙여 그대로)만 적는다.
확인용 AI가 첫 번째 AI의 판단에 끌리지 않도록 type, fact, opposite_check, same_language_check, doc_id, location, city, 메모는 쓰지 않는다.
후보 파일은 check_candidates.py와 같은 규칙으로 읽는다: ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고, 없으면 파일 전체를 읽는다.
화면에는 개수와 출력 파일 이름만 보인다(질문 내용을 화면에 내지 않는다).
"""
import sys
from pathlib import Path

import yaml

USAGE = "사용법: uv run python src/questions/make_type_check.py <후보 파일> <출력 파일>"
TYPES = ("single_fact", "paraphrase")


def read_block(path):
    """후보 파일에서 YAML 글자를 꺼낸다(check_candidates.py와 같은 규칙)."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    fences = [i for i, l in enumerate(lines) if l.lstrip().startswith("```")]
    if fences:
        end = fences[1] if len(fences) > 1 else len(lines)
        lines = lines[fences[0] + 1:end]
    return "\n".join(lines)


def passages_of(c):
    return [e["passage"] for f in c.get("required_facts") or [] for e in f.get("evidence") or []]


def block(c):
    out = [f"## {c['id']}", f"- 질문 언어: {c['question_language']}", f"- 근거 구절 언어: {c['evidence_language']}",
           f"- 질문: {c['question']}", f"- 정답: {c['answer']}"]
    for n, p in enumerate(passages_of(c), 1):
        out.append(f"- 근거 구절 {n}:")
        out += ["> " + l for l in str(p).removesuffix("\n").split("\n")]
    return "\n".join(out)


def main():
    if len(sys.argv) != 3:
        print(USAGE, file=sys.stderr)
        return 1
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    try:
        data = yaml.safe_load(read_block(src))
    except (OSError, UnicodeDecodeError) as err:
        print(f"후보 파일을 읽지 못함: {err}", file=sys.stderr)
        return 1
    except yaml.YAMLError as err:
        mark = getattr(err, "problem_mark", None)   # 오류 글에는 YAML 줄의 글자가 들어가므로 줄 번호만 보인다
        print("후보 파일의 YAML을 읽지 못함" + (f" (블록의 {mark.line + 1}번째 줄)" if mark else ""), file=sys.stderr)
        return 1
    if not isinstance(data, list):
        print("후보 파일의 맨 위가 목록이 아님", file=sys.stderr)
        return 1
    picked = [c for c in data if isinstance(c, dict) and c.get("type") in TYPES]
    text = f"후보 {len(picked)}개다. 아래 후보마다 지시문 4번의 형식으로 답하라.\n\n" + "\n\n".join(block(c) for c in picked)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
    print(f"후보 {len(picked)}개를 씀: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
