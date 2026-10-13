"""공공데이터포털에서 분야마다 정해 둔 검색어(portal_queries.json)로 검색해 결과의 이름 목록을 저장한다.

  python portal_search.py        결과는 portal_search.json에 쓴다

기준 ④(통계 표)와 ⑤(대상 자료)의 표시는 이 목록을 보고 portal.json에 따로 적는다.
"""
import html, json, re, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).parent
UA = {"User-Agent": "Mozilla/5.0"}


def get(url):
    err = None
    for wait in (0, 5, 20, 60):
        time.sleep(wait)
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8", "replace")
            time.sleep(1.5)
            return r
        except Exception as e:
            err = e
    raise RuntimeError(f"요청 실패: {err}")


def search(keyword, dtype):
    q = urllib.parse.urlencode({"keyword": keyword, "dType": dtype, "perPage": 20})
    h = get("https://www.data.go.kr/tcs/dss/selectDataSetList.do?" + q)
    counts = dict(re.findall(r"(파일데이터|오픈 ?API)\s*\(?\s*<[^>]*>?\s*([\d,]+)", h))
    names = []
    for u, t in re.findall(r'href="(/data/\d+/\w+\.do)[^"]*"[^>]*>(.*?)</a>', h, flags=re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()
        if t and (u, t) not in names:
            names.append((u, t))
    return {"counts": counts, "names": [{"id": u.split("/")[2], "name": t} for u, t in names]}


def main():
    queries = json.loads((HERE / "portal_queries.json").read_text(encoding="utf-8"))
    out = {}
    for dom, kws in queries.items():
        out[dom] = {}
        for kw in kws:
            out[dom][kw] = {"FILE": search(kw, "FILE"), "API": search(kw, "API")}
            c = out[dom][kw]["FILE"]["counts"]
            print(f"{dom} | {kw} | {c}", flush=True)
        (HERE / "portal_search.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
