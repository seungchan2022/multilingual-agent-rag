```yaml
- id: "c-013"
  question: "During Hideyoshi's Invasions of Korea, how many Korean warrior monks participated in the Battle of Cheongju in 1593?"
  question_language: "en"
  evidence_language: "en"
  type: "single_fact"
  answer: "More than 8,000"
  required_facts:
    - fact: "More than 8,000 Korean warrior monks participated in the Battle of Cheongju in 1593."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-cheongju"
          location: "History"
          passage: "In 1593, the Battle of Cheongju took place between Japanese forces and Joseon that then ruled the Korean peninsula during Hideyoshi's Invasions of Korea, in which more than 8,000 Korean warrior monks participated."
  opposite_check:
    - "1593년"
    - "승병"
    - "8,000"
    - "8000명"
    - "청주 전투"
  same_language_check:
    - "1593"
    - "8,000"
    - "warrior monks"
    - "Battle of Cheongju"

- id: "c-014"
  question: "In South Korea, which city is home to a correctional facility specifically designated for non-Korean inmates?"
  question_language: "en"
  evidence_language: "en"
  type: "paraphrase"
  answer: "Cheonan"
  required_facts:
    - fact: "Cheonan is the site of a prison exclusively intended for foreign prisoners."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-cheonan"
          location: "Population diversity"
          passage: "In addition, Cheonan is the site of the prison exclusively intended for foreign prisoners, with more than 1,000 foreign inmates."
  opposite_check:
    - "외국인 교도소"
    - "외국인 수감자"
    - "교도소"
    - "1,000명"
  same_language_check:
    - "exclusively intended for foreign"
    - "foreign prisoners"
    - "foreign inmates"

- id: "c-015"
  question: "Which globally recognized b-boy dance group, known for winning a major international competition, originated in Jeonju?"
  question_language: "en"
  evidence_language: "en"
  type: "paraphrase"
  answer: "Last for One"
  required_facts:
    - fact: "Jeonju is the hometown of the breakdancing crew Last for One, who are international Battle of the Year champions."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-jeonju"
          location: "Attractions"
          passage: "Jeonju is the hometown of the breakdancing crew Last for One, international Battle of the Year champions."
  opposite_check:
    - "라스트 포 원"
    - "배틀 오브 더 이어"
    - "브레이크댄스"
  same_language_check:
    - "Last for One"
    - "Battle of the Year"
    - "breakdancing crew"

- id: "c-016"
  question: "According to the provided documents, how many vehicles were trapped when a tunnel flooded in Cheongju during the annual monsoon, and what is the literal meaning of Cheonan's Samgeori park?"
  question_language: "en"
  evidence_language: "en"
  type: "multi_doc"
  answer: "15 vehicles were trapped in Cheongju, and Samgeori means '3-way intersection'."
  required_facts:
    - fact: "The Cheongju tunnel flooded during the annual monsoon, trapping 15 vehicles."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-cheongju"
          location: "Transport"
          passage: "In 2023, the Cheongju tunnel flooded during the annual monsoon which trapped 15 vehicles and resulted in at least 7 deaths and 11 reported missing."
    - fact: "Cheonan's Samgeori park means '3-way intersection'."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-cheonan"
          location: "History"
          passage: "Cheonan's Samgeori (meaning \"3-way intersection\") park has been noted as a strategic point of transportation and a place where culture has spread for a long time."
  opposite_check:
    - "차량 15대"
    - "15대 고립"
    - "세 거리"
    - "세 갈래"
    - "삼거리"
  same_language_check:
    - "trapped 15 vehicles"
    - "annual monsoon"
    - "3-way intersection"
    - "Samgeori"

- id: "c-017"
  question: "Which city's gallery features an installation of Damien Hirst's 'Hymn' in a glass box, and which city's international music festival was named among Songlines' 25 Best International Festivals in 2014?"
  question_language: "en"
  evidence_language: "en"
  type: "multi_doc"
  answer: "Cheonan features 'Hymn', and Jeonju's festival was named by Songlines."
  required_facts:
    - fact: "Cheonan's Arario Gallery has an installation of Damien Hirst's 'Hymn' in a glass box."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-cheonan"
          location: "Galleries"
          passage: "There is also an installation of Damien Hirst's \"Hymn\" in a glass box constructed as a part of the building."
    - fact: "The Jeonju International Sori Festival was among Songlines' 25 Best International Festivals in 2014."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-jeonju"
          location: "Attractions"
          passage: "The Jeonju International Sori Festival was among Songlines' 25 Best International Festivals in 2014."
  opposite_check:
    - "데미안 허스트"
    - "송라인즈"
    - "유리 상자"
    - "25대 페스티벌"
  same_language_check:
    - "Damien Hirst's"
    - "glass box"
    - "Songlines"
    - "25 Best International Festivals"

- id: "c-018"
  question: "Opened in 2022, Legoland Korea Resort holds what ranking in terms of size among all Legoland theme parks in the world?"
  question_language: "en"
  evidence_language: "en"
  type: "single_fact"
  answer: "It is the 2nd largest in the world."
  required_facts:
    - fact: "Legoland Korea Resort is the 2nd largest Legoland theme park in the world."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-chuncheon"
          location: "Resort"
          passage: "Legoland Korea Resort, the 10th Legoland theme park and the 2nd largest in the world, opened in 2022."
  opposite_check:
    - "레고랜드"
    - "세계 2위"
    - "두 번째로 큰"
    - "10번째"
  same_language_check:
    - "10th Legoland"
    - "2nd largest in the world"
    - "Legoland Korea Resort"

- id: "c-019"
  question: "According to the historical population data for Busan, what was the city's population in 1970?"
  question_language: "en"
  evidence_language: "en"
  type: "table_numeric"
  answer: "1,842,259"
  required_facts:
    - fact: "Busan's population in 1970 was 1,842,259."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-busan"
          location: "Demographics"
          passage: |
            | Year | Pop. | ±% |
            | 1970 | 1,842,259 | +59.6% |
  opposite_check:
    - "1970년 인구"
    - "1,842,259"
    - "1842259"
    - "184만"
  same_language_check:
    - "1970"
    - "1,842,259"
    - "Historical population"

- id: "c-020"
  question: "Based on the administrative divisions of Gangneung, what is the area of Jumunjin-eup in square kilometers?"
  question_language: "en"
  evidence_language: "en"
  type: "table_numeric"
  answer: "60.52"
  required_facts:
    - fact: "The area of Jumunjin-eup is 60.52 km2."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-gangneung"
          location: "Administrative divisions"
          passage: |
            | Name | Korean name | Area(km2) | Population | Households |
            | Jumunjin-eup | 주문진읍 | 60.52 | 19,299 | 9,098 |
  opposite_check:
    - "주문진읍"
    - "60.52"
    - "60.52km2"
  same_language_check:
    - "Jumunjin-eup"
    - "60.52"
    - "Area(km2)"

- id: "c-021"
  question: "Which major Buddhist sanctuary in Jeju features a natural water source that is purportedly therapeutic?"
  question_language: "en"
  evidence_language: "en"
  type: "paraphrase"
  answer: "Yakcheonsa"
  required_facts:
    - fact: "The Buddhist temple Yakcheonsa in Jeju has a natural mineral spring claimed to have healing powers."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-jeju"
          location: "Tourism"
          passage: "The Buddhist temple Yakcheonsa has a natural mineral spring claimed to have healing powers, and is one of the largest temples in East Asia."
  opposite_check:
    - "약천사"
    - "광천수"
    - "치유"
    - "동아시아"
  same_language_check:
    - "Yakcheonsa"
    - "natural mineral spring"
    - "healing powers"
    - "largest temples"

- id: "c-022"
  question: "What seasonal nickname is given to Busan due to the nationwide influx of visitors to its coastal shorelines?"
  question_language: "en"
  evidence_language: "en"
  type: "paraphrase"
  answer: "The summer capital of Korea"
  required_facts:
    - fact: "Busan is called the summer capital of Korea because it attracts tourists from all over the country to its beaches."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-busan"
          location: "Parks, beaches, and highlights"
          passage: "Busan is called the summer capital of Korea, since it attracts tourists from all over the country to its six beaches."
  opposite_check:
    - "여름 수도"
    - "여름의 수도"
    - "여름수도"
    - "해변"
  same_language_check:
    - "summer capital of Korea"
    - "tourists from all over"
    - "six beaches"

- id: "c-023"
  question: "Comparing the climate records of Busan and Jeju City, which city has the higher all-time record high temperature, and what was that temperature in Celsius?"
  question_language: "en"
  evidence_language: "en"
  type: "multi_doc"
  answer: "Busan has the higher record, at 38.8 °C."
  required_facts:
    - fact: "Busan's highest temperature ever recorded is 38.8 °C."
      in_answer: false
      evidence:
        - doc_id: "wiki-en-busan"
          location: "Climate"
          passage: "The highest temperature ever recorded is 38.8 °C (101.8 °F) on 29 July 2026, while the lowest temperature ever recorded is −14.0 °C (6.8 °F) on 13 January 1915."
    - fact: "Jeju City's highest temperature ever recorded is 37.5 °C."
      in_answer: false
      evidence:
        - doc_id: "wiki-en-jeju"
          location: "Climate"
          passage: "The highest temperature ever recorded is 37.5 °C (99.5 °F) on 25 July 1942 while the lowest temperature ever recorded is −6.0 °C (21.2 °F) on 16 February 1977."
    - fact: "Busan's highest temperature (38.8 °C) is higher than Jeju City's highest temperature (37.5 °C)."
      in_answer: true
      evidence: []
  opposite_check:
    - "38.8"
    - "37.5"
    - "역대 최고 기온"
    - "38.8도"
  same_language_check:
    - "38.8 °C"
    - "37.5 °C"
    - "Record high"

- id: "c-024"
  question: "Name the sister cities of Andong and Gangneung that are located in China."
  question_language: "en"
  evidence_language: "en"
  type: "multi_doc"
  answer: "Andong's sister cities in China are Pingdingshan and Xi'an. Gangneung's sister city in China is Mangshi (in Yunnan)."
  required_facts:
    - fact: "Andong has a sister city relationship with Pingdingshan and Xi'an in China."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-andong"
          location: "Sister cities"
          passage: "- Pingdingshan, China"
        - doc_id: "wiki-en-andong"
          location: "Sister cities"
          passage: "- Xi'an, China"
    - fact: "Gangneung's sister city in China is Mangshi, Yunnan."
      in_answer: true
      evidence:
        - doc_id: "wiki-en-gangneung"
          location: "Sister cities"
          passage: "- Mangshi, Yunnan, China, since November 21, 2012"
  opposite_check:
    - "망시"
    - "윈난성"
    - "핑딩산"
    - "시안"
    - "중국 자매도시"
  same_language_check:
    - "Mangshi"
    - "Pingdingshan"
    - "Xi'an"
    - "Yunnan"
    - "Sister cities"

```

c-014: "prison exclusively intended for foreign prisoners"를 "correctional facility specifically designated for non-Korean inmates"로 바꿈.
c-015: "breakdancing crew"를 "b-boy dance group"으로, "international Battle of the Year champions"를 "winning a major international competition"으로, "hometown"을 "originated in"으로 바꿈.
c-021: "temple"을 "sanctuary"로, "natural mineral spring claimed to have healing powers"를 "natural water source that is purportedly therapeutic"으로 바꿈.
c-022: "summer capital of Korea"를 "seasonal nickname"으로, "tourists from all over the country to its six beaches"를 "nationwide influx of visitors to its coastal shorelines"로 바꿈.