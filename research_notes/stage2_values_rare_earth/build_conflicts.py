"""알려진 부딪히는 값 목록을 만든다(이슈 #7, 값 목록 3단계).

실행: .venv/bin/python research_notes/stage2_values_rare_earth/build_conflicts.py
읽는 것(읽기만 한다): compare.json, values.json, vocab.json, verdicts.json, data/corpus/markdown/*.md
쓰는 것: data/questions/known_conflicts.json (src/questions/check_candidates.py가 읽는다),
         research_notes/stage2_values_rare_earth/known_conflicts.md (문제 지침에 붙일 한국어 목록)

부딪히는 값(충돌)인 묶음: compare.json에서 판정이 "다름"이고 (읽을 것이 아니거나, verdicts.json이 "부딪힘"이라고 한 것).
읽을 것인 "다름" 묶음에 판정이 없거나, 판정의 열쇠가 어느 "다름" 묶음에도 안 맞으면 아무것도 쓰지 않고 오류로 멈춘다.
충돌 묶음의 곳은 전부 적는다(문제에 쓸 수 없는 것은 소수 값만이 아니다).
verdicts.json의 "manual"은 compare.json 묶음이 아닌 충돌(숫자를 낱말로 적은 것 등)이다.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import compare as cp  # noqa: E402

MD_DIR = ROOT / "data" / "corpus" / "markdown"
OUT_JSON = ROOT / "data" / "questions" / "known_conflicts.json"
OUT_MD = HERE / "known_conflicts.md"
SCOPE_ORDER = [cp.SCOPE_SAME_DOC, cp.SCOPE_SAME_LANG, cp.SCOPE_OTHER_LANG]
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


def key_of(obj, qty, cond):
    return f"{obj}|{qty}|{cond}"


def read_lines(doc_id, cache={}):
    if doc_id not in cache:
        cache[doc_id] = (MD_DIR / f"{doc_id}.md").read_text(encoding="utf-8").split("\n")
    return cache[doc_id]


def quantity_labels(vocab):
    """양 열쇠 -> 한국어 이름(vocab의 한국어 줄 이름이나 열 이름, 끝의 괄호는 뗀다). 없으면 열쇠 그대로."""
    out = {}
    hangul = re.compile("[가-힣]")
    entries = [(lab, e["quantity"]) for lab, e in vocab["infobox_label"].items()]
    entries += [(lab, q) for lab, q in vocab["table_column"].items() if q != "@object"]
    for lab, q in entries:
        if hangul.search(lab) and q not in out:
            out[q] = re.sub(r"\s*\(.*\)\s*$", "", lab).strip() or lab
    return out


def values_of(raws):
    """raw 글들에서 두 자리 이상 숫자(쉼표와 소수점을 뺀 자릿수)를 쉼표 없이 적힌 그대로, 겹치지 않게."""
    out = []
    for raw in raws:
        for m in NUM_RE.findall(raw):
            v = m.replace(",", "")
            if len(v.replace(".", "")) >= 2 and v not in out:
                out.append(v)
    return out


def section_of(places):
    """곳들(doc_id, lang)의 모든 짝에서 나온 범위를 정해진 차례로 ' · '로 잇는다."""
    scopes = set()
    for i, a in enumerate(places):
        for b in places[i + 1:]:
            scopes.add(cp.scope_of(a, b))
    return " · ".join(s for s in SCOPE_ORDER if s in scopes)


def line_text(lines):
    return "·".join(str(n) for n in lines) + "줄"


def make_entry(section, obj, qty, cond, places, labels, why=None):
    """places: [{doc_id, lines, quotes: {줄: 원문 줄}, raws, items: [{line, label, raw}]}] -> 항목 하나."""
    targets = []
    for doc in dict.fromkeys(p["doc_id"] for p in places):
        mine = [p for p in places if p["doc_id"] == doc]
        quotes, items = [], []
        for p in mine:
            for ln in p["lines"]:
                q = p["quotes"][ln].rstrip()
                if q not in quotes:
                    quotes.append(q)
            items += p["items"]
        targets.append({"doc_id": doc, "quotes": quotes, "values": values_of([i["raw"] for i in items]),
                        "places": [{"line": i["line"], "label": i["label"], "raw": i["raw"]} for i in items]})
    bits = []
    for p in places:
        raws = list(dict.fromkeys(p["raws"]))
        bits.append(f"`{p['doc_id']}` {line_text(p['lines'])} {', '.join(raws)}")
    label = labels.get(qty)
    head = f"{obj} {label + '(' + qty + ')' if label else qty}" + (f" [조건 {cond}]" if cond else "")
    text = f"{head}: " + " / ".join(bits) + (f" — {why}" if why else "")
    return {"section": section, "text": text, "object": obj, "quantity": qty, "condition": cond, "targets": targets}


def collect(compare, records, vocab, verdicts):
    """충돌 항목 목록과 오류 목록을 돌려준다."""
    errors = []
    groups = {key_of(g["object"], g["quantity"], g["condition"]): g for g in compare["groups"]}
    different = {k for k, g in groups.items() if g["verdict"] == "다름"}
    given = {k: v for k, v in verdicts.items() if k != "manual"}
    missing = sorted(k for k in different if groups[k]["review"] and k not in given)
    if missing:
        errors.append(("읽을 \"다름\" 묶음에 판정이 없다", missing))
    unknown = sorted(k for k in given if k not in different)
    if unknown:
        errors.append(("판정의 열쇠가 어느 \"다름\" 묶음에도 안 맞는다", unknown))
    bad_value = sorted(k for k, v in given.items() if v.get("verdict") not in ("부딪힘", "부딪힘 아님"))
    if bad_value:
        errors.append(("판정 글자가 \"부딪힘\"이나 \"부딪힘 아님\"이 아니다", bad_value))
    contradict = sorted(k for k, v in given.items() if k in different and not groups[k]["review"] and v.get("verdict") == "부딪힘 아님")
    if contradict:
        errors.append(("읽지 않아도 되는 \"다름\" 묶음에 \"부딪힘 아님\" 판정이 있다(규칙은 충돌로 본다)", contradict))
    labels = quantity_labels(vocab)
    keyed = cp.apply_keys(records, vocab)            # 묶을 때와 같은 열쇠로 자리를 찾는다
    entries = []
    for k in sorted(different):
        g = groups[k]
        if g["review"] and given.get(k, {}).get("verdict") != "부딪힘":
            continue
        places = []
        for p in g["places"]:
            recs = [r for r in keyed if r["doc_id"] == p["doc_id"] and r["line"] in p["lines"] and r["object"] == g["object"]
                    and r["quantity"] == g["quantity"] and r["condition"] == g["condition"]
                    and (r["where"] == "표" or r["raw"] in p["raws"])]
            if sorted(r["raw"] for r in recs) != sorted(p["raws"]):
                errors.append(("compare.json의 곳을 values.json의 자리와 맞추지 못했다", [p["place"]]))
                continue
            places.append({"doc_id": p["doc_id"], "lang": p["lang"], "lines": p["lines"], "raws": p["raws"],
                           "quotes": {int(ln): q for ln, q in p["quotes"].items()},
                           "items": [{"line": r["line"], "label": r["label"], "raw": r["raw"]} for r in sorted(recs, key=lambda r: (r["line"], r["start"]))]})
        entries.append(make_entry(" · ".join(s for s in SCOPE_ORDER if s in g["scopes"]), g["object"], g["quantity"], g["condition"], places, labels))
    by_id = {r["id"]: r for r in records}
    for m in verdicts.get("manual", []):
        places = []
        for pl in m["places"]:
            if "id" in pl:
                r = by_id.get(pl["id"])
                if r is None:
                    errors.append(("manual의 자리 id가 values.json에 없다", [pl["id"]]))
                    continue
                places.append({"doc_id": r["doc_id"], "lang": r["lang"], "lines": [r["line"]], "raws": [r["raw"]], "quotes": {r["line"]: r["quote"]},
                               "items": [{"line": r["line"], "label": r["label"], "raw": r["raw"]}]})
            else:
                lines = read_lines(pl["doc_id"])
                if not 1 <= pl["line"] <= len(lines) or pl["raw"] not in lines[pl["line"] - 1]:
                    errors.append(("manual의 raw가 그 줄에 없다", [f"{pl['doc_id']}:{pl['line']}: {pl['raw']}"]))
                    continue
                lang = "ko" if pl["doc_id"].startswith("wiki-ko-") else "en"
                places.append({"doc_id": pl["doc_id"], "lang": lang, "lines": [pl["line"]], "raws": [pl["raw"]],
                               "quotes": {pl["line"]: lines[pl["line"] - 1]}, "items": [{"line": pl["line"], "label": "", "raw": pl["raw"]}]})
        if len(places) >= 2:
            entries.append(make_entry(section_of(places), m["object"], m["quantity"], m["condition"], places, labels, m["why"]))
    entries.sort(key=lambda e: (tuple(SCOPE_ORDER.index(s) for s in e["section"].split(" · ")), e["object"], e["quantity"], e["condition"]))
    return entries, errors


INTRO = (
    "이 목록은 코퍼스 20개 문서에서 같은 대상의 같은 양이 문서끼리, 또는 한 문서 안에서 서로 다른 값으로 적힌 곳이다. "
    "문제의 정답이나 근거 구절로 쓰면 안 된다. 값 목록(`values.json`)에서 (대상, 양, 조건)이 같은 자리끼리 묶고, "
    "숫자가 정확히 같은 경우만 같은 값으로 보았다(반올림·어림·범위·단위 환산이 정확히 같지 않으면 다른 값). "
    "그 기준은 decisions/stage2.md 2026-10-22 '희토류 원소 값 목록의 \"다른 값\" 기준' 줄에 있다. "
    "읽어야 하는 묶음은 AI(Claude)가 원문을 읽고 부딪히는지 판정했다(`verdicts.json`). 숫자를 낱말로 적어 값 목록에 없는 부딪힘은 AI가 찾은 것만 손으로 더했다(`verdicts.json`의 manual). 한계: 숫자가 없는 본문 문장은 비교하지 않았다"
    "(decisions/stage2.md 2026-10-22 '희토류 원소 값 목록에 넣는 값' ㉣)."
)


def markdown(entries):
    out = ["# 알려진 부딪히는 값", "", INTRO, ""]
    seen = []
    for e in entries:
        if e["section"] not in seen:
            seen.append(e["section"])
    for s in seen:
        mine = [e for e in entries if e["section"] == s]
        out += [f"## {s} ({len(mine)}개)", ""]
        out += [f"- {e['text']}" for e in mine]
        out.append("")
    return "\n".join(out)


def main():
    compare = json.loads((HERE / "compare.json").read_text(encoding="utf-8"))
    records = json.loads((HERE / "values.json").read_text(encoding="utf-8"))
    vocab = json.loads((HERE / "vocab.json").read_text(encoding="utf-8"))
    verdicts = json.loads((HERE / "verdicts.json").read_text(encoding="utf-8"))
    entries, errors = collect(compare, records, vocab, verdicts)
    if errors:
        print("오류: 아무것도 쓰지 않았다")
        for what, items in errors:
            print(f"  {what} ({len(items)}):")
            for x in items:
                print("    ", x)
        sys.exit(1)
    OUT_JSON.write_text(json.dumps(entries, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown(entries), encoding="utf-8")
    by = {}
    for e in entries:
        by[e["section"]] = by.get(e["section"], 0) + 1
    print("절별 항목 수:", by)
    n_manual = len(verdicts.get("manual", []))
    print(f"항목 {len(entries)}개 (compare 묶음 {len(entries) - n_manual}개 + manual {n_manual}개), 대상(targets) {sum(len(e['targets']) for e in entries)}개")


if __name__ == "__main__":
    main()
