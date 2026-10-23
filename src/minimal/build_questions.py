"""최소판 비교에 쓸 질문 파일을 만드는 프로그램. 한국어 질문 19개와 각각의 영어 번역 19개, 모두 38개를 만든다.

  .venv/bin/python src/minimal/build_questions.py

한국어 질문은 두 원본 파일(round2, step4)에서 글자 그대로 가져오고, 영어 질문과 답은 아래 SPEC에 적힌 번역을 쓴다.
근거 줄은 SPEC에 적힌 줄 번호로 코퍼스(data/corpus/markdown/)에서 줄 글자를 읽어 적는다.
줄 번호가 범위를 벗어나거나 그 줄에 기대한 글자가 없으면 예외를 던지고 멈춘다(SPEC을 고쳐서 맞추지 않는다).
결과는 data/minimal/questions.json에 쓴다. 두 번 돌리면 바이트까지 같다.
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"
OUT = ROOT / "data" / "minimal" / "questions.json"

SRC_A = "research_notes/stage2_stem_select/round2/rare_earth/questions.json"
SRC_B = "research_notes/stage2_stem_select/step4/rare_earth/questions.json"

# 원본 A에서 쓰는 id와 순서. re-03은 뺀다.
A_IDS = ["re-01", "re-02", "re-04", "re-05", "re-06", "re-07", "re-08", "re-09", "re-10"]

# 영어 질문 19개를 사용자가 DeepL로 되옮겨 확인했다(decisions/judgments.md 2026-10-22 "영어 질문 19개를 DeepL로" 줄).
# 영어 질문 글을 바꾸면 False로 되돌리고 다시 확인받는다.
EN_TRANSLATION_CHECKED = True

EN_QUESTION_A = ("What is the mass in kg of a rectangular cuboid of {name} that is 3 cm wide, 4 cm long, "
                 "and 5 cm high? (Use its density near room temperature.)")

# 원본 A 항목: id -> (영어 원소 이름, 근거 [(doc_id, 줄 번호, 그 줄에 있어야 하는 글자), ...])
SPEC_A = {
    "re-01": ("europium", [("wiki-en-europium", 19, "5.246"), ("wiki-en-europium", 80, "5.24")]),
    "re-02": ("lutetium", [("wiki-ko-lutetium", 19, "9.841"), ("wiki-en-lutetium", 19, "9.840"),
                           ("wiki-ko-ytterbium", 83, "9.841"), ("wiki-en-ytterbium", 92, "9.841")]),
    "re-04": ("yttrium", [("wiki-ko-yttrium", 19, "4.472")]),
    "re-05": ("thulium", [("wiki-ko-thulium", 19, "9.32"), ("wiki-en-thulium", 19, "9.320"),
                          ("wiki-ko-ytterbium", 83, "9.32"), ("wiki-en-ytterbium", 92, "9.32")]),
    "re-06": ("dysprosium", [("wiki-ko-dysprosium", 19, "8.540"), ("wiki-en-dysprosium", 19, "8.550")]),
    "re-07": ("praseodymium", [("wiki-en-praseodymium", 19, "6.773")]),
    "re-08": ("samarium", [("wiki-ko-samarium", 19, "7.52")]),
    "re-09": ("lanthanum", [("wiki-en-lanthanum", 19, "6.145")]),
    "re-10": ("erbium", [("wiki-ko-erbium", 19, "9.066")]),
}

# 원본 B 항목(원본 파일 순서대로): id -> (영어 질문, 영어 답, 영어 단위, 근거)
SPEC_B = {
    "R-ko-038": ("What is the excitation energy, in keV, of the terbium nuclear isomer ¹⁴²ᵐ²Tb (terbium-142m2)?",
                 "621.4 keV", "keV", [("wiki-ko-isotopes-of-terbium", 26, "621.4")]),
    "R-ko-125": ("What is the excitation energy, in keV, of the terbium nuclear isomer ¹⁴⁴ᵐ⁴Tb (terbium-144m4)?",
                 "544.5 keV", "keV", [("wiki-ko-isotopes-of-terbium", 36, "544.5")]),
    "R-ko-110": ("What is the half-life, in seconds, of the terbium nuclear isomer ¹⁴⁴ᵐ¹Tb (terbium-144m1)?",
                 "4.25 seconds", "s", [("wiki-ko-isotopes-of-terbium", 31, "4.25"),
                                       ("wiki-ko-isotopes-of-terbium", 32, "4.25"),
                                       ("wiki-ko-isotopes-of-terbium", 33, "4.25")]),
    "R-ko-090": ("What is the half-life, in minutes, of the neodymium isotope ¹³⁵Nd (neodymium-135)?",
                 "12.4 minutes", "min", [("wiki-ko-isotopes-of-neodymium", 32, "12.4")]),
    "R-ko-082": ("What is the half-life, in days, of the neodymium isotope ¹⁴⁷Nd (neodymium-147)?",
                 "10.98 days", "days", [("wiki-ko-isotopes-of-neodymium", 53, "10.98")]),
    "R-en-092": ("In clinical trials of boron neutron capture therapy (BNCT), what was the median survival time, "
                 "in months, of patients with recurrent gliomas treated at Japan's JRR4 reactor?",
                 "10.8 months", "months", [("wiki-en-neutron-capture-therapy", 146, "10.8")]),
    "R-en-131": ("In the trial by Yamamoto et al., in which patients with newly diagnosed glioblastoma received "
                 "boron neutron capture therapy (BNCT) at Japan's JRR-4 reactor followed by an additional X-ray boost, "
                 "what was the overall median survival time in months?",
                 "27.1 months", "months", [("wiki-en-neutron-capture-therapy", 129, "27.1"),
                                           ("wiki-en-neutron-capture-therapy", 146, "27.1")]),
    "R-en-138": ("In clinical trials of boron neutron capture therapy (BNCT), what was the median survival time, "
                 "in months, of glioma patients treated at the MIT Research Reactor (MITR) in the United States?",
                 "11.1 months", "months", [("wiki-en-neutron-capture-therapy", 144, "11.1")]),
    "R-en-193": ("In the trial in which Miyatake and Kawabata combined boron neutron capture therapy (BNCT) "
                 "with an additional X-ray boost for patients with newly diagnosed glioblastoma, "
                 "what was the median survival time in months?",
                 "23.5 months", "months", [("wiki-en-neutron-capture-therapy", 125, "23.5"),
                                           ("wiki-en-neutron-capture-therapy", 145, "23.5")]),
    "R-en-091": ("In the boron neutron capture therapy (BNCT) clinical trial carried out at Studsvik, Sweden, "
                 "what was the median survival time, in months, when re-examined using the complete survival data?",
                 "17.7 months", "months", [("wiki-en-neutron-capture-therapy", 147, "17.7"),
                                           ("wiki-en-neutron-capture-therapy", 159, "17.7")]),
}

BASIS_A = "코퍼스를 꾸릴 때 그 원소의 다른 언어 문서를 넣지 않음. 원문 대조는 하지 않음(원래 두 언어 위키백과에 다 있는 값)"
BASIS_B = ("도메인 고르기 3 세기에서 AI가 코퍼스의 반대 언어 문서와 원문 대조"
           "(research_notes/stage2_stem_select/step3/confirm.json)")


def load_corpus():
    """documents.yaml의 문서 언어와 문서별 줄 목록을 읽는다."""
    docs = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
    language = {d["doc_id"]: d["language"] for d in docs}
    lines = {}
    for doc_id in language:
        p = MARKDOWN / f"{doc_id}.md"
        if p.is_file():
            lines[doc_id] = p.read_text(encoding="utf-8").split("\n")
    return language, lines


def table_header_line(ls, n):
    """n번째 줄(1부터)이 표 행이면 그 표 덩어리의 첫 줄 번호를, 아니면 None을 돌려준다."""
    if not ls[n - 1].startswith("|"):
        return None
    while n > 1 and ls[n - 2].startswith("|"):
        n -= 1
    return n


def make_evidence(spec, language, lines):
    """SPEC의 근거 목록을 코퍼스에서 읽은 줄 글자와 함께 근거 항목 목록으로 만든다."""
    out = []
    for doc_id, line, expect in spec:
        if doc_id not in language:
            raise ValueError(f"documents.yaml에 없는 doc_id: {doc_id}")
        if doc_id not in lines:
            raise ValueError(f"마크다운 파일이 없음: {doc_id}")
        ls = lines[doc_id]
        if not 1 <= line <= len(ls):
            raise ValueError(f"{doc_id}: 줄 번호 {line}가 범위(1~{len(ls)})를 벗어남")
        text = ls[line - 1]
        if expect not in text:
            raise ValueError(f"{doc_id}:{line}: 기대한 글자 '{expect}'가 줄에 없음: {text!r}")
        # value_text: 그 줄에서 정답 값을 적은 글자. 검색 채점은 청크에 든 원문 줄 목록에 근거 줄이 있고 청크 글에 이 글자가 있어야 맞음으로 센다
        # (긴 문단을 문장 경계에서 나누면 같은 줄 번호의 조각이 여럿 생기기 때문, decisions/stage4.md 2026-10-23 Codex 1차 지적 2. 줄 목록은 2026-10-23 "원문 줄 번호 목록" 줄)
        out.append({"doc_id": doc_id, "language": language[doc_id], "line": line, "text": text,
                    "value_text": expect, "table_header_line": table_header_line(ls, line)})
    return out


def branch_of(evidence):
    """근거 문서 언어가 모두 ko면 한국어만, 모두 en이면 영어만, 섞이면 두 언어."""
    langs = {e["language"] for e in evidence}
    if langs == {"ko"}:
        return "한국어만"
    if langs == {"en"}:
        return "영어만"
    return "두 언어"


def build():
    language, lines = load_corpus()
    src_a = {q["id"]: q for q in json.loads((ROOT / SRC_A).read_text(encoding="utf-8"))}
    src_b = json.loads((ROOT / SRC_B).read_text(encoding="utf-8"))
    if [q["id"] for q in src_b] != list(SPEC_B):
        raise ValueError("원본 B의 id 순서가 SPEC_B와 다름")

    # (원본 파일, 원본 항목, 영어 질문, 영어 답, 한국어 단위, 영어 단위, 근거 SPEC, 한 언어만일 때 이유)
    items = []
    for sid in A_IDS:
        name, spec = SPEC_A[sid]
        q = src_a[sid]
        items.append((SRC_A, q, EN_QUESTION_A.format(name=name), q["answer"], "kg", "kg", spec, BASIS_A))
    for q in src_b:
        en_q, en_a, en_unit, spec = SPEC_B[q["id"]]
        items.append((SRC_B, q, en_q, en_a, q["unit"], en_unit, spec, BASIS_B))

    result = []
    for i, (src, q, en_q, en_a, ko_unit, en_unit, spec, basis) in enumerate(items, 1):
        evidence = make_evidence(spec, language, lines)
        branch = branch_of(evidence)
        common = {"source": {"file": src, "id": q["id"]}, "value": q["value"], "evidence": evidence,
                  "branch": branch, "one_language_basis": None if branch == "두 언어" else basis}
        ko_id, en_id = f"q{i:02d}-ko", f"q{i:02d}-en"
        result.append({"id": ko_id, "lang": "ko", "pair_id": en_id, "source": common["source"],
                       "question": q["question"], "answer": q["answer"], "value": common["value"],
                       "unit": ko_unit, "evidence": evidence, "branch": branch,
                       "one_language_basis": common["one_language_basis"], "translation_checked": None})
        result.append({"id": en_id, "lang": "en", "pair_id": ko_id, "source": common["source"],
                       "question": en_q, "answer": en_a, "value": common["value"],
                       "unit": en_unit, "evidence": evidence, "branch": branch,
                       "one_language_basis": common["one_language_basis"], "translation_checked": EN_TRANSLATION_CHECKED})
    return result


def main(out=OUT):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")
    print(f"{len(text)}바이트를 {out}에 썼다")


if __name__ == "__main__":
    main(*sys.argv[1:2])
