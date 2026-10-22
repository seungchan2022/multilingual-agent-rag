# Codex 검토 기록 (이슈 #7, 2단계 희토류 원소 문서 목록·수집·변환)

2차 검토 때 Codex가 1차 지적을 하나씩 대조하는 데 쓴다. 이슈를 닫을 때 커밋한 뒤 지운다.

- 1차 검토: 2026-10-22, `gpt-6.1-sol`, `max`. 고정 프롬프트(`.codex/review-prompt.md`)에 아래 "1차 요청"과 이슈 #7 본문을 붙여 넘겼다.
- 2차 검토: 아직 하지 않았다.

## 1차 지적의 처리

(1차 검토가 끝나면 적는다)

## 1차 요청

- 단계: 2단계 가운데 이슈 #7 `[2단계] 희토류 원소 문서 목록·수집·변환`. 1차 검토다. 브랜치 `7-rare-earth-corpus`는 `main`에서 땄고, 이 이슈의 커밋은 `git log e1a0c77..HEAD`로 볼 수 있다.
- 무엇을 했나: 이슈 #6에서 정한 도메인(희토류 원소)의 위키백과 문서 20개(한국어 10, 영어 10)로 코퍼스를 새로 만들었다. 문서 목록을 적고, 원문을 받아 마크다운으로 바꾸고, 사용자가 두 문서를 열어 본 지적을 변환 규칙으로 고쳤다. 변환 검사를 희토류 원소 기준으로 다시 썼고, 표의 모양을 다시 셌다. 도시 때 사실 목록 대신 값 목록(문서에 적힌 값을 대상과 양마다 모은 목록)을 만들어 문서끼리 견주고, 같은 대상·양이 다르게 적힌 "부딪히는 값" 209개를 `data/questions/known_conflicts.json`에 썼다. 그 목록으로 3 세기(도메인을 고를 때 AI가 원문과 대조해 센 단계)의 한쪽 언어 사실이 언어마다 18개 남는지 다시 셌다. 이어서 남은 도메인 기준과 여러 문서 연결 질문·표 질문의 재료를 확인했다. 두 번째 소스는 사용자 결정으로 찾지 않았다.
- 산출물(읽을 것):
  - 결정: `decisions/stage2.md`의 2026-10-22 줄들, `decisions/common.md`의 2026-10-22 "도시 때 만든 것은 기록과 도구·규칙으로 나눠 다룬다" 줄
  - 판단: `decisions/judgments.md`의 2026-10-22 줄들
  - 계획 변경: `STEPPER.md`. 이 이슈에서 바꾼 곳은 `git diff e1a0c77..HEAD -- STEPPER.md`로 본다
  - 미정 목록: `DECISIONS.md`의 "아직 정하지 않은 것". 이 이슈에서 더하거나 고치거나 지운 줄은 `git diff e1a0c77..HEAD -- DECISIONS.md`로 본다
  - 코퍼스: `data/corpus/documents.yaml`, `data/corpus/markdown/`, `src/corpus/`(`fetch.py`, `build.py`, `check_build.py`)
  - 표 모양: `research_notes/stage2_table_shapes_rare_earth/`
  - 값 목록과 부딪히는 값: `research_notes/stage2_values_rare_earth/`(`extract.py`, `vocab.json`, `values.json`, `compare.py`, `compare.json`, `review.md`, `verdicts.json`, `build_conflicts.py`, `known_conflicts.md`, `recheck_step3.py`, `recheck_step3.json`, `confirm_more.json`, `materials.py`, `materials.md`, `materials_check.md`, `same_sample.md`)와 `data/questions/known_conflicts.json`. `src/questions/check_candidates.py`는 오류 문구 두 줄의 경로만 바꿨다
  - 이슈 #7 체크리스트: 아래 "이슈 #7 본문"에 그대로 붙였다
- 이번 검토에서 특히 볼 것:
  1. 결과를 본 뒤 바꾼 것의 기록이 정직한가. ㉠ 견주기 결과를 읽다가 동위 원소 존재비가 두 열쇠로 갈라진 것을 찾아 합쳤다(커밋 `af06ca9`) ㉡ 3 세기 다시 세기에서 후보 검사 기준 셈이 영어 17개로 모자란 것을 본 뒤, 사용자 결정으로 3 세기 차례를 이어 영어 사실 2개를 더 확인했다(`decisions/stage2.md` 2026-10-22 "3 세기 사실이 남는지는 …" 줄, `confirm_more.json`) ㉢ 그 결정의 이유에 적은 "가장 엄격한 셈"이 틀려 바로잡았다. 바꾼 것 자체를 되돌리라고 하지 말고, 무엇을 본 뒤 무엇을 바꿨는지 숨김없이 적었는지를 봐라.
  2. `verdicts.json`의 판정 197개 가운데 표본을 원문 줄(`data/corpus/markdown/`)과 대조해라. 부딪히는 값을 놓치는 쪽인 "부딪힘 아님" 76개를 중심으로 봐라. 판정 기준은 `decisions/stage2.md` 2026-10-22 "희토류 원소 값 목록의 '다른 값' 기준" 줄과, AI가 가른 규칙(`decisions/judgments.md` 2026-10-22 "희토류 원소 값 목록과 견주기를 검토했다" 줄의 근거 칸)이다.
  3. 오늘 판단 기록 줄의 숫자가 저장된 결과(`values.json`, `compare.json`, `verdicts.json`, `known_conflicts.json`, `recheck_step3.json`, `materials.json`)와 맞는가.
  4. 체크된 항목 가운데 완료 기준을 미루거나 바꾼 것(진행 안내 끝의 "알려진 부딪히는 값" 목록, 두 번째 소스, 3단계 질문 프로그램의 시험)이 실제 사용자 결정에 묶여 있는가.
