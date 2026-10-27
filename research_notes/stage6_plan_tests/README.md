# 이슈 #14 1단계 고리의 원인 시험 (2026-10-27)

결과 숫자(190번 견주기)에는 쓰지 않은 짧은 시험이다. 판단과 결정의 근거로 썼다. 스크립트는 처음에 세션 임시 폴더(scratchpad)에서 돌렸고, 닫는 검토 전에 그대로 옮겼다. 스크립트 안의 경로는 돌릴 때의 절대 경로다.

| 폴더 | 무엇 | 쓴 곳 |
|---|---|---|
| `plan_temperature/` | 계획 쓰기의 온도(0 / 0.7)와 JSON 꼴 강제가 옮겨 쓰기를 깨뜨리는지(q01-ko 등). 출력은 화면에만 찍었고, 닫는 검토 1차 지적 2로 대화 기록(Claude Code 세션 transcript)에서 되살려 `out_test.txt`(JSON 꼴 강제 켬·끔, 0.7, 5번씩), `out_test_temp.txt`(온도 0 / 0.7, 10번씩), `out_test_four.txt`(온도 0으로 다섯 질문)에 저장했다 | `decisions/stage6.md` 2026-10-27 "계획 쓰기의 온도" 줄 ㉡, `decisions/judgments.md` 2026-10-27 `judge-en-v2` 190번 줄 |
| `judge_prompt/` | 판정 모델(gemma3:4b)에게 지시문을 바꿔 계획을 다시 판정시킴. `test_judge.py`·`out.jsonl`: q09-ko·q14-ko × 씨앗 5, 지금 판과 고친 판. `test_reason.py`·`out_reason.jsonl`: 계획 8개 × 지시문 4개 × 씨앗 1(정답 표시는 Claude가 계획을 질문과 대조해 붙임, 스크립트의 `EXPECT`) | `decisions/judgments.md` 2026-10-27 "네 번째 190번" 줄, `decisions/stage6.md` 2026-10-27 "저지먼트·리파이먼트를 뺀다" 줄 |
| `tool_probe/` | 생성 모델(qwen3:8b)에게 검색 도구를 주고 여러 차례 주고받게 함. 질문 5개(q03-en, q09-en, q13-en, q14-en, q12-ko) × 지시문 2개(자유롭게 / 계획대로 세 번), 씨앗 1, 온도 0. 검색 결과는 호출마다 위 4개만 돌려줌 | `decisions/stage6.md` 2026-10-27 "③의 검색어는 계획대로" 줄 ㉢, "③ 도구 호출 검색은 따로 붙이지 않고" 줄 |
