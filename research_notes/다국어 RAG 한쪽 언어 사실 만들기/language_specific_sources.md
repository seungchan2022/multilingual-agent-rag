# 원래부터 한 언어에만 있는 내용으로 "한쪽 언어 문서에만 답이 있는 질문"을 만드는 다국어·교차 언어 QA/RAG 벤치마크

조사일: 2026-10-21.

이 노트는 앞 조사 `research_notes/다국어 RAG 교차 언어 평가 설계/benchmark_construction.md`가 다룬 것을 되풀이하지 않는다. 앞 조사가 다룬 것은 XOR-TyDi QA·MKQA 등이 문서 풀 구성으로 교차 언어 조건을 만드는 방식과, BordIRlines의 관점 비대칭 개념이다. 앞 조사의 3절 Gaps에는 "Wikipedia 언어판 사이에서 한 언어판에만 있는 사실을 직접 찾아내 질문으로 만든 벤치마크는 찾지 못했다"가 있었다. 이번 조사는 그 빈 곳을 채운다.

표기 규칙은 다음과 같다.

- **[원문 확인]**: arXiv 또는 ACL Anthology에서 논문 PDF를 내려받아 본문에서 직접 확인했다. "PDF p.N"은 PDF 파일의 쪽 순서다. 논문에 인쇄된 쪽 번호와 다를 수 있다. 인용은 원문 그대로다. 인용 앞의 한국어 문장이 그 인용의 뜻이다.
- **[그림 판독]**: 원형 그래프 같은 그림을 이미지로 렌더링해서 라벨에 적힌 숫자를 읽었다.
- **[데이터 확인]**: 공개 데이터 파일을 내려받아 직접 셌다. 주소를 함께 적었다.
- **[직접 확인]**: 위키백과 API로 내가 따로 확인했다(2026-10-21). 논문이 한 일이 아니다. 방법과 한계를 함께 적었다.
- **[원문 내 불일치]**: 같은 논문 안에서 숫자나 규칙이 서로 맞지 않는다. 한쪽을 고르지 않고 둘 다 적었다.
- **[미확인]**: 확인하지 못했다.
- **[2차 출처만]**: 검색 결과 요약에서만 봤고 원문은 확인하지 않았다.
- 연도는 arXiv 번호 앞 네 자리(첫 제출 연월)를 따랐다. 학회 이름은 PDF 머리글이나 ACL Anthology 주소에서 본 것만 적었다.
- 후보를 찾을 때는 웹 검색을 썼다. 아래의 방법과 숫자는 모두 원문 PDF나 공개 데이터에서 다시 확인한 것이다.

---

## 1. 한 언어에만 있는 지식을 일부러 쓰는 벤치마크는 어느 것인가

### Takeaway

"다른 언어판에 같은 글이 없다"를 질문 선정 조건으로 직접 쓴 벤치마크는 ECLeKTic(2025)과 KoLasSimpleQA(2025) 두 개다. 둘 다 한국어를 포함한다. 둘 다 위키백과 글이 있는지만 보고, 답이 되는 사실이 다른 언어의 다른 글에 있는지는 보지 않는다. MultiLoKo(2025)는 그 언어권에서 조회수가 높은 글 가운데 지역 주제를 사람이 점수로 골랐다. 그래서 한국어 원천 글의 대부분은 영어판도 있다. 한국 시험이나 한국 자료를 원천으로 삼은 벤치마크(KMMLU, CLIcK, HAE-RAE, KoSimpleQA, INCLUDE의 한국어 부분)와 BertaQA, CaLMQA는 "지역 지식"을 얻는다. 다만 다른 언어에 없는지는 확인하지 않는다. BLEnD, XLQA, XNationQA, Global-MMLU, BordIRlines, TriviaRoomQA는 같은 질문을 여러 언어에 두거나 번역에서 출발한다. 그래서 "한쪽 언어에만 있는 사실" 조건에 맞지 않는다.

### Cited Findings

#### 1-A. 요약표

판정 열의 뜻은 다음과 같다. "맞음"은 다른 언어판에 같은 글이 없는 것을 선정 조건으로 썼다는 뜻이다. 확인 단위는 글이다. "부분"은 지역 지식을 원천에서 얻지만 다른 언어에 없는지는 확인하지 않았다는 뜻이다. "안 맞음"은 같은 질문을 여러 언어에 두거나 번역에서 출발한다는 뜻이다. 각 칸의 근거는 1-B와 2절, 3절에 원문 인용으로 적었다.

| 벤치마크(연도) | 원천 | 한쪽 언어 내용을 고르는 방법 | 다른 언어에 없음을 확인하는 방법 | 규모 | 언어(한국어) | 주제와 STEM | 판정 |
|---|---|---|---|---|---|---|---|
| [ECLeKTic](https://arxiv.org/abs/2502.21228) (2025, Google) | 12개 언어 위키백과 2023년 7월 덤프 | 다른 11개 언어에 같은 글이 없는 글을 언어마다 100개씩 뽑음(200자 이상, 2023년 조회 100회 이상). 주석자가 일반 과학·상식 주제를 뺌 | 글 단위만 봄. 같은 글인지 무엇으로 판정했는지(언어 간 링크인지 등)는 논문에 없음. 사실 단위 확인은 없음 | 원천 질문 384개, 번역을 합쳐 4,608개 | 12개 언어, 한국어 포함(한국어 원천 질문 33개) | 전체의 Science and Technology 7.7%, 한국어 원천 질문에서는 3.0% | 맞음(글 단위) |
| [KoLasSimpleQA](https://arxiv.org/abs/2505.16591) (2025) | 9개 언어 위키백과 전체 | 언어 간 링크 수(n_ill)가 0인 글을 무작위로 400개 뽑아 "language-specific"으로 씀 | 글 단위만 봄. 언어 간 링크가 0개이므로 어느 언어판에도 같은 글이 없음. 사실 단위 확인은 없음 | 2,147개(일반 1,306개, 언어 고유 841개) | 9개 언어, 한국어 포함(일반 151개, 언어 고유 84개) | 주제 분포 보고를 찾지 못함 | 맞음(글 단위). 데이터 공개 주소가 404 |
| [MultiLoKo](https://arxiv.org/abs/2504.10356) (2025, Meta) | 언어별 조회수 상위 6천 개 위키백과 글(2016–2021) | 문단의 지역성을 사람이 1–5점으로 매겨 지역 주제만 남김. 이 규칙의 방향이 본문과 부록에서 반대 | 없음. [직접 확인] 한국어 dev 질문 250개의 원천 글 가운데 192개는 영어판이 있음 | 언어당 500개(dev 250개 공개, test 250개 비공개) | 31개 언어, 한국어 포함 | 주제 분포 보고를 찾지 못함 | 부분 |
| [KMMLU](https://arxiv.org/abs/2402.11548) (2024) | 한국 시험(PSAT, 국가자격시험, 수능 등 533개 출처) | 번역 없이 한국 시험에서 모음. 한국 지식이 필요한 문항 비율은 사후에 표본으로 잼(20.4%) | 없음 | 35,030개 | 한국어만 | 45개 과목, STEM 포함. 대부분은 보편 지식 | 부분 |
| [CLIcK](https://arxiv.org/abs/2403.06412) (2024) | 한국 시험 6종, KIIP 교재(GPT-4로 생성) | 검증 기준 가운데 하나가 "Questions should centrally relate to Korea" | 없음 | 1,995개 | 한국어만 | 문화 8개, 언어 3개 범주. STEM 범주 없음 | 부분 |
| [HAE-RAE Bench](https://arxiv.org/abs/2309.02706) (2023) | 국립국어원 자료, TV 「우리말 겨루기」, 나무위키 '한국사' 문서, KLAT | 한국 고유 어휘·역사·상식·독해 과제로 설계 | 없음 | 1,538개 | 한국어만 | STEM 과제 없음 | 부분 |
| [KoSimpleQA](https://arxiv.org/abs/2510.18368) (2025) | 크라우드 작업자가 직접 씀(근거 링크 최대 4개) | "Korean cultural contexts"에 근거한 질문을 쓰게 함 | 없음 | 938개(v2) | 한국어만(영어 번역본 포함) | Science & Technology가 19.2%로 가장 많음 | 부분 |
| [INCLUDE](https://arxiv.org/abs/2411.19799) (2024) | 52개국 현지 시험 1,926개 | 현지 시험 원문을 그대로 씀. 시험 단위로 지역성 표시(region-agnostic, region-explicit, cultural, region-implicit) | 없음 | 197,243개 | 44개 언어, 한국어 1,781개 | region-agnostic 34.4%(수학·물리가 예시) | 부분 |
| [BertaQA](https://arxiv.org/abs/2406.07302) (2024) | 바스크어 퀴즈(공개 출처를 크롤링했고 지금은 없음) | 원천에 이미 local/global 표시가 있었음 | 질문 일부를 따옴표로 묶어 구글에서 검색했고 결과가 없었음. 질문 문장이 웹에 있는지만 본 것이고 답이 있는지는 아님 | 4,756개 | 바스크어·영어(한국어 없음) | 8개 범주에 Science and Technology 포함(local 292개) | 부분(한국어 없음) |
| [CaLMQA](https://arxiv.org/abs/2406.17761) (2024) | 각국 Q&A 게시판(한국어는 네이버 지식iN) | 한 문화나 몇몇 문화에만 있는 개념을 묻거나, 지역마다 답이 다른 질문만 모음 | 없음(GPT-4o-mini로 문화 특수성 판정) | 51.7K개 | 23개 언어, 한국어 5,875개 | Technology, Health 범주 포함 | 부분(근거 문서 없음, 장문 답) |
| [BLEnD](https://arxiv.org/abs/2406.09948) (2024) | 원어민이 만든 질문 템플릿 500개와 원어민 답 | 한 나라에만 해당하는 문항은 오히려 뺌 | 해당 없음 | 52.6k개 | 13개 언어, 16개 나라·지역, 한국어(남한·북한) | 일상 6개 범주, STEM 없음 | 안 맞음 |
| [BordIRlines](https://arxiv.org/abs/2410.01171) (2024) | 영토 분쟁 지역과 당사국에 관한 위키백과 글 | 같은 영토를 언어마다 다르게 쓰는 점을 이용 | 해당 없음 | 질의 720개, 질의-문서 쌍 19,916개 | 49개 언어, 한국어 영토 7개 | 영토 분쟁만 | 안 맞음 |
| [XLQA](https://arxiv.org/abs/2508.16139) (2025) | 영어 기존 QA(MKQA, MLQA, HotpotQA)를 번역 | 지역마다 답이 달라지는지를 LLM과 웹 검색으로 찾고 사람이 확인 | 해당 없음 | 질문 3,000개 × 8개 언어 | 8개 언어, 한국어 포함 | 주제 표시 없음 | 안 맞음(번역에서 출발) |
| [XNationQA](https://aclanthology.org/2025.emnlp-main.756/) (2025, EMNLP) | 영어 위키백과 목록과 위키데이터 | 9개 나라의 고유 사실(전쟁, 국립공원, 지도자, 유네스코 유산) | 해당 없음 | 49,280개 | 7개 언어, 한국어 없음 | STEM 없음 | 안 맞음(번역, 한국어 없음) |
| [Global-MMLU](https://arxiv.org/abs/2412.03304) (2024) | 영어 MMLU 번역 | MMLU 문항에 문화 민감(CS)/문화 무관(CA) 표시 | 해당 없음 | 표시한 문항 2,850개 | 42개 언어, 한국어 포함 | STEM 문항 950개 중 30개만 CS | 안 맞음(번역). STEM 근거로만 씀 |
| [Sweden-related factual knowledge](https://arxiv.org/abs/2510.21360) (2025) | 라디오 프로그램 출연자, 스포츠 대회 | 국제 보도가 적은 스웨덴 인물·사건을 사람이 직접 씀 | 확인 절차를 찾지 못함(초록과 2절 일부만 읽음) | 1,293개 | 스웨덴어·영어(한국어 없음) | 문화·미디어·스포츠 | 부분(한국어 없음) |
| [TriviaRoomQA](https://arxiv.org/abs/2607.21445) (2026) | 퀴즈 문제 | 여러 언어 병렬 질문 | 해당 없음(초록만 확인) | 병렬 3,300개, 프랑스어만 5,340개 | 유럽 6개 언어(한국어 없음) | 288개 주제 | 안 맞음 |
| XOR-TyDi QA (2021) | 앞 조사 1절이 다룸 | TyDi QA에서 "답 없음"인 질문을 가져옴 | 앞 조사에 따르면 "답 없음"은 Google 검색 1위 글 하나에서 답 문단을 찾지 못했다는 뜻 | 앞 조사 참조 | 앞 조사 참조 | 앞 조사 참조 | 안 맞음(질문을 먼저 정하고 답을 찾는 방식. "답 없음"은 검색 1위 글 하나에 답이 없다는 뜻이고 사실이 없음을 확인한 것이 아님. 한국어 질문·영어 근거라는 방향은 과제의 두 방향 중 하나와 같음) |
| [InfoGap](https://arxiv.org/abs/2410.04282) (2024) / [WikiGap](https://arxiv.org/abs/2505.24195) (2025) | 같은 주제의 두 언어 위키백과 글 | 벤치마크가 아니다. 두 글을 사실 단위로 비교해 한쪽에만 있는 사실을 찾는 방법이다 | 사실 단위(GPT-4 분해, LaBSE 정렬, GPT-4 함의 판정) | 전기 2.7K개(InfoGap) | 영어·러시아어·프랑스어, WikiGap은 중국어 추가(한국어 없음) | 전기(InfoGap), 음식 등(WikiGap 예) | 방법으로만 참고 |

#### 1-B. 벤치마크별 판정 근거

**맞음: 다른 언어판에 같은 글이 없는 것을 선정 조건으로 씀**

- [원문 확인] ECLeKTic은 12개 언어 가운데 한 언어에만 있는 위키백과 글을 골라 질문의 바탕으로 삼았다. §2, PDF p.3: "As a basis for such question/answer pairs, we selected articles in Wikipedia that only exist in one of the 12 target languages, and not in any of the others (English, French, German, Hebrew, Hindi, Indonesian, Italian, Japanese, Korean, Mandarin Chinese, Portuguese, and Spanish)." — [Goldman et al., 2025 (ECLeKTic)](https://arxiv.org/abs/2502.21228)
- [원문 확인] ECLeKTic은 독일어판에만 있는 성우 Tobias Meister 글을 대표 예로 든다. 최종 결과를 "주로 한 언어에서만 알려진 사실"로 설명한다. §1, PDF p.2: "We identified those facts using Wikipedia articles in 12 languages that lack equivalents in the other 11, such as the article on the aforementioned Tobias Meister, that exists only on the German Wikipedia." 같은 쪽: "The result is a set of 4,224 question/answer pairs, each addressing a fact primarily known in one language (henceforth, the source language)". — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] KoLasSimpleQA는 언어 간 링크가 하나도 없는 글을 그 언어 고유 지식으로 분류한다. §2.2.1, PDF p.3: "Thus, if an entity lacks versions in other languages (n_ill = 0), it is classified as language-specific, indicating the knowledge is unique to that language. Conversely, if an entity appears in many language versions (n_ill is large), it likely represents global knowledge, making it general." — [Jiang et al., 2025 (KoLasSimpleQA)](https://arxiv.org/abs/2505.16591)

**부분: 지역 지식을 원천에서 얻지만 다른 언어에 없는지는 확인하지 않음**

- [원문 확인] MultiLoKo는 언어마다 따로 모은 지역 관련 질문 500개를 본체로 삼는다. Abstract, PDF p.1: "a main partition consisting of 500 questions per language, separately sourced to be locally relevant to the specific language". 다른 언어판과 비교하는 절차는 수집 단계(§2, PDF p.3)에 없다. — [Hupkes & Bogoychev, 2025 (MultiLoKo)](https://arxiv.org/abs/2504.10356)
- [원문 확인] KMMLU는 모든 문항을 한국 시험에서 가져왔고 번역한 것이 없다고 쓴다. §1, PDF p.1: "Unique to KMMLU is its sourcing: all questions are derived from Korean exams, ensuring authentic Korean language without any translated material." 그러나 한국 고유 지식이 필요한 문항은 일부다(3절 참조, 20.4%). — [Son et al., 2024 (KMMLU)](https://arxiv.org/abs/2402.11548)
- [원문 확인] CLIcK는 한국 공식 시험과 교재에서 데이터를 가져왔다. Abstract, PDF p.1: "CLIcK sources its data from official Korean exams and textbooks, partitioning the questions into eleven categories under the two main categories of language and culture." — [Kim et al., 2024 (CLIcK)](https://arxiv.org/abs/2403.06412)
- [원문 확인] HAE-RAE Bench는 한국 고유 지식과 문화 맥락을 떠올리는 능력에 초점을 둔다. Abstract, PDF p.1: "the HAE-RAE Bench emphasizes a model’s aptitude for recalling Korean-specific knowledge and cultural contexts." — [Son et al., 2023 (HAE-RAE Bench)](https://arxiv.org/abs/2309.02706)
- [원문 확인] KoSimpleQA는 한국 문화 지식에 초점을 둔 사실성 벤치마크다. v2 Abstract, PDF p.1: "a benchmark for evaluating factuality in large language models (LLMs) with a focus on Korean cultural knowledge. KoSimpleQA is designed to be challenging yet easy to grade, consisting of 938 short, fact-seeking questions with unambiguous answers." PDF 머리글은 "Published as a conference paper at COLM 2026"이다. — [Ko et al., 2025 (KoSimpleQA)](https://arxiv.org/abs/2510.18368)
- [원문 확인] INCLUDE는 현지 시험을 모아 197,243개 질문을 만들었다. 모든 질문은 원래 언어와 문자로 되어 있다. §3, PDF p.3: "INCLUDE is a dataset of 197,243 MCQA pairs from 1,926 examinations across 44 languages and 15 scripts. These examinations are collected from local sources in 52 countries ... All questions in the dataset are presented in their native languages and scripts." — [Romanou et al., 2024 (INCLUDE)](https://arxiv.org/abs/2411.19799)
- [원문 확인] BertaQA는 바스크 문화에 관한 local 질문과 더 넓은 관심사의 global 질문으로 나뉜다. 원래 바스크어로 쓰였고 전문 번역으로 영어판을 만들었다. §1, PDF p.1–2: "BERTAQA is a multiple-choice trivia dataset with 4,756 questions divided into two subsets: local questions about the Basque Country and its culture, and global questions about subjects of broader interest. These questions were originally authored in Basque and professionally translated into English, making the dataset fully parallel in these two languages." 이 문장은 같은 쪽에서 각주를 사이에 두고 이어진다. — [Etxaniz et al., 2024 (BertaQA)](https://arxiv.org/abs/2406.07302)
- [원문 확인] CaLMQA는 번역하지 않고 문화 특수 질문만 모았다. 정의는 두 갈래다. 한 문화나 몇몇 문화에만 있는 개념을 묻는 질문, 그리고 문화·지역 맥락에 따라 답이 달라지는 질문이다. Abstract, PDF p.1: "We only collect culturally specific questions that (1) refer to concepts unique to one or a few cultures ... or (2) have different answers depending on the cultural or regional context". — [Arora et al., 2024 (CaLMQA)](https://arxiv.org/abs/2406.17761)
- [원문 확인] 스웨덴 벤치마크는 국제 보도가 적은 스웨덴 인물과 사건을 사람이 직접 써서 만들었다. Abstract, PDF p.1: "we therefore introduce a manually written question-answering benchmark specifically targeted to Sweden-related personalities and events, many of which receive very limited coverage in international media." 초록과 2절 일부만 읽었다. 다른 언어에 없는지 확인하는 절차는 읽은 범위에서 찾지 못했다. — [Kunz, 2025](https://arxiv.org/abs/2510.21360)

**안 맞음: 같은 질문을 여러 언어에 두거나, 번역에서 출발하거나, 같은 주제를 비교함**

- [원문 확인] BLEnD는 한 나라에만 적용되는 문항을 일부러 뺐다. 그다음 모든 나라에 같은 템플릿을 씌웠다. §3, PDF p.5: "The collected questions are filtered to eliminate duplicates and country-specific items that can only apply to one country/region. For example, items with proper nouns from a single country/region are excluded. Then the questions are formatted into templates like “What is a common snack for preschool kids in your country?”" — [Myung et al., 2024 (BLEnD)](https://arxiv.org/abs/2406.09948)
- [원문 확인] BordIRlines는 언어판이 서로 비슷하게 "중립적"으로 쓰였으리라 예상하면서도, 따로 쓰이므로 보장되지는 않는다고 본다. 즉 같은 주제가 여러 언어에 있다는 전제다. §3.2, PDF p.4: "we expect articles in different languages to report from similarly “neutral” viewpoints, and minimize culturally specific biases. Still, as articles are independently authored, this is not guaranteed." — [Li et al., 2024 (BordIRlines)](https://arxiv.org/abs/2410.01171)
- [원문 확인] XLQA는 기존 영어 ODQA 벤치마크의 테스트 질문에서 출발해 GPT-4.1로 번역했다. §3.1, PDF p.4: "We begin by collecting high-quality English seed questions from the test sets of existing ODQA benchmarks, such as MKQA (Longpre et al., 2021), MLQA (Lewis et al., 2020), and HotpotQA (Yang et al., 2018)". 이어서 "we generate multilingual questions translated into diverse target languages by utilizing GPT-4.1". 학회(EMNLP 2025)는 검색 결과의 ACL Anthology 미리보기 주소에서만 봤다[2차 출처만]. — [Roh et al., 2025 (XLQA)](https://arxiv.org/abs/2508.16139)
- [원문 확인] XNationQA는 영어 위키백과 목록과 위키데이터에서 사실을 얻었다. 그다음 영어 템플릿으로 질문을 만들어 7개 언어로 옮겼다. 7개 언어에 한국어는 없다. §1, PDF p.2: "nine countries (Japan, India, China, Germany, Spain, Russia, Mexico, the USA, and the UK), fully translated into seven languages (Japanese, Hindi, Chinese, German, Spanish, Russian, and English)". "XNationQA Dataset" 절, PDF p.4: "We used English Wikipedia pages to obtain lists for four specific domains ... After extracting the entity list, we used Wikidata to mine additional information." — [Tanwar et al., 2025 (XNationQA)](https://aclanthology.org/2025.emnlp-main.756/)
- [원문 확인] Global-MMLU는 영어 MMLU를 번역하고 문항마다 문화 민감 여부를 표시했다. 한국어는 OpenAI의 MMMLU(전문가 번역)에서 가져왔다. PDF p.12: "we utilized the remaining 10 languages: Bengali, Chinese, German, Indonesian, Italian, Japanese, Korean, Portuguese, Swahili, Yoruba from this dataset." — [Singh et al., 2024 (Global-MMLU)](https://arxiv.org/abs/2412.03304)
- [원문 확인] TriviaRoomQA는 유럽 6개 언어의 병렬 질문이다. Abstract, PDF p.1: "The benchmark contains 3,300 parallel multiple-choice questions in six European languages and additional 5,340 French-only questions". 초록만 확인했다. — [Mosolova & Seddah, 2026](https://arxiv.org/abs/2607.21445)
- 앞 조사 1절(XOR-TyDi QA): XOR의 "같은 언어로 답할 수 없음"은 Google 검색 1위 글 하나에서 주석자가 답 문단을 고르지 못했다는 뜻이다. 같은 언어 위키백과 전체에 그 사실이 없다는 뜻이 아니다. 또 XOR은 질문을 먼저 정하고 다른 언어에서 답을 찾았다. 과제처럼 한 언어 문서의 사실에서 출발해 질문을 만든 것이 아니다. 질문 언어와 근거 언어의 방향(한국어 질문, 영어 근거)은 과제가 쓰는 두 방향 가운데 하나와 같다. — [앞 조사 노트의 출처: Asai et al., 2021](https://arxiv.org/abs/2010.11856)

### Inferences

- ECLeKTic과 KoLasSimpleQA는 검색 없이 모델 기억만 보는 closed-book 평가다. 두 벤치마크의 "다른 언어판에 글이 없음"은 모델이 사전학습 중에 그 사실을 다른 언어로 보았을 가능성을 근사하려는 기준이다(ECLeKTic §2.1, PDF p.4). 검색 코퍼스에 그 사실이 없는지를 보는 기준이 아니다. RAG 평가 코퍼스에 옮길 때는 이 차이를 감안해야 한다.
- 과제의 조건은 "코퍼스 안에서 한 언어의 문서에만 있는 사실"이다. ECLeKTic과 KoLasSimpleQA의 조건은 "위키백과 전체에서 다른 언어판에 같은 글이 없음"이다. 과제 조건은 코퍼스 단위이고 사실 단위다. 두 벤치마크의 조건은 위키백과 단위이고 글 단위다. 따라서 두 벤치마크의 방식을 그대로 옮길 수는 없다. 특히 한국어 글과 영어 글을 같은 STEM 주제로 짝지어 넣는 코퍼스에는 "같은 글이 없음"이라는 기준이 처음부터 적용되지 않는다.
- 번역에서 출발한 벤치마크(XLQA, XNationQA, Global-MMLU)와 같은 질문을 나라별로 두는 벤치마크(BLEnD)는 "지역마다 답이 다르다"를 다룬다. "한쪽 언어 문서에만 답이 있다"는 다루지 않는다. 과제의 교차 언어 조건과는 다른 축이다.

### Gaps

- 한국어·영어 짝 문서 안에서 사실 단위로 "한쪽에만 있음"을 확인해 질문을 만든 QA/RAG 벤치마크는 찾지 못했다. 검색은 후보 이름 위주로 했으므로 없다고 단정할 수 없다.
- Google Research 블로그 글은 읽지 않았다. 논문 원문을 우선했다.
- XOR-TyDi QA는 앞 조사 내용 말고 새로 확인한 것이 없다.

---

## 2. 내용을 어떻게 고르고 "다른 언어에 없음"을 어떻게 확인하는가

### Takeaway

확인 방식은 세 가지로 나뉜다. 첫째는 글이 있는지로 판정하는 방식이다. ECLeKTic은 다른 11개 언어에 같은 글이 없는지를 보는데, 판정 방법은 논문에 없다. KoLasSimpleQA는 언어 간 링크가 0개인지를 본다. 둘째는 사람의 판단이나 원천의 성격으로 대신하는 방식이다. MultiLoKo의 지역성 점수, ECLeKTic 주석 지침의 "일반 과학 주제 제거", CLIcK의 "한국 중심" 기준, INCLUDE의 시험 단위 지역성 표시, CaLMQA의 LLM 필터가 여기에 든다. 셋째는 확인하지 않는 방식이다. 답이 되는 사실이 다른 언어 문서에 없음을 사실 단위로 확인한 QA 벤치마크는 찾지 못했다. 같은 주제의 두 언어 글을 사실 단위로 비교하는 방법으로는 InfoGap(2024)이 있다. 직접 확인해 보니 ECLeKTic의 한국어 원천 질문 33개 가운데 적어도 2개는 답이 2023년 7월 이전 영어 위키백과의 다른 글에 이미 있었다.

### Cited Findings

#### 2-A. 글이 있는지로 판정: ECLeKTic

- [원문 확인] 선정 조건. 2023년 7월 위키백과 덤프에서 언어마다 글 100개를 뽑았다. 조건은 200자 이상, 2023년 조회 100회 이상, 다른 11개 언어에 같은 글이 없을 것이다. §2, PDF p.3: "Concretely, we analyzed the July 2023 dump of Wikipedia and for each language sampled 100 articles that contain at least 200 characters, had at least 100 views during 2023, and most importantly do not have equivalent articles in any of the other 11 languages." — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인 / 미확인] "같은 글(equivalent article)"을 무엇으로 판정했는지는 논문에 없다. 본문 전체를 "interlanguage", "language link", "Wikidata", "sitelink"로 검색했지만 해당하는 서술이 없었다. 언어 간 링크를 썼으리라고 짐작은 할 수 있지만 확인되지 않는다. — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 질문 생성과 1단계 검토. Gemini가 글의 첫 10문장으로 질문과 답을 제안했다. 주석자는 질문이 그 언어와 특히 관련 있는지 확인했다. 예로 든 것은 일반 상식이나 과학 사실이 아닐 것이다. §2, PDF p.3: "In the first, annotators were presented with Gemini-suggested a question-and-answer pair based on the 10 first sentences of each Wikipedia page. The annotators verified that the questions are based on the context, answerable from the context, and that the question is particularly relevant to the language in question, e.g., it does not relate to general common knowledge or scientific facts." — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 주석 지침 A.1. 과학이나 사회학 같은 일반 주제 글은 지우게 했다. 독일 생물학자에 관한 독일어 질문은 그 언어와 관련된 질문으로 친다. 자연 현상에 관한 질문은 지운다. 다른 언어권 주제를 다루는 질문도 지운다. 예는 한국에서만 유명한 K-pop 그룹에 관한 중국어 질문이다. Appendix A.1, PDF p.15: "Make sure that the topic of the article and/or the question relates to the speakers of that relevant language. In other words, mark as “to remove” also articles that relate to general topics like science or sociology. Note that a question in, e.g., German about a German biologist counts as a question that relates to the language and not a general scientific question, but a question about natural phenomena – should be removed. Also note that questions in one language, that refer to topics relevant to another language, are also to be removed. For example, a question in Chinese that refer to a K-pop band that is famous mostly in Korea." — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 같은 지침은 지역 인물에 정보를 덧붙이게 했다(예: "the Indian TV series"). 지역 인물인지 세계적 인물인지는 구글 검색으로 판단하게 했다. Appendix A.1, PDF p.15: "questions that refer to locally-known figures add the relevant information explicitly to the question. For example, when a question is asking about a TV series in India, prepend "the Indian TV series" to its name. You can use Google search to understand whether an entity is locally- or globally-known." — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 2단계 번역. Gemini가 나머지 11개 언어로 번역했다. 번역 전문 주석자가 고쳤고, 언어 쌍이 드물면 영어를 거쳤다. 번역할 수 없는 예(원천 언어 단어의 뜻을 묻는 질문 등)는 버렸다. 주석은 모두 400시간, 27명이 했다. §2, PDF p.4. — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 논문은 이 방식이 근사라고 밝힌다. 어떤 언어판에 글이 없으면 그 언어 사용자들이 그 주제에 관심이 없고, 인터넷에도 그 정보가 드물다고 가정한다. §2.1, PDF p.4: "Conversely, we assume that the absence of an article from a certain Wikipedia reflects the lack of interest of online speakers in that topic. The information on that topic is therefore assumed to appear sparsely on the internet, if at all." 같은 쪽: "these assumptions allow us to treat the (non)existence of a fact in Wikipedia as an approximate to the (in)accessibility of that fact to a model trained on online data." — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 한계. 2023년 7월 기준이므로 시간이 지나면 다시 만들어야 할 수 있다. §7, PDF p.11: "This makes ECLeKTic somewhat time-dependent, so in the future it would probably require an update." — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 규모. 전체 4,608개 가운데 4,224개는 번역된 목표 언어 질문이고 384개는 원천 언어 질문이다. §2.2, PDF p.4–5: "The resulting benchmark includes 4608 question/answer pairs in 12 languages. 4224 of which are evaluated as target examples ... and 384 are questions in their source language". 4,608은 384×12이고 4,224는 384×11이다. 검색 요약 사이트들이 이 두 숫자를 "서로 다른 규모"처럼 적었지만 모순이 아니다. — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 이 벤치마크는 closed-book 평가다. 원천 언어의 위키백과 문단을 질문과 함께 제공한다. §1, PDF p.2: "each question-answer pair is accompanied by the Wikipedia paragraphs on which it was based, in its original (source) language." 공식 데이터는 Kaggle에 있다(각주 1, PDF p.1). — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)

#### 2-B. 언어 간 링크 수로 판정: KoLasSimpleQA

- [원문 확인] 9개 언어 위키백과 전체를 크롤링했다. 글마다 언어 간 링크 수(n_ill)를 셌다. §2.2.1, PDF p.3: "We crawled all Wikipedia pages in nine languages and extracted their contents. Unlike conventional methods focusing only on entry content, we specifically extracted inter-language link information for each entry and counted the number of these links, denoted as n_ill." — [Jiang et al., 2025](https://arxiv.org/abs/2505.16591)
- [원문 확인] 언어마다 n_ill = 0인 글에서 무작위로 400개를 뽑았다. n_ill이 가장 큰 상위 400개는 일반 지식으로 뽑았다. §2.2.1, PDF p.3: "we randomly select N_specific entries from those where n_ill = 0, ensuring that they represent language-specific knowledge ... Additionally, we identify the top N_general entries with the highest n_ill values ... We set N_specific = 400 and N_general = 400." 그림 2(PDF p.4)의 예는 "汉朝"(n_ill 122, 일반)와 "平淮西碑"(n_ill 0, 언어 고유)다. — [Jiang et al., 2025](https://arxiv.org/abs/2505.16591)
- [원문 확인] n_ill은 링크 전체의 수다. 그러므로 n_ill = 0은 9개 언어뿐 아니라 어떤 언어판에도 같은 글이 없다는 뜻이다. 글 단위로는 ECLeKTic보다 엄격하다. ECLeKTic은 "다른 11개 언어"만 본다. — [Jiang et al., 2025](https://arxiv.org/abs/2505.16591), [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] 질문 생성과 검토. GPT-4o로 (E1, R, E2) 삼중항을 뽑고 질문을 만든 뒤 영어로 번역했다(§2.2.2, PDF p.3–4). 검토는 2단계다. 먼저 GPT-4o가 기준으로 거르고, 다음으로 원어민 주석자가 참조 답을 보지 않고 직접 답한 뒤 그 답을 참조 답과 비교했다. §2.2.3, PDF p.4: "In Stage 2, native-speaking human annotators review the questions without reference answers, checking if they meet the criteria. For qualified questions, annotators provide answers, using search engines if needed, and cite sources (e.g., URLs)." — [Jiang et al., 2025](https://arxiv.org/abs/2505.16591)
- [원문 내 불일치] §2.3(PDF p.4)은 "Initially, 400 Wikipedia entries were selected for each language"라고 쓴다. 그러나 §2.2.1은 언어마다 N_specific = 400과 N_general = 400, 합해서 800개를 뽑는다고 쓴다. — [Jiang et al., 2025](https://arxiv.org/abs/2505.16591)
- [미확인] 크롤링 시점(덤프 날짜)은 논문에서 찾지 못했다.
- [데이터 확인] 논문이 밝힌 공개 주소 github.com/opendatalab/KoLasSimpleQA는 2026-10-21에 GitHub API로 조회하면 404다. Hugging Face 검색에서도 찾지 못했다. 그래서 한국어 언어 고유 문항의 실제 주제는 볼 수 없었다. — [Jiang et al., 2025](https://arxiv.org/abs/2505.16591)

#### 2-C. 사람이 지역성을 점수로 매김: MultiLoKo

- [원문 확인] 1단계. 언어마다 2016–2021년 조회수 상위 6천 개 글에서 문단(3천 자)을 뽑았다. 주석자가 지역성을 1–5점으로 매겼다. 1은 그 언어에 고유한 주제(예: 스웨덴 밖에서 알려지지 않은 스웨덴 가수)이고 5는 세계적으로 알려진 주제(예: 유튜브)다. §2, PDF p.3: "The first step in our protocol is the sampling of the 6K most visited Wikipedia pages for each language for the period of 2016-2021. We sample paragraphs from those pages by randomly selecting a word in the page and expanding left and right until we reach 3K characters. Next, we ask annotators to judge the local relevance of the samples on a scale from 1 to 5, where 1 refers to topics specific to the language (e.g. a Swedish singer not known outside of Sweden) and 5 to globally well-known topics (e.g. ‘Youtube’). We disregard all topics that have a locality score above 3." — [Hupkes & Bogoychev, 2025](https://arxiv.org/abs/2504.10356)
- [원문 내 불일치] 부록 D.1은 반대 규칙을 적는다. Appendix D.1, PDF p.24: "We disregard everything with a locality rating of 3 or lower." 본문을 따르면 1–3점(지역)을 남기고, 부록을 따르면 4–5점(국제)을 남긴다. 3점의 정의는 "National Significance. Content that is widely recognized within a single country, but relatively unknown internationally."(표 3, PDF p.24)이다. 어느 쪽이 실제로 쓰였는지는 확인하지 못했다. — [Hupkes & Bogoychev, 2025](https://arxiv.org/abs/2504.10356)
- [원문 확인] 한계. 영어, 스페인어, 포르투갈어, 중국어, 프랑스어처럼 여러 문화에 걸친 언어는 따로 통제하지 않았다. §7, PDF p.13: "We did not separately control for that and the data for those languages thus likely comprises a mix of different locales." — [Hupkes & Bogoychev, 2025](https://arxiv.org/abs/2504.10356)
- [데이터 확인] README에 따르면 데이터는 크롤링으로 학습에 섞이지 않도록 비밀번호를 건 압축 파일로 공개된다. README는 비밀번호를 적어 두고 데이터를 다른 곳에 다시 올리지 말라고 한다. dev 파일은 언어마다 250개 질문이다. 비공개 test는 "the topics it includes are more obscure"(주제가 더 잘 알려지지 않은 것)다. 그래서 이 노트에는 질문과 답의 문장을 옮기지 않는다. — [MultiLoKo GitHub README](https://github.com/facebookresearch/multiloko)

#### 2-D. 원천의 성격이나 사람의 판단으로 대신함(다른 언어 확인 없음)

- [원문 확인] CLIcK의 검증 기준 네 가지 가운데 하나가 "한국과 중심적으로 관련될 것"이다. 다른 언어 자료와 비교하는 기준은 없다. §3.2, PDF p.4: "1. Questions are solely based on the given text. 2. Information in Questions remains consistent over time. 3. Questions should centrally relate to Korea. 4. Questions should be objective and free from bias." — [Kim et al., 2024](https://arxiv.org/abs/2403.06412)
- [원문 확인] CLIcK의 원천은 한국 시험 6종(CSAT, TOPIK, PSE(9급 공무원), PSAT, KHB(한국사능력검정 기본), Kedu(한국어교원))과 KIIP(사회통합프로그램) 교재 하나다. 교재에서는 GPT-4로 새 질문을 만들었다. §3.1과 표 3, PDF p.3–4: "we employ two approaches: 1) following the AGIEval dataset (Zhong et al., 2023) to select questions from standardized Korean exams, and 2) using GPT-4 to generate new questions based on textbooks." — [Kim et al., 2024](https://arxiv.org/abs/2403.06412)
- [원문 내 불일치] CLIcK의 숫자는 서로 맞지 않는다. 표 1(PDF p.3)의 합계 행은 교재 1,245개, 시험 750개, 계 1,995개다. 그러나 표 1 각 행을 더하면 교재 686개, 시험 1,309개다(직접 계산. 계 1,995는 맞음). 표 2(PDF p.4)의 시험별 개수를 더하면 1,245개다(직접 계산). §3.2(PDF p.4)는 "the initial dataset, which consisted of 1,985 samples, was reduced to 1,245 samples, accounting for 62.9% of the original dataset"라고 쓴다. 전체 1,995개는 초록, 본문, 표 1에서 같다. — [Kim et al., 2024](https://arxiv.org/abs/2403.06412)
- [원문 확인] KMMLU는 시험 533개 출처에서 자동 크롤링했다. §3.2, PDF p.4: "Our dataset is a compilation of questions from 533 diverse sources, spanning the Public Service Aptitude Test (PSAT), Korean License Tests, and the College Scholastic Ability Test (CSAT) ... Initially, we collected 371,002 questions using automatic crawling." 걸러낸 뒤 243,777개가 남았다. — [Son et al., 2024](https://arxiv.org/abs/2402.11548)
- [원문 확인] KMMLU는 한국 지식이 필요한 정도를 사후 표본으로 쟀다. 범주마다 10문항씩 무작위로 골랐고(KMMLU 450개, 번역 MMLU 570개) 저자 두 명이 판정했다. 그 결과 KMMLU의 20.4%가 한국 문화 관행, 사회 규범, 법 체계를 알아야 풀린다. §6.1과 그림 4, PDF p.8: "Conversely, 20.4% of KMMLU requires understanding Korean cultural practices, societal norms, and legal frameworks." 이 문장은 판정 표본(450개)에 대한 값이다. — [Son et al., 2024](https://arxiv.org/abs/2402.11548)
- [원문 확인] KMMLU-KOR 부분집합. 키워드 필터로 후보 2,149개를 모았다. 저자 두 명이 따로 검토해 Cultural, Regional, Legal, Others로 나누었고 1,305개가 남았다. Appendix I, PDF p.23–24: "We initially adopted a keyword filter to collect 2,149 candidate questions. Then, two authors independently reviewed each question, eliminating irrelevant entries and categorizing the pertinent ones into four distinct categories ... Following the filtering, 1,305 questions remained, constituting the KMMLU-KOR subset." — [Son et al., 2024](https://arxiv.org/abs/2402.11548)
- [원문 내 불일치] KMMLU 문항 수는 초록과 §3.1(PDF p.1, p.4)에서 35,030개다. 같은 §3.2(PDF p.5)의 테스트 세트 설명에는 "35,050 questions in total"이 나온다. — [Son et al., 2024](https://arxiv.org/abs/2402.11548)
- [원문 확인] HAE-RAE Bench의 과제별 원천은 다음과 같다. 외래어(LW)와 표준 용어(SN)는 국립국어원 자료다. 희귀어(RW)는 KBS 「우리말 겨루기」다. 상식(GK)은 크라우드소싱으로 모았고 전통 17개, 법 10개, 지리 49개, K-pop 50개, 드라마 50개다. 역사(HI)는 나무위키 "Korean history" 태그 문서 40개에서 저자가 직접 만들었다. 독해(RC)는 KLAT 공개 표본이다. §3.1–3.6, PDF p.3–4. 역사 과제, PDF p.4: "We first sourced web pages tagged “Korean history" from Namuwiki, Korea’s equivalent to Wikipedia, and randomly selected 40 pages. From each page, authors manually crafted five questions." 표 1(PDF p.3)의 개수는 LW 169, RW 405, SN 153, RC 447, GK 176, HI 188, 합 1,538(직접 계산)이다. — [Son et al., 2023](https://arxiv.org/abs/2309.02706)
- [원문 확인] KoSimpleQA의 작성 기준. 크라우드 작업자(Selectstar, Flitto)가 한국 문화 맥락에 근거한 사실 질문을 썼다. 문화는 넓게 정의했다(전통 명절부터 예능 프로그램 세부까지). 강한 상용 LLM 4개 가운데 적어도 하나가 틀려야 한다. 2023-12-31까지의 지식으로 답할 수 있어야 한다. 근거 링크를 최대 4개 남긴다. 주제 범주는 SimpleQA의 것을 따랐다. §3.1, PDF p.3–5. PDF p.4: "We define “culture” broadly, extending beyond traditional heritage (e.g., history, literature) to encompass modern sociocultural trends and contemporary interests unique to native speakers." 영어나 다른 언어 자료에 그 사실이 없는지 확인하는 절차는 없다. — [Ko et al., 2025](https://arxiv.org/abs/2510.18368)
- [데이터 확인] KoSimpleQA 저장소에는 파일이 두 개 있다. `kosimpleqa.json`은 1,000개이고 v1 초록의 개수다. `updated_kosimpleqa_with_trans.json`은 938개이고 v2와 같으며 영어 번역 필드가 있다. 내려받아 셌다. — [naver-ai/KoSimpleQA](https://github.com/naver-ai/KoSimpleQA)
- [원문 확인] INCLUDE의 지역성 표시는 문항 하나하나가 아니라 시험 출처 단위다. §3.2, PDF p.4: "Given the prohibitive cost of performing sample-level annotation, we only perform a coarse annotation by labeling the exam sources of QA pairs, rather than individual samples." 한계 절(PDF p.11)도 같은 점을 적는다: "our regional knowledge labels were annotated at the exam topic level, rather than at the individual question level". — [Romanou et al., 2024](https://arxiv.org/abs/2411.19799)
- [원문 확인] INCLUDE의 네 가지 표시와 비율(PDF p.5). region-agnostic 34.4%는 특정 지역 지식이 필요 없고 어느 언어로 물어도 답이 같은 문항이다. region-explicit 18.8%는 법, 규제, 절차 지식이다. cultural 16.4%는 그 지역의 문화나 역사 맥락이다. region-implicit 30.4%는 나머지 가운데 지역 맥락이 필요할 수 있는 문항이다. 원문: "Region-agnostic questions do not require knowledge of particular regions (e.g., mathematics, physics), and their answers should remain common regardless of the language in which a question is posed." — [Romanou et al., 2024](https://arxiv.org/abs/2411.19799)
- [원문 확인] INCLUDE의 원천은 두 갈래다. 새로 파싱하고 검증한 118,606개(60.2%)와 기존 벤치마크(ArabicMMLU, ChineseMMLU, TurkishMMLU, PersianMMLU, VNHSGE, EXAMS)에서 가져온 78,637개(39.8%)다. §3.1, PDF p.4. — [Romanou et al., 2024](https://arxiv.org/abs/2411.19799)
- [원문 확인] BertaQA의 local/global 구분은 원천에 이미 있었다. 저자는 이를 확인만 했다. 질문 몇 개를 따옴표로 묶어 구글에서 검색했지만 결과가 없었다. 저자는 답은 웹에서 찾을 수 있을지도 모르지만 같은 질문은 없다고 적는다. §2, PDF p.3: "The dataset was originally compiled in Basque by crawling public sources that are no longer available. The questions were already classified into local and global topics ... To check whether the content is present in other websites, we wrote some of the questions verbatim in Google search using quotation marks, but received no results. Finding the answer to some of these questions on the web is still possible, but at least the same questions are not present on the web." — [Etxaniz et al., 2024](https://arxiv.org/abs/2406.07302)
- [원문 확인] CaLMQA는 고·중자원 언어에서는 각국 커뮤니티 Q&A 게시판에서 질문을 모았다. 저자원 언어에서는 프리랜서가 질문을 썼다. 자동으로 모은 질문은 GPT-4o-mini로 문화 특수성과 품질을 판정해 52%를 남겼다. §2.2, PDF p.3: "We filter our questions using GPT-4o-mini, with two model passes that assess each question’s cultural specificity and general quality, retaining 52% of questions". 한국어 게시판은 네이버 지식iN(https://kin.naver.com/qna/)이다(PDF p.14 표). — [Arora et al., 2024](https://arxiv.org/abs/2406.17761)

#### 2-E. 사실 단위로 비교하는 방법: InfoGap, WikiGap(벤치마크 아님)

- [원문 확인] InfoGap은 같은 주제의 두 언어 글을 사실 단위로 맞춰 본다. 단계는 세 가지다. GPT-4로 문단을 원자 사실로 쪼갠다. LaBSE 임베딩으로 후보 사실을 정렬하되 문단 정렬로 후보를 좁힌다. GPT-4로 한쪽 사실이 다른 쪽 사실에서 함의되는지 판정한다. §2.1–2.2, PDF p.2–3: "we use GPT-4 (Achiam et al., 2023) for fact decomposition"; "multilingual LaBSE embeddings (Feng et al., 2020)"; "we prompt GPT-4 to compare an English fact to its aligned facts in F." — [Samir et al., 2024 (InfoGap)](https://arxiv.org/abs/2410.04282)
- [원문 확인] InfoGap의 신뢰도. 언어 쌍과 방향마다 80개 사실을 사람이 표시했고, 사람 판정과의 F1은 0.78–0.90이다(En→Fr 0.81, Fr→En 0.90, En→Ru 0.78, Ru→En 0.88). 주석자 간 일치도는 Cohen's κ 0.71(En/Fr), 0.78(En/Ru)이다. 표 2와 §2.3, PDF p.4: "One author annotated 80 facts in each language pair and for both directions within each language pair." — [Samir et al., 2024](https://arxiv.org/abs/2410.04282)
- [원문 확인] InfoGap으로 본 결과의 예. 러시아어 전기 내용의 평균 34%가 영어판에 없다. §1, PDF p.2: "we find that on average 34% of the content in Russian biographies is not present in their English counterparts." 대상은 영어·러시아어·프랑스어 위키백과의 전기 2.7K개다(Abstract, PDF p.1). 한국어는 없다. — [Samir et al., 2024](https://arxiv.org/abs/2410.04282)
- [원문 확인] WikiGap은 InfoGap을 바탕으로 프랑스어·러시아어·중국어판에만 있는 사실을 영어 위키백과 화면에 보여 준다. 중국어를 추가하면서 사람 평가로 성능이 비슷한지 확인했다고 쓴다. §3.3.1, PDF p.11: "we incorporated support for Chinese into the fact decomposition and verification modules ... and conducting human evaluation on Chinese texts to confirm that InfoGap performs comparably to its performance on the original languages". 중국어 평가의 수치는 찾지 못했다[미확인]. — [Wang et al., 2025 (WikiGap)](https://arxiv.org/abs/2505.24195)

#### 2-F. 직접 확인: 글이 없다고 사실이 없는 것은 아니다(ECLeKTic 한국어 원천 질문)

- [데이터 확인] ECLeKTic 공식 데이터는 Kaggle에 있다. 여기서는 제3자가 Hugging Face에 올린 사본(`ura-hcmut/ECLeKTic`의 `eclektic_main.jsonl`)을 썼다. 사본은 384행이다. 원천 언어별 개수는 hi 64, en 39, zh 35, ko 33, es 32, id 31, he 29, it 29, pt 28, ja 26, fr 22, de 16이다. 이 개수를 384로 나누면 논문 그림 3의 비율과 모두 맞는다(예: ko 33/384 = 8.6%, hi 64/384 = 16.7%, de 16/384 = 4.2%). 그래서 사본이 공식 데이터와 같은 384개라고 보았다. 공식 Kaggle 파일과 직접 대조하지는 않았다. — [ura-hcmut/ECLeKTic (Hugging Face)](https://huggingface.co/datasets/ura-hcmut/ECLeKTic), [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [직접 확인] 한국어 원천 질문 33개의 위키백과 글을 2026-10-21 기준 언어 간 링크로 조회했다. 32개는 어떤 언어로도 링크가 없다. 1개(박영훈 (영화 감독))는 지금 프랑스어판 링크가 있다. 프랑스어는 ECLeKTic의 12개 언어 가운데 하나다. 그러므로 이 글은 지금 기준으로는 선정 조건을 벗어난다. 이 조회는 지금 상태이고 2023년 7월 덤프 상태가 아니다. 방법: `ko.wikipedia.org/w/api.php?action=query&prop=langlinks&lllimit=max&redirects=1`. — [Wikipedia API](https://ko.wikipedia.org/w/api.php)
- [직접 확인] 한국어 원천 질문의 답 가운데 몇 개를 골라 영어 위키백과 본문을 검색했다(검색어 8개). 다음 두 개는 2023-07-01 이전 판에 이미 답이 있었다. 비율이 아니라 손으로 고른 예다.
  - 질문 387(원천 글 "한국의 여성주의", 1927년 결성 단체 → 근우회)의 답은 영어 글 "Geunuhoe"의 2023-04-29 판(rev 1152241248)에 있다: "was a Korean women's organization founded in June 1927". 원천 글에 영어판이 없어도, 답은 영어 위키백과의 다른 글에 있었다. — [en.wikipedia "Geunuhoe" rev 1152241248](https://en.wikipedia.org/w/index.php?oldid=1152241248)
  - 질문 369(원천 글 "남원 실상사 동·서 삼층석탑", 실상사를 창건한 홍척이 산 시대의 왕 → 흥덕왕)의 답은 영어 글 "Silsangsa"의 2023-01-08 판(rev 1132278076)에 있다: "the temple was constructed in the era of [[Heungdeok of Silla]] by the great monk Hongcheok". — [en.wikipedia "Silsangsa" rev 1132278076](https://en.wikipedia.org/w/index.php?oldid=1132278076)
  - 질문 379(안동 간고등어의 재료 → 고등어)는 지금 영어 글 "Andong", "Chub mackerel" 등에 "salted mackerel"이 나온다. 그러나 "Andong" 글의 2023-03-30 판(rev 1147358754)에서는 "salted mackerel"을 찾지 못했다. 다른 글의 2023년 판은 확인하지 않았다. 그래서 덤프 시점에 있었는지는 판정하지 않는다.
  - 다른 검색어("Kang Geun-ho", "Hyon Song-wol" Gangneung 등)로 나온 영어 글은 답이 되는 사실이 들어 있는지 확인하지 않았다. 세지 않는다.
  - 방법: `en.wikipedia.org/w/api.php?action=query&list=search`로 찾았다. 그다음 `prop=revisions&rvstart=2023-07-01T00:00:00Z&rvdir=older&rvlimit=1`로 그 날짜 직전 판의 본문을 받아 문자열을 찾았다. — [Wikipedia API](https://en.wikipedia.org/w/api.php)
- [데이터 확인] 사람이 검토한 문항에도 오류가 남아 있다. 질문 365는 원천 글이 "대한민국 민법 제764조"인데 질문 문장은 "대한민국 민법 376조에 따르면"이다. — [ura-hcmut/ECLeKTic](https://huggingface.co/datasets/ura-hcmut/ECLeKTic)

#### 2-G. 직접 확인: MultiLoKo 한국어 원천 글의 영어판

- [직접 확인] MultiLoKo 한국어 dev 질문 250개는 서로 다른 위키백과 글 250개에서 나왔다. 각 질문의 `id`가 "순위_제목" 꼴이다. 이 글들의 영어 언어 간 링크를 2026-10-21에 조회했다. 192개(76.8%)는 영어판이 있고 57개(22.8%)는 없으며 1개(419민주묘지역)는 제목을 찾지 못했다. 영어판이 있는 예는 문화방송, 트와이스, 연평도 포격, 서울대학교, 경기도다. 없는 예는 국민연금, 대한민국 헌법 제1조, 남영동 대공분실, 전원일기다. 한계가 있다. 파일 이름에서 괄호가 빠진 제목 26개는 변형을 추측해서 맞췄다(예: "도깨비 드라마" → 넘겨주기를 거쳐 "쓸쓸하고 찬란하神 - 도깨비"). "정인숙 1945년"은 "정인숙 (모델)"로 넘겨졌는데 같은 사람인지 확인하지 않았다. 지금 상태이고, 글 단위다. 방법: `ko.wikipedia.org/w/api.php?action=query&prop=langlinks&lllang=en&redirects=1`. — [MultiLoKo 데이터](https://github.com/facebookresearch/multiloko), [Wikipedia API](https://ko.wikipedia.org/w/api.php)

### Inferences

- ECLeKTic과 KoLasSimpleQA의 "글이 없음"은 "그 사실이 다른 언어에 없음"을 보장하지 않는다. 한국어 원천 33개에서 손으로 고른 몇 개만 봐도 2개는 당시 영어 위키백과의 다른 글에 답이 있었다. 이 방식으로 고른 사실도 사실 단위로 다시 확인해야 "다른 언어 문서에 없음"을 말할 수 있다.
- 과제 코퍼스는 20–30개 문서로 작고 닫혀 있다. 그러므로 "다른 언어에 없음"을 확인하는 범위는 위키백과 전체가 아니라 코퍼스 안의 다른 언어 문서다. 이 범위에 가장 가까운 기존 방법은 InfoGap이다. 같은 주제의 두 언어 글을 사실 단위로 쪼개고, 맞추고, 함의를 판정한다. 다만 InfoGap은 한국어로 검증된 적이 없다. 과제에 쓰려면 한국어·영어에서 사람 판정과 맞는지 따로 확인해야 한다.
- MultiLoKo처럼 조회수 상위 글에서 고르면 지역 주제라도 영어판이 있는 경우가 많다(한국어 dev 원천 글의 76.8%). "지역 주제"와 "한 언어에만 있는 글"은 다른 조건이다.

### Gaps

- ECLeKTic이 "같은 글"을 무엇으로 판정했는지(언어 간 링크, 위키데이터 등) 확인하지 못했다.
- ECLeKTic 공식 Kaggle 데이터는 직접 열지 않았다. 제3자 사본을 썼고, 개수가 논문 그림과 맞는 것만 확인했다.
- KoLasSimpleQA는 덤프 날짜와 데이터를 확인하지 못했다. 한국어 언어 고유 문항 84개의 주제도 모른다.
- MultiLoKo의 지역성 규칙(3점 초과를 버림 / 3점 이하를 버림) 가운데 어느 것이 실제로 쓰였는지 확인하지 못했다.
- ECLeKTic 영어 검색은 손으로 고른 예다. 33개 전체에서 답이 영어 위키백과 어딘가에 있는 비율은 재지 않았다.
- WikiGap의 중국어 사람 평가 수치는 찾지 못했다.

---

## 3. 한국어를 포함하는가, 과학·STEM처럼 언어에 따라 잘 달라지지 않는 분야는 어떻게 다루는가

### Takeaway

한국어는 ECLeKTic(원천 질문 33개), KoLasSimpleQA(언어 고유 84개), MultiLoKo(500개), INCLUDE(1,781개), CaLMQA(5,875개), BLEnD, BordIRlines, XLQA, Global-MMLU에 들어 있다. KMMLU, CLIcK, HAE-RAE, KoSimpleQA는 한국어 전용이다. STEM은 세 가지로 다뤄진다. 첫째는 빼는 것이다. ECLeKTic은 일반 과학 주제를 지침으로 뺐다. 둘째는 "지역과 무관"으로 분류하는 것이다. INCLUDE는 수학·물리를 region-agnostic의 예로 들고, Global-MMLU는 STEM 950문항 중 30개만 문화 민감으로 판정했다. 셋째는 한국에 묶어서 남기는 것이다. KMMLU 그림 1은 한국 법규, 한반도 생태, 국내 기관, 국내 사고를 예로 든다. KoSimpleQA는 Science & Technology가 19.2%(180개)로 가장 많다. 그 가운데 96개는 질문에 "최초·처음·첫"이 들어 있다(예: 대한민국 최초의 통신위성, 누리호 첫 발사 성공). BertaQA의 local Science and Technology는 292개다. 다만 한국에 관한 STEM 사실이 한국어에만 있는 것은 아니다. KoSimpleQA의 STEM 문항이 근거로 든 한국어 위키백과 글 43개 가운데 33개는 영어판이 있다.

### Cited Findings

#### 3-A. 한국어 포함 여부와 규모

| 벤치마크 | 한국어 | 한국어 규모와 성격 | 출처 |
|---|---|---|---|
| ECLeKTic | 포함 | 원천 질문 33개(전체 384개의 8.6%). 다른 언어 원천 질문의 한국어 번역도 포함 | 그림 3, PDF p.5 [그림 판독] [Goldman et al., 2025](https://arxiv.org/abs/2502.21228); 사본 데이터 [데이터 확인] [ura-hcmut/ECLeKTic](https://huggingface.co/datasets/ura-hcmut/ECLeKTic) |
| KoLasSimpleQA | 포함 | 일반 151개, 언어 고유 84개(표 2, PDF p.4) | [Jiang et al., 2025](https://arxiv.org/abs/2505.16591) |
| MultiLoKo | 포함 | 언어당 500개(dev 250개 공개). 데이터에 `korean` 폴더가 있음 | [데이터 확인] [MultiLoKo](https://github.com/facebookresearch/multiloko) |
| INCLUDE | 포함 | 전체 1,781개(표 8, PDF p.23). 공개된 INCLUDE-BASE 한국어 test 500개는 전문 자격시험 250개(region explicit)와 경제학 250개(region implicit) | [Romanou et al., 2024](https://arxiv.org/abs/2411.19799); [데이터 확인] [CohereLabs/include-base-44](https://huggingface.co/datasets/CohereLabs/include-base-44) |
| CaLMQA | 포함 | 질문 5,875개, 답 있는 것 75개(표 1, PDF p.5). 네이버 지식iN | [Arora et al., 2024](https://arxiv.org/abs/2406.17761) |
| BLEnD | 포함 | 한국어로 남한(KR)과 북한(KP) 두 지역(PDF p.2) | [Myung et al., 2024](https://arxiv.org/abs/2406.09948) |
| BordIRlines | 포함 | 표 2(PDF p.14)의 한국어 행: Territories 7, Articles 13, Passages 74, Passage-Query Pairs 142. 사람 주석 5개 언어에도 한국어가 있음(§3.3, PDF p.4) | [Li et al., 2024](https://arxiv.org/abs/2410.01171) |
| XLQA | 포함 | 8개 언어 중 하나. 영어 답과 다른 한국어 답 1,188개, 37.3%(표 5, PDF p.7) | [Roh et al., 2025](https://arxiv.org/abs/2508.16139) |
| Global-MMLU | 포함 | 한국어는 OpenAI MMMLU의 전문가 번역(PDF p.12) | [Singh et al., 2024](https://arxiv.org/abs/2412.03304) |
| KMMLU, CLIcK, HAE-RAE, KoSimpleQA | 한국어 전용 | 각각 35,030개, 1,995개, 1,538개, 938개 | [KMMLU](https://arxiv.org/abs/2402.11548), [CLIcK](https://arxiv.org/abs/2403.06412), [HAE-RAE](https://arxiv.org/abs/2309.02706), [KoSimpleQA](https://arxiv.org/abs/2510.18368) |
| BertaQA, XNationQA, InfoGap·WikiGap, 스웨덴 벤치마크, TriviaRoomQA | 없음 | — | [BertaQA](https://arxiv.org/abs/2406.07302), [XNationQA](https://aclanthology.org/2025.emnlp-main.756/), [InfoGap](https://arxiv.org/abs/2410.04282), [WikiGap](https://arxiv.org/abs/2505.24195), [스웨덴](https://arxiv.org/abs/2510.21360), [TriviaRoomQA](https://arxiv.org/abs/2607.21445) |

- [원문 확인 + 직접 계산] BordIRlines 표 2의 첫 열(Territories)을 49개 언어 모두 더하면 720이다. 이 값은 전체 질의 수 720과 같다. 영어 값 251은 전체 영토 수와 같다. 그러므로 이 열은 언어별 질의 수이고, 한국어 질의는 7개다. 앞 조사 4절 Gaps의 "BordIRlines의 49개 언어에서 한국어 질문이 몇 개인지는 확인하지 못했다"에 대한 답이다. — [Li et al., 2024](https://arxiv.org/abs/2410.01171)
- [원문 내 불일치] XLQA는 "Among the 3,000 source questions, 2,356 (73.9%) were categorized as locale-sensitive"라고 쓴다(§4.1, PDF p.5). 그러나 2,356/3,000은 78.5%다. 표 5의 언어별 비율(예: ko 1,188 = 37.3%)은 분모를 약 3,185로 잡아야 맞는다(직접 계산). — [Roh et al., 2025](https://arxiv.org/abs/2508.16139)
- [데이터 확인 / 원문 내 불일치] INCLUDE-BASE는 "Each language has a maximum of 550 samples, with 500 drawn from domains that correspond to regional knowledge and 50 from STEM subjects"라고 쓴다(§4.1, PDF p.5). 그러나 공개된 한국어 test는 500개뿐이다. 전문 자격시험 250개와 경제학 250개이고 STEM은 0개다. validation 10개도 같은 두 과목이다. 논문 표 9(PDF p.29)와 표 11(PDF p.31)에서 한국어 행 바로 아래에 History 335와 Finance 40이 보인다. 두 단 배치로 보면 이 두 줄은 리투아니아어 칸에 속한다. 공개 데이터의 한국어에도 없다. 표 6(PDF p.22)의 한국어 값(Humanities 91.6, Professional 46.4)은 경제학과 전문 자격시험 두 과목과 맞는다. — [Romanou et al., 2024](https://arxiv.org/abs/2411.19799), [CohereLabs/include-base-44](https://huggingface.co/datasets/CohereLabs/include-base-44)
- [데이터 확인] ECLeKTic의 한국어 원천 질문 33개의 원천 글은 다음처럼 묶인다(내가 제목을 보고 묶음). 한국 법조문이 9개다(형법 제57조·제297조의2·제362조, 민법 제653조·제764조, 헌법 제119조, 노역장, 기망행위, 혼인 (대한민국 민법)). 지역 문화재·유적이 5개다(남원 실상사 동·서 삼층석탑, 서산 둔당리 지석묘, 평택 무성산성지, 감은사지 서삼층석탑 사리장엄구, 고창 삼인리 송악). 지역 기관·시설이 4개다(전주송북초등학교, 강릉아트센터, 한국장애인고용공단, 중앙대로 (부산 양산)). 연예인이 3개다(임재욱, 정재곤, 박영훈 (영화 감독)). 민속·음식·대중문화·지역 축제가 5개다(지신밟기, 신고산타령, 안동 간고등어, 복학왕, 안양공공예술프로젝트). 역사·인물이 4개다(구삼국사, 조선의 유학자, 강근호, 한국의 여성주의). 종교가 1개(일원상), 기타가 2개(고려저수지, 3cf)다. 논문 그림 13의 한국어 영역 분포와 견주면, Government·Law·Politics 33.3%는 33개 중 11개에 해당한다. — [ura-hcmut/ECLeKTic](https://huggingface.co/datasets/ura-hcmut/ECLeKTic), [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)

#### 3-B. STEM을 빼거나 "지역과 무관"으로 분류하는 경우

- [원문 확인] ECLeKTic은 일반 과학 주제를 지침으로 뺐다(2-A의 Appendix A.1 인용). 그래도 Gemini가 자동 분류한 10개 영역에 Science and Technology가 남았다. 분류는 100개 표본으로 검증했다(각주 4, PDF p.5). — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [그림 판독] ECLeKTic 전체 영역 분포(그림 4, PDF p.5): Arts and Culture 22.7%, Government·Law·Politics 18.4%, History 14.0%, Religion·Philosophy·Mythology 8.2%, Sports and Recreation 7.9%, Science and Technology 7.7%, Media and Communication 7.1%, Education and Academia 5.6%, Social Structures and Organizations 4.3%, Business and Economics 4.1%(합 100.0). — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [그림 판독] ECLeKTic 한국어 원천 질문의 영역 분포(그림 13, PDF p.23, 300dpi로 확대해 읽음): Government·Law·Politics 33.3%, Arts and Culture 27.3%, History 18.2%, Religion·Philosophy·Mythology 6.1%, Media and Communication 6.1%, Science and Technology 3.0%, Education and Academia 3.0%, Social Structures and Organizations 3.0%. 33개를 기준으로 하면 3.0%는 1개다(추론. 1/33 = 3.03%). 어느 문항인지는 데이터에 영역 표시가 없어 알 수 없다. — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] ECLeKTic은 영역 분포가 언어 사용자들의 고유한 관심을 반영한다고 해석한다. 히브리어·힌디어는 종교, 프랑스어·이탈리아어는 예술·문화, 중국어는 역사가 많다. §2.2, PDF p.5. — [Goldman et al., 2025](https://arxiv.org/abs/2502.21228)
- [원문 확인] INCLUDE는 수학·물리를 "지역과 무관"의 예로 든다(2-D 인용, PDF p.5). INCLUDE-BASE는 언어마다 지역 지식 영역 500개와 STEM 50개를 뽑도록 설계했다(PDF p.5). 한국어 공개분에는 STEM이 없다(3-A). — [Romanou et al., 2024](https://arxiv.org/abs/2411.19799)
- [원문 확인] Global-MMLU는 MMLU 57개 과목에서 50개씩, 2,850개를 표시했다(PDF p.5). 인문·사회는 문화·지역 지식이 자주 필요했다. STEM과 의학은 대체로 필요하지 않았다. STEM 950개 가운데 30개(3.15%)만 문화 민감(CS)이다. §2.2, PDF p.8: "Questions from categories in Humanities and Social Sciences frequently required cultural or regional knowledge, while those from the STEM and Medical categories generally did not ... Within the STEM category, only 30 out of 950 samples (3.15%) were identified as CS". — [Singh et al., 2024](https://arxiv.org/abs/2412.03304)
- [원문 내 불일치] Global-MMLU PDF p.9는 STEM이 CS 전체의 2.9%라고 쓴다: "questions from the STEM category, which contribute 33.3% of the MMLU Annotated, are under-represented in CS, making up only 2.9% of all questions identified as requiring CS knowledge." 그러나 CS는 792개다(PDF p.13: "It includes 792 annotated samples in English"). 30/792는 3.8%다(직접 계산). — [Singh et al., 2024](https://arxiv.org/abs/2412.03304)
- [원문 확인] KMMLU는 한국 지식이 필요한 20.4%를 뺀 나머지가 일반 지식이라고 쓴다. 수학처럼 어느 나라 지식에도 묶이지 않는 분야가 예다. §6.1, PDF p.8: "while 20.4% of KMMLU’s content is culturally specific, the remainder broadly assesses a language model’s general knowledge, including areas such as mathematics, which are universally applicable and not tied to any particular country’s knowledge base." — [Son et al., 2024](https://arxiv.org/abs/2402.11548)
- [원문 확인] CLIcK(문화 8개, 언어 3개 범주, 표 1 PDF p.3), HAE-RAE(어휘·역사·상식·독해), BLEnD(음식, 스포츠, 가족, 교육, 명절·여가, 직장 생활. PDF p.2)에는 STEM 범주가 없다. CLIcK의 문화 범주는 KIIP 교재 목차를 따랐다. §3.3, PDF p.4: "We adopt eight subcategories based on the KIIP textbook." — [Kim et al., 2024](https://arxiv.org/abs/2403.06412), [Son et al., 2023](https://arxiv.org/abs/2309.02706), [Myung et al., 2024](https://arxiv.org/abs/2406.09948)
- [원문 확인] TriviaRoomQA 초록은 모델이 역사·지리·수학처럼 지식 집약적인 주제에 강하다고 쓴다. 유명인, 음악, 영화, 뉴스 같은 대중문화에는 약하다. Abstract, PDF p.1: "models are strong on knowledge-intensive topics such as history, geography, and mathematics, but substantially weaker on everyday popular-culture topics such as celebrities, music, movies, and news." 초록만 확인했다. — [Mosolova & Seddah, 2026](https://arxiv.org/abs/2607.21445)

#### 3-C. STEM을 한국(또는 지역)에 묶어서 남기는 경우

- [원문 확인 + 그림 판독] KMMLU 그림 1(PDF p.2)은 "필요한 한국 지식의 종류"(Cultural, Regional, Legal, Other)와 과목군을 표로 맞춰 예를 든다. STEM과 Applied Science 칸의 예는 다음과 같다.
  - STEM × Cultural(토목공학): "우리나라 대도시지역의 주요 문제라고 볼 수 없는 것은?"
  - STEM × Regional(생태학): "한반도의 생태축에 속하지 않는 것은?"
  - STEM × Legal(토목공학): "주택건설기준 등에 관한 규정상 도로 및 주차장의 경계선으로부터 공동주택의 외벽까지는 최소 얼마 이상을 띄워야 하는가?"
  - STEM × Other(생물학): "국내 대표적인 미생물 균주 분양 기관인 생물자원센터(KCTC) 홈페이지에서 균주를 검색할 때 나타나는 검색 결과에 포함되지 않는 것은?"
  - Applied Science × Regional(해양공학): "우리나라 동해안에서 남서풍이 오래 불면 어떤 현상이 일어나겠는가?"
  - Applied Science × Legal(에너지관리): "'개발행위허가'만으로 태양광 발전소를 건설할 수 있는 '관리지역'의 면적제한 기준은 최대 몇 m2 미만인가?"
  - Applied Science × Other(가스기술): "국내에서 발생한 대형 도시가스 사고 중 대구 도시가스 폭발사고의 주원인은?"
  - Other × Regional(농학): "우리나라에서 배추의 F1품종의 종자생산이 남해안과 그 인근 도서 지방에 집중되어 있는 이유를 설명한 것 중 옳지 않은 것은?"
  - 그림 1 바로 아래 본문(PDF p.2)은 GPT-4가 "localized knowledge"(지역화된 지식)가 필요한 영역에서 약하다고 쓴다. — [Son et al., 2024](https://arxiv.org/abs/2402.11548)
- [그림 판독] KoSimpleQA 주제 분포(그림 2, PDF p.4, 300dpi로 확대해 읽음): Science & Technology 19.2%, Politics 16.5%, Art 13.1%, Other 10.6%, Geography 9.9%, Music 8.3%, Sports 8.2%, TV Show 7.1%, History 3.9%, Games 3.1%. — [Ko et al., 2025](https://arxiv.org/abs/2510.18368)
- [데이터 확인] KoSimpleQA 938개 파일에서 "science & technology"는 180개다(180/938 = 19.2%, 그림과 맞음). 1,000개 파일에서는 196개다. 938개 파일의 180개 가운데 96개는 질문 문장에 "최초·처음·첫"이 들어 있다. 111개는 "국내·대한민국·한국·우리나라·국산·한반도"가 들어 있다. 둘 중 하나라도 들어 있는 것은 128개다(단순 문자열 검색으로 셈). 예는 다음과 같다. "대한민국 최초의 통신위성은 무엇인가요?"(무궁화 1호). "누리호 처음 발사 성공 년도는?"(2022년). "대한민국 최초의 달탐사선은 무엇인가요?"(다누리). "1999년 한국과학기술연구원에서 선보인 '반인반마'의 로봇은?"(센토). "대한민국 최초의 화학박사의 이름은?"(이태규). "국산 1호 신약은?"(선플라). "1983년 11월 세계 3번째로 64K D램을 개발한 한국 기업은?"(삼성전자). 근거 링크는 뉴스, 기업 사이트, 네이버 지식백과, 한국어 위키백과가 섞여 있다. 한국어 위키백과를 근거로 든 문항은 180개 중 45개다. — [naver-ai/KoSimpleQA](https://github.com/naver-ai/KoSimpleQA)
- [직접 확인] 위 45개 문항이 근거로 든 한국어 위키백과 글은 서로 다른 제목 43개다. 2026-10-21 기준 영어 언어 간 링크를 조회했다. 33개는 영어판이 있다. 10개는 없다(LG전자의 역사, V3, 누리호 3차 발사, 대한민국에서 개발된 신약, 두산모빌리티이노베이션, 아이네트, 전자신문, 코시크, 크레마 (전자제품), 한국반도체). 글 단위 확인이다. 영어판이 있는 글에 그 질문의 답이 있는지는 보지 않았다. — [naver-ai/KoSimpleQA](https://github.com/naver-ai/KoSimpleQA), [Wikipedia API](https://ko.wikipedia.org/w/api.php)
- [원문 확인] BertaQA의 Science and Technology는 local 292개, global 296개다(표, PDF p.16). local의 예는 "Which town in Biscay is associated with dynamite?"(비스카야에서 다이너마이트와 관련된 마을은?)다(표 1, PDF p.2). — [Etxaniz et al., 2024](https://arxiv.org/abs/2406.07302)
- [원문 확인] CaLMQA의 주제 범주에는 Technology("Questions about the technology, technological advancements, uses of technology and digital innovation.")와 Health and Wellness가 있다(표 12, PDF p.22). 대부분 언어에서 가장 많은 범주는 종교·관습, 통치·사회, 역사 가운데 하나다. 영어와 한국어는 예외다(PDF p.18: "(the exceptions being English and Korean)"). 한국어에서 가장 많은 범주가 무엇인지는 확인하지 못했다. — [Arora et al., 2024](https://arxiv.org/abs/2406.17761)

### Inferences

- 기존 벤치마크에서 "한국에 고유한 STEM 사실"은 다섯 부류로 나타난다. 한국 법규·기준, 한반도 지리·생태·기후, 국내 기관·기업·국가 사업, 국내 "최초" 기록, 국내 사고·사례다(KMMLU 그림 1, KoSimpleQA, ECLeKTic 지침의 "독일 생물학자" 예). 반대로 일반 원리, 자연 현상, 보편 수치는 ECLeKTic 지침이 빼라고 한 바로 그 내용이다. Global-MMLU와 INCLUDE도 이것을 "지역과 무관"으로 분류한다.
- 과제의 상황(STEM 주제에서 한국어 글은 짧고 숫자 대부분이 영어 글에도 있음)은 이 관찰과 맞는다. 일반 STEM 내용은 언어 사이에서 겹친다. 한국어 쪽에만 있는 사실을 얻으려면 한국 쪽 사례, 기관, 규정, 역사로 주제를 옮겨야 할 가능성이 크다. 다만 "한국에 관한 것"이 "한국어에만 있는 것"은 아니다. KoSimpleQA의 STEM 근거 글 43개 중 33개가 영어판이 있다. 그러므로 어느 쪽으로 가든 코퍼스 안에서 사실 단위 확인이 따로 필요하다.
- 반대 방향(영어 문서에만 있는 사실)은 이번 조사의 벤치마크가 거의 다루지 않는다. 앞 조사의 XOR-TyDi 사례(일본어판에 없는 Ron Paul의 학위 정보)처럼, 짧은 한국어 STEM 글에 없는 영어 글의 세부 사실이 그 후보가 될 수 있다. 이것은 이번 노트의 근거로 확인한 내용이 아니라 추론이다.

### Gaps

- KoLasSimpleQA 한국어 언어 고유 84개에 STEM이 얼마나 있는지 알 수 없다(데이터 미공개, 주제 분포 보고 없음).
- MultiLoKo 한국어 질문의 주제 분포는 세지 않았다. 질문 문장은 공개 조건 때문에 옮기지 않았다.
- INCLUDE 한국어 전체 1,781개의 과목 구성은 모른다. 공개된 것은 BASE 부분뿐이다.
- ECLeKTic 한국어 Science and Technology 1개가 어느 문항인지는 알 수 없다(데이터에 영역 표시 없음).
- CaLMQA 한국어에서 가장 많은 주제 범주는 확인하지 못했다.
- 스웨덴 벤치마크의 표본 수는 초록이 1,293개인데 하위 집합 합(1,190 + 102)은 1,292다[원문 내 불일치]. 원인을 확인하지 않았다.
