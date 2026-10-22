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


class InfoboxImage(unittest.TestCase):
    """정보 상자의 그림: 이름표와 값의 줄은 그림만 지우고, 다른 모양의 줄은 줄째로 지운다."""

    def box(self, row):
        raw = ('<div class="mw-parser-output"><table class="infobox"><tr><th>Density</th><td>8.54 g/cm³</td></tr>'
               + row + '</table><p>글</p></div>').encode("utf-8")
        md = convert_wiki({"title": "T"}, raw)
        self.assertIn("- Density: 8.54 g/cm³", md)  # 상자 자체가 읽힌다
        self.assertIn("글", md)
        return md

    def test_영어_격자_상수는_줄을_남긴다(self):
        md = self.box('<tr><th>Lattice constants</th><td><div style="float:right;"><span typeof="mw:File/Frameless">'
                      '<a href="/wiki/File:X.svg"><img alt="Hexagonal close packed crystal structure for dysprosium" src="x"></a>'
                      '</span></div><i>a</i>&#160;=&#160;359.16&#160;pm<br /><i>c</i>&#160;=&#160;565.01&#160;pm (at&#160;20&#160;°C)'
                      '<sup class="reference"><a href="#c">[3]</a></sup></td></tr>')
        self.assertIn("- Lattice constants: a = 359.16 pm / c = 565.01 pm (at 20 °C)", md)
        self.assertNotIn("Hexagonal close packed", md)
        self.assertNotIn("[3]", md)

    def test_한국어_전자껍질은_그림과_설명을_지운다(self):
        md = self.box('<tr><th>준위별 전자 수</th><td>2, 8, 18, 31, 8, 2<div><figure typeof="mw:File">'
                      '<a href="/wiki/x" title="툴륨의 전자껍질 (2, 8, 18, 31, 8, 2)">'
                      '<img alt="툴륨의 전자껍질 (2, 8, 18, 31, 8, 2)" src="x"></a>'
                      '<figcaption>툴륨의 전자껍질 (2, 8, 18, 31, 8, 2)</figcaption></figure></div></td></tr>')
        self.assertIn("- 준위별 전자 수: 2, 8, 18, 31, 8, 2", md)
        self.assertNotIn("전자껍질", md)

    def test_한국어_결정_구조는_값_사이의_그림만_지운다(self):
        md = self.box('<tr><th>결정 구조</th><td>조밀&#160;육방&#160;격자 (hcp)\n<div style="float:right;">'
                      '<span typeof="mw:File"><a href="/wiki/x"><img src="x"></a></span></div>'
                      '&#x20;(<a href="/wiki/y">hP2</a>)</td></tr>')
        self.assertIn("- 결정 구조: 조밀 육방 격자 (hcp) (hP2)", md)

    def test_칸_하나인_사진_줄은_줄째로_지운다_영어(self):
        md = self.box('<tr><td colspan="2"><span typeof="mw:File"><a href="/wiki/x"><img src="x"></a></span>'
                      '<div class="infobox-caption">Artist\'s impression of KELT-9b</div></td></tr>')
        self.assertNotIn("Artist's impression", md)

    def test_칸_하나인_사진_줄은_줄째로_지운다_한국어(self):
        md = self.box('<tr><td colspan="2"><span typeof="mw:File"><a href="/wiki/x"><img src="x"></a></span>'
                      '<br>글리제 436 b의 상상도.</td></tr>')
        self.assertNotIn("상상도", md)

    def test_값_칸에_그림만_있는_줄은_없다(self):
        md = self.box('<tr><th>Flag</th><td><span typeof="mw:File"><a href="/wiki/x">'
                      '<img alt="Flag of X" src="x"></a></span></td></tr>')
        self.assertNotIn("Flag", md)

    def test_정보_상자_맨_아래_보기_토론_편집_줄은_지운다(self):
        md = self.box('<tr><td class="infobox-below noprint" colspan="2"><span class="noprint">보기</span>'
                      '<span> | 출처</span></td></tr>')
        self.assertNotIn("출처", md)


def box_md(rows):
    """정보 상자 줄들을 문서 앞에 둔 마크다운. 첫 줄 '# T'와 뒤의 본문 '글' 사이가 정보 상자와 표다."""
    raw = f'<div class="mw-parser-output"><table class="infobox">{rows}</table><p>글</p></div>'.encode("utf-8")
    return convert_wiki({"title": "T"}, raw)


def swatches(n, names="X"):
    """주기율표 그림의 원소 칸 n개: 글자색이 투명한 span이 든 링크."""
    return "".join(f'<td><a href="/wiki/{names}{i}" title="{names}{i}"><span style="display:block;width:6px;height:8px;'
                   f'overflow:hidden;padding:0;color:transparent;background-color:#ff9999;">{names}{i}</span></a></td>'
                   for i in range(n))


VAPOR = ('<tr><td colspan="2"><b>증기 압력</b><div><table class="wikitable">'
         '<tr><th>압력 (Pa)</th><th>1</th><th>10</th></tr>'
         '<tr><th>온도 (K)</th><td>1117</td><td>1235</td></tr></table></div></td></tr>')


class InfoboxPeriodicTable(unittest.TestCase):
    """주기율표 그림 줄: 원소 칸(글자색이 투명한 span)이 100개 이상 든 줄만 지우고 묶음 제목과 다른 줄은 둔다."""

    def test_한국어_겹친_격자(self):
        grid = (f'<table class="wikitable"><tr><td><table style="border:none"><tr>{swatches(118, "원소")}</tr></table>'
                '</td></tr></table>')
        md = box_md(f'<tr><th class="infobox-header" colspan="2">주기율표 정보</th></tr><tr><td colspan="2">{grid}</td></tr>'
                    '<tr><th>원자 번호</th><td>69</td></tr>')
        self.assertEqual(md, "# T\n\n- 주기율표 정보\n  - 원자 번호: 69\n\n글\n")

    def test_영어_div_안의_표(self):
        grid = (f'<div class="ib-element-periodic-table"><table class="periodic-table-32-micro"><tr>{swatches(118)}</tr>'
                '</table></div>')
        md = box_md(f'<tr><th class="infobox-header" colspan="2">Thulium in the periodic table</th></tr><tr><td colspan="2">{grid}</td></tr>'
                    '<tr><th>Atomic number</th><td>69</td></tr>')
        self.assertEqual(md, "# T\n\n- Thulium in the periodic table\n  - Atomic number: 69\n\n글\n")

    def test_원소_칸이_적으면_지우지_않는다(self):
        md = box_md(f'<tr><th class="infobox-header" colspan="2">묶음</th></tr><tr><td colspan="2"><table><tr>{swatches(5)}</tr></table></td></tr>')
        self.assertIn("X0", md)


class InfoboxNestedTable(unittest.TestCase):
    """정보 상자 줄 안의 자료 표는 마크다운 표가 된다. 표 앞에 이름 줄, 표 앞뒤는 빈 줄, 목록은 표 뒤에서 이어진다."""

    def test_이름_줄_다음에_표가_오고_목록이_이어진다(self):
        md = box_md('<tr><th class="infobox-header" colspan="2">물리적 성질</th></tr><tr><th>녹는점</th><td>1818 K</td></tr>' + VAPOR
                    + '<tr><th>밀도</th><td>9.32</td></tr><tr><th class="infobox-header" colspan="2">원자의 성질</th></tr><tr><th>산화 상태</th><td>3</td></tr>')
        self.assertEqual(md, "# T\n\n- 물리적 성질\n  - 녹는점: 1818 K\n  - 증기 압력\n\n"
                             "| 압력 (Pa) | 1 | 10 |\n|---|---|---|\n| 온도 (K) | 1117 | 1235 |\n\n"
                             "  - 밀도: 9.32\n- 원자의 성질\n  - 산화 상태: 3\n\n글\n")

    def test_묶음_제목이_표의_이름이다(self):
        md = box_md('<tr><th class="infobox-header" colspan="2">주요 동위원소</th></tr><tr><td colspan="2"><table class="wikitable">'
                    '<tr><th>동위체</th><th>반감기</th></tr><tr><td>¹⁶⁷Tm</td><td>9.25 d</td></tr></table></td></tr>')
        self.assertEqual(md, "# T\n\n- 주요 동위원소\n\n| 동위체 | 반감기 |\n|---|---|\n| ¹⁶⁷Tm | 9.25 d |\n\n글\n")

    def test_이름_줄이_없는_첫_줄의_표(self):
        md = box_md('<tr><td colspan="2"><table class="wikitable"><tr><th>a</th><th>b</th></tr>'
                    '<tr><td>1</td><td>2</td></tr></table></td></tr><tr><th>밀도</th><td>9</td></tr>')
        self.assertEqual(md, "# T\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n- 밀도: 9\n\n글\n")

    def test_한_줄짜리_배치용_표는_글자로_둔다(self):
        md = box_md('<tr><td colspan="2"><table class="infobox-subbox"><tr><td colspan="2"><b>스펙트럼 선</b></td></tr>'
                    '</table></td></tr>')
        self.assertEqual(md, "# T\n\n- 스펙트럼 선\n\n글\n")


class ValueBreak(unittest.TestCase):
    """값 칸(td)의 <br>은 ' / '다. 머리글 칸(th)과 괄호뿐인 조각 옆, 값 칸 밖의 <br>은 빈칸 하나다."""

    def test_값_칸의_줄바꿈은_슬래시다(self):
        md = box_md('<tr><th>원자 반지름</th><td>0.48<br>0.38D</td></tr>')
        self.assertIn("- 원자 반지름: 0.48 / 0.38D", md)

    def test_표의_값_칸도_슬래시다(self):
        md = convert('<table><tr><th>a</th><th>b</th></tr><tr><td>x<br>y</td><td>z</td></tr></table>')
        self.assertIn("| x / y | z |", md)

    def test_정보_상자_안_표의_값_칸도_슬래시다(self):
        md = box_md('<tr><td colspan="2"><table class="wikitable"><tr><th>a</th><th>b</th></tr>'
                    '<tr><td>1<br>2</td><td>3</td></tr></table></td></tr>')
        self.assertIn("| 1 / 2 | 3 |", md)

    def test_머리글_칸의_줄바꿈은_빈칸이다(self):
        md = box_md('<tr><th>동위체<br>번호</th><td>1</td></tr>')
        self.assertIn("- 동위체 번호: 1", md)

    def test_값_칸_안_표의_머리글_칸은_빈칸이다(self):
        md = box_md('<tr><td colspan="2"><table class="wikitable"><tr><th>DE<br>(MeV)</th><th>b</th></tr>'
                    '<tr><td>1<br>2</td><td>3</td></tr></table></td></tr>')
        self.assertIn("| DE (MeV) | b |", md)
        self.assertIn("| 1 / 2 | 3 |", md)

    def test_앞_조각이_괄호뿐이면_빈칸이다(self):
        md = box_md('<tr><th>밀도</th><td>(실온) (poly)<br>8.5</td></tr>')
        self.assertIn("- 밀도: (실온) (poly) 8.5", md)

    def test_뒤_조각이_괄호뿐이면_빈칸이다(self):
        md = box_md('<tr><th>산화 상태</th><td>3<br>(염기성 산화물)</td></tr>')
        self.assertIn("- 산화 상태: 3 (염기성 산화물)", md)

    def test_값_칸_밖의_줄바꿈은_빈칸이다(self):
        self.assertEqual(convert('<p>La<br>2O<br>3</p>'), "La 2O 3")


class ChemicalFormula(unittest.TestCase):
    """화학식 틀(.chemf) 안의 <br>은 없앤다. 첨자를 위아래로 쌓은 줄바꿈이라 빈칸이 되면 원소 기호에서 떨어진다."""

    STACK = '<span class="nowrap"><span style="display:inline-block;"><sup>{sup}</sup><br /><sub>{sub}</sub></span></span>'

    def test_쌓은_아래첨자는_원소_기호에_붙는다(self):
        stack = self.STACK.format(sup="", sub="2")
        md = convert(f'<p>oxide <span class="chemf nowrap">La{stack}O<sub>3</sub></span>, ok</p>')
        self.assertEqual(md, "oxide La2O3, ok")

    def test_쌓은_위첨자는_원소_기호에_붙는다(self):
        stack = self.STACK.format(sup="3+", sub="")
        md = convert(f'<p>ion <span class="chemf nowrap">La{stack}</span>.</p>')
        self.assertEqual(md, "ion La³⁺.")

    def test_질량수_위첨자는_앞에서_붙는다(self):
        stack = self.STACK.format(sup="139", sub="")
        md = convert(f'<p><span class="chemf nowrap">{stack}La</span> is stable</p>')
        self.assertEqual(md, "¹³⁹La is stable")

    def test_화학식_밖의_줄바꿈은_빈칸이다(self):
        self.assertEqual(convert('<p>La<br>2O</p>'), "La 2O")

    def test_값_칸_안의_화학식도_값_칸_규칙보다_먼저_없앤다(self):
        stack = self.STACK.format(sup="", sub="2")
        md = box_md(f'<tr><th>산화물</th><td><span class="chemf">La{stack}O<sub>3</sub></span></td></tr>')
        self.assertIn("- 산화물: La2O3", md)


class InfoboxNavbar(unittest.TestCase):
    def test_묶음_제목의_v_e를_지운다(self):
        md = box_md('<tr><th class="infobox-header"><a href="/wiki/Isotopes_of_thulium">Isotopes of thulium</a>'
                    '<div style="float:right"><div class="navbar plainlinks hlist navbar-mini"><ul>'
                    '<li class="nv-view"><a href="/wiki/Template:X"><abbr title="View this template">v</abbr></a></li>'
                    '<li class="nv-edit"><a href="/wiki/Special:EditPage/Template:X"><abbr title="Edit this template">e</abbr></a></li>'
                    '</ul></div></div></th></tr><tr><th>Mass</th><td>169</td></tr>')
        self.assertEqual(md, "# T\n\n- Isotopes of thulium\n  - Mass: 169\n\n글\n")


class EmptyColumn(unittest.TestCase):
    """값 칸(td)이 모두 빈 열은 머리글까지 지운다. th는 값으로 세지 않는다."""

    def test_빈_열을_지운다(self):
        md = convert("<table><tr><th>이름</th><th>비고</th><th>값</th></tr>"
                     "<tr><td>a</td><td></td><td>1</td></tr><tr><td>b</td><td></td><td>2</td></tr></table>")
        self.assertEqual(md, "| 이름 | 값 |\n|---|---|\n| a | 1 |\n| b | 2 |")

    def test_값이_하나라도_있는_열은_남긴다(self):
        md = convert("<table><tr><th>이름</th><th>비고</th></tr>"
                     "<tr><td>a</td><td></td></tr><tr><td>b</td><td>x</td></tr></table>")
        self.assertEqual(md, "| 이름 | 비고 |\n|---|---|\n| a |  |\n| b | x |")

    def test_머리글을_되풀이한_th_칸의_글자는_값이_아니다(self):
        md = convert('<table><tr><th>이름</th><th>값</th><th rowspan="2">비고</th></tr><tr><th colspan="2">세부</th></tr>'
                     "<tr><td>a</td><td>1</td><td></td></tr></table>")
        self.assertEqual(md, "| 이름 | 값 |\n|---|---|\n| 세부 | 세부 |\n| a | 1 |")

    def test_줄_이름표_열은_남긴다(self):
        md = convert("<table><tr><th>구분</th><th>1</th></tr><tr><th>온도</th><td>9</td></tr></table>")
        self.assertEqual(md, "| 구분 | 1 |\n|---|---|\n| 온도 | 9 |")


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


class NoInfobox(unittest.TestCase):
    def test_정보_상자가_없으면_본문만_옮긴다(self):
        raw = '<div class="mw-parser-output"><p>글</p><h2>절</h2><p>내용</p></div>'.encode("utf-8")
        self.assertEqual(convert_wiki({"title": "T"}, raw), "# T\n\n글\n\n## 절\n\n내용\n")


class FetchDocs(unittest.TestCase):
    def test_to_markdown도_함께_바뀐다(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "domain_select"))
        from fetch_docs import to_markdown
        raw = (f'<div class="mw-parser-output"><p>10<sup>2</sup> {math_span("a")}</p></div>').encode("utf-8")
        self.assertIn(r"10² \(a\)", to_markdown("T", raw))


if __name__ == "__main__":
    unittest.main()
