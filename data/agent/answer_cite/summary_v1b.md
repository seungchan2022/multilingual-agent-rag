# 답 쓰기 판 견주기

- base: `data/agent/plan_search/runs.jsonl` (base_kind: 처음 계획 10줄, 최종 180줄)
- new: `data/agent/answer_cite/runs_v1b.jsonl`
- 짝지은 실행: 190쌍

## 두 쪽의 수

| 항목 | base | new |
| --- | --- | --- |
| 근거를 찾음 | 175/190 | 175/190 |
| 맞음 | 167/190 | 175/190 |
| 근거를 찾고도 틀림 | 8/175 | 0/175 |
| 답 언어가 질문과 같음 | 188/190 | 187/190 |
| 끊김 | 2/190 | 0/190 |
| 생각 과정에 숫자 계산을 씀 | 82/190 | 90/190 |

## 틀림 → 맞음 (8개)

- q01-en 씨앗2: base `` / new `0.31476 kg`
- q05-en 씨앗2: base `0.00576 kg` / new `0.513 kg`
- q08-en 씨앗2: base `0.00092175 kg` / new `0.3687 kg`
- q01-en 씨앗3: base `0.000003144 kg` / new `0.3144 kg`
- q02-en 씨앗3: base `0.006543 kg` / new `0.59046 kg`
- q03-en 씨앗4: base `` / new `0.268 kg`
- q02-en 씨앗5: base `0.00692 kg` / new `0.59046 kg`
- q08-en 씨앗5: base `0.0092175 kg` / new `0.3687 kg`

## 맞음 → 틀림 (0개)

- 없음

## new의 공통 검사

- 꼴 오류: 0개
- 없음
- 근거를 찾은 실행 가운데 근거 칸이 근거 청크를 가리킴: 170/175
- cites_evidence가 false인 실행: 5개
- q19-ko 씨앗1, q19-ko 씨앗2, q19-ko 씨앗3, q19-ko 씨앗4, q19-ko 씨앗5
- wrong_attached 합: 24 (23개 실행)
- q01-ko 씨앗1: 1
- q02-en 씨앗1: 1
- q04-en 씨앗1: 1
- q05-en 씨앗1: 1
- q12-ko 씨앗1: 1
- q19-ko 씨앗1: 1
- q02-en 씨앗2: 1
- q05-en 씨앗2: 1
- q12-ko 씨앗2: 1
- q19-ko 씨앗2: 1
- q02-en 씨앗3: 1
- q05-en 씨앗3: 1
- q19-ko 씨앗3: 1
- q01-ko 씨앗4: 1
- q02-en 씨앗4: 1
- q04-en 씨앗4: 1
- q05-en 씨앗4: 1
- q19-ko 씨앗4: 1
- q02-en 씨앗5: 1
- q04-en 씨앗5: 1
- q05-en 씨앗5: 1
- q12-ko 씨앗5: 2
- q19-ko 씨앗5: 1
- no_number_facts 합: 6
- facts_without_chunks(청크 번호가 빈 사실) 합: 6 (6개 실행)
- q02-en 씨앗1: 1
- q04-en 씨앗2: 1
- q02-en 씨앗3: 1
- q02-en 씨앗4: 1
- q02-en 씨앗5: 1
- q09-en 씨앗5: 1
- citation_missing인 실행: 0개
- 없음
- 목록에 없는 청크 번호(invalid_chunks)가 있는 실행: 0개
- 없음
