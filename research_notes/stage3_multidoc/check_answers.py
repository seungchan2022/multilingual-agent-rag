"""answers/NN.json이 batches/NN.json의 낱말에 빠짐없이 답했는지, 후보의 구절이 원문 그 줄에 글자 그대로 있는지 센다."""
import json, sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).parent
MD = HERE.parents[1] / "data/corpus/markdown"
VERDICTS = {"이름 아님", "같은 대상 아님", "이어 찾기 안 됨", "한 문서로 답 나옴", "답이 하나 아님", "영어 문서에 있음", "값이 부딪힘", "제외 목록", "후보"}
lines_of = {}
def line(doc, n):
    if doc not in lines_of:
        lines_of[doc] = (MD / f"{doc}.md").read_text(encoding="utf-8").splitlines()
    L = lines_of[doc]
    return L[n - 1] if 1 <= n <= len(L) else None

def check_cand(c, where):
    errs = []
    for k in ("question", "answer", "bridge", "target", "en_terms", "en_result", "ko_conflict", "bucket"):
        if not c.get(k): errs.append(f"{where}: {k} 없음")
    for k in ("bridge", "target"):
        p = c.get(k) or {}
        if not p.get("doc", "").count("-ko-"): errs.append(f"{where}: {k} 문서가 한국어가 아님")
        l = line(p.get("doc", ""), p.get("line", 0)) if (MD / f"{p.get('doc','')}.md").exists() else None
        if l is None or p.get("passage", "\0") not in l: errs.append(f"{where}: {k} 구절이 {p.get('doc')}:{p.get('line')}에 없음")
    if c.get("bucket") not in ("두 언어 도시", "한국어 도시"): errs.append(f"{where}: bucket 값")
    return errs

total = Counter(); errs = []; cands = []
for bf in sorted((HERE / "batches").glob("*.json")):
    af = HERE / "answers" / bf.name
    want = [x["name"] for x in json.loads(bf.read_text(encoding="utf-8"))]
    if not af.exists():
        errs.append(f"{bf.name}: 답 파일 없음"); continue
    got = json.loads(af.read_text(encoding="utf-8"))
    names = [a.get("name") for a in got]
    if names != want:
        miss = [n for n in want if n not in names]; extra = [n for n in names if n not in want]
        errs.append(f"{bf.name}: 낱말이 다름 (빠짐 {len(miss)} {miss[:5]}, 더함 {len(extra)} {extra[:5]}, 순서/중복 확인)")
    for a in got:
        v = a.get("verdict")
        if v not in VERDICTS: errs.append(f"{bf.name}/{a.get('name')}: verdict '{v}'")
        total[v] += 1
        if v == "후보":
            errs += check_cand(a, f"{bf.name}/{a['name']}")
            cands.append((bf.name, a))
            for i, o in enumerate(a.get("other_candidates") or []):
                errs += check_cand(o, f"{bf.name}/{a['name']}/other{i}")
                cands.append((bf.name, o))
        elif not a.get("reason"):
            errs.append(f"{bf.name}/{a.get('name')}: reason 없음")
print("판정:", dict(total))
print("후보:", len(cands), Counter(c.get("bucket") for _, c in cands))
for b, c in cands: print(" ", b, c.get("name"), "|", c.get("question"), "|", c.get("bucket"))
print("문제:", len(errs)); [print(" ", e) for e in errs]
