# 대조 카드: batch2_en-en.yaml

이 파일은 후보마다 카드 하나로, 순서표(data/questions/final_set_guide.md)의 "대조할 것"을 따라 카드마다 칸을 채운다. 확인한 칸은 [ ]를 [x]로 바꾼다. 하지 않은 칸은 그대로 둔다. 판정은 채택·수정·폐기 가운데 하나만 남긴다. 애매한 것은 메모에 적는다. 근거 구절이 원문에 글자 그대로 있는지, 개수·형식, 찾기 기록(`opposite_check`, `same_language_check`)의 찾을 말 개수와 언어는 후보 검사가 이미 봤다. 찾을 말이 문서에서 나오는 곳(걸린 곳)은 프로그램이 찾았다. 카드의 이름표는 후보 YAML 칸 이름을 백틱으로 적고 괄호에 한국어 뜻을 붙인다(예: `passage`(근거 구절)). 칸 뜻은 순서표(data/questions/final_set_guide.md)의 "후보 YAML 칸의 뜻"에 있다. 카드마다 끝에 그 후보의 원본 YAML을 참고용으로 붙인다.

---

## c-013 · `type`(유형): single_fact(단일 사실) · 도시 갈래: 두 언어 도시(청주시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): During Hideyoshi's Invasions of Korea, how many Korean warrior monks participated in the Battle of Cheongju in 1593?
- `answer`(정답): More than 8,000
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: More than 8,000 Korean warrior monks participated in the Battle of Cheongju in 1593. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-cheongju.md 42줄](../../../data/corpus/markdown/wiki-en-cheongju.md#L42) · `location`(위치): History
    > In 1593, the Battle of Cheongju took place between Japanese forces and Joseon that then ruled the Korean peninsula during Hideyoshi's Invasions of Korea, in which more than 8,000 Korean warrior monks participated.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `More than 8,000` · 정답과 사실에서 뽑은 숫자: `8,000`, `1593`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-cheongju): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378953230 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `1593`, `8,000`, `warrior monks`, `Battle of Cheongju`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서가 아닌 같은 언어 문서의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `1593`, `warrior monks`, `Battle of Cheongju`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다.
- `term`(찾을 말) `8,000`:
  - 걸린 곳 1: [wiki-en-jeonju.md 80줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L80) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > | 1975 | 30[8,000] | +20.8% |

  - 걸린 곳 2: [wiki-en-jeonju.md 87줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L87) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > | 2010 | 64[8,000] | +4.0% |

  - 걸린 곳 3: [wiki-en-jeonju.md 88줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L88) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > | 2015 | 65[8,000] | +1.5% |
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말과, 프로그램이 한국어 문서 14개에서 찾은 걸린 곳 전부다. 찾을 말 `1593년`, `승병`, `8000명`, `청주 전투`: 걸린 곳이 없다.
- `term`(찾을 말) `8,000`:
  - 걸린 곳 1: [wiki-ko-jeonju.md 184줄](../../../data/corpus/markdown/wiki-ko-jeonju.md#L184) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42643645
    > | 1975 | 30[8,000] | +20.8% |

  - 걸린 곳 2: [wiki-ko-jeonju.md 191줄](../../../data/corpus/markdown/wiki-ko-jeonju.md#L191) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42643645
    > | 2010 | 64[8,000] | +4.0% |

  - 걸린 곳 3: [wiki-ko-jeonju.md 192줄](../../../data/corpus/markdown/wiki-ko-jeonju.md#L192) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42643645
    > | 2015 | 65[8,000] | +1.5% |

  - 걸린 곳 4: [wiki-ko-sejong.md 451줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L451) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42585449
    > …와 강내면 3개리가 편입된데 대해서는 받아들일수 없다는 입장이다. 이들 지역이 세종시에 편입되면 당장 인구 [8,000]명이 줄고 지방세 및 교부세가 연간 200억원가량 감소하는 불이익이 예상되기 때문이다. 김재욱 청원군수는 이…

  - 걸린 곳 5: [wiki-ko-gwangju.md 320줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L320) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42623705
    > …2,644 | 323,066 | 411,196 | 488,154 | 441,000 | 479,880 | 52[8,000] |
- 할 일: 걸린 문장을 하나씩 읽는다.
- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `1593년`, `승병`, `8,000`, `8000명`, `청주 전투`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(청주시)의 한국어 문서를 통째로 읽었다
- 할 일 1 (wiki-ko-cheongju): [wiki-ko-cheongju.md](../../../data/corpus/markdown/wiki-ko-cheongju.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 2 (kto-ko-cheongju-cheongnamdae): [kto-ko-cheongju-cheongnamdae.md](../../../data/corpus/markdown/kto-ko-cheongju-cheongnamdae.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 single_fact(단일 사실)다. 아래 뜻과 견준다.
- 단일 사실: 질문이 근거 구절의 핵심 낱말을 그대로 썼다(이름은 빼고 본다). 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?

<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>

- "During"(~동안) → "during"(~동안) · 같은 말 · 핵심 낱말 아니오 · 같은 시간 관계를 나타내는 말이다.
- "Hideyoshi's Invasions of Korea,"(히데요시의 조선 침략) → "Hideyoshi's Invasions of Korea"(히데요시의 조선 침략) · 이름 · 핵심 낱말 아니오 · 역사적 사건의 고유명사다.
- "how many"(몇 명) → "more than 8,000"(8,000명 넘게) · 같은 말 · 핵심 낱말 아니오 · 인원수를 묻는 틀이며 근거 구절에서 그 인원수를 제시한다.
- "Korean warrior monks"(한국인 승병들) → "Korean warrior monks"(한국인 승병들) · 같은 말 · 핵심 낱말 예 · 근거 구절의 말을 그대로 썼다.
- "participated"(참여했나) → "participated"(참여했다) · 같은 말 · 핵심 낱말 예 · 근거 구절의 말을 그대로 썼다.
- "in"(~에) → "in which"(그 전투에) · 같은 말 · 핵심 낱말 아니오 · 전투에 참여했다는 관계를 나타내며, 근거 구절에서도 같은 전치사를 썼다.
- "the Battle of Cheongju"(청주 전투) → "the Battle of Cheongju"(청주 전투) · 이름 · 핵심 낱말 아니오 · 전투의 고유명사다.
- "in 1593?"(1593년에?) → "In 1593"(1593년에) · 같은 말 · 핵심 낱말 예 · 같은 연도를 그대로 나타냈다.

</details>

- 판단할 질문: ChatGPT 목록에서 "가르기 어려움"이나 "짝 없음"인 줄마다, 그 조각의 뜻이 문서에 있는가? (근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)
- 판단할 질문: ChatGPT 목록에서 "핵심 낱말 예"인 줄에 "바꾼 말"이 없는가? (있으면 단일 사실이 아니다)
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-013
question: During Hideyoshi's Invasions of Korea, how many Korean warrior monks participated
  in the Battle of Cheongju in 1593?
question_language: en
evidence_language: en
type: single_fact
answer: More than 8,000
required_facts:
- fact: More than 8,000 Korean warrior monks participated in the Battle of Cheongju
    in 1593.
  in_answer: true
  evidence:
  - doc_id: wiki-en-cheongju
    location: History
    passage: In 1593, the Battle of Cheongju took place between Japanese forces and
      Joseon that then ruled the Korean peninsula during Hideyoshi's Invasions of
      Korea, in which more than 8,000 Korean warrior monks participated.
opposite_check:
- 1593년
- 승병
- 8,000
- 8000명
- 청주 전투
same_language_check:
- '1593'
- 8,000
- warrior monks
- Battle of Cheongju
```

</details>

---

## c-014 · `type`(유형): paraphrase(표현 불일치) · 도시 갈래: 두 언어 도시(천안시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): In South Korea, which city is home to a correctional facility specifically designated for non-Korean inmates?
- `answer`(정답): Cheonan
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Cheonan is the site of a prison exclusively intended for foreign prisoners. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-cheonan.md 208줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L208) · `location`(위치): Population diversity
    > In addition, Cheonan is the site of the prison exclusively intended for foreign prisoners, with more than 1,000 foreign inmates.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `Cheonan` · 정답과 사실에서 뽑은 숫자: 없음
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-cheonan): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378953224 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `exclusively intended for foreign`, `foreign prisoners`, `foreign inmates`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `exclusively intended for foreign`, `foreign prisoners`, `foreign inmates`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말과, 프로그램이 한국어 문서 14개에서 찾은 걸린 곳 전부다. 찾을 말 `외국인 교도소`, `외국인 수감자`, `1,000명`: 걸린 곳이 없다.
- `term`(찾을 말) `교도소`:
  - 걸린 곳 1: [wiki-ko-cheongju.md 395줄](../../../data/corpus/markdown/wiki-ko-cheongju.md#L395) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42630014
    > - 청주[교도소], 청주여자교도소 (서원구 미평동)

  - 걸린 곳 2: [wiki-ko-cheongju.md 395줄](../../../data/corpus/markdown/wiki-ko-cheongju.md#L395) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42630014
    > - 청주교도소, 청주여자[교도소] (서원구 미평동)

  - 걸린 곳 3: [wiki-ko-gyeongju.md 449줄](../../../data/corpus/markdown/wiki-ko-gyeongju.md#L449) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42639825
    > - 대구지방교정청 경주[교도소]
- 할 일: 걸린 문장을 하나씩 읽는다.
- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `외국인 교도소`, `외국인 수감자`, `교도소`, `1,000명`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(천안시)의 한국어 문서를 통째로 읽었다
- 할 일 1 (wiki-ko-cheonan): [wiki-ko-cheonan.md](../../../data/corpus/markdown/wiki-ko-cheonan.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 2 (kto-ko-cheonan-samgeori-park): [kto-ko-cheonan-samgeori-park.md](../../../data/corpus/markdown/kto-ko-cheonan-samgeori-park.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 paraphrase(표현 불일치)다. 질문을 뜻이 끊기는 조각으로 나눠, 아래 짝 목록에 조각마다 한 줄씩 `질문 조각 → 근거 구절의 짝 (같은 말 / 바꾼 말 / 이름)` 꼴로 적는다(예: `처음 생긴 → 창단된 (바꾼 말)`). 이름(고유명사)은 "이름"으로 적는다. 줄이 모자라면 더한다. 목록을 다 채운 뒤 아래 접힌 칸을 펼쳐 Gemini가 적은 바꾼 말과 견준다.
- 표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).
- 짝 목록:
  - 
  - 
  - 
  - 

- 판단할 질문: "바꾼 말" 줄이 하나 이상 있는가?
- 판단할 질문: 질문에 그대로 쓴 낱말("같은 말" 줄)이 답을 드러내지 않는가? (예: "특별자치시". 드러내면 바꾼 말을 찾지 않아도 답이 나오므로 쓸 수 없다. "이름" 줄은 답을 가리키는 설명이라 빼고 본다)
- 판단할 질문: 접힌 칸의 Gemini 짝 가운데 짝 목록과 다른 것이 없는가?

<details><summary>Gemini가 적은 바꾼 말(짝 목록을 채운 뒤 펼친다)</summary>

"prison exclusively intended for foreign prisoners"를 "correctional facility specifically designated for non-Korean inmates"로 바꿈.

</details>

<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>

- "In South Korea"(대한민국에서) → 없음 · 짝 없음 · 핵심 낱말 예 · 근거 구절에는 대한민국이라는 위치 정보가 나오지 않는다.
- "which city"(어느 도시) → "Cheonan"(천안) · 가르기 어려움 · 핵심 낱말 아니오 · 장소를 묻는 틀과 구체적인 지명은 같은 뜻이 아니며, 근거 구절에는 도시라는 분류가 명시되어 있지 않다.
- "is home to"(~가 자리하고 있다) → "is the site of"(~의 소재지이다) · 바꾼 말 · 핵심 낱말 예 · 어떤 시설이 자리한 곳이라는 뜻을 다른 말로 표현했다.
- "a correctional facility"(교정시설) → "the prison"(교도소) · 가르기 어려움 · 핵심 낱말 예 · 교정시설은 교도소보다 넓은 범위의 시설을 가리킨다.
- "specifically designated for"(특별히 지정된) → "exclusively intended for"(오직 ~을 위해 마련된) · 가르기 어려움 · 핵심 낱말 예 · 특정 대상을 위한 시설이라는 뜻은 겹치지만, 근거 구절은 다른 대상을 배제한다는 더 강한 뜻을 담고 있다.
- "non-Korean inmates"(한국인이 아닌 수감자들) → "foreign prisoners"(외국인 수감자들) · 바꾼 말 · 핵심 낱말 예 · 외국인 수감자를 한국인이 아닌 수감자라는 다른 표현으로 나타냈다.

</details>

- 판단할 질문: ChatGPT 목록에서 "가르기 어려움"이나 "짝 없음"인 줄마다, 그 조각의 뜻이 문서에 있는가? (근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)
- 판단할 질문: ChatGPT 목록에서 "핵심 낱말 예"인 줄에 "바꾼 말"이 하나 이상 있는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-014
question: In South Korea, which city is home to a correctional facility specifically
  designated for non-Korean inmates?
question_language: en
evidence_language: en
type: paraphrase
answer: Cheonan
required_facts:
- fact: Cheonan is the site of a prison exclusively intended for foreign prisoners.
  in_answer: true
  evidence:
  - doc_id: wiki-en-cheonan
    location: Population diversity
    passage: In addition, Cheonan is the site of the prison exclusively intended for
      foreign prisoners, with more than 1,000 foreign inmates.
opposite_check:
- 외국인 교도소
- 외국인 수감자
- 교도소
- 1,000명
same_language_check:
- exclusively intended for foreign
- foreign prisoners
- foreign inmates
```

</details>

---

## c-015 · `type`(유형): paraphrase(표현 불일치) · 도시 갈래: 두 언어 도시(전주시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Which globally recognized b-boy dance group, known for winning a major international competition, originated in Jeonju?
- `answer`(정답): Last for One
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Jeonju is the hometown of the breakdancing crew Last for One, who are international Battle of the Year champions. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-jeonju.md 164줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L164) · `location`(위치): Attractions
    > Jeonju is the hometown of the breakdancing crew Last for One, international Battle of the Year champions.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `Last for One` · 정답과 사실에서 뽑은 숫자: 없음
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-jeonju): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1379135207 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `Last for One`, `Battle of the Year`, `breakdancing crew`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `Last for One`, `Battle of the Year`, `breakdancing crew`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말 `라스트 포 원`, `배틀 오브 더 이어`, `브레이크댄스`: 프로그램이 한국어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `라스트 포 원`, `배틀 오브 더 이어`, `브레이크댄스`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(전주시)의 한국어 문서를 통째로 읽었다
- 할 일 1 (wiki-ko-jeonju): [wiki-ko-jeonju.md](../../../data/corpus/markdown/wiki-ko-jeonju.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 2 (kto-ko-jeonju-hanok-village): [kto-ko-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-ko-jeonju-hanok-village.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 3 (portal-ko-jeonju-population): [portal-ko-jeonju-population.md](../../../data/corpus/markdown/portal-ko-jeonju-population.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 paraphrase(표현 불일치)다. 질문을 뜻이 끊기는 조각으로 나눠, 아래 짝 목록에 조각마다 한 줄씩 `질문 조각 → 근거 구절의 짝 (같은 말 / 바꾼 말 / 이름)` 꼴로 적는다(예: `처음 생긴 → 창단된 (바꾼 말)`). 이름(고유명사)은 "이름"으로 적는다. 줄이 모자라면 더한다. 목록을 다 채운 뒤 아래 접힌 칸을 펼쳐 Gemini가 적은 바꾼 말과 견준다.
- 표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).
- 짝 목록:
  - 
  - 
  - 
  - 

- 판단할 질문: "바꾼 말" 줄이 하나 이상 있는가?
- 판단할 질문: 질문에 그대로 쓴 낱말("같은 말" 줄)이 답을 드러내지 않는가? (예: "특별자치시". 드러내면 바꾼 말을 찾지 않아도 답이 나오므로 쓸 수 없다. "이름" 줄은 답을 가리키는 설명이라 빼고 본다)
- 판단할 질문: 접힌 칸의 Gemini 짝 가운데 짝 목록과 다른 것이 없는가?

<details><summary>Gemini가 적은 바꾼 말(짝 목록을 채운 뒤 펼친다)</summary>

"breakdancing crew"를 "b-boy dance group"으로, "international Battle of the Year champions"를 "winning a major international competition"으로, "hometown"을 "originated in"으로 바꿈.

</details>

<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>

- "Which"(어느) → "Last for One"(라스트 포 원) · 가르기 어려움 · 핵심 낱말 아니오 · 대상을 묻는 말과 근거 구절에 나온 구체적인 이름은 같은 뜻이 아니다.
- "globally recognized"(세계적으로 인정받는) → 없음 · 짝 없음 · 핵심 낱말 예 · 근거 구절은 국제 대회 우승 사실을 말하지만 세계적으로 인정받는다는 뜻은 직접 나타내지 않는다.
- "b-boy dance group"(비보이 춤 그룹) → "breakdancing crew"(브레이크댄스 팀) · 바꾼 말 · 핵심 낱말 예 · 브레이크댄스를 하는 팀이라는 뜻을 다른 말로 표현했다.
- "known for"(~로 알려진) → 없음 · 짝 없음 · 핵심 낱말 예 · 근거 구절에는 우승 사실만 있으며 그 사실로 유명하거나 알려졌다는 설명은 없다.
- "winning"(우승한) → "champions"(우승자들) · 바꾼 말 · 핵심 낱말 예 · 우승자라는 말을 우승했다는 동작으로 바꿔 표현했다.
- "a major"(주요한) → 없음 · 짝 없음 · 핵심 낱말 예 · 근거 구절에는 대회가 주요하거나 중요한 대회라는 설명이 없다.
- "international"(국제적인) → "international"(국제적인) · 같은 말 · 핵심 낱말 예 · 근거 구절의 말을 그대로 썼다.
- "competition"(대회) → "Battle of the Year"(배틀 오브 더 이어) · 가르기 어려움 · 핵심 낱말 예 · 대회라는 일반적인 표현과 특정 대회의 고유명사는 가리키는 범위가 다르다.
- "originated in"(~에서 시작된) → "is the hometown of"(~의 고향이다) · 바꾼 말 · 핵심 낱말 예 · 해당 팀이 나온 곳이라는 뜻을 고향이라는 말 대신 시작된 곳으로 표현했다.
- "Jeonju"(전주) → "Jeonju"(전주) · 이름 · 핵심 낱말 아니오 · 지명의 고유명사다.

</details>

- 판단할 질문: ChatGPT 목록에서 "가르기 어려움"이나 "짝 없음"인 줄마다, 그 조각의 뜻이 문서에 있는가? (근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)
- 판단할 질문: ChatGPT 목록에서 "핵심 낱말 예"인 줄에 "바꾼 말"이 하나 이상 있는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-015
question: Which globally recognized b-boy dance group, known for winning a major international
  competition, originated in Jeonju?
question_language: en
evidence_language: en
type: paraphrase
answer: Last for One
required_facts:
- fact: Jeonju is the hometown of the breakdancing crew Last for One, who are international
    Battle of the Year champions.
  in_answer: true
  evidence:
  - doc_id: wiki-en-jeonju
    location: Attractions
    passage: Jeonju is the hometown of the breakdancing crew Last for One, international
      Battle of the Year champions.
opposite_check:
- 라스트 포 원
- 배틀 오브 더 이어
- 브레이크댄스
same_language_check:
- Last for One
- Battle of the Year
- breakdancing crew
```

</details>

---

## c-016 · `type`(유형): multi_doc(여러 문서 연결) · 도시 갈래: 두 언어 도시(청주시, 천안시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): According to the provided documents, how many vehicles were trapped when a tunnel flooded in Cheongju during the annual monsoon, and what is the literal meaning of Cheonan's Samgeori park?
- `answer`(정답): 15 vehicles were trapped in Cheongju, and Samgeori means '3-way intersection'.
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: The Cheongju tunnel flooded during the annual monsoon, trapping 15 vehicles. · 정답에 들어감(`in_answer: true`)
  - `fact`(사실) 2: Cheonan's Samgeori park means '3-way intersection'. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-cheongju.md 113줄](../../../data/corpus/markdown/wiki-en-cheongju.md#L113) · `location`(위치): Transport
    > In 2023, the Cheongju tunnel flooded during the annual monsoon which trapped 15 vehicles and resulted in at least 7 deaths and 11 reported missing.
  - 사실 2의 근거 1: [wiki-en-cheonan.md 32줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L32) · `location`(위치): History
    > Cheonan's Samgeori (meaning "3-way intersection") park has been noted as a strategic point of transportation and a place where culture has spread for a long time.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: 위 `answer`(정답)에서 값마다 골라 찾는다 · 정답과 사실에서 뽑은 숫자: `15`, `3`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-cheongju): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378953230 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 할 일 2 (wiki-en-cheonan): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378953224 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서 안의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `trapped 15 vehicles`, `annual monsoon`, `3-way intersection`: 근거 문서 안에서는 걸린 곳이 없다.
- `term`(찾을 말) `Samgeori`:
  - 걸린 곳 1: [wiki-en-cheonan.md 118줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L118) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953224
    > [Samgeori] park has been a strategic point of transportation and a pla…

  - 걸린 곳 2: [wiki-en-cheonan.md 120줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L120) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953224
    > …geori is a resting area for the animal residents of Cheonan [Samgeori] Park, and it provides scenery for visitors with its willow …
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서가 아닌 같은 언어 문서의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `trapped 15 vehicles`, `annual monsoon`, `3-way intersection`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다.
- `term`(찾을 말) `Samgeori`:
  - 걸린 곳 1: [kto-en-cheonan-samgeori-park.md 7줄](../../../data/corpus/markdown/kto-en-cheonan-samgeori-park.md#L7) · 짧은 문서라 링크를 열어 전체를 볼 수 있다
    > …on Park was established in the 1970s to commemorate Cheonan [Samgeori], a junction of the Samnamdaero (Great Road connecting Hanya…
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말과, 프로그램이 한국어 문서 14개에서 찾은 걸린 곳 전부다. 찾을 말 `차량 15대`, `15대 고립`, `세 거리`, `세 갈래`: 걸린 곳이 없다.
- `term`(찾을 말) `삼거리`:
  - 걸린 곳 1: [wiki-ko-cheonan.md 290줄](../../../data/corpus/markdown/wiki-ko-cheonan.md#L290) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42545685
    > … - 1호선 경부고속도로 (충청북도 청주시) ← 천안호두휴게소 - 독립기념관 나들목 - 천안 분기점 - 천안[삼거리]휴게소 - 천안 나들목 - 망향휴게소 - 북천안 나들목 - 입장거봉포도휴게소 → (경기도 안성시)

  - 걸린 곳 2: [wiki-ko-suwon.md 305줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L305) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42534963
    > - 중부대로 : 중동사거리(기점) - 가톨릭대학교 성빈센트병원 - 동수원사거리 (경수대로) - 아주대[삼거리] - 법원사거리 - 나촌말삼거리 → (용인시 기흥구 영덕동)

  - 걸린 곳 3: [wiki-ko-suwon.md 305줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L305) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42534963
    > …리(기점) - 가톨릭대학교 성빈센트병원 - 동수원사거리 (경수대로) - 아주대삼거리 - 법원사거리 - 나촌말[삼거리] → (용인시 기흥구 영덕동)

  - 걸린 곳 4: [kto-ko-cheonan-samgeori-park.md 1줄](../../../data/corpus/markdown/kto-ko-cheonan-samgeori-park.md#L1) · 짧은 문서라 링크를 열어 전체를 볼 수 있다
    > # 천안[삼거리]공원

  - 걸린 곳 5: [kto-ko-cheonan-samgeori-park.md 7줄](../../../data/corpus/markdown/kto-ko-cheonan-samgeori-park.md#L7) · 짧은 문서라 링크를 열어 전체를 볼 수 있다
    > 조선 시대부터 한양과 경상도, 전라도를 잇는 삼남대로의 분기점이자 민요 흥타령으로 유명한 천안[삼거리]를 기념해 1970년대 조성한 공원이다. 행사장과 주차장 위주로 쓰이던 공간을 재개발해 2025년 9월 가족…
- 할 일: 걸린 문장을 하나씩 읽는다.
- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `차량 15대`, `15대 고립`, `세 거리`, `세 갈래`, `삼거리`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(청주시, 천안시)의 한국어 문서를 통째로 읽었다
- 할 일 1 (wiki-ko-cheongju): [wiki-ko-cheongju.md](../../../data/corpus/markdown/wiki-ko-cheongju.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 2 (wiki-ko-cheonan): [wiki-ko-cheonan.md](../../../data/corpus/markdown/wiki-ko-cheonan.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 3 (kto-ko-cheongju-cheongnamdae): [kto-ko-cheongju-cheongnamdae.md](../../../data/corpus/markdown/kto-ko-cheongju-cheongnamdae.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 4 (kto-ko-cheonan-samgeori-park): [kto-ko-cheonan-samgeori-park.md](../../../data/corpus/markdown/kto-ko-cheonan-samgeori-park.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 multi_doc(여러 문서 연결)다. 아래 뜻과 견준다.
- 여러 문서 연결: 둘 이상의 문서나 구절을 합쳐야 답이 나온다(비교, 집계, 여러 단계). 표의 값이나 수치를 비교하는 질문도 여기다. 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-016
question: According to the provided documents, how many vehicles were trapped when
  a tunnel flooded in Cheongju during the annual monsoon, and what is the literal
  meaning of Cheonan's Samgeori park?
question_language: en
evidence_language: en
type: multi_doc
answer: 15 vehicles were trapped in Cheongju, and Samgeori means '3-way intersection'.
required_facts:
- fact: The Cheongju tunnel flooded during the annual monsoon, trapping 15 vehicles.
  in_answer: true
  evidence:
  - doc_id: wiki-en-cheongju
    location: Transport
    passage: In 2023, the Cheongju tunnel flooded during the annual monsoon which
      trapped 15 vehicles and resulted in at least 7 deaths and 11 reported missing.
- fact: Cheonan's Samgeori park means '3-way intersection'.
  in_answer: true
  evidence:
  - doc_id: wiki-en-cheonan
    location: History
    passage: Cheonan's Samgeori (meaning "3-way intersection") park has been noted
      as a strategic point of transportation and a place where culture has spread
      for a long time.
opposite_check:
- 차량 15대
- 15대 고립
- 세 거리
- 세 갈래
- 삼거리
same_language_check:
- trapped 15 vehicles
- annual monsoon
- 3-way intersection
- Samgeori
```

</details>

---

## c-017 · `type`(유형): multi_doc(여러 문서 연결) · 도시 갈래: 두 언어 도시(천안시, 전주시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Which city's gallery features an installation of Damien Hirst's 'Hymn' in a glass box, and which city's international music festival was named among Songlines' 25 Best International Festivals in 2014?
- `answer`(정답): Cheonan features 'Hymn', and Jeonju's festival was named by Songlines.
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Cheonan's Arario Gallery has an installation of Damien Hirst's 'Hymn' in a glass box. · 정답에 들어감(`in_answer: true`)
  - `fact`(사실) 2: The Jeonju International Sori Festival was among Songlines' 25 Best International Festivals in 2014. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-cheonan.md 126줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L126) · `location`(위치): Galleries
    > There is also an installation of Damien Hirst's "Hymn" in a glass box constructed as a part of the building.
  - 사실 2의 근거 1: [wiki-en-jeonju.md 162줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L162) · `location`(위치): Attractions
    > The Jeonju International Sori Festival was among Songlines' 25 Best International Festivals in 2014.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: 위 `answer`(정답)에서 값마다 골라 찾는다 · 정답과 사실에서 뽑은 숫자: `25`, `2014`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-cheonan): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378953224 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 할 일 2 (wiki-en-jeonju): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1379135207 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `Damien Hirst's`, `glass box`, `Songlines`, `25 Best International Festivals`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `Damien Hirst's`, `glass box`, `Songlines`, `25 Best International Festivals`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말 `데미안 허스트`, `송라인즈`, `유리 상자`, `25대 페스티벌`: 프로그램이 한국어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `데미안 허스트`, `송라인즈`, `유리 상자`, `25대 페스티벌`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(천안시, 전주시)의 한국어 문서를 통째로 읽었다
- 할 일 1 (wiki-ko-jeonju): [wiki-ko-jeonju.md](../../../data/corpus/markdown/wiki-ko-jeonju.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 2 (wiki-ko-cheonan): [wiki-ko-cheonan.md](../../../data/corpus/markdown/wiki-ko-cheonan.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 3 (kto-ko-jeonju-hanok-village): [kto-ko-jeonju-hanok-village.md](../../../data/corpus/markdown/kto-ko-jeonju-hanok-village.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 4 (kto-ko-cheonan-samgeori-park): [kto-ko-cheonan-samgeori-park.md](../../../data/corpus/markdown/kto-ko-cheonan-samgeori-park.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 5 (portal-ko-jeonju-population): [portal-ko-jeonju-population.md](../../../data/corpus/markdown/portal-ko-jeonju-population.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 multi_doc(여러 문서 연결)다. 아래 뜻과 견준다.
- 여러 문서 연결: 둘 이상의 문서나 구절을 합쳐야 답이 나온다(비교, 집계, 여러 단계). 표의 값이나 수치를 비교하는 질문도 여기다. 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-017
question: Which city's gallery features an installation of Damien Hirst's 'Hymn' in
  a glass box, and which city's international music festival was named among Songlines'
  25 Best International Festivals in 2014?
question_language: en
evidence_language: en
type: multi_doc
answer: Cheonan features 'Hymn', and Jeonju's festival was named by Songlines.
required_facts:
- fact: Cheonan's Arario Gallery has an installation of Damien Hirst's 'Hymn' in a
    glass box.
  in_answer: true
  evidence:
  - doc_id: wiki-en-cheonan
    location: Galleries
    passage: There is also an installation of Damien Hirst's "Hymn" in a glass box
      constructed as a part of the building.
- fact: The Jeonju International Sori Festival was among Songlines' 25 Best International
    Festivals in 2014.
  in_answer: true
  evidence:
  - doc_id: wiki-en-jeonju
    location: Attractions
    passage: The Jeonju International Sori Festival was among Songlines' 25 Best International
      Festivals in 2014.
opposite_check:
- 데미안 허스트
- 송라인즈
- 유리 상자
- 25대 페스티벌
same_language_check:
- Damien Hirst's
- glass box
- Songlines
- 25 Best International Festivals
```

</details>

---

## c-018 · `type`(유형): single_fact(단일 사실) · 도시 갈래: 두 언어 도시(춘천시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Opened in 2022, Legoland Korea Resort holds what ranking in terms of size among all Legoland theme parks in the world?
- `answer`(정답): It is the 2nd largest in the world.
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Legoland Korea Resort is the 2nd largest Legoland theme park in the world. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-chuncheon.md 134줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L134) · `location`(위치): Resort
    > Legoland Korea Resort, the 10th Legoland theme park and the 2nd largest in the world, opened in 2022.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: 위 `answer`(정답)에서 값마다 골라 찾는다 · 정답과 사실에서 뽑은 숫자: `2`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-chuncheon): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1376994978 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `10th Legoland`, `2nd largest in the world`, `Legoland Korea Resort`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `10th Legoland`, `2nd largest in the world`, `Legoland Korea Resort`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말과, 프로그램이 한국어 문서 14개에서 찾은 걸린 곳 전부다. 찾을 말 `세계 2위`, `두 번째로 큰`: 걸린 곳이 없다.
- `term`(찾을 말) `레고랜드`:
  - 걸린 곳 1: [wiki-ko-chuncheon.md 279줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L279) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42647646
    > - [레고랜드] 코리아: 중도에 있음.

- `term`(찾을 말) `10번째`:
  - 걸린 곳 1: [wiki-ko-suwon.md 250줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L250) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42534963
    > 2013년 KBO 리그 [10번째] 구단인 kt wiz가 창단됐다. 2014년 한국 야구 퓨처스 리그에 참가하고, 2015년부터 1군 페넌트레…
- 할 일: 걸린 문장을 하나씩 읽는다.
- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `레고랜드`, `세계 2위`, `두 번째로 큰`, `10번째`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(춘천시)의 한국어 문서를 통째로 읽었다
- 할 일 1 (wiki-ko-chuncheon): [wiki-ko-chuncheon.md](../../../data/corpus/markdown/wiki-ko-chuncheon.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 할 일 2 (kto-ko-chuncheon-samaksan-cable-car): [kto-ko-chuncheon-samaksan-cable-car.md](../../../data/corpus/markdown/kto-ko-chuncheon-samaksan-cable-car.md)를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다.
- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 single_fact(단일 사실)다. 아래 뜻과 견준다.
- 단일 사실: 질문이 근거 구절의 핵심 낱말을 그대로 썼다(이름은 빼고 본다). 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?

<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>

- "Opened in 2022"(2022년에 개장한) → "opened in 2022"(2022년에 개장했다) · 같은 말 · 핵심 낱말 예 · 개장과 연도를 나타내는 말을 그대로 썼다.
- "Legoland Korea Resort"(레고랜드 코리아 리조트) → "Legoland Korea Resort"(레고랜드 코리아 리조트) · 이름 · 핵심 낱말 아니오 · 시설의 고유명사다.
- "holds what ranking"(몇 위에 해당하는가) → "the 2nd"(두 번째) · 가르기 어려움 · 핵심 낱말 아니오 · 순위를 묻는다는 점은 겹치지만, 질문은 순위 값을 묻고 근거 구절은 구체적인 순위를 제시한다.
- "in terms of size"(크기를 기준으로) → "largest"(가장 큰) · 가르기 어려움 · 핵심 낱말 예 · 크기를 비교한다는 뜻은 겹치지만, 근거 구절의 말에는 크기가 큰 쪽을 기준으로 한다는 뜻이 더 들어 있다.
- "among all"(모든 것 가운데) → "in the world"(전 세계에서) · 가르기 어려움 · 핵심 낱말 아니오 · 전체를 비교 대상으로 삼는다는 뜻은 겹치지만, 모든 대상과 세계라는 범위는 같은 말이 아니다.
- "Legoland theme parks"(레고랜드 테마파크들) → "Legoland theme park"(레고랜드 테마파크) · 같은 말 · 핵심 낱말 예 · 근거 구절의 말을 그대로 썼으며 단수와 복수의 차이만 있다.
- "in the world"(세계에서) → "in the world"(세계에서) · 같은 말 · 핵심 낱말 예 · 비교하는 지역적 범위를 그대로 나타냈다.

</details>

- 판단할 질문: ChatGPT 목록에서 "가르기 어려움"이나 "짝 없음"인 줄마다, 그 조각의 뜻이 문서에 있는가? (근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)
- 판단할 질문: ChatGPT 목록에서 "핵심 낱말 예"인 줄에 "바꾼 말"이 없는가? (있으면 단일 사실이 아니다)
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-018
question: Opened in 2022, Legoland Korea Resort holds what ranking in terms of size
  among all Legoland theme parks in the world?
question_language: en
evidence_language: en
type: single_fact
answer: It is the 2nd largest in the world.
required_facts:
- fact: Legoland Korea Resort is the 2nd largest Legoland theme park in the world.
  in_answer: true
  evidence:
  - doc_id: wiki-en-chuncheon
    location: Resort
    passage: Legoland Korea Resort, the 10th Legoland theme park and the 2nd largest
      in the world, opened in 2022.
opposite_check:
- 레고랜드
- 세계 2위
- 두 번째로 큰
- 10번째
same_language_check:
- 10th Legoland
- 2nd largest in the world
- Legoland Korea Resort
```

</details>

---

## c-019 · `type`(유형): table_numeric(표·수치·조건) · 도시 갈래: 영어 도시(부산광역시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): According to the historical population data for Busan, what was the city's population in 1970?
- `answer`(정답): 1,842,259
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Busan's population in 1970 was 1,842,259. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-busan.md 358줄](../../../data/corpus/markdown/wiki-en-busan.md#L358) · `location`(위치): Demographics
    > | Year | Pop. | ±% |
    > | 1970 | 1,842,259 | +59.6% |

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `1,842,259` · 정답과 사실에서 뽑은 숫자: `1,842,259`, `1970`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-busan): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1379685823 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서 안의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `1970`, `1,842,259`: 근거 문서 안에서는 걸린 곳이 없다.
- `term`(찾을 말) `Historical population`:
  - 걸린 곳 1: [wiki-en-busan.md 356줄](../../../data/corpus/markdown/wiki-en-busan.md#L356) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379685823
    > [Historical population]
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서가 아닌 같은 언어 문서의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `1,842,259`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다.
- `term`(찾을 말) `1970`:
  - 걸린 곳 1: [wiki-en-jeonju.md 79줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L79) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > | [1970] | 255,000 | +19.7% |

  - 걸린 곳 2: [wiki-en-cheongju.md 46줄](../../../data/corpus/markdown/wiki-en-cheongju.md#L46) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953230
    > …ea, having almost quadrupled its population from 147,000 in [1970] to 582,158 in 2000.

  - 걸린 곳 3: [wiki-en-chuncheon.md 57줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L57) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > | [1970] | 209,821 | +9.5% |

  - 걸린 곳 4: [wiki-en-chuncheon.md 118줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L118) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > …. Subsequently, Myeongdong Dakgalbi Alley was formed in the [1970]s. Mak-guksu are dark-colored noodles made from buckwheat. I…

  - 걸린 곳 5: [wiki-en-chuncheon.md 118줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L118) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > …ate-night snack but began to be eaten in all seasons in the [1970]s.

  - 걸린 곳 6: [wiki-en-jeju.md 37줄](../../../data/corpus/markdown/wiki-en-jeju.md#L37) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1377658564
    > The city has grown quite rapidly since the [1970]s. Shin Jeju (신제주), or "new Jeju", was created some decades …

  - 걸린 곳 7: [wiki-en-jeju.md 37줄](../../../data/corpus/markdown/wiki-en-jeju.md#L37) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1377658564
    > …of buildings that were common throughout the city until the [1970]s are gradually disappearing.

  - 걸린 곳 8: [wiki-en-andong.md 33줄](../../../data/corpus/markdown/wiki-en-andong.md#L33) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378924154
    > Since the [1970]s Andong has developed rapidly, although the population has …

  - 걸린 곳 9: [wiki-en-andong.md 37줄](../../../data/corpus/markdown/wiki-en-andong.md#L37) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378924154
    > … education and Korean folklore, has grown rapidly since the [1970]s. Other tertiary institutions include Andong Science Colleg…

  - 걸린 곳 10: [kto-en-cheonan-samgeori-park.md 7줄](../../../data/corpus/markdown/kto-en-cheonan-samgeori-park.md#L7) · 짧은 문서라 링크를 열어 전체를 볼 수 있다
    > … Cheonan Three-way Intersection Park was established in the [1970]s to commemorate Cheonan Samgeori, a junction of the Samnamd…

- `term`(찾을 말) `Historical population`:
  - 걸린 곳 1: [wiki-en-jeonju.md 71줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L71) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > [Historical population]

  - 걸린 곳 2: [wiki-en-chuncheon.md 52줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L52) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > [Historical population]

  - 걸린 곳 3: [wiki-en-jeju.md 71줄](../../../data/corpus/markdown/wiki-en-jeju.md#L71) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1377658564
    > [Historical population]
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말 `1970년 인구`, `1,842,259`, `1842259`, `184만`: 프로그램이 한국어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `1970년 인구`, `1,842,259`, `1842259`, `184만`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(부산광역시)의 한국어 문서를 통째로 읽었다
부산광역시는 한국어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 table_numeric(표·수치·조건)다. 아래 뜻과 견준다.
- 표·수치·조건: 답이 표에 있거나, 문서에 값이 여러 개라 조건(연도, 기준)에 맞는 것을 골라야 한다. 문장에 수치가 하나뿐이면 아니다. 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-019
question: According to the historical population data for Busan, what was the city's
  population in 1970?
question_language: en
evidence_language: en
type: table_numeric
answer: 1,842,259
required_facts:
- fact: Busan's population in 1970 was 1,842,259.
  in_answer: true
  evidence:
  - doc_id: wiki-en-busan
    location: Demographics
    passage: '| Year | Pop. | ±% |

      | 1970 | 1,842,259 | +59.6% |

      '
opposite_check:
- 1970년 인구
- 1,842,259
- '1842259'
- 184만
same_language_check:
- '1970'
- 1,842,259
- Historical population
```

</details>

---

## c-020 · `type`(유형): table_numeric(표·수치·조건) · 도시 갈래: 영어 도시(강릉시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Based on the administrative divisions of Gangneung, what is the area of Jumunjin-eup in square kilometers?
- `answer`(정답): 60.52
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: The area of Jumunjin-eup is 60.52 km2. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-gangneung.md 78줄](../../../data/corpus/markdown/wiki-en-gangneung.md#L78) · `location`(위치): Administrative divisions
    > | Name | Korean name | Area(km2) | Population | Households |
    > | Jumunjin-eup | 주문진읍 | 60.52 | 19,299 | 9,098 |

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `60.52` · 정답과 사실에서 뽑은 숫자: `60.52`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-gangneung): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378182836 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `Jumunjin-eup`, `60.52`, `Area(km2)`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `Jumunjin-eup`, `60.52`, `Area(km2)`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말 `주문진읍`, `60.52`, `60.52km2`: 프로그램이 한국어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `주문진읍`, `60.52`, `60.52km2`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(강릉시)의 한국어 문서를 통째로 읽었다
강릉시는 한국어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 table_numeric(표·수치·조건)다. 아래 뜻과 견준다.
- 표·수치·조건: 답이 표에 있거나, 문서에 값이 여러 개라 조건(연도, 기준)에 맞는 것을 골라야 한다. 문장에 수치가 하나뿐이면 아니다. 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-020
question: Based on the administrative divisions of Gangneung, what is the area of
  Jumunjin-eup in square kilometers?
question_language: en
evidence_language: en
type: table_numeric
answer: '60.52'
required_facts:
- fact: The area of Jumunjin-eup is 60.52 km2.
  in_answer: true
  evidence:
  - doc_id: wiki-en-gangneung
    location: Administrative divisions
    passage: '| Name | Korean name | Area(km2) | Population | Households |

      | Jumunjin-eup | 주문진읍 | 60.52 | 19,299 | 9,098 |

      '
opposite_check:
- 주문진읍
- '60.52'
- 60.52km2
same_language_check:
- Jumunjin-eup
- '60.52'
- Area(km2)
```

</details>

---

## c-021 · `type`(유형): paraphrase(표현 불일치) · 도시 갈래: 영어 도시(제주시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Which major Buddhist sanctuary in Jeju features a natural water source that is purportedly therapeutic?
- `answer`(정답): Yakcheonsa
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: The Buddhist temple Yakcheonsa in Jeju has a natural mineral spring claimed to have healing powers. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-jeju.md 67줄](../../../data/corpus/markdown/wiki-en-jeju.md#L67) · `location`(위치): Tourism
    > The Buddhist temple Yakcheonsa has a natural mineral spring claimed to have healing powers, and is one of the largest temples in East Asia.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `Yakcheonsa` · 정답과 사실에서 뽑은 숫자: 없음
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-jeju): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1377658564 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `Yakcheonsa`, `natural mineral spring`, `healing powers`, `largest temples`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `Yakcheonsa`, `natural mineral spring`, `healing powers`, `largest temples`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말 `약천사`, `광천수`, `치유`, `동아시아`: 프로그램이 한국어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `약천사`, `광천수`, `치유`, `동아시아`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(제주시)의 한국어 문서를 통째로 읽었다
제주시는 한국어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 paraphrase(표현 불일치)다. 질문을 뜻이 끊기는 조각으로 나눠, 아래 짝 목록에 조각마다 한 줄씩 `질문 조각 → 근거 구절의 짝 (같은 말 / 바꾼 말 / 이름)` 꼴로 적는다(예: `처음 생긴 → 창단된 (바꾼 말)`). 이름(고유명사)은 "이름"으로 적는다. 줄이 모자라면 더한다. 목록을 다 채운 뒤 아래 접힌 칸을 펼쳐 Gemini가 적은 바꾼 말과 견준다.
- 표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).
- 짝 목록:
  - 
  - 
  - 
  - 

- 판단할 질문: "바꾼 말" 줄이 하나 이상 있는가?
- 판단할 질문: 질문에 그대로 쓴 낱말("같은 말" 줄)이 답을 드러내지 않는가? (예: "특별자치시". 드러내면 바꾼 말을 찾지 않아도 답이 나오므로 쓸 수 없다. "이름" 줄은 답을 가리키는 설명이라 빼고 본다)
- 판단할 질문: 접힌 칸의 Gemini 짝 가운데 짝 목록과 다른 것이 없는가?

<details><summary>Gemini가 적은 바꾼 말(짝 목록을 채운 뒤 펼친다)</summary>

"temple"을 "sanctuary"로, "natural mineral spring claimed to have healing powers"를 "natural water source that is purportedly therapeutic"으로 바꿈.

</details>

<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>

- "Which"(어느) → "Yakcheonsa"(약천사) · 가르기 어려움 · 핵심 낱말 아니오 · 대상을 묻는 말과 구체적인 사찰 이름은 같은 뜻이 아니다.
- "major"(주요한) → 없음 · 짝 없음 · 핵심 낱말 예 · 근거 구절에는 사찰의 규모가 크다는 설명이 있지만 중요하거나 주요하다는 뜻은 없다.
- "Buddhist"(불교의) → "Buddhist"(불교의) · 같은 말 · 핵심 낱말 예 · 근거 구절의 말을 그대로 썼다.
- "sanctuary"(성소) → "temple"(사찰) · 가르기 어려움 · 핵심 낱말 예 · 성소는 종교적으로 신성한 장소를 넓게 가리키며 사찰은 구체적인 종교 시설을 뜻한다.
- "in Jeju"(제주에 있는) → 없음 · 짝 없음 · 핵심 낱말 예 · 근거 구절에는 제주라는 위치 정보가 없다.
- "features"(갖추고 있다) → "has"(가지고 있다) · 바꾼 말 · 핵심 낱말 예 · 어떤 것을 가지고 있다는 뜻을 다른 말로 표현했다.
- "a"(하나의) → "a"(하나의) · 같은 말 · 핵심 낱말 아니오 · 근거 구절에 같은 관사가 있으며 핵심적인 사실을 나타내지 않는다.
- "natural"(천연의) → "natural"(천연의) · 같은 말 · 핵심 낱말 예 · 근거 구절의 말을 그대로 썼다.
- "water source"(수원) → "mineral spring"(광천) · 가르기 어려움 · 핵심 낱말 예 · 물이 나오는 곳이라는 뜻은 겹치지만 수원은 광물질을 함유한 샘보다 넓은 범위를 가리킨다.
- "that is purportedly therapeutic?"(치유 효과가 있다고 전해지는?) → "claimed to have healing powers"(치유 능력이 있다고 주장되는) · 바꾼 말 · 핵심 낱말 예 · 치유 효과가 있다고 주장된다는 뜻을 다른 표현과 문장 구조로 나타냈다.

</details>

- 판단할 질문: ChatGPT 목록에서 "가르기 어려움"이나 "짝 없음"인 줄마다, 그 조각의 뜻이 문서에 있는가? (근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)
- 판단할 질문: ChatGPT 목록에서 "핵심 낱말 예"인 줄에 "바꾼 말"이 하나 이상 있는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-021
question: Which major Buddhist sanctuary in Jeju features a natural water source that
  is purportedly therapeutic?
question_language: en
evidence_language: en
type: paraphrase
answer: Yakcheonsa
required_facts:
- fact: The Buddhist temple Yakcheonsa in Jeju has a natural mineral spring claimed
    to have healing powers.
  in_answer: true
  evidence:
  - doc_id: wiki-en-jeju
    location: Tourism
    passage: The Buddhist temple Yakcheonsa has a natural mineral spring claimed to
      have healing powers, and is one of the largest temples in East Asia.
opposite_check:
- 약천사
- 광천수
- 치유
- 동아시아
same_language_check:
- Yakcheonsa
- natural mineral spring
- healing powers
- largest temples
```

</details>

---

## c-022 · `type`(유형): paraphrase(표현 불일치) · 도시 갈래: 영어 도시(부산광역시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): What seasonal nickname is given to Busan due to the nationwide influx of visitors to its coastal shorelines?
- `answer`(정답): The summer capital of Korea
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Busan is called the summer capital of Korea because it attracts tourists from all over the country to its beaches. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-busan.md 211줄](../../../data/corpus/markdown/wiki-en-busan.md#L211) · `location`(위치): Parks, beaches, and highlights
    > Busan is called the summer capital of Korea, since it attracts tourists from all over the country to its six beaches.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: `The summer capital of Korea` · 정답과 사실에서 뽑은 숫자: 없음
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-busan): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1379685823 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말 `summer capital of Korea`, `tourists from all over`, `six beaches`: 근거 문서 안에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말 `summer capital of Korea`, `tourists from all over`, `six beaches`: 근거 문서가 아닌 같은 언어 문서에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다.
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말 `여름 수도`, `여름의 수도`, `여름수도`, `해변`: 프로그램이 한국어 문서 14개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다.
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `여름 수도`, `여름의 수도`, `여름수도`, `해변`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(부산광역시)의 한국어 문서를 통째로 읽었다
부산광역시는 한국어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 paraphrase(표현 불일치)다. 질문을 뜻이 끊기는 조각으로 나눠, 아래 짝 목록에 조각마다 한 줄씩 `질문 조각 → 근거 구절의 짝 (같은 말 / 바꾼 말 / 이름)` 꼴로 적는다(예: `처음 생긴 → 창단된 (바꾼 말)`). 이름(고유명사)은 "이름"으로 적는다. 줄이 모자라면 더한다. 목록을 다 채운 뒤 아래 접힌 칸을 펼쳐 Gemini가 적은 바꾼 말과 견준다.
- 표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).
- 짝 목록:
  - 
  - 
  - 
  - 

- 판단할 질문: "바꾼 말" 줄이 하나 이상 있는가?
- 판단할 질문: 질문에 그대로 쓴 낱말("같은 말" 줄)이 답을 드러내지 않는가? (예: "특별자치시". 드러내면 바꾼 말을 찾지 않아도 답이 나오므로 쓸 수 없다. "이름" 줄은 답을 가리키는 설명이라 빼고 본다)
- 판단할 질문: 접힌 칸의 Gemini 짝 가운데 짝 목록과 다른 것이 없는가?

<details><summary>Gemini가 적은 바꾼 말(짝 목록을 채운 뒤 펼친다)</summary>

"summer capital of Korea"를 "seasonal nickname"으로, "tourists from all over the country to its six beaches"를 "nationwide influx of visitors to its coastal shorelines"로 바꿈.

</details>

<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>

- "What"(무슨) → "the summer capital of Korea"(한국의 여름 수도) · 가르기 어려움 · 핵심 낱말 아니오 · 별명의 내용을 묻는 말과 근거 구절에 나온 구체적인 별명은 같은 뜻이 아니다.
- "seasonal"(계절과 관련된) → "summer"(여름) · 가르기 어려움 · 핵심 낱말 예 · 계절과 관련된다는 뜻은 겹치지만 근거 구절은 여름이라는 특정 계절을 나타낸다.
- "nickname"(별명) → "is called"(~라고 불린다) · 바꾼 말 · 핵심 낱말 예 · 특정한 이름으로 불린다는 내용을 별명이라는 말로 나타냈다.
- "is given to"(~에 붙여지는) → "is called"(~라고 불린다) · 바꾼 말 · 핵심 낱말 아니오 · 이름이 붙는다는 뜻을 불린다는 말로 다르게 표현한 것으로 별명을 묻는 틀의 일부다.
- "Busan"(부산) → "Busan"(부산) · 이름 · 핵심 낱말 아니오 · 지명의 고유명사다.
- "due to"(~때문에) → "since"(~때문에) · 바꾼 말 · 핵심 낱말 아니오 · 원인과 이유를 나타내는 같은 뜻을 다른 말로 표현했다.
- "the"(그) → "the"(그) · 같은 말 · 핵심 낱말 아니오 · 근거 구절에도 같은 관사가 쓰였으며 핵심적인 사실을 나타내지 않는다.
- "nationwide"(전국적인) → "from all over the country"(전국 각지에서) · 바꾼 말 · 핵심 낱말 예 · 전국이라는 범위를 여러 지역에서 온다는 말로 풀어 표현했다.
- "influx of visitors"(방문객들이 대거 몰려드는 것) → "attracts tourists"(관광객을 끌어들인다) · 가르기 어려움 · 핵심 낱말 예 · 사람들이 방문한다는 뜻은 겹치지만 대규모 유입이라는 뜻은 근거 구절에 없으며 방문객은 관광객보다 넓은 범위다.
- "to its coastal shorelines?"(그 도시의 해안선으로?) → "to its six beaches"(그 도시의 여섯 해변으로) · 가르기 어려움 · 핵심 낱말 예 · 바닷가라는 공간은 겹치지만 해안선은 해변보다 넓은 범위이고 근거 구절에는 여섯 곳이라는 구체적인 수가 더 들어 있다.

</details>

- 판단할 질문: ChatGPT 목록에서 "가르기 어려움"이나 "짝 없음"인 줄마다, 그 조각의 뜻이 문서에 있는가? (근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)
- 판단할 질문: ChatGPT 목록에서 "핵심 낱말 예"인 줄에 "바꾼 말"이 하나 이상 있는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-022
question: What seasonal nickname is given to Busan due to the nationwide influx of
  visitors to its coastal shorelines?
question_language: en
evidence_language: en
type: paraphrase
answer: The summer capital of Korea
required_facts:
- fact: Busan is called the summer capital of Korea because it attracts tourists from
    all over the country to its beaches.
  in_answer: true
  evidence:
  - doc_id: wiki-en-busan
    location: Parks, beaches, and highlights
    passage: Busan is called the summer capital of Korea, since it attracts tourists
      from all over the country to its six beaches.
opposite_check:
- 여름 수도
- 여름의 수도
- 여름수도
- 해변
same_language_check:
- summer capital of Korea
- tourists from all over
- six beaches
```

</details>

---

## c-023 · `type`(유형): multi_doc(여러 문서 연결) · 도시 갈래: 영어 도시(부산광역시, 제주시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Comparing the climate records of Busan and Jeju City, which city has the higher all-time record high temperature, and what was that temperature in Celsius?
- `answer`(정답): Busan has the higher record, at 38.8 °C.
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Busan's highest temperature ever recorded is 38.8 °C. · 답을 내는 데만 쓰임(`in_answer: false`)
  - `fact`(사실) 2: Jeju City's highest temperature ever recorded is 37.5 °C. · 답을 내는 데만 쓰임(`in_answer: false`)
  - `fact`(사실) 3: Busan's highest temperature (38.8 °C) is higher than Jeju City's highest temperature (37.5 °C). · 정답에 들어감(`in_answer: true`) (근거 없음 — 다른 사실들에서 나오는 결론이라 문서에 이 문장이 없다. 채점 때 답에 이 결론이 들어 있는지 본다)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-busan.md 82줄](../../../data/corpus/markdown/wiki-en-busan.md#L82) · `location`(위치): Climate
    > The highest temperature ever recorded is 38.8 °C (101.8 °F) on 29 July 2026, while the lowest temperature ever recorded is −14.0 °C (6.8 °F) on 13 January 1915.
  - 사실 2의 근거 1: [wiki-en-jeju.md 86줄](../../../data/corpus/markdown/wiki-en-jeju.md#L86) · `location`(위치): Climate
    > The highest temperature ever recorded is 37.5 °C (99.5 °F) on 25 July 1942 while the lowest temperature ever recorded is −6.0 °C (21.2 °F) on 16 February 1977.

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: 위 `answer`(정답)에서 값마다 골라 찾는다 · 정답과 사실에서 뽑은 숫자: `38.8`, `37.5`
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-busan): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1379685823 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 할 일 2 (wiki-en-jeju): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1377658564 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서 안의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `38.8 °C`, `37.5 °C`: 근거 문서 안에서는 걸린 곳이 없다.
- `term`(찾을 말) `Record high`:
  - 걸린 곳 1: [wiki-en-busan.md 90줄](../../../data/corpus/markdown/wiki-en-busan.md#L90) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379685823
    > | [Record high] °C (°F) | 18.4 (65.1) | 20.3 (68.5) | 22.9 (73.2) | 28.1 (8…

  - 걸린 곳 2: [wiki-en-jeju.md 92줄](../../../data/corpus/markdown/wiki-en-jeju.md#L92) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1377658564
    > | [Record high] °C (°F) | 23.6 (74.5) | 24.5 (76.1) | 28.8 (83.8) | 30.9 (8…

  - 걸린 곳 3: [wiki-en-jeju.md 110줄](../../../data/corpus/markdown/wiki-en-jeju.md#L110) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1377658564
    > | [Record high] °C (°F) | 18.8 (65.8) | 20.1 (68.2) | 21.4 (70.5) | 27.3 (8…
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서가 아닌 같은 언어 문서의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `38.8 °C`, `37.5 °C`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다.
- `term`(찾을 말) `Record high`:
  - 걸린 곳 1: [wiki-en-jeonju.md 55줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L55) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > | [Record high] °C (°F) | 18.3 (64.9) | 22.9 (73.2) | 29.6 (85.3) | 31.2 (8…

  - 걸린 곳 2: [wiki-en-cheongju.md 60줄](../../../data/corpus/markdown/wiki-en-cheongju.md#L60) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953230
    > | [Record high] °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 28.2 (82.8) | 31.3 (8…

  - 걸린 곳 3: [wiki-en-chuncheon.md 184줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L184) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > | [Record high] °C (°F) | 12.7 (54.9) | 19.9 (67.8) | 23.5 (74.3) | 32.0 (8…

  - 걸린 곳 4: [wiki-en-cheonan.md 54줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L54) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953224
    > | [Record high] °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.9 (80.4) | 31.2 (8…

  - 걸린 곳 5: [wiki-en-andong.md 198줄](../../../data/corpus/markdown/wiki-en-andong.md#L198) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378924154
    > | [Record high] °C (°F) | 13.2 (55.8) | 23.2 (73.8) | 26.6 (79.9) | 32.1 (8…

  - 걸린 곳 6: [wiki-en-gangneung.md 60줄](../../../data/corpus/markdown/wiki-en-gangneung.md#L60) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378182836
    > | [Record high] °C (°F) | 18.7 (65.7) | 21.4 (70.5) | 27.1 (80.8) | 33.6 (9…
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말과, 프로그램이 한국어 문서 14개에서 찾은 걸린 곳 전부다. 찾을 말 `38.8도`: 걸린 곳이 없다.
- `term`(찾을 말) `38.8`:
  - 걸린 곳 1: [wiki-ko-cheongju.md 95줄](../../../data/corpus/markdown/wiki-ko-cheongju.md#L95) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42630014
    > | 평균 월간 일조시간 | 166.9 | 176.9 | 207.6 | 220.0 | 2[38.8] | 196.5 | 150.1 | 173.1 | 176.4 | 204.1 | 160.6 | 161.0 | 2…

- `term`(찾을 말) `37.5`:
  - 걸린 곳 1: [wiki-ko-suwon.md 83줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L83) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42534963
    > …) | 25.0 (77.0) | 30.5 (86.9) | 33.2 (91.8) | 35.1 (95.2) | [37.5] (99.5) | 39.3 (102.7) | 34.0 (93.2) | 29.0 (84.2) | 25.8 (7…

- `term`(찾을 말) `역대 최고 기온`:
  - 걸린 곳 1: [wiki-ko-jeonju.md 100줄](../../../data/corpus/markdown/wiki-ko-jeonju.md#L100) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42643645
    > | [역대 최고 기온] °C (°F) | 18.3 (64.9) | 22.9 (73.2) | 29.6 (85.3) | 31.2 (8…

  - 걸린 곳 2: [wiki-ko-cheongju.md 86줄](../../../data/corpus/markdown/wiki-ko-cheongju.md#L86) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42630014
    > | [역대 최고 기온] °C (°F) | 15.6 (60.1) | 22.1 (71.8) | 25.9 (78.6) | 31.3 (8…

  - 걸린 곳 3: [wiki-ko-chuncheon.md 72줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L72) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42647646
    > | [역대 최고 기온] °C (°F) | 12.7 (54.9) | 19.9 (67.8) | 24.9 (76.8) | 32.0 (8…

  - 걸린 곳 4: [wiki-ko-cheonan.md 61줄](../../../data/corpus/markdown/wiki-ko-cheonan.md#L61) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42545685
    > | [역대 최고 기온] °C (°F) | 16.5 (61.7) | 22.2 (72.0) | 26.7 (80.1) | 31.2 (8…

  - 걸린 곳 5: [wiki-ko-suwon.md 83줄](../../../data/corpus/markdown/wiki-ko-suwon.md#L83) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42534963
    > | [역대 최고 기온] °C (°F) | 15.3 (59.5) | 19.3 (66.7) | 25.0 (77.0) | 30.5 (8…

  - 걸린 곳 6: [wiki-ko-gwangju.md 58줄](../../../data/corpus/markdown/wiki-ko-gwangju.md#L58) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42623705
    > | [역대 최고 기온] °C (°F) | 18.8 (65.8) | 22.6 (72.7) | 26.8 (80.2) | 30.4 (8…
- 할 일: 걸린 문장을 하나씩 읽는다.
- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `38.8`, `37.5`, `역대 최고 기온`, `38.8도`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(부산광역시, 제주시)의 한국어 문서를 통째로 읽었다
부산광역시, 제주시는 한국어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 multi_doc(여러 문서 연결)다. 아래 뜻과 견준다.
- 여러 문서 연결: 둘 이상의 문서나 구절을 합쳐야 답이 나온다(비교, 집계, 여러 단계). 표의 값이나 수치를 비교하는 질문도 여기다. 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-023
question: Comparing the climate records of Busan and Jeju City, which city has the
  higher all-time record high temperature, and what was that temperature in Celsius?
question_language: en
evidence_language: en
type: multi_doc
answer: Busan has the higher record, at 38.8 °C.
required_facts:
- fact: Busan's highest temperature ever recorded is 38.8 °C.
  in_answer: false
  evidence:
  - doc_id: wiki-en-busan
    location: Climate
    passage: The highest temperature ever recorded is 38.8 °C (101.8 °F) on 29 July
      2026, while the lowest temperature ever recorded is −14.0 °C (6.8 °F) on 13
      January 1915.
- fact: Jeju City's highest temperature ever recorded is 37.5 °C.
  in_answer: false
  evidence:
  - doc_id: wiki-en-jeju
    location: Climate
    passage: The highest temperature ever recorded is 37.5 °C (99.5 °F) on 25 July
      1942 while the lowest temperature ever recorded is −6.0 °C (21.2 °F) on 16 February
      1977.
- fact: Busan's highest temperature (38.8 °C) is higher than Jeju City's highest temperature
    (37.5 °C).
  in_answer: true
  evidence: []
opposite_check:
- '38.8'
- '37.5'
- 역대 최고 기온
- 38.8도
same_language_check:
- 38.8 °C
- 37.5 °C
- Record high
```

</details>

---

## c-024 · `type`(유형): multi_doc(여러 문서 연결) · 도시 갈래: 영어 도시(안동시, 강릉시)

이 카드만 보고 위에서부터 차례로 한다. 칸마다 "할 일"을 하고 "판단할 질문"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. 문제가 있으면 `[ ]`로 두고 맨 아래 "이유"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 "메모"에 적는다.

**후보**
- `question`(질문): Name the sister cities of Andong and Gangneung that are located in China.
- `answer`(정답): Andong's sister cities in China are Pingdingshan and Xi'an. Gangneung's sister city in China is Mangshi (in Yunnan).
- `required_facts`(꼭 필요한 사실):
  - `fact`(사실) 1: Andong has a sister city relationship with Pingdingshan and Xi'an in China. · 정답에 들어감(`in_answer: true`)
  - `fact`(사실) 2: Gangneung's sister city in China is Mangshi, Yunnan. · 정답에 들어감(`in_answer: true`)
- `passage`(근거 구절):
  - 사실 1의 근거 1: [wiki-en-andong.md 218줄](../../../data/corpus/markdown/wiki-en-andong.md#L218) · `location`(위치): Sister cities
    > - Pingdingshan, China
  - 사실 1의 근거 2: [wiki-en-andong.md 220줄](../../../data/corpus/markdown/wiki-en-andong.md#L220) · `location`(위치): Sister cities
    > - Xi'an, China
  - 사실 2의 근거 1: [wiki-en-gangneung.md 209줄](../../../data/corpus/markdown/wiki-en-gangneung.md#L209) · `location`(위치): Sister cities
    > - Mangshi, Yunnan, China, since November 21, 2012

**영어 읽는 법** — 영어로 적힌 칸: `question`(질문), `answer`(정답), `fact`(사실), `passage`(근거 구절). 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 1~8을 판단한다. 옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. 이 낱말들은 이 카드에서 `Cmd+F`로 찾는다. 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).

#### 1. 근거 구절만 읽고 정답이 나온다
- 할 일: 위 `passage`(근거 구절)를 읽는다.
- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?
- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 "5개 자치구 중"이면 근거 문서에 자치구가 5개인지 본다.
- [ ] 확인함

#### 2. 정답이 하나로 정해진다
- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.
- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?
- [ ] 확인함

#### 3. 같은 문서 안에 다른 값이 없다
- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. 정답의 값: 위 `answer`(정답)에서 값마다 골라 찾는다 · 정답과 사실에서 뽑은 숫자: 없음
- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다.
- 할 일 1 (wiki-en-andong): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378924154 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 할 일 2 (wiki-en-gangneung): 크롬에서 https://en.wikipedia.org/w/index.php?oldid=1378182836 를 연다. 페이지에서 오른쪽 클릭 → "한국어로 번역". `Cmd+F`로 위 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서 안의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `Mangshi`, `Pingdingshan`, `Xi'an`, `Yunnan`: 근거 문서 안에서는 걸린 곳이 없다.
- `term`(찾을 말) `Sister cities`:
  - 걸린 곳 1: [wiki-en-andong.md 212줄](../../../data/corpus/markdown/wiki-en-andong.md#L212) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378924154
    > ## [Sister cities]

  - 걸린 곳 2: [wiki-en-gangneung.md 205줄](../../../data/corpus/markdown/wiki-en-gangneung.md#L205) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378182836
    > ## [Sister cities]
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 4. 같은 언어(영어)의 다른 문서에 다른 값이 없다
- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 "포함할 파일"에 `data/corpus/markdown/*-en-*`를 적는다. 3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. 걸린 줄은 번역기에 붙여 읽는다.
- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?
- Gemini가 고른 찾을 말과, 프로그램이 영어 문서에서 찾은 근거 문서가 아닌 같은 언어 문서의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다. 찾을 말 `Mangshi`, `Pingdingshan`, `Xi'an`, `Yunnan`: 근거 문서가 아닌 같은 언어 문서에서는 걸린 곳이 없다.
- `term`(찾을 말) `Sister cities`:
  - 걸린 곳 1: [wiki-en-jeonju.md 213줄](../../../data/corpus/markdown/wiki-en-jeonju.md#L213) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379135207
    > ## [Sister cities]

  - 걸린 곳 2: [wiki-en-cheongju.md 144줄](../../../data/corpus/markdown/wiki-en-cheongju.md#L144) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953230
    > ## Twin towns – [sister cities]

  - 걸린 곳 3: [wiki-en-chuncheon.md 213줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L213) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > ## [Sister cities]

  - 걸린 곳 4: [wiki-en-chuncheon.md 236줄](../../../data/corpus/markdown/wiki-en-chuncheon.md#L236) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1376994978
    > In March 2005, Chuncheon sent letters of protest to its [sister cities] in Japan (Kakamigahara, Higashichikuma, and Hofu) and indef…

  - 걸린 곳 5: [wiki-en-cheonan.md 210줄](../../../data/corpus/markdown/wiki-en-cheonan.md#L210) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1378953224
    > ## Twin towns – [sister cities]

  - 걸린 곳 6: [wiki-en-busan.md 78줄](../../../data/corpus/markdown/wiki-en-busan.md#L78) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379685823
    > …roughly 180 km (112 miles) away. Busan and Fukuoka are also [sister cities].

  - 걸린 곳 7: [wiki-en-busan.md 512줄](../../../data/corpus/markdown/wiki-en-busan.md#L512) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1379685823
    > ### [Sister cities]

  - 걸린 곳 8: [wiki-en-jeju.md 184줄](../../../data/corpus/markdown/wiki-en-jeju.md#L184) · 원문 주소(앞뒤 문맥을 볼 때): https://en.wikipedia.org/w/index.php?oldid=1377658564
    > ## Twin towns – [sister cities]
- 할 일: 걸린 곳의 인용 글을 하나씩 번역기에 붙여 읽는다.
- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?
- [ ] 확인함

#### 5. 한국어 문서: 프로그램이 찾은 걸린 곳을 읽었다
Gemini가 고른 찾을 말과, 프로그램이 한국어 문서 14개에서 찾은 걸린 곳 전부다. 찾을 말 `망시`, `윈난성`, `핑딩산`, `중국 자매도시`: 걸린 곳이 없다.
- `term`(찾을 말) `시안`:
  - 걸린 곳 1: [wiki-ko-chuncheon.md 336줄](../../../data/corpus/markdown/wiki-ko-chuncheon.md#L336) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42647646
    > - 엘리[시안] 강촌

  - 걸린 곳 2: [wiki-ko-gyeongju.md 517줄](../../../data/corpus/markdown/wiki-ko-gyeongju.md#L517) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42639825
    > | 산시성 (섬서성) [시안]시 | 중화인민공화국 | 1994년 11월 18일 |

  - 걸린 곳 3: [wiki-ko-sejong.md 443줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L443) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42585449
    > ### 충청남도 세종[시안]과 정부 직할 세종특별자치시안 대립

  - 걸린 곳 4: [wiki-ko-sejong.md 443줄](../../../data/corpus/markdown/wiki-ko-sejong.md#L443) · 원문 주소(앞뒤 문맥을 볼 때): https://ko.wikipedia.org/w/index.php?oldid=42585449
    > ### 충청남도 세종시안과 정부 직할 세종특별자치[시안] 대립
- 할 일: 걸린 문장을 하나씩 읽는다.
- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?
- [ ] 확인함

#### 6. 한국어 문서: 다른 말로도 찾아봤다
- Gemini가 고른 찾을 말: `망시`, `윈난성`, `핑딩산`, `시안`, `중국 자매도시`
- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 한국어 문서가 다른 말로 적었을 것 같으면, 더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. "포함할 파일"은 `data/corpus/markdown/*-ko-*`. 걸린 곳이 있으면 그 줄을 읽는다.
- 판단할 질문: 한국어 문서 어디에도 같은 사실이 다른 표현으로 없는가?
- 더 찾아본 말과 걸린 곳:
- [ ] 확인함

#### 7. 한국어 문서: 같은 도시(안동시, 강릉시)의 한국어 문서를 통째로 읽었다
안동시, 강릉시는 한국어 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다.
- [ ] 확인함

#### 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다
- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.
- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?
- 판단할 질문: 질문이 묻는 사실만 "정답에 들어감"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 "답을 내는 데만 쓰임"인가? `answer`(정답)에 "정답에 들어감"인 사실이 모두 들어 있는가?
- [ ] 확인함

#### 9. 유형이 맞다
- 할 일: 이 후보의 유형은 multi_doc(여러 문서 연결)다. 아래 뜻과 견준다.
- 여러 문서 연결: 둘 이상의 문서나 구절을 합쳐야 답이 나온다(비교, 집계, 여러 단계). 표의 값이나 수치를 비교하는 질문도 여기다. 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.
- 판단할 질문: 이 후보가 이 뜻에 맞는가?
- [ ] 확인함

#### 적기
- 판정(하나만 남긴다): 채택 / 수정 / 폐기
- 이유(한 줄. 문제가 없으면 "1~9 문제 없음"):
- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):

<details><summary>참고용 원본 YAML</summary>

```yaml
id: c-024
question: Name the sister cities of Andong and Gangneung that are located in China.
question_language: en
evidence_language: en
type: multi_doc
answer: Andong's sister cities in China are Pingdingshan and Xi'an. Gangneung's sister
  city in China is Mangshi (in Yunnan).
required_facts:
- fact: Andong has a sister city relationship with Pingdingshan and Xi'an in China.
  in_answer: true
  evidence:
  - doc_id: wiki-en-andong
    location: Sister cities
    passage: '- Pingdingshan, China'
  - doc_id: wiki-en-andong
    location: Sister cities
    passage: '- Xi''an, China'
- fact: Gangneung's sister city in China is Mangshi, Yunnan.
  in_answer: true
  evidence:
  - doc_id: wiki-en-gangneung
    location: Sister cities
    passage: '- Mangshi, Yunnan, China, since November 21, 2012'
opposite_check:
- 망시
- 윈난성
- 핑딩산
- 시안
- 중국 자매도시
same_language_check:
- Mangshi
- Pingdingshan
- Xi'an
- Yunnan
- Sister cities
```

</details>
