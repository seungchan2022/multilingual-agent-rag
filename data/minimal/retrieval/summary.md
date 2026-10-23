# 검색 비교 요약

결과 파일 `data/minimal/retrieval/results.jsonl`의 304줄(조합 8개)에서 계산했다. 크기 128 묶음은 k = 8, 256 묶음은 k = 4로, 명목 예산이 1,024토큰으로 같다. ✔는 가져온 청크 가운데 근거 하나와 문서가 같고, 그 줄이 청크의 줄 번호 목록에 있고, `value_text`가 청크 글에 글자 그대로 든 청크가 있는 질문이다.

## 조합별 ✔ 수

| 청크 묶음 | 모델 | k | 전체 ✔ | ko·한국어만 | ko·영어만 | ko·두 언어 | en·한국어만 | en·영어만 | en·두 언어 | 다른 언어 16개 ✔ |
|---|---|---|---|---|---|---|---|---|---|---|
| size128_notitle | bge-m3 | 8 | 21/38 | 5/8 | 6/8 | 2/3 | 0/8 | 6/8 | 2/3 | 6/16 |
| size128_title | bge-m3 | 8 | 31/38 | 6/8 | 8/8 | 3/3 | 3/8 | 8/8 | 3/3 | 11/16 |
| size256_notitle | bge-m3 | 4 | 23/38 | 6/8 | 5/8 | 2/3 | 2/8 | 6/8 | 2/3 | 7/16 |
| size256_title | bge-m3 | 4 | 32/38 | 7/8 | 8/8 | 3/3 | 3/8 | 8/8 | 3/3 | 11/16 |
| size128_notitle | gte-multilingual-base | 8 | 26/38 | 7/8 | 5/8 | 2/3 | 4/8 | 6/8 | 2/3 | 9/16 |
| size128_title | gte-multilingual-base | 8 | 30/38 | 8/8 | 3/8 | 3/3 | 5/8 | 8/8 | 3/3 | 8/16 |
| size256_notitle | gte-multilingual-base | 4 | 18/38 | 6/8 | 1/8 | 1/3 | 3/8 | 6/8 | 1/3 | 4/16 |
| size256_title | gte-multilingual-base | 4 | 24/38 | 7/8 | 3/8 | 3/3 | 2/8 | 7/8 | 2/3 | 5/16 |

## 가져온 청크의 토큰 합(질문마다)

같은 명목 예산으로 견줬으므로 실제로 가져온 양은 조합마다 다르다. 토큰은 bge-m3 토크나이저로 센 값이다.

| 청크 묶음 | 모델 | 평균 | 최소 | 최대 |
|---|---|---|---|---|
| size128_notitle | bge-m3 | 841 | 526 | 1134 |
| size128_title | bge-m3 | 957.7 | 770 | 1296 |
| size256_notitle | bge-m3 | 710.8 | 465 | 931 |
| size256_title | bge-m3 | 810.2 | 654 | 961 |
| size128_notitle | gte-multilingual-base | 907.9 | 685 | 1283 |
| size128_title | gte-multilingual-base | 944.3 | 668 | 1384 |
| size256_notitle | gte-multilingual-base | 710.8 | 294 | 958 |
| size256_title | gte-multilingual-base | 755.3 | 401 | 967 |

## 고른 조합

- 가장 많은 전체 ✔: 32. 이 수와 차이가 2개 이하(30 이상)인 조합이 비긴 것이다.
- 비긴 조합: size128_title × bge-m3(31), size256_title × bge-m3(32), size128_title × gte-multilingual-base(30)
- 1. 다른 언어 16개의 ✔ 수가 많은 조합: size128_title × bge-m3=11/16, size256_title × bge-m3=11/16, size128_title × gte-multilingual-base=8/16
  - 남은 조합: size128_title × bge-m3, size256_title × bge-m3
- 2. 과제 권장 모델(gte-multilingual-base)을 쓴 조합: size128_title × bge-m3=아니오, size256_title × bge-m3=아니오
  - 남은 조합: size128_title × bge-m3, size256_title × bge-m3
- 3. 제목을 붙이지 않은 조합: size128_title × bge-m3=붙임, size256_title × bge-m3=붙임
  - 남은 조합: size128_title × bge-m3, size256_title × bge-m3
- 4. 청크 크기가 작은 조합: size128_title × bge-m3=128, size256_title × bge-m3=256
  - 남은 조합: size128_title × bge-m3
- **고른 조합: size128_title × bge-m3**

## 청크 묶음

토큰 길이는 청크 파일의 `tokens`(bge-m3 토크나이저)이고, 90%는 작은 순서로 세어 ceil(0.9 × 청크 수)번째 값이다. 한도를 넘긴 청크는 가장 작은 단위(표 머리글 + 행 하나, 문장 하나, 정보 상자 줄 하나)가 크기 한도보다 커서 그대로 둔 것이다.

| 청크 묶음 | 청크 수 | 길이 최소 | 중앙값 | 90% | 최대 | 한도 넘긴 청크 수 | 넘긴 청크 길이 최소 | 중앙값 | 최대 |
|---|---|---|---|---|---|---|---|---|---|
| size128_notitle | 1285 | 7 | 109 | 142 | 172 | 254 | 129 | 142 | 172 |
| size128_title | 1383 | 18 | 113 | 150 | 182 | 352 | 129 | 148 | 182 |
| size256_notitle | 625 | 7 | 182 | 242 | 256 | 0 | - | - | - |
| size256_title | 646 | 21 | 190 | 242 | 256 | 0 | - | - | - |

한도를 넘긴 청크의 문서별 수:

- size128_notitle: wiki-en-isotopes-of-yttrium 24, wiki-en-lanthanum 1, wiki-en-neutron-capture-therapy 2, wiki-en-praseodymium 2, wiki-ko-isotopes-of-neodymium 57, wiki-ko-isotopes-of-terbium 86, wiki-ko-isotopes-of-yttrium 81, wiki-ko-yttrium 1
- size128_title: wiki-en-isotopes-of-yttrium 110, wiki-en-lanthanum 2, wiki-en-neutron-capture-therapy 12, wiki-en-praseodymium 2, wiki-ko-isotopes-of-neodymium 57, wiki-ko-isotopes-of-terbium 86, wiki-ko-isotopes-of-yttrium 81, wiki-ko-ytterbium 1, wiki-ko-yttrium 1
- size256_notitle: 없음
- size256_title: 없음
