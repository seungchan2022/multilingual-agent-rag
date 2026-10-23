"""check.py가 틀림을 잡는지 본다: 청크 묶음 사본과 마크다운 표를 하나씩 일부러 망가뜨려 check.py에 넣는다.

  .venv/bin/python research_notes/stage5_table_chunks/mutate.py <임시 폴더> > research_notes/stage5_table_chunks/mutate_output.txt

임시 폴더에 청크 묶음 사본과 check.py의 출력이 쓰인다(저장소의 청크와 판정 파일은 건드리지 않는다).
"잡음"이면 check.py가 그 망가뜨림을 틀림으로 판정한 것이다. 마지막 "변환 대조"는 망가뜨리지 않은 표에 문제를 내지 않는지 본다.
"""
import contextlib
import io
import json
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import check  # noqa: E402

SCR = Path(sys.argv[1])
SRC = ROOT / "data" / "minimal" / "chunks"
T = "wiki-ko-isotopes-of-terbium"


def md_lines(did):
    return (ROOT / "data" / "corpus" / "markdown" / f"{did}.md").read_text(encoding="utf-8").split("\n")


def load(n):
    return [json.loads(l) for l in (SRC / f"{n}.jsonl").read_text(encoding="utf-8").splitlines()]


def find(cs, did, line):
    return next(c for c in cs if c["doc_id"] == did and line in c["lines"])


def run(label, name, mutate):
    d = SCR / label
    if d.exists():
        shutil.rmtree(d)
    (d / "chunks").mkdir(parents=True)
    (d / "out").mkdir()
    for n in check.SETS:
        shutil.copy(SRC / f"{n}.jsonl", d / "chunks" / f"{n}.jsonl")
    cs = load(name)
    mutate(cs)
    (d / "chunks" / f"{name}.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cs), encoding="utf-8")
    check.CHUNKS, check.HERE = d / "chunks", d / "out"
    with contextlib.redirect_stdout(io.StringIO()):
        check.main()
    out = (d / "out" / "output.txt").read_text(encoding="utf-8").splitlines()
    line = next(l for l in out if l.startswith(name + ":"))
    caught = "틀림 0," not in line or "없음" not in line.split("행 빠짐·겹침")[1]
    print(("잡음 " if caught else "놓침 ") + label + " | " + line[:220])


def drop_header2(cs):  # 터븀 128 조각에서 둘째 머리글 줄(11줄)을 뺀다
    c = find(cs, T, 40)
    c["lines"].remove(11)
    c["text"] = "\n".join(l for l in c["text"].split("\n") if not l.startswith("| 핵자 수 | 들뜬 에너지"))


def swap_cells(cs):  # 영어 툴륨 정보 상자 표의 한 행에서 칸 둘을 바꾼다(줄 목록은 그대로)
    c = find(cs, "wiki-en-thulium", 63)
    c["text"] = c["text"].replace("| ¹⁶⁸Tm | synth | 93.1 d |", "| ¹⁶⁸Tm | 93.1 d | synth |")


def drop_row(cs):  # 한 행을 글과 줄 목록에서 함께 뺀다(빠짐)
    c = find(cs, T, 40)
    c["lines"].remove(40)
    src = md_lines(T)[39]
    c["text"] = "\n".join(l for l in c["text"].split("\n") if l != src)


def dup_row(cs):  # 한 행을 다른 조각에도 넣는다(겹침)
    b = find(cs, T, 41)
    src = md_lines(T)[39]
    b["lines"] = sorted(set(b["lines"]) | {40})
    lines = b["text"].split("\n")
    k = next(i for i, l in enumerate(lines) if l.startswith("| ¹"))
    lines.insert(k, src)
    b["text"] = "\n".join(lines)


def wrong_header(cs):  # 다른 표(네오디뮴)의 머리글을 붙인다
    c = find(cs, T, 40)
    c["text"] = c["text"].replace(c["text"].split("\n")[0], md_lines("wiki-ko-isotopes-of-neodymium")[10], 1)


def drop_name_line(cs):  # 정보 상자 조각에서 '  - 증기 압력' 줄을 뺀다
    c = find(cs, "wiki-ko-lutetium", 26)
    c["lines"].remove(24)
    c["text"] = "\n".join(l for l in c["text"].split("\n") if l != "  - 증기 압력")


def ex2_swap(cs):  # 예외 2의 한 행에서 제품과 반응을 바꾼다
    c = find(cs, "wiki-en-neutron-capture-therapy", 197)
    c["text"] = c["text"].replace("| University of Tsukuba | iBNCT | ⁹Be(p,n)⁹B |", "| University of Tsukuba | ⁹Be(p,n)⁹B | iBNCT |")


def ex1_order(cs):  # 예외 1의 이름 둘의 순서를 바꾼다
    c = find(cs, "wiki-en-neutron-capture-therapy", 58)
    c["text"] = c["text"].replace("Boric acid\nBoron nitride nanotubes", "Boron nitride nanotubes\nBoric acid")


def group_line(cs):  # 정보 상자 조각에서 묶음 이름 줄을 뺀다
    c = find(cs, "wiki-ko-lutetium", 58)
    c["lines"].remove(52)
    c["text"] = "\n".join(l for l in c["text"].split("\n") if l != "- 주요 동위원소")


def main():
    for label, name, f in [("둘째 머리글 줄 빠짐", "size128_notitle", drop_header2),
                           ("칸 자리 바뀜", "size256_notitle", swap_cells),
                           ("행 빠짐", "size128_notitle", drop_row), ("행 겹침", "size128_notitle", dup_row),
                           ("다른 표 머리글", "size128_notitle", wrong_header),
                           ("표 이름 줄 빠짐", "size128_title", drop_name_line),
                           ("예외 2 칸 바뀜", "size256_title", ex2_swap), ("예외 1 순서 바뀜", "size128_notitle", ex1_order),
                           ("묶음 이름 줄 빠짐", "size256_notitle", group_line)]:
        run(label, name, f)

    # 변환 쪽: 터븀 마크다운 표를 망가뜨려 check_table에 넣는다
    docs = {d["doc_id"]: d for d in yaml.safe_load((ROOT / "data/corpus/documents.yaml").read_text(encoding="utf-8"))["documents"]}
    col = {c["doc_id"]: c for c in yaml.safe_load((ROOT / "data/corpus/collected.yaml").read_text(encoding="utf-8"))["documents"]}
    _, calls = check.traced(docs[T], (ROOT / "data/corpus" / col[T]["raw_file"]).read_bytes())
    g = [l for l in md_lines(T) if l.startswith("|")]
    snap = next(s for s, r in calls if any(it[0] == "b" and it[1] and it[1][0] == g[0] for it in r))

    def bad_table(label, lines):
        rec, _ = check.check_table(snap, 9, lines)
        print(("잡음 " if rec["problems"] else "놓침 ") + "변환: " + label + " | " + str(rec["problems"])[:160])

    def row(cells):
        return "| " + " | ".join(cells) + " |"

    x = list(g)
    cs = check.md_cells(x[20])
    cs[3], cs[4] = cs[4], cs[3]
    x[20] = row(cs)
    bad_table("한 행에서 칸 둘 바뀜", x)
    x = list(g)
    cs = check.md_cells(x[20])
    x[20] = row(cs[:3] + cs[4:] + [""])
    bad_table("한 행에서 칸이 왼쪽으로 밀림", x)
    x = list(g)
    x.pop(30)
    bad_table("행 하나 빠짐", x)
    rec, _ = check.check_table(snap, 9, g)
    print(("문제 없음(기대대로) " if not rec["problems"] else "문제 냄(틀림) ") + "변환 대조: 망가뜨리지 않은 표 | " + str(rec["problems"]))


if __name__ == "__main__":
    main()
