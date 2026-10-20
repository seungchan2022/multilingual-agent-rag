"""새 후보 분야(한국의 인공위성, 태양계 탐사선)의 4 문서 측정(decisions/stage2.md 2026-10-20 "새 후보 분야 여섯을 문서 측정부터 거른다"의 4와
"4 문서 측정에 선 4를 더한다" 줄)을 하는 프로그램.

  .venv/bin/python src/domain_select/round3_measure.py targets   네트워크 없이 대상 20개를 출력한다
  .venv/bin/python src/domain_select/round3_measure.py fetch     한국어(고정한 판)·영어(2에서 남긴 판) HTML을 받고 영어는 마크다운도 만든다
  .venv/bin/python src/domain_select/round3_measure.py count     선 1~4의 원자료를 results.json에 쓴다
  .venv/bin/python src/domain_select/round3_measure.py summary   results.json으로 summary.md를 쓴다

선 1~3은 stepper_check.py와 같은 규칙(research_notes/stage2_domain_survey/measure.py의 measure(html))이다.
선 4는 한 문서에서 단위가 붙은 숫자를 뽑아 반대 언어 문서에 없는 것만 센다.
"""
import json
import re
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stepper_check as sc  # noqa: E402  measure, api(UA·쉬기·429 다시 해 보기)를 그대로 쓴다
from moons_check import infobox_lines  # noqa: E402
from fetch_docs import to_markdown  # noqa: E402  한국어 md/를 만든 변환

ROOT = sc.ROOT
ROUND3 = ROOT / "research_notes" / "stage2_stem_select" / "round3"
OUT = ROUND3 / "measure"
DOMAINS = ("kr_satellites", "probes")
LINE1_MIN = 5000      # 선 1: 본문 길이 중앙값(한국어, 영어 각각)
TABLE_DOCS_MIN = 4    # 선 2·3: 표 있는 문서 수
ONLY_MIN = 36         # 선 4: 그 언어에만 있는 숫자 수(분야의 대상 10개 합, 한국어·영어 각각)
TOL = 0.01            # 같은 값으로 보는 허용 오차(±1%)

# 단위 표: 표기 -> (차원, 그 차원 기준 단위로 바꾸는 곱). 기준 단위: 길이 m, 질량 kg, 시간 s, 속도 m/s, 넓이 m², 부피 m³,
# 출력 W, 에너지 J, 온도 K(섭씨는 +273.15를 따로 더함), 각도 °.
UNITS = {}


def _add(dim, factor, *names):
    for n in names:
        UNITS[n] = (dim, factor)


_add("길이", 1e-3, "mm", "㎜")
_add("길이", 1e-2, "cm", "㎝")
_add("길이", 1.0, "m")
_add("길이", 1e3, "km", "Km", "KM", "㎞")
_add("길이", 0.3048, "ft")
_add("길이", 1609.344, "mi")
_add("길이", 1.495978707e11, "AU", "au")
_add("길이", 9.4607304725808e15, "광년", "light-years", "light-year", "light years", "light year")
_add("질량", 1e-3, "g")
_add("질량", 1.0, "kg", "Kg", "KG", "㎏")
_add("질량", 1e3, "t", "톤")
_add("질량", 0.45359237, "lb")
_add("시간", 1.0, "초", "s")
_add("시간", 60.0, "분", "min")
_add("시간", 3600.0, "시간", "h", "hr")
_add("시간", 86400.0, "일", "d", "days", "day")
_add("시간", 2629746.0, "개월", "months", "month")           # 1개월 = 30.4375일
_add("시간", 31557600.0, "년", "yr", "years", "year")        # 1년 = 365.25일
_add("속도", 1000 / 3600, "km/h")
_add("속도", 1.0, "m/s")
_add("속도", 1000.0, "km/s")
_add("넓이", 1.0, "m²", "㎡", "m2")
_add("넓이", 1e6, "km²", "㎢", "km2")
_add("부피", 1.0, "m³", "㎥", "m3")
_add("부피", 1e-3, "L")
_add("출력", 1.0, "W")
_add("출력", 1e3, "kW", "㎾")
_add("출력", 1e6, "MW", "㎿")
_add("출력", 1e9, "GW")
_add("에너지", 3600.0, "Wh")
_add("에너지", 3.6e6, "kWh")
_add("온도", 1.0, "°C", "℃", "K")
_add("각도", 1.0, "°")
CELSIUS = {"°C", "℃"}

_UNIT_RE = "|".join(re.escape(u) for u in sorted(UNITS, key=len, reverse=True))
NUM = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"
# 숫자 앞은 영문자·숫자·점이 아니어야 하고(제22호, KITSAT-1이 아니라 앞이 한글이면 받는다), 숫자 뒤 0~1칸 공백 다음 단위가 온다.
UNIT_NUM = re.compile(rf"(?<![A-Za-z0-9_.])(?<!\d,)(?P<num>{NUM})(?P<sp>[    ]?)(?P<unit>{_UNIT_RE})")
SPACE_GROUP = re.compile(r"\d{1,3}(?:[   ]\d{3})+")
COMMA_GROUP = re.compile(r"\d{1,3}(?:,\d{3})+")
TOKEN = re.compile(r"(?<![\d.])\d+(?:\.\d+)?")


def to_base(value, unit):
    dim, f = UNITS[unit]
    v = value * f
    if unit in CELSIUS:
        v += 273.15
    return dim, v


def _skip(text, m):
    """연도·날짜·세대 표현처럼 단위가 붙은 값이 아닌 것."""
    num, unit, sp = m.group("num"), m.group("unit"), m.group("sp")
    end = m.end()
    nxt = text[end:end + 1]
    # 영어 단위(알파벳으로 끝남)는 뒤에 영문자가 더 붙으면 다른 낱말이다(5 mi|llion, 5 to).
    if unit[-1].isascii() and unit[-1].isalpha() and nxt.isascii() and nxt.isalpha():
        return True
    if unit in ("년", "year", "years", "yr") and re.fullmatch(r"\d{4}", num) and 1000 <= int(num) <= 2100:
        return True
    if unit == "s" and not sp and re.fullmatch(r"\d{4}", num) and 1000 <= int(num) <= 2100:   # 1990s
        return True
    if unit == "년" and nxt == "대":      # 60년대
        return True
    if unit == "분" and nxt == "기":      # 3분기
        return True
    if unit == "일":
        before = text[max(0, m.start() - 3):m.start()]
        if re.search(r"월\s*$", before):  # 8월 11일
            return True
    if unit == "K" and nxt in ("B", "b", "i"):     # KB, Kbps
        return True
    return False


def extract(text):
    """글에서 단위가 붙은 숫자를 모두 뽑는다. [{raw, digits, value, unit, dim, base}]"""
    out = []
    for m in UNIT_NUM.finditer(text):
        if _skip(text, m):
            continue
        digits = m.group("num").replace(",", "")
        unit = m.group("unit")
        value = float(digits)
        dim, base = to_base(value, unit)
        out.append({"raw": m.group(0), "digits": digits, "value": value, "unit": unit, "dim": dim, "base": base})
    return out


def close(a, b, tol=TOL):
    """두 기준 단위 값이 ±1% 안인가(큰 쪽의 1%). 둘 다 0이면 같다."""
    return abs(a - b) <= tol * max(abs(a), abs(b))


def dedupe(items):
    """같은 차원에서 기준 값이 ±1% 안인 것을 한 값으로 묶는다. [{...대표 항목, mentions:[raw...]}]"""
    groups = []
    for it in sorted(items, key=lambda i: (i["dim"], i["base"])):
        for g in groups:
            if g["dim"] == it["dim"] and close(g["base"], it["base"]):
                g["mentions"].append(it["raw"])
                g["digits_all"].append(it["digits"])
                break
        else:
            groups.append({**it, "mentions": [it["raw"]], "digits_all": [it["digits"]]})
    return groups


def number_tokens(text):
    """반대 언어 글의 숫자 글자들. 쉼표·좁은 공백 자리를 지운 뒤 소수점이 붙은 한 덩어리를 한 글자로 본다."""
    t = SPACE_GROUP.sub(lambda m: re.sub(r"[   ]", "", m.group(0)), text)
    t = COMMA_GROUP.sub(lambda m: m.group(0).replace(",", ""), t)
    return set(TOKEN.findall(t))


def find_in_other(group, other_tokens, other_items):
    """그룹이 반대 언어 문서에 있는가. (이유, 찾은 글자) 또는 None. (a) 같은 숫자 글자, (b) 같은 차원 ±1%."""
    for d in group["digits_all"]:
        if d in other_tokens:
            return {"reason": "a", "found": d}
    for o in other_items:
        if o["dim"] == group["dim"] and close(o["base"], group["base"]):
            return {"reason": "b", "found": o["raw"]}
    return None


def only_numbers(text, other_text):
    """text에 있고 other_text에 없는 숫자. 돌려주는 값: 모든 항목(이유 포함) 목록."""
    groups = dedupe(extract(text))
    tokens = number_tokens(other_text)
    other_items = extract(other_text)
    res = []
    for g in groups:
        hit = find_in_other(g, tokens, other_items)
        res.append({"raw": g["raw"], "mentions": g["mentions"], "value": g["value"], "unit": g["unit"], "dim": g["dim"],
                    "base": g["base"], "other_lang": hit if hit else "그 언어에만"})
    return res


def md_infobox_count(md):
    """마크다운 제목 아래 첫 덩어리에서 '- 이름: 값' 줄(들여쓴 줄 포함)의 수(정보 상자가 마크다운에 들어 있는지 본다)."""
    lines = md.split("\n")
    n, started = 0, False
    for ln in lines[1:]:
        if ln.lstrip().startswith("- "):
            started = True
            if ": " in ln:
                n += 1
        elif started and not ln.strip():
            break
    return n


# --- 대상 불러오기 ------------------------------------------------------

def load_targets():
    rows, missing = [], []
    for dom in DOMAINS:
        base = ROUND3 / dom
        qs = json.loads((base / "questions.json").read_text(encoding="utf-8"))
        docs = json.loads((base / "docs.json").read_text(encoding="utf-8"))
        for q in qs:
            title = q["evidence_quotes"][0]["doc"]
            ec = q.get("en_check") or {}
            revid = (docs.get(title) or {}).get("revid")
            if not revid or not ec.get("en_revid") or not ec.get("en_title"):
                missing.append(f"{dom} {q['target']}")
            rows.append({"domain": dom, "id": q["id"], "target": q["target"], "ko_title": title, "ko_revid": revid,
                         "en_title": ec.get("en_title"), "en_revid": ec.get("en_revid")})
    if missing:
        raise SystemExit("대상을 맞추지 못했다: " + ", ".join(missing))
    return rows


def cmd_targets():
    for r in load_targets():
        print(f"{r['domain']} | {r['id']} | {r['target']} | {r['ko_title']} | {r['ko_revid']} | {r['en_title']} | {r['en_revid']}")


def paths(r):
    c = OUT / "cache" / r["domain"]
    return {"ko_html": c / f"ko_{r['ko_revid']}.html", "en_html": c / f"en_{r['en_revid']}.html",
            "en_md": c / f"en_{r['en_revid']}.md",
            "ko_md": ROUND3 / r["domain"] / "md" / f"{r['ko_title']}.md"}


def cmd_fetch():
    rows = load_targets()
    log = OUT / "fetched.jsonl"
    for r in rows:
        p = paths(r)
        p["ko_html"].parent.mkdir(parents=True, exist_ok=True)
        for lang, rev, title in (("ko", r["ko_revid"], r["ko_title"]), ("en", r["en_revid"], r["en_title"])):
            f = p[f"{lang}_html"]
            if not f.exists():
                d = sc.api(lang, action="parse", oldid=rev, prop="text|revid|displaytitle")
                if "parse" not in d:
                    raise RuntimeError(f"{r['domain']} {r['target']} {lang}: {d.get('error')}")
                assert d["parse"]["revid"] == rev, (r["target"], lang)
                f.write_text(d["parse"]["text"], encoding="utf-8")
                rec = {"domain": r["domain"], "target": r["target"], "lang": lang, "title": d["parse"]["title"], "revid": rev,
                       "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
                with log.open("a", encoding="utf-8") as lf:
                    lf.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f"{r['domain']} | {r['target']} | {lang} | {rev}", flush=True)
        if not p["en_md"].exists():
            p["en_md"].write_text(to_markdown(r["en_title"], p["en_html"].read_bytes()), encoding="utf-8")


# --- 세기 ------------------------------------------------------------

def count_doc(r, lang, other_lang, p, other_md_text):
    html = p[f"{lang}_html"].read_text(encoding="utf-8")
    md = p[f"{lang}_md"].read_text(encoding="utf-8")
    m = sc.measure(html)
    nums = only_numbers(md, other_md_text)
    return {"domain": r["domain"], "id": r["id"], "target": r["target"], "lang": lang,
            "title": r["ko_title"] if lang == "ko" else r["en_title"],
            "revid": r["ko_revid"] if lang == "ko" else r["en_revid"],
            "chars": m["chars"], "table_count": len(m["tables"]),
            "infobox_lines": len(infobox_lines(html)), "md_infobox_lines": md_infobox_count(md),
            "numbers": nums, "only_count": sum(1 for n in nums if n["other_lang"] == "그 언어에만")}


def cmd_count():
    rows = []
    for r in load_targets():
        p = paths(r)
        ko_md = p["ko_md"].read_text(encoding="utf-8")
        en_md = p["en_md"].read_text(encoding="utf-8")
        rows.append(count_doc(r, "ko", "en", p, en_md))
        rows.append(count_doc(r, "en", "ko", p, ko_md))
    (OUT / "results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("센 문서", len(rows))


# --- 선 판정과 summary ---------------------------------------------------

def summarize(rows):
    out = []
    for dom in DOMAINS:
        rs = [r for r in rows if r["domain"] == dom]
        if not rs:
            continue
        ko = [r for r in rs if r["lang"] == "ko"]
        en = [r for r in rs if r["lang"] == "en"]
        med = lambda l: int(statistics.median([r["chars"] for r in l])) if l else 0
        s = {"domain": dom, "ko_docs": len(ko), "en_docs": len(en), "ko_median": med(ko), "en_median": med(en),
             "ko_tables": sum(1 for r in ko if r["table_count"] >= 1), "en_tables": sum(1 for r in en if r["table_count"] >= 1),
             "ko_only": sum(r["only_count"] for r in ko), "en_only": sum(r["only_count"] for r in en),
             "ko_infobox": sum(r["infobox_lines"] for r in ko), "en_infobox": sum(r["infobox_lines"] for r in en)}
        s["line1"] = s["ko_median"] >= LINE1_MIN and s["en_median"] >= LINE1_MIN
        s["line2"] = s["en_tables"] >= TABLE_DOCS_MIN
        s["line3"] = s["ko_tables"] >= TABLE_DOCS_MIN
        s["line4"] = s["ko_only"] >= ONLY_MIN and s["en_only"] >= ONLY_MIN
        s["passed"] = s["line1"] and s["line2"] and s["line3"] and s["line4"]
        out.append(s)
    return out


def render(summ, rows):
    yn = lambda v: "넘음" if v else "못 넘음"
    L = ["# 새 후보 분야 4 문서 측정 (선 1~4)", "",
         "| 분야 | 선 1 한국어 중앙값 | 선 1 영어 중앙값 | 선 2 표 있는 영어 문서 | 선 3 표 있는 한국어 문서 | 선 4 한국어에만 있는 숫자 | 선 4 영어에만 있는 숫자 | "
         "정보 상자 줄(한국어, 기록) | 정보 상자 줄(영어, 기록) | 선 1 | 선 2 | 선 3 | 선 4 | 분야 판정 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in summ:
        L.append(f"| {s['domain']} | {s['ko_median']:,} | {s['en_median']:,} | {s['en_tables']}/{s['en_docs']} | {s['ko_tables']}/{s['ko_docs']} | "
                 f"{s['ko_only']} | {s['en_only']} | {s['ko_infobox']} | {s['en_infobox']} | {yn(s['line1'])} | {yn(s['line2'])} | "
                 f"{yn(s['line3'])} | {yn(s['line4'])} | {'통과' if s['passed'] else '탈락'} |")
    L += ["", f"선 1: 한국어·영어 본문 길이(measure의 chars) 중앙값이 각각 {LINE1_MIN:,} 이상. 선 2: 표 있는 영어 문서 {TABLE_DOCS_MIN}/10 이상. "
          f"선 3: 표 있는 한국어 문서 {TABLE_DOCS_MIN}/10 이상. 선 4: 그 언어에만 있는 숫자가 한국어·영어 각각 {ONLY_MIN} 이상. "
          "정보 상자 줄은 기록만 하며 거르는 데 쓰지 않는다. 분야 판정: 선 넷을 모두 넘어야 통과.", ""]
    for s in summ:
        L += [f"## {s['domain']} 대상별", "",
              "| 대상 | 한국어 본문 | 영어 본문 | 한국어 표 | 영어 표 | 한국어에만 있는 숫자 | 영어에만 있는 숫자 |", "|---|---|---|---|---|---|---|"]
        for ko in [r for r in rows if r["domain"] == s["domain"] and r["lang"] == "ko"]:
            en = next(r for r in rows if r["domain"] == ko["domain"] and r["id"] == ko["id"] and r["lang"] == "en")
            L.append(f"| {ko['id']} {ko['target']} | {ko['chars']:,} | {en['chars']:,} | {ko['table_count']} | {en['table_count']} | "
                     f"{ko['only_count']} | {en['only_count']} |")
        L.append("")
    return "\n".join(L)


def cmd_summary():
    rows = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
    text = render(summarize(rows), rows)
    (OUT / "summary.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    fn = {"targets": cmd_targets, "fetch": cmd_fetch, "count": cmd_count, "summary": cmd_summary}.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if not fn:
        raise SystemExit(__doc__)
    fn()
