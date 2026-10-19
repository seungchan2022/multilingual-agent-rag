"""후보 고르기 실험(이슈 #6)의 근거 문서를 한국어 위키백과에서 받아 마크다운으로 바꾼다.

  .venv/bin/python src/domain_select/fetch_docs.py <후보 폴더> <문서 제목> ...

받는 방식과 마크다운 변환은 코퍼스 프로그램(src/corpus/fetch.py의 get, src/corpus/build.py의 convert_wiki)을
그대로 쓴다. 고른 뒤 만들 코퍼스와 같은 글에서 근거를 옮기기 위해서다.
<후보 폴더>/raw/에 받은 HTML을, <후보 폴더>/md/에 마크다운을, <후보 폴더>/docs.json에 제목·판 번호·주소를 쓴다.
"""
import json, sys, time, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "corpus"))
from fetch import UA, GAP, get  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from build import convert_wiki, drop_all, prepare, prune, render, walk  # noqa: E402


def to_markdown(title, raw):
    """convert_wiki는 정보 상자가 있다고 보고 쓴 것이라, 정보 상자가 없는 문서(식을 옮길 문서)는 그 부분만 건너뛴다."""
    soup = BeautifulSoup(raw.decode("utf-8"), "html.parser")
    root = soup.find("div", class_="mw-parser-output")
    if root.find("table", class_="infobox", recursive=False):
        return convert_wiki({"title": title}, raw)
    prepare(root)
    drop_all(root)
    items = []
    walk(root, items)
    return render(title, [], prune(items))


def api(params):
    url = "https://ko.wikipedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": 2})
    return json.loads(get(url, {"User-Agent": UA, "Accept-Encoding": "gzip"}))


def main():
    out, titles = Path(sys.argv[1]), sys.argv[2:]
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "md").mkdir(parents=True, exist_ok=True)
    docs_path = out / "docs.json"
    docs = json.loads(docs_path.read_text(encoding="utf-8")) if docs_path.exists() else {}
    for t in titles:
        page = api({"action": "query", "titles": t, "prop": "revisions", "rvprop": "ids", "redirects": 1})["query"]["pages"][0]
        if "missing" in page:
            sys.exit(f"없는 문서: {t}")
        revid = page["revisions"][0]["revid"]
        time.sleep(GAP)
        r = api({"action": "parse", "oldid": revid, "prop": "text|revid"})["parse"]
        assert r["revid"] == revid, t
        raw = r["text"].encode("utf-8")
        (out / "raw" / f"{page['title']}.html").write_bytes(raw)
        md = to_markdown(page["title"], raw)
        (out / "md" / f"{page['title']}.md").write_text(md, encoding="utf-8")
        docs[page["title"]] = {"revid": revid, "url": f"https://ko.wikipedia.org/w/index.php?oldid={revid}"}
        print(f"{page['title']}  판 {revid}  마크다운 {len(md)}자")
        docs_path.write_text(json.dumps(docs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        time.sleep(GAP)


if __name__ == "__main__":
    main()
