"""위키백과 문서 16개를 마크다운으로 바꿀 규칙을 정할 때 본 수를, 받아 둔 HTML에서 다시 센다.

  python survey.py

결과는 survey.json에 쓴다. 규칙은 decisions/stage2.md의 2026-10-14 줄에 있다.
받아 둔 HTML은 stage2_domain_survey/cache/에 있고(저장소에는 없다), 판 번호는 stage2_fact_count/docs.json에 있다.
"""
import html, json, re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).parent
CACHE = HERE.parent / "stage2_domain_survey" / "cache"
DOCS = json.loads((HERE.parent / "stage2_fact_count" / "docs.json").read_text(encoding="utf-8"))
VOID = {"br", "img", "hr", "input", "meta", "link", "col", "wbr", "source", "area", "base", "embed", "param", "track"}
BOX = re.compile(r"infobox|navbox|metadata|ambox|sistersitebox|side-box|authority-control|noprint|portalbox")


def text(s):
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def attr(tag, name):
    m = re.search(name + r'="([^"]*)"', tag)
    return m.group(1) if m else ""


def filename(tag):
    return unquote(re.sub(r"^\d+px-", "", attr(tag, "src").split("?")[0].split("/")[-1]))


class Images(HTMLParser):
    """상자(정보 상자, 맨 아래 상자 등) 밖에 있는 가로 50픽셀 이상의 그림을 센다."""

    def __init__(self):
        super().__init__()
        self.stack, self.box, self.count = [], 0, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img":
            if not self.box and int(a.get("width") or 0) >= 50:
                self.count += 1
            return
        if tag in VOID:
            return
        inbox = bool(BOX.search(a.get("class") or ""))
        self.stack.append((tag, inbox))
        self.box += inbox

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            t, inbox = self.stack.pop()
            self.box -= inbox
            if t == tag:
                break


def survey(d):
    h = (CACHE / f"{d['lang']}_{d['revid']}.html").read_text(encoding="utf-8")
    imgs = re.findall(r"<img[^>]*>", h)
    p = Images()
    p.feed(h)
    signs = [i for i in imgs if re.search(r"Korean_(Highway|National_Route|Local_Route)", filename(i))]
    flags = [i for i in imgs if filename(i).startswith("Flag_of_") and attr(i, "alt") and int(attr(i, "width") or 99) <= 40]
    notes = []  # 글자 표시([a])가 붙는 설명 목록
    for m in re.finditer(r'<ol[^>]*class="[^"]*references[^"]*"[^>]*data-mw-group[^>]*>', h):
        block = h[m.start():h.find("</ol>", m.start())]
        notes += [text(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", block, flags=re.S)]
    marks = [text(m) for m in re.findall(r'<sup[^>]*class="[^"]*(?:noprint|Inline-Template)[^"]*"[^>]*>.*?</sup>', h, flags=re.S)]
    return {
        "city": d["city"], "lang": d["lang"], "revid": d["revid"],
        "sections": [text(m) for m in re.findall(r"<h2[^>]*>(.*?)</h2>", h, flags=re.S)],
        "infobox_tables": len(re.findall(r'<table[^>]*class="[^"]*infobox', h)),
        "images_outside_boxes_50px": p.count,
        "road_signs": len(signs), "road_signs_with_alt": sum(bool(attr(i, "alt")) for i in signs),
        "road_sign_alts": [attr(i, "alt") for i in signs],
        "flags": len(flags),
        "explanatory_notes": notes,
        "editor_marks": marks,
        "notice_boxes": [text(h[m.start():h.find("</table>", m.start())])[:80] for m in re.finditer(r'<table[^>]*class="[^"]*\bambox', h)],
        "population_change_tables": len(re.findall(r'<table[^>]*class="[^"]*table-pale', h)),
        "pie_charts": len(re.findall(r'class="smooth-pie-container"', h)),
    }


def main():
    rows = [survey(d) for d in DOCS]
    total = {k: sum(r[k] for r in rows) for k in ("images_outside_boxes_50px", "road_signs", "road_signs_with_alt", "flags")}
    total["explanatory_notes"] = sum(len(r["explanatory_notes"]) for r in rows)
    (HERE / "survey.json").write_text(json.dumps({"total": total, "documents": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(total)
    for r in rows:
        print(r["city"], r["lang"], r["images_outside_boxes_50px"], r["road_signs"], r["flags"], len(r["explanatory_notes"]), r["editor_marks"], len(r["notice_boxes"]))


if __name__ == "__main__":
    main()
