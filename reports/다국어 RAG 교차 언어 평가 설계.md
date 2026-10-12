# 기존 벤치마크는 양쪽 언어 근거를 검증하지 않는다

같은 사실이 두 언어 문서에 모두 있는 경우를 기존 벤치마크는 "막지" 않는다. 조사한 범위에서 "질문 언어 문서에는 답이 없다"를 사람이 검증해 보장한 벤치마크는 하나도 찾지 못했고, 교차 언어 조건은 모두 **검색 대상 문서 묶음(풀)을 다른 언어로만 채우는 방식**으로 만들어졌다. 가장 자주 인용되는 XOR-TyDi QA의 "같은 언어로 답할 수 없는 질문"도 실제로는 "Google 검색 1위 문서 하나에서 주석자가 답 문단을 고르지 못한 질문"이며, 저자 스스로 이 절차가 답의 존재를 과소 추정한다고 적는다. 두 언어 문서를 한 풀에 섞는 벤치마크(XOR-Full, LAReQA, CLIRMatrix MULTI-8, NeuCLIR MLIR)는 어느 언어 근거든 정답으로 인정하고, 채점은 "답이 든 구절을 하나라도 찾았는가"를 보는 계열과 "판정된 관련 구절을 전부 분모에 넣는" 계열로 갈린다. 한편 검색기가 질문과 같은 언어의 문서를 먼저 올린다는 보고가 여러 논문에서 반복된다(다만 한국어 질문에서는 영어 문서 쪽 점수가 더 높게 나온 표와 그 반대인 표가 같은 논문 안에 함께 있다). 그래서 같은 사실이 질문 언어에도 있는 문항에서 나온 정답은 교차 언어 능력의 증거가 되지 못하고 언어 선호를 관찰하는 재료가 될 뿐이다(이 결론은 논문이 직접 말한 것이 아니라 설계와 수치에서 끌어낸 조사자 추론이다). 질문 30개, 문서 20~30개 규모에서는 큰 벤치마크가 하지 못한 전수 확인을 사람이 할 수 있다는 것이 유일한 이점이고, 대신 문항을 근거 언어별로 나누는 순간 칸마다 5~10문항이 되어 수치 차이를 통계적으로 주장하기 어렵다. 30문항 규모의 다국어 RAG 평가셋 설계를 직접 다룬 논문은 찾지 못했으므로, 4절의 권고는 전부 큰 벤치마크의 설계 원리를 옮겨 온 추론이다.

**이 보고서의 표기.** 각 주장 뒤에 확인 수준을 붙였다. 〔원문〕은 조사 노트 작성자가 논문 본문(arXiv·ACL Anthology의 PDF 또는 HTML)에서 해당 문장이나 표의 행을 직접 읽은 것이다. 〔요약〕은 요약 도구가 돌려준 내용, 검색 결과 요약, 다른 논문의 인용으로만 확인한 것이다(공식 문서 페이지를 요약 도구로 읽은 경우도 여기에 넣었다). 〔추론〕은 논문이 말한 것이 아니라 조사자가 끌어낸 것이다. 태그는 직전 태그 이후의 문장들에 적용된다. 4절은 예외로, 절 전체가 추론이고 논문에서 가져온 문장에만 〔원문〕이나 〔요약〕을 붙였다. 영어 인용문은 원문 그대로다. 게재 학회는 확인된 것만 참고 문헌에 적었고, 연도는 확인된 arXiv 날짜를 따랐다.

## 교차 언어 조건은 검증이 아니라 문서 풀 구성으로 만들어졌다

먼저 용어다. 정보 검색 문헌에서 **monolingual(단일 언어)** 은 질문과 문서가 같은 언어인 경우, **cross-lingual(교차 언어, CLIR)** 은 질문과 문서의 언어가 다른 경우, **multilingual(다국어, MLIR) 또는 mixed-language** 는 여러 언어 문서를 한 풀에 넣고 순위 목록 하나를 만드는 경우를 가리킨다. MIRACL은 "monolingual retrieval ... where the queries and the corpora are in the same language ... as opposed to cross-lingual retrieval"이라고 대비하고 ([Zhang et al., 2022](https://arxiv.org/abs/2210.09984)), CLIRMatrix는 CLIR을 "search queries and candidate documents are written in different languages"로 정의하며 ([Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)), MLIR은 "a single ranked list of documents across many languages"를 만드는 과제다 ([Lawrie et al., 2022](https://arxiv.org/abs/2209.01335)). 〔원문〕 다만 "cross-lingual"은 논문마다 세 층위로 쓰인다. 풀 전체가 다른 언어인 경우(XOR-Retrieve, NeuCLIR CLIR), 섞인 풀 안에서 특정 질문의 근거가 다른 언어에 있다는 질문별 딱지(XOR-Full, MIA 2022), 학습 언어와 평가 언어가 다르다는 뜻(MLQA의 XLT)이다. 한국어·영어가 섞인 풀을 쓰는 평가셋의 "교차 언어 질문"은 두 번째 뜻이다. 그리고 **두 언어 모두에 근거가 있는 질문을 가리키는 정해진 용어는 조사한 논문 어디에도 없었다.** 이런 문항을 둔다면 이름을 직접 정의해야 한다. 〔추론〕

### XOR-TyDi QA의 "답할 수 없음"은 1위 문서 하나의 판정이다

XOR-TyDi QA("XOR QA: Cross-lingual Open-Retrieval Question Answering")는 한국어를 포함한 7개 언어의 질문 4만 개로, 교차 언어 질문을 다룬 대표 벤치마크다. 초록은 이 질문들을 "TYDI QA could not find same-language answers for"라고 소개하고, 질문 선정 절(§2.1.1)은 기준을 이렇게 적는다. "A question is unanswerable in TYDI QA if an annotator cannot select a passage answer (a paragraph in the article that contains an answer)." ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)) 그런데 TyDi QA에서 주석자가 본 문서는 질문마다 하나뿐이다. "A Wikipedia article is then paired with each question by performing a Google search on the question text, restricted to the Wikipedia domain for each language, and selecting the top-ranked result." ([Clark et al., 2020](https://arxiv.org/abs/2003.05002)) 〔원문〕 두 인용을 합치면 XOR의 교차 언어 질문은 **"같은 언어 Wikipedia 전체에 답이 없는 질문"이 아니라 "Google 1위 문서 하나에서 답 문단을 못 찾은 질문"** 이다. 〔추론〕 XOR 논문도 부록 A에서 "questions can be labeled as unanswerable simply because of annotation errors"라고, 그리고 이 절차에서 "the answer coverage is underestimated"라고 인정한다 ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)). 〔원문〕 후속 논문 MIA 2022가 이 질문들을 "require evidence only presented in English Wikipedia"라고 요약한 것은 ([Asai et al., 2022](https://arxiv.org/abs/2207.00758)) 〔원문〕 원 절차가 보장하는 것보다 강한 표현이다. 〔추론〕

XOR은 과제를 셋으로 나눈다. **XOR-Retrieve**와 **XOR-EnglishSpan**은 검색 대상이 영어 Wikipedia뿐이어서 질문 언어 문서가 풀에 아예 없다. **XOR-Full**은 질문 언어 Wikipedia와 영어 Wikipedia를 모두 열어 두고 "a system does not know a priori in which language we can find information"이라고 적으며, "XOR QA allows for both retrieval paths", "evidence paragraphs can be found both in the target language and English"라고 양쪽 경로를 명시적으로 허용한다. XOR-Full 평가 데이터는 교차 언어 문항과 같은 언어 문항을 섞고, 앞의 두 과제는 교차 언어 문항만 쓴다 ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)). 〔원문〕 XOR-Full의 같은 언어 문항에 대해 영어 Wikipedia에도 같은 답이 있는지는 확인하지 않았으므로, 두 언어에 다 있는 사실은 딱지 없이 섞여 있을 수 있다. 〔추론〕 한국어 수치로는 짧은 답이 있는 질문 비율이 TyDi QA 29%에서 XOR-TyDi QA 68%로 늘었고, 한국어 교차 언어 평가 문항은 646개, 같은 언어 평가 문항은 505개다 ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)). 〔원문〕

### "없음"은 Wikipedia 규모에서 증명할 수 없다고 논문들이 직접 말한다

MIRACL은 관련 문단을 못 찾은 질문을 버리면서 이렇게 적는다. "just because no relevant passage was found in the top-10 candidates presented to the annotator, it is not necessarily the case that no relevant passage exists in the corpus. ... Short of exhaustively evaluating the corpus (obviously impractical), we cannot conclude with certainty that no relevant passage exists." ([Zhang et al., 2022](https://arxiv.org/abs/2210.09984)) CORA 논문("One Question Answering Model for Many Languages with Cross-lingual Dense Passage Retrieval")은 MKQA에서 "답 없음"으로 표시된 일본어 질문 400개를 사람이 분석했는데, 329개는 질문 자체가 불충분했고 나머지 71개 중 17개는 모델의 답이 맞았다. 각주는 "it is difficult to prove an answer does not exist in the millions of multilingual documents even if the annotation says so"라고 적는다 ([Asai et al., 2021b](https://arxiv.org/abs/2107.11976)). 〔원문〕

### 벤치마크별로 보면 배타성은 모두 풀 구성에서 나온다

아래 표는 조사 노트가 원문에서 확인한 내용만 줄인 것이다. "질문 언어 문서에 답이 없도록 했는가" 열이 핵심이다.

| 벤치마크 | 유형 | 질문 언어 문서에 답이 없도록 했는가 | 같은 내용이 여러 언어에 있을 때 |
|---|---|---|---|
| TyDi QA, Mr.TyDi, MIRACL, NoMIRACL, MIRAGE-Bench | 단일 언어 | 해당 없음(질문과 문서가 같은 언어) | 해당 없음 |
| MLQA (G-XLT) | 교차 언어 독해, 검색 없음 | 문단이 주어지므로 해당 없음 | 병렬 데이터에서 질문 언어만 교체 |
| MKQA | 문서와 무관한 답 주석 | 아니오. 지역에 따라 답이 달라지지 않는 질문을 일부러 고름 | 답을 Wikidata 개체로 통일 |
| XOR-Retrieve, XOR-EnglishSpan | 교차 언어 | 풀이 영어뿐 + TyDi "답 없음" 딱지(전수 검증 아님) | 답 문자열 포함 여부로 채점 |
| XOR-Full | 두 언어 풀 | 아니오. "allows for both retrieval paths" | 답 문자열로 채점, 근거 언어 구분 안 함 |
| LAReQA | 다국어 풀 | 아니오 | 모든 번역판이 정답(질문당 11개) |
| CLIRMatrix BI-139 / MULTI-8 | 교차 언어 / 혼합 | 풀 구성 / 아니오 | Wikidata 링크로 관련도 딱지를 다른 언어판에 전파 |
| NeuCLIR CLIR / MLIR | 교차 언어 / 다국어 | 풀 구성(영어 주제, 비영어 문서) | 한 말뭉치로 보고 순위 목록 하나 |
| Futurepedia | 병렬 문서 재배치 | 과제별 풀 구성 | 8개 언어 병렬(한국어 포함) |
| XRAG 단일 언어 검색 / 다국어 검색 | 교차 언어 RAG | 풀이 영어뿐 / 두 언어 문서가 답의 일부씩 보유 | 근거 2개가 서로 보완 |
| XBCP | 교차 언어 / 다국어 | 근거 문서를 번역해 한 언어로 배치 | 번역으로 통제 |

출처는 순서대로 [Clark et al., 2020](https://arxiv.org/abs/2003.05002), [Zhang et al., 2021](https://arxiv.org/abs/2108.08787), [Zhang et al., 2022](https://arxiv.org/abs/2210.09984), [Thakur et al., 2023](https://arxiv.org/abs/2312.11361), [Thakur et al., 2024](https://arxiv.org/abs/2410.13716), [Lewis et al., 2020](https://arxiv.org/abs/1910.07475), [Longpre et al., 2021](https://arxiv.org/abs/2007.15207), [Asai et al., 2021](https://arxiv.org/abs/2010.11856), [Roy et al., 2020](https://arxiv.org/abs/2004.05484), [Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/), [Lawrie et al., 2024](https://arxiv.org/abs/2404.08071), [Wu et al., 2024](https://arxiv.org/abs/2410.21970), [Liu et al., 2025](https://arxiv.org/abs/2505.10089), [Lu et al., 2026](https://arxiv.org/abs/2606.15345)다. 〔원문〕

표에서 몇 가지는 풀어 둘 가치가 있다. LAReQA는 병렬 번역 데이터를 한 풀에 넣어 "an XQuAD-R question will have 11 relevant answers"가 되게 하고, 그 목적은 "incorrect answers in the same language are preferred over correct answers in a different language"라는 현상을 재는 것이다 ([Roy et al., 2020](https://arxiv.org/abs/2004.05484)). CLIRMatrix MULTI-8은 "Each query will have relevant documents in the other 7 languages"이고, 언어 간 링크가 빠져 관련 문서를 놓칠 수 있다고 인정한다 ([Sun & Duh, 2020](https://aclanthology.org/2020.emnlp-main.340/)). XRAG는 교차 언어 RAG를 "질문 언어와 다른 언어의 문서가 최소 하나 있는 것"으로 정의하고, 다국어 설정에서는 두 근거 문서가 "each contribute partial information needed to answer the question, and only together do they provide a complete answer"가 되게 만든다 ([Liu et al., 2025](https://arxiv.org/abs/2505.10089)). XRAG가 말하는 "monolingual retrieval"은 질문이 비영어이고 검색 문서가 전부 영어인 경우라서 정보 검색 쪽 정의와 충돌하니 인용할 때 주의해야 한다. MKQA는 반대 방향의 설계다. "we reserve our assessment to geographically invariant queries"라고 적어, 언어에 따라 답이 달라지지 않는 질문만 평가한다 ([Longpre et al., 2021](https://arxiv.org/abs/2007.15207)). 〔원문〕

정리하면 교차 언어 조건을 만드는 방법은 세 가지다. 풀을 다른 언어 문서로만 채우는 방법(XOR-Retrieve, NeuCLIR CLIR, XRAG 단일 언어 검색, XBCP 교차 언어), 풀을 섞고 같은 사실의 모든 언어판을 정답으로 세는 방법(LAReQA, CLIRMatrix MULTI-8, XOR-Full), 풀을 섞되 각 언어 문서가 답의 서로 다른 일부만 갖게 하는 방법(XRAG 다국어 검색)이다. 섞인 풀에서 중복을 허용한 벤치마크 가운데 LAReQA와 Faux Polyglot은 중복을 언어 선호를 재는 도구로 일부러 썼고, XOR-Full과 CLIRMatrix MULTI-8은 일반적인 평가를 위해 허용했을 뿐 언어 선호를 따로 재지 않는다. **"검증으로 배타성을 보장한 벤치마크가 없다"는 것은 조사한 범위 안에서 찾지 못했다는 뜻이지 없다는 증명이 아니다.** Wikipedia 언어판 사이에서 한 언어판에만 있는 사실을 직접 찾아내 질문으로 만든 벤치마크도 찾지 못했다. 〔추론〕

XOR이 내세운 "information asymmetry"(다른 문화권의 개체에 관한 정보가 질문자 언어의 Wikipedia에는 덜 실리는 현상)는 질문 구성의 동기이지 선정 기준이 아니다. 논문은 일본어판 Ron Paul 문서에 학위 정보가 없는 예를 들지만 ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)) 〔원문〕 개별 질문이 실제로 비대칭 때문에 답이 없었는지는 확인하지 않았다. 〔추론〕

한국어에 한정하면, 한국어 질문과 한국어 문서가 함께 있는 것은 TyDi QA 계열(Mr.TyDi, MIRACL, NoMIRACL, MIRAGE-Bench)이고, 한국어 질문에 영어 근거를 사람이 주석한 것은 XOR-TyDi QA다. MKQA는 한국어 질문만 있고 근거 문서가 없으며, MLQA·XQuAD·CLIRMatrix MULTI-8·NeuCLIR·XRAG·Faux Polyglot에는 한국어가 없다. 〔원문〕 영어 질문에 한국어 근거를 붙인 방향은 XBCP(기계 번역 근거)와 CLIRMatrix BI-139(자동 생성 딱지)에서만 확인했고, 사람이 주석한 영어 질문·한국어 근거 QA 벤치마크는 찾지 못했다. 〔추론〕

## 근거가 여럿일 때 채점은 "하나면 충분"과 "전부 센다"로 갈린다

검색 지표의 뜻부터 적는다. 검색기가 돌려준 상위 k개 가운데 관련 구절의 비율이 **Precision@k**, 정답으로 표시된 관련 구절 가운데 상위 k개 안에 들어온 비율이 **Recall@k**다. **Hit@k(Success@k)** 는 상위 k개 안에 관련 구절이 하나라도 있으면 1이고, **MRR**은 첫 번째 관련 구절의 순위의 역수를 평균한 값이며, **nDCG@k**는 관련 구절이 위쪽에 놓일수록 높은 점수를 주는 순위 가중 지표다. **qrels**는 "어느 질문에 어느 문서가 관련인가"를 사람이 판정해 둔 목록이다. 검색 방식으로는 질문과 문서가 공유하는 단어를 세는 어휘 기반 방식인 **BM25**와, 문장을 벡터(임베딩)로 바꿔 가까운 것을 찾는 **dense 검색**이 뒤에 나온다.

### 답 문자열 계열은 하나면 충분하고, qrels 계열은 전부를 분모에 넣는다

open-domain QA 계열은 구절 ID가 아니라 답 문자열로 채점한다. DPR("Dense Passage Retrieval for Open-Domain Question Answering")의 top-k 정확도는 "retrieved passages that contain the answer" 기준이고 ([Karpukhin et al., 2020](https://arxiv.org/abs/2004.04906)), XOR-Retrieve는 "the fraction of the questions for which the minimal answer is contained in the top n tokens selected"로 정의한다 ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)). 주석된 구절이 아니어도 답 문자열이 들어 있으면 맞은 것이므로 **질문 단위로 "하나면 충분"** 이고, 근거가 어느 언어였는지는 구분하지 않는다. 〔원문: 인용문, 추론: 해석〕 MS MARCO는 "there is often only one qrel per query"라서 MRR@10을 쓴다 ([Arabzadeh et al., 2021](https://arxiv.org/abs/2109.00062)). 질문당 주석된 양성 구절은 평균 1.1개다 ([Qu et al., 2021](https://arxiv.org/abs/2010.08191)). 〔원문〕 DPR의 정확도가 질문 단위 비율임을 명시한 문장은 노트 작성자가 찾지 못했고 표 설명만 확인했다(확인하지 못한 부분).

BEIR, MIRACL, TREC 계열은 판정된 관련 구절을 전부 qrels에 넣고 nDCG@10과 Recall@100을 쓴다. MIRACL은 상위 10개 후보를 원어민이 이진 판정하므로 한 질문에 관련 구절이 여럿 남을 수 있다 ([Zhang et al., 2022](https://arxiv.org/abs/2210.09984)). BEIR는 nDCG@10을 고른 이유를 설명하면서 판정되지 않은 문서를 비관련으로 본다고 명시한다. "All other unseen documents are assumed to be irrelevant." ([Thakur et al., 2021](https://arxiv.org/abs/2104.08663)) 〔원문〕

이 두 계열의 차이가 "같은 사실을 말하는 구절이 두 언어에 있을 때" 그대로 드러난다. 같은 사실을 담은 대체 구절이 3개(예를 들어 한국어 2개, 영어 1개)인 질문에서 시스템이 1개만 찾으면, Hit@k와 MRR은 만점이고 구절 단위 Recall@k는 1/3이다. 필요한 것을 다 찾았는데도 점수가 낮게 나오는 왜곡이다. 반대로 MRR은 여러 사실이 모두 필요한 질문에서 첫 사실 하나만 찾아도 만점이 되어 실패를 가린다. 〔추론〕

### FEVER는 "모두 필요"와 "대체 가능"을 한 규칙에 담았다

"하나만 찾으면 되는가, 전부 찾아야 하는가"에 가장 직접 답하는 선례는 사실 검증 벤치마크 FEVER다. 근거를 묶음 단위로 주석하고, 한 묶음 안의 문장은 전부 필요하며, 묶음이 여러 개면 완전한 묶음 하나로 충분하다. "all sentences must be selected for the evidence to be marked as correct. ... Some claims may be equally supported by different pieces of evidence; in this case one complete set of sentences should be predicted." ([Thorne et al., 2018](https://arxiv.org/abs/1803.05355)) 공유 과제의 점수도 같은 규칙이다. "Where multiple sets of evidence was annotated in the data, only one set was required for the claim to be considered correct for the FEVER score." ([Thorne et al., 2018b](https://arxiv.org/abs/1811.10971)) FEVER에서 둘 이상의 문장이 적절한 근거로 판정된 주장은 31.75%, 여러 문장의 조합이 필요한 주장은 16.82%였다. 〔원문〕

다른 다중 홉(여러 문서의 사실을 이어야 답할 수 있는 질문) 벤치마크는 대체 근거를 다루지 않는다. HotpotQA는 gold(정답으로 주석된) 지지 문장 집합과의 EM(집합이 정확히 같으면 1)·F1(겹친 정도)을 쓰고 ([Yang et al., 2018](https://arxiv.org/abs/1809.09600)), MultiHop-RAG는 "Hit@K metric measures the fraction of evidence that appears in the top-K retrieved set"라고 서술하며 답 없는 질문은 검색 평가에서 뺀다 ([Tang & Yang, 2024](https://arxiv.org/abs/2401.15391)). 〔원문〕 HotpotQA식 집합 일치는 대체 구절을 골라도 0이 되므로 대체 근거가 있는 평가셋에는 맞지 않는다. 〔추론〕

이 프로젝트가 이미 정한 구조(필수 사실마다 근거 구절을 붙여 적는 방식)는 FEVER의 묶음을 한 단계 분해한 형태다. 필수 사실들 사이는 "모두 필요", 한 사실의 대체 구절들 사이는 "하나면 충분"이 된다. 여기에 대응하는 검색 지표는 "모든 필수 사실에 대해 대체 구절이 상위 k에 하나 이상 있는가"(질문 단위 0/1)와 "상위 k에서 근거가 하나 이상 잡힌 필수 사실의 비율"이다. 이 두 지표와 그 이름(노트에서는 all-facts-covered@k, fact recall@k)은 **조사자가 붙인 것이며 위 논문들이 정의한 지표가 아니다.** "필수 사실마다 대체 근거 구절을 여러 개 적어 두고 검색을 채점"하는 방식을 그대로 정의한 프레임워크는 찾지 못했다. 〔추론〕

RAG 평가 프레임워크는 구절 ID 대신 사실 단위를 센다. TREC 2024 RAG 트랙은 **nugget**(답에 들어 있는지 이진 판정할 수 있는 사실 하나)을 vital(반드시 있어야 함)과 okay(있으면 좋음)로 나누고, 답이 각 nugget을 support, partial_support, not_support 하는지 판정하며, vital nugget만 엄격하게 세는 Vital Strict를 주 지표로 쓴다 ([Pradeep et al., 2024](https://arxiv.org/abs/2411.09607)). RAGChecker의 claim recall은 정답의 주장 가운데 검색된 청크가 담고 있는 비율이고, context utilization은 검색 문맥에 들어 있던 정답 주장 가운데 답에 실제로 쓰인 비율이다 ([Ru et al., 2024](https://arxiv.org/abs/2408.08067)). 〔원문〕 Ragas의 context recall도 정답의 주장 가운데 검색 문맥이 지지하는 비율이다 ([Ragas 문서](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/)). 〔요약〕 사실 단위 지표는 어느 구절이 지지하는지를 묻지 않으므로 대체 근거와 언어 차이를 자연스럽게 흡수하지만, 판정을 LLM에 맡기게 된다. 부분 지지를 0.5로 줄지 0으로 줄지는 두 변형 모두 선례가 있어 결과를 보기 전에 하나로 정해야 한다. 〔추론〕

### 여러 언어에 걸친 근거는 언어와 무관하게 관련으로 센다

다국어 풀에서 확인된 관행은 관련성을 언어와 무관하게 판정하고 순위 목록 하나로 채점하는 것이다. NeuCLIR 2023 MLIR은 "systems should treat the three document collections ... across all three languages as a single corpus"라고 하고 nDCG@20으로 보고하며, 언어별 분석은 따로 한다. "Language fairness for MLIR is not yet a well-defined concept with widely-reported measures." 여기서 제안한 측정은 상위 R개(R은 그 주제의 전체 관련 문서 수)에서 각 언어 문서가 차지하는 비율(exposure)을 그 언어의 관련 문서 비율과 비교하는 것이다 ([Lawrie et al., 2024](https://arxiv.org/abs/2404.08071)). PEER는 같은 관련도의 문서가 언어와 무관하게 같은 순위를 받는지 Kruskal-Wallis 검정으로 본다 ([Yang et al., 2024b](https://arxiv.org/abs/2405.00978)). 〔원문〕 **"질문 언어 근거 재현율"과 "다른 언어 근거 재현율"을 갈라 대표 지표로 보고하는 벤치마크는 조사 범위에서 찾지 못했다.** NeuCLIR MLIR이 번역·중복 문서를 어떻게 처리하는지도 확인하지 못했다. PEER는 30문항·문서 20~30개 규모에서는 표본이 작아 그대로 쓰기 어렵다고 본다. 〔추론〕

### Precision@k는 판정이 빠진 구절을 오답으로 센다

Precision@k에는 고유한 약점이 있다. "these measures make no distinction in pooled collections between documents that are explicitly judged as nonrelevant and documents that are assumed to be nonrelevant because they are unjudged." ([Buckley & Voorhees, 2004](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=150469)) 여기서 "pooled"는 여러 시스템의 상위 결과를 모아 사람에게 판정을 맡긴 후보 집합을 가리키며, 이 보고서에서 말하는 검색 대상 문서 풀과는 다른 뜻이다. 관련인데 목록에서 빠진 구절을 시스템이 가져오면 오답으로 계산된다는 뜻이다. BEIR는 **Hole@10**(상위 10개 중 사람이 판정한 적 없는 구절의 비율)을 재고, TREC-COVID에서 빠진 판정 980쌍을 어느 시스템이 가져온 것인지 가린 채 원래 지침대로 채웠더니 dense 검색기 ANCE의 점수가 0.654에서 0.735로 올라 BM25보다 6.7포인트 높아졌다고 보고한다 ([Thakur et al., 2021](https://arxiv.org/abs/2104.08663)). MS MARCO에서는 양성으로 표시되지 않은 최상위 구절의 70%가 실제로는 양성이었다는 보고가 있다 ([Qu et al., 2021](https://arxiv.org/abs/2010.08191)). FEVER도 "crowd-sourcing annotations of false-positive predictions at a later date"를 권한다 ([Thorne et al., 2018](https://arxiv.org/abs/1803.05355)). 〔원문〕

문서 20~30개 규모는 이 문제를 처음부터 없앨 수 있는 크기다. 교과서는 "For tiny collections like Cranfield, exhaustive judgments of relevance for each query and document pair were obtained"라고 적는다 ([Manning et al., 2008](https://nlp.stanford.edu/IR-book/html/htmledition/assessing-relevance-1.html)). 〔원문〕 질문마다 전 구절을 판정해 두면 Hole@k가 0이 된다. 전수 판정을 하지 않고 사후에 채운다면, 그것은 기준을 바꾸는 일이 아니라 같은 기준으로 빠진 판정을 채우는 일이지만, 채우는 절차와 시점을 결과를 보기 전에 정해 두어야 그 구분이 유지된다. 〔추론〕

## 검색기는 같은 언어 문서를 먼저 올리고, 생성기 쪽 선호는 그보다 약하다

언어 선호(language preference, language bias)는 내용이 같거나 비슷한데도 검색기나 LLM이 특정 언어의 문서를 더 높게 올리거나 더 많이 쓰는 현상이다. BM25와 dense 검색의 뜻은 앞 절에 적었다.

### 다섯 편이 같은 방향을 보고하지만 한국어에서는 방향이 엇갈린다

Faux Polyglot("Faux Polyglot: A Study on Information Disparity in Multilingual Large Language Models")은 모델이 미리 알 수 없는 허구의 개체로 문서 170개와 사실형 질문 27개를 만들어 5개 언어로 번역했다. 검색에서는 "for the top-10 retrieved documents, models preferred the Native Language Document 68% of the time"이었고, 생성에서는 질문 언어 문서가 답의 출처인 경우가 42%, 다른 언어 문서가 29.58%, 둘 다인 경우가 8.55%, 어느 쪽도 아닌 경우가 19.8%였다 ([Sharma et al., 2024](https://arxiv.org/abs/2407.05502)). 〔원문〕 이 논문의 언어는 영어, 힌디어, 독일어, 아랍어, 중국어이고 한국어는 없다. 중요한 세부가 있다. **한 언어 문서에만 있는 사실(exclusive facts)을 묻는 질문에서는 그 차이가 사라졌다.** "Native and Foreign Documents again perform similarly." 저자는 다른 언어 문서에서 답을 끌어내려면 "queries that specifically target exclusive information in the foreign document"를 던져야 한다고 정리한다. 〔원문〕

Park & Lee("Investigating Language Preference of Multilingual RAG Systems")는 **MLRS**라는 지표를 제안한다. 여러 언어로 검색한 뒤 질문 언어가 아닌 문서를 번역하고 다시 순위를 매겨 순위가 얼마나 오르는지를 재는 것이다. 표의 각 열은 "문서를 그 언어로 번역했을 때의 순위 상승 점수"이지 "그 언어 문서가 몇 등으로 뽑혔는가"가 아니다. 결론은 "retrievers tend to prefer high-resource and query languages"다 ([Park & Lee, 2025](https://arxiv.org/abs/2502.11175)). 한국어 질문 행은 불리한 쪽까지 그대로 적어 둔다. Table 1(bge-m3)에서는 한국어로 번역했을 때 41.15, **영어로 번역했을 때 43.49(+2.34)** 로 영어가 더 높다. 그런데 같은 논문의 Table 2(질문 100개 표본, GPT-4o-mini 번역, top-10 안에서 계산)에서는 한국어 47.15, **영어 42.59(-4.56)** 로 방향이 반대다. 논문은 이 차이를 설명하지 않는다. 영어 질문에서는 영어 56.03, 한국어 33.02(-23.01)로 격차가 훨씬 크다. 번역기를 바꾸자 격차가 커졌다는 것("GPT-based translation amplifies the distinctness of language preference trends")도 논문이 직접 적는다. 생성기 쪽은 질문 언어와 답 언어가 같을 때의 이득이 "marginal"이라고 한다. 실험 규모는 MKQA 질문 2,827개이고 생성기는 aya-expanse-8B, Phi-4, Qwen2.5-7B-Instruct, Llama3.1-8B-Instruct다. 〔원문〕 **한국어 질문에서 영어 문서를 더 선호하는지 한국어 문서를 더 선호하는지는 한 논문 안에서도 엇갈리므로, 이 프로젝트의 시스템에서 어느 쪽인지는 직접 재야 한다.** 〔추론〕

Yang et al.("Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods")은 "queries in different languages, but with identical semantics, should yield equivalent ranking lists"라는 전제에서, 뜻이 같은 질문을 여러 언어로 던져 순위 목록이 얼마나 비슷한지를 **MRC@k**로 잰다(값이 높을수록 질문 언어가 바뀌어도 순위가 일관된다는 뜻이다). BM25가 0.6, XLM-R 기반 DPR이 11.7로 "more than a 20-fold disparity"가 났고, 이유는 BM25가 "high retrieval rates for documents in the same language as the query"를 보이기 때문이다. 대상은 유럽 24개 언어이고 한국어는 없다 ([Yang et al., 2024](https://aclanthology.org/2024.mrl-1.23.pdf)). BordIRlines도 "On IR, we find a preference toward retrieving query-language documents"라고 보고하되 언어별 편차가 크다고 적는다 ([Li et al., 2024](https://arxiv.org/abs/2410.01171)). Goworek et al.은 XLM-R이 질문과 같은 언어 문서를 치우쳐 가져오는 반면 Nomic은 훨씬 고르다고 보고한다 ([Goworek et al., 2025](https://arxiv.org/pdf/2511.19324)). 〔원문〕 Wang et al.("All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG")은 재순위기가 영어와 질문 언어 문서를 선호해 다른 언어의 근거를 밀어낸다고 주장한다 ([Wang et al., 2026](https://arxiv.org/abs/2604.20199)). 〔요약: 초록만〕

### 측정 방법은 네 갈래이고, 검색과 생성을 분리하는 것이 공통 원칙이다

첫째는 번역 후 재순위(Park & Lee의 MLRS)다. 둘째는 뜻이 같은 질문을 여러 언어로 던져 순위를 비교하는 것(Yang et al.의 MRC@k, 질문 언어와 문서 언어의 교차표)이다. 셋째는 검색된 상위 k개의 언어 구성을 세는 것(Sharma et al., Goworek et al., NeuCLIR의 exposure)이다. 넷째는 정답 문서의 언어를 통제하고 생성만 따로 보는 것이다. Qi et al.("On the Consistency of Multilingual Context Utilization in Retrieval-Augmented Generation")은 문맥 없음, 질문 언어 정답 문서 1개, 다른 언어 정답 문서 1개의 조건에 방해 문서를 더해 비교하고, 맞았지만 언어가 틀린 답을 따로 센다. MKQA에서 Aya-Expanse-8B의 정답률은 **문맥 없음 41.4, 질문 언어 정답 문서 73.6, 다른 언어 정답 문서 71.1**이었다(이 표는 언어가 틀린 정답도 정답으로 센다). 논문의 요지는 "a surprising ability of LLMs to extract relevant information from passages in a different language than the query, but a much weaker ability to produce a full answer in the correct language"이고, 질문 언어로 된 방해 문서가 더 큰 영향을 준다고도 보고한다 ([Qi et al., 2025](https://arxiv.org/abs/2504.00597)). 〔원문〕 XOR이 과제를 셋으로 나눈 이유도 같다. "the first two tasks enable researchers to diagnose where their models fail." ([Asai et al., 2021](https://arxiv.org/abs/2010.11856)) 〔원문〕

답의 언어는 별도 측정 대상이다. Marchisio et al.("Understanding and Mitigating Language Confusion in LLMs")은 응답을 줄 단위로 나눠 fastText로 언어를 판별하는 통과율(LPR)을 쓰는데, 판별기가 짧은 글에 약해서 "examples answerable with a single word/phrase"는 평가에서 뺐다. 한국어 단일 언어 LPR은 Llama 3 70B-I가 0.0, Mixtral 8x7B가 61.2였다 ([Marchisio et al., 2024](https://arxiv.org/abs/2406.20052)). 〔원문〕 이 표의 모델은 모두 35B~70B급이거나 API 모델이며, **4B~8B 오픈소스 모델의 한국어 답 언어 혼동률을 보고한 표는 찾지 못했다.** Chirkova et al.("Retrieval-augmented generation in multilingual settings")은 답이 사용자 언어로 쓰인 비율(correct language rate)을 따로 재고, 고유명사 음차 차이 때문에 단어 단위 일치가 실패한다며 문자 3-gram 재현율을 쓴다 ([Chirkova et al., 2024](https://arxiv.org/abs/2407.01463)). 〔원문〕

### 한국어·영어 쌍에서는 한국어 질문으로 영어 문서를 찾는 방향이 가장 약하다

Jang et al.("Improving Korean-English Cross-Lingual Retrieval: A Data-Centric Study of Language Composition and Model Merging")의 bge-m3 기본 모델 NDCG@10 평균은 영어 질문→한국어 문서 85.81, **한국어 질문→영어 문서 80.01**, 한국어 단일 언어 86.29, 영어 단일 언어 89.99다. gte-multilingual-base(84.30 / 75.02 / 81.54 / 89.45), multilingual-e5-base(80.11 / 65.98 / 84.62 / 89.50), multilingual-e5-large(87.04 / 76.88 / 87.43 / 90.35)도 같은 순서로 적으면 네 모델 모두 한국어 질문→영어 문서가 가장 낮다 ([Jang et al., 2025](https://arxiv.org/abs/2507.08480)). 〔원문〕 BGE-M3 논문의 MKQA(한국어 질문으로 영어 Wikipedia 검색, Recall@100)에서는 **BM25 27.9, M3 Dense 71.6, M3 Dense+Sparse 71.6**이었다. 저자는 sparse 방식이 약한 이유를 "there are only very limited co-existed terms for cross-lingual retrieval"라고 설명한다 ([Chen et al., 2024](https://arxiv.org/abs/2402.03216)). 〔원문〕 이 표의 "Sparse"는 BM25가 아니라 M3 모델이 학습한 sparse 가중치이므로, BM25와 dense를 묶은 하이브리드의 근거로는 대용일 뿐이다. 스크립트가 다른 언어 쌍에서 BM25가 0에 가깝다는 보고(영어→중국어 Recall@10 0.0, 일본어→영어 3.1과 0.2)는 있지만 한국어 쌍의 수치는 아니다 ([Goworek et al., 2025](https://arxiv.org/pdf/2511.19324)). 〔원문〕 **한국어·영어 교차 언어에서 BM25 + dense 하이브리드를 평가한 1차 출처, paraphrase-multilingual-MiniLM-L12-v2의 한국어·영어 교차 언어 검색 수치는 찾지 못했다.** MKQA에서 BM25가 0이 아닌 이유는 두 논문 모두 설명하지 않는다. 한국어 질문에 섞인 로마자 이름, 약어, 숫자가 영어 문서와 겹쳤을 것이라는 것은 조사자의 추정이다. 〔추론〕

## 30문항에서는 근거 언어를 문항별로 고정하고 단계별로 기록해야 읽을 수 있다

이 절은 전부 조사자 추론이다. 30문항·문서 20~30개 규모에서 실험한 논문도, 수십 문항 규모의 다국어 RAG 평가셋 설계를 다룬 논문이나 실무 가이드도 찾지 못했다. 아래는 앞 절들의 근거를 이 규모에 옮긴 것이고, 어느 선택지를 택할지는 이 보고서가 정하지 않는다. 이 절에서 태그가 없는 문장은 모두 〔추론〕이다.

### 세 가지 선택지는 서로 다른 것을 잰다

예시는 설명을 위해 지어낸 가상의 것이다. 풀에 영어 문서 「Helios 프로젝트 개요」가 있고 거기에 "출시일은 2031년 3월"이라는 문장이 있다고 하자. 질문은 한국어로 "Helios 프로젝트는 언제 출시되었나?"다.

| 선택지 | 가상의 예 | 잴 수 있는 것 | 잴 수 없는 것 | 선례 |
|---|---|---|---|---|
| A. 근거가 질문과 다른 언어 문서에만 있다 | 출시일이 영어 문서에만 있다. 한국어 문서 어디에도 출시일이 없다. | 정답이면 (검색 기록과 함께 볼 때) 영어 문서를 찾아 그 내용으로 답했다는 것. 오답이면 검색 실패, 읽기 실패, 답 언어 실패 중 어디인지. | 모델이 문맥 없이도 아는 사실이면 정답이 교차 언어 읽기의 증거가 아니다. BM25가 맞힌 경우 "Helios", "2031" 같은 로마자·숫자 겹침 때문일 수 있다. 언어 선호는 볼 수 없다(고를 대상이 없다). | XOR-Retrieve, Qi et al.의 다른 언어 정답 문서 조건, Faux Polyglot의 exclusive 사실, XRAG 단일 언어 검색, XBCP |
| B. 같은 사실이 두 언어 문서에 모두 있다 | 출시일이 영어 문서와 한국어 문서 「헬리오스 사업 소개」 양쪽에 있다. | 어느 언어 문서가 더 높은 순위로 뽑혔는가(언어 선호). 답이 맞는가. | 교차 언어 능력. 한국어 문서만으로 답할 수 있으므로 정답이 단일 언어 문항의 정답과 구별되지 않는다. 두 문서의 내용이 같아서 생성기가 어느 쪽을 썼는지도 답만으로는 알 수 없다. | LAReQA, CLIRMatrix MULTI-8, Faux Polyglot의 broad 질문, Park & Lee, Chirkova et al.의 영어+사용자 언어 조건 |
| C. 두 언어 문서가 답의 일부씩 갖는다 | 출시 연도는 영어 문서에, 출시 장소는 한국어 문서에 있고 질문이 둘 다 묻는다. | 두 언어 문서를 모두 가져와 합치는 능력. | 실패했을 때 교차 언어 때문인지 여러 사실을 합치는 일 자체가 어려워서인지 가르기 어렵다. | XRAG 다국어 검색 |

B형 문항은 근거 문서가 둘이라 그중 하나가 상위 k에 들 확률이 근거가 하나인 문항보다 높아져 더 쉬워질 수 있다. 이는 확률에 관한 추론이며 직접 잰 연구는 찾지 못했다. 같은 사실을 두 언어에 두되 한쪽을 조금 다르게 쓰면(Faux Polyglot의 contradiction 사실) 생성기가 어느 문서를 썼는지 답에서 드러나지만, "충돌 처리"라는 다른 능력을 함께 재게 된다. 〔추론〕

A형과 B형을 섞고 문항마다 "근거 언어: 한국어만 / 영어만 / 둘 다"를 고정해 결과를 칸별로 보고하면 A형으로 교차 언어 능력을, B형으로 언어 선호를 따로 읽을 수 있다. 그 대가는 표본이다. 근거 언어 세 칸과 질문 언어 두 가지로 나누면 칸마다 5문항 안팎이 된다. 그리고 근거에서 따라 나오는 조건부 결론이 하나 있다. **교차 언어 능력을 재는 것이 목적이라면 A형 문항 없이는 그것을 잴 수 없다.** B형만으로는 Faux Polyglot과 Park & Lee가 보고한 같은 언어 선호 때문에 시스템이 질문 언어 문서만 찾아도 만점이 된다. 〔추론〕

### 이 규모에서만 가능한 것과 이 규모라서 불가능한 것

가능한 것은 전수 확인이다. A형 문항에서 "질문 언어 문서 어디에도 이 사실이 없다"를 사람이 문서 20~30개를 전부 읽어 확인할 수 있다. XOR, MIRACL, CORA가 Wikipedia 규모에서 하지 못한다고 적은 바로 그 검증이다. 같은 이유로 질문마다 전 구절의 관련성을 판정해 두면 Precision@k의 "판정 없는 구절" 문제가 사라진다. 〔추론〕

불가능한 것은 통계적 주장이다. Wilson 구간(표본이 작을 때 비율의 불확실한 범위를 계산하는 방식)으로 95% 구간을 계산하면 30문항 중 24개 정답(80%)은 62.7%~90.5%, 10문항 중 8개 정답은 49.0%~94.3%, 10문항 중 5개 정답은 23.7%~76.3%, 5문항 중 4개 정답은 37.6%~96.4%다(이 보고서를 쓰며 다시 계산해 조사 노트의 값과 일치함을 확인했다). 〔추론〕 표본이 작을 때 흔히 쓰는 정규 근사(CLT) 방식에 대해 Bowyer et al.은 "CLT-based methods perform very poorly, usually dramatically underestimating uncertainty"라고 적고 Wilson score나 베이지안 구간을 권한다 ([Bowyer et al., 2025](https://arxiv.org/abs/2503.01747)). 〔원문〕 하위 집합이 10문항 안팎이면 "교차 언어가 단일 언어보다 못하다" 같은 차이는 수치가 아니라 문항별 실패 사례를 읽는 정성 분석으로 뒷받침해야 한다. 〔추론〕

같은 질문의 한국어판과 영어판을 둘 다 넣는다면 그 둘은 독립 표본이 아니다. Miller는 번역된 다국어 평가에 대해 "Because the inclusion of questions is non-independent, a key assumption of the Central Limit Theorem (or a bootstrap) is violated"라고 적고 짝 비교를 권한다 ([Miller, 2024](https://arxiv.org/abs/2411.00640)). 〔원문〕 대신 번역 쌍은 "같은 질문에서 한국어판은 맞고 영어판은 틀린 경우의 수"라는, 질문 난이도가 상쇄된 신호를 준다. Yang et al.의 설계(뜻이 같은 질문, 고정된 풀)를 가장 작게 옮긴 형태다. 번역 쌍을 넣을지, 넣으면 30문항에 어떻게 세는지는 정해야 할 사항이다. 〔추론〕

### 문항마다 기록해 둘 것

큰 벤치마크의 지표는 그대로 옮겨지지 않는다. 검색하는 단위가 문서이고 문서가 100개 이하일 때만 Recall@100이 자동으로 1이 된다. 청크 단위로 검색하면 문서 20~30개도 청크가 100개를 넘을 수 있어 그렇지 않다(문서 20개를 10개씩 나누면 청크 200개이고, 정답 청크가 150번째면 위에서 100개 안에 없다). 어느 쪽이든 이 규모에서 의미가 있는 것은 정답 구절의 순위(상위 1개, 상위 3개 안에 들었는가)와 상위 k개의 언어 구성이다. 〔2026-10-12 고침. 처음에는 "문서 20~30개에서 Recall@100은 자동으로 1이 되므로"라고 적었다. 검색 단위가 문서라고 가정한 문장인데 이 프로젝트는 청크 단위로 검색하므로 틀리다. Codex 1차 검토의 지적이다. 이 문장을 근거로 정한 결정은 없다.〕

단계를 나눠 기록해야 한다. XOR과 Qi et al.을 따르면 문항마다 검색 성공 여부(근거 구절이 상위 k에 들었는가, 어느 언어 구절로 들었는가), 답의 정답 여부, 답의 언어를 따로 남긴다. Qi et al.에서 다른 언어 문서를 줬을 때의 주된 실패는 내용 이해가 아니라 답 언어였다. 답 언어 판별은 사실형 단답에서 fastText류 자동 판별이 믿기 어려우므로(Marchisio et al.이 단답을 뺀 이유) 한글 문자 비율 같은 스크립트 기준이나 사람 확인이 더 맞을 수 있다. 한국어 답에 영어 고유명사를 그대로 쓴 경우를 정답으로 볼지도 채점 규칙에서 미리 정해야 한다. 〔추론〕

모델의 기억(parametric knowledge, 문서를 읽지 않고도 학습 때 익힌 지식으로 답하는 것)을 배제해야 한다. 실제 사실을 쓰면 모델이 문맥 없이도 꽤 맞힌다. Qi et al.의 문맥 없음 41.4(Aya-Expanse-8B, MKQA, 언어 평균 정답률)와 Chirkova et al.의 MKQA 한국어 검색 없음 21.5(Command-R-35B, 문자 3-gram 재현율)가 그 가능성을 보여 준다. 〔원문: 수치. Chirkova 표의 열 순서는 요약〕 둘 다 이 프로젝트의 모델과 문서가 아니고, Chirkova et al.의 모델은 4B~8B보다 훨씬 크다. 문항마다 문맥 없는 실행 결과를 함께 기록하거나, Faux Polyglot처럼 문서에만 있는 사실을 쓰면 이 혼선이 줄어든다. 〔추론〕

BM25에는 두 가지 표시가 필요하다. A형 문항마다 "질문과 정답 문서가 공유하는 로마자·숫자 토큰이 있는가"를 적어 두면 BM25의 정답이 토큰 겹침 때문인지 가를 수 있다. 그리고 문서 20~30개 풀에서 질문과 공유 토큰이 없는 문서는 BM25 점수가 모두 0이 되어 순서가 동점 처리(색인 순서 등)로 정해지므로, 점수를 함께 기록하고 점수 0인 문서가 상위 k에 든 경우를 검색 성공으로 세지 않는 규칙이 필요하다. 하이브리드에서는 BM25가 올린 같은 언어의 무관한 문서가 다른 언어의 정답 문서를 밀어낼 수 있으므로, dense 단독, BM25 단독, 하이브리드를 A형 문항에서 따로 재야 한다. 한국어 BM25가 형태소 분석기 선택에 따라 달라지는지는 1차 출처로 확인하지 못했다. 〔추론〕

방향을 합치지 않는다. Jang et al.에서 한국어 질문→영어 문서가 영어 질문→한국어 문서보다 일관되게 낮았으므로 두 방향을 따로 보고하는 편이 맞다. 다만 그 수치는 큰 풀의 것이고, 문서 20~30개 풀에서는 차이가 상위 3개 안에서 사라질 수 있다. 같은 이유로, 이 평가셋에서 교차 언어 문항이 전부 맞더라도 그것은 "이 작은 풀에서는 찾았다"는 뜻이지 큰 말뭉치에서의 교차 언어 검색 능력을 보여 주지 않는다. A형 문항의 난이도는 같은 주제의 질문 언어 문서가 풀에 있는지에 따라 달라지므로(Qi et al.의 방해 문서 결과) 그 여부도 문항 메타데이터로 적어 둘 만하다. 〔추론〕

마지막으로, 번역 후 재순위(MLRS)는 번역기 품질이 결과를 바꾼다는 것이 원 논문에서 드러났으므로 번역기를 따로 두지 않는 이 과제에는 맞지 않는다고 본다. 이 규모에서 그대로 쓸 수 있는 언어 선호 측정은 상위 k개의 언어 구성 세기, B형 문항에서 충족된 필수 사실이 어느 언어 구절로 잡혔는지의 분포, 번역 쌍의 순위 비교 세 가지다. 〔추론〕

## Conclusion

조사를 시작할 때의 질문은 "기존 벤치마크가 양쪽 언어에 다 있는 사실을 허용하는가, 제한하는가"였는데, 실제로 드러난 것은 그 질문이 큰 벤치마크에서는 성립하지 않는다는 점이다. Wikipedia 규모에서는 "질문 언어에 답이 없다"를 확인할 수 없어서, 벤치마크들은 풀을 한 언어로 제한하거나 답 문자열로 채점해 이 문제를 비켜 갔다. 문서 20~30개짜리 평가셋은 반대 위치에 있다. 풀 구성과 채점으로 비켜 갈 필요 없이 문항마다 근거의 언어 분포를 사람이 확정할 수 있고, 그렇게 확정한 딱지가 이 평가셋이 큰 벤치마크보다 더 정확하게 말할 수 있는 유일한 부분이다.

그래서 남는 결정은 지표가 아니라 문항 배분이다. 30문항을 A형에 많이 쓰면 교차 언어 능력에 대해 조금 더 말할 수 있고 언어 선호는 볼 수 없으며, B형에 쓰면 그 반대다. 어느 쪽이든 칸별 수치는 구간이 넓어 근거가 약하고, 단계별 기록과 실패 사례가 실질적인 증거가 된다. 정해야 할 것은 세 가지로 좁혀진다. 교차 언어 문항의 근거를 다른 언어에만 둘지와 그 문항 수, 번역 쌍을 넣을지와 그 세는 방법, 검색 채점에서 대체 구절을 "필수 사실 단위"로 셀지다. 확인하지 못한 채 남은 것 가운데 설계에 영향을 줄 만한 것은 Qi et al. 부록의 한국어 행(다른 언어 문서를 줬을 때 한국어 답의 정답률과 언어 오류 비율)과 4B~8B 모델의 한국어 답 언어 혼동 수치다.

## 참고 문헌

저자는 조사 노트에 기록된 범위까지만 적었다. "et al."로 끝나는 항목은 노트에 전체 저자 목록이 없다.

- Arabzadeh, Vtyurina, Yan, Clarke (2021). "Shallow pooling for sparse labels". https://arxiv.org/abs/2109.00062
- Artetxe, Ruder, Yogatama (2020). "On the Cross-lingual Transferability of Monolingual Representations" (XQuAD). https://arxiv.org/abs/1910.11856
- Asai, Kasai, Clark, Lee, Choi, Hajishirzi (2021). "XOR QA: Cross-lingual Open-Retrieval Question Answering". NAACL-HLT 2021. https://arxiv.org/abs/2010.11856
- Asai, Yu, Kasai, Hajishirzi (2021b). "One Question Answering Model for Many Languages with Cross-lingual Dense Passage Retrieval" (CORA). https://arxiv.org/abs/2107.11976
- Asai et al. (2022). "MIA 2022 Shared Task: Evaluating Cross-lingual Open-Retrieval Question Answering for 16 Diverse Languages". https://arxiv.org/abs/2207.00758
- Bowyer, Aitchison, Ivanova (2025). "Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints". ICML 2025. https://arxiv.org/abs/2503.01747
- Buckley, Voorhees (2004). "Retrieval Evaluation with Incomplete Information". SIGIR 2004. https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=150469
- Chen, Xiao, Zhang, Luo, Lian, Liu (2024). "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation" (BGE-M3). https://arxiv.org/abs/2402.03216
- Chirkova, Rau, Déjean, Formal, Clinchant, Nikoulina (2024). "Retrieval-augmented generation in multilingual settings". KnowLLM Workshop 2024. https://arxiv.org/abs/2407.01463
- Clark et al. (2020). "TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages". https://arxiv.org/abs/2003.05002
- Goworek, Macmillan-Scott, Özyiğit (2025). "What Drives Cross-lingual Ranking? Retrieval Approaches with Multilingual Language Models". 프리프린트. https://arxiv.org/pdf/2511.19324
- Jang, Son, Lee, Hong, Lim (2025). "Improving Korean-English Cross-Lingual Retrieval: A Data-Centric Study of Language Composition and Model Merging". 프리프린트. https://arxiv.org/abs/2507.08480
- Karpukhin et al. (2020). "Dense Passage Retrieval for Open-Domain Question Answering". EMNLP 2020. https://arxiv.org/abs/2004.04906
- Lawrie, Yang, Oard, Mayfield (2022). "Neural Approaches to Multilingual Information Retrieval". https://arxiv.org/abs/2209.01335
- Lawrie, MacAvaney, Mayfield, McNamee, Oard, Soldaini, Yang (2024). "Overview of the TREC 2023 NeuCLIR Track". TREC 2023 Proceedings. https://arxiv.org/abs/2404.08071
- Lewis, Oğuz, Rinott, Riedel, Schwenk (2020). "MLQA: Evaluating Cross-lingual Extractive Question Answering". https://arxiv.org/abs/1910.07475
- Li, Luo, Haider, Agashe, Li, Liu, Miao, Ramakrishnan, Yuan, Callison-Burch (2024). "Multilingual Retrieval Augmented Generation for Culturally-Sensitive Tasks: A Benchmark for Cross-lingual Robustness" (BordIRlines). ACL 2025 Findings. https://arxiv.org/abs/2410.01171
- Liu et al. (2025). "XRAG: Cross-lingual Retrieval-Augmented Generation". 프리프린트. https://arxiv.org/abs/2505.10089
- Longpre, Lu, Daiber (2021). "MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering". https://arxiv.org/abs/2007.15207
- Lu, Zeng, Qi, Yu, Zhao, Yang, Yanaka, Yokoya, Xuan (2026). "Beyond Monolingual Deep Research: Evaluating Agents and Retrievers with Cross-Lingual BrowseComp-Plus" (XBCP). 프리프린트. https://arxiv.org/abs/2606.15345
- Manning, Raghavan, Schütze (2008). "Introduction to Information Retrieval", 8장 "Assessing relevance". https://nlp.stanford.edu/IR-book/html/htmledition/assessing-relevance-1.html
- Marchisio, Ko, Bérard, Dehaze, Ruder (2024). "Understanding and Mitigating Language Confusion in LLMs". EMNLP 2024. https://arxiv.org/abs/2406.20052
- Miller (2024). "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations". 프리프린트. https://arxiv.org/abs/2411.00640
- Park, Lee (2025). "Investigating Language Preference of Multilingual RAG Systems". ACL 2025 Findings. https://arxiv.org/abs/2502.11175
- Pradeep, Thakur, Upadhyay, Campos, Craswell, Lin (2024). "Initial Nugget Evaluation Results for the TREC 2024 RAG Track with the AutoNuggetizer Framework". https://arxiv.org/abs/2411.09607
- Qi, Fernández, Bisazza (2025). "On the Consistency of Multilingual Context Utilization in Retrieval-Augmented Generation". MRL Workshop 2025. https://arxiv.org/abs/2504.00597
- Qu et al. (2021). "RocketQA: An Optimized Training Approach to Dense Passage Retrieval for Open-Domain Question Answering". NAACL 2021. https://arxiv.org/abs/2010.08191
- Ragas 공식 문서, "Context Recall" (2026-10-12 열람, 요약 도구 경유). https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/
- Roy et al. (2020). "LAReQA: Language-agnostic answer retrieval from a multilingual pool". https://arxiv.org/abs/2004.05484
- Ru et al. (2024). "RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation". https://arxiv.org/abs/2408.08067
- Sharma, Murray, Xiao (2024). "Faux Polyglot: A Study on Information Disparity in Multilingual Large Language Models". NAACL 2025. https://arxiv.org/abs/2407.05502
- Sun, Duh (2020). "CLIRMatrix: A massively large collection of bilingual and multilingual datasets for Cross-Lingual Information Retrieval". EMNLP 2020. https://aclanthology.org/2020.emnlp-main.340/
- Tang, Yang (2024). "MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries". https://arxiv.org/abs/2401.15391
- Thakur et al. (2021). "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models". NeurIPS 2021 Datasets and Benchmarks. https://arxiv.org/abs/2104.08663
- Thakur, Bonifacio, Zhang, Ogundepo, Kamalloo, Alfonso-Hermelo, Li, Liu, Chen, Rezagholizadeh, Lin (2023). "'Knowing When You Don't Know': A Multilingual Relevance Assessment Dataset for Robust Retrieval-Augmented Generation" (NoMIRACL). https://arxiv.org/abs/2312.11361
- Thakur, Kazi, Luo, Lin, Ahmad (2024). "MIRAGE-Bench: Automatic Multilingual Benchmark Arena for Retrieval-Augmented Generation Systems". https://arxiv.org/abs/2410.13716
- Thorne, Vlachos, Christodoulopoulos, Mittal (2018). "FEVER: a large-scale dataset for Fact Extraction and VERification". NAACL 2018. https://arxiv.org/abs/1803.05355
- Thorne, Vlachos, Cocarascu, Christodoulopoulos, Mittal (2018b). "The Fact Extraction and VERification (FEVER) Shared Task". https://arxiv.org/abs/1811.10971
- Wang, Mo, Shi, Zhang, Zheng, Cao, Chen, Lu, Lin, He, Han, Sun (2026). "All Languages Matter: Understanding and Mitigating Language Bias in Multilingual RAG". 초록만 확인. https://arxiv.org/abs/2604.20199
- Wu et al. (2024). "Not All Languages are Equal: Insights into Multilingual Retrieval-Augmented Generation" (Futurepedia). 프리프린트. https://arxiv.org/abs/2410.21970
- Yang, Jiang, Baldwin (2024). "Language Bias in Multilingual Information Retrieval: The Nature of the Beast and Mitigation Methods". MRL Workshop 2024. https://aclanthology.org/2024.mrl-1.23.pdf
- Yang, Jänich, Mayfield, Lawrie (2024b). "Language Fairness in Multilingual Information Retrieval" (PEER). SIGIR 2024. https://arxiv.org/abs/2405.00978
- Yang et al. (2018). "HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering". EMNLP 2018. https://arxiv.org/abs/1809.09600
- Zhang, Ma, Shi, Lin (2021). "Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval". https://arxiv.org/abs/2108.08787
- Zhang, Thakur, Ogundepo, Kamalloo, Alfonso-Hermelo, Li, Liu, Rezagholizadeh, Lin (2022). "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages". https://arxiv.org/abs/2210.09984
