# 기존 다국어·교차 언어 QA/검색/RAG 벤치마크의 교차 언어 질문 정의와 구성 방식

조사일: 2026-10-12. 표기 규칙은 다음과 같다.

- **[원문 확인]**: arXiv 또는 ACL Anthology의 논문 PDF를 내려받아 본문에서 직접 확인한 내용이다. 짧은 원문 인용과 절 이름을 붙였다. 절 번호를 기록하지 못한 곳은 "(절 미기록)"이라고 적었다.
- **[2차 출처만]**: 검색 결과 요약에서만 본 내용이다. 원문은 확인하지 않았다.
- 게재 학회는 CLIRMatrix(EMNLP 2020 프로시딩 머리글을 봄) 말고는 따로 확인하지 않았다. 나머지는 모두 arXiv 판을 기준으로 적었다.
- 저자와 연도는 내려받은 PDF의 제목부와 arXiv 날짜 표기에서 확인했다. 과제에서 준 인용 연도와 arXiv 날짜가 다른 경우가 있다. MIRACL은 arXiv v1이 2022-10-18이고(Zhang, Thakur, Ogundepo, Kamalloo, Alfonso-Hermelo, Li, Liu, Rezagholizadeh, Lin), NoMIRACL은 arXiv 번호가 2312(2023년 12월)이며 v3이 2024-11-10이다(Thakur, Bonifacio, Zhang, Ogundepo, Kamalloo, Alfonso-Hermelo, Li, Liu, Chen, Rezagholizadeh, Lin). 본문에서는 과제 표기에 맞춰 각각 2023, 2024로 적었다. CORA는 Asai, Yu, Kasai, Hajishirzi(arXiv v2 2021-10-28), MIRAGE-Bench는 Thakur, Kazi, Luo, Lin, Ahmad(arXiv v2 2025-03-29), XBCP는 Lu, Zeng, Qi, Yu, Zhao, Yang, Yanaka, Yokoya, Xuan(arXiv v2 2026-06-17)이다.
- 2024년 이후 논문 가운데 Faux Polyglot, Futurepedia, Park & Lee, Chirkova et al., MIRAGE-Bench, BordIRlines, XRAG, XBCP는 arXiv 프리프린트로 취급한다.

---

## 1. XOR-TyDi QA(XOR-Retrieve, XOR-EnglishSpan, XOR-Full)의 질문 선정 방식과 "같은 언어 Wikipedia로 답할 수 없는 질문"의 실제 의미

### Takeaway

XOR-TyDi QA의 교차 언어 질문은 TyDi QA에서 "답 없음"으로 표시된 질문을 가져온 것이다. 이 "답 없음"은 같은 언어 Wikipedia 전체를 뒤진 결과가 아니다. Google 검색 1위 문서 하나에서 주석자가 답 문단을 고르지 못했다는 뜻이다. XOR-Retrieve와 XOR-EnglishSpan은 검색 대상을 영어 Wikipedia로만 한정해 교차 언어 조건을 만든다. XOR-Full은 질문 언어 Wikipedia와 영어 Wikipedia를 둘 다 열어 두고 어느 쪽에서 답을 찾아도 인정한다.

### Cited Findings

대상 논문: "XOR QA: Cross-lingual Open-Retrieval Question Answering", Akari Asai, Jungo Kasai, Jonathan H. Clark, Kenton Lee, Eunsol Choi, Hannaneh Hajishirzi, 2021 (arXiv:2010.11856v3).

**질문 선정**

- [원문 확인] 질문은 TyDi QA에서 같은 언어 답을 찾지 못한 질문이다. Abstract: "We construct a large-scale dataset built on 40K information-seeking questions across 7 diverse non-English languages that TYDI QA could not find same-language answers for." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] "답할 수 없음"의 정의는 주석자가 문서 안에서 답 문단을 고르지 못한 것이다. §2.1.1 Question Selection: "A question is unanswerable in TYDI QA if an annotator cannot select a passage answer (a paragraph in the article that contains an answer). We randomly sample 5,000 questions without any passage answer annotations (unanswerable questions) from the TYDI QA training data" — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] TyDi QA에서 주석자가 본 문서는 질문마다 하나뿐이다. TyDi QA 데이터 수집 절차의 "Article retrieval" 단계(절 미기록): "A Wikipedia article is then paired with each question by performing a Google search on the question text, restricted to the Wikipedia domain for each language, and selecting the top-ranked result." — [Clark et al., 2020, "TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages"](https://arxiv.org/abs/2003.05002)
- [원문 확인] 평가용(test) 질문은 학습 데이터가 아니라 TyDi QA의 개발(dev) 세트에서 온다. §2.1.1: "We randomly sample 5,000 questions without any passage answer annotations (unanswerable questions) from the TYDI QA training data, and split them into training (4,500) and development (500) sets. We use the development data from TYDI QA as our test data, since the TYDI QA's original test data is not publicly available." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- 위 두 인용을 합치면, XOR의 "같은 언어로 답할 수 없음"은 같은 언어 Wikipedia의 Google 1위 문서 하나에서 주석자가 답 문단을 찾지 못했다는 조작적 정의다. 해당 언어 Wikipedia 전체에 답이 없다는 것을 검증한 것은 아니다. — [Asai et al., 2021](https://arxiv.org/abs/2010.11856); [Clark et al., 2020](https://arxiv.org/abs/2003.05002)
- [원문 확인] XOR 논문도 이 절차가 답 존재 여부를 과소 추정한다고 적는다. Appendix A(Appendix B 바로 앞 문단): "questions can be labeled as unanswerable simply because of annotation errors. ... In this procedure, the answer coverage is underestimated when the search engine fails to retrieve relevant articles (retrieval errors) or the annotator overlooks answer content from the selected articles (answer annotation errors, Asai and Choi, 2020)." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 후속 논문은 이 조건을 원 절차보다 강하게 요약한다. MIA 2022 §3 Shared Task Data: "Asai et al. (2021a) collect answers for questions in TyDi QA that are unanswerable using the same-language Wikipedia. ... some questions can be answered based on the target language's Wikipedia (monolingual) while others require evidence only presented in English Wikipedia (cross-lingual)." 여기서 "only presented in English Wikipedia"는 XOR의 실제 절차(1위 문서 하나 확인)가 보장하는 것보다 강한 표현이다. — [Asai et al., 2022, "MIA 2022 Shared Task: Evaluating Cross-lingual Open-Retrieval Question Answering for 16 Diverse Languages"](https://arxiv.org/abs/2207.00758)

**주석 절차**

- [원문 확인] 4단계로 진행한다. §2.1: "1) collection of questions from TYDI QA without a same-language answer which require cross-lingual reference to answer (§2.1.1); 2) question translation from a target language to the pivot language of English where the missing information may exist (§2.1.2); 3) answer retrieval in the pivot language given a set of candidate documents (§2.1.3); 4) answer verification and translation from the pivot language back to the original language (§2.1.4)." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 영어를 축 언어로 삼은 이유. §2: "We focus on cross-lingual retrieval from English Wikipedia because in our preliminary investigation we were able to find answers to a majority of the questions from resource-rich English Wikipedia, and native speakers with much annotation experience were readily available via crowdsourcing in English." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 번역된 질문은 주석에만 쓰고 모델에는 주지 않는다. §2.1.2: "they are not provided to models during evaluation." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 교차 언어 데이터와 같은 언어 데이터를 섞는다. §2.1.4: "we mix the annotated cross-lingual data with the same-language data from TYDI QA to reflect the actual question distributions from native speakers (in-language data)." Table 2 설명: "Cross-lingual data comes from our reannotated questions that did not originally have same-language answers in TYDI QA. In-language data are taken directly from answerable questions in TYDI QA." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)

**세 과제의 문서 풀과 채점**

- [원문 확인] XOR-Retrieve는 영어 Wikipedia만 검색 대상이다. §3.1: "Given a question in Li and English Wikipedia Weng, the task is to retrieve English paragraphs for the question." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR-Retrieve는 정답 문단 ID가 아니라 답 문자열 포함 여부로 채점한다. §3.1 Evaluation: "we measure the recall by computing the fraction of the questions for which the minimal answer is contained in the top n tokens selected. We evaluate with n = 2k, 5k". 답 문자열이 들어 있는 문단이면 주석된 문단이 아니어도 맞은 것으로 센다. — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR-EnglishSpan도 영어 Wikipedia만 쓴다. §3.2: "Given a question in Li and English Wikipedia Weng, a system retrieves paragraphs from Weng and extracts an answer." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR-Full은 두 언어 Wikipedia를 모두 쓰고, 답이 어느 언어에 있는지 시스템에 알려 주지 않는다. §3.3: "Given a question in target language Li and Wikipedia in both English and Li (Weng and Wi), a system is required to generate an answer in Li. In this task, a system does not know a priori in which language we can find information that the user is seeking. Note that the XOR-FULL evaluation data includes both cross-lingual and in-language data, while XOR-RETRIEVE and XOR-ENGLISHSPAN only use cross-lingual data during evaluation." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR-Full은 두 검색 경로를 다 인정한다. §2.2 Qualitative examples: "In the last question of Table 3, on the other hand, only the Wikipedia of the target language can provide the answer. XOR QA allows for both retrieval paths." §3.3 Baselines: "evidence paragraphs can be found both in the target language and English". — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR-Full은 근거 문단이 아니라 답 문자열로 채점한다. §3.3 Evaluation: "Some answers in XOR-FULL are translated from English so the same spans may not exist in the target language's Wikipedia. For this reason, we use token-level BLEU scores ... in addition to F1 and EM." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 답이 없는 질문은 평가에서 뺀다. §4 Experiments 설정 문단(§4.2 바로 앞): "We only evaluate questions having answers and do not give credit to predicting 'no answers' as in prior open-retrieval work". — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)

**한국어 수치**

- [원문 확인] Table 1(짧은 답이 있는 질문 비율, TyDi QA dev 기준). 한국어는 TyDi QA 29%에서 XOR-TyDi QA 68%로, 39%p 늘었다. 전체는 50%에서 72%로 늘었다. 본문: "cross-lingual retrieval significantly increases the answer coverage in all languages by up to 40% (Bengali)". — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] Table 2(답이 있는 데이터 크기). 한국어 교차 언어 데이터는 train 2,469 / dev 299 / test 646이고, 같은 언어 데이터는 train 1,856 / dev 72 / test 505이다. — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] Table 3의 한국어 예시는 "1993년 프랑스 총리는 누구인가요?"에 해당하는 질문이다. 본문: "The first question is unanswerable in Korean Wikipedia, but there is a clear description about who was the prime minister of France at the time in English Wikipedia." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)

**"없음" 표시가 얼마나 약한지 보여 주는 후속 증거**

- [원문 확인] CORA 논문의 사람 분석(§5 바로 앞의 "Human analysis on unanswerable questions" 문단): "MKQA includes questions that are marked as unanswerable by native English speakers given English knowledge sources. We sample 400 unanswerable Japanese questions whose top one retrieved passage is from a non-English Wikipedia article. Among these, 329 unanswerable questions are underspecified ... For 17 out of the 71 remaining questions, the answers predicted by CORA are correct." — [Asai et al., 2021, "One Question Answering Model for Many Languages with Cross-lingual Dense Passage Retrieval"](https://arxiv.org/abs/2107.11976)
- [원문 확인] 같은 논문 각주 10: "it is difficult to prove an answer does not exist in the millions of multilingual documents even if the annotation says so." — [Asai et al., 2021 (CORA)](https://arxiv.org/abs/2107.11976)

### Inferences

- "XOR-TyDi의 교차 언어 질문은 같은 언어 Wikipedia로 답할 수 없는 질문이다"라는 말은 절반만 맞다. 선정 기준은 1위 문서 하나와 주석자 판단이다. 저자도 과소 추정을 인정한다. 엄밀한 "근거가 영어에만 있음"이 아니라 "TyDi 절차에서 같은 언어 답을 못 찾음"으로 읽어야 한다.
- XOR은 교차 언어 조건을 두 가지 방법으로 만든다. Retrieve와 EnglishSpan은 문서 풀을 다른 언어로만 한정한다. Full은 풀을 섞어 두고 질문별로 교차 언어 또는 같은 언어 딱지만 붙인다. 두 방법 모두 "질문 언어 문서에 답이 없음"을 전수 검증하지 않는다.
- XOR-Full의 같은 언어 질문(TyDi에서 답이 있던 질문)은 영어 Wikipedia에 같은 답이 있는지 확인하지 않았다. 따라서 "두 언어에 다 있는 사실"은 XOR-Full 안에 딱지 없이 섞여 있을 수 있다. 채점이 답 문자열 기준이라 어느 언어 근거를 썼는지는 구분하지 않는다.
- 문서가 20~30개인 평가셋은 Wikipedia 규모와 달리 "질문 언어 문서에 이 사실이 없다"를 사람이 전부 읽어 확인할 수 있다. XOR이 하지 못한 검증이 소규모에서는 가능하다.

### Gaps

- XOR-TyDi의 교차 언어 질문 가운데 실제로 같은 언어 Wikipedia 다른 문서에 답이 있는 비율은 논문에서 찾지 못했다. 그런 수치를 낸 후속 분석도 이번에 확인하지 못했다.
- XOR의 test 질문은 TyDi QA dev 세트에서 왔다. dev 세트 질문에 대해 "같은 언어 답 없음"을 어떤 규칙으로 정했는지(주석자가 여럿일 때의 처리 등)는 추출한 본문에서 확인하지 못했다. 학습 데이터에 대한 정의("without any passage answer annotations")가 그대로 적용되는지 불확실하다.
- XOR 공식 페이지(https://nlp.cs.washington.edu/xorqa/)와 GitHub README는 열어 보지 않았다. 위 내용은 모두 arXiv v3 본문 기준이다.
- MIA 2022 초록의 "potential answer overlaps in existing datasets may overestimate models' performance"가 무엇의 겹침(학습·평가 답 겹침인지, 언어 간 겹침인지)을 가리키는지 해당 본문을 읽지 않아 확인하지 못했다.

---

## 2. 벤치마크별 과제 유형(단일 언어·교차 언어·다국어 혼합)과, 언어 간 병렬·중복 내용이 있을 때 관련 문서를 정하는 방식

### Takeaway

조사한 벤치마크는 세 부류로 나뉜다. 첫째는 질문과 문서가 같은 언어인 단일 언어 벤치마크다(TyDi QA, Mr.TyDi, MIRACL, NoMIRACL, MIRAGE-Bench, XQuAD). 둘째는 문서 풀을 다른 언어로 한정해 교차 언어 조건을 만드는 벤치마크다(XOR-Retrieve, NeuCLIR CLIR, CLIRMatrix BI-139, XRAG 단일 언어 검색 설정, XBCP 교차 언어 설정). 셋째는 여러 언어 문서를 한 풀에 섞는 벤치마크다(XOR-Full, LAReQA, CLIRMatrix MULTI-8, NeuCLIR MLIR, BordIRlines, Futurepedia, XRAG 다국어 설정). 같은 내용이 여러 언어에 있을 때는 "모든 언어판을 다 관련 문서로 센다"가 명시적으로 확인된 주된 방식이다. "질문 언어 문서에 답이 없음"을 검증으로 보장한 벤치마크는 찾지 못했다. 배타성을 둔 곳은 모두 풀을 그렇게 구성해서 얻었다.

### Cited Findings

**단일 언어(질문 언어와 문서 언어가 같음)**

- [원문 확인] TyDi QA: 질문은 번역 없이 각 언어로 직접 쓰고, 같은 언어 Wikipedia 문서 하나와 짝짓는다. Abstract: "questions are written by people who want to know the answer, but don't know the answer yet, and the data is collected directly in each language without the use of translation." — [Clark et al., 2020](https://arxiv.org/abs/2003.05002)
- [원문 확인] XQuAD: SQuAD v1.1의 문단과 질문을 통째로 번역한 병렬 데이터다. 질문과 문단을 같은 언어로 짝지어 쓰는 추출형 QA다. §(XQuAD 소개, 절 미기록): "XQuAD consists of a subset of 240 paragraphs and 1190 question-answer pairs from the development set of SQuAD v1.1 together with their translations into ten languages: Spanish, German, Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, and Hindi. Both the context paragraphs and the questions are translated by professional human translators". — [Artetxe, Ruder, Yogatama, 2020, "On the Cross-lingual Transferability of Monolingual Representations"](https://arxiv.org/abs/1910.11856)
- [원문 확인] XOR 논문 Table 4는 TyDi QA와 XQuAD를 "Cross-lingual" 아님으로, MLQA를 "Cross-lingual"로 분류한다. 본문 §2.2: "our dataset requires cross-lingual retrieval unlike other multilingual datasets such as TYDI QA or XQuAD (Artetxe et al., 2020), which focus on same-language QA." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] Mr.TyDi: TyDi QA를 검색 과제로 바꾼 단일 언어 검색 벤치마크다. Abstract: "a multi-lingual benchmark dataset for mono-lingual retrieval in eleven typologically diverse languages". §1: "mono-lingual retrieval in non-English languages (e.g., Bengali queries against Bengali documents) rather than cross-lingual retrieval, where documents and queries are in different languages (e.g., English queries against Arabic documents)." — [Zhang, Ma, Shi, Lin, 2021, "Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval"](https://arxiv.org/abs/2108.08787)
- [원문 확인] MIRACL: 18개 언어 단일 언어 검색. Abstract: "Our dataset is designed to support the creation and evaluation of models for monolingual retrieval, where the queries and the corpora are in the same language." 과제 정의 절(절 미기록): "a query q is a well-formed natural language question in some language Ln (one of 18) and the documents draw from a snapshot of Wikipedia in the same language Cn". — [Zhang et al., 2023, "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages"](https://arxiv.org/abs/2210.09984)
- [원문 확인] MIRACL은 관련 문단을 하나도 못 찾은 질문을 버렸고, 그것이 "없음"의 증명은 아니라고 적는다(§3 끝부분, 절 미기록): "we aimed to have at least one relevant passage per query, and therefore these queries were discarded from the final dataset. ... just because no relevant passage was found in the top-10 candidates presented to the annotator, it is not necessarily the case that no relevant passage exists in the corpus. ... Short of exhaustively evaluating the corpus (obviously impractical), we cannot conclude with certainty that no relevant passage exists." — [Zhang et al., 2023](https://arxiv.org/abs/2210.09984)
- [원문 확인] NoMIRACL: 18개 언어. 질문과 문단이 같은 언어인 RAG 견고성 평가다. Abstract: "NoMIRACL includes both a non-relevant and a relevant subset. Queries in the non-relevant subset contain passages judged as non-relevant, whereas queries in the relevant subset include at least a single judged relevant passage." 프롬프트 절(절 미기록): "a list of contexts along with the input query, both in the same language." — [Thakur et al., 2024, "'Knowing When You Don't Know': A Multilingual Relevance Assessment Dataset for Robust Retrieval-Augmented Generation"](https://arxiv.org/abs/2312.11361)
- [원문 확인, 프리프린트] MIRAGE-Bench: MIRACL에서 만든 18개 언어 RAG 생성 평가다. §3.1: "MIRACL introduced in Zhang et al. (2023) is a monolingual retrieval dataset". (절 미기록): "MIRAGE-BENCH data is sourced from MIRACL (Zhang et al., 2023), a multilingual retrieval dataset containing human-generated queries and human-labeled relevance judgments for Wikipedia passages." — [Thakur et al., 2024, "MIRAGE-Bench: Automatic Multilingual Benchmark Arena for Retrieval-Augmented Generation Systems"](https://arxiv.org/abs/2410.13716)

**병렬 번역 데이터(같은 내용이 모든 언어에 있도록 만든 것)**

- [원문 확인] MLQA: Wikipedia에서 자연적으로 병렬인 문장을 찾아 만든 7개 언어 병렬 추출형 QA다. §1: "MLQA is a multi-way parallel extractive QA evaluation benchmark in seven languages: English, Arabic, German, Vietnamese, Spanish, Simplified Chinese and Hindi. To construct MLQA, we first automatically identify sentences from Wikipedia articles which have the same or similar meaning in multiple languages." — [Lewis, Oğuz, Rinott, Riedel, Schwenk, 2020, "MLQA: Evaluating Cross-lingual Extractive Question Answering"](https://arxiv.org/abs/1910.07475)
- [원문 확인] MLQA의 교차 언어 과제(G-XLT)는 병렬 데이터에서 질문 언어만 바꿔 끼워 만든다. 문단은 시스템에 주어지며 검색은 없다. §1: "generalised cross-lingual transfer (G-XLT) requires models to answer questions where the question and context language is different, e.g. questions in Hindi and contexts in Arabic, a setting possible because MLQA is highly parallel." 과제 정의 절(절 미기록): "This evaluation setup is possible because MLQA is highly parallel, allowing us to swap qz for qy for parallel instances without changing the question's meaning." — [Lewis et al., 2020](https://arxiv.org/abs/1910.07475)
- [원문 확인] MKQA: Natural Questions 1만 개를 25개 언어로 사람이 번역했다. 답은 문서와 무관하게 Wikidata 개체에 연결했다. §1: "we replace NQ's passage embedded answer spans with high-quality, language- and retrieval-independent answer annotations, linked directly against Wikidata entities". "Parallel Questions" 문단: "Our evaluation set is fully aligned, or 'parallel', across all available languages, meaning the same examples exist in all languages." — [Longpre, Lu, Daiber, 2021, "MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering"](https://arxiv.org/abs/2007.15207)
- [원문 확인] MKQA는 지역에 따라 답이 달라지지 않는 질문을 일부러 고른다. 정보 비대칭을 이용하는 설계와 반대 방향이다. §1: "We confirm that a large majority of these queries are geographically invariant, meaning that their answer is not culturally or geographically dependent (we found that less than 4% of answers are rendered incorrect by geographical and cultural context". "Parallel Questions" 문단: "we reserve our assessment to geographically invariant queries for the purpose of more fair comparison between methods." — [Longpre et al., 2021](https://arxiv.org/abs/2007.15207)
- [원문 확인, 프리프린트] MKQA의 지식은 주로 영어 Wikipedia에 기반한다는 후속 논문의 설명. Park & Lee §3.1: "This dataset is therefore parallel between languages and grounds knowledge primarily in English Wikipedia." — [Park & Lee, 2025, "Investigating Language Preference of Multilingual RAG Systems"](https://arxiv.org/abs/2502.11175)

**여러 언어가 섞인 풀에서 병렬 답을 전부 정답으로 세는 방식**

- [원문 확인] LAReQA(XQuAD-R, MLQA-R): 질문 하나에 대해 모든 언어판 답 문장이 관련 문서다. §3.1: "Our goal is to construct a QA retrieval task over a large multilingual pool where many or most of the target answers are found in a different language than the question itself. ... These sets are designed so as to include parallel QA pairs across languages, allowing us to match questions with answers from different languages." §3.2 Evaluation: "This metric is suitable when there are multiple relevant results for a given query. In our case, an XQuAD-R question will have 11 relevant answers". — [Roy et al., 2020, "LAReQA: Language-agnostic answer retrieval from a multilingual pool"](https://arxiv.org/abs/2004.05484)
- [원문 확인] LAReQA는 "같은 언어의 틀린 답을 다른 언어의 맞는 답보다 선호하는" 현상을 재려고 설계했다. Figure 1 설명: "A weakly aligned multilingual embedding space enables zero-shot transfer between languages, but incorrect answers in the same language are preferred over correct answers in a different language." — [Roy et al., 2020](https://arxiv.org/abs/2004.05484)
- [원문 확인] CLIRMatrix: 단일 언어 검색기로 관련도 딱지를 만든 뒤 Wikidata 링크로 다른 언어판 문서에 전파한다. §1: "The core idea is to synthesize relevance labels via an existing monolingual IR system, then propagate the labels via Wikidata links that connect documents in different languages." Figure 2 설명: "Wikidata links are exploited to propagate the label to the corresponding Chinese documents, which are assumed to be topically similar." — [Sun & Duh, 2020, "CLIRMatrix: A massively large collection of bilingual and multilingual datasets for Cross-Lingual Information Retrieval"](https://aclanthology.org/2020.emnlp-main.340/)
- [원문 확인] CLIRMatrix는 두 부분으로 나뉜다. Abstract: "(1) BI-139, a bilingual dataset of queries in one language matched with relevant documents in another language for 139×138=19,182 language pairs, and (2) MULTI-8, a multilingual dataset of queries and documents jointly aligned in 8 different languages." §1: "MULTI-8 ... Arabic (ar), German (de), English (en), Spanish (es), French (fr), Japanese (ja), Russian (ru), Chinese (zh). Each query will have relevant documents in the other 7 languages." — [Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)
- [원문 확인] CLIRMatrix는 언어 간 링크가 빠져 관련 문서를 놓칠 수 있다고 인정한다. 각주 6: "We acknowledge that there are potentially missing interlanguage links in Wikidata. This implies that our method may miss the labeling of some relevant documents." — [Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)

**TREC NeuCLIR(뉴스 문서, 영어 주제)**

- [원문 확인] NeuCLIR 2022의 세 과제. §2 Task Definition: "We explore three tasks in the TREC 2022 NeuCLIR track: ad hoc CLIR, reranking CLIR, and monolingual. All three tasks use the same document collections, topics, and relevance assessments. Monolingual runs use topics manually translated into the language of the documents; ad hoc and reranking runs use the original English topics." — [Lawrie et al., 2023, "Overview of the TREC 2022 NeuCLIR Track"](https://arxiv.org/abs/2304.12367)
- [원문 확인] NeuCLIR 2023의 CLIR과 MLIR. §2.1.1: "Systems receive a document collection in Chinese, Persian, or Russian, and a set of topics written in English." §2.1.4: "In NeuCLIR 2023, a new multilingual retrieval task was added. This task is identical to the CLIR task described in §2.1.1, except systems must search all three document collections and produce a single unified ranked list." — [Lawrie et al., 2024, "Overview of the TREC 2023 NeuCLIR Track"](https://arxiv.org/abs/2404.08071)

**2024~2026 다국어 RAG 벤치마크**

- [원문 확인, 프리프린트] BordIRlines: 영토 분쟁 질문 720개(분쟁 지역 251곳), 49개 언어. 질문마다 검색 방식(IR mode)별 문서 집합을 붙인다. §3.1: "BORDIRLINES is a multilingual dataset covering 49 languages. It builds on top of the BORDERLINES dataset (Li et al., 2024b), which consists of 720 queries for 251 disputed territories. ... associating each query with several sets of retrieved Wikipedia documents (1 set per IR mode). Each set consists of the 10 most-relevant documents, as scored by IR systems." — [Li et al., 2024/2025, "Multilingual Retrieval Augmented Generation for Culturally-Sensitive Tasks: A Benchmark for Cross-lingual Robustness"](https://arxiv.org/abs/2410.01171)
- [원문 확인, 프리프린트] BordIRlines의 검색 방식 표(절 미기록, 표가 평문으로 풀려 있어 방식 이름과 설명을 나열 순서대로 짝지음): qlang은 "monolingual IR in query lang", qlang+en은 "multilingual IR in query lang and en", rel_langs는 "multilingual IR in all relevant languages", en_only는 "cross-lingual IR in en", swap_docs는 "cross-lingual IR in non-query lang"이다. Figure에는 no_ir를 더해 6개 방식으로 적혀 있다. — [Li et al., 2024/2025](https://arxiv.org/abs/2410.01171)
- [원문 확인, 프리프린트] BordIRlines의 관련도 판정은 내용 기준이고 언어와 무관하다. (절 미기록): "each query-document pair is annotated for two content factors: relevance – whether it directly discusses the status of a territory – and territorial viewpoint – which claimant it supports (or Neutral or N/A). ... First, we performed a small-scale human annotation effort, on 5 languages: English, Chinese, Hindi, Spanish, and Korean. Second, informed by the human effort, we designed an LLM-as-annotator approach to annotate the full dataset." 사람과 LLM의 관련도 일치는 "76% F1 agreement rate"이다. — [Li et al., 2024/2025](https://arxiv.org/abs/2410.01171)
- [원문 확인, 프리프린트] Futurepedia: 8개 언어 병렬 문서 197개와 QA. §2.1: "we collect Wikipedia documents created from January 2018 to April 2024 in eight languages: English (en), French (fr), Spanish (es), Portuguese (pt), Chinese (zh), Japanese (ja), Korean (ko), and Arabic (ar). ... Ultimately, we obtain 197 parallel documents and corresponding QA pairs in eight languages." 개체를 허구로 바꿔 모델의 사전 지식을 막는다("translate the fictional entities into eight languages"). — [Wu et al., 2024, "Not All Languages are Equal: Insights into Multilingual Retrieval-Augmented Generation"](https://arxiv.org/abs/2410.21970)
- [원문 확인, 프리프린트] Futurepedia의 세 과제는 같은 병렬 문서를 어떻게 배치하느냐로 나뉜다. §2.2: "Monolingual Knowledge Extraction: This task requires the RALMs to extract answers from documents and resolve questions within the same language"; "Cross-lingual Knowledge Transfer: ... we challenge RALMs with documents and QA pairs written in different languages within this evaluation task. This task imitates the real-world scenario where there are no high-quality documents in the query language". 세 번째 과제 Multilingual Knowledge Selection은 그림에서 여러 언어 문서(일부는 틀린 내용)를 함께 주는 형태로 확인했다. 본문 정의 문장은 추출하지 못했다. — [Wu et al., 2024](https://arxiv.org/abs/2410.21970)
- [원문 확인, 프리프린트] XRAG: 교차 언어 RAG를 "질문 언어와 다른 언어 문서가 최소 하나 있는 것"으로 정의한다. §3: "given a question q, the LLM is prompted to generate an answer ã in the same language as the question by referring to a collection of m articles D ... that contains articles in a language different than the question: ... Language(q) = Language(ã); ∃ di ∈ D, Language(di) ≠ Language(q)". — [Liu et al., 2025, "XRAG: Cross-lingual Retrieval-Augmented Generation"](https://arxiv.org/abs/2505.10089)
- [원문 확인, 프리프린트] XRAG의 두 설정. 단일 언어 검색 설정은 근거와 방해 문서가 모두 영어다("Language(q) ∈ {de, es, zh, ar}; Language(D+) = Language(D−) = en"). 다국어 검색 설정은 근거 문서 둘이 영어와 질문 언어에 걸쳐 있다("Language(D+) = {en, Language(q)}; Language(D−) = {en, Language(q)}"). §3: "In a multilingual retrieval setting, LLMs use articles in both the question language and other languages to answer a question. This corresponds to a cross-lingual RAG scenario where documents in a resource-rich language provide additional information for LLMs to answer questions in a second language." — [Liu et al., 2025](https://arxiv.org/abs/2505.10089)
- [원문 확인, 프리프린트] XRAG의 근거 문서 둘은 서로의 복사본이 아니다. 각각 답의 일부만 담는다. §3: "The supporting articles each contribute partial information needed to answer the question, and only together do they provide a complete answer; in contrast, the distracting articles are topically related but cannot answer the question." 구성은 같은 사건을 다룬 다른 언어 뉴스 기사를 짝지어 한다(§4.1: "We then group articles in different languages about the same event to form related article pairs"). 방해 문서는 한 질문에 6개다(Table 4 설명). — [Liu et al., 2025](https://arxiv.org/abs/2505.10089)
- [원문 확인, 프리프린트] Faux Polyglot: 허구 주제의 문서를 만들어 5개 언어(en, hi, de, ar, zh)로 기계 번역해 병렬로 만든 뒤, 어느 언어 문서를 선호하는지 본다. Figure 2 설명: "core facts were crafted manually, then expanded using GPT-4-turbo ... We then translated these documents into target languages using Google Translate". 연구 질문 RQ3: "How do multilingual LLM's information preference change if all relevant documents are in Foreign Languages?" — [Sharma, Murray, Xiao, 2024, "Faux Polyglot: A Study on Information Disparity in Multilingual Large Language Models"](https://arxiv.org/abs/2407.05502)
- [원문 확인, 프리프린트] Faux Polyglot의 결과. Abstract: "We found that LLMs displayed systemic bias towards information in the same language as the query language in both document retrieval and answer generation. Furthermore, in scenarios where no information is in the language of the query, LLMs prefer documents in high-resource languages during generation". — [Sharma et al., 2024](https://arxiv.org/abs/2407.05502)
- [원문 확인, 프리프린트] XBCP: 영어 질문과 답은 그대로 두고 근거 문서만 번역해 언어를 바꾼다. §3.1: "questions remain in English, final answers are evaluated in English, and only the evidence documents vary in languages." "In the cross-lingual setting, each query is assigned to one evidence language, so all supporting documents for that query appear in the same language (English serves as an untranslated reference). ... In the multilingual setting, 5,040 evidence document instances are randomly but equally assigned to 12 languages, making 420 evidence docs per language". — [Lu et al., 2026, "Beyond Monolingual Deep Research: Evaluating Agents and Retrievers with Cross-Lingual BrowseComp-Plus"](https://arxiv.org/abs/2606.15345)
- [원문 확인, 프리프린트] XBCP의 결과. Abstract: "Results reveal substantial degradation when evidence is translated. ... Notably, accuracy remains lower even when all gold evidence is supplied directly." — [Lu et al., 2026](https://arxiv.org/abs/2606.15345)
- [원문 확인, 프리프린트] Chirkova et al.: MKQA와 XOR-TyDi QA로 검색 대상 언어를 바꿔 가며 비교한다. Table 1의 열 머리글로 "No retrieval", "Retrieval from Wiki in", "User lang", "English+UL", "English", "All langs"를 확인했다(평문 추출이라 열 순서와 묶임은 불확실하다). Table 1 설명: "RAG brings substantial performance improvement in all languages, and retrieval from multilingual Wikipedia is beneficial in most cases." — [Chirkova et al., 2024, "Retrieval-augmented generation in multilingual settings"](https://arxiv.org/abs/2407.01463)
- [2차 출처만] 2026년 7월 arXiv 2607.02966 ("Distill Where the Student Goes: Teacher-Regularized RL for English-Evidence Cross-Lingual RAG")은 질문은 여러 언어, 검색 문단은 영어로 고정한 "English-evidence" 설정을 다룬다고 검색 요약에 나온다. 원문은 열지 않았다. — [arXiv:2607.02966](https://arxiv.org/abs/2607.02966)

**요약 표(위 원문 확인 내용만 모음)**

표의 각 행은 이 절과 1번 절의 인용 항목을 줄인 것이다. 출처는 해당 항목의 링크를 따른다. 표에만 있는 새 주장은 없다.

| 벤치마크 | 유형 | 질문 언어 문서에 답이 없도록 했는가 | 중복·병렬 내용 처리 |
|---|---|---|---|
| TyDi QA, Mr.TyDi, MIRACL, NoMIRACL, MIRAGE-Bench | 단일 언어 | 해당 없음 | 해당 없음 |
| XQuAD | 단일 언어(병렬 번역) | 해당 없음 | 모든 언어에 같은 내용 |
| MLQA G-XLT | 교차 언어 독해(검색 없음) | 문단이 주어져서 해당 없음 | 병렬 인스턴스에서 질문만 교체 |
| MKQA | 문서와 무관한 답 주석 | 아니오(지역 무관 질문을 선호) | 답을 Wikidata 개체로 통일 |
| XOR-Retrieve, XOR-EnglishSpan | 교차 언어(영어 풀만) | 풀 구성으로 배제 + TyDi "답 없음" 딱지(전수 검증 아님) | 답 문자열 포함 여부로 채점 |
| XOR-Full | 두 언어 풀 | 아니오("allows for both retrieval paths") | 답 문자열로 채점, 근거 언어 구분 안 함 |
| LAReQA | 다국어 풀 | 아니오 | 모든 번역판이 정답(11개) |
| CLIRMatrix BI-139 / MULTI-8 | 교차 언어 / 혼합 | 풀 구성(BI) / 아니오(MULTI) | Wikidata 링크로 딱지 전파 |
| NeuCLIR CLIR / MLIR | 교차 언어 / 다국어 | 풀 구성(영어 주제, 비영어 문서) | Gaps 참조 |
| BordIRlines | 방식별(단일·교차·다국어) | 방식별 풀 구성 | 내용 기준 관련도, 언어 무관 |
| Futurepedia | 병렬 문서 재배치 | 과제별 풀 구성 | 8개 언어 병렬 |
| XRAG 단일 언어 검색 / 다국어 검색 | 교차 언어 | 풀 구성(영어만) / 두 언어가 답의 일부씩 보유 | 근거 2개가 상보적 |
| XBCP 교차 언어 / 다국어 | 교차 언어 / 다국어 | 근거를 한 언어로 번역 배치 | 번역으로 통제 |

### Inferences

- 교차 언어 조건을 만드는 방법은 세 가지로 정리된다. (a) 풀을 다른 언어 문서로만 채운다(XOR-Retrieve, NeuCLIR CLIR, XRAG 단일 언어 검색, XBCP 교차 언어, Futurepedia 교차 언어 과제). (b) 풀을 섞고 같은 사실의 모든 언어판을 정답으로 센다(LAReQA, CLIRMatrix MULTI-8, XOR-Full의 답 문자열 채점). (c) 풀을 섞되 각 언어 문서가 답의 서로 다른 일부만 갖게 한다(XRAG 다국어 검색).
- 조사 범위에서 "질문 언어 문서에 답이 없음"을 사람이 검증해 보장한 벤치마크는 없었다. 배타성이 있는 곳은 모두 풀 구성이나 번역 배치로 얻었다. Wikipedia 규모에서는 MIRACL과 CORA가 "없음"을 확정할 수 없다고 명시한다.
- 섞인 풀에서 같은 사실이 두 언어에 있으면, 시스템이 질문 언어 문서만으로 답해도 맞은 것이 된다. LAReQA와 Faux Polyglot은 이 상황을 일부러 만들어 "같은 언어 선호"를 잰다. 이 두 연구에서 중복은 언어 선호를 재는 도구다. XOR-Full과 CLIRMatrix MULTI-8도 중복을 허용하지만 목적은 일반적인 QA·다국어 검색 평가이고 언어 선호를 따로 재지 않는다.
- 한국어·영어 30문항, 20~30문서 평가셋에 대한 선택지는 다음과 같다. 어느 것을 택할지는 이 노트의 범위 밖이다.
  - 근거를 다른 언어에만 두면, 교차 언어 검색에 실패한 것이 곧 오답으로 드러난다. 선례는 XOR-Retrieve, XRAG 단일 언어 검색, XBCP다. 소규모에서는 "질문 언어 문서에 없음"을 전수 확인할 수 있다.
  - 두 언어에 다 두고 양쪽을 정답 근거로 표시하면, 교차 언어 검색 능력은 분리해 잴 수 없다. 대신 어느 언어 문서를 가져오는지(언어 선호)를 볼 수 있다. 선례는 LAReQA, CLIRMatrix MULTI-8, Faux Polyglot이다.
  - 두 언어가 답의 일부씩 갖게 하면, 두 언어 문서를 모두 가져와 합쳐야 한다. 선례는 XRAG 다국어 검색이다.

### Gaps

- NeuCLIR 2023 MLIR에서 같은 사건을 다룬 중국어·페르시아어·러시아어 문서를 각각 어떻게 판정하는지(언어별 독립 판정인지, 중복 처리 규칙이 있는지)는 해당 절을 추출하지 못해 확인하지 못했다. 확인한 것은 MLIR 주제 65개가 평가에 남았다는 것과 "single unified ranked list" 요건뿐이다.
- NeuCLIR 2024 개요와 그 이후 트랙(보고서 생성 과제 등)은 조사하지 않았다.
- NoMIRACL의 비관련 부분집합이 MIRACL에서 버려진 질문("invalid")에서 왔다는 연결은 두 논문의 서술로 짐작되지만, NoMIRACL 본문에서 그 문장을 직접 인용하지는 못했다.
- Futurepedia의 Multilingual Knowledge Selection 과제 정의 문장과 XBCP 다국어 설정에서 영어 원본 문서가 풀에 남는지는 확인하지 못했다.
- "MultiCLIR"라는 이름의 벤치마크는 찾지 못했다. MMed-Bench-IR(arXiv 2606.24200)과 "2026 ACL language bias in multilingual RAG" 연구는 검색 요약에만 나왔고 원문은 확인하지 않았다.
- BordIRlines와 XRAG의 게재 학회(검색 요약에는 각각 ACL 2025 Findings, Findings of EMNLP 2025로 나옴)는 원문에서 확인하지 않았다.

---

## 3. 언어판 사이의 "정보 비대칭"을 명시적으로 논하고 교차 언어 질문 구성에 쓴 벤치마크

### Takeaway

"information asymmetry"라는 말을 직접 쓰고 그것을 데이터 구성의 동기로 삼은 것은 XOR-TyDi QA다. 다만 XOR은 비대칭인 사실을 골라낸 것이 아니라, TyDi QA에서 답을 못 찾은 질문을 비대칭 또는 정보 부족의 결과로 해석해 다시 주석했다. 그 밖의 벤치마크는 비대칭을 가정하거나(Futurepedia, XRAG) 번역으로 인위적으로 만든다(XBCP, Faux Polyglot). MKQA는 반대로 언어에 따라 달라지지 않는 질문을 고른다.

### Cited Findings

- [원문 확인] XOR의 두 개념 정의. Abstract: "many languages face both information scarcity—where languages have few reference articles—and information asymmetry—where questions reference concepts from other cultures." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR §1의 설명과 예시: "it is important to support retrieving answers in languages other than the original language due to information scarcity of low-resource languages (Miniwatts Marketing Group, 2011). Moreover, questions strongly related to entities from other cultures are less likely to have answer content in the questioner's language due to cultural bias (information asymmetry, Callahan and Herring, 2011). For example, Fig. 1 shows that the Japanese Wikipedia article of an American politician, Ron Paul, does not have information about his college degree perhaps because Japanese Wikipedia editors are less interested in specific educational backgrounds of American politicians." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] XOR §1은 질문이 답할 수 없었던 원인을 두 개념에 돌린다: "Questions in our dataset are inherited from TYDI QA (Clark et al., 2020), which are written by native speakers and are originally unanswerable due to the information scarcity or asymmetry issues." 그러나 Appendix A는 주석 오류도 원인이라고 적는다("questions can be labeled as unanswerable simply because of annotation errors"). — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 비대칭은 양방향이다. 영어판이 대상 언어권 주제를 더 자세히 다루는 경우와 대상 언어판에만 답이 있는 경우가 모두 예시로 나온다. §2.2: "The second example shows English Wikipedia sometimes contains rich information about a target language-specific topic (e.g., economy in Krasnodar, a city in Russia). ... In the last question of Table 3, on the other hand, only the Wikipedia of the target language can provide the answer." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] 영어에도 대상 언어에도 없는 경우. 각주 6(텔루구어): "Those questions often ask some specific information of local administration districts, and are often unanswerable because (a) they are typically not described in English Wikipedia and (b) the overall coverage of Telugu Wikipedia is quite low." — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] CORA는 Wikipedia 언어판이 서로 병렬이 아님을 과제 정의에 넣는다. §2 Method: "evidence passages can be retrieved from any language. These passages come from Wikipedia articles that are not necessarily parallel over languages." — [Asai et al., 2021 (CORA)](https://arxiv.org/abs/2107.11976)
- [원문 확인, 프리프린트] Chirkova et al.은 비영어 지식 저장소의 가치를 현지·문화 특화 정보로 설명한다. §1: "considering non-English knowledge datastores ensures access to local or culture-specific inf[ormation]" (추출된 문장이 여기서 끊겨 있어 뒤는 확인하지 못함). — [Chirkova et al., 2024](https://arxiv.org/abs/2407.01463)
- [원문 확인, 프리프린트] XRAG는 자원이 풍부한 언어가 정보를 보탠다는 시나리오로 설명한다. §3: "documents in a resource-rich language provide additional information for LLMs to answer questions in a second language." 각주 1은 실제 사용 데이터 관찰을 언급한다: "An initial study on a proprietary dataset of real-world LLM traffic from non-English users in Germany, Japan, and Spain found that using only English or native-language search results was inferior to combining both (see Appendix A)." — [Liu et al., 2025](https://arxiv.org/abs/2505.10089)
- [원문 확인, 프리프린트] Futurepedia의 교차 언어 과제는 "질문 언어에 좋은 문서가 없는 상황"을 흉내 낸다. §2.2: "This task imitates the real-world scenario where there are no high-quality documents in the query language". — [Wu et al., 2024](https://arxiv.org/abs/2410.21970)
- [원문 확인, 프리프린트] Faux Polyglot은 언어 간 지식 충돌과 단절을 전제로 둔다. Abstract: "real-life scenarios where linguistic divide and knowledge conflicts between multilingual sources are known occurrences". — [Sharma et al., 2024](https://arxiv.org/abs/2407.05502)
- [원문 확인, 프리프린트] BordIRlines는 같은 주제가 언어판마다 다른 관점으로 쓰이는 점(관점 비대칭)을 이용한다. (절 미기록): "Geopolitical Bias is the tendency to report geopolitical knowledge differently depending on the language of interaction." Abstract: "retrieving multilingual documents best improves response consistency and decreases geopolitical bias over RAG with purely in-language documents." — [Li et al., 2024/2025](https://arxiv.org/abs/2410.01171)
- [원문 확인] MKQA는 반대 방향이다. 지역·문화에 따라 답이 달라지지 않는 질문만 평가 대상으로 삼는다("we reserve our assessment to geographically invariant queries"). — [Longpre et al., 2021](https://arxiv.org/abs/2007.15207)

### Inferences

- XOR의 "information asymmetry"는 질문 구성의 동기이지 선정 기준이 아니다. 선정 기준은 TyDi의 "답 없음" 딱지다. 개별 질문이 실제로 비대칭 때문에 답이 없었는지는 확인하지 않았다.
- XOR의 용어를 빌리면 한국어·영어 평가셋의 교차 언어 질문은 두 방향으로 나뉜다. 한국어 질문인데 영어 문서에만 근거가 있는 경우(해외 주제, Ron Paul 유형)와 영어 질문인데 한국어 문서에만 근거가 있는 경우(한국 지역 주제)다. XOR은 앞의 방향(비영어 질문, 영어 근거)만 새로 주석했다.

### Gaps

- Wikipedia 언어판 사이에서 "한 언어판에만 있는 사실"을 직접 찾아내 질문으로 만든 벤치마크는 이번 조사에서 찾지 못했다. 검색을 두 번만 했으므로 없다고 단정할 수는 없다.
- XOR이 인용한 Callahan and Herring (2011)의 원문은 확인하지 않았다.
- 한국어 Wikipedia와 영어 Wikipedia 사이의 정보 비대칭 규모를 잰 연구는 조사하지 않았다.

---

## 4. 한국어 포함 여부(한국어 질문·한국어 문서가 있는 벤치마크)

### Takeaway

한국어 질문과 한국어 Wikipedia 문서가 함께 있는 것은 TyDi QA 계열(TyDi QA, Mr.TyDi, MIRACL, NoMIRACL, MIRAGE-Bench)이다. 한국어 질문에 영어 근거를 붙인 교차 언어 데이터는 XOR-TyDi QA(와 이를 쓴 MIA 2022)다. MKQA는 한국어 질문만 있고 근거 문서가 없다. MLQA, XQuAD, CLIRMatrix MULTI-8, NeuCLIR, XRAG, Faux Polyglot에는 한국어가 없다.

### Cited Findings

- [원문 확인] XOR-TyDi QA: 한국어 포함. §2.1.1: "Arabic, Bengali, Finnish, Japanese, Korean, Russian and Telugu." 한국어 질문은 TyDi QA의 원어민 질문이다. 교차 언어 부분의 근거는 영어 Wikipedia, 같은 언어 부분의 근거는 한국어 Wikipedia다. 수치는 1번 절에 적었다. — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] TyDi QA: 한국어가 포함된다는 것은 XOR 논문("We choose 7 languages ... out of the 10 non-English languages")과 Mr.TyDi의 언어 표로 확인했다. TyDi QA 본문에서 추출한 "Korean" 언급은 관련 연구 문단뿐이어서, TyDi QA 논문 자체의 언어 목록 문장은 직접 인용하지 못했다. — [Clark et al., 2020](https://arxiv.org/abs/2003.05002); [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] Mr.TyDi: 한국어 포함(11개 언어 표에 "Korean (Ko)"). 한국어 질문과 한국어 Wikipedia 문단이다. — [Zhang et al., 2021](https://arxiv.org/abs/2108.08787)
- [원문 확인] MIRACL: 한국어 포함. §1: "Arabic (ar), Bengali (bn), English (en), Spanish (es), Farsi (fa), Finnish (fi), French (fr), Hindi (hi), Indonesian (id), Japanese (ja), Korean (ko), Russian (ru), Swahili (sw), Telugu (te), Thai (th), Chinese (zh), and two 'surprise' languages". 한국어 질문과 한국어 Wikipedia 문단이다. — [Zhang et al., 2023](https://arxiv.org/abs/2210.09984)
- [원문 확인] NoMIRACL: 한국어 포함(언어 나열에 "Korean (ko)"). 실험에서는 언어·부분집합마다 질문을 최대 250개로 제한한다("we limit the maximum number of 250 queries for each language and subset"). — [Thakur et al., 2024](https://arxiv.org/abs/2312.11361)
- [원문 확인, 프리프린트] MIRAGE-Bench: MIRACL의 18개 언어를 물려받는다. 한국어는 절제 실험 언어로 명시된다(§6.3: "a subset of seven languages including Arabic (ar), Bengali (bn), Finnish (fi), Japanese (ja), Korean (ko), Russian (ru) and Telugu (te)"). — [Thakur et al., 2024 (MIRAGE-Bench)](https://arxiv.org/abs/2410.13716)
- [원문 확인] MKQA: 한국어 포함(Table 1의 언어 코드 "ko-KR", 한국어 예시 질문 "전 세계에서 누가 가장 많은 피스타치오를 생산하나요"). 영어 질문을 사람이 번역한 것이고 근거 문서는 붙어 있지 않다. — [Longpre et al., 2021](https://arxiv.org/abs/2007.15207)
- [원문 확인] MIA 2022: 한국어 포함(Table 1에 "Korean (ko)", XOR-TyDi QA와 MKQA 양쪽에 걸침). — [Asai et al., 2022 (MIA)](https://arxiv.org/abs/2207.00758)
- [원문 확인] CLIRMatrix: BI-139의 언어 목록에 "ko:Korean"이 있다. MULTI-8은 ar, de, en, es, fr, ja, ru, zh이고 한국어가 없다. — [Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)
- [원문 확인, 프리프린트] BordIRlines: 사람 주석을 한 5개 언어에 한국어가 들어 있다("English, Chinese, Hindi, Spanish, and Korean"). — [Li et al., 2024/2025](https://arxiv.org/abs/2410.01171)
- [원문 확인, 프리프린트] Futurepedia: 한국어 포함(8개 언어에 "Korean (ko)"). 병렬 문서와 QA다. — [Wu et al., 2024](https://arxiv.org/abs/2410.21970)
- [원문 확인, 프리프린트] Chirkova et al.: Table 1의 MKQA 행과 XOR TyDi QA 행 모두에 Korean이 있다. — [Chirkova et al., 2024](https://arxiv.org/abs/2407.01463)
- [원문 확인, 프리프린트] Park & Lee: 생성기 언어 선호 실험에 한국어 포함("eight languages: English (en), Korean (ko), Chinese (zh), French (fr), Japanese (ja), Italian (it), Portuguese (pt), and Spanish (es)"). 데이터는 MKQA다. — [Park & Lee, 2025](https://arxiv.org/abs/2502.11175)
- [원문 확인, 프리프린트] XBCP: 근거 문서 번역 대상 12개 언어에 한국어 포함("Chinese, English, French, German, Japanese, Korean, Portuguese, and Spanish, as well as ... Swahili, Wolof, Yoruba, and Zulu"). 질문은 영어, 근거가 한국어인 방향이다. 언어별 표에서 한국어 행은 N=69이다. — [Lu et al., 2026](https://arxiv.org/abs/2606.15345)
- [원문 확인] 한국어 없음: MLQA(7개 언어: English, Arabic, German, Vietnamese, Spanish, Simplified Chinese, Hindi) — [Lewis et al., 2020](https://arxiv.org/abs/1910.07475). XQuAD(영어 원본 + Spanish, German, Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, Hindi) — [Artetxe et al., 2020](https://arxiv.org/abs/1910.11856). NeuCLIR(문서는 Chinese, Persian, Russian, 주제는 영어) — [Lawrie et al., 2024](https://arxiv.org/abs/2404.08071). XRAG(영어 + Arabic, Chinese, German, Spanish) — [Liu et al., 2025](https://arxiv.org/abs/2505.10089). Faux Polyglot(en, hi, de, ar, zh) — [Sharma et al., 2024](https://arxiv.org/abs/2407.05502).
- [원문 확인] LAReQA: 논문 본문에서 "Korean" 검색 결과가 없었다. XQuAD와 MLQA를 변환한 것이므로 한국어가 없다고 본다. — [Roy et al., 2020](https://arxiv.org/abs/2004.05484)

### Inferences

- 한국어 질문에 영어 근거를 붙이고 사람이 주석한 기존 데이터는 XOR-TyDi QA의 한국어 부분이 대표적이다. 영어 질문에 한국어 근거를 붙인 방향은 XBCP(기계 번역으로 만든 근거)와 CLIRMatrix BI-139(자동 생성 딱지)에서만 확인했다. 사람이 주석한 영어 질문·한국어 근거 QA 벤치마크는 이번 조사에서 찾지 못했다.
- 한국어·영어가 섞인 풀에서 같은 사실이 두 언어에 있는 경우를 다룬 한국어 포함 벤치마크는 Futurepedia(병렬 문서)와 Park & Lee(MKQA 기반 언어 선호 분석)다.

### Gaps

- TyDi QA 논문 자체의 한국어 데이터 크기와 언어 목록 문장은 직접 인용하지 못했다.
- BordIRlines의 49개 언어에서 한국어 질문이 몇 개인지는 확인하지 못했다.
- KorQuAD 같은 한국어 전용 데이터와 한국어·영어 교차 언어 전용 데이터는 조사 범위에 넣지 않았다. MKQA와 TyDi QA 논문의 관련 연구 문단에 KorQuAD 1.0(Lim et al., 2019)이 언급된다는 것만 확인했다.

---

## 5. "cross-lingual"과 "multilingual"을 구분하는 용어

### Takeaway

정보 검색 쪽(Mr.TyDi, MIRACL, NeuCLIR, CLIRMatrix)의 구분은 일관된다. monolingual은 질문과 문서가 같은 언어, cross-lingual(CLIR)은 질문과 문서가 다른 언어, multilingual(MLIR) 또는 mixed-language는 여러 언어 문서를 한 풀에 넣고 순위 목록 하나를 만드는 것이다. 다만 "multilingual"은 "여러 언어 각각에서 단일 언어 과제를 한다"는 뜻으로도 쓰인다. XRAG는 "monolingual retrieval"을 다른 뜻으로 쓴다. 평가셋 문서에는 용어 정의를 따로 적어야 한다.

### Cited Findings

- [원문 확인] CLIR의 정의. CLIRMatrix §1: "Cross-Lingual Information Retrieval (CLIR) is a retrieval task in which search queries and candidate documents are written in different languages." — [Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)
- [원문 확인] monolingual 대 cross-lingual. MIRACL(과제 정의 절, 절 미기록): "our focus is monolingual retrieval across diverse languages, where the queries and the corpora are in the same language (e.g., Thai queries searching Thai documents), as opposed to cross-lingual retrieval, where the queries and the corpora are in different languages (e.g., searching a Swahili corpus with Arabic queries)." — [Zhang et al., 2023](https://arxiv.org/abs/2210.09984)
- [원문 확인] "multi-lingual"을 "여러 언어의 단일 언어 과제 묶음"으로 쓰는 예. Mr.TyDi Abstract: "a multi-lingual benchmark dataset for mono-lingual retrieval in eleven typologically diverse languages". — [Zhang et al., 2021](https://arxiv.org/abs/2108.08787)
- [원문 확인] MLIR의 정의. Lawrie et al. Abstract: "Cross Language IR (CLIR) where queries are expressed in one language and documents in another, the multilingual (MLIR) task to create a single ranked list of documents across many languages is considerably more challenging." §1: "MLIR seeks to produce a total ordering over retrieved documents, regardless of language, such that the most useful documents appear at the top of the ranking." — [Lawrie, Yang, Oard, Mayfield, 2022/2023, "Neural Approaches to Multilingual Information Retrieval"](https://arxiv.org/abs/2209.01335)
- [원문 확인] NeuCLIR 2023 Abstract: "ranked MLIR for news, with topics in English. This task requires generating a single ranked list for a given topic that includes Chinese, Persian and Russian documents. The principal additional challenge in this task is that scores computed for documents in different languages are usually incomparable". — [Lawrie et al., 2024](https://arxiv.org/abs/2404.08071)
- [원문 확인] "mixed-language retrieval"과 "multilingual retrieval"은 같은 말로 쓰인다. CLIRMatrix §1: "the latter supports research in mixed-language retrieval (a.k.a multilingual retrieval (Savoy and Braschler ...". 같은 논문에서 BI-139는 "bilingual retrieval", MULTI-8 평가는 "single-language retrieval and mix-language retrieval settings"라고 부른다. — [Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)
- [원문 확인] XOR 논문이 CLIR과 자기 과제를 구분하는 방식(결론 바로 앞 관련 연구 절, 절 미기록): "while CLIR typically retrieves documents from a single (low-resource) language (Zhang et al., 2019), XOR QA considers documents from both English and the query language. In many applications, we do not know a priori in which language we can find target information." XOR은 자기 데이터 안에서 "cross-lingual data"와 "in-language data"로 나눈다(Table 2). — [Asai et al., 2021](https://arxiv.org/abs/2010.11856)
- [원문 확인] "multilingual open QA"의 정의(근거가 어느 언어에서든 올 수 있음). CORA §2(위첨자가 깨져 추출되어 기호 표기는 복원함): "We define multilingual open QA as the task of answering a question q in a target language L given a collection of multilingual reference passages C^multi, where evidence passages can be retrieved from any language." 같은 논문은 "many-to-many cross-lingual retrieval"이라는 표현도 쓴다. — [Asai et al., 2021 (CORA)](https://arxiv.org/abs/2107.11976)
- [원문 확인] MIA 2022는 XOR-Full 안에서 "(monolingual)"과 "(cross-lingual)"을 질문별 딱지로 쓴다: "some questions can be answered based on the target language's Wikipedia (monolingual) while others require evidence only presented in English Wikipedia (cross-lingual)." — [Asai et al., 2022 (MIA)](https://arxiv.org/abs/2207.00758)
- [원문 확인] MLQA의 "cross-lingual"은 두 가지 뜻이다. XLT는 학습 언어와 평가 언어가 다른 것(전이)이고, G-XLT는 질문 언어와 문단 언어가 다른 것이다. §1: "cross-lingual transfer (XLT), requires models trained in one language (in our case English) to transfer to test data in a different language. The second, generalised cross-lingual transfer (G-XLT) requires models to answer questions where the question and context language is different". — [Lewis et al., 2020](https://arxiv.org/abs/1910.07475)
- [원문 확인] LAReQA는 "language-agnostic", "multilingual pool", "weak / strong alignment", "language bias"라는 말을 쓴다. Abstract: "LAReQA tests for 'strong' cross-lingual alignment, requiring semantically related cross-language pairs to be closer in representation space than unrelated same-language pairs." — [Roy et al., 2020](https://arxiv.org/abs/2004.05484)
- [원문 확인, 프리프린트] XRAG의 용어는 정보 검색 쪽 관례와 다르다. "Cross-lingual RAG with Monolingual Retrieval"은 질문이 비영어이고 검색 문서가 전부 영어인 경우다. "Cross-lingual RAG with Multilingual Retrieval"은 검색 문서가 영어와 질문 언어에 걸친 경우다. Figure 1 설명: "(a) monolingual retrieval, where the LLM uses retrieved English documents to respond to a German query; (b) multilingual retrieval, where the LLM uses retrieved English and German documents to respond to a German query." XRAG는 질문과 문서가 같은 언어인 설정을 "monolingual settings"라고도 부른다(§1). — [Liu et al., 2025](https://arxiv.org/abs/2505.10089)
- [원문 확인, 프리프린트] BordIRlines는 검색 방식 이름으로 구분한다: "monolingual IR in query lang"(qlang), "multilingual IR in query lang and en"(qlang+en), "multilingual IR in all relevant languages"(rel_langs), "cross-lingual IR in en"(en_only), "cross-lingual IR in non-query lang"(swap_docs). — [Li et al., 2024/2025](https://arxiv.org/abs/2410.01171)
- [원문 확인, 프리프린트] 다국어 RAG 쪽 용어. Park & Lee §1: "Multilingual Retrieval-Augmented Generation (mRAG) extends traditional Retrieval-Augmented Generation (RAG) ... by leveraging multilingual external sources". Chirkova et al.은 질문 언어를 "user language (UL)"라고 부르고 검색 대상을 "User lang", "English+UL", "English", "All langs"로 나눈다(평문 추출이라 열 순서는 불확실하다). — [Park & Lee, 2025](https://arxiv.org/abs/2502.11175); [Chirkova et al., 2024](https://arxiv.org/abs/2407.01463)
- [원문 확인, 프리프린트] Futurepedia의 과제 이름: "Monolingual Knowledge Extraction", "Cross-lingual Knowledge Transfer", "Multilingual Knowledge Selection". — [Wu et al., 2024](https://arxiv.org/abs/2410.21970)
- [원문 확인, 프리프린트] XBCP의 구분: "In the cross-lingual setting, each query is paired with evidence in a single assigned language. In the multilingual setting, the full evidence corpus is distributed equally and randomly across 12 languages". — [Lu et al., 2026](https://arxiv.org/abs/2606.15345)

### Inferences

- 문헌에서 가장 널리 통하는 세 구분은 다음과 같다. monolingual(또는 in-language)은 질문과 근거가 같은 언어다. cross-lingual은 질문과 근거가 다른 언어다. multilingual(또는 mixed-language)은 한 풀에 여러 언어 문서가 섞여 있고 근거가 어느 언어에든 있을 수 있다.
- "cross-lingual"은 논문마다 세 층위로 쓰인다. 풀 전체의 속성(풀이 다른 언어 문서뿐, NeuCLIR CLIR·XOR-Retrieve), 질문별 딱지(섞인 풀 안에서 이 질문의 근거가 다른 언어에 있음, XOR-Full·MIA), 학습과 평가 언어의 차이(MLQA XLT)다. 한국어·영어가 섞인 풀을 쓰는 평가셋에서 "교차 언어 질문"은 두 번째 뜻에 해당한다.
- 질문별 딱지로 쓸 때, 두 언어 모두에 근거가 있는 질문을 어떻게 부를지는 조사한 논문 어디에도 정해진 용어가 없다. XOR-Full과 MIA는 이 경우를 따로 분류하지 않는다. 평가셋에서 이 경우를 둔다면 이름을 직접 정의해야 한다.
- XRAG의 "monolingual retrieval"은 질문이 다른 언어인데도 monolingual이라고 부른다. 정보 검색 쪽 정의와 충돌하므로 인용할 때 주의가 필요하다.

### Gaps

- 교차 언어·다국어 검색이나 다국어 RAG를 다룬 서베이 논문은 이번에 읽지 못했다. 위 용어 정리는 개별 벤치마크 논문과 Lawrie et al.의 MLIR 논문만을 근거로 한다.
- "두 언어 모두에 근거가 있는 질문"을 가리키는 표준 용어가 있는지는 확인하지 못했다. 조사한 논문에서는 찾지 못했다.
