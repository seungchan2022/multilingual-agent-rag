# 답 쓰기 판 견주기

- base: `data/agent/plan_search/runs.jsonl` (base_kind: 처음 계획 10줄, 최종 180줄)
- new: `data/agent/answer_cite/runs_v1.jsonl`
- 짝지은 실행: 190쌍

## 두 쪽의 수

| 항목 | base | new |
| --- | --- | --- |
| 근거를 찾음 | 175/190 | 175/190 |
| 맞음 | 167/190 | 163/190 |
| 근거를 찾고도 틀림 | 8/175 | 12/175 |
| 답 언어가 질문과 같음 | 188/190 | 188/190 |
| 끊김 | 2/190 | 0/190 |
| 생각 과정에 숫자 계산을 씀 | 82/190 | 80/190 |

## 틀림 → 맞음 (5개)

- q05-en 씨앗2: base `0.00576 kg` / new `0.513 kg`
- q08-en 씨앗2: base `0.00092175 kg` / new `0.3687 kg`
- q01-en 씨앗3: base `0.000003144 kg` / new `0.3144 kg`
- q02-en 씨앗3: base `0.006543 kg` / new `0.59046 kg`
- q03-en 씨앗4: base `` / new `0.26832 kg`

## 맞음 → 틀림 (9개)

- q09-en 씨앗1: base `0.544 kg` / new `0.414 kg`
- q07-en 씨앗2: base `0.4512 kg` / new `0.005688 kg`
- q09-en 씨앗2: base `0.544 kg` / new `The mass of the cuboid is 0.0071 kg.`
- q06-en 씨앗3: base `0.406 kg` / new `0.000010155 kg`
- q09-en 씨앗3: base `0.544 kg` / new `The mass of the rectangular cuboid of erbium is 0.0018 kg.`
- q01-en 씨앗5: base `0.3144` / new `0.003144 kg`
- q05-en 씨앗5: base `0.513 kg` / new `The mass of the rectangular cuboid is 0.00000128 kg.`
- q06-en 씨앗5: base `0.406 kg` / new `0.0006773 kg`
- q09-en 씨앗5: base `0.544 kg` / new `0.414 kg`

## new의 공통 검사

- 꼴 오류: 0개
- 없음
- 근거를 찾은 실행 가운데 근거 칸이 근거 청크를 가리킴: 169/175
- cites_evidence가 false인 실행: 6개
- q09-en 씨앗1, q18-ko 씨앗1, q09-en 씨앗2, q09-en 씨앗3, q09-en 씨앗4, q09-en 씨앗5
- wrong_attached 합: 10 (10개 실행)
- q02-en 씨앗1: 1
- q18-ko 씨앗1: 1
- q02-en 씨앗2: 1
- q19-ko 씨앗2: 1
- q02-en 씨앗3: 1
- q19-ko 씨앗3: 1
- q02-en 씨앗4: 1
- q04-en 씨앗4: 1
- q09-en 씨앗4: 1
- q02-en 씨앗5: 1
- no_number_facts 합: 32
- facts_without_chunks(청크 번호가 빈 사실) 합: 22 (21개 실행)
- q01-en 씨앗1: 2
- q02-en 씨앗1: 1
- q05-en 씨앗1: 1
- q04-ko 씨앗2: 1
- q04-en 씨앗2: 1
- q05-ko 씨앗2: 1
- q07-ko 씨앗2: 1
- q07-en 씨앗2: 1
- q08-en 씨앗2: 1
- q01-ko 씨앗3: 1
- q05-ko 씨앗3: 1
- q07-ko 씨앗3: 1
- q08-ko 씨앗3: 1
- q05-en 씨앗4: 1
- q01-ko 씨앗5: 1
- q01-en 씨앗5: 1
- q02-en 씨앗5: 1
- q04-en 씨앗5: 1
- q05-ko 씨앗5: 1
- q07-ko 씨앗5: 1
- q07-en 씨앗5: 1
- citation_missing인 실행: 0개
- 없음
- 목록에 없는 청크 번호(invalid_chunks)가 있는 실행: 0개
- 없음
