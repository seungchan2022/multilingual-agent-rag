# 한영 교차 검색용 오픈 다국어 임베딩 모델 사실표 (M3 Pro 36GB 로컬 실행 포함)

조사일: 2026-10-23. 모든 값은 아래 링크의 원문(Hugging Face 모델 카드·설정 파일·HF 메타데이터 API, SBERT 문서, Google 문서, Ollama 라이브러리, GitHub 이슈)에서 읽었다. 확인하지 못한 값은 `확인 못 함`으로 적었다. 실제로 모델을 내려받아 돌려 본 측정은 하지 않았다(메모리·속도는 측정값이 아니다).

표기 약속
- "메타데이터" = Hugging Face 메타데이터 API(`https://huggingface.co/api/models/<repo>`)의 값. 카드 본문이 아니라 저장소 등록 정보에서 나온 값이라 따로 표시한다. 파라미터 수는 이 API의 `safetensors.total`(가중치 파일의 원소 수)이다.
- "HF 저장소 생성일" = 메타데이터의 `createdAt`. 공식 발표일이 아니다.
- 모델 번호(표 공통): ① paraphrase-multilingual-MiniLM-L12-v2 ② gte-multilingual-base ③ bge-m3 ④ multilingual-e5-large ⑤ multilingual-e5-large-instruct ⑥ Qwen3-Embedding-0.6B ⑦ EmbeddingGemma-300m ⑧ jina-embeddings-v3 ⑨ snowflake-arctic-embed-l-v2.0 ⑩ nomic-embed-text-v2-moe ⑪ KURE-v1 / 추가로 찾은 2026년 모델: ⑫ EmbeddingGemma 2 ⑬ harrier-oss-v1-0.6b ⑭ jina-embeddings-v5-text-small ⑮ KURE-v3 ⑯ Nemotron-3-Embed-1B-BF16

## 1. 크기·임베딩 차원·최대 입력 길이·토크나이저

### Takeaway
과제 권장 모델 ①은 384차원, 파라미터 약 1.18억 개이며, sentence-transformers(이하 ST)에서 최대 입력이 **128토큰**이다. 128토큰을 넘는 글은 **앞 128토큰만 남기고 잘린다(truncation)**. ②·③·⑧·⑨·⑪·⑫·⑮는 8192토큰, ⑥·⑬·⑭·⑯은 32K, ④·⑤·⑩은 512토큰, ⑦은 2K다.

### Cited Findings

| 모델 | 파라미터 | 임베딩 차원 | 최대 입력 토큰 | 토크나이저 |
|---|---|---|---|---|
| ① paraphrase-multilingual-MiniLM-L12-v2 | 117,654,272 (메타데이터, F32 117,653,760 + I64 512) [api](https://huggingface.co/api/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 384 [1_Pooling/config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/1_Pooling/config.json) | ST `max_seq_length` **128** [sentence_bert_config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/sentence_bert_config.json). 모델 위치 임베딩 상한 512 (`max_position_embeddings`) [config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/config.json) | `PreTrainedTokenizerFast`, `model_max_length` 512 [tokenizer_config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/tokenizer_config.json). 어휘 250,037개, BertModel 12층·hidden 384 [config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/config.json) |
| ② gte-multilingual-base | 305,369,089 (메타데이터, F16) [api](https://huggingface.co/api/models/Alibaba-NLP/gte-multilingual-base). 카드 "Model Size: 305M" [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base) | 768. 카드 예제 주석은 128–768 사이로 줄일 수 있다고 함 ("elastic dense") [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base) | 8192 [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base), ST `max_seq_length` 8192 [sentence_bert_config.json](https://huggingface.co/Alibaba-NLP/gte-multilingual-base/blob/main/sentence_bert_config.json) | `XLMRobertaTokenizer` [tokenizer_config.json](https://huggingface.co/Alibaba-NLP/gte-multilingual-base/blob/main/tokenizer_config.json), 어휘 250,048, 12층, RoPE 위치 표현 [config.json](https://huggingface.co/Alibaba-NLP/gte-multilingual-base/blob/main/config.json) |
| ③ bge-m3 | 카드에 없음. 가중치 파일 `pytorch_model.bin` 2,271,145,830 bytes(fp32 저장) [파일 목록 API](https://huggingface.co/api/models/BAAI/bge-m3/tree/main). 제3자 표기: 568M — [arctic 카드 표](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0), [nomic 카드 표](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe); Ollama 태그 `567m` [ollama](https://ollama.com/library/bge-m3/tags) | 1024 [card](https://huggingface.co/BAAI/bge-m3) | 8192 [card](https://huggingface.co/BAAI/bge-m3), ST `max_seq_length` 8192 [sentence_bert_config.json](https://huggingface.co/BAAI/bge-m3/blob/main/sentence_bert_config.json) | `XLMRobertaTokenizer` [tokenizer_config.json](https://huggingface.co/BAAI/bge-m3/blob/main/tokenizer_config.json), 어휘 250,002, 24층 [config.json](https://huggingface.co/BAAI/bge-m3/blob/main/config.json) |
| ④ multilingual-e5-large | 559,890,432 (메타데이터, F32) [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large) | 1024, 24층 [card](https://huggingface.co/intfloat/multilingual-e5-large) | 512. 카드 "Long texts will be truncated to at most 512 tokens" [card](https://huggingface.co/intfloat/multilingual-e5-large), ST 512 [sentence_bert_config.json](https://huggingface.co/intfloat/multilingual-e5-large/blob/main/sentence_bert_config.json) | `XLMRobertaTokenizer`, 어휘 250,002 [tokenizer_config.json](https://huggingface.co/intfloat/multilingual-e5-large/blob/main/tokenizer_config.json), [config.json](https://huggingface.co/intfloat/multilingual-e5-large/blob/main/config.json) |
| ⑤ multilingual-e5-large-instruct | 559,890,432 (메타데이터, F16) [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large-instruct) | 1024, 24층 [card](https://huggingface.co/intfloat/multilingual-e5-large-instruct) | 512 (카드 Limitations) [card](https://huggingface.co/intfloat/multilingual-e5-large-instruct); `sentence_bert_config.json` 없음, 토크나이저 `model_max_length` 512 [tokenizer_config.json](https://huggingface.co/intfloat/multilingual-e5-large-instruct/blob/main/tokenizer_config.json) | `XLMRobertaTokenizer` [tokenizer_config.json](https://huggingface.co/intfloat/multilingual-e5-large-instruct/blob/main/tokenizer_config.json) |
| ⑥ Qwen3-Embedding-0.6B | 595,776,512 (메타데이터, BF16) [api](https://huggingface.co/api/models/Qwen/Qwen3-Embedding-0.6B). 카드 "0.6B", 28층 [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 최대 1024, 32–1024 사이로 지정 가능(MRL) [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 32K [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B); `max_position_embeddings` 32768 [config.json](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/config.json). `sentence_bert_config.json` 없음. 토크나이저 `model_max_length`는 131072라 학습 길이와 다름 [tokenizer_config.json](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/tokenizer_config.json) | `Qwen2Tokenizer` [tokenizer_config.json](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/tokenizer_config.json), 어휘 151,669 [config.json](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/config.json) |
| ⑦ EmbeddingGemma-300m | 302,863,104 (메타데이터, F32) [api](https://huggingface.co/api/models/google/embeddinggemma-300m); 카드 "300M" [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card); HF 블로그 "308M" [blog](https://huggingface.co/blog/embeddinggemma) — 세 값이 서로 다름 | 768, MRL로 512/256/128 [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card) | 2K [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card), Ollama "2K context window" [ollama](https://ollama.com/library/embeddinggemma/tags) | 확인 못 함 (HF 저장소가 승인제라 설정 파일이 401로 막힘) [api](https://huggingface.co/api/models/google/embeddinggemma-300m) |
| ⑧ jina-embeddings-v3 | 572,310,396 (메타데이터, BF16) [api](https://huggingface.co/api/models/jinaai/jina-embeddings-v3) | 1024, MRL 32–1024 [card](https://huggingface.co/jinaai/jina-embeddings-v3) | 8192 [card](https://huggingface.co/jinaai/jina-embeddings-v3) | `XLMRobertaTokenizer`, `model_max_length` 8194 [tokenizer_config.json](https://huggingface.co/jinaai/jina-embeddings-v3/blob/main/tokenizer_config.json) |
| ⑨ snowflake-arctic-embed-l-v2.0 | 567,754,752 (메타데이터, F32) [api](https://huggingface.co/api/models/Snowflake/snowflake-arctic-embed-l-v2.0); 카드 568M(임베딩층 제외 303M) [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) | 1024, MRL 256 [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) | 8192 (bge-m3-retromae 기반, RoPE) [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0); `sentence_bert_config.json` 없음 | `XLMRobertaTokenizer`, `model_max_length` 8192 [tokenizer_config.json](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0/blob/main/tokenizer_config.json) |
| ⑩ nomic-embed-text-v2-moe | 475,292,928 (메타데이터) [api](https://huggingface.co/api/models/nomic-ai/nomic-embed-text-v2-moe); 카드 전체 475M·추론 때 활성 305M, 전문가 8개 중 2개 사용(MoE) [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) | 768, MRL로 256까지 [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) | 512 [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe), ST 512 [sentence_bert_config.json](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe/blob/main/sentence_bert_config.json) | `XLMRobertaTokenizer` [tokenizer_config.json](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe/blob/main/tokenizer_config.json), 어휘 250,048 [config.json](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe/blob/main/config.json) |
| ⑪ KURE-v1 | 567,754,752 (메타데이터, F32) [api](https://huggingface.co/api/models/nlpai-lab/KURE-v1) | 1024 [card](https://huggingface.co/nlpai-lab/KURE-v1) | 8192 [card](https://huggingface.co/nlpai-lab/KURE-v1), ST 8192 [sentence_bert_config.json](https://huggingface.co/nlpai-lab/KURE-v1/blob/main/sentence_bert_config.json) | `XLMRobertaTokenizer` [tokenizer_config.json](https://huggingface.co/nlpai-lab/KURE-v1/blob/main/tokenizer_config.json) |
| ⑫ EmbeddingGemma 2 | 744,371,512 (메타데이터) [api](https://huggingface.co/api/models/google/embeddinggemma-2); 카드 전체 740M = 텍스트 270M + 시각 170M + 음성 300M [card](https://huggingface.co/google/embeddinggemma-2) | 768, MRL 128/256/512 [card](https://huggingface.co/google/embeddinggemma-2) | 8,192 [card](https://huggingface.co/google/embeddinggemma-2); Ollama 태그 페이지는 "256K context window"로 표기 [ollama](https://ollama.com/library/embeddinggemma-2/tags) — 서로 다름 | `GemmaTokenizer` [tokenizer_config.json](https://huggingface.co/google/embeddinggemma-2/blob/main/tokenizer_config.json), 어휘 262,144 [card](https://huggingface.co/google/embeddinggemma-2) |
| ⑬ harrier-oss-v1-0.6b | 596,049,920 (메타데이터) [api](https://huggingface.co/api/models/microsoft/harrier-oss-v1-0.6b); 카드 0.6B [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) | 1,024 [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) | 32,768 [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) | `Qwen2Tokenizer` [tokenizer_config.json](https://huggingface.co/microsoft/harrier-oss-v1-0.6b/blob/main/tokenizer_config.json), Qwen3Model 28층 [config.json](https://huggingface.co/microsoft/harrier-oss-v1-0.6b/blob/main/config.json) |
| ⑭ jina-embeddings-v5-text-small | 카드 677M [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small); 메타데이터 596,049,920 [api](https://huggingface.co/api/models/jinaai/jina-embeddings-v5-text-small) — 서로 다름 | 1024, MRL 32–1024 [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) | 32768 [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) | `Qwen2Tokenizer` [tokenizer_config.json](https://huggingface.co/jinaai/jina-embeddings-v5-text-small/blob/main/tokenizer_config.json) |
| ⑮ KURE-v3 | 1,140,918,272 (메타데이터) [api](https://huggingface.co/api/models/nlpai-lab/KURE-v3); 카드 1.1B [card](https://huggingface.co/nlpai-lab/KURE-v3) | 2,048, MRL 1,024/512/256 [card](https://huggingface.co/nlpai-lab/KURE-v3) | 8,192 [card](https://huggingface.co/nlpai-lab/KURE-v3) | `TokenizersBackend`, `model_max_length` 8192 [tokenizer_config.json](https://huggingface.co/nlpai-lab/KURE-v3/blob/main/tokenizer_config.json), 어휘 131,072 [config.json](https://huggingface.co/nlpai-lab/KURE-v3/blob/main/config.json) |
| ⑯ Nemotron-3-Embed-1B-BF16 | 약 1.14B [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16); 메타데이터 1,140,918,272 [api](https://huggingface.co/api/models/nvidia/Nemotron-3-Embed-1B-BF16) | 2048 (앞에서 잘라 1024·512 사용 가능) [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16) | 32768 [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16), ST 32768 [sentence_bert_config.json](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16/blob/main/sentence_bert_config.json) | `TokenizersBackend` [tokenizer_config.json](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16/blob/main/tokenizer_config.json), 어휘 131,072 [config.json](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16/blob/main/config.json) |

① 긴 입력 처리 (질문에 대한 직접 답)
- ST 문서: "Each model has a maximum sequence length under `model.max_seq_length` ... Longer texts will be truncated to the first `model.max_seq_length` tokens"(최대 길이를 넘는 글은 앞쪽 그 길이만큼만 남기고 잘린다). 값은 바꿀 수 있으나 "You cannot increase the length higher than what is maximally supported by the respective transformer model"(모델이 지원하는 최대치보다 크게 할 수 없다), "if a model was trained on short texts, the representations for long texts might not be that good"(짧은 글로 학습한 모델은 긴 글 표현이 나쁠 수 있다) — [SBERT Computing Embeddings](https://sbert.net/examples/sentence_transformer/applications/computing-embeddings/README.html)
- ①의 ST 설정 128, 모델 위치 임베딩 512 → ST에서 128토큰 뒤는 잘린다. 512까지 올릴 수는 있다 — [sentence_bert_config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/sentence_bert_config.json), [config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/config.json)
- ①의 모듈 구성은 Transformer → Pooling(mean) 두 개뿐이고 Normalize 모듈이 없다(②·③·④·⑤·⑧·⑨·⑩·⑪은 Normalize 포함) — [① modules.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/modules.json), [③ modules.json](https://huggingface.co/BAAI/bge-m3/blob/main/modules.json)

풀링(문장 벡터를 만드는 방식): ① mean, ② CLS, ③ CLS, ④ mean, ⑤ mean, ⑥ last-token, ⑧ mean, ⑨ CLS, ⑩ mean, ⑪ CLS — 각 저장소의 `1_Pooling/config.json` ([①](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/1_Pooling/config.json), [②](https://huggingface.co/Alibaba-NLP/gte-multilingual-base/blob/main/1_Pooling/config.json), [③](https://huggingface.co/BAAI/bge-m3/blob/main/1_Pooling/config.json), [④](https://huggingface.co/intfloat/multilingual-e5-large/blob/main/1_Pooling/config.json), [⑤](https://huggingface.co/intfloat/multilingual-e5-large-instruct/blob/main/1_Pooling/config.json), [⑥](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/1_Pooling/config.json), [⑧](https://huggingface.co/jinaai/jina-embeddings-v3/blob/main/1_Pooling/config.json), [⑨](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0/blob/main/1_Pooling/config.json), [⑩](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe/blob/main/1_Pooling/config.json), [⑪](https://huggingface.co/nlpai-lab/KURE-v1/blob/main/1_Pooling/config.json)); ⑬ last-token [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b); ⑭ last-token [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small); ⑯ average pooling [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16); ⑫ mean [card](https://huggingface.co/google/embeddinggemma-2)

### Inferences
- 20개 위키백과 문서를 청크로 나눌 때, ①은 청크가 128토큰(한국어는 XLM-R 계열 어휘라 글자 수 기준으로 더 짧을 수 있음)을 넘으면 뒷부분이 벡터에 반영되지 않는다. 청크 크기를 정할 때 ①의 128토큰이 다른 모델과 비교의 공정성 조건이 된다.
- ①에 Normalize 모듈이 없으므로, 코사인이 아닌 내적으로 점수를 내면 길이 차이가 점수에 섞인다. 코사인 유사도를 쓰거나 `normalize_embeddings=True`로 맞추면 된다(ST 기능 — 출처는 ②카드 예제에서 같은 인자 사용 [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base)).
- ①의 토크나이저 내부 알고리즘(SentencePiece/WordPiece)은 파일에서 직접 확인하지 못했다. 어휘 250,037개와 `<s>`/`</s>` 특수 토큰은 XLM-R 계열과 비슷하다는 추정만 가능하다.

### Gaps
- ⑤·⑥·⑨·⑧·⑬·⑭는 `sentence_bert_config.json`이 없어 ST로 불러왔을 때 실제 `model.max_seq_length` 값은 실행해서 확인해야 한다(⑥은 토크나이저 값 131072가 쓰일 수 있음).
- ⑦의 토크나이저·ST 설정은 승인제 저장소라 읽지 못함.
- ⑦의 파라미터 수(300M·302.9M·308M), ⑭(677M·596M), ⑫의 문맥 길이(8,192·256K)는 출처끼리 다르다. 어느 쪽이 맞는지 판정하지 않았다.

## 2. 학습 목표: 검색(질문–문단)용인가, 문장 유사도·바꿔 말하기용인가

### Takeaway
①은 영어 바꿔 말하기(paraphrase) 모델을 교사로 두고 병렬 번역 문장으로 증류한 **문장 유사도 중심** 모델이다. SBERT 문서는 이를 "Semantic Search Models"(검색 전용) 목록이 아니라 "Multilingual Models" 목록에 둔다. 나머지 ②–⑯은 카드에서 검색(retrieval)을 주 용도로 밝힌다.

### Cited Findings

| 모델 | 학습 목표 / 용도 (원문 근거) |
|---|---|
| ① | "Multilingual version of paraphrase-MiniLM-L12-v2, trained on parallel data for 50+ languages" — [SBERT Pretrained Models](https://sbert.net/docs/sentence_transformer/pretrained_models.html). 방식: 고정된 영어 교사 모델의 벡터를 학생 모델이 번역문에서도 똑같이 내도록 MSE로 학습 — [SBERT Multilingual](https://sbert.net/examples/sentence_transformer/training/multilingual/README.html). 교사 paraphrase-MiniLM-L12-v2의 학습 데이터: AllNLI, sentence-compression, SimpleWiki, altlex, msmarco-triplets, quora_duplicates, coco_captions, flickr30k_captions, yahoo_answers_title_question, S2ORC_citation_pairs, stackexchange_duplicate_questions, wiki-atomic-edits — [SBERT Paraphrase Data](https://sbert.net/examples/sentence_transformer/training/paraphrases/README.html). 카드: "can be used for tasks like clustering or semantic search" — [card](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2). 같은 SBERT 문서의 "Semantic Search Models"는 multi-qa-* 모델들이다 — [SBERT Pretrained Models](https://sbert.net/docs/sentence_transformer/pretrained_models.html) |
| ② | "state-of-the-art (SOTA) results in multilingual retrieval tasks", dense와 sparse 벡터 모두 생성; 논문 "mGTE: ... Text Representation and Reranking Models for Multilingual Text Retrieval" — [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base) |
| ③ | dense·sparse·multi-vector 검색을 한 모델에서 수행; bge-m3-unsupervised(대조학습)에서 통합 미세조정 — [card](https://huggingface.co/BAAI/bge-m3) |
| ④ | 1단계: 약지도 대조 사전학습(mC4 1B, NLLB 번역쌍 2.4B, Wikipedia 섹션제목–문단 150M 등), 2단계: 지도 미세조정(MS MARCO, NQ, Mr. TyDi 11개 언어, MIRACL 16개 언어 등) — [card](https://huggingface.co/intfloat/multilingual-e5-large) |
| ⑤ | 1단계 약지도 텍스트쌍 10억 개 대조 사전학습, 2단계 E5-mistral 논문 데이터로 미세조정 — [card](https://huggingface.co/intfloat/multilingual-e5-large-instruct) |
| ⑥ | "specifically designed for text embedding and ranking tasks", 텍스트 검색·코드 검색·분류·군집·이중언어 문장 찾기 — [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) |
| ⑦ | "well-suited for search and retrieval tasks, including classification, clustering, and semantic similarity search"; 학습 데이터 약 3,200억 토큰, 정보 검색용 합성·과제 데이터 포함 — [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card). Gemma3 기반을 양방향 어텐션으로 바꿈 — [HF blog](https://huggingface.co/blog/embeddinggemma) |
| ⑧ | 다중 과제 모델, LoRA 어댑터 5개(`retrieval.query`, `retrieval.passage`, `separation`, `classification`, `text-matching`) — [card](https://huggingface.co/jinaai/jina-embeddings-v3) |
| ⑨ | "optimizing for retrieval performance and inference efficiency" — [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) |
| ⑩ | "excels at multilingual retrieval", 16억 쌍으로 학습, consistency filtering — [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) |
| ⑪ | bge-m3를 한국어 질문–문서–어려운 오답(5개) 2,000,000건으로 CachedGISTEmbedLoss 미세조정, "Korean text retrieval" — [card](https://huggingface.co/nlpai-lab/KURE-v1) |
| ⑫ | 검색·RAG·분류·군집용, 과제별 지시 접두어 사용 — [card](https://huggingface.co/google/embeddinggemma-2) |
| ⑬ | 다국어 데이터 혼합으로 대조학습, 0.6b는 더 큰 임베딩 모델로부터 지식 증류 추가 — [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) |
| ⑭ | Qwen3-Embedding-4B로부터 임베딩 증류 + 과제별 대조 손실; 과제 `retrieval`, `text-matching`, `clustering`, `classification` — [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) |
| ⑮ | "Korean-English bilingual dense retrieval model" — [card](https://huggingface.co/nlpai-lab/KURE-v3); 기반 모델 Nemotron-3-Embed-1B-BF16 (메타데이터) [api](https://huggingface.co/api/models/nlpai-lab/KURE-v3) |
| ⑯ | "optimized for retrieval and semantic similarity tasks", 다국어·교차언어 검색, RAG용; Ministral-3-3B에서 가지치기+증류 — [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16) |

### Inferences
- ①은 교사 데이터에 msmarco-triplets(검색 데이터)가 섞여 있으므로 "검색 데이터를 전혀 안 봤다"고 쓰면 틀린다. 정확한 표현은 "문장 유사도·바꿔 말하기 중심의 증류 모델이며, 질문–문단 비대칭 검색 전용으로 학습된 모델은 아니다"이다.
- ①의 다국어 능력은 "같은 뜻의 번역문을 같은 벡터로" 맞추는 방식에서 온다. 그래서 한국어 질문–영어 문단처럼 **언어도 다르고 형태(질문 대 설명문)도 다른** 짝에는 따로 검증이 필요하다(추정).

### Gaps
- ②·⑥의 학습 데이터·손실의 세부(논문 arXiv 2407.19669, 2506.05176)는 이번에 읽지 않았다.
- ①의 학생 모델 초기값(어떤 다국어 MiniLM에서 시작했는지)은 카드·SBERT 문서에서 확인 못 함.

## 3. 필요한 질문/문단 접두어·지시문, trust_remote_code 필요 여부

### Takeaway
접두어를 안 붙이면 성능이 떨어진다고 카드가 명시한 모델: ④(`query: `/`passage: `), ⑤·⑬(질문에만 `Instruct: ...\nQuery: `), ⑩(`search_query: `/`search_document: `). ①·③·⑪은 접두어가 없다. `trust_remote_code=True`(저장소의 파이썬 코드를 내려받아 실행)가 필요한 모델: ②, ⑧, ⑩, ⑭.

### Cited Findings

| 모델 | 질문/문단 접두어 | trust_remote_code |
|---|---|---|
| ① | 없음. ST 설정에 prompts 항목 없음 [config_sentence_transformers.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/config_sentence_transformers.json), 카드 예제도 없음 [card](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 불필요 (표준 BertModel) [config.json](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/blob/main/config.json) |
| ② | 카드 예제에 접두어 없음 [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base) | **필요**: `SentenceTransformer(..., trust_remote_code=True)`, "Requires sentence-transformers>=3.0.0" [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base). 모델 코드는 별도 저장소 `Alibaba-NLP/new-impl` [config.json `auto_map`](https://huggingface.co/Alibaba-NLP/gte-multilingual-base/blob/main/config.json) |
| ③ | "no longer requires adding instructions to the queries" [card](https://huggingface.co/BAAI/bge-m3) | 불필요 (XLMRobertaModel) [config.json](https://huggingface.co/BAAI/bge-m3/blob/main/config.json) |
| ④ | `query: ` / `passage: ` 필수: "Yes, this is how the model is trained, otherwise you will see a performance degradation" [card](https://huggingface.co/intfloat/multilingual-e5-large) | 불필요 [config.json](https://huggingface.co/intfloat/multilingual-e5-large/blob/main/config.json) |
| ⑤ | 질문: `Instruct: {과제 한 문장}\nQuery: {질문}`, 문서: 없음; 지시문 없으면 성능 저하 [card](https://huggingface.co/intfloat/multilingual-e5-large-instruct) | 불필요 [config.json](https://huggingface.co/intfloat/multilingual-e5-large-instruct/blob/main/config.json) |
| ⑥ | 질문 prompt `Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:`, 문서 `""` [config_sentence_transformers.json](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/config_sentence_transformers.json). 지시문 사용 시 대부분 1–5% 향상, 다국어 환경에서도 지시문은 영어로 쓰라고 권장; transformers>=4.51.0 필요 [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 불필요 (Qwen3ForCausalLM 표준 구현) [config.json](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/config.json) |
| ⑦ | 질문 `task: search result \| query: {content}`, 문서 `title: {title \| "none"} \| text: {content}` [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card); ST의 `encode_query`/`encode_document`가 자동 적용 [HF blog](https://huggingface.co/blog/embeddinggemma) | 확인 못 함 (설정 파일 접근 불가) |
| ⑧ | `task="retrieval.query"` / `"retrieval.passage"`; ST prompts `Represent the query for retrieving evidence documents: ` / `Represent the document for retrieval: ` [config_sentence_transformers.json](https://huggingface.co/jinaai/jina-embeddings-v3/blob/main/config_sentence_transformers.json), [card](https://huggingface.co/jinaai/jina-embeddings-v3) | **필요** [card](https://huggingface.co/jinaai/jina-embeddings-v3) |
| ⑨ | 질문에만 `query: ` [config_sentence_transformers.json](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0/blob/main/config_sentence_transformers.json), [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) | 불필요 [config.json](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0/blob/main/config.json) |
| ⑩ | `search_query: ` / `search_document: ` 필수 ("must include a task instruction prefix") [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) | **필요** (카드 Limitations) [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) |
| ⑪ | 없음 (prompts `{}`) [config_sentence_transformers.json](https://huggingface.co/nlpai-lab/KURE-v1/blob/main/config_sentence_transformers.json) | 불필요 [config.json](https://huggingface.co/nlpai-lab/KURE-v1/blob/main/config.json) |
| ⑫ | SearchQuery `task: search result \| query: {query}`, Document `title: {title} \| text: {content}` (제목 없으면 `none`) [card](https://huggingface.co/google/embeddinggemma-2) | 확인 못 함 (카드 예제는 `SentenceTransformer(model_id)`만 사용 [Google 가이드](https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers)) |
| ⑬ | 질문: `Instruct: ...\nQuery: ` 필수, 문서: 없음 [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b), prompts `web_search_query` 등 [config_sentence_transformers.json](https://huggingface.co/microsoft/harrier-oss-v1-0.6b/blob/main/config_sentence_transformers.json) | 확인 못 함 (메타데이터 태그에 custom_code 없음 [api](https://huggingface.co/api/models/microsoft/harrier-oss-v1-0.6b)) |
| ⑭ | `Query: ` / `Document: ` [config_sentence_transformers.json](https://huggingface.co/jinaai/jina-embeddings-v5-text-small/blob/main/config_sentence_transformers.json), `task="retrieval"` [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) | **필요** [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) |
| ⑮ | `query: ` / `passage: `, `encode_query`/`encode_document`가 자동 적용 [card](https://huggingface.co/nlpai-lab/KURE-v3), [config_sentence_transformers.json](https://huggingface.co/nlpai-lab/KURE-v3/blob/main/config_sentence_transformers.json) | 확인 못 함 |
| ⑯ | `query: ` / `passage: ` [config_sentence_transformers.json](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16/blob/main/config_sentence_transformers.json) | 확인 못 함 |

### Inferences
- ②의 카드 transformers 예제 `outputs.last_hidden_state[:, 0][:dimension]`은 차원이 아니라 배치(문장 수) 축을 자른다. 차원을 줄이려면 `[:, :dimension]`이어야 한다. 카드 원문 코드를 그대로 베끼지 말 것(카드 원문은 [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base)).
- 접두어가 있는 모델을 비교에 넣으면, 접두어를 지켰는지가 비교 조건의 하나가 된다. ST의 `prompt_name`(또는 `encode_query`/`encode_document`)으로 넣으면 손으로 붙이는 실수를 줄일 수 있다.

### Gaps
- ⑦·⑫·⑬·⑮·⑯의 trust_remote_code 필요 여부는 실제 로딩으로만 확정 가능.

## 4. 라이선스와 사용 제한

### Takeaway
상업 이용 제한 없는 공개 라이선스: ①②⑥⑨⑩(Apache-2.0), ③④⑤⑪⑬(MIT), ⑫⑮(Apache-2.0), ⑯(OpenMDW-1.1). 제한 있음: ⑦(Gemma 이용약관, HF 승인 필요), ⑧·⑭(CC BY-NC 4.0, 비상업).

### Cited Findings

| 모델 | 라이선스 | 제한·비고 |
|---|---|---|
| ① | apache-2.0 [api](https://huggingface.co/api/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 없음 |
| ② | apache-2.0 [api](https://huggingface.co/api/models/Alibaba-NLP/gte-multilingual-base) | 없음 |
| ③ | mit [api](https://huggingface.co/api/models/BAAI/bge-m3) | 없음 |
| ④ | mit [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large) | 없음 |
| ⑤ | mit [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large-instruct) | 없음 |
| ⑥ | apache-2.0 [api](https://huggingface.co/api/models/Qwen/Qwen3-Embedding-0.6B) | 없음 |
| ⑦ | gemma [api](https://huggingface.co/api/models/google/embeddinggemma-300m); 카드 "Terms of Use" [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card) | HF 저장소 `gated: manual` — 로그인하고 약관에 동의해야 내려받을 수 있음 [api](https://huggingface.co/api/models/google/embeddinggemma-300m) |
| ⑧ | CC BY-NC 4.0: "If you need to use it beyond those platforms or on-premises within your company, note that the models is licensed under CC BY-NC 4.0" [card](https://huggingface.co/jinaai/jina-embeddings-v3) | 비상업 (CC BY-NC 4.0) [card](https://huggingface.co/jinaai/jina-embeddings-v3) |
| ⑨ | Apache 2.0 [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) | 없음 |
| ⑩ | apache-2.0 [api](https://huggingface.co/api/models/nomic-ai/nomic-embed-text-v2-moe) | 없음 |
| ⑪ | MIT [card](https://huggingface.co/nlpai-lab/KURE-v1) | 없음 |
| ⑫ | Apache 2.0 [card](https://huggingface.co/google/embeddinggemma-2); `gated: false` [api](https://huggingface.co/api/models/google/embeddinggemma-2) | 없음 |
| ⑬ | mit [api](https://huggingface.co/api/models/microsoft/harrier-oss-v1-0.6b) | 없음 |
| ⑭ | cc-by-nc-4.0 [api](https://huggingface.co/api/models/jinaai/jina-embeddings-v5-text-small) | 비상업 (cc-by-nc-4.0) [api](https://huggingface.co/api/models/jinaai/jina-embeddings-v5-text-small) |
| ⑮ | apache-2.0 [api](https://huggingface.co/api/models/nlpai-lab/KURE-v3) | 없음 |
| ⑯ | OpenMDW-1.1, "ready for commercial use" [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16) | 없음 |

### Inferences
- 이 과제는 비상업 학습 과제라 ⑧·⑭의 CC BY-NC도 쓸 수는 있다고 볼 수 있으나, 이것은 법적 판단이 아니라 추정이다. 사용자 확인이 필요한 지점이다.
- ⑦은 HF 로그인·약관 동의라는 사용자 손이 가는 일이 생긴다(Ollama의 `embeddinggemma`로 받으면 HF 승인 절차는 없음 — Ollama 페이지 근거 [ollama](https://ollama.com/library/embeddinggemma)).

### Gaps
- Gemma 이용약관의 금지 용도 조항 원문은 이번에 읽지 않았다.

## 5. 공식 지원 언어와 한국어 포함 여부

### Takeaway
카드 본문이나 공식 문서에 **한국어가 이름으로 나오는** 모델: ④(Mr. TyDi 표의 ko 열), ⑧(조정한 30개 언어), ⑪·⑮(한국어·영어), ⑬, ⑯(평가 34개 언어). ③·⑥·⑦·⑫·⑭는 "100개 이상 언어"라고만 하고 한국어를 이름으로 적지 않는다.

### Cited Findings

| 모델 | 공식 언어 범위 | 한국어 |
|---|---|---|
| ① | 50+ 언어 [SBERT Pretrained Models](https://sbert.net/docs/sentence_transformer/pretrained_models.html) | 카드 메타데이터 언어 목록(50개)에 ko 있음 [api](https://huggingface.co/api/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) (메타데이터) |
| ② | "over 70 languages" [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base) | 메타데이터 목록(75개)에 ko 있음 [api](https://huggingface.co/api/models/Alibaba-NLP/gte-multilingual-base) (메타데이터) |
| ③ | "more than 100 working languages" [card](https://huggingface.co/BAAI/bge-m3) | 공식 명시 확인 못 함 (카드에 언어 목록 없음). 한국어 검색 평가 결과는 KURE 카드에 있음 [KURE-v1 card](https://huggingface.co/nlpai-lab/KURE-v1) |
| ④ | xlm-roberta의 100개 언어, 저자원 언어는 성능 저하 가능 [card](https://huggingface.co/intfloat/multilingual-e5-large) | 카드 Mr. TyDi 표에 ko 열 [card](https://huggingface.co/intfloat/multilingual-e5-large); 메타데이터 목록에 ko [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large) |
| ⑤ | xlm-roberta의 100개 언어 [card](https://huggingface.co/intfloat/multilingual-e5-large-instruct) | 메타데이터 목록에 ko [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large-instruct) (메타데이터) |
| ⑥ | "100+ Languages" [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 확인 못 함 (언어 이름 목록 없음) |
| ⑦ | "100+ spoken languages" [Google 카드](https://ai.google.dev/gemma/docs/embeddinggemma/model_card) | 확인 못 함 |
| ⑧ | 기반은 100개 언어, 조정은 30개 언어 [card](https://huggingface.co/jinaai/jina-embeddings-v3) | **있음** (30개 목록에 Korean) [card](https://huggingface.co/jinaai/jina-embeddings-v3) |
| ⑨ | 카드 본문 언어 목록 확인 못 함 | 메타데이터 목록(74개)에 ko [api](https://huggingface.co/api/models/Snowflake/snowflake-arctic-embed-l-v2.0) (메타데이터) |
| ⑩ | "~100 languages" [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) | 메타데이터 목록(101개)에 ko [api](https://huggingface.co/api/models/nomic-ai/nomic-embed-text-v2-moe) (메타데이터) |
| ⑪ | "Korean, English" [card](https://huggingface.co/nlpai-lab/KURE-v1) | **있음** [card](https://huggingface.co/nlpai-lab/KURE-v1) |
| ⑫ | "100+ languages", 학습 데이터 140개 이상 언어 [card](https://huggingface.co/google/embeddinggemma-2) | 확인 못 함 |
| ⑬ | 목록에 Korean 포함 [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) | **있음** [card](https://huggingface.co/microsoft/harrier-oss-v1-0.6b) |
| ⑭ | "119+ languages" [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) | 확인 못 함 (카드 예문에 한국어 문장 한 줄은 있음 [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small)) |
| ⑮ | "Korean-English bilingual" [card](https://huggingface.co/nlpai-lab/KURE-v3) | **있음** [card](https://huggingface.co/nlpai-lab/KURE-v3) |
| ⑯ | 평가 34개 언어 [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16) | **있음** (34개 목록에 Korean) [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16) |

### Inferences
- "100개 이상 언어"만 적힌 모델(③·⑥·⑦·⑫·⑭)도 한국어를 실제로 다룰 가능성은 높지만, 과제 보고서에 "공식 지원"이라고 쓰려면 근거가 약하다. "카드에 한국어 명시 없음"으로 적는 것이 정확하다.
- 메타데이터의 language 목록은 업로드한 쪽이 적는 태그라 카드 본문보다 약한 근거다.

### Gaps
- ③·⑥·⑦의 기술 보고서(arXiv 2402.03216, 2506.05176, 2509.20354)의 학습 언어 목록은 읽지 않았다.

## 6. 공개일

### Takeaway
공식 발표일이 원문에 적힌 것: ⑦ 2025-09-04, ⑨ 2024-12-04, ⑭ 2026-02-18, ⑯ 2026-07-16. 나머지는 HF 저장소 생성일만 있다(공개일과 같다고 볼 근거 없음).

### Cited Findings

| 모델 | 원문에 적힌 공개일 | HF 저장소 생성일 (메타데이터) |
|---|---|---|
| ① | 확인 못 함 | 2022-03-02 [api](https://huggingface.co/api/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) |
| ② | 확인 못 함 (논문 arXiv 2407.19669) [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base) | 2024-07-20 [api](https://huggingface.co/api/models/Alibaba-NLP/gte-multilingual-base) |
| ③ | 확인 못 함 (카드 News의 가장 이른 항목 2024/2/1) [card](https://huggingface.co/BAAI/bge-m3) | 2024-01-27 [api](https://huggingface.co/api/models/BAAI/bge-m3) |
| ④ | 확인 못 함 (기술 보고서 arXiv 2402.05672) [card](https://huggingface.co/intfloat/multilingual-e5-large) | 2023-06-30 [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large) |
| ⑤ | 확인 못 함 | 2024-02-08 [api](https://huggingface.co/api/models/intfloat/multilingual-e5-large-instruct) |
| ⑥ | 확인 못 함 (카드에 "as of June 5, 2025" 순위 언급) [card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) | 2025-06-03 [api](https://huggingface.co/api/models/Qwen/Qwen3-Embedding-0.6B) |
| ⑦ | 2025-09-04 ("Today, Google releases EmbeddingGemma") [HF blog](https://huggingface.co/blog/embeddinggemma) | 2025-07-17 [api](https://huggingface.co/api/models/google/embeddinggemma-300m) |
| ⑧ | 확인 못 함 (arXiv 2409.10173) | 2024-09-05 [api](https://huggingface.co/api/models/jinaai/jina-embeddings-v3) |
| ⑨ | 2024-12-04 [card](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0) | 2024-11-08 [api](https://huggingface.co/api/models/Snowflake/snowflake-arctic-embed-l-v2.0) |
| ⑩ | 확인 못 함 (arXiv 2502.07972) | 2025-02-07 [api](https://huggingface.co/api/models/nomic-ai/nomic-embed-text-v2-moe) |
| ⑪ | 확인 못 함 | 2024-12-18 [api](https://huggingface.co/api/models/nlpai-lab/KURE-v1) |
| ⑫ | 확인 못 함 | 2026-09-14 [api](https://huggingface.co/api/models/google/embeddinggemma-2) |
| ⑬ | 확인 못 함 | 2026-03-30 [api](https://huggingface.co/api/models/microsoft/harrier-oss-v1-0.6b) |
| ⑭ | 2026-02-18 [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small) | 2026-01-22 [api](https://huggingface.co/api/models/jinaai/jina-embeddings-v5-text-small) |
| ⑮ | 확인 못 함 | 2026-10-15 [api](https://huggingface.co/api/models/nlpai-lab/KURE-v3) |
| ⑯ | 2026-07-16 [card](https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16) | 2026-07-14 [api](https://huggingface.co/api/models/nvidia/Nemotron-3-Embed-1B-BF16) |

### Inferences
- ①의 2022-03-02는 sentence-transformers 모델들이 HF 조직으로 일괄 옮겨진 날로 보인다(추정). ① 자체는 그보다 먼저 나왔을 수 있다.

### Gaps
- ①·②·③·④·⑤·⑥·⑧·⑩·⑪·⑫·⑬·⑮의 공식 발표일.

## 7. M3 Pro(36GB)에서의 로컬 실행: ST + MPS, 알려진 MPS 문제, Ollama, 메모리

### Takeaway
ST는 MPS(애플 실리콘 GPU)가 있으면 자동으로 그쪽에 모델을 올린다. 이번에 찾은 **알려진 MPS/맥 문제는 둘**: ⑥ Qwen3-Embedding-0.6B가 macOS에서 SDPA 어텐션으로 NaN 벡터를 내는 이슈(열려 있음, `attn_implementation="eager"`로 회피), ③ bge-m3의 MPS 메모리 누수 사용자 보고 1건. 그 밖의 모델은 "알려진 문제 확인 못 함"이지 "문제없음이 확인됨"이 아니다. 가중치 크기는 모두 수백 MB–수 GB로 36GB에 비해 작다. ①은 Ollama 공식 라이브러리에서 찾지 못했다(Ollama의 `paraphrase-multilingual`은 다른 모델인 mpnet-base-v2다).

### Cited Findings

ST와 MPS 일반
- "The model will automatically be placed on the most performant available device, e.g. cuda or mps if available" — [SBERT Computing Embeddings](https://sbert.net/examples/sentence_transformer/applications/computing-embeddings/README.html)

모델별 MPS·맥 관련 근거

| 모델 | MPS·맥 관련 원문 근거 |
|---|---|
| ① | 알려진 문제 확인 못 함 |
| ② | 카드는 xformers 설치·unpadding을 권장 [card](https://huggingface.co/Alibaba-NLP/gte-multilingual-base). 그러나 기본 설정은 `use_memory_efficient_attention: false`, `unpad_inputs: false` [config.json](https://huggingface.co/Alibaba-NLP/gte-multilingual-base/blob/main/config.json)이고, 모델 코드는 이때 `torch.nn.functional.scaled_dot_product_attention`을 쓴다 [new-impl modeling.py](https://huggingface.co/Alibaba-NLP/new-impl/blob/main/modeling.py). MPS 실행 보고는 확인 못 함 |
| ③ | 사용자 보고: MPS에서 약 3000문장 처리 후 RAM 20GB 초과, OOM으로 종료 (transformers로 `max_length=8192` 사용, 2025-03-01, 미해결) [HF 토론 #109](https://huggingface.co/BAAI/bge-m3/discussions/109) |
| ④ | 알려진 문제 확인 못 함 |
| ⑤ | 알려진 문제 확인 못 함 |
| ⑥ | "Qwen3 produces `nan` embeddings (SDPA + macOS)": macOS에서 CPU·MPS, FP32·FP16 모두 NaN, `attn_implementation="eager"`이면 정상; 이후 댓글에서 transformers 직접 호출은 CPU 정상·MPS NaN으로 보고 (2025-08-25 열림, 상태 open) [ST 이슈 #3498](https://github.com/huggingface/sentence-transformers/issues/3498) |
| ⑦ | 알려진 문제 확인 못 함 (float16 가능 여부도 확인 못 함 — 아래 ⑫의 경고는 ⑫ 전용) |
| ⑧ | 카드는 FlashAttention-2를 Ampere/Ada/Hopper GPU에서 선택 사항으로 언급 [card](https://huggingface.co/jinaai/jina-embeddings-v3). MPS 보고 확인 못 함 |
| ⑨ | 알려진 문제 확인 못 함 |
| ⑩ | "For best performance on GPU" megablocks 설치 권장; Limitations "Resource requirements may be higher than traditional dense models due to MoE architecture" [card](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe). MPS 보고 확인 못 함 |
| ⑪ | 알려진 문제 확인 못 함 |
| ⑫ | "Do not use `float16` ... In `float16` the model returns NaN or silently degraded embeddings rather than raising an error" — bfloat16 또는 float32 사용 [card](https://huggingface.co/google/embeddinggemma-2), [Google 가이드](https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers). 텍스트만 쓰면 `config_kwargs={"vision_config": None, "audio_config": None}`로 시각·음성 인코더(270M)를 안 올릴 수 있음 [Google 가이드](https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers) |
| ⑬ | 알려진 문제 확인 못 함 |
| ⑭ | 요구 버전 `transformers>=4.57.0`, `torch>=2.8.0`, `peft>=0.15.2`; flash-attention은 선택 [card](https://huggingface.co/jinaai/jina-embeddings-v5-text-small). MPS 보고 확인 못 함 |
| ⑮ | 카드 예제가 `attn_implementation="flash_attention_2"`로 불러옴 [card](https://huggingface.co/nlpai-lab/KURE-v3). MPS 보고 확인 못 함 |
| ⑯ | 알려진 문제 확인 못 함 |

Ollama 공식 라이브러리 (태그·파일 크기·문맥 길이는 Ollama 페이지 표기 그대로)

| 모델 | Ollama |
|---|---|
| ① | 공식 라이브러리에서 확인 못 함. `paraphrase-multilingual`은 `278m-mpnet-base-v2-fp16` 태그·563MB·512 context로, 다른 모델(paraphrase-multilingual-mpnet-base-v2, 768차원)이다 [ollama](https://ollama.com/library/paraphrase-multilingual/tags), [readme](https://ollama.com/library/paraphrase-multilingual) |
| ② | 확인 못 함 (Ollama 검색 "gte"에서 나오지 않음 [search](https://ollama.com/search?q=gte)) |
| ③ | `bge-m3:567m`, 1.2GB, 8K context [ollama](https://ollama.com/library/bge-m3/tags) |
| ④ | 공식 아님: 커뮤니티 업로드 `jeffh/intfloat-multilingual-e5-large`, `home-rag/multilingual-e5-large` [search](https://ollama.com/search?q=e5) |
| ⑤ | 공식 아님: 커뮤니티 `jeffh/intfloat-multilingual-e5-large-instruct` [search](https://ollama.com/search?q=e5) |
| ⑥ | `qwen3-embedding:0.6b`, 639MB, 32K context [ollama](https://ollama.com/library/qwen3-embedding/tags) |
| ⑦ | `embeddinggemma:300m` 622MB, `300m-qat-q4_0` 239MB, 2K context; Ollama v0.11.10 이상 필요 [ollama tags](https://ollama.com/library/embeddinggemma/tags), [readme](https://ollama.com/library/embeddinggemma) |
| ⑧ | 확인 못 함 (검색 "jina" 상위 결과에 v3 없음 [search](https://ollama.com/search?q=jina)) |
| ⑨ | `snowflake-arctic-embed2:568m`, 1.2GB, 8K context [ollama](https://ollama.com/library/snowflake-arctic-embed2/tags) |
| ⑩ | `nomic-embed-text-v2-moe:latest`, 958MB, 512 context [ollama](https://ollama.com/library/nomic-embed-text-v2-moe/tags) |
| ⑪ | 공식 아님: 커뮤니티 `daynice/kure-v1` [search](https://ollama.com/search?q=kure) |
| ⑫ | `embeddinggemma-2:270m/440m/570m/740m`, 304MB–1.3GB, "256K context window" 표기 [ollama](https://ollama.com/library/embeddinggemma-2/tags) |
| ⑬ | 공식 아님: 커뮤니티 `leoipulsar/harrier-0.6b` [search](https://ollama.com/search?q=harrier) |
| ⑭ | 공식 아님: 커뮤니티 `corvojaeger/jina-embeddings-v5-text-small` [search](https://ollama.com/search?q=jina) |
| ⑮ | 확인 못 함 |
| ⑯ | 확인 못 함 |

참고(목록 밖, Ollama에서 발견): `granite-embedding:278m` — 563MB, 512 context, 지원 언어에 Korean 포함, Apache 2.0, 2024-12-18 공개 [ollama](https://ollama.com/library/granite-embedding), [tags](https://ollama.com/library/granite-embedding/tags)

메모리 관련 원문 값
- ③ `pytorch_model.bin` 2,271,145,830 bytes [파일 목록 API](https://huggingface.co/api/models/BAAI/bge-m3/tree/main)
- ⑦ 양자화 시 "under 200 MB of RAM" [HF blog](https://huggingface.co/blog/embeddinggemma)

### Inferences
- 가중치만의 대략 메모리(계산값, 측정 아님: 파라미터 수 × float32 4바이트): ① 약 0.47GB, ② 약 1.2GB, ③·⑨·⑪ 약 2.3GB, ④·⑤ 약 2.2GB, ⑥·⑬ 약 2.4GB, ⑦ 약 1.2GB, ⑧ 약 2.3GB, ⑩ 약 1.9GB, ⑫ 약 3.0GB(텍스트만 올리면 더 작음), ⑮·⑯ 약 4.6GB. 실제 사용량은 배치 크기와 입력 길이에 따른 활성값이 더해진다. 36GB 통합 메모리에서 어느 것도 가중치 때문에 못 올릴 수준은 아니다.
- ③의 누수 보고는 입력을 8192토큰까지 패딩한 사용법에서 나온 단일 사례다. 위키 청크처럼 짧은 입력·작은 배치에서는 다를 수 있으나, 확인은 실행으로만 가능하다.
- ⑬ harrier와 ⑭ jina-v5는 ⑥과 같은 Qwen3 구조라서 ⑥의 macOS SDPA NaN 문제가 같이 나타날 수 있다(추정, 근거 이슈 없음). 쓸 경우 첫 실행에서 NaN 검사를 넣는 것이 안전하다.
- ⑮는 카드 예제의 flash_attention_2가 맥에서 쓸 수 없는 CUDA 전용 구현이므로, 맥에서는 이 인자를 빼고 불러야 할 것이다(추정).
- Ollama로 돌리면 PyTorch MPS 문제(⑥ NaN, ③ 누수)를 피할 수 있으나, 같은 모델이라도 Ollama 쪽은 GGUF 변환본이라 ST 결과와 수치가 다를 수 있다(추정). 비교 실험에서는 한 실행 방식으로 통일하는 것이 공정하다.

### Gaps
- 이번 조사에서는 어떤 모델도 실제로 M3 Pro에서 실행해 보지 않았다. "MPS에서 돈다"는 주장은 모든 모델에 대해 실행으로 확인해야 한다.
- ⑧·⑩·⑭(커스텀 코드 모델)의 MPS 호환성 보고는 찾지 못했다.
- Ollama의 ⑫ 문맥 길이 256K와 카드 8,192 중 어느 것이 실제 적용값인지 확인 못 함.
