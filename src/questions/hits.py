"""찾기 기록(opposite_check, same_language_check)의 찾을 말이 문서에서 나오는 곳(걸린 곳)을 계산하는 곳.

웹 AI는 찾을 말만 적고, 걸린 곳은 이 파일이 찾는다. 후보 검사(check_candidates.py)와 대조 카드를 만드는 프로그램이 같은 계산을 쓰도록 한 곳에 둔다.
같은 폴더의 프로그램이 `from hits import ...`로 불러 쓴다(src/questions/ 안의 파일을 직접 실행하면 이 폴더가 import 경로에 잡힌다).
"""
import re
from functools import cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"

DOCS = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
DOC_LANG = {d["doc_id"]: d["language"] for d in DOCS}
# 찾기 기록 칸 이름 -> 근거 문서와 같은 언어 문서를 찾는 칸인가
FIELDS = {"opposite_check": False, "same_language_check": True}


@cache
def doc_text(doc_id):
    return (MARKDOWN / f"{doc_id}.md").read_text(encoding="utf-8")


def normalize(passage):
    """YAML 블록 글자가 붙이는 맨 끝 줄바꿈 하나를 뗀다."""
    return passage[:-1] if passage.endswith("\n") else passage


def is_table_passage(passage):
    nonempty = [l for l in normalize(passage).split("\n") if l.strip()]
    return bool(nonempty) and all(l.startswith("|") for l in nonempty)


def positions(text, piece):
    """piece가 text에서 시작하는 모든 위치(겹쳐도 센다)."""
    out, n = [], text.find(piece)
    while n != -1:
        out.append(n)
        n = text.find(piece, n + 1)
    return out


def evidence_spans(c):
    """이 후보의 근거 구절이 원문에서 덮는 (시작, 끝) 목록을 doc_id별로 모은다. 구절이 문서에 없으면 건너뛴다(그 실패는 따로 알린다).
    표 구절이 아닌 구절은 문서에서 그 글자가 나오는 모든 곳, 표 구절은 구절의 줄이 모두 문서에 있을 때 구절의 줄과 줄 끝 공백만 뺀 글자가 같은 문서의 모든 줄."""
    out = {}
    facts = c.get("required_facts")
    for f in facts if isinstance(facts, list) else []:
        ev = f.get("evidence") if isinstance(f, dict) else None
        for item in ev if isinstance(ev, list) else []:
            doc, ps = (item.get("doc_id"), item.get("passage")) if isinstance(item, dict) else (None, None)
            if not (isinstance(doc, str) and doc in DOC_LANG and isinstance(ps, str)):
                continue
            ps, text = normalize(ps), doc_text(doc)
            if is_table_passage(ps):
                rows = {l.rstrip() for l in ps.split("\n") if l.strip()}
                if not rows <= {l.rstrip() for l in text.split("\n")}:
                    continue
                at = 0
                for line in text.split("\n"):
                    if line.rstrip() in rows:
                        out.setdefault(doc, []).append((at, at + len(line.rstrip())))
                    at += len(line) + 1
            elif ps:
                out.setdefault(doc, []).extend((n, n + len(ps)) for n in positions(text, ps))
    return out


def record_docs(c, field):
    """field에서 찾는 문서들의 doc_id. opposite_check는 근거 문서와 언어가 다른 문서, same_language_check는 언어가 같은 문서(근거 문서 포함).
    c의 evidence_language가 ko나 en이 아니면 빈 목록."""
    el = c.get("evidence_language")
    if el not in ("ko", "en"):
        return []
    same = FIELDS[field]
    return [d for d, lang in DOC_LANG.items() if (lang == el) == same]


def term_hits(c, field, term):
    """term이 field에서 찾는 문서들에 나오는 곳마다 (doc_id, 시작, 끝). 대소문자를 가리지 않고, 문서 순서 다음 위치 순서로 돌려준다.
    same_language_check는 이 후보의 근거 구절 안에 통째로 들어가는 곳을 뺀다."""
    skip = evidence_spans(c) if FIELDS[field] else {}
    out = []
    for d in record_docs(c, field):
        for m in re.finditer(re.escape(term), doc_text(d), re.IGNORECASE):
            if any(a <= m.start() and m.end() <= b for a, b in skip.get(d, [])):
                continue
            out.append((d, m.start(), m.end()))
    return out
