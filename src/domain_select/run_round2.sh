#!/bin/bash
# 후보 고르기 실험(이슈 #6)의 정식 실험. 분야마다 몸풀기 한 번 뒤에 A(base) → C(context)를 하나씩 돌린다. 동시에 돌리지 않는다.
#   bash src/domain_select/run_round2.sh [폴더 이름 ...]   (기본: rare_earth exoplanets moons)
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE=research_notes/stage2_stem_select
if [ $# -gt 0 ]; then TOPICS=("$@"); else TOPICS=(rare_earth exoplanets moons); fi

for t in "${TOPICS[@]}"; do
  R=$BASE/round2/$t/results
  Q=$BASE/round2/$t/questions.json
  if [ -e "$R" ]; then echo "$R가 이미 있다. 결과에 덧붙지 않게 멈춘다" >&2; exit 1; fi
  mkdir -p "$R"
  echo "[$(date '+%H:%M:%S')] $t 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions $BASE/short_test/warmup.json --seeds 1 --out "$R/warmup.jsonl" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t A 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions "$Q" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t C 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py context --questions "$Q" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t 끝" | tee -a "$R/run.log"
done
