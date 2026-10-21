"""마크다운 글에서 숫자를 읽는 규칙(decisions/stage2.md 2026-10-21 "세는 규칙 보완의 방향" 줄 ㉡, "세는 규칙 보완: 변환의 적는 방식과
세는 범위" 줄 ㉢㉣). 옛 규칙 round3_measure.py의 extract를 대신할 새 규칙이다. 옛 규칙은 지난 결과를 다시 만들 수 있게 그대로 둔다.

  read(text)            글에 나온 숫자마다 항목 하나를 글에 나온 차례로 돌려준다.
  quantities(text)      read 가운데 kind가 "양"인 항목만.
  unknown_digits(text)  kind가 "모르는 숫자"인 항목의 digits 집합.
  close(a, b)           두 기준 값이 큰 쪽의 1% 안인가.
  group(items)          한 언어 문서들의 양 항목을 같은 차원·1% 안 값끼리 묶는다.
  judge(groups, other)  묶음마다 반대 언어 문서들에 있는지(있음, 있을 수 있음, 그 언어에만) 판정을 단다.

항목은 dict다. 공통 칸: kind("양", "모르는 숫자", "비율", "날짜", "이름"), raw(항목이 차지한 글자 그대로), start·end(text 안의 위치),
line(0부터 센 줄 번호). "양"은 value(적힌 값), unit(적힌 단위 글자), dim(차원), base(기준 단위로 바꾼 값), how(단위를 어디서 얻었나:
"뒤", "앞", "이름 칸", "머리글", "여러 칸")와 digits(적힌 값의 숫자 글자 목록: 지수는 앞의 수, 큰 수 낱말은 낱말 앞의 수마다, 여러 칸은 칸마다)를 더 갖고,
"모르는 숫자"는 digits(쉼표와 묶음 공백을 지운 숫자 글자 하나)를 더 갖는다.
이 단계에서는 값을 읽기만 한다. 반대 언어에 같은 값이 있는지 보는 일은 하지 않는다.

읽는 방법은 읽는 쪽 규칙에 쓴 대로다. 단위 목록에 없는 단위는 읽지 않고(그 숫자는 모르는 숫자), 규칙에 없는 모양을 만나도 규칙을
늘리지 않는다. 숫자 글자 하나는 항목 하나에만 든다.
"""
import bisect
import re

SKIP = frozenset("​‌‍⁠﻿­")     # 없는 것으로 보고 건너뛰는 글자(마지막은 round4_corpus_check.SENT)
SP = "    "                                          # 숫자와 단위 사이에 올 수 있는 한 칸
GROUP_SP = "   "                                     # 세 자리 묶음을 가르는 공백(보통 띄어쓰기는 묶음이 아니다)

# --- 단위 표 -----------------------------------------------------------------
# 표기 -> (차원, 기준 단위로 바꾸는 곱). 기준 단위: 길이 m, 질량 kg, 시간 s, 속도 m/s, 가속도 m/s², 넓이 m², 부피 m³, 밀도 kg/m³,
# 압력 Pa, 에너지 J, 몰 에너지 J/mol, 출력 W, 온도 K(섭씨와 화씨는 따로 바꾼다), 각도 °, 진동수 Hz, 몰 질량 kg/mol, 열전도율 W/(m·K),
# 몰 열용량 J/(mol·K), 비열 J/(kg·K), 비저항 Ω·m, 열팽창 1/K. 가운뎃점(· ⋅ ∙)과 µ·μ는 같은 글자로 본다(norm).
UNITS = {}


def _add(dim, factor, *names):
    for n in names:
        UNITS[n] = (dim, factor)


_add("길이", 1, "m", "미터")
_add("길이", 1e3, "km", "킬로미터")
_add("길이", 1e-2, "cm", "센티미터")
_add("길이", 1e-3, "mm", "밀리미터")
_add("길이", 1e-6, "µm", "마이크로미터")
_add("길이", 1e-9, "nm", "나노미터")
_add("길이", 1e-12, "pm", "피코미터")
_add("길이", 1e-10, "Å", "옹스트롬")
_add("길이", 1.495978707e11, "au", "AU", "천문단위")
_add("길이", 9.4607304725808e15, "ly", "light-year", "light-years", "light year", "light years", "광년")
_add("길이", 3.0856775814913673e16, "pc", "parsec", "parsecs", "파섹")
_add("길이", 3.0856775814913673e19, "kpc", "킬로파섹")
_add("길이", 3.0856775814913673e22, "Mpc", "메가파섹")
_add("길이", 3.0856775814913673e25, "Gpc")
_add("길이", 1609.344, "mi", "mile", "miles", "마일")
_add("길이", 0.3048, "ft", "foot", "feet", "피트")
_add("길이", 0.0254, "inch", "inches", "인치")
_add("길이", 6.3781e6, "R⊕", "R🜨")
_add("길이", 6.957e8, "R☉")
_add("길이", 7.1492e7, "RJ")
_add("질량", 1, "kg", "킬로그램")
_add("질량", 1e-3, "g", "그램")
_add("질량", 1e-6, "mg", "밀리그램")
_add("질량", 1e-9, "µg")
_add("질량", 1e3, "t", "tonne", "tonnes", "톤")
_add("질량", 0.45359237, "lb", "lbs", "pound", "pounds", "파운드")
_add("질량", 5.9722e24, "M⊕", "M🜨")
_add("질량", 1.98847e30, "M☉")
_add("시간", 1, "s", "sec", "second", "seconds", "초")
_add("시간", 1e-3, "ms")
_add("시간", 1e-6, "µs")
_add("시간", 1e-9, "ns")
_add("시간", 60, "min", "minute", "minutes", "분")
_add("시간", 3600, "h", "hr", "hrs", "hour", "hours", "시간")
_add("시간", 86400, "d", "day", "days", "일")
_add("시간", 604800, "week", "weeks", "주")
_add("시간", 2629746, "month", "months", "개월")
_add("시간", 31557600, "y", "yr", "yrs", "year", "years", "년")
_add("시간", 3.15576e10, "kyr")
_add("시간", 3.15576e13, "Myr")
_add("시간", 3.15576e16, "Gyr")
_add("속도", 1, "m/s")
_add("속도", 1e3, "km/s")
_add("속도", 1 / 3.6, "km/h")
_add("속도", 0.44704, "mph")
_add("가속도", 1, "m/s²", "m/s2")
_add("넓이", 1, "m²", "m2", "제곱미터")
_add("넓이", 1e6, "km²", "km2", "제곱킬로미터")
_add("넓이", 1e-4, "cm²", "cm2")
_add("넓이", 1e4, "ha", "헥타르")
_add("넓이", 4046.8564224, "acre", "acres")
_add("넓이", 2589988.110336, "sq mi")
_add("부피", 1, "m³", "m3", "세제곱미터")
_add("부피", 1e-6, "cm³", "cm3", "mL", "밀리리터")
_add("부피", 1e9, "km³", "km3")
_add("부피", 1e-3, "L", "ℓ", "liter", "liters", "litre", "litres", "리터")
_add("밀도", 1000, "g/cm³", "g/cm3", "g/mL")
_add("밀도", 1, "kg/m³", "kg/m3", "g/L")
_add("압력", 1, "Pa", "파스칼")
_add("압력", 100, "hPa", "mbar")
_add("압력", 1e3, "kPa")
_add("압력", 1e6, "MPa")
_add("압력", 1e9, "GPa")
_add("압력", 1e5, "bar")
_add("압력", 101325, "atm", "기압")
_add("에너지", 1, "J")
_add("에너지", 1e3, "kJ")
_add("에너지", 1.602176634e-19, "eV", "전자볼트")
_add("에너지", 1.602176634e-16, "keV")
_add("에너지", 1.602176634e-13, "MeV")
_add("에너지", 1.602176634e-10, "GeV")
_add("에너지", 1.602176634e-7, "TeV")
_add("에너지", 3600, "Wh")
_add("에너지", 3.6e6, "kWh")
_add("에너지", 3.6e9, "MWh")
_add("에너지", 3.6e12, "GWh")
_add("에너지", 4.184, "cal")
_add("에너지", 4184, "kcal")
_add("몰 에너지", 1, "J/mol")
_add("몰 에너지", 1e3, "kJ/mol")
_add("몰 에너지", 4184, "kcal/mol")
_add("출력", 1, "W", "와트")
_add("출력", 1e3, "kW", "킬로와트")
_add("출력", 1e6, "MW", "메가와트")
_add("출력", 1e9, "GW", "기가와트")
_add("출력", 1e12, "TW")
_add("출력", 3.828e26, "L☉")
_add("온도", 1, "K", "켈빈", "°C", "℃", "°F", "℉")
_add("각도", 1, "°")
_add("각도", 57.29577951308232, "rad")
_add("각도", 1 / 3.6e6, "mas")
_add("각도", 1 / 3600, "arcsec", "초각")
_add("각도", 1 / 60, "arcmin", "분각")
_add("진동수", 1, "Hz", "헤르츠")
_add("진동수", 1e3, "kHz")
_add("진동수", 1e6, "MHz")
_add("진동수", 1e9, "GHz")
_add("몰 질량", 1e-3, "g/mol")
_add("몰 질량", 1, "kg/mol")
_add("열전도율", 1, "W/(m·K)", "W/m·K")
_add("몰 열용량", 1, "J/(mol·K)")
_add("비열", 1, "J/(kg·K)")
_add("비열", 1000, "J/(g·K)")
_add("비저항", 1, "Ω·m")
_add("비저항", 1e-6, "µΩ·m")
_add("비저항", 1e-9, "nΩ·m")
_add("열팽창", 1e-6, "µm/(m·K)")
CELSIUS = {"°C", "℃"}
FAHRENHEIT = {"°F", "℉"}


def norm(u):
    """단위 글자를 표의 표기로: 가운뎃점·µ를 하나로, 접두어와 Ω 사이의 한 칸을 지우고, "° C"를 °C로."""
    u = u.replace("⋅", "·").replace("∙", "·").replace("μ", "µ")
    u = re.sub(r"([µn]) Ω", r"\1Ω", u)
    return re.sub(r"^° ?([CF])$", r"°\1", u)


def to_base(value, key):
    """(차원, 기준 단위로 바꾼 값). key는 UNITS의 표기."""
    dim, f = UNITS[key]
    if key in CELSIUS:
        return dim, value + 273.15
    if key in FAHRENHEIT:
        return dim, (value - 32) * 5 / 9 + 273.15
    return dim, value * f


def _unit_pattern(key):
    """표의 표기를 글에서 찾는 정규식으로. 가운뎃점·µ는 같은 글자들 가운데 어느 것이든, °C와 °F는 도 기호 뒤 한 칸을 받는다."""
    out = ""
    for k, ch in enumerate(key):
        if ch == "·":
            out += "[·⋅∙]"
        elif ch == "µ":
            out += "[µμ]"
        elif ch == "Ω" and k > 0 and key[k - 1] in "µn":
            out += " ?Ω"
        elif ch in "CF" and key[:k] == "°":
            out += " ?" + ch
        else:
            out += re.escape(ch)
    return re.compile(out)


# 첫 글자 -> [(길이, 정규식, 표기)] (긴 것부터). 첫 글자는 µ·μ를 둘 다 넣는다.
_BY_FIRST = {}
for _key in sorted(UNITS, key=len, reverse=True):
    _first = {"µ": "µμ"}.get(_key[0], _key[0])
    for _c in _first:
        _BY_FIRST.setdefault(_c, []).append((len(_key), _unit_pattern(_key), _key))

# 단위 바로 뒤에 이런 글자가 오면 그 단위가 아니다(더 긴 낱말이나 다른 단위의 일부).
_BAD_AFTER = frozenset("/·⋅∙^_☉⊕🜨♃′″")
PARTICLES = ("은", "는", "이", "가", "을", "를", "에", "의", "와", "과", "도", "로", "으로", "만", "까지", "부터", "보다", "처럼", "마다", "씩",
             "째", "쯤", "경", "간", "동안", "가량", "정도", "여", "이상", "이하", "미만", "초과", "내외", "전후", "안팎", "남짓", "후", "뒤",
             "전", "내", "이내", "당", "짜리", "및", "라", "였")


def is_hangul(c):
    return "가" <= c <= "힣"


def is_supsub(c):
    o = ord(c)
    return (0x2070 <= o <= 0x209F or o in (0xB2, 0xB3, 0xB9) or 0x2B0 <= o <= 0x2FF or 0x1D2C <= o <= 0x1D7F)


def particle_follows(s, e):
    """s[e:]가 조사·접미사 목록의 말로 시작하는가."""
    return any(s.startswith(p, e) for p in PARTICLES)


def boundary_ok(s, e, key):
    """단위(표기 key)가 s[:e]에서 끝난다고 볼 수 있는가."""
    if e >= len(s):
        return True
    c = s[e]
    if (c.isascii() and c.isalnum()) or c in _BAD_AFTER or is_supsub(c):
        return False
    if is_hangul(key[-1]) and is_hangul(c):
        return particle_follows(s, e)
    return True


def find_unit(s, pos):
    """pos(공백 한 칸 뒤도 봄)에서 시작하는 단위. 가장 긴 것을 고르고 경계를 지키지 않으면 다음으로 긴 것을 본다.
    돌려주는 값: (적힌 단위 글자, 표기, 단위가 끝나는 자리) 또는 None."""
    q = pos + 1 if pos < len(s) and s[pos] in SP else pos
    if q >= len(s):
        return None
    for _, pat, key in _BY_FIRST.get(s[q], ()):
        m = pat.match(s, q)
        if m and boundary_ok(s, m.end(), key):
            return m.group(0), key, m.end()
    return None


# --- 숫자의 모양 -----------------------------------------------------------------
_S = f"[{SP}]"
_G = f"[{GROUP_SP}]"
_NUM = (rf"(?:[0-9]{{1,3}}(?:,[0-9]{{3}})+(?![0-9])|[0-9]{{1,3}}(?:{_G}[0-9]{{3}})+(?![0-9])|[0-9]+)"
        rf"(?:\.[0-9]{{3}}(?:{_G}[0-9]{{3}})+(?![0-9])|\.[0-9]+)?")
NUM_RE = re.compile(_NUM)
DIGIT_RE = re.compile("[0-9]")
_SUPNUM = {c: str(i) for i, c in enumerate("⁰¹²³⁴⁵⁶⁷⁸⁹")}
_SUPRUN = "[⁺⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+"
EXP_RE = re.compile(rf" ?[×·⋅] ?10(?:(?P<sup>{_SUPRUN})|\^\{{?(?P<car>[+−-]?[0-9]+)\}}?)")
POWER_RE = re.compile(_SUPRUN)
TOL_RE = re.compile(rf"(?:{_S}?±{_S}?{_NUM}|\+{_NUM}{_S}?[−-]{_NUM})")
TOL_PAREN_RE = re.compile(r"\([0-9]+(?:\.[0-9]+)?\)")
KO_BIG = {"조": 12, "억": 8, "만": 4}
KO_TIER = {"조": 3, "억": 2, "만": 1}
KO_GROUP_RE = re.compile(r"(?P<th>천)?(?P<big>[조억만])?")
KO_NEXT_RE = re.compile(rf" ?(?P<num>{_NUM})(?P<th>천)?(?P<big>[조억만])?")
EN_BIG_RE = re.compile(r" ?(?P<w>thousand|million|billion|trillion)(?![A-Za-z])", re.I)
EN_BIG = {"thousand": 3, "million": 6, "billion": 9, "trillion": 12}
RANGE_SEP_RE = re.compile(r" ?[–∼~] ?| +to +|-")
NAME_CHAIN_RE = re.compile(r"[0-9]+(?:\.[0-9]+)?(?:-[0-9]+(?:\.[0-9]+)?){2,}")
_MON = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December"
        r"|Jan\.|Feb\.|Mar\.|Apr\.|Jun\.|Jul\.|Aug\.|Sep\.|Oct\.|Nov\.|Dec\.)(?![A-Za-z])")
_YEAR = r"(?:1[0-9]{3}|20[0-9]{2}|2100)"
# 날짜 표기(규칙 5). 년·월·일 사이의 띄어쓰기는 있어도 없어도 되고, 영어 표기 사이는 보통 띄어쓰기나 묶음 공백 한 칸이다.
DATE_RES = [re.compile(r) for r in (
    r"(?<![0-9])[0-9]{4} ?년 ?[0-9]{1,2} ?월 ?[0-9]{1,2} ?일",
    r"(?<![0-9])[0-9]{4} ?년 ?[0-9]{1,2} ?월",
    r"(?<![0-9])[0-9]{1,2} ?월 ?[0-9]{1,2} ?일",
    rf"(?<![0-9]){_YEAR}년대",
    r"(?<![0-9])[0-9]+세기",
    rf"(?<![0-9]){_YEAR}s(?![A-Za-z])",
    r"(?<![0-9])[0-9]+(?:st|nd|rd|th) century(?![A-Za-z])",
    r"(?<![0-9-])[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])(?![0-9])",
    rf"(?<![0-9.,])[0-9]{{1,2}}{_S}{_MON}{_S}[0-9]{{4}}(?![0-9])",
    rf"(?<![A-Za-z]){_MON}{_S}[0-9]{{1,2}},{_S}[0-9]{{4}}(?![0-9])",
    rf"(?<![A-Za-z]){_MON}{_S}[0-9]{{4}}(?![0-9])",
    rf"(?<![0-9.,])[0-9]{{1,2}}{_S}{_MON}",
)]
_PLAIN = r"[0-9]+(?:\.[0-9]+)?"
HMS_RE = re.compile(rf"(?P<h>{_PLAIN})[hʰ] ?(?P<m>{_PLAIN})[mᵐ](?: ?(?P<s>{_PLAIN})[sˢ])?(?![A-Za-z])")     # 적경 15h 19m 26s
DMS_RE = re.compile(rf"(?P<d>{_PLAIN})° ?(?P<m>{_PLAIN})′(?: ?(?P<s>{_PLAIN})″)?")                           # 도·분·초 43° 15′ 20″
NEXT_PART_RE = re.compile(rf"[{SP}](?P<num>{_PLAIN})")
PERCENT_RE = re.compile(rf"{_S}?%")
FRACTION_RE = re.compile(rf"(?<![0-9.,])(?P<n>{_NUM})분의 ?(?P<m>{_NUM})")


def _digits(token):
    return re.sub(rf"[,{GROUP_SP}]", "", token)


def _sup_int(run):
    sign = -1 if run.startswith("⁻") else 1
    return sign * int("".join(_SUPNUM[c] for c in run if c in _SUPNUM))


def sign_ok(s, q):
    """s[q]의 부호 글자가 부호인가: 바로 앞이 줄 처음이거나 숫자·글자가 아닐 때만."""
    if q == 0:
        return True
    c = s[q - 1]
    return not (c.isalnum() or is_supsub(c))


def _ko_big(s, end, value):
    """수 뒤의 만·억·조·천 묶음. 큰 것부터 차례로 띄어쓰기를 두거나 붙어서 이어지면 한 숫자다. (값, 끝) 또는 None."""
    g = KO_GROUP_RE.match(s, end)
    if not (g.group("th") or g.group("big")):
        return None
    mult = (1e3 if g.group("th") else 1) * (10.0 ** KO_BIG[g.group("big")] if g.group("big") else 1)
    total, tier, e, more = value * mult, KO_TIER.get(g.group("big"), 0), g.end(), []
    while tier > 0:
        n = KO_NEXT_RE.match(s, e)
        if not n or not (n.group("th") or n.group("big")):
            break
        t2 = KO_TIER.get(n.group("big"), 0)
        if t2 >= tier:
            break
        m2 = (1e3 if n.group("th") else 1) * (10.0 ** KO_BIG[n.group("big")] if n.group("big") else 1)
        total += float(_digits(n.group("num"))) * m2
        more.append(_digits(n.group("num")))
        tier, e = t2, n.end()
    # 뒤에 조사가 아닌 한글이 바로 붙으면 큰 수 낱말이 아니다(5만큼). 단위가 붙으면 괜찮다(4561만년)
    if e < len(s) and is_hangul(s[e]) and not particle_follows(s, e) and not find_unit(s, e):
        return None
    return total, e, more


def parse_value(s, p):
    """p(숫자 첫 글자)에서 값을 읽는다: 숫자 [지수 | 큰 수 낱말] [오차 폭]. 돌려주는 값은 dict:
    digits(처음 숫자의 글자), value, end, plain(지수·큰 수 낱말·오차 폭이 없는 정수),
    all(양의 digits: 처음 숫자와 큰 수 낱말에 이어진 수들)."""
    m = NUM_RE.match(s, p)
    digits = _digits(m.group(0))
    end = m.end()
    value = float(digits)
    plain = "." not in digits
    all_digits = [digits]
    e = EXP_RE.match(s, end)
    pw = POWER_RE.match(s, end) if digits == "10" else None
    if e:
        n = _sup_int(e.group("sup")) if e.group("sup") else int(e.group("car").replace("−", "-"))
        value *= 10.0 ** n
        end, plain = e.end(), False
    elif pw:
        value = 10.0 ** _sup_int(pw.group(0))
        end, plain = pw.end(), False
    else:
        kb = _ko_big(s, end, value)
        eb = EN_BIG_RE.match(s, end)
        if kb:
            (value, end, more), plain = kb, False
            all_digits += more
        elif eb:
            value *= 10.0 ** EN_BIG[eb.group("w").lower()]
            end, plain = eb.end(), False
    t = TOL_RE.match(s, end) or TOL_PAREN_RE.match(s, end)
    if t:
        end, plain = t.end(), False
    return {"digits": digits, "value": value, "end": end, "plain": plain, "all": all_digits}


# --- 한 줄(또는 표 칸) 읽기 -----------------------------------------------------

PRE_RE = re.compile(r"(?P<w>(?:섭씨|화씨) ?영하|영하|섭씨|화씨|초속|시속) ?$")


def resolve_unit(s, vend, pre):
    """값이 끝난 자리 뒤의 단위. pre는 값 앞의 말(PRE_RE의 match)이나 None. {text, key, end, how, use_pre, neg, per}."""
    word = pre.group("w") if pre else ""
    u = find_unit(s, vend)
    info = {"use_pre": False, "neg": False, "per": None}
    if word in ("초속", "시속"):
        if u and UNITS[u[1]][0] == "길이":
            return {**info, "text": u[0], "key": u[1], "end": u[2], "how": "앞", "use_pre": True, "per": 1 if word == "초속" else 3600}
        return {**info, "text": u[0], "key": u[1], "end": u[2], "how": "뒤"} if u else None
    neg = word.endswith("영하")
    if word and u and UNITS[u[1]][0] == "온도":
        # 영하 N °C: 단위는 뒤에서 얻고 영하는 부호만 바꾼다. 섭씨 N °C의 섭씨는 쓸 데가 없다
        return {**info, "text": u[0], "key": u[1], "end": u[2], "how": "뒤", "use_pre": neg, "neg": neg}
    if word:
        q = vend + 1 if s[vend:vend + 1] in SP else vend
        if s.startswith("도", q) and boundary_ok(s, q + 1, "도"):
            return {**info, "text": "도", "key": "°F" if word.startswith("화씨") else "°C", "end": q + 1, "how": "앞", "use_pre": True,
                    "neg": neg}
    if u:
        return {**info, "text": u[0], "key": u[1], "end": u[2], "how": "뒤"}
    return None


def _quantity(a, b, value, info, digits):
    if info["neg"]:
        value = -abs(value)
    if info["per"]:
        dim, base = "속도", value * UNITS[info["key"]][1] / info["per"]
    else:
        dim, base = to_base(value, info["key"])
    return {"kind": "양", "start": a, "end": b, "value": value, "unit": info["text"], "dim": dim, "base": base, "how": info["how"], "digits": digits}


YEAR_UNITS = {"년", "year", "years", "yr"}


def _is_year(info, v, a, p):
    """년·year·years·yr 앞의 1000~2100 정수는 연도다(날짜)."""
    return info["key"] in YEAR_UNITS and v["plain"] and a == p and 1000 <= v["value"] <= 2100


def _is_name_before(seg, p):
    """숫자 바로 앞이 이름을 이루는 자리인가: 영문자(G9), 영문자나 한글 뒤의 하이픈(Kepler-22b), 제(제22호)."""
    prev = seg[p - 1] if p > 0 else ""
    if prev.isascii() and prev.isalpha() or prev == "제":
        return True
    return prev == "-" and p > 1 and (seg[p - 2].isascii() and seg[p - 2].isalpha() or is_hangul(seg[p - 2]))


def _extend(seg, item, key):
    """같은 차원의 단위가 큰 것부터 작은 것 차례로 띄어쓰기만 사이에 두고 이어지면 한 값이다(3 days 7.5 hours).
    값은 처음 단위로 나타내고, 이어진 항목은 how를 "여러 칸"으로 한다. 온도는 더하는 값이 아니라 잇지 않는다."""
    if item["dim"] == "온도":
        return item
    dim, last = UNITS[key]
    total, end, digits = item["base"], item["end"], list(item["digits"])
    while True:
        m = NEXT_PART_RE.match(seg, end)
        u = find_unit(seg, m.end()) if m else None
        if not u or UNITS[u[1]][0] != dim or UNITS[u[1]][1] >= last:
            break
        total += float(m.group("num")) * UNITS[u[1]][1]
        digits.append(m.group("num"))
        last, end = UNITS[u[1]][1], u[2]
    if end == item["end"]:
        return item
    return {**item, "end": end, "value": total / UNITS[key][1], "base": total, "how": "여러 칸", "digits": digits}


def _ctx_info(seg, a, end, ctx):
    """단위가 안 붙은 숫자(seg[a:end])가 이름 칸이나 머리글의 단위를 받는가."""
    if not ctx or a < ctx["from"] or _is_suffix_name(seg, end):
        return None
    return {"text": ctx["text"], "key": ctx["key"], "end": end, "how": ctx["how"], "use_pre": False, "neg": False, "per": None}


def _is_suffix_name(seg, end):
    """숫자 뒤가 차례말(40번째, 1차)이거나 단위가 아닌 영문자(22b, 6s²)인가."""
    return seg.startswith(("번째", "차"), end) or (end < len(seg) and seg[end].isascii() and seg[end].isalpha())


def _read_one(seg, p, add, ctx):
    """p(숫자 첫 글자)에서 항목을 만들고 읽은 끝 자리를 돌려준다."""
    num_end = NUM_RE.match(seg, p).end()
    if _is_name_before(seg, p):
        add("이름", p, num_end)
        return num_end
    chain = NAME_CHAIN_RE.match(seg, p)
    if chain and not (p > 0 and seg[p - 1] in "0123456789-"):
        for m in NUM_RE.finditer(chain.group(0)):
            add("이름", p + m.start(), p + m.end())
        return chain.end()
    a, sign = p, 1
    if p > 0 and seg[p - 1] in "+-−" and sign_ok(seg, p - 1):
        a, sign = p - 1, (1 if seg[p - 1] == "+" else -1)
    multi = HMS_RE.match(seg, p)
    if multi:
        g = multi.groupdict()
        deg = float(g["h"]) * 15 + float(g["m"]) * 0.25 + float(g["s"] or 0) / 240
        multi_digits = [g[k] for k in "hms" if g[k]]
    else:
        multi = DMS_RE.match(seg, p)
        if multi:
            g = multi.groupdict()
            deg = float(g["d"]) + float(g["m"]) / 60 + float(g["s"] or 0) / 3600
            multi_digits = [g[k] for k in "dms" if g[k]]
    if multi:
        add("양", a, multi.end(), value=sign * deg, unit="°", dim="각도", base=sign * deg, how="여러 칸", digits=multi_digits)
        return multi.end()
    v = parse_value(seg, p)
    pre = PRE_RE.search(seg, max(0, a - 8), a)
    # 범위: 끝값 뒤에 단위가 있을 때만
    sm = RANGE_SEP_RE.match(seg, v["end"])
    if sm:
        q, bsign = sm.end(), 1
        if sm.group(0) != "-" and seg[q:q + 1] in ("−", "-", "+") and seg[q + 1:q + 2].isdigit():
            bsign, q = (1 if seg[q] == "+" else -1), q + 1
        if seg[q:q + 1].isdigit():
            vb = parse_value(seg, q)
            info = resolve_unit(seg, vb["end"], pre) or _ctx_info(seg, q, vb["end"], ctx)
            if info:
                add(**_quantity(pre.start() if info["use_pre"] else a, v["end"], sign * v["value"], info, v["all"]))
                add(**_quantity(sm.end(), info["end"], bsign * vb["value"], info, vb["all"]))
                return info["end"]
    info = resolve_unit(seg, v["end"], pre)
    if info and _is_year(info, v, a, p):
        add("날짜", a, info["end"])       # 연도(2026-10-20 규칙 그대로)
        return info["end"]
    if info:
        item = _quantity(pre.start() if info["use_pre"] else a, info["end"], sign * v["value"], info, v["all"])
        if info["how"] == "뒤":
            item = _extend(seg, item, info["key"])
        add(**item)
        return item["end"]

    pc = PERCENT_RE.match(seg, v["end"])
    if pc:
        add("비율", a, pc.end())
        return pc.end()
    if _is_suffix_name(seg, v["end"]):
        add("이름", a, v["end"])         # 차례말(40번째, 1차), 단위가 아닌 영문자가 붙은 것(22b, 6s²)
        return v["end"]
    info = _ctx_info(seg, a, v["end"], ctx)
    if info and _is_year(info, v, a, p):
        add("날짜", a, v["end"])
        return v["end"]
    if info:
        add(**_quantity(a, v["end"], sign * v["value"], info, v["all"]))
        return v["end"]
    add("모르는 숫자", a, v["end"], digits=v["digits"])
    return v["end"]


def _scan_segment(seg, ctx=None):
    """한 줄(또는 표 칸)에서 항목을 모두 읽는다. 위치는 seg 안의 자리다. ctx는 이름 칸·머리글에서 얻은 단위
    {"text", "key", "how", "from"} (from 자리부터의 숫자에 쓴다)."""
    items, taken = [], []

    def add(kind=None, a=None, b=None, **kw):
        items.append({"kind": kind, "start": a, "end": b, **kw} if kind else kw)

    found = sorted((m for r in DATE_RES for m in r.finditer(seg)), key=lambda m: (m.start(), -m.end()))
    for m in found:
        if not any(a < m.end() and m.start() < b for a, b in taken):
            add("날짜", m.start(), m.end())
            taken.append((m.start(), m.end()))
    for m in FRACTION_RE.finditer(seg):
        add("모르는 숫자", m.start("n"), m.end("n"), digits=_digits(m.group("n")))
        add("모르는 숫자", m.start("m"), m.end("m"), digits=_digits(m.group("m")))
        taken.append((m.start(), m.end()))
    i = 0
    while True:
        m = DIGIT_RE.search(seg, i)
        if not m:
            break
        p = m.start()
        hit = next((b for a, b in taken if a <= p < b), None)
        i = hit if hit else _read_one(seg, p, add, ctx)
    return sorted(items, key=lambda it: it["start"])


def _clean(text):
    """건너뛰는 글자를 뺀 글과, 뺀 글의 자리마다 원래 text의 자리."""
    idx = [i for i, c in enumerate(text) if c not in SKIP]
    return "".join(text[i] for i in idx), idx


INFOBOX_RE = re.compile(r"^ *- (?P<name>.+?): ")
BRACKET_RE = re.compile(r"[\(\[]([^()\[\]]+)[\)\]]")
SEPARATOR_RE = re.compile(r"^\|[\s:|-]*-[\s:|-]*$")


def _unit_in(text):
    """text가 단위 하나이면 (적힌 글자, 표기), 아니면 None."""
    t = text.strip()
    return (t, norm(t)) if norm(t) in UNITS else None


def _cells(line):
    """표 줄을 |로 가른 칸의 (칸 번호, 시작, 끝). \\|는 가르지 않는다."""
    pipes = [i for i, c in enumerate(line) if c == "|" and (i == 0 or line[i - 1] != "\\")]
    bounds = pipes + ([len(line)] if line.rstrip()[-1:] != "|" else [])
    return [(k, bounds[k] + 1, bounds[k + 1]) for k in range(len(bounds) - 1)]


def _segments(lines):
    """줄 목록 [(시작 자리, 글)]을 읽을 조각 [(시작 자리, 글, ctx)]으로 가른다: 표는 칸마다, 나머지는 줄마다."""
    out, k = [], 0
    while k < len(lines):
        if not lines[k][1].startswith("|"):
            off, ln = lines[k]
            m = INFOBOX_RE.match(ln)
            ctx = None
            if m:
                unit = None
                for g in BRACKET_RE.finditer(m.group("name")):
                    if g.end() == len(m.group("name").rstrip()):
                        unit = _unit_in(g.group(1))
                ctx = unit and {"text": unit[0], "key": unit[1], "how": "이름 칸", "from": m.end()}
            out.append((off, ln, ctx))
            k += 1
            continue
        end = k
        while end < len(lines) and lines[end][1].startswith("|"):
            end += 1
        table = end - k >= 2 and SEPARATOR_RE.match(lines[k + 1][1])
        header = {}
        if table:
            for n, a, b in _cells(lines[k][1]):
                units = [u for g in BRACKET_RE.finditer(lines[k][1][a:b]) if (u := _unit_in(g.group(1)))]
                if units:
                    header[n] = units[-1]
        for r in range(k, end):
            off, ln = lines[r]
            for n, a, b in _cells(ln):
                u = header.get(n) if r > k + 1 else None
                out.append((off + a, ln[a:b], u and {"text": u[0], "key": u[1], "how": "머리글", "from": 0}))
        k = end
    return out


MATH_RE = re.compile(r"\\\((?P<a>.*?)\\\)|\\\[(?P<b>.*?)\\\]", re.S)
MATH_NUM_RE = re.compile(_PLAIN)


def _mask_math(m):
    """수식 글에서 위·아래 첨자 자리(^{…}, _{…}, ^x, _x)와 명령(\\times 등)을 같은 길이의 빈칸으로 바꾼다."""
    out = list(m)
    i = 0
    while i < len(m):
        if m[i] in "^_":
            j = i + 1
            if m[j:j + 1] == "{":
                depth = 0
                while j < len(m):
                    depth += (m[j] == "{") - (m[j] == "}")
                    j += 1
                    if depth == 0:
                        break
            elif m[j:j + 1] == "\\":
                j += 1
                while m[j:j + 1].isascii() and m[j:j + 1].isalpha():
                    j += 1
                j = max(j, i + 3)
            else:
                j += 1
            out[i:j] = " " * (j - i)
            i = j
        else:
            i += 1
    return re.sub(r"\\(?:[A-Za-z]+|.)", lambda c: " " * len(c.group(0)), "".join(out))


def _math_items(s, a, b):
    """수식 s[a:b] 안의 숫자. 단위는 읽지 않아 모두 모르는 숫자이고, 영문자가 바로 붙은 것은 이름이다."""
    m = _mask_math(s[a:b])
    out = []
    for t in MATH_NUM_RE.finditer(m):
        prev, nxt = m[t.start() - 1:t.start()] if t.start() else "", m[t.end():t.end() + 1]
        if (prev.isascii() and prev.isalpha()) or (nxt.isascii() and nxt.isalpha()):
            out.append({"kind": "이름", "start": a + t.start(), "end": a + t.end()})
        else:
            out.append({"kind": "모르는 숫자", "start": a + t.start(), "end": a + t.end(), "digits": t.group(0)})
    return out


def read(text):
    """글 하나(마크다운 전체)에서 숫자마다 항목 하나를 글에 나온 차례로 돌려준다."""
    s, idx = _clean(text)
    nl = [i for i, c in enumerate(text) if c == "\n"]
    items, w = [], s
    for m in MATH_RE.finditer(s):
        g = "a" if m.group("a") is not None else "b"
        items += _math_items(s, m.start(g), m.end(g))
        w = w[:m.start()] + re.sub(r"[^\n]", "\ufffc", m.group(0)) + w[m.end():]      # 수식 자리는 읽지 않고 단위가 넘나들지도 못한다
    lines, pos = [], 0
    for ln in w.split("\n"):
        lines.append((pos, ln))
        pos += len(ln) + 1
    for off, seg, ctx in _segments(lines):
        for it in _scan_segment(seg, ctx):
            items.append({**it, "start": off + it["start"], "end": off + it["end"]})
    out = []
    for it in sorted(items, key=lambda it: it["start"]):
        a, b = idx[it["start"]], idx[it["end"] - 1] + 1
        out.append({**it, "start": a, "end": b, "raw": text[a:b], "line": bisect.bisect_left(nl, a)})
    return out


def quantities(text):
    return [i for i in read(text) if i["kind"] == "양"]


def unknown_digits(text):
    return {i["digits"] for i in read(text) if i["kind"] == "모르는 숫자"}


# --- 같은 값 판정 -----------------------------------------------------------------

TOL = 0.01      # 같은 값으로 보는 허용 오차(큰 쪽의 1%, round3_measure.TOL과 같다)


def close(a, b, tol=TOL):
    """두 기준 값이 큰 쪽의 tol 안인가. 둘 다 0이면 같다."""
    return abs(a - b) <= tol * max(abs(a), abs(b))


def group(items):
    """한 언어 문서들의 양 항목(read의 양 항목에 그 문서를 가리키는 doc을 붙인 것)을 서로 다른 값으로 묶는다. 같은 dim이고
    묶음의 첫 기준 값과 close인 것이 한 묶음이다. 돌려주는 값: [{dim, base(첫 항목의 기준 값), mentions(항목 목록)}]."""
    groups = []
    for it in sorted(items, key=lambda i: (i["dim"], i["base"])):
        for g in groups:
            if g["dim"] == it["dim"] and close(g["base"], it["base"]):
                g["mentions"].append(it)
                break
        else:
            groups.append({"dim": it["dim"], "base": it["base"], "mentions": [it]})
    return groups


def judge(groups, other_docs):
    """묶음마다 verdict와 found를 단다. other_docs: [(doc, 그 문서의 read 항목 목록)] (반대 언어 문서들).
    "있음": 같은 dim이고 close인 양 항목이 있다(found: {doc, raw}). "있을 수 있음": 묶음 언급의 digits 가운데 하나가 반대 언어
    문서의 모르는 숫자 digits와 글자 그대로 같다(found: {doc, digits}). "그 언어에만": 둘 다 아니다(found: None).
    반대 언어의 비율, 날짜, 이름 항목은 근거가 아니다. 문서 차례대로 보아 처음 찾은 것을 적는다."""
    for g in groups:
        g["verdict"], g["found"] = "그 언어에만", None
        mine = {d for m in g["mentions"] for d in m["digits"]}
        maybe = None
        for doc, items in other_docs:
            hit = next((i for i in items if i["kind"] == "양" and i["dim"] == g["dim"] and close(g["base"], i["base"])), None)
            if hit:
                g["verdict"], g["found"] = "있음", {"doc": doc, "raw": hit["raw"]}
                break
            if not maybe:
                same = next((i for i in items if i["kind"] == "모르는 숫자" and i["digits"] in mine), None)
                if same:
                    maybe = {"doc": doc, "digits": same["digits"]}
        if g["verdict"] == "그 언어에만" and maybe:
            g["verdict"], g["found"] = "있을 수 있음", maybe
    return groups
