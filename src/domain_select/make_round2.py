"""정식 질문(round2)을 짧은 시험 질문에서 만든다(이슈 #6).

  .venv/bin/python src/domain_select/make_round2.py

세 분야(rare_earth, exoplanets, moons)마다 research_notes/stage2_stem_select/round2/<분야>/에
questions.json, md/, docs.json을 쓴다. 짧은 시험 질문 하나마다 같은 대상으로 정식 질문 하나를 만들고,
재료 값은 짧은 시험의 value 하나뿐이다. round2/<분야>/results/가 이미 있으면 아무것도 쓰지 않고 멈춘다.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check_questions import evaluate

BASE = Path(__file__).resolve().parents[2] / "research_notes/stage2_stem_select"
FIELDS = ["rare_earth", "exoplanets", "moons"]

DENSITY_QUOTE = "한 물체의 평균 밀도는 그 전체 질량을 그 전체 부피로 나눈 것과 같다."
GRAM_QUOTE = "오늘날에는 SI 단위계의 기본 단위인 ‘킬로그램의 1/1000’"
DAY_QUOTE = "이렇게 하면 하루는 24시간, 즉 1,440 분, 86,400 초가 된다."

# 분야마다 다른 것: 질문 꼴, 덧붙일 근거 문서(문서 이름, 문서가 있는 폴더, 인용)
ORBIT_DOCS = [("날", "solar", DAY_QUOTE)]
EXTRA_DOCS = {
    "rare_earth": [("밀도", "chem", DENSITY_QUOTE), ("그램", "chem", GRAM_QUOTE)],
    "exoplanets": ORBIT_DOCS,
    "moons": ORBIT_DOCS,
}
ORBIT_QUESTION = {
    "exoplanets": "외계 행성 {t}{josa} 모항성 주위를 3바퀴 도는 데 걸리는 시간은 몇 시간인가?",
    "moons": "위성 {t}{josa} 모행성 주위를 3바퀴 도는 데 걸리는 시간은 몇 시간인가?",
}


def josa(name):
    """주어 뒤 조사. 받침 있는 한글은 이, 없으면 가. 영문 b, c는 비, 씨로 읽어 가."""
    ch = name[-1]
    if "가" <= ch <= "힣":
        return "이" if (ord(ch) - 0xAC00) % 28 else "가"
    if ch in "bc":
        return "가"
    raise ValueError(f"조사를 정할 수 없는 이름: {name}")


def fmt(x):
    """사람에게 보이는 숫자: 유효숫자 6자리, 끝의 0 없음."""
    return format(x, ".6g")


def make_question(field, sq):
    """짧은 시험 질문 하나로 정식 질문 하나를 만든다."""
    t, v = sq["target"], sq["value"]
    lit = repr(float(v))
    if field == "rare_earth":
        calc, unit_factor, unit = f"3 * 4 * 5 * {lit} / 1000", "1000", " kg"
        question = f"가로 3 cm, 세로 4 cm, 높이 5 cm인 {t} 직육면체의 질량은 몇 kg인가? (상온 근처의 밀도로 계산한다)"
        req, conv = [v, round(v * 1000, 10)], []
    else:
        calc, unit_factor, unit = f"{lit} * 3 * 24", "24", "시간"
        question = ORBIT_QUESTION[field].format(t=t, josa=josa(t))
        req, conv = [v, round(v * 24, 10)], [24]
    value = round(evaluate(calc)[0], 10)
    if field == "rare_earth":
        steps = ["부피를 구한다: 3 × 4 × 5 = 60 cm³",
                 f"질량 = 밀도 × 부피 = {fmt(v)} × 60 = {fmt(round(v * 60, 10))} g",
                 f"1 g은 1/1000 kg이므로 {fmt(round(v * 60, 10))} g ÷ 1000 = {fmt(value)} kg"]
    else:
        steps = [f"공전 주기는 {fmt(v)}일이다",
                 f"3바퀴 도는 데 걸리는 날 수: {fmt(v)} × 3 = {fmt(round(v * 3, 10))}일",
                 f"하루는 24시간이므로 {fmt(round(v * 3, 10))} × 24 = {fmt(value)}시간"]
    quotes = list(sq["evidence_quotes"]) + [{"doc": d, "quote": q} for d, _, q in EXTRA_DOCS[field]]
    return {"id": sq["id"], "kind": "값 + 계산", "subject": sq["subject"], "target": t,
            "unit_factor": unit_factor, "question": question, "answer": f"{fmt(value)}{unit}",
            "value": value, "calc": calc, "steps": steps, "evidence_quotes": quotes,
            "ingredient": v, "requirements": [req], "unit_conv": conv}


def stop_if_results(out_root):
    """results/가 이미 있는 분야가 있으면 아무것도 쓰기 전에 멈춘다."""
    for f in FIELDS:
        if (out_root / f / "results").exists():
            print(f"{out_root / f / 'results'}가 이미 있다. 결과에 덧붙지 않게 멈춘다", file=sys.stderr)
            sys.exit(1)


def write_field(field, base, out_root):
    shorts = json.loads((base / "short_test" / field / "questions.json").read_text(encoding="utf-8"))
    out = out_root / field
    (out / "md").mkdir(parents=True, exist_ok=True)
    qs = [make_question(field, sq) for sq in shorts]
    (out / "questions.json").write_text(json.dumps(qs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 근거 문서: (문서 이름, 그 문서가 있는 폴더)
    docs = {sq["evidence_quotes"][0]["doc"]: base / "short_test" / field for sq in shorts}
    docs.update({d: base / src for d, src, _ in EXTRA_DOCS[field]})
    meta = {}
    for d, folder in docs.items():
        shutil.copyfile(folder / "md" / f"{d}.md", out / "md" / f"{d}.md")
        meta[d] = json.loads((folder / "docs.json").read_text(encoding="utf-8"))[d]
    (out / "docs.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(qs)


def main(base=BASE):
    out_root = base / "round2"
    stop_if_results(out_root)
    for f in FIELDS:
        print(f"{f}: 질문 {write_field(f, base, out_root)}개")


if __name__ == "__main__":
    main()
