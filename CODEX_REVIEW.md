# Codex 검토 기록 (이슈 #7, 2단계 희토류 원소 문서 목록·수집·변환)

2차 검토 때 Codex가 1차 지적을 하나씩 대조하는 데 쓴다. 이슈를 닫을 때 커밋한 뒤 지운다.

- 1차 검토: 2026-10-22 18:26:12~18:41:55, `gpt-6.1-sol`, `max`. 고정 프롬프트(`.codex/review-prompt.md`)에 아래 "1차 요청"과 이슈 #7 본문을 붙여 넘겼다. 지적 3개(심각 0, 보통 2, 낮음 1). Codex가 문제없다고 본 것: 문서 20개·판, 원본 재변환 해시, 변환 검사 12개, 저장 집계(4,042자리·737묶음·209개)의 재현, 결과를 본 뒤 고친 경위와 미루거나 생략한 셋이 사용자 결정에 묶임. "부딪힘 아님" 76개는 모두, 부딪힘은 표본 33개를 원문과 대조했다.
- 2차 검토: 2026-10-22 18:52:26~18:59:37, `gpt-6.1-sol`, `max`. 고정 프롬프트에 아래 "2차 요청"과 이 파일 전체(커밋 `6d3530b`), 이슈 #7 본문을 붙여 넘겼다. 1차 지적 셋을 모두 "해소됨"으로 가렸고 새 지적 1개(낮음)를 냈다.

## 1차 지적의 처리

사용자가 셋 다 반영하기로 했다("가로 진행하고 다음 작업들도 이어서 자동으로 진행해줘"). 반영한 결과(커밋 `7456beb`, `7bcce8c`, `6c83020`): 판정 199개(부딪힘 125, 부딪힘 아님 74), 부딪히는 값 213개, 3 세기 사실은 후보 검사 기준 한국어 20개(표 15)·영어 18개(표 5), 질문 재료 수는 그대로다(`decisions/judgments.md` 2026-10-22 "이슈 #7 Codex 1차 검토" 줄).

| 지적 | 판정 | 처리 |
|---|---|---|
| 1 `verdicts.json`의 Sm-149 반감기(`wiki-ko-samarium.md` 62줄 `>2×10¹⁵ y`, 89줄 `2×10¹⁵년 이상`)를 "같은 하한"으로 부딪힘 아님 판정해 부딪히는 값 목록에서 빠짐(보통) | 맞음. `compare.py` 설명(14줄)이 "부등호가 다르면 다른 값"이고, 수가 같을 때만 같은 값이라는 기준(`decisions/stage2.md` 2026-10-22)으로도 경계를 넣는지가 다르다 | 판정을 부딪힘으로 고친다. 같은 까닭으로 `wiki-ko-ytterbium.md` 117줄 "나머지 방사성 동위원소들은 반감기가 2시간을 넘지 않으며 대부분 20분 이하"와 `wiki-en-ytterbium.md` 119줄 "less than 2 hours … less than 20 minutes"도 견준다. 두 언어의 대상 열쇠가 달라(`other Yb radioactive isotopes`와 `remaining radioactive ytterbium isotopes`) 묶이지 않았으므로 `vocab.json`의 `place_override`로 한국어 두 자리의 대상을 영어와 맞춘다 |
| 2 연대(`1990s`, `mid-1990s`)를 1990초로 읽어 `wiki-en-neutron-capture-therapy.md` 101줄 "until the 1990s"와 111줄 "mid-1990s"를 같음으로 보고 부딪힘을 놓침(보통) | 맞음. 값 목록의 연대 21곳이 연대로 읽히지 않았고(영어 18곳은 초로, 한국어 3곳은 단위 없는 수로. 처음에 "모두 그렇게 읽혔다"고 적은 것을 2차 지적으로 바로잡음), "초·중·후반"이 사라졌다 | `extract.py`가 연대를 연대(단위 `decade`, 초·중·후반 `decade_part`)로 읽고, `compare.py`는 연대와 초·중·후반이 모두 같을 때만 같은 값으로 본다. 3 세기 기록과 함께 쓰는 `src/domain_select/quantities.py`는 고치지 않는다 |
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

## 1차 지적 원문

보통 2건, 낮음 1건입니다. 파일은 수정하지 않았습니다.

1. **문제**: [verdicts.json:282](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_values_rare_earth/verdicts.json:282)에서 Sm-149 반감기의 다른 부등호를 “같은 하한”으로 기각했습니다.
   - **근거**: [사마륨 문서:62](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-ko-samarium.md:62)는 `>2×10¹⁵ y`, 같은 파일 89줄은 `2×10¹⁵년 이상(≥)`입니다. 경계 포함 여부가 다르고, `compare.py:14`도 다른 부등호를 다른 값으로 명시합니다. 이 묶음은 충돌 목록에서 빠졌습니다.
   - **심각도**: 보통
   - **고칠 방법**: 판정을 `부딪힘`으로 고치고 충돌 목록·사실 재계산·질문 재료와 판단 기록을 갱신하세요. 이 누락을 반영하면 후보 검사 기준 한국어 사실 수가 21개에서 20개로 바뀝니다.

2. **문제**: [values.json:3938](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_values_rare_earth/values.json:3938)에서 연대의 정밀도 차이를 잃어 충돌을 놓쳤습니다.
   - **근거**: [중성자 포획 치료 문서:101](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-en-neutron-capture-therapy.md:101)의 `until the 1990s`와 111줄의 `mid-1990s`가 모두 `1990 s`로 저장됩니다. 따라서 `compare.json:34`에서 “같음”, 검토 제외로 처리됩니다. 이는 `decisions/stage2.md:129`의 “덜 자세하게 적힌 날짜도 다른 값” 기준과 어긋납니다.
   - **심각도**: 보통
   - **고칠 방법**: 연대를 초 단위 `s`로 읽지 않도록 고치고, `mid-` 같은 시기 정밀도를 보존하세요. 해당 묶음을 다시 판정하고 충돌 목록과 파생 결과를 갱신하세요.

3. **문제**: [classify.py:65](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_table_shapes_rare_earth/classify.py:65)와 생성된 표 모양 보고서에 수정 전 설명이 남았습니다.
   - **근거**: “줄바꿈을 빈칸 하나로 바꿔 항목의 경계가 사라졌다”고 적지만, [이트륨 문서:58](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-ko-yttrium.md:58)·60줄은 이미 `0.48 / 0.38D`, `1.83 / 0.89`로 경계를 보존합니다.
   - **심각도**: 낮음
   - **고칠 방법**: 이트륨은 경계 보존 완료, 중성자 포획 치료 표의 문단 경계는 남은 한계로 구분해 설명하고 `shapes.json`·`shapes.md`를 다시 생성하세요.

**문제없다고 판단한 부분**: 문서 20개·판 일치, 원본 재변환 해시, 변환 검사 12개와 저장 집계 4,042자리·737묶음·209개의 재현은 확인했습니다.  
결과를 본 뒤 고친 경위와 세 가지 연기·생략은 사용자 결정 기록에 연결됩니다.  
“부딪힘 아님” 76개는 전수, 나머지 충돌은 33개 표본을 원문 대조했습니다. 나머지 충돌 전수는 미확인이고, 최종 평가용 질문은 찾거나 열지 않았습니다.

## 2차 요청

- 단계: 이슈 #7의 2차 검토다. 1차 뒤에 고친 커밋은 `git log 13d637c..HEAD`로 본다(`7456beb` 연대 읽기, `7bcce8c` 표 모양 설명, `6c83020` 판정·묶음과 다시 만든 결과, `0ae4a68` 기록).
- 할 일: 위 "1차 지적의 처리"의 지적 셋을 하나씩 대조해 해소됨 / 절반만 됨 / 안 됨으로 가르고, 고치면서 새로 생긴 문제만 더 써라.
- 이번에 특히 볼 것:
  1. 연대 고침이 다른 값을 바꾸지 않았는가. 바뀐 것은 연대 21곳뿐이어야 한다(`git diff 13d637c..HEAD -- research_notes/stage2_values_rare_earth/values.json`). `src/domain_select/quantities.py`는 바뀌지 않았어야 한다.
  2. 다시 만든 결과의 숫자(판정 199개 가운데 부딪힘 125·부딪힘 아님 74, 부딪히는 값 213개, 3 세기 사실 한국어 20개·영어 18개, 질문 재료)가 저장된 파일과 맞는가.
  3. 이터븀 117줄 두 자리의 대상을 영어 열쇠에 맞춘 것(`vocab.json`의 `place_override`)과 지운 옛 판정 열쇠가 기록과 맞는가.

## 2차 지적의 처리

| 지적 | 판정 | 처리 |
|---|---|---|
| 1차 지적 1~3 | Codex가 모두 "해소됨"으로 가렸다 | 없음 |
| 새 지적 1 `decisions/judgments.md` 146줄과 이 파일 15줄의 "연대 21곳이 모두 초로 읽힌 고장"이 부정확함. 고치기 전 커밋 `13d637c`에서 영어 18곳은 단위 `s`, 한국어 3곳은 단위 없는 수였다(낮음) | 맞음. `13d637c`와 지금의 `values.json`을 프로그램으로 견줘, 바뀐 21곳이 영어 18곳(단위 `s`)과 한국어 3곳(단위 없음, `wiki-ko-dysprosium` 69줄·`wiki-ko-lutetium` 63줄의 `1950년대`, `wiki-ko-samarium` 95줄의 `1920년대`)임을 확인했다. 값·판정·부딪히는 값·다시 센 결과는 바뀌지 않고 기록의 문장만 틀렸다 | 틀린 사실을 바로잡는 문서 맞추기라(`CLAUDE.md` 2, 6) 먼저 고쳤다(커밋 `b64499f`). 두 기록의 문장을 "연대로 읽지 못한 고장(영어 18곳은 초로, 한국어 3곳은 단위 없는 수로)"으로 바꾸고 바로잡았다고 적었다. 이슈 #7 본문과 흐름 요약의 같은 말도 고쳤다. 산출물(값 목록, 판정, 부딪히는 값 목록)은 고치지 않았다. 반영 여부는 사용자가 정하는 일이라(`STEPPER.md` "단계를 닫는 절차" ⑥) 닫기 승인을 받을 때 알린다. 다시 검토받지 않는다 |

## 2차 지적 원문

1차 지적 3건은 모두 **해소됨**입니다. 추가 지적은 **낮음 1건**입니다.

| 1차 지적 | 판정 | 확인 근거 |
|---|---|---|
| 1. Sm-149·이터븀 부등호 | 해소됨 | 충돌 목록 반영, 이터븀 두 대상 정렬, 옛 판정 열쇠 삭제 확인 |
| 2. 연대 읽기 | 해소됨 | 4,042개 중 연대 21곳의 `reps`만 변경. `quantities.py`는 동일 |
| 3. 표 모양 설명 | 해소됨 | 실제 표와 설명이 일치하고, 두 보고서 재생성 결과도 일치 |

추가 지적:

- **문제**: [decisions/judgments.md:146](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/judgments.md:146)의 “연대 21곳이 모두 초로 읽힌 고장”은 부정확합니다. [CODEX_REVIEW.md:15](/Users/seungchan/Workspace/MultilingualAgentRAG/CODEX_REVIEW.md:15)에도 같은 설명이 있습니다.
- **근거**: 수정 전 커밋 `13d637c`의 값을 대조하면 영어 18곳은 `unit: "s"`였지만, 한국어 3곳은 `unit: ""`였습니다. 수정된 연대는 21곳이 맞지만, 모두 초 단위였던 것은 아닙니다.
- **심각도**: 낮음
- **고칠 방법**: 두 기록을 “연대 21곳 가운데 영어 18곳은 초로, 한국어 3곳은 단위 없는 수로 읽혔다”로 고치십시오.

**문제없다고 판단한 부분**

- 판정 199개(125·74), 충돌 213개, 후보 검사 후 사실 한국어 20개(표 15)·영어 18개(표 5)는 재계산과 일치합니다.
- 질문 재료는 언어별 연결 12개·표/수치/조건 6개이며, 교체된 재료도 원문과 일치합니다.
- 추가 시험 5개는 통과했습니다. 전체 시험 97개는 재실행하지 않았고, 최종 평가용 질문은 찾거나 열지 않았습니다. 파일은 수정하지 않았습니다.
