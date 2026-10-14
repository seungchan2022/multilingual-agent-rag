"""커밋 직전에 stage된 문서 파일이 collected.yaml의 해시와 같은지 검사하는 프로그램.

  uv run python src/corpus/check_staged.py

작업 폴더가 아니라 git index의 내용으로 검사한다. 원본과 마크다운의 해시가 기록과 다르면
손으로 고친 것으로 보고 문제를 한 줄씩 출력하며 종료 코드 1로 끝난다. 문제가 없으면 출력 없이 0이다.
.githooks/pre-commit이 data/corpus/의 파일이 stage되어 있을 때 부른다.
"""
import hashlib, subprocess, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def staged(path):
    """index에 있는 파일의 바이트. 없으면 None."""
    r = subprocess.run(["git", "show", f":data/corpus/{path}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    text = staged("collected.yaml")
    if text is None:
        print("collected.yaml: index에 없음")
        return 1
    problems = []
    for doc in yaml.safe_load(text).get("documents", []):
        for kind, prefix in (("원본", "raw"), ("마크다운", "markdown")):
            path, expected = doc.get(f"{prefix}_file"), doc.get(f"{prefix}_sha256")
            if not path or not expected:
                problems.append(f"{doc['doc_id']}: {kind}의 경로나 해시 칸이 없음")
                continue
            data = staged(path)
            if data is None:
                problems.append(f"{doc['doc_id']}: {kind}이 index에 없음 ({path})")
            elif hashlib.sha256(data).hexdigest() != expected:
                problems.append(f"{doc['doc_id']}: {kind}의 해시가 기록과 다름 ({path})")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
