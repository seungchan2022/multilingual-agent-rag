"""build.py가 만든 마크다운을 검사하는 프로그램. 문서 목록은 documents.yaml에서 읽는다.

  uv run python src/corpus/check_build.py

data/corpus/markdown/의 글자를 읽어 항목마다 통과/실패를 한 줄씩 출력하고, 실패가 있으면 종료 코드 1로 끝낸다.
변환 코드(build.py)를 불러 쓰지 않는다. 글자를 찾고 줄을 찾는 단순한 검사만 한다.
마지막 항목만 build.py를 하위 프로세스로 두 번 실행해 결과 파일의 해시를 견준다.
"""
import hashlib, re, subprocess, sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"

DOCS = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
TEXT = {}   # doc_id -> 마크다운 글자 (없으면 빠짐)
for d in DOCS:
    p = MARKDOWN / f"{d['doc_id']}.md"
    if p.is_file():
        TEXT[d["doc_id"]] = p.read_text(encoding="utf-8")
LINES = {k: v.split("\n") for k, v in TEXT.items()}

results = []


def report(name, problems):
    """problems가 비면 통과, 아니면 실패하고 이유를 들여 써서 보인다."""
    results.append(not problems)
    print(f"{'통과' if not problems else '실패'}  {name}")
    for p in problems[:10]:
        print(f"      {p}")
    if len(problems) > 10:
        print(f"      ... 외 {len(problems) - 10}건")


# 1
bad = []
for d in DOCS:
    t = TEXT.get(d["doc_id"])
    if t is None:
        bad.append(f"{d['doc_id']}: 파일이 없음")
    elif t.split("\n")[0] != f"# {d['title']}":
        bad.append(f"{d['doc_id']}: 첫 줄이 '# {d['title']}'가 아님")
report(f"1. 파일 {len(DOCS)}개가 모두 있고 첫 줄이 '# 제목'", bad)

# 2
BANNED = ["[편집", "[edit", "원본 편집", "출처 필요", "citation needed", "<img", "<br", "<td", "<table",
          "http://", "https://"]
# 주소 글자를 허용하는 곳은 정보 상자의 '- 웹사이트:' / '- Website:' 줄뿐이다. 그 밖의 주소는 실패다.
SITE_LINE = re.compile(r"^(  )?- (웹사이트|Website): https?://\S+$")
bad = [f"{k}:{n} '{w}'" for k, ls in LINES.items() for n, l in enumerate(ls, 1)
       if not SITE_LINE.match(l) for w in BANNED if w in l]
report("2. 편집 표시, 태그 찌꺼기, 주소가 없다 (정보 상자 웹사이트 줄은 제외)", bad)

# 3
HEADS = ["같이 보기", "외부 링크", "각주", "내용주", "참고 문헌", "See also", "External links", "References", "Notes"]
DROPPED = re.compile(r"#{2,6} (" + "|".join(HEADS) + ")")
bad = [f"{k}:{n} '{l}'" for k, ls in LINES.items() for n, l in enumerate(ls, 1) if DROPPED.fullmatch(l)]
report("3. 지우기로 한 절 제목이 없다", bad)


# 4
def cells(line):
    return len(re.split(r"(?<!\\)\|", line)) - 2


bad = []
for k, ls in LINES.items():
    head = None
    for n, l in enumerate(ls, 1):
        if l.startswith("|"):
            if head is None:
                head = cells(l)
            elif cells(l) != head:
                bad.append(f"{k}:{n} 열 {cells(l)}개, 머리글은 {head}개")
        else:
            head = None
report("4. 표의 모든 줄이 머리글 줄과 열 수가 같다", bad)

# 5
bad = [f"{k}:{n} '{l[:30]}'" for k, v in LINES.items() for n, l in enumerate(v, 1) if l.lstrip().startswith("- •")]
report("5. 어느 파일에도 '•'로 시작하는 목록 줄이 없다", bad)

# 6
bad = []
rows = (yaml.safe_load((CORPUS / "collected.yaml").read_text(encoding="utf-8")) or {}).get("documents") or []
by = {r["doc_id"]: r for r in rows}
for d in DOCS:
    r = by.get(d["doc_id"])
    p = MARKDOWN / f"{d['doc_id']}.md"
    if not r or not r.get("markdown_file") or not r.get("markdown_sha256"):
        bad.append(f"{d['doc_id']}: markdown_file/markdown_sha256이 없음")
    elif not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != r["markdown_sha256"]:
        bad.append(f"{d['doc_id']}: 해시가 파일과 다름")
report(f"6. collected.yaml의 {len(DOCS)}줄에 마크다운 파일과 해시가 있고 맞다", bad)

# 7
bad = []
for d in DOCS:
    r = by.get(d["doc_id"])
    if not r or not r.get("raw_file") or not r.get("raw_sha256"):
        bad.append(f"{d['doc_id']}: raw_file/raw_sha256이 없음")
    else:
        p = CORPUS / r["raw_file"]
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != r["raw_sha256"]:
            bad.append(f"{d['doc_id']}: 원본의 해시가 기록과 다름")
report(f"7. collected.yaml의 {len(DOCS)}줄에 원본 파일과 해시가 있고 맞다", bad)

# 8
RUNS = ["수소 헬륨 리튬", "Hydrogen Helium Lithium"]
bad = [f"{k}:{n} '{w}'" for k, ls in LINES.items() for n, l in enumerate(ls, 1) for w in RUNS if w in l]
report("8. 주기율표의 원소 이름이 이어진 줄이 없다", bad)

# 9
NAV_WORDS = ["view, talk, edit", "보기 • 토론"]
bad = []
for k, ls in LINES.items():
    for n, l in enumerate(ls, 1):
        if l.strip() == "- | 출처":
            bad.append(f"{k}:{n} '{l.strip()}'")
        for w in NAV_WORDS:
            if w in l:
                bad.append(f"{k}:{n} '{w}'")
        if l.endswith(" v, e"):
            bad.append(f"{k}:{n} 줄이 ' v, e'로 끝남: '{l.strip()}'")
report("9. 정보 상자 맨 아래 안내 줄 찌꺼기가 없다 ('- | 출처', 'view, talk, edit', '보기 • 토론', ' v, e'로 끝나는 묶음 줄)", bad)

# 10
# 원소 문서는 정보 상자에 물리적 성질 묶음이 있는 문서다(문서 번호가 아니라 마크다운에서 찾는다).
GROUP = {"- 물리적 성질", "- Physical properties"}
ATOMIC = ("- 원자 번호 (Z):", "- Atomic number (Z):")
ELEMENTS = [k for k, ls in LINES.items() if any(l.strip() in GROUP for l in ls)]
bad = [f"{k}: 원자 번호 줄은 있는데 '물리적 성질' 묶음이 없어 원소 문서로 잡히지 않음"
       for k, ls in LINES.items() if k not in ELEMENTS and any(l.strip().startswith(ATOMIC) for l in ls)]
if not ELEMENTS:
    bad.append("원소 문서를 하나도 찾지 못함")


def table_after(ls, i):
    """i번째 줄 다음이 빈 줄이고 그다음이 표 줄이면 참."""
    return i + 2 < len(ls) and ls[i + 1] == "" and ls[i + 2].startswith("|")


for k in ELEMENTS:
    ls = LINES[k]
    for what, names in [("증기 압력", ("- 증기 압력", "- Vapor pressure")),
                        ("동위원소", ("- 주요 동위원소", "- Isotopes of "))]:
        idx = [i for i, l in enumerate(ls) if l.strip().startswith(names)]
        if not idx:
            bad.append(f"{k}: {what} 이름 줄이 없음")
        for i in idx:
            if not table_after(ls, i):
                bad.append(f"{k}:{i + 1} '{ls[i].strip()}' 다음에 빈 줄과 표가 오지 않음")
report(f"10. 원소 문서 {len(ELEMENTS)}개: 증기 압력과 동위원소 이름 줄 다음에 빈 줄과 표가 온다", bad)

# 11
# 정보 상자가 없는 문서(원소 문서가 아닌 문서)에도 제목 아래에 본문 문단이 있다.
bad = []
for k, ls in LINES.items():
    if k in ELEMENTS:
        continue
    if not any(l.strip() and not l.startswith(("#", "-", "|", " ")) for l in ls[1:]):
        bad.append(f"{k}: 제목 아래에 본문 문단이 없음")
report(f"11. 원소 문서가 아닌 문서 {len(LINES) - len(ELEMENTS)}개: 제목 아래에 본문 문단이 있다", bad)

# 12
bad = []
runs = []
for _ in range(2):
    r = subprocess.run([sys.executable, str(ROOT / "src" / "corpus" / "build.py"), "--verify"],
                       capture_output=True, text=True)
    runs.append(r.stdout)
    if r.returncode != 0:
        bad += [f"{l}" for l in r.stdout.splitlines() if l.endswith(("다름", "없음"))]
        if not any(l.endswith(("다름", "없음")) for l in r.stdout.splitlines()):
            bad.append(f"build.py --verify가 실패함: {r.stderr[-200:]}")
if f"같음 {len(DOCS)}," not in runs[0]:
    bad.append(f"같음이 {len(DOCS)}개가 아님")
if runs[0] != runs[1]:
    bad.append("두 번의 출력이 다름")
report(f"12. 원본으로 다시 만든 마크다운 {len(DOCS)}개의 해시가 기록과 같다 (두 번, 파일을 쓰지 않음)", bad)

sys.exit(0 if all(results) else 1)
