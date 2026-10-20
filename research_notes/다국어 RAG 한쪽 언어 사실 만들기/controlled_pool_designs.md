# 다국어 RAG에서 "답이 한쪽 언어 문서에만 있다"는 조건을 풀로 만드는 평가 설계

> **2026-10-21 원문 대조로 바로잡은 값.** 이 노트는 조사한 그대로 둔다. 아래 값은 원문 대조(`verification.md`)에서 바뀌었고, 보고서(`reports/다국어 RAG 한쪽 언어 사실 만들기.md`)는 바로잡은 값을 쓴다. 이 노트의 숫자를 옮겨 쓸 때는 아래를 먼저 본다.
> - DELTA 표 1 비율의 분모(E 등): "논문에 적혀 있지 않다" → 부록 Q에 36,751(질문 2,827개 × 질문 언어 13개)로 적혀 있다. 같은 부록은 정답 출처가 영어 위키백과에서 만든 근거를 언어 간 링크로 옮긴 것이라, 링크가 없으면 0이 된다고 적는다(`verification.md` [153], [164]).

조사일 2026-10-21. 확인 수준 표기는 이전 노트와 같은 방식이다.

- **[원문 확인, §x]**: 논문 원문을 내려받아(arXiv HTML을 텍스트로 바꾸거나 PDF를 pdftotext로 바꿔) 해당 문장을 직접 찾아 읽었다. 따옴표 안 영어는 원문 글자 그대로다. 수식은 텍스트 변환 때 LaTeX 표기(`P_{q}` 등)로 남은 곳이 있다. `...`는 내가 줄인 곳이다.
- **[표 이미지 확인]**: PDF 쪽을 그림으로 바꿔 표의 행과 열을 눈으로 대조했다.
- **[내 계산]**: 원문 표의 숫자로 내가 계산했다(스크립트로 검산).
- **[검색 결과만]**: 검색 결과 요약으로만 봤다. 원문을 읽지 않았다.

"풀"은 이 노트에서 두 가지를 가리킨다. (1) 검색 풀: 검색기가 찾는 문서 모음. (2) 문맥: 검색 없이 모델에 직접 넣어 주는 문서 묶음. 두 가지를 섞어 쓰지 않도록 항목마다 어느 쪽인지 적었다.

이전 노트(`research_notes/다국어 RAG 교차 언어 평가 설계/language_bias_small_set_design.md`)가 이미 다룬 내용은 다시 적지 않는다. 검색기·생성기의 같은 언어 선호 수치(Sharma 68%·42%), Qi et al. Table 3의 in/out 정확도, XOR QA §3.3의 과제 구분, Chirkova의 다섯 검색 조건, MLRS 정의, 작은 표본 통계가 여기에 든다. Sharma et al.은 이전 노트가 v1을 인용했다. 이번에는 최신판 v3(NAACL 2025)를 읽었다.

"Inferences" 항목은 모두 내 추론이다. 문서 20~30개 규모의 풀로 실험한 논문은 찾지 못했다.

## 1. 같은 정보를 다른 언어에 두거나 한 언어판을 빼서, 다른 언어 근거를 찾아 쓰는지 시험한 연구와 그 풀을 만드는 방법

### Takeaway
검색 풀 안에서 문항마다 언어판을 통제한 설계는 드물다. LAReQA는 같은 언어 정답을 빼거나 정답 하나만 남긴다. Goworek et al.은 평행 번역 문서마다 한 언어판만 남긴다. Sharma et al.은 검색 풀에는 모든 언어판을 넣고, 생성 문맥에서만 두 문서 묶음을 서로 다른 언어에 배정한다. 나머지는 대부분 둘 중 하나다. 검색 없이 문맥의 언어만 바꾸거나(Qi, Wu, Ki, MLNeedle, XRAG, CLEAR, X-MADAM-RAG, WiLoVa-QA), 코퍼스 전체의 언어만 고른다(Chirkova, Park & Lee, BordIRLines). 이 분류는 내 분류다.

### Cited Findings

#### A. 검색 풀 안에서 문항 단위로 언어판을 통제한 연구 (Sharma는 검색과 생성을 함께 다루며, 언어 배정은 생성 문맥에서 한다)

**LAReQA** — Roy, Constant, Al-Rfou, Barua, Phillips, Yang, EMNLP 2020. 학회판 첫 쪽으로 학회를 확인했고, 본문은 arXiv v1 PDF로 읽었다. — [ACL Anthology PDF](https://aclanthology.org/2020.emnlp-main.477.pdf), [arXiv 2004.05484](https://arxiv.org/abs/2004.05484)
- 풀을 언어로 통제하나: **예.** 검색 풀 안의 평행 정답 문장을 언어별로 뺀다.
- 목표: "Our goal is to construct a QA retrieval task over a large multilingual pool where many or most of the target answers are found in a different language than the question itself." (뜻: 정답 대부분이 질문과 다른 언어에 있는 큰 다국어 풀의 검색 과제를 만든다) [원문 확인, §3.1] — [arXiv 2004.05484](https://arxiv.org/abs/2004.05484)
- 만드는 순서 [모두 원문 확인, §3.1] — [arXiv 2004.05484](https://arxiv.org/abs/2004.05484)
  1. 평행 QA 세트를 검색 과제로 바꾼다: "we take the existing cross-lingual extractive QA tasks XQuAD and MLQA and convert them into retrieval tasks: XQuAD-R and MLQA-R."
  2. XQuAD는 "each question appears in 11 different languages and has 11 parallel correct answers."(질문 하나가 11개 언어로 있고 평행 정답이 11개)이다. MLQA는 "a variable number (2–4) of parallel correct answers across the corpus"(2~4개)이고 "Contexts surrounding the answer sentence are not guaranteed to be parallel."(정답 문장 주변 문맥은 평행이 보장되지 않음)이다.
  3. 문단을 문장으로 쪼개 모든 문장을 후보로 넣는다: "we break each contextual paragraph into sentences, and include all sentences across the dataset as candidate answers."
  4. 정답 판정: "A sentence is considered a correct answer to a question if it contains the target answer span for either that question or an equivalent question in another language (as identified by qas id)." (그 질문이나 다른 언어 동등 질문의 정답 구간을 담은 문장이 정답)
- **같은 언어 정답 빼기(Remove One Target)**: "for each question, we remove one of its 11 target answers from the multilingual candidate pool. If a model is free of same-language bias, the effect of removing a single target should be constant, regardless of whether the removed target was in the same language as the question or not." (11개 정답 중 하나를 풀에서 뺀다. 같은 언어 편향이 없다면 같은 언어 정답을 빼든 다른 언어 정답을 빼든 효과가 같아야 한다) 조건 이름은 "−same"과 "−rand"다 [원문 확인, §5.2·Table 3 캡션]. 결과: "all our baselines perform better when a random cross-language target is removed (−rand), as compared to the same-language target (−same)". 가장 덜 치우친 모델은 "the X-Y baseline only displays a minimal bias, falling from 0.62 to 0.61 mAP"였다 [원문 확인, §5.2] — [arXiv 2004.05484](https://arxiv.org/abs/2004.05484)
- **한 언어판만 남기기(Limit to One Target)**: "we evaluate on retrieval from a multilingual pool containing just one correct answer. For XQuAD-R, since each question has 11 answers, this means evaluating on each target separately, with the other 10 targets removed from the pool." (정답 하나만 남기고 나머지 10개를 뺀 채 언어쌍마다 따로 잰다) 이때 지표는 "mAP is equivalent to mean reciprocal rank (MRR)"이고, 결과는 질문 언어×정답 언어 히트맵(Figure 4)이다 [원문 확인, §5.2] — [arXiv 2004.05484](https://arxiv.org/abs/2004.05484)
- 지표의 성질: "Any model that ranks all C correct answers in the top C positions (regardless of order) will achieve a perfect 1.0. Note, such a model cannot have strong language bias" (모든 언어의 정답을 위에 올려야 만점이므로 만점 모델은 강한 언어 편향을 가질 수 없다) [원문 확인, §3.2] — [arXiv 2004.05484](https://arxiv.org/abs/2004.05484)

**Goworek, Macmillan-Scott, Özyiğit, "What Drives Cross-lingual Ranking?"** — arXiv 2511.19324 v1(2025-11). 학회는 확인하지 못했다(프리프린트). — [arXiv HTML v1](https://arxiv.org/html/2511.19324v1)
- 풀을 언어로 통제하나: **예.** 평행 번역 문서에서 문서마다 한 언어판만 남겨 다국어 풀을 만든다.
- 순서: "For the mMARCO dataset, we first deduplicated the translated passages across languages, resulting in a pool of 7,433 unique documents. These documents were then evenly distributed across the 14 target languages, assigning exactly one unique passage to each language to ensure balanced representation." (언어를 넘어 번역 사본을 중복 제거해 고유 문서 7,433개를 만들고, 14개 언어에 고르게 나눠 배정했다) [원문 확인, 부록 C]. 본문에도 같은 내용이 있다: "translations are deduplicated across languages and the resulting 7,433 unique documents are evenly redistributed across all 14 languages, assigning 530–531 queries per pair for a total of 97,720 query–document pairs." [원문 확인, §3.1] — [arXiv HTML v1](https://arxiv.org/html/2511.19324v1)
- 주의: "assigning exactly one unique passage to each language"는 글자대로 읽으면 "언어마다 문서 하나"라서 모호하다. "evenly redistributed"와 함께 읽으면 "고유 문서 하나를 한 언어에만 배정"으로 보인다. 이 해석은 내 읽기이고 코드로 확인하지 않았다.
- 검색: "top-100 document retrieval for each query is performed over the full multilingual document pool" [원문 확인, §3.1] — [arXiv HTML v1](https://arxiv.org/html/2511.19324v1)
- 잰 것: "(a) Probability that the model retrieves a document written in the same language as the query." / "(b) Distribution of retrieved document languages when the correct document is not in the query language." (같은 언어 문서를 가져올 확률, 정답 문서가 질문 언어가 아닐 때 가져온 문서의 언어 분포) [원문 확인, Figure 6 캡션] — [arXiv HTML v1](https://arxiv.org/html/2511.19324v1)

**Sharma, Murray, Xiao, "Faux Polyglot"** — NAACL 2025(arXiv 코멘트). arXiv v3로 읽었다. — [arXiv HTML v3](https://arxiv.org/html/2407.05502v3)
- 풀을 언어로 통제하나: **생성 단계에서 예.** 두 문서 묶음을 서로 다른 언어에 배정한다. 검색 단계에서는 사실이 언어별로 배타적이지 않다(아래 Inferences).
- 만드는 순서 [모두 원문 확인] — [arXiv HTML v3](https://arxiv.org/html/2407.05502v3)
  1. 전제(premise)마다 두 판을 만든다: "we created two variants for each premise: “original” and “alternate”. We manually created a set of 10 core facts about the premise for the original set. For the alternate set, we edit these core facts based on the setup of the premise" (original 핵심 사실 10개를 손으로 쓰고, alternate는 그것을 고친다) [부록 A.2]. 두 판의 관계: "There are two versions: original and alternate – each with some shared, contradictory, and exclusive facts." [§2.1.1]
  2. 사실을 늘린다: "we expanded each core facts using OpenAI GPT-4-turbo model where we added a consistency check ... The result was 5 extensions for each core fact, making a total of 50 story facts for the original document set and 50 for the alternate document set on each premise." [부록 A.2]
  3. 문서를 만든다: "we created a total of 14 documents, 7 for each document set in the festival setting ... 2 were long documents ... and 5 were short documents ... The average length of these documents was 484.85 words." [부록 A.2]
  4. 모델 기억에 없는지 확인한다: "prompting each evaluated model with “Tell me about named entity” with temperature = 0 ... We also performed a Google search of the named entities and ensured that no article about the named entities existed as of June 2024." [부록 A.2]
  5. 다국어로 만든다: "For the documents in the festival setting, we repeat the document creation step for each language, where we create a document set in English before translating it into the target language to mimic a real-world setting where the data is not entirely parallel." (언어마다 영어 문서 묶음을 새로 만든 뒤 번역해, 완전히 평행하지 않게 했다) 번역기는 "translate-shell, a Python package that uses Google Translate at the backend"이다 [부록 A.2].
  6. 검색: "We embedded all the documents, got the query embedding for each premise, and obtained the ranked list of documents based on the cosine similarity score." [§2.4]
  7. 생성 문맥: "context = original document set in Languagei + alternate document set in Languagej. Languagei and Languagej are permutations over {en, de, zh, ar, hi}." [§2.4]. 조합 수는 "We had all permutations and combinations of these contexts across the 5 target languages, making it 5 × 5 contexts for each premise"이다 [부록 A.3].
- 어느 문서를 썼는지 재는 법: 기준 답을 두 개 만든다. "We change the context to the original document set for the original reference answer and to the alternate document set for the alternate reference answer." [원문 확인, §3.2.2]. 생성 답을 두 기준 답과 비교해 Original / Alternate / Both / None으로 나눈다 [원문 확인, §3.2.3의 "Source Reference proportion" 문단을 내가 요약; 원문 문장에 오타가 섞여 있어 통째로 옮기지 않았다] — [arXiv HTML v3](https://arxiv.org/html/2407.05502v3)

#### B. 코퍼스 전체의 언어만 고른 연구 (문항별 통제 없음)

**Chirkova, Rau, Déjean, Formal, Clinchant, Nikoulina** — KnowLLM Workshop 2024. 학회는 ACL Anthology 항목 2024.knowllm-1.15를 검색 결과로 확인했다. — [arXiv HTML v1](https://arxiv.org/html/2407.01463v1), [ACL Anthology](https://aclanthology.org/2024.knowllm-1.15)
- 풀을 언어로 통제하나: **문항 단위로는 아니오.** 데이터스토어의 언어만 바꾼다. 다섯 조건은 이전 노트에 있으니 만드는 법만 덧붙인다.
- 문단 만들기: "construct passages by splitting Wikipedia article into chunks of 100 words (or 100 Unicode characters for non whitespace separated languages, namely Chinese, Japanese, and Thai) and prepending the article title to each chunk." [원문 확인, §4 Experimental details] — [arXiv HTML v1](https://arxiv.org/html/2407.01463v1)
- 여러 언어 풀: "In the latter two cases with run retrieval over the embeddings of passages in multiple languages, so that the selected passages may be also in multiple languages." [원문 확인, §5 Table 1 설명 문단] — [arXiv HTML v1](https://arxiv.org/html/2407.01463v1)
- 정답이 어느 언어에 있는가에 대한 저자 설명: "On the MKQA dataset, retrieval from English is more beneficial, which is expected since questions in MKQA were initially written by relying on the English Wikipedia and then translated into other languages." 그리고 "XOR-TyDi QA includes questions grounded in both English and user languages ... and we observe that retrieval from Wikipedia in the user language is more beneficial." [원문 확인, §5 Table 1 설명 문단] — [arXiv HTML v1](https://arxiv.org/html/2407.01463v1)

**Park & Lee, "Investigating Language Preference of Multilingual RAG Systems"** — Findings of ACL 2025(arXiv 코멘트), arXiv v4. — [arXiv HTML v4](https://arxiv.org/html/2502.11175v4)
- 풀을 언어로 통제하나: **아니오.** 자연 위키 데이터스토어를 쓰고, 정보가 어느 언어에 있는지는 통제하지 않는다. 대신 검색된 문서를 번역해 같은 내용을 다른 언어로 바꿔 놓는다.
- 데이터스토어: "we retrieve from two main Wikipedia sources: the KILT version of English Wikipedia and the Wikipedia edition in the user’s native language" [원문 확인, §3.3] — [arXiv HTML v4](https://arxiv.org/html/2502.11175v4)
- 데이터셋: "This dataset is therefore parallel between languages and grounds knowledge primarily in English Wikipedia. In our experiments, we also select a subset of 2.7K samples, overlapping between MKQA and KILT NQ datasets" [원문 확인, §3.1] — [arXiv HTML v4](https://arxiv.org/html/2502.11175v4)
- 같은 정보를 한 언어로 맞추기(생성 실험): "we isolate language effects by providing generators with retrieved passages unified in a single target language—selected from the eight candidates (en, ko, zh, fr, ja, it, pt, es)." 그리고 "In the second, all retrieved passages are unified into a single target language (single-language document set)." [원문 확인, §5.2.1]. 번역기는 "NLLB-200-distilled-600M"이다 [원문 확인, §3.3] — [arXiv HTML v4](https://arxiv.org/html/2502.11175v4)

**BordIRLines** — Li et al., Findings of ACL 2025(arXiv 코멘트), arXiv v3. — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 풀을 언어로 통제하나: **언어 단위로 예.** 문항(영토)마다 색인할 문서와 언어를 정한다. 사실 단위의 배타성은 통제하지 않는다.
- 색인 범위: "In lieu of retrieving over the entirety of the Wikipedia KB, we index only the articles most likely to find relevant information – on the territory, and on each claimant (from the annotations of BorderLines). This greatly reduces the search space and the likelihood of retrieving non-relevant documents." [원문 확인, §3.2] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 문서 단위: "We segmented articles into paragraphs by splitting articles on double newlines, and used these paragraphs as the documents." [원문 확인, §3.2] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 같은 언어 문서를 빼는 모드: "swap_docs adversarially selects documents a language besides the query language"(원문 그대로이며 단어가 하나 빠진 듯하다) [원문 확인, §2.2]. 예시는 "“Ceuta” with es query but ar docs."이다 [원문 확인, 부록 F.2 각주]. 영어만 쓰는 모드: "en_only retrieves only English." [원문 확인, §2.2] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 규모: "720 queries for 251 disputed territories". "Each set consists of the 10 most-relevant documents". "In total, there are 19,916 unique query-document pairs, drawn from 7,436 passages from 905 Wikipedia articles." [원문 확인, §3.1] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 관련성 주석: 사람 주석은 "English, Chinese, Hindi, Spanish, and Korean"의 5개 언어에서 했다 [원문 확인, §3.3 각주]. "On relevance, the LLM judged 21.5% of retrievals to be relevant." 각주는 "Low relevance is expected with IR over real-world documents. We emphasize that the results of RAG do not depend at all on these annotations"라고 적는다 [원문 확인, §3.3] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 관련 문서만 / 비관련 문서만 넣는 조건: "We therefore perform experiments in which we perform RAG with only relevant and non-relevant documents." 이 조건에서는 "We kept only those queries which, after relevance filtering, had 1+ documents."이고, 720문항 중 446문항이 남았다 [원문 확인, 부록 F.3] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)

**Wang et al., "All Languages Matter"** — ACL 2026 main(arXiv 코멘트), arXiv v1. — [arXiv HTML v1](https://arxiv.org/html/2604.20199v1)
- 풀을 언어로 통제하나: **아니오.** 자연 풀의 후보를 언어별로 나눠, 언어 하나만 남긴 문맥으로 상한을 추정한다.
- 풀: "for each query q\in\mathcal{Q}, we retrieve documents from a unified multilingual corpus that contains documents from all evaluation languages (13 languages in total)." [원문 확인, §2.1] — [arXiv HTML v1](https://arxiv.org/html/2604.20199v1)
- 언어별 오라클: "the pool of 50 retrieved candidates is partitioned by document language. Within each language group, we select the top-5 documents (or fewer if insufficient candidates exist) to generate a language-specific answer. The final performance for query q is defined as the maximum score achieved across all language groups" (후보 50개를 언어별로 나누고 언어마다 상위 5개로 답을 만든 뒤, 가장 좋은 언어의 점수를 상한으로 삼는다) [원문 확인, §2.1] — [arXiv HTML v1](https://arxiv.org/html/2604.20199v1)

**Moon et al., "Quality-Aware Translation Tagging in Multilingual RAG system"** — EMNLP 2025 MRL Workshop(arXiv 코멘트). — [arXiv HTML v1](https://arxiv.org/html/2510.23070v1)
- 풀을 언어로 통제하나: **아니오.** 한국어를 포함한 자연 위키 색인이다: "We construct our document index from Wikipedia, comprising 25M English, 1.6M Korean, 1.5M Finnish, and 11M Chinese examples." [원문 확인, §4] — [arXiv HTML v1](https://arxiv.org/html/2510.23070v1)

#### C. 검색 없이 문맥의 언어를 문항 단위로 통제한 연구

**Qi, Fernández, Bisazza** — MRL Workshop 2025 Best Paper(arXiv 코멘트), arXiv v4. in/out 결과 수치는 이전 노트에 있다. — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- 풀을 언어로 통제하나: **후보 풀은 자연 검색으로 만들고, 모델에 주는 문맥을 통제한다.** 통제하는 것은 정답 문단과 방해 문단의 언어와 개수다.
- 후보 풀 만들기: "we construct the set of relevant passages P_{q} by performing in-language retrieval for the L parallel versions of q in each language and taking the union of the top-30 ranked passages in each language" (평행 질문의 각 언어판으로 그 언어 위키에서 상위 30개를 뽑아 합친다) [원문 확인, §3.2] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- 정답 문단 표시와 문항 거르기: "we tag the gold passages in P_{q} based on whether they contain the gold answer as a substring". 그리고 "we only consider queries for which P_{q} contains at least one gold passage in any of the studied languages" [원문 확인, §3.2] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- 단일 문단 조건: "only one gold passage is provided to the model either in the query language (in-language; ...) or in a different language (out-language; ...)". XQUAD에서는 "we iterate over the 11 out-language passage versions for each query and report the average accuracy"다. MKQA·GMMLU는 평행 정답 문단이 없으므로 "we randomly sample 3 different out-language passages from P_{q} and report accuracy averaged over the 3 single-passage answers."다 [원문 확인, §4] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- 다중 문단 조건: "we set the maximum number of passages to 4 and simulate two practical scenarios: (i) a weak retriever finds one out-language gold passage while the other three are distractors; (ii) a strong retriever finds three out-language gold passages while the remaining one is a distractor. In both cases, we compare accuracies when the distractors are in-language vs. out-language." [원문 확인, §5] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)

**Wu et al., "Not All Languages are Equal" (Futurepedia)** — arXiv 2410.21970 v1(2024-10). 학회는 확인하지 못했다. — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1), [arXiv PDF v1](https://arxiv.org/pdf/2410.21970v1)
- 풀을 언어로 통제하나: **검색 풀이 없다.** "During evaluation, we simplify the retrieval process by directly providing the gold documents." (평가 때 검색을 생략하고 정답 문서를 직접 준다) 문서 안에서만 덩어리를 고른다: "Each document is divided into 200-token chunks, and we employ mcontriever-msmarco as the retriever to select the 5 most relevant chunks for the QA as context for length control." [원문 확인, 부록 B] — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)
- 만드는 순서 [원문 확인, §2.1] — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)
  1. "we collect Wikipedia documents created from January 2018 to April 2024 in eight languages: English (en), French (fr), Spanish (es), Portuguese (pt), Chinese (zh), Japanese (ja), Korean (ko), and Arabic (ar)." 동시에 "we also gather the parallel factual triples from WikiData and utilize GPT-4o to convert them into natural language QA pairs"
  2. 세 단계로 고친다: "Timestamp Modification"(시점을 "random years between 2124 and 2200"으로), "Entities Modification"("generate similar and reasonable entities"), "Translation & Update"("translate the fictional entities into eight languages and then update documents and QA pairs in all languages").
  3. 검수: "For each language, we hire three experts proficient in both English and the target language ... Ultimately, we obtain 197 parallel documents and corresponding QA pairs in eight languages."
- 교차 언어 과제의 의도: "This task imitates the real-world scenario where there are no high-quality documents in the query language" [원문 확인, §2.2] — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)
- 언어마다 답이 다른 지식 선택 과제: "we present RALMs with eight randomly ordered documents in different languages, each providing a distinct answer". 각주는 "Since our data is fictional, we consider all these answers as potentially correct."다 [원문 확인, §3.5]. 언어마다 다른 개체를 만든 지시문: "Given the original entity {ENTITY}, you should provide 8 unique and reasonable entities of the same type as the original entity." [원문 확인, 부록 C] — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)
- 같은 답을 여러 언어에 두는 조건: "we construct an experimental setup that includes k non-English documents containing the same answer, referred to k-voting answer, while the remaining documents still present different answers." [원문 확인, §3.5] — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)

**Ki, Carpuat, McNamee, Khashabi, Yang, Lawrie, Duh, "Linguistic Nepotism"** — ICML 2026(PDF 첫 쪽 "Proceedings of the 43rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026"). — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- 풀을 언어로 통제하나: **검색 없음.** 같은 문서를 한 언어로만 바꿔 넣는 대조 문맥이다.
- 번역으로 평행 문서 만들기: "Since no parallel long-form mRAG datasets are publicly available, we construct multilingual variants ... for each target language ... using Machine Translation (MT)." [원문 확인, §3.1 Step 1]. 번역 품질: "MTℓ is implemented using Google Translate API ... the translation quality remains reasonable, with average COMET quality estimation scores of 0.541." [원문 확인, §3.1] — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- 대조 문맥: "For each statement, we construct contrastive contexts where only the document to be cited, d_{c_i}, is presented in a language ℓ ∈ Leval, while all other evidence documents remain in English." (인용할 문서 하나만 언어 ℓ로 바꾸고 나머지는 영어로 둔다) [원문 확인, §3.2] — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- 거르기와 규모: LLM 판정 3개 중 2개 이상의 동의와 NLI 함의를 둘 다 통과한 문장만 남겼다. "The final pool consists of 792 statements that pass both filters" [원문 확인, §3.1]. 데이터: "We adopt the WebGPT test set (Nakano et al., 2022) (270 queries), with relevant evidence documents for each query collected by human annotators using Bing." 그리고 "we only use queries with K < 10 evidence documents." 대상 언어에 한국어가 들어 있다 [원문 확인, §4] — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- 한국어 행(Table 1, 인용 정확도 %, 괄호는 같은 문서가 영어일 때와의 차이) [표 이미지 확인]: LLaMA-3.1 8B 61.7 (−5.68)\*, Qwen-3 8B 49.7 (−12.9)\*\*\*, Aya23 8B 42.2 (−17.8)\*\*\*, Qwen-3 14B 70.3 (−12.7)\*\*\*, Gemma-3 27B 77.5 (−8.71)\*\*\*, LLaMA-3.3 70B 69.2 (−16.7)\*\*\*. 영어 기준값은 순서대로 67.4, 62.6, 60.0, 83.0, 86.2, 85.9다. 별표는 Bonferroni 보정 t-검정 결과다(\*: p<0.05, \*\*\*: p<0.001). — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- 초록 결론: "models sometimes trade-off document relevance for language preference" [원문 확인, 초록] — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)

**Hengle, Bajpai, Dan, Chakraborty, MLNeedle** — NAACL 2025. — [ACL Anthology PDF](https://aclanthology.org/2025.naacl-long.267.pdf), [arXiv HTML v1](https://arxiv.org/html/2408.10151v1)
- 풀을 언어로 통제하나: **검색 없음(긴 문맥).** 정답 문서(needle)의 언어·위치와 방해 문서(haystack)의 언어를 따로 바꾼다.
- 설계: "Among these documents, exactly one contains the correct answer to the question Q, while the remaining K-1 distractor documents do not." 또 "The content of N and H remains unchanged, only the language varies." 그리고 "The language of the question is kept fixed in English." [원문 확인, §2.1] — [arXiv HTML v1](https://arxiv.org/html/2408.10151v1)
- 평행 정답 문서의 출처: MLQA를 골랐다. 이유는 "each question-answer pair is present in multiple languages"이다 [원문 확인, §2.2]. 방해 문서: "we use multilingual sentence-BERT ... to retrieve K-1 documents from mMARCO that are most relevant to the question but do not contain the answer." [원문 확인, §2.2] — [arXiv HTML v1](https://arxiv.org/html/2408.10151v1)
- 한 요인씩 바꾸기: "To isolate the effects of needle language, we keep the distractor passages (H) in English." 그리고 "We keep the language of the needle constant, as English, and then systematically change the language of the haystack." [원문 확인, §3.2–3.3] — [arXiv HTML v1](https://arxiv.org/html/2408.10151v1)

**Liu, Trenous, Ribeiro, Byrne, Hieber, XRAG** — Findings of EMNLP 2025(ACL Anthology 페이지로 확인). — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1), [ACL Anthology](https://aclanthology.org/2025.findings-emnlp.849/)
- 풀을 언어로 통제하나: **검색 없음.** 정답 문서와 방해 문서를 정해 준다. 다국어 설정에서는 답에 필요한 정보를 영어 문서와 질문 언어 문서에 나눠 둔다.
- 정보를 나눠 두기: "The supporting articles each contribute partial information needed to answer the question, and only together do they provide a complete answer" [원문 확인, §3]. 언어 배치: "In the multilingual retrieval setting, each question will have one supporting document and three distracting documents in English, and the same again in the question language." [원문 확인, §4.4]. 질문 언어는 {de, es, zh, ar}이다 [원문 확인, §3 수식] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)
- 다국어 문서 짝: "we use international events from Wiki 2024 and a multilingual dense retriever to search across different languages for articles related to the events. We then group articles in different languages about the same event to form related article pairs." [원문 확인, §4.1] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)
- 방해 문서가 답을 담지 않게: "we select distracting documents that are published at least two weeks before the supporting articles to ensure that the distracting documents do not answer the question." [원문 확인, §4.4] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)
- 통제 분석: "we successively replace the question, supporting articles, and distracting articles by their English counterparts from the monolingual RAG baseline." 결과: "replacing non-English supporting articles with their English translations improves average accuracy noticeably" [원문 확인, §5.4] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)

**Zhao, Huang, Chen, You, Yu, CLEAR ("When Abundance Conceals Weakness")** — arXiv 2601.07041 v1(2026-01). 프리프린트이고 학회는 확인하지 못했다. — [arXiv HTML v1](https://arxiv.org/html/2601.07041v1)
- 풀을 언어로 통제하나: **검색 없음.** 근거 문단의 언어를 바꾼다. 한국어는 대상이 아니다: "\mathcal{L}=\{\text{af, bn, de, fr, is, ja, sw, zh, tr, en}\}" [원문 확인, §3.1] — [arXiv HTML v1](https://arxiv.org/html/2601.07041v1)
- Task 3: "we replace same-language evidence with evidence written in a different language." Task 4: "we present the model with two explicitly contradictory evidence sources expressed in different languages. Using a symmetric 2 × 2 permutation design for each language pair, we control for query-language bias and isolate source competition." [원문 확인, §3.2] — [arXiv HTML v1](https://arxiv.org/html/2601.07041v1)
- 정답 개체의 배치 제약: "the ground-truth entity must appear explicitly in supportive evidence and be absent or replaced in conflicting evidence." [원문 확인, §3.1] — [arXiv HTML v1](https://arxiv.org/html/2601.07041v1)

**Kang, Fu, Zhao, X-MADAM-RAG / X-RAMDocs-ZHEN** — arXiv 2606.12903 v1(2026-06). 프리프린트다. — [arXiv HTML v1](https://arxiv.org/html/2606.12903v1)
- 풀을 언어로 통제하나: **검색 없음.** 조건별로 증거 조각을 만들어 준다. 자세한 내용은 2번 질문에 있다.

**Pei, Peng, Blaschke, Litschko, Plank, WiLoVa-QA** — LREC 2026(arXiv 코멘트). — [arXiv HTML v1](https://arxiv.org/html/2603.14782v1)
- 풀을 언어로 통제하나: **검색 없음.** 같은 주제의 두 언어(변이형) 문서 중 무엇을 문맥에 넣을지 바꾼다. 사실은 자연 문서에서 사람이 찾았다(D절).
- 문맥 조건: "(1a) question-only: asking the question without any additional context information; (1b) +standard: providing lead section text from the Wikipedia article in the standard language as context; (1c) +local: providing lead section text from the Wikipedia article in the local language; (1d) +standard+local: providing lead section texts from both the standard and the local from Wikipedia articles." 번역 조건도 있다: "To isolate retrieval deficiencies attributable to cross-lingual retrieval rather than context information, we additionally assess (1e) +local (translated)" [원문 확인, §4] — [arXiv HTML v1](https://arxiv.org/html/2603.14782v1)

#### D. 자연 문서에서 "한쪽 언어에만 있는 사실"을 찾아 쓴 연구

**WiLoVa-QA**(위 논문)의 만드는 순서 [모두 원문 확인] — [arXiv HTML v1](https://arxiv.org/html/2603.14782v1)
1. 문서 짝 맞추기: "We obtain 111.6K and 24.6K aligned Wikipedia pages for Cantonese-Mandarin (yue-cmn) and Bavarian-German (bar-deu)" [§3.2]
2. 지역어 쪽이 더 긴 짝만 남긴다: "we only keep Wikipedia pairs for which both the lead section ... and the whole document in the local language edition are longer than those of the corresponding page in the standard language." 그 결과 "only 5.38% (6.2K/111.6K) and 4.07% (1.0K/24.6K) of yue-cmn and bar-deu pairs remained." [§3.2]
3. 번역본과 구조 불일치를 뺀다: "(i) translated, if the local page seems to be a direct translation of the standard page ... and (ii) structural mismatch ..." 비율은 "more than half of inspected bar-deu pages, 52.5% (261/497), are nearly direct translations, whereas only 26.6% (61/229) for yue-cmn pages."이고, 남은 것은 "only 18.9% (94/497) of bar-deu pairs contain distinctive content ... more than half of yue-cmn pairs, 59.8% (137/229)"이다 [§3.2].
4. 사람이 두 판의 첫 단락(lead section)을 대조한다: "For each pair of lead sections, we ask annotators to identify 2-3 pieces of information that are present only on the local side and missing on the standard side." [§3.3]. 첫 단락을 쓴 이유: "Wikipedia lead sections typically range from a few dozen to a few hundred tokens ..., making it feasible for annotators to compare pages from two language varieties" [§3.3]
5. 질문 쓰기 규칙: "(a) are as diverse as possible, (b) can be answered with a short phrase, and (c) make sense as stand-alone questions." 그리고 "we ask annotators to avoid frequently composing questions that ask for the year/date of an event or require multi-hop reasoning." [§3.3]
6. 규모: "137 yue-cmn and 94 bar-deu article pairs were annotated." [§3.3]

**Goldman et al., ECLeKTic** — arXiv 2502.21228 v3(2025-11). 학회는 확인하지 못했다. 검색 없는 closed-book 과제다. — [arXiv HTML v3](https://arxiv.org/html/2502.21228v3)
- 풀을 언어로 통제하나: **해당 없음.** 문서가 존재하는지로 "한 언어에만 있음"을 정한다.
- 고르는 법: "we selected articles in Wikipedia that only exist in one of the 12 target languages, and not in any of the others (English, French, German, Hebrew, Hindi, Indonesian, Italian, Japanese, Korean, Mandarin Chinese, Portuguese, and Spanish)". 조건은 "we analyzed the July 2023 dump of Wikipedia and for each language sampled 100 articles that contain at least 200 characters, had at least 100 views during 2023, and most importantly do not have equivalent articles in any of the other 11 languages."이다 [원문 확인, §2] — [arXiv HTML v3](https://arxiv.org/html/2502.21228v3)
- 질문 만들기와 검수: Gemini가 첫 10문장으로 질문·답을 제안하고 주석자가 확인한다. 그다음 11개 언어로 자동 번역하고 번역 전문가가 검수한다. 투입량은 "the human annotation effort amounted to 400 cumulative hours, performed by a team of 27 annotators."다 [원문 확인, §2]. 규모: "4608 question/answer pairs in 12 languages. 4224 of which are evaluated as target examples ... and 384 are questions in their source language" [원문 확인, §2.2] — [arXiv HTML v3](https://arxiv.org/html/2502.21228v3)
- 일반 과학 주제를 빼는 지침: "mark as “to remove” also articles that relate to general topics like science or sociology. Note that a question in, e.g., German about a German biologist counts as a question that relates to the language and not a general scientific question, but a question about natural phenomena – should be removed." (과학·사회학 같은 일반 주제는 지운다. 독일 생물학자에 대한 독일어 질문은 남기지만, 자연 현상에 대한 질문은 지운다) [원문 확인, 부록 A.1] — [arXiv HTML v3](https://arxiv.org/html/2502.21228v3)

**Samir, Park, Field, Shwartz, Tsvetkov, InfoGap** — EMNLP 2024(arXiv 코멘트 "To appear at EMNLP'24"). — [arXiv HTML v1](https://arxiv.org/html/2410.04282v1)
- 풀을 언어로 통제하나: **해당 없음.** 같은 주제의 두 언어 문서에서 한쪽에만 있는 사실을 찾는 도구다.
- 순서: GPT-4로 문단을 사실로 쪼갠다. 다음으로 LaBSE로 사실을 정렬한다(문단 그래프로 후보를 줄이고 hubness를 보정). "Overall, this process enables us to retrieve k=2 facts from F that may convey the same information as e_{i}." 마지막으로 GPT-4가 함의를 판정한다 [원문 확인, §2.1–2.2]. GPT-4를 쓴 이유: "to our knowledge there are no publicly available models that can determine the entailment between a premise and a hypothesis in different languages." [원문 확인, §2.2] — [arXiv HTML v1](https://arxiv.org/html/2410.04282v1)
- 겹침 정도의 예: "The median of the distribution is 0.35, indicating that for half of the biographies, only 35% of the information in the En article can be found in the Fr article." 반대 방향은 "the median of the Fr → En distribution is 0.55"다 [원문 확인, §3.2] — [arXiv HTML v1](https://arxiv.org/html/2410.04282v1)

**Asai et al., XOR QA** — NAACL 2021. 이전 노트에 없던 만드는 법만 적는다. — [arXiv HTML](https://arxiv.org/html/2010.11856)
- "답할 수 없음"의 정의: "A question is unanswerable in TyDi QA if an annotator cannot select a passage answer (a paragraph in the article that contains an answer)." [원문 확인, §2.1.1] — [arXiv HTML](https://arxiv.org/html/2010.11856)
- 영어에서 답 찾기: "We first run Google Search to retrieve as many as top 10 Wikipedia articles, resulting in 387 paragraphs per question on average. We score them with Path Retriever ... and present the five highest scoring paragraphs." [원문 확인, §2.1.3] — [arXiv HTML](https://arxiv.org/html/2010.11856)

#### E. 자연 풀에서 정답이 어느 언어에 있는지를 센 연구 (통제하지 않고 측정)

**Park, Kim, Hwang, Lee, DELTA ("Enhancing Multilingual RAG Systems with Debiased Language Preference-Guided Query Fusion")** — Findings of ACL 2026(arXiv 코멘트), arXiv v3. — [arXiv HTML v3](https://arxiv.org/html/2601.02956v3)
- 세는 법: "Following the MKQA protocol anchored to KILT ..., we identify the location of gold passages (WPIDs) within the multilingual Wikipedia datastore. We report this distribution as Gold Availability, as the number of queries whose gold passage WPID is present in that language’s Wikipedia corpus for each language of query." [원문 확인, §2.2] — [arXiv HTML v3](https://arxiv.org/html/2601.02956v3)
- Table 1 [표 이미지 확인]: 영어 #q 26934, ratio 73.29%다. 한국어 #q 306, ratio 0.83%다. 한국어 행의 Retriever Recall@50은 Base(한국어 질문) 15.62, EN(영어로 번역한 질문) 24.81이다. ratio의 분모는 논문에 적혀 있지 않다. en·ar·ko 세 행은 모두 #q ÷ 36,751로 재현된다 [내 계산; 분모의 뜻은 확인하지 못함]. — [arXiv PDF](https://arxiv.org/pdf/2601.02956)
- 결론: "for a vast majority of queries, English Wikipedia also serves as the sole repository of ground-truth, inducing a dominant gold availability prior." (대부분의 질문에서 정답 근거가 영어 위키에만 있다) [원문 확인, §2.2] — [arXiv HTML v3](https://arxiv.org/html/2601.02956v3)
- 지역 관련 질문: "about 20% of these queries have gold pages only in the corresponding local Wikipedia." [원문 확인, §2.3]. Table 2 캡션은 "Local-gold coverage by predicted L_loc"이고 ko는 12.50%다 [표 이미지 확인]. 본문은 "only in"(그 언어에만)이라고 쓰고, 표 정의는 "p(gold WPID exists in local Wikipedia | L_loc)"(그 언어에 있음)다. 원문만으로는 둘이 같은 양인지 분명하지 않다. — [arXiv HTML v3](https://arxiv.org/html/2601.02956v3)

**Qi et al. Table 6** — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- 정의: "# Inlang: Number of queries having gold passages retrieved from the corpora of the query language. # Outlang: Number of queries having out-language gold passages. ... # Overlap: Number of queries that have useful information retrieved from both in-language and out-language corpora." [원문 확인, Table 6 캡션] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- MKQA 한국어 질문: Inlang 2934, Outlang 5947, Overlap 2930, 전체 5951이다 [원문 확인, Table 6]. 셋으로 나누면 한국어 문단에만 4, 다른 언어 문단에만 3017, 둘 다 2930이다 [내 계산]. 영어 질문은 영어에만 164, 다른 언어에만 620, 둘 다 5167이다 [내 계산]. 여기서 "다른 언어"는 영어만이 아니라 연구한 다른 23개 언어 전체다. 이 숫자는 그 사실이 위키에 있는지를 센 것이 아니다. 언어마다 상위 30개로 검색한 문단(P_q) 안에 정답 문자열이 나왔는지를 센 것이다(§3.2의 P_q 정의와 정답 표시 규칙). 그래서 "한국어 문단에만 4"는 "한국어 위키에만 있는 사실이 4개"라는 뜻이 아니다. — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- 저자 문장: "only out-language gold passages are available for most of the queries (e.g., 88% in Khmer MKQA and 91% in Yoruba GMMLU)" [원문 확인, §3.2] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)

#### F. 확인했지만 이 질문의 "풀 통제"와 맞지 않는 것
- **Yang, Jänich, Mayfield, Lawrie, "Language Fairness in Multilingual Information Retrieval" (PEER)** — SIGIR 2024 short(arXiv 코멘트). 문서 풀이 아니라 순위 목록에 붙은 언어 표시를 바꿔 지표를 검증한다: "We used NeuCLIR’22 runs to create new synthetic runs with relevant documents in the same positions, but with languages assigned to the relevant documents either fairly or unfairly." [원문 확인, §4.2] — [arXiv HTML v1](https://arxiv.org/html/2405.00978v1)
- **Huo et al., "Breaking Language Preference in Multilingual RAG via Language-Controllable Retrieval and Language-Agnostic Reasoning"** — Findings of ACL 2026. 검색 결과 요약으로만 봤다. 요약에 따르면 검색 언어를 모델이 고르는 방법론 논문이고, 평가 풀 설계 논문이 아니다 [검색 결과만]. — [ACL Anthology preview](https://preview.aclanthology.org/ingest-acl/2026.findings-acl.374/)

### Inferences
- **분류 (내 분류).** 연구는 통제 지점에 따라 네 가지로 나뉜다.

  | 통제 지점 | 연구 | 우리 과제와의 관계 |
  |---|---|---|
  | 검색 풀 안에서 문항 단위로 언어판 통제 | LAReQA(−same/−rand, Limit to One), Goworek(문서마다 한 언어판) | 우리 설계(검색 풀에서 사실이 한 언어 문서에만 있음)와 가장 가깝다 |
  | 코퍼스 전체의 언어 선택 | Chirkova, Park & Lee, BordIRLines, All Languages Matter(언어별 오라클) | 사실의 위치는 통제하지 않는다 |
  | 검색 없이 문맥 언어 통제 | Qi, Wu, Ki, MLNeedle, XRAG, CLEAR, X-MADAM-RAG, WiLoVa-QA, Sharma(생성 문맥) | 생성 단계만 분리해 볼 때의 선례다 |
  | 자연 문서에서 한쪽 언어에만 있는 사실 찾기 | XOR QA, ECLeKTic, WiLoVa-QA, InfoGap | 사실을 찾는 절차의 선례다 |

- **Sharma의 검색 단계는 배타성을 시험하지 않는다.** 문서 묶음을 다섯 언어로 모두 번역했고 "all the documents"를 임베딩했다. 그러므로 검색 풀에는 모든 사실이 다섯 언어로 다 들어 있다. "한 언어에만 있는 사실" 조건은 생성 문맥(original은 언어 i, alternate는 언어 j)에서만 생긴다. 따라서 Sharma의 검색 결과는 언어 선호 측정이다. 교차 언어로 찾아냈는지는 재지 않는다. (원문 문장들을 조합한 내 추론이다. 문서 170개가 전제·언어별로 어떻게 나뉘는지는 원문에서 찾지 못했다.)
- **LAReQA의 두 조건은 우리 "두 언어 모두" 무리를 통제군으로 쓰는 방법을 보여 준다.** 질문이 한국어일 때, 같은 사실이 두 언어에 있는 문항에서 한국어판만 빼면 −same에 해당한다. 영어판만 빼면 −rand에 해당한다(두 언어뿐이라 rand가 곧 다른 언어). 질문이 영어이면 반대로 영어판을 빼는 것이 −same이다. 그러면 같은 문항으로 "같은 언어 사본이 있을 때와 없을 때"를 짝지어 비교할 수 있다. 우리 풀은 20~30개라서 문항마다 문서를 빼고 다시 색인하는 비용이 작다.
- **Qi의 "언어별 검색 결과 합집합"은 우리에게 필요 없다.** 그 방법은 언어가 많아 교차 언어 검색을 다 할 수 없을 때 쓴 근사다. 저자도 그 근사가 검색 성능을 과대평가할 수 있다고 적었다(3번 질문). 문서 20~30개 풀은 전체를 한 번에 검색할 수 있다.
- **같은 정보를 다른 언어로 두는 설계는 대부분 기계 번역에 기댄다**(Sharma, Ki, Park & Lee, XRAG 통제 분석, WiLoVa 번역 조건). 그러면 번역 품질이 또 하나의 변수가 된다. Ki는 이 변수를 COMET-QE 평균 0.541로 보고했다. 우리 과제처럼 자연 위키 문서를 쓰면 이 변수는 없다. 대신 두 언어 문서의 내용이 다르다는 변수가 생긴다.

### Gaps
- Goworek et al.의 "assigning exactly one unique passage to each language"가 정확히 무엇을 뜻하는지 코드나 데이터로 확인하지 않았다.
- Sharma et al.의 코드·데이터 저장소는 열어 보지 않았다. 문서 170개가 전제·언어별로 어떻게 나뉘는지는 원문에서 찾지 못했다.
- DELTA Table 1의 ratio 분모가 무엇인지 원문에 없다.
- Wu et al.(Futurepedia), Goworek et al., ECLeKTic, CLEAR, X-MADAM-RAG의 게재 학회는 확인하지 못했다(arXiv 판만 확인).
- Huo et al.(Findings of ACL 2026)은 원문을 읽지 않았다.
- 문서 20~30개 규모의 검색 풀에서 언어판을 통제한 연구는 찾지 못했다.

## 2. 한 코퍼스 안에 "두 언어 모두 / 한국어(비영어)만 / 영어만" 문항을 섞은 설계가 있나, 그 이유는

### Takeaway
한국어-영어 검색 코퍼스에 세 무리를 섞은 1차 출처는 찾지 못했다. 가장 가까운 것은 중국어-영어 X-RAMDocs-ZHEN이다. 이 벤치마크에는 "중국어만 정답 근거" 50, "영어만 정답 근거" 50, "두 언어 일치" 50, 충돌 조건 150이 있다. 다만 검색 없이 증거 조각을 주고, 사람 검수가 없는 2026년 프리프린트다. 문항 무리를 한 평가셋에 섞는 이유를 밝힌 것은 XOR QA("실제 질문 분포를 반영하려고")뿐이었다. Sharma와 XRAG는 사실이나 근거를 언어에 걸쳐 나눠 두는 이유로 실제 다국어 정보 환경을 든다.

### Cited Findings
- **X-RAMDocs-ZHEN (Kang, Fu, Zhao, arXiv 2606.12903 v1, 2026)** — [arXiv HTML v1](https://arxiv.org/html/2606.12903v1)
  - 여섯 조건 [원문 확인, §3.2 Table 1; 표의 열은 Display Label / Internal Label / Description / N이고, 아래에는 Internal Label 열을 빼고 칸마다 따로 옮겼다]:

    | Display Label | Description | N |
    |---|---|---|
    | "C1: Chinese-only correct" | "Correct evidence in Chinese." | 50 |
    | "C2: English-only correct" | "Correct evidence in English." | 50 |
    | "C3: Bilingual consistent" | "Both languages support same candidate." | 50 |
    | "C4: Chinese true, EN false" | "Chinese supports reference; English supports competing candidate." | 50 |
    | "C5: English true, ZH false" | "English supports reference; Chinese supports competing candidate." | 50 |
    | "C6: Conflict with optional noise" | "Bilingual conflict; noise present in 34 of 50 cases." | 50 |
  - 과제 정의: "Given a question and a set of Chinese and/or English evidence snippets, the system must produce an answer or a conflict-aware response using only the visible evidence. Evidence may support a single candidate, multiple matching candidates, or incompatible candidates across languages." [원문 확인, §3.1]
  - 규모: "300 samples across 534 evidence documents, split evenly between Chinese and English. Questions are bilingual (175 Chinese, 125 English). Conflicts cover entities (144), dates (101), and numbers (55)." 그리고 "No completed human audit is available." [원문 확인, §3.1]
  - 만드는 법: "The benchmark starts from RAMDocs records, normalizes question, answer, and document fields, renders controlled Chinese–English evidence snippets, assigns one of the six balanced evidence conditions, and replaces private source identifiers with public evidence IDs." [원문 확인, §3.3]
  - 정답 정보 숨기기: "Gold answers, document roles, language roles, condition labels, expected behavior, and supported-answer metadata are hidden from standard prompts and used only for construction and automatic evaluation." [원문 확인, §3.3]
  - 이유로 든 것: 동기는 충돌이다. "In realistic multilingual scenarios, a system may retrieve Chinese and English sources that support different answers to the same question". 과제는 "We focus on a complementary diagnostic question: how do RAG systems behave when evidence in different languages supports conflicting answers?"다 [원문 확인, §1]. 단일 언어 조건(C1·C2)과 두 언어 일치 조건(C3)을 왜 넣었는지 따로 설명한 문장은 찾지 못했다. 원문은 "six balanced evidence conditions"라고만 적는다.
- **Sharma et al. (NAACL 2025)** — 같은 문맥 안에 공유 사실(두 언어 모두)과 배타 사실(한 언어만)이 함께 있다. 문서 묶음 두 개에 "each with some shared, contradictory, and exclusive facts"가 있고, 두 묶음을 언어 i와 j에 배정하기 때문이다 [원문 확인, §2.1.1·§2.4]. 5×5 조합에는 두 묶음이 같은 언어인 경우도 들어간다. 부록 목차에는 "A.6.2 Preference for Both when both context documents are in Foreign Languages"가 있다 [원문 확인, 부록 목차]. — [arXiv HTML v3](https://arxiv.org/html/2407.05502v3)
  - 이유: "The overarching goal of our dataset is to emulate a real-world multilingual information environment where different, sometimes conflicting, facts and perspectives are represented in different languages." [원문 확인, §2.1]. 또 "Documents about the same event in different languages often focus on different or conflicting facts due to cultural differences and historical narratives." [원문 확인, 부록 A.1] — [arXiv HTML v3](https://arxiv.org/html/2407.05502v3)
- **XOR QA (NAACL 2021)** — XOR-Full은 교차 언어 문항과 같은 언어 문항을 섞는다. — [arXiv HTML](https://arxiv.org/html/2010.11856)
  - 이유: "Finally, we mix the annotated cross-lingual data with the same-language data from TyDi QA to reflect the actual question distributions from native speakers (in-language data)." (원어민의 실제 질문 분포를 반영하려고 섞는다) [원문 확인, §2.1.4]
  - 두 무리의 정의: "Cross-lingual data comes from our reannotated questions that did not originally have same-language answers in TyDi QA. In-language data are taken directly from answerable questions in TyDi QA." [원문 확인, §2.2 Table 2 캡션]. "같은 언어" 무리는 "질문 언어 문서에서 답을 찾았다"는 뜻이다. 영어 위키에 같은 답이 없다는 확인은 원문에서 찾지 못했다.
  - 한국어 예: "The first question is unanswerable in Korean Wikipedia, but there is a clear description about who was the prime minister of France at the time in English Wikipedia." 그리고 "In the last question of Table 3, on the other hand, only the Wikipedia of the target language can provide the answer. Xor QA allows for both retrieval paths." [원문 확인, §2.2] — [arXiv HTML](https://arxiv.org/html/2010.11856)
- **WiLoVa-QA (LREC 2026)** — "(1d) +standard+local" 조건은 두 언어 문서를 모두 주되 답은 한쪽(지역어)에만 있게 한다 [원문 확인, §4]. 결과: "Adding a standard lead section (+standard) as context only shows marginal gain (e.g., +3.40 on bar-deu Llama3.1-70B) or even sometimes hurts performance (e.g., -5.45 on yue-cmn Llama3.1-70B), where +local substantially improves QA performance over the baseline (e.g., +27.66 on yue-cmn and +7.38 on bar-deu Llama3.1-70B)." [원문 확인, §4] — [arXiv HTML v1](https://arxiv.org/html/2603.14782v1)
- **XRAG (Findings of EMNLP 2025)** — 한 문항의 답에 필요한 정보를 영어 문서 하나와 질문 언어 문서 하나에 나눈다. 이유: "This corresponds to a cross-lingual RAG scenario where documents in a resource-rich language provide additional information for LLMs to answer questions in a second language." [원문 확인, §3] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)
- **Wu et al. (Futurepedia)** — "k-voting answer"(같은 답을 비영어 문서 k개에 두고 나머지는 언어마다 다른 답) 조건이 "같은 사실이 여러 언어에 있음"과 "한 언어에만 있음"을 한 문맥에 섞는다 [원문 확인, §3.5]. — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)
- **검색 결과 기준의 세 무리 비율(Qi et al. Table 6, MKQA 한국어; 언어마다 상위 30개로 검색한 문단 안에서 정답 문자열이 나온 언어 기준이며, 위키 전체에 그 사실이 있는지를 센 것이 아니다)**: 한국어 문단에만 4, 다른 언어 문단에만 3017, 둘 다 2930(전체 5951)이다 [원문 확인한 숫자로 내 계산]. — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)

### Inferences
- 섞는 이유는 두 갈래다. 하나는 **진단용**이다. X-RAMDocs-ZHEN은 무리마다 50개로 균형을 맞춰 조건끼리 비교한다. 다른 하나는 **실제 상황 흉내**다. XOR QA는 실제 질문 분포를, Sharma는 실제 다국어 정보 환경을, XRAG는 자원이 많은 언어의 문서가 정보를 보태는 상황을 든다. 무리별 개수를 정하는 방식도 다르다. 진단용은 같은 개수로 맞춘다. XOR QA는 자연 비율을 따른다. Sharma는 개수 비율을 정하는 대신 5×5 언어 조합을 모두 돌렸다. 우리 설계가 어느 갈래를 따르는지 정해야 무리별 개수의 근거를 댈 수 있다.
- 자연 비율을 따르면 "한국어만" 무리는 매우 작아질 수 있다. Qi의 MKQA 한국어 질문에서, 언어마다 상위 30개로 검색한 문단 중 한국어 문단에서만 정답 문자열이 나온 경우는 5951개 중 4개였다. 이 수는 "한국어 위키에만 있는 사실"의 수가 아니다. 검색된 문단 안에서 문자열 일치로 센 수다. 또 MKQA는 영어 NQ 질문을 번역한 것이다(Chirkova·Park & Lee·DELTA가 같은 점을 지적). 한국 관련 주제를 일부러 고르면 다르다. DELTA의 지역 관련 질문에서 ko 지역 위키에 정답 출처(WPID)가 있는 비율은 12.50%였다.
- "두 언어 모두" 무리는 X-RAMDocs-ZHEN의 C3처럼 "두 근거가 일치할 때"의 행동을 보는 조건이다. 이전 노트의 결론과 마찬가지로, 이 무리의 정답은 교차 언어 능력의 증거가 아니다. 다만 LAReQA의 −same처럼 같은 문항에서 한쪽 사본을 빼는 짝 조건을 붙이면 같은 문항 안에서 비교할 수 있다(1번 질문의 Inferences).
- 표본 크기: X-RAMDocs-ZHEN은 조건마다 50문항이다. 우리 규모(문서 20~30개)에서는 무리마다 그보다 훨씬 적은 문항이 나온다. 이전 노트의 Wilson 구간 계산이 그대로 적용된다.

### Gaps
- 한국어-영어 검색 풀에서 세 무리를 섞은 1차 출처를 찾지 못했다.
- X-RAMDocs-ZHEN은 사람 검수가 없는 프리프린트다. 단일 언어 조건(C1·C2)과 두 언어 일치 조건(C3)을 넣은 이유를 따로 적은 문장이 없다. "Chinese-only correct"가 "영어 증거가 아예 없음"인지 "영어 증거는 있으나 정답이 아님"인지 표 설명("Correct evidence in Chinese.")만으로는 알 수 없다.
- XOR-Full의 "같은 언어" 문항이 영어 위키에도 답이 있는지는 확인하지 못했다.

## 3. 통제된 풀이 실제 코퍼스와 다르다는 점(인위성)을 저자들은 어떻게 말하고, 한계로 어떻게 적나

### Takeaway
저자들은 대체로 세 가지를 적는다. (1) 합성·번역 데이터가 실제 데이터와 다르다는 점을 Limitations에 적고, 그 대가로 기억이나 내용 차이를 분리할 수 있었다고 정당화한다. (2) 정답 문서를 직접 주는 설정은 "완벽한 검색"을 가정한 것이라고 밝힌다. (3) "한쪽 언어에만 있다"는 판정이 짝 문서 하나와의 비교에 그친다는 점을 적는다. 통제의 부작용(문장 틀만 보고도 풀리는 문제)을 따로 만든 시험으로 확인한 예도 있다(X-MADAM-RAG).

### Cited Findings
**(a) 합성·번역 데이터의 대가**
- Sharma et al.: "In this study, we use carefully curated artificial tasks to demonstrate an important phenomenon. We modeled our creation on the different information conflicts that we saw in the coverage of controversial topics. However, there are trade-offs to using such synthetic data instead of empirical data. Aligning with tasks such as the Winograd Schema Challenge, our method allowed us to isolate confounding factors such as model’s parametric knowledge." (인위적 과제를 썼고 합성 데이터에는 대가가 있다. 대신 모델 기억 같은 교란 요인을 분리할 수 있었다) [원문 확인, §7 Limitations]. 합성 데이터를 쓴 또 다른 이유: "real-world controversies may activate guardrails in high-resource languages such as English, which can confound our results" [원문 확인, §2 "Need for Synthetic Data"] — [arXiv HTML v3](https://arxiv.org/html/2407.05502v3)
- CLEAR: "Our multilingual datasets are constructed by translating established English benchmarks and verifying semantic fidelity. This choice enables controlled, scalable evaluation, but it does not fully capture phenomena specific to natively authored multilingual data (e.g., culturally grounded entities, language-specific discourse patterns)." (영어 벤치마크를 번역해 만들었으므로 통제는 쉽지만, 원래 그 언어로 쓴 데이터의 특성은 담지 못한다) [원문 확인, Limitations "Translated datasets"] — [arXiv HTML v1](https://arxiv.org/html/2601.07041v1)
- Park & Lee: "This process relies heavily on the quality of the translation model employed." 그리고 "our experiments focus on Wikipedia-based datasets in a specific set of languages, which may not generalize to all linguistic varieties or specialized domains." [원문 확인, Limitations] — [arXiv HTML v4](https://arxiv.org/html/2502.11175v4)
- Ki et al.: "ELI5 was the only publicly available dataset that met the requirements of our setup. To complement this, we additionally run experiments on MIRACL (Zhang et al., 2023) in Appendix K" [원문 확인, Limitations] — [PDF](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- Wu et al.: 기존 데이터를 쓰지 않은 이유로 "existing benchmarks often lack parallel data, fail to provide ground truth answers, and are hindered by time sensitivity."를 든다 [원문 확인, §2.1]. arXiv v1 본문에서 Limitations 절은 찾지 못했다. — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)

**(b) 완벽한 검색을 가정한다는 고백**
- Qi et al., XQUAD를 쓴 이유: "this dataset is the only one allowing us to assess LLMs’ abilities to use the exact same information provided in different languages, simulating an impossible scenario where retrieval works perfectly in all languages." (같은 정보를 여러 언어로 줄 수 있는 유일한 데이터지만, 모든 언어에서 검색이 완벽한 "불가능한 상황"을 흉내 낸다) [원문 확인, §3.1] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- Qi et al. Limitations: "simulating cross-language retrieval by combining results of N in-language retrievers may yield a more comprehensive set of passages than what we could obtain from a single run of a cross-language retriever. While this does not affect our results on the side of context utilization, it may overestimate retriever performance when our findings are applied to real-world mRAG systems." 그리고 "XQUAD was the only one including parallel gold passages, which allowed us to fully isolate the effect of a passage language from that of its content. However, its extractive QA nature makes it less representative of realistic mRAG tasks, highlighting the need to develop better parallel mRAG datasets in future work." [원문 확인, Limitations] — [arXiv HTML v4](https://arxiv.org/html/2504.00597v4)
- XRAG: "Even when given supporting articles—simulating ideal retrieval— ..." [원문 확인, §5.2]. 방해 문서를 넣은 이유: "this simulates a realistic RAG scenario with imperfect retrieval, where we can control the quality of the grounding by the inclusion of distractors." [원문 확인, §3]. 각주: "N.B.: QA pairs are generated by GPT-4o, and evaluation may be biased in its favor." [원문 확인, §5.2 각주]. Limitations: "our multilingual retrieval setting solely covers the scenario of two languages (English and the question language)." [원문 확인, §7] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)
- Wu et al.: "we simplify the retrieval process by directly providing the gold documents." [원문 확인, 부록 B] — [arXiv HTML v1](https://arxiv.org/html/2410.21970v1)
- BordIRLines: 색인을 줄인 효과를 "This greatly reduces the search space and the likelihood of retrieving non-relevant documents."라고 적는다 [원문 확인, §3.2]. Limitations: "the scope of our setting is largely confined to Wikipedia ... Some data leakage is possible, but this is less of a problem for our queries which do not have a definitive answer which can be memorized." [원문 확인, Limitations] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- MLNeedle: "We select the distractor passages (haystacks) purely based on semantic-similarity with the query. We do not experiment with randomly selected distractors" [원문 확인, NAACL판 Limitation] — [ACL Anthology PDF](https://aclanthology.org/2025.naacl-long.267.pdf)

**(c) "한쪽 언어에만 있다" 판정이 미치는 범위**
- WiLoVa-QA: "This simple filtering has some limitations. Our preprocessing and annotation only ensure that the information on the local-language page is absent from the paired standard page. It remains unknown whether such information is attested on other Wikipedia pages of the standard language, in resources outside of Wikipedia, or even in other languages beyond our study." (짝 문서 하나에 없다는 것만 확인했다. 같은 언어의 다른 문서, 위키 밖, 다른 언어에 있는지는 모른다) [원문 확인, §3.2] — [arXiv HTML v1](https://arxiv.org/html/2603.14782v1)
- ECLeKTic은 가정을 본문의 절 하나로 따로 밝힌다: "There are several important assumptions we made in the construction of ECLeKTic, which we make explicit here." 핵심 가정은 "Conversely, we assume that the absence of an article from a certain Wikipedia reflects the lack of interest of online speakers in that topic. The information on that topic is therefore assumed to appear sparsely on the internet, if at all."이다. 결론은 "Together, these assumptions allow us to treat the (non)existence of a fact in Wikipedia as an approximate to the (in)accessibility of that fact to a model trained on online data."다 [원문 확인, §2.1]. Limitations에는 시점 의존성을 적는다: "This makes ECLeKTic somewhat time-dependent, so in the future it would probably require an update." [원문 확인, §7] — [arXiv HTML v3](https://arxiv.org/html/2502.21228v3)
- XOR QA: "questions can be labeled as unanswerable simply because of annotation errors." 이어서 "the answer coverage is underestimated when the search engine fails to retrieve relevant articles (retrieval errors) or the annotator overlooks answer content from the selected articles (answer annotation errors ...)." 그리고 "An annotation procedure that misses too many answers will lead to an artificially small dataset." [원문 확인, 부록 A "Limits of traditional annotation"] — [arXiv HTML](https://arxiv.org/html/2010.11856)
- InfoGap: "it is not guaranteed that similarly high-accuracy can be achieved if we were to apply InfoGap to more specialized domains, where domain expertise may be required to assess the equivalence of two facts in different languages, such as comparing Wikipedia articles concerning scientific topics." (과학 주제처럼 전문 분야에서는 두 언어 사실이 같은지 판단하는 데 전문 지식이 필요할 수 있다) [원문 확인, §6 Limitations] — [arXiv HTML v1](https://arxiv.org/html/2410.04282v1)

**(d) 통제된 조각이 지름길을 만든다는 점**
- X-MADAM-RAG: "a zero-call rule-only extractor reaches 1.0000 on the same benchmark, revealing strong template regularity." (모델 없이 규칙만 쓴 추출기가 만점을 받아, 문장 틀이 지나치게 규칙적임이 드러났다) 이를 시험하려고 문장 틀을 지운 판을 만들었다. 결과는 "On its 100-sample subset, rule-only extraction falls to 0.0000, but X-MADAM-RAG also drops to 0.3000 strict accuracy"였다 [원문 확인, 초록] — [arXiv HTML v1](https://arxiv.org/html/2606.12903v1)
- 같은 논문의 Limitations: "X-RAMDocs-ZHEN uses controlled snippets derived from RAMDocs fields rather than naturally retrieved multilingual passages." 주장 범위는 "Our claims are limited to controlled Chinese-English evidence-conflict diagnosis; we do not claim broad hallucination detection, robustness to natural retrieval, or human-validated faithfulness."로 좁힌다 [원문 확인, §7]. 서론에도 "We do not claim that the benchmark is human-validated, that X-MADAM-RAG solves hallucination detection, or that the results generalize to natural multilingual retrieval."라고 적는다 [원문 확인, §1] — [arXiv HTML v1](https://arxiv.org/html/2606.12903v1)
- XRAG는 문자열 일치로 풀리는 문제를 피하려고 요약에서 질문을 만들었다: "generating questions directly from articles often leads to questions with high overlap in wording, making it easy to answer through string matching" [원문 확인, §4.2] — [arXiv HTML v1](https://arxiv.org/html/2505.10089v1)

**(e) 통제하지 않은 자연 풀의 교란 요인**
- DELTA: "we identify two major confounders: a gold availability prior and cultural priors." 그리고 "Our analysis shows that ground-truth evidence in standard benchmarks is overwhelmingly concentrated in English resources". 기존 측정법에 대해서는 "Critically, these structural factors contaminate existing methods park2025investigating for measuring language preference."라고 쓴다 [원문 확인, §1]. Limitations: "our conclusions are drawn from a Wikipedia-based mRAG setup." [원문 확인, Limitations] — [arXiv HTML v3](https://arxiv.org/html/2601.02956v3)
- All Languages Matter는 DELTA와 엇갈리는 문장을 낸다: "oracle evidence is distributed across multiple languages rather than dominated by any single one." [원문 확인, §1] — [arXiv HTML v1](https://arxiv.org/html/2604.20199v1). 두 논문은 "정답이 어디 있나"를 다르게 정의한다. DELTA는 KILT 출처 ID(WPID)가 그 언어 위키에 있는지를 센다. All Languages Matter는 언어별 문맥으로 만든 답 중 어느 쪽이 가장 좋았는지를 센다. Qi는 언어마다 상위 30개로 검색한 문단 중 정답 문자열이 들어 있는 문단을 센다. 정의의 차이는 원문 확인, 이것이 결론 차이의 원인이라는 해석은 내 추론이다.

**(f) 한계를 어디에, 어떤 형식으로 적었나**
- Limitations 절: [Sharma §7](https://arxiv.org/html/2407.05502v3), [Qi](https://arxiv.org/html/2504.00597v4), [CLEAR](https://arxiv.org/html/2601.07041v1), [X-MADAM-RAG §7](https://arxiv.org/html/2606.12903v1), [XRAG §7](https://arxiv.org/html/2505.10089v1), [BordIRLines](https://arxiv.org/html/2410.01171v3), [Park & Lee](https://arxiv.org/html/2502.11175v4), [DELTA](https://arxiv.org/html/2601.02956v3), [ECLeKTic §7](https://arxiv.org/html/2502.21228v3), [InfoGap §6](https://arxiv.org/html/2410.04282v1), [MLNeedle(NAACL판)](https://aclanthology.org/2025.naacl-long.267.pdf), [Ki](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf), [All Languages Matter](https://arxiv.org/html/2604.20199v1), [Goworek](https://arxiv.org/html/2511.19324v1) [원문 확인, 각 논문]. 그중 Goworek et al.의 Limitations는 데이터셋이 "modest in size, domain coverage and language diversity"라는 점만 적는다. 중복 제거 후 언어별 재배정이라는 인위적 구성에 대한 언급은 찾지 못했다 [원문 확인, Limitations] — [arXiv HTML v1](https://arxiv.org/html/2511.19324v1)
- 본문에 가정 절을 따로 둔다: ECLeKTic §2.1 "Assumptions in ECLeKTic" [원문 확인] — [arXiv HTML v3](https://arxiv.org/html/2502.21228v3)
- 데이터 구성 절 안에서 바로 적는다: WiLoVa-QA §3.2 "This simple filtering has some limitations." [원문 확인] — [arXiv HTML v1](https://arxiv.org/html/2603.14782v1). BordIRLines는 §3.3 각주에 "Low relevance is expected with IR over real-world documents."라고 적는다 [원문 확인] — [arXiv HTML v3](https://arxiv.org/html/2410.01171v3)
- 각 인위 조건이 어떤 실제 상황을 흉내 내는지 이름을 붙인다: Qi "(i) a weak retriever ... (ii) a strong retriever" [§5], Wu "This task imitates the real-world scenario where there are no high-quality documents in the query language" [§2.2], BordIRLines "Each IR mode is motivated by some real-world information access needs a user may have." [§2.2], Sharma "to mimic a real-world setting where the data is not entirely parallel" [부록 A.2] [모두 원문 확인] — [Qi](https://arxiv.org/html/2504.00597v4), [Wu](https://arxiv.org/html/2410.21970v1), [BordIRLines](https://arxiv.org/html/2410.01171v3), [Sharma](https://arxiv.org/html/2407.05502v3)
- 인위성을 따로 시험하는 대조 조건을 둔다: X-MADAM-RAG의 "naturalized stress test" [§3.4], WiLoVa-QA의 "(1e) +local (translated)" [§4], XRAG의 영어 번역 기준선("We also translate non-English supporting and distracting articles into English using Google Translate.") [§5.4], Ki의 MIRACL 재실험 [Limitations] [모두 원문 확인] — [X-MADAM-RAG](https://arxiv.org/html/2606.12903v1), [WiLoVa-QA](https://arxiv.org/html/2603.14782v1), [XRAG](https://arxiv.org/html/2505.10089v1), [Ki](https://www.cs.jhu.edu/~kevinduh/papers/ki26nepo.pdf)
- 주장 범위를 문장으로 좁힌다: X-MADAM-RAG "Our claims are limited to ..." [§7, 원문 확인] — [arXiv HTML v1](https://arxiv.org/html/2606.12903v1)

### Inferences
- **우리 풀에서 가장 직접적인 위험은 WiLoVa-QA가 적은 범위 문제다.** "한국어 문서에만 있다"를 짝 영어 문서 하나와만 비교해 정하면, 같은 사실이 풀 안의 다른 영어 문서에 있을 수 있다. 우리 풀은 20~30개로 닫혀 있다. 그래서 위키 전체를 다룬 WiLoVa·ECLeKTic과 달리 풀 안의 모든 문서와 대조할 수 있다. 이 점은 작은 닫힌 풀의 장점이다. 다만 모델 기억(사전학습 지식)에 그 사실이 있는지는 풀 대조로 알 수 없다. 이 문제는 이전 노트의 "문맥 없는 실행" 항목에 있다.
- **STEM 주제에 직접 걸리는 근거가 세 개 있다.**
  - ECLeKTic은 일반 과학 주제를 아예 지우라고 지시했다. 그런 사실이 특정 언어에 묶이지 않기 때문이다(부록 A.1). 이 지침을 따르면 "자연 현상에 대한 질문"은 제외 대상이다. 한국 과학자·기관처럼 그 언어 화자와 관련된 주제만 남는다.
  - WiLoVa-QA는 bar-deu 짝 문서의 52.5%가 거의 직역이었다고 보고했다. 한국어 STEM 문서가 영어 문서의 부분 번역이면 같은 문제가 생긴다. WiLoVa는 직역 문서를 사람 판단으로 걸렀다.
  - InfoGap은 과학 주제에서 두 언어 사실의 동등성 판단에 전문 지식이 필요할 수 있다고 적었다. 같은 수치도 단위·반올림·기준 연도가 다르면 "같은 사실인가"가 갈린다(이 예는 내가 든 것이다).
- WiLoVa-QA가 연도·날짜 질문을 피하라고 한 이유는 배타성이 아니라 다양성("as diverse as possible")이다. 우리 과제에서 숫자가 두 언어에 다 나온다는 문제와는 이유가 다르다.
- **X-MADAM-RAG의 교훈.** 한쪽 언어에만 있는 사실을 문장을 끼워 넣어 만들면, 그 문장의 틀 때문에 검색이나 답이 쉬워질 수 있다. 규칙만 쓰는 기준선(예: 문자열 일치나 BM25)이 높게 나오는지 보면 이 위험을 점검할 수 있다(내 추론). 자연 위키 문장을 그대로 쓰면 이 위험은 줄어든다.
- **"정답이 어디 있나"의 정의를 미리 고정해야 한다.** DELTA(출처 ID), Qi(정답 문자열), All Languages Matter(답의 질)는 정의가 달라 서로 엇갈리는 결론을 냈다. 우리 과제에서 "이 사실은 한국어 문서에만 있다"를 판정하는 규칙도 결과를 보기 전에 정해야 한다. 이는 CLAUDE.md 3번 규칙과도 맞는다.

### Gaps
- 인위적 풀과 자연 풀의 결과 차이를 수치로 잰 연구는 X-MADAM-RAG의 stress test와 XRAG의 번역 기준선 정도였다. 둘 다 우리 설정(자연 위키 문서, 검색 있음)과 다르다.
- Wu et al.(Futurepedia) arXiv v1 본문에서 Limitations 절을 찾지 못했다. 학회판이 있다면 다를 수 있다.
- 각 논문의 코드·데이터 저장소는 열어 보지 않았다. Qi et al.은 arXiv 코멘트에 "All codes and data are released"라고 적었다.
- 문서 20~30개 풀에서 위 한계들이 얼마나 크게 나타나는지 잰 연구는 찾지 못했다.
