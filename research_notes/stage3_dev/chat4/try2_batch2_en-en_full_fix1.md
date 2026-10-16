```yaml
- id: c-013
  question: How many Korean warrior monks participated in the Battle of Cheongju in 1593?
  question_language: en
  evidence_language: en
  type: single_fact
  answer: More than 8,000.
  required_facts:
    - fact: In 1593, the Battle of Cheongju took place, in which more than 8,000 Korean warrior monks participated.
      evidence:
        - doc_id: wiki-en-cheongju
          location: History
          passage: "In 1593, the Battle of Cheongju took place between Japanese forces and Joseon that then ruled the Korean peninsula during Hideyoshi's Invasions of Korea, in which more than 8,000 Korean warrior monks participated."
  opposite_check:
    - term: "승군"
      hits: []
    - term: "승병"
      hits: []
    - term: "1593년"
      hits: []
  same_language_check:
    - term: "warrior monks"
      hits: []
    - term: "1593"
      hits: []
    - term: "8,000 Korean"
      hits: []

- id: c-014
  question: In which year did the dancing festival that means "pleasure and joy" in Cheonan attain the status of "promising"?
  question_language: en
  evidence_language: en
  type: paraphrase
  answer: 2007.
  required_facts:
    - fact: The festival in Cheonan meaning "pleasure and joy" attained the status of "promising" in 2007.
      evidence:
        - doc_id: wiki-en-cheonan
          location: Festivals
          passage: "Cheonan's most well-known festival is Heungtaryeong Festival (흥타령 축제). 흥 means pleasure and joy in the Korean language, and usually refers to Korean music."
        - doc_id: wiki-en-cheonan
          location: Festivals
          passage: "The festival started in 2003 and it received the position of \"prepared\" and \"promising\" in 2006 and 2007, respectively."
  opposite_check:
    - term: "유망"
      hits: []
    - term: "흥타령"
      hits:
        - doc_id: wiki-ko-cheonan
          excerpt: "- 천안 흥타령 축제"
          same_fact: false
          why: 축제 이름만 나열되어 있을 뿐 2007년에 유망축제로 지정되었다는 사실이 없다
        - doc_id: kto-ko-cheonan-samgeori-park
          excerpt: "조선 시대부터 한양과 경상도, 전라도를 잇는 삼남대로의 분기점이자 민요 흥타령으로 유명한"
          same_fact: false
          why: 민요 이름으로 쓰였을 뿐 2007년 축제 지정 사실이 아니다
    - term: "기쁨과 즐거움"
      hits: []
  same_language_check:
    - term: "promising"
      hits: []
    - term: "pleasure and joy"
      hits: []
    - term: "2007"
      hits:
        - doc_id: wiki-en-busan
          excerpt: "- Shenzhen, China (2007)\n- Tianjin, China (2007)"
          same_fact: false
          why: 부산의 자매결연 연도이다
        - doc_id: wiki-en-andong
          excerpt: "In the late 1990s and early 2000s it became a tourism"
          same_fact: false
          why: 안동 관광 설명이며 2007년이 아니다

- id: c-015
  question: Which international magazine listed a festival from Jeonju among its 25 best in 2014, and what was the name of the Japanese prefecture that caused Chuncheon to protest in March 2005?
  question_language: en
  evidence_language: en
  type: multi_doc
  answer: The magazine is Songlines, and the prefecture is Shimane Prefecture.
  required_facts:
    - fact: The Jeonju International Sori Festival was among Songlines' 25 Best International Festivals in 2014.
      evidence:
        - doc_id: wiki-en-jeonju
          location: Attractions
          passage: "The Jeonju International Sori Festival was among Songlines' 25 Best International Festivals in 2014."
    - fact: In March 2005, Chuncheon sent letters of protest to its sister cities in Japan due to the enactment of "Day of Takeshima" in Shimane Prefecture.
      evidence:
        - doc_id: wiki-en-chuncheon
          location: Sister cities
          passage: "In March 2005, Chuncheon sent letters of protest to its sister cities in Japan (Kakamigahara, Higashichikuma, and Hofu) and indefinitely postponed culture exchange events in protest of the enactment of \"Day of Takeshima\" in Shimane Prefecture."
    - fact: The magazine is Songlines, and the prefecture is Shimane Prefecture.
      evidence: []
  opposite_check:
    - term: "송라인즈"
      hits: []
    - term: "시마네"
      hits: []
    - term: "다케시마"
      hits: []
  same_language_check:
    - term: "Songlines"
      hits: []
    - term: "Shimane"
      hits: []
    - term: "Takeshima"
      hits: []

- id: c-016
  question: According to the sister cities table, in what year did Cheongju establish a sister city relationship with Bellingham?
  question_language: en
  evidence_language: en
  type: table_numeric
  answer: 2008.
  required_facts:
    - fact: Cheongju established a sister city relationship with Bellingham in 2008.
      evidence:
        - doc_id: wiki-en-cheongju
          location: Twin towns – sister cities
          passage: |
            | City | Prefecture/Province/State | Country | Year |
            | Bellingham | Washington | United States | 2008 |
  opposite_check:
    - term: "벨링엄"
      hits: []
    - term: "벨링햄"
      hits: []
    - term: "벨링헴"
      hits:
        - doc_id: wiki-ko-cheongju
          excerpt: "| 미국 | 워싱턴주 | 벨링헴 |"
          same_fact: false
          why: 표에 도시 이름만 있고 2008년이라는 연도 값이 없다
  same_language_check:
    - term: "Bellingham"
      hits: []
    - term: "Washington"
      hits: []
    - term: "2008"
      hits:
        - doc_id: wiki-en-busan
          excerpt: "- Saint Petersburg, Russia (2008)"
          same_fact: false
          why: 부산의 자매도시 결연 연도이다

- id: c-017
  question: In what year did the biggest puppet festival in South Korea, located in Chuncheon, begin, and what was the population of Cheongju in 1970 before it almost quadrupled by 2000?
  question_language: en
  evidence_language: en
  type: multi_doc
  answer: The festival began in 1989, and the population of Cheongju in 1970 was 147,000.
  required_facts:
    - fact: Chuncheon Puppet Festival, which is the biggest puppet festival in South Korea, began in 1989.
      evidence:
        - doc_id: wiki-en-chuncheon
          location: Festivals
          passage: "Chuncheon Puppet Festival, which began in 1989, is the biggest puppet festival in South Korea."
    - fact: The population of Cheongju in 1970 was 147,000 before it almost quadrupled by 2000.
      evidence:
        - doc_id: wiki-en-cheongju
          location: History
          passage: "Cheongju experienced one of the largest population growths in Korea, having almost quadrupled its population from 147,000 in 1970 to 582,158 in 2000."
    - fact: The festival began in 1989, and the population of Cheongju in 1970 was 147,000.
      evidence: []
  opposite_check:
    - term: "인형극제"
      hits:
        - doc_id: wiki-ko-chuncheon
          excerpt: "- 춘천인형극제"
          same_fact: false
          why: 이름만 있을 뿐 1989년에 시작했다는 연도 값이 없다
    - term: "147,000"
      hits: []
    - term: "147000"
      hits: []
  same_language_check:
    - term: "Puppet Festival"
      hits: []
    - term: "147,000"
      hits: []
    - term: "quadrupled"
      hits: []

- id: c-018
  question: Which institution in Jeonju was constructed between 1908 and 1914 by a French cleric named Xavier Baudonet?
  question_language: en
  evidence_language: en
  type: paraphrase
  answer: Jeongdong Catholic Church.
  required_facts:
    - fact: Jeongdong Catholic Church was built on 1908–1914 by French priest Xavier Baudonet.
      evidence:
        - doc_id: wiki-en-jeonju
          location: Attractions
          passage: "Jeongdong Catholic Church was built on 1908–1914 by French priest Xavier Baudonet on the site of the Korean Catholic martyrs in 1791 and 1801."
  opposite_check:
    - term: "보두네"
      hits: []
    - term: "바우도넷"
      hits: []
    - term: "프랑스인 신부"
      hits: []
  same_language_check:
    - term: "Xavier Baudonet"
      hits: []
    - term: "cleric"
      hits: []
    - term: "French priest"
      hits: []

- id: c-019
  question: What type of fish, historically brought inland using special salting techniques to prevent spoiling, is a popular local delicacy in Andong?
  question_language: en
  evidence_language: en
  type: single_fact
  answer: Mackerel.
  required_facts:
    - fact: Mackerel is a popular local delicacy in Andong, historically brought inland using special salting techniques to prevent spoiling.
      evidence:
        - doc_id: wiki-en-andong
          location: Local specialty foods
          passage: "Mackerel is another popular local delicacy. Caught downstream where the Nakdong River meets the sea, in ancient times the fish would spoil before being brought further inland. Using special salting techniques, Andong was the furthest inland the fish could be brought, so aristocrats would travel to Andong specially for the salted fish."
  opposite_check:
    - term: "염장"
      hits: []
    - term: "고등어"
      hits: []
    - term: "상하기 전"
      hits: []
  same_language_check:
    - term: "salting techniques"
      hits: []
    - term: "spoil before"
      hits: []
    - term: "Mackerel"
      hits:
        - doc_id: wiki-en-andong
          excerpt: "and salted mackerel."
          same_fact: false
          why: 목록에 나열된 부분으로 본문 안의 구체적인 염장 역사 이야기가 아니다
        - doc_id: wiki-en-busan
          excerpt: "- Fish: Mackerel"
          same_fact: false
          why: 부산의 시조 어류 소개이다

- id: c-020
  question: According to the climate data for Busan, what is the record low temperature for the month of February in Celsius?
  question_language: en
  evidence_language: en
  type: table_numeric
  answer: -12.6.
  required_facts:
    - fact: The record low temperature for February in Busan is -12.6 Celsius.
      evidence:
        - doc_id: wiki-en-busan
          location: Climate
          passage: |
            | Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |
            | Record low °C (°F) | −14.0 (6.8) | −12.6 (9.3) | −9.7 (14.5) | −1.5 (29.3) | 5.4 (41.7) | 9.3 (48.7) | 13.8 (56.8) | 15.4 (59.7) | 9.6 (49.3) | 1.8 (35.2) | −6.5 (20.3) | −12.0 (10.4) | −14.0 (6.8) |
  opposite_check:
    - term: "−12.6"
      hits: []
    - term: "-12.6"
      hits: []
    - term: "영하 12.6"
      hits: []
  same_language_check:
    - term: "−12.6"
      hits: []
    - term: "-12.6"
      hits: []
    - term: "Record low"
      hits:
        - doc_id: wiki-en-busan
          excerpt: "while the lowest temperature ever recorded is −14.0 °C (6.8 °F) on 13 January 1915."
          same_fact: false
          why: 표가 아닌 본문의 연대기적 최저 기온 설명이다
        - doc_id: wiki-en-andong
          excerpt: "| Record low °C (°F) | −20.4 (−4.7) | −18.6 (−1.5)"
          same_fact: false
          why: 안동의 통계이다
        - doc_id: wiki-en-cheonan
          excerpt: "| Record low °C (°F) | −23.9 (−11.0) | −19.9 (−3.8)"
          same_fact: false
          why: 천안의 통계이다
        - doc_id: wiki-en-cheongju
          excerpt: "| Record low °C (°F) | −24.1 (−11.4) | −26.4 (−15.5)"
          same_fact: false
          why: 청주의 통계이다
        - doc_id: wiki-en-chuncheon
          excerpt: "| Record low °C (°F) | −25.6 (−14.1) | −27.9 (−18.2)"
          same_fact: false
          why: 춘천의 통계이다
        - doc_id: wiki-en-gangneung
          excerpt: "| Record low °C (°F) | −20.2 (−4.4) | −15.9 (3.4)"
          same_fact: false
          why: 강릉의 통계이다
        - doc_id: wiki-en-jeju
          excerpt: "| Record low °C (°F) | −5.8 (21.6) | −6.0 (21.2)"
          same_fact: false
          why: 제주의 통계이다
        - doc_id: wiki-en-jeju
          excerpt: "| Record low °C (°F) | −6.2 (20.8) | −3.0 (26.6)"
          same_fact: false
          why: 제주 고산리의 통계이다
        - doc_id: wiki-en-jeonju
          excerpt: "| Record low °C (°F) | −17.1 (1.2) | −16.6 (2.1)"
          same_fact: false
          why: 전주의 통계이다

- id: c-021
  question: What is the name of the unusually bowl-shaped mountain in Jeju popular for seeing the first sunrise, and what trail in Gangneung allows visitors to observe a coastal terrace formed 23 million years ago?
  question_language: en
  evidence_language: en
  type: multi_doc
  answer: The mountain is Seongsan Ilchulbong, and the trail is Jeongdong-Simgok Badabuchae Trail.
  required_facts:
    - fact: Seongsan Ilchulbong is an unusually bowl-shaped mountain in Jeju popular for seeing the first sunrise.
      evidence:
        - doc_id: wiki-en-jeju
          location: Tourism
          passage: "Seongsan Ilchulbong, an unusually bowl-shaped mountain, is popular for seeing the first sunrise of the year."
    - fact: Jeongdong-Simgok Badabuchae Trail is a trail in Gangneung where visitors can observe the coastal terrace formed 23 million years ago.
      evidence:
        - doc_id: wiki-en-gangneung
          location: Beaches
          passage: "Jeongdong-Simgok Badabuchae Trail is a 2.86 km trail where visitors can observe the coastal terrace formed 23 million years ago."
    - fact: The mountain is Seongsan Ilchulbong, and the trail is Jeongdong-Simgok Badabuchae Trail.
      evidence: []
  opposite_check:
    - term: "성산일출봉"
      hits: []
    - term: "바다부채길"
      hits: []
    - term: "2300만"
      hits: []
  same_language_check:
    - term: "bowl-shaped"
      hits: []
    - term: "Badabuchae"
      hits: []
    - term: "23 million"
      hits: []

- id: c-022
  question: What is the highest mountain in Busan, and in what year was the dam built in Andong that provided a reliable source of electricity?
  question_language: en
  evidence_language: en
  type: multi_doc
  answer: The highest mountain in Busan is Geumjeongsan, and the Andong Dam was built in 1976.
  required_facts:
    - fact: Geumjeongsan is the highest mountain in Busan.
      evidence:
        - doc_id: wiki-en-busan
          location: Geography
          passage: "Geumjeongsan, the highest mountain in the city, is on the north."
    - fact: The Andong Dam was built in 1976, providing the city with a reliable source of electricity.
      evidence:
        - doc_id: wiki-en-andong
          location: History
          passage: "In 1976 the Andong Dam was built, providing the city with a reliable source of electricity."
    - fact: The highest mountain in Busan is Geumjeongsan, and the Andong Dam was built in 1976.
      evidence: []
  opposite_check:
    - term: "금정산"
      hits: []
    - term: "안동댐"
      hits: []
    - term: "신뢰할 수 있는 전력"
      hits: []
  same_language_check:
    - term: "Geumjeongsan"
      hits: []
    - term: "Andong Dam"
      hits:
        - doc_id: wiki-en-andong
          excerpt: "Andong also has Andong Dam. In the area where Andong Dam is located,"
          same_fact: false
          why: 댐 건립 연도가 아닌 댐 주변 기념비에 관한 서술이다
    - term: "reliable source of electricity"
      hits: []

- id: c-023
  question: Which South Korean head of state, who previously held office, was originally from Gangneung?
  question_language: en
  evidence_language: en
  type: paraphrase
  answer: Choi Kyu-Ha.
  required_facts:
    - fact: Choi Kyu-Ha, a former president of South Korea, is from Gangneung.
      evidence:
        - doc_id: wiki-en-gangneung
          location: Notable people
          passage: "- Choi Kyu-Ha, former president of South Korea"
  opposite_check:
    - term: "최규하"
      hits: []
    - term: "대통령 최규하"
      hits: []
    - term: "국가원수"
      hits: []
  same_language_check:
    - term: "Choi Kyu-Ha"
      hits: []
    - term: "head of state"
      hits: []
    - term: "former president"
      hits:
        - doc_id: wiki-en-cheongju
          excerpt: "- Choi Soon-ho, football manager and former professional football player."
          same_fact: false
          why: 축구선수 출신이라는 뜻으로 대통령이 아니다

- id: c-024
  question: Which aviation company has its main office situated in Jeju City?
  question_language: en
  evidence_language: en
  type: paraphrase
  answer: Jeju Air.
  required_facts:
    - fact: Jeju Air has its headquarters in Jeju City.
      evidence:
        - doc_id: wiki-en-jeju
          location: Economy
          passage: "Jeju Air has its headquarters in Jeju City."
  opposite_check:
    - term: "제주항공"
      hits: []
    - term: "항공사 본사"
      hits: []
    - term: "항공 기업"
      hits: []
  same_language_check:
    - term: "Jeju Air"
      hits: []
    - term: "aviation company"
      hits: []
    - term: "main office"
      hits: []

```

c-014: "dancing festival that means 'pleasure and joy'"는 "Heungtaryeong Festival (흥타령 축제). 흥 means pleasure and joy"를, "attain the status of 'promising'"은 "received the position of 'promising'"을 바꾼 말이다.
c-018: "institution"은 "Catholic Church"를, "French cleric"은 "French priest"를 바꾼 말이다.
c-023: "head of state, who previously held office"는 "former president"를 바꾼 말이다.
c-024: "aviation company"는 "Air"를, "main office situated"는 "headquarters"를 바꾼 말이다.