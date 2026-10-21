#!/bin/bash
# 후보 고르기 실험(이슈 #6)의 4 모델 시험에 문서를 넣고 묻는 조건(C, run.py의 context)을 더한다.
# 결정: decisions/stage2.md "4 모델 시험에 문서를 넣고 묻는 조건 … 더한다" 줄.
# 문서 없이(base) 돌린 결과가 끝난 분야에만 돌린다. 분야마다 몸풀기 한 번 뒤에 C를 돌리고, 동시에 돌리지 않고 하나씩 돌린다.
#   bash src/domain_select/run_model_test_context.sh [분야 ...]   (기본: exoplanets rare_earth)
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE=research_notes/stage2_stem_select/step4
WARMUP=research_notes/stage2_stem_select/short_test/warmup.json
if [ $# -gt 0 ]; then TOPICS=("$@"); else TOPICS=(exoplanets rare_earth); fi

python3 src/domain_select/check_model_test.py

for t in "${TOPICS[@]}"; do
  R=$BASE/$t/results
  if [ ! -f "$R/base.jsonl" ] || [ "$(wc -l < "$R/base.jsonl" | tr -d ' ')" != 100 ]; then
    echo "$R/base.jsonl이 없거나 100줄이 아니다. 문서 없이 돌린 것이 끝나야 한다" >&2; exit 1
  fi
  if [ -e "$R/context.jsonl" ]; then echo "$R/context.jsonl이 이미 있다. 결과에 덧붙지 않게 멈춘다" >&2; exit 1; fi
  echo "[$(date '+%H:%M:%S')] $t C 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions "$WARMUP" --seeds 1 --out "$R/warmup_context.jsonl" 2>>"$R/run.log"
  python3 src/domain_select/run.py context --questions "$BASE/$t/questions.json" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t C 끝" | tee -a "$R/run.log"
done
