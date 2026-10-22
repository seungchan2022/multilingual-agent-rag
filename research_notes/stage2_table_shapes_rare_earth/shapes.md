# 마크다운 표의 모양(희토류 원소 코퍼스)

`classify.py`가 `tables.json`에서 만든다. 표 하나가 여러 모양에 들 수 있다. 처리 방법은 4단계(청크 전략)에서 정한다.
모양은 이 코퍼스의 표를 읽고 정했다. 도시 코퍼스 때의 목록(`research_notes/stage2_table_shapes/shapes.md`)은 옮기지 않았다.

마크다운 표 37개. 변환 코드가 표로 받았지만 마크다운에 남지 않은 것 3개(wiki-ko-dysprosium, wiki-ko-erbium, wiki-ko-thulium의 토막글 안내 상자).

## 어디에 있는 표인가

| 묶음 | 표 수 |
|---|---|
| 정보 상자의 증기 압력 표 | 14 |
| 정보 상자의 주요 동위원소 표 | 15 |
| 동위 원소 문서의 목록 표 | 4 |
| 그 밖의 본문 표 | 4 |

## 모양

| 모양 | 판정 | 표 수 |
|---|---|---|
| 세로로 합친 칸이 있는 표 | 기계 판정 | 9 |
| 가로로 합친 칸이 있는 표 | 기계 판정 | 19 |
| 머리글이 두 줄인 표 | 기계 판정 | 12 |
| 머리글 줄이 없는 표 | 기계 판정 | 1 |
| 줄 이름(th)이 첫 칸에 있는 표 | 기계 판정 | 22 |
| 칸 안에 줄바꿈이 있는 표 | 기계 판정 | 12 |
| 표 제목(caption)이 있는 표 | 기계 판정 | 3 |
| 표 전체 폭 줄(각주 등)이 있는 표 | 기계 판정 | 2 |
| 같은 대상이 이어진 여러 줄에 놓인 표 | 기계 판정 | 9 |
| 줄마다 열의 뜻이 바뀌는 표 | 기계 판정 | 4 |
| 가로로 놓인 표(항목이 줄로 놓이고 머리글 줄이 값) | 읽어서 판정 | 14 |
| 머리글 첫 줄이 묶음 이름인 표 | 읽어서 판정 | 8 |
| 한 칸에 여러 항목이 든 표(줄바꿈이 항목을 나눔) | 읽어서 판정 | 2 |
| 목록을 여러 열로 나눈 표(한 줄의 칸끼리 관계가 없음) | 읽어서 판정 | 1 |
| 위 모양이 하나도 없는 표 | 기계 판정(위 목록의 나머지) | 0 |

## 모양마다 표

### 세로로 합친 칸이 있는 표 (9)
- `wiki-ko-isotopes-of-yttrium:9`
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-ko-yttrium:55`
- `wiki-ko-isotopes-of-terbium:9`
- `wiki-ko-isotopes-of-neodymium:11`
- `wiki-en-lanthanum:60`
- `wiki-en-europium:58`
- `wiki-en-praseodymium:59`
- `wiki-en-neutron-capture-therapy:187`

### 가로로 합친 칸이 있는 표 (19)
- `wiki-ko-thulium:54`
- `wiki-en-thulium:59`
- `wiki-ko-dysprosium:56`
- `wiki-en-dysprosium:60`
- `wiki-ko-ytterbium:57`
- `wiki-en-ytterbium:60`
- `wiki-ko-lutetium:54`
- `wiki-en-lutetium:59`
- `wiki-ko-isotopes-of-yttrium:9`
- `wiki-en-isotopes-of-yttrium:3`
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-ko-erbium:55`
- `wiki-ko-samarium:56`
- `wiki-ko-yttrium:55`
- `wiki-ko-isotopes-of-terbium:9`
- `wiki-ko-isotopes-of-neodymium:11`
- `wiki-en-lanthanum:60`
- `wiki-en-europium:58`
- `wiki-en-praseodymium:59`

### 머리글이 두 줄인 표 (12)
- `wiki-en-thulium:59`
- `wiki-en-dysprosium:60`
- `wiki-en-ytterbium:60`
- `wiki-en-lutetium:59`
- `wiki-ko-isotopes-of-yttrium:9`
- `wiki-en-isotopes-of-yttrium:3`
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-ko-isotopes-of-terbium:9`
- `wiki-ko-isotopes-of-neodymium:11`
- `wiki-en-lanthanum:60`
- `wiki-en-europium:58`
- `wiki-en-praseodymium:59`

### 머리글 줄이 없는 표 (1)
- `wiki-en-neutron-capture-therapy:56`

### 줄 이름(th)이 첫 칸에 있는 표 (22)
- `wiki-ko-thulium:26`
- `wiki-en-thulium:27`
- `wiki-en-thulium:59`
- `wiki-ko-dysprosium:26`
- `wiki-en-dysprosium:27`
- `wiki-en-dysprosium:60`
- `wiki-ko-ytterbium:26`
- `wiki-en-ytterbium:27`
- `wiki-en-ytterbium:60`
- `wiki-ko-lutetium:26`
- `wiki-en-lutetium:27`
- `wiki-en-lutetium:59`
- `wiki-en-isotopes-of-yttrium:3`
- `wiki-ko-erbium:26`
- `wiki-ko-samarium:26`
- `wiki-ko-yttrium:26`
- `wiki-en-lanthanum:27`
- `wiki-en-lanthanum:60`
- `wiki-en-europium:27`
- `wiki-en-europium:58`
- `wiki-en-praseodymium:27`
- `wiki-en-praseodymium:59`

### 칸 안에 줄바꿈이 있는 표 (12)
- `wiki-ko-thulium:54`
- `wiki-ko-dysprosium:56`
- `wiki-ko-ytterbium:57`
- `wiki-ko-lutetium:54`
- `wiki-ko-isotopes-of-yttrium:9`
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-ko-erbium:55`
- `wiki-ko-samarium:56`
- `wiki-ko-yttrium:55`
- `wiki-ko-isotopes-of-terbium:9`
- `wiki-ko-isotopes-of-neodymium:11`
- `wiki-en-neutron-capture-therapy:187`

### 표 제목(caption)이 있는 표 (3)
- `wiki-en-neutron-capture-therapy:56`
- `wiki-en-neutron-capture-therapy:141`
- `wiki-en-samarium-cobalt-magnet:22`

### 표 전체 폭 줄(각주 등)이 있는 표 (2)
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-en-neutron-capture-therapy:141`

### 같은 대상이 이어진 여러 줄에 놓인 표 (9)
- `wiki-ko-isotopes-of-yttrium:9`
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-ko-yttrium:55`
- `wiki-ko-isotopes-of-terbium:9`
- `wiki-ko-isotopes-of-neodymium:11`
- `wiki-en-lanthanum:60`
- `wiki-en-europium:58`
- `wiki-en-praseodymium:59`
- `wiki-en-neutron-capture-therapy:187`

### 줄마다 열의 뜻이 바뀌는 표 (4)
- `wiki-ko-isotopes-of-yttrium:9`
- `wiki-en-isotopes-of-yttrium:23`
- `wiki-ko-isotopes-of-terbium:9`
- `wiki-ko-isotopes-of-neodymium:11`

### 가로로 놓인 표(항목이 줄로 놓이고 머리글 줄이 값) (14)
기준: 줄이 둘(머리글 줄과 값 줄)이고 첫 칸이 줄 이름이다. 정보 상자의 증기 압력 표: 머리글 줄의 압력 값(1 Pa …)과 아래 줄의 온도 값이 열마다 짝이다
- `wiki-ko-thulium:26`
- `wiki-en-thulium:27`
- `wiki-ko-dysprosium:26`
- `wiki-en-dysprosium:27`
- `wiki-ko-ytterbium:26`
- `wiki-en-ytterbium:27`
- `wiki-ko-lutetium:26`
- `wiki-en-lutetium:27`
- `wiki-ko-erbium:26`
- `wiki-ko-samarium:26`
- `wiki-ko-yttrium:26`
- `wiki-en-lanthanum:27`
- `wiki-en-europium:27`
- `wiki-en-praseodymium:27`

### 머리글 첫 줄이 묶음 이름인 표 (8)
기준: 영어 정보 상자의 주요 동위원소 표: 첫 머리글 줄은 'Main isotopes'(세 열)와 'Decay'(두 열)이고 열 이름은 둘째 줄에 있다
- `wiki-en-thulium:59`
- `wiki-en-dysprosium:60`
- `wiki-en-ytterbium:60`
- `wiki-en-lutetium:59`
- `wiki-en-isotopes-of-yttrium:3`
- `wiki-en-lanthanum:60`
- `wiki-en-europium:58`
- `wiki-en-praseodymium:59`

### 한 칸에 여러 항목이 든 표(줄바꿈이 항목을 나눔) (2)
기준: 칸 안의 줄바꿈이 글이 길어 바꾼 것이 아니라 다른 항목을 나눈다. 변환은 줄바꿈을 빈칸 하나로 바꿔(decisions/stage2.md 2026-10-14 표 규칙 ㉢) 항목의 경계가 사라졌다
- `wiki-ko-yttrium:55`: 붕괴 에너지 칸에 값 둘: '0.48 ⏎ 0.38D', '1.83 ⏎ 0.89'
- `wiki-en-neutron-capture-therapy:187`: 첫 열의 머리글과 칸이 네 항목(Manufacturer, Product, Reaction, Accelerator type)을 한 칸에 담는다

### 목록을 여러 열로 나눈 표(한 줄의 칸끼리 관계가 없음) (1)
기준: 머리글 없이 이름 목록을 두 열로 흘려 놓은 표. 마크다운에서는 첫 줄이 머리글 자리에 놓였다
- `wiki-en-neutron-capture-therapy:56`: Table 1. 붕소 전달 물질 이름 23개를 두 열로 나눔

### 위 모양이 하나도 없는 표 (0)
