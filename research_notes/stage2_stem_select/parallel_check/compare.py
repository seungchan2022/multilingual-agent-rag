"""Ollama 동시 처리 시험(이슈 #6): 다시 돌린 A의 생성 글이 첫 번째 재기에 저장된 같은 질문·씨앗의 글과 같은지 본다.

  python3 research_notes/stage2_stem_select/parallel_check/compare.py <다시 돌린 결과.jsonl> ...

기준은 research_notes/stage2_stem_select/chem/results/base.jsonl이다. 생성 글(gen.text)이 글자 그대로 같은지를 센다.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SAVED = ROOT / "research_notes/stage2_stem_select/chem/results/base.jsonl"


def rows(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


saved = {(r["id"], r["seed"]): r for r in rows(SAVED)}
for path in sys.argv[1:]:
    new = rows(path)
    same = [r for r in new if r["gen"]["text"] == saved[(r["id"], r["seed"])]["gen"]["text"]]
    print(f"{Path(path).name}: {len(new)}개 가운데 저장된 글과 같은 것 {len(same)}개, "
          f"호출 시간 합 {sum(r['gen']['seconds'] for r in new):.1f}초")
    for r in new:
        s = saved[(r["id"], r["seed"])]
        if r["gen"]["text"] != s["gen"]["text"]:
            a, b = r["gen"]["text"], s["gen"]["text"]
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            print(f"  다름 {r['id']} 씨앗 {r['seed']}: {i}번째 글자부터. 새 {a[i:i + 30]!r} / 저장 {b[i:i + 30]!r}")
