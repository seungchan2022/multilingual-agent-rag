"""앞 묶음들의 후보 YAML에서 질문 문장만 뽑아, 새 채팅의 첫 요청에 붙일 파일을 만드는 프로그램.

  uv run python src/questions/list_questions.py <출력 파일> <후보 파일> [<후보 파일> ...]

후보 파일은 check_candidates.py와 같은 규칙으로 읽는다: ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고, 없으면 파일 전체를 읽는다.
준 순서대로 후보마다 question 한 줄을 쓴다. 화면에는 개수와 출력 파일 이름만 보인다(질문 내용을 화면에 내지 않는다).
"""
import sys
from pathlib import Path

import yaml

USAGE = "사용법: uv run python src/questions/list_questions.py <출력 파일> <후보 파일> [<후보 파일> ...]"


def read_block(path):
    """후보 파일에서 YAML 글자를 꺼낸다(check_candidates.py와 같은 규칙)."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    fences = [i for i, l in enumerate(lines) if l.lstrip().startswith("```")]
    if fences:
        end = fences[1] if len(fences) > 1 else len(lines)
        lines = lines[fences[0] + 1:end]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        print(USAGE, file=sys.stderr)
        return 1
    dest, questions = Path(sys.argv[1]), []
    for src in sys.argv[2:]:
        try:
            data = yaml.safe_load(read_block(src))
        except OSError as err:
            print(f"후보 파일을 읽지 못함: {err}", file=sys.stderr)
            return 1
        except yaml.YAMLError as err:
            mark = getattr(err, "problem_mark", None)   # 오류 글에는 YAML 줄의 글자가 들어가므로 줄 번호만 보인다
            print(f"후보 파일의 YAML을 읽지 못함: {src}" + (f" (블록의 {mark.line + 1}번째 줄)" if mark else ""), file=sys.stderr)
            return 1
        if not isinstance(data, list):
            print(f"후보 파일의 맨 위가 목록이 아님: {src}", file=sys.stderr)
            return 1
        questions += [str(c["question"]).strip() for c in data if isinstance(c, dict) and c.get("question")]
    dest.write_text("\n".join(questions) + "\n", encoding="utf-8")
    print(f"질문 {len(questions)}개를 씀: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
