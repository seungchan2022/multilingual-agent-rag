# 세 가지 조건으로 문제집을 돌린다.
#   base    : 문서 없이 생성 모델만 (기준 점수)
#   refine  : base의 답에서 시작해 판정 모델이 보고 다시 쓰게 함 (플로우 PDF 1단계, 판정은 처음 답 포함 최대 3번)
#   context : 근거 글을 시스템 프롬프트에 넣고 생성 모델만 (맞는 글 넣어 보기)
# 모든 호출의 입력과 출력을 results/<조건>.jsonl에 남긴다.
import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
URL = "http://localhost:11434/api/chat"
GEN_MODEL = "qwen3:8b"
JUDGE_MODEL = "gemma3:4b"
GEN_TEMPERATURE = 0.6  # qwen3:8b 기본값. 0이면 씨앗을 바꿔도 같은 답이 나온다.
SEEDS = range(1, 11)
MAX_ROUNDS = 3  # 플로우 PDF 의사코드의 max_refine=3: 답 쓰기와 판정을 최대 3번

GEN_SYSTEM = (
    "너는 질문에 답하는 도우미다. 아래 JSON 형식으로만 답하라.\n"
    '{"reason": "답에 이르는 생각을 단계별로 적는다", "answer": "최종 답만 짧게 적는다"}'
)
CONTEXT_SYSTEM = GEN_SYSTEM + "\n\n아래 참고 글을 바탕으로 답하라.\n참고 글:\n{evidence}"
JUDGE_SYSTEM = (
    "너는 다른 모델이 쓴 답을 검사하는 판정자다. 정답은 주어지지 않는다.\n"
    "아래 기준으로 답의 풀이(reason)와 최종 답(answer)을 검사하라.\n"
    "1. 풀이의 각 단계가 질문과 앞 단계에서 이어지는가 (건너뛴 단계나 비약이 없는가)\n"
    "2. 풀이와 최종 답이 서로 맞는가\n"
    "3. 근거 없이 지어낸 사실이 없는가 (확실하지 않은 사실을 단정하지 않았는가)\n"
    "4. 질문이 묻는 것에, 질문이 요구한 형식으로 답했는가\n"
    "먼저 문제점을 적고, 그다음 통과 여부를 정하고, 통과가 아니면 구체적인 수정 지시를 적어라.\n"
    'JSON으로만 답하라: {"issues": ["문제점"], "pass": true 또는 false, "revision_instruction": "수정 지시"}'
)
REFINE_USER = (
    "질문: {question}\n\n"
    "너의 이전 답:\n{draft}\n\n"
    "판정자의 지적: {issues}\n"
    "수정 지시: {instruction}\n\n"
    "지적을 참고해 다시 풀어라. 지적이 맞으면 고치고, 틀렸다고 판단되면 풀이에 그 이유를 적고 원래 답을 유지해도 된다. "
    "같은 JSON 형식으로만 답하라."
)


def chat(model, system, user, temperature, seed, fmt_json=True):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "stream": False,
        # 길이 상한: format=json에서 끝없이 이어지는 출력이 한 번 나와(c-010 씨앗 7) 더했다.
        # 상한을 넣기 전에 끝난 답 96개의 가장 긴 것이 1164토큰이라 2048이면 정상 답은 잘리지 않는다.
        "options": {"temperature": temperature, "seed": seed,
                    "num_predict": 2048 if model == GEN_MODEL else 1024},
    }
    if model == GEN_MODEL:
        body["think"] = False
    if fmt_json:
        body["format"] = "json"
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    # Ollama가 가끔 HTTP 500을 돌려줘서(c-010 judgement 호출에서 두 번) 같은 요청을 다시 보낸다.
    # judgement는 temperature 0, generate는 seed가 같아서 다시 보내도 결과는 같다.
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                res = json.loads(r.read())
            break
        except urllib.error.HTTPError:
            if attempt == 2:
                raise
            time.sleep(3)
    text = res["message"]["content"]
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    return {"text": text, "parsed": parsed, "seconds": round(time.time() - t0, 2),
            "gen_tokens": res.get("eval_count")}


def norm(s):
    return re.sub(r"[\s,]", "", str(s))


def grade(q, answer):
    """돌리기 전에 정한 채점 규칙: 최종 답(answer 칸)에 정답의 핵심 값이 제자리에 있으면 맞음."""
    a = norm(answer)
    if "slots" in q:
        parts = re.split(r"[,/;\n]", str(answer))
        ok = {}
        for city, value in q["slots"].items():
            ok[city] = any(city in p and value in p for p in parts)
        return all(ok.values())
    for key in q["keys"]:
        if q.get("numeric"):
            if not re.search(rf"(?<!\d){key}(?!\d)", a):
                return False
        elif key not in a:
            return False
    return True


def numbers_of(answer):
    """최종 답에서 쉼표를 지우고 숫자를 모두 뽑는다."""
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", str(answer).replace(",", ""))]


def grade_record(q, answer):
    """채점 기록. value가 있는 문제는 답의 마지막 숫자가 정답값의 ±1% 안이면 맞음(사용자가 정한 규칙).
    value가 없는 문제는 기존 grade 규칙 그대로이고 기록에는 correct만 둔다."""
    if "value" not in q:
        return {"correct": grade(q, answer)}
    nums = numbers_of(answer)
    picked = nums[-1] if nums else None
    value = q["value"]
    correct = picked is not None and abs(picked - value) <= abs(value) * 0.01
    diff = round(abs(picked - value) / abs(value) * 100, 4) if picked is not None else None
    return {"answer_key": q["answer"], "value": value, "numbers": nums, "picked": picked,
            "diff_pct": diff, "multi": len(nums) >= 2, "correct": correct}


def evidence_of(q):
    """context 조건에 넣을 근거 글. 옛 문제는 evidence 문자열, 새 문제는 evidence_quotes를 줄로 잇는다."""
    if "evidence" in q:
        return q["evidence"]
    return "\n".join(f"[{e['doc']}] {e['quote']}" for e in q["evidence_quotes"])


def answer_of(parsed):
    if isinstance(parsed, dict):
        return parsed.get("answer", "")
    return ""


def load_questions(path, only=None):
    qs = json.loads(Path(path).read_text(encoding="utf-8"))
    return [q for q in qs if not only or q["id"] in only]


def write(path, row):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_base(qs, out, seeds):
    for q in qs:
        for s in seeds:
            g = chat(GEN_MODEL, GEN_SYSTEM, q["question"], GEN_TEMPERATURE, s)
            ans = answer_of(g["parsed"])
            rec = grade_record(q, ans)
            write(out, {"cond": "base", "id": q["id"], "kind": q["kind"], "seed": s, "gen": g,
                        "final_answer": ans, "correct": rec["correct"], "grade": rec})


def run_context(qs, out, seeds):
    for q in qs:
        system = CONTEXT_SYSTEM.replace("{evidence}", evidence_of(q))
        for s in seeds:
            g = chat(GEN_MODEL, system, q["question"], GEN_TEMPERATURE, s)
            ans = answer_of(g["parsed"])
            rec = grade_record(q, ans)
            write(out, {"cond": "context", "id": q["id"], "kind": q["kind"], "seed": s, "gen": g,
                        "final_answer": ans, "correct": rec["correct"], "grade": rec})


def run_refine(qs, out, base_rows, seeds, judge_system=JUDGE_SYSTEM):
    base = {(r["id"], r["seed"]): r for r in base_rows}
    for q in qs:
        for s in seeds:
            b = base[(q["id"], s)]
            draft = b["gen"]
            rounds = []
            for rnd in range(1, MAX_ROUNDS + 1):
                draft_text = draft["text"]
                try:
                    j = chat(JUDGE_MODEL, judge_system, f"질문: {q['question']}\n\n답:\n{draft_text}", 0, s)
                except urllib.error.HTTPError as err:
                    # 세 번 다시 보내도 서버 오류(c-010의 몇 seed)면 그 회차에서 멈추고, 지금의 답을 최종 답으로 둔다.
                    j = {"text": "", "parsed": None, "seconds": 0, "gen_tokens": 0, "error": f"HTTP {err.code}"}
                    rec = grade_record(q, answer_of(draft["parsed"]))
                    rounds.append({"round": rnd, "draft": draft, "draft_answer": answer_of(draft["parsed"]),
                                   "draft_correct": rec["correct"], "draft_grade": rec, "judge": j, "passed": False})
                    break
                jp = j["parsed"] if isinstance(j["parsed"], dict) else {}
                passed = jp.get("pass") is True
                rec = grade_record(q, answer_of(draft["parsed"]))
                rounds.append({"round": rnd, "draft": draft, "draft_answer": answer_of(draft["parsed"]),
                               "draft_correct": rec["correct"], "draft_grade": rec, "judge": j, "passed": passed})
                if passed or rnd == MAX_ROUNDS:
                    break
                user = REFINE_USER.format(question=q["question"], draft=draft_text,
                                          issues=json.dumps(jp.get("issues", []), ensure_ascii=False),
                                          instruction=jp.get("revision_instruction", ""))
                draft = chat(GEN_MODEL, GEN_SYSTEM, user, GEN_TEMPERATURE, s)
            final = rounds[-1]["draft_answer"]
            rec = grade_record(q, final)
            write(out, {"cond": "refine", "id": q["id"], "kind": q["kind"], "seed": s, "rounds": rounds,
                        "final_answer": final, "correct": rec["correct"], "grade": rec})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cond", choices=["base", "refine", "context"])
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--seeds", type=int, nargs="*")
    ap.add_argument("--questions", default=str(HERE / "questions.json"),
                    help="문제 파일 (기본: 이 폴더의 questions.json). 결과는 이 파일 폴더의 results/에 둔다")
    ap.add_argument("--out")
    ap.add_argument("--judge-system", help="refine의 판정 모델 시스템 프롬프트 파일 (기본: 코드의 JUDGE_SYSTEM)")
    ap.add_argument("--base", help="refine이 시작할 base 결과 파일 (기본: 문제 파일 폴더의 results/base.jsonl)")
    a = ap.parse_args()
    qs = load_questions(a.questions, a.only)
    seeds = a.seeds or list(SEEDS)
    results = Path(a.questions).parent / "results"
    out = Path(a.out) if a.out else results / f"{a.cond}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.cond == "base":
        run_base(qs, out, seeds)
    elif a.cond == "context":
        run_context(qs, out, seeds)
    else:
        base_path = Path(a.base) if a.base else results / "base.jsonl"
        base_rows = [json.loads(l) for l in base_path.read_text(encoding="utf-8").splitlines() if l.strip()]
        judge_system = Path(a.judge_system).read_text(encoding="utf-8") if a.judge_system else JUDGE_SYSTEM
        run_refine(qs, out, base_rows, seeds, judge_system)
    print("done", a.cond, file=sys.stderr)


if __name__ == "__main__":
    main()
