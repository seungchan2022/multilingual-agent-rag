"""고른 12곳의 위키백과 문서 16개를, 받아 둔 HTML(stage2_domain_survey/cache)에서 읽기 쉬운 글로 바꿔 text/에 쓴다.

  python to_text.py

사실을 세는 사람이나 서브에이전트가 읽을 글이다. 코퍼스의 마크다운이 아니다(그것은 이슈 ③에서 만든다).
건너뛰는 상자(정보 상자, 둘러보기 상자, 각주)는 measure.py의 SKIP과 같다. 표는 줄마다 "| 칸 | 칸 |"으로 쓴다.
"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
SURVEY = HERE.parent / "stage2_domain_survey"
sys.path.insert(0, str(SURVEY))
from measure import SKIP, VOID  # noqa: E402

GROUPS = {"both": ["전주시", "청주시", "춘천시", "천안시"], "en": ["부산광역시", "제주시", "안동시", "강릉시"], "ko": ["수원시", "경주시", "세종특별자치시", "광주광역시"]}
BLOCK = {"p", "li", "tr", "table", "dd", "dt", "div", "ul", "ol", "blockquote", "caption"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skip, self.out = [], 0, []

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.out.append(" ")
        if tag in VOID:
            return
        cls = dict(attrs).get("class") or ""
        skip = bool(SKIP.search(cls)) or tag in ("style", "script") or (tag == "sup" and "reference" in cls)
        self.stack.append((tag, skip))
        if skip:
            self.skip += 1
        if self.skip:
            return
        if tag in BLOCK:
            self.out.append("\n")
        if re.fullmatch(r"h[2-6]", tag):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        if tag in ("td", "th"):
            self.out.append(" | ")

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, skip = self.stack.pop()
            if skip:
                self.skip -= 1
            if t == tag:
                break
        if not self.skip and (tag in BLOCK or re.fullmatch(r"h[2-6]", tag)):
            self.out.append(" |\n" if tag == "tr" else "\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data.replace("\n", " "))


def convert(html):
    t = Text(); t.feed(html); t.close()
    lines = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in "".join(t.out).split("\n")]
    return "\n".join(l for l in lines if l and l != "|") + "\n"


def main():
    fetched = {}
    for l in (SURVEY / "fetched.jsonl").read_text(encoding="utf-8").splitlines():
        d = json.loads(l)
        if d["domain"].startswith("도시") and "철도" not in d["domain"]:
            fetched[d["subject"]] = d
    (HERE / "text").mkdir(exist_ok=True)
    docs = []
    for group, cities in GROUPS.items():
        for c in cities:
            for lang in (("ko", "en") if group == "both" else (group,)):
                rec = fetched[c][lang]
                txt = convert((SURVEY / "cache" / f"{lang}_{rec['revid']}.html").read_text(encoding="utf-8"))
                f = HERE / "text" / f"{c}_{lang}.txt"
                f.write_text(txt, encoding="utf-8")
                docs.append({"city": c, "group": group, "lang": lang, "title": rec["title"], "revid": rec["revid"], "file": f"text/{f.name}", "chars": len(txt)})
                print(c, lang, rec["title"], rec["revid"], len(txt))
    (HERE / "docs.json").write_text(json.dumps(docs, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
