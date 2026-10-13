"""도시 20곳의 관광공사 관광정보(국문·영문)에서 관광지·문화시설의 명소 글을 조사한다.

  python survey.py codes     지역 코드 목록을 받아 도시마다 쓸 코드를 codes.json에 쓴다
  python survey.py fetch     목록과 설명 글을 받는다. 받은 응답은 cache/에 두고 다시 받지 않는다
  python survey.py report    cache/에서 pairs.json, unmatched.json, summary.md를 만든다

규칙은 decisions/stage2.md의 2026-10-13 "20곳 전체에서 관광공사 관광정보의 명소 글을 한 번에 조사한다" 줄에 있다.
인증키는 프로젝트의 .env에 있는 DATA_GO_KR_KEY를 쓴다.
"""
import hashlib, html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
CACHE = HERE / "cache"
BASE = "https://apis.data.go.kr/B551011"
TYPES = {"KorService2": ("12", "14"), "EngService2": ("76", "78")}
# 특별시·광역시·특별자치시는 지역 전체, 일반 시는 그 지역 안에서 이름으로 찾는다
METRO = ["서울특별시", "부산광역시", "인천광역시", "대구광역시", "대전광역시", "울산광역시", "세종특별자치시"]
CITY = ["수원시", "전주시", "경주시", "제주시", "창원시", "청주시", "춘천시", "강릉시", "포항시", "여수시", "안동시", "천안시"]


def key():
    env = dict(l.strip().split("=", 1) for l in (HERE.parent.parent / ".env").read_text().splitlines() if "=" in l)
    return env["DATA_GO_KR_KEY"]


def call(svc, op, **p):
    """응답을 cache/에 두고, 있으면 다시 받지 않는다."""
    p = {"MobileOS": "ETC", "MobileApp": "corpus-survey", "_type": "json", **p}
    name = hashlib.sha1(json.dumps([svc, op, p], sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    f = CACHE / f"{svc}_{op}_{name}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))["response"]
    url = f"{BASE}/{svc}/{op}?serviceKey={urllib.parse.quote(key(), safe='%')}&" + urllib.parse.urlencode(p)
    for wait in (0, 5, 20, 60):  # 시간 초과 같은 일시적 실패는 기다렸다 다시 받는다
        time.sleep(wait)
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")
            break
        except OSError as e:
            err = e
    else:
        raise RuntimeError(f"요청 실패: {err}")
    time.sleep(0.3)
    r = json.loads(raw)  # 한도에 걸리면 JSON이 아니어서 여기서 멈춘다
    if r.get("response", {}).get("header", {}).get("resultCode") != "0000":
        raise RuntimeError(f"이상 응답: {raw[:300]}")
    CACHE.mkdir(exist_ok=True)
    f.write_text(json.dumps({"params": p, "response": r}, ensure_ascii=False), encoding="utf-8")
    return r


def items(r):
    b = r["response"]["body"]
    it = b["items"]["item"] if b.get("items") else []
    return it, int(b.get("totalCount") or 0)


def listing(svc, op, **p):
    out, page = [], 1
    while True:
        it, tot = items(call(svc, op, numOfRows=1000, pageNo=page, **p))
        out += it
        if len(out) >= tot or not it:
            assert len(out) == tot, f"받은 수 {len(out)} != 전체 수 {tot}: {svc} {op} {p}"
            return out
        page += 1


def codes():
    regions = listing("KorService2", "ldongCode2")
    out = {"regions": regions, "cities": {}}
    for m in METRO:
        hit = [r for r in regions if r["name"] == m]
        out["cities"][m] = [{"regn": r["code"], "signgu": None, "name": r["name"]} for r in hit]
    for r in regions:
        for s in listing("KorService2", "ldongCode2", lDongRegnCd=r["code"]):
            for c in CITY:
                if s["name"] == c or s["name"].startswith(c + " "):
                    out["cities"].setdefault(c, []).append({"regn": r["code"], "signgu": s["code"], "name": s["name"]})
            if "광주" in s["name"]:
                out["cities"].setdefault("광주(이름에 광주가 든 코드. 사람이 보고 가른다)", []).append({"regn": r["code"], "signgu": s["code"], "name": r["name"] + " " + s["name"]})
    (HERE / "codes.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for c, v in out["cities"].items():
        print(c, [(x["regn"], x["signgu"], x["name"]) for x in v])


def clean(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()


def city_items(svc, cds):
    seen = {}
    for c in cds:
        for t in TYPES[svc]:
            p = {"lDongRegnCd": c["regn"], "contentTypeId": t}
            if c["signgu"]:
                p["lDongSignguCd"] = c["signgu"]
            for i in listing(svc, "areaBasedList2", **p):
                seen[i["contentid"]] = i
    return list(seen.values())


def match(en, ko_by_title):
    """영어 제목 끝 괄호의 한글 이름이 한국어 제목과 글자 그대로 같은 것."""
    t = en["title"].rstrip()
    hit = [k for kt, k in ko_by_title.items() if t.endswith("(" + kt + ")")]
    return max(hit, key=lambda k: len(k["title"])) if hit else None


def build(fetch_detail):
    cds = json.loads((HERE / "codes.json").read_text(encoding="utf-8"))["use"]
    pairs, unmatched, summary = [], [], []
    for city, c in cds.items():
        ko, en = city_items("KorService2", c), city_items("EngService2", c)
        ko_by_title = {k["title"]: k for k in ko}
        en1 = [e for e in en if e.get("cpyrhtDivCd") == "Type1"]
        ko1 = [k for k in ko if k.get("cpyrhtDivCd") == "Type1"]
        n_pair = n_ko3 = 0
        for e in en1:
            k = match(e, ko_by_title)
            if k is None:
                def d(x):
                    try:
                        return abs(float(x["mapx"]) - float(e["mapx"])) + abs(float(x["mapy"]) - float(e["mapy"]))
                    except Exception:
                        return 9e9
                near = min(ko, key=d) if ko else None
                unmatched.append({"city": city, "en_title": e["title"], "en_id": e["contentid"],
                                  "nearest_ko_title": near and near["title"], "nearest_ko_type": near and (near.get("cpyrhtDivCd") or "빈값"),
                                  "nearest_dist": near and round(d(near), 6)})
                continue
            if k.get("cpyrhtDivCd") != "Type1":
                n_ko3 += 1
                continue
            n_pair += 1
            row = {"city": city, "ko_title": k["title"], "ko_id": k["contentid"], "en_title": e["title"], "en_id": e["contentid"]}
            if fetch_detail:
                for lang, svc, cid in (("ko", "KorService2", k["contentid"]), ("en", "EngService2", e["contentid"])):
                    it, _ = items(call(svc, "detailCommon2", contentId=cid))
                    row[lang + "_overview"] = clean(it[0].get("overview")) if it else ""
                    row[lang + "_chars"] = len(row[lang + "_overview"])
            pairs.append(row)
        summary.append({"city": city, "ko_all": len(ko), "ko_type1": len(ko1), "en_all": len(en), "en_type1": len(en1),
                        "pairs_both_type1": n_pair, "en_type1_ko_not_type1": n_ko3,
                        "en_type1_unmatched": sum(1 for u in unmatched if u["city"] == city)})
        print(json.dumps(summary[-1], ensure_ascii=False), flush=True)
    return pairs, unmatched, summary


def report():
    pairs, unmatched, summary = build(True)
    (HERE / "pairs.json").write_text(json.dumps(pairs, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "unmatched.json").write_text(json.dumps(unmatched, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    {"codes": codes, "fetch": lambda: build(True), "report": report}[sys.argv[1]]()
