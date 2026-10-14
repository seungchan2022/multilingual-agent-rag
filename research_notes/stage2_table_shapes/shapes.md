# 마크다운 표의 모양

`classify.py`가 `tables.json`에서 만든다. 표 하나가 여러 모양에 들 수 있다. 처리 방법은 4단계에서 정한다.

마크다운 표 100개(위키백과 98, 통계 표 2).

| 모양 | 판정 | 표 수 |
|---|---|---|
| 머리글 줄이 없는 표 | 읽어서 판정 | 11 |
| 한 줄에 여러 대상이 옆으로 놓인 표 | 읽어서 판정 | 6 |
| 머리글이 두 줄인 표 | 읽어서 판정 | 1 |
| 같은 머리글이 여러 열에 붙은 표 | 읽어서 판정 | 4 |
| 머리글 칸이 일부만 찬 표 | 읽어서 판정 | 1 |
| 표 중간에 머리글이 다시 나오는 표 | 읽어서 판정 | 1 |
| 합계 줄이 있는 표 | 읽어서 판정 | 13 |
| 줄의 소속이 순서로만 드러나는 표 | 읽어서 판정 | 2 |
| 줄 이름이 없는 표 | 읽어서 판정 | 1 |
| 열이 달·해·종류로 나뉜 표 | 읽어서 판정 | 26 |
| 세로로 합친 칸이 있는 표 | 기계 판정 | 16 |
| 가로로 합친 칸이 있는 표 | 기계 판정 | 10 |
| 칸 안에 줄바꿈이 있는 표 | 기계 판정 | 31 |
| 칸 안에 목록이 있는 표 | 기계 판정 | 0 |
| 내용 줄이 없는 표 | 기계 판정 | 4 |
| 모든 칸이 빈 줄이 있는 표 | 기계 판정 | 1 |
| 통계 표 | 기계 판정 | 2 |
| 위 모양이 하나도 없는 표 | 기계 판정(위 목록의 나머지) | 32 |

## 원문 표 전체(틀로 풀린 표 포함)

변환 코드가 받은 원문 표 가운데 마크다운 표가 되지 않은 것: 틀로 풀린 표는 목록이나 표를 옆으로 나란히 놓으려고 표의 틀만 빌린 것이라, 표로 옮기지 않고 칸의 내용을 위에서 아래로 적었다(`decisions/stage2.md` 2026-10-14 표 규칙 ㉣㉤). 비어서 빠진 표는 글자가 없는 표다(춘천 한국어 문서 '교육 기관' 절).

| 항목 | 수 |
|---|---|
| table_items가 받은 위키백과 원문 HTML 표 | 123 |
| table_items가 받은 통계 표(CSV) | 2 |
| 마크다운 표가 됨 | 100 |
| 틀로 풀림 | 24 |
| 비어서 빠짐 | 1 |
| 칸을 합친 표(세로나 가로) | 19 |
| 칸 안에 줄바꿈이 있는 표 | 33 |
| 칸 안에 목록이 있는 표 | 17 |
| 표 안에 표가 있는 것 | 7 |
| 칸을 합쳤거나 표 전체 너비의 줄이 있는 표 | 54 |

## 한 칸에 값이 둘 들어 줄끼리 짝을 이루는 표 (0개)

후보 표 23개(한 줄에서 칸 둘 이상이 같은 수의 조각으로 나뉜 줄이 있는 표)를 AI가 전부 읽었다. 짝을 이루는 표는 없었다.

- wiki-ko-jeonju#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-jeonju#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-cheongju#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-cheongju#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-chuncheon#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-chuncheon#3 — 제목 칸 안의 단위 줄(Area / (km2))
- wiki-en-chuncheon#4 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-cheonan#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-cheonan#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-busan#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-jeju#2 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-jeju#3 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-jeju#4 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-jeju#5 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-andong#2 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-en-gangneung#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-suwon#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-gyeongju#2 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-gyeongju#8 — 제목 칸 안의 구분 줄(고등학교 / (일반계))
- wiki-ko-gwangju#1 — 같은 값의 섭씨와 화씨(또는 mm와 인치). 짝을 이루는 서로 다른 값이 아니다
- wiki-ko-gwangju#7 — 제목 칸 안의 구분 줄(2013 / (추정))
- wiki-ko-gwangju#8 — 한 칸의 설명 글이 줄을 넘긴 것. 옆 칸과 짝을 이루지 않는다
- wiki-ko-gwangju#12 — 제목 칸 안의 구분 줄(1999년 / (육성이전))

## 머리글 줄이 없는 표 (11개)

원문에 제목 줄이 없어, 첫 줄(내용)이 마크다운 표의 머리글 자리에 놓였다.

- wiki-ko-cheongju#3 — 고속철도 노선과 역  
  `data/corpus/markdown/wiki-ko-cheongju.md` 342번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 철도
- wiki-ko-cheongju#4 — 일반철도 노선과 역  
  `data/corpus/markdown/wiki-ko-cheongju.md` 347번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 철도
- wiki-ko-cheongju#5 — 고속도로 이름과 나들목  
  `data/corpus/markdown/wiki-ko-cheongju.md` 356번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 도로
- wiki-ko-cheongju#6 — 일반 도로 번호와 도로 이름  
  `data/corpus/markdown/wiki-ko-cheongju.md` 364번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 도로
- wiki-ko-cheongju#7 — 버스 터미널과 운행  
  `data/corpus/markdown/wiki-ko-cheongju.md` 374번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 고속·시외버스
- wiki-ko-chuncheon#8 — 철도 노선과 역  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 375번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 철도
- wiki-ko-chuncheon#9 — 고속도로 이름과 나들목  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 383번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 고속도로
- wiki-ko-chuncheon#10 — 일반 도로 번호와 도로 이름  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 391번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 일반도로
- wiki-ko-chuncheon#11 — 버스 터미널과 운행  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 399번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 고속·시외버스
- wiki-ko-chuncheon#13 — 대학 종류와 학교 이름  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 426번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교육 기관
- wiki-en-gangneung#4 — 철도 노선과 역  
  `data/corpus/markdown/wiki-en-gangneung.md` 166번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Transportation(교통) / Trains(철도)

## 한 줄에 여러 대상이 옆으로 놓인 표 (6개)

한 줄에 서로 다른 대상 여럿이 나란히 있어, 줄 하나가 대상 하나가 아니다.

- wiki-ko-cheongju#6 — 도로 번호·도로 이름 짝 4개가 한 줄에  
  `data/corpus/markdown/wiki-ko-cheongju.md` 364번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 도로
- wiki-ko-cheongju#7 — 터미널·운행 짝 2개가 한 줄에  
  `data/corpus/markdown/wiki-ko-cheongju.md` 374번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 고속·시외버스
- wiki-ko-chuncheon#10 — 도로 번호·도로 이름 짝 3개가 한 줄에  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 391번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 일반도로
- wiki-ko-chuncheon#11 — 터미널·운행 짝 2개가 한 줄에  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 399번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 고속·시외버스
- wiki-ko-chuncheon#13 — 같은 종류의 학교 이름이 여러 열에 흩어짐  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 426번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교육 기관
- wiki-ko-chuncheon#14 — 같은 종류의 학교 이름이 여러 열에 흩어짐  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 433번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교육 기관

## 머리글이 두 줄인 표 (1개)

제목 줄이 두 줄이라, 마크다운에서는 둘째 제목 줄이 내용 줄처럼 놓였다.

- wiki-en-gangneung#3 — 1줄: 국가 지정/도 지정, 2줄: 국보·보물 등  
  `data/corpus/markdown/wiki-en-gangneung.md` 127번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Culture(문화) / Heritage(문화유산)

## 같은 머리글이 여러 열에 붙은 표 (4개)

가로로 합친 제목 칸이 펴져, 서로 다른 열이 같은 이름을 가졌다.

- wiki-en-gangneung#3 — State-designated heritage가 9열, Province-designated heritage가 5열  
  `data/corpus/markdown/wiki-en-gangneung.md` 127번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Culture(문화) / Heritage(문화유산)
- wiki-ko-suwon#6 — 지방자치단체 2열(국내 도시는 시·도와 시·군, 외국 도시는 나라와 도시)  
  `data/corpus/markdown/wiki-ko-suwon.md` 319번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 교류 도시
- wiki-ko-cheongju#8 — 도시 2열(시·도·주와 시·군·구)  
  `data/corpus/markdown/wiki-ko-cheongju.md` 488번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 자매 도시
- wiki-ko-sejong#4 — 구분 2열(이전 단계와 분야)  
  `data/corpus/markdown/wiki-ko-sejong.md` 186번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 이전 기관 / 중앙행정기관

## 머리글 칸이 일부만 찬 표 (1개)

제목 줄의 칸 대부분이 비어 있다.

- wiki-ko-chuncheon#14 — 제목 줄이 '고등학교'와 빈칸 5개  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 433번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교육 기관

## 표 중간에 머리글이 다시 나오는 표 (1개)

표 중간에 제목 줄이 한 번 더 있어, 그 아래 줄은 첫 제목이 아니라 새 제목에 속한다.

- wiki-ko-gwangju#14 — 박물관 6줄 뒤에 '미술관 | 주소 | 홈페이지' 줄  
  `data/corpus/markdown/wiki-ko-gwangju.md` 451번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 문화 / 박물관·미술관

## 합계 줄이 있는 표 (13개)

대상 줄들의 앞이나 사이나 끝에 그 합계 줄이 있다.

- wiki-ko-jeonju#2 — 끝 줄 전주시  
  `data/corpus/markdown/wiki-ko-jeonju.md` 117번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42643645 · 절: 행정 구역
- wiki-ko-cheongju#2 — 끝 줄 총합계  
  `data/corpus/markdown/wiki-ko-cheongju.md` 109번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 행정 구역
- wiki-ko-chuncheon#3 — 끝 줄 합계  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 92번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 행정 구역
- wiki-en-chuncheon#3 — 끝 줄 Total  
  `data/corpus/markdown/wiki-en-chuncheon.md` 73번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Administrative divisions(행정 구역)
- wiki-ko-cheonan#2 — 구 소계 2줄과 끝 줄 총계  
  `data/corpus/markdown/wiki-ko-cheonan.md` 79번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 행정 구역
- wiki-ko-suwon#5 — 끝 줄 수원시  
  `data/corpus/markdown/wiki-ko-suwon.md` 164번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 행정 / 행정 구역
- wiki-ko-gyeongju#4 — 끝 줄 경주시  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 125번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 행정 구역
- wiki-ko-sejong#1 — 끝 줄 세종특별자치시  
  `data/corpus/markdown/wiki-ko-sejong.md` 86번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 행정 구역
- wiki-ko-gwangju#2 — 끝 줄 광주광역시  
  `data/corpus/markdown/wiki-ko-gwangju.md` 79번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 행정 구역
- wiki-en-gangneung#2 — 끝 줄 Gangneung-si  
  `data/corpus/markdown/wiki-en-gangneung.md` 78번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Administrative divisions(행정 구역)
- wiki-ko-sejong#4 — 첫 줄 36개 기관  
  `data/corpus/markdown/wiki-ko-sejong.md` 186번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 이전 기관 / 중앙행정기관
- wiki-ko-gwangju#10 — 첫 줄 합계  
  `data/corpus/markdown/wiki-ko-gwangju.md` 357번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업
- wiki-ko-gwangju#7 — 매출액 합계, 수출액 합계 줄  
  `data/corpus/markdown/wiki-ko-gwangju.md` 318번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업

## 줄의 소속이 순서로만 드러나는 표 (2개)

줄 이름만으로는 무엇에 속한 줄인지 알 수 없고, 위나 아래의 줄을 봐야 안다.

- wiki-ko-cheonan#2 — 동 줄들 뒤에 그 동들이 속한 구의 소계 줄(서북구, 동남구)  
  `data/corpus/markdown/wiki-ko-cheonan.md` 79번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 행정 구역
- wiki-ko-gwangju#7 — '완성차'·'부품' 줄이 두 번 나오고, 위의 합계 줄(매출액, 수출액)에 따라 뜻이 갈린다  
  `data/corpus/markdown/wiki-ko-gwangju.md` 318번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업

## 줄 이름이 없는 표 (1개)

줄마다 무엇을 센 값인지 적힌 칸이 없다.

- wiki-ko-gyeongju#8 — 학생 수 줄과 교직원 수 줄에 이름이 없고, 표 위 제목('학생 · 교직원 현황')으로만 짐작된다  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 327번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 교육

## 열이 달·해·종류로 나뉜 표 (26개)

맨 윗줄이 달·해·종류처럼 한 항목을 나눈 칸이고, 맨 왼쪽 열은 무엇을 센 값인지를 적는다. 그래서 값 하나의 뜻에 줄 이름과 열 이름이 둘 다 필요하다.

- wiki-ko-jeonju#1 — 기후 표  
  `data/corpus/markdown/wiki-ko-jeonju.md` 98번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42643645 · 절: 지리 / 기후
- wiki-en-jeonju#1 — 기후 표  
  `data/corpus/markdown/wiki-en-jeonju.md` 53번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379135207 · 절: Geography and administrative divisions(지리와 행정 구역) / Climate(기후)
- wiki-ko-cheongju#1 — 기후 표  
  `data/corpus/markdown/wiki-ko-cheongju.md` 84번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 지리 / 기후
- wiki-en-cheongju#1 — 기후 표  
  `data/corpus/markdown/wiki-en-cheongju.md` 58번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378953230 · 절: Geography(지리) / Climate(기후)
- wiki-ko-chuncheon#1 — 기후 표  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 70번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 지리 / 기후
- wiki-en-chuncheon#4 — 기후 표  
  `data/corpus/markdown/wiki-en-chuncheon.md` 182번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Climate(기후)
- wiki-ko-cheonan#1 — 기후 표  
  `data/corpus/markdown/wiki-ko-cheonan.md` 59번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 지리 / 기후
- wiki-en-cheonan#1 — 기후 표  
  `data/corpus/markdown/wiki-en-cheonan.md` 52번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378953224 · 절: Geography(지리) / Climate(기후)
- wiki-en-busan#1 — 기후 표  
  `data/corpus/markdown/wiki-en-busan.md` 88번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Geography(지리) / Climate(기후)
- wiki-en-jeju#2 — 기후 표  
  `data/corpus/markdown/wiki-en-jeju.md` 90번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-jeju#3 — 기후 표  
  `data/corpus/markdown/wiki-en-jeju.md` 108번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-jeju#4 — 기후 표  
  `data/corpus/markdown/wiki-en-jeju.md` 126번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-jeju#5 — 기후 표  
  `data/corpus/markdown/wiki-en-jeju.md` 138번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-andong#2 — 기후 표  
  `data/corpus/markdown/wiki-en-andong.md` 196번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378924154 · 절: Climate(기후)
- wiki-en-gangneung#1 — 기후 표  
  `data/corpus/markdown/wiki-en-gangneung.md` 58번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Geography(지리) / Climate(기후)
- wiki-ko-suwon#1 — 기후 표  
  `data/corpus/markdown/wiki-ko-suwon.md` 81번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 지리와 지질 / 기후
- wiki-ko-gyeongju#2 — 기후 표  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 100번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 지리 / 기후
- wiki-ko-gwangju#1 — 기후 표  
  `data/corpus/markdown/wiki-ko-gwangju.md` 56번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 지리 / 기후
- wiki-ko-suwon#3 — 산업별 사업체 수(2009년, 2018년, 증감율)  
  `data/corpus/markdown/wiki-ko-suwon.md` 147번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 산업과 경제 / 변천
- wiki-ko-gyeongju#7 — 의료시설 건수·병상수  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 310번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 경제 / 서비스업
- wiki-ko-gyeongju#8 — 학생·교직원 수  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 327번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 교육
- wiki-ko-gwangju#7 — 자동차 생산·매출·수출  
  `data/corpus/markdown/wiki-ko-gwangju.md` 318번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업
- wiki-ko-gwangju#10 — 기업 수  
  `data/corpus/markdown/wiki-ko-gwangju.md` 357번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업
- wiki-ko-gwangju#11 — 제조업체 수  
  `data/corpus/markdown/wiki-ko-gwangju.md` 365번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업
- wiki-ko-gwangju#12 — 고용·업체·매출  
  `data/corpus/markdown/wiki-ko-gwangju.md` 384번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업
- wiki-ko-gwangju#13 — 고용·기업체·매출  
  `data/corpus/markdown/wiki-ko-gwangju.md` 403번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업

## 세로로 합친 칸이 있는 표 (16개)

칸 하나가 아래로 여러 줄에 걸쳐 있었다. 마크다운에서는 같은 글자가 줄마다 되풀이된다.

- wiki-ko-cheongju#8  
  `data/corpus/markdown/wiki-ko-cheongju.md` 488번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 자매 도시
- wiki-ko-chuncheon#13  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 426번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교육 기관
- wiki-ko-chuncheon#14  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 433번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교육 기관
- wiki-ko-chuncheon#19  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 545번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 자매 도시 / 자매결연 도시
- wiki-ko-chuncheon#20  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 558번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 자매 도시 / 우호 도시
- wiki-en-chuncheon#5  
  `data/corpus/markdown/wiki-en-chuncheon.md` 215번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Sister cities(자매 도시)
- wiki-ko-cheonan#2  
  `data/corpus/markdown/wiki-ko-cheonan.md` 79번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 행정 구역
- wiki-en-gangneung#2  
  `data/corpus/markdown/wiki-en-gangneung.md` 78번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Administrative divisions(행정 구역)
- wiki-en-gangneung#3  
  `data/corpus/markdown/wiki-en-gangneung.md` 127번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Culture(문화) / Heritage(문화유산)
- wiki-ko-suwon#6  
  `data/corpus/markdown/wiki-ko-suwon.md` 319번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 교류 도시
- wiki-ko-gyeongju#4  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 125번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 행정 구역
- wiki-ko-gyeongju#9  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 336번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 스포츠
- wiki-ko-sejong#4  
  `data/corpus/markdown/wiki-ko-sejong.md` 186번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 이전 기관 / 중앙행정기관
- wiki-ko-gwangju#15  
  `data/corpus/markdown/wiki-ko-gwangju.md` 509번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 문화 / 공원
- wiki-ko-gwangju#20  
  `data/corpus/markdown/wiki-ko-gwangju.md` 679번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 국제 교류
- wiki-ko-gwangju#22  
  `data/corpus/markdown/wiki-ko-gwangju.md` 700번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 국제 교류

## 가로로 합친 칸이 있는 표 (10개)

칸 하나가 옆으로 여러 칸에 걸쳐 있었다(표 전체 너비의 줄은 뺀다).

- wiki-ko-cheongju#2  
  `data/corpus/markdown/wiki-ko-cheongju.md` 109번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 행정 구역
- wiki-ko-cheongju#8  
  `data/corpus/markdown/wiki-ko-cheongju.md` 488번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 자매 도시
- wiki-ko-chuncheon#3  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 92번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 행정 구역
- wiki-en-chuncheon#3  
  `data/corpus/markdown/wiki-en-chuncheon.md` 73번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Administrative divisions(행정 구역)
- wiki-en-chuncheon#5  
  `data/corpus/markdown/wiki-en-chuncheon.md` 215번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Sister cities(자매 도시)
- wiki-ko-cheonan#2  
  `data/corpus/markdown/wiki-ko-cheonan.md` 79번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 행정 구역
- wiki-en-gangneung#3  
  `data/corpus/markdown/wiki-en-gangneung.md` 127번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Culture(문화) / Heritage(문화유산)
- wiki-ko-suwon#6  
  `data/corpus/markdown/wiki-ko-suwon.md` 319번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 교류 도시
- wiki-ko-sejong#4  
  `data/corpus/markdown/wiki-ko-sejong.md` 186번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 이전 기관 / 중앙행정기관
- wiki-ko-gwangju#15  
  `data/corpus/markdown/wiki-ko-gwangju.md` 509번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 문화 / 공원

## 칸 안에 줄바꿈이 있는 표 (31개)

칸 하나 안에서 줄이 바뀌었다. 마크다운에서는 빈칸 하나가 된다.

- wiki-ko-jeonju#1  
  `data/corpus/markdown/wiki-ko-jeonju.md` 98번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42643645 · 절: 지리 / 기후
- wiki-ko-jeonju#2  
  `data/corpus/markdown/wiki-ko-jeonju.md` 117번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42643645 · 절: 행정 구역
- wiki-en-jeonju#1  
  `data/corpus/markdown/wiki-en-jeonju.md` 53번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379135207 · 절: Geography and administrative divisions(지리와 행정 구역) / Climate(기후)
- wiki-ko-cheongju#1  
  `data/corpus/markdown/wiki-ko-cheongju.md` 84번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 지리 / 기후
- wiki-ko-cheongju#5  
  `data/corpus/markdown/wiki-ko-cheongju.md` 356번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 도로
- wiki-en-cheongju#1  
  `data/corpus/markdown/wiki-en-cheongju.md` 58번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378953230 · 절: Geography(지리) / Climate(기후)
- wiki-ko-chuncheon#1  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 70번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 지리 / 기후
- wiki-en-chuncheon#3  
  `data/corpus/markdown/wiki-en-chuncheon.md` 73번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Administrative divisions(행정 구역)
- wiki-en-chuncheon#4  
  `data/corpus/markdown/wiki-en-chuncheon.md` 182번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Climate(기후)
- wiki-ko-cheonan#1  
  `data/corpus/markdown/wiki-ko-cheonan.md` 59번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 지리 / 기후
- wiki-ko-cheonan#2  
  `data/corpus/markdown/wiki-ko-cheonan.md` 79번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42545685 · 절: 행정 구역
- wiki-en-cheonan#1  
  `data/corpus/markdown/wiki-en-cheonan.md` 52번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378953224 · 절: Geography(지리) / Climate(기후)
- wiki-en-busan#1  
  `data/corpus/markdown/wiki-en-busan.md` 88번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Geography(지리) / Climate(기후)
- wiki-en-busan#2  
  `data/corpus/markdown/wiki-en-busan.md` 111번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Administrative divisions(행정 구역)
- wiki-en-jeju#2  
  `data/corpus/markdown/wiki-en-jeju.md` 90번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-jeju#3  
  `data/corpus/markdown/wiki-en-jeju.md` 108번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-jeju#4  
  `data/corpus/markdown/wiki-en-jeju.md` 126번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-jeju#5  
  `data/corpus/markdown/wiki-en-jeju.md` 138번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Climate(기후)
- wiki-en-andong#2  
  `data/corpus/markdown/wiki-en-andong.md` 196번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378924154 · 절: Climate(기후)
- wiki-en-gangneung#1  
  `data/corpus/markdown/wiki-en-gangneung.md` 58번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378182836 · 절: Geography(지리) / Climate(기후)
- wiki-ko-suwon#1  
  `data/corpus/markdown/wiki-ko-suwon.md` 81번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 지리와 지질 / 기후
- wiki-ko-gyeongju#2  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 100번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 지리 / 기후
- wiki-ko-gyeongju#3  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 114번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 정치
- wiki-ko-gyeongju#6  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 272번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 관광 / 행사
- wiki-ko-gyeongju#8  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 327번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 교육
- wiki-ko-sejong#1  
  `data/corpus/markdown/wiki-ko-sejong.md` 86번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 행정 구역
- wiki-ko-sejong#4  
  `data/corpus/markdown/wiki-ko-sejong.md` 186번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 이전 기관 / 중앙행정기관
- wiki-ko-sejong#5  
  `data/corpus/markdown/wiki-ko-sejong.md` 212번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 이전 기관 / 정부출연 연구기관
- wiki-ko-gwangju#1  
  `data/corpus/markdown/wiki-ko-gwangju.md` 56번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 지리 / 기후
- wiki-ko-gwangju#8  
  `data/corpus/markdown/wiki-ko-gwangju.md` 334번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업
- wiki-ko-gwangju#9  
  `data/corpus/markdown/wiki-ko-gwangju.md` 344번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 경제 / 산업

## 칸 안에 목록이 있는 표 (0개)

칸 하나 안에 점 목록이 있었다. 마크다운에서는 쉼표로 이어진다.


## 내용 줄이 없는 표 (4개)

마크다운 표가 머리글 자리 한 줄뿐이다.

- wiki-ko-cheongju#3  
  `data/corpus/markdown/wiki-ko-cheongju.md` 342번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 철도
- wiki-ko-cheongju#4  
  `data/corpus/markdown/wiki-ko-cheongju.md` 347번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 철도
- wiki-ko-cheongju#7  
  `data/corpus/markdown/wiki-ko-cheongju.md` 374번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 교통 / 고속·시외버스
- wiki-ko-chuncheon#11  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 399번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 교통 / 고속·시외버스

## 모든 칸이 빈 줄이 있는 표 (1개)

내용 줄 가운데 모든 칸이 빈 줄이 있다.

- wiki-ko-cheongju#8  
  `data/corpus/markdown/wiki-ko-cheongju.md` 488번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42630014 · 절: 자매 도시

## 통계 표 (2개)

공공데이터포털의 CSV를 옮긴 표(원문 HTML이 없다).

- portal-ko-suwon-population#1  
  `data/corpus/markdown/portal-ko-suwon-population.md` 3번째 줄 · 원문 https://www.data.go.kr/data/15051539/fileData.do · 절: 
- portal-ko-jeonju-population#1  
  `data/corpus/markdown/portal-ko-jeonju-population.md` 3번째 줄 · 원문 https://www.data.go.kr/data/15126886/fileData.do · 절: 

## 위 모양이 하나도 없는 표 (32개)

제목 줄 한 줄, 줄마다 대상 하나인 표.

- wiki-ko-jeonju#3  
  `data/corpus/markdown/wiki-ko-jeonju.md` 177번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42643645 · 절: 인구
- wiki-ko-jeonju#4  
  `data/corpus/markdown/wiki-ko-jeonju.md` 197번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42643645 · 절: 인구
- wiki-en-jeonju#2  
  `data/corpus/markdown/wiki-en-jeonju.md` 73번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379135207 · 절: Geography and administrative divisions(지리와 행정 구역) / Demographics(인구)
- wiki-en-cheongju#2  
  `data/corpus/markdown/wiki-en-cheongju.md` 146번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378953230 · 절: Twin towns – sister cities(자매 도시)
- wiki-ko-chuncheon#4  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 136번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 인구
- wiki-ko-chuncheon#5  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 156번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 인구
- wiki-ko-chuncheon#6  
  `data/corpus/markdown/wiki-ko-chuncheon.md` 198번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42647646 · 절: 행정 / 춘천시의회
- wiki-en-chuncheon#1  
  `data/corpus/markdown/wiki-en-chuncheon.md` 54번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1376994978 · 절: Population(인구)
- wiki-en-busan#3  
  `data/corpus/markdown/wiki-en-busan.md` 284번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Culture and attractions(문화와 명소) / Festivals(축제)
- wiki-en-busan#4  
  `data/corpus/markdown/wiki-en-busan.md` 330번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Culture and attractions(문화와 명소) / Media(언론)
- wiki-en-busan#5  
  `data/corpus/markdown/wiki-en-busan.md` 358번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Demographics(인구)
- wiki-en-busan#6  
  `data/corpus/markdown/wiki-en-busan.md` 393번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Sports(스포츠)
- wiki-en-busan#7  
  `data/corpus/markdown/wiki-en-busan.md` 424번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Festivals and events(축제와 행사)
- wiki-en-busan#8  
  `data/corpus/markdown/wiki-en-busan.md` 445번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1379685823 · 절: Medical facilities(의료 시설) / Major medical centers(주요 병원)
- wiki-en-jeju#1  
  `data/corpus/markdown/wiki-en-jeju.md` 73번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Demographics(인구)
- wiki-en-jeju#7  
  `data/corpus/markdown/wiki-en-jeju.md` 152번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Administrative divisions(행정 구역)
- wiki-en-jeju#8  
  `data/corpus/markdown/wiki-en-jeju.md` 162번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1377658564 · 절: Administrative divisions(행정 구역)
- wiki-en-andong#1  
  `data/corpus/markdown/wiki-en-andong.md` 55번째 줄 · 원문 https://en.wikipedia.org/w/index.php?oldid=1378924154 · 절: Administrative divisions(행정 구역)
- wiki-ko-suwon#2  
  `data/corpus/markdown/wiki-ko-suwon.md` 104번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42534963 · 절: 인구통계
- wiki-ko-gyeongju#1  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 69번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 지리 / 위치
- wiki-ko-gyeongju#5  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 165번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 인구
- wiki-ko-gyeongju#10  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 510번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 자매 도시 / 자매결연 도시
- wiki-ko-gyeongju#11  
  `data/corpus/markdown/wiki-ko-gyeongju.md` 525번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42639825 · 절: 자매 도시 / 우호교류 도시
- wiki-ko-sejong#2  
  `data/corpus/markdown/wiki-ko-sejong.md` 148번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 인구 / 인구추이
- wiki-ko-sejong#3  
  `data/corpus/markdown/wiki-ko-sejong.md` 163번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 인구 / 인구동태
- wiki-ko-sejong#6  
  `data/corpus/markdown/wiki-ko-sejong.md` 281번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42585449 · 절: 문화 / 축제
- wiki-ko-gwangju#3  
  `data/corpus/markdown/wiki-ko-gwangju.md` 108번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 인구 / 인구추이
- wiki-ko-gwangju#4  
  `data/corpus/markdown/wiki-ko-gwangju.md` 132번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 인구 / 인구동태
- wiki-ko-gwangju#16  
  `data/corpus/markdown/wiki-ko-gwangju.md` 568번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 문화 / 숙박
- wiki-ko-gwangju#17  
  `data/corpus/markdown/wiki-ko-gwangju.md` 581번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 문화 / 레포츠
- wiki-ko-gwangju#18  
  `data/corpus/markdown/wiki-ko-gwangju.md` 599번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 스포츠
- wiki-ko-gwangju#21  
  `data/corpus/markdown/wiki-ko-gwangju.md` 693번째 줄 · 원문 https://ko.wikipedia.org/w/index.php?oldid=42623705 · 절: 국제 교류
