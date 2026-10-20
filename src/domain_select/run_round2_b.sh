#!/bin/bash
# 후보 고르기 실험(이슈 #6)의 정식 실험. 분야마다 몸풀기 두 번(base, refine) 뒤에 B(refine)를 하나씩 돌린다.
# B-v1과 B-v2는 같은 스크립트로 돌리고, 판정 프롬프트 파일(judge_prompts/<판>.txt)만 다르다(첫 인자 v1 또는 v2).
# 첫 번째 실험(run_round1.sh)과 달리 질문을 묶음으로 나눠 동시에 보내지 않는다(decisions/stage2.md 2026-10-19 "B-v2 전 확인" 줄).
#   bash src/domain_select/run_round2_b.sh <v1|v2> <폴더 이름> [폴더 이름 ...]
# 출력: v1은 results/refine.jsonl(결과 페이지가 읽는 이름), v2는 results/refine_v2.jsonl
set -euo pipefail
cd "$(dirname "$0")/../.."
BASE=research_notes/stage2_stem_select
if [ $# -lt 2 ]; then
  echo "사용법: bash src/domain_select/run_round2_b.sh <v1|v2> <폴더 이름> [폴더 이름 ...]" >&2
  exit 1
fi
V=$1
shift
JS=src/domain_select/judge_prompts/$V.txt
if [ ! -e "$JS" ]; then echo "$JS가 없다" >&2; exit 1; fi
if [ "$V" = "v1" ]; then OUTNAME=refine.jsonl; else OUTNAME=refine_$V.jsonl; fi

for t in "$@"; do
  R=$BASE/round2/$t/results
  Q=$BASE/round2/$t/questions.json
  if [ ! -e "$R/base.jsonl" ]; then echo "$R/base.jsonl이 없다. A를 먼저 돌려야 한다" >&2; exit 1; fi
  if [ -e "$R/$OUTNAME" ]; then echo "$R/$OUTNAME이 이미 있다. 결과에 덧붙지 않게 멈춘다" >&2; exit 1; fi
  echo "[$(date '+%H:%M:%S')] $t B-$V 시작" | tee -a "$R/run.log"
  python3 src/domain_select/run.py base --questions $BASE/short_test/warmup.json --seeds 1 --out "$R/warmup_b_$V.jsonl" 2>>"$R/run.log"
  python3 src/domain_select/run.py refine --questions $BASE/short_test/warmup.json --seeds 1 --base "$R/warmup_b_$V.jsonl" --judge-system "$JS" --out "$R/warmup_b_${V}_refine.jsonl" 2>>"$R/run.log"
  python3 src/domain_select/run.py refine --questions "$Q" --judge-system "$JS" --out "$R/$OUTNAME" 2>>"$R/run.log"
  echo "[$(date '+%H:%M:%S')] $t B-$V 끝" | tee -a "$R/run.log"
done
