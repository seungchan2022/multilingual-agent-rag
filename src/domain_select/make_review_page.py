"""후보 고르기 실험(이슈 #6)의 질문을 사용자가 확인할 HTML 페이지로 만든다.

  python3 src/domain_select/make_review_page.py <후보 폴더> <후보 이름>

<후보 폴더>/questions.json과 docs.json을 읽어 <후보 폴더>/review.html에 쓴다.
"만들며 본 것"은 후보마다 다르므로 <후보 폴더>/review_notes.html이 있으면 그 내용을 그대로 넣는다.
"""
import html, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
NAME = sys.argv[2]
qs = json.loads((ROOT / "questions.json").read_text(encoding="utf-8"))
docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))

e = html.escape

cards = []
for q in qs:
    steps = "".join(f"<li>{e(s)}</li>" for s in q["steps"])
    ev = "".join(
        f'<li><a href="{e(docs[x["doc"]]["url"])}" target="_blank" rel="noopener">{e(x["doc"])}</a>'
        f'<span class="rev">판 {docs[x["doc"]]["revid"]}</span><q>{e(x["quote"])}</q></li>'
        for x in q["evidence_quotes"])
    cards.append(f"""
<article class="q" id="{q['id']}">
  <header><span class="qid">{q['id']}</span><h2>{e(q['question'])}</h2></header>
  <div class="ans"><span class="lbl">정답</span><span class="num">{e(q['answer'])}</span><span class="calc">{e(q['calc'])}</span></div>
  <div class="cols">
    <section><h3>단계별 해설</h3><ol class="steps">{steps}</ol></section>
    <section><h3>근거 글 (한국어 위키백과, 글자 그대로)</h3><ul class="ev">{ev}</ul></section>
  </div>
</article>""")

notes_path = ROOT / "review_notes.html"
notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""

page = f"""<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(NAME)} 질문 검토</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* 실험 노트처럼: 왼쪽에 위치와 볼 것, 아래로 질문 카드가 이어진다 */
:root {{
  --bg: #f3f5f7; --paper: #ffffff; --ink: #1c2530; --muted: #5b6876; --line: #d5dbe1;
  --accent: #1f5fa8; --accent-soft: #e3ecf7; --warn: #8a5a00; --warn-soft: #fbf1dc;
  --sans: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #12171d; --paper: #1a2129; --ink: #e4e9ee; --muted: #9aa7b4; --line: #2c3743;
  --accent: #7fb0ea; --accent-soft: #1d2d40; --warn: #e2b764; --warn-soft: #33290f; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #12171d; --paper: #1a2129; --ink: #e4e9ee; --muted: #9aa7b4; --line: #2c3743;
  --accent: #7fb0ea; --accent-soft: #1d2d40; --warn: #e2b764; --warn-soft: #33290f; color-scheme: dark; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: var(--sans); font-size: 15px; line-height: 1.65; }}
.wrap {{ max-width: 980px; margin: 0 auto; padding-block: 28px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 20px; }}
h1 {{ font-size: 1.6rem; margin: 0; text-wrap: balance; }}
.where {{ font-family: var(--mono); font-size: .85rem; color: var(--muted); }}
.intro {{ background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 16px 18px; display: grid; gap: 10px; }}
.intro p, .intro ul {{ margin: 0; }}
.intro ul {{ padding-left: 1.2em; }}
.notes {{ background: var(--warn-soft); border-radius: 6px; padding: 14px 18px; }}
.notes h2 {{ font-size: 1rem; margin: 0 0 6px; color: var(--warn); }}
.notes ul {{ margin: 0; padding-left: 1.2em; }}
.q {{ background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 18px; display: grid; gap: 14px; }}
.q header {{ display: flex; gap: 12px; align-items: baseline; }}
.qid {{ font-family: var(--mono); font-size: .8rem; color: var(--accent); background: var(--accent-soft); padding: 2px 8px; border-radius: 4px; flex: none; }}
.q h2 {{ font-size: 1.08rem; margin: 0; font-weight: 600; text-wrap: balance; min-width: 0; }}
.ans {{ display: flex; flex-wrap: wrap; gap: 6px 14px; align-items: baseline; border-left: 3px solid var(--accent); padding-left: 12px; }}
.lbl, h3 {{ font-size: .75rem; letter-spacing: .06em; color: var(--muted); font-weight: 500; margin: 0 0 6px; }}
.lbl {{ margin: 0; }}
.num {{ font-family: var(--mono); font-size: 1.15rem; font-weight: 500; font-variant-numeric: tabular-nums; }}
.calc {{ font-family: var(--mono); font-size: .85rem; color: var(--muted); overflow-wrap: anywhere; }}
.cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.cols > section {{ min-width: 0; }}
@media (max-width: 720px) {{ .cols {{ grid-template-columns: 1fr; }} }}
.steps {{ margin: 0; padding-left: 1.3em; display: grid; gap: 4px; font-variant-numeric: tabular-nums; }}
.ev {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }}
.ev li {{ display: grid; grid-template-columns: auto 1fr; gap: 0 8px; }}
.ev a {{ color: var(--accent); font-weight: 500; }}
.rev {{ font-family: var(--mono); font-size: .75rem; color: var(--muted); align-self: center; }}
.ev q {{ grid-column: 1 / -1; font-family: var(--mono); font-size: .82rem; background: var(--bg); padding: 4px 8px; border-radius: 4px; overflow-wrap: anywhere; quotes: none; }}
a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
</style>
<div class="wrap">
  <div class="where">2단계 &gt; 도메인 다시 고르기(#6) &gt; 2. 질문 만들기 &gt; {e(NAME)}</div>
  <h1>{e(NAME)} 질문 {len(qs)}개</h1>
  <div class="intro">
    <p>후보 고르기 실험에 쓸 질문입니다. 모델에게는 질문만 보이고, 정답과 해설은 채점과 사용자 확인에만 씁니다. C(근거 글을 넣고 답)에서는 오른쪽 근거 글을 모델에게 줍니다.</p>
    <p><b>보실 것</b> 두 가지입니다.</p>
    <ul>
      <li>해설을 근거 글과 함께 따라갈 수 있는가</li>
      <li>단계가 지나치게 많은 질문이 없는가</li>
    </ul>
    <p>프로그램 검사(<code>src/domain_select/check_questions.py</code>)는 10개 모두 통과했습니다. 검사한 것: 근거 글이 받은 문서에 그대로 있는가, 계산식을 다시 하면 정답이 나오는가, 연산이 두 개 이상인가, 단위 바꾸기가 있는가.</p>
  </div>
{notes}
  {''.join(cards)}
</div>
"""
out = ROOT / "review.html"
out.write_text(page, encoding="utf-8")
print(out, len(page))
