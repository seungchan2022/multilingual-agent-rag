# 표·정보 상자·숫자가 많은 글에서 임베딩 검색이 얼마나 되는가

조사일 2026-10-23. 대상 후보는 셋이다. paraphrase-multilingual-MiniLM-L12-v2(아래 "MiniLM-L12 다국어"), gte-multilingual-base(아래 "mGTE"), bge-m3.

확인 수준 표기:
- **[원문 확인]**: 논문 PDF를 pdftotext로 텍스트로 바꿔 해당 문장과 표를 직접 읽었다.
- **[표 이미지 확인]**: PDF 쪽을 그림으로 열어 표·그림의 숫자를 눈으로 읽었다.
- **[요약 도구 경유]**: WebFetch가 쪽을 읽고 돌려준 요약에서 옮겼다. 숫자는 요약이 표에서 옮긴 값이고, 내가 원문 표를 직접 대조하지는 않았다. 보고서에 쓰기 전에 원문 대조가 필요하다.
- **[검색 결과만]**: 검색 결과 요약으로만 봤다. 근거로 쓰지 않고 빈 곳(Gaps)에만 둔다.
- **[내 계산]**: 원문 숫자로 내가 계산했다.

가장 중요한 한 줄: **세 후보 어느 것도 표 검색이나 숫자 검색을 독립적으로 잰 결과를 찾지 못했다.** 후보에 대한 독립 숫자는 bge-m3의 숫자 비교 실험 하나뿐이다(질문 2). 나머지는 다른 모델로 잰 결과(대리 근거)이거나 모델을 만든 쪽이 스스로 낸 숫자다.

## 질문 1. 표·정보 상자 같은 구조화된 글의 임베딩 검색을 잰 벤치마크가 있는가, 어느 공개 모델이 잘하는가

### Takeaway
영어 표 검색 벤치마크(TARGET, TEmBed-T)는 있고, 표를 마크다운으로 바꿔 통째로 임베딩하면 BM25보다 대체로 낫다. 표 제목이 빠지면 성능이 크게 떨어진다. 그러나 세 후보를 표 검색으로 잰 결과는 없고, 한국어나 다국어 표 검색 벤치마크도 찾지 못했다.

### Cited Findings

**TARGET (Ji, Glenn, Parameswaran, Hulsebos; arXiv v1 2025-05-14; 학회는 NeurIPS 2024 Table Representation Learning 워크숍)** [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2505.11545v1). 학회 표기는 TEmBed-T의 참고문헌 [8]에서 확인 [표 이미지 확인] — [TEmBed-T PDF](https://arxiv.org/pdf/2607.24130).
- 데이터: 질의응답 OTTQA·FeTaQA, 사실 검증 TabFact, 텍스트→SQL Spider·BIRD. 앞의 셋은 위키백과에서 온 표다(TEmBed-T 2.1절이 "Wikipedia-derived corpora"라고 적음 [표 이미지 확인]). 모두 영어다.
- 표 직렬화: 마크다운으로 바꾸고 행을 이어 붙여 한 문자열로 임베딩. 논문은 마크다운이 JSON보다 낫다고 적는다(원문 "markdown formatting yields better results", 뜻: 마크다운 형식이 더 좋은 결과를 낸다).
- 표 4(k=10, 앞 셋은 Recall@10, Spider·BIRD는 capped recall@10). 모델 비교:

| 모델 | OTTQA | FeTaQA | TabFact | Spider | BIRD |
|---|---|---|---|---|---|
| text-embedding-3-small (OpenAI, 유료) | 0.950 | 0.722 | 0.779 | 0.618 | 0.858 |
| stella_en_400M_v5 (영어 전용) | 0.963 | 0.741 | 0.824 | 0.657 | 0.961 |
| multilingual-e5-large-instruct | 0.918 | 0.655 | 0.741 | 0.620 | 0.894 |
| multilingual-e5-large-instruct, 열 이름만 | 0.549 | 0.188 | 0.430 | 0.613 | 0.909 |

- 표 3에서 BM25: OTTQA 0.967, FeTaQA 0.082, TabFact 0.338. 표 제목을 빼면 BM25 OTTQA가 0.592로 떨어진다(원문 "The performance drops for BM25 and TF-IDF to 0.592 and 0.583 respectively, if the table title is not included", 뜻: 표 제목을 넣지 않으면 BM25와 TF-IDF가 각각 0.592, 0.583으로 떨어진다).
- 표 셀 값(행)을 빼고 열 이름만 임베딩하면 질의응답·사실 검증에서 크게 떨어진다(위 표의 "열 이름만" 행, stella도 OTTQA 0.963→0.658, FeTaQA 0.741→0.208).
- 행 하나씩 임베딩(row-level)은 표 통째와 비슷한 성능이다(stella: OTTQA 0.951, FeTaQA 0.711, TabFact 0.848). 비용 때문에 큰 규모에는 실용적이지 않다고 적는다.
- 코퍼스가 커지면 재현율이 떨어지고, 표를 약 1만 개 넘게 더하면 눈에 띄게 떨어진다.
- 성격: 저자들이 만든 벤치마크에서 남의 모델들을 잰 결과이므로 모델 쪽에서 보면 독립 평가다. 세 후보는 들어 있지 않다.

**TEmBed-T (Poostforoushan, Vogel, Binnig; arXiv v1 2026-07-27; VLDB 2026 TaDA 워크숍)** [표 이미지 확인] — [arXiv PDF](https://arxiv.org/pdf/2607.24130)
- TARGET의 다섯 코퍼스(BIRD, FeTaQA, OTTQA, Spider, TabFact)에서 표 검색 MRR@10을 쟀다. 모두 영어다.
- 표 1(행 100개까지 넣음, 마크다운): GritLM 0.6934, Granite-R2 0.6550, MiniLM 0.4737(CSV로는 0.4842).
- 그림 2(데이터셋 평균 MRR@10, 머리글만 → 머리글+행 100개): Granite-R2 0.56→0.70, GritLM 0.56→0.72, MiniLM 0.50→0.54, Hashing(단어 빈도 기준선) 0.21→0.32.
- 논문 해석: "MiniLM shows a markedly smaller gain ... MiniLM's lower-capacity representation already saturates on schema-level signal"(뜻: MiniLM은 행을 넣었을 때 얻는 이득이 눈에 띄게 작다, 용량이 작은 표현이 이미 머리글 수준 신호에서 포화된다).
- 여기의 "MiniLM"은 참고문헌 [17](MiniLM 증류 논문, NeurIPS 2020)만 달려 있고 어떤 체크포인트인지 적혀 있지 않다. MiniLM-L12 다국어와 같은 모델이라고 볼 근거는 없다.
- CSV와 마크다운 중 늘 나은 쪽은 없다(그림 8, 부록 A.4 "no format uniformly preferable", 뜻: 어느 형식도 한결같이 낫지 않다).
- 값 섞기 시험(행 안의 값 짝을 깨뜨린 표와 원래 표를 구별하는가): 트랜스포머 임베딩 셋(Granite-R2, GritLM, MiniLM)의 정확도 평균이 0.1287–0.1965로 우연(0.50)보다 낮다(표 3·5, v0 설정). 통계·숫자가 대부분인 ECB 데이터셋에서는 셋 모두 0.0000이다(표 5). 원문 "Its statistical content carries minimal lexical discriminability ... Transformer-based approaches and the bag-of-words baseline collapse entirely on ECB with 0% accuracy"(뜻: 통계 내용이라 어휘로 구별할 거리가 거의 없고, 트랜스포머 방식과 단어 주머니 기준선이 ECB에서 0%로 무너진다).

**한국어·다국어 표 검색 벤치마크** — 찾지 못했다(Gaps 참고).

### Inferences
- 우리 표는 마크다운 표이고 위키백과에서 온 것이라 TARGET의 OTTQA·FeTaQA·TabFact와 형태가 가깝다. 다만 그 결과는 영어 질문과 영어 표에서 나온 것이고, 한국어 질문이나 한↔영 교차 검색에 그대로 옮겨진다는 근거는 없다.
- 다국어 모델의 대리 근거는 multilingual-e5-large-instruct 하나다. 이 모델은 영어 전용 stella보다 모든 데이터셋에서 낮았다(OTTQA 0.918 대 0.963, FeTaQA 0.655 대 0.741). 다국어 모델이 영어 표에서 영어 전용 모델보다 약할 수 있다는 정도만 말할 수 있다. 세 후보의 순위는 이것으로 정할 수 없다.
- TARGET에서 표 제목을 빼면 BM25가 크게 떨어지고, 열 이름만 남기면 밀집 임베딩도 크게 떨어진다. 그러니 표 청크가 무엇에 관한 표인지는 제목과 셀 값 양쪽에서 온다. 이것은 청크 앞에 문서·절 제목을 붙이는 결정과 관련이 있다(우리 프로젝트에 대한 내 추론이다).
- TEmBed-T에서 MiniLM이 행 100개를 넣어도 0.50→0.54로 거의 오르지 않았다. 논문은 용량 탓으로 설명한다. 내 추론으로는 입력 길이 상한 때문에 행 대부분이 잘려 아예 들어가지 않았을 가능성도 있다(행 100개는 MiniLM 계열의 128 또는 256 토큰 상한을 넘는다). 논문은 이 가능성을 다루지 않았다. 이 체크포인트가 무엇인지도 모르므로 추론으로만 둔다.
- TEmBed-T 값 섞기 시험이 말하는 것: 임베딩 벡터는 "어느 값이 어느 행에 붙어 있는가"를 거의 담지 못한다. 따라서 정답 청크를 찾는 일(질문이 원소 이름과 속성 이름을 담고 있다)과 그 청크 안에서 맞는 행의 값을 읽는 일은 다르다. 뒤의 일은 임베딩이 아니라 생성 모델이 표를 읽어서 해야 한다.

### Gaps
- 세 후보(MiniLM-L12 다국어, mGTE, bge-m3)를 표 검색으로 잰 독립 결과를 찾지 못했다.
- 한국어 또는 다국어 표 검색 벤치마크를 찾지 못했다. 검색에 걸린 것은 모두 원문을 읽지 않았다 [검색 결과만]: 2022 LREC 한국어 표 질의응답 데이터(임베딩 검색이 아니라 질의응답, https://aclanthology.org/2022.lrec-1.657), VisR-Bench(15개 언어, 표·그림·글 쪽 혼합, https://arxiv.org/pdf/2603.04238), snowflake-arctic-embed-l-v2.0 한국어 조정판이 "마크다운 표 검색에 맞췄다"는 모델 쪽 주장(https://www.promptlayer.com/models/snowflake-arctic-embed-l-v20-ko).
- "Metadata matters in dense table retrieval"(Gomm & Hulsebos, 2025)이라는 논문이 검색 요약에 한 번 나왔으나 다시 찾았을 때 찾지 못해 존재를 확인하지 못했다(https://ir.cwi.nl/pub/36085, 읽지 않음).
- MTEB/MMTEB 안에 표 검색 과제가 있다는 근거를 찾지 못했다(검색 결과에 없었음). 없다고 확인한 것은 아니다.
- 정보 상자(infobox)를 따로 다룬 임베딩 검색 평가는 찾지 못했다.

## 질문 2. 임베딩 모델은 숫자·단위·고유 이름(원소 이름, ¹⁴⁷Nd 같은 동위원소 표기)을 잘 못 다루는가

### Takeaway
숫자만 다른 두 글을 구별하는 일은 거의 우연 수준이다(13개 모델 평균 약 0.52–0.54, 우연 0.50). bge-m3도 "같은 수"는 95–100%로 찾지만 "보다 큰/작은 수"는 20–37%다. 단, 우리 질문은 대부분 숫자를 열쇠로 찾는 것이 아니라 원소·속성 이름으로 청크를 찾고 숫자는 답으로 읽는 구조라, 이 약점이 그대로 적용되지는 않는다. 동위원소 표기에 대한 근거는 찾지 못했다.

### Cited Findings

**Revealing the Numeracy Gap (Deng, Duan, Tang, Yang, HKUST; arXiv v1 2025-09-06)** [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2509.05691v1)
- 설정: 금융 분야 합성 표본 1,000개(EmbedNum-1K). 질문 하나에 답 둘이 있고, 두 답은 숫자 값만 다르다. 질문과 코사인 유사도가 더 높은 답이 맞는 답이면 정답. 우연 수준은 0.50.
- 13개 모델의 원래 정수 데이터 정확도(%): RoBERTa 50.8, finance-embedding 53.4, SimCSE-BERT-unsup 51.3, MiniLM-L6 50.6, MPNet 51.5, gte-Qwen2-7B-instruct 51.4, Linq-Embed-Mistral 51.4, Qwen3-Embedding-8B 53.7, SFR-Embedding-Mistral 52.1, e5-mistral-7b-instruct 51.5, NV-Embed-v2 52.1, Fin-E5 51.7, text-embedding-3-small 52.7.
- 위 13개의 평균은 51.9다 [내 계산: 합 674.2 ÷ 13 = 51.86]. 논문 본문은 전체 평균을 0.54라고 적는다. 0.54는 18개 형식 변형 전체의 평균으로 보이나 확인하지 않았다(불일치로 기록).
- 자릿수: 1자리 55.9, 2자리 52.5, 3자리 50.6, 4자리 50.0(우연). 소수: 한 자리 51.5 ~ 네 자리 50.8. 1보다 작은 수(0.8, 0.08, 0.008)는 61.6, 58.3, 56.3. 쉼표 구분(3,035)은 50.5.
- 형식에 따라 최대 12%p 달라진다. "8%"와 "0.08"을 다르게 다룬다.
- 대형 언어 모델 기반 임베딩이 평균 약 0.56, 인코더 기반이 약 0.51.
- 사전에 없는 숫자(소수, 큰 정수, 쉼표 숫자)는 토큰화에서 쪼개지며, 저자들은 이것을 낮은 정확도와 연결한다.
- 단위는 퍼센트 표기 말고는 분석하지 않았다.
- 세 후보는 평가 대상에 없다. MiniLM-L6은 영어 모델이다.
- 검색 요약은 이 논문이 EACL 2026 Findings에 실렸다고 했으나 학회 쪽 원문을 열지 않았다 [검색 결과만].

**Long-context Language Models Fail in Basic Retrieval Tasks Without Sufficient Reasoning Steps (Yu 외, Tsinghua·OpenCSG; arXiv v9 2025-08-26, 처음 올린 때는 2024-10)** [원문 확인, 부록 C.4.2 표 10] — [arXiv PDF](https://arxiv.org/pdf/2410.04422)
- 설정: 정수 20개 후보 가운데 질의에 맞는 수 하나를 임베딩 유사도로 찾는다. 후보 범위는 0–30, 0–100, 0–1,000, 0–10,000. 질의는 두 종류: "같은 수"(예: "The integer equal to 310", 뜻: 310과 같은 정수)와 "보다 큰/작은 수". 칸마다 표본 100개.
- 결과(정확도 %, 범위 30 / 100 / 1k / 10k 순):

| 모델 | 질의 종류 | 30 | 100 | 1k | 10k |
|---|---|---|---|---|---|
| e5-large-multilingual | 큰/작은 수 | 36 | 31 | 21 | 16 |
| e5-large-multilingual | 같은 수 | 95 | 98 | 99 | 99 |
| bge-m3 | 큰/작은 수 | 37 | 29 | 20 | 23 |
| bge-m3 | 같은 수 | 95 | 98 | 99 | 100 |

- 원문: "they only function properly when retrieval is based on equality relations; however, their performance significantly declines with more advanced logical operations, such as greater-than or less-than comparisons"(뜻: 같음 관계로 찾을 때만 제대로 작동하고, 보다 큼·작음 같은 논리 연산에서는 성능이 크게 떨어진다).
- 이것이 후보(bge-m3)를 독립적으로 잰 유일한 숫자 결과다. 질의와 후보가 숫자 하나만 담은 짧은 글이라 우리 청크와는 다르다.

**Simple Entity-Centric Questions Challenge Dense Retrievers (Sciavolino, Zhong, Lee, Chen; arXiv 2021-09-17, v3 2022-02-22, EMNLP 2021)** [요약 도구 경유, 초록만] — [arXiv](https://arxiv.org/abs/2109.08535)
- 위키데이터 사실로 만든 고유 이름 중심 질문에서 밀집 검색기가 희소 검색보다 크게 뒤진다(원문 "dense retrievers drastically underperform sparse methods", 뜻: 밀집 검색기가 희소 방법보다 크게 못하다). 데이터 늘리기로는 고쳐지지 않는다. 2023년 이전 연구이고, 대상은 당시 DPR 계열이다. 세 후보는 대상이 아니다. 초록에는 숫자가 없어 숫자는 옮기지 않았다.

### Inferences
- 우리 질문("네오디뮴-147의 반감기는?")에서 질문이 담는 것은 원소 이름, 질량수, 속성 이름이고, 답인 숫자는 질문에 없다. 그러니 "숫자만 다른 두 글을 구별"(EmbedNum)이나 "보다 큰 수 찾기"(LCLM 표 10)는 정답 청크를 찾는 일과 다른 과제다. 이 결과를 "bge-m3는 밀도 값을 못 찾는다"로 읽으면 안 된다.
- 예외가 있다. 동위원소 표가 행 경계에서 여러 청크로 나뉘면, 질문의 "147"이 147–150행 청크와 143–146행 청크 가운데 어느 것인지 가르는 열쇠가 된다. 이것은 "숫자로 청크 구별하기"이고, 위 두 논문이 약하다고 보인 바로 그 과제다. 3자리 정수는 EmbedNum에서 50.6%(우연)였다. 따라서 큰 표를 나눈 청크 사이에서 임베딩이 맞는 청크를 고르는 힘은 약할 것으로 예상한다(내 추론, 후보로 잰 근거는 아님).
- LCLM 표 10에서 "같은 수" 찾기는 95–100%였다. 질문의 숫자와 똑같은 글자가 청크에 있으면 임베딩도 꽤 맞힌다는 뜻일 수 있다. 다만 그 실험은 숫자 하나짜리 짧은 글이라, 숫자가 많은 표 청크 안의 숫자 하나에도 그렇다고 볼 근거는 없다.
- 고유 이름은 2021년 DPR 계열에서 약점이었다. 그 뒤의 모델(세 후보)에 같은 약점이 남아 있는지는 확인하지 못했다.

### Gaps
- ¹⁴⁷Nd(위 첨자), Nd-147, neodymium-147, 네오디뮴-147처럼 같은 동위원소를 여러 방식으로 쓴 것을 임베딩이 같은 것으로 보는지에 대한 근거를 찾지 못했다. 값싼 확인 방법(이 조사에서 하지 않음): 세 후보의 토크나이저에 이 네 표기를 넣어 어떻게 쪼개지는지 보고, 표기끼리의 코사인 유사도를 잰다.
- 단위(g/cm³, K, MeV, keV, 년/일 같은 반감기 단위)를 임베딩이 어떻게 다루는지 다룬 연구를 찾지 못했다.
- 한국어 숫자 표기(예: "9.841 g/cm³" 대 "9.841그램")나 한국어 원소 이름의 임베딩 처리에 대한 근거를 찾지 못했다.
- 세 후보 가운데 MiniLM-L12 다국어와 mGTE의 숫자 처리를 잰 결과는 찾지 못했다.

## 질문 3. 긴 입력 모델(8192 토큰)과 짧은 입력 모델(128/512 토큰)은 표 청크에서 다른가, 상한을 넘으면 어떻게 되는가

### Takeaway
MiniLM-L12 다국어의 입력 상한은 128 토큰이고, sentence-transformers는 넘는 부분을 잘라 앞쪽 토큰만 임베딩한다. 문서에는 경고를 띄운다는 말이 없다. mGTE와 bge-m3는 8192 토큰이다. 표 청크에서 둘을 직접 비교한 연구는 찾지 못했다.

### Cited Findings
- MiniLM-L12 다국어 모델 카드: 구조 칸에 "Transformer({'max_seq_length': 128, 'do_lower_case': False})", 출력 384차원. 넘는 입력을 어떻게 하는지는 카드에 적혀 있지 않다 [요약 도구 경유] — [모델 카드](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)(2026-10-23 열람).
- sentence-transformers 문서: "Longer texts will be truncated to the first `model.max_seq_length` tokens"(뜻: 더 긴 글은 앞쪽 max_seq_length 토큰까지만 남기고 잘린다). "You cannot increase the length higher than what is maximally supported by the respective transformer model"(뜻: 모델이 지원하는 최대보다 늘릴 수 없다). "if a model was trained on short texts, the representations for long texts might not be that good"(뜻: 짧은 글로 학습한 모델은 긴 글의 표현이 좋지 않을 수 있다). 잘릴 때 경고를 띄운다는 문장은 이 쪽에 없다 [요약 도구 경유] — [sbert.net 문서](https://sbert.net/examples/sentence_transformer/applications/computing-embeddings/README.html)(2026-10-23 열람).
- mGTE(gte-multilingual-base) 모델 카드: "Supports text lengths up to 8192 tokens", 305M 매개변수, 출력 768차원(128–768로 줄일 수 있음), 밀집 벡터와 함께 희소 벡터도 낸다. 지원 언어는 본문 "over 70", 머리 태그 "75 languages"로 같은 쪽 안에서 다르다 [요약 도구 경유] — [모델 카드](https://huggingface.co/Alibaba-NLP/gte-multilingual-base)(2026-10-23 열람).
- mGTE 논문(Zhang 외, Alibaba Tongyi Lab·HK PolyU; arXiv v2 2024-10-14; EMNLP 2024 Industry Track): 대조 사전학습 때 질의는 512, 문서는 1024 토큰으로 자른다. 검색 과제 평가 때 문서 쪽 최대 길이를 1024로 둔다는 각주가 있다(표 3). 8192와 512를 직접 비교한 검색 실험은 없다 [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2407.19669). 논문의 모델 이름은 mGTE-TRM이고 304M이다. 카드가 이 논문을 인용하므로 카드의 305M 모델과 같은 모델로 본다(매개변수 수 차이는 기록만 함).
- BGE-M3 논문(Chen, Xiao, Zhang, Luo, Lian, Liu; arXiv 2402.03216, v5 2025-12-12 개정, 처음 2024-02): 최대 길이 8192. 긴 문서 검색 MLDR(nDCG@10 평균)에서 비교 모델 mE5-large 등은 512로, M3는 8192로 쟀다. 512로 자른 M3와 비교한 실험은 없다. 긴 문서 학습 데이터를 뺀 경우 Dense가 MLDR 41.2, 학습 없이 256토큰마다 CLS를 넣는 방식(MCLS)으로 45.0 [요약 도구 경유, 모델을 만든 쪽 자체 보고] — [arXiv HTML](https://arxiv.org/html/2402.03216).
- MLDR(긴 문서) 비교, mGTE 논문 표 4(nDCG@10, 모델을 만든 쪽 보고): mE5-base(최대 514) 30.5, mE5-large(514) 34.2, BGE-M3 Dense(8192) 52.5, mGTE Dense(8192) 56.6 [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2407.19669).
- TEmBed-T: MiniLM은 행 100개를 넣어도 MRR@10이 0.50→0.54로 작게 올랐고, 다른 트랜스포머는 0.56→0.70, 0.56→0.72로 크게 올랐다 [표 이미지 확인] — [arXiv PDF](https://arxiv.org/pdf/2607.24130)(질문 1 참고, 체크포인트 미상).

### Inferences
- 우리 표 청크는 행 경계에서 나누고 머리글 행을 다시 붙인다. MiniLM-L12 다국어(128 토큰)로는 청크의 앞쪽 128 토큰(머리글과 처음 몇 행)만 벡터에 들어가고, 뒤쪽 행에 있는 값과 동위원소 이름은 벡터에 전혀 반영되지 않는다. 이때 오류가 나지 않으므로, 청크 크기를 정할 때 토크나이저로 길이를 직접 세야 한다(문서에 경고 문장이 없다는 것까지만 확인했다. 실제로 경고가 뜨는지는 확인하지 않았다).
- 같은 이유로, 청크 앞에 제목을 붙이면 128 토큰 안에서 제목이 차지하는 몫이 커져 표 내용이 더 많이 잘린다. 이것은 MiniLM-L12 다국어에만 크게 걸리는 문제다(내 추론).
- MLDR 결과는 긴 문서에서 512로 자른 모델이 8192 모델보다 크게 낮다는 것을 보이지만, 비교 모델이 달라 "길이만의 효과"로 나눠 볼 수 없다. 모두 모델을 만든 쪽이 낸 숫자다.
- 값싼 확인 방법(이 조사에서 하지 않음): 세 후보의 토크나이저로 우리 청크 전체의 토큰 수를 세고, 128을 넘는 청크와 512를 넘는 청크의 비율을 낸다. 한국어는 같은 내용이라도 토큰이 더 많이 나올 수 있으므로 언어별로 나눠 센다.

### Gaps
- 표 청크에서 긴 입력 모델과 짧은 입력 모델을 같은 조건으로 비교한 연구를 찾지 못했다.
- 8192 토큰을 받는 모델이라도 긴 표 청크 안의 한 행 값을 벡터가 얼마나 담는지(긴 입력에서 정보가 희석되는지)에 대한 표 대상 근거를 찾지 못했다.
- sentence-transformers가 잘릴 때 실제로 경고를 내는지는 문서에서 확인하지 못했다.

## 질문 4. 밀집+희소(bge-m3 희소·다중 벡터, BM25 혼합)가 숫자·표 검색에 도움이 되는가 (짧게)

### Takeaway
표·숫자에 한정한 근거는 찾지 못했다. 긴 문서에서는 희소 검색이 밀집보다 낫고, 둘을 합치면 더 낫다는 것이 bge-m3와 mGTE의 자체 보고다. 영어 표 검색(TARGET)에서는 오히려 BM25가 밀집보다 약했다. 한↔영 교차 검색에서는 희소가 약하다.

### Cited Findings
- BGE-M3 자체 보고(MIRACL dev, nDCG@10 평균): BM25 31.9, mE5-large 66.6, M3 Dense 69.2, Sparse 53.9, Multi-vec 70.5, Dense+Sparse 70.4, All 71.5 [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2402.03216).
- BGE-M3 자체 보고(MLDR, nDCG@10 평균): BM25 53.6, Dense 52.5, Sparse 62.2, Multi-vec 57.6, Dense+Sparse 64.8, All 65.0. 원문 "M3 (Sparse) turns out to be a more effective method for long document retrieval, which achieves another about 10 points improvement over the dense method"(뜻: 긴 문서 검색에서는 희소 방식이 더 효과적이며 밀집보다 약 10점 높다) — 같은 출처.
- BGE-M3는 교차 언어 검색(MKQA)에서 희소가 약한 까닭을 "there are only very limited co-existed terms for cross-lingual retrieval"(뜻: 언어가 다르면 질문과 문서에 함께 나오는 낱말이 아주 적다)로 적는다 — 같은 출처. 논문은 희소가 정확한 용어·고유 이름·숫자에 도움이 된다고 따로 주장하지 않는다.
- mGTE 논문 표 4(모델을 만든 쪽 보고, nDCG@10, MKQA만 Recall@20):

| 모델 | MLDR | MIRACL | MKQA |
|---|---|---|---|
| BGE-M3 Dense | 52.5 | 67.7 | 67.8 |
| BGE-M3 Sparse | 62.2 | 53.9 | 36.3 |
| BGE-M3 Dense+Sparse | 64.8 | 68.9 | 68.1 |
| mGTE Dense | 56.6 | 62.1 | 65.8 |
| mGTE Sparse | 71.0 | 55.9 | 31.6 |
| mGTE Dense+Sparse | 71.3 | 64.5 | 66.0 |

  [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2407.19669). MKQA는 교차 언어 질의응답이라 희소가 크게 약하다(BGE-M3 36.3, mGTE 31.6).
- TARGET(영어 표): BM25는 FeTaQA 0.082, TabFact 0.338로 밀집 표 임베딩(stella 0.741, 0.824)보다 크게 낮다. 원문은 희소 어휘 검색이 표에서는 글에서보다 "less effective"(뜻: 덜 효과적)라고 적는다 [요약 도구 경유] — [arXiv HTML](https://arxiv.org/html/2505.11545v1).

### Inferences
- 우리 코퍼스에서 혼합이 도울 수 있는 자리는 질문과 청크에 같은 글자가 나오는 경우다. 원소 기호(Nd), 질량수(147), 같은 언어로 된 원소 이름이 그렇다. 숫자와 원소 기호는 한국어 글과 영어 글에 같은 글자로 나오므로 교차 언어에서도 희소가 일부 맞을 수 있다. 이것은 검증하지 않은 가설이다. 반대로 원소 이름(네오디뮴/neodymium)과 속성 이름(반감기/half-life)은 언어가 다르면 글자가 겹치지 않아, MKQA에서처럼 희소가 약할 것이다.
- 혼합 여부는 뒤에 정하기로 되어 있으므로 여기서는 근거만 남긴다.

### Gaps
- 숫자·표 검색에서 밀집+희소 혼합의 효과를 잰 연구를 찾지 못했다.
- 혼합 검색이 recall을 올린다는 업체 평가 숫자(Anthropic Contextual Retrieval, 2024)가 검색에 걸렸으나 2차 블로그 요약으로만 봤고 원문을 읽지 않아 근거로 쓰지 않는다 [검색 결과만].

### 출처 사이 불일치 기록 (고치지 않고 기록만)
- BGE-M3 MIRACL Dense 평균: BGE-M3 논문 69.2, mGTE 논문 표 4 67.7. Dense+Sparse도 70.4 대 68.9로 다르다. 어느 쪽이 맞는지 확인하지 않았다(평가 언어 집합이나 설정 차이일 수 있음).
- mGTE Dense: 같은 논문 안에서 표 4 평균 66.7, 표 5 평균 58.9, BEIR 51.1 대 50.9로 다르다. 논문에 설명이 없다.
- EmbedNum: 본문 평균 0.54, 원래 정수 데이터 13개 모델 평균 51.9 [내 계산].
- mGTE 매개변수 수: 카드 305M, 논문 304M. 지원 언어: 카드 본문 70, 태그 75.
