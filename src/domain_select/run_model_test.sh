#!/bin/bash
# 후보 고르기 실험(이슈 #6)의 4 모델 시험. 먼저 질문 파일을 검사하고(통과하지 않으면 멈춤),
# 분야마다 몸풀기 한 번 뒤에 base 조건을 돌린다. 동시에 돌리지 않고 하나씩 돌린다.
#   bash src/domain_select/run_model_test.sh [분야 ...]   (기본: exoplanets rare_earth)
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE=research_notes/stage2_stem_select/step4
WARMUP=research_notes/stage2_stem_select/short_test/warmup.json
if [ $# -gt 0 ]; then TOPICS=("$@"); else TOPICS=(exoplanets rare_earth); fi

python3 src/domain_select/check_model_test.py

for t in "${TOPICS[@]}"; do
  R=$BASE/$t/results
  if [ -e "$R" ]; then echo "$R가 이미 있다. 결과에 덧붙지 않게 멈춘다" >&2; exit 1; fi
  mkdir -p "$R"
  echo "[$(date '+%H:%M:%S')] $t 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions "$WARMUP" --seeds 1 --out "$R/warmup.jsonl" 2>>"$R/run.log"
  python3 src/domain_select/run.py base --questions "$BASE/$t/questions.json" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t 끝" | tee -a "$R/run.log"
done
