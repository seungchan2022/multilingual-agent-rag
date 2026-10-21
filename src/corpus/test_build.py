"""변환(build.py)의 위첨자와 수식 시험. 네트워크를 쓰지 않는다.

  .venv/bin/python -m unittest discover -s src/corpus -p "test_*.py"

규칙은 decisions/stage2.md 2026-10-21 '세는 규칙 보완: 변환의 적는 방식과 세는 범위' 줄에 있다.
"""
import sys, unittest
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import convert_wiki, drop_all, inline, prepare, prune, render, walk  # noqa: E402


def math_span(tex, kind="inline", wrap=True):
    """위키백과의 수식 요소 모양: 숨긴 <math>와 그림."""
    alt = "{\\displaystyle " + tex + "}" if wrap else tex
    return (f'<span class="mwe-math-element mwe-math-element-{kind}">'
            f'<span class="mwe-math-mathml-{kind} mwe-math-mathml-a11y" style="display: none;">'
            f'<math alttext="{alt}"><semantics><mrow/></semantics></math></span>'
            f'<img src="x" class="mwe-math-fallback-image-{kind}" alt="{alt}"></span>')


def convert(body):
    """HTML 조각을 마크다운 줄들로. 정보 상자가 없는 문서의 길."""
    root = BeautifulSoup(f'<div class="mw-parser-output">{body}</div>', "html.parser").div
    prepare(root)
    drop_all(root)
    items = []
    walk(root, items)
    return render("T", [], prune(items)).split("\n", 2)[2].rstrip("\n")


def text_of(html):
    return inline(BeautifulSoup(f"<p>{html}</p>", "html.parser").p)


class Superscript(unittest.TestCase):
    def test_바꾼다(self):
        for html, want in [
            ("8.06×10<sup>24</sup> kg", "8.06×10²⁴ kg"),
            ("4f<sup>12</sup> 6s<sup>2</sup>", "4f¹² 6s²"),
            ("Er<sup>3+</sup>", "Er³⁺"),
            ("10<sup>−3</sup>", "10⁻³"),
            ("<sup>152m</sup>Eu", "¹⁵²ᵐEu"),
            ("km<sup>2</sup>", "km²"),
            ("1<sup>st</sup>", "1ˢᵗ"),
            ("a<sup>(n-1)=D</sup>", "a⁽ⁿ⁻¹⁾⁼ᴰ"),
        ]:
            self.assertEqual(text_of(html), want)

    def test_그대로_둔다(self):
        self.assertEqual(text_of("Bb<sup>†</sup>"), "Bb†")
        self.assertEqual(text_of("값<sup>가</sup>"), "값가")
        self.assertEqual(text_of("q<sup>q C</sup>"), "qq C")

    def test_아래첨자는_이어_붙인다(self):
        self.assertEqual(text_of("H<sub>2</sub>O"), "H2O")

    def test_지우는_것은_지운다(self):
        md = convert('<p>a<sup class="reference">[1]</sup>b<sup class="noprint">x</sup>c'
                     '<sup class="Inline-Template">y</sup>d<sup>2</sup></p>')
        self.assertEqual(md, "abcd²")

    def test_모든_자리(self):
        md = convert("<p>m 10<sup>2</sup></p>"
                     "<ul><li>목록 10<sup>3</sup></li></ul>"
                     "<dl><dd>dd 10<sup>4</sup></dd></dl>"
                     "<table><tr><th>머리 m<sup>2</sup></th></tr><tr><td>칸 10<sup>5</sup></td></tr></table>")
        for want in ["m 10²", "- 목록 10³", "dd 10⁴", "| 머리 m² |", "| 칸 10⁵ |"]:
            self.assertIn(want, md)

    def test_정보_상자_이름과_값(self):
        raw = ('<div class="mw-parser-output"><table class="infobox"><tr><th>밀도 g/cm<sup>3</sup></th>'
               '<td>5.5×10<sup>3</sup></td></tr></table><p>글</p></div>').encode("utf-8")
        self.assertIn("- 밀도 g/cm³: 5.5×10³", convert_wiki({"title": "T"}, raw))


class Formula(unittest.TestCase):
    def test_글_속_수식(self):
        m = math_span("\\alpha ")  # 위키백과의 alt는 {\displaystyle \alpha } 꼴이라 안쪽 끝 띄어쓰기가 남는다
        self.assertEqual(convert(f"<p>and ( {m} is negative</p>"), r"and ( \(\alpha \) is negative")

    def test_따로_선_수식(self):
        m = math_span(r"e={\sqrt {1+x}}", "block")
        md = convert(f"<p>given by</p><dl><dd>{m}</dd></dl>")
        self.assertIn(r"\[e={\sqrt {1+x}}\]", md)

    def test_껍데기만_벗긴다(self):
        m = math_span(r"{\scriptstyle a}+b")
        self.assertEqual(convert(f"<p>{m}</p>"), r"\({\scriptstyle a}+b\)")
        # 글 전체를 감싼 껍데기가 아니면 그대로 둔다
        m = math_span(r"{\displaystyle a}+{b}", wrap=False)
        self.assertEqual(convert(f"<p>{m}</p>"), r"\({\displaystyle a}+{b}\)")

    def test_그림의_alt를_쓴다(self):
        html = ('<p>x <span class="mwe-math-element mwe-math-element-inline">'
                '<img class="mwe-math-fallback-image-inline" alt="{\\displaystyle n}"></span> y</p>')
        self.assertEqual(convert(html), r"x \(n\) y")

    def test_TeX가_없으면_지워진다(self):
        html = '<p>x <span class="mwe-math-element mwe-math-element-inline"><img src="a"></span> y</p>'
        self.assertEqual(convert(html), "x y")

    def test_표_칸_목록_정보_상자(self):
        md = convert(f"<table><tr><th>a</th></tr><tr><td>{math_span('x|y')}</td></tr></table>"
                     f"<ul><li>목록 {math_span('z')}</li></ul>")
        self.assertIn(r"| \(x\|y\) |", md)  # 칸 안의 | 는 \| 로 바뀐다
        self.assertIn(r"- 목록 \(z\)", md)
        raw = (f'<div class="mw-parser-output"><table class="infobox"><tr><th>식</th><td>{math_span("E=mc^{2}")}</td></tr>'
               f'</table><p>글</p></div>').encode("utf-8")
        self.assertIn(r"- 식: \(E=mc^{2}\)", convert_wiki({"title": "T"}, raw))

    def test_수식_그림이_든_정보_상자_줄이_남는다(self):
        raw = (f'<div class="mw-parser-output"><table class="infobox"><tr><th>식</th><td>{math_span("a")}</td></tr>'
               f'</table><p>글</p></div>').encode("utf-8")
        self.assertIn(r"- 식: \(a\)", convert_wiki({"title": "T"}, raw))


class FetchDocs(unittest.TestCase):
    def test_to_markdown도_함께_바뀐다(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "domain_select"))
        from fetch_docs import to_markdown
        raw = (f'<div class="mw-parser-output"><p>10<sup>2</sup> {math_span("a")}</p></div>').encode("utf-8")
        self.assertIn(r"10² \(a\)", to_markdown("T", raw))


if __name__ == "__main__":
    unittest.main()
