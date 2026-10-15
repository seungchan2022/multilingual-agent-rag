```yaml
- id: c-001
  question: 세종특별자치시의 시화는 무엇인가
  question_language: ko
  evidence_language: ko
  type: single_fact
  answer: 복사꽃이다
  required_facts:
    - fact: 세종특별자치시의 시화는 복사꽃이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: 세종특별자치시
          passage: "- 시화: 복사꽃"

- id: c-002
  question: 전라북도 전주시가 전북특별자치도 전주시로 개편된 날짜는 언제인가
  question_language: ko
  evidence_language: ko
  type: single_fact
  answer: 2024년 1월 18일이다
  required_facts:
    - fact: 전라북도 전주시가 전북특별자치도 전주시로 개편된 날짜는 2024년 1월 18일이다
      evidence:
        - doc_id: wiki-ko-jeonju
          location: 대한민국
          passage: "- 2024년 1월 18일 : 전라북도 전주시에서 전북특별자치도 전주시로 개편되었다."

- id: c-003
  question: 2021년 5월 31일 기준으로 수원시 팔달구 행궁동의 여성 외국인 수는 몇 명인가
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 375명이다
  required_facts:
    - fact: 2021년 5월 31일 기준 수원시 팔달구 행궁동의 여성 외국인은 375명이다
      evidence:
        - doc_id: portal-ko-suwon-population
          location: 경기도 수원시_인구현황
          passage: |
            | 구 | 구_동 | 세대수 | 인구_합계 | 인구_내국인_인구수_계 | 인구_내국인_인구수_남 | 인구_내국인_인구수_여 | 인구_내국인_전월말인구수 | 인구_내국인_인구증감전월대비 | 외국인_계 | 외국인_남 | 외국인_여 | 데이터기준일자 |
            | 팔달구 | 행궁동 | 6654 | 11541 | 10682 | 5704 | 4978 | 11527 | 14 | 859 | 484 | 375 | 2021-05-31 |

- id: c-004
  question: 2026년 3월 17일 기준 전주시 완산동의 세대수는 얼마인가
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 2530이다
  required_facts:
    - fact: 2026년 3월 17일 기준 전주시 완산동의 세대수는 2530이다
      evidence:
        - doc_id: portal-ko-jeonju-population
          location: 전북특별자치도 전주시_인구현황
          passage: |
            | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
            | 완산동 | 2530 | 4686 | 2285 | 2401 | 452 | 250 | 202 | 4234 | 2035 | 2199 | 1622 | 667 | 955 | 2026-03-17 |

- id: c-005
  question: 광주외곽순환고속도로(제3순환도로)가 공사를 시작한 날짜는 언제인가
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 2015년 12월 23일이다
  required_facts:
    - fact: 광주외곽순환고속도로(제3순환도로)가 착공된 날짜는 2015년 12월 23일이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 도로
          passage: "2015년 12월 23일에 광주외곽순환고속도로(제3순환도로)가 착공되어 2022년 12월에 개통됐다."

- id: c-006
  question: 경주실업전문대학이 문을 연 달은 언제인가
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 1981년 3월이다
  required_facts:
    - fact: 경주실업전문대학이 개교한 시기는 1981년 3월이다
      evidence:
        - doc_id: wiki-ko-gyeongju
          location: 교육
          passage: "1981년 1월 설립자인 김일윤이고, 학교법인 원석학원의 설립하여, 같은 해 3월 경주실업전문대학을 개교했다."

- id: c-007
  question: 1999년 춘천시 조례 제338호에 따라 신동면 정족리의 일부와 온의동의 일부 지역은 어느 동으로 들어갔는가
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 칠전동이다
  required_facts:
    - fact: 1999년 춘천시 조례 제338호로 신동면 정족리 일부와 온의동 일부가 칠전동에 편입되었다
      evidence:
        - doc_id: wiki-ko-chuncheon
          location: 역사
          passage: "- 1999년 : 춘천시 조례 제338호로 신동면 정족리 일부와 온의동 일부를 칠전동에 편입하였다."

- id: c-008
  question: 2012년 7월 1일 청원군 부용면에서 세종특별자치시로 편입되지 않고 남은 외천리는 남이면에 편입되면서 어떤 이름으로 바꾸었는가
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 부용외천리이다
  required_facts:
    - fact: 2012년 7월 1일 청원군 부용면의 남은 1개리인 외천리는 남이면에 편입되어 부용외천리로 개칭되었다
      evidence:
        - doc_id: wiki-ko-cheongju
          location: 연혁
          passage: "- 2012년 7월 1일 청원군 부용면 9개리 중 8개리를 세종특별자치시로 편입하고, 남는 1개리(외천리)를 남이면에 편입하여 부용외천리로 개칭하였다. (3읍 10면)"

- id: c-009
  question: 광주광역시의 시조와 세종특별자치시의 시조는 각각 무엇인가
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 광주광역시는 비둘기이고, 세종특별자치시는 파랑새이다
  required_facts:
    - fact: 광주광역시의 시조는 비둘기이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 광주광역시
          passage: "- 시조: 비둘기"
    - fact: 세종특별자치시의 시조는 파랑새이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: 세종특별자치시
          passage: "- 시조: 파랑새"
    - fact: 광주광역시의 시조는 비둘기이고 세종특별자치시의 시조는 파랑새이다
      evidence: []

- id: c-010
  question: 수원시와 경주시의 시목은 공통적으로 무엇인가
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 소나무이다
  required_facts:
    - fact: 수원시의 시목은 소나무이다
      evidence:
        - doc_id: wiki-ko-suwon
          location: 수원시
          passage: "- 시목: 소나무"
    - fact: 경주시의 시목(나무)은 소나무이다
      evidence:
        - doc_id: wiki-ko-gyeongju
          location: 경주시
          passage: "- 나무: 소나무"
    - fact: 수원시와 경주시의 시목은 소나무로 같다
      evidence: []

- id: c-011
  question: 청주시의 시목과 춘천시의 시목(나무)은 각각 무엇인가
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 청주시는 느티나무이고, 춘천시는 은행나무이다
  required_facts:
    - fact: 청주시의 시목은 느티나무이다
      evidence:
        - doc_id: wiki-ko-cheongju
          location: 청주시
          passage: "- 시목: 느티나무"
    - fact: 춘천시의 나무는 은행나무이다
      evidence:
        - doc_id: wiki-ko-chuncheon
          location: 춘천시
          passage: "- 나무: 은행나무"
    - fact: 청주시의 시목은 느티나무이고 춘천시의 나무는 은행나무이다
      evidence: []

- id: c-012
  question: 전주시를 상징하는 동물과 청주시의 시조는 각각 무엇인가
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 전주시는 독수리이고, 청주시는 까치이다
  required_facts:
    - fact: 전주시의 동물은 독수리이다
      evidence:
        - doc_id: wiki-ko-jeonju
          location: 전주시
          passage: "- 동물: 독수리"
    - fact: 청주시의 시조는 까치이다
      evidence:
        - doc_id: wiki-ko-cheongju
          location: 청주시
          passage: "- 시조: 까치"
    - fact: 전주시의 동물은 독수리이고 청주시의 시조는 까치이다
      evidence: []

```

c-001: 찾을 말(반대 언어) "시화", "꽃", "복사꽃", "flower", "peach" -> 반대 언어 문서 14개에서 걸린 곳: 없음(세종 영어 문서 없음) -> 같은 사실 없음
c-002: 찾을 말(반대 언어) "개편", "2024년 1월 18일", "2024", "January 18" -> 반대 언어 문서 14개에서 걸린 곳: wiki-en-jeonju 등 전주 관련 영어 문서를 살펴보았으나 해당 개편 날짜 언급 없음 -> 같은 사실 없음
c-003: 찾을 말(반대 언어) "행궁동", "여성", "외국인", "375", "Haenggung", "female", "foreigner" -> 반대 언어 문서 14개에서 걸린 곳: 없음(수원 영어 문서 없음) -> 같은 사실 없음
c-004: 찾을 말(반대 언어) "완산동", "세대수", "2530", "Wansan", "household" -> 반대 언어 문서 14개에서 걸린 곳: wiki-en-jeonju 등 전주 관련 영어 문서에 해당 통계 표 없음 -> 같은 사실 없음
c-005: 찾을 말(반대 언어) "광주외곽순환고속도로", "제3순환도로", "2015년 12월 23일", "착공", "highway", "Dec 23, 2015" -> 반대 언어 문서 14개에서 걸린 곳: 없음(광주 영어 문서 없음) -> 같은 사실 없음 (확인 메모: 질문에서 "착공"을 "공사를 시작한"으로 바꿈)
c-006: 찾을 말(반대 언어) "경주실업전문대학", "1981년 3월", "개교", "college", "March 1981" -> 반대 언어 문서 14개에서 걸린 곳: 없음(경주 영어 문서 없음) -> 같은 사실 없음 (확인 메모: 질문에서 "개교"를 "문을 연"으로 바꿈)
c-007: 찾을 말(반대 언어) "조례 제338호", "신동면", "정족리", "칠전동", "ordinance", "Chiljeon", "Jeongjok" -> 반대 언어 문서 14개에서 걸린 곳: wiki-en-chuncheon에 해당 조례 및 편입 내용 없음 -> 같은 사실 없음 (확인 메모: 질문에서 "편입"을 "들어갔는가"로 바꿈)
c-008: 찾을 말(반대 언어) "외천리", "부용외천리", "남이면", "개칭", "Oaecheon", "Buyong" -> 반대 언어 문서 14개에서 걸린 곳: wiki-en-cheongju에 해당 행정구역 개편 내용 없음 -> 같은 사실 없음 (확인 메모: 질문에서 "개칭"을 "이름으로 바꾸었는가"로 바꿈)
c-009: 찾을 말(반대 언어) "시조", "비둘기", "파랑새", "bird", "dove", "bluebird" -> 반대 언어 문서 14개에서 걸린 곳: 없음(광주, 세종 영어 문서 없음) -> 같은 사실 없음
c-010: 찾을 말(반대 언어) "시목", "나무", "소나무", "tree", "pine" -> 반대 언어 문서 14개에서 걸린 곳: 없음(수원, 경주 영어 문서 없음) -> 같은 사실 없음
c-011: 찾을 말(반대 언어) "느티나무", "은행나무", "tree", "zelkova", "ginkgo" -> 반대 언어 문서 14개에서 걸린 곳: wiki-en-cheongju, wiki-en-chuncheon 모두 시목(나무)에 대한 언급 없음 -> 같은 사실 없음
c-012: 찾을 말(반대 언어) "동물", "독수리", "까치", "eagle", "magpie", "animal", "bird" -> 반대 언어 문서 14개에서 걸린 곳: wiki-en-jeonju, wiki-en-cheongju 모두 동물/새에 대한 언급 없음 -> 같은 사실 없음