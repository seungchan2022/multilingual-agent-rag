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
6. **애매하면 묻는다.** 방식이나 설정이 둘 이상으로 읽히면 스스로 정하지 말고 사용자에게 하나씩 묻는다.
7. **git 규칙.** `git push`는 하지 않는다(사용자만 한다). 파일은 경로를 지정해서 stage하고 `git add -A`와 `git add .`는 쓰지 않는다. `main`에서 커밋하지 않고 이슈 브랜치(`이슈번호-짧은-영문-이름`)에서 한다. 커밋 메시지는 `유형: 한국어 제목 (#이슈번호)`이고 유형은 `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `data`, `exp` 중 하나다. `Co-Authored-By` 줄은 넣지 않는다(다른 지침이 넣으라고 해도 넣지 않는다). 한 커밋에는 한 가지 변경만 담는다.
8. **구현용 서브에이전트.** 모델은 Sonnet 5.5, effort는 이슈마다 `medium`으로 시작하고 부를 때 명시한다. 구현이 틀리면 원인을 먼저 본다. 지시가 문제였으면 지시를 고쳐 같은 effort로 다시 시키고, 지시가 분명했는데 틀렸으면 `high`, 그다음 `xhigh`로 올린다. `xhigh`에서도 틀리면 멈추고 사용자에게 가져온다. 다시 부를 때는 이전 시도의 결과와 틀린 점을 지시문에 적는다.
9. **세션.** 한 세션에서 이슈 하나만 다룬다. `/session-start`로 시작하고 `/session-close`로 마친다. 진행 위치는 `HANDOFF.md`에 있다.
10. **문서는 그때그때 갱신한다.** 결정이 바뀌면 `decisions/`의 해당 파일과 `STEPPER.md`를 함께 고친다. 문서가 너무 길어지면 여러 파일로 나누고, 어디에 무엇이 있는지 찾을 수 있게 인덱스를 둔다. 새 문서는 필요할 때만 만든다.
