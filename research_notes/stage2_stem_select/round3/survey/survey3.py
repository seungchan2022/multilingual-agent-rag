"""새 후보 분야 여섯(decisions/stage2.md 2026-10-20 "새 후보 분야 여섯을 문서 측정부터 거른다")의 1 대상 조사.

  .venv/bin/python research_notes/stage2_stem_select/round3/survey/survey3.py

분야마다 한국어 위키백과 분류에서 하위 분류를 깊이만큼 따라가 본 이름공간(ns=0) 문서를 모으고, 영어 링크(langlinks en)가
있는 문서만 한국어 위키 글의 `| 칸 = 값` 줄에서 물을 값을 읽는다. 값 글자를 다섯 가지(하나/범위/여럿/어림/없음)로
가르는 clean, kind, 요청 함수 api, ko_texts, resolve는 field_survey/survey.py의 것을 경로에서 불러와 그대로 쓴다.
셈한 대상 = 영어 링크가 있고, 값 칸이 있고, kind가 `하나`이고, 단위를 기준 단위로 바꿀 수 있는 문서.
결과는 같은 폴더의 survey.json과 summary.md에 쓴다(위키 글은 넣지 않는다).

칸 이름 정규식은 아래 FIELDS에 있다. 정한 근거는 분야마다 영어 링크가 있는 문서의 정보 상자 칸 이름을 센 표(2026-10-20,
실행 전 탐색)다. 근거로 본 문서 이름은 각 칸 옆 주석에 적었다.
"""
import importlib.util, json, re, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).parent

_spec = importlib.util.spec_from_file_location(
    "field_survey", ROOT / "research_notes" / "stage2_stem_select" / "field_survey" / "survey.py")
fs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fs)  # fs.api, fs.resolve, fs.ko_texts, fs.clean, fs.kind (요청 사이에 GAP=2초 쉼, 묶어서 묻고 get으로 다시 한다)

# 단위 표: 소문자 단위 글자 -> 기준 단위로 곱할 값. 표에 없는 단위는 바꿀 수 없는 것으로 보고 셈에서 뺀다.
MASS = {"kg": 1, "㎏": 1, "g": 1e-3, "t": 1e3, "톤": 1e3, "킬로그램": 1, "그램": 1e-3, "lb": 0.45359237, "lbs": 0.45359237, "파운드": 0.45359237}
LEN_M = {"m": 1, "km": 1e3, "㎞": 1e3, "㎜": 1e-3, "cm": 1e-2, "mm": 1e-3, "미터": 1, "킬로미터": 1e3, "ft": 0.3048, "피트": 0.3048}
LEN_KM = {"km": 1, "㎞": 1, "m": 1e-3, "킬로미터": 1, "미터": 1e-3, "mi": 1.609344, "마일": 1.609344}
VOL = {"m3": 1, "m³": 1, "㎥": 1, "km3": 1e9, "hm3": 1e6}
MW = {"mw": 1, "mwe": 1, "kw": 1e-3, "gw": 1e3, "gwe": 1e3, "w": 1e-6}
KW = {"kw": 1, "mw": 1e3, "w": 1e-3, "hp": 0.745699872, "ps": 0.7354988}

# 분야: 분류, 깊이, 값(앞의 것부터). 값마다 (기준 단위, 단위 표, 칸 이름 정규식 목록(앞의 것이 먼저), 근거 문서)
FIELDS = {
    "한국의 인공위성": {
        "category": "분류:대한민국의 인공위성", "depth": 0,
        "values": {
            # 중량 18개(OSSI-1 "950g", 과학기술위성 1호). 질량 칸을 쓴 문서는 보지 못했지만 같은 뜻이라 뒤에 둔다
            "질량(kg)": ("kg", MASS, [r"^(중량|질량)$", r"^(발사\s*(중량|질량)|건조\s*(중량|질량))$"], "OSSI-1, 과학기술위성 1호"),
            # 궤도고도 5개(도요샛 "550km 태양동기궤도"). 근지점·원지점은 높이가 둘이라 이 값으로 세지 않는다
            "궤도 고도(km)": ("km", LEN_KM, [r"^궤도\s*고도$"], "도요샛"),
        },
    },
    "태양계 탐사선": {
        "category": "분류:태양계 탐사선", "depth": 1,
        "values": {
            # 중량 72개(EnVision "805kg")
            "질량(kg)": ("kg", MASS, [r"^(중량|질량)$", r"^(발사\s*(중량|질량)|건조\s*(중량|질량))$"], "EnVision"),
        },
    },
    "한국의 댐": {
        "category": "분류:대한민국의 댐", "depth": 1,
        "values": {
            # 영어 링크 있는 댐 문서의 칸 이름에 높이·길이 칸은 하나도 없었다(공산댐, 임하댐, 대청다목적댐). 이름은 흔한 꼴로 둔다
            "높이(m)": ("m", LEN_M, [r"^(댐\s*높이|제방\s*높이|높이)$"], "공산댐, 임하댐, 대청다목적댐(칸 없음)"),
            "길이(m)": ("m", LEN_M, [r"^(댐\s*길이|제방\s*길이|길이)$"], "공산댐, 임하댐, 대청다목적댐(칸 없음)"),
            # 총저수용량 4개(임하댐 "5억 9500만m3")
            "총저수용량(m3)": ("m3", VOL, [r"^총\s*저수\s*용량$"], "임하댐"),
        },
    },
    "한국의 교량": {
        "category": "분류:대한민국의 교량", "depth": 2,
        "values": {
            # 총길이 17개(올림픽대교 "1,770m"). 같은 문서에 길이 칸("1,225m")이 따로 있어 길이는 총길이로 세지 않는다. 참고로만 센다
            "총길이(m)": ("m", LEN_M, [r"^총\s*길이$"], "올림픽대교"),
            # 주경간 17개(울산대교 "1,150m")
            "주경간(m)": ("m", LEN_M, [r"^(주\s*경간|최대\s*경간(장)?)$"], "울산대교"),
            "길이(m, 참고)": ("m", LEN_M, [r"^길이$"], "올림픽대교(총길이와 다른 값이 함께 있음). 판정에는 쓰지 않는다"),
        },
        "reference_only": ["길이(m, 참고)"],
    },
    "한국의 원자력 발전소": {
        "category": "분류:대한민국의 원자력 발전소", "depth": 0,
        "values": {
            # 설비용량 3개(고리원자력발전소 "4,414", 단위 글자 없음)
            "설비 용량(MW)": ("MW", MW, [r"^(총\s*)?설비\s*용량$"], "고리원자력발전소"),
        },
    },
    "한국의 고속철도 차량": {
        "category": "분류:대한민국의 고속철도 차량", "depth": 1,
        "values": {
            # 편성길이 6개(EMU-370 "200,100", 단위 글자 없음)
            "편성 길이(m)": ("m", LEN_M, [r"^편성\s*길이$"], "EMU-370"),
            # 편성출력 3개(HEMU-430X "시제차 : 410 x 20 = 8,200 kW"). 전동기출력은 전동기 하나의 값이라 쓰지 않는다
            "출력(kW)": ("kW", KW, [r"^(편성\s*출력|출력)$"], "HEMU-430X"),
        },
    },
}

MIN_COUNT, GUESS_LIMIT, GUESS_BAND = 10, 0.2, 0.01  # 기준(바꾸지 않는다): 셈한 대상 10개 이상, 찍기 20% 이상이면 떨어짐, ±1%
KO_MULT = {"조": 1e12, "억": 1e8, "만": 1e4, "천": 1e3}


def category_docs(cat, depth):
    """분류의 본 이름공간 문서를 하위 분류 depth단계까지 따라가며 모은다(중복 제거, 처음 만난 차례)."""
    docs, todo, done = {}, [(cat, 0)], set()
    while todo:
        c, d = todo.pop(0)
        if c in done:
            continue
        done.add(c)
        cont = {}
        while True:
            q = fs.api("ko.wikipedia.org", {"action": "query", "list": "categorymembers", "cmtitle": c,
                                            "cmlimit": "max", "cmtype": "page|subcat", **cont})
            for m in q["query"]["categorymembers"]:
                if m["ns"] == 0:
                    docs.setdefault(m["title"], None)
                elif m["ns"] == 14 and d < depth:
                    todo.append((m["title"], d + 1))
            if "continue" not in q:
                break
            cont = q["continue"]
    return list(docs)


def en_links(titles):
    """한국어 제목 -> 영어 제목(없으면 None). 50개씩 묶어 묻는다."""
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        q = fs.api("ko.wikipedia.org", {"action": "query", "titles": "|".join(chunk), "prop": "langlinks",
                                        "lllang": "en", "lllimit": "max", "redirects": 1})["query"]
        pages = {p["title"]: p for p in q["pages"]}
        for t in chunk:
            ll = (pages.get(fs.resolve(q, t)) or {}).get("langlinks", [])
            out[t] = ll[0]["title"] if ll else None
    return out


def find_cell(text, patterns):
    """위키 글의 '| 칸 = 값' 줄에서 정규식이 앞선 것부터, 같은 정규식이면 글에서 먼저 나온 비어 있지 않은 값 칸의 (칸 이름, 정리한 글자)."""
    cells = []
    for line in text.splitlines():
        m = re.match(r"\s*\|\s*([^=]{1,40}?)\s*=\s*(.*)$", line)
        if m and m.group(2).strip():
            cells.append((re.sub(r"\[\[|\]\]", "", m.group(1)).strip(), m.group(2)))
    for pat in patterns:
        for name, raw in cells:
            if re.search(pat, name):
                return name, fs.clean(raw)
    return None, ""


def parse_number(s):
    """값 글자의 첫 수와 그 뒤 단위 글자. 억·만·천 같은 우리말 자릿수와 ×10^n을 풀고, 읽을 수 없으면 (None, "")."""
    m = re.match(r"\D*?(\d[\d,]*\.?\d*|\.\d+)(.*)$", s)
    if not m:
        return None, ""
    num, rest = float(m.group(1).replace(",", "")), m.group(2)
    total, cur = 0.0, num
    while True:
        k = re.match(r"\s*(조|억|만|천)(.*)$", rest)
        if not k:
            break
        total += cur * KO_MULT[k.group(1)]
        rest, cur = k.group(2), None
        n = re.match(r"\s*(\d[\d,]*\.?\d*)(.*)$", rest)
        if not n:
            break
        cur, rest = float(n.group(1).replace(",", "")), n.group(2)
    if cur is not None:
        total += cur
    e = re.match(r"\s*[×x]\s*10\^?([-−]?\d+)(.*)$", rest)
    if e:
        total *= 10 ** int(e.group(1).replace("−", "-"))
        rest = e.group(2)
    u = re.match(r"\s*([A-Za-zµμ㎏㎥㎞㎜]+[\d³²]?|[가-힣]+)", rest)
    return total, (u.group(1) if u else "")


def measure(raw_text, base, table):
    """값 글자 하나 -> 대상 기록 일부. 하나가 아니면 숫자와 단위를 읽지 않는다."""
    k = fs.kind(raw_text)
    rec = {"raw": raw_text[:80], "kind": k, "number": None, "unit": None, "base_value": None, "unit_assumed": False, "excluded": None}
    if k != "하나":
        return rec
    num, unit = parse_number(raw_text)
    rec["number"], rec["unit"] = num, unit
    if num is None:
        rec["excluded"] = "숫자를 읽지 못함"
    elif unit == "":
        rec["base_value"], rec["unit_assumed"] = num, True  # 단위 글자가 없으면 기준 단위로 본다(판정 한계에 적는다)
    elif unit.lower() in table:
        rec["base_value"] = num * table[unit.lower()]
    else:
        rec["excluded"] = f"바꿀 수 없는 단위 '{unit}'"
    return rec


def guess_check(vals):
    """셈한 대상의 값 가운데 하나 v를 골라 모두 v라 답할 때 v의 ±1% 안에 드는 대상 수의 최댓값과 그 v(같으면 작은 v)."""
    best_n, best_v = 0, None
    for v in sorted(set(vals)):
        n = sum(1 for x in vals if abs(x - v) <= GUESS_BAND * abs(v))
        if n > best_n:
            best_n, best_v = n, v
    return best_n, best_v


def main():
    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {"fetched_utc": fetched, "criteria": {"min_count": MIN_COUNT, "guess_limit": GUESS_LIMIT, "guess_band": GUESS_BAND},
              "fields": {}}
    for field, spec in FIELDS.items():
        titles = category_docs(spec["category"], spec["depth"])
        links = en_links(titles)
        linked = [t for t in titles if links[t]]
        texts = fs.ko_texts(linked) if linked else {}
        out = {"category": spec["category"], "depth": spec["depth"], "docs_total": len(titles),
               "docs_en_linked": len(linked), "docs": [{"ko": t, "en": links[t]} for t in titles], "values": {}}
        chosen = None
        for vname, (base, table, pats, basis) in spec["values"].items():
            ref = vname in spec.get("reference_only", [])
            targets = []
            for t in linked:
                cell, raw_text = find_cell(texts[t][1], pats)
                rec = {"title": t, "cell": cell, **measure(raw_text, base, table)}
                targets.append(rec)
            counted = [r for r in targets if r["base_value"] is not None and r["kind"] == "하나"]
            n = len(counted)
            gn, gv = guess_check([r["base_value"] for r in counted])
            ratio = gn / n if n else None
            guessed = ratio is not None and ratio >= GUESS_LIMIT
            ok = n >= MIN_COUNT and not guessed
            out["values"][vname] = {
                "base_unit": base, "patterns": pats, "basis_docs": basis, "reference_only": ref,
                "kind_counts": {k: sum(1 for r in targets if r["kind"] == k) for k in ("하나", "범위", "여럿", "어림", "없음")},
                "excluded": [{"title": r["title"], "reason": r["excluded"]} for r in targets if r["excluded"]],
                "counted": n, "guess_max": gn, "guess_v": gv, "guess_ratio": ratio, "guessed": guessed, "passes": ok and not ref,
                "targets": targets,
            }
            if ok and not ref and chosen is None:
                chosen = vname
        out["chosen_value"] = chosen
        out["verdict"] = "통과" if chosen else "탈락"
        out["fail_reason"] = None if chosen else "값마다: " + "; ".join(
            f"{v} 셈 {d['counted']}개" + (f", 찍기 {d['guess_max']}/{d['counted']}" if d["counted"] else "")
            + (" (10개 미만)" if d["counted"] < MIN_COUNT else " (찍기로 떨어짐)")
            for v, d in out["values"].items() if not d["reference_only"])
        report["fields"][field] = out
        print(field, "문서", len(titles), "영어 링크", len(linked), {v: d["counted"] for v, d in out["values"].items()}, out["verdict"], flush=True)
    (HERE / "survey.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    write_summary(report)
    print("저장:", (HERE / "survey.json").relative_to(ROOT))


def write_summary(report):
    L = [f"# 새 후보 분야 대상 조사 요약 (받은 때 {report['fetched_utc']} UTC)", "",
         "`survey3.py`가 `survey.json`에서 계산한 값이다. 기준: 셈한 대상 10개 이상, 찍기 최댓값/셈한 대상 0.2 미만, 모두 v라 답할 때 v의 ±1%.",
         "찍기 최댓값 칸은 `대상 수 (v)`, 비율은 최댓값/셈한 대상이다. 참고만 하는 값(판정에 안 쓴 값)은 `*`로 표시했다.", "",
         "| 분야 | 분류(깊이) | 모은 문서 | 영어 링크 있음 | 값 | 셈한 대상 | 찍기 최댓값 (v) | 비율 | 값 판정 | 분야 판정 | 정한 값 |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for f, o in report["fields"].items():
        first = True
        for v, d in o["values"].items():
            if d["reference_only"]:
                vp = "참고"
            elif d["counted"] < MIN_COUNT:
                vp = "10개 미만"
            elif d["guessed"]:
                vp = "찍기로 떨어짐"
            else:
                vp = "통과"
            gm = f"{d['guess_max']} ({d['guess_v']:g})" if d["counted"] else "-"
            ra = f"{d['guess_ratio']:.2f}" if d["counted"] else "-"
            L.append("| " + " | ".join([
                f if first else "", f"{o['category']} ({o['depth']})" if first else "",
                str(o["docs_total"]) if first else "", str(o["docs_en_linked"]) if first else "",
                v + ("*" if d["reference_only"] else ""), str(d["counted"]), gm, ra, vp,
                o["verdict"] if first else "", (o["chosen_value"] or "-") if first else ""]) + " |")
            first = False
    L += ["", "## 탈락 이유", ""]
    L += [f"- {f}: {o['fail_reason']}" for f, o in report["fields"].items() if o["fail_reason"]] or ["- 없음"]
    L += ["", "## 값마다 kind 분포(영어 링크 있는 문서 기준)와 셈에서 뺀 대상", "",
          "| 분야 | 값 | 하나 | 범위 | 여럿 | 어림 | 없음 | 단위 때문에 뺌 | 단위 글자 없어 기준 단위로 본 대상 |", "|---|---|---|---|---|---|---|---|---|"]
    for f, o in report["fields"].items():
        for v, d in o["values"].items():
            k = d["kind_counts"]
            assumed = sum(1 for r in d["targets"] if r["unit_assumed"] and r["base_value"] is not None)
            L.append(f"| {f} | {v} | {k['하나']} | {k['범위']} | {k['여럿']} | {k['어림']} | {k['없음']} | {len(d['excluded'])} | {assumed} |")
    ex = [(f, v, e) for f, o in report["fields"].items() for v, d in o["values"].items() for e in d["excluded"]]
    if ex:
        L += ["", "셈에서 뺀 대상(단위를 바꿀 수 없음):", ""] + [f"- {f} / {v}: {e['title']} ({e['reason']})" for f, v, e in ex]
    L += ["", "## 칸 이름 정규식과 근거", "",
          "정보 상자 칸 이름은 영어 링크가 있는 문서의 위키 글에서 `| 칸 = 값` 줄의 칸 이름을 센 표를 보고 정했다(2026-10-20, 실행 전). "
          "정규식이 여럿이면 앞의 것부터 찾고, 같은 정규식이면 글에서 먼저 나온 비어 있지 않은 칸을 쓴다.", "",
          "| 분야 | 값 | 칸 이름 정규식 | 근거 문서 |", "|---|---|---|---|"]
    for f, o in report["fields"].items():
        for v, d in o["values"].items():
            pats = ", ".join("`" + p.replace("|", "\\|") + "`" for p in d["patterns"])  # 표 칸 안의 |는 \|로 쓴다
            L.append(f"| {f} | {v} | {pats} | {d['basis_docs']} |")
    L += ["", "## 한계", "",
          "- 값 칸을 정보 상자에 한정하지 않고 위키 글의 `| 칸 = 값` 줄 어디서든 찾는다(field_survey/survey.py와 같은 방식).",
          "- 단위 글자가 없는 값은 기준 단위로 보았다(`단위 글자 없어 기준 단위로 본 대상`). 실제 단위가 다를 수 있다.",
          "- 값 글자에서 첫 수와 그 바로 뒤 글자를 단위로 읽는다. 괄호 안의 다른 단위 값은 보지 않는다.",
          "- 본문 길이와 표의 수는 세지 않았다(뒤 단계)."]
    (HERE / "summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
