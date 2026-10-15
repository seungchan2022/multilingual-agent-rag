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
    "칸 뜻은 순서표(data/questions/final_set_guide.md)의 \"후보 YAML 칸의 뜻\"에 있다. "
    "카드마다 끝에 그 후보의 원본 YAML을 참고용으로 붙인다."
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


NUM_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")
CARD_INTRO = (
    "이 카드만 보고 위에서부터 차례로 한다. 칸마다 \"할 일\"을 하고 \"판단할 질문\"에 답한 뒤, 문제가 없으면 그 칸의 `[ ]`를 `[x]`로 바꾼다. "
    "문제가 있으면 `[ ]`로 두고 맨 아래 \"이유\"에 적는다. 번역기(파파고 등)를 브라우저에 열어 둔다. 시작과 끝 시각을 \"메모\"에 적는다."
)
TYPE_MEANING = {
    "single_fact": "단일 사실: 질문이 근거 구절의 핵심 낱말을 그대로 썼다(이름은 빼고 본다).",
    "paraphrase": "표현 불일치: 질문이 근거 구절의 핵심 낱말을 다른 말로 바꿔 썼다(이름은 빼고 본다).",
    "table_numeric": "표·수치·조건: 답이 표에 있거나, 문서에 값이 여러 개라 조건(연도, 기준)에 맞는 것을 골라야 한다. 문장에 수치가 하나뿐이면 아니다.",
    "multi_doc": "여러 문서 연결: 둘 이상의 문서나 구절을 합쳐야 답이 나온다(비교, 집계, 여러 단계).",
}


def numbers_of(c):
    """정답과 근거 구절에서 숫자(1,234 / 12.5 / 1969)를 순서대로, 중복 없이, 최대 6개."""
    texts = [str(c.get("answer"))]
    for f in c.get("required_facts") or []:
        texts += [item["passage"] for item in f.get("evidence") or []]
    return list(dict.fromkeys(n for t in texts for n in NUM_RE.findall(t)))[:6]


def item(n, title, body):
    return ["", f"#### {n}. {title}"] + body + ["- [ ] 확인함"]


def verdict_block(searched):
    return ["", "#### 적기",
            "- 판정(하나만 남긴다): 채택 / 수정 / 폐기",
            "- 이유(한 줄. 문제가 없으면 \"1~9 문제 없음\"):",
            f"- 더 찾아본 말과 걸린 곳({searched}):",
            "- 메모(시작·끝 시각, 애매한 것, Claude에게 물을 것):"]


def details_block(c):
    dump = yaml.safe_dump(c, allow_unicode=True, sort_keys=False).rstrip("\n")
    return ["", "<details><summary>참고용 원본 YAML</summary>", "", "```yaml", dump, "```", "", "</details>"]


def source_hint(d, out_dir, opposite):
    """같은 도시의 반대 언어 문서 하나를 어떻게 읽는지."""
    did = d["doc_id"]
    if opposite == "ko":
        return f"{link(out_dir, did)}를 열어 3번의 찾을 말로 `Cmd+F` 하고 앞뒤를 읽는다."
    if did.startswith("wiki-"):
        return (f"크롬에서 {d['url']} 를 연다. 페이지에서 오른쪽 클릭 → \"한국어로 번역\". "
                "`Cmd+F`로 3번의 찾을 말(한국어)과 숫자를 찾아 앞뒤를 읽는다. 절 이름으로 짐작해 고르지 않는다.")
    if did.startswith("portal-"):
        return f"{link(out_dir, did)}를 열어 표를 본다."
    return f"{link(out_dir, did)}를 열어 내용 전체를 번역기에 붙여 읽는다. 짧은 글이다."


def answered_card(c, out_dir):
    el = c["evidence_language"]
    opposite = "en" if el == "ko" else "ko"
    opp, own = LANG_NAME[opposite], LANG_NAME[el]
    tr = "번역기로 " if opposite == "en" else ""
    out = ["---", "", f"## {c['id']} · `type`(유형): {type_label(c['type'])} · 도시 묶음: {city_part(c)}", "", CARD_INTRO, "",
           "**후보**", f"- `question`(질문): {c['question']}", f"- `answer`(정답): {c['answer']}", "- `required_facts`(꼭 필요한 사실):"]
    passages = []
    for i, f in enumerate(c["required_facts"], 1):
        out.append(f"  - `fact`(사실) {i}: {f['fact']}" + ("" if f.get("evidence") else " (근거 없음 — 다른 사실에서 나오는 결론)"))
        for j, ev in enumerate(f.get("evidence") or [], 1):
            passages += [f"  - 사실 {i}의 근거 {j}: {passage_link(out_dir, ev['doc_id'], ev['passage'])} · `location`(위치): {ev['location']}",
                         quote(ev["passage"], 4)]
    out += ["- `passage`(근거 구절):"] + (passages or ["  - 없음"])

    out += item(1, "근거 구절만 읽고 정답이 나온다", [
        "- 할 일: 위 `passage`(근거 구절)를 읽는다.",
        "- 판단할 질문: 이 구절만 받은 사람이 `question`(질문)에 `answer`(정답)대로 답할 수 있는가? 조건과 단위까지 구절에 있는가?"])
    out += item(2, "정답이 하나로 정해진다", [
        "- 할 일: 위 `passage`(근거 구절)에 질문의 답이 될 만한 값(숫자, 이름)이 몇 개 있는지 본다.",
        "- 판단할 질문: 그런 값이 여러 개라면, 질문이 그중 하나만 가리키는가?"])
    nums = numbers_of(c)
    docs = evidence_docs(c)
    doc_links = f" 근거 문서: {', '.join(link(out_dir, d) for d in docs)}." if len(docs) > 1 else ""
    out += item(3, "같은 문서 안에 다른 값이 없다", [
        "- 찾을 말: 질문에서 그 사실의 이름(무엇에 대한 질문인지)을 하나 이상 고르고, 정답의 값도 찾는다. 정답에서 뽑은 숫자: "
        + (", ".join(f"`{n}`" for n in nums) if nums else "없음"),
        "- 할 일: 위 근거 문서 링크를 `Cmd+클릭`해 열고, `Cmd+F`로 찾을 말을 하나씩 찾아 걸린 곳을 `Enter`로 넘겨 본다. "
        "근거 구절이 있는 줄에서는 앞뒤 한두 문장도 읽는다." + doc_links,
        "- 판단할 질문: 걸린 곳마다, 같은 것이 `answer`(정답)과 다른 값으로 적혀 있지 않은가? 앞뒤 문장이 다른 대상 이야기로 바뀌지 않는가?"])
    out += item(4, f"같은 언어({own})의 다른 문서에 다른 값이 없다", [
        f"- 할 일: `Cmd+Shift+F`(폴더 찾기)를 연다. 찾기 칸 아래 `...`을 눌러 \"포함할 파일\"에 `data/corpus/markdown/*-{el}-*`를 적는다. 3번의 찾을 말로 찾는다.",
        "- 판단할 질문: 근거 문서 말고 다른 문서가 걸리면, 거기에 같은 것이 다른 값으로 적혀 있지 않은가?"])

    checks = c.get("opposite_check") or []
    terms = [it["term"] for it in checks]
    with_hits = [it for it in checks if it.get("hits")]
    none_terms = [f"`{it['term']}`" for it in checks if not it.get("hits")]
    if with_hits:
        body = [f"Gemini가 {opp} 문서에서 찾은 말과 걸린 곳이다. 찾을 말마다 나오는 곳은 아래가 전부다(검사 프로그램이 확인함)."
                + (f" {', '.join(none_terms)}은(는) {opp} 문서 어디에도 없다." if none_terms else "")]
        for it in with_hits:
            body.append(f"- `term`(찾을 말) `{it['term']}`:")
            for k, h in enumerate(it["hits"], 1):
                line = line_of_text(h["doc_id"], h["excerpt"])
                body += [f"  - 걸린 곳 {k}: {link(out_dir, h['doc_id'], line, line is not None)}", quote(h["excerpt"], 4), "",
                         f"    Gemini의 판단: 같은 사실 {'맞음' if h['same_fact'] else '아님'} — {h['why']}"]
        body += [f"- 할 일: 걸린 문장을 하나씩 {tr}읽는다." if opposite == "ko" else "- 할 일: 걸린 문장을 하나씩 번역기에 붙여 읽는다.",
                 "- 판단할 질문: 이 문장이 위 `required_facts`(꼭 필요한 사실)와 같은 사실을 말하는가?"]
    elif terms:
        body = [f"Gemini가 찾은 말 {', '.join(none_terms)}은(는) {opp} 문서 어디에도 없다(검사 프로그램이 확인함). 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다."]
    else:
        body = ["Gemini가 찾은 말이 없다. 이 칸은 읽을 것이 없으니 `[x]`로 바꾼다."]
    out += item(5, f"{opp} 문서: Gemini가 찾은 걸린 곳을 {tr}읽었다", body)

    out += item(6, f"{opp} 문서: 다른 말로도 찾아봤다", [
        "- Gemini가 찾은 말: " + (", ".join(f"`{t}`" for t in terms) if terms else "없음"),
        "- 할 일: 그 사실의 이름과 숫자가 위 말에 들어 있는지 본다. 빠졌거나 " + opp + " 문서가 다른 말로 적었을 것 같으면, "
        + (f"번역기로 그 이름을 {opp}로 옮겨 나온 말이나 더 짧은 말로 폴더 찾기를 한다. " if opposite == "en" else "더 짧은 말이나 비슷한 말로 폴더 찾기를 한다. ")
        + f"\"포함할 파일\"은 `data/corpus/markdown/*-{opposite}-*`. 걸린 곳이 있으면 그 줄을 {tr}읽는다.",
        f"- 판단할 질문: {opp} 문서 어딘가에 같은 사실이 다른 표현으로 있는가?",
        "- 찾아본 말과 결과를 맨 아래 \"더 찾아본 말과 걸린 곳\"에 적는다."])

    cities = list(dict.fromkeys(DOC[d]["city"] for d in docs))
    same_city = [d for d in _DOCS if d["city"] in cities and d["language"] == opposite]
    if same_city:
        body = [f"- 할 일 {n} ({d['doc_id']}): {source_hint(d, out_dir, opposite)}" for n, d in enumerate(same_city, 1)]
        body.append(f"- 판단할 질문: 이 문서 어디에든 위 `required_facts`(꼭 필요한 사실)와 같은 사실이 있는가?")
    else:
        body = [f"같은 도시의 {opp} 문서가 없다({own} 도시). 이 칸은 `[x]`로 바꾼다."]
    out += item(7, f"{opp} 문서: 같은 도시({', '.join(cities)})의 {opp} 문서를 통째로 읽었다", body)

    out += item(8, "꼭 필요한 사실이 빠짐없고 군더더기 없다", [
        "- 할 일: 위 `required_facts`(꼭 필요한 사실)와 `answer`(정답)를 견준다.",
        "- 판단할 질문: 정답을 말하는 데 이 사실들이 꼭 필요하고, 이것 말고 더 필요한 사실은 없는가?"])
    out += item(9, "유형이 맞다", [
        f"- 할 일: 이 후보의 유형은 {type_label(c['type'])}다. 아래 뜻과 견준다.",
        f"- {TYPE_MEANING.get(c['type'], '')} 두 유형에 다 맞으면 여러 문서 연결 → 표·수치·조건 → 단일 사실/표현 불일치 순서로 먼저 맞는 것이다.",
        "- 판단할 질문: 이 후보가 이 뜻에 맞는가?"])
    return out + verdict_block("6번에서 직접 찾은 것. 예: \"industrial → 영어 문서 3곳, 모두 다른 이야기\"") + details_block(c)


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
    out += item(1, "문서 전체에서 한국어 표현과 영어 표현으로 찾아봐도 답이 없다", [
        "- 할 일: 질문의 이름과 숫자를 한국어와 영어(번역기)로 폴더 찾기를 한다. \"포함할 파일\"은 `data/corpus/markdown`.",
        "- 판단할 질문: 질문의 답이 되는 내용이 어디에도 없는가?"])
    out += item(2, "문서를 보지 않고 일반 지식으로도 답할 수 없다", [
        "- 할 일: 문서를 열지 않고 `question`(질문)을 읽는다.",
        "- 판단할 질문: 세상에 실제로 답이 있는 질문은 아닌가?"])
    out += item(3, "전제가 너무 뻔하게 틀리지 않았다", [
        "- 할 일: `question`(질문)이 깔고 있는 전제를 찾는다.",
        "- 판단할 질문: 그 전제가 한눈에 틀렸다고 보이지 않는가?"])
    return out + verdict_block("찾아본 말과 걸린 곳") + details_block(c)


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
