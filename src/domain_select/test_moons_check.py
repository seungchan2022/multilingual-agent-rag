"""moons_check.py 시험. 네트워크를 쓰지 않는다."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import moons_check as mc


class Infobox(unittest.TestCase):
    def test_counts_only_th_td_rows(self):
        html = """<table class="infobox"><tr><th colspan=2>제목</th></tr>
        <tr><td colspan=2>그림</td></tr>
        <tr><th>반지름</th><td>198 km</td></tr>
        <tr><th>빈 값</th><td> </td></tr>
        <tr><th>중력</th><td>0.06 m/s</td></tr>
        <tr><th>안</th><td><table><tr><th>겹침</th><td>1</td></tr><tr><th>겹침2</th><td>2</td></tr></table></td></tr>
        </table>"""
        self.assertEqual([n for n, _ in mc.infobox_lines(html)], ["반지름", "중력", "안"])

    def test_no_infobox(self):
        self.assertEqual(mc.infobox_lines("<table class='wikitable'><tr><th>a</th><td>b</td></tr></table>"), [])


ROWS = "<tr><th>이름</th><th>크기</th></tr><tr><td>가</td><td>1</td></tr>"


class Pick(unittest.TestCase):
    def test_pick(self):
        html = f"""<table class="wikitable">{ROWS}</table>
        <table class="infobox"><tr><td>x</td><td>y</td></tr><tr><td>x</td><td>y</td>
          <td><table class="wikitable">{ROWS}</table></td></tr></table>
        <table class="plain">{ROWS}</table>
        <table class="wikitable"><tr><th>이름</th><th>크기</th></tr></table>
        <table class="sortable">{ROWS}</table>"""
        self.assertEqual(len(mc.pick_tables(html)), 2)


class Match(unittest.TestCase):
    def table(self, rows):
        html = "<table class='wikitable'>" + "".join(rows) + "</table>"
        return mc.pick_tables(html)[0]

    def test_name_boundary_and_number(self):
        t = self.table(["<tr><td>프레아</td><td>12</td></tr>",
                        "<tr><td>레아</td><td>527 km</td></tr>",
                        "<tr><td>미마스 (위성)</td><td>없음</td></tr>",
                        "<tr><td>미란다 12</td><td>-</td></tr>"])
        self.assertEqual(list(mc.match_rows(t, ["레아", "미마스", "미란다"])), ["레아"])


if __name__ == "__main__":
    unittest.main()
