"""최소판 질문 38개를 Baseline 방식(문서 없이)으로 한 번씩 돌려, 답이 질문 언어로 나오는지 본다(이슈 #8 12번).

  .venv/bin/python research_notes/stage4_answer_language/check_language.py

기준은 돌리기 전에 정했다(decisions/stage4.md 2026-10-23 "답을 질문 언어로 하게 하는 방법" 줄):
38개 모두 질문 언어로 답하면 통과. 언어는 reason과 answer를 합친 글의 한글 음절 수와 로마자 수로 가른다.
모든 호출의 입력과 출력을 results.jsonl에 남기고, 요약을 summary.json에 쓴다.
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


def chat(user):
    body = {"model": MODEL, "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
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


def main():
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    chat("안녕")  # 몸풀기 호출. 결과는 쓰지 않는다.
    rows = []
    with open(HERE / "results.jsonl", "w", encoding="utf-8") as out:
        for q in questions:
            text, seconds, tokens = chat(q["question"])
            try:
                parsed = json.loads(text)
                judged, hangul, latin = language_of(f'{parsed.get("reason", "")} {parsed.get("answer", "")}')
            except (json.JSONDecodeError, AttributeError):
                parsed, judged, hangul, latin = None, None, None, None
            row = {"id": q["id"], "lang": q["lang"], "question": q["question"], "system": SYSTEM,
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
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    sys.exit(0 if summary["pass"] else 1)


if __name__ == "__main__":
    main()
