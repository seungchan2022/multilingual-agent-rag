"""후보 묶음 YAML을 사람이 원문과 대조할 Markdown 카드 파일로 바꾸는 프로그램.

  uv run python src/questions/make_cards.py <후보 파일> <출력 .md> [--memo <Gemini 답 전체 파일>] [--types <ChatGPT 답 파일>]

영어를 읽지 못하는 사람이 후보를 원문과 견주기 어려워서, 후보마다 대조에 필요한 것(질문, 정답, 근거 구절, 원문 링크,
반대 언어 문서 확인 재료, 판정 칸)을 한 카드에 모은다. 후보 파일은 check_candidates.py를 통과한 것이다.
후보 파일은 check_candidates.py와 같은 규칙으로 읽는다: ```로 시작하는 줄이 있으면 첫 번째와 다음 ``` 줄 사이만 읽고, 없으면 파일 전체를 읽는다.
링크는 출력 파일이 있는 폴더에서 원문 파일까지의 상대 경로에 줄 번호(#L숫자)를 붙인 Markdown 링크다.
사용자가 채운 답을 잃지 않도록 출력 파일이 이미 있으면 덮어쓰지 않고 종료 코드 1로 끝낸다.
표현 불일치(paraphrase) 카드의 칸 9에는 Gemini가 적은 바꾼 말(메모)을 접어서 붙인다. 메모는 후보 파일에 없고
Gemini의 답 전체를 저장한 파일에 있다: YAML 코드 블록이 끝난 뒤 `c-009: …` 꼴로 시작하는 줄(후보마다 한 줄, 줄 앞의 공백·`-`·`*`는 뗀다).
그 파일을 `--memo`로 준다. 묶음에 paraphrase 후보가 있는데 `--memo`가 없으면 사용법을 보이고 종료 코드 1로 끝낸다(출력 파일을 만들지 않음).
단일 사실(single_fact)과 표현 불일치 카드의 칸 9에는 확인용 AI(ChatGPT)의 짝 목록을 접어서 붙인다. 그 답 파일을 `--types`로 준다:
코드 블록이 있으면 모든 블록 안, 없으면 파일 전체에서 `## c-001` 줄마다 구역을 나누고, 구역 안에서 `- `로 시작하는 줄을 그대로 쓴다.
같은 id의 구역이 두 번 나오면 뒤의 것을 쓴다(재요청으로 받은 답을 원래 답 파일 끝에 붙여 저장하는 경우).
`--types`를 주면 카드를 쓰기 전에 답을 검사한다. 대상은 single_fact·paraphrase 후보 전부다(make_type_check.py가 넣는 범위):
그 후보의 구역이 없거나 줄이 없는 것, 줄이 `- "조각" → 짝 · 가름 · 핵심 낱말 예|아니오 · 까닭` 꼴이 아닌 것(가름은 같은 말·바꾼 말·이름·짝 없음·가르기 어려움,
짝이 `없음`이면 가름은 `짝 없음`이고 반대도 같다), 영어 조각·짝의 닫는 따옴표 뒤에 한글 뜻 괄호가 없는 것.
문제가 있으면 카드를 쓰지 않고 후보마다 문제를 보인 뒤, 같은 ChatGPT 채팅에 붙여 넣을 재요청 글을 보이고 종료 코드 1로 끝낸다.
single_fact·paraphrase 후보 가운데 질문 언어나 근거 언어가 영어인 것이 있는데 `--types`가 없으면 사용법을 보이고 종료 코드 1로 끝낸다(한국어 묶음은 선택).
"""
import os, re, sys, unicodedata
from pathlib import Path

import yaml
from hits import doc_text, is_table_passage, normalize, record_docs, term_hits

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
MARKDOWN = CORPUS / "markdown"

_DOCS = yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]
DOC = {d["doc_id"]: d for d in _DOCS}
BOTH_CITY = "두 언어 문서를 다 넣는 도시"
USAGE = "사용법: uv run python src/questions/make_cards.py <후보 파일> <출력 .md> [--memo <Gemini 답 전체 파일>] [--types <ChatGPT 답 파일>]  (묶음에 paraphrase 후보가 있으면 --memo 필수, single_fact·paraphrase 후보에 영어가 있으면 --types 필수)"
LANG_NAME = {"ko": "한국어", "en": "영어"}
NOT_FOUND = "(원문에서 찾지 못함)"
NO_MEMO = "Gemini가 적은 바꾼 말이 없다."
MEMO_RE = re.compile(r"^\s*[-*]?\s*(c-\d{3}):\s*(.*\S)\s*$")
TYPES_HEAD_RE = re.compile(r"^##\s*(c-\d{3})\s*$")
TYPES_TEMPLATE = "- 질문 조각 → 근거 구절의 짝 · 가름"
TYPES_KINDS = ("같은 말", "바꾼 말", "이름", "짝 없음", "가르기 어려움")
TYPES_KEY = ("핵심 낱말 예", "핵심 낱말 아니오")
REREQUEST = "아래 후보의 목록이 빠졌거나 지시문 4번 형식과 다르다. 이 후보들만 지시문 4번 형식대로 다시 써라. 코드 블록 하나에 넣는다: "
OLD_SHAPE = "찾기 기록이 예전 모양이다. 후보 검사(check_candidates.py)를 먼저 통과시킨다"
MEANING_Q = ("- 판단할 질문: ChatGPT 목록에서 \"가르기 어려움\"이나 \"짝 없음\"인 줄마다, 그 조각의 뜻이 문서에 있는가? "
             "(근거 구절 밖이어도 문서에 있으면 된다. 없으면 질문이 문서에 없는 전제를 깔고 있으므로 다른 줄과 관계없이 고치거나 버린다)")

INTRO = (
    "이 파일은 후보마다 카드 하나로, 순서표(data/questions/final_set_guide.md)의 \"대조할 것\"을 따라 카드마다 칸을 채운다. "
    "확인한 칸은 [ ]를 [x]로 바꾼다. 하지 않은 칸은 그대로 둔다. 판정은 채택·수정·폐기 가운데 하나만 남긴다. "
    "애매한 것은 메모에 적는다. 근거 구절이 원문에 글자 그대로 있는지, 개수·형식, 찾기 기록(`opposite_check`, `same_language_check`)의 찾을 말 개수와 언어는 후보 검사가 이미 봤다. 찾을 말이 문서에서 나오는 곳(걸린 곳)은 프로그램이 찾았다. "
    "카드의 이름표는 후보 YAML 칸 이름을 백틱으로 적고 괄호에 한국어 뜻을 붙인다(예: `passage`(근거 구절)). "
    "칸 뜻은 순서표(data/questions/final_set_guide.md)의 \"후보 YAML 칸의 뜻\"에 있다. "
    "카드마다 끝에 그 후보의 원본 YAML을 참고용으로 붙인다."
)
TYPE_KO = {"single_fact": "단일 사실", "table_numeric": "표·수치·조건", "multi_doc": "여러 문서 연결",
           "paraphrase": "표현 불일치", "no_answer": "답 없음"}



def topic(word):
    """한글 낱말 뒤에 붙일 '은'/'는'. 마지막 글자에 받침이 있으면 '은'."""
    ch = word[-1] if word else ""
    return "은" if "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 else "는"

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


# ---------- 줄 번호 ----------

def is_separator(line):
    line = line.rstrip()
    return line.startswith("|") and "-" in line and re.fullmatch(r"[|\-: ]+", line) is not None


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
        return f" · 원문 주소(앞뒤 문맥을 볼 때): {DOC[doc_id]['url']}"
    if doc_id.startswith("portal-"):
        return " · 표 문서라 링크를 열어 본다"
    return " · 짧은 문서라 링크를 열어 전체를 볼 수 있다"


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


NUM_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")
CARD_INTRO = (
    "이 카드만 보고 위에서부터 차례로 한다. 칸마다 \"할 일\"을 하고 \"판단할 질문\"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. "
    "문제가 있으면 `[ ]`로 두고 맨 아래 \"이유\"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 \"메모\"에 적는다."
)
TYPE_MEANING = {
    "single_fact": "단일 사실: 질문이 근거 구절의 핵심 낱말을 그대로 썼다(이름은 빼고 본다).",
    "paraphrase": "표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).",
    "table_numeric": "표·수치·조건: 답이 표에 있거나, 문서에 값이 여러 개라 조건(연도, 기준)에 맞는 것을 골라야 한다. 문장에 수치가 하나뿐이면 아니다.",
    "multi_doc": "여러 문서 연결: 둘 이상의 문서나 구절을 합쳐야 답이 나온다(비교, 집계, 여러 단계). 표의 값이나 수치를 비교하는 질문도 여기다.",
}


def numbers_of(c):
    """정답 글과 required_facts의 모든 fact 글에서 숫자(1,234 / 12.5 / 1969)를 정답, 사실 1, 사실 2 순서로, 중복 없이 뽑는다. 근거 구절(passage)에서는 뽑지 않는다."""
    texts = [str(c.get("answer"))]
    for f in c.get("required_facts") or []:
        texts.append(str(f.get("fact")))
    return list(dict.fromkeys(n for t in texts for n in NUM_RE.findall(t)))


def answer_value(answer):
    """정답 글에서 끝의 "이다", "입니다", "."를 떼고 앞뒤 공백을 없앤다."""
    a = str(answer).strip()
    prev = None
    while prev != a:
        prev = a
        for suf in ("입니다", "이다", "."):
            if a.endswith(suf):
                a = a[:-len(suf)].strip()
    return a


def item(n, title, body):
    return ["", f"#### {n}. {title}"] + body + ["- [ ] 확인함"]


def english_reading(fields, items, type_note):
    """영어로 적힌 칸이 있으면 번역기로 읽는 법 한 줄(없으면 빈 목록). fields는 영어인 칸 이름들."""
    if not fields:
        return []
    return ["", f"**영어 읽는 법** — 영어로 적힌 칸: {', '.join(fields)}. 하나씩 번역기에 붙여 한국어로 읽고, 옮긴 글로 칸 {items}을 판단한다. "
            "옮긴 글이 원문과 맞는지 두 가지를 본다: ① 숫자와 날짜가 원문과 같은가 ② 원문에 뜻을 뒤집거나 범위를 바꾸는 낱말"
            "(not, no, never, without, except, only, all, each, every, more, less, than, before, after, at least, at most)이 있으면 옮긴 글에도 그 뜻이 있는가. "
            "이 낱말들은 이 카드에서 `Cmd+F`로 찾는다." + type_note]


def verdict_block():
    return ["", "#### 적기",
            "- 판정(하나만 남긴다): 채택 / 수정 / 폐기",
            "- 이유(한 줄. 문제가 없으면 \"1~9 문제 없음\"):",
            "- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):"]


def details_block(c):
    dump = yaml.safe_dump(c, allow_unicode=True, sort_keys=False).rstrip("\n")
    return ["", "<details><summary>참고용 원본 YAML</summary>", "", "```yaml", dump, "```", "", "</details>"]


def source_hint(d, out_dir, opposite, terms_ref="3번의 찾을 말"):
    """같은 도시의 반대 언어 문서 하나를 어떻게 읽는지. terms_ref는 찾을 말이 어디에 적혀 있는지(3번 칸 안에서 쓰면 "위 찾을 말")."""
    did = d["doc_id"]
    if opposite == "ko":
        return f"{link(out_dir, did)}를 열어 {terms_ref}로 `Cmd+F` 하고 앞뒤를 읽는다."
    if did.startswith("wiki-"):
        return (f"크롬에서 {d['url']} 를 연다. 페이지에서 오른쪽 클릭 → \"한국어로 번역\". "
                f"`Cmd+F`로 {terms_ref}(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.")
    if did.startswith("portal-"):
        return f"{link(out_dir, did)}를 열어 표를 본다."
    return f"{link(out_dir, did)}를 열어 내용 전체를 번역기에 붙여 읽는다. 짧은 글이다."


def hit_snippet(doc_id, start, end):
    """걸린 곳이 있는 줄에서 걸린 글자 앞뒤 60글자까지를 보인다. 걸린 글자는 [ ]로 싸고, 줄 안에서 잘린 쪽에는 …를 붙인다."""
    text = doc_text(doc_id)
    ls = text.rfind("\n", 0, start) + 1
    le = text.find("\n", end)
    le = len(text) if le == -1 else le
    a, b = max(ls, start - 60), min(le, end + 60)
    return ("…" if a > ls else "") + text[a:start] + "[" + text[start:end] + "]" + text[end:b] + ("…" if b < le else "")


def hit_lines(out_dir, groups):
    """찾을 말마다 프로그램이 찾은 걸린 곳(링크, 그 줄의 앞뒤)을 줄로 만든다. groups는 걸린 곳이 있는 `(찾을 말, [(doc_id, 시작, 끝)])` 목록."""
    body = []
    for term, hits in groups:
        body.append(f"- `term`(찾을 말) `{term}`:")
        for k, (doc_id, start, end) in enumerate(hits, 1):
            line = doc_text(doc_id).count("\n", 0, start) + 1
            body += [f"  - 걸린 곳 {k}: {link(out_dir, doc_id, line)}{source_note(doc_id)}", quote(hit_snippet(doc_id, start, end), 4), ""]
    return body[:-1]


def terms_of(c, field):
    """찾기 기록 칸의 찾을 말들(글자). 칸이 없으면 빈 목록."""
    return [str(t) for t in c.get(field) or []]


def same_language_block(c, out_dir, docs, in_evidence, el):
    """같은 언어 문서에서 Gemini가 고른 찾을 말(`same_language_check`)을 프로그램이 찾은 걸린 곳 가운데 근거 문서 안(in_evidence=True) 또는 그 밖의 것을 보인다.
    후보에 그 칸이 없으면 빈 목록."""
    if c.get("same_language_check") is None:
        return []
    where = "근거 문서 안" if in_evidence else "근거 문서가 아닌 같은 언어 문서"
    own = LANG_NAME[el]
    reading = "번역기에 붙여 읽는다" if el == "en" else "읽는다"
    groups = [(t, [h for h in term_hits(c, "same_language_check", t) if (h[0] in docs) == in_evidence])
              for t in terms_of(c, "same_language_check")]
    with_hits = [g for g in groups if g[1]]
    none_terms = [f"`{t}`" for t, hits in groups if not hits]
    if not with_hits:
        names = ", ".join(none_terms) if none_terms else "없음"
        return [f"- Gemini가 고른 찾을 말 {names}: {where}에서는 프로그램이 찾은 걸린 곳이 없다. 위 직접 찾기는 그대로 해야 한다."]
    out = [f"- Gemini가 고른 찾을 말과, 프로그램이 {own} 문서에서 찾은 {where}의 걸린 곳 전부다. 위 직접 찾기는 그대로 해야 한다."
           + (f" 찾을 말 {', '.join(none_terms)}: {where}에서는 걸린 곳이 없다." if none_terms else "")]
    out += hit_lines(out_dir, with_hits)
    out += [f"- 할 일: 걸린 곳의 인용 글을 하나씩 {reading}.",
            "- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가?"]
    return out


def paraphrase_body(c, memos, types=None):
    return [
        "- 할 일: 이 후보의 유형은 paraphrase(표현 불일치)다. 질문을 뜻이 끊기는 조각으로 나눠, 아래 짝 목록에 조각마다 한 줄씩 "
        "`질문 조각 → 근거 구절의 짝 (같은 말 / 바꾼 말 / 이름)` 꼴로 적는다(예: `처음 생긴 → 창단된 (바꾼 말)`). 이름(고유명사)은 \"이름\"으로 적는다. "
        "줄이 모자라면 더한다. 목록을 다 채운 뒤 아래 접힌 칸을 펼쳐 Gemini가 적은 바꾼 말과 견준다.",
        f"- {TYPE_MEANING['paraphrase']}",
        "- 짝 목록:"] + ["  - "] * 4 + [
        "",
        "- 판단할 질문: \"바꾼 말\" 줄이 하나 이상 있는가?",
        "- 판단할 질문: 질문에 그대로 쓴 낱말(\"같은 말\" 줄)이 답을 드러내지 않는가? (예: \"특별자치시\". 드러내면 바꾼 말을 찾지 않아도 답이 나오므로 쓸 수 없다. \"이름\" 줄은 답을 가리키는 설명이라 빼고 본다)",
        "- 판단할 질문: 접힌 칸의 Gemini 짝 가운데 짝 목록과 다른 것이 없는가?",
        "",
        "<details><summary>Gemini가 적은 바꾼 말(짝 목록을 채운 뒤 펼친다)</summary>",
        "",
        memos.get(c["id"], NO_MEMO),
        "",
        "</details>",
        ""] + (types_block(c, types) + ["", MEANING_Q, "- 판단할 질문: ChatGPT 목록에서 \"핵심 낱말 예\"인 줄에 \"바꾼 말\"이 하나 이상 있는가?"] if types is not None else [])


def types_block(c, types):
    """칸 9에 붙일 ChatGPT 짝 목록 접힌 칸(`--types`를 줬을 때만 부른다)."""
    return ["<details><summary>ChatGPT(확인용 AI)의 짝 목록</summary>", "", *types.get(c["id"], []), "", "</details>"]


def answered_card(c, out_dir, memos, types=None):
    el = c["evidence_language"]
    opposite = "en" if el == "ko" else "ko"
    opp, own = LANG_NAME[opposite], LANG_NAME[el]
    tr = "번역기로 " if opposite == "en" else ""
    out = ["---", "", f"## {c['id']} · `type`(유형): {type_label(c['type'])} · 도시 갈래: {city_part(c)}", "", CARD_INTRO, "",
           "**후보**", f"- `question`(질문): {c['question']}", f"- `answer`(정답): {c['answer']}", "- `required_facts`(꼭 필요한 사실):"]
    passages = []
    for i, f in enumerate(c["required_facts"], 1):
        role = {True: " · 정답에 들어감(`in_answer: true`)", False: " · 답을 내는 데만 쓰임(`in_answer: false`)"}.get(f.get("in_answer"), "")
        out.append(f"  - `fact`(사실) {i}: {f['fact']}{role}" + ("" if f.get("evidence") else " (근거 없음 — 다른 사실들에서 나오는 결론이라 문서에 이 문장이 없다. 채점 때 답에 이 결론이 들어 있는지 본다)"))
        for j, ev in enumerate(f.get("evidence") or [], 1):
            passages += [f"  - 사실 {i}의 근거 {j}: {passage_link(out_dir, ev['doc_id'], ev['passage'])} · `location`(위치): {ev['location']}",
                         quote(ev["passage"], 4)]
    out += ["- `passage`(근거 구절):"] + (passages or ["  - 없음"])
    fields = (["`question`(질문)", "`answer`(정답)", "`fact`(사실)"] if c.get("question_language") == "en" else []) + (["`passage`(근거 구절)"] if el == "en" else [])
    out += english_reading(fields, "1~8", " 옮긴 글은 뜻을 보는 데만 쓴다. 칸 9의 유형(같은 말 / 바꾼 말)은 번역기로 정하지 않는다(`EVALUATION.md` ①).")

    out += item(1, "근거 구절만 읽고 정답이 나온다", [
        "- 할 일: 위 `passage`(근거 구절)를 읽는다.",
        "- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?",
        "- 판단할 질문: 질문이 깔고 있는 전제(개수, 날짜, 소속 등)가 문서와 맞는가? 예: 질문이 \"5개 자치구 중\"이면 근거 문서에 자치구가 5개인지 본다."])
    out += item(2, "정답이 하나로 정해진다", [
        "- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.",
        "- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?"])
    nums = numbers_of(c)
    val = answer_value(c["answer"])
    value_part = ("위 `answer`(정답)에서 값마다 골라 찾는다" if len(val) > 30 else f"`{val}`")
    docs = evidence_docs(c)
    doc_links = f" 근거 문서: {', '.join(link(out_dir, d) for d in docs)}." if len(docs) > 1 else ""
    if el == "en":
        read3 = [f"- 할 일 {n} ({d}): {source_hint(DOC[d], out_dir, 'en', terms_ref='위 찾을 말')}" for n, d in enumerate(docs, 1)]
        read3 = ["- 할 일: 근거 문서가 영어라 한국어 낱말로는 `Cmd+F`가 걸리지 않는다. 근거 문서마다 아래대로 한다. 근거 구절이 있는 곳에서는 앞뒤 한두 문장도 읽는다."] + read3
    else:
        read3 = ["- 할 일: 위 근거 문서 링크를 `Cmd+클릭`해 열고, `Cmd+F`로 찾을 말을 하나씩 찾아 걸린 곳을 `Enter`로 넘겨 본다. "
                 "근거 구절이 있는 줄에서는 앞뒤 한두 문장도 읽는다." + doc_links]
    out += item(3, "같은 문서 안에 다른 값이 없다", [
        "- 찾을 말: 질문에서 무엇에 대한 질문인지 나타내는 이름(예: 시조, 인구)을 하나 이상 골라 찾고, 아래 정답의 값도 찾는다. "
        f"정답의 값: {value_part} · 정답과 사실에서 뽑은 숫자: "
        + (", ".join(f"`{n}`" for n in nums) if nums else "없음"),
    ] + read3 + [
        "- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?"]
        + same_language_block(c, out_dir, docs, True, el))
    if el == "en":
        find4 = ("3번의 찾을 말(한국어 대상 낱말)을 번역기로 영어로 옮긴 말과 숫자로 찾는다. "
                 "걸린 줄은 번역기에 붙여 읽는다.")
    else:
        find4 = "3번의 찾을 말로 찾는다."
    out += item(4, f"같은 언어({own})의 다른 문서에 다른 값이 없다", [
        f"- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 \"포함할 파일\"에 `data/corpus/markdown/*-{el}-*`를 적는다. {find4}",
        "- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?"]
        + same_language_block(c, out_dir, docs, False, el))

    terms = terms_of(c, "opposite_check")
    groups = [(t, term_hits(c, "opposite_check", t)) for t in terms]
    with_hits = [g for g in groups if g[1]]
    none_terms = [f"`{t}`" for t, hits in groups if not hits]
    n_docs = len(record_docs(c, "opposite_check"))
    if with_hits:
        body = [f"Gemini가 고른 찾을 말과, 프로그램이 {opp} 문서 {n_docs}개에서 찾은 걸린 곳 전부다."
                + (f" 찾을 말 {', '.join(none_terms)}: 걸린 곳이 없다." if none_terms else "")]
        body += hit_lines(out_dir, with_hits)
        body += [f"- 할 일: 걸린 문장을 하나씩 {tr}읽는다." if opposite == "ko" else "- 할 일: 걸린 문장을 하나씩 번역기에 붙여 읽는다.",
                 "- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 다른 이야기인가(같은 사실을 말하지 않는가)?"]
    elif terms:
        body = [f"Gemini가 고른 찾을 말 {', '.join(none_terms)}: 프로그램이 {opp} 문서 {n_docs}개에서 찾았으나 걸린 곳이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다."]
    else:
        body = ["Gemini가 고른 찾을 말이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다."]
    out += item(5, f"{opp} 문서: 프로그램이 찾은 걸린 곳을 {tr}읽었다", body)

    out += item(6, f"{opp} 문서: 다른 말로도 찾아봤다", [
        "- Gemini가 고른 찾을 말: " + (", ".join(f"`{t}`" for t in terms) if terms else "없음"),
        "- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 " + opp + " 문서가 다른 말로 적었을 것 같으면, "
        + (f"번역기로 그 이름을 {opp}로 옮겨 나온 말이나 더 짧은 말로 폴더 찾기를 한다. " if opposite == "en" else "더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. ")
        + f"\"포함할 파일\"은 `data/corpus/markdown/*-{opposite}-*`. 걸린 곳이 있으면 그 줄을 {tr}읽는다.",
        f"- 판단할 질문: {opp} 문서 어디에도 같은 사실이 다른 표현으로 없는가?",
        "- 더 찾아본 말과 걸린 곳:"])

    cities = list(dict.fromkeys(DOC[d]["city"] for d in docs))
    same_city = [d for d in _DOCS if d["city"] in cities and d["language"] == opposite]
    if same_city:
        body = [f"- 할 일 {n} ({d['doc_id']}): {source_hint(d, out_dir, opposite)}" for n, d in enumerate(same_city, 1)]
        body.append(f"- 판단할 질문: 이 문서 어디에도 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 없는가?")
    else:
        body = [f"{', '.join(cities)}{topic(cities[-1]) if cities else '는'} {opp} 문서가 없는 도시라 통째로 읽을 문서가 없다. 이 칸은 `[x]`로 바꾼다."]
    out += item(7, f"{opp} 문서: 같은 도시({', '.join(cities)})의 {opp} 문서를 통째로 읽었다", body)

    out += item(8, "꼭 필요한 사실이 빠짐없고 군더더기 없다", [
        "- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.",
        "- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?",
        "- 판단할 질문: 질문이 묻는 사실만 \"정답에 들어감\"이고, 답을 내는 데만 쓰는 값(예: 합을 묻는 질문의 두 값)은 \"답을 내는 데만 쓰임\"인가? `answer`(정답)에 \"정답에 들어감\"인 사실이 모두 들어 있는가?"])
    if c["type"] == "paraphrase":
        return out + item(9, "유형이 맞다", paraphrase_body(c, memos, types)) + verdict_block() + details_block(c)
    out += item(9, "유형이 맞다", [
        f"- 할 일: 이 후보의 유형은 {type_label(c['type'])}다. 아래 뜻과 견준다.",
        f"- {TYPE_MEANING.get(c['type'], '')} 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.",
        "- 판단할 질문: 이 후보가 이 뜻에 맞는가?"]
        + (["", *types_block(c, types), "", MEANING_Q, "- 판단할 질문: ChatGPT 목록에서 \"핵심 낱말 예\"인 줄에 \"바꾼 말\"이 없는가? (있으면 단일 사실이 아니다)"]
           if types is not None and c["type"] == "single_fact" else []))
    return out + verdict_block() + details_block(c)


def no_answer_card(c, out_dir):
    out = ["---", "", f"## {c['id']} · `type`(유형): {type_label('no_answer')} · 질문 언어 {c['question_language']}", "", CARD_INTRO, "",
           "**후보**", f"- `question`(질문): {c['question']}",
           f"- `expected_refusal`(기대하는 거절): {c['expected_refusal']}",
           f"- `no_answer_reason`(답이 없다고 본 까닭): {c['no_answer_reason']}", "- `rebuttal`(반박 구절):"]
    rebuttal = c.get("rebuttal") or []
    if not rebuttal:
        out.append("  - 없음")
    for item_ in rebuttal:
        out.append(f"  - {passage_link(out_dir, item_['doc_id'], item_['passage'])} · `location`(위치): {item_['location']}")
        out.append(quote(item_["passage"], 4))
    fields = (["`question`(질문)", "`expected_refusal`(기대하는 거절)", "`no_answer_reason`(답이 없다고 본 까닭)"] if c.get("question_language") == "en" else []) \
        + (["`rebuttal`(반박 구절)"] if any(DOC[r["doc_id"]]["language"] == "en" for r in rebuttal if r.get("doc_id") in DOC) else [])
    out += english_reading(fields, "1~3", "")
    out += item(1, "문서 전체에서 한국어 표현과 영어 표현으로 찾아봐도 답이 없다", [
        "- 할 일: 질문의 이름과 숫자를 한국어와 영어(번역기)로 폴더 찾기를 한다. \"포함할 파일\"은 `data/corpus/markdown`.",
        "- 판단할 질문: 질문의 답이 되는 내용이 어디에도 없는가?",
        "- 찾아본 말과 걸린 곳:"])
    out += item(2, "문서를 보지 않고 일반 지식으로도 답할 수 없다", [
        "- 할 일: 문서를 열지 않고 `question`(질문)을 읽는다.",
        "- 판단할 질문: 세상에 실제로 답이 있는 질문은 아닌가?"])
    out += item(3, "전제가 너무 뻔하게 틀리지 않았다", [
        "- 할 일: `question`(질문)이 깔고 있는 전제를 찾는다.",
        "- 판단할 질문: 그 전제가 한눈에 틀렸다고 보이지 않는가?"])
    return out + verdict_block() + details_block(c)


def read_memos(path):
    """Gemini 답 전체 파일에서 YAML 코드 블록이 끝난 뒤의 `c-009: …` 줄들을 {id: 글}로 꺼낸다."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    fences = [i for i, l in enumerate(lines) if l.lstrip().startswith("```")]
    if fences:
        lines = lines[fences[1] + 1:] if len(fences) > 1 else []
    memos = {}
    for l in lines:
        m = MEMO_RE.match(l)
        if m:
            memos[m.group(1)] = m.group(2)
    return memos


def read_types(path):
    """ChatGPT 답 파일에서 `## c-001` 구역마다 `- `로 시작하는 줄들을 {id: [줄]}로 꺼낸다.
    코드 블록이 있으면 모든 블록 안만 읽고(재요청 답을 파일 끝에 붙여 저장해도 읽히게), 없으면 파일 전체를 읽는다.
    같은 id의 구역이 두 번 나오면 뒤의 것을 쓴다(다시 받은 답이 앞의 답을 대신한다)."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    if any(l.lstrip().startswith("```") for l in lines):
        inside, kept = False, []
        for l in lines:
            if l.lstrip().startswith("```"):
                inside = not inside
            elif inside:
                kept.append(l)
        lines = kept
    types, cur = {}, None
    for l in lines:
        m = TYPES_HEAD_RE.match(l)
        if m:
            cur = types[m.group(1)] = []
        elif cur is not None and l.startswith("- ") and not l.startswith(TYPES_TEMPLATE):
            cur.append(l.rstrip())
    return types


QUOTED = r'"[^"\n]*\S[^"\n]*"(?:\([^)]*\))?'
PIECE_RE = re.compile(f"^{QUOTED}$")
PAIR_RE = re.compile(rf"^{QUOTED}(?:,\s*{QUOTED})*$")


def piece_text(line):
    """줄의 질문 조각 글(따옴표 안). 조각 꼴이 아니면 None."""
    if " → " not in line:
        return None
    piece = line[2:].split(" → ", 1)[0].strip()
    return piece[1:piece.index('"', 1)] if PIECE_RE.match(piece) else None


def check_type_cover(question, lines):
    """조각 덮기 검사: 조각이 질문에 있는지, 조각이 덮지 못한 질문 글자가 있는지. 질문 내용은 내지 않는다."""
    covered, out = [False] * len(question), []
    low = question.lower()
    for n, line in enumerate(lines, 1):
        piece = piece_text(line)
        if not piece:
            continue
        start = low.find(piece.lower())
        if start < 0:
            out.append(f"{n}번째 줄: 조각이 질문에 없음")
            continue
        while start >= 0:
            covered[start:start + len(piece)] = [True] * len(piece)
            start = low.find(piece.lower(), start + 1)
    rest = sum(1 for ch, ok in zip(question, covered)
               if not ok and not ch.isspace() and unicodedata.category(ch)[0] not in "PZC")
    if rest:
        out.append(f"질문에서 조각으로 덮이지 않은 부분이 있음({rest}글자)")
    return out


def check_type_line(line, q_lang, e_lang):
    """답 한 줄의 문제를 글로 돌려준다(없으면 빈 목록). 줄의 내용은 화면에 내지 않는다."""
    if " → " not in line:
        return [" → 가 없음"]
    piece, rest = line[2:].split(" → ", 1)
    cells = rest.split(" · ")
    if len(cells) != 4:
        return [f"칸 수가 4가 아님({len(cells)}칸): 짝 · 가름 · 핵심 낱말 예/아니오 · 까닭"]
    pair, kind, key, reason = (x.strip() for x in cells)
    out = []
    if not PIECE_RE.match(piece.strip()):
        out.append("질문 조각이 큰따옴표로 감싼 비지 않은 글이 아님")
    if not (pair == "없음" or PAIR_RE.match(pair)):
        out.append("짝이 큰따옴표로 감싼 비지 않은 글(여러 개면 쉼표로 이음) 또는 `없음`이 아님")
    if kind not in TYPES_KINDS:
        out.append("가름이 다섯 값(같은 말 · 바꾼 말 · 이름 · 짝 없음 · 가르기 어려움) 가운데 하나가 아님")
    if key not in TYPES_KEY:
        out.append("셋째 칸이 `핵심 낱말 예` 또는 `핵심 낱말 아니오`가 아님")
    if not reason:
        out.append("까닭이 비었음")
    if (pair == "없음") != (kind == "짝 없음"):
        out.append("짝이 `없음`인 것과 가름이 `짝 없음`인 것이 서로 맞지 않음")
    for name, text, lang in (("질문 조각", piece, q_lang), ("짝", pair, e_lang)):
        if lang != "en":
            continue
        for m in re.finditer(r'"([^"]*)"', text):
            if re.search(r"[A-Za-z]", m.group(1)) and not re.match(r"\([^)]*[가-힣][^)]*\)", text[m.end():]):
                out.append(f"영어 {name}의 닫는 따옴표 바로 뒤에 한국어 뜻 괄호가 없음")
                break
    return out


def check_types(typed, types):
    """single_fact·paraphrase 후보마다 답의 문제를 {id: [글]}로 돌려준다. 문제 없는 후보는 넣지 않는다."""
    problems = {}
    for c in typed:
        lines = types.get(c["id"])
        if not lines:
            problems[c["id"]] = ["답에 이 후보의 구역이 없거나 줄이 하나도 없음"]
            continue
        found = [f"{n}번째 줄: {p}" for n, line in enumerate(lines, 1)
                 for p in check_type_line(line, c.get("question_language"), c.get("evidence_language"))]
        found += check_type_cover(c["question"], lines)
        if found:
            problems[c["id"]] = found
    return problems


def build(data, batch_name, out_dir, memos, types=None):
    lines = [f"# 대조 카드: {batch_name}", "", INTRO, ""]
    for c in data:
        card = no_answer_card(c, out_dir) if c.get("type") == "no_answer" else answered_card(c, out_dir, memos, types)
        lines += card + [""]
    return "\n".join(lines)


def stringify_terms(data):
    """찾을 말을 글자로 바꾼다: 따옴표 없이 적은 숫자(예: 1969)는 글자로, 옛 모양의 `{term, hits}` 항목은 term만 꺼낸다.
    `term`이 없는 사전처럼 글자로 바꿀 수 없는 항목이 있으면 ValueError."""
    for c in data:
        for field in ("opposite_check", "same_language_check"):
            if isinstance(c.get(field), list):
                terms = []
                for t in c[field]:
                    if isinstance(t, dict):
                        t = t.get("term")
                    if not isinstance(t, (str, int, float)) or isinstance(t, bool):
                        raise ValueError(OLD_SHAPE)
                    terms.append(str(t))
                c[field] = terms


def main():
    args, memo_path, types_path = sys.argv[1:], None, None
    if "--memo" in args:
        i = args.index("--memo")
        if i + 1 >= len(args):
            print(USAGE)
            return 1
        memo_path = Path(args[i + 1])
        args = args[:i] + args[i + 2:]
    if "--types" in args:
        i = args.index("--types")
        if i + 1 >= len(args):
            print(USAGE)
            return 1
        types_path = Path(args[i + 1])
        args = args[:i] + args[i + 2:]
    if len(args) != 2:
        print(USAGE)
        return 1
    src, dest = Path(args[0]), Path(args[1])
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
    if any(isinstance(c, dict) and c.get("type") == "paraphrase" for c in data) and memo_path is None:
        print("이 묶음에 paraphrase 후보가 있어 --memo가 필요하다.\n" + USAGE)
        return 1
    typed = [c for c in data if isinstance(c, dict) and c.get("type") in ("single_fact", "paraphrase")]
    if types_path is None and any("en" in (c.get("question_language"), c.get("evidence_language")) for c in typed):
        print("이 묶음의 single_fact·paraphrase 후보에 영어가 있어 --types가 필요하다.\n" + USAGE)
        return 1
    memos = {}
    if memo_path is not None:
        try:
            memos = read_memos(memo_path)
        except (OSError, UnicodeDecodeError) as err:
            print(f"메모 파일을 읽지 못함: {err}")
            return 1
    types = None
    if types_path is not None:
        try:
            types = read_types(types_path)
        except (OSError, UnicodeDecodeError) as err:
            print(f"ChatGPT 답 파일을 읽지 못함: {err}")
            return 1
    try:
        stringify_terms(data)
    except ValueError as err:
        print(err)
        return 1
    if types is not None:
        problems = check_types(typed, types)
        if problems:
            for cid, found in problems.items():
                print(f"ChatGPT 답의 문제  {cid}")
                for f in found:
                    print(f"  {f}")
            rule = "-" * 60
            print(f"카드를 쓰지 않음. 같은 ChatGPT 채팅에 아래 글을 붙여 보내고, 받은 답을 답 파일 끝에 붙여 저장한 뒤 다시 돌린다(같은 후보는 뒤의 답을 쓴다).\n{rule}\n{REREQUEST}{', '.join(problems)}\n{rule}")
            return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    out_dir = dest.parent.resolve()
    dest.write_text(build(data, src.name, out_dir, memos, types), encoding="utf-8")
    print(f"카드 {len(data)}개를 씀: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
