"""코퍼스의 문단·표·행 길이를 bge-m3 토크나이저의 토큰으로 센다(이슈 #8 9번 청크 크기 후보).

  uv run --no-project --with tokenizers --with huggingface_hub python -I research_notes/stage4_chunk_lengths/lengths.py data/corpus/markdown

빈 줄로 나눈 덩어리 가운데 #으로 시작하는 제목 줄은 빼고, |로 시작하면 표, 아니면 문단으로 본다. 결과는 output.txt.
"""
import sys, glob, statistics as st
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer
t = Tokenizer.from_file(hf_hub_download("BAAI/bge-m3", "tokenizer.json"))
n = lambda x: len(t.encode(x, add_special_tokens=False).ids)
paras, rows, heads, tables = [], [], [], []
for f in sorted(glob.glob(sys.argv[1] + "/*.md")):
    blocks = open(f, encoding="utf-8").read().split("\n\n")
    for b in blocks:
        b = b.strip()
        if not b or b.startswith("#"):
            continue
        ls = b.split("\n")
        if ls[0].startswith("|"):
            tables.append(n(b)); heads.append(n(ls[0]))
            rows += [n(l) for l in ls[2:] if l.startswith("|")]
        else:
            paras.append(n(b))
def show(name, xs):
    xs = sorted(xs); q = lambda p: xs[min(len(xs)-1, int(p*len(xs)))]
    over = {k: sum(x > k for x in xs) for k in (128, 256, 512)}
    print(f"{name}: 개수 {len(xs)}, 중앙 {q(.5)}, 90% {q(.9)}, 최대 {xs[-1]}, 128초과 {over[128]}, 256초과 {over[256]}, 512초과 {over[512]}")
show("문단(표 아닌 덩어리)", paras); show("표 전체", tables); show("표 머리글 줄", heads); show("표 행", rows)
