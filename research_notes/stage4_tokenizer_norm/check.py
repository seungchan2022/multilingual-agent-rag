"""임베딩 후보 세 모델의 토크나이저가 위 첨자·아래 첨자·전각 글자를 평범한 글자와 같은 토큰으로 바꾸는지 본다(이슈 #8 8번).

  uv run --no-project --with tokenizers --with huggingface_hub python -I research_notes/stage4_tokenizer_norm/check.py

결과는 output.txt. tokenizer.json만 Hugging Face에서 받는다.
"""
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer
import unicodedata
models = ["sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "Alibaba-NLP/gte-multilingual-base", "BAAI/bge-m3"]
pairs = [("¹⁴⁷Nd", "147Nd"), ("¹³⁹La", "139La"), ("La³⁺", "La3+"), ("La₂O₃", "La2O3"), ("９.８４１ g/cm³", "9.841 g/cm3"), ("ｇ／ｃｍ", "g/cm")]
for m in models:
    t = Tokenizer.from_file(hf_hub_download(m, "tokenizer.json"))
    print(m, "normalizer:", t.normalizer.__class__.__name__ if t.normalizer else None)
    for a, b in pairs:
        ta, tb = t.encode(a, add_special_tokens=False).tokens, t.encode(b, add_special_tokens=False).tokens
        print(f"  {a!r:16} {ta}  | {b!r:14} {tb}  same={ta==tb}")
print("NFKC:", [unicodedata.normalize("NFKC", a) for a, _ in pairs])
