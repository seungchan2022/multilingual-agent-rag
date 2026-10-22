"""도메인을 고를 때(3 세기) 확인한 "그 언어에만 있는 사실"이 알려진 부딪히는 값에 걸려도 기준을 채우는지 다시 센다(이슈 #7).

실행: .venv/bin/python research_notes/stage2_values_rare_earth/recheck_step3.py [부딪히는 값 목록 경로]
      (경로를 주지 않으면 data/questions/known_conflicts.json)
읽는 것(읽기만 한다): step3/confirm.json, confirm_more.json(있을 때만), step3/results.json, step3/md/*.md, data/corpus/documents.yaml,
                    data/corpus/markdown/*.md, values.json, 부딪히는 값 목록
쓰는 것: recheck_step3.json

2단계 기준: 언어마다 한 쪽에만 있는 확인된 사실(side == "one")이 18개 이상이고, 그 가운데 표(in_table)가 3개 이상.
확인된 사실 = confirm.json에서 field == "rare_earth", read_ok == true, truth == "그 언어에만"인 기록.
confirm_more.json(있을 때만)은 3 세기 때 확인하지 못한 기록(read_ok, truth가 null)을 나중에 확인한 것이다.
같은 no의 confirm.json 기록에 read_ok, truth, note만 덮어 합친다. 그 no가 confirm.json에 없거나, field, lang, side, group이 다르거나,
confirm.json에서 이미 채워져 있거나, confirm_more에 같은 no가 두 번 있으면 오류로 멈춘다. 사실마다 출처(source)를 "3 세기"나 "confirm_more"로 적는다.

사실 하나는 값 묶음(group)의 언급(mention)들로 3 세기 마크다운에 있다. 언급을 오늘의 문서에서 찾는다.
  1) 옛 줄이 오늘 문서에 줄 하나로 정확히 한 번 있으면 줄 안 위치를 그대로 쓴다.
  2) 아니면 창(앞 40자 + raw + 뒤 40자, 줄 끝에서 자름)이 오늘 문서에 정확히 한 번 있을 때 쓴다.
  3) 그래도 안 되면 앞이나 뒤 한쪽만 붙인 창(raw + 뒤 40자, 앞 40자 + raw)을 차례로 해 본다. (해석: 옛 줄과 오늘 줄이
     중간 글자만 다를 때, 예를 들어 "(실험값) 228 pm"과 "(실험값) / 228 pm"을 잇기 위해서다.)
  4) 그래도 안 되면 "찾지 못함"으로 적고 짐작하지 않는다.
언급의 자리 = values.json에서 그 문서, 그 줄(1부터)의 기록 가운데 [start, end)가 언급의 줄 안 위치를 담는 것. 없으면 "자리 없음".

막는 기준 둘:
  (A) 값 자체: 언급의 자리가 목록 항목 대상의 places 가운데 하나(문서, 줄, raw가 같다).
  (B) 검사기 기준: src/questions/check_candidates.py의 conflict_reasons(266~282줄)가 언급의 줄 하나로 된 구절에 하는 일.
      줄이 같은 문서 대상의 quotes 가운데 하나와 줄 끝 공백을 떼고 같거나(268~270줄, 자리),
      대상의 values 가운데 하나가 쉼표를 뺀 줄에 정규식으로 있으면(272~275줄, 값) 막힌다.
      (항목 맨 위의 quotes, values와 해(table_years) 규칙, 표 구절의 머리글 행 빼기는 따르지 않는다. 이 목록에는 맨 위 quotes,
      values가 없고, 표 줄 하나는 원래 검사기에서 머리글 행으로 빠져 자리 규칙에 안 걸리지만 여기서는 줄이 같으면 막는다.)

사실이 쓸 수 있는 때: 언급 하나라도 찾았고, (A)는 자리가 있고, 그 기준에 막히지 않았을 때.
  (B)는 자리가 없어도 줄이 안 막혔으면 쓸 수 있고, 그렇게만 쓸 수 있는 사실은 따로 센다.
엄격한 쪽: 쓸 수 있는 데다 찾은 언급이 하나도 막히지 않은 사실.
"""
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STEP3 = ROOT / "research_notes" / "stage2_stem_select" / "step3"
DOCS_YAML = ROOT / "data" / "corpus" / "documents.yaml"
MD_DIR = ROOT / "data" / "corpus" / "markdown"
VALUES = HERE / "values.json"
OUT = HERE / "recheck_step3.json"
DEFAULT_CONFLICTS = ROOT / "data" / "questions" / "known_conflicts.json"
CONFIRM_MORE = HERE / "confirm_more.json"
SRC_STEP3 = "3 세기"
SRC_MORE = "confirm_more"

NEED_ONE = 18        # 언어마다 한 쪽에만 있는 확인된 사실의 하한
NEED_TABLE = 3       # 그 가운데 표의 하한
WINDOW = 40
MISSING = "찾지 못함"
NO_SLOT = "자리 없음"
OK = "사용 가능"
BLOCKED = "막힘"


def read_text(path):
    """줄바꿈을 바꾸지 않고 읽는다(오프셋이 어긋나지 않게)."""
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


# --- 입력 -------------------------------------------------------------------
def merged_confirm(more_path):
    """confirm.json 기록에 confirm_more의 read_ok, truth, note를 덮어 합친다. 기록마다 source를 붙인다."""
    rows = json.loads((STEP3 / "confirm.json").read_text(encoding="utf-8"))
    rows = [dict(r, source=SRC_STEP3) for r in rows]
    if not Path(more_path).exists():
        return rows
    by_no = {r["no"]: r for r in rows}
    seen = set()
    for m in json.loads(Path(more_path).read_text(encoding="utf-8")):
        no = m["no"]
        if no in seen:
            sys.exit(f"오류: confirm_more에 {no}가 두 번 있음")
        seen.add(no)
        base = by_no.get(no)
        if base is None:
            sys.exit(f"오류: confirm_more의 {no}가 confirm.json에 없음")
        for k in ("field", "lang", "side", "group"):
            if m[k] != base[k]:
                sys.exit(f"오류: confirm_more의 {no}의 {k}({m[k]})가 confirm.json({base[k]})과 다름")
        if base["read_ok"] is not None or base["truth"] is not None:
            sys.exit(f"오류: confirm_more의 {no}는 confirm.json에 이미 채워져 있어 덮어쓸 수 없음")
        base.update(read_ok=m["read_ok"], truth=m["truth"], note=m["note"], source=SRC_MORE)
    return rows


def confirmed_facts(more_path=CONFIRM_MORE):
    """확인된 희토류 사실(그 언어에만)."""
    return [r for r in merged_confirm(more_path) if r.get("field") == "rare_earth" and r.get("read_ok") is True and r.get("truth") == "그 언어에만"]


def old_groups():
    """3 세기 결과에서 (언어, 쪽, 묶음 id) -> 묶음, 그리고 문서 목록."""
    f = json.loads((STEP3 / "results.json").read_text(encoding="utf-8"))["fields"]["rare_earth"]
    groups = {(lang, side, g["id"]): g for lang, sides in f["groups"].items() for side, gs in sides.items() for g in gs}
    return groups, f["docs"]


def today_doc_ids():
    """(언어, revid 글자) -> 오늘의 doc_id."""
    docs = yaml.safe_load(DOCS_YAML.read_text(encoding="utf-8"))["documents"]
    return {(d["language"], d["version"].removeprefix("revid ")): d["doc_id"] for d in docs}


def load_conflicts(path):
    """부딪히는 값 목록의 항목 가운데 대상마다 (항목 번호, 문서, places, quotes, values)를 펼친다."""
    entries = json.loads(Path(path).read_text(encoding="utf-8"))
    targets = []
    for n, e in enumerate(entries, 1):
        for t in e["targets"]:
            targets.append({"entry": n, "doc_id": t["doc_id"], "places": t["places"], "quotes": t["quotes"], "values": t["values"]})
    return targets


# --- 오늘 문서에서 언급 찾기 --------------------------------------------------
def line_of(text, pos):
    """text에서 글자 위치 pos가 있는 줄 번호(0부터)와 그 줄이 시작하는 위치."""
    n = text.count("\n", 0, pos)
    start = text.rfind("\n", 0, pos) + 1
    return n, start


def locate(mention, old_text, new_text):
    """언급을 오늘 문서에서 찾는다. (줄 번호 1부터, 줄 안 start, 방법) 또는 (None, None, 이유)."""
    raw, start = mention["raw"], mention["start"]
    if old_text[start:mention["end"]] != raw:
        return None, None, "옛 문서의 위치가 raw와 맞지 않음"
    ln, ls = line_of(old_text, start)
    old_lines = old_text.split("\n")
    if ln != mention["line"]:
        return None, None, "옛 문서의 줄 번호가 위치와 맞지 않음"
    old_line, off = old_lines[ln], start - ls
    new_lines = new_text.split("\n")
    same = [i for i, l in enumerate(new_lines) if l == old_line]
    if len(same) == 1:
        return same[0] + 1, off, "줄"
    end_off = off + len(raw)
    for label, nb, na in (("창", WINDOW, WINDOW), ("뒤 창", 0, WINDOW), ("앞 창", WINDOW, 0)):
        before, after = old_line[max(0, off - nb):off], old_line[end_off:end_off + na]
        window = before + raw + after
        if new_text.count(window) != 1:
            continue
        pos = new_text.index(window) + len(before)
        nl, nls = line_of(new_text, pos)
        return nl + 1, pos - nls, label
    return None, None, "줄도 창도 오늘 문서에서 정확히 한 번 나오지 않음"


def slot_of(records, doc_id, line, off):
    """values.json에서 doc_id의 line(1부터) 줄의 기록 가운데 [start, end)가 off를 담는 것. 없으면 None."""
    for r in records.get((doc_id, line), []):
        if r["start"] <= off < r["end"]:
            return r
    return None


# --- 막는 기준 ---------------------------------------------------------------
def blocked_A(doc_id, line, slot, targets):
    """(A) 자리가 목록 대상의 places 가운데 하나인가. 걸린 항목 번호들."""
    if slot is None:
        return []
    return [t["entry"] for t in targets if t["doc_id"] == doc_id and any(p["line"] == line and p["raw"] == slot["raw"] for p in t["places"])]


def blocked_B(doc_id, text_line, targets):
    """(B) check_candidates.conflict_reasons가 이 줄 하나에 하는 일. [(항목 번호, "자리"나 "값 v")]."""
    flat = text_line.replace(",", "")                                       # check_candidates 272줄
    out = []
    for t in targets:
        if t["doc_id"] != doc_id:
            continue
        if any(text_line.rstrip() == q.rstrip() for q in t["quotes"]):      # 268~270줄(줄이 인용과 같다)
            out.append((t["entry"], "자리"))
        for v in dict.fromkeys(t["values"]):                                # 273~275줄
            if re.search(r"(?<!\d)(?<!\d\.)" + re.escape(v.replace(",", "")) + r"(?!\d)(?!\.\d)", flat):
                out.append((t["entry"], "값 " + v))
    return out


# --- 한 사실 -----------------------------------------------------------------
def check_fact(fact, groups, docs, doc_ids, records, targets, cache):
    group = groups[(fact["lang"], fact["side"], fact["group"])]
    ments = []
    for m in group["mentions"]:
        d = docs[m["doc"]]
        key = (d["lang"], str(d["revid"]))
        old_path = STEP3 / "md" / f"rare_earth_{d['lang']}_{d['revid']}.md"
        old_text = cache.setdefault(old_path, read_text(old_path))
        old_line = old_text.split("\n")[m["line"]]
        item = {"raw": m["raw"], "old_line": old_line}
        doc_id = doc_ids.get(key)
        if doc_id is None:
            item.update(status=MISSING, why="오늘 코퍼스에 같은 판의 문서가 없음", A=MISSING, B=MISSING)
            ments.append(item)
            continue
        new_path = MD_DIR / f"{doc_id}.md"
        new_text = cache.setdefault(new_path, read_text(new_path))
        line, off, how = locate(m, old_text, new_text)
        item["doc_id"] = doc_id
        if line is None:
            item.update(status=MISSING, why=how, A=MISSING, B=MISSING)
            ments.append(item)
            continue
        new_line = new_text.split("\n")[line - 1]
        slot = slot_of(records, doc_id, line, off)
        item.update(status="찾음", how=how, line=line, new_line=new_line, slot=slot["id"] if slot else NO_SLOT)
        hits_a = blocked_A(doc_id, line, slot, targets)
        hits_b = blocked_B(doc_id, new_line, targets)
        item["A"] = NO_SLOT if slot is None else (BLOCKED if hits_a else OK)
        item["A_entries"] = hits_a
        item["B"] = BLOCKED if hits_b else OK
        item["B_reasons"] = [f"항목 {n} {why}" for n, why in hits_b]
        ments.append(item)
    found = [m for m in ments if m["status"] == "찾음"]
    use_a = [m for m in found if m["A"] == OK]
    use_b = [m for m in found if m["B"] == OK]
    use_b_slot = [m for m in use_b if m["slot"] != NO_SLOT]
    return {
        "no": fact["no"], "source": fact["source"], "lang": fact["lang"], "side": fact["side"], "in_table": fact["in_table"], "note": fact["note"],
        "mentions": ments,
        "A": bool(use_a), "B": bool(use_b),
        "A_strict": bool(use_a) and not any(m["A"] == BLOCKED for m in found),
        "B_strict": bool(use_b) and len(use_b) == len(found),
        "B_only_without_slot": bool(use_b) and not use_b_slot,
    }


def run(conflicts_path, more_path=CONFIRM_MORE):
    groups, docs = old_groups()
    doc_ids = today_doc_ids()
    records = {}
    for r in json.loads(VALUES.read_text(encoding="utf-8")):
        records.setdefault((r["doc_id"], r["line"]), []).append(r)
    targets = load_conflicts(conflicts_path)
    cache = {}
    return [check_fact(f, groups, docs, doc_ids, records, targets, cache) for f in confirmed_facts(more_path)]


def summarize(results, lang):
    """언어 하나의 세기: 한 쪽에만 있는 확인된 사실에서 기준별로 쓸 수 있는 수와 그 가운데 표 수."""
    rows = [r for r in results if r["lang"] == lang and r["side"] == "one"]

    def count(key):
        sel = [r for r in rows if (key(r) if callable(key) else r[key])]
        return {"사실": len(sel), "표": sum(r["in_table"] for r in sel)}

    out = {"확인됨": count(lambda r: True), "A": count("A"), "B": count("B"), "confirm_more 출처": count(lambda r: r["source"] == SRC_MORE),
           "A 엄격": count("A_strict"), "B 엄격": count("B_strict"),
           "B만 자리 없이": count("B_only_without_slot")}
    for k in ("확인됨", "A", "B", "A 엄격", "B 엄격"):
        out[k]["기준"] = "충족" if out[k]["사실"] >= NEED_ONE and out[k]["표"] >= NEED_TABLE else "미달"
    return out


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_CONFLICTS
    results = run(path)
    summary = {lang: summarize(results, lang) for lang in ("ko", "en")}
    not_found = [{"no": r["no"], "raw": m["raw"], "old_line": m["old_line"], "why": m["why"]} for r in results for m in r["mentions"] if m["status"] == MISSING]
    no_slot = [{"no": r["no"], "raw": m["raw"], "doc_id": m["doc_id"], "line": m["line"], "new_line": m["new_line"]}
               for r in results for m in r["mentions"] if m["status"] == "찾음" and m["slot"] == NO_SLOT]
    OUT.write_text(json.dumps({"conflicts": str(path), "need": {"one": NEED_ONE, "table": NEED_TABLE}, "summary": summary,
                               "not_found": not_found, "no_slot": no_slot, "facts": results}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"부딪히는 값 목록: {path}")
    print(f"기준: 언어마다 한 쪽에만 있는 확인된 사실 {NEED_ONE}개 이상, 그 가운데 표 {NEED_TABLE}개 이상")
    for lang in ("ko", "en"):
        for name, v in summary[lang].items():
            print(f"{lang} {name}: 사실 {v['사실']}, 표 {v['표']}" + (f" -> {v['기준']}" if "기준" in v else ""))
    print(f"찾지 못한 언급 {len(not_found)}개")
    for x in not_found:
        print(f"  {x['no']} {x['raw']!r}: {x['why']} | {x['old_line']}")
    print(f"자리 없는 언급 {len(no_slot)}개")
    for x in no_slot:
        print(f"  {x['no']} {x['raw']!r}: {x['doc_id']} {x['line']}줄 | {x['new_line']}")
    print(f"쓴 파일: {OUT}")


if __name__ == "__main__":
    main(sys.argv)
