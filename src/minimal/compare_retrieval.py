"""조합 8개(청크 묶음 4개 × 모델 2개)로 질문 38개를 검색해 채점하고, 정해진 기준대로 조합 하나를 고르는 프로그램.

  uv run python src/minimal/compare_retrieval.py                  # 검색 304번 → results.jsonl → summary.md
  uv run python src/minimal/compare_retrieval.py --summary-only   # 검색 없이 있는 results.jsonl에서 요약만 다시 만든다

규칙은 decisions/stage4.md의 2026-10-23 줄(비교에서 재는 것 / 가장 많은 것을 고르되 2개 이하 차이는 비김 / 비긴 조합을 고르는 순서 /
검색 예산은 1,024토큰 / Codex 1차 검토 ㉣·㉤·㉦·㉧ / MiniLM은 비교에서 재기 전에 뺀다 / 청크마다 원문 줄 번호 목록)에 있다.
검색은 src/minimal/search.py, 모델은 src/minimal/index.py의 load_model이다. 요약은 results.jsonl만 읽고(청크 묶음 수치만 청크 파일에서 읽는다)
시계와 무작위를 쓰지 않으므로 같은 파일에서는 같은 요약이 나온다. 요약에 찍는 시간은 출력의 걸린 시간뿐이고, 결과 줄의 시간 칸(embed_seconds, search_seconds)은 요약이 읽지 않는다.
"""
import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from index import CHUNK_SETS, CHUNKS, DSN, MODELS, QUESTIONS, ROOT, load_model, read_chunks  # noqa: E402
from search import embed_query, search  # noqa: E402

OUT_DIR = ROOT / "data" / "minimal" / "retrieval"
RESULTS = OUT_DIR / "results.jsonl"
SUMMARY = OUT_DIR / "summary.md"
K = {128: 8, 256: 4}   # 크기별 k. 명목 예산 1,024토큰(크기 × k)이 같다
MAX_GAP = 2            # 가장 많은 전체 ✔와 이 수 이하로 차이 나는 조합은 비긴 것이다
GROUPS = [(lang, branch) for lang in ("ko", "en") for branch in ("한국어만", "영어만", "두 언어")]
GTE = "gte-multilingual-base"
MODEL_ORDER = [GTE, "bge-m3"]   # 고르는 순서 5칸


def parse_chunk_set(name):
    """'size128_notitle' -> (128, False). 크기와 제목을 붙였는지를 이름에서 읽는다."""
    m = re.fullmatch(r"size(\d+)_(title|notitle)", name)
    return int(m.group(1)), m.group(2) == "title"


def is_cross(question):
    """질문 언어와 근거 언어가 다른 16개((ko, 영어만) 8 + (en, 한국어만) 8)에 드는가."""
    return (question["lang"], question["branch"]) in (("ko", "영어만"), ("en", "한국어만"))


def matched_evidence(question, chunk):
    """chunk(doc_id, lines, text)가 채운 근거 번호 목록(질문 evidence[]의 0부터 센 자리).
    근거 하나를 채우는 조건: doc_id가 같고, 그 line이 청크 lines에 있고, value_text가 청크 text에 글자 그대로 든다.
    줄 범위(line_start~line_end)는 보지 않는다. 표 조각은 줄이 이어지지 않기 때문이다."""
    found = []
    for i, e in enumerate(question["evidence"]):
        if not e["value_text"]:
            raise ValueError(f"{question['id']} 근거 {i}: value_text가 비어 있다(빈 글은 어느 글에나 들어 채점이 거짓이 된다)")
        if e["doc_id"] == chunk["doc_id"] and e["line"] in chunk["lines"] and e["value_text"] in chunk["text"]:
            found.append(i)
    return found


def result_row(chunk_set, model, question, found, embed_seconds, search_seconds):
    """검색 결과 found(search의 (chunk_id, distance, doc_id, lines, text, tokens, language, line_start, line_end) 목록, 순위 순)를 결과 파일의 한 줄로 바꾼다.
    query는 검색 쿼리로, 최소판은 질문 글 그대로다. embed_seconds는 그 질문 글을 벡터로 바꾼 시간, search_seconds는 search 호출 하나의 시간이다."""
    size, _ = parse_chunk_set(chunk_set)
    retrieved = []
    for rank, (chunk_id, distance, doc_id, lines, text, tokens, language, line_start, line_end) in enumerate(found, 1):
        evidence = matched_evidence(question, {"doc_id": doc_id, "lines": lines, "text": text})
        retrieved.append({"rank": rank, "chunk_id": chunk_id, "doc_id": doc_id, "language": language, "distance": distance,
                          "lines": list(lines), "line_start": line_start, "line_end": line_end, "tokens": tokens, "evidence": evidence})
    hit_ranks = [r["rank"] for r in retrieved if r["evidence"]]
    return {"chunk_set": chunk_set, "model": model, "k": K[size], "question_id": question["id"], "lang": question["lang"],
            "branch": question["branch"], "cross": is_cross(question), "query": question["question"],
            "embed_seconds": embed_seconds, "search_seconds": search_seconds, "hit": bool(hit_ranks), "hit_ranks": hit_ranks,
            "retrieved": retrieved, "retrieved_tokens": sum(r["tokens"] for r in retrieved)}


def run_search(questions):
    """조합 8개 × 질문 38개를 검색해 결과 줄 목록을 만든다(모델 → 청크 묶음 → 질문 순). 질문 벡터는 모델마다 한 번만 만든다.
    그래서 같은 모델의 청크 묶음 4개는 같은 질문에 같은 embed_seconds를 쓴다(조합마다 다시 재지 않는다)."""
    import psycopg
    rows = []
    with psycopg.connect(DSN) as conn:
        for model_key in MODELS:
            model = load_model(model_key)
            vectors, embed_seconds = [], []
            for q in questions:
                start = time.perf_counter()
                vectors.append(embed_query(model, q["question"]))
                embed_seconds.append(time.perf_counter() - start)
            for chunk_set in CHUNK_SETS:
                k = K[parse_chunk_set(chunk_set)[0]]
                for q, vector, embed_s in zip(questions, vectors, embed_seconds):
                    start = time.perf_counter()
                    found = search(conn, chunk_set, model_key, vector, k)
                    search_s = time.perf_counter() - start
                    rows.append(result_row(chunk_set, model_key, q, found, embed_s, search_s))
                print(f"검색함: {chunk_set} × {model_key}: 질문 {len(questions)}개, k = {k}", flush=True)
    return rows


def write_results(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def read_results(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def combo_counts(rows):
    """결과 줄에서 조합마다 센다. {(chunk_set, model): {total, n, groups{(lang, branch): (✔, 질문 수)}, cross, cross_n, tokens[]}}.
    조합의 순서는 결과 파일에 처음 나온 순서다."""
    counts = {}
    for r in rows:
        c = counts.setdefault((r["chunk_set"], r["model"]), {"total": 0, "n": 0, "groups": {}, "cross": 0, "cross_n": 0, "tokens": []})
        c["total"] += r["hit"]
        c["n"] += 1
        hit, n = c["groups"].get((r["lang"], r["branch"]), (0, 0))
        c["groups"][(r["lang"], r["branch"])] = (hit + r["hit"], n + 1)
        if r["cross"]:
            c["cross"] += r["hit"]
            c["cross_n"] += 1
        c["tokens"].append(r["retrieved_tokens"])
    return counts


# 고르는 순서(비긴 조합끼리). (이름, 값(클수록 앞선다), 값을 보이는 글). 앞 칸에서 값이 정확히 같을 때만 다음 칸으로 간다.
STEPS = [
    ("1. 다른 언어 16개의 ✔ 수가 많은 조합", lambda combo, c: c["cross"], lambda combo, c: f"{c['cross']}/{c['cross_n']}"),
    ("2. 과제 권장 모델(gte-multilingual-base)을 쓴 조합", lambda combo, c: combo[1] == GTE, lambda combo, c: "예" if combo[1] == GTE else "아니오"),
    ("3. 제목을 붙이지 않은 조합", lambda combo, c: not parse_chunk_set(combo[0])[1], lambda combo, c: "붙임" if parse_chunk_set(combo[0])[1] else "붙이지 않음"),
    ("4. 청크 크기가 작은 조합", lambda combo, c: -parse_chunk_set(combo[0])[0], lambda combo, c: str(parse_chunk_set(combo[0])[0])),
    ("5. 모델 순서(gte-multilingual-base → bge-m3)", lambda combo, c: -MODEL_ORDER.index(combo[1]), lambda combo, c: combo[1]),
]


def choose(counts):
    """조합 하나를 고른다. {best, tied(비긴 조합과 전체 ✔), steps(칸마다 들어온 조합의 값과 남은 조합), chosen}를 돌려준다.
    비긴 조합이 하나뿐이면 steps는 비어 있다. 5칸까지 가고도 둘 이상 남으면 RuntimeError(일어나면 안 되는 일)."""
    best = max(c["total"] for c in counts.values())
    tied = [combo for combo, c in counts.items() if c["total"] >= best - MAX_GAP]
    remaining, steps = tied, []
    for name, key, show in STEPS:
        if len(remaining) == 1:
            break
        top = max(key(combo, counts[combo]) for combo in remaining)
        steps.append({"name": name, "values": [(combo, show(combo, counts[combo])) for combo in remaining],
                      "remaining": [combo for combo in remaining if key(combo, counts[combo]) == top]})
        remaining = steps[-1]["remaining"]
    if len(remaining) != 1:
        raise RuntimeError(f"5칸까지 가도 하나로 갈리지 않음: {remaining}")
    return {"best": best, "tied": [(combo, counts[combo]["total"]) for combo in tied], "steps": steps, "chosen": remaining[0]}


def label(combo):
    return f"{combo[0]} × {combo[1]}"


def percentile90(values):
    """가장 가까운 순위(nearest rank) 방식 90%: 작은 순서로 세어 ceil(0.9 × n)번째 값."""
    ordered = sorted(values)
    return ordered[-(-9 * len(ordered) // 10) - 1]


def num(x):
    return str(int(x)) if x == int(x) else f"{x:.1f}"


def distribution(values):
    """(최소, 중앙값, 90%, 최대). 값이 없으면 None."""
    if not values:
        return None
    return min(values), statistics.median(values), percentile90(values), max(values)


def chunk_stats(chunk_rows):
    """청크 묶음 하나의 수치: 청크 수, 토큰 분포, 한도를 넘긴 청크의 수·토큰 분포(최소, 중앙값, 최대)·문서별 수."""
    over = [r for r in chunk_rows if r["over_limit"]]
    per_doc = {}
    for r in over:
        per_doc[r["doc_id"]] = per_doc.get(r["doc_id"], 0) + 1
    over_dist = distribution([r["tokens"] for r in over])
    return {"n": len(chunk_rows), "tokens": distribution([r["tokens"] for r in chunk_rows]), "over_n": len(over),
            "over": over_dist and (over_dist[0], over_dist[1], over_dist[3]), "per_doc": dict(sorted(per_doc.items()))}


def read_chunk_stats(chunk_sets):
    return {s: chunk_stats(read_chunks(CHUNKS / f"{s}.jsonl")) for s in chunk_sets}


def build_summary(rows, stats):
    """결과 줄(read_results의 결과)과 청크 묶음 수치(chunk_stats)로 요약 글을 만든다. 시간·무작위는 쓰지 않는다."""
    counts = combo_counts(rows)
    picked = choose(counts)
    out = ["# 검색 비교 요약", "",
           f"결과 파일 `data/minimal/retrieval/results.jsonl`의 {len(rows)}줄(조합 {len(counts)}개)에서 계산했다. "
           "크기 128 묶음은 k = 8, 256 묶음은 k = 4로, 명목 예산이 1,024토큰으로 같다. "
           "✔는 가져온 청크 가운데 근거 하나와 문서가 같고, 그 줄이 청크의 줄 번호 목록에 있고, `value_text`가 청크 글에 글자 그대로 든 청크가 있는 질문이다.", "",
           "## 조합별 ✔ 수", "",
           "| 청크 묶음 | 모델 | k | 전체 ✔ | " + " | ".join(f"{lang}·{branch}" for lang, branch in GROUPS) + " | 다른 언어 16개 ✔ |",
           "|" + "---|" * (len(GROUPS) + 5)]
    for combo, c in counts.items():
        k = K[parse_chunk_set(combo[0])[0]]
        cells = [f"{c['groups'].get(g, (0, 0))[0]}/{c['groups'].get(g, (0, 0))[1]}" for g in GROUPS]
        out.append(f"| {combo[0]} | {combo[1]} | {k} | {c['total']}/{c['n']} | " + " | ".join(cells) + f" | {c['cross']}/{c['cross_n']} |")
    out += ["", "## 가져온 청크의 토큰 합(질문마다)", "",
            "같은 명목 예산으로 견줬으므로 실제로 가져온 양은 조합마다 다르다. 토큰은 bge-m3 토크나이저로 센 값이다.", "",
            "| 청크 묶음 | 모델 | 평균 | 최소 | 최대 |", "|---|---|---|---|---|"]
    for combo, c in counts.items():
        out.append(f"| {combo[0]} | {combo[1]} | {num(round(sum(c['tokens']) / len(c['tokens']), 1))} | {min(c['tokens'])} | {max(c['tokens'])} |")

    out += ["", "## 고른 조합", "",
            f"- 가장 많은 전체 ✔: {picked['best']}. 이 수와 차이가 {MAX_GAP}개 이하({picked['best'] - MAX_GAP} 이상)인 조합이 비긴 것이다.",
            "- 비긴 조합: " + ", ".join(f"{label(combo)}({total})" for combo, total in picked["tied"])]
    if not picked["steps"]:
        out.append("- 비긴 조합이 하나뿐이어서 고르는 순서를 쓰지 않았다.")
    for step in picked["steps"]:
        out.append(f"- {step['name']}: " + ", ".join(f"{label(combo)}={value}" for combo, value in step["values"]))
        out.append("  - 남은 조합: " + ", ".join(label(combo) for combo in step["remaining"]))
    out += [f"- **고른 조합: {label(picked['chosen'])}**", "",
            "## 청크 묶음", "",
            "토큰 길이는 청크 파일의 `tokens`(bge-m3 토크나이저)이고, 90%는 작은 순서로 세어 ceil(0.9 × 청크 수)번째 값이다. "
            "한도를 넘긴 청크는 가장 작은 단위(표 머리글 + 행 하나, 문장 하나, 정보 상자 줄 하나)가 크기 한도보다 커서 그대로 둔 것이다.", "",
            "| 청크 묶음 | 청크 수 | 길이 최소 | 중앙값 | 90% | 최대 | 한도 넘긴 청크 수 | 넘긴 청크 길이 최소 | 중앙값 | 최대 |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for name, s in stats.items():
        over = s["over"] or ("-", "-", "-")
        out.append(f"| {name} | {s['n']} | " + " | ".join(num(x) for x in s["tokens"]) + f" | {s['over_n']} | " + " | ".join(num(x) if x != "-" else x for x in over) + " |")
    out += ["", "한도를 넘긴 청크의 문서별 수:", ""]
    for name, s in stats.items():
        out.append(f"- {name}: " + (", ".join(f"{doc} {n}" for doc, n in s["per_doc"].items()) if s["per_doc"] else "없음"))
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description="조합 8개 × 질문 38개 검색 비교")
    parser.add_argument("--summary-only", action="store_true", help="검색을 다시 돌리지 않고 있는 results.jsonl에서 요약만 다시 만든다")
    args = parser.parse_args()
    started = time.time()
    if not args.summary_only:
        questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
        write_results(RESULTS, run_search(questions))
        print(f"\n결과 {RESULTS.relative_to(ROOT)} 씀\n")
    rows = read_results(RESULTS)
    text = build_summary(rows, read_chunk_stats(dict.fromkeys(r["chunk_set"] for r in rows)))
    SUMMARY.write_text(text, encoding="utf-8")
    print(text)
    print(f"요약 {SUMMARY.relative_to(ROOT)} 씀 ({time.time() - started:.1f}초)")


if __name__ == "__main__":
    main()
