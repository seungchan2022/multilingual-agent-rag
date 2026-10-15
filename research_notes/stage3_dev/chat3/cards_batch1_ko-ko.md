# 대조 카드: batch1_ko-ko.yaml

이 파일은 후보마다 카드 하나로, 순서표(data/questions/final_set_guide.md)의 "대조할 것"을 따라 카드마다 칸을 채운다. 확인한 칸은 [ ]를 [x]로 바꾼다. 하지 않은 칸은 그대로 둔다. 판정은 채택·수정·폐기 가운데 하나만 남긴다. 애매한 것은 메모에 적는다. 근거 구절이 원문에 글자 그대로 있는지, 개수·형식, opposite_check가 원문과 맞는지는 후보 검사가 이미 봤다.

---

## c-001 · single_fact · 두 언어 도시(춘천시)

**질문**: 춘천경공업단지가 조성되기 시작한 연도는 언제인가?
**정답**: 1969년

### 근거
- 사실 1: 춘천경공업단지는 1969년부터 조성되었다
  - 문서: [wiki-ko-chuncheon.md 218줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L218) · 위치: 경제
  - 구절:
    > 1969년부터 춘천경공업단지가 조성되었으며, 73년 5월 공업장려지구로 지정되었다.

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-chuncheon.md](../../../data/corpus/markdown/wiki-en-chuncheon.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1376994978
  - [kto-en-chuncheon-samaksan-cable-car.md](../../../data/corpus/markdown/kto-en-chuncheon-samaksan-cable-car.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- Gemini가 찾은 말과 걸린 곳:
  - `1969`: 걸린 곳 2곳
    - [wiki-en-chuncheon.md 178줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L178) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1376994978
      > The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969), and the highest was 39.5 °C (103 °F) (1 August 2018).
      Gemini의 판단: 같은 사실 아님 — 1969년이라는 연도가 아니라, 최저 기온이 관측된 날짜(1969년 2월 6일)를 설명하는 내용 중 일부로 쓰였음
    - [wiki-en-busan.md 622줄](../../../data/corpus/markdown/wiki-en-busan.md#L622) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      > - Kim Wonhae (born 1969), actor and comedian
      Gemini의 판단: 같은 사실 아님 — 배우 김원해의 출생 연도를 나타냄
  - `Chuncheon Light Industrial Complex`: 걸린 곳 없음
  - `Light Industrial`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-002 · single_fact · 한국어 도시(세종특별자치시)

**질문**: 세종특별자치시를 상징하는 시조(새)는 무엇인가?
**정답**: 파랑새

### 근거
- 사실 1: 세종특별자치시의 시조는 파랑새이다
  - 문서: [wiki-ko-sejong.md 22줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L22) · 위치: 첫 부분
  - 구절:
    > - 시조: 파랑새

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- Gemini가 찾은 말과 걸린 곳:
  - `Bluebird`: 걸린 곳 없음
  - `Parangsae`: 걸린 곳 없음
  - `City bird`: 걸린 곳 2곳
    - [wiki-en-busan.md 418줄](../../../data/corpus/markdown/wiki-en-busan.md#L418) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      > The mascot was a seagull, the city bird of Busan named, "Duria". East Timor took part in the games for the first time.
      Gemini의 판단: 같은 사실 아님 — 부산광역시의 상징 새에 대한 내용임
    - [wiki-en-cheonan.md 74줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L74) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
      > - City Bird: Dove
      Gemini의 판단: 같은 사실 아님 — 천안시의 상징 새에 대한 내용임

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-003 · table_numeric · 한국어 도시(수원시)

**질문**: 2021년 5월 31일 데이터 기준으로, 수원시 팔달구 고등동의 외국인 계(합계) 인구수는 몇 명인가?
**정답**: 2849명

### 근거
- 사실 1: 2021년 5월 31일 기준 수원시 팔달구 고등동의 외국인 계 인구수는 2849명이다
  - 문서: [portal-ko-suwon-population.md 3줄](../../../data/corpus/markdown/portal-ko-suwon-population.md#L3) · 위치: 첫 부분
  - 구절:
    > | 구 | 구_동 | 세대수 | 인구_합계 | 인구_내국인_인구수_계 | 인구_내국인_인구수_남 | 인구_내국인_인구수_여 | 인구_내국인_전월말인구수 | 인구_내국인_인구증감전월대비 | 외국인_계 | 외국인_남 | 외국인_여 | 데이터기준일자 |
    > | 팔달구 | 고등동 | 8991 | 21931 | 19082 | 9630 | 9452 | 21445 | 486 | 2849 | 1562 | 1287 | 2021-05-31 |

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- Gemini가 찾은 말과 걸린 곳:
  - `Godeung-dong`: 걸린 곳 없음
  - `2849`: 걸린 곳 없음
  - `21931`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-004 · table_numeric · 두 언어 도시(전주시)

**질문**: 2026년 3월 17일 기준 전주시 효자4동의 65세 이상 인구수 합계(계)는 몇 명인가?
**정답**: 4917명

### 근거
- 사실 1: 2026년 3월 17일 기준 전주시 효자4동의 65세 이상 인구수 계는 4917명이다
  - 문서: [portal-ko-jeonju-population.md 3줄](../../../data/corpus/markdown/portal-ko-jeonju-population.md#L3) · 위치: 첫 부분
  - 구절:
    > | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
    > | 효자4동 | 17120 | 38687 | 18784 | 19903 | 7219 | 3648 | 3571 | 31468 | 15136 | 16332 | 4917 | 2184 | 2733 | 2026-03-17 |

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-jeonju.md](../../../data/corpus/markdown/wiki-en-jeonju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
  - [kto-en-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- Gemini가 찾은 말과 걸린 곳:
  - `Hyoja4-dong`: 걸린 곳 없음
  - `Hyoja-4-dong`: 걸린 곳 없음
  - `4917`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-005 · multi_doc · 한국어 도시(수원시, 세종특별자치시)

**질문**: 수원시와 세종특별자치시의 시화(시의 꽃)를 각각 무엇인지 쓰시오.
**정답**: 수원시는 진달래, 세종특별자치시는 복사꽃이다

### 근거
- 사실 1: 수원시의 시화는 진달래이다
  - 문서: [wiki-ko-suwon.md 19줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L19) · 위치: 첫 부분
  - 구절:
    > - 시화: 진달래
- 사실 2: 세종특별자치시의 시화는 복사꽃이다
  - 문서: [wiki-ko-sejong.md 21줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L21) · 위치: 첫 부분
  - 구절:
    > - 시화: 복사꽃

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- Gemini가 찾은 말과 걸린 곳:
  - `City flower`: 걸린 곳 1곳
    - [wiki-en-cheonan.md 73줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L73) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
      > - City Flower: Golden bell flower
      Gemini의 판단: 같은 사실 아님 — 천안시의 시화에 대한 내용임
  - `Azalea`: 걸린 곳 없음
  - `Peach blossom`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-006 · multi_doc · 두 언어 도시(춘천시, 청주시)

**질문**: 춘천시와 청주시의 시조(시를 상징하는 새)는 각각 무엇인가?
**정답**: 춘천시는 산까치, 청주시는 까치이다

### 근거
- 사실 1: 춘천시의 시조(새)는 산까치이다
  - 문서: [wiki-ko-chuncheon.md 19줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L19) · 위치: 첫 부분
  - 구절:
    > - 새: 산까치
- 사실 2: 청주시의 시조는 까치이다
  - 문서: [wiki-ko-cheongju.md 20줄](../../../data/corpus/markdown/wiki-ko-cheongju.md#L20) · 위치: 첫 부분
  - 구절:
    > - 시조: 까치

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-cheongju.md](../../../data/corpus/markdown/wiki-en-cheongju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953230
  - [wiki-en-chuncheon.md](../../../data/corpus/markdown/wiki-en-chuncheon.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1376994978
  - [kto-en-cheongju-cheongnamdae.md](../../../data/corpus/markdown/kto-en-cheongju-cheongnamdae.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
  - [kto-en-chuncheon-samaksan-cable-car.md](../../../data/corpus/markdown/kto-en-chuncheon-samaksan-cable-car.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- Gemini가 찾은 말과 걸린 곳:
  - `City bird`: 걸린 곳 2곳
    - [wiki-en-cheonan.md 74줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L74) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
      > - City Bird: Dove
      Gemini의 판단: 같은 사실 아님 — 천안시의 상징 새에 대한 내용임
    - [wiki-en-busan.md 418줄](../../../data/corpus/markdown/wiki-en-busan.md#L418) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      > The mascot was a seagull, the city bird of Busan named, "Duria". East Timor took part in the games for the first time.
      Gemini의 판단: 같은 사실 아님 — 부산광역시의 상징 새에 대한 내용임
  - `Magpie`: 걸린 곳 없음
  - `Mountain magpie`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-007 · multi_doc · 한국어 도시(광주광역시)

**질문**: 광주광역시의 5개 자치구 중에서 세대 수가 가장 많은 구와 가장 적은 구는 각각 어디인가?
**정답**: 가장 많은 구는 북구이고 가장 적은 구는 동구이다

### 근거
- 사실 1: 동구의 세대 수는 45,860이다
  - 문서: [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · 위치: 행정 구역
  - 구절:
    > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
    > | 동구 | 東區 | 45,860 | 98,784 | 49.2 |
- 사실 2: 서구의 세대 수는 120,107이다
  - 문서: [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · 위치: 행정 구역
  - 구절:
    > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
    > | 서구 | 西區 | 120,107 | 305,028 | 47.78 |
- 사실 3: 남구의 세대 수는 87,514이다
  - 문서: [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · 위치: 행정 구역
  - 구절:
    > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
    > | 남구 | 南區 | 87,514 | 220,165 | 61.01 |
- 사실 4: 북구의 세대 수는 178,735이다
  - 문서: [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · 위치: 행정 구역
  - 구절:
    > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
    > | 북구 | 北區 | 178,735 | 446,316 | 120.29 |
- 사실 5: 광산구의 세대 수는 148,252이다
  - 문서: [wiki-ko-gwangju.md 79줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L79) · 위치: 행정 구역
  - 구절:
    > | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
    > | 광산구 | 光山區 | 148,252 | 400,753 | 222.9 |
- 사실 6: 광주광역시 5개 자치구 중 세대 수가 가장 많은 곳은 북구, 가장 적은 곳은 동구이다
  - (다른 사실에서 나오는 결론)

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- Gemini가 찾은 말과 걸린 곳:
  - `178,735`: 걸린 곳 없음
  - `45,860`: 걸린 곳 없음
  - `Buk-gu`: 걸린 곳 2곳
    - [wiki-en-busan.md 14줄](../../../data/corpus/markdown/wiki-en-busan.md#L14) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      > List Jeon Jaesoo (Democratic) Buk-gu / Gangseo-gu A district,
      Gemini의 판단: 같은 사실 아님 — 국회의원 지역구 이름의 일부임
    - [wiki-en-busan.md 14줄](../../../data/corpus/markdown/wiki-en-busan.md#L14) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      > Kim Do-eup (People Power) Buk-gu / Gangseo-gu B district, Suh Byung-soo (People Power)
      Gemini의 판단: 같은 사실 아님 — 국회의원 지역구 이름의 일부임

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-008 · multi_doc · 두 언어 도시(전주시)

**질문**: 2026년 3월 17일을 기준으로, 전주시 노송동과 완산동의 18세미만인구수(계)를 합하면 총 몇 명인가?
**정답**: 1342명

### 근거
- 사실 1: 2026년 3월 17일 기준 전주시 노송동의 18세미만인구수(계)는 890명이다
  - 문서: [portal-ko-jeonju-population.md 3줄](../../../data/corpus/markdown/portal-ko-jeonju-population.md#L3) · 위치: 첫 부분
  - 구절:
    > | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
    > | 노송동 | 5286 | 9970 | 4858 | 5112 | 890 | 472 | 418 | 9080 | 4386 | 4694 | 3380 | 1418 | 1962 | 2026-03-17 |
- 사실 2: 2026년 3월 17일 기준 전주시 완산동의 18세미만인구수(계)는 452명이다
  - 문서: [portal-ko-jeonju-population.md 3줄](../../../data/corpus/markdown/portal-ko-jeonju-population.md#L3) · 위치: 첫 부분
  - 구절:
    > | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
    > | 완산동 | 2530 | 4686 | 2285 | 2401 | 452 | 250 | 202 | 4234 | 2035 | 2199 | 1622 | 667 | 955 | 2026-03-17 |
- 사실 3: 노송동과 완산동의 18세미만인구수를 더하면 총 1342명이다
  - (다른 사실에서 나오는 결론)

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-jeonju.md](../../../data/corpus/markdown/wiki-en-jeonju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
  - [kto-en-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- Gemini가 찾은 말과 걸린 곳:
  - `Nosong-dong`: 걸린 곳 없음
  - `Wansan-dong`: 걸린 곳 없음
  - `1342`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-009 · paraphrase · 한국어 도시(경주시)

**질문**: 경상북도에 속한 시·군 중에서 땅 넓이 기준으로 안동시 다음으로 큰 곳은 어디인가?
**정답**: 경주시

### 근거
- 사실 1: 경상북도에서 안동시에 이어 두 번째로 넓은 기초자치단체는 경주시이다
  - 문서: [wiki-ko-gyeongju.md 123줄](../../../data/corpus/markdown/wiki-ko-gyeongju.md#L123) · 위치: 행정 구역
  - 구절:
    > 경주시의 행정구역 면적은 1,324.41km2로, 경상북도에서 안동시에 이어 두 번째로 넓은 기초자치단체이다.

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- Gemini가 찾은 말과 걸린 곳:
  - `second largest`: 걸린 곳 3곳
    - [wiki-en-busan.md 132줄](../../../data/corpus/markdown/wiki-en-busan.md#L132) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379685823
      > Busan is the second largest city in Korea, a maritime logistics hub, and a world-class mega port, it acts as a gateway to the Eurasian continent.
      Gemini의 판단: 같은 사실 아님 — 부산이 한국에서 두 번째로 큰 도시라는 내용임
    - [wiki-en-jeju.md 47줄](../../../data/corpus/markdown/wiki-en-jeju.md#L47) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1377658564
      > A bus ride from Jeju City to Seogwipo (the second largest city on the island) is typically an hour.
      Gemini의 판단: 같은 사실 아님 — 서귀포가 제주도에서 두 번째로 큰 도시라는 내용임
    - [wiki-en-gangneung.md 113줄](../../../data/corpus/markdown/wiki-en-gangneung.md#L113) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378182836
      > Gyeongpo Lake is the second largest lagoon in the east coast. Its size has shrunk due to continuous development since the early 20th century.
      Gemini의 판단: 같은 사실 아님 — 경포호가 동해안에서 두 번째로 큰 석호라는 내용임
  - `after Andong`: 걸린 곳 없음
  - `1,324.41`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-010 · paraphrase · 두 언어 도시(천안시)

**질문**: 고려시대 망이·망소이의 난이 일어났을 때 명학소민들에 의해 전소된, 길을 오가는 사람들의 편의를 도모할 목적으로 만들어졌던 천안 직산군 지역의 시설 이름은 무엇인가?
**정답**: 홍경원

### 근거
- 사실 1: 고려시대에 직산군에 교통의 편의를 위해 설치되었던 홍경원은 망이·망소이의 난 때 명학소민들이 불태웠다
  - 문서: [wiki-ko-cheonan.md 29줄](../../../data/corpus/markdown/wiki-ko-cheonan.md#L29) · 위치: 역사
  - 구절:
    > 직산군은 고려시대에 홍경원이 설치되어 있던 곳으로, 본래 교통의 편의를 위해 설치되었던 홍경원은 막강한 경제력을 행사하였던 것으로 추측되는데, 망이·망소이의 난 때에는 명학소민들이 홍경원을 불태우고,

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-cheonan.md](../../../data/corpus/markdown/wiki-en-cheonan.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1378953224
  - [kto-en-cheonan-samgeori-park.md](../../../data/corpus/markdown/kto-en-cheonan-samgeori-park.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- Gemini가 찾은 말과 걸린 곳:
  - `Honggyeongwon`: 걸린 곳 없음
  - `Mang-i`: 걸린 곳 없음
  - `Myeonghakso`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-011 · paraphrase · 한국어 도시(세종특별자치시)

**질문**: 대한민국에서 내부에 시, 군, 구 같은 하급 지자체를 전혀 포함하지 않고 단독으로 운영되는 광역 단위 특별자치시의 명칭은 무엇인가?
**정답**: 세종특별자치시

### 근거
- 사실 1: 세종특별자치시는 하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제 광역지방자치단체이다
  - 문서: [wiki-ko-sejong.md 79줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L79) · 위치: 행정 구역
  - 구절:
    > 세종특별자치시는 하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제 광역지방자치단체로

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다): 없음(한국어 도시)
- Gemini가 찾은 말과 걸린 곳:
  - `single-tier`: 걸린 곳 없음
  - `basic local government`: 걸린 곳 없음
  - `without lower-level`: 걸린 곳 없음

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):

---

## c-012 · paraphrase · 두 언어 도시(전주시)

**질문**: 과거 완산으로 불렸던 지역을 두고 《삼국사기》 지리지 백제편에서는 어떠한 별명을 달아 놓았는가?
**정답**: 비사벌

### 근거
- 사실 1: 《삼국사기》 지리지 백제편에서 전주(완산)의 별칭이 '비사벌'이라고 주(註)를 달았다
  - 문서: [wiki-ko-jeonju.md 31줄](../../../data/corpus/markdown/wiki-ko-jeonju.md#L31) · 위치: 지명 유래
  - 구절:
    > 전주는 '비사벌'이라고 불리기도 했다. 이는 《삼국사기》의 지리지 백제편에서 완산의 별칭이 '비사벌'이라고 주(註)를 달았기 때문이다.

### 반대 언어 문서 확인 재료
- 같은 도시의 반대 언어 문서(통째로 번역해 읽는다):
  - [wiki-en-jeonju.md](../../../data/corpus/markdown/wiki-en-jeonju.md) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
  - [kto-en-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
- Gemini가 찾은 말과 걸린 곳:
  - `Bisabeol`: 걸린 곳 없음
  - `Samguk Sagi`: 걸린 곳 없음
  - `Wansan`: 걸린 곳 4곳
    - [wiki-en-jeonju.md 41줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L41) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
      > Jeonju is divided into two wards, Deokjin District and Wansan District that, in turn, are divided into approximately 40 neighborhoods.
      Gemini의 판단: 같은 사실 아님 — 전주시 완산구에 대한 내용임
    - [wiki-en-jeonju.md 97줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L97) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
      > In 892 (or 900), Gyeon Hwon renamed the city Wansan and established it as the capital of the Later Baekje kingdom.
      Gemini의 판단: 같은 사실 아님 — 견훤이 전주의 이름을 완산으로 바꾸었다는 내용임
    - [wiki-en-jeonju.md 97줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L97) · 원문 주소: https://en.wikipedia.org/w/index.php?oldid=1379135207
      > From Wansan, Gyeon Hwon campaigned against Silla which climaxed with the destruction of Geumseong (the capital of the Silla kingdom) and the assassination of King Gyeongae in 927.
      Gemini의 판단: 같은 사실 아님 — 완산에서 신라에 대항하여 작전을 펼쳤다는 내용임
    - [kto-en-jeonju-hanok-village.md 3줄](../../../data/corpus/markdown/kto-en-jeonju-hanok-village.md#L3) · 짧은 문서라 파일 내용을 그대로 번역기에 붙인다
      > Address: 99 Girin-daero, Wansan-gu, Jeonju-si, Jeonbuk-do
      Gemini의 판단: 같은 사실 아님 — 주소의 일부인 완산구를 나타냄

### 판정
- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 "질문", "정답", "구절"
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 "구절"
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 "문서" 링크를 Cmd+클릭해 열고 Cmd+F
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 반대 언어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 위 "Gemini가 찾은 말과 걸린 곳"
- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 위 찾은 말, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 통째로 번역해 읽었다 — 볼 곳: 위 "같은 도시의 반대 언어 문서"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 위 "근거"의 사실들, "정답"
- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 유형, "질문", "구절"
- 판정: 채택 / 수정 / 폐기
- 이유:
- 더 찾아본 말과 걸린 곳:
- 메모(애매한 것, Claude에게 물을 것):
