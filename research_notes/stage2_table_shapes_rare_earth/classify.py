"""희토류 원소 코퍼스의 마크다운 표를 모양별로 나눠 센다(이슈 #7 "표의 모양을 다시 센다").

  .venv/bin/python research_notes/stage2_table_shapes_rare_earth/classify.py

extract.py가 만든 tables.json을 읽는다. 모양은 이 코퍼스의 표 37개를 읽고 정했다(도시 때의 모양 목록을 옮기지 않았다).
- 기계 판정: 원문 HTML 표의 구조(합친 칸, 머리글 줄 수, 칸 안의 줄바꿈 등)와 마크다운 줄에서 바로 정해지는 것.
- 읽어서 판정: AI가 tables_dump.md의 표를 읽고 고른 표. 아래 MANUAL에 표마다 이유를 적었다.
표 하나가 여러 모양에 들 수 있다. 처리 방법은 4단계(청크 전략)에서 정한다.
결과: shapes.json(모양마다 표 목록), shapes.md(사람이 읽는 보고).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALL = json.loads((HERE / "tables.json").read_text(encoding="utf-8"))
TABLES = [t for t in ALL if t["md_line_no"]]          # 마크다운에 남은 표. 나머지는 변환이 지운 안내 상자다
DROPPED = [t for t in ALL if not t["md_line_no"]]


def key(t):
    return f"{t['doc_id']}:{t['md_line_no']}"


def rows(t):
    """마크다운 표의 머리글 아래 줄들을 칸으로 나눈다."""
    return [[c.strip() for c in l.strip()[1:-1].split(" | ")] for l in t["md_lines"][2:]]


def repeated_first(t):
    """첫 칸이 바로 앞 줄과 같은 줄이 있다(세로로 합친 칸을 되풀이해 적어 같은 대상이 여러 줄에 놓임)."""
    rs = rows(t)
    return any(a[0] == b[0] and a[0] for a, b in zip(rs, rs[1:]))


def meaning_shift(t):
    """줄마다 열의 뜻이 바뀐다: 둘째부터 넷째 칸이 같은 글자이고 'keV'가 든 줄이 있다
    (동위 원소 목록 표의 핵 이성질체 줄. 원문에서 Z·N·질량 세 칸을 합쳐 들뜬 에너지를 적었다)."""
    return any(len(r) >= 4 and r[1] == r[2] == r[3] and "keV" in r[1] for r in rows(t))


MECHANICAL = [
    ("세로로 합친 칸이 있는 표", lambda t: t["rowspan_cells"]["count"] > 0),
    ("가로로 합친 칸이 있는 표", lambda t: t["colspan_cells"]["count"] > 0),
    ("머리글이 두 줄인 표", lambda t: t["top_th_rows"] >= 2),
    ("머리글 줄이 없는 표", lambda t: t["top_th_rows"] == 0),
    ("줄 이름(th)이 첫 칸에 있는 표", lambda t: t["row_header_rows"] > 0),
    ("칸 안에 줄바꿈이 있는 표", lambda t: t["br_cells"]["count"] > 0),
    ("표 제목(caption)이 있는 표", lambda t: bool(t["caption"])),
    ("표 전체 폭 줄(각주 등)이 있는 표", lambda t: bool(t["full_width_rows"])),
    ("같은 대상이 이어진 여러 줄에 놓인 표", repeated_first),
    ("줄마다 열의 뜻이 바뀌는 표", meaning_shift),
]

# 읽어서 판정. 표마다 이유.
MANUAL = {
    "가로로 놓인 표(항목이 줄로 놓이고 머리글 줄이 값)": {
        "rule": "줄이 둘(머리글 줄과 값 줄)이고 첫 칸이 줄 이름이다. 정보 상자의 증기 압력 표: 머리글 줄의 압력 값(1 Pa …)과 아래 줄의 온도 값이 열마다 짝이다",
        "pick": lambda t: t["rows"] == 2 and t["row_header_rows"] == 1,
    },
    "머리글 첫 줄이 묶음 이름인 표": {
        "rule": "영어 정보 상자의 주요 동위원소 표: 첫 머리글 줄은 'Main isotopes'(세 열)와 'Decay'(두 열)이고 열 이름은 둘째 줄에 있다",
        "pick": lambda t: bool(t["md_lines"]) and t["md_lines"][0].startswith("| Main isotopes | Main isotopes"),
    },
    "한 칸에 여러 항목이 든 표(줄바꿈이 항목을 나눔)": {
        "rule": "칸 안의 줄바꿈이 글이 길어 바꾼 것이 아니라 다른 항목을 나눈다. 값 칸 안의 줄바꿈은 ` / `로 바꾸므로(decisions/stage2.md 2026-10-22 \"값 칸 안의 줄바꿈은 ` / `로 바꾼다\") 줄바꿈이 나눈 항목은 경계가 남는다. 줄바꿈이 아니라 문단으로 항목을 나눈 칸은 이 규칙에 들지 않아 항목이 빈칸으로 이어진 채 남는다(남은 한계)",
        "keys": {
            "wiki-ko-yttrium:55": "붕괴 에너지 칸에 값 둘이 ` / `로 나뉘어 경계가 남아 있다: 58줄 `0.48 / 0.38D`, 60줄 `1.83 / 0.89`",
            "wiki-en-neutron-capture-therapy:187": "첫 열의 머리글과 칸이 네 항목(Manufacturer, Product, Reaction, Accelerator type)을 한 칸에 담는다. 항목을 줄바꿈이 아니라 문단으로 나눈 칸이라 ` / `로 바뀌지 않고 빈칸으로 이어진 채 남는다(남은 한계)",
        },
    },
    "목록을 여러 열로 나눈 표(한 줄의 칸끼리 관계가 없음)": {
        "rule": "머리글 없이 이름 목록을 두 열로 흘려 놓은 표. 마크다운에서는 첫 줄이 머리글 자리에 놓였다",
        "keys": {"wiki-en-neutron-capture-therapy:56": "Table 1. 붕소 전달 물질 이름 23개를 두 열로 나눔"},
    },
}


def classify():
    shapes = {}
    for name, f in MECHANICAL:
        shapes[name] = {"how": "기계 판정", "tables": [key(t) for t in TABLES if f(t)]}
    for name, m in MANUAL.items():
        if "pick" in m:
            picked = [key(t) for t in TABLES if m["pick"](t)]
        else:
            picked = list(m["keys"])
            missing = [k for k in picked if k not in {key(t) for t in TABLES}]
            assert not missing, f"없는 표: {missing}"
        shapes[name] = {"how": "읽어서 판정", "rule": m["rule"], "tables": picked,
                        "notes": m.get("keys", {})}
    any_shape = {k for s in shapes.values() for k in s["tables"]}
    shapes["위 모양이 하나도 없는 표"] = {"how": "기계 판정(위 목록의 나머지)",
                                   "tables": [key(t) for t in TABLES if key(t) not in any_shape]}
    return shapes


def group_of(t):
    """표를 어디에 있는 표인지로 묶는다(보고용)."""
    if t["md_lines"] and t["rows"] == 2 and t["row_header_rows"] == 1:
        return "정보 상자의 증기 압력 표"
    if t["cols"] <= 6 and t["md_lines"] and ("동위체" in t["md_lines"][0] or "Main isotopes" in t["md_lines"][0]):
        return "정보 상자의 주요 동위원소 표"
    if t["rows"] > 50:
        return "동위 원소 문서의 목록 표"
    return "그 밖의 본문 표"


def report(shapes):
    o = ["# 마크다운 표의 모양(희토류 원소 코퍼스)", "",
         "`classify.py`가 `tables.json`에서 만든다. 표 하나가 여러 모양에 들 수 있다. 처리 방법은 4단계(청크 전략)에서 정한다.",
         "모양은 이 코퍼스의 표를 읽고 정했다. 도시 코퍼스 때의 목록(`research_notes/stage2_table_shapes/shapes.md`)은 옮기지 않았다.", "",
         f"마크다운 표 {len(TABLES)}개. 변환 코드가 표로 받았지만 마크다운에 남지 않은 것 {len(DROPPED)}개"
         f"({', '.join(sorted({t['doc_id'] for t in DROPPED}))}의 토막글 안내 상자).", "",
         "## 어디에 있는 표인가", "", "| 묶음 | 표 수 |", "|---|---|"]
    groups = {}
    for t in TABLES:
        groups.setdefault(group_of(t), []).append(key(t))
    for g, ks in groups.items():
        o.append(f"| {g} | {len(ks)} |")
    o += ["", "## 모양", "", "| 모양 | 판정 | 표 수 |", "|---|---|---|"]
    for name, s in shapes.items():
        o.append(f"| {name} | {s['how']} | {len(s['tables'])} |")
    o += ["", "## 모양마다 표", ""]
    for name, s in shapes.items():
        o.append(f"### {name} ({len(s['tables'])})")
        if s.get("rule"):
            o.append(f"기준: {s['rule']}")
        for k in s["tables"]:
            note = s.get("notes", {}).get(k)
            o.append(f"- `{k}`" + (f": {note}" if note else ""))
        o.append("")
    return "\n".join(o)


def main():
    shapes = classify()
    (HERE / "shapes.json").write_text(json.dumps(shapes, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "shapes.md").write_text(report(shapes), encoding="utf-8")
    for name, s in shapes.items():
        print(f"{len(s['tables']):>3}  {name}")


if __name__ == "__main__":
    main()
