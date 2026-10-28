# Codex 검토 기록

## 이슈 #15 설계 검토 1차 (2026-10-28, 닫을 때의 1차·2차와 따로 셈)

명령: `.codex/review-prompt.md` + "이번 검토"(설계 검토 1차, 볼 것: `decisions/stage6.md` 47~53행, `decisions/judgments.md` 192행, 확대 페이지 `history/stage6/15-answer-synthesis.html`, 따르는 문서, `src/minimal/generate.py`·`scoring.py`, `src/agent/graph.py`, `data/agent/plan_search/runs.jsonl`), `codex exec -m gpt-6.1-sol -c model_reasoning_effort="max" --sandbox read-only`, 11:25~11:36

### 지적 원문

심각 1건, 보통 5건, 낮음 1건입니다.

1. **문제**: 판 0에서 재사용할 입력이 현재 시스템의 입력과 다릅니다. [decisions/stage6.md:52](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage6.md:52)
   - **근거**: 현재 시스템은 44행 결정대로 **처음 계획**으로 검색합니다. 그런데 52행은 고친 계획의 `search.merged`와 `answer`를 지정합니다. 원본 기록 17·55·93·131·169행의 q09-ko는 처음 계획에서 청크 12개, 고친 계획에서 13개이며 참고 글도 다릅니다. 총 정답 수가 같아도 현재 시스템에 인용만 더한 비교가 되지 않습니다.
   - **심각도**: 심각
   - **고칠 방법**: `first_plan_search`·`first_plan_answer`가 있는 실행은 그 둘을, 없는 실행은 `search`·`answer`를 판 0으로 선택하십시오. 이 선택을 청크·참고 글·`hit_ranks`·비교할 답에 일관되게 적용하고 190건의 입력 일치를 확인하십시오.

2. **문제**: 인용 성공 기준이 사실별 인용의 정확성과 구분되지 않습니다. [decisions/stage6.md:51](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage6.md:51)
   - **근거**: 기준은 근거 칸이 `hit_ranks`를 가리키는 실행 수입니다. q08-en의 `chunks`에 청크 번호 1~9를 전부 넣어도 정답 근거인 2번을 포함합니다. 이 검사만으로는 사실마다 출처를 정확히 연결했는지 알 수 없습니다. 숫자 대조도 기록용이므로 이 빈틈을 막지 않습니다.
   - **심각도**: 보통
   - **고칠 방법**: 이 수치를 ‘정답 근거 청크 포함 수’로 명명하고, 사실별 잘못된 추가 인용·인용 누락을 별도로 기록하는 방법을 실행 전에 정하십시오. 잘못된 연결의 교정은 정한 대로 ⑥·⑨에 남겨도 됩니다.

3. **문제**: 판 2와 후속 판에서 인용·꼴·언어 검사를 계속한다는 측정 절차가 빠졌습니다. [decisions/stage6.md:51](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage6.md:51)
   - **근거**: ㉡의 판 2 기준에는 정답으로 바뀐 수·오답으로 바뀐 수·숫자 계산 여부만 있습니다. 계산 지시로 정답은 늘지만 인용이 비거나 잘못 연결되는 경우를 어떻게 처리할지 없습니다. 두 판의 스키마가 같아도 이런 내용상의 퇴행은 가능합니다.
   - **심각도**: 보통
   - **고칠 방법**: 판 1의 공통 검사를 판 2·후속 판에서도 수행하고, 퇴행하면 원인을 분석한다고 명시하십시오. 판단 기록 192행에서 약속한 끊김 수도 별도로 계속 세십시오.

4. **문제**: 빈 `citations`를 거절로 세는 규칙이 평가 정의와 충돌합니다. [decisions/stage6.md:53](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/stage6.md:53)
   - **근거**: ㉢은 “근거 칸이 빈 답은 코드가 거절로 셀 수 있다”고 합니다. 하지만 `answer: "0.3687 kg", citations: []`는 정한 구조를 만족하면서도 거절이 아닙니다. 실제 채점 함수로 확인하면 q08-en에서는 정답입니다. [EVALUATION.md:12](/Users/seungchan/Workspace/MultilingualAgentRAG/EVALUATION.md:12)는 답하지 못한다는 말이 있고 물은 답을 내놓지 않아야 거절로 정의합니다.
   - **심각도**: 보통
   - **고칠 방법**: 빈 인용 여부와 거절 여부를 분리하십시오. 숫자로 답하고 인용만 비운 경우는 ‘인용 누락’으로 기록하고, 거절은 `answer` 원문을 평가 정의에 따라 판정하십시오.

5. **문제**: 대표 출력 예가 승인된 출력 구조를 어깁니다. [15-answer-synthesis.html:302](/Users/seungchan/Workspace/MultilingualAgentRAG/history/stage6/15-answer-synthesis.html:302)
   - **근거**: 302행의 `reason`에는 금지한 `[2]`가 있고, 304행은 `citations: [2]`입니다. 결정 47행은 `reason`의 번호를 금지하고 `citations`를 사실별 객체 목록으로 정했습니다. 바로 아래 306행 설명과도 충돌합니다.
   - **심각도**: 보통
   - **고칠 방법**: 예와 한국어 뜻의 `reason`에서 `[2]`를 제거하고, 근거 칸을 `citations: [{"fact": "Density of lanthanum at 20 °C is 6.145 g/cm³", "chunks": [2]}]`로 맞추십시오.

6. **문제**: 생각 모드 전환 설명에 이전 정책이 남았습니다. [15-answer-synthesis.html:331](/Users/seungchan/Workspace/MultilingualAgentRAG/history/stage6/15-answer-synthesis.html:331), [DECISIONS.md:97](/Users/seungchan/Workspace/MultilingualAgentRAG/DECISIONS.md:97)
   - **근거**: HTML 331·344행과 미정 목록은 “지시문으로 되지 않으면 켠다”고 합니다. 최신 결정 51행은 다른 고침부터 찾아 새 판으로 재고, 다른 고침을 찾지 못했을 때만 시간과 함께 사용자에게 묻도록 앞 결정을 명시적으로 좁혔습니다.
   - **심각도**: 보통
   - **고칠 방법**: 세 위치를 최신 결정에 맞춰, 다른 수정부터 시험하고 생각 모드는 마지막에 사용자에게 묻는다고 고치십시오.

7. **문제**: 확정된 검색 계획 제외가 흐름에는 미정으로 남았습니다. [15-answer-synthesis.html:239](/Users/seungchan/Workspace/MultilingualAgentRAG/history/stage6/15-answer-synthesis.html:239)
   - **근거**: 바뀐 흐름에 `질문 + 청크 (+ 검색 계획?)`이라고 적혀 있습니다. 결정 48행과 같은 페이지 301·343행은 넘기지 않는다고 확정했습니다.
   - **심각도**: 낮음
   - **고칠 방법**: `(+ 검색 계획?)`을 삭제하십시오.

**문제없다고 판단한 부분**  
원본 190줄에서 근거 발견 175번·정답 167번·실패 8번(끊김 2번 포함), 질량 질문 90번 중 부피 숫자를 쓴 82번의 정답 여부는 기록과 일치합니다.  
새 구현과 새 지시문의 실행 효과는 미확인입니다. 파일은 수정하지 않았고 최종 평가용 질문은 찾거나 열지 않았습니다.
### 처리

| 지적 | 원문 대조 | 처리 |
|---|---|---|
| 1 판 0의 입력 (심각) | 맞음. ⑧ 기록에서 처음 계획 기록이 따로 있는 실행 10번, q09-ko 5번은 청크 12개 대 13개로 참고 글이 다름. 판 0을 다시 센 값은 175·167·8·188·82와 같음 | 고침: `decisions/stage6.md` 2026-10-28 "Codex 설계 검토 1차 지적 1·4" 줄 ① |
| 2 인용 성공 기준 (보통) | 맞음. 청크 번호를 모두 적어도 "근거 청크를 가리킴"을 통과함 | 기준을 바꾸는 일이라 사용자에게 물음(3과 함께) |
| 3 판 2의 공통 검사 (보통) | 맞음. 판 2 기준에 근거 칸·꼴·언어·끊김 검사가 없음 | 기준을 바꾸는 일이라 사용자에게 물음(2와 함께) |
| 4 빈 근거 칸과 거절 (보통) | 맞음. `EVALUATION.md` 12행의 거절 정의와 어긋남 | 고침: 같은 줄 ② |
| 5 확대 페이지의 예 (보통) | 맞음. 예의 `reason`에 `[2]`, 근거 칸이 번호 목록 | 고침: 예를 결정한 꼴로 |
| 6 생각 모드 문구 (보통) | 맞음. 확대 페이지 두 곳과 `DECISIONS.md` 미정 목록에 앞 정책 | 고침: 최신 결정(다른 고침 먼저, 생각 모드는 마지막에 물음)으로 |
| 7 흐름 줄의 "(+ 검색 계획?)" (낮음) | 맞음 | 고침: 지움 |
