# Codex 검토 기록 (이슈 #7, 2단계 희토류 원소 문서 목록·수집·변환)

2차 검토 때 Codex가 1차 지적을 하나씩 대조하는 데 쓴다. 이슈를 닫을 때 커밋한 뒤 지운다.

- 1차 검토: 2026-10-22 18:26:12~18:41:55, `gpt-6.1-sol`, `max`. 고정 프롬프트(`.codex/review-prompt.md`)에 아래 "1차 요청"과 이슈 #7 본문을 붙여 넘겼다. 지적 3개(심각 0, 보통 2, 낮음 1). Codex가 문제없다고 본 것: 문서 20개·판, 원본 재변환 해시, 변환 검사 12개, 저장 집계(4,042자리·737묶음·209개)의 재현, 결과를 본 뒤 고친 경위와 미루거나 생략한 셋이 사용자 결정에 묶임. "부딪힘 아님" 76개는 모두, 부딪힘은 표본 33개를 원문과 대조했다.
- 2차 검토: 2026-10-22, `gpt-6.1-sol`, `max`. 고정 프롬프트에 아래 "2차 요청"과 이 파일 전체, 이슈 #7 본문을 붙여 넘겼다.

## 1차 지적의 처리

사용자가 셋 다 반영하기로 했다("가로 진행하고 다음 작업들도 이어서 자동으로 진행해줘"). 반영한 결과(커밋 `7456beb`, `7bcce8c`, `6c83020`): 판정 199개(부딪힘 125, 부딪힘 아님 74), 부딪히는 값 213개, 3 세기 사실은 후보 검사 기준 한국어 20개(표 15)·영어 18개(표 5), 질문 재료 수는 그대로다(`decisions/judgments.md` 2026-10-22 "이슈 #7 Codex 1차 검토" 줄).

| 지적 | 판정 | 처리 |
|---|---|---|
| 1 `verdicts.json`의 Sm-149 반감기(`wiki-ko-samarium.md` 62줄 `>2×10¹⁵ y`, 89줄 `2×10¹⁵년 이상`)를 "같은 하한"으로 부딪힘 아님 판정해 부딪히는 값 목록에서 빠짐(보통) | 맞음. `compare.py` 설명(14줄)이 "부등호가 다르면 다른 값"이고, 수가 같을 때만 같은 값이라는 기준(`decisions/stage2.md` 2026-10-22)으로도 경계를 넣는지가 다르다 | 판정을 부딪힘으로 고친다. 같은 까닭으로 `wiki-ko-ytterbium.md` 117줄 "나머지 방사성 동위원소들은 반감기가 2시간을 넘지 않으며 대부분 20분 이하"와 `wiki-en-ytterbium.md` 119줄 "less than 2 hours … less than 20 minutes"도 견준다. 두 언어의 대상 열쇠가 달라(`other Yb radioactive isotopes`와 `remaining radioactive ytterbium isotopes`) 묶이지 않았으므로 `vocab.json`의 `place_override`로 한국어 두 자리의 대상을 영어와 맞춘다 |
| 2 연대(`1990s`, `mid-1990s`)를 1990초로 읽어 `wiki-en-neutron-capture-therapy.md` 101줄 "until the 1990s"와 111줄 "mid-1990s"를 같음으로 보고 부딪힘을 놓침(보통) | 맞음. 값 목록의 연대 21곳이 모두 그렇게 읽혔고, "초·중·후반"이 사라졌다 | `extract.py`가 연대를 연대(단위 `decade`, 초·중·후반 `decade_part`)로 읽고, `compare.py`는 연대와 초·중·후반이 모두 같을 때만 같은 값으로 본다. 3 세기 기록과 함께 쓰는 `src/domain_select/quantities.py`는 고치지 않는다 |
| 3 `research_notes/stage2_table_shapes_rare_earth/classify.py`의 "한 칸에 여러 항목이 든 표" 설명이 줄바꿈 규칙을 고치기 전 상태로 남음(낮음) | 맞음 | 이트륨 칸은 ` / `로 경계가 살아났고 중성자 포획 치료 장비 표는 문단으로 나뉜 항목이 빈칸으로 이어진 채 남는다고 고쳐 `shapes.json`·`shapes.md`를 다시 만든다 |

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

## 2차 요청

- 단계: 이슈 #7의 2차 검토다. 1차 뒤에 고친 커밋은 `git log 13d637c..HEAD`로 본다(`7456beb` 연대 읽기, `7bcce8c` 표 모양 설명, `6c83020` 판정·묶음과 다시 만든 결과, `0ae4a68` 기록).
- 할 일: 위 "1차 지적의 처리"의 지적 셋을 하나씩 대조해 해소됨 / 절반만 됨 / 안 됨으로 가르고, 고치면서 새로 생긴 문제만 더 써라.
- 이번에 특히 볼 것:
  1. 연대 고침이 다른 값을 바꾸지 않았는가. 바뀐 것은 연대 21곳뿐이어야 한다(`git diff 13d637c..HEAD -- research_notes/stage2_values_rare_earth/values.json`). `src/domain_select/quantities.py`는 바뀌지 않았어야 한다.
  2. 다시 만든 결과의 숫자(판정 199개 가운데 부딪힘 125·부딪힘 아님 74, 부딪히는 값 213개, 3 세기 사실 한국어 20개·영어 18개, 질문 재료)가 저장된 파일과 맞는가.
  3. 이터븀 117줄 두 자리의 대상을 영어 열쇠에 맞춘 것(`vocab.json`의 `place_override`)과 지운 옛 판정 열쇠가 기록과 맞는가.

