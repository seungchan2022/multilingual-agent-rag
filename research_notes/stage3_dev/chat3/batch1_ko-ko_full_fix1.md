```yaml
- id: c-001
  question: 춘천경공업단지가 조성되기 시작한 연도는 언제인가?
  question_language: ko
  evidence_language: ko
  type: single_fact
  answer: 1969년
  required_facts:
    - fact: 춘천경공업단지는 1969년부터 조성되었다
      evidence:
        - doc_id: wiki-ko-chuncheon
          location: 경제
          passage: 1969년부터 춘천경공업단지가 조성되었으며, 73년 5월 공업장려지구로 지정되었다.
  opposite_check:
    - term: 1969
      hits:
        - doc_id: wiki-en-chuncheon
          excerpt: "The lowest measured temperature was −27.9 °C (−18 °F) (6 February 1969), and the highest was 39.5 °C (103 °F) (1 August 2018)."
          same_fact: false
          why: 1969년이라는 연도가 아니라, 최저 기온이 관측된 날짜(1969년 2월 6일)를 설명하는 내용 중 일부로 쓰였음
        - doc_id: wiki-en-busan
          excerpt: "- Kim Wonhae (born 1969), actor and comedian"
          same_fact: false
          why: 배우 김원해의 출생 연도를 나타냄
    - term: Chuncheon Light Industrial Complex
      hits: []
    - term: Light Industrial
      hits: []

- id: c-002
  question: 세종특별자치시를 상징하는 시조(새)는 무엇인가?
  question_language: ko
  evidence_language: ko
  type: single_fact
  answer: 파랑새
  required_facts:
    - fact: 세종특별자치시의 시조는 파랑새이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: 첫 부분
          passage: "- 시조: 파랑새"
  opposite_check:
    - term: Bluebird
      hits: []
    - term: Parangsae
      hits: []
    - term: City bird
      hits:
        - doc_id: wiki-en-busan
          excerpt: "The mascot was a seagull, the city bird of Busan named, \"Duria\". East Timor took part in the games for the first time."
          same_fact: false
          why: 부산광역시의 상징 새에 대한 내용임
        - doc_id: wiki-en-cheonan
          excerpt: "- City Bird: Dove"
          same_fact: false
          why: 천안시의 상징 새에 대한 내용임

- id: c-003
  question: 2021년 5월 31일 데이터 기준으로, 수원시 팔달구 고등동의 외국인 계(합계) 인구수는 몇 명인가?
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 2849명
  required_facts:
    - fact: 2021년 5월 31일 기준 수원시 팔달구 고등동의 외국인 계 인구수는 2849명이다
      evidence:
        - doc_id: portal-ko-suwon-population
          location: 첫 부분
          passage: |
            | 구 | 구_동 | 세대수 | 인구_합계 | 인구_내국인_인구수_계 | 인구_내국인_인구수_남 | 인구_내국인_인구수_여 | 인구_내국인_전월말인구수 | 인구_내국인_인구증감전월대비 | 외국인_계 | 외국인_남 | 외국인_여 | 데이터기준일자 |
            | 팔달구 | 고등동 | 8991 | 21931 | 19082 | 9630 | 9452 | 21445 | 486 | 2849 | 1562 | 1287 | 2021-05-31 |
  opposite_check:
    - term: Godeung-dong
      hits: []
    - term: 2849
      hits: []
    - term: 21931
      hits: []

- id: c-004
  question: 2026년 3월 17일 기준 전주시 효자4동의 65세 이상 인구수 합계(계)는 몇 명인가?
  question_language: ko
  evidence_language: ko
  type: table_numeric
  answer: 4917명
  required_facts:
    - fact: 2026년 3월 17일 기준 전주시 효자4동의 65세 이상 인구수 계는 4917명이다
      evidence:
        - doc_id: portal-ko-jeonju-population
          location: 첫 부분
          passage: |
            | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
            | 효자4동 | 17120 | 38687 | 18784 | 19903 | 7219 | 3648 | 3571 | 31468 | 15136 | 16332 | 4917 | 2184 | 2733 | 2026-03-17 |
  opposite_check:
    - term: Hyoja4-dong
      hits: []
    - term: Hyoja-4-dong
      hits: []
    - term: 4917
      hits: []

- id: c-005
  question: 수원시와 세종특별자치시의 시화(시의 꽃)를 각각 무엇인지 쓰시오.
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 수원시는 진달래, 세종특별자치시는 복사꽃이다
  required_facts:
    - fact: 수원시의 시화는 진달래이다
      evidence:
        - doc_id: wiki-ko-suwon
          location: 첫 부분
          passage: "- 시화: 진달래"
    - fact: 세종특별자치시의 시화는 복사꽃이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: 첫 부분
          passage: "- 시화: 복사꽃"
  opposite_check:
    - term: City flower
      hits:
        - doc_id: wiki-en-cheonan
          excerpt: "- City Flower: Golden bell flower"
          same_fact: false
          why: 천안시의 시화에 대한 내용임
    - term: Azalea
      hits: []
    - term: Peach blossom
      hits: []

- id: c-006
  question: 춘천시와 청주시의 시조(시를 상징하는 새)는 각각 무엇인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 춘천시는 산까치, 청주시는 까치이다
  required_facts:
    - fact: 춘천시의 시조(새)는 산까치이다
      evidence:
        - doc_id: wiki-ko-chuncheon
          location: 첫 부분
          passage: "- 새: 산까치"
    - fact: 청주시의 시조는 까치이다
      evidence:
        - doc_id: wiki-ko-cheongju
          location: 첫 부분
          passage: "- 시조: 까치"
  opposite_check:
    - term: City bird
      hits:
        - doc_id: wiki-en-cheonan
          excerpt: "- City Bird: Dove"
          same_fact: false
          why: 천안시의 상징 새에 대한 내용임
        - doc_id: wiki-en-busan
          excerpt: "The mascot was a seagull, the city bird of Busan named, \"Duria\". East Timor took part in the games for the first time."
          same_fact: false
          why: 부산광역시의 상징 새에 대한 내용임
    - term: Magpie
      hits: []
    - term: Mountain magpie
      hits: []

- id: c-007
  question: 광주광역시의 5개 자치구 중에서 세대 수가 가장 많은 구와 가장 적은 구는 각각 어디인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 가장 많은 구는 북구이고 가장 적은 구는 동구이다
  required_facts:
    - fact: 동구의 세대 수는 45,860이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 행정 구역
          passage: |
            | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
            | 동구 | 東區 | 45,860 | 98,784 | 49.2 |
    - fact: 서구의 세대 수는 120,107이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 행정 구역
          passage: |
            | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
            | 서구 | 西區 | 120,107 | 305,028 | 47.78 |
    - fact: 남구의 세대 수는 87,514이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 행정 구역
          passage: |
            | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
            | 남구 | 南區 | 87,514 | 220,165 | 61.01 |
    - fact: 북구의 세대 수는 178,735이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 행정 구역
          passage: |
            | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
            | 북구 | 北區 | 178,735 | 446,316 | 120.29 |
    - fact: 광산구의 세대 수는 148,252이다
      evidence:
        - doc_id: wiki-ko-gwangju
          location: 행정 구역
          passage: |
            | 자치구 | 한자 | 세대 | 인구 (명) | 면적 (km2) |
            | 광산구 | 光山區 | 148,252 | 400,753 | 222.9 |
    - fact: 광주광역시 5개 자치구 중 세대 수가 가장 많은 곳은 북구, 가장 적은 곳은 동구이다
      evidence: []
  opposite_check:
    - term: 178,735
      hits: []
    - term: 45,860
      hits: []
    - term: Buk-gu
      hits:
        - doc_id: wiki-en-busan
          excerpt: "List Jeon Jaesoo (Democratic) Buk-gu / Gangseo-gu A district,"
          same_fact: false
          why: 국회의원 지역구 이름의 일부임
        - doc_id: wiki-en-busan
          excerpt: "Kim Do-eup (People Power) Buk-gu / Gangseo-gu B district, Suh Byung-soo (People Power)"
          same_fact: false
          why: 국회의원 지역구 이름의 일부임

- id: c-008
  question: 2026년 3월 17일을 기준으로, 전주시 노송동과 완산동의 18세미만인구수(계)를 합하면 총 몇 명인가?
  question_language: ko
  evidence_language: ko
  type: multi_doc
  answer: 1342명
  required_facts:
    - fact: 2026년 3월 17일 기준 전주시 노송동의 18세미만인구수(계)는 890명이다
      evidence:
        - doc_id: portal-ko-jeonju-population
          location: 첫 부분
          passage: |
            | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
            | 노송동 | 5286 | 9970 | 4858 | 5112 | 890 | 472 | 418 | 9080 | 4386 | 4694 | 3380 | 1418 | 1962 | 2026-03-17 |
    - fact: 2026년 3월 17일 기준 전주시 완산동의 18세미만인구수(계)는 452명이다
      evidence:
        - doc_id: portal-ko-jeonju-population
          location: 첫 부분
          passage: |
            | 구분 | 세대수 | 인구수(계) | 인구수(남) | 인구수(여) | 18세미만인구수(계) | 18세미만인구수(남) | 18세미만인구수(여) | 18세이상인구수(계) | 18세이상인구수(남) | 18세이상인구수(여) | 65세이상인구수(계) | 65세이상인구수(남) | 65세이상인구수(여) | 데이터기준일자 |
            | 완산동 | 2530 | 4686 | 2285 | 2401 | 452 | 250 | 202 | 4234 | 2035 | 2199 | 1622 | 667 | 955 | 2026-03-17 |
    - fact: 노송동과 완산동의 18세미만인구수를 더하면 총 1342명이다
      evidence: []
  opposite_check:
    - term: Nosong-dong
      hits: []
    - term: Wansan-dong
      hits: []
    - term: 1342
      hits: []

- id: c-009
  question: 경상북도에 속한 시·군 중에서 땅 넓이 기준으로 안동시 다음으로 큰 곳은 어디인가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 경주시
  required_facts:
    - fact: 경상북도에서 안동시에 이어 두 번째로 넓은 기초자치단체는 경주시이다
      evidence:
        - doc_id: wiki-ko-gyeongju
          location: 행정 구역
          passage: 경주시의 행정구역 면적은 1,324.41km2로, 경상북도에서 안동시에 이어 두 번째로 넓은 기초자치단체이다.
  opposite_check:
    - term: second largest
      hits:
        - doc_id: wiki-en-busan
          excerpt: "Busan is the second largest city in Korea, a maritime logistics hub, and a world-class mega port, it acts as a gateway to the Eurasian continent."
          same_fact: false
          why: 부산이 한국에서 두 번째로 큰 도시라는 내용임
        - doc_id: wiki-en-jeju
          excerpt: "A bus ride from Jeju City to Seogwipo (the second largest city on the island) is typically an hour."
          same_fact: false
          why: 서귀포가 제주도에서 두 번째로 큰 도시라는 내용임
        - doc_id: wiki-en-gangneung
          excerpt: "Gyeongpo Lake is the second largest lagoon in the east coast. Its size has shrunk due to continuous development since the early 20th century."
          same_fact: false
          why: 경포호가 동해안에서 두 번째로 큰 석호라는 내용임
    - term: after Andong
      hits: []
    - term: 1,324.41
      hits: []

- id: c-010
  question: 고려시대 망이·망소이의 난이 일어났을 때 명학소민들에 의해 전소된, 길을 오가는 사람들의 편의를 도모할 목적으로 만들어졌던 천안 직산군 지역의 시설 이름은 무엇인가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 홍경원
  required_facts:
    - fact: 고려시대에 직산군에 교통의 편의를 위해 설치되었던 홍경원은 망이·망소이의 난 때 명학소민들이 불태웠다
      evidence:
        - doc_id: wiki-ko-cheonan
          location: 역사
          passage: 직산군은 고려시대에 홍경원이 설치되어 있던 곳으로, 본래 교통의 편의를 위해 설치되었던 홍경원은 막강한 경제력을 행사하였던 것으로 추측되는데, 망이·망소이의 난 때에는 명학소민들이 홍경원을 불태우고,
  opposite_check:
    - term: Honggyeongwon
      hits: []
    - term: Mang-i
      hits: []
    - term: Myeonghakso
      hits: []

- id: c-011
  question: 대한민국에서 내부에 시, 군, 구 같은 하급 지자체를 전혀 포함하지 않고 단독으로 운영되는 광역 단위 특별자치시의 명칭은 무엇인가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 세종특별자치시
  required_facts:
    - fact: 세종특별자치시는 하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제 광역지방자치단체이다
      evidence:
        - doc_id: wiki-ko-sejong
          location: 행정 구역
          passage: 세종특별자치시는 하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제 광역지방자치단체로
  opposite_check:
    - term: single-tier
      hits: []
    - term: basic local government
      hits: []
    - term: without lower-level
      hits: []

- id: c-012
  question: 과거 완산으로 불렸던 지역을 두고 《삼국사기》 지리지 백제편에서는 어떠한 별명을 달아 놓았는가?
  question_language: ko
  evidence_language: ko
  type: paraphrase
  answer: 비사벌
  required_facts:
    - fact: 《삼국사기》 지리지 백제편에서 전주(완산)의 별칭이 '비사벌'이라고 주(註)를 달았다
      evidence:
        - doc_id: wiki-ko-jeonju
          location: 지명 유래
          passage: 전주는 '비사벌'이라고 불리기도 했다. 이는 《삼국사기》의 지리지 백제편에서 완산의 별칭이 '비사벌'이라고 주(註)를 달았기 때문이다.
  opposite_check:
    - term: Bisabeol
      hits: []
    - term: Samguk Sagi
      hits: []
    - term: Wansan
      hits:
        - doc_id: wiki-en-jeonju
          excerpt: "Jeonju is divided into two wards, Deokjin District and Wansan District that, in turn, are divided into approximately 40 neighborhoods."
          same_fact: false
          why: 전주시 완산구에 대한 내용임
        - doc_id: wiki-en-jeonju
          excerpt: "In 892 (or 900), Gyeon Hwon renamed the city Wansan and established it as the capital of the Later Baekje kingdom."
          same_fact: false
          why: 견훤이 전주의 이름을 완산으로 바꾸었다는 내용임
        - doc_id: wiki-en-jeonju
          excerpt: "From Wansan, Gyeon Hwon campaigned against Silla which climaxed with the destruction of Geumseong (the capital of the Silla kingdom) and the assassination of King Gyeongae in 927."
          same_fact: false
          why: 완산에서 신라에 대항하여 작전을 펼쳤다는 내용임
        - doc_id: kto-en-jeonju-hanok-village
          excerpt: "Address: 99 Girin-daero, Wansan-gu, Jeonju-si, Jeonbuk-do"
          same_fact: false
          why: 주소의 일부인 완산구를 나타냄

```

c-009: "땅 넓이 기준"을 "면적"으로, "다음으로 큰 곳"을 "이어 두 번째로 넓은"으로 바꿈
c-010: "길을 오가는 사람들의 편의를 도모할 목적으로 만들어졌던"을 "교통의 편의를 위해 설치되었던"으로, "전소된"을 "불태우고"로 바꿈
c-011: "내부에 시, 군, 구 같은 하급 지자체를 전혀 포함하지 않고 단독으로 운영되는"을 "하위 행정구역으로 시·군·구의 기초지방자치단체를 두지 않는 단층제"로 바꿈
c-012: "어떠한 별명을 달아 놓았는가"를 "별칭이 '비사벌'이라고 주(註)를 달았기 때문이다"로 바꿈