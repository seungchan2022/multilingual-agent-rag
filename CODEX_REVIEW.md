# Codex 검토 기록: 5단계 첫째 이슈(최소판 지식 베이스), 이슈 #10

1차 검토: 2026-10-23, `gpt-6.1-sol`, `max`. 아래는 지적 원문과 처리. 이슈를 닫을 때 커밋한 뒤 지운다(`decisions/common.md` 2026-10-11).

## 1차 지적 원문

확인한 범위에서 **보통 1건, 낮음 1건**입니다. 심각한 문제는 찾지 못했습니다.

1. **문제**: 검색 실행 기록에 정해 둔 항목이 빠졌습니다. [compare_retrieval.py:57](/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal/compare_retrieval.py:57)의 `result_row()`와 `results.jsonl`에는 실제 검색 쿼리·검색 시간·문서 언어·원문 첫 줄과 끝 줄이 없습니다.

   **근거**: [decisions/stage4.md:31](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage4.md:31)의 ㉥은 5단계 검색 비교에도 ㉡의 항목을 남기도록 정했습니다. 현재 304개 기록은 ✔ 재계산에는 충분하지만, 합의한 실행 기록 형식은 충족하지 않습니다.

   **심각도**: 보통

   **고칠 방법**: 검색 호출에서 실제 쿼리와 소요 시간을 기록하고, 청크의 문서 언어·줄 범위도 저장하도록 프로그램과 시험을 보완하십시오. 기존 기록에서 복원할 수 없는 검색 시간은 `미확인`으로 남겨야 합니다.

2. **문제**: 제품 이름이 없는 표 행을 실제보다 하나 적게 기록했습니다. [decisions/stage5.md:11](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage5.md:11)의 ㉥은 193·194·201줄의 **3행**이라고 적었지만, **196줄도 해당하여 4행**입니다. [표 확인 reading.md:70](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage5_table_chunks/reading.md:70)도 네 줄을 열거하면서 “세 행”이라고 씁니다.

   **근거**: 원본 HTML에서 읽은 196줄의 조각은 `Dawon Medax`, 반응식, `LINAC`의 셋입니다. 현재 청크도 이 행의 Product 칸을 비웁니다. 프로그램과 설명의 대상 행 수가 다릅니다.

   **심각도**: 낮음

   **고칠 방법**: 결정 기록에 196줄을 포함한 정정 줄을 추가하고, 표 확인 문서의 “세 행”을 “네 행”으로 고치십시오.

**문제없다고 판단한 부분**: 304개 재채점·청크 통계·요약표가 일치하며, 정해진 선택 규칙대로 `128 + 제목 + bge-m3, k=8`이 골라집니다.  
고정 원본 20개 검증, 청크 네 묶음의 바이트 재현, 표 검사·변형 검사 결과를 확인했습니다.  
DB 확인과 표준 시험 전체 통과는 권한 제약으로 **미확인**입니다. 메모리로 대체한 청크·검색 시험은 76개 통과, 파일 시험 4개 제외입니다.
## 1차 지적 처리

| 지적 | 심각도 | 판정 | 처리 | 어디 |
|---|---|---|---|---|
| 1 검색 비교 기록에 정한 칸(검색 쿼리, 문서 언어, 원문 줄 범위, 검색 시간)이 빠짐 | 보통 | 동의. 구현 지시서가 `decisions/stage4.md` "실행 기록" 줄 ㉥을 옮기지 않았다. ✔ 판정과 고르기에는 영향이 없다 | 반영(사용자 승인 "진행해"). 프로그램에 칸을 더하고 비교를 다시 돌려, ✔·가져온 청크·거리가 첫 실행과 같은지 견준다 | `src/minimal/compare_retrieval.py`, `test_compare_retrieval.py`, `data/minimal/retrieval/results.jsonl` |
| 2 제품 이름이 없는 표 행을 3행으로 적음(실제 193·194·196·201줄의 4행) | 낮음 | 동의. 청크는 4행 모두 맞게 비웠고 기록의 수만 틀렸다 | 반영(사용자 승인). 결정 기록에 바로잡는 줄, 표 확인 문서 고침 | `decisions/stage5.md`, `research_notes/stage5_table_chunks/reading.md` |
