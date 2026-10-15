"""한국어 문서 14개에서 두 문서 이상에 함께 나오는 낱말(고리 후보)을 뽑는다.

낱말은 한글·영문·숫자가 이어진 덩어리에서 흔한 조사·어미를 떼어 낸 것이다.
문서 3개 이하에 나오는 낱말만 남긴다(더 흔한 낱말은 이름이 아닐 가능성이 크다).
숫자가 든 낱말과 용언·부사처럼 끝나는 낱말(-다, -며, -고 등)은 뺀다. 이름인지는 서브에이전트가 가른다.
한계: 4개 이상의 한국어 문서에 나오는 이름, 같은 대상을 다른 글자로 적은 것(예: 경부고속선과 경부고속철도), 조사를 떼다 남은 조각(예: 곳으)은 잡지 못하거나 잘못 잡는다.
결과: shared_names.json (낱말마다 나오는 문서와 줄 번호, 맡을 문서)
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "data/corpus/markdown"
OUT = Path(__file__).with_name("shared_names.json")

# 맡기는 순서: 한국어 도시의 문서 먼저 (결정 2026-10-15)
ORDER = [
    "wiki-ko-suwon", "portal-ko-suwon-population", "wiki-ko-gyeongju", "wiki-ko-sejong", "wiki-ko-gwangju",
    "wiki-ko-jeonju", "kto-ko-jeonju-hanok-village", "portal-ko-jeonju-population",
    "wiki-ko-cheongju", "kto-ko-cheongju-cheongnamdae",
    "wiki-ko-chuncheon", "kto-ko-chuncheon-samaksan-cable-car",
    "wiki-ko-cheonan", "kto-ko-cheonan-samgeori-park",
]
JOSA = sorted("은 는 이 가 을 를 의 에 에서 에게 으로 로 와 과 도 만 까지 부터 이다 였다 이며 이고 으로서 로서 에는 에서는 으로는 로는 과의 와의 이라는 라는 인 한 된 하는 하여 했다 한다 되었다 하였다".split(), key=len, reverse=True)
STOP_MAX_DF = 3
NOT_NOUN_END = re.compile(r"(다|며|고|는|을|할|된|한|던|게|지|면|서|어|아|여|요|죠|니|라|든|도록|기|음|함|됨|적|인|들|등)$")
TOKEN = re.compile(r"[가-힣A-Za-z0-9]+")

def norm(tok):
    for j in JOSA:
        if tok.endswith(j) and len(tok) - len(j) >= 2:
            return tok[: -len(j)]
    return tok

def main():
    docs = {d: (MD / f"{d}.md").read_text(encoding="utf-8").splitlines() for d in ORDER}
    assert sorted(ORDER) == sorted(p.stem for p in MD.glob("*-ko-*.md")), "한국어 문서 목록이 다르다"
    where = {}
    for d, lines in docs.items():
        for i, line in enumerate(lines, 1):
            for t in TOKEN.findall(line):
                t = norm(t)
                if len(t) < 2 or t.isdigit():
                    continue
                where.setdefault(t, {}).setdefault(d, []).append(i)
    items = []
    for t, by_doc in sorted(where.items()):
        if re.search(r"[0-9]", t) or NOT_NOUN_END.search(t):
            continue
        if 2 <= len(by_doc) <= STOP_MAX_DF:
            owner = min(by_doc, key=ORDER.index)
            items.append({"name": t, "docs": {d: v for d, v in by_doc.items()}, "owner": owner})
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print(len(items), Counter(x["owner"] for x in items))

main()
