"""1단계 고리의 실행 기록(run.py), 짝 질문 검색 기록(pair_search.py), 지금 시스템의 기록(runs_minimal.jsonl)을 견주어 요약을 만드는 프로그램(이슈 #14).

  .venv/bin/python src/agent/compare.py     # runs.jsonl + pair_search.jsonl + runs_minimal.jsonl + questions.json → summary.md

숫자는 세 기록 파일과 data/minimal/questions.json에서만 계산한다. 표와 분자/분모, 그리고 아래 규칙대로 나온 "다음 할 일" 줄만 쓰고 해석 글은 쓰지 않는다.
시계와 무작위를 쓰지 않으므로 같은 기록에서는 같은 요약이 나온다(요약은 기록에서 언제든 다시 만들 수 있어 이미 있어도 덮어쓴다).
규칙은 decisions/stage6.md의 2026-10-26 줄(재는 법의 첫째 / 남길 기준의 하나 / 남길 기준의 둘 / 답까지 돌린다 / 비교용이 넘기는 청크 수를 실행마다 맞춘다 /
다른 판 검색을 남길지와 번역을 고칠지는 한 표로 정한다 / 판정 순서 / 모델 답의 꼴 검사)에 있다.
기록이 온전한지 먼저 본다. 어긋나면 ValueError로 멈춘다: ① runs.jsonl이 190줄이고 (질문 ID, 씨앗) 짝이 빠짐없이 한 번씩이며 code_commit이 하나이고 code_dirty가 모두 false
② 꼴 오류 줄이 하나라도 있으면 그 줄들을 보이고 값을 내지 않는다 ③ pair_search.jsonl이 질문마다 한 줄 ④ 실행마다 합친 목록의 원래 질문 8개 chunk_id가
runs_minimal.jsonl의 같은 질문·씨앗의 retrieved와 같고 comparison_retrieved의 위 8개와도 같다(다르면 코드 고장이다).
맞음은 기록의 correct를 쓰지 않고 저장된 answer 글을 scoring.grade로 다시 채점한 값이다(compare_generation.py와 같은 방식).
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
from generate import RUNS as MINIMAL_RUNS, SEEDS  # noqa: E402
from index import QUESTIONS, ROOT  # noqa: E402
from scoring import grade  # noqa: E402

OUT_DIR = ROOT / "data" / "agent" / "plan_search"
RUNS = OUT_DIR / "runs.jsonl"
PAIR_SEARCH = OUT_DIR / "pair_search.jsonl"
SUMMARY = OUT_DIR / "summary.md"
MIN_REFINED = 10   # 다시 쓰기가 일어난 실행이 이 수 미만이면 "이 질문으로는 잴 수 없음"(질문 2개 × 씨앗 5개)
LINE = 11          # 이 수 이상 많으면 남기거나 번역을 고친다(10번 이하는 비김)


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def original_ids(search):
    """검색 기록의 합친 목록에서 원래 질문으로 가져온 청크의 chunk_id(순위 순)."""
    return [c["chunk_id"] for c in search["merged"] if c["source"] == "original"]


def check_runs(rows, questions, seeds=SEEDS):
    """runs.jsonl이 온전한지 본다: 줄 수, (질문 ID, 씨앗) 짝, code_commit 하나, code_dirty 모두 false. 어긋나면 ValueError."""
    expected = {(q["id"], seed) for q in questions for seed in seeds}
    if len(rows) != len(expected):
        raise ValueError(f"runs.jsonl이 {len(rows)}줄이다({len(expected)}줄이어야 한다)")
    pairs = Counter((r["question_id"], r["seed"]) for r in rows)
    missing, extra = sorted(expected - set(pairs)), sorted(set(pairs) - expected)
    repeated = sorted(key for key, n in pairs.items() if n > 1)
    if missing or extra or repeated:
        raise ValueError(f"runs.jsonl의 (질문 ID, 씨앗) 짝이 맞지 않는다: 빠짐 {missing}, 모르는 짝 {extra}, 겹침 {repeated}")
    commits = sorted({r["code_commit"] for r in rows})
    if len(commits) != 1:
        raise ValueError(f"runs.jsonl의 code_commit이 하나가 아니다: {commits}")
    dirty = sorted((r["question_id"], r["seed"]) for r in rows if r["code_dirty"])
    if dirty:
        raise ValueError(f"code_dirty가 true인 줄이 있다(커밋하지 않은 변경이 있는 채로 돌림): {dirty}")


def check_shape_errors(rows):
    """꼴 오류 줄이 하나라도 있으면 그 줄들(질문, 씨앗, 칸, 까닭)을 보이고 ValueError로 멈춘다. 값을 내지 않는다."""
    bad = [r for r in rows if r["shape_error"]]
    if bad:
        lines = [f'{r["question_id"]} 씨앗{r["seed"]} {r["shape_error"]["stage"]} {r["shape_error"]["index"]}번째: {"; ".join(r["shape_error"]["problems"])}'
                 for r in bad]
        raise ValueError(f"꼴 오류 줄이 {len(bad)}개 있어 값을 내지 않는다:\n" + "\n".join(lines))


def check_pair_rows(rows, questions):
    """pair_search.jsonl이 질문마다 한 줄인지 본다. 어긋나면 ValueError."""
    ids = Counter(r["question_id"] for r in rows)
    expected = {q["id"] for q in questions}
    if set(ids) != expected or any(n > 1 for n in ids.values()):
        raise ValueError(f"pair_search.jsonl이 질문마다 한 줄이 아니다: 빠짐 {sorted(expected - set(ids))}, "
                         f"모르는 질문 {sorted(set(ids) - expected)}, 겹침 {sorted(k for k, n in ids.items() if n > 1)}")


def check_original_eight(runs, pair_rows, minimal):
    """합친 목록의 원래 질문 8개가 지금 시스템의 retrieved와 같고 comparison_retrieved의 위 8개와도 같은지 본다.
    다르면 코드 고장으로 ValueError("코드 고장")."""
    minimal_by = {(r["question_id"], r["seed"]): [c["chunk_id"] for c in r["retrieved"]] for r in minimal}
    sources = [(f'{r["question_id"]} 씨앗{r["seed"]}', r["question_id"], r["seed"], r["search"], r["comparison_retrieved"]) for r in runs]
    sources += [(f'{r["question_id"]}(짝 질문 검색)', r["question_id"], seed, r["search"], r["comparison_retrieved"])
                for r in pair_rows for seed in sorted({s for _, s in minimal_by})]
    for name, qid, seed, search, comparison in sources:
        ours, theirs, top = original_ids(search), minimal_by[(qid, seed)], [c["chunk_id"] for c in comparison[:len(original_ids(search))]]
        if ours != theirs or ours != top:
            raise ValueError(f"코드 고장: {name}의 원래 질문 청크가 다르다. 합친 목록 {ours}, runs_minimal {theirs}, comparison_retrieved 위 {len(ours)}개 {top}")


def has_evidence(chunks):
    return any(c["evidence"] for c in chunks)


def per_run(runs, pair_rows, minimal, questions):
    """실행마다 세는 값. 비교용은 상대가 넘긴 청크 수 N만큼 comparison_retrieved의 위에서 잘라 근거가 하나라도 있으면 hit다."""
    by_id = {q["id"]: q for q in questions}
    pair_by = {r["question_id"]: r["search"] for r in pair_rows}
    minimal_by = {(r["question_id"], r["seed"]): r for r in minimal}
    cells = []
    for r in runs:
        q, comparison, refined = by_id[r["question_id"]], r["comparison_retrieved"], r["n_refinements"] > 0
        fixed, first, pair = r["search"], r["first_plan_search"] if refined else r["search"], pair_by[r["question_id"]]
        first_answer = r["first_plan_answer"] if refined else r["answer"]
        current = minimal_by[(r["question_id"], r["seed"])]
        cells.append({
            "question_id": r["question_id"], "seed": r["seed"], "refined": refined, "plan_passed": r["plan_passed"],
            "current_hit": current["hit"], "fixed_hit": fixed["hit"], "first_hit": first["hit"], "pair_hit": pair["hit"],
            "n_fixed": fixed["n_chunks"], "n_first": first["n_chunks"], "n_pair": pair["n_chunks"],
            "cmp_fixed": has_evidence(comparison[:fixed["n_chunks"]]), "cmp_first": has_evidence(comparison[:first["n_chunks"]]),
            "cmp_pair": has_evidence(comparison[:pair["n_chunks"]]),
            "improved": refined and not first["hit"] and fixed["hit"], "worsened": refined and first["hit"] and not fixed["hit"],
            "current_correct": grade(q, current["answer"])["correct"], "fixed_correct": grade(q, r["answer"]["answer"])["correct"],
            "first_correct": grade(q, first_answer["answer"])["correct"]})
    return cells


def totals(cells):
    """표에 쓰는 합. 모두 실행(cells) 가운데 센 수다."""
    t = {key: sum(c[key] for c in cells) for key in
         ("current_hit", "fixed_hit", "first_hit", "pair_hit", "cmp_fixed", "cmp_first", "cmp_pair", "refined", "improved", "worsened",
          "current_correct", "fixed_correct", "first_correct")}
    t["n"] = len(cells)
    t["plan_failed"] = sum(c["plan_passed"] is False for c in cells)
    t["current_hit_correct"] = sum(c["current_correct"] for c in cells if c["current_hit"])
    t["fixed_hit_correct"] = sum(c["fixed_correct"] for c in cells if c["fixed_hit"])
    t["first_hit_correct"] = sum(c["first_correct"] for c in cells if c["first_hit"])
    t["diff_fixed"], t["diff_first"], t["diff_pair"] = t["fixed_hit"] - t["cmp_fixed"], t["first_hit"] - t["cmp_first"], t["pair_hit"] - t["cmp_pair"]
    return t


def next_steps(t):
    """"다음 할 일" 줄 둘. 가.(계획 검사와 고치기)를 먼저 정하고, 그 계획의 새 시스템 값으로 나.(다른 판 검색)를 정한다."""
    if t["refined"] < MIN_REFINED:
        first_line, decided = "계획 검사와 고치기: 이 질문으로는 잴 수 없음(남겨 둠). 새 시스템은 고친 계획으로 센다", True
    elif t["improved"] > t["worsened"]:
        first_line, decided = "계획 검사와 고치기: 남김. 새 시스템은 고친 계획으로 센다", True
    else:
        first_line, decided = "계획 검사와 고치기: 원인 가르기 필요(판정·다시 쓰기 기록을 읽음)", False
    if not decided:
        return [first_line, "가.가 정해진 뒤. 가.에서 남기면(고친 계획으로 셈): " + other_versions(t, "fixed")
                + " / 가.에서 빼면(처음 계획으로 셈): " + other_versions(t, "first")]
    return [first_line, other_versions(t, "fixed")]


def other_versions(t, which):
    """나.(다른 판 검색) 줄. which는 새 시스템을 셀 계획("fixed" 고친 계획, "first" 처음 계획)이다."""
    diff, pair_diff, hit = t[f"diff_{which}"], t["diff_pair"], t[f"{which}_hit"]
    if diff >= LINE:
        line = "다른 판 검색 남김" + (f" (짝 질문으로 검색 {t['pair_hit']}이 새 시스템 {hit}보다 높아도 번역은 지금 고치지 않고 기록만)"
                                   if t["pair_hit"] > hit else "")
    elif pair_diff >= LINE:
        line = "번역이 문제: 계획 요청 글을 고쳐 다시 잼"
    else:
        line = "다른 판 검색 뺌"
    return f"{line} (새 시스템 − 비교용 = {diff}, 짝 질문으로 검색 − 비교용 = {pair_diff})"


def frac(a, b):
    return f"{a}/{b}"


def source_lines(runs, pair_rows, minimal):
    return [f"- 새 시스템: `data/agent/plan_search/runs.jsonl` {len(runs)}줄, code_commit `{runs[0]['code_commit']}`, "
            f"run_id " + ", ".join(f"`{run_id}`" for run_id in sorted({r["run_id"] for r in runs})) + f", langgraph {runs[0]['langgraph_version']}",
            f"- 짝 질문으로 검색: `data/agent/plan_search/pair_search.jsonl` {len(pair_rows)}줄, code_commit `{pair_rows[0]['code_commit']}`",
            f"- 지금 시스템: `data/minimal/generation/{MINIMAL_RUNS['minimal'].name}` {len(minimal)}줄, code_commit `{minimal[0]['code_commit']}`"]


def build_summary(runs, pair_rows, minimal, questions, seeds=SEEDS):
    """기록(check_runs 등을 통과한 것)과 질문 파일로 요약 글을 만든다. 시계·무작위는 쓰지 않는다."""
    cells = per_run(runs, pair_rows, minimal, questions)
    t = totals(cells)
    n, n_seeds = t["n"], len(seeds)
    out = ["# 1단계 고리 견주기 요약", "",
           "아래 수는 모두 실행 기록 세 파일과 `data/minimal/questions.json`에서 계산했다. 분모는 돌린 횟수(질문 × 씨앗)다.", "",
           "## 출처", ""] + source_lines(runs, pair_rows, minimal)
    out += ["", "## 센 방법", "",
            "- 근거를 찾음(hit): 가져온 청크 안에 정답의 근거 줄이 있었는지(`evidence`가 있는 청크가 하나라도 있는지)다.",
            "- 새 시스템(고친 계획): 실행의 `search.hit`. 새 시스템(처음 계획): 다시 쓰기가 있던 실행은 `first_plan_search.hit`, 없던 실행은 `search.hit`.",
            "- 비교용: 원래 질문으로 k = 16 검색한 `comparison_retrieved`를, 상대가 그 실행에서 넘긴 청크 수(`n_chunks`)만큼 위에서 잘라 근거가 하나라도 있으면 hit다. 상대마다 따로 센다.",
            f"- 짝 질문으로 검색: 질문마다의 결과(모델을 쓰지 않아 씨앗마다 같다)를 씨앗 {n_seeds}개에 똑같이 셈해 {n}번으로 센다.",
            "- 맞음: 저장된 answer 글을 `scoring.grade`로 다시 채점한 값이다. 처음 계획으로 셀 때의 답은 다시 쓰기가 있던 실행은 `first_plan_answer`, 없던 실행은 `answer`다.",
            "", f"## 근거를 찾은 수 ({n}번 가운데)", "", "| 센 것 | 근거를 찾은 수 |", "|---|---|",
            f"| 지금 시스템 (원래 질문 8개) | {frac(t['current_hit'], n)} |",
            f"| 새 시스템 (고친 계획) | {frac(t['fixed_hit'], n)} |",
            f"| 새 시스템 (처음 계획) | {frac(t['first_hit'], n)} |",
            f"| 짝 질문으로 검색 | {frac(t['pair_hit'], n)} |",
            f"| 비교용 (고친 계획이 넘긴 수에 맞춤) | {frac(t['cmp_fixed'], n)} |",
            f"| 비교용 (처음 계획이 넘긴 수에 맞춤) | {frac(t['cmp_first'], n)} |",
            f"| 비교용 (짝 질문으로 검색이 넘긴 수에 맞춤) | {frac(t['cmp_pair'], n)} |",
            "", "## 차이 (그 상대에 맞춘 비교용과의 차이)", "", "| 차이 | 값 |", "|---|---|",
            f"| 새 시스템(고친 계획) − 비교용 | {t['fixed_hit']} − {t['cmp_fixed']} = {t['diff_fixed']} |",
            f"| 새 시스템(처음 계획) − 비교용 | {t['first_hit']} − {t['cmp_first']} = {t['diff_first']} |",
            f"| 짝 질문으로 검색 − 비교용 | {t['pair_hit']} − {t['cmp_pair']} = {t['diff_pair']} |",
            "", "## 계획 검사와 고치기", "", "| 센 것 | 수 |", "|---|---|",
            f"| 다시 쓰기가 일어난 실행 | {frac(t['refined'], n)} |",
            f"| 나아짐 (처음 계획 hit 아님 → 고친 계획 hit) | {frac(t['improved'], t['refined'])} |",
            f"| 나빠짐 (처음 계획 hit → 고친 계획 hit 아님) | {frac(t['worsened'], t['refined'])} |",
            f"| 계획 검사 불통과 (`plan_passed` false) | {frac(t['plan_failed'], n)} |",
            "", "## 답", "", "| 센 것 | 지금 시스템 | 새 시스템 (고친 계획) | 새 시스템 (처음 계획) |", "|---|---|---|---|",
            f"| 맞은 답 | {frac(t['current_correct'], n)} | {frac(t['fixed_correct'], n)} | {frac(t['first_correct'], n)} |",
            f"| 근거를 찾은 실행 가운데 맞은 답 | {frac(t['current_hit_correct'], t['current_hit'])} | {frac(t['fixed_hit_correct'], t['fixed_hit'])} | "
            f"{frac(t['first_hit_correct'], t['first_hit'])} |"]

    distribution = {key: Counter(c[key] for c in cells) for key in ("n_fixed", "n_first", "n_pair")}
    out += ["", "## 넘긴 청크 수의 분포 (실행 수)", "", "| 넘긴 청크 수 | 고친 계획 | 처음 계획 | 짝 질문으로 검색 |", "|---|---|---|---|"]
    for k in sorted(set().union(*distribution.values())):
        out.append(f"| {k} | " + " | ".join(str(distribution[key][k]) for key in ("n_fixed", "n_first", "n_pair")) + " |")

    out += ["", f"## 질문마다 {n_seeds}번 가운데 근거를 찾은 수", "",
            "| 질문 ID | 지금 시스템 | 새 (고친) | 새 (처음) | 짝 질문으로 검색 | 비교용 (고친에 맞춤) | 비교용 (처음에 맞춤) | 비교용 (짝에 맞춤) |",
            "|---|---|---|---|---|---|---|---|"]
    for q in questions:
        mine = [c for c in cells if c["question_id"] == q["id"]]
        out.append(f"| {q['id']} | " + " | ".join(frac(sum(c[key] for c in mine), n_seeds) for key in
                                                   ("current_hit", "fixed_hit", "first_hit", "pair_hit", "cmp_fixed", "cmp_first", "cmp_pair")) + " |")
    out += ["", "## 다음 할 일", "",
            f"규칙은 `decisions/stage6.md`의 \"판정 순서\", \"남길 기준의 둘\", \"한 표로 정한다\" 줄이다. 다시 쓰기 {MIN_REFINED}번 미만이면 잴 수 없음, 차이 {LINE} 이상이면 많음이다.", ""]
    first_line, second_line = next_steps(t)
    out += [f"- 가. {first_line}", f"- 나. {second_line}"]
    return "\n".join(out) + "\n"


def main():
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    runs, pair_rows, minimal = read_jsonl(RUNS), read_jsonl(PAIR_SEARCH), read_jsonl(MINIMAL_RUNS["minimal"])
    check_runs(runs, questions)
    check_shape_errors(runs)
    check_pair_rows(pair_rows, questions)
    check_original_eight(runs, pair_rows, minimal)
    text = build_summary(runs, pair_rows, minimal, questions)
    SUMMARY.write_text(text, encoding="utf-8")
    print(text)
    print(f"요약 {SUMMARY.relative_to(ROOT)} 씀")


if __name__ == "__main__":
    main()
