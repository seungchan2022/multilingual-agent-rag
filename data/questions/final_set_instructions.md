# 최종 평가셋 지시서

이 글은 사용자가 웹 임시 채팅의 AI에게 주는 글이다. 아래 "AI에게 주는 글" 부분을 그대로 붙여 넣고, 원문(마크다운 파일 28개)을 함께 올린다. 문서 목록은 "AI에게 주는 글" 안에 들어 있다. 규칙의 출처는 `EVALUATION.md`의 ①②③이고, 이 글과 어긋나면 `EVALUATION.md`가 맞다. 사용자가 진행하는 순서와 문제가 생겼을 때의 대처는 `final_set_guide.md`에 있다.

이 글에는 실제 질문이 없다. 형식을 보여 주는 예는 지어낸 것이다.

문서 목록은 2단계에서 채웠다. 남은 `<...>`는 요청할 때마다 그때 넣는 값이다.

---

## AI에게 주는 글

너는 검색 시스템을 평가할 질문의 후보를 만든다. 내가 올린 문서들만 근거로 쓴다. 네가 원래 알고 있는 지식으로 정답이나 근거를 만들지 마라. 후보는 내가 문서와 하나씩 대조해서 고르거나 버린다. 그러니 그럴듯한 것보다 문서로 확인되는 것이 중요하다. 확인되지 않으면 만들지 마라.

### 1. 내가 올린 것

- 문서 목록: 아래 표다. 문서마다 식별자(`doc_id`), 언어(`ko` 또는 `en`), 제목이 있다.
- 문서 본문: 마크다운 파일이다. 아래에서 "원문"은 이 마크다운 파일을 가리킨다.

| doc_id | 언어 | 제목 |
|---|---|---|
| `wiki-ko-jeonju` | ko | 전주시 |
| `wiki-en-jeonju` | en | Jeonju |
| `wiki-ko-cheongju` | ko | 청주시 |
| `wiki-en-cheongju` | en | Cheongju |
| `wiki-ko-chuncheon` | ko | 춘천시 |
| `wiki-en-chuncheon` | en | Chuncheon |
| `wiki-ko-cheonan` | ko | 천안시 |
| `wiki-en-cheonan` | en | Cheonan |
| `wiki-en-busan` | en | Busan |
| `wiki-en-jeju` | en | Jeju City |
| `wiki-en-andong` | en | Andong |
| `wiki-en-gangneung` | en | Gangneung |
| `wiki-ko-suwon` | ko | 수원시 |
| `wiki-ko-gyeongju` | ko | 경주시 |
| `wiki-ko-sejong` | ko | 세종특별자치시 |
| `wiki-ko-gwangju` | ko | 광주광역시 |
| `kto-ko-jeonju-hanok-village` | ko | 전북 전주 한옥마을 [슬로시티] |
| `kto-en-jeonju-hanok-village` | en | Jeonju Hanok Village [Slow City] (전북 전주 한옥마을 [슬로시티]) |
| `kto-ko-cheongju-cheongnamdae` | ko | 청남대 |
| `kto-en-cheongju-cheongnamdae` | en | Cheongnamdae Presidential Villa (청남대) |
| `kto-ko-chuncheon-samaksan-cable-car` | ko | 춘천 삼악산 호수케이블카 |
| `kto-en-chuncheon-samaksan-cable-car` | en | Chuncheon Samaksan Mountain Lake Cable Car (춘천 삼악산 호수케이블카) |
| `kto-ko-cheonan-samgeori-park` | ko | 천안삼거리공원 |
| `kto-en-cheonan-samgeori-park` | en | Cheonan Three-way Intersection Park (천안삼거리공원) |
| `kto-en-busan-haeundae-green-railway` | en | Haeundae Green Railway (Mipo-Songjeong) (해운대 그린레일웨이 (미포~송정 구간)) |
| `kto-en-jeju-ara-dong-trail` | en | Ara-dong History and Culture Trail (아라동 역사문화탐방로) |
| `portal-ko-suwon-population` | ko | 경기도 수원시_인구현황 |
| `portal-ko-jeonju-population` | ko | 전북특별자치도 전주시_인구현황 |

### 2. 만들 것

후보 60개를 아래 개수대로 만든다. 답 있는 질문 48개와 답 없는 질문 12개다.

답 있는 질문은 유형과 언어 조합마다 아래 개수를 만든다.

| 유형 | 한국어 질문·한국어 문서 | 영어 질문·영어 문서 | 한국어 질문·영어 문서 | 영어 질문·한국어 문서 | 합계 |
|---|---|---|---|---|---|
| `single_fact` | 2 | 2 | 2 | 2 | 8 |
| `table_numeric` | 2 | 2 | 2 | 2 | 8 |
| `multi_doc` | 4 | 4 | 4 | 4 | 16 |
| `paraphrase` | 4 | 4 | 4 | 4 | 16 |
| 합계 | 12 | 12 | 12 | 12 | 48 |

`table_numeric` 8개 가운데 답이 표에 있는 질문을 근거 문서 언어마다 2개 이상 만든다(한국어 문서의 표에서 2개 이상, 영어 문서의 표에서 2개 이상). 어떤 모양의 표인지는 가리지 않는다.

답 없는 질문(`no_answer`)은 한국어 질문 6개, 영어 질문 6개를 만든다.

특정 문서에 몰리지 않게 여러 문서에서 고르게 만든다.

### 3. 유형의 뜻

| 유형 | 뜻 |
|---|---|
| `single_fact` | 답이 문서의 한 구절에 있다 |
| `table_numeric` | 답이 표에 있거나, 문서에 값이 여러 개 있어서 조건(연도, 단위, 기준)에 맞는 것을 골라야 한다. 문장에 수치가 하나만 있는 것은 여기에 넣지 않는다 |
| `multi_doc` | 둘 이상의 문서나 구절을 합쳐야 답이 나온다. 비교, 집계, 여러 단계를 거치는 질문을 포함한다 |
| `paraphrase` | 답은 문서에 있지만 질문의 표현이 문서의 표현과 다르다. 문서에 나온 낱말을 그대로 쓰지 않고 다른 말로 묻는다 |
| `no_answer` | 문서에 답이 없고, 문서를 보지 않고 일반 지식으로도 답할 수 없다 |

한 질문은 유형 하나에만 속한다. 답 있는 질문이 두 유형의 뜻에 다 맞으면 아래 순서로 보아 먼저 맞는 유형으로 적는다.

1. 둘 이상의 문서나 구절을 합쳐야 답이 나오면 `multi_doc`이다. 표의 값이나 수치를 비교하는 질문도 여기다.
2. 답이 표에 있거나, 여러 값 가운데 조건에 맞는 것을 골라야 하면 `table_numeric`이다. 질문의 표현을 문서와 다르게 바꿨어도 여기다.
3. 나머지는 `single_fact` 또는 `paraphrase`다. 아래 기준으로 가른다.

`table_numeric`의 예(지어낸 것): 문서에 "관중 수는 2018년 3만 명, 2019년 4만 명, 2020년 1만 명이었다"가 있을 때 "2019년 관중 수는 몇 명인가"는 `table_numeric`이다. 문서에 "그 클럽은 1902년에 창단되었다"만 있을 때 "그 클럽은 언제 창단되었나"는 답이 수치이지만 값이 하나뿐이라 `single_fact`다.

`single_fact`와 `paraphrase`는 이렇게 가른다. 질문이 근거 구절의 핵심 낱말(사실을 나타내는 낱말)을 그대로 썼으면 `single_fact`이고, 다른 말로 바꿔 썼으면 `paraphrase`다. 질문 언어와 문서 언어가 다르면 질문을 문서의 언어로 옮겼을 때를 기준으로 본다. 이름(고유명사)은 판단에서 뺀다.

| 근거 구절 | 질문 | 유형 |
|---|---|---|
| Arsenal was founded in 1886. | 아스널은 언제 창단되었나 | `single_fact`. "창단"은 "founded"를 그대로 옮긴 말이다 |
| 같은 구절 | 아스널이 처음 생긴 해는 | `paraphrase`. "처음 생긴"은 "founded"를 바꿔 쓴 말이다 |

위 표는 가르는 방법을 보여 주는 지어낸 예다. `paraphrase` 후보에는 확인 메모에 문서의 어느 낱말을 어떤 말로 바꿨는지 적는다.

### 4. 언어의 규칙

- `question_language`는 질문을 쓴 언어다.
- `evidence_language`는 그 질문의 근거 구절이 있는 문서의 언어다.
- 한 질문의 근거 구절은 모두 한 가지 언어의 문서에서 나와야 한다. 문서는 여러 개여도 된다.
- 반대 언어의 문서에 같은 사실이 있으면 그 사실로 질문을 만들지 마라. 예를 들어 영어 문서의 사실로 질문을 만들려면, 한국어 문서 어디에도 그 사실이 없어야 한다. 만들기 전에 반대 언어 문서 전체에서 그 사실을 찾아봐라.
- 아래 두 영어 문서는 한국어 문서를 줄여 옮긴 것이다. 그 안의 사실은 모두 짝이 되는 한국어 문서에도 있다.
  - `kto-en-jeonju-hanok-village` (짝이 되는 한국어 문서: `kto-ko-jeonju-hanok-village`)
  - `kto-en-cheonan-samgeori-park` (짝이 되는 한국어 문서: `kto-ko-cheonan-samgeori-park`)
  - 이 두 문서의 구절은 `passage`에도 `rebuttal`에도 옮겨 적지 마라.
  - 이 두 문서도 바로 위 규칙의 "반대 언어 문서"에 들어간다. 한국어 문서의 사실로 질문을 만들기 전에 이 두 문서에서도 그 사실을 찾아봐라.
- 정답(`answer`)과 필수 사실(`fact`)은 질문과 같은 언어로 쓴다. 근거 구절(`passage`)은 원문의 언어 그대로 둔다.

### 5. 답 있는 질문의 규칙

- 정답은 근거 구절만 읽고 나와야 한다. 문맥, 조건, 단위까지 근거 구절에 있어야 한다.
- 정답이 하나로 정해지는 질문만 만든다. 읽는 사람에 따라 답이 달라질 수 있으면 만들지 마라.
- 근거로 쓸 값이 같은 문서의 다른 곳(맨 위의 요약 목록, 본문, 표)에 다른 값으로 적혀 있으면 그 값으로 질문을 만들지 마라. 예(지어낸 것): 맨 위의 요약 목록에는 면적이 512.3 km2, 본문에는 511.8 km2로 적혀 있다. 반올림하거나 버리거나 "약"을 붙여 적은 값과, 한쪽을 덜 자세하게 적은 값도 다른 값으로 본다(예(지어낸 것): 표에는 820.6 mm, 본문에는 821 mm 또는 "약 820 mm". 한 곳에는 "1972년 3월 1일", 다른 곳에는 "1972년"). 값이 같고 적는 방식만 다른 것(예: "15"와 "fifteen")과 같은 값을 다른 단위로 함께 적은 것(예: "16.2 (61.2)"의 괄호 안 화씨)은 다른 값이 아니다. 기준 날짜가 서로 다르게 적혀 있어 구분되는 값(예: 2019년 인구와 2024년 인구)은 서로 다른 사실이다. 이런 값을 쓰면 질문에 그 날짜를 넣고, 확인 메모에 다른 날짜의 값이 있다고 적어라.
- 표의 합계 줄이나 소계 줄이 그 아래(또는 위) 줄들을 더한 값과 맞지 않으면 그 합계·소계 값으로 질문을 만들지 마라. 더한 줄 가운데 문서에 한 번만 나오는 줄의 값은 써도 된다.
- 같은 도시의 반대 언어 문서가 같은 것을 다른 값으로 적었으면(예: 두 문서의 자매도시 목록이 서로 다르다) 그것으로 질문을 만들지 마라.
- 같은 언어의 다른 문서가 같은 것을 다른 값으로 적었어도 그것으로 질문을 만들지 마라. 문서는 모두 하나의 검색 대상에 함께 들어가므로, 다른 문서에 다른 값이 있으면 코퍼스 안에서 답이 둘이 된다. 예: `wiki-ko-suwon`의 행정 구역 표에는 장안구 인구가 날짜 없이 307,151명이고, `portal-ko-suwon-population`의 장안구 동들을 더하면 2021-05-31 기준 277,206명이다. 위의 규칙처럼 반올림·버림·어림·덜 자세하게 적은 값도 다른 값이고, 기준 날짜가 서로 다르게 적혀 있어 구분되는 값은 서로 다른 사실이다.
- `required_facts`에는 정답에 꼭 들어가야 하는 사실을 하나씩 적는다. 여러 개이면 모두 있어야 정답이다.
- 필수 사실마다 그 사실의 근거 구절을 `evidence`에 적는다. 같은 사실이 여러 곳에 있으면 여러 개를 적는다. 그중 어느 것이든 그 사실의 근거가 된다. 찾을 수 있는 것은 빠짐없이 적는다.
- 다른 필수 사실들에서 나오는 결론(예: "A가 B보다 많다")은 필수 사실로 적고 `evidence`를 `[]`로 둔다.
- `passage`는 원문에서 글자 그대로 옮긴다. 줄이거나 고치거나 번역하지 마라. 띄어쓰기와 문장 부호도 그대로 둔다.
- 답이 표에 있으면 `passage`에 표의 머리글 행과 해당 행을 원문 그대로 적는다. 구분선 행(`|---|---|`)은 적지 않는다.
- `location`에는 그 구절이 있는 절의 제목을 적는다.

### 6. 답 없는 질문의 규칙

- 문서에 답이 없는 것만으로는 안 된다. 문서를 보지 않는 사람이 일반 지식으로 답할 수 있는 질문은 만들지 마라.
- 쓸 수 있는 방법은 두 가지다. 전제가 틀린 질문(문서의 내용과 어긋나는 것을 사실인 것처럼 깔고 묻는다)과, 존재하지 않는 대상을 묻는 질문이다.
- 전제가 너무 뻔하게 틀린 질문은 만들지 마라. 문서의 주제 안에서 그럴듯하게 들려야 한다.
- `expected_refusal`에는 맞는 대답이 무엇인지 적는다. 예: "그런 것은 없다고 답한다."
- `no_answer_reason`에는 문서에서 무엇을 찾아봤고 왜 답이 없는지, 그리고 왜 일반 지식으로도 답할 수 없는지를 적는다.
- 문서에 전제를 반박하는 구절이 있으면 `rebuttal`에 원문 그대로 적는다. 없으면 `[]`로 둔다.

### 7. 내는 형식

YAML로 낸다. 코드 블록 하나에 전부 넣는다. `id`는 `c-001`부터 차례로 붙인다.

아래는 형식을 보여 주는 지어낸 예다. 내용을 따라 하지 말고 칸의 모양만 따른다.

```yaml
- id: c-001
  question: 축구와 농구 중 선발 인원이 더 많은 종목은 무엇인가
  question_language: ko
  evidence_language: en
  type: multi_doc
  answer: 축구가 더 많다. 축구는 11명, 농구는 5명이 선발로 뛴다
  required_facts:
    - fact: 축구의 선발은 11명이다
      evidence:
        - doc_id: en-football
          location: Players and equipment
          passage: "Each team consists of a maximum of eleven players"
    - fact: 농구의 선발은 5명이다
      evidence:
        - doc_id: en-basketball
          location: Rules
          passage: "Five players from each team may be on the court at one time"
    - fact: 축구가 농구보다 선발 인원이 많다
      evidence: []

- id: c-002
  question: 축구의 선발 인원은 몇 명인가
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 11명이다
  required_facts:
    - fact: 축구의 선발 인원은 11명이다
      evidence:
        - doc_id: ko-sports-table
          location: 종목별 비교 표
          passage: |
            | 종목 | 선발 인원 | 경기 시간 |
            | 축구 | 11 | 90분 |

- id: c-003
  question: 축구에서 선발 12번째 선수의 포지션 이름은 무엇인가
  question_language: ko
  evidence_language: null
  type: no_answer
  answer: null
  required_facts: []
  expected_refusal: 선발은 11명이라 12번째 선수는 없다고 답한다
  no_answer_reason: 문서 전체에서 선발 인원을 찾아봤고 모두 11명으로 적혀 있다. 12번째 선발 선수는 실제로도 없어서 일반 지식으로도 답할 수 없다
  rebuttal:
    - doc_id: en-football
      location: Players and equipment
      passage: "Each team consists of a maximum of eleven players"
```

### 8. YAML 뒤에 따로 적을 것

코드 블록 뒤에, 답 있는 후보마다 한 줄씩 확인 메모를 적는다. 내가 대조할 때 쓴다.

```
c-001: 반대 언어(한국어) 문서에서 찾아본 표현 "선발", "11명", "5명" → 같은 사실 없음
```

찾아봤는데 확신이 서지 않으면 "확신 없음"이라고 적는다. 숨기지 마라.

### 9. 내기 전에 스스로 확인할 것

- 개수가 2번의 표와 맞는가
- 모든 `passage`가 원문에 글자 그대로 있는가
- 한 질문의 근거가 한 가지 언어의 문서에만 있고, 반대 언어 문서에 같은 사실이 없는가
- `passage`와 `rebuttal`을 가져온 문서(`doc_id`)가 `kto-en-jeonju-hanok-village`나 `kto-en-cheonan-samgeori-park`가 아닌가
- 근거로 쓴 값이 같은 문서의 다른 곳, 같은 언어의 다른 문서, 같은 도시의 반대 언어 문서에 다른 값(반올림·버림·어림·덜 자세하게 적은 값 포함)으로 적혀 있지 않은가. 표의 합계·소계 값이면 더한 값과 맞는가
- 근거 구절만 읽고 정답이 나오는가
- 답 없는 질문이 일반 지식으로도 답할 수 없는가
- 유형이 3번의 뜻과 맞는가

개수를 채울 수 없는 칸이 있으면 억지로 채우지 말고, 어느 칸이 몇 개 모자라는지와 이유를 적는다.

---

## 나눠서 요청할 때

문서가 많아 한 번에 올릴 수 없으면 근거 문서의 언어별로 나눈다. 위 글의 2번 뒤에 아래 문단을 붙인다.

> 이번에는 `<ko 또는 en>` 문서만 올렸다. `evidence_language`가 `<ko 또는 en>`인 답 있는 질문 24개만 만든다. 반대 언어 문서에 같은 사실이 있는지는 네가 확인할 수 없으니 확인 메모에 "반대 언어 문서 확인 못 함"이라고 적는다. 그 확인은 내가 한다.

답 없는 질문 12개는 문서를 전부 올릴 수 있는 채팅에서 따로 요청하거나, 언어별 채팅에서 6개씩 요청한다. 뒤의 경우에는 `no_answer_reason`에 "올린 문서에서만 찾아봤다"고 적게 한다.

## 한 칸만 다시 요청할 때

> `<유형>`, 질문 언어 `<ko 또는 en>`, 근거 문서 언어 `<ko 또는 en>`인 후보를 `<개수>`개 더 만든다. 규칙은 같다. 아래 질문들과 같은 사실을 묻지 마라.
> `<이미 받은 그 칸의 후보 질문을 붙인다>`

## 겹치지 않게 할 때

개발용 질문과 연습 때 받은 질문을 붙이고, 위 글의 2번 뒤에 아래 문단을 붙인다.

> 아래 질문들은 이미 쓰고 있다. 같은 사실을 묻는 질문을 만들지 마라.
> `<개발용 질문과 연습 질문의 질문 문장만 붙인다>`
