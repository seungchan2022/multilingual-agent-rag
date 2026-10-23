# Codex 검토 기록: 4단계(최소판 설계), 이슈 #8

1차 검토: 2026-10-23, `gpt-6.1-sol`, `max`. 아래는 지적 원문과 처리. 단계를 닫을 때 커밋한 뒤 지운다(`decisions/common.md` 2026-10-11).

## 1차 지적 원문

지적 **7개: 심각 2개·보통 3개·낮음 2개**입니다. 현재 기록만으로는 최소판 설계가 완료됐다고 보기 어렵습니다.

1. **문제**: 청크 크기와 표 보존 규칙을 동시에 지킬 수 없습니다. [stage4.md:12](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage4.md:12), 16·22줄.
   - **근거**: 세 후보 토크나이저에서 터븀 표의 머리글 두 줄만 **146토큰**, q10 근거 행까지 붙이면 **193토큰**입니다. 함께 두기로 한 ¹⁴⁴ᵐ¹Tb의 세 행과 머리글은 **314토큰**으로 256도 넘습니다. [lengths.py:21](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage4_chunk_lengths/lengths.py:21)는 첫 머리글만 세고 둘째 머리글은 데이터 행으로 셉니다. 본문에도 문장 하나가 156토큰인 사례가 있어 문장 경계만으로 128을 지킬 수 없습니다.
   - **심각도**: 심각
   - **고칠 방법**: 128·256 후보는 유지하면서 긴 머리글·동일 대상 행 묶음·긴 문장·문장 겹침이 한도와 충돌할 때의 대체 규칙을 정하십시오. 제목·반복 머리글·특수 토큰까지 포함한 완성 청크로 위 반례를 확인해야 합니다.

2. **문제**: 정답이 없는 청크도 검색 성공으로 집계됩니다. [stage4.md:10](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage4.md:10)의 줄 범위 판정, 17줄.
   - **근거**: q19의 근거인 [questions.json:1093](/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json:1093)은 478토큰짜리 문단 한 줄입니다. 첫 문장은 104토큰이고 정답 `17.7`이 없지만, 분할한 청크의 줄 번호는 여전히 159이므로 현재 규칙에서는 ✔입니다. 조합 선정과 “검색은 성공했는데 생성이 틀림”이라는 원인 분류가 함께 왜곡됩니다.
   - **심각도**: 심각
   - **고칠 방법**: 출처용 줄 번호와 함께 실제 포함한 문장·문자 구간을 기록하십시오. 근거도 답을 지지하는 구절과 구간으로 지정하고, 필요한 구절을 가져왔을 때 성공으로 세십시오. q19의 정답 없는 앞 조각은 실패해야 합니다.

3. **문제**: 벡터 검색의 거리 함수와 벡터 정규화가 미정입니다. [stage4.md:20](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage4.md:20).
   - **근거**: “정확한 검색”은 코사인·L2·내적 중 무엇으로 순위를 정하는지 규정하지 않습니다. 이들은 서로 다른 순위를 만들 수 있습니다. 조사 메모도 MiniLM에는 Normalize 모듈이 없다는 점을 짚었으나 결정에 반영되지 않았습니다. [pgvector 공식 문서](https://github.com/pgvector/pgvector#querying)에서도 거리 함수를 별도로 선택합니다.
   - **심각도**: 보통
   - **고칠 방법**: 비교 전에 거리 함수·벡터 정규화·정렬 방향을 고정하고 기록하십시오. 예를 들어 후보 모두 벡터를 정규화하고 코사인 거리 오름차순으로 검색하도록 명시할 수 있습니다.

4. **문제**: 동일한 최대 예산을 실제 검색량이 같은 것으로 설명합니다. [stage4.md:17](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage4.md:17), 29줄 ㉢.
   - **근거**: 청크는 128·256토큰 **이하**이고, 작은 정보 상자 묶음도 합치지 않습니다. 가령 두 크기에서 동일한 100토큰 청크들이 검색되면 k=8은 800토큰, k=4는 400토큰입니다. `128×8=256×4`만으로 “읽는 양과 오답 글의 양도 거의 같다”는 결론은 나오지 않습니다.
   - **심각도**: 보통
   - **고칠 방법**: k=4/8은 유지하고 설명을 “동일한 최대 예산”으로 고치십시오. 실행 기록에 공통 토크나이저로 센 실제 검색 토큰 합계와 생성 입력 길이를 추가하고, 실제 양까지 통제한 비교라는 해석은 피하십시오.

5. **문제**: 비김 규칙을 전부 적용해도 조합 하나가 정해지지 않을 수 있습니다. [stage4.md:19](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage4.md:19).
   - **근거**: `gte / 128 / 제목 없음`과 `MiniLM / 128 / 제목 없음`이 전체 ✔와 교차 언어 ✔까지 같으면 네 기준이 모두 같습니다. 둘 다 과제 권장 모델이므로 두 번째 기준도 구분하지 못합니다.
   - **심각도**: 보통
   - **고칠 방법**: 기존 순서를 유지하고, 끝까지 같을 때 적용할 고정된 모델 ID 순서를 결과를 보기 전에 덧붙이십시오.

6. **문제**: 답 언어 시험의 응답 시간 중앙값이 잘못 계산됐습니다. [check_language.py:110](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage4_answer_language/check_language.py:110), `summary_A/B/C.json`, [judgments.md:154](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/judgments.md:154).
   - **근거**: 38개에서는 가운데 두 값의 평균을 구해야 하는데 20번째 값만 사용했습니다. 원본으로 계산한 중앙값은 A **5.615초**, B **5.80초**, C **4.965초**입니다. 기록의 5.67·5.94·5.30초와 다릅니다.
   - **심각도**: 낮음
   - **고칠 방법**: `statistics.median()`을 사용하고 저장된 결과만 재집계해 요약과 판단 기록을 맞추십시오. 언어 통과 결과에는 영향이 없습니다.

7. **문제**: KURE 비교 수치의 대상 범위가 잘못 옮겨졌고, 측정 차이를 반복 실행의 흔들림으로 단정합니다. [references.md:18](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/references.md:18), [korean_benchmarks.md:12](</Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/한영 교차 검색 임베딩 후보/korean_benchmarks.md:12>), `stage4.md:15`.
   - **근거**: 메모의 0.004~0.014는 여러 한국어 튜닝 모델의 차이 범위입니다. 같은 메모에서 KURE-v1 하나의 차이는 **0.7616−0.7509=0.0107**입니다. 또한 다른 주체가 낸 점수 차이만으로 동일 조건 반복 실행의 변동 폭이 약 0.01이라고 입증할 수는 없습니다.
   - **심각도**: 낮음
   - **고칠 방법**: KURE-v1 수치를 0.0107로 맞추고, “서로 다른 측정에서 차이가 관찰됐으며 반복 실행의 변동 폭은 미확인”으로 표현을 낮추십시오. 후보 선택 자체를 바꿀 필요는 없습니다.

**문제없다고 판단한 부분**: 질문 38개의 구성·근거 문자열, 기존 시험 7개, 메모리 재생성의 바이트 일치를 확인했습니다.  
언어 결과 v1 19/38·A 38/38·B 22/38·C 38/38은 원본과 일치합니다.  
실제 최소판 실행과 외부 벤치마크 원문 전체 재대조는 미확인입니다. 파일 수정과 최종 평가용 질문 열람은 하지 않았습니다.
## 1차 지적 처리

| 지적 | 심각도 | 처리 | 어디 |
|---|---|---|---|
| 1 청크 크기와 표 보존 규칙 충돌 | 심각 | 반영. 가장 작은 단위(머리글 전부 + 행 하나, 문장 하나, 정보 상자 줄 하나)는 자르지 않고 한도를 넘긴 채 둔다. 첫 칸이 같은 행 묶기와 문장 겹침은 한도 안에 들 때만. 넘는 청크 수를 기록. MiniLM의 한계를 적음 | `decisions/stage4.md` 2026-10-23 "Codex 1차 검토" 줄 ㉠~㉣, ㉨ |
| 2 정답 없는 조각도 ✔ | 심각 | 반영. ✔ = 줄 범위에 근거 줄 + 청크 글에 근거 값 글자(`value_text`). 질문 파일에 `value_text` 추가, 시험 추가 | 같은 줄 ㉤, `src/minimal/build_questions.py`, `test_build_questions.py`, `data/minimal/questions.json` |
| 3 거리 함수·정규화 미정 | 보통 | 반영. L2 정규화 + 코사인 거리(`<=>`) 오름차순 | 같은 줄 ㉥ |
| 4 같은 예산을 같은 양으로 설명 | 보통 | 반영. "같은 명목 예산"으로 낮추고 실제 토큰 합과 생성 입력 길이를 실행 기록에 더함 | 같은 줄 ㉦ |
| 5 비김 규칙이 끝까지 안 갈릴 수 있음 | 보통 | 반영. 5번(모델 순서 gte → MiniLM → bge-m3)을 더함 | 같은 줄 ㉧ |
| 6 시간 중앙값 계산 잘못 | 낮음 | 반영. `statistics.median`으로 고치고 저장된 결과로 다시 셈(v1 5.765, A 5.615, B 5.8, C 4.965초) | `research_notes/stage4_answer_language/`, `decisions/judgments.md` 두 줄 |
| 7 KURE 수치·표현 | 낮음 | 반영. KURE-v1 0.7616 − 0.7509 = 0.0107, 반복 측정 흔들림은 미확인으로 낮춤 | `decisions/references.md` S12 (마), `decisions/stage4.md` 임베딩 후보 줄 ㉢ |
