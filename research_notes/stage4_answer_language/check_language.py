"""최소판 질문 38개를 Baseline 방식(문서 없이)으로 한 번씩 돌려, 답이 질문 언어로 나오는지 본다(이슈 #8 12번).

  .venv/bin/python research_notes/stage4_answer_language/check_language.py [v1|A|B|C]

기준은 돌리기 전에 정했다(decisions/stage4.md 2026-10-23 "답을 질문 언어로 하게 하는 방법" 줄):
38개 모두 질문 언어로 답하면 통과. 언어는 reason과 answer를 합친 글의 한글 음절 수와 로마자 수로 가른다.
후보(decisions/stage4.md 2026-10-23 "답 언어를 고칠 후보를 A → B → C 순서로" 줄):
  v1: 첫 확인의 한국어 지시문(계산 줄 없음). 결과는 results.jsonl, summary.json
  A : 영어 지시문 하나(계산 줄, 언어 줄 포함)
  B : 한국어 지시문(계산 줄 포함) 그대로, 질문 끝에 질문 언어의 한 문장을 붙임
  C : 질문 언어에 맞는 지시문(한국어판, 영어판)을 바꿔 끼움
v1이 아니면 결과는 results_<후보>.jsonl, summary_<후보>.json에 쓴다.
"""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
QUESTIONS = ROOT / "data" / "minimal" / "questions.json"
URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:8b"
OPTIONS = {"temperature": 0.7, "top_p": 0.8, "top_k": 20, "min_p": 0, "seed": 1, "num_predict": 2048}

# 도메인 고르기 실험의 generate 지시문(src/domain_select/run.py GEN_SYSTEM)에 언어 줄을 더했다.
SYSTEM = (
    "너는 질문에 답하는 도우미다. 아래 JSON 형식으로만 답하라.\n"
    '{"reason": "답에 이르는 생각을 단계별로 적는다", "answer": "최종 답만 짧게 적는다"}\n'
    "질문과 같은 언어로 답하라. 질문이 한국어면 reason과 answer를 한국어로, 영어면 영어로 쓴다."
)
CALC_KO = "계산이 필요하면 reason에 식을 쓰고, 단위를 바꾸는 단계(예: g → kg)를 따로 적은 뒤, 계산을 한 번 다시 확인하라."
# 13번에서 정한 계산 줄을 더한 한국어 지시문(B, C의 한국어판)
SYSTEM_KO = (
    "너는 질문에 답하는 도우미다. 아래 JSON 형식으로만 답하라.\n"
    '{"reason": "답에 이르는 생각을 단계별로 적는다", "answer": "최종 답만 짧게 적는다"}\n'
    + CALC_KO + "\n"
    "질문과 같은 언어로 답하라. 질문이 한국어면 reason과 answer를 한국어로, 영어면 영어로 쓴다."
)
# SYSTEM_KO를 영어로 옮긴 것(A, C의 영어판). 사용자가 DeepL로 되옮겨 확인한다.
SYSTEM_EN = (
    "You are an assistant that answers questions. Answer only in the JSON format below.\n"
    '{"reason": "Write the reasoning that leads to the answer, step by step", "answer": "Write only the final answer, briefly"}\n'
    "If a calculation is needed, write the formula in reason, write the unit conversion step (e.g., g → kg) separately, "
    "and then check the calculation once more.\n"
    "Answer in the same language as the question. If the question is in Korean, write reason and answer in Korean; "
    "if it is in English, write them in English."
)
SUFFIX_B = {"en": "\n\nAnswer in English.", "ko": "\n\n한국어로 답하라."}


def prompt_for(variant, q):
    """후보마다 (지시문, 질문 글)을 돌려준다."""
    if variant == "v1":
        return SYSTEM, q["question"]
    if variant == "A":
        return SYSTEM_EN, q["question"]
    if variant == "B":
        return SYSTEM_KO, q["question"] + SUFFIX_B[q["lang"]]
    if variant == "C":
        return (SYSTEM_EN if q["lang"] == "en" else SYSTEM_KO), q["question"]
    raise ValueError(variant)


def chat(system, user):
    body = {"model": MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "stream": False, "think": False, "format": "json", "options": OPTIONS}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        res = json.loads(r.read())
    return res["message"]["content"], round(time.time() - t0, 2), res.get("eval_count")


def language_of(text):
    """한글 음절이 로마자보다 같거나 많으면 ko, 적으면 en."""
    hangul = len(re.findall(r"[가-힣]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return ("ko" if hangul >= latin else "en"), hangul, latin


def main(variant="v1"):
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    suffix = "" if variant == "v1" else f"_{variant}"
    chat(*prompt_for(variant, questions[0])[:1], "안녕")  # 몸풀기 호출. 결과는 쓰지 않는다.
    rows = []
    with open(HERE / f"results{suffix}.jsonl", "w", encoding="utf-8") as out:
        for q in questions:
            system, user = prompt_for(variant, q)
            text, seconds, tokens = chat(system, user)
            try:
                parsed = json.loads(text)
                judged, hangul, latin = language_of(f'{parsed.get("reason", "")} {parsed.get("answer", "")}')
            except (json.JSONDecodeError, AttributeError):
                parsed, judged, hangul, latin = None, None, None, None
            row = {"id": q["id"], "lang": q["lang"], "variant": variant, "question": q["question"],
                   "system": system, "user": user,
                   "options": OPTIONS, "output": text, "parsed": parsed, "answer_lang": judged,
                   "hangul": hangul, "latin": latin, "ok": judged == q["lang"],
                   "seconds": seconds, "gen_tokens": tokens}
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            out.flush()
            rows.append(row)
            print(f'{q["id"]} {q["lang"]}→{judged} {"OK" if row["ok"] else "FAIL"} {seconds}s', flush=True)
    failed = [r["id"] for r in rows if not r["ok"]]
    summary = {"total": len(rows), "ok": len(rows) - len(failed), "failed": failed, "pass": not failed,
               "seconds_total": round(sum(r["seconds"] for r in rows), 1),
               "seconds_median": sorted(r["seconds"] for r in rows)[len(rows) // 2]}
    summary["variant"] = variant
    (HERE / f"summary{suffix}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    sys.exit(0 if summary["pass"] else 1)


if __name__ == "__main__":
    main(*sys.argv[1:2])
