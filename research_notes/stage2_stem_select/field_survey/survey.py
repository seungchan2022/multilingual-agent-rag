"""새 분야 후보(이슈 #6)마다 대상의 한국어·영어 위키백과 문서가 있는지와, 한국어 문서의 정보 상자에
짧은 시험으로 물을 값이 숫자 하나로 적혀 있는지를 센다.

  .venv/bin/python research_notes/stage2_stem_select/field_survey/survey.py

영어 제목으로 영어 위키백과에서 한국어 링크(langlinks)를 찾고, 한국어 문서의 위키 글(원소는 `틀:원소 정보/이름`)에서
값 칸을 읽는다. 값은 다섯 가지로 가른다: 하나(± 오차는 하나로 친다), 범위("113-115"), 여럿("572.6×557.2×446.4",
쌍성의 "0.70/0.63", 줄을 바꿔 적은 두 값), 어림("약", "~", "≥", ">"), 없음. 줄을 바꿔 같은 값을 다른 단위로 한 번 더 적은
것("284.12년 / (103,774 일)")도 여럿에 들어, 하나는 실제보다 적게 셀 수 있다.
결과는 같은 폴더의 survey.json에 쓴다(위키 글은 넣지 않는다).
요청은 제목을 묶어 보내고, 코퍼스 프로그램의 get(쉬기·다시 하기)을 쓴다.
"""
import json, re, sys, time, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src" / "corpus"))
from fetch import UA, GAP, get  # noqa: E402

OUT = Path(__file__).with_name("survey.json")

# 분야마다: 영어 제목, 물을 값(이름: 칸 이름 정규식), 원소 정보 틀을 읽는지
FIELDS = {
    "덜 알려진 위성": {
        "titles": ["Miranda (moon)", "Ariel (moon)", "Umbriel", "Titania (moon)", "Oberon (moon)", "Proteus (moon)",
                   "Nereid (moon)", "Hyperion (moon)", "Phoebe (moon)", "Iapetus (moon)", "Rhea (moon)",
                   "Dione (moon)", "Tethys (moon)", "Mimas (moon)", "Amalthea (moon)", "Himalia (moon)",
                   "Charon (moon)", "Larissa (moon)"],
        "values": {"공전 주기": r"^공전\s*주기$", "긴반지름": r"^긴반지름$", "반지름": r"^반지름$"},
    },
    "왜행성·소행성": {
        "titles": ["Ceres (dwarf planet)", "4 Vesta", "2 Pallas", "10 Hygiea", "Haumea", "Makemake",
                   "Eris (dwarf planet)", "90377 Sedna", "50000 Quaoar", "90482 Orcus", "25143 Itokawa",
                   "162173 Ryugu", "101955 Bennu", "433 Eros", "951 Gaspra", "243 Ida", "16 Psyche", "99942 Apophis",
                   "3 Juno", "225088 Gonggong"],
        "values": {"긴반지름": r"^(긴반지름|궤도장반경)$", "공전 주기": r"^공전\s*주기$", "지름": r"^(지름|평균 지름)$"},
    },
    "가까운 항성": {
        "titles": ["Proxima Centauri", "Barnard's Star", "Wolf 359", "Lalande 21185", "Luyten 726-8", "Ross 154",
                   "Epsilon Eridani", "Lacaille 9352", "Ross 128", "61 Cygni", "Procyon", "Groombridge 34",
                   "Epsilon Indi", "Tau Ceti", "Gliese 1061", "Luyten's Star", "Teegarden's Star", "Kapteyn's Star",
                   "Van Maanen's Star", "Altair", "Vega", "Fomalhaut"],
        "values": {"질량": r"^질량$", "표면온도": r"^표면온도$", "반지름": r"^반지름$"},
    },
    "외계 행성": {
        "titles": ["Kepler-22b", "Gliese 581c", "TRAPPIST-1e", "Proxima Centauri b", "HD 209458 b", "51 Pegasi b",
                   "Kepler-452b", "Ross 128 b", "Kepler-186f", "Gliese 667 Cc", "WASP-12b", "HD 189733 b",
                   "Kepler-16b", "55 Cancri e", "Teegarden's Star b", "LHS 1140 b", "K2-18b", "Kepler-62f",
                   "Gliese 581d", "Gliese 581g", "Gliese 876 b", "Kepler-10b", "CoRoT-7b", "Fomalhaut b", "HR 8799 b",
                   "Beta Pictoris b", "Gliese 436 b", "TRAPPIST-1b", "Kepler-69c", "Kepler-62e",
                   "Upsilon Andromedae b", "Tau Boötis b", "47 Ursae Majoris b", "HD 80606 b", "Gliese 1214 b",
                   "KELT-9b"],
        "values": {"공전주기": r"^공전\s*주기$", "평균거리": r"^평균거리$"},
    },
    "혜성": {
        "titles": ["2P/Encke", "55P/Tempel–Tuttle", "109P/Swift–Tuttle", "17P/Holmes", "103P/Hartley",
                   "67P/Churyumov–Gerasimenko", "81P/Wild", "9P/Tempel", "19P/Borrelly", "3D/Biela",
                   "21P/Giacobini–Zinner", "29P/Schwassmann–Wachmann", "73P/Schwassmann–Wachmann", "46P/Wirtanen",
                   "45P/Honda–Mrkos–Pajdušáková", "12P/Pons–Brooks", "13P/Olbers", "26P/Grigg–Skjellerup",
                   "Comet Hale–Bopp", "Comet Hyakutake", "Comet Shoemaker–Levy 9", "Comet McNaught", "Comet West",
                   "Comet Ikeya–Seki", "C/2020 F3 (NEOWISE)", "C/2013 A1 (Siding Spring)", "Comet ISON",
                   "C/2011 W3 (Lovejoy)", "C/2023 A3 (Tsuchinshan–ATLAS)", "Comet Kohoutek", "Comet Arend–Roland",
                   "Great Comet of 1811", "Comet Bennett", "C/2011 L4 (PANSTARRS)", "96P/Machholz", "8P/Tuttle",
                   "15P/Finlay", "41P/Tuttle–Giacobini–Kresák"],
        "values": {"근일점": r"^(근일점|perihelion)$", "공전 주기": r"^(공전\s*주기|period)$",
                   "이심률": r"^(이심률|궤도 이심률|eccentricity)$"},
    },
    "희토류 원소": {
        "titles": ["Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Samarium", "Europium",
                   "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium",
                   "Scandium", "Yttrium"],
        "values": {"밀도": r"^밀도센티$", "녹는점": r"^녹는점K$"},
        "element": True,
    },
    "유기 화합물": {
        "titles": ["Benzoic acid", "Acetanilide", "Naphthalene", "Phenol", "Aniline", "Toluene", "Ethylene glycol",
                   "Glycerol", "Salicylic acid", "Urea", "Succinic acid", "Oxalic acid", "Citric acid",
                   "Acetophenone", "Benzaldehyde", "Nitrobenzene", "Cyclohexane", "Anthracene", "Pyridine",
                   "Resorcinol"],
        "values": {"밀도": r"^Density$", "끓는점": r"^BoilingPtC$", "녹는점": r"^MeltingPtC$"},
    },
    "방사성 동위원소": {
        "titles": ["Caesium-137", "Strontium-90", "Iodine-131", "Cobalt-60", "Carbon-14", "Plutonium-239",
                   "Radon-222", "Radium-226", "Tritium", "Technetium-99m", "Americium-241", "Polonium-210",
                   "Uranium-235", "Uranium-238", "Thorium-232", "Potassium-40", "Iodine-129", "Krypton-85",
                   "Plutonium-238"],
        "values": {"반감기": r"^(반감기|halflife)$"},
    },
    "태풍": {
        "titles": ["Typhoon Maemi", "Typhoon Rusa", "Typhoon Sarah (1959)", "Typhoon Hinnamnor",
                   "Typhoon Mitag (2019)", "Typhoon Lingling (2019)", "Typhoon Bolaven (2012)",
                   "Typhoon Sanba (2012)", "Typhoon Chaba (2016)", "Typhoon Kong-rey (2018)",
                   "Typhoon Soulik (2018)", "Typhoon Maysak (2020)", "Typhoon Haishen (2020)",
                   "Typhoon Khanun (2023)", "Typhoon Nari (2007)", "Typhoon Ewiniar (2006)", "Typhoon Megi (2004)",
                   "Typhoon Prapiroon (2000)"],
        "values": {"최저기압": r"^최저기압$", "10분최대풍속": r"^10분최대풍속$"},
    },
    "교량": {
        "titles": ["Incheon Bridge", "Gwangan Bridge", "Akashi Kaikyō Bridge", "Golden Gate Bridge",
                   "Millau Viaduct", "Humber Bridge", "Great Belt Bridge", "Tsing Ma Bridge", "Seohae Bridge",
                   "Yi Sun-sin Bridge", "Ulsan Bridge", "Busan–Geoje Fixed Link", "Banpo Bridge",
                   "Hong Kong–Zhuhai–Macau Bridge", "Øresund Bridge", "Sydney Harbour Bridge", "Brooklyn Bridge",
                   "Second Jindo Bridge"],
        "values": {"주경간": r"^(주경간|최대경간장|mainspan)$", "총길이": r"^(총길이|길이)$"},
    },
    "항공기": {
        "titles": ["Boeing 747", "Airbus A380", "Boeing 787 Dreamliner", "Airbus A350", "Concorde",
                   "Antonov An-225 Mriya", "Boeing 737", "Airbus A320 family", "KAI KF-21 Boramae",
                   "KAI T-50 Golden Eagle", "Lockheed SR-71 Blackbird", "Boeing B-52 Stratofortress",
                   "Lockheed C-130 Hercules", "Embraer E-Jet family", "ATR 72", "Boeing 777",
                   "McDonnell Douglas MD-11", "Tupolev Tu-144", "Ilyushin Il-76", "Airbus A330"],
        "values": {"길이": r"^(length alt|length main|길이|전장)$"},
    },
    "발사체": {
        "titles": ["Nuri (rocket)", "Naro-1", "Saturn V", "Falcon 9", "Falcon Heavy", "Space Launch System",
                   "Ariane 5", "Ariane 6", "Soyuz-2", "Long March 5", "H-IIA", "H3 (rocket)", "Electron (rocket)",
                   "Atlas V", "Delta IV Heavy", "Proton-M", "PSLV", "LVM3", "Vega (rocket)", "N1 (rocket)",
                   "Energia (rocket)"],
        "values": {"높이": r"^(높이|height)$", "질량": r"^(질량|mass)$"},
    },
}

UNIT_TEMPLATES = ("태양질량", "태양반경", "태양광도", "지구질량", "목성질량", "목성반경")


def api(host, params):
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": 2})
    body = get(url, {"User-Agent": UA, "Accept-Encoding": "gzip"})
    time.sleep(GAP)
    return json.loads(body)


def resolve(q, t):
    """요청한 제목이 정규화·넘겨주기를 거쳐 실제로 가리키는 제목."""
    norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
    redir = {r["from"]: r["to"] for r in q.get("redirects", [])}
    t = norm.get(t, t)
    return redir.get(t, t)


def ko_links(titles):
    """영어 제목 -> 한국어 제목(없으면 None). 50개씩 묶어 묻는다."""
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        q = api("en.wikipedia.org", {"action": "query", "titles": "|".join(chunk), "prop": "langlinks",
                                     "lllang": "ko", "lllimit": "max", "redirects": 1})["query"]
        pages = {p["title"]: p for p in q["pages"]}
        for t in chunk:
            p = pages.get(resolve(q, t))
            ll = (p or {}).get("langlinks", [])
            out[t] = ll[0]["title"] if ll else None
    return out


def ko_texts(titles):
    """한국어 제목 -> (글 길이 바이트, 위키 글). 없으면 (0, ""). 20개씩 묶어 묻는다."""
    out = {}
    for i in range(0, len(titles), 20):
        chunk = titles[i:i + 20]
        q = api("ko.wikipedia.org", {"action": "query", "titles": "|".join(chunk), "prop": "revisions|info",
                                     "rvprop": "content", "rvslots": "main", "redirects": 1})["query"]
        pages = {p["title"]: p for p in q["pages"]}
        for t in chunk:
            p = pages.get(resolve(q, t))
            if not p or p.get("missing") or "revisions" not in p:
                out[t] = (0, "")
            else:
                out[t] = (p.get("length", 0), p["revisions"][0]["slots"]["main"]["content"])
    return out


def template(m):
    """틀 하나를 글자로 바꾼다. 값을 담는 틀만 살리고 나머지(출처 등)는 지운다."""
    parts = [s.strip() for s in m.group(1).split("|")]
    name, args = parts[0].lower(), [a for a in parts[1:] if "=" not in a]
    if name == "val":
        return " × ".join(a for a in args if a not in ("x", "×")) if ("x" in args or "×" in args) else (args[0] if args else "")
    if name in ("convert", "cvt", "단위 변환"):
        return " ".join(args[:2])
    if name == "e":
        return f"×10^{args[0]}" if args else ""
    if name in ("nowrap", "nobr"):
        return args[0] if args else ""
    if name in ("nbsp", "nnbsp"):
        return " "
    for u in UNIT_TEMPLATES:
        if name.startswith(u):
            return f" {u}"
    return ""


def clean(raw):
    s = re.sub(r"<ref[^>]*/>", "", raw)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*>.*$", "", s)  # 줄 끝까지 닫히지 않은 출처
    for _ in range(3):  # 안쪽 틀부터
        s = re.sub(r"\{\{([^{}]*)\}\}", template, s)
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"<br\s*/?>", " / ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&gt;", ">").replace("&lt;", "<").replace("'''", "").replace("''", "")
    return re.sub(r"\s+", " ", s).strip()


def kind(s):
    """값 글자 -> 하나 / 범위 / 여럿 / 어림 / 없음."""
    if not re.search(r"\d", s):
        return "없음"
    t = re.sub(r"±\s*[\d.]+", "", s)                    # ± 오차는 하나로 친다
    t = re.sub(r"\(\s*\+[\d.]+\s*,\s*[-−][\d.]+\s*\)", "", t)  # (+0.23, -0.20)
    t = re.sub(r"×\s*10\^?[-−]?\d+", "", t)              # 과학 표기
    if re.search(r"약|~|≈|≥|≤|>|<|\?|추정", t):
        return "어림"
    if re.search(r"\d\s*(?:-|–|―|~|to)\s*\d", t):
        return "범위"
    if re.search(r"\d\s*[×x]\s*\d", t) or re.search(r"\d\s*/\s*\d", t) or re.search(r"\b[AB]\s*:", t):
        return "여럿"
    if sum(1 for part in t.split(" / ") if re.search(r"\d", part)) > 1:  # 줄을 바꿔 둘 이상 적음. 같은 값의 다른 단위도 여기 든다
        return "여럿"
    return "하나"


def values(text, patterns):
    """위키 글의 '| 칸 = 값' 줄에서 물을 값마다 처음 나온 값을 찾아 (정리한 글자, 가른 결과)를 돌려준다."""
    found = {}
    for line in text.splitlines():
        m = re.match(r"\s*\|\s*([^=]{1,40}?)\s*=\s*(.*)$", line)
        if not m:
            continue
        name = re.sub(r"\[\[|\]\]", "", m.group(1)).strip()
        for vname, pat in patterns.items():
            if vname not in found and re.search(pat, name, re.I) and m.group(2).strip():
                c = clean(m.group(2))
                found[vname] = {"text": c[:80], "kind": kind(c)}
    return {v: found.get(v, {"text": "", "kind": "없음"}) for v in patterns}


def main():
    report = {}
    for field, spec in FIELDS.items():
        links = ko_links(spec["titles"])
        kos = [k for k in links.values() if k]
        texts = ko_texts(kos)
        if spec.get("element"):
            tmpl = ko_texts([f"틀:원소 정보/{k}" for k in kos])
        rows = []
        for t in spec["titles"]:
            ko = links[t]
            row = {"en": t, "ko": ko}
            if ko:
                size, text = texts[ko]
                if spec.get("element"):
                    text = tmpl[f"틀:원소 정보/{ko}"][1]
                row["ko_bytes"] = size
                row["values"] = values(text, spec["values"])
            rows.append(row)
        report[field] = rows
        n_ko = sum(1 for r in rows if r["ko"])
        single = {v: sum(1 for r in rows if r["ko"] and r["values"][v]["kind"] == "하나") for v in spec["values"]}
        print(f"{field}: 고른 대상 {len(rows)}, 한국어 문서 {n_ko} | 값이 하나로 적힌 대상 "
              + ", ".join(f"{v} {n}" for v, n in single.items()))
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("저장:", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
