"""근거 칸이 있는 답 쓰기의 지시문 두 판, 틀(JSON 스키마), 요청 본문, 답 하나의 기록과 공통 검사(이슈 #15).

규칙은 decisions/stage6.md의 2026-10-28 줄(④ 답변 합성의 인용 꼴 / ④ 답 쓰기 지시문 두 판의 전문 / 근거 칸의 공통 검사 /
판 0 고르기와 근거 칸이 빈 것의 셈)에 있다.
지시문(CITE_V1, CITE_V2)은 결정 줄의 전문과 글자가 같다. 한 글자도 바꾸지 않는다(test_answer.py가 전문을 따로 적어 견준다).
최소판 지시문(generate.SYSTEM_EN, generate.CONTEXT_EN)은 바꾸지 않는다. 시스템 메시지는 그 판의 글 뒤에 CONTEXT_EN으로 참고 글을 붙인 것이다.
요청 본문은 generate.request_body에서 format만 schema(n)으로 바꾼 것이고, 보내기는 generate.send다. 이 파일은 모델을 부르지 않는다.
채점은 generate.graded가 answer 칸만 보고 한다(근거 칸은 채점에 들어가지 않는다). 거절인지는 코드가 정하지 않는다(answer 원문을 사람이 본다).
번호는 그 실행에서 넘긴 청크 목록의 순위(1부터)다. 코드가 번호를 chunk_id·doc_id·줄로 바꿔 기록하고, 사실의 숫자가 인용한 청크 글에 있는지 값으로 견준다.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
import generate  # noqa: E402
from scoring import numbers_of  # noqa: E402

CONTEXT_VERSION = "ctx-en-v1"

_HEAD = [
    "You are an assistant that answers questions. Answer only in the JSON format below.",
    '{"reason": "Write the reasoning that leads to the answer, step by step", "answer": "Write only the final answer, briefly", '
    '"citations": [{"fact": "A fact from the reference passages that you used", "chunks": [the number of the passage that contains it]}]}',
]
_TAIL = [
    "In citations, list every fact from the reference passages that you used for the answer, one item per fact, "
    "with the number of each passage that contains it. Do not write passage numbers in reason or answer.",
    "If the reference passages do not contain the facts needed to answer, write in answer that the question cannot be answered from the passages, "
    "and write [] for citations.",
    "Answer in the same language as the question. If the question is in Korean, write reason, answer, and fact in Korean; "
    "if it is in English, write them in English.",
]
_CALC_V1 = [
    "If a calculation is needed, write the formula in reason, write the unit conversion step (e.g., g → kg) separately, "
    "and then check the calculation once more.",
]
_CALC_V2 = [
    "If a calculation is needed, do it in reason with the actual numbers from the question and the passages, one step at a time (e.g., 2.5 × 4 = 10). "
    "Do not only describe the steps in words.",
    "Write the unit conversion (e.g., g → kg) as a step with numbers too, check the calculation once more, and write the final result of the calculation in answer.",
]
CITE_V1 = "\n".join(_HEAD + _CALC_V1 + _TAIL)
CITE_V2 = "\n".join(_HEAD + _CALC_V2 + _TAIL)
SYSTEMS = {"cite-en-v1": CITE_V1, "cite-en-v2": CITE_V2}


def prompt_version(version):
    return f"{version}+{CONTEXT_VERSION}"


def messages_of(version, question, found):
    """(시스템 메시지, 사용자 메시지). 시스템 메시지 = 그 판의 글 + 참고 글 줄, 사용자 메시지 = 질문 글."""
    return SYSTEMS[version] + generate.CONTEXT_EN.format(passages=generate.passages_of(found)), question["question"]


def schema(n):
    """답 꼴의 틀. 세 칸 모두 필수이고 chunks의 번호는 1부터 n(그 실행에서 넘긴 청크 수)까지만 쓸 수 있다."""
    citation = {"type": "object",
                "properties": {"fact": {"type": "string"}, "chunks": {"type": "array", "items": {"type": "integer", "enum": list(range(1, n + 1))}}},
                "required": ["fact", "chunks"]}
    return {"type": "object",
            "properties": {"reason": {"type": "string"}, "answer": {"type": "string"}, "citations": {"type": "array", "items": citation}},
            "required": ["reason", "answer", "citations"]}


def request_body(system_message, user_message, seed, n):
    """generate.request_body에서 format만 schema(n)으로 바꾼 요청 본문. 생성 설정은 그대로다."""
    body = generate.request_body(system_message, user_message, seed)
    body["format"] = schema(n)
    return body


def shape_ok_of(parsed):
    """JSON 객체이고 reason·answer 글과 citations 목록이 있으며, citations의 항목마다 fact 글과 chunks 정수 목록이 있으면 true."""
    if not isinstance(parsed, dict) or not all(isinstance(parsed.get(key), str) for key in ("reason", "answer")):
        return False
    citations = parsed.get("citations")
    return isinstance(citations, list) and all(
        isinstance(item, dict) and isinstance(item.get("fact"), str) and isinstance(item.get("chunks"), list)
        and all(isinstance(c, int) and not isinstance(c, bool) for c in item["chunks"]) for item in citations)


def cited_of(citations, found):
    """사실마다 {fact, chunks, mapped, invalid_chunks, numbers, checks}. 번호는 found(넘긴 청크 목록)의 순위다.
    mapped는 목록에 있는 번호의 rank·chunk_id·doc_id·line_start·line_end, invalid_chunks는 목록에 없는 번호다.
    checks는 mapped 청크마다 사실의 숫자 가운데 그 청크 글에 값이 없는 것(missing_numbers)이다."""
    cited = []
    for item in citations:
        mapped, checks, invalid = [], [], []
        numbers = numbers_of(item["fact"])
        for rank in item["chunks"]:
            if not 1 <= rank <= len(found):
                invalid.append(rank)
                continue
            chunk_id, _, doc_id, _, text, _, _, line_start, line_end = found[rank - 1]
            mapped.append({"rank": rank, "chunk_id": chunk_id, "doc_id": doc_id, "line_start": line_start, "line_end": line_end})
            in_chunk = {abs(x) for x in numbers_of(text)}   # 값의 크기로 견준다: numbers_of는 Tb-144의 -를 음수로 읽는다
            checks.append({"rank": rank, "missing_numbers": [x for x in numbers if abs(x) not in in_chunk]})
        cited.append({"fact": item["fact"], "chunks": item["chunks"], "mapped": mapped, "invalid_chunks": invalid, "numbers": numbers, "checks": checks})
    return cited


def checks_of(parsed, cited, hit_ranks, picked, aborted):
    """공통 검사(decisions/stage6.md 2026-10-28 "근거 칸의 공통 검사").
    shape_ok: 꼴이 맞음. 꼴이 틀리면 근거 칸을 읽을 수 없으므로 cites_evidence·wrong_attached·no_number_facts·facts_without_chunks·citation_missing은 null이다.
    cites_evidence: hit_ranks가 비어 있지 않을 때 근거 칸 전체의 청크 번호가 hit_ranks와 겹치면 true, 아니면 false. hit_ranks가 비면 null.
    wrong_attached: (사실, 인용한 청크) 쌍 가운데 사실에 숫자가 있고 그 숫자 하나라도 청크 글에 없는 쌍의 수.
    no_number_facts: 숫자가 없는 사실의 수. facts_without_chunks: 청크 번호가 빈 사실의 수(참고 글 밖의 지식, decisions/stage6.md 2026-10-28 "청크가 없는 사실" 줄).
    citation_missing: answer에서 숫자를 골랐는데 근거 칸이 빈 목록. aborted: 끊김."""
    ok = shape_ok_of(parsed)
    if not ok:
        return {"shape_ok": False, "cites_evidence": None, "wrong_attached": None, "no_number_facts": None, "facts_without_chunks": None,
                "citation_missing": None, "aborted": aborted}
    cited_ranks = {c for item in cited for c in item["chunks"]}
    return {"shape_ok": True,
            "cites_evidence": bool(cited_ranks & set(hit_ranks)) if hit_ranks else None,
            "wrong_attached": sum(bool(check["missing_numbers"]) for item in cited if item["numbers"] for check in item["checks"]),
            "no_number_facts": sum(not item["numbers"] for item in cited),
            "facts_without_chunks": sum(not item["chunks"] for item in cited),
            "citation_missing": picked is not None and not cited,
            "aborted": aborted}


def record_of(question, found, hit_ranks, system_message, user_message, fields):
    """답 하나의 기록. system_message, user_message, fields(graph.reply_fields의 칸: 글·시간·토큰·끊김·시간 셋), generate.graded의 채점 칸,
    citations(모델이 쓴 근거 칸 원본, 읽지 못하면 null), cited(꼴이 맞을 때 사실마다 번호를 문서로 바꾼 것, 아니면 null), checks(공통 검사)."""
    try:
        parsed = json.loads(fields["output"])
    except json.JSONDecodeError:
        parsed = None
    graded = generate.graded(question, fields["output"])
    ok = shape_ok_of(parsed)
    cited = cited_of(parsed["citations"], found) if ok else None
    return {"system_message": system_message, "user_message": user_message, **fields, **graded,
            "citations": parsed.get("citations") if isinstance(parsed, dict) else None, "cited": cited,
            "checks": checks_of(parsed, cited, hit_ranks, graded["picked"], fields["aborted"])}
