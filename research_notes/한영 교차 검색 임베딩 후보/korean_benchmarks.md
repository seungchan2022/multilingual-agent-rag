# Open-weight embedding models on Korean retrieval benchmarks (2025–2026), and their English / Korean↔English ability

> **정정(2026-10-23, Codex 4단계 검토 1차 지적 7·2차 지적 2)**: 이 메모의 "Observed run-to-run spread", "near noise" 같은 표현은 서로 다른 곳에서 같은 모델을 잰 점수가 약 0.01 달랐다는 관찰일 뿐이다. 같은 조건으로 다시 잰 흔들림 폭은 확인되지 않았다. KURE-v1과 bge-m3의 차이는 0.7616 − 0.7509 = 0.0107이다(`decisions/references.md` S12 (마)).


Research date: 2026-10-23. "Self-reported" = the model's own authors published the number. "Third-party" = someone else ran it. "Raw" = I read the value from a stored result JSON file, not from a summary table.

Conventions used throughout:
- **Belebele direction (verified in mteb source).** In mteb `BelebeleRetrieval`, a subset named `X-Y` uses **X as the passage (corpus) language and Y as the query language**: `lang_corpus, lang_question = languages[0], languages[1]`, where `"{x}-eng_Latn" -> [x, "eng-Latn"]` — [mteb belebele_retrieval.py @3e7f34a](https://github.com/embeddings-benchmark/mteb/blob/3e7f34a7167c1c76030e9e7f1ec06eda2cc89f2b/mteb/tasks/retrieval/multilingual/belebele_retrieval.py). So:
  - `kor_Hang-kor_Hang` = Korean query → Korean passage (Q_ko→P_ko)
  - `kor_Hang-eng_Latn` = **English query → Korean passage** (Q_en→P_ko)
  - `eng_Latn-kor_Hang` = **Korean query → English passage** (Q_ko→P_en)
  - Cross-check: arXiv 2507.08480 reports multilingual-e5-large Belebele "en-ko 92.03 / ko-en 86.45", which equal the MTEB-results subsets `kor_Hang-eng_Latn` 0.9203 and `eng_Latn-kor_Hang` 0.8645. So the paper's "en-ko" means English query → Korean doc.
- **XPQA direction is NOT verified.** The mteb task file only lists `eng-kor` / `kor-eng` pairs. The query/corpus assignment happens in a preprocessed dataset I did not inspect — [mteb xpqa_retrieval.py @3e7f34a](https://github.com/embeddings-benchmark/mteb/blob/3e7f34a7167c1c76030e9e7f1ec06eda2cc89f2b/mteb/tasks/retrieval/multilingual/xpqa_retrieval.py).
- **Observed run-to-run spread: about 0.01 nDCG@10.** The same model run independently by two parties gives different values:
  - Qwen3-Embedding-0.6B, KURE repo vs MTEB results repo:
    - Belebele ko-ko 0.9124 vs 0.9222
    - AutoRAG 0.8338 vs 0.8292
    - Ko-StrategyQA 0.7586 vs 0.7655
    - Belebele Q_ko→P_en 0.8572 vs 0.8618
  - EmbeddingGemma-300m: Belebele ko-ko 0.9430 vs 0.9414.
  - Differences below about 0.01 should not be read as real ranking differences.
  - Sources: [KURE raw results @ac3d004](https://github.com/nlpai-lab/KURE/tree/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results) and [MTEB results repo @0acf39c](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results).

## Q1. What Korean retrieval benchmarks exist, and which open models top them (with scores)?

### Takeaway
The most current and largest Korean leaderboard is the nlpai-lab KURE repo's **MTEB(kor, v2) Retrieval**: 9 Korean tasks, nDCG@10, updated 2026-10-22. The overall top models there are 1–8B or late-interaction models (KURE-v2, Nemotron-3-Embed-8B, KURE-v3, Qwen3-Embedding-8B). Among ~0.6B single-vector models, the Korean fine-tunes of bge-m3 / arctic-embed-l-v2.0 (snowflake-arctic-embed-l-v2.0-ko 0.7653, KURE-v1 0.7616, BGE-m3-ko 0.7547) sit only 0.004–0.014 above bge-m3 (0.7509). That gap is roughly the observed run-to-run spread. The two assignment-recommended models rank lower:
- gte-multilingual-base is not on the KURE leaderboard. It is 17th of 22 on the older 7-task card and 12th of 17 on the KURE-v1 card (top-1 Recall).
- paraphrase-multilingual-MiniLM-L12-v2 is far behind on every Korean retrieval task with data.

### Cited Findings

**Benchmark inventory**
- **MTEB(kor, v2) Retrieval** (as defined in the KURE repo; date 2026-10-22). The 9 tasks are:
  - Ko-StrategyQA
  - AutoRAGRetrieval
  - MIRACLRetrieval (ko, dev split)
  - PublicHealthQA
  - BelebeleRetrieval (only `kor_Hang-kor_Hang`)
  - MrTidyRetrieval
  - MultiLongDocRetrieval (mean of dev and test)
  - LawIRKo
  - SQuADKorV1Retrieval

  Metric: average nDCG@10, plus Recall@10 — [KURE README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/README.md); conventions in [make_leaderboard_mteb_kor.py @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/make_leaderboard_mteb_kor.py).
- **Older "Korean Retrieval Benchmark" (7 tasks, nDCG@10)**, used on the dragonkue model cards. It has the 8 tasks minus MultiLongDoc, which is reported separately, and it includes **XPQA**. It has no LawIRKo or SQuADKorV1. Its averages are **not comparable** with MTEB(kor, v2) averages — [dragonkue/snowflake-arctic-embed-l-v2.0-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko) (no date on the card).
- **KURE-v1 / KoE5 card benchmark.** It averages 8 Korean tasks (the 7 above plus MultiLongDoc) as Recall / Precision / NDCG / F1 at top-k 1/3/5/10. This is a third aggregate, and all its column headers are mislabelled "_top1" even in the k=3/5/10 tables — [KURE-v1 card](https://huggingface.co/nlpai-lab/KURE-v1), [KoE5 card](https://huggingface.co/nlpai-lab/KoE5).
- **AutoRAG Korean embedding benchmark (Marker-Inc-Korea).**
  - Corpus: parsed PDFs in finance, public sector, medical, legal, and commerce — per the [snowflake-ko card's dataset description](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko).
  - Metrics: F1, Recall, Precision, mAP, mRR, NDCG at k = 1/3/5/10/50.
  - No date is on the page — [GitHub README](https://github.com/Marker-Inc-Korea/AutoRAG-example-korean-embedding-benchmark).
  - It is also packaged as the MTEB task AutoRAGRetrieval.
- **MIRACL-ko (nDCG@10) and MKQA-ko (Korean queries retrieving from the English Wikipedia corpus, Recall@100).** These are used in the BGE-M3 paper — [arXiv 2402.03216 HTML](https://arxiv.org/html/2402.03216).
- **Ko-StrategyQA paired with English StrategyQA, and Belebele ko/en, as Korean↔English CLIR benchmarks** — [arXiv 2507.08480 HTML](https://arxiv.org/html/2507.08480), v2 2026-05-19.

**Ranking 1 — MTEB(kor, v2) Retrieval, average nDCG@10 over 9 tasks** ([KURE dense results README @ac3d004, commit 2026-10-22](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md)).
- All rows were run by nlpai-lab.
- They are **self-reported for nlpai-lab models** (KURE-*, KoE5) and **third-party for all others**.
- Columns: Type / Params / Avg nDCG@10 / Avg Recall@10. Recall comes from the [README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/README.md).

| # | Model | Type | Params | Avg nDCG@10 | Avg R@10 |
|---|---|---|---|---|---|
| 1 | nlpai-lab/KURE-v2 | late-interaction | 154M | 0.8160 | 0.8921 |
| 2 | nvidia/Nemotron-3-Embed-8B-BF16 | dense | 8.0B | 0.8127 | 0.8934 |
| 3 | yjoonjang/colbert-ko-en-v2 | late-interaction | 149M | 0.8063 | 0.8827 |
| 4 | nlpai-lab/KURE-v3 | dense | 1.1B | 0.8027 | 0.8857 |
| 5 | sionic-ai/comsat-embed-ko-8b-preview | dense | 7.6B | 0.7927 | 0.8876 |
| 6 | lightonai/mLateOn | late-interaction | 307M | 0.7906 | 0.8740 |
| 7 | Qwen/Qwen3-Embedding-8B | dense | 7.6B | 0.7826 | 0.8815 |
| 8 | nvidia/Nemotron-3-Embed-1B-BF16 | dense | 1.1B | 0.7817 | 0.8690 |
| 9 | Qwen/Qwen3-Embedding-4B | dense | 4.0B | 0.7737 | 0.8753 |
| 10 | perplexity-ai/pplx-embed-v1-4b | dense | 4.0B | 0.7705 | 0.8699 |
| 11 | microsoft/harrier-oss-v1-27b | dense | 27.0B | 0.7667 | 0.8624 |
| 12 | dragonkue/snowflake-arctic-embed-l-v2.0-ko | dense | 568M | 0.7653 | 0.8609 |
| 13 | codefuse-ai/F2LLM-v2-8B | dense | 7.6B | 0.7638 | 0.8593 |
| 14 | telepix/PIXIE-Rune-v1.5 | dense | 568M | 0.7618 | 0.8596 |
| 15 | nlpai-lab/KURE-v1 | dense | 568M | 0.7616 | 0.8629 |
| 16 | nvidia/llama-nemotron-embed-1b-v2 | dense | 1.2B | 0.7564 | 0.8560 |
| 17 | dragonkue/BGE-m3-ko | dense | 568M | 0.7547 | 0.8513 |
| 18 | BAAI/bge-m3 | dense | 568M | 0.7509 | 0.8588 |
| 19 | jinaai/jina-embeddings-v5-text-small-retrieval | dense | 596M | 0.7419 | 0.8434 |
| 20 | perplexity-ai/pplx-embed-v1-0.6b | dense | 596M | 0.7390 | 0.8377 |
| 21 | perplexity-ai/pplx-embed-v1-late-0.6b | late-interaction | 596M | 0.7381 | 0.8328 |
| 22 | nlpai-lab/KoE5 | dense | 560M | 0.7337 | 0.8300 |
| 23 | nlpai-lab/KURE-v2-unsupervised | late-interaction | 154M | 0.7283 | 0.8268 |
| 24 | google/embeddinggemma-300m | dense | 308M | 0.7254 | 0.8383 |
| 25 | Qwen/Qwen3-Embedding-0.6B | dense | 596M | 0.7140 | 0.8222 |
| 26 | dragonkue/colbert-ko-0.1b | late-interaction | 149M | 0.6776 | 0.7723 |
| 27 | yjoonjang/colbert-ko-v1 | late-interaction | 149M | 0.6282 | 0.7212 |

- **gte-multilingual-base, multilingual-e5-large, and paraphrase-multilingual-MiniLM-L12-v2 are not in this leaderboard** — same README.
- **My spot-check of the raw files.** I recomputed per-task values from the raw JSON for bge-m3 and KURE-v1, and they match the README exactly:
  - bge-m3:
    - AutoRAG 0.8301
    - Belebele ko-ko 0.9315
    - Ko-StrategyQA 0.7941
    - LawIRKo 0.7174
    - MIRACL 0.7015
    - MrTidy 0.6471
    - MLDR (0.4301+0.4273)/2 = 0.4287
    - PublicHealthQA 0.8041
    - SQuADKorV1 0.9038
  - KURE-v1: AutoRAG 0.87076 → 0.8708; MLDR (0.4753+0.4521)/2 = 0.4637.
  - Source: [KURE raw results @ac3d004](https://github.com/nlpai-lab/KURE/tree/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results).
- **The bge-m3 Korean numbers in the KURE repo are not an independent replication.** They are the same files (model revision 5617a9f, mteb 1.12.75 for Belebele) as in the MTEB results repo — [MTEB results bge-m3 BelebeleRetrieval.json @0acf39c](https://github.com/embeddings-benchmark/results/blob/0acf39c2bd00210e746b163fdcf215954f281af0/results/BAAI__bge-m3/5617a9f61b028005a4858fdac845db406aefb181/BelebeleRetrieval.json).
- **Per-task, MTEB(kor, v2), nDCG@10, for selected dense models** (same README @ac3d004):

| Model | AutoRAG | PublicHealthQA | Ko-StrategyQA | LawIRKo | SQuADKorV1 | Belebele(ko-ko) | MrTidy | MLDR | MIRACL |
|---|---|---|---|---|---|---|---|---|---|
| KURE-v3 | 0.9324 | 0.8639 | 0.8192 | 0.8158 | 0.9666 | 0.9673 | 0.6320 | 0.4781 | 0.7489 |
| Qwen3-Embedding-8B | 0.8276 | 0.8721 | 0.8363 | 0.8171 | 0.9063 | 0.9824 | 0.6187 | 0.5046 | 0.6783 |
| snowflake-arctic-embed-l-v2.0-ko | 0.9093 | 0.8337 | 0.8050 | 0.7735 | 0.9447 | 0.9518 | 0.5712 | 0.4304 | 0.6685 |
| KURE-v1 | 0.8708 | 0.8193 | 0.7999 | 0.7426 | 0.9357 | 0.9502 | 0.5909 | 0.4637 | 0.6816 |
| BGE-m3-ko | 0.8738 | 0.8155 | 0.7959 | 0.7322 | 0.9414 | 0.9503 | 0.6099 | 0.3899 | 0.6833 |
| bge-m3 | 0.8301 | 0.8041 | 0.7941 | 0.7174 | 0.9038 | 0.9315 | 0.6471 | 0.4287 | 0.7015 |
| KoE5 | 0.8434 | 0.8351 | 0.8001 | 0.7756 | 0.8980 | 0.9425 | 0.5841 | 0.3015 | 0.6235 |
| embeddinggemma-300m | 0.8187 | 0.8170 | 0.8008 | 0.6850 | 0.9114 | 0.9430 | 0.5253 | 0.3844 | 0.6434 |
| Qwen3-Embedding-0.6B | 0.8338 | 0.8107 | 0.7586 | 0.7526 | 0.8490 | 0.9124 | 0.4870 | 0.4199 | 0.6023 |

- **The two assignment-recommended models plus multilingual-e5-large, per task, nDCG@10, from the MTEB results repo.**
  - These are raw values I extracted. Submitters vary, so I treat them as third-party relative to the Korean fine-tune authors.
  - No 9-task average is possible for these models, because LawIRKo and SQuADKorV1 are missing.
  - The bge-m3 row is shown for comparison (same files as above).
  - Sources ([MTEB results @0acf39c](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results)):
    - [MiniLM folder bf3bf13](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/sentence-transformers__paraphrase-multilingual-MiniLM-L12-v2/bf3bf13ab40c3157080a7ab344c831b9ad18b5eb)
    - gte-multilingual-base folders [7fc0678](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/Alibaba-NLP__gte-multilingual-base/7fc06782350c1a83f88b15dd4b38ef853d3b8503) and [ca1791e](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/Alibaba-NLP__gte-multilingual-base/ca1791e0bcc104f6db161f27de1340241b13c5a4)
    - multilingual-e5-large folders [4dc6d85](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/intfloat__multilingual-e5-large/4dc6d853a804b9c8886ede6dda8a073b7dc08a81) and [ab10c1a](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/intfloat__multilingual-e5-large/ab10c1a7f42e74530fe7ae5be82e6d4f11a719eb)

| Model | AutoRAG | Ko-StrategyQA | MIRACL-ko (dev) | MrTidy-ko | PublicHealthQA | Belebele ko-ko | MLDR-ko dev / test |
|---|---|---|---|---|---|---|---|
| paraphrase-multilingual-MiniLM-L12-v2 | 0.4230 | 0.4590 | 0.2568 | 0.1272 | 0.6741 | 0.7149 | 0.0838 / 0.1051 |
| gte-multilingual-base | 0.7711 | 0.7512 | 0.6270 | 0.5646 | 0.7523 | not in repo | not in repo (ko) |
| multilingual-e5-large | 0.8134 | 0.8035 | not in repo (ko) | not in repo (ko) | 0.8232 | 0.9450 | not in repo (ko) |
| bge-m3 (reference) | 0.8301 | 0.7941 | 0.7015 | 0.6471 | 0.8041 | 0.9315 | 0.4301 / 0.4273 |

- **Ranking 2 — older 7-task Korean Retrieval Benchmark, average nDCG@10.** Source: dragonkue card, no date. It is self-reported for dragonkue models and third-party for others. The card lists 22 models; the values below are a selection in card order, which leaves out PwC-Embedding_expr, e5-mistral-7b-instruct, gte-Qwen2-7B-instruct, SFR-Embedding-2_R, and granite-embedding-278m. Values:
  - dragonkue/snowflake-arctic-embed-l-v2.0-ko 0.740433
  - dragonkue/BGE-m3-ko 0.729993
  - KURE-v1 0.727739
  - bge-m3 0.724169
  - Snowflake/snowflake-arctic-embed-l-v2.0 0.724104
  - multilingual-e5-large 0.721607
  - KoE5 0.711356
  - bge-multilingual-gemma2 0.704274
  - jina-embeddings-v3 0.701314
  - multilingual-e5-large-instruct 0.69837
  - nomic-embed-text-v2-moe 0.693773
  - multilingual-e5-base 0.689429
  - Qwen3-Embedding-0.6B 0.676200
  - gte-multilingual-base 0.663766
  - openai text-embedding-3-large 0.662239
  - upskyy/bge-m3-korean 0.6567
  - jhgan/ko-sroberta-multitask 0.526301

  The same card has a separate MultiLongDocRetrieval table. gte-multilingual-base is **first** there at 0.48402, then KURE-v1 0.47528, snowflake-ko 0.4459, and bge-m3 0.43011 — [dragonkue/snowflake-arctic-embed-l-v2.0-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko).
- **Ranking 3 — KURE-v1 card, 8-task average, top-1 Recall.** Self-reported for KURE and KoE5; no date. Values:
  - KURE-v1 0.52640
  - BGE-m3-ko 0.52361
  - bge-m3 0.51778
  - snowflake-arctic-embed-l-v2.0 0.51246
  - KoE5 0.50157
  - multilingual-e5-large 0.50052
  - gte-multilingual-base 0.46469 (12th of 17)
  - upskyy/bge-m3-korean 0.43125

  At top-10 Recall, bge-m3 (0.79195) is above BGE-m3-ko (0.78450) and only 0.005 below KURE-v1 (0.79682) — [KURE-v1 card](https://huggingface.co/nlpai-lab/KURE-v1).
- **Ranking 4 — AutoRAG Korean benchmark.** Third-party (Marker-Inc-Korea); no date on the page.
  - At top-1, all metrics are equal:
    - KU-HIAI-ONTHEIT-large-v1.1 0.7193
    - KU-HIAI-ONTHEIT-large-v1 0.7105
    - KoE5 0.6930
    - bge-m3 0.6754
    - Upstage Embedding (API) 0.6579
    - openai_embed_3_large 0.6053
    - gte-multilingual-base 0.5877
    - multilingual-e5-large-instruct 0.4649
    - **paraphrase-multilingual-MiniLM-L12-v2 0.2982 (last of 16)**
  - Recall@5: bge-m3 0.9298, KoE5 0.9035, gte-multilingual-base 0.8596, MiniLM 0.4912.
  - Source: [AutoRAG-example-korean-embedding-benchmark README](https://github.com/Marker-Inc-Korea/AutoRAG-example-korean-embedding-benchmark).
- **Conflict.** The dragonkue/BGE-m3-ko card reproduces the AutoRAG table with different values:
  - bge-m3 top-1 0.6578, vs 0.6754 in the AutoRAG README
  - KoE5 top-1 0.7018, vs 0.6930
  - It adds BGE-m3-ko at top-1 0.7456 (self-reported), which would rank first — [BGE-m3-ko card](https://huggingface.co/dragonkue/BGE-m3-ko); contradicted for bge-m3/KoE5 by the [AutoRAG README](https://github.com/Marker-Inc-Korea/AutoRAG-example-korean-embedding-benchmark).
- **BGE-M3 paper (self-reported by BAAI, Feb 2024), MIRACL dev, ko, nDCG@10:**
  - M3 Dense 69.9; M3 All (dense + sparse + multi-vector) 72.1
  - mE5-large 66.5
  - E5-mistral-7b 61.8
  - BM25 37.1

  Source: [arXiv 2402.03216](https://arxiv.org/html/2402.03216).
- **Qwen3-Embedding and EmbeddingGemma.** On the Korean-only leaderboard above, the Qwen3-Embedding ranks are 7 (8B), 9 (4B), and 25 (0.6B), and embeddinggemma-300m is 24 — [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md).

### Inferences
- Among models a laptop can run locally (≤ ~0.6B, single dense vector), the Korean-retrieval leaders cluster tightly. On MTEB(kor, v2): snowflake-ko 0.7653, PIXIE-Rune 0.7618, KURE-v1 0.7616, BGE-m3-ko 0.7547, bge-m3 0.7509. The spread across all five (0.0144) is barely above the ~0.01 run-to-run spread, so "Korean fine-tune beats bge-m3" is a small effect on Korean benchmarks.
- On every Korean task with data, gte-multilingual-base is consistently below bge-m3: AutoRAG −0.059, Ko-StrategyQA −0.043, MIRACL −0.075, MrTidy −0.083, PublicHealthQA −0.052. The exception is long documents (MLDR), where gte is the best of the cards' models.
- On Korean retrieval, paraphrase-multilingual-MiniLM-L12-v2 is roughly half of bge-m3 or worse: MIRACL 0.2568 vs 0.7015, MrTidy 0.1272 vs 0.6471, AutoRAG 0.4230 vs 0.8301.
- The AutoRAG top-1 values look like multiples of 1/114 (0.2982 ≈ 34/114, 0.7193 ≈ 82/114). That suggests about 114 queries, so one query is worth about 0.009 at top-1. Small differences there are noise.
- Belebele uses short parallel FLORES passages, and most models score above 0.9 on it. It discriminates weakly between strong models.

### Gaps
- Two items came only from a search-tool summary, without opening the pages, so they are unverified and not used:
  - a community leaderboard `su-park/mteb_ko_leaderboard`, reportedly last updated October 2024
  - a claim that Qwen3-Embedding-8B was No.1 on MMTEB (multilingual MTEB, not Korean) at 70.58 on 2025-06-05
- I did not confirm whether "MTEB(kor, v2)" is an official mteb benchmark name or nlpai-lab's own label. I also did not check the official MTEB leaderboard UI for a Korean tab.
- There is no Korean leaderboard row for gte-multilingual-base, multilingual-e5-large, or MiniLM on LawIRKo / SQuADKorV1, so they have no 9-task averages.
- No benchmark found covers Korean or English retrieval over **infobox / numeric-table content** (the user's rare-earth Wikipedia corpus). MIRACL and Mr.TyDi are Wikipedia prose passages.
- The model cards give no release dates; only the KURE repo gives a release log.

## Q2. Korean fine-tunes: base model, data, Korean gain over base, and English / cross-lingual retention

### Takeaway
The main 0.6B Korean fine-tunes are KURE-v1, BGE-m3-ko, snowflake-arctic-embed-l-v2.0-ko, and KoE5. They are trained on Korean query–document–hard-negative data from bge-m3, arctic-embed-l-v2.0, or multilingual-e5-large. None of their model cards reports English or Korean↔English scores. However, raw result files in the KURE repo (Belebele cross-lingual subsets) and its English RTEB table show **no loss**: Korean fine-tuning of bge-m3 slightly *raised* Belebele Korean↔English scores (+0.02), and KURE-v1 matches bge-m3 on English RTEB (0.5202 vs 0.5151). In contrast, Korean-only late-interaction models (colbert-ko-v1, colbert-ko-0.1b) collapse on cross-lingual retrieval.

### Cited Findings

**Model facts (from model cards; no dates on cards unless stated)**

nlpai-lab/KURE-v1 — [KURE-v1 card](https://huggingface.co/nlpai-lab/KURE-v1); [KURE README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/README.md)
- Base: BAAI/bge-m3.
- Data: "Korean query-document-hard_negative(5) data", 2,000,000 examples (dataset-size tag 1879136).
- Training: CachedGISTEmbedLoss, batch 4096, lr 2e-5, 1 epoch.
- Spec: 1024-dim, 8192 tokens, MIT license.
- Released 2024-12-21 per the README log.

nlpai-lab/KoE5 — [KoE5 card](https://huggingface.co/nlpai-lab/KoE5)
- Base: intfloat/multilingual-e5-large.
- Data: ko-triplet-v1.0, about 700k+ examples (745k rows; dataset updated 2024-11-29).
- Training: CachedMultipleNegativesRankingLoss, batch 512, 1 epoch.
- Spec: 512-token limit, MIT license.
- Released 2024-10-02 per the README log.

dragonkue/BGE-m3-ko — [BGE-m3-ko card](https://huggingface.co/dragonkue/BGE-m3-ko)
- Base: BAAI/bge-m3.
- Data: "additionally trained on the Korean dataset"; no dataset names given.
- Training: batch 32768, lr 3e-5, 3 epochs.
- The card says that after training, miracl cosine_ndcg@10 **dropped by 0.02** vs base, while NDCG on a financial AutoRAG set rose 0.09 (top-1). It gives no base-model table to verify this. Self-reported.

dragonkue/snowflake-arctic-embed-l-v2.0-ko — [snowflake-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko)
- Base: Snowflake/snowflake-arctic-embed-l-v2.0.
- Data: AI Hub Korean machine-reading-comprehension sets (administrative, general, news, books, numerical-operation, finance/legal) plus "clustered datasets".
- Training: CachedGISTEmbedLoss, max length 1300.
- English claim: "Based on my own experience" it outperformed BGE-M3 across domains. This is anecdotal, with no numbers.

nlpai-lab/KURE-v3 — [KURE-v3 card](https://huggingface.co/nlpai-lab/KURE-v3); [KURE README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/README.md)
- Released **2026-10-20** (3 days before this research).
- 1.1B params, 2048-dim (Matryoshka 1024/512/256), 8192 tokens, Apache-2.0.
- Uses "query: " / "passage: " prompts.
- Called "a Korean-English bilingual dense retrieval model".
- Base chain is confusing: the README lists base nvidia/Nemotron-3-Embed-1B-BF16, while the HF model tree lists mistralai/Ministral-3-3B-Base-2512 as base and Nemotron-3-Embed-1B as parent.
- The card states no training data.
- All its numbers are self-reported.

nlpai-lab/KURE-v2 — [KURE README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/README.md)
- Released 2026-08-29.
- **Late-interaction** (ColBERT-style multi-vector), 154M params, base skt/A.X-Encoder-base.
- It is not a drop-in single-vector model.

upskyy/bge-m3-korean
- Fine-tune of bge-m3. Base and data are from its name only; I did not open its card.
- It scores **below** bge-m3 on every Korean table seen:
  - MTEB-ko 7-task 0.6567 vs 0.724169
  - KURE-v1 card top-1 Recall 0.43125 vs 0.51778
- Sources: [snowflake-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko), [KURE-v1 card](https://huggingface.co/nlpai-lab/KURE-v1).

**Korean gain over the base model** (MTEB(kor, v2) average nDCG@10; [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md))
- bge-m3 0.7509 → KURE-v1 0.7616 (+0.0107), BGE-m3-ko 0.7547 (+0.0038).
- snowflake-arctic-embed-l-v2.0 → snowflake-ko 0.7653. The base is not on the v2 leaderboard. On the older 7-task table: 0.724104 → 0.740433 (+0.0163) — [snowflake-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko).
- multilingual-e5-large → KoE5 0.7337. The base is not on v2. On the 7-task table KoE5 is **below** its base: 0.711356 vs 0.721607 (same card).
- Per task, the Korean fine-tunes of bge-m3 lose on MrTidy and MIRACL:
  - MrTidy: bge-m3 0.6471 vs KURE-v1 0.5909 and BGE-m3-ko 0.6099
  - MIRACL: bge-m3 0.7015 vs KURE-v1 0.6816 and BGE-m3-ko 0.6833

  They gain on AutoRAG, LawIRKo, and SQuADKorV1 (same README). MrTidy and MIRACL are the **Wikipedia-based** tasks.

**English retention after Korean fine-tuning — RTEB(eng)** ([KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md))
- The benchmark is 8 public non-code tasks: legal, finance, and medical (CUREv1, ChatDoctor, FinQA, AILACasedocs, LegalSummarization, HC3Finance, FinanceBench, AILAStatutes). The metric is mean nDCG@10.
- It is **not** the official RTEB leaderboard number, and it is self-reported for KURE models.
- Values:
  - Nemotron-3-Embed-8B 0.7390
  - comsat-embed-ko-8b 0.6921
  - Qwen3-Embedding-8B 0.6861
  - **KURE-v3 0.6859**
  - pplx-embed-v1-4b 0.6812
  - Nemotron-3-Embed-1B 0.6650
  - Qwen3-Embedding-4B 0.6549
  - F2LLM-v2-8B 0.6403
  - pplx-0.6b 0.6369
  - jina-v5-small 0.6069
  - Qwen3-Embedding-0.6B 0.5802
  - mLateOn 0.5720
  - **embeddinggemma-300m 0.5531**
  - PIXIE-Rune-v1.5 0.5457
  - pplx-late-0.6b 0.5246
  - **KURE-v1 0.5202**
  - **bge-m3 0.5151**
  - KURE-v2 0.4504
- So KURE-v1 vs its base bge-m3 is 0.5202 vs 0.5151: no English loss on this measure.
- KURE-v2 (Korean-tuned late-interaction from a Korean/English encoder) is the lowest at 0.4504.
- BGE-m3-ko, snowflake-ko, and KoE5 have **no** RTEB(eng) results in the repo (their result folders contain only `mteb_kor`) — [KURE raw results @ac3d004](https://github.com/nlpai-lab/KURE/tree/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results).

**Korean↔English cross-lingual retention — Belebele subsets, nDCG@10**
- These are raw values I extracted from the stored JSON. In the KURE repo they were run by nlpai-lab (self-reported for KURE/KoE5, third-party for others). The KURE leaderboard itself does not use these cross-lingual subsets.
- Sources: [KURE raw results @ac3d004, `<model>/mteb_kor/**/BelebeleRetrieval.json`](https://github.com/nlpai-lab/KURE/tree/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results), and, where marked (M), [MTEB results repo @0acf39c](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results).

| Model | Type | Q_ko→P_ko (`kor_Hang-kor_Hang`) | Q_en→P_ko (`kor_Hang-eng_Latn`) | **Q_ko→P_en** (`eng_Latn-kor_Hang`) |
|---|---|---|---|---|
| comsat-embed-ko-8b-preview | dense 7.6B | 0.9853 | 0.9903 | 0.9806 |
| Qwen3-Embedding-8B | dense 7.6B | 0.9824 | 0.9881 | 0.9777 |
| Nemotron-3-Embed-8B | dense 8B | 0.9714 | 0.9723 | 0.9634 |
| Nemotron-3-Embed-1B | dense 1.1B | 0.9629 | 0.9663 | 0.9424 |
| KURE-v3 | dense 1.1B | 0.9673 | 0.9638 | 0.9395 |
| Qwen3-Embedding-4B | dense 4B | 0.9522 | 0.9574 | 0.9354 |
| embeddinggemma-300m | dense 308M | 0.9430 | 0.9521 | 0.9296 |
| embeddinggemma-300m (M) | dense 308M | 0.9414 | 0.9513 | 0.9293 |
| BGE-m3-ko | dense 568M | 0.9503 | 0.9243 | 0.9124 |
| PIXIE-Rune-v1.5 | dense 568M | 0.9617 | 0.9437 | 0.9102 |
| KURE-v1 | dense 568M | 0.9502 | 0.9237 | 0.9058 |
| KURE-v2 | late-int. 154M | 0.9660 | 0.8840 | 0.9048 |
| KoE5 | dense 560M | 0.9425 | 0.9365 | 0.9039 |
| snowflake-arctic-embed-l-v2.0-ko | dense 568M | 0.9518 | 0.9226 | 0.8978 |
| bge-m3 (M; same file in KURE repo) | dense 568M | 0.9315 | 0.9032 | 0.8832 |
| snowflake-arctic-embed-l-v2.0 (base) (M) | dense (size not read) | 0.9271 | 0.8936 | 0.8666 |
| multilingual-e5-large (M) | dense (size not read) | 0.9450 | 0.9203 | 0.8645 |
| Qwen3-Embedding-0.6B (M) | dense 596M | 0.9222 | 0.9130 | 0.8618 |
| Qwen3-Embedding-0.6B | dense 596M | 0.9124 | 0.9108 | 0.8572 |
| paraphrase-multilingual-MiniLM-L12-v2 (M) | dense (size not read) | 0.7149 | 0.7579 | 0.7038 |
| dragonkue/colbert-ko-0.1b | late-int. 149M | 0.9644 | 0.5985 | 0.8051 |
| yjoonjang/colbert-ko-v1 | late-int. 149M | 0.9154 | 0.1487 | 0.4105 |

- **Base → Korean fine-tune deltas on Q_ko→P_en, the user's hardest direction:**
  - bge-m3 0.8832 → KURE-v1 0.9058 (+0.023) and BGE-m3-ko 0.9124 (+0.029).
    - These runs also used different mteb versions: bge-m3 1.12.75, KURE-v1 1.21.6, BGE-m3-ko 1.19.4.
    - Even so, both deltas exceed the ~0.005 spread observed on this subset between two Qwen3-0.6B runs (0.8572 vs 0.8618).
  - arctic-l-v2.0 0.8666 → snowflake-ko 0.8978 (+0.031). Base and fine-tune were run by different parties with different mteb versions (1.18.0 vs 2.12.30).
  - mE5-large 0.8645 → KoE5 0.9039 (+0.039). Different runners.
- **Korean-only ColBERT models lose cross-lingual ability.** colbert-ko-v1 drops to 0.1487 (Q_en→P_ko), while its sibling colbert-ko-en-v2 (Korean+English) scores 0.8597 there — same KURE raw files.
- **Independent CLIR study: arXiv 2507.08480** (Jang et al.; v2 2026-05-19; ACL 2026 MeLLM Workshop).
  - Base models before fine-tuning, nDCG@10, labels as "query lang-doc lang":
    - bge-m3: Belebele en-ko 90.37 / ko-en 88.36; StrategyQA en-ko 81.24 / ko-en **71.65**
    - multilingual-e5-large: 92.03 / 86.45; 82.04 / **67.30**
    - gte-multilingual-base: 88.06 / 85.66; 80.54 / **64.38**
    - multilingual-e5-base: 82.28 / 77.52; 77.94 / 54.44
  - The paper finds that adding cross-lingual training data raises CLIR but slightly lowers monolingual IR. For bge-m3 "koenen": ko-en CLIR avg 80.01 → 81.26, en-en mono avg 89.99 → 89.55. The authors say Model Merging mitigates the trade-off.
  - It reports no Korean-only or English-only training runs.
  - Source: [arXiv 2507.08480 HTML](https://arxiv.org/html/2507.08480); [abstract page](https://arxiv.org/abs/2507.08480).
  - Independence caveat: the author list includes Youngjoon Jang (who publishes the yjoonjang/colbert-ko-* models) and Heuiseok Lim. Affiliations are not shown on the abstract page, so I could not confirm overlap with nlpai-lab (KURE). The paper does not evaluate KURE.

### Inferences
- For bge-m3-family Korean fine-tunes (KURE-v1, BGE-m3-ko), the evidence suggests Korean fine-tuning did **not** hurt, and slightly helped, Korean↔English retrieval on Belebele. KURE-v1 did not hurt English on RTEB(eng). However, all of KURE-v1's English and cross-lingual evidence was produced by its own authors, and Belebele is near ceiling.
- Korean fine-tunes of bge-m3 lose 0.02–0.06 on the two **Wikipedia** Korean tasks (MrTidy, MIRACL). Their gains come from PDF, legal, and SQuAD-style tasks. The user's corpus is Wikipedia, so bge-m3's Korean "deficit" vs KURE-v1 may not apply to this corpus.
- For every **dense** model in the Belebele table, including MiniLM, **Korean query → English passage** is the weakest of the three directions. The same holds for all four base models on StrategyQA in 2507.08480. Examples: bge-m3 0.8832 vs 0.9032 the other way; StrategyQA ko-en 71.65 vs en-ko 81.24. This is the case the user worries about (Korean questions answerable only from English documents).
- The Korean-tuned late-interaction models are the exception: they are weakest the other way, on English query → Korean passage. Examples: KURE-v2 0.8840 vs 0.9048; colbert-ko-0.1b 0.5985 vs 0.8051; colbert-ko-v1 0.1487 vs 0.4105.

### Gaps
- There are no English benchmark numbers anywhere for BGE-m3-ko, snowflake-arctic-embed-l-v2.0-ko, KoE5, or upskyy/bge-m3-korean. Their cross-lingual evidence is only the Belebele subsets above.
- I found no third-party (non-nlpai-lab) English or cross-lingual evaluation of KURE-v1.
- KURE-v3 has no cross-lingual numbers beyond the Belebele raw file, no stated training data, and was released 3 days ago.
- I did not open the upskyy model card.
- I could not verify XPQA query/passage direction, so XPQA cross-lingual numbers are omitted from the conclusions. For reference only, XPQA `eng-kor` / `kor-eng` nDCG@10 (MTEB results repo):
  - MiniLM 0.2151 / 0.2260
  - gte-multilingual-base 0.3177 / 0.2937
  - multilingual-e5-large 0.3109 / 0.3402
  - Qwen3-0.6B 0.3230 / 0.2747
  - snowflake-arctic-l-v2.0 0.3778 / 0.3915

## Q3. Where do bge-m3, gte-multilingual-base, multilingual-e5-large, Qwen3-Embedding, EmbeddingGemma, and paraphrase-multilingual-MiniLM-L12-v2 rank on Korean benchmarks, and how do they do on English / Korean↔English?

### Takeaway
On Korean retrieval, the order of the named general-purpose models is:

Qwen3-Embedding-8B (0.7826) > Qwen3-Embedding-4B (0.7737) > bge-m3 (0.7509) > EmbeddingGemma-300m (0.7254) > Qwen3-Embedding-0.6B (0.7140), all on MTEB(kor, v2).

The other three named models differ:
- multilingual-e5-large is roughly tied with bge-m3 overall, and mixed per task:
  - 7-task card: 0.721607 vs 0.724169
  - MTEB repo, where it is higher: Ko-StrategyQA 0.8035 vs 0.7941, PublicHealthQA 0.8232 vs 0.8041, Belebele ko-ko 0.9450 vs 0.9315
  - MTEB repo, where it is lower: AutoRAG 0.8134 vs 0.8301
- gte-multilingual-base is below bge-m3 on every Korean task with data except long documents.
- paraphrase-multilingual-MiniLM-L12-v2 is far behind everywhere.

On Korean↔English (Belebele and MKQA), bge-m3 is solid but not top among small models. EmbeddingGemma-300m scores higher than bge-m3 on both cross-lingual directions despite its lower Korean average. MiniLM is the weakest by a wide margin.

### Cited Findings

**bge-m3 (568M, dense; also sparse and multi-vector modes)**
- Korean, MTEB(kor, v2): 0.7509, rank 18 of 27. On MrTidy it is 2nd of 27 (0.6471), behind only Nemotron-3-Embed-8B (0.6540), and the best among models of 1.1B or fewer — [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md).
- Korean, older 7-task table: 0.724169 (4th of 22) — [snowflake-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko).
- Korean, AutoRAG top-1: 0.6754 (4th of 16) — [AutoRAG README](https://github.com/Marker-Inc-Korea/AutoRAG-example-korean-embedding-benchmark).
- Korean↔English, Belebele:
  - Q_en→P_ko 0.9032
  - Q_ko→P_en 0.8832
  - en-en 0.9563
  - Source: [MTEB results bge-m3 BelebeleRetrieval.json @0acf39c](https://github.com/embeddings-benchmark/results/blob/0acf39c2bd00210e746b163fdcf215954f281af0/results/BAAI__bge-m3/5617a9f61b028005a4858fdac845db406aefb181/BelebeleRetrieval.json).
- Korean query → English Wikipedia, **MKQA-ko Recall@100** (self-reported, BAAI, Feb 2024):
  - M3 Dense 71.6; M3 All 71.8
  - mE5-large 68.1
  - OpenAI-3 63.9
  - E5-mistral-7b 59.4
  - BM25 27.9
  - Source: [arXiv 2402.03216](https://arxiv.org/html/2402.03216).
- StrategyQA (2507.08480): ko→en 71.65, en→ko 81.24, en-en 84.42 — [arXiv 2507.08480](https://arxiv.org/html/2507.08480).
- English, RTEB(eng) 8-task: 0.5151 — [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md).

**gte-multilingual-base (dense; size not read)**
- Korean, 7-task table: 0.663766 (17th of 22), but **1st on MultiLongDocRetrieval** (0.48402) — [snowflake-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko).
- Korean, per task (MTEB results repo):
  - AutoRAG 0.7711
  - Ko-StrategyQA 0.7512
  - MIRACL-ko 0.6270
  - MrTidy-ko 0.5646
  - PublicHealthQA 0.7523
  - Folders: [7fc0678](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/Alibaba-NLP__gte-multilingual-base/7fc06782350c1a83f88b15dd4b38ef853d3b8503), [ca1791e](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/Alibaba-NLP__gte-multilingual-base/ca1791e0bcc104f6db161f27de1340241b13c5a4).
- Korean, AutoRAG top-1: 0.5877 (7th of 16) — [AutoRAG README](https://github.com/Marker-Inc-Korea/AutoRAG-example-korean-embedding-benchmark).
- Korean↔English (2507.08480, independent):
  - Belebele en→ko 88.06, ko→en 85.66, ko-ko 87.96, en-en 94.63
  - StrategyQA en→ko 80.54, ko→en **64.38**, en-en 84.26
  - CLIR overall 79.66 vs bge-m3 82.91
  - Source: [arXiv 2507.08480](https://arxiv.org/html/2507.08480).
- The MTEB results repo has no Korean Belebele subsets for this model.

**multilingual-e5-large (dense; size not read from its own card)**
- Korean, 7-task table: 0.721607 (6th of 22) — [snowflake-ko card](https://huggingface.co/dragonkue/snowflake-arctic-embed-l-v2.0-ko).
- Korean, BGE-M3 paper MIRACL-ko: 66.5 — [arXiv 2402.03216](https://arxiv.org/html/2402.03216).
- Korean↔English, Belebele (MTEB results repo): Q_en→P_ko 0.9203, Q_ko→P_en 0.8645 — [ab10c1a folder](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/intfloat__multilingual-e5-large/ab10c1a7f42e74530fe7ae5be82e6d4f11a719eb).
- Korean↔English, StrategyQA ko→en: 67.30 — [arXiv 2507.08480](https://arxiv.org/html/2507.08480).
- MKQA-ko R@100: 68.1 — [arXiv 2402.03216](https://arxiv.org/html/2402.03216).

**Qwen3-Embedding (0.6B / 4B / 8B, dense, decoder-based)**
- Korean, MTEB(kor, v2) — [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md):
  - 8B: 0.7826 (rank 7)
  - 4B: 0.7737 (rank 9)
  - 0.6B: 0.7140 (rank 25)
- Korean↔English, Belebele Q_ko→P_en: 8B 0.9777, 4B 0.9354, 0.6B 0.8572–0.8618 (two runs) — KURE raw files and [MTEB results Qwen3-0.6B folder](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/Qwen__Qwen3-Embedding-0.6B/b22da495047858cce924d27d76261e96be6febc0).
- English, RTEB(eng): 8B 0.6861, 4B 0.6549, 0.6B 0.5802 (all above bge-m3's 0.5151) — [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md).

**EmbeddingGemma-300m (308M, dense)**
- Korean, MTEB(kor, v2): 0.7254 (rank 24) — [KURE results README @ac3d004](https://github.com/nlpai-lab/KURE/blob/ac3d004c1012e181a20171a6b6211b8d2272d461/eval/dense/results/README.md).
- Korean↔English, Belebele: Q_en→P_ko 0.9521 / 0.9513 and Q_ko→P_en 0.9296 / 0.9293. These come from two independent runs (KURE repo / MTEB repo) that agree within 0.001 — [MTEB results embeddinggemma folder 64614b0](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/google__embeddinggemma-300m/64614b0b8b64f0c6c1e52b07e4e9a4e8fe4d2da2).
- English, RTEB(eng): 0.5531 (bge-m3 0.5151) — same KURE README.

**paraphrase-multilingual-MiniLM-L12-v2**
- Korean, per task (MTEB results repo):
  - AutoRAG 0.4230
  - Ko-StrategyQA 0.4590
  - MIRACL-ko 0.2568
  - MrTidy-ko 0.1272
  - PublicHealthQA 0.6741
  - MLDR-ko 0.0838 / 0.1051
  - Folder: [bf3bf13](https://github.com/embeddings-benchmark/results/tree/0acf39c2bd00210e746b163fdcf215954f281af0/results/sentence-transformers__paraphrase-multilingual-MiniLM-L12-v2/bf3bf13ab40c3157080a7ab344c831b9ad18b5eb).
- Korean, AutoRAG top-1: 0.2982 (last of 16) — [AutoRAG README](https://github.com/Marker-Inc-Korea/AutoRAG-example-korean-embedding-benchmark).
- Korean↔English, Belebele: ko-ko 0.7149, Q_en→P_ko 0.7579, Q_ko→P_en 0.7038 — same MTEB folder.
- It is not on the KURE, dragonkue 7-task, or KURE-v1-card leaderboards.

### Inferences
- **Ranking the user's three candidates on Korean retrieval: bge-m3 > gte-multilingual-base >> paraphrase-multilingual-MiniLM-L12-v2.** The same order holds on Korean↔English: bge-m3 CLIR overall 82.91 vs gte 79.66 (2507.08480); Belebele Q_ko→P_en bge-m3 0.8832 vs MiniLM 0.7038. This makes bge-m3 a reasonable third "strong reference".
- If the reference model should be stronger than bge-m3 on Korean while staying ~0.6B, dense, and local, there are two options:
  - **KURE-v1**: same architecture and size as bge-m3. It scores slightly higher on Korean overall (+0.011, near noise), Belebele Korean↔English (+0.02), and English RTEB (+0.005), but **lower on the Wikipedia tasks** MrTidy and MIRACL. Its evidence is self-reported.
  - **EmbeddingGemma-300m**: smaller, lower on Korean overall (0.7254), but stronger than bge-m3 on both Korean↔English directions and on English RTEB. It is independently replicated on Belebele.
- Larger options (Qwen3-Embedding-4B/8B, Nemotron-3-Embed-8B, KURE-v3) lead every Korean, cross-lingual, and English table but are 1–8B. Whether they are practical locally depends on the user's hardware, which I did not assess.
- The only directly on-target public evidence for "Korean question, English Wikipedia document" is MKQA-ko from the BGE-M3 paper (self-reported, 2024). It does not include the newer models. A small in-domain test on the user's own 20 articles would be more decisive than any of these leaderboards.

### Gaps
- No Korean↔English numbers were found for gte-multilingual-base on Belebele in MTEB format (only the 2507.08480 paper numbers), and none for multilingual-e5-large on MIRACL-ko / MrTidy-ko in the MTEB repo (ko subset missing).
- No MKQA-ko numbers were found for gte-multilingual-base, Qwen3-Embedding, EmbeddingGemma, or KURE-v1. The MTEB-repo MKQA files for bge-m3, Qwen3-0.6B, and EmbeddingGemma contain no ko subset. MiniLM's MKQA file has a `train:ko` value (0.0262) whose setup I did not verify, so I excluded it.
- No English RTEB numbers were found for gte-multilingual-base, multilingual-e5-large, or MiniLM.
- I did not verify licenses for every model. Licenses stated on cards I read: KURE-v1 MIT, KoE5 MIT, KURE-v3 Apache-2.0.
- I did not verify official Qwen3-Embedding or EmbeddingGemma model-card scores; only the third-party Korean runs above were used.
