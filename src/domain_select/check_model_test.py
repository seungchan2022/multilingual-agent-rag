"""4 모델 시험의 질문 파일 검사(2026-10-20 "코퍼스 단위 검사의 규칙" 4, 2026-10-21 "4 모델 시험에는 정답이 숫자 하나인 값만").

Claude가 만든 질문(step4/<분야>/questions.json)이 시험에 쓰기 전에 아래를 지키는지 본다.
1 칸이 다 있고 모양이 맞다  2 번호가 판정 문서의 모델 시험 값과 같고 언어가 맞다
3 근거 문장이 원문에 글자 그대로 있다  4 시험 값(raw)이 근거 문장 안에 있다
5 value가 raw의 첫 수와 같다  6 질문에 정답 수가 드러나지 않는다
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STEP3 = ROOT / "research_notes/stage2_stem_select/step3"
STEP4 = ROOT / "research_notes/stage2_stem_select/step4"
FIELDS = ["exoplanets", "rare_earth"]
KIND = {"ko": "한국어 문서", "en": "영어 문서"}
STR_KEYS = ["id", "kind", "lang", "subject", "target", "question", "answer", "unit"]
NUM = re.compile(r"\d+(?:\.\d+)?")


def is_text(x):
    return isinstance(x, str) and x.strip() != ""


def first_number(raw):
    """raw에서 쉼표를 지우고 찾은 첫 수의 글자. 없으면 None."""
    m = NUM.search(raw.replace(",", ""))
    return m.group(0) if m else None


def check_item(q):
    """칸과 모양(검사 1). 문제 글의 목록."""
    p = []
    for k in ["id", "kind", "lang", "subject", "target", "question", "answer", "value", "unit", "evidence_quotes"]:
        if k not in q:
            p.append(f"칸 {k}이 없다")
    for k in STR_KEYS:
        if k in q and not is_text(q[k]):
            p.append(f"{k}가 빈 글이 아니어야 한다")
    if "lang" in q and q["lang"] not in KIND:
        p.append(f"lang이 ko/en이 아니다: {q['lang']!r}")
    elif "lang" in q and "kind" in q and q["kind"] != KIND[q["lang"]]:
        p.append(f"kind {q['kind']!r}가 lang {q['lang']}와 맞지 않다")
    if "value" in q and (isinstance(q["value"], bool) or not isinstance(q["value"], (int, float))):
        p.append(f"value가 수가 아니다: {q['value']!r}")
    if "evidence_quotes" in q:
        eq = q["evidence_quotes"]
        if not isinstance(eq, list) or not eq:
            p.append("evidence_quotes가 비지 않은 목록이 아니다")
        else:
            for i, e in enumerate(eq):
                if not isinstance(e, dict) or not is_text(e.get("doc")) or not is_text(e.get("quote")):
                    p.append(f"evidence_quotes[{i}]의 doc, quote가 빈 글이 아니어야 한다")
    return p


def check_field(questions, values, texts):
    """한 분야의 질문 목록 검사. 문제 글의 목록(비면 통과)."""
    problems = []
    by_no = {v["no"]: v for v in values}
    seen = set()
    for q in questions:
        qid = q.get("id") if isinstance(q, dict) else None
        tag = f"[{qid}] "
        if not isinstance(q, dict):
            problems.append("[?] 항목이 객체가 아니다")
            continue
        item = check_item(q)
        problems += [tag + x for x in item]
        if qid in seen:
            problems.append(tag + "id가 겹친다")
        seen.add(qid)
        v = by_no.get(qid)
        if v is None:
            continue  # 남는 id는 아래에서 알린다
        if q.get("lang") in KIND and q["lang"] != v["lang"]:
            problems.append(tag + f"lang {q['lang']}이 판정 문서의 언어 {v['lang']}와 다르다")
        quotes = []
        eq = q.get("evidence_quotes")
        if isinstance(eq, list):
            for e in eq:
                if isinstance(e, dict) and is_text(e.get("doc")) and is_text(e.get("quote")):
                    quotes.append(e["quote"])
                    text = texts.get((q.get("lang"), e["doc"]))
                    if text is None:
                        problems.append(tag + f"문서 ({q.get('lang')}, {e['doc']})가 코퍼스에 없다")
                    elif e["quote"] not in text:
                        problems.append(tag + f"근거 문장이 원문에 없다: {e['quote'][:40]}")
        raw = v["raw"]
        if quotes and not any(raw in s for s in quotes):
            problems.append(tag + f"시험 값 {raw!r}이 근거 문장에 없다")
        num = first_number(raw)
        if num is None:
            problems.append(tag + f"시험 값 {raw!r}에 수가 없다")
            continue
        val = q.get("value")
        if isinstance(val, (int, float)) and not isinstance(val, bool) and abs(val - float(num)) > 1e-9:
            problems.append(tag + f"value {val}가 {raw!r}의 첫 수 {num}와 다르다")
        if is_text(q.get("question")) and re.search(rf"(?<![\d.]){re.escape(num)}(?![\d.])", q["question"]):
            problems.append(tag + f"질문에 정답 수 {num}가 드러난다")
    qids = {q.get("id") for q in questions if isinstance(q, dict)}
    for no in sorted(set(by_no) - qids):
        problems.append(f"[{no}] 질문이 빠졌다")
    for no in sorted(x for x in qids - set(by_no) if x is not None):
        problems.append(f"[{no}] 판정 문서에 없는 번호다")
    return problems


def load_values(judge, field):
    mv = judge["model_values"][field]
    return [{"no": r["no"], "lang": lang, "raw": r["raw"]} for lang in ("ko", "en") for r in mv[lang]]


def load_texts(results, field):
    texts = {}
    for d in results["fields"][field]["docs"]:
        f = STEP3 / "md" / f"{field}_{d['lang']}_{d['revid']}.md"
        if f.exists():
            texts[(d["lang"], d["title"])] = f.read_text(encoding="utf-8")
    return texts


def main():
    judge = json.loads((STEP3 / "judge.json").read_text(encoding="utf-8"))
    results = json.loads((STEP3 / "results.json").read_text(encoding="utf-8"))
    bad = False
    for field in FIELDS:
        qf = STEP4 / field / "questions.json"
        if not qf.exists():
            print(f"{field}: 질문 파일이 없다 ({qf})")
            bad = True
            continue
        questions = json.loads(qf.read_text(encoding="utf-8"))
        problems = check_field(questions, load_values(judge, field), load_texts(results, field))
        if problems:
            bad = True
            print(f"{field}: 문제 {len(problems)}개")
            for p in problems:
                print("  " + p)
        else:
            print(f"{field}: 통과 (질문 {len(questions)}개)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
