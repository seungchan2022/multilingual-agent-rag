#!/bin/bash
# 후보 고르기 실험(이슈 #6)의 정식 실험. 분야마다 몸풀기 두 번(base, refine) 뒤에 B-v1(refine)을 하나씩 돌린다.
# 첫 번째 실험(run_round1.sh)과 달리 질문을 묶음으로 나눠 동시에 보내지 않는다(decisions/stage2.md 2026-10-19 "B-v2 전 확인" 줄).
#   bash src/domain_select/run_round2_b.sh <폴더 이름> [폴더 이름 ...]
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE=research_notes/stage2_stem_select
if [ $# -eq 0 ]; then
  echo "사용법: bash src/domain_select/run_round2_b.sh <폴더 이름> [폴더 이름 ...]" >&2
  exit 1
fi

for t in "$@"; do
  R=$BASE/round2/$t/results
  Q=$BASE/round2/$t/questions.json
  if [ ! -e "$R/base.jsonl" ]; then echo "$R/base.jsonl이 없다. A를 먼저 돌려야 한다" >&2; exit 1; fi
  if [ -e "$R/refine.jsonl" ]; then echo "$R/refine.jsonl이 이미 있다. 결과에 덧붙지 않게 멈춘다" >&2; exit 1; fi
  echo "[$(date '+%H:%M:%S')] $t B-v1 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions $BASE/short_test/warmup.json --seeds 1 --out "$R/warmup_b.jsonl" 2>>"$R/run.log"
  python3 src/domain_select/run.py refine --questions $BASE/short_test/warmup.json --seeds 1 --base "$R/warmup_b.jsonl" --out "$R/warmup_b_refine.jsonl" 2>>"$R/run.log"
  python3 src/domain_select/run.py refine --questions "$Q" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t B-v1 끝" | tee -a "$R/run.log"
done
