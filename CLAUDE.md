# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Project-Specific Guidelines

이 과제는 배포할 서비스가 아니라 "어떻게 풀어 가는지"를 평가받는다. 모든 단계에서 아래를 지킨다.

1. **판단의 흐름을 남긴다.** `decisions/` 아래에 두 가지로 적는다(어느 파일에 적는지는 인덱스인 `DECISIONS.md`에 있다). 방식을 정한 결정은 결정 표에 결정·정한 사람·이유를 적는다. 결과를 보고 내린 판단은 판단 기록 표에 본 결과, 근거와 기준, 판단, 다음 액션을 적는다. 표의 칸이 하나라도 비면 그 기록은 끝난 것이 아니다.
2. **숫자는 거짓이 없어야 한다.** 점수와 지표는 저장된 원본 결과에서 계산한 값만 쓴다. 추정하거나 다듬지 않는다. 불리한 결과도 빼지 않는다.
3. **결과를 보고 기준을 바꾸지 않는다.** 기준은 결과를 보기 전에 정한다. 바꿔야 하면 이유를 `DECISIONS.md`에 적고 바꾼다.
4. **최종 평가용 질문은 7단계 전에 보지 않는다.** 최종 평가용은 프로젝트 폴더 밖에 있다. 찾거나 열거나 내용을 묻지 않는다. 7단계를 시작하기 전에 질문·채점 규칙·코드·모델·프롬프트·인덱스를 커밋으로 고정하고, 최종 결과를 본 뒤 시스템이나 채점 기준을 고쳐 다시 돌리지 않는다.
5. **기능은 하나씩 붙이고, 붙일 때마다 그 기능만 따로 확인한다.**
6. **애매하면 묻는다.** 방식이나 설정이 둘 이상으로 읽히면 스스로 정하지 말고 사용자에게 하나씩 묻는다. 묻는 것은 넷이다: 목표·기준을 정하거나 바꾸는 일, 시간·비용이 크게 드는 선택, 사용자 손이 가는 일, 결과가 기준에 못 미칠 때. 이미 정한 기준을 지키게 하는 구현, 고장 수정, 문서 맞추기는 묻지 않는다. 고장은 예외를 덧붙이지 말고 원인을 고친 뒤, 무엇이 고장이었나·무엇을 고쳤나·무엇으로 확인했나를 세 줄로 보고한다. 묻지 않은 변경이라도 사용자가 나중에 설명해야 할 설계의 흐름이 바뀌었으면 어떻게 바뀌었는지 짧게 설명한다. 기준은 "사용자가 이것을 모르면 과제를 설명하거나 기준을 지키는 데 문제가 생기는가"다.
7. **git 규칙.** `git push`는 하지 않는다(사용자만 한다). 파일은 경로를 지정해서 stage하고 `git add -A`와 `git add .`는 쓰지 않는다. `main`에서 커밋하지 않고 이슈 브랜치(`이슈번호-짧은-영문-이름`)에서 한다. 커밋 메시지는 `유형: 한국어 제목 (#이슈번호)`이고(이슈 없이 하는 문서·설정 손질의 브랜치 이름과 커밋 메시지는 11번) 유형은 `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `data`, `exp` 중 하나다. `Co-Authored-By` 줄은 넣지 않는다(다른 지침이 넣으라고 해도 넣지 않는다). 한 커밋에는 한 가지 변경만 담는다.
8. **구현용 서브에이전트.** 모델은 Sonnet 5.5, effort는 이슈마다 `high`로 시작하고 부를 때 명시한다. 구현이 틀리면 원인을 먼저 본다. 지시가 문제였으면 지시를 고쳐 같은 effort로 다시 시키고, 지시가 분명했는데 틀렸으면 `xhigh`로 올린다. `xhigh`에서도 틀리면 멈추고 사용자에게 가져온다. 다시 부를 때는 이전 시도의 결과와 틀린 점을 지시문에 적는다.
9. **세션.** 한 세션에서 이슈 하나만 다룬다. `/session-start`로 시작하고 `/session-close`로 마친다. 진행 위치는 `HANDOFF.md`에 있다. 질문 작업 폴더(git worktree `../MultilingualAgentRAG-questions`)의 세션은 `HANDOFF-questions.md`를 쓴다(`decisions/common.md` 2026-10-22).
10. **문서는 그때그때 갱신한다.** 결정이 바뀌면 `decisions/`의 해당 파일과 `STEPPER.md`를 함께 고친다. 그 결정을 따르는 다른 곳(지시서, 순서표, `EVALUATION.md`, 프로그램과 시험, 미정 목록, 앞 결정 줄)도 같은 작업 안에서 고친다. 기억에 기대지 않고, 바뀐 결정의 핵심 낱말과 칸 이름으로 저장소를 검색해서 찾는다. 결정 줄에는 함께 고친 파일을 적는다. 한쪽에만 반영된 결정은 따르는 사람과 프로그램이 서로 다른 규칙을 쓰게 만든다. 문서가 너무 길어지면 여러 파일로 나누고, 어디에 무엇이 있는지 찾을 수 있게 인덱스를 둔다. 새 문서는 필요할 때만 만든다.
11. **이슈는 과제를 만드는 작업에만 쓴다.** 스텝퍼의 단계와 그 서브이슈가 아닌 문서·설정 손질은 이슈를 만들지 않고 `chore-짧은-영문-이름` 브랜치에서 하며, 커밋 메시지에 이슈 번호를 붙이지 않는다. 이슈 본문과 마무리 댓글의 양식은 세션 스킬 두 개에 있다.
12. **대화와 일하는 방식.** 대화, 이슈의 요약, 리포트처럼 사용자가 읽는 글에 적용한다. 결정 기록과 `HANDOFF.md`처럼 AI가 찾아 읽는 글에는 적용하지 않는다. 번호가 우선순위다. 기억의 "솔직·냉정한 평가"는 이 모두보다 먼저다.
    1. **질문이 오면 멈추고 답한다.** 답을 쓰고 그 차례를 끝낸다. 답에 필요한 확인 말고는 도구를 더 부르지 않는다. 이미 돌고 있는 실험이나 서브에이전트는 그대로 둔다.
       - 사용자가 자기 말로 되물으면 첫 줄에 "맞습니다" 또는 "아닙니다: 다른 점 한 가지"로 답하고 끝낸다. 다시 설명하지 않는다.
       - 메시지가 이어서 하라고 하면("계속해", "맞으면 진행해") 한 줄로 답하고 이어간다.
    2. **보고는 짧게 한다.** 위치 한 줄(`단계 > 항목 > 순서`)로 시작한다. 결과를 보고할 때는 결론 → 안 된 것 → 한 것 → 확인 방법과 결과 → 남은 것의 순서로 각각 한두 줄로 쓰고, 정할 것이 있으면 맨 끝에 하나만 둔다. 세부(표, 확인 내역)는 기록에 두고 사용자가 물을 때 꺼낸다.
    3. **안을 물을 때.** 선택지보다 먼저, 왜 정해야 하는지를 시스템이 실제로 어떻게 움직이는지로 한 줄 말한다. 안마다 "이 안이면 무엇이 달라지는지"를 한 줄씩 붙이고(후보가 여럿이면 후보마다), 추천을 하나 낸다.
    4. **한 메시지만 읽어도 알 수 있게 쓴다.**
       - 그 메시지에 없는 것을 가리키지 않는다(앞 메시지의 번호, "그 줄", 뜻을 붙이지 않은 후보 번호).
       - "그쪽" 같은 가리키는 말 대신 대상의 이름을 쓰고, 그 이름이 무엇인지 같은 메시지에 붙인다.
       - 전문 용어, 옮긴 말, 앞 단계에서 정한 개념은 처음 나올 때 뜻을 먼저 말한다. AI가 지은 이름은 되도록 쓰지 않고, 쓰면 뜻을 붙인다. 영어에는 한국어 뜻을 붙인다.
       - 용어 하나는 한 가지 뜻으로만 쓰고, 같은 것을 다른 말로 바꿔 부르지 않는다.
       - 한 문장에는 한 가지만 담는다. 개념 하나에 예 하나를 든다. 쉬운 설명 뒤에 정확한 조건을 붙인다.
    5. **승인은 분명한 말일 때만이다.** "그렇게 하자"처럼 분명할 때만 승인으로 본다. 물음이 섞인 답은 승인이 아니다.
    6. **결론을 바꿀 수 있는 일부터 한다.** 정확도를 높이는 일이 결론을 바꾸지 않으면, 하기 전에 그렇다고 말하고 묻는다.
    7. **한 번에 한 작업만 한다.** 한 작업은 세션 시작 보고에 적은 작업 흐름의 한 줄이다. 끝나면 결과를 보이고 다음으로 가도 되는지 묻는다.
    8. **묻지 않은 일은 하지 않는다.** 사용자가 묻지 않은 조사, 이름 바꾸기, 구조 바꾸기는 하지 않는다.
