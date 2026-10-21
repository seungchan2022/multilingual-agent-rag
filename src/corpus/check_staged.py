"""커밋 직전에 stage된 문서 파일을 collected.yaml과 견주는 두 가지 검사를 하는 프로그램.

  uv run python src/corpus/check_staged.py

작업 폴더가 아니라 git index의 내용으로 검사한다.
 1. 원본과 마크다운 파일의 해시가 기록과 다르면 손으로 고친 것으로 본다.
 2. index의 build.py와 data/corpus/를 임시 폴더에 꺼내 build.py --verify를 돌려,
    원본으로 다시 만든 마크다운이 기록과 다르면 원본이나 변환 코드만 바뀐 것으로 본다.
    documents.yaml에 converter_commit이 있으면 index의 build.py 대신 그 커밋의 build.py로 돌린다.
문제를 한 줄씩 출력하며 종료 코드 1로 끝난다. 문제가 없으면 출력 없이 0이다.
.githooks/pre-commit이 data/corpus/, build.py, uv.lock, .python-version이 stage되어 있을 때 부른다.
"""
import hashlib, subprocess, sys, tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def staged(path):
    """index에 있는 파일의 바이트. 없으면 None."""
    r = subprocess.run(["git", "show", f":data/corpus/{path}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def rebuilt_problems(count):
    """index의 내용으로 마크다운을 다시 만들어 기록과 견준 결과의 문제 목록."""
    with tempfile.TemporaryDirectory() as tmp:
        prefix = f"--prefix={tmp}/"
        listing = subprocess.run(["git", "ls-files", "-z", "data/corpus"], cwd=ROOT, capture_output=True)
        for cmd, data in ((["git", "checkout-index", prefix, "--", "src/corpus/build.py"], None),
                          (["git", "checkout-index", "-z", "--stdin", prefix], listing.stdout)):
            r = subprocess.run(cmd, cwd=ROOT, input=data, capture_output=True)
            if r.returncode != 0:
                return [f"index에서 다시 만들 파일을 꺼내지 못함: {r.stderr.decode().strip()}"]
        text = staged("documents.yaml")
        commit = (yaml.safe_load(text) or {}).get("converter_commit") if text else None
        if commit:  # 코퍼스가 묶인 변환: index의 build.py 대신 그 커밋의 build.py를 쓴다
            r = subprocess.run(["git", "show", f"{commit}:src/corpus/build.py"], cwd=ROOT, capture_output=True)
            if r.returncode != 0:
                return [f"converter_commit {commit}의 build.py를 꺼내지 못함: {r.stderr.decode().strip()}"]
            Path(f"{tmp}/src/corpus/build.py").write_bytes(r.stdout)
        r = subprocess.run([sys.executable, f"{tmp}/src/corpus/build.py", "--verify"], capture_output=True, text=True)
    if r.returncode == 0:
        lines = r.stdout.strip().splitlines()
        same = lines[-1].split("같음")[-1].split(",")[0].strip() if lines else ""
        return [] if same == str(count) else [f"다시 만든 문서 수(같음 {same})가 기록의 문서 수({count})와 다름"]
    problems = []
    for line in r.stdout.splitlines():
        if line.endswith("다름"):
            problems.append(f"{line}: 원본으로 다시 만든 마크다운이 기록과 다름")
        elif line.endswith("없음"):
            problems.append(f"{line}: 원본이나 기록이 없음")
    return problems or [f"build.py --verify 실패: {r.stderr[-300:]}"]


def main():
    text = staged("collected.yaml")
    if text is None:
        print("collected.yaml: index에 없음")
        return 1
    problems = []
    docs = yaml.safe_load(text).get("documents", [])
    for doc in docs:
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
    problems += rebuilt_problems(len(docs))
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
