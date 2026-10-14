"""서브에이전트가 뽑은 사실(facts/)을 검사하고 센다.

  python check.py            checked.json과 hits.txt를 쓰고 수를 낸다
  uv run python check.py --markdown   코퍼스의 마크다운으로 다시 센다. checked_markdown.json 등에 쓴다

규칙은 decisions/stage2.md의 2026-10-13 "문서 16개에서 한쪽 언어 문서에만 있는 사실을 세는 방법" 줄에 있다.
 ① 옮긴 구절(quote)이 원문에 글자 그대로 없으면 버린다(공백만 하나로 줄여 견준다).
 ② 반대 언어의 위키백과 문서 8개에서 사실의 낱말(keys_num, keys_name)을 찾는다. 아래일 때 "겹칠 수 있음"이다.
    - 수와 이름 낱말(다른 도시의 문서에서는 그 도시 이름도)이 200자 안에 함께 나온다
    - 같은 도시의 반대 언어 문서인데 사실에 이름 낱말이 없으면 수만 나와도 본다
    - 수가 없는 사실은 이름 낱말이 나오면 본다
    수 하나가 상관없는 자리에 나온 것(연도 등)은 겹침으로 보지 않는다. 처음에는 낱말이 나오기만 하면 겹침으로 봤는데
    279개 가운데 194개가 걸려(대부분 연도) 읽을 수 없었다. 바꾼 것은 decisions/stage2.md에 적었다.
    그 자리를 사람이 읽고 내린 판정은 cleared.json에 {사실의 id: "같은 사실 아님" 또는 "같은 사실"}로 적는다.
"""
import itertools, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
norm = lambda s: re.sub(r"\s+", " ", s).strip()
docs = json.loads((HERE / "docs.json").read_text(encoding="utf-8"))
# --markdown: 대조할 글을 코퍼스의 마크다운(data/corpus/markdown/)으로 바꾼다. 검사 규칙은 같고 글만 다르다.
# 2026-10-14에 정보 상자를 코퍼스에 남기기로 해서 다시 세는 것이다(decisions/stage2.md). 결과는 *_markdown 파일에 따로 쓴다.
MARKDOWN = "--markdown" in sys.argv
SUFFIX = "_markdown" if MARKDOWN else ""
if MARKDOWN:
    import yaml
    CORPUS = HERE.parents[1] / "data" / "corpus"
    text = {}
    for d in yaml.safe_load((CORPUS / "documents.yaml").read_text(encoding="utf-8"))["documents"]:
        t = norm((CORPUS / "markdown" / (d["doc_id"] + ".md")).read_text(encoding="utf-8"))
        key = (d["city"], d["language"]) if d["doc_id"].startswith("wiki-") else ("포털:" + d["doc_id"], d["language"])
        text[key] = t
    assert all((d["city"], d["lang"]) in text for d in docs), "문서 목록의 도시 이름이 docs.json과 다르다"
else:
    text = {(d["city"], d["lang"]): norm((HERE / d["file"]).read_text(encoding="utf-8")) for d in docs}
    # 고른 명소 소개 글과 통계 표(text/extra_이름_언어.txt)도 반대 언어 문서로 넣어 대조한다
    for f in sorted((HERE / "text").glob("extra_*.txt")):
        name, lang = f.stem[len("extra_"):].rsplit("_", 1)
        text[("포털:" + name, lang)] = norm(f.read_text(encoding="utf-8"))
cleared = json.loads((HERE / "cleared.json").read_text(encoding="utf-8")) if (HERE / "cleared.json").exists() else {}

facts = []
for f in sorted((HERE / "facts").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    if "facts" in d:
        facts += [dict(x, city=d["city"], lang=d["lang"], group="한 언어 도시") for x in d["facts"]]
    else:
        for lang in ("ko", "en"):
            facts += [dict(x, city=d["city"], lang=lang, group="두 언어 도시") for x in d.get(lang + "_only", [])]
n = {}
for x in facts:
    k = (x["city"], x["lang"]); n[k] = n.get(k, 0) + 1
    x["id"] = f"{x['city']}_{x['lang']}_{n[k]:02d}"


def find(key, t):
    """수는 다른 수의 일부가 아닐 때만 찾은 것으로 본다. 쉼표는 지우고 견준다."""
    if re.fullmatch(r"[\d,.\-−]+", key):
        k = key.replace(",", "")
        return [m.start() for m in re.finditer(r"(?<![\d.])" + re.escape(k) + r"(?![\d]|\.\d)", t.replace(",", ""))]
    return [m.start() for m in re.finditer(re.escape(key.lower()), t.lower())]


# 도시 이름의 반대 언어 표기. 다른 도시의 문서에서 수가 이 이름 가까이에 나올 때만 겹침으로 본다.
OTHER_NAME = {"수원시": "Suwon", "경주시": "Gyeongju", "세종특별자치시": "Sejong", "광주광역시": "Gwangju", "부산광역시": "부산", "제주시": "제주",
              "안동시": "안동", "강릉시": "강릉", "전주시": {"ko": "Jeonju", "en": "전주"}, "청주시": {"ko": "Cheongju", "en": "청주"},
              "춘천시": {"ko": "Chuncheon", "en": "춘천"}, "천안시": {"ko": "Cheonan", "en": "천안"}}
NEAR = 200
is_num = lambda k: bool(re.fullmatch(r"[\d,.\-−]+", k))
lines = []
for x in facts:
    x["quote_ok"] = norm(x["quote"]) in text[(x["city"], x["lang"])]
    nm = OTHER_NAME[x["city"]]
    nm = nm[x["lang"]] if isinstance(nm, dict) else nm
    nums = [k for k in x.get("keys_num", []) if len(k) >= 3]
    names = [k for k in x.get("keys_name", []) if len(k) >= 2]
    hits = []
    for (city, lang), t in text.items():
        if lang == x["lang"]:
            continue
        tn = t.replace(",", "")
        # 같은 도시의 반대 언어 문서에서는 도시 이름이 어디에나 나오므로 사실의 이름 낱말만 쓴다
        anchors = names if city == x["city"] else names + [nm]
        npos = [(k, q) for k in nums for q in find(k, t)]
        apos = [(k, q) for k in anchors for q in find(k, tn)]
        if nums and names or nums and city != x["city"]:
            strong = [(k, q, a) for k, q in npos for a, r in apos if abs(q - r) <= NEAR]
        elif nums:           # 같은 도시의 문서인데 이름 낱말이 없는 사실: 수만 나와도 본다
            strong = [(k, q, "") for k, q in npos]
        else:                # 수가 없는 사실: 이름 낱말이 나오면 본다
            strong = [(k, q, "") for k, q in [(k, q) for k in names for q in find(k, tn)]]
        for k, q, a in strong[:2]:
            hits.append({"doc": f"{city}_{lang}", "key": k + (" + " + a if a else ""), "around": tn[max(0, q - 100): q + 100]})
    x["hits"] = hits
    if not x["quote_ok"]:
        x["status"] = "버림: 구절이 원문에 없음"
    elif not hits:
        x["status"] = "통과"
    elif cleared.get(x["id"]) == "같은 사실 아님":
        x["status"] = "통과(읽고 확인)"
    elif cleared.get(x["id"]) == "같은 사실":
        x["status"] = "뺌: 반대 언어 문서에 같은 사실"
    else:
        x["status"] = "겹칠 수 있음"
        lines.append(f"## {x['id']} [{x['kind']}] {x['fact']} (값: {x.get('value')})")
        lines += [f"   - {h['doc']} '{h['key']}': …{h['around']}…" for h in hits]
(HERE / f"checked{SUFFIX}.json").write_text(json.dumps(facts, ensure_ascii=False, indent=1), encoding="utf-8")
(HERE / f"hits{SUFFIX}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

ok = [x for x in facts if x["status"].startswith("통과")]
print("상태별:", {s: sum(1 for x in facts if x["status"] == s) for s in sorted({x["status"] for x in facts})})
out = {}
for lang in ("ko", "en"):
    L = [x for x in ok if x["lang"] == lang]
    multi = [(a["id"], b["id"], a["kind"]) for a, b in itertools.combinations(L, 2)
             if a["kind"] == b["kind"] != "other" and a["city"] != b["city"]]
    out[lang] = {"통과한 사실": len(L), "그중 표에서 나온 사실": sum(1 for x in L if x["from_table"]),
                 "한 언어 도시의 문서에서": sum(1 for x in L if x["group"] == "한 언어 도시"),
                 "두 언어 도시의 문서에서": sum(1 for x in L if x["group"] == "두 언어 도시"),
                 "여러 문서 연결 후보(같은 종류의 사실 둘)": len(multi),
                 "종류별 문서 수": {k: len({x["city"] for x in L if x["kind"] == k}) for k in sorted({x["kind"] for x in L}) if k != "other"}}
    print(lang, json.dumps(out[lang], ensure_ascii=False))
(HERE / f"counts{SUFFIX}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
