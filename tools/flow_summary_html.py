#!/usr/bin/env python3
"""흐름 요약 마크다운을 읽어 견본과 같은 모양의 HTML 한 파일로 바꾼다.

실행: python3 tools/flow_summary_html.py history/stage1/1-evaluation-frame.md
양식의 정의: .claude/skills/flow-summary/SKILL.md 의 "마크다운 양식"
"""
import re
import sys
from pathlib import Path

STYLE = r"""*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --desk:#b9bfca;--paper:#e6e9ee;--paper-2:#d9dde4;--card:#ffffff;--ink:#1f2230;--muted:#3b4558;--soft:#59627a;
  --rule:rgba(45,49,66,.20);--accent:#eb6c36;--accent-tint:rgba(235,108,54,.10);
  --link:#2e5aa8;--link-tint:rgba(46,90,168,.10);--slate-tint:rgba(79,93,117,.12);
  --sans:-apple-system,'Apple SD Gothic Neo','Pretendard','Noto Sans KR',system-ui,sans-serif;
  --mono:ui-monospace,'SF Mono',Menlo,monospace;
}
body{font-family:var(--sans);background:var(--desk);color:var(--ink);line-height:1.75;font-size:16px;-webkit-text-size-adjust:100%}
main{max-width:680px;margin:0 auto;padding:28px 16px 64px;background:var(--paper)}
@media(min-width:720px){body{padding:32px 16px}main{padding:40px 36px 64px;border-radius:12px;border:1px solid var(--rule)}}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.14em;color:var(--muted);margin-bottom:8px}
h1{font-size:28px;line-height:1.25;font-weight:700;letter-spacing:-.02em;margin-bottom:8px}
.meta{font-size:13px;color:var(--soft);margin-bottom:16px}
.lead{font-size:16px;margin-bottom:12px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin:20px 0 8px}
.stat{background:var(--card);border:1px solid var(--rule);border-radius:8px;padding:12px;min-width:0;overflow-wrap:anywhere}
.stat b{display:block;font-size:24px;line-height:1.2}
.stat span{font-size:12px;line-height:1.5;display:block;color:var(--muted)}
h2{font-size:20px;line-height:1.3;margin:40px 0 4px;padding-top:16px;border-top:1px solid var(--rule)}
h2 small{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.12em;color:var(--soft);font-weight:500;margin-bottom:4px}
.sub{font-size:14px;color:var(--muted);margin-bottom:12px}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0}
.toc a{font-size:13px;color:var(--ink);text-decoration:none;border:1px solid var(--rule);background:var(--card);border-radius:999px;padding:4px 12px}
.tools{display:flex;justify-content:flex-end;margin:12px 0}
button{font:inherit;font-size:13px;color:var(--muted);background:none;border:1px solid var(--rule);border-radius:6px;padding:4px 12px}
figure{margin:16px 0}
figure svg{width:100%;max-width:560px;height:auto;display:block;margin:0 auto}
figcaption{font-size:13px;color:var(--muted);margin-top:8px}
details.card{background:var(--card);border:1px solid var(--rule);border-radius:8px;margin:8px 0}
details.card>summary{list-style:none;cursor:pointer;padding:12px 40px 12px 16px;position:relative}
details.card>summary::-webkit-details-marker{display:none}
details.card>summary::after{content:"+";position:absolute;right:16px;top:10px;font-size:20px;color:var(--soft)}
details.card[open]>summary::after{content:"\2212"}
.t{display:block;font-weight:700;font-size:16px;line-height:1.4}
.gist{display:block;font-size:14px;color:var(--muted);margin-top:4px}
.tag{display:inline-block;font-size:11px;font-weight:600;border-radius:4px;padding:1px 8px;margin-bottom:4px}
.tag.user{background:var(--accent-tint);color:#b54a1c}
.tag.codex{background:var(--link-tint);color:var(--link)}
.tag.check{background:var(--slate-tint);color:var(--muted)}
.body{padding:4px 16px 16px;border-top:1px solid var(--rule)}
.steps{list-style:none;margin:12px 0 4px;border-left:2px solid var(--rule);padding-left:16px}
.steps li{position:relative;padding:4px 0 10px;font-size:15px}
.steps li::before{content:"";position:absolute;left:-22px;top:12px;width:10px;height:10px;border-radius:50%;background:var(--card);border:2px solid var(--soft)}
.steps li.snag::before{border-color:var(--accent)}
.steps li.done::before{background:var(--ink);border-color:var(--ink)}
.steps b,.rows dt{display:block;font-size:12px;letter-spacing:.04em;color:var(--soft);font-weight:600}
.steps li.snag b{color:#b54a1c}
.rows{margin-top:12px}
.rows dd{font-size:15px;margin-bottom:10px}
.ex{background:var(--paper);border-radius:6px;padding:12px 14px;font-size:14px;margin-top:8px}
.ex b{font-size:12px;color:var(--soft);display:block}
.scroll{overflow-x:auto;margin:12px 0}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card)}
th,td{border:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:top}
th{font-size:12px;color:var(--muted);background:var(--paper-2);white-space:nowrap}
ul.plain{margin:8px 0 0 22px;font-size:15px}
ul.plain li{margin-bottom:6px}
.again{display:grid;gap:8px;margin-top:12px}
.again div{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--accent);border-radius:6px;padding:10px 12px}
.again div.rec{border-left-color:var(--soft)}
.again strong{display:block;font-size:15px}
.again span{display:block;font-size:14px;color:var(--muted)}
.again em{font-style:normal;font-size:12px;color:var(--soft)}
code{font-family:var(--mono);font-size:.88em;background:var(--paper-2);border-radius:4px;padding:1px 4px}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--rule);font-size:13px;color:var(--soft)}
footer a{color:var(--link)}
@media print{body,main{background:#fff}main{border:0}details.card{break-inside:avoid}.tools,.toc{display:none}}
"""

SCRIPT = r"""(function(){
  var cards=document.querySelectorAll('details.card'),btn=document.getElementById('toggle'),open=false;
  function set(v){cards.forEach(function(d){d.open=v});open=v;btn.textContent=v?'모두 접기':'모두 펼치기'}
  btn.addEventListener('click',function(){set(!open)});
  window.addEventListener('beforeprint',function(){set(true)});
})();
"""

LABEL = re.compile(r"^\*\*(.+?)\*\*:\s*(.*)$")


def warn(n, text):
    print(f"경고: {n}번째 줄이 양식에 없다: {text}", file=sys.stderr)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    """`코드`, **굵게**, [글](주소)만 바꾸고 나머지는 이스케이프한다."""
    stash = []

    def keep(m):
        stash.append("<code>" + esc(m.group(1)) + "</code>")
        return f"\x00{len(stash) - 1}\x00"

    s = esc(re.sub(r"`([^`]+)`", keep, s))
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)


def tokenize(lines):
    """줄을 (종류, 줄 번호, 값) 토막으로 나눈다."""
    toks, i = [], 0
    while i < len(lines):
        s, n = lines[i], i + 1
        if not s.strip():
            i += 1
        elif re.match(r"#{1,6} ", s):
            level = len(s) - len(s.lstrip("#"))
            toks.append((f"h{level}", n, s[level:].strip()))
            i += 1
        elif s.startswith("```"):
            body, i = [], i + 1
            lang = s[3:].strip()
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            toks.append(("fence", n, (lang, body)))
            i += 1
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            toks.append(("table", n, rows))
        elif s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append((i + 1, lines[i][2:].strip()))
                i += 1
            toks.append(("list", n, items))
        elif s.startswith("> "):
            toks.append(("quote", n, s[2:].strip()))
            i += 1
        else:
            para = [s.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"(#|```|\||- |> )", lines[i]):
                para.append(lines[i].strip())
                i += 1
            toks.append(("para", n, " ".join(para)))
    return toks


def odd(n, text):
    """양식에 없는 줄: 경고하고 sub 문단으로 넣는다."""
    warn(n, text)
    return f'<p class="sub">{inline(text)}</p>'


def table_html(rows):
    out = ['<div class="scroll"><table>']
    for k, row in enumerate(rows):
        tag = "th" if k == 0 else "td"
        out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in row) + "</tr>")
    out.append("</table></div>")
    return "\n".join(out)


def again_html(rows):
    out = ['<div class="again">']
    for name, state, where in rows[1:]:
        out.append(f"<div><strong>{inline(name)}</strong><span>{inline(state)}</span>"
                   f"<em>쓰이는 곳: {inline(where)}</em></div>")
    out.append("</div>")
    return "\n".join(out)


def stats_html(rows):
    out = ['<div class="stats">']
    for label, value in rows[1:]:
        m = re.match(r"^(.*?)\s*\((.*)\)\s*$", value)
        if m:
            out.append(f'<div class="stat"><b>{inline(m.group(1))}</b>'
                       f"<span>{inline(label)}<br>{inline(m.group(2))}</span></div>")
        else:
            out.append(f'<div class="stat"><b>{inline(value)}</b><span>{inline(label)}</span></div>')
    out.append("</div>")
    return "\n".join(out)


def is_step(label):
    return label.startswith("처음") or label in ("걸린 것", "정한 것") or "변경" in label


def card_list(items):
    parsed = [(n, LABEL.match(t), t) for n, t in items]
    if not any(m for _, m, _ in parsed):
        return '<ul class="plain">' + "".join(f"<li>{inline(t)}</li>" for _, _, t in parsed) + "</ul>"
    out, rows, k = [], [], 0

    def flush():
        if rows:
            out.append('<dl class="rows">' + "".join(rows) + "</dl>")
            rows.clear()

    if parsed[0][1] and parsed[0][1].group(1).startswith("처음"):
        steps = []
        while k < len(parsed) and parsed[k][1] and is_step(parsed[k][1].group(1)):
            steps.append(parsed[k][1])
            k += 1
        lis = []
        for j, m in enumerate(steps):
            cls = "" if j == 0 else ' class="done"' if j == len(steps) - 1 else ' class="snag"'
            lis.append(f"<li{cls}><b>{inline(m.group(1))}</b>{inline(m.group(2))}</li>")
        out.append('<ol class="steps">' + "".join(lis) + "</ol>")
    for n, m, t in parsed[k:]:
        if not m:
            flush()
            out.append(odd(n, t))
        elif m.group(1) == "예":
            flush()
            out.append(f'<p class="ex"><b>예</b>{inline(m.group(2))}</p>')
        else:
            rows.append(f"<dt>{inline(m.group(1))}</dt><dd>{inline(m.group(2))}</dd>")
    flush()
    return "\n".join(out)


def plain_html(toks):
    """번호 없는 절(과 번호 절의 카드 앞 부분)의 내용."""
    out = []
    for kind, n, v in toks:
        if kind == "para":
            out.append(f'<p class="sub">{inline(v)}</p>')
        elif kind == "list":
            out.append('<ul class="plain">' + "".join(f"<li>{inline(t)}</li>" for _, t in v) + "</ul>")
        elif kind == "table":
            again = [c.strip() for c in v[0]] == ["내용", "상태", "쓰이는 곳"]
            out.append(again_html(v) if again else table_html(v))
        else:
            out.append(odd(n, f"({kind}) " + str(v)))
    return "\n".join(out)


def card_html(title, toks):
    m = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", title)
    tags = []
    if m:
        title = m.group(1)
        for tag in (t.strip() for t in m.group(2).split(",")):
            cls = "user" if tag.startswith("사용자") else "codex" if tag.startswith("Codex") else "check"
            tags.append(f'<span class="tag {cls}">{inline(tag)}</span>')
    gist, body = "", []
    for tok in toks:
        if tok[0] == "quote" and not gist:
            gist = tok[2]
        elif tok[0] == "list":
            body.append(card_list(tok[2]))
        elif tok[0] == "table":
            body.append(table_html(tok[2]))
        else:
            body.append(odd(tok[1], str(tok[2])))
    if not gist:
        warn(0, f"카드 '{title}'에 한 줄 결론(> 줄)이 없다")
    return ('<details class="card">\n  <summary>' + " ".join(tags) + f'<span class="t">{inline(title)}</span>'
            f'<span class="gist">{inline(gist)}</span></summary>\n  <div class="body">'
            + "\n".join(body) + "</div>\n</details>")


def flow_html(toks, svg_path):
    out = ["<figure>"]
    for kind, n, v in toks:
        if kind == "fence" and v[0] == "mermaid":
            if svg_path.exists():
                out.append(svg_path.read_text(encoding="utf-8").strip())
            else:
                print(f"경고: {svg_path} 가 없어 Mermaid 코드를 그대로 넣는다", file=sys.stderr)
                out.append("<pre>" + esc("\n".join(v[1])) + "</pre>")
        elif kind == "para":
            out.append(f"<figcaption>{inline(v)}</figcaption>")
        else:
            out.append(odd(n, f"({kind}) " + str(v)))
    out.append("</figure>")
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        sys.exit("사용법: python3 tools/flow_summary_html.py <흐름 요약 .md>")
    src = Path(sys.argv[1])
    toks = tokenize(src.read_text(encoding="utf-8").split("\n"))
    m = re.match(r"^(\d+)단계 흐름 요약: (.+)$", toks[0][2]) if toks and toks[0][0] == "h1" else None
    if not m:
        sys.exit("첫 줄이 '# N단계 흐름 요약: 이름' 꼴이 아니다")
    stage, name = m.group(1), m.group(2)

    head, secs = [], []
    for t in toks[1:]:
        if t[0] == "h2":
            secs.append((t, []))
        elif secs:
            secs[-1][1].append(t)
        else:
            head.append(t)

    parts = [f'<p class="eyebrow">{stage}단계 · 흐름 요약</p>', f"<h1>{inline(name)}</h1>"]
    paras = 0
    for kind, n, v in head:
        if kind == "para" and paras == 0:
            parts.append(f'<p class="meta">{inline(v)}</p>')
        elif kind == "para" and paras == 1:
            parts.append(f'<p class="lead">{inline(v)}</p>')
        elif kind == "para":
            parts.append(f'<p class="sub">{inline(v)}</p>')
        elif kind == "table":
            parts.append(stats_html(v))
        else:
            parts.append(odd(n, f"({kind}) " + str(v)))
        paras += kind == "para"

    toc = []
    for i, ((_, _, title), _) in enumerate(secs, 1):
        mm = re.match(r"^(\d+)\.\s+(.*)$", title)
        toc.append(f'<a href="#sec-{i}">{inline((mm.group(1) + " " + mm.group(2)) if mm else title)}</a>')
    parts.append('<nav class="toc">\n  ' + "".join(toc) + "\n</nav>")

    tools_done = False
    for i, ((_, n, title), body) in enumerate(secs, 1):
        mm = re.match(r"^(\d+)\.\s+(.*)$", title)
        if mm:
            if not tools_done:
                parts.append('<div class="tools"><button type="button" id="toggle">모두 펼치기</button></div>')
                tools_done = True
            parts.append(f'<h2 id="sec-{i}"><small>{int(mm.group(1)):02d}</small>{inline(mm.group(2))}</h2>')
            first = next((k for k, t in enumerate(body) if t[0] == "h3"), len(body))
            parts.append(plain_html(body[:first]))
            cards = body[first:]
            starts = [k for k, t in enumerate(cards) if t[0] == "h3"] + [len(cards)]
            for a, b in zip(starts, starts[1:]):
                parts.append(card_html(cards[a][2], cards[a + 1:b]))
            continue
        parts.append(f'<h2 id="sec-{i}">{inline(title)}</h2>')
        if title == "흐름":
            parts.append(flow_html(body, src.with_name(src.stem + "-flow.svg")))
        elif title == "원본":
            foot = ["<footer>", "  <p>원본</p>"]
            for kind, n, v in body:
                if kind == "list":
                    foot += [f"  <p>{inline(t)}</p>" for _, t in v]
                else:
                    foot.append(odd(n, f"({kind}) " + str(v)))
            parts.append("\n".join(foot + ["</footer>"]))
        else:
            parts.append(plain_html(body))

    page = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            f"<title>{stage}단계 흐름 요약: {esc(name)}</title>\n<style>\n{STYLE}</style>\n</head>\n<body>\n<main>\n\n"
            + "\n\n".join(p for p in parts if p) + f"\n\n</main>\n<script>\n{SCRIPT}</script>\n</body>\n</html>\n")
    out = src.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
