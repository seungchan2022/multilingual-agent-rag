# 인계 (질문 작업)

**지금**: 3단계 개발용 질문(질문 작업) · 진행 중인 이슈 없음 · 시작 전. 이슈 #5 `[3단계] 질문`은 열려 있고 체크리스트는 도시 때 것이다
**다음**: 이슈 #5를 개발용과 최종 평가용으로 나누고, 개발용 서브이슈와 브랜치를 사용자 승인을 받아 만든다

---

## 다음 세션의 Claude에게

- 이 파일은 질문 작업 폴더(`/Users/seungchan/Workspace/MultilingualAgentRAG-questions`, 같은 저장소의 git worktree)의 인계 파일이다. 최소판 작업은 저장소 폴더에서 `HANDOFF.md`로 동시에 진행한다(`decisions/common.md` 2026-10-22 "Claude 세션 두 개로 동시에" 줄)
- 브랜치: 없음(`main`을 떼어 꺼낸 상태, `git switch --detach main`). 이 폴더는 `main`을 꺼내지 않는다. 새 브랜치는 `git switch -c <이슈번호-짧은-영문-이름> main`
- 맨 위 커밋: 이 파일을 넣은 `chore-parallel-tracks`의 커밋 `docs: 최소판과 질문 작업을 동시에 하는 방법을 정한다`. `[진행 중]` 커밋은 없다
- 끝낸 항목: 없음(이 작업의 첫 세션 전)
- 남은 항목(이슈 #5 개발용을 시작할 때)
  1. 이슈 #5를 개발용(지금)과 최종 평가용(10-25 뒤)으로 나눈다. 체크리스트의 순서, "하지 않는 것: 3단계 뒤 중간 검토", 도시 때 항목(`city_group`, `kto-en-*`, `excluded.json`)을 고친다(`DECISIONS.md` 미정 목록 "이슈 #5(`[3단계] 질문`)를 개발용 … 나눈다" 줄, "도시가 직접 적힌 곳" 줄)
  2. 3단계 프로그램과 시험을 희토류 원소에 맞게 고친다. `src/questions`의 시험은 92개 가운데 실패 9·오류 65다. 후보 검사(`src/questions/check_candidates.py`)는 도시 칸을 읽어 지금 불러오지 못하고, "값" 규칙이 흔한 두 자리 수(20, 50)로 관계없는 줄까지 막는다. 영어 한쪽 언어 사실이 18개로 여유가 없어 이 규칙에 민감하다(미정 목록 "도시가 직접 적힌 곳" 줄, "3단계 프로그램의 시험" 줄)
  3. 진행 안내 끝의 "알려진 부딪히는 값" 목록을 `research_notes/stage2_values_rare_earth/known_conflicts.md`로 바꾼다(`data/questions/known_conflicts.json`이 프로그램용)
  4. 영어 문서가 근거인 후보를 사용자가 대조하기 전에 대조 방법을 사용자와 다시 정한다(미정 목록 "영어 근거 질문의 대조 방법을 다시 본다" 줄. 이슈 #5 체크리스트에는 체크되어 있다)
- 정확히 멈춘 지점: 시작 전
- 커밋되지 않은 변경: 없음
- 구현용 서브에이전트 effort: `high`로 시작한다
- 다음 세션의 작업 흐름과 추천 effort
  1. 이슈 #5를 나누는 방법을 사용자와 정하고 서브이슈·브랜치를 만든다 — high
  2. 3단계 프로그램과 시험을 고친다(구현은 Sonnet 5.5 서브에이전트) — high
- 주의할 점
  - **최소판이 먼저다.** 사용자에게 가는 두 작업의 요청이 겹치면 최소판 쪽을 먼저 한다. 질문 작업은 최소판 일 사이의 틈에 한다
  - **코퍼스(`data/corpus/`)를 바꾸지 않는다.** 바뀌면 질문마다 반대 언어 문서 확인을 다시 해야 한다
  - **`main`이 앞서 있으면** 세션을 시작할 때 `git rebase main`으로 옮긴다. 합칠 때는 `session-close` 9번의 질문 작업 폴더 방법을 쓴다
  - 이 폴더에는 `.venv`가 없다. 시험은 `/Users/seungchan/Workspace/MultilingualAgentRAG/.venv/bin/python -m unittest discover -s <폴더>`
  - 사용자는 영어를 읽지 못한다. 최종 평가용 질문은 프로젝트 밖에 있고 찾거나 열지 않는다
  - 커밋 제목은 50자 이하(훅). `git add -A`는 거부된다
- 뒤 단계에서 확인되는 것: 없음
- 한계: 없음
- 읽어야 할 결정: `decisions/common.md` 2026-10-22 "Claude 세션 두 개로 동시에" 줄과 "10-25까지의 범위를 새 도메인에 맞춰 다시 정한다" 줄. `STEPPER.md` 3단계 줄. `DECISIONS.md` 미정 목록에서 다룰 단계에 3단계가 든 줄. 질문 재료는 `research_notes/stage2_values_rare_earth/materials_check.md`(여러 문서 연결 12개, 표·수치·조건 6개)와 `research_notes/stage2_stem_select/step3/confirm.json`(한쪽 언어 사실)
