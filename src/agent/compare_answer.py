"""답 쓰기 판끼리 견주어 요약 마크다운을 만드는 프로그램(이슈 #15): 판 1은 판 0과, 판 2는 판 1과 견준다.

  .venv/bin/python src/agent/compare_answer.py --base data/agent/plan_search/runs.jsonl --new data/agent/answer_cite/runs_v1.jsonl --out <요약 경로>
  .venv/bin/python src/agent/compare_answer.py --base data/agent/answer_cite/runs_v1.jsonl --new data/agent/answer_cite/runs_v2.jsonl --out <요약 경로>

규칙은 decisions/stage6.md의 2026-10-28 줄(차례로 붙여 따로 잰다 / ④를 잴 때의 기준 / 판 0 고르기 / 근거 칸의 공통 검사)에 있다.
숫자는 두 기록 파일과 data/minimal/questions.json에서만 계산한다. 표와 분자/분모, 목록만 쓰고 해석 글은 쓰지 않는다.
--base가 ⑧ 기록(data/agent/plan_search/runs.jsonl)이면 판 0을 run_answer.pick_base의 규칙으로 고르고, run_answer.py의 기록이면 그대로 쓴다.
질문·씨앗으로 짝지어 센다. 두 쪽이 190쌍으로 다 짝지어지지 않으면 ValueError로 멈춘다. 요약 파일이 이미 있으면 덮어쓰지 않고 멈춘다.
맞음은 기록의 correct를 쓰지 않고 저장된 answer 글을 scoring.grade로 다시 채점한 값이다(compare.py와 같은 방식).
공통 검사는 근거 칸이 있는 새 쪽만 센다(판 0 쪽에는 근거 칸이 없다).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402
import run_answer  # noqa: E402
from index import QUESTIONS  # noqa: E402
from scoring import grade  # noqa: E402

EXPECTED_PAIRS = 190
# 생각 과정에 쓴 숫자 계산: 숫자, (단위 따위로) 숫자·=·줄바꿈 없는 글 15자 이하, 셈 기호(× * ÷ + −), 숫자. 예: 3 × 4, 5.246 g/cm³ × 60, 9.841 − 9.32.
# / - x ·는 단위(g/cm³, J/(mol·K))와 이름(Tb-144)에 흔해 넣지 않는다(빼기는 − 기호만 센다). ⑧ 기록에서 질량 질문의 부피 숫자(60)를 쓴 82번과 같은 82번을 잡는다
CALCULATION = re.compile(r"\d[^\d\n=]{0,15}?[×*÷+−]\s*\d")


def cells_of(rows):
    """기록 줄을 (질문 ID, 씨앗)마다 {hit, answer, base_kind}로 바꾼다. 근거 칸이 있는 기록(source 칸이 있음)은 그대로,
    ⑧ 기록은 판 0(run_answer.pick_base)을 고른다. (질문 ID, 씨앗)이 겹치면 ValueError."""
    cells = {}
    for r in rows:
        key = (r["question_id"], r["seed"])
        if key in cells:
            raise ValueError(f"(질문 ID, 씨앗)이 겹친다: {key}")
        if "source" in r:
            cells[key] = {"hit": r["hit"], "hit_ranks": r["hit_ranks"], "answer": r["answer"], "base_kind": r["source"]["base_kind"]}
        else:
            search, answer, kind = run_answer.pick_base(r)
            cells[key] = {"hit": search["hit"], "hit_ranks": search["hit_ranks"], "answer": answer, "base_kind": kind}
    return cells


def pair_up(base, new, expected=None):
    """두 쪽의 (질문 ID, 씨앗)이 모두 expected쌍(기본 EXPECTED_PAIRS)이고 서로 같지 않으면 ValueError. 기록 순서대로 키 목록을 돌려준다."""
    expected = EXPECTED_PAIRS if expected is None else expected
    if len(base) != expected or len(new) != expected or set(base) != set(new):
        raise ValueError(f"짝이 맞지 않는다: base {len(base)}개, new {len(new)}개({expected}쌍이어야 한다), "
                         f"base에만 있음 {sorted(set(base) - set(new))}, new에만 있음 {sorted(set(new) - set(base))}")
    return list(base)


def side_counts(cells, keys, by_id):
    """한 쪽의 수: 근거를 찾음, 맞음(저장된 answer 글을 다시 채점), 근거를 찾고도 틀림, 답 언어 같음, 끊김, 생각 과정에 숫자 계산을 쓴 수."""
    correct = {key: grade(by_id[key[0]], cells[key]["answer"]["answer"])["correct"] for key in keys}
    return {"hit": sum(cells[key]["hit"] for key in keys), "correct": sum(correct.values()),
            "hit_wrong": sum(cells[key]["hit"] and not correct[key] for key in keys),
            "lang_ok": sum(bool(cells[key]["answer"]["lang_ok"]) for key in keys),
            "aborted": sum(bool(cells[key]["answer"]["aborted"]) for key in keys),
            "calculation": sum(bool(CALCULATION.search(str(cells[key]["answer"]["reason"]))) for key in keys), "correct_by": correct}


def changes(base, new, keys, base_counts, new_counts):
    """(틀림 → 맞음 목록, 맞음 → 틀림 목록). 항목은 (질문 ID, 씨앗, base의 answer 글, new의 answer 글)."""
    def item(key):
        return (key[0], key[1], base[key]["answer"]["answer"], new[key]["answer"]["answer"])
    fixed = [item(k) for k in keys if not base_counts["correct_by"][k] and new_counts["correct_by"][k]]
    broken = [item(k) for k in keys if base_counts["correct_by"][k] and not new_counts["correct_by"][k]]
    return fixed, broken


def new_checks(new, keys):
    """새 쪽의 공통 검사 셈. 목록의 항목은 (질문 ID, 씨앗)이다. 꼴이 틀린 실행은 근거 칸을 읽지 못해 null인 검사는 세지 않는다."""
    def where(test):
        return [k for k in keys if test(new[k]["answer"])]
    wrong = [(k, new[k]["answer"]["checks"]["wrong_attached"]) for k in keys if new[k]["answer"]["checks"]["wrong_attached"]]
    hit_keys = [k for k in keys if new[k]["hit"]]
    return {"shape_errors": where(lambda a: not a["checks"]["shape_ok"]),
            "hit_cites": sum(new[k]["answer"]["checks"]["cites_evidence"] is True for k in hit_keys), "n_hit": len(hit_keys),
            "cites_false": where(lambda a: a["checks"]["cites_evidence"] is False),
            "wrong_attached_sum": sum(n for _, n in wrong), "wrong_attached": wrong,
            "no_number_facts": sum(new[k]["answer"]["checks"]["no_number_facts"] or 0 for k in keys),
            "facts_without_chunks": [(k, new[k]["answer"]["checks"]["facts_without_chunks"]) for k in keys
                                     if new[k]["answer"]["checks"].get("facts_without_chunks")],
            "citation_missing": where(lambda a: a["checks"]["citation_missing"]),
            "invalid_chunks": [(k, [c for item in new[k]["answer"]["cited"] for c in item["invalid_chunks"]]) for k in keys
                               if any(item["invalid_chunks"] for item in new[k]["answer"]["cited"] or [])]}


def name(key):
    return f"{key[0]} 씨앗{key[1]}"


def lines_of(keys):
    return ["- " + ", ".join(name(k) for k in keys) if keys else "- 없음"]


def change_lines(items):
    return [f"- {qid} 씨앗{seed}: base `{base_text}` / new `{new_text}`" for qid, seed, base_text, new_text in items] or ["- 없음"]


def render(base, new, base_path, new_path, by_id, expected=None):
    """요약 마크다운 글. 두 기록(cells_of의 결과)을 짝지어 센다."""
    keys = pair_up(base, new, expected)
    n = len(keys)
    b, w = side_counts(base, keys, by_id), side_counts(new, keys, by_id)
    fixed, broken = changes(base, new, keys, b, w)
    c = new_checks(new, keys)
    kinds = {kind: sum(base[k]["base_kind"] == kind for k in keys) for kind in ("first_plan", "final")}
    out = ["# 답 쓰기 판 견주기", "",
           f"- base: `{base_path}` (base_kind: 처음 계획 {kinds['first_plan']}줄, 최종 {kinds['final']}줄)", f"- new: `{new_path}`",
           f"- 짝지은 실행: {n}쌍", "",
           "## 두 쪽의 수", "", "| 항목 | base | new |", "| --- | --- | --- |",
           f"| 근거를 찾음 | {b['hit']}/{n} | {w['hit']}/{n} |", f"| 맞음 | {b['correct']}/{n} | {w['correct']}/{n} |",
           f"| 근거를 찾고도 틀림 | {b['hit_wrong']}/{b['hit']} | {w['hit_wrong']}/{w['hit']} |",
           f"| 답 언어가 질문과 같음 | {b['lang_ok']}/{n} | {w['lang_ok']}/{n} |", f"| 끊김 | {b['aborted']}/{n} | {w['aborted']}/{n} |",
           f"| 생각 과정에 숫자 계산을 씀 | {b['calculation']}/{n} | {w['calculation']}/{n} |", "",
           f"## 틀림 → 맞음 ({len(fixed)}개)", "", *change_lines(fixed), "",
           f"## 맞음 → 틀림 ({len(broken)}개)", "", *change_lines(broken), "",
           "## new의 공통 검사", "",
           f"- 꼴 오류: {len(c['shape_errors'])}개", *lines_of(c["shape_errors"]),
           f"- 근거를 찾은 실행 가운데 근거 칸이 근거 청크를 가리킴: {c['hit_cites']}/{c['n_hit']}",
           f"- cites_evidence가 false인 실행: {len(c['cites_false'])}개", *lines_of(c["cites_false"]),
           f"- wrong_attached 합: {c['wrong_attached_sum']} ({len(c['wrong_attached'])}개 실행)",
           *([f"- {name(k)}: {count}" for k, count in c["wrong_attached"]] or ["- 없음"]),
           f"- no_number_facts 합: {c['no_number_facts']}",
           f"- facts_without_chunks(청크 번호가 빈 사실) 합: {sum(n for _, n in c['facts_without_chunks'])} ({len(c['facts_without_chunks'])}개 실행)",
           *([f"- {name(k)}: {count}" for k, count in c["facts_without_chunks"]] or ["- 없음"]),
           f"- citation_missing인 실행: {len(c['citation_missing'])}개", *lines_of(c["citation_missing"]),
           f"- 목록에 없는 청크 번호(invalid_chunks)가 있는 실행: {len(c['invalid_chunks'])}개",
           *([f"- {name(k)}: {numbers}" for k, numbers in c["invalid_chunks"]] or ["- 없음"]), ""]
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(description="답 쓰기 판끼리 견주어 요약 마크다운을 만든다")
    parser.add_argument("--base", type=Path, required=True, help="견줄 바탕 기록: ⑧ 기록(판 0을 규칙으로 고름) 또는 run_answer.py의 기록")
    parser.add_argument("--new", type=Path, required=True, help="새 판의 기록(run_answer.py의 기록)")
    parser.add_argument("--out", type=Path, required=True, help="요약 마크다운 경로. 이미 있으면 멈춘다")
    args = parser.parse_args(argv)
    generate.check_new(args.out)
    by_id = {q["id"]: q for q in json.loads(QUESTIONS.read_text(encoding="utf-8"))}
    text = render(cells_of(run_answer.read_jsonl(args.base)), cells_of(run_answer.read_jsonl(args.new)), args.base, args.new, by_id)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "x", encoding="utf-8") as f:
        f.write(text)
    print(f"요약을 씀: {args.out}")


if __name__ == "__main__":
    main()
