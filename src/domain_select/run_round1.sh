#!/bin/bash
# 후보 고르기 실험(이슈 #6)의 첫 번째 재기. 주제마다 A(base) → B-v1(refine) → C(context)를 차례로 돌린다.
# B-v1은 질문을 네 묶음으로 나눠 동시에 돌리고 refine.jsonl 하나로 합친다(decisions/stage2.md 2026-10-19).
#   bash src/domain_select/run_round1.sh [주제 폴더 이름 ...]   (기본: chem solar mineral)
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE=research_notes/stage2_stem_select
if [ $# -gt 0 ]; then TOPICS=("$@"); else TOPICS=(chem solar mineral); fi

for t in "${TOPICS[@]}"; do
  Q=$BASE/$t/questions.json
  R=$BASE/$t/results
  if [ -e "$R" ]; then echo "$R가 이미 있다. 결과에 덧붙지 않게 멈춘다" >&2; exit 1; fi
  mkdir -p "$R"
  ids=($(python3 -c "import json,sys;print(' '.join(q['id'] for q in json.load(open(sys.argv[1]))))" "$Q"))
  echo "[$(date '+%H:%M:%S')] $t A 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions "$Q" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t B-v1 시작" | tee -a "$R/run.log"
  pids=()
  i=1
  for g in "${ids[*]:0:3}" "${ids[*]:3:3}" "${ids[*]:6:2}" "${ids[*]:8:2}"; do
    python3 src/domain_select/run.py refine --questions "$Q" --only $g --out "$R/refine_p$i.jsonl" 2>>"$R/run.log" &
    pids+=($!)
    i=$((i + 1))
  done
  for p in "${pids[@]}"; do wait "$p" || echo "B-v1 묶음 하나가 오류로 끝남(pid $p)" | tee -a "$R/run.log"; done
  python3 - "$Q" "$R" <<'EOF'
# 네 묶음을 질문 차례, 씨앗 차례로 합친다. 같은 (질문, 씨앗)이 둘이면 멈춘다.
import json, sys
from pathlib import Path
qs, r = json.load(open(sys.argv[1])), Path(sys.argv[2])
order = {q["id"]: n for n, q in enumerate(qs)}
rows = [json.loads(l) for i in range(1, 5) for l in (r / f"refine_p{i}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
keys = [(x["id"], x["seed"]) for x in rows]
assert len(keys) == len(set(keys)), "같은 (질문, 씨앗)이 둘 있다"
rows.sort(key=lambda x: (order[x["id"]], x["seed"]))
(r / "refine.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
print(f"refine.jsonl {len(rows)}줄")
EOF
  echo "[$(date '+%H:%M:%S')] $t C 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py context --questions "$Q" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t 끝" | tee -a "$R/run.log"
done
