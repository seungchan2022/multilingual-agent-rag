# 다국어 RAG의 언어 편향과 소규모 평가셋으로 교차 언어 능력을 재는 방법

조사일 2026-10-12. 확인 수준 표기는 아래 세 가지다.

- **[원문 확인]**: 논문 본문(arXiv HTML 또는 PDF를 텍스트로 변환한 것)에서 해당 문장·표의 행을 직접 읽었다.
- **[WebFetch 추출]**: 원문 페이지를 요약 도구로 읽은 결과다. 원문 페이지이긴 하지만 표의 열 순서나 문장을 내가 직접 대조하지 못했다.
- **[2차 출처만]**: 검색 결과 요약이나 다른 논문의 인용으로만 확인했다.

"Inferences" 항목은 모두 논문이 실험한 내용이 아니라 내 추론이다. 30문항·문서 20~30개 규모에서 실험한 논문은 찾지 못했다.

## 1. 어떤 논문이 다국어 RAG·다국어 검색의 언어 선호(편향)를 다루고, 무엇을 숫자로 보였나

### Takeaway
검색기는 질문과 같은 언어의 문서와 영어 문서를 더 높게 올리고, 생성기는 질문 언어 문서를 조금 더 쓰는 경향이 여러 논문에서 반복해서 보고됐다. 다만 한국어 질문에서 영어 문서 선호의 방향은 같은 논문 안에서도 번역기와 표본에 따라 뒤집혔고, 생성기 쪽 선호는 검색기 쪽보다 약하다.

### Cited Findings

**(1) Park & Lee, "Investigating Language Preference of Multilingual RAG Systems", Findings of ACL 2025** — [arXiv 2502.11175v4](https://arxiv.org/html/2502.11175v4)
- 초록의 결론: "retrievers tend to prefer high-resource and query languages, yet this preference does not consistently improve generation performance." [WebFetch 추출, 초록]
- 질문과 문서 언어가 같을 때: "when the query and document languages are identical, the retriever shows a high preference." [원문 확인, §4.1 Table 1 설명]
- 영어 문서: "English often outperforms even monolingual configurations, likely due to the abundance of English data in pre-training" [원문 확인, §4.1]
- 한국어 질문 행(Table 1, MLRS 점수, 괄호는 Lq=Ld 대비 변화) [원문 확인]. **열의 뜻에 주의**: 각 열은 질문 언어가 아닌 문서를 그 언어(Ld)로 번역했을 때의 순위 상승 점수다. "그 언어 문서가 몇 등으로 뽑혔는가"가 아니다. Lq=Ld 열은 질문 언어(ko)로 번역한 경우다.
  - bge-m3: Ld=ko 41.15, Ld=en 43.49 (+2.34), zh 34.42 (-6.73), fr 36.42 (-4.73), ja 37.18 (-3.97), it 35.72 (-5.43), pt 35.30 (-5.85), es 35.93 (-5.22)
  - paraphrase-multilingual-MiniLM-L12-v2 (p-mMiniLM): Ld=ko 42.95, Ld=en 44.62 (+1.67), zh 36.04 (-6.91), fr 37.08 (-5.87), ja 38.47 (-4.48), it 36.07 (-6.88), pt 36.18 (-6.77), es 36.45 (-6.50)
  - paraphrase-multilingual-mpnet-base-v2: Ld=ko 42.53, Ld=en 44.98 (+2.45)
- 영어 질문 행(Table 1, bge-m3): Ld=en 56.03, Ld=ko 33.02 (-23.01) [원문 확인]. 즉 영어 질문에서는 문서를 한국어로 번역했을 때의 점수가 크게 낮다.
- **같은 논문 안의 불일치**: Table 2(질문 100개 표본, GPT-4o-mini 번역, top-10 안에서만 계산)에서는 한국어 질문이 Ld=ko 47.15, Ld=en 42.59 (-4.56)로 방향이 반대다 [원문 확인, §4.3]. 논문은 Table 2가 "consistent with prior MLRS findings"라고만 쓰고 이 방향 차이를 설명하지 않는다.
- 문서 언어의 자원 수준: "documents from high-resource languages consistently achieve the highest preference scores, followed by mid-resource and then low-resource languages" [원문 확인, §4.2]. 이 논문은 한국어를 low-resource 예로 든다: "low-resource (e.g., Korean)" [원문 확인, §4.2].
- 생성기: "the generator produces more consistent responses in languages that use Latin scripts (e.g., en, fr, it, pt, es) compared to non-Latin languages (e.g., ko, zh, ja)" / 질문 언어와 답 언어가 같을 때의 이득은 "this improvement is marginal" [원문 확인, §5.1.2]
- 비영어 질문의 성능: "it achieves optimal performance when it receives retrieved passages that directly match the query language. In these cases, translating all passages into English does not enhance performance" [원문 확인, §5.2.2]
- 실험 규모: MKQA 2,827개 질문, 검색기 BGE-m3, 생성기 aya-expanse-8B·Phi-4·Qwen2.5-7B-Instruct·Llama3.1-8B-Instruct [원문 확인, §4.3·§5.2]

**(2) Sharma, Murray, Xiao, "Faux Polyglot: A Study on Information Disparity in Multilingual Large Language Models", NAACL 2025** — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- 검색: "for the top-10 retrieved documents, models preferred the Native Language Document 68% of the time across both premises ... with an average z-score of 1.03 for Native Language versus -0.25 for Foreign Language" [원문 확인, §4.1]
- 생성: "the Native Language documents were the source for the answer 42% (SE = 0.54%) of times compared to 29.58% (SE = 0.5)% for Foreign Language Documents while only 8.55% (SE = 0.30%) contains information from both the sources, and 19.8% (SE= 0.43%) the answer was from none of the sources" [원문 확인, §4.2.1]
- 질문 유형별(같은 논문): broad 질문은 native 57.05% 대 foreign 25.38%, specific-contradiction은 35.36% 대 12.13% [원문 확인, §4.2.2]. 반면 exclusive 질문(한 언어 문서에만 있는 사실)은 "Native and Foreign Documents again perform similarly, though the none score remains high" [원문 확인, §4.2.2]
- 질문 언어 문서가 없을 때: 생성 단계에서 "LLMs preferred high-resource languages as their second language" [원문 확인, §5]
- 언어는 en, hi, de, ar, zh 다섯 개이고 **한국어는 없다** [WebFetch 추출, §2.1]. 검색기는 OpenAI·Cohere·Voyage 임베딩, 생성기는 GPT·Claude·aya-23 계열이다 [WebFetch 추출, §2.3].

**(3) Li et al. (Bryan Li, Fiona Luo, Samar Haider, Adwait Agashe, Tammy Li, Runqi Liu, Muqing Miao, Shriya Ramakrishnan, Yuan Yuan, Chris Callison-Burch), "Multilingual Retrieval Augmented Generation for Culturally-Sensitive Tasks: A Benchmark for Cross-lingual Robustness" (BordIRLines), Findings of ACL 2025** — [arXiv 2410.01171](https://arxiv.org/html/2410.01171)
- "On IR, we find a preference toward retrieving query-language documents" [원문 확인, §1]
- 언어별 편차: "Although IR systems implemented with OpenAI and M3 embeddings both show an aggregate preference for retrieving query-language documents, the actual probabilities vary widely across query languages." [원문 확인, 부록]
- 소규모 사람 주석을 한 5개 언어에 한국어가 들어 있다: "English, Chinese, Hindi, Spanish, and Korean" [원문 확인, §3]. 한국어만 따로 본 선호 수치는 확인하지 못했다.

**(4) Yang, Jiang, Baldwin, "Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods", MRL Workshop 2024** — [ACL Anthology 2024.mrl-1.23](https://aclanthology.org/2024.mrl-1.23.pdf)
- BM25가 신경망 검색기보다 편향이 크다: "BM25 exhibits larger language bias than neural retrieval frameworks like mDPR" [원문 확인, §1]
- 공정성 지표 MRC@5 평균(×100): BM25 0.6, mBERT-DPR 13.1, XLM-R-DPR 11.7 [원문 확인, Table 3]. "more than a 20-fold disparity between BM25 and the neural retrieval ranker DPR, with scores of 0.6 and 11.7" [원문 확인, §4.3]
- 원인 설명: "BM25's output document languages and query languages exhibit a strong correlation along the diagonal line ... resulting in high retrieval rates for documents in the same language as the query." [원문 확인, §4.3]
- 대상은 유럽 24개 언어(MultiEuP-v2)이고 **한국어는 없다** [원문 확인, §2.3].

**(5) Goworek, Macmillan-Scott, Özyiğit, "What Drives Cross-lingual Ranking? Retrieval Approaches with Multilingual Language Models", arXiv preprint 2025-11 (프리프린트)** — [arXiv 2511.19324](https://arxiv.org/pdf/2511.19324)
- "XLM-R disproportionately retrieves documents written in the same language as the query ... In contrast, Nomic demonstrates a much more uniform retrieval pattern, suggesting stronger cross-lingual alignment." [원문 확인, §5 Linguistic Factors, Figure 6]
- 정확한 비율 숫자는 그림(Figure 6)에만 있어 읽지 못했다.

**(6) Wang et al. (Dan Wang, Guozhao Mo, Yafei Shi, Cheng Zhang, Bo Zheng, Boxi Cao, Xuanang Chen, Yaojie Lu, Hongyu Lin, Ben He, Xianpei Han, Le Sun), "All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG", ACL 2026 main (arXiv 2604.20199, 2026-04)** — [arXiv 2604.20199](https://arxiv.org/abs/2604.20199)
- 재순위기(reranker)가 영어와 질문 언어 문서를 선호해, 다른 언어에 흩어진 결정적 근거를 밀어낸다는 주장이다 [WebFetch 추출, 초록 요약만. 본문 미확인].

**(7) 이름만 확인한 2026년 프리프린트** [2차 출처만, 검색 요약]
- "LangSAE Editing" ([arXiv 2601.04768](https://arxiv.org/html/2601.04768v1)): 공유 풀에서 같은 언어 문서가 몰리는 현상을 "same-language crowding"이라 부른다고 요약됨.
- SHIFT ([arXiv 2606.18801 요약 페이지](https://www.emergentmind.com/papers/2606.18801)): 다국어 dense 검색기가 질문 언어 문서를 선호한다고 요약됨.
- "Enhancing Multilingual RAG Systems with Debiased Language Preference-Guided Query Fusion" ([arXiv 2601.02956](https://arxiv.org/html/2601.02956v1)): Park & Lee의 후속 계열로 요약됨.
- 세 편 모두 저자·수치를 원문에서 확인하지 않았다.

### Inferences
- 한국어 질문에 대해 "영어 문서를 더 선호한다"와 "한국어 문서를 더 선호한다" 둘 다 Park & Lee 한 논문 안에 근거가 있다. 우리 시스템에서 어느 쪽인지는 직접 재야 알 수 있다.
- 검색 단계의 같은 언어 선호(Sharma 68%)가 생성 단계의 선호(42% 대 29.58%)보다 뚜렷하다. 소규모 평가에서 언어 편향이 드러난다면 검색 순위 쪽에서 먼저 보일 가능성이 높다.

### Gaps
- mDPR, mContriever, multilingual-E5가 "같은 내용의 번역 문서 중 같은 언어 쪽을 더 높게 올린다"를 직접 잰 논문은 이번 조사에서 원문으로 확인하지 못했다. Yang et al.은 mBERT·XLM-R 기반 DPR을, Goworek et al.은 XLM-R·Nomic 등을 썼다.
- Yang et al.이 인용한 Lawrie et al. (2023)의 "documents in higher-resource languages tend to be ranked higher"는 Yang et al.의 인용문으로만 확인했다 [2차 출처만].
- "multilingual RAG in the wild"라는 제목의 논문은 찾지 못했다. 가장 가까운 것은 Chirkova et al. (2024)이며 2번 질문에 적었다.

## 2. 언어 편향을 어떻게 재는가 (실험 설계와 지표)

### Takeaway
방법은 네 갈래다. 같은 뜻의 질문을 여러 언어로 던져 순위를 비교하는 방법, 다른 언어 문서를 질문 언어로 번역해 순위가 얼마나 오르는지 보는 방법, 정답 문서의 언어를 통제하고 생성만 따로 보는 방법, 답의 언어를 자동 판별하는 방법이다. 검색과 생성을 분리해서 재는 것이 공통된 원칙이다.

### Cited Findings

**순위 이동으로 재기 (번역 후 재순위)**
- Park & Lee (2025)의 MLRS: "a novel metric that quantifies how much the ranking of retrieved documents improves when non-query language documents are translated into the query language ... (i) retrieving documents across multiple languages, (ii) translating documents that are not in the query language into the query language, and (iii) re-ranking the translated documents to measure rank improvements." [원문 확인, §2] — [arXiv 2502.11175v4](https://arxiv.org/html/2502.11175v4)
- 저자들이 밝힌 한계: 번역 모델 품질에 크게 의존한다 [WebFetch 추출, Limitations]. 번역기를 NLLB-200-distilled-600M에서 GPT-4o-mini로 바꾸자 선호 격차가 커졌다: "GPT-based translation amplifies the distinctness of language preference trends" [원문 확인, §4.3]

**같은 뜻의 질문을 여러 언어로 (평행 질문)**
- Yang et al. (2024)의 전제: "queries in different languages, but with identical semantics, should yield equivalent ranking lists when retrieving on the same multilingual documents" [원문 확인, 초록]. 두 언어 질문의 순위 목록 상관을 평균한 MRC@k를 쓴다 [원문 확인, §2.1]. 평행 질문은 기계 번역이 아니다: "These parallel query sets are from the original dataset, not machine-translated" [원문 확인, §1] — [ACL Anthology](https://aclanthology.org/2024.mrl-1.23.pdf)
- 같은 논문은 top-100 결과에서 질문 언어와 문서 언어의 교차표(Figure 6)를 그려 대각선 쏠림을 본다 [원문 확인, §4.3]. — [ACL Anthology](https://aclanthology.org/2024.mrl-1.23.pdf)

**검색된 문서의 언어 구성 세기**
- Sharma et al. (2024): 검색 유사도를 질문별 z-score로 정규화하고 top-10의 언어 구성을 센다 [WebFetch 추출, §3.1.2]. 결과 문장은 원문 확인(1번 질문 참조). — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- Goworek et al. (2025, 프리프린트): "Probability that the model retrieves a document written in the same language as the query" 와 "Distribution of retrieved document languages when the correct document is not in the query language" [원문 확인, Figure 6 캡션] — [arXiv 2511.19324](https://arxiv.org/pdf/2511.19324)

**기억과 문맥을 분리하기 (가상의 사실)**
- Sharma et al. (2024): "To study LLM's information preference in RAG, we need to separate the effects of parametric memory from in-context non-parametric memory. We created a synthetic dataset with fictional entities that were not in the LLM's pre-training data." [원문 확인, §2] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- 문서에 넣는 사실을 세 종류로 나눴다. 그중 하나가 "Exclusive Facts: facts that are exclusive to documents in a certain language." [원문 확인, §2.1]. 질문도 그에 맞춰 "Specific-Exclusive: Queries that target the exclusive facts in different languages." [원문 확인, §2.2] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- 규모: 문서 170개, 사실형 질문 27개(broad 6, specific-contradiction 9, specific-exclusive 9, specific-differential 3) [원문 확인, §2] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)

**검색과 생성을 분리하기 (정답 문서 언어 통제)**
- Qi, Fernández, Bisazza, "On the Consistency of Multilingual Context Utilization in Retrieval-Augmented Generation" (arXiv 2504.00597v4; arXiv 코멘트에 MRL Workshop 2025 Best Paper라고 적혀 있음) — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
  - 설계 의도: "we aim to assess model robustness in a challenging scenario where the important information is only provided in a different language than the query, along with several in-language distractors." [원문 확인, §5]
  - 조건: 문맥 없음(No Ctx), 질문 언어 정답 문서 1개(1 Gold (in)), 다른 언어 정답 문서 1개(1 Gold (out)), 여기에 질문 언어 또는 다른 언어 방해 문서 추가 [원문 확인, Table 3]
  - 채점: "strict lexical matching, that is, 1 if the entire gold answer string ... is a substring of the model response" [원문 확인, §3.3]
  - 맞았지만 언어가 틀린 답을 따로 센다: "a notable portion of questions are answered correctly but in the wrong language even though the models were explicitly prompted to answer in the target language" [원문 확인, §4]
- Asai, Kasai, Clark, Lee, Choi, Hajishirzi, "XOR QA: Cross-lingual Open-Retrieval Question Answering", NAACL 2021 — [arXiv 2010.11856](https://arxiv.org/html/2010.11856)
  - 과제를 셋으로 나눠 실패 지점을 진단한다: XOR-Retrieve(영어 문단 검색), XOR-EnglishSpan(영어 답 추출), XOR-Full(질문 언어로 답 생성). "Xor-Full is our ultimate goal, and the first two tasks enable researchers to diagnose where their models fail" [원문 확인, §1]
  - "Note that the Xor-Full evaluation data includes both cross-lingual and in-language data, while XOR-Retrieve and Xor-EnglishSpan only use cross-lingual data during evaluation." [원문 확인, §3.3]

**검색 대상 언어를 바꿔 가며 비교하기**
- Chirkova, Rau, Déjean, Formal, Clinchant, Nikoulina, "Retrieval-augmented generation in multilingual settings", KnowLLM Workshop 2024 — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)
  - 검색 없음, 영어 위키만, 질문 언어 위키만, 둘 다, 전체 언어의 다섯 조건을 비교한다 [WebFetch 추출, Table 1]
  - BordIRLines(Li et al.)도 같은 방식으로 "IR mode"를 다섯 개 정의한다: "qlang retrieves documents in the query (user's) language." / "qlang+en retrieves information in the query language and English." [원문 확인, §2] — [arXiv 2410.01171](https://arxiv.org/html/2410.01171)

**답의 언어 재기 (language confusion)**
- Marchisio, Ko, Bérard, Dehaze, Ruder, "Understanding and Mitigating Language Confusion in LLMs", EMNLP 2024 — [arXiv 2406.20052v3](https://arxiv.org/html/2406.20052v3)
  - LPR: "percentage of model responses that pass our line-level language confusion detector without error" / WPR: "percentage of responses where all words are in the desired language" / [LPR 문장은 원문 확인, §2.2 Language Confusion Metrics. WPR 문장과 LCPR이 둘의 조화평균이라는 설명은 WebFetch 추출]
  - 줄 단위 판별: "We split a response into lines (by newline character) and check each line against the user's desired language with fastText." [원문 확인, §2.2]. 4단어를 넘는 줄에만 적용한다는 조건은 [WebFetch 추출].
  - 짧은 답은 평가에서 뺐다: "As LID tools underperform on short sequences and non-standard text, we manually filter out: a) examples answerable with a single word/phrase" [원문 확인, §2.4]
- Chirkova et al. (2024): "we also control the correct language rate, CLR, which measures which percentage of model outputs are written in the user language. We detect languages using fasttext library" [원문 확인, 부록] — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)
- 같은 논문의 character 3-gram recall은 고유명사 음차 차이 때문에 도입했다: "models generate a transliteration of named entities in other languages different from the one contained in the ground-truth label ... Since word-level matching fails to capture similarity in the describ[ed case]" [원문 확인, 부록] — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)

### Inferences
- 우리 규모에서 그대로 쓸 수 있는 측정은 세 가지다. (a) 같은 질문의 한국어판과 영어판으로 같은 문서 풀을 검색해 정답 문서의 순위를 비교하기, (b) 검색된 상위 k개의 언어 구성 세기, (c) 답의 언어를 따로 기록하기.
- MLRS 방식(번역 후 재순위)은 번역기 품질이 결과를 바꾼다는 것이 원 논문에서 드러났으므로, 번역기를 따로 두지 않는 우리 과제에는 맞지 않는다.
- Marchisio et al.이 한 단어·구로 답하는 예시를 일부러 뺀 것으로 보아, 사실형 단답이 많은 30문항에서 fastText류 자동 판별은 믿기 어렵다. 한글 문자 비율 같은 스크립트 기준이나 사람 확인이 더 맞을 수 있다.
- 한국어 답에서 영어 고유명사를 그대로 쓰는 경우(Chirkova의 code-switching)가 exact match 채점에서 오답으로 잡힐 수 있다. 정답 표기를 한국어·영어 둘 다 허용할지는 채점 규칙에서 미리 정해야 한다.

### Gaps
- "같은 문서의 번역본 여러 개를 한 풀에 넣고 어느 언어가 1등인지 본다"는 설계를 그대로 쓴 논문은 원문으로 확인하지 못했다. 가장 가까운 것은 Park & Lee의 번역 후 재순위와 Goworek et al.의 mMARCO(번역 문서를 언어별로 나눠 배치) 설정이다.
- Marchisio et al.의 지표 정의 문장은 WebFetch 추출이다. 정의의 정확한 문구가 중요하면 원문 §2를 다시 확인해야 한다.

## 3. 한국어에 대한 근거가 있는가

### Takeaway
한국어-영어 교차 언어 검색 수치는 BGE-M3 논문(MKQA)과 Jang et al. (2025, 프리프린트)에 있고, 둘 다 dense 모델에서 교차 언어가 단일 언어보다 낮게 나온다. 답 언어 혼동은 Marchisio et al.에서 한국어가 특히 나쁜 언어였지만, 그 수치는 35B~70B 모델의 것이고 우리가 쓸 4B~8B 모델의 한국어 수치는 찾지 못했다.

### Cited Findings

**한국어 질문 → 영어 문서 검색 (MKQA, Recall@100)**
- Chen, Xiao, Zhang, Luo, Lian, Liu, "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation" (2024) — [arXiv 2402.03216](https://arxiv.org/html/2402.03216)
- 설정: "the MKQA benchmark ..., which includes queries in 25 non-English languages. For each query, it needs to retrieve the passages containing answers from the English Wikipedia corpus." [원문 확인, §4.2]
- Table 2의 ko 행 [원문 확인]: BM25 27.9, mDPR 50.9, mContriever 59.7, mE5-large 68.1, E5-mistral-7b 59.4, OpenAI-3 63.9, M3 Dense 71.6, M3 Sparse 31.4, M3 Multi-vec 71.7, M3 Dense+Sparse 71.6, M3 All 71.8
- 같은 표의 평균(Avg) 행: BM25 39.9, mDPR 60.6, mContriever 67.9, mE5-large 70.9, M3 Dense 75.1, M3 Sparse 45.3, M3 Dense+Sparse 75.3, M3 All 75.5 [원문 확인]

**한국어 단일 언어 검색 (MIRACL dev, nDCG@10)**
- 같은 논문 Table 1의 ko 열 [원문 확인]: BM25 37.1, mDPR 41.9, mContriever 48.3, mE5-large 66.5, M3 Dense 69.9, M3 Sparse 61.5, M3 Dense+Sparse 71.2, M3 All 72.1

**한국어-영어 양방향 (NDCG@10)**
- Jang, Son, Lee, Hong, Lim, "Improving Korean-English Cross-Lingual Retrieval: A Data-Centric Study of Language Composition and Model Merging" (arXiv 2507.08480, 2025, 프리프린트) — [arXiv 2507.08480](https://arxiv.org/html/2507.08480v1)
- 표기: "𝒯(en-ko) refers to a task for retrieving relevant documents from a Korean document pool given an English query" / 지표: "We report NDCG@10" [원문 확인, §3·§4]
- Table 1의 bge-m3 base 행 [원문 확인]:
  - 교차 언어: Belebele en-ko 90.37, ko-en 88.36 / StrategyQA en-ko 81.24, ko-en 71.65 / 평균 en-ko 85.81, ko-en 80.01
  - 단일 언어: Belebele ko-ko 93.16, en-en 95.55 / StrategyQA ko-ko 79.41, en-en 84.42 / 평균 ko-ko 86.29, en-en 89.99
- Table 2의 Base 행(열 순서 en-ko / ko-en / ko-ko / en-en / OVR, 두 벤치마크 평균) [원문 확인. 머리글과 bge-m3 Base 행 85.81 / 80.01 / 86.29 / 89.99 / 85.52가 Table 1 평균과 일치함을 확인]:
  - gte-multilingual-base: 84.30 / 75.02 / 81.54 / 89.45 / 82.58
  - multilingual-e5-base: 80.11 / 65.98 / 84.62 / 89.50 / 80.05
  - multilingual-e5-large: 87.04 / 76.88 / 87.43 / 90.35 / 85.42
  - 네 모델 모두 ko-en(한국어 질문→영어 문서)이 네 칸 중 가장 낮다.
- 저자가 밝힌 한계: 합성 학습 데이터가 실제 질의-문서 쌍을 다 담지 못할 수 있다 [원문 확인, Limitations]. 한국어·영어를 함께 다루는 검색 벤치마크가 적어 Belebele와 StrategyQA를 썼다는 설명은 [2차 출처만, 검색 요약].

**한국어 질문의 RAG 성능 (character 3-gram recall, 생성기 Command-R-35B, 검색기 BGE-m3)**
- Chirkova et al. (2024) Table 1 — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)
  - MKQA 한국어: 21.5 / 32.2 / 31.5 / 38.4 / 38.1
  - XOR-TyDi QA 한국어: 31.0 / 33.4 / 40.8 / 40.0 / 41.8
  - 숫자 다섯 개는 [원문 확인]. 열 순서(검색 없음 / 영어 위키 / 질문 언어 위키 / 둘 다 / 전체 언어)는 [WebFetch 추출]이다. 영어 행이 "58.4, 70.2, —, —, 68.5"인 것과는 맞는다.
- 프롬프트로 답 언어를 고정해도 한국어는 예외가 있었다: "both models achieve CRL > 95% in most cases (except SOLAR-10.7B for Korean)" [원문 확인, 부록] — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)
- SOLAR-10.7B의 한국어 correct language rate가 검색 없음 61.9, 영어 검색 53.1, 질문 언어 검색 28.8이라는 수치는 [WebFetch 추출]이고 원문 행을 대조하지 못했다. — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)

**한국어 답 언어 혼동 (Language Confusion Benchmark)**
- Marchisio et al. (2024) — [arXiv 2406.20052v3](https://arxiv.org/html/2406.20052v3)
- 한국어는 15개 언어에 포함된다. 단일 언어 설정의 한국어 프롬프트는 저자들이 원어민에게 의뢰해 만든 100개다: "Native prompts | Ours | Human-generated | 100 | 400 | es, fr, ja, ko" [원문 확인, Table 1]. 교차 언어 설정은 영어로 지시하고 대상 언어로 답하게 한다 [원문 확인, Table 1 캡션].
- Table 3, 한국어 LPR(줄 단위 통과율) [원문 확인]:
  - 단일 언어(한국어로 묻고 한국어 답 기대): Llama 2 70B-I 0.0, Llama 3 70B-I 0.0, Mixtral 8x7B 61.2, Mistral Large 64.0
  - 교차 언어(영어로 지시, 한국어 답 기대): Llama 2 70B-I 4.8, Llama 3 70B-I 0.8, Llama 3.1 70B-I 51.5, Mixtral 8x7B 56.9, Mistral Large 41.1, Command R 69.2, Command R+ 91.1
- Llama 3.1 70B-I의 단일 언어 한국어 LPR 100.0, GPT-4o와 Command 계열의 나머지 값, 한국어 WPR·LCPR 값은 [WebFetch 추출]이고 원문 셀을 대조하지 못했다.
- **이 표의 모델은 모두 35B~70B급이거나 API 모델이다.** 4B~8B 모델은 들어 있지 않다.
- 양자화의 영향: "We compare FP16 with W8, W8A8, and W4 variants of Command R+ on monolingual generation." [원문 확인, §4.4 Impact of quantization]. W4에서 부정적 영향이 나타난다는 결론 문장은 [WebFetch 추출]. — [arXiv 2406.20052v3](https://arxiv.org/html/2406.20052v3)

**한국어가 포함된 그 밖의 실험**
- Qi et al. (2025)의 MKQA·GMMLU 언어별 표에 ko 행이 있다 [원문 확인: 행 존재만. 값은 읽지 않음] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- XOR QA의 7개 언어에 한국어가 있다: "Arabic, Bengali, Finnish, Japanese, Korean, Russian and Telugu" [원문 확인, §2]. 예시: "The first question is unanswerable in Korean Wikipedia, but there is a clear description about who was the prime minister of France at the time in English Wikipedia." [원문 확인, Table 3 설명] — [arXiv 2010.11856](https://arxiv.org/html/2010.11856)

### Inferences
- bge-m3 기준으로 한국어 질문→영어 문서(ko-en 평균 80.01)가 한국어 단일 언어(86.29)와 영어 단일 언어(89.99)보다 낮다. 방향에 따라서도 다르다(en-ko 85.81 대 ko-en 80.01, StrategyQA만 보면 81.24 대 71.65). 따라서 한국어 질문→영어 근거와 영어 질문→한국어 근거를 합치지 말고 따로 보고하는 편이 맞다. 교차 언어 질문의 검색 순위가 같은 언어 질문보다 낮게 나오는 것은 예상 범위다. 다만 이 벤치마크는 문서 수천 개 이상의 풀이고, 문서 20~30개 풀에서는 그 차이가 top-3 안에서 사라질 수 있다.
- Llama 3 70B가 한국어 단일 언어 LPR 0.0이었고 Llama 3.1 70B에서 크게 올랐다는 점은, 답 언어 문제가 모델 세대에 따라 크게 달라진다는 뜻이다. 우리가 고른 4B~8B 모델에서는 직접 재야 한다.
- 로컬 모델을 4비트 양자화로 돌린다면 Marchisio et al.의 양자화 관찰이 해당될 수 있다. 다만 그 문장은 WebFetch 추출이다.

### Gaps
- **paraphrase-multilingual-MiniLM-L12-v2의 한국어-영어 교차 언어 검색 벤치마크 수치는 찾지 못했다.** Park & Lee에서 MLRS 재순위 인코더로 쓰인 것이 전부다.
- gte-multilingual-base의 한국어-영어 수치는 Jang et al. (프리프린트) Table 2 한 곳에서만 찾았다. 두 벤치마크(Belebele, StrategyQA)의 평균이고 벤치마크별 값은 읽지 않았다.
- 4B~8B 오픈소스 모델(예: Gemma, Qwen, Llama 3.1-8B, aya-expanse-8B)의 한국어 답 언어 혼동률을 따로 보고한 표는 확인하지 못했다. 검색 요약에 "Controlling Language Confusion in Multilingual LLMs"가 한국어 프롬프트 1,000개로 실험했다고 나왔으나 [2차 출처만]이고 저자·수치를 확인하지 않았다 ([요약 페이지](https://www.themoonlight.io/review/controlling-language-confusion-in-multilingual-llms)).
- MMTEB·MTEB 리더보드의 한국어-영어 교차 언어 과제 점수는 직접 조회하지 않았다.

## 4. 스크립트가 다른 언어 사이에서 BM25는 어떻게 동작하고, 하이브리드는 무엇을 보고하는가

### Takeaway
BM25는 질문과 문서의 언어가 다르면 공유 단어가 거의 없어 크게 약해지고, 스크립트가 다르면 거의 0에 가깝다는 보고가 있다. 다만 한국어 질문→영어 위키(MKQA)에서 BM25 Recall@100이 27.9로 0은 아니었다. BM25 + dense 하이브리드를 한국어 교차 언어에서 평가한 1차 출처는 찾지 못했다. 가장 가까운 대용 근거인 BGE-M3의 Dense+Sparse(BM25가 아니라 M3 자체의 학습된 sparse 가중치)는 한국어에서 dense 단독 대비 이득이 0.0포인트였다.

### Cited Findings

- Chen et al. (2024), MKQA 한국어 질문→영어 문서 Recall@100 [원문 확인, Table 2]: BM25 27.9, M3 Sparse 31.4, M3 Dense 71.6, M3 Dense+Sparse 71.6, M3 All 71.8 — [arXiv 2402.03216](https://arxiv.org/html/2402.03216)
- 저자의 설명: "although M3-Embedding (Sparse) is still better than BM25, it performs badly compared with other methods. This is because there are only very limited co-existed terms for cross-lingual retrieval as the query and passage are presented in different languages." [원문 확인, §4.2]
- **주의**: 이 표의 "Sparse"와 "Dense+Sparse"는 BM25가 아니라 M3 모델이 내는 학습된 sparse 가중치와 dense 점수의 결합이다. BM25는 별도 기준선 행으로만 있고, BM25 + dense 조합은 이 논문에 없다.
- 반대로 단일 언어(MIRACL 한국어)에서는 M3의 결합이 이득이었다: M3 Dense 69.9 → Dense+Sparse 71.2 → All 72.1 [원문 확인, Table 1]
- Goworek et al. (2025, 프리프린트) — [arXiv 2511.19324](https://arxiv.org/pdf/2511.19324)
  - "Without translation (Figure 3a), BM25 retrieves almost no relevant documents for non-English pairs, as expected for methods that depend on shared lexical forms." [원문 확인, §4.2, mMARCO]
  - "reliance on BM25 without translation reduces effectiveness to near zero for most non-English pairs" [원문 확인, §4.2]
  - Table 6의 BM25 Recall@10 [원문 확인]: CLIRMatrix EN-ES 31.4, EN-ZH 0.0, AR-RU 1.7, JA-EN 3.1 / mMARCO EN-ES 29.8, EN-ZH 0.0, AR-RU 5.3, JA-EN 0.2
  - "Lexical overlap is often non-existent across scripts" [원문 확인, §1]
  - BM25 성능은 언어 간 유사도와 강하게 상관한다: "BM25 retrieval correlates strongly with features associated with typological proximity ... reflecting its reliance on surface-form overlap." [원문 확인, Table 8 설명]
  - **이 논문에서 한국어는 Large-Scale 데이터셋(영어 질문만)에만 들어 있다** [원문 확인, Table 1]. 한국어 쌍의 BM25 수치는 본문 표에서 확인하지 못했으므로 위 수치를 한국어 결과로 읽으면 안 된다.
- Yang et al. (2024): 다국어 문서 풀에서 BM25는 질문과 같은 언어 문서를 주로 돌려준다(1번 질문의 Figure 6 설명 참조) [원문 확인, §4.3] — [ACL Anthology](https://aclanthology.org/2024.mrl-1.23.pdf)
- XOR QA 계열 시스템이 BM25는 질문 언어 안에서만 쓰고 교차 언어는 dense에 맡겼다는 설명(MIA 2022 Shared Task 제출, [arXiv 2207.01940](https://arxiv.org/pdf/2207.01940))과, Mr. TyDi에서 sparse-dense 하이브리드가 BM25보다 나았다는 설명([arXiv 2108.08787](https://arxiv.org/pdf/2108.08787))은 [2차 출처만, 검색 요약]이다. Mr. TyDi는 단일 언어 벤치마크다.

### Inferences
- MKQA에서 BM25가 0이 아닌 27.9인 이유를 두 논문 모두 설명하지 않는다. 한국어 질문 안에 로마자 이름, 약어, 숫자가 섞여 있으면 영어 문서와 토큰이 겹칠 수 있다는 것이 내 추정이다. 따라서 교차 언어 문항마다 "질문과 정답 문서가 공유하는 로마자·숫자 토큰이 있는가"를 표시해 두면 BM25의 정답이 교차 언어 능력 때문인지 토큰 겹침 때문인지 가를 수 있다.
- 한 풀에 한국어·영어 문서가 섞여 있으면 BM25는 사실상 질문과 같은 언어 문서만 올릴 것이다. 같은 사실이 두 언어에 모두 있으면 BM25는 같은 언어 쪽을 찾아 정답을 맞히고, 다른 언어에만 있으면 (토큰 겹침이 없는 한) 못 찾을 것이다. 이 대비는 "근거가 다른 언어에만 있는 문항"이 있어야만 관찰된다.
- 하이브리드(BM25 + dense)를 순위 융합(RRF 등)으로 묶으면, BM25가 올린 같은 언어의 무관한 문서가 다른 언어의 정답 문서를 밀어낼 수 있다. BGE-M3 논문의 한국어 Dense+Sparse 이득 0.0은 M3 자체 sparse를 가중합한 결과여서 BM25 + dense에 대한 대용 근거일 뿐이고, RRF에서 손해가 나는지를 보여 주는 한국어 수치는 찾지 못했다. 기능을 하나씩 붙여 확인한다는 프로젝트 원칙대로 dense 단독, BM25 단독, 하이브리드를 교차 언어 문항에서 따로 재야 한다.
- 문서 20~30개 풀에서 질문과 공유 토큰이 없는 문서는 BM25 점수가 모두 0이 된다. 이때 상위 k개의 순서는 동점 처리(색인 순서 등)로 정해질 수 있으므로, BM25 점수를 함께 기록하고 점수 0인 문서가 top-k에 든 경우는 검색 성공으로 세지 않는 규칙이 필요하다.
- 한국어 BM25는 형태소 분석기 선택에 따라 단일 언어 성능도 달라질 수 있다. 이번 조사에서 이를 뒷받침할 1차 출처는 확인하지 못했다.

### Gaps
- 한국어 질문과 영어 문서(또는 그 반대)로 BM25 + dense 하이브리드를 평가한 1차 출처는 찾지 못했다. BGE-M3의 MKQA 표는 M3 자체 sparse와의 결합이고, 영어 질문→한국어 문서 방향도 없다.
- RRF 방식 하이브리드의 교차 언어 성능을 보고한 1차 출처를 확인하지 못했다.

## 5. 교차 언어 능력을 분리해 재는 소규모 평가셋 설계 권고와 표본 크기 한계

### Takeaway
교차 언어를 재려는 벤치마크는 근거가 질문 언어에는 없도록 일부러 구성했고(XOR QA, Qi et al., Sharma et al.의 exclusive 사실), 모델의 기억을 배제하려고 가상의 사실이나 문맥 없는 기준선을 썼다. 30문항 규모의 통계는 구간이 매우 넓고, 같은 질문의 번역 쌍은 독립 표본으로 세면 안 된다.

### Cited Findings

**근거를 다른 언어에만 두는 설계**
- XOR QA (Asai et al., 2021): "Multilingual question answering tasks typically assume that answers exist in the same language as the question." / "Questions in our dataset are inherited from TyDi QA ..., which are written by native speakers and are originally unanswerable due to the information scarcity or asymmetry issues." [원문 확인, 초록·§1] — [arXiv 2010.11856](https://arxiv.org/html/2010.11856)
- 표본 추출: "We randomly sample 5,000 questions without any passage answer annotations (unanswerable questions) from the TyDi QA training data" [원문 확인, §2.1]
- Qi et al. (2025): 정답 문서를 다른 언어로만 주고 질문 언어 방해 문서를 붙인 조건을 따로 둔다(2번 질문 인용 참조) [원문 확인, §5] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- Sharma et al. (2024): 한 언어 문서에만 있는 exclusive 사실과 그것을 겨냥한 질문 유형을 따로 둔다 [원문 확인, §2] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)

**같은 질문을 두 언어로, 근거는 고정**
- Yang et al. (2024): 같은 뜻의 질문을 24개 언어로 고정된 다국어 문서 풀에 던진다. 평행 질문의 품질이 중요하다는 결론: 번역으로 만든 평행 질문은 "silver-standard"라고 부른다 [원문 확인, §4.2] — [ACL Anthology](https://aclanthology.org/2024.mrl-1.23.pdf)
- Qi et al. (2025): XQUAD에서는 같은 정답 문단이 여러 언어로 있어 질문 언어만 바꿔 비교한다 [WebFetch 추출, §3] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)

**결과를 근거 언어별로 나눠 보고**
- XOR QA: 교차 언어 문항만 쓰는 과제(XOR-Retrieve, XOR-EnglishSpan)와 둘을 섞은 과제(XOR-Full)를 구분한다 [원문 확인, §3.3] — [arXiv 2010.11856](https://arxiv.org/html/2010.11856)
- Chirkova et al. (2024)와 BordIRLines: 검색 대상 언어 조건별로 표를 나눈다(2번 질문 참조). — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1), [arXiv 2410.01171](https://arxiv.org/html/2410.01171)
- Qi et al.: in-language와 out-language, 그리고 "correct but wrong language"를 따로 보고한다 [원문 확인, Table 3·부록 표 캡션] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)

**기억(parametric knowledge)의 배제**
- Sharma et al.: 사전학습 데이터에 없는 가상의 개체를 썼다 [원문 확인, §2]. 한계로 "we did not probe into the effect of pre-training knowledge"를 든다 [WebFetch 추출, §8]. — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- Qi et al. Table 3 (MKQA, Aya-Expanse-8B, 정답률 %) [원문 확인]: No Ctx 41.4, 1 Gold (in) 73.6, 1 Gold (out) 71.1. 문맥 없이도 41.4%를 맞힌다. **이 표는 언어가 틀린 정답도 정답으로 센다**: "we also consider as valid the questions that were answered correctly but in the wrong language" [원문 확인, §5] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- Chirkova et al.: MKQA 한국어에서 검색 없이 21.5 (character 3-gram recall) [원문 확인한 숫자, 열 순서는 WebFetch 추출] — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)

**채점 방식의 한계**
- Qi et al.: "Our work relies on strict lexical matching to compute model answer accuracy and to detect gold passages." [원문 확인, Limitations] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- Chirkova et al.: 음차 차이 때문에 단어 단위 매칭이 실패한다(2번 질문 인용 참조) [원문 확인] — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)

**작은 표본의 통계**
- Miller, "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations" (arXiv 2411.00640, 2024, 프리프린트) — [arXiv 2411.00640](https://arxiv.org/html/2411.00640)
  - "We suggest reporting the standard error of the mean alongside (beneath) the mean when reporting eval scores." [원문 확인, §2.1]
  - 번역 쌍은 묶음이다: "multilingual evals such as MGSM consist of the same question translated into many languages. Because the inclusion of questions is non-independent, a key assumption of the Central Limit Theorem (or a bootstrap) is violated" [원문 확인, §2.2]
  - "Failure to adjust standard errors for clustered sampling may lead an unsuspecting analyst to suppose that the measurement of the overall eval score is much more precise than it actually is." [원문 확인, §2.2]
  - 두 시스템 비교: "We therefore recommend using the paired version of the standard error estimate wherever practicable." [원문 확인, §4.2]
  - 규모: "new evals should contain at least 1,000 questions in order to have good signaling ability" (저자가 가정한 수치를 넣은 예시 계산이며 "these parameters are fictional"이라고 밝힘) [원문 확인, §5]
- Bowyer, Aitchison, Ivanova, "Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints", ICML 2025 Spotlight Position Paper — [arXiv 2503.01747](https://arxiv.org/html/2503.01747)
  - "In these small-data settings, we demonstrate that CLT-based methods perform very poorly, usually dramatically underestimating uncertainty (i.e. producing error bars that are too small)." [원문 확인, 초록]
  - "We would, therefore, recommend using WS or Bayesian intervals in practice." (WS는 Wilson score) [원문 확인, §3.1]
  - N=100에서도 "95% CLT-based intervals achieve a coverage of only 92.5%" [원문 확인, §3.1]
  - 묶음 자료: "To our knowledge there are no readily available frequentist methods, tailored to such clustered data ... only the Bayesian method based on a clustered model (Eq. 8) achieves the right coverage across different sample sizes." [원문 확인, §3.2]
  - 짝 비교: "We would recommend using the paired Bayes method as it can account for correlations and thus produce narrower intervals." [원문 확인, §3.4]
  - 시뮬레이션이 N = 3, 10, 30, 100을 다룬다는 것과 정답률이 0이나 1 근처일 때 구간이 0으로 줄어든다는 설명은 [WebFetch 추출, §3.1].

### Inferences
아래는 모두 30문항·문서 20~30개 설정에 대한 내 추론이다.

- **구간의 폭.** Wilson 95% 구간을 직접 계산하면 30문항 중 24개 정답(80%)은 62.7%~90.5%, 27개 정답은 74.4%~96.5%다. 교차 언어 문항만 10개라면 8개 정답은 49.0%~94.3%, 5개 정답은 23.7%~76.3%다. 5문항 중 4개 정답은 37.6%~96.4%다. 하위 집합이 10문항 안팎이면 "교차 언어가 단일 언어보다 못하다" 같은 차이를 통계적으로 주장하기 어렵고, 문항별 실패 사례를 읽는 정성 분석이 주된 근거가 된다.
- **번역 쌍의 실효 표본.** 같은 질문의 한국어판·영어판을 둘 다 넣으면 30문항이 아니라 서로 다른 질문 수만큼만 독립 표본이다(Miller §2.2의 논리를 적용한 추론). 대신 짝 비교(같은 질문에서 한국어판은 맞고 영어판은 틀린 경우의 수)는 질문 난이도를 상쇄하므로 작은 표본에서 가장 읽기 쉬운 신호다.
- **지표의 크기 조정.** 논문들의 Recall@100이나 nDCG@10은 문서 수천~수백만 개 풀의 값이다. 문서 20~30개에서는 Recall@100이 자동으로 1이 되므로, 정답 문서의 순위(top-1, top-3 포함 여부)와 상위 k개의 언어 구성만 의미가 있다.
- **기억 배제.** 실제 사실(위키류)을 쓰면 4B~8B 모델도 문맥 없이 맞힐 수 있다(Qi의 No Ctx 41.4, Chirkova의 21.5가 그 가능성을 보여 준다. 다만 둘 다 우리 모델·문서가 아니다). 문항마다 문맥 없는 실행 결과를 함께 기록하거나, 문서에만 있는 사실을 쓰면 이 혼선을 줄일 수 있다.
- **단계 분리.** XOR QA처럼 검색 성공(정답 문서가 top-k 안)과 답 정답 여부, 답 언어를 문항마다 따로 기록하면 30문항에서도 실패가 어느 단계에서 났는지 가를 수 있다.
- **방해 문서.** Qi et al.은 질문 언어 방해 문서가 더 큰 영향을 준다고 보고했다("in-language distractors have a larger impact in most cases" [원문 확인, §5.1]). 교차 언어 문항의 근거가 다른 언어에만 있더라도, 같은 주제의 질문 언어 문서가 풀에 있는지에 따라 난이도가 달라진다. 이 여부를 문항 메타데이터로 적어 두는 것이 좋다.

### Gaps
- 수십 문항 규모의 다국어 RAG 평가셋 설계를 직접 다룬 논문이나 실무 가이드는 찾지 못했다. 위 권고는 큰 벤치마크의 설계 원리와 일반 통계 권고를 옮겨 온 것이다.
- 실무자 글(블로그)은 검색 요약에 몇 개 나왔으나 열어 보지 않았고 근거로 쓰지 않았다.
- Bowyer et al.의 N=30 시뮬레이션 수치(그림에만 있음)는 읽지 못했다.

## 6. 같은 사실이 두 언어 모두에 있을 때, 정답으로부터 무엇을 결론 낼 수 있고 없는가

### Takeaway
같은 사실이 질문 언어 문서에도 있으면, 정답은 "시스템이 다른 언어 문서를 찾아 읽었다"는 증거가 되지 못한다. 검색기와 생성기가 같은 언어 쪽을 더 쓴다는 보고가 있기 때문이다. 이 경우 관찰할 수 있는 것은 교차 언어 능력이 아니라 언어 선호(어느 언어 문서가 뽑히고 쓰였는가)다.

### Cited Findings

- 검색기는 같은 언어 문서를 먼저 올린다: top-10의 68%가 질문 언어 문서 (Sharma et al., 2024) [원문 확인, §4.1]. 저자의 해석: "most multilingual documents do not even reach the context of the LLMs in the generation phase" [원문 확인, §5] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- 두 언어 문서가 함께 주어지면 생성기는 질문 언어 쪽을 더 쓴다: 42% 대 29.58%, 둘 다 쓴 경우는 8.55% [원문 확인, §4.2.1] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- 한 언어에만 있는 사실을 물으면 그 차이가 사라진다: exclusive 질문에서 "Native and Foreign Documents again perform similarly" [원문 확인, §4.2.2]. 저자의 정리: "to generate results from Foreign Documents, the user must issue specific-differential or specific-exclusive queries (queries that specifically target exclusive information in the foreign document)" [원문 확인, §5] — [arXiv 2407.05502](https://arxiv.org/html/2407.05502v1)
- 정답 근거 문단의 수가 결과를 바꾼다: Qi et al. Table 3 (MKQA, Aya-Expanse-8B)에서 1 Gold (in) 73.6, 1 Gold (out) 71.1, 3 Gold (out) 77.7 [원문 확인]. "models provided with 3 out-language gold passages achieve higher accuracy than when provided with a single in-language gold passage in the query language" [원문 확인, §5.1]. 두 가지 주의: (a) 이 표는 언어가 틀린 정답도 정답으로 센다 [원문 확인, §5]. (b) 3개의 gold가 같은 문단의 번역 사본인지 서로 다른 문단인지는 원문에서 확인하지 못했다(MKQA의 다른 언어 gold는 검색된 위키 문단에서 뽑았다는 설명은 WebFetch 추출). 따라서 "번역 사본이 늘면 쉬워진다"의 직접 근거는 아니다. — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- 다른 언어 문서만 줘도 모델은 내용을 꽤 뽑아낸다: "a surprising ability of LLMs to extract relevant information from passages in a different language than the query, but a much weaker ability to produce a full answer in the correct language" [원문 확인, 초록]. "the main barrier appears to lie on the side of generation, namely, whether models can formulate a proper response in the correct target language." [원문 확인, §4.1] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- 실제 위키 기반(MKQA)에서 in/out 차이는 작았다: "in-language gold passages outperform out-language ones, however the gap is much smaller than in XQUAD and almost disappears when also considering the portion of questions that are answered correctly in the wrong language." [원문 확인, §4] — [arXiv 2504.00597v4](https://arxiv.org/html/2504.00597v4)
- 두 언어 문서를 함께 검색하면 성능은 오른다: Chirkova et al.의 MKQA 한국어에서 영어만 32.2, 한국어만 31.5, 둘 다 38.4 [숫자 원문 확인, 열 순서는 WebFetch 추출] — [arXiv 2407.01463](https://arxiv.org/html/2407.01463v1)
- XOR QA는 이 문제를 과제 정의로 처리했다. 교차 언어 능력을 보는 과제에는 교차 언어 문항만 쓰고, 섞인 과제(XOR-Full)는 따로 둔다 [원문 확인, §3.3]. XOR-Full에서도 "Some answers in Xor-Full are translated from English so the same spans may not exist in the target language's Wikipedia." [원문 확인, §3.3] — [arXiv 2010.11856](https://arxiv.org/html/2010.11856)

### Inferences
사용자가 정해야 할 것은 "교차 언어 문항의 근거를 다른 언어에만 둘 것인가, 같은 사실이 질문 언어에도 있어도 되는가"이다. 논문들은 이 선택에 직접 답하지 않는다. 아래는 위 근거에서 내가 끌어낸 것이며 판정이 아니라 각 선택이 무엇을 잴 수 있게 하는지의 정리다.

**선택 A: 근거가 다른 언어 문서에만 있다**
- 결론 낼 수 있는 것: 정답이면 (검색된 문서 로그와 함께 볼 때) 다른 언어 문서를 찾았고 그 내용으로 답했다. 오답이면 검색 실패인지, 읽기 실패인지, 답 언어 실패인지 단계별 기록으로 가를 수 있다.
- 결론 낼 수 없는 것: 모델이 문맥 없이도 아는 사실이면 정답이 교차 언어 읽기의 증거가 아니다. 문맥 없는 실행이 틀리는 문항이어야 한다. BM25가 맞힌 경우는 로마자·숫자 토큰 겹침 때문일 수 있다.
- 선례: XOR QA(XOR-Retrieve), Qi et al.의 out-language gold 조건, Sharma et al.의 exclusive 사실.

**선택 B: 같은 사실이 두 언어 문서에 모두 있다**
- 결론 낼 수 있는 것: 어느 언어 문서가 더 높은 순위로 뽑혔는지(언어 선호), 그리고 답이 맞는지. 검색 로그에 문서 언어를 남기면 "같은 언어 쪽을 뽑았다"는 비율을 셀 수 있다.
- 결론 낼 수 없는 것: 교차 언어 능력. 같은 언어 문서만으로 답할 수 있으므로, 정답은 단일 언어 문항의 정답과 구별되지 않는다. 생성기가 실제로 어느 문서를 썼는지는 답만 봐서는 알 수 없다(두 문서의 내용이 같으므로). 또 근거 문서가 둘이면 그중 하나가 top-k에 들 확률이 근거가 하나인 문항보다 높아지므로 문항이 더 쉬워질 수 있다(확률에 관한 내 추론이며 이를 직접 잰 논문은 없다).
- 선례: Park & Lee, Sharma et al.의 broad·contradiction 질문, Chirkova의 "English + user language" 조건. 이들은 교차 언어 능력이 아니라 선호와 종합 성능을 재려고 이 조건을 썼다.

**둘을 섞는 경우**
- 문항마다 "근거 언어: 한국어만 / 영어만 / 둘 다"를 메타데이터로 고정하고 결과를 이 세 칸으로 나눠 보고하면, A형 문항으로 교차 언어 능력을, B형 문항으로 언어 선호를 따로 읽을 수 있다. 다만 30문항을 세 칸과 두 질문 언어로 나누면 칸마다 5문항 안팎이 되고, 5문항 중 4개 정답의 Wilson 95% 구간은 37.6%~96.4%다. 칸이 늘수록 칸별 수치는 정량 근거로 쓰기 어렵다.
- 같은 사실을 두 언어에 두되 한쪽을 조금 다르게 쓰는 방식(Sharma et al.의 contradiction 사실)은 생성기가 어느 문서를 썼는지 답에서 드러나게 해 준다. 그러나 이는 "충돌 처리"라는 다른 능력을 함께 재게 되므로 교차 언어 능력만 분리한다는 목적과는 다르다.

**공통 주의**
- 어느 선택이든 답 언어(질문 언어로 답했는가)는 정답 여부와 따로 기록해야 한다. Qi et al.에서 다른 언어 문서를 줬을 때의 주된 실패가 내용 이해가 아니라 답 언어였기 때문이다.
- Qi et al.의 "in/out 차이가 작다"는 결과는 aya-expanse-8B 등 7~9B급 모델과 Llama-3.2-3B에서 나온 것으로 우리 모델 크기대와 가깝다. 다만 그 실험의 언어 평균이고 한국어만의 값은 내가 읽지 않았다.

### Gaps
- "같은 사실이 두 언어에 있을 때 정답을 교차 언어 능력의 증거로 볼 수 있는가"를 명시적으로 논한 문장은 어느 논문에서도 찾지 못했다. 위 결론은 각 논문의 설계 선택과 수치에서 끌어낸 추론이다.
- 문서 20~30개 풀에서 사본이 두 언어로 있을 때 top-k 포함 확률이 얼마나 달라지는지 잰 연구는 찾지 못했다.
- Qi et al.의 한국어 행 값(in/out 정답률, 언어가 틀린 정답 비율)은 부록 Table 15에 있으나 이번에 읽지 않았다. A형 문항의 예상 실패 양상을 미리 보려면 그 행을 확인할 가치가 있다.
