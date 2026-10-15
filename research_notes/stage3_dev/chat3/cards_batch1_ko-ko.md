# 대조 카드: batch1_ko-ko.yaml

이 파일은 후보마다 카드 하나로, 순서표(data/questions/final_set_guide.md)의 "대조할 것"을 따라 카드마다 칸을 채운다. 확인한 칸은 [ ]를 [x]로 바꾼다. 하지 않은 칸은 그대로 둔다. 판정은 채택·수정·폐기 가운데 하나만 남긴다. 애매한 것은 메모에 적는다. 근거 구절이 원문에 글자 그대로 있는지, 개수·형식, `opposite_check`(반대 언어 찾기 기록)가 원문과 맞는지는 후보 검사가 이미 봤다. 카드의 이름표는 후보 YAML 칸 이름을 백틱으로 적고 괄호에 한국어 뜻을 붙인다(예: `passage`(근거 구절)). 칸 뜻은 순서표(data/questions/final_set_guide.md)의 "후보 YAML 칸의 뜻"에 있다.

---

## c-001 · `type`(유형): single_fact(단일 사실) · 도시 묶음: 두 언어 도시(춘천시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다.

**후보**
- `question`(질문): 춘천경공업단지가 조성되기 시작한 연도는 언제인가?
- `answer`(정답): 1969년
- `required_facts`(꼭 필요한 사실): `fact`(사실) 1 "춘천경공업단지는 1969년부터 조성되었다"
- `passage`(근거 구절): "1969년부터 춘천경공업단지가 조성되었으며, 73년 5월 공업장려지구로 지정되었다."
- `doc_id`(문서): [wiki-ko-chuncheon.md 218줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L218) · `location`(위치): 경제

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절 한 줄만 받은 사람이 `question`(질문)에 "1969년"이라고 답할 수 있는가?
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 연도가 몇 개 있는지 본다.
- 판단할 질문: 연도가 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 할 일: 위 `doc_id`(문서) 링크를 `Cmd+클릭`해 연다. `Cmd+F`로 `경공업단지`를 찾고, `Enter`로 걸린 곳을 하나씩 넘겨 본다. 218줄에서는 구절의 앞뒤 한두 문장도 읽는다.
- 판단할 질문: 걸린 곳마다, 춘천경공업단지가 조성된 해가 1969가 아닌 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 곳 이야기로 바뀌지 않는가?
- [ ] 확인함

#### 4. 같은 언어(한국어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-ko-*`를 적는다. `경공업단지`를 찾는다.
- 판단할 질문: `wiki-ko-chuncheon` 말고 다른 한국어 문서가 걸리면, 거기에 춘천경공업단지의 다른 연도가 적혀 있지 않은가?
- [ ] 확인함

#### 5. 영어 문서: Gemini가 찾은 걸린 곳을 번역기로 읽었다
Gemini가 영어 문서에서 `1969`를 찾았고, 나오는 곳은 아래 2곳이 전부다(검사 프로그램이 확인함). `Chuncheon Light Industrial Complex`, `Light Industrial`은 영어 문서 어디에도 없다.
- 걸린 곳 1: [wiki-en-chuncheon.md 178줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L178)
  > The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969), and the highest was 39.5 °C (103 °F) (1 August 2018).
- 걸린 곳 2: [wiki-en-busan.md 622줄](../../../data/corpus/markdown/wiki-en-busan.md#L622)
  > - Kim Wonhae (born 1969), actor and comedian
- 할 일: 두 문장을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 이 문장이 "춘천경공업단지가 1969년에 조성되었다"와 같은 사실을 말하는가?
- [ ] 확인함

#### 6. 영어 문서: 다른 말로도 찾아봤다
- 할 일: 번역기에 "경공업단지"를 넣어 나온 영어 말과, 더 짧은 말(예: `industrial`)로 폴더 찾기를 한다. 이번에는 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 걸린 곳이 있으면 그 줄을 번역기로 읽는다.
- 판단할 질문: 영어 문서 어딘가에 춘천경공업단지가 1969년에 조성되었다는 말이 다른 표현으로 있는가?
- 찾아본 말과 결과를 맨 아래 "더 찾아본 말과 걸린 곳"에 적는다.
- [ ] 확인함

#### 7. 영어 문서: 같은 도시(춘천)의 영어 문서를 통째로 읽었다
- 할 일 1: 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1376994978 (춘천 영어 위키백과, 우리가 가져온 판)를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 `경공업`, `1969`를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 할 일 2: [kto-en-chuncheon-samaksan-cable-car.md](../../../data/corpus/markdown/kto-en-chuncheon-samaksan-cable-car.md)(춘천 케이블카 영어 소개 글)를 열어 내용 전체를 번역기에 붙여 읽는다. 짧은 글이다.
- 판단할 질문: 두 문서 어디에든 경공업단지가 1969년에 조성되었다는 이야기가 있는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 위 `question`(질문)과 `passage`(근거 구절)의 핵심 낱말을 견준다.
- 판단할 질문: 질문의 "경공업단지", "조성"이 구절에 같은 낱말로 있는가? 같으면 single_fact(단일 사실), 다른 말로 바꿨으면 paraphrase(표현 불일치)다. 이 후보는 single_fact로 적혀 있다.
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 더 찾아본 말과 걸린 곳(6번에서 직접 찾은 것. 예: "industrial → 영어 문서 3곳, 모두 다른 이야기"):
- 메모(애매한 것, Claude에게 물을 것):

---

## c-002 · `type`(유형): single_fact(단일 사실) · 도시 묶음: 한국어 도시(세종특별자치시)

- `question`(질문): 세종특별자치시를 상징하는 시조(새)는 무엇인가?
- `answer`(정답): 파랑새

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 세종특별자치시의 시조는 파랑새이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-sejong.md 22줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L22) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > - 시조: 파랑새

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `Bluebird` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Parangsae` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `City bird` → `hits`(걸린 곳) 2곳
    - [wiki-en-busan.md 418줄](../../../data/corpus/markdown/wiki-en-busan.md#L418) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      - `excerpt`(걸린 구절):
        > The mascot was a seagull, the city bird of Busan named, "Duria". East Timor took part in the games for the first time.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 부산광역시의 상징 새에 대한 내용임
    - [wiki-en-cheonan.md 74줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L74) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
      - `excerpt`(걸린 구절):
        > - City Bird: Dove
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 천안시의 상징 새에 대한 내용임

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-003 · `type`(유형): table_numeric(표·수치·조건) · 도시 묶음: 한국어 도시(수원시)

- `question`(질문): 2021년 5월 31일 데이터 기준으로, 수원시 팔달구 고등동의 외국인 계(합계) 인구수는 몇 명인가?
- `answer`(정답): 2849명

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 2021년 5월 31일 기준 수원시 팔달구 고등동의 외국인 계 인구수는 2849명이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [portal-ko-suwon-population.md 3줄](../../../data/corpus/markdown/portal-ko-suwon-population.md#L3) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > | 구 | 구_동 | 세대수 | 인구_합계 | 인구_내국인_인구수_계 | 인구_내국인_인구수_남 | 인구_내국인_인구수_여 | 인구_내국인_전월말인구수 | 인구_내국인_인구증감전월대비 | 외국인_계 | 외국인_남 | 외국인_여 | 데이터기준일자 |
      > | 팔달구 | 고등동 | 8991 | 21931 | 19082 | 9630 | 9452 | 21445 | 486 | 2849 | 1562 | 1287 | 2021-05-31 |

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `Godeung-dong` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `2849` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `21931` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 해당 없음: 위 `term`(찾을 말)마다 `hits`(걸린 곳)이 없음
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-004 · `type`(유형): table_numeric(표·수치·조건) · 도시 묶음: 두 언어 도시(전주시)

- `question`(질문): 2026년 3월 17일 기준 전주시 효자4동의 65세 이상 인구수 합계(계)는 몇 명인가?
- `answer`(정답): 4917명

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 2026년 3월 17일 기준 전주시 효자4동의 65세 이상 인구수 계는 4917명이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [portal-ko-jeonju-population.md 3줄](../../../data/corpus/markdown/portal-ko-jeonju-population.md#L3) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
      > | 효자4동 | 17120 | 38687 | 18784 | 19903 | 7219 | 3648 | 3571 | 31468 | 15136 | 16332 | 4917 | 2184 | 2733 | 2026-03-17 |

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-jeonju.md](../../../data/corpus/markdown/wiki-en-jeonju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
  - [kto-en-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `Hyoja4-dong` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Hyoja-4-dong` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `4917` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 해당 없음: 위 `term`(찾을 말)마다 `hits`(걸린 곳)이 없음
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-005 · `type`(유형): multi_doc(여러 문서 연결) · 도시 묶음: 한국어 도시(수원시, 세종특별자치시)

- `question`(질문): 수원시와 세종특별자치시의 시화(시의 꽃)를 각각 무엇인지 쓰시오.
- `answer`(정답): 수원시는 진달래, 세종특별자치시는 복사꽃이다

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 수원시의 시화는 진달래이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-suwon.md 19줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L19) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > - 시화: 진달래
- `fact`(사실) 2: 세종특별자치시의 시화는 복사꽃이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-sejong.md 21줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L21) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > - 시화: 복사꽃

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `City flower` → `hits`(걸린 곳) 1곳
    - [wiki-en-cheonan.md 73줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L73) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
      - `excerpt`(걸린 구절):
        > - City Flower: Golden bell flower
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 천안시의 시화에 대한 내용임
  - `term`(찾을 말) `Azalea` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Peach blossom` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-006 · `type`(유형): multi_doc(여러 문서 연결) · 도시 묶음: 두 언어 도시(춘천시, 청주시)

- `question`(질문): 춘천시와 청주시의 시조(시를 상징하는 새)는 각각 무엇인가?
- `answer`(정답): 춘천시는 산까치, 청주시는 까치이다

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 춘천시의 시조(새)는 산까치이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-chuncheon.md 19줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L19) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > - 새: 산까치
- `fact`(사실) 2: 청주시의 시조는 까치이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-cheongju.md 20줄](../../../data/corpus/markdown/wiki-ko-cheongju.md#L20) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > - 시조: 까치

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-cheongju.md](../../../data/corpus/markdown/wiki-en-cheongju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953230
  - [wiki-en-chuncheon.md](../../../data/corpus/markdown/wiki-en-chuncheon.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1376994978
  - [kto-en-cheongju-cheongnamdae.md](../../../data/corpus/markdown/kto-en-cheongju-cheongnamdae.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
  - [kto-en-chuncheon-samaksan-cable-car.md](../../../data/corpus/markdown/kto-en-chuncheon-samaksan-cable-car.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `City bird` → `hits`(걸린 곳) 2곳
    - [wiki-en-cheonan.md 74줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L74) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
      - `excerpt`(걸린 구절):
        > - City Bird: Dove
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 천안시의 상징 새에 대한 내용임
    - [wiki-en-busan.md 418줄](../../../data/corpus/markdown/wiki-en-busan.md#L418) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      - `excerpt`(걸린 구절):
        > The mascot was a seagull, the city bird of Busan named, "Duria". East Timor took part in the games for the first time.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 부산광역시의 상징 새에 대한 내용임
  - `term`(찾을 말) `Magpie` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Mountain magpie` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-007 · `type`(유형): multi_doc(여러 문서 연결) · 도시 묶음: 한국어 도시(광주광역시)

- `question`(질문): 광주광역시의 5개 자치구 중에서 세대 수가 가장 많은 구와 가장 적은 구는 각각 어디인가?
- `answer`(정답): 가장 많은 구는 북구이고 가장 적은 구는 동구이다

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 동구의 세대 수는 45,860이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
      > | 동구 | 東區 | 45,860 | 98,784 | 49.2 |
- `fact`(사실) 2: 서구의 세대 수는 120,107이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
      > | 서구 | 西區 | 120,107 | 305,028 | 47.78 |
- `fact`(사실) 3: 남구의 세대 수는 87,514이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
      > | 남구 | 南區 | 87,514 | 220,165 | 61.01 |
- `fact`(사실) 4: 북구의 세대 수는 178,735이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
      > | 북구 | 北區 | 178,735 | 446,316 | 120.29 |
- `fact`(사실) 5: 광산구의 세대 수는 148,252이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
      > | 광산구 | 光山區 | 148,252 | 400,753 | 222.9 |
- `fact`(사실) 6: 광주광역시 5개 자치구 중 세대 수가 가장 많은 곳은 북구, 가장 적은 곳은 동구이다
  - `evidence`(근거): 없음 — 다른 사실에서 나오는 결론

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `178,735` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `45,860` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Buk-gu` → `hits`(걸린 곳) 2곳
    - [wiki-en-busan.md 14줄](../../../data/corpus/markdown/wiki-en-busan.md#L14) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      - `excerpt`(걸린 구절):
        > List Jeon Jaesoo (Democratic) Buk-gu / Gangseo-gu A district,
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 국회의원 지역구 이름의 일부임
    - [wiki-en-busan.md 14줄](../../../data/corpus/markdown/wiki-en-busan.md#L14) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      - `excerpt`(걸린 구절):
        > Kim Do-eup (People Power) Buk-gu / Gangseo-gu B district, Suh Byung-soo (People Power)
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 국회의원 지역구 이름의 일부임

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-008 · `type`(유형): multi_doc(여러 문서 연결) · 도시 묶음: 두 언어 도시(전주시)

- `question`(질문): 2026년 3월 17일을 기준으로, 전주시 노송동과 완산동의 18세미만인구수(계)를 합하면 총 몇 명인가?
- `answer`(정답): 1342명

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 2026년 3월 17일 기준 전주시 노송동의 18세미만인구수(계)는 890명이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [portal-ko-jeonju-population.md 3줄](../../../data/corpus/markdown/portal-ko-jeonju-population.md#L3) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
      > | 노송동 | 5286 | 9970 | 4858 | 5112 | 890 | 472 | 418 | 9080 | 4386 | 4694 | 3380 | 1418 | 1962 | 2026-03-17 |
- `fact`(사실) 2: 2026년 3월 17일 기준 전주시 완산동의 18세미만인구수(계)는 452명이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [portal-ko-jeonju-population.md 3줄](../../../data/corpus/markdown/portal-ko-jeonju-population.md#L3) · `location`(위치): 첫 부분
    - `passage`(근거 구절):
      > | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
      > | 완산동 | 2530 | 4686 | 2285 | 2401 | 452 | 250 | 202 | 4234 | 2035 | 2199 | 1622 | 667 | 955 | 2026-03-17 |
- `fact`(사실) 3: 노송동과 완산동의 18세미만인구수를 더하면 총 1342명이다
  - `evidence`(근거): 없음 — 다른 사실에서 나오는 결론

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-jeonju.md](../../../data/corpus/markdown/wiki-en-jeonju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
  - [kto-en-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `Nosong-dong` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Wansan-dong` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `1342` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 해당 없음: 위 `term`(찾을 말)마다 `hits`(걸린 곳)이 없음
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-009 · `type`(유형): paraphrase(표현 불일치) · 도시 묶음: 한국어 도시(경주시)

- `question`(질문): 경상북도에 속한 시·군 중에서 땅 넓이 기준으로 안동시 다음으로 큰 곳은 어디인가?
- `answer`(정답): 경주시

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 경상북도에서 안동시에 이어 두 번째로 넓은 기초자치단체는 경주시이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-gyeongju.md 123줄](../../../data/corpus/markdown/wiki-ko-gyeongju.md#L123) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > 경주시의 행정구역 면적은 1,324.41km2로, 경상북도에서 안동시에 이어 두 번째로 넓은 기초자치단체이다.

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `second largest` → `hits`(걸린 곳) 3곳
    - [wiki-en-busan.md 132줄](../../../data/corpus/markdown/wiki-en-busan.md#L132) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      - `excerpt`(걸린 구절):
        > Busan is the second largest city in Korea, a maritime logistics hub, and a world-class mega port, it acts as a gateway to the Eurasian continent.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 부산이 한국에서 두 번째로 큰 도시라는 내용임
    - [wiki-en-jeju.md 47줄](../../../data/corpus/markdown/wiki-en-jeju.md#L47) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1377658564
      - `excerpt`(걸린 구절):
        > A bus ride from Jeju City to Seogwipo (the second largest city on the island) is typically an hour.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 서귀포가 제주도에서 두 번째로 큰 도시라는 내용임
    - [wiki-en-gangneung.md 113줄](../../../data/corpus/markdown/wiki-en-gangneung.md#L113) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378182836
      - `excerpt`(걸린 구절):
        > Gyeongpo Lake is the second largest lagoon in the east coast. Its size has shrunk due to continuous development since the early 20th century.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 경포호가 동해안에서 두 번째로 큰 석호라는 내용임
  - `term`(찾을 말) `after Andong` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `1,324.41` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-010 · `type`(유형): paraphrase(표현 불일치) · 도시 묶음: 두 언어 도시(천안시)

- `question`(질문): 고려시대 망이·망소이의 난이 일어났을 때 명학소민들에 의해 전소된, 길을 오가는 사람들의 편의를 도모할 목적으로 만들어졌던 천안 직산군 지역의 시설 이름은 무엇인가?
- `answer`(정답): 홍경원

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 고려시대에 직산군에 교통의 편의를 위해 설치되었던 홍경원은 망이·망소이의 난 때 명학소민들이 불태웠다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-cheonan.md 29줄](../../../data/corpus/markdown/wiki-ko-cheonan.md#L29) · `location`(위치): 역사
    - `passage`(근거 구절):
      > 직산군은 고려시대에 홍경원이 설치되어 있던 곳으로, 본래 교통의 편의를 위해 설치되었던 홍경원은 막강한 경제력을 행사하였던 것으로 추측되는데, 망이·망소이의 난 때에는 명학소민들이 홍경원을 불태우고,

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-cheonan.md](../../../data/corpus/markdown/wiki-en-cheonan.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
  - [kto-en-cheonan-samgeori-park.md](../../../data/corpus/markdown/kto-en-cheonan-samgeori-park.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `Honggyeongwon` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Mang-i` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Myeonghakso` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 해당 없음: 위 `term`(찾을 말)마다 `hits`(걸린 곳)이 없음
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-011 · `type`(유형): paraphrase(표현 불일치) · 도시 묶음: 한국어 도시(세종특별자치시)

- `question`(질문): 대한민국에서 내부에 시, 군, 구 같은 하급 지자체를 전혀 포함하지 않고 단독으로 운영되는 광역 단위 특별자치시의 명칭은 무엇인가?
- `answer`(정답): 세종특별자치시

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 세종특별자치시는 하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제 광역지방자치단체이다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-sejong.md 79줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L79) · `location`(위치): 행정 구역
    - `passage`(근거 구절):
      > 세종특별자치시는 하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제 광역지방자치단체로

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `single-tier` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `basic local government` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `without lower-level` → `hits`(걸린 곳) 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 해당 없음: 위 `term`(찾을 말)마다 `hits`(걸린 곳)이 없음
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-012 · `type`(유형): paraphrase(표현 불일치) · 도시 묶음: 두 언어 도시(전주시)

- `question`(질문): 과거 완산으로 불렸던 지역을 두고 《삼국사기》 지리지 백제편에서는 어떠한 별명을 달아 놓았는가?
- `answer`(정답): 비사벌

### `required_facts`(꼭 필요한 사실)
- `fact`(사실) 1: 《삼국사기》 지리지 백제편에서 전주(완산)의 별칭이 '비사벌'이라고 주(註)를 달았다
  - `evidence`(근거) 1
    - `doc_id`(문서): [wiki-ko-jeonju.md 31줄](../../../data/corpus/markdown/wiki-ko-jeonju.md#L31) · `location`(위치): 지명 유래
    - `passage`(근거 구절):
      > 전주는 '비사벌'이라고 불리기도 했다. 이는 《삼국사기》의 지리지 백제편에서 완산의 별칭이 '비사벌'이라고 주(註)를 달았기 때문이다.

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-jeonju.md](../../../data/corpus/markdown/wiki-en-jeonju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
  - [kto-en-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- `opposite_check`(반대 언어 찾기 기록):
  - `term`(찾을 말) `Bisabeol` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Samguk Sagi` → `hits`(걸린 곳) 없음
  - `term`(찾을 말) `Wansan` → `hits`(걸린 곳) 4곳
    - [wiki-en-jeonju.md 41줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L41) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
      - `excerpt`(걸린 구절):
        > Jeonju is divided into two wards, Deokjin District and Wansan District that, in turn, are divided into approximately 40 neighborhoods.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 전주시 완산구에 대한 내용임
    - [wiki-en-jeonju.md 97줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L97) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
      - `excerpt`(걸린 구절):
        > In 892 (or 900), Gyeon Hwon renamed the city Wansan and established it as the capital of the Later Baekje kingdom.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 견훤이 전주의 이름을 완산으로 바꾸었다는 내용임
    - [wiki-en-jeonju.md 97줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L97) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
      - `excerpt`(걸린 구절):
        > From Wansan, Gyeon Hwon campaigned against Silla which climaxed with the destruction of Geumseong (the capital of the Silla kingdom) and the assassination of King Gyeongae in 927.
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 완산에서 신라에 대항하여 작전을 펼쳤다는 내용임
    - [kto-en-jeonju-hanok-village.md 3줄](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md#L3) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
      - `excerpt`(걸린 구절):
        > Address: 99 Girin-daero, Wansan-gu, Jeonju-si, Jeonbuk-do
      - `same_fact`·`why`(Gemini의 판단): 같은 사실 아님 — 주소의 일부인 완산구를 나타냄

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):
