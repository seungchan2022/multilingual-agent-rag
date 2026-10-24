"""Baseline과 최소판의 실행 기록(generate.py가 남긴 두 파일)을 질문 파일과 함께 읽어 비교 요약을 만드는 프로그램.

  .venv/bin/python src/minimal/compare_generation.py     # runs_baseline.jsonl + runs_minimal.jsonl + questions.json → summary.md

숫자는 두 기록 파일과 data/minimal/questions.json에서만 계산한다. 표와 분자/분모만 쓰고 해석 글은 쓰지 않는다.
맞음은 기록의 correct를 쓰지 않고, 저장된 answer 글을 src/minimal/scoring.py의 규칙(숫자 바로 뒤 괄호 오차 표기를 숫자로 세지 않음)으로 다시 채점한 값을 쓴다.
기록 파일은 고치지 않는다. 원래 correct와 달라진 답은 요약에 모두 나열한다. 단위 확인(scoring.unit_check)은 맞음을 바꾸지 않고 따로 센다.
시계와 무작위를 쓰지 않으므로 같은 기록에서는 같은 요약이 나온다(요약은 기록에서 언제든 다시 만들 수 있어 이미 있어도 덮어쓴다).
기록이 온전한지 먼저 본다: 파일마다 줄 수가 질문 수 × 씨앗 수(190)이고, (질문 ID, 씨앗) 짝이 빠짐없이 한 번씩 있고, code_commit이 하나뿐이어야 한다. 어긋나면 ValueError로 멈춘다.
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare_retrieval import GROUPS, num  # noqa: E402
from generate import RUNS, SEEDS, SYSTEMS  # noqa: E402
from index import QUESTIONS, ROOT  # noqa: E402
from scoring import grade, unit_check  # noqa: E402

SUMMARY = ROOT / "data" / "minimal" / "generation" / "summary.md"
LABEL = {"baseline": "Baseline", "minimal": "최소판"}


def read_runs(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def check_runs(runs, questions, seeds=SEEDS):
    """시스템마다 기록이 온전한지 본다: 시스템 칸, 줄 수, (질문 ID, 씨앗) 짝, code_commit. 어긋나면 ValueError."""
    expected = {(q["id"], seed) for q in questions for seed in seeds}
    for system, rows in runs.items():
        if {r["system"] for r in rows} != {system}:
            raise ValueError(f"{system} 기록에 다른 시스템의 줄이 섞여 있다: {sorted({r['system'] for r in rows})}")
        if len(rows) != len(expected):
            raise ValueError(f"{system} 기록이 {len(rows)}줄이다({len(expected)}줄이어야 한다)")
        pairs = Counter((r["question_id"], r["seed"]) for r in rows)
        missing, extra = sorted(expected - set(pairs)), sorted(set(pairs) - expected)
        repeated = sorted(key for key, n in pairs.items() if n > 1)
        if missing or extra or repeated:
            raise ValueError(f"{system} 기록의 (질문 ID, 씨앗) 짝이 맞지 않는다: 빠짐 {missing}, 모르는 짝 {extra}, 겹침 {repeated}")
        commits = sorted({r["code_commit"] for r in rows})
        if len(commits) != 1:
            raise ValueError(f"{system} 기록의 code_commit이 하나가 아니다: {commits}")


def regrade(runs, questions):
    """저장된 answer 글을 새 규칙으로 다시 채점한 사본. 줄의 correct, numbers, picked는 새 값이고, 기록의 correct는 old_correct에 둔다.
    unit_check는 단위 확인('같음', '다름', '없음')이다. 원래 runs는 바꾸지 않는다."""
    by_id = {q["id"]: q for q in questions}
    out = {}
    for system, rows in runs.items():
        out[system] = []
        for r in rows:
            q = by_id[r["question_id"]]
            out[system].append({**r, "old_correct": r["correct"], **grade(q, r["answer"]), "unit_check": unit_check(q, r["answer"])})
    return out


def system_stats(rows):
    """시스템 하나의 전체 수치. 개수는 그대로 세고(분모는 줄 수), 시간·토큰은 중앙값이다(prompt_tokens는 null을 뺀다)."""
    tokens = [r["prompt_tokens"] for r in rows if r["prompt_tokens"] is not None]
    return {"n": len(rows), "correct": sum(r["correct"] for r in rows), "old_correct": sum(r["old_correct"] for r in rows),
            "multi": sum(len(r["numbers"]) >= 2 for r in rows),
            "unit_diff": sum(r["unit_check"] == "다름" for r in rows), "unit_none": sum(r["unit_check"] == "없음" for r in rows),
            "lang_ok": sum(r["lang_ok"] for r in rows),
            "not_parsed": sum(not r["parsed_ok"] for r in rows), "no_number": sum(r["picked"] is None for r in rows),
            "aborted": sum(r["aborted"] for r in rows), "gen_seconds": statistics.median(r["gen_seconds"] for r in rows),
            "prompt_tokens": statistics.median(tokens) if tokens else None, "prompt_tokens_n": len(tokens)}


def group_counts(rows, questions, seeds=SEEDS):
    """묶음마다 (맞은 답 수, 답 수). 묶음은 (질문 언어, 갈래) 여섯 개, 질문 언어만 둘, 갈래만 셋이다. 질문 언어·갈래는 질문 파일의 칸이다."""
    meta = {q["id"]: (q["lang"], q["branch"]) for q in questions}
    keys = list(GROUPS) + [(lang, None) for lang in ("ko", "en")] + [(None, branch) for branch in ("한국어만", "영어만", "두 언어")]
    out = {key: [0, 0] for key in keys}
    n_questions = Counter(meta.values())
    for key in keys:
        out[key][1] = sum(n for (lang, branch), n in n_questions.items() if key[0] in (None, lang) and key[1] in (None, branch)) * len(seeds)
    for r in rows:
        lang, branch = meta[r["question_id"]]
        for key in keys:
            if key[0] in (None, lang) and key[1] in (None, branch):
                out[key][0] += r["correct"]
    return {key: tuple(v) for key, v in out.items()}


def pair_counts(runs):
    """같은 질문·같은 씨앗의 짝마다 (Baseline 맞음, 최소판 맞음)을 세어 네 칸으로 나눈다."""
    base = {(r["question_id"], r["seed"]): r["correct"] for r in runs["baseline"]}
    mini = {(r["question_id"], r["seed"]): r["correct"] for r in runs["minimal"]}
    counts = Counter((base[key], mini[key]) for key in base)
    return {"both": counts[(True, True)], "baseline_only": counts[(True, False)], "minimal_only": counts[(False, True)],
            "neither": counts[(False, False)], "pairs": len(base)}


def question_retrieval(rows, questions):
    """최소판 기록에서 질문마다 (검색 ✔, hit_ranks). 검색은 질문마다 같으므로 씨앗마다 다르면 ValueError."""
    found = {}
    for r in rows:
        found.setdefault(r["question_id"], set()).add((r["hit"], tuple(r["hit_ranks"])))
    for qid, values in found.items():
        if len(values) != 1:
            raise ValueError(f"{qid}: 씨앗마다 검색 결과가 다르다: {sorted(values)}")
    return {q["id"]: next(iter(found[q["id"]])) for q in questions}


def hit_by_correct(rows):
    """최소판 답 하나마다 (검색 ✔, 답 맞음)을 센 2×2: {(hit, correct): 개수}."""
    counts = Counter((r["hit"], r["correct"]) for r in rows)
    return {(h, c): counts[(h, c)] for h in (True, False) for c in (True, False)}


def correct_per_question(rows, questions):
    """질문마다 씨앗들 가운데 맞은 답 수."""
    counts = Counter()
    for r in rows:
        counts[r["question_id"]] += r["correct"]
    return {q["id"]: counts[q["id"]] for q in questions}


def distribution(per_question, seeds=SEEDS):
    """맞은 수가 len(seeds), …, 0인 질문 수."""
    counts = Counter(per_question.values())
    return {k: counts[k] for k in range(len(seeds), -1, -1)}


def aborted_list(rows):
    """질문마다 끊긴 답의 씨앗."""
    out = {}
    for r in rows:
        if r["aborted"]:
            out.setdefault(r["question_id"], []).append(r["seed"])
    return out


def changed_answers(runs):
    """원래 기록의 correct와 새 규칙의 correct가 다른 줄(시스템 순서, 파일의 순서)."""
    return [r for system in SYSTEMS for r in runs[system] if r["old_correct"] != r["correct"]]


def multi_number_answers(runs):
    """새 규칙으로 꺼낸 숫자가 둘 이상인 줄(시스템 순서, 파일의 순서). 맞음·틀림은 바꾸지 않고 표시만 한다."""
    return [r for system in SYSTEMS for r in runs[system] if len(r["numbers"]) >= 2]


def unit_diff_answers(runs):
    """단위가 질문의 단위와 다른 줄(시스템 순서, 파일의 순서)."""
    return [r for system in SYSTEMS for r in runs[system] if r["unit_check"] == "다름"]


def table_text(text):
    """표 칸에 넣는 글: 줄바꿈은 빈칸으로, | 는 \\|로 바꾼다."""
    return " ".join(str(text).split()).replace("|", "\\|")


def source_lines(runs):
    out = []
    for system in SYSTEMS:
        rows = runs[system]
        out.append(f"- {LABEL[system]}: `data/minimal/generation/{RUNS[system].name}` {len(rows)}줄, code_commit `{rows[0]['code_commit']}`, "
                   f"run_id " + ", ".join(f"`{run_id}`" for run_id in sorted({r["run_id"] for r in rows})))
    return out


def build_summary(runs, questions, seeds=SEEDS):
    """두 시스템의 기록(check_runs를 통과한 것)과 질문 파일로 요약 글을 만든다. 시계·무작위는 쓰지 않는다.
    기록을 regrade로 다시 채점한 뒤 모든 표에 새 맞음을 쓴다."""
    n_seeds = len(seeds)
    units = {q["id"]: q["unit"] for q in questions}
    runs = regrade(runs, questions)
    head = " | ".join(LABEL[s] for s in SYSTEMS)
    stats = {s: system_stats(runs[s]) for s in SYSTEMS}
    groups = {s: group_counts(runs[s], questions, seeds) for s in SYSTEMS}
    pairs = pair_counts(runs)
    retrieval = question_retrieval(runs["minimal"], questions)
    per_question = {s: correct_per_question(runs[s], questions) for s in SYSTEMS}
    aborted = {s: aborted_list(runs[s]) for s in SYSTEMS}

    out = ["# 생성 비교 요약", "",
           "아래 수는 모두 실행 기록 두 파일과 `data/minimal/questions.json`에서 계산했다. 맞음은 아래 \"채점 규칙\"의 새 규칙으로 다시 채점한 값이다.", "",
           "## 출처", ""] + source_lines(runs)
    changed = changed_answers(runs)
    out += ["", "## 채점 규칙", "",
            "맞음은 기록에 저장된 `answer` 글에서 쉼표를 지우고 숫자를 모두 꺼내, 마지막 숫자가 정답 값의 ±1% 안이면 맞음이다. "
            "숫자 바로 뒤에 붙은 괄호 안 정수(오차 표기, 예: `621.4(11)`)는 숫자로 세지 않는다. 괄호 앞에 빈칸이 있으면(`621.4 (11)`) 센다. "
            "기록 파일의 `correct`는 고치지 않았고, 이 요약의 모든 맞음은 새 규칙으로 다시 채점한 값이다.", "",
            f"| 맞은 답 | {head} |", "|---|---|---|",
            "| 원래 기록의 `correct` 합 | " + " | ".join(f"{stats[s]['old_correct']}/{stats[s]['n']}" for s in SYSTEMS) + " |",
            "| 새 규칙의 합 | " + " | ".join(f"{stats[s]['correct']}/{stats[s]['n']}" for s in SYSTEMS) + " |", "",
            f"맞음·틀림이 바뀐 답: {len(changed)}/{sum(stats[s]['n'] for s in SYSTEMS)}개"]
    if changed:
        out += ["", "| 시스템 | 질문 ID | 씨앗 | answer | 원래 → 새 |", "|---|---|---|---|---|"]
        for r in changed:
            out.append(f"| {LABEL[r['system']]} | {r['question_id']} | {r['seed']} | {table_text(r['answer'])} | "
                       f"{'맞음' if r['old_correct'] else '틀림'} → {'맞음' if r['correct'] else '틀림'} |")
    out += ["", "## 시스템마다 전체", "", f"| 칸 | {head} |", "|---|---|---|"]
    rows_ = [("맞은 답", lambda s: f"{s['correct']}/{s['n']}"),
             ("답 언어가 질문 언어와 같은 답(`lang_ok`)", lambda s: f"{s['lang_ok']}/{s['n']}"),
             ("JSON이 읽히지 않은 답(`parsed_ok` false)", lambda s: f"{s['not_parsed']}/{s['n']}"),
             ("숫자를 못 꺼낸 답(`picked` null)", lambda s: f"{s['no_number']}/{s['n']}"),
             ("되풀이로 끊긴 답(`aborted`)", lambda s: f"{s['aborted']}/{s['n']}"),
             ("숫자가 둘 이상인 답", lambda s: f"{s['multi']}/{s['n']}"),
             ("단위 다름(`unit_check`)", lambda s: f"{s['unit_diff']}/{s['n']}"),
             ("단위 없음(`unit_check`)", lambda s: f"{s['unit_none']}/{s['n']}"),
             ("생성 시간 중앙값(초)", lambda s: f"{s['gen_seconds']:.2f}"),
             ("입력 토큰 중앙값(`prompt_tokens`, null 제외)",
              lambda s: f"{num(s['prompt_tokens'])} ({s['prompt_tokens_n']}/{s['n']}줄)" if s["prompt_tokens"] is not None else f"- (0/{s['n']}줄)")]
    for name, cell in rows_:
        out.append(f"| {name} | " + " | ".join(cell(stats[s]) for s in SYSTEMS) + " |")

    multi = multi_number_answers(runs)
    out += ["", "## 숫자가 둘 이상인 답", "",
            "새 규칙으로 answer에서 꺼낸 숫자가 둘 이상인 답이다. 마지막 숫자를 골랐고, 맞음·틀림은 바꾸지 않았다.",
            "" if multi else "없음"]
    if multi:
        out += ["| 시스템 | 질문 ID | 씨앗 | answer | 꺼낸 숫자들 | 고른 숫자 | 맞음 |", "|---|---|---|---|---|---|---|"]
        for r in multi:
            out.append(f"| {LABEL[r['system']]} | {r['question_id']} | {r['seed']} | {table_text(r['answer'])} | "
                       f"{', '.join(str(n) for n in r['numbers'])} | {r['picked']} | {'맞음' if r['correct'] else '틀림'} |")

    unit_diff = unit_diff_answers(runs)
    out += ["", "## 단위가 다른 답", "",
            "고른 숫자(마지막 숫자) 바로 뒤의 글자 덩어리가 질문의 단위와 다른 단위인 답이다. 맞음·틀림은 바꾸지 않았다.",
            "" if unit_diff else "없음"]
    if unit_diff:
        out += ["| 시스템 | 질문 ID | 씨앗 | answer | 질문 단위 |", "|---|---|---|---|---|"]
        for r in unit_diff:
            out.append(f"| {LABEL[r['system']]} | {r['question_id']} | {r['seed']} | {table_text(r['answer'])} | {units[r['question_id']]} |")

    out += ["", "## 질문 언어 × 근거 문서 갈래마다 맞은 답", "",
            f"분모는 그 묶음의 질문 수 × {n_seeds}(씨앗 수)다.", "",
            f"| 묶음 | 질문 수 | {head} |", "|---|---|---|---|"]
    for key in groups["baseline"]:
        lang, branch = key
        name = f"{lang}·{branch}" if lang and branch else (f"질문 언어 {lang}" if lang else f"갈래 {branch}")
        total = groups["baseline"][key][1]
        out.append(f"| {name} | {total // n_seeds} | " + " | ".join(f"{groups[s][key][0]}/{groups[s][key][1]}" for s in SYSTEMS) + " |")

    out += ["", "## 같은 질문·같은 씨앗 짝", "", f"Baseline 줄과 최소판 줄을 (질문 ID, 씨앗)으로 맞춘 짝 {pairs['pairs']}개다.", "",
            "| 칸 | 짝 수 |", "|---|---|"]
    for name, key in (("둘 다 맞음", "both"), ("Baseline만 맞음", "baseline_only"), ("최소판만 맞음", "minimal_only"), ("둘 다 틀림", "neither")):
        out.append(f"| {name} | {pairs[key]}/{pairs['pairs']} |")

    cells = hit_by_correct(runs["minimal"])
    n_answers = len(runs["minimal"])
    hit_questions = sum(hit for hit, _ in retrieval.values())
    out += ["", "## 최소판의 검색 ✔ × 답 맞음", "",
            "답 하나(질문 × 씨앗)마다 센다. 검색 ✔는 가져온 청크 가운데 근거 줄이 든 청크가 있는 경우(`hit`)다.", "",
            "| 검색 | 답 맞음 | 답 틀림 | 합 |", "|---|---|---|---|"]
    for hit, name in ((True, "✔"), (False, "✘")):
        out.append(f"| {name} | {cells[(hit, True)]} | {cells[(hit, False)]} | {cells[(hit, True)] + cells[(hit, False)]}/{n_answers} |")
    out += ["", f"검색은 질문마다 같으므로 질문 단위로는 검색 ✔인 질문이 {hit_questions}/{len(questions)}개다.",
            "", f"## 질문마다 {n_seeds}번 가운데 맞은 수의 분포", "", f"| 맞은 수 | {head} |", "|---|---|---|"]
    dist = {s: distribution(per_question[s], seeds) for s in SYSTEMS}
    for k in range(n_seeds, -1, -1):
        out.append(f"| {k}/{n_seeds} | " + " | ".join(f"{dist[s][k]}/{len(questions)}" for s in SYSTEMS) + " |")

    out += ["", "## 질문별", "",
            f"맞은 수는 씨앗 {n_seeds}번 가운데 맞은 답 수다. 검색 칸의 숫자는 근거 줄이 든 청크의 순위(`hit_ranks`)다.", "",
            f"| 질문 ID | 질문 언어 | 갈래 | Baseline | 최소판 | 검색 | 끊긴 답 |", "|---|---|---|---|---|---|---|"]
    for q in questions:
        hit, ranks = retrieval[q["id"]]
        search_cell = f"✔ {', '.join(str(r) for r in ranks)}" if hit else "✘"
        cut = [f"{LABEL[s]} 씨앗 {seed}" for s in SYSTEMS for seed in aborted[s].get(q["id"], [])]
        out.append(f"| {q['id']} | {q['lang']} | {q['branch']} | {per_question['baseline'][q['id']]}/{n_seeds} | "
                   f"{per_question['minimal'][q['id']]}/{n_seeds} | {search_cell} | {', '.join(cut) if cut else '-'} |")
    return "\n".join(out) + "\n"


def main():
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    runs = {system: read_runs(RUNS[system]) for system in SYSTEMS}
    check_runs(runs, questions)
    text = build_summary(runs, questions)
    SUMMARY.write_text(text, encoding="utf-8")
    print(text)
    print(f"요약 {SUMMARY.relative_to(ROOT)} 씀")


if __name__ == "__main__":
    main()
