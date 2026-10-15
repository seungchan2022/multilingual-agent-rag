"""후보 묶음 YAML을 사람이 원문과 대조할 Markdown 카드 파일로 바꾸는 프로그램.

  uv run python src/questions/make_cards.py <후보 파일> <출력 .md>

영어를 읽지 못하는 사람이 후보를 원문과 견주기 어려워서, 후보마다 대조에 필요한 것(질문, 정답, 근거 구절, 원문 링크,
반대 언어 문서 확인 재료, 판정 칸)을 한 카드에 모은다. 후보 파일은 check_candidates.py를 통과한 것이다.
후보 파일은 check_candidates.py와 같은 규칙으로 읽는다: ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고, 없으면 파일 전체를 읽는다.
링크는 출력 파일이 있는 폴더에서 원문 파일까지의 상대 경로에 줄 번호(#L숫자)를 붙인 Markdown 링크다.
사용자가 채운 답을 잃지 않도록 출력 파일이 이미 있으면 덮어쓰지 않고 종료 코드 1로 끝낸다.
"""
import os, re, sys
from functools import cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"

_DOCS = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
DOC = {d["doc_id"]: d for d in _DOCS}
BOTH_CITY = "두 언어 문서를 다 넣는 도시"
USAGE = "사용법: uv run python src/questions/make_cards.py <후보 파일> <출력 .md>"
LANG_NAME = {"ko": "한국어", "en": "영어"}
NOT_FOUND = "(원문에서 찾지 못함)"

INTRO = (
    "이 파일은 후보마다 카드 하나로, 순서표(data/questions/final_set_guide.md)의 \"대조할 것\"을 따라 카드마다 칸을 채운다. "
    "확인한 칸은 [ ]를 [x]로 바꾼다. 하지 않은 칸은 그대로 둔다. 판정은 채택·수정·폐기 가운데 하나만 남긴다. "
    "애매한 것은 메모에 적는다. 근거 구절이 원문에 글자 그대로 있는지, 개수·형식, `opposite_check`(반대 언어 찾기 기록)가 원문과 맞는지는 후보 검사가 이미 봤다. "
    "카드의 이름표는 후보 YAML 칸 이름을 백틱으로 적고 괄호에 한국어 뜻을 붙인다(예: `passage`(근거 구절)). "
    "칸 뜻은 순서표(data/questions/final_set_guide.md)의 \"후보 YAML 칸의 뜻\"에 있다."
)
TYPE_KO = {"single_fact": "단일 사실", "table_numeric": "표·수치·조건", "multi_doc": "여러 문서 연결",
           "paraphrase": "표현 불일치", "no_answer": "답 없음"}


def type_label(t):
    return f"{t}({TYPE_KO[t]})" if t in TYPE_KO else str(t)


# ---------- 읽기 ----------

def read_block(path):
    """후보 파일에서 YAML 글자를 꺼낸다(check_candidates.py와 같은 규칙)."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    fences = [i for i, l in enumerate(lines) if l.lstrip().startswith("```")]
    if fences:
        end = fences[1] if len(fences) > 1 else len(lines)
        lines = lines[fences[0] + 1:end]
    return "\n".join(lines)


@cache
def doc_text(doc_id):
    return (MARKDOWN / f"{doc_id}.md").read_text(encoding="utf-8")


# ---------- 줄 번호 ----------

def is_separator(line):
    line = line.rstrip()
    return line.startswith("|") and "-" in line and re.fullmatch(r"[|\-: ]+", line) is not None


def normalize(passage):
    return passage[:-1] if passage.endswith("\n") else passage


def is_table_passage(passage):
    nonempty = [l for l in normalize(passage).split("\n") if l.strip()]
    return bool(nonempty) and all(l.startswith("|") for l in nonempty)


def line_of_text(doc_id, piece):
    """piece가 원문에서 처음 시작하는 줄 번호(1부터). 없으면 None."""
    text = doc_text(doc_id)
    n = text.find(piece)
    return None if n == -1 else text.count("\n", 0, n) + 1


def line_of_passage(doc_id, passage):
    """구절이 시작하는 줄 번호. 표 구절은 머리글 행의 줄 번호. 못 찾으면 None."""
    p = normalize(passage)
    if not is_table_passage(passage):
        return line_of_text(doc_id, p)
    L = [l.rstrip() for l in p.split("\n")]
    ls = [l.rstrip() for l in doc_text(doc_id).split("\n")]
    for i in range(len(ls) - 1):
        if ls[i] == L[0] and is_separator(ls[i + 1]):
            j = i
            while j < len(ls) and ls[j].startswith("|"):
                j += 1
            if all(l in set(ls[i:j]) for l in L[1:]):
                return i + 1
    return None


def link(out_dir, doc_id, line=None, found=True):
    """원문 파일로 가는 상대 경로 Markdown 링크. found가 False면 링크 대신 못 찾았다는 글."""
    if not found:
        return f"{doc_id}.md {NOT_FOUND}"
    rel = Path(os.path.relpath(MARKDOWN / f"{doc_id}.md", out_dir)).as_posix()
    if line is None:
        return f"[{doc_id}.md]({rel})"
    return f"[{doc_id}.md {line}줄]({rel}#L{line})"


def source_note(doc_id):
    """링크 뒤에 붙일 원문 안내. 읽히는 웹 페이지는 위키백과 문서뿐이라 그 주소만 보이고, 나머지는 보는 방법을 적는다."""
    if doc_id.startswith("wiki-"):
        return f"원문 주소: {DOC[doc_id]['url']}"
    if doc_id.startswith("portal-"):
        return "표 문서라 파일을 직접 본다"
    return "짧은 문서라 파일 내용을 그대로 번역기에 붙인다"


def quote(text, indent):
    """여러 줄 글을 줄마다 '> '를 붙여 들여 쓴다."""
    pad = " " * indent
    return "\n".join(f"{pad}> {l}" if l else f"{pad}>" for l in normalize(text).split("\n"))


# ---------- 카드 ----------

def passage_link(out_dir, doc_id, passage):
    line = line_of_passage(doc_id, passage)
    return link(out_dir, doc_id, line, line is not None)


def evidence_docs(c):
    """근거 문서 id들(처음 나온 순서, 중복 없음)."""
    out = []
    for f in c.get("required_facts") or []:
        for item in f.get("evidence") or []:
            d = item.get("doc_id")
            if d in DOC and d not in out:
                out.append(d)
    return out


def city_part(c):
    docs = evidence_docs(c)
    groups = {DOC[d]["city_group"] for d in docs}
    if BOTH_CITY in groups:
        short = "두 언어 도시"
    else:
        short = "한국어 도시" if c.get("evidence_language") == "ko" else "영어 도시"
    cities = list(dict.fromkeys(DOC[d]["city"] for d in docs))
    return f"{short}({', '.join(cities)})" if cities else short


def answered_card(c, out_dir):
    el = c["evidence_language"]
    opposite = "en" if el == "ko" else "ko"
    out = ["---", "", f"## {c['id']} · `type`(유형): {type_label(c['type'])} · 도시 묶음: {city_part(c)}", "",
           f"- `question`(질문): {c['question']}", f"- `answer`(정답): {c['answer']}", "", "### `required_facts`(꼭 필요한 사실)"]
    for i, f in enumerate(c["required_facts"], 1):
        out.append(f"- `fact`(사실) {i}: {f['fact']}")
        if not f.get("evidence"):
            out.append("  - `evidence`(근거): 없음 — 다른 사실에서 나오는 결론")
        for j, item in enumerate(f.get("evidence") or [], 1):
            out.append(f"  - `evidence`(근거) {j}")
            out.append(f"    - `doc_id`(문서): {passage_link(out_dir, item['doc_id'], item['passage'])} · `location`(위치): {item['location']}")
            out.append("    - `passage`(근거 구절):")
            out.append(quote(item["passage"], 6))
    out += ["", "### 반대 언어 문서 확인 재료"]
    cities = {DOC[d]["city"] for d in evidence_docs(c)}
    same_city = [d for d in _DOCS if d["city"] in cities and d["language"] == opposite]
    how = "(직접 읽는다)" if opposite == "ko" else "(통째로 번역해 읽는다)"
    if same_city:
        out.append(f"- 같은 도시의 반대 언어 문서{how}:")
        for d in same_city:
            out.append(f"  - {link(out_dir, d['doc_id'])} · {source_note(d['doc_id'])}")
    else:
        out.append(f"- 같은 도시의 반대 언어 문서{how}: 없음({LANG_NAME[el]} 도시)")
    checks = c.get("opposite_check") or []
    out.append("- `opposite_check`(반대 언어 찾기 기록):" + ("" if checks else " 없음"))
    for it in checks:
        hits = it.get("hits") or []
        out.append(f"  - `term`(찾을 말) `{it['term']}` → `hits`(걸린 곳) " + (f"{len(hits)}곳" if hits else "없음"))
        for h in hits:
            line = line_of_text(h["doc_id"], h["excerpt"])
            out.append(f"    - {link(out_dir, h['doc_id'], line, line is not None)} · {source_note(h['doc_id'])}")
            out.append("      - `excerpt`(걸린 구절):")
            out.append(quote(h["excerpt"], 8))
            out.append(f"      - `same_fact`·`why`(Gemini의 판단): 같은 사실 {'맞음' if h['same_fact'] else '아님'} — {h['why']}")
    read5 = "걸린 곳을 번역기로 읽었다" if opposite == "en" else "걸린 곳을 읽었다"
    if opposite == "en":
        item6 = "(빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다)"
        item7 = "볼 곳: 위 \"같은 도시의 반대 언어 문서\"마다: 위키백과 문서는 원문 주소를 크롬에서 열고 페이지를 한국어로 번역한 뒤 Cmd+F, 관광 소개 글은 파일 내용을 번역기에 붙인다 (없으면 해당 없음)"
    else:
        item6 = "(빠졌으면 폴더 찾기를 더 했다)"
        item7 = "볼 곳: 위 \"같은 도시의 반대 언어 문서\"의 링크를 열어 읽는다 (없으면 해당 없음)"
    read7 = "통째로 번역해 읽었다" if opposite == "en" else "통째로 읽었다"
    out += ["", "### 판정",
            "- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 위 `question`(질문), `answer`(정답), `passage`(근거 구절)",
            "- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 위 `passage`(근거 구절)",
            "- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 위 `doc_id`(문서) 링크를 Cmd+클릭해 열고 Cmd+F",
            f"- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(Cmd+Shift+F, 포함할 파일 `data/corpus/markdown/*-{el}-*`)",
            f"- [ ] 5. 반대 언어 문서: {read5} — " + ("볼 곳: 위 `hits`(걸린 곳)의 `excerpt`(걸린 구절)" if any(it.get("hits") for it in checks) else "해당 없음: 위 `term`(찾을 말)마다 `hits`(걸린 곳)이 없음"),
            f"- [ ] 6. 반대 언어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 {item6} — 볼 곳: 위 `term`(찾을 말), 폴더 찾기(포함할 파일 `data/corpus/markdown/*-{opposite}-*`)",
            f"- [ ] 7. 반대 언어 문서: 같은 도시의 반대 언어 문서를 {read7} — {item7}",
            "- [ ] 8. 꼭 필요한 사실이 빠짐없고 군더더기 없다 — 볼 곳: 위 `required_facts`(꼭 필요한 사실)의 `fact`(사실)들, `answer`(정답)",
            "- [ ] 9. 유형이 맞다 — 볼 곳: 제목의 `type`(유형), 위 `question`(질문), `passage`(근거 구절)"]
    out += verdict_lines("더 찾아본 말과 걸린 곳")
    return out


def verdict_lines(searched):
    return ["- 판정: 채택 / 수정 / 폐기", "- 이유:", f"- {searched}:", "- 메모(애매한 것, Claude에게 물을 것):"]


def no_answer_card(c, out_dir):
    out = ["---", "", f"## {c['id']} · `type`(유형): {type_label('no_answer')} · 질문 언어 {c['question_language']}", "",
           f"- `question`(질문): {c['question']}",
           f"- `expected_refusal`(기대하는 거절): {c['expected_refusal']}",
           f"- `no_answer_reason`(답이 없다고 본 까닭): {c['no_answer_reason']}", "", "### `rebuttal`(반박 구절)"]
    rebuttal = c.get("rebuttal") or []
    if not rebuttal:
        out.append("없음")
    for item in rebuttal:
        out.append(f"- `doc_id`(문서): {passage_link(out_dir, item['doc_id'], item['passage'])} · `location`(위치): {item['location']}")
        out.append("  - `passage`(근거 구절):")
        out.append(quote(item["passage"], 4))
    out += ["", "### 판정",
            "- [ ] 1. 문서 전체에서 한국어 표현과 영어 표현으로 찾아봐도 답이 없다 — 볼 곳: 폴더 찾기(포함할 파일 `data/corpus/markdown`)",
            "- [ ] 2. 문서를 보지 않고 일반 지식으로도 답할 수 없다",
            "- [ ] 3. 전제가 너무 뻔하게 틀리지 않았다"]
    out += verdict_lines("찾아본 말과 걸린 곳")
    return out


def build(data, batch_name, out_dir):
    lines = [f"# 대조 카드: {batch_name}", "", INTRO, ""]
    for c in data:
        card = no_answer_card(c, out_dir) if c.get("type") == "no_answer" else answered_card(c, out_dir)
        lines += card + [""]
    return "\n".join(lines)


def stringify_terms(data):
    """따옴표 없이 적은 숫자 term(예: 1969)을 글자로 바꾼다."""
    for c in data:
        for it in c.get("opposite_check") or []:
            if isinstance(it, dict) and isinstance(it.get("term"), (int, float)) and not isinstance(it["term"], bool):
                it["term"] = str(it["term"])


def main():
    if len(sys.argv) != 3:
        print(USAGE)
        return 1
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    if dest.exists():
        print(f"이미 있는 파일이라 덮어쓰지 않음: {dest} (채워 둔 답을 잃지 않도록. 다른 이름을 주거나 직접 지울 것)")
        return 1
    try:
        data = yaml.safe_load(read_block(src))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as err:
        print(f"후보 파일을 읽지 못함: {err}")
        return 1
    if not isinstance(data, list):
        print("후보 파일의 맨 위가 목록이 아님")
        return 1
    stringify_terms(data)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out_dir = dest.parent.resolve()
    dest.write_text(build(data, src.name, out_dir), encoding="utf-8")
    print(f"카드 {len(data)}개를 씀: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
