```yaml
- id: c-001
  question: 대한민국에서 유일하게 경운기 전용 도로가 설치되어 있는 도시는 어디인가?
  question_language: ko
  evidence_language: ko
  type: single_fact
  answer: 경주시이다.
  required_facts:
    - fact: 경주시에는 대한민국에서 유일하게 경운기 전용 도로가 설치되어 있다
      evidence:
        - doc_id: wiki-ko-gyeongju
          location: "### 기타"
          passage: 대한민국에서 유일하게 경운기 전용 도로가 설치되어 있다.

- id: c-002
  question: 2004년 12월 29일에 개통될 당시 상무지구에서 동림 나들목을 잇는 도시고속도로의 이름은 무엇이었나?
  question_language: ko
  evidence_language: ko
  type: single_fact
  answer: 센다이로
  required_facts:
    - fact: 상무지구에서 동림 나들목을 잇는 도시고속도로는 2004년 12월 29일 개통 당시에 센다이로라고 불렸다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: "### 도로"
          passage: 자매도시간 상호원칙에 따라 2004년 12월 29일에 상무지구에서 동림 나들목을 잇는 도시고속도로인 (개통 당시에는 일반도로였음) 센다이로가 개통되었으나, 광주 관문도로에 명명된 일본식 이름에 대한 부정적인 여론에 따라 지금은 빛고을대로로 변경되었다.

- id: c-003
  question: 2026년 3월 17일 데이터 기준으로 전주시 풍남동의 세대수는 얼마인가?
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 2141세대이다.
  required_facts:
    - fact: 2026년 3월 17일 기준 전주시 풍남동의 세대수는 2141이다
      evidence:
        - doc_id: portal-ko-jeonju-population
          location: "# 전북특별자치도 전주시_인구현황"
          passage: |
            | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
            | 풍남동 | 2141 | 3354 | 1629 | 1725 | 151 | 82 | 69 | 3203 | 1547 | 1656 | 1491 | 615 | 876 | 2026-03-17 |

- id: c-004
  question: 세종특별자치시에서 2020년부터 2025년 사이에 출생아 수가 가장 적었던 연도의 출생아 수는 몇 명인가?
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 2023년의 2,761명이다.
  required_facts:
    - fact: 2020년 세종특별자치시 출생아 수는 3,468명이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "### 인구동태"
          passage: |
            | 연도 | 출생(명) | 사망(명) | 혼인(쌍) | 이혼(쌍) |
            | 2020년 | 3,468 | 1,317 | 1,854 | 601 |
    - fact: 2021년 세종특별자치시 출생아 수는 3,570명이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "### 인구동태"
          passage: |
            | 연도 | 출생(명) | 사망(명) | 혼인(쌍) | 이혼(쌍) |
            | 2021년 | 3,570 | 1,354 | 1,627 | 624 |
    - fact: 2022년 세종특별자치시 출생아 수는 3,209명이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "### 인구동태"
          passage: |
            | 연도 | 출생(명) | 사망(명) | 혼인(쌍) | 이혼(쌍) |
            | 2022년 | 3,209 | 1,678 | 1,664 | 546 |
    - fact: 2023년 세종특별자치시 출생아 수는 2,761명이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "### 인구동태"
          passage: |
            | 연도 | 출생(명) | 사망(명) | 혼인(쌍) | 이혼(쌍) |
            | 2023년 | 2,761 | 1,595 | 1,705 | 569 |
    - fact: 2024년 세종특별자치시 출생아 수는 2,895명이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "### 인구동태"
          passage: |
            | 연도 | 출생(명) | 사망(명) | 혼인(쌍) | 이혼(쌍) |
            | 2024년 | 2,895 | 1,700 | 1,842 | 560 |
    - fact: 2025년 세종특별자치시 출생아 수는 2,960명이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "### 인구동태"
          passage: |
            | 연도 | 출생(명) | 사망(명) | 혼인(쌍) | 이혼(쌍) |
            | 2025년 | 2,960 | 1,632 | 2,003 | 538 |
    - fact: 2020년부터 2025년 사이 중 2023년의 출생아 수가 2,761명으로 가장 적다
      evidence: []

- id: c-005
  question: 수원시와 광주광역시를 상징하는 시조(새)는 각각 무엇인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 수원시는 백로이고, 광주광역시는 비둘기이다.
  required_facts:
    - fact: 수원시의 시조는 백로이다
      evidence:
        - doc_id: wiki-ko-suwon
          location: "# 수원시"
          passage: "- 시조: 백로"
    - fact: 광주광역시의 시조는 비둘기이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: "# 광주광역시"
          passage: "- 시조: 비둘기"

- id: c-006
  question: 세종특별자치시와 수원시의 현재 단체장(시장)은 각각 누구인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 세종특별자치시의 단체장은 조상호이고, 수원시의 단체장은 이재준이다.
  required_facts:
    - fact: 세종특별자치시의 단체장은 조상호이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "# 세종특별자치시"
          passage: "- 단체장: 조상호(더불어민주당)"
    - fact: 수원시의 단체장은 이재준이다
      evidence:
        - doc_id: wiki-ko-suwon
          location: "# 수원시"
          passage: "- 단체장: 이재준(더불어민주당)"

- id: c-007
  question: 브라질에 위치한 수원시의 자매도시와 천안시의 국제 우호교류 도시는 각각 어디인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 수원시의 자매도시는 파라나주 쿠리치바이고, 천안시의 국제 우호교류 도시는 상파울루 주 깜삐나스이다.
  required_facts:
    - fact: 브라질에 위치한 수원시의 자매도시는 파라나주 쿠리치바이다
      evidence:
        - doc_id: wiki-ko-suwon
          location: "## 교류 도시"
          passage: |
            | 자매결연도시 | 지방자치단체 | 지방자치단체 |
            | 자매도시 | 브라질 | 파라나주 쿠리치바 |
    - fact: 브라질에 위치한 천안시의 국제 우호교류 도시는 상파울루 주 깜삐나스이다
      evidence:
        - doc_id: wiki-ko-cheonan
          location: "### 국제 우호교류"
          passage: "- 브라질 상파울루 주 깜삐나스 (2019년)"

- id: c-008
  question: 고려대학교의 캠퍼스 또는 소속 기관 중 세종특별자치시와 청주시에 위치한 것은 각각 무엇인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 세종특별자치시에는 고려대학교 세종캠퍼스가 위치해 있고, 청주시에는 고려대학교 세종캠퍼스 의생명공학원이 위치해 있다.
  required_facts:
    - fact: 세종특별자치시에는 고려대학교 세종캠퍼스가 있다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "## 교육 기관"
          passage: "- 고려대학교 세종캠퍼스"
    - fact: 청주시에는 고려대학교 세종캠퍼스 의생명공학원이 있다
      evidence:
        - doc_id: wiki-ko-cheongju
          location: "#### 사립대학"
          passage: "- 고려대학교 세종캠퍼스 의생명공학원"

- id: c-009
  question: 13세기에 황룡사 9층 목탑을 망가뜨린 군대는 누구인가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 몽골군이다.
  required_facts:
    - fact: 13세기에 몽골군이 황룡사에 있던 9층 목탑을 파괴했다
      evidence:
        - doc_id: wiki-ko-gyeongju
          location: "## 역사"
          passage: 13세기에는 몽골군이 황룡사에 있던 9층 목탑을 파괴했다.

- id: c-010
  question: 광주광역시에 자리 잡고 있는 신문을 발행하는 회사와 방송국은 각각 몇 곳인가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 신문을 발행하는 회사(신문사)는 6개, 방송국(방송사)은 8개이다.
  required_facts:
    - fact: 광주에는 방송사 8개와 신문사 6개가 있다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: "## 주요 기관"
          passage: 광주에는 방송사 8개와 신문사 6개가 있다.

- id: c-011
  question: 한국에서 가장 먼저 세워진 특수목적 고등학교의 이름은 무엇이며, 어느 동에 지어졌는가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 경기과학고등학교이며, 송죽동에 지어졌다.
  required_facts:
    - fact: 대한민국 최초의 특수목적 고등학교는 경기과학고등학교이며 1983년 송죽동에 설립되었다
      evidence:
        - doc_id: wiki-ko-suwon
          location: "### 고등학교"
          passage: "- 1983년 장안구 송죽동에 대한민국 최초의 특수목적 고등학교인 경기과학고등학교가 설립되었다."

- id: c-012
  question: 세종특별자치시가 매일 대전광역시로부터 전달받는 식수의 양은 어느 정도인가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 1일 6만 톤이다.
  required_facts:
    - fact: 세종시는 1일 6만 톤의 대전광역시 수돗물을 공급받게 된다
      evidence:
        - doc_id: wiki-ko-sejong
          location: "## 기반시설"
          passage: 세종시는 1일 6만 톤의 대전광역시 수돗물을 공급받게 된다.

```

c-001: 반대 언어(영어) 문서에서 찾아본 표현 "경운기", "전용 도로" → wiki-en-gyeongju 문서가 존재하지 않아 영어 문서에 같은 사실 없음
c-002: 반대 언어(영어) 문서에서 찾아본 표현 "센다이로", "동림 나들목", "상무지구" → wiki-en-gwangju 문서가 존재하지 않아 영어 문서에 같은 사실 없음
c-003: 반대 언어(영어) 문서에서 찾아본 표현 "Pungnam-dong", "2,141" → wiki-en-jeonju에는 풍남동의 인구나 세대수에 대한 세부 기록이 없어 같은 사실 없음
c-004: 반대 언어(영어) 문서에서 찾아본 표현 "birth", "2023", "2,761" → wiki-en-sejong 문서가 존재하지 않아 영어 문서에 같은 사실 없음
c-005: 반대 언어(영어) 문서에서 찾아본 표현 "bird", "egret", "pigeon" → wiki-en-suwon, wiki-en-gwangju 문서가 모두 존재하지 않아 영어 문서에 같은 사실 없음
c-006: 반대 언어(영어) 문서에서 찾아본 표현 "mayor", "Jo Sang-ho", "Lee Jae-joon" → wiki-en-sejong, wiki-en-suwon 문서가 모두 존재하지 않아 영어 문서에 같은 사실 없음
c-007: 반대 언어(영어) 문서에서 찾아본 표현 "Brazil", "Curitiba", "Campinas" → wiki-en-cheonan의 Sister cities 목록에 브라질 관련 도시가 존재하지 않으며, wiki-en-suwon 문서는 존재하지 않아 같은 사실 없음
c-008: 반대 언어(영어) 문서에서 찾아본 표현 "Korea University" → wiki-en-cheongju의 Education 목록에 관련 대학이 없으며, wiki-en-sejong 문서는 존재하지 않아 같은 사실 없음
c-009: paraphrase 대체 확인(파괴했다 → 망가뜨린) / 반대 언어(영어) 문서에서 찾아본 표현 "Mongol", "pagoda", "Hwangnyongsa" → wiki-en-gyeongju 문서가 존재하지 않아 영어 문서에 같은 사실 없음
c-010: paraphrase 대체 확인(방송사 → 방송국 / 신문사 → 신문을 발행하는 회사 / 있다 → 자리 잡고 있는) / 반대 언어(영어) 문서에서 찾아본 표현 "broadcasting", "newspaper", "8", "6" → wiki-en-gwangju 문서가 존재하지 않아 영어 문서에 같은 사실 없음
c-011: paraphrase 대체 확인(대한민국 최초의 → 한국에서 가장 먼저 세워진 / 설립되었다 → 지어졌는가) / 반대 언어(영어) 문서에서 찾아본 표현 "Gyeonggi Science High School", "Songjuk-dong" → wiki-en-suwon 문서가 존재하지 않아 영어 문서에 같은 사실 없음
c-012: paraphrase 대체 확인(1일 → 매일 / 수돗물 → 식수 / 공급받게 된다 → 전달받는 / 6만 톤 → 어느 정도) / 반대 언어(영어) 문서에서 찾아본 표현 "60,000 tons", "tap water" → wiki-en-sejong 문서가 존재하지 않아 영어 문서에 같은 사실 없음