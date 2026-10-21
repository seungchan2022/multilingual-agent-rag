# 표본 읽기 종이

읽는 방법: decisions/stage2.md 2026-10-21 "세는 규칙 보완: 표본 읽기의 크기와 잴 문서" 줄 ㉣. 항목마다 verdicts.json에 판정을 적는다.
- "그 언어에만": read_ok(값과 단위를 문서대로 읽었는가)와 truth(그 언어에만 / 반대 언어에 있음 / 세는 범위의 수가 아님)
- "있음"·"있을 수 있음": read_ok와 truth(같은 사실이 반대 언어에 있음 / 반대 언어에 없음 / 세는 범위의 수가 아님)
- 끝까지 읽는 문서: ai_list(세는 범위의 수: 줄, raw, value, unit). 조건: 끝까지 읽는 문서는 plain이 20,000자 이하인 문서 가운데서 뽑는다(AI가 끝까지 읽을 수 있는 길이로 정했다).
- 언급 옆의 글은 그 줄 안에서 앞뒤 150자이고 언급은 【】로 싼다.

표본의 수: ko A 그 언어에만 136개 중 25개 뽑음, ko B 그 언어에만 111개 중 25개 뽑음, ko A 있음 쪽 660개 중 13개 뽑음, ko B 있음 쪽 88개 중 12개 뽑음, en A 그 언어에만 538개 중 25개 뽑음, en B 그 언어에만 59개 중 25개 뽑음, en A 있음 쪽 744개 중 13개 뽑음, en B 있음 쪽 93개 중 12개 뽑음, ko 문서 A 55개 중 1개 뽑음, ko 문서 B 10개 중 1개 뽑음, en 문서 A 42개 중 1개 뽑음, en 문서 B 10개 중 1개 뽑음

### S001 (묶음 A, kr_satellites, ko, 그룹 ko19)

- verdict: 그 언어에만, dim: 길이, base: 1.4, 표 안: 아니오
- 언급:
  - [대한민국] raw `1400mm` (줄 194, 뒤): 비는 주로 여름에 많이 내리는데 연 강수량의 50~60%가 이때 집중된다. 이를 장마라고 하며 특히 6월 말에서 7월 중순까지를 장마철이라 한다. 각 지역의 연 평균 강수량은 중부 지방이 1100~【1400mm】, 남부 지방이 1000~1800mm, 경북 지역이 1000~1200mm이다. 경상남도 해안 지역은 약 1800mm이며 제주도는 1450~1850mm이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S002 (묶음 A, exoplanets, ko, 그룹 ko3)

- verdict: 그 언어에만, dim: 각도, base: 7.82222e-07, 표 안: 아니오
- 언급:
  - [글리제 436 b] raw `0.002816 초각` (줄 15, 뒤): - 각거리: 【0.002816 초각】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S003 (묶음 A, exoplanets, ko, 그룹 ko65)

- verdict: 그 언어에만, dim: 길이, base: 3.88954e+11, 표 안: 아니오
- 언급:
  - [외계 행성] raw `2.6 천문단위` (줄 162, 뒤): …중력 렌즈법을 이용하여 발견했으며 질량은 지구의 5.5배 수준으로 지금까지 주계열성 주위를 도는 외계 행성들 중 질량이 가장 작다. 이 행성 이전 발견되었던 질량 작은 행성들은 전부 어머니 항성 바로 옆에 붙어 있었지만, OGLE-2005-BLG-390Lb는 항성에서 【2.6 천문단위】 떨어진 곳을 돌고 있다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S004 (묶음 A, rare_earth, ko, 그룹 ko23)

- verdict: 그 언어에만, dim: 길이, base: 5.5493e-10, 표 안: 아니오
- 언급:
  - [루테튬] raw `554.93 pm` (줄 29, 뒤):   - 격자 상수: a = 350.53 pm c = 【554.93 pm】 (20 °C에서)
  - [툴륨] raw `555.39 pm` (줄 30, 뒤):   - 격자 상수: a = 353.77 pm c = 【555.39 pm】 (20 °C에서)
  - [어븀] raw `558.49 pm` (줄 30, 뒤):   - 격자 상수: a = 355.93 pm c = 【558.49 pm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 5.3773e-10: [Samarium] raw `537.73` (줄 98): | SmH2 |  | cubic | Fm3m | 225 | cF12 | 【537.73】 | 537.73 | 537.73 | 4 | 6.51 |
  - base 5.76e-10: [Samarium] raw `576` (줄 116): | SmP |  | cubic | Fm3m | 225 | cF8 | 【576】 | 576 | 576 | 4 | 6.3 |
  - base 5.871e-10: [Samarium] raw `587.1` (줄 107): | SmF2 | purple | cubic | Fm3m | 225 | cF12 | 【587.1】 | 587.1 | 587.1 | 4 | 6.18 |
  - base 5.94e-10: [Samarium] raw `594` (줄 95): | Sm2O3 |  | trigonal | P3m1 | 164 | hP5 | 377.8 | 377.8 | 【594】 | 1 | 7.89 |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S005 (묶음 A, kr_satellites, ko, 그룹 ko155)

- verdict: 그 언어에만, dim: 진동수, base: 4.01e+08, 표 안: 아니오
- 언급:
  - [우리별 3호] raw `401 MHz` (줄 14, 뒤): - 트랜스폰더: VHF-band 상향링크 (148 MHz 주파수 대역, 9600bps), UHF band 하향링크 (【401 MHz】 주파수 대역, 9600bps 및 2.2GHz, 8GHz), X-band 송신기(3.3 Mbps)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S006 (묶음 A, kr_satellites, ko, 그룹 ko111)

- verdict: 그 언어에만, dim: 시간, base: 1.45152e+06, 표 안: 아니오
- 언급:
  - [대한민국] raw `16.8일` (줄 593, 뒤): 문화예술활동 직접 관람률은 63%이고 관람 비율은 영화-대중음악 및 연예-뮤지컬 등 순이었다. 노동자들의 연차소진율은 77.7%였고, 평균 연차사용일수는 【16.8일】이었다. 연차 휴가 중 '여행 및 여가목적'의 사용 비율은 45.5%로, '휴식목적'의 사용 비율은 30.6%였다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [KOMPSAT-3] `16.8`: … designed to acquire high- and very-high-resolution imagery with a footprint of 【16.8】 km. The satellite has the capacity to acquire 20 minutes of imagery on each orb…
  - [KOMPSAT-3] `16.8`: | Multispectral | 1 | 0.45 - 0.52 μm (blue) | 2.8 m | 【16.8】 km |
  - [KOMPSAT-3] `16.8`: |  | 2 | 0.52 - 0.60 μm (green) | 2.8 m | 【16.8】 km |
  - [KOMPSAT-3] `16.8`: |  | 3 | 0.63 - 0.69μm (rouge) | 2.8 m | 【16.8】 km |
  - [KOMPSAT-3] `16.8`: |  | 4 | 0.76 - 0.90 μm (near-infrared) | 2.8 m | 【16.8】 km |

### S007 (묶음 A, exoplanets, ko, 그룹 ko12)

- verdict: 그 언어에만, dim: 각도, base: 100.954, 표 안: 아니오
- 언급:
  - [COROT-7b] raw `06ʰ 43ᵐ 49.0ˢ` (줄 6, 여러 칸): - 적경: 【06ʰ 43ᵐ 49.0ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [GJ 1214 b] `06`:   - Albedo: 0.51±0.【06】 (Bond)
  - [CoRoT-7b] `06`:   - Mass: 6.【06】±0.65 M🜨
  - [CoRoT-7b] `06`: CoRoT-7b's mass is somewhat uncertain at 6.【06】±0.65M🜨, while its radius and orbital period are well known from CoRoT photometr…
  - [Proxima Centauri b] `06`: …ly understood, but it is probably a terrestrial planet with a minimum mass of 1.【06】 M🜨 and a slightly larger radius than that of Earth. The planet orbits within th…
  - [Proxima Centauri b] `06`: …tidally locked. If the eccentricity of Proxima Centauri b was higher than 0.1–0.【06】, it would tend to enter a Mercury-like 3:2 resonance or higher-order resonances…

### S008 (묶음 A, kr_satellites, ko, 그룹 ko44)

- verdict: 그 언어에만, dim: 길이, base: 730000, 표 안: 아니오
- 언급:
  - [우리별 3호] raw `730km` (줄 21, 뒤): 우리별 1호, 우리별 2호에 이어 1999년 5월 26일 발사되었다. 발사체는 인도의 PSLV-C2이며 크기는 495x604x852mm, 무게 110kg로서, 【730km】 고도의 원형 태양동기궤도를 선회한다. 자세제어방식은 3축 안정화 방식으로 자기토커에 의해 제어가 이루어지며, 지향정확도는 0.5도 이내, 최대공급전력은 180W으로서 수준 있는 과학 실험을 할 수 있게 되었으며 과학실험 자료를 지상으로 내려 보내는데 X 밴드 영역을 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 695000: [STSat-1] raw `695 km` (줄 23):   - Apogee altitude: 【695 km】 (432 mi)
  - base 685000: [KOMPSAT-3] raw `685 km` (줄 22):   - Altitude: 【685 km】 (426 mi)
  - base 674315: [STSat-1] raw `419 mi` (줄 22):   - Perigee altitude: 675 km (【419 mi】)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S009 (묶음 A, exoplanets, ko, 그룹 ko37)

- verdict: 그 언어에만, dim: 길이, base: 2.13925e+09, 표 안: 아니오
- 언급:
  - [글리제 1214 b] raw `0.0143 ± 0.0019` (줄 11, 이름 칸): - 평균거리(AU): 【0.0143 ± 0.0019】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S010 (묶음 A, exoplanets, ko, 그룹 ko10)

- verdict: 그 언어에만, dim: 각도, base: 39.8958, 표 안: 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `02ʰ 39ᵐ 35ˢ` (줄 60, 여러 칸): 센타우루스자리 알파 계의 근처에 있기 때문에 프록시마 b에서 바라본 하늘은 지구에서 봤을 때와 거의 비슷하지만 센타우루스자리에서 가장 밝게 빛나던 별은 보이지 않을 것이다. 태양은 센타우루스자리 알파 계의 현재 적경 및 적위의 대척점인 적경 【02ʰ 39ᵐ 35ˢ】, 적위 +60° 50′(2000년 기준)에서 겉보기등급 +0.5의 노란색 별로 보일 것이다. 이 위치는 3.4 등성 카시오페이아자리 엡실론의 근처이며 심장 성운의 바로 앞 근처이다. 이 위치 때문에 외계 관측자 눈에는 카시오페이아자리의 ＼/＼/ 모양이 /＼/＼/ 모양…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 41.6: [Tau Boötis b] raw `41.6°` (줄 11):   - Inclination: 【41.6°】+1.0° −0.9°
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Tau Boötis b] `35`: …ulted in measured carbon abundance similar to that of Jupiter, in the form of 0.【35】% carbon monoxide volume admixture to hydrogen-helium atmosphere. The upper limi…
  - [GJ 1214 b] `35`:   - Mass: 8.41+0.36 −0.【35】 M🜨
  - [GJ 1214 b] `35`: …ellar spectral lines due to the Doppler effect, yielding a mass of 8.41+0.36 −0.【35】 M🜨. Given the planet's mass and radius, its density can be calculated. Through …
  - [Kepler-16b] `02`: …ed the possibility of a habitable planet orbiting at a distance of about 0.95–1.【02】 AU, which could retain the thermal energy required to keep water in a liquid st…
  - [Proxima Centauri b] `39`:   - Temperature: Teq: 234 K (−【39】 °C; −38 °F)

### S011 (묶음 A, kr_satellites, ko, 그룹 ko51)

- verdict: 그 언어에만, dim: 길이, base: 6e+06, 표 안: 아니오
- 언급:
  - [무궁화 5호] raw `6,000 km` (줄 26, 뒤): 무궁화 3호 보다 2배의 송신출력이며, 교신거리는 한국에서 【6,000 km】 까지이다. 서쪽으로는, 한국에서 하와이 까지가 7,000 km 인데, 그보다 약간 못 미친다. 동쪽으로는 인도의 동쪽 해안인 벵골만까지 커버가 되나, 소말리아 해적 소탕을 위해 청해부대가 작전중인 UAE, 소말리아에는 미치지 못한다. 남쪽으로는 호주의 북부 해안까지 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 6.378e+06: [Geocentric orbit] raw `6,378 km` (줄 138): …arth's own rotation at surface on the equator (for compari­son; not an orbit) | 【6,378 km】 | 0 km | 465.1 m/s (1,674 km/h or 1,040 mph) | 23 h 56 min 4.09 sec | −62.6 MJ/…
  - base 6.6e+06: [Geocentric orbit] raw `6,600` (줄 140): | Low Earth orbit | 【6,600】 – 8,400 km | 200 – 2,000 km | Circular orbit: 7.7–6.9 km/s (27,720–24,840 km/h …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S012 (묶음 A, kr_satellites, ko, 그룹 ko13)

- verdict: 그 언어에만, dim: 길이, base: 0.83, 표 안: 아니오
- 언급:
  - [과학기술위성 1호] raw `830 mm` (줄 10, 뒤): - 크기: 665*551*【830 mm】
  - [과학기술위성 1호] raw `830 mm` (줄 19, 뒤): 2003년 9월 27일 오후 3시 11분(한국시각) 플레세츠크(Plesetsk) 우주센터에서 러시아의 COSMOS 3M 로켓에 의해 발사되었다. 고도 690km의 태양동기궤도를 돌고 있으며 106kg의 무게와 665*551*【830 mm】의 크기를 가진다. 주임무는 원자외선영역의 천체 및 지구 분광관측과 오로라의 발생원인 규명을 위한 입자검출 실험이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 0.852: [KITSAT-3] raw `85.2 cm` (줄 12):   - Dimensions: 49.5 cm × 60.4 cm × 【85.2 cm】 (19.5 in × 23.8 in × 33.5 in)
  - base 0.8: [STSat-1] raw `80 cm` (줄 12):   - Dimensions: 66 cm x 60 cm x 【80 cm】
  - base 0.9: [STSat-2A] raw `90 cm` (줄 11):   - Dimensions: 62 cm x 70 cm x 【90 cm】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [South Korea] `830`: …a Strait (Tsushima Strait) Sea of Japan (East Sea) | Seoul | 서울특별시 | 서울特別市ᵇ | 9,【830】,452 |

### S013 (묶음 A, exoplanets, ko, 그룹 ko39)

- verdict: 그 언어에만, dim: 길이, base: 3.14156e+09, 표 안: 아니오
- 언급:
  - [외계 행성] raw `0.021 천문단위` (줄 156, 뒤): 6월 글리제 876의 세 번째 행성 존재 사실이 공표되었다. 질량은 지구의 7.5배로, 현재 이 행성은 주계열성을 도는 모든 발견된 외계 행성들 중 두 번째로 가볍다. 암석 행성일 가능성이 크다. 어머니 항성으로부터의 거리는 【0.021 천문단위】, 공전 주기는 1.94일이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Gliese 581c] `0.021`:   - Eccentricity: 0.032+0.027 −【0.021】

### S014 (묶음 A, exoplanets, ko, 그룹 ko68)

- verdict: 그 언어에만, dim: 길이, base: 5.68472e+12, 표 안: 아니오
- 언급:
  - [외계 행성] raw `38 AU` (줄 195, 뒤): …원경의 화상을 통해 추가로 항성에 보다 가까이 붙어 있는 세 번째 행성의 존재도 확인했다. 2004년 켁 망원경으로 얻은 자료를 통해 사진에 나타난 천체 셋은 행성이 맞음을 검증했다. 이들의 질량 및 항성으로부터의 거리는 각각 10 MJ - 24 AU, 10 MJ - 【38 AU】, 7 MJ - 68 AU이었다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5.98391e+12: [Methods of detecting exoplanets] raw `40 AU` (줄 158): …ral times more massive than Jupiter, and to have an orbital radius greater than 【40 AU】.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [GJ 1214 b] `38`:   - Semi-amplitude: 14.【38】+0.57 −0.56 m/s
  - [Gliese 436 b] `38`:   - Semi-amplitude: 17.【38】±0.17 m/s
  - [Proxima Centauri b] `38`:   - Temperature: Teq: 234 K (−39 °C; −【38】 °F)
  - [Proxima Centauri b] `38`: …radiation. Its equilibrium temperature is estimated to be about 234 K (−39 °C; −【38】 °F). Various factors, such as the orbital properties of Proxima Centauri b, the…
  - [Ross 128 b] `38`: …for habitability. The planet is only 35% more massive than Earth, receives only 【38】% more starlight, and is expected to be a temperature suitable for liquid water …

### S015 (묶음 A, rare_earth, ko, 그룹 ko63)

- verdict: 그 언어에만, dim: 몰 에너지, base: 247000, 표 안: 아니오
- 언급:
  - [툴륨] raw `247 kJ/mol` (줄 21, 뒤):   - 기화열: 【247 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [Dysprosium] `247`:   - Poisson ratio: 0.【247】
  - [Praseodymium] `247`: …Praseodymium is calculated to have a very large atomic radius; with a radius of 【247】 pm, barium, rubidium and caesium are larger. However, observationally, it is us…

### S016 (묶음 A, exoplanets, ko, 그룹 ko36)

- verdict: 그 언어에만, dim: 길이, base: 8.97587e+08, 표 안: 아니오
- 언급:
  - [외계 행성] raw `0.006AU` (줄 204, 뒤): B형 준왜성인 케플러 70의 주위를 【0.006AU】 떨어져 돌고 있는 외계 행성이다. 지나칠 정도로 가까운 거리 때문에 행성은 극단적으로 작열하며, 표면온도가 7178K에 육박한다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Proxima Centauri b] `0.006`: …g by a factor of 100 over a timespan of hours; its luminosity averaged at 0.155±【0.006】 L☉.

### S017 (묶음 A, kr_satellites, ko, 그룹 ko141)

- verdict: 그 언어에만, dim: 시간, base: 6.40619e+10, 표 안: 아니오
- 언급:
  - [차세대소형위성 1호] raw `2030년` (줄 72, 뒤): 기존 계획에서는 한국형발사체 개발 이후 대형위성을 발사할 수 있도록 추력을 지속 확대할 계획이었으나 최근 위성의 소형화 추세에 맞춰 먼저 500kg 이하 위성을 얹어 우주로 보낼 수 있는 소형발사체 KSLV-S로 확장(2025~【2030년】)하고, 이후 3톤급 정지궤도위성 발사가 가능한 대형발사체로 확장(2030~2040년)해 나갈 방침이다.
  - [차세대소형위성 1호] raw `2030` (줄 72, 뒤): …이후 대형위성을 발사할 수 있도록 추력을 지속 확대할 계획이었으나 최근 위성의 소형화 추세에 맞춰 먼저 500kg 이하 위성을 얹어 우주로 보낼 수 있는 소형발사체 KSLV-S로 확장(2025~2030년)하고, 이후 3톤급 정지궤도위성 발사가 가능한 대형발사체로 확장(【2030】~2040년)해 나갈 방침이다.
  - [차세대소형위성 1호] raw `2040년` (줄 72, 뒤): …위성을 발사할 수 있도록 추력을 지속 확대할 계획이었으나 최근 위성의 소형화 추세에 맞춰 먼저 500kg 이하 위성을 얹어 우주로 보낼 수 있는 소형발사체 KSLV-S로 확장(2025~2030년)하고, 이후 3톤급 정지궤도위성 발사가 가능한 대형발사체로 확장(2030~【2040년】)해 나갈 방침이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S018 (묶음 A, exoplanets, ko, 그룹 ko43)

- verdict: 그 언어에만, dim: 길이, base: 6.32799e+09, 표 안: 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `0.0423` (줄 50, 뒤): … 스펙트럼상 M형 별인 적색왜성이기 때문이다. 즉, 모항성인 프록시마의 온도가 낮기 때문에(표면온도 약 3000 °C) 이렇게 가까움에도 프록시마 b가 생명체 거주 가능 영역에 있을 수 있는 것이다. 태양 질량의 8분의 1 수준인 프록시마 주변의 생물권은 항성으로부터 【0.0423】 ~ 0.0816 AU 범위에 걸쳐 있다. 2016년 10월 프랑스 CNRS 연구재단의 천문학자들은 b에 지구 비슷한 바다와 미약한 대기가 존재할 가능성이 매우 높다고 주장했다. 그러나 b는 지구에서 봤을 때 항성 앞을 지나가지 않기 때문에 이 가설을 검증하기는 어렵다…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.8815e+09: [CoRoT-7b] raw `0.046 AU` (줄 20): … times that of Earth and orbits every 3.7 days at a distance of 6.9 million km (【0.046 AU】; 4.3 million mi).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S019 (묶음 A, exoplanets, ko, 그룹 ko124)

- verdict: 그 언어에만, dim: 시간, base: 1.89216e+08, 표 안: 아니오
- 언급:
  - [외계 행성] raw `2190 ± 460일` (줄 129, 뒤): 목성급 질량으로, 긴 공전 주기를 갖는 최초의 발견 사례. 항성에서 2.11 천문단위 떨어져 있으며 이심율은 0.049이다. 동반 행성도 발견되었는데, 3.39 천문단위 거리에 이심율은 0.220 ± 0.028, 공전주기는 【2190 ± 460일】이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S020 (묶음 A, exoplanets, ko, 그룹 ko125)

- verdict: 그 언어에만, dim: 시간, base: 2.87174e+08, 표 안: 아니오
- 언급:
  - [외계 행성] raw `9.1년` (줄 198, 뒤): …외선천문연구부 이재우, 김승리 박사와 충북대학교 김천휘 교수 등 국내외 학자 7명으로 이루어진 연구팀이 두 별로 이뤄진 쌍성(서로의 중력에 묶여 회전하는 두 개의 별) 주위에서 공전하고 있는 2개의 외계행성을 세계 최초로 발견했다고 5일 발표했다. 이 두 개의 행성은 【9.1년】과 15.8년의 주기로 쌍성계의 질량중심 주위를 공전하고 있다. 행성들의 질량은 각각 목성의 8.5배와 19.2배이고, 표면온도는 각각 영하 3도와 영하 43도로 추정된다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [Kepler-22b] `9.1`:   - Mass: <【9.1】 M🜨
  - [Kepler-22b] `9.1`: … limit is 52.8 M🜨). As of 2023, the upper limit has been constrained to at most 【9.1】 M🜨.

### S021 (묶음 A, exoplanets, ko, 그룹 ko59)

- verdict: 그 언어에만, dim: 길이, base: 1.27009e+11, 표 안: 아니오
- 언급:
  - [케플러-22b] raw `0.849 AU` (줄 26, 뒤): 케플러-22b는 모항성의 밝기가 태양의 79%이지만, 모항성으로부터 약 【0.849 AU】 떨어져 있어 지구가 받는 태양열보다 9.6% 더 받고 있다. 따라서 케플러-22b의 실제 표면 온도는 예상보다 훨씬 뜨거울 것이다. 또한 지름도 지구의 2.4배나 되므로 온실 효과 등도 대단히 높을 것이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.21473e+11: [Kepler-22b] raw `0.812+0.011 −0.013 AU` (줄 8):   - Semi-major axis: 【0.812+0.011 −0.013 AU】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S022 (묶음 A, rare_earth, ko, 그룹 ko239)

- verdict: 그 언어에만, dim: 열팽창, base: 6.7e-06, 표 안: 아니오
- 언급:
  - [프라세오디뮴] raw `6.7 µm/(m·K)` (줄 31, 뒤):   - 열팽창: (실온) (α, poly) 【6.7 µm/(m·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S023 (묶음 A, exoplanets, ko, 그룹 ko31)

- verdict: 그 언어에만, dim: 길이, base: 3.13135e+07, 표 안: 아니오
- 언급:
  - [글리제 436 b] raw `0.438 RJ` (줄 18, 뒤): - 반지름: 【0.438 RJ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S024 (묶음 A, exoplanets, ko, 그룹 ko29)

- verdict: 그 언어에만, dim: 길이, base: 4e+06, 표 안: 아니오
- 언급:
  - [글리제 436 b] raw `4,000 킬로미터` (줄 31, 뒤): …표면 위를 지나가는 것을 발견했다. 통과 현상을 통하여 글리제 436 b의 반지름과 질량을 알 수 있었는데, 두 물리적 수치 모두 해왕성의 그것과 유사했다. 글리제 436 b는 통과 현상을 보이는 외계 행성들 중 가장 질량이 작기도 하다. 이 행성의 지름은 천왕성보다 【4,000 킬로미터】, 해왕성보다 5,000 킬로미터 더 크며 질량은 근소하게 더 크다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S025 (묶음 A, exoplanets, ko, 그룹 ko69)

- verdict: 그 언어에만, dim: 길이, base: 6.13351e+12, 표 안: 아니오
- 언급:
  - [외계 행성] raw `41 천문단위` (줄 153, 뒤): …목성의 5배 정도에, 갈색 왜성에서 약 55 천문단위 떨어진 거리를 돌고 있는 것으로 확인되었다. 이 행성은 매우 뜨거운데(1250 켈빈), 주로 중력 수축 때문이다. 갈색 왜성의 질량은 목성의 25배 정도에 불과하다. 2005년 후반기 갈색 왜성과 행성 사이 거리는 【41 천문단위】에 행성질량은 목성의 3.3배로 수정되었는데, 이는 갈색 왜성과 지구 사이 거리가 예상보다 가까웠기 때문이다. 2006년 갈색 왜성 주위에 원시행성계 원반이 있음이 확인되었으며, 갈색 왜성 주변에서도 행성이 생겨날 수 있음이 입증되었다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5.98391e+12: [Methods of detecting exoplanets] raw `40 AU` (줄 158): …ral times more massive than Jupiter, and to have an orbital radius greater than 【40 AU】.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Gliese 581c] `41`: …f the planetary atmosphere. For example, Venus has an effective temperature of −【41】 °C (−42 °F), but a surface temperature of 464 °C (867 °F) (mainly due to a 96.5…
  - [Tau Boötis b] `41`:   - Inclination: 【41】.6°+1.0° −0.9°
  - [GJ 1214 b] `41`:   - Mass: 8.【41】+0.36 −0.35 M🜨
  - [GJ 1214 b] `41`: …hifts in stellar spectral lines due to the Doppler effect, yielding a mass of 8.【41】+0.36 −0.35 M🜨. Given the planet's mass and radius, its density can be calculate…
  - [Kepler-16b] `41`: … a K-type and M-type binary star system. The stars orbit each other about every 【41】 days. The stars have masses of 0.68 M☉ and 0.20 M☉ and radii of 0.64 R☉ and 0.2…

### S026 (묶음 B, exoplanets, ko, 그룹 ko107)

- verdict: 그 언어에만, dim: 시간, base: 1.9872e+09, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `23000` (줄 21, 머리글): | 게자리 55 | h |  | ~【23000】 | ~15 |  |  | 2008 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S027 (묶음 B, exoplanets, ko, 그룹 ko20)

- verdict: 그 언어에만, dim: 길이, base: 2.69276e+11, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `1.8` (줄 145, 머리글): | HD 113766 | 【1.8】, 4-9, 30-80 | 지구형 행성 생성의 증거 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.48e+11: [HD 147513 b] raw `248,000,000 km` (줄 8):   - Apastron: 1.66 AU (【248,000,000 km】)
  - base 2.99196e+11: [HD 23596 b] raw `2.00 AU` (줄 20): … orbit is higher than all the planets in the Solar System, bringing as close as 【2.00 AU】 to as far as 3.66 AU from the parent star.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [HD 147513 b] `1.8`:   - Semi-amplitude: 29.3 ± 【1.8】

### S028 (묶음 B, exoplanets, ko, 그룹 ko53)

- verdict: 그 언어에만, dim: 시간, base: 78796.8, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `0.912` (줄 51, 머리글): | SWEEPS-02 | b |  | 【0.912】 | 0.015 |  | >86 | 2006 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S029 (묶음 B, exoplanets, ko, 그룹 ko43)

- verdict: 그 언어에만, dim: 길이, base: 3.39425e+17, 표 안: 아니오
- 언급:
  - [글리제 86 b] raw `11 파섹` (줄 8, 뒤): - 거리: 35.9 광년(【11 파섹】)
  - [글리제 86 b] raw `35.9 광년` (줄 8, 뒤): - 거리: 【35.9 광년】(11 파섹)
  - [글리제 86 b] raw `36 광년` (줄 23, 뒤): 글리제 86 b는 에리다누스자리 방향으로 지구로부터 약 【36 광년】 떨어진 곳에 있는 외계 행성이다. 보다 정확하게 표기하면 글리제 86 Ab인데, 이는 글리제 86 항성계는 A와 B 두 개의 항성으로 이루어져 있고 글리제 86 b는 이 중 주성 A 옆을 돌고 있기 때문이다. 글리제 86 b의 모항성 글리제 86은 K형 주계열성이다.…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.31126e+17: [Gliese 86 b] raw `35 light-years` (줄 20): …on star "B") and/or shortened to Gl 86 b, is an extrasolar planet approximately 【35 light-years】 away in the constellation of Eridanus. The planet was discovered orbiting a K-t…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [HD 23596 b] `11`:   - Mass: 【11】.914+0.990 −1.768 MJ
  - [Gliese 86 b] `11`:   - Longitude of ascending node: 73.33°+0.10° −0.【11】°

### S030 (묶음 B, exoplanets, ko, 그룹 ko10)

- verdict: 그 언어에만, dim: 길이, base: 6.7319e+09, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `0.0450` (줄 94, 머리글): | 글리제 436 | c | 4.7 ME | 5.1859 | 【0.0450】 | 0.2 | 2008 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S031 (묶음 B, exoplanets, ko, 그룹 ko71)

- verdict: 그 언어에만, dim: 시간, base: 448062, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `5.1859` (줄 94, 머리글): | 글리제 436 | c | 4.7 ME | 【5.1859】 | 0.0450 | 0.2 | 2008 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S032 (묶음 B, exoplanets, ko, 그룹 ko87)

- verdict: 그 언어에만, dim: 시간, base: 7.84512e+07, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `908` (줄 37, 머리글): | HD 208487 | c | 0.46? | 【908】? | 1.8? | 0.19? |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S033 (묶음 B, exoplanets, ko, 그룹 ko42)

- verdict: 그 언어에만, dim: 길이, base: 2.39357e+14, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `1600` (줄 96, 머리글): | HD 44179 B | b |  |  | 【1600】 |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S034 (묶음 B, exoplanets, ko, 그룹 ko33)

- verdict: 그 언어에만, dim: 길이, base: 1.49598e+12, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `10.0` (줄 99, 머리글): | 랄랑드 21185 | c | 508.48 | 10957.8 | 【10.0】 | 0 |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S035 (묶음 B, rare_earth, ko, 그룹 ko66)

- verdict: 그 언어에만, dim: 에너지, base: 9.90145e-15, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `61.8(1) keV` (줄 30, 뒤): | ¹³¹ᵐCe | 【61.8(1) keV】 | 61.8(1) keV | 61.8(1) keV | 5.0(10) min | β⁺ | ¹³¹La | (1/2+) |  |  |
  - [세륨 동위 원소] raw `61.8(1) keV` (줄 30, 뒤): | ¹³¹ᵐCe | 61.8(1) keV | 【61.8(1) keV】 | 61.8(1) keV | 5.0(10) min | β⁺ | ¹³¹La | (1/2+) |  |  |
  - [세륨 동위 원소] raw `61.8(1) keV` (줄 30, 뒤): | ¹³¹ᵐCe | 61.8(1) keV | 61.8(1) keV | 【61.8(1) keV】 | 5.0(10) min | β⁺ | ¹³¹La | (1/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.01081e-14: [Isotopes of cerium] raw `63.09(9) keV` (줄 38): | ¹³¹ᵐCe | 【63.09(9) keV】 | 63.09(9) keV | 63.09(9) keV | 1966 | 5.4(4) min | β⁺ | ¹³¹La | (1/2+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S036 (묶음 B, exoplanets, ko, 그룹 ko75)

- verdict: 그 언어에만, dim: 시간, base: 3.672e+06, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `42.5` (줄 48, 머리글): | 공작자리 피2 | b | 0.69 | 【42.5】 | 0.25 | 0.429 |  | 1998 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S037 (묶음 B, exoplanets, ko, 그룹 ko109)

- verdict: 그 언어에만, dim: 시간, base: 8.83613e+09, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `280년` (줄 26, 뒤): | 에리다누스자리 엡실론 | c | ~0.1 | ~【280년】 | ~40 | ~0.3 |  | 2002 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S038 (묶음 B, rare_earth, ko, 그룹 ko22)

- verdict: 그 언어에만, dim: 시간, base: 3e-07, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `300 ns` (줄 61, 뒤): | ¹⁵³Ce | 58 | 95 | 152.94058(43)# | 500# ms [>【300 ns】] | β⁻ | ¹⁵³Pr | 3/2-# |  |  |
  - [세륨 동위 원소] raw `300 ns` (줄 62, 뒤): | ¹⁵⁴Ce | 58 | 96 | 153.94342(54)# | 300# ms [>【300 ns】] | β⁻ | ¹⁵⁴Pr | 0+ |  |  |
  - [세륨 동위 원소] raw `300 ns` (줄 63, 뒤): | ¹⁵⁵Ce | 58 | 97 | 154.94804(64)# | 200# ms [>【300 ns】] | β⁻ | ¹⁵⁵Pr | 5/2-# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.08e-07: [Isotopes of cerium] raw `308(5) ns` (줄 44): | ¹³⁴ᵐCe | 3208.6(4) keV | 3208.6(4) keV | 3208.6(4) keV | 1980 | 【308(5) ns】 | IT | ¹³⁴Ce | 10+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S039 (묶음 B, exoplanets, ko, 그룹 ko5)

- verdict: 그 언어에만, dim: 각도, base: 40.5306, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `+40° 31′ 50.287″` (줄 7, 여러 칸): - 적위: 【+40° 31′ 50.287″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 38.898: [HD 23596 b] raw `38.898°` (줄 11):   - Inclination: 【38.898°】+15.759° −77.179°
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S040 (묶음 B, exoplanets, ko, 그룹 ko80)

- verdict: 그 언어에만, dim: 시간, base: 2.14592e+07, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `0.68년` (줄 103, 뒤): | PSR B1828-10 | A | 3 ME | 【0.68년】 | 0.93 |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S041 (묶음 B, exoplanets, ko, 그룹 ko101)

- verdict: 그 언어에만, dim: 시간, base: 3.15576e+08, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `10년` (줄 41, 뒤): | HD 50499 | d | 2 | >【10년】 |  |  |  | 2005 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [HAT-P-9b] `10`:   - Surface gravity: 【10】.3 m/s² (34 ft/s²) 1.05 g
  - [Gliese 86 b] `10`:   - Longitude of ascending node: 73.33°+0.【10】° −0.11°

### S042 (묶음 B, exoplanets, ko, 그룹 ko76)

- verdict: 그 언어에만, dim: 시간, base: 8.99338e+06, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `104.090` (줄 120, 머리글): | HD 223084 | b | 1.21 | 【104.090】 | 0.44 |  |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S043 (묶음 B, exoplanets, ko, 그룹 ko51)

- verdict: 그 언어에만, dim: 시간, base: 46742.4, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `0.541` (줄 62, 머리글): | SWEEPS-15 | b |  | 【0.541】 | 0.01 |  | >84 | 2006 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S044 (묶음 B, exoplanets, ko, 그룹 ko0)

- verdict: 그 언어에만, dim: 각도, base: -50.8333, 표 안: 아니오
- 언급:
  - [글리제 86 b] raw `-50° 50′ 00″` (줄 7, 여러 칸): - 적위: 【-50° 50′ 00″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [HD 23596 b] `00`: …rbit is higher than all the planets in the Solar System, bringing as close as 2.【00】 AU to as far as 3.66 AU from the parent star.
  - [Gliese 86 b] `50`:   - Inclination: 【50】.00°±0.01°
  - [Gliese 86 b] `50`:   - Inclination: 【50】.00°±0.01°
  - [Gliese 86 b] `00`:   - Inclination: 50.【00】°±0.01°

### S045 (묶음 B, exoplanets, ko, 그룹 ko94)

- verdict: 그 언어에만, dim: 시간, base: 1.60944e+08, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `5.1년` (줄 93, 뒤): | 제밍가 | b | 1.7 ME | 【5.1년】 | 3.3 |  | 1997 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S046 (묶음 B, exoplanets, ko, 그룹 ko47)

- verdict: 그 언어에만, dim: 밀도, base: 1.23e+06, 표 안: 아니오
- 언급:
  - [HD 147513 b] raw `1230 g/cm³` (줄 18, 뒤): - 밀도: ~【1230 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S047 (묶음 B, exoplanets, ko, 그룹 ko41)

- verdict: 그 언어에만, dim: 길이, base: 5.23593e+13, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `350` (줄 140, 머리글): | HD 141569 | 86 - 【350】 | 원반을 안쪽, 바깥쪽으로 나눔 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S048 (묶음 B, exoplanets, ko, 그룹 ko63)

- verdict: 그 언어에만, dim: 시간, base: 145498, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `1.684` (줄 60, 머리글): | SWEEPS-13 | b |  | 【1.684】 | 0.027 |  | >86 | 2006 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S049 (묶음 B, exoplanets, ko, 그룹 ko97)

- verdict: 그 언어에만, dim: 시간, base: 2.14592e+08, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `6.8년` (줄 40, 뒤): | HD 50499 | c | 1.7 | 【6.8년】 |  |  |  | 2005 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S050 (묶음 B, rare_earth, ko, 그룹 ko31)

- verdict: 그 언어에만, dim: 시간, base: 4, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `4.0(6) s` (줄 58, 뒤): | ¹⁵⁰Ce | 58 | 92 | 149.93041(5) | 【4.0(6) s】 | β⁻ | ¹⁵⁰Pr | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.8: [Isotopes of cerium] raw `3.8(2) s` (줄 23): | ¹²³Ce | 58 | 65 | 122.93528(32)# | 1984 | 【3.8(2) s】 | β⁺ (?%) | ¹²³La | (5/2)(+#) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S051 (묶음 A, rare_earth, ko, 그룹 ko259)

- verdict: 있음, dim: 온도, base: 673.15, 표 안: 아니오
- 언급:
  - [이트륨] raw `400 °C` (줄 64, 뒤): …를 막는 산화피막(산화이트륨 Y2O3로 이루어진)을 생성하기 때문에 비교적 안정한 편이다. 이 산화피막은 이트륨 금속이 수증기 안에서 750 °C 로 가열될 때 1 μm의 두께를 가질 수 있다. 잘게 나눠졌을 때, 이트륨은 공기 중에서 불안정하다. 작은 이트륨 조각은 【400 °C】 이상의 온도에서 불이 붙을 수 있다. 질화 이트륨(YN)은 이트륨이 질소(N) 기체 안에서 1000 °C 로 가열될 때 생성된다.
  - [사마륨] raw `400°C` (줄 91, 뒤): 사마륨은 네오디뮴 자석 다음으로 강력한 사마륨-코발트 자석을 만드는데 사용된다. 이 때, 사마륨과 코발트의 비율은 1:5이거나 2:17인 경우가 많다. 이러한 자석은 철보다 1만배 이상 강력한 것이다. 또, 네오디뮴 자석은 300~【400°C】 가량의 온도에서 자성을 잃는데 비해 사마륨-코발트 자석은 700°C 이상의 고온에서도 자성을 잃지 않는다. 주로 소형 전동기, 헤드셋, 기타나 그와 비슷한 악기의 자석식 픽업 등에 사용된다.
- found: [Yttrium] raw `400 °C` (줄 70): …r vapor. When finely divided, however, yttrium is very unstable in air; shavings or turnings of the metal can ignite in air at temperatures exceeding 【400 °C】. Yttrium nitride (YN) is formed when the metal is heated to 1000 °C in nitrogen.

### S052 (묶음 A, probes, ko, 그룹 ko16)

- verdict: 있음, dim: 길이, base: 1000, 표 안: 아니오
- 언급:
  - [베네라 8호] raw `1 km` (줄 24, 뒤): …이 거칠어 착륙에 실패한 후 11초 동안만 신호를 보냈다. 착륙선에서 보내온 금성의 온도와 기압(섭씨 470도, 기압은 지구의 90배) 자료를 분석해 베네라 7호의 자료가 옮음을 확인했고, 표면의 사진을 찍기에 빛의 양이 적합하다고 보내왔다. 이는 지구에서 흐린 날에 【1 km】 밖에 있는 물체를 보는 것과 같다.
  - [트리톤 호퍼] raw `1km` (줄 21, 뒤): 로켓:트리톤 표면에서 잠깐 튀어 올랐다가 다시 내려오는 것이 목적이다. 1번에 약 【1km】 정도 뛰어오를 수 있고 5km 앞으로 갈 수 있다.
  - [미국 항공 우주국] raw `1km` (줄 319, 뒤): 1998년, 미국 의회는 NASA에 2008년까지 직경 【1km】 이상의 근지구 소행성(전 지구적 파괴를 위협하는) 90%를 탐지하도록 지시했다. 이 초기 임무는 2011년까지 달성되었다. 2005년, 원래의 USA 스페이스가드 임무는 조지 E. 브라운 주니어 근지구 천체 조사법에 의해 확장되었으며, 이 법은 NASA에 2020년까…
- found: [Venera 8] raw `1 km` (줄 45): …d the light level as being suitable for surface photography, finding it to be similar to the amount of light on Earth on an overcast day with roughly 【1 km】 visibility.

### S053 (묶음 A, probes, ko, 그룹 ko38)

- verdict: 있음, dim: 길이, base: 6.87795e+18, 표 안: 예
- 언급:
  - [EPOXI] raw `727` (줄 53, 머리글): | WASP-3 | 거문고자리 | 【727】 | b |
- found: [EPOXI] raw `727` (줄 52): | WASP-3 | Lyra | 【727】 | b |

### S054 (묶음 A, kr_satellites, ko, 그룹 ko95)

- verdict: 있음, dim: 시간, base: 5556, 표 안: 아니오
- 언급:
  - [OSSI-1] raw `92.6분` (줄 23, 뒤): - 주기: 【92.6분】
- found: [OSSI-1] raw `92.6 minutes` (줄 25):   - Period: 【92.6 minutes】

### S055 (묶음 A, rare_earth, ko, 그룹 ko65)

- verdict: 있음, dim: 몰 에너지, base: 331000, 표 안: 아니오
- 언급:
  - [프라세오디뮴] raw `331 kJ/mol` (줄 21, 뒤):   - 기화열: 【331 kJ/mol】
- found: [Praseodymium] raw `331 kJ/mol` (줄 22):   - Heat of vaporization: 【331 kJ/mol】

### S056 (묶음 A, kr_satellites, ko, 그룹 ko100)

- verdict: 있을 수 있음, dim: 시간, base: 18000, 표 안: 아니오
- 언급:
  - [협정 세계시] raw `5시간` (줄 58, 뒤): UTC는 계절의 변화에 따라 변하지 않지만 시간대 관할 구역이 일광 절약 시간제(서머타임)를 관찰하면 상용시가 변할 수 있다. 예를 들어 미국 동부 해안의 현지 시간은 겨울 동안 UTC보다 【5시간】 늦지만 일광 절약 시간제가 적용될 때는 4시간 늦다.
- found: [Koreasat 5] 숫자 글자 `5` (줄 0): # Koreasat 【5】

### S057 (묶음 A, kr_satellites, ko, 그룹 ko130)

- verdict: 있음, dim: 시간, base: 3.15576e+08, 표 안: 아니오
- 언급:
  - [무궁화 1호] raw `10년` (줄 23, 뒤): 1995년 8월 5일에 미국 케이프커내버럴 공군 기지에서 발사했다. 이때 6번 연료통 점화 퓨즈가 고장나서 위성과 분리되지 못하는 사고가 나, 【10년】 예정이던 수명이 4년 4개월로 단축되었다. 이에 무궁화 2호와 무궁화 3호의 개발이 앞당겨졌다.
  - [대한민국] raw `10년` (줄 483, 뒤): …구조는 매우 낮은 출산율, 빠른 고령화, 높은 인구 밀도 등의 특징을 보인다. 2024년 기준 합계출산율은 0.75명으로, 2000년대 이후 세계적으로 가장 낮은 수준을 유지하고 있다. 2025년 1분기 출생아 수는 65,022명으로 전년 동기 대비 7.4% 증가하며 【10년】 만에 반등했으나, 여전히 낮은 수준이다. 이러한 저출산 현상은 높은 사교육비 지출, 주택 비용 상승, 장시간 근무 문화, 일과 가정의 양립 어려움, 성별 역할 인식 등이 복합적으로 작용한 결과로 분석된다.
  - [대한민국] raw `10년` (줄 573, 뒤): SBS와 한국갤럽이 2011년 천 명을 대상으로 설문조사한 결과, 우리 사회의 경쟁 수준은 평균 76점으로 【10년】 전보다 20점 가까이 높아져 경쟁이 계속 가속화한다. 국민 10명 중 8명이 "과도한 경쟁에 부담을 느낀다"라고 대답하여 상당수가 부담감을 느끼는 것으로 나타났다.
- found: [Koreasat 1] raw `10 years` (줄 5): - Mission duration: 【10 years】

### S058 (묶음 A, rare_earth, ko, 그룹 ko206)

- verdict: 있음, dim: 압력, base: 1.48e+10, 표 안: 아니오
- 언급:
  - [프라세오디뮴] raw `14.8 GPa` (줄 36, 뒤):   - 전단 탄성 계수: (α form) 【14.8 GPa】
- found: [Praseodymium] raw `14.8 GPa` (줄 41):   - Shear modulus: 【14.8 GPa】

### S059 (묶음 A, rare_earth, ko, 그룹 ko179)

- verdict: 있음, dim: 압력, base: 2.06e+08, 표 안: 아니오
- 언급:
  - [이터븀] raw `206 MPa` (줄 41, 뒤):   - 비커스 굳기: 【206 MPa】
- found: [Ytterbium] raw `205` (줄 45):   - Vickers hardness: 【205】–250 MPa

### S060 (묶음 A, exoplanets, ko, 그룹 ko44)

- verdict: 있음, dim: 길이, base: 6.8815e+09, 표 안: 아니오
- 언급:
  - [목동자리 타우 b] raw `0.046` (줄 11, 이름 칸): - 평균거리(AU): 【0.046】
- found: [CoRoT-7b] raw `6.9 million km` (줄 20): …rvations of CoRoT-7 also detected a second super-Earth, CoRoT-7c, which has a mass 8.4 times that of Earth and orbits every 3.7 days at a distance of 【6.9 million km】 (0.046 AU; 4.3 million mi).

### S061 (묶음 A, kr_satellites, ko, 그룹 ko82)

- verdict: 있을 수 있음, dim: 시간, base: 476, 표 안: 아니오
- 언급:
  - [과학기술위성 2호] raw `7분 56초` (줄 30, 여러 칸): - 2009년 8월 19일 : 2A호가 나로호에 실려 발사될 예정이었으나, 소프트웨어 결함으로 발사 【7분 56초】 전 발사가 취소되었다.
- found: [NEXTSat-2] 숫자 글자 `7` (줄 17): At 【7】:07 p.m., the first satellite signal was received at the King Sejong Station in Antarctica, and at 7:58 p.m., initial communication was made through t…

### S062 (묶음 A, kr_satellites, ko, 그룹 ko59)

- verdict: 있음, dim: 속도, base: 7800, 표 안: 아니오
- 언급:
  - [지구 주회 궤도] raw `7.8km/s` (줄 4, 뒤): 우주선은 중력에 의한 구심 가속도가 속도의 수평 성분에 의한 원심 가속도보다 작거나 같을 때 궤도에 진입한다. 지구 저궤도의 경우, 이 속도는 약 【7.8km/s】(28,100km/h)이다. 이에 비해 지금까지 달성한 가장 빠른 비행기의 속도(우주선으로 달성한 속도 제외)는 1967년 노스아메리칸 X-15가 달성한 2.2km/s(7,900km/h)이다. 고도 600km에서 지구 궤도 속도에 도달하는 데 필요한 에너지는 약 36M…
  - [지구 주회 궤도] raw `28,100km/h` (줄 4, 뒤): 우주선은 중력에 의한 구심 가속도가 속도의 수평 성분에 의한 원심 가속도보다 작거나 같을 때 궤도에 진입한다. 지구 저궤도의 경우, 이 속도는 약 7.8km/s(【28,100km/h】)이다. 이에 비해 지금까지 달성한 가장 빠른 비행기의 속도(우주선으로 달성한 속도 제외)는 1967년 노스아메리칸 X-15가 달성한 2.2km/s(7,900km/h)이다. 고도 600km에서 지구 궤도 속도에 도달하는 데 필요한 에너지는 약 36MJ/kg이며, 이는 …
- found: [Geocentric orbit] raw `7.8 km/s` (줄 4): … is less than or equal to the centrifugal acceleration due to the horizontal component of its velocity. For a low Earth orbit, this velocity is about 【7.8 km/s】 (28,100 km/h; 17,400 mph); by contrast, the fastest crewed airplane speed ever achieved (excluding speeds achieved by deorbiting spacecraft) was 2.2 …

### S063 (묶음 A, probes, ko, 그룹 ko88)

- verdict: 있음, dim: 시간, base: 122400, 표 안: 아니오
- 언급:
  - [미국 항공 우주국] raw `34시간` (줄 35, 뒤): … 프렌드십 7호에서 수행되었으며, 재진입 전에 세 번의 완전한 궤도를 돌았다. 글렌은 자동 조종 장치 오작동으로 인해 마지막 두 궤도의 일부를 수동으로 비행해야 했다. 여섯 번째이자 마지막 머큐리 임무는 1963년 5월 고든 쿠퍼에 의해 수행되었으며, 페이스 7호에서 【34시간】 동안 22번의 궤도를 돌았다. 머큐리 프로그램은 인간을 우주 궤도에 진입시키고, 추적 및 제어 시스템을 개발하며, 유인 우주 비행과 관련된 다른 문제들을 식별하는 목표를 달성하며 엄청난 성공으로 인정받았다.
- found: [NASA] raw `34 hours` (줄 53): …rbits manually due to an autopilot malfunction. The sixth and final Mercury mission was flown by Gordon Cooper in May 1963, completing 22 orbits over 【34 hours】 aboard Faith 7. The Mercury program was widely recognized as a resounding success, achieving its objectives to orbit a human in space, develop tracki…

### S064 (묶음 B, exoplanets, ko, 그룹 ko26)

- verdict: 있음, dim: 길이, base: 5.47528e+11, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `3.66` (줄 13, 이름 칸): - 원일점(AU): 【3.66】
  - [HD 23596 b] raw `3.66 천문단위` (줄 29, 뒤): …이 행성은 아마도 단단한 표면이 없는, 가스 행성일 것이다. 항성으로부터 평균 2.83 천문단위 떨어져 있으며 1565일 걸려 초속 19.7 킬로미터 속도로 항성 주위를 1회 돈다. 다만 행성 궤도는 다소 찌그러져 있으며 항성에 가까워질 때는 2 천문단위, 멀어질 때 【3.66 천문단위】까지 물러난다.
- found: [HD 23596 b] raw `3.66 AU` (줄 20): …ty of 19.7 km/s. The eccentricity of the planet's orbit is higher than all the planets in the Solar System, bringing as close as 2.00 AU to as far as 【3.66 AU】 from the parent star.

### S065 (묶음 B, rare_earth, ko, 그룹 ko40)

- verdict: 있음, dim: 시간, base: 210, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `3.5(3) min` (줄 26, 뒤): | ¹²⁹Ce | 58 | 71 | 128.91810(3) | 【3.5(3) min】 | β⁺ | ¹²⁹La | (5/2+) |  |  |
- found: [Isotopes of cerium] raw `3.5(3) min` (줄 34): | ¹²⁹Ce | 58 | 71 | 128.918102(30) | 1977 | 【3.5(3) min】 | β⁺ | ¹²⁹La | (5/2+) |  |  |

### S066 (묶음 B, rare_earth, ko, 그룹 ko36)

- verdict: 있을 수 있음, dim: 시간, base: 29, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `29(2) s` (줄 24, 뒤): | ¹²⁷Ce | 58 | 69 | 126.92273(6) | 【29(2) s】 | β⁺ | ¹²⁷La | 5/2+# |  |  |
- found: [Holmium] 숫자 글자 `29` (줄 14):   - Electrons per shell: 2, 8, 18, 【29】, 8, 2

### S067 (묶음 B, rare_earth, ko, 그룹 ko73)

- verdict: 있음, dim: 에너지, base: 3.9311e-13, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `2453.6(3) keV` (줄 28, 뒤): | ¹³⁰ᵐCe | 【2453.6(3) keV】 | 2453.6(3) keV | 2453.6(3) keV | 100(8) ns |  |  | (7-) |  |  |
  - [세륨 동위 원소] raw `2453.6(3) keV` (줄 28, 뒤): | ¹³⁰ᵐCe | 2453.6(3) keV | 【2453.6(3) keV】 | 2453.6(3) keV | 100(8) ns |  |  | (7-) |  |  |
  - [세륨 동위 원소] raw `2453.6(3) keV` (줄 28, 뒤): | ¹³⁰ᵐCe | 2453.6(3) keV | 2453.6(3) keV | 【2453.6(3) keV】 | 100(8) ns |  |  | (7-) |  |  |
- found: [Isotopes of cerium] raw `2453.6(3) keV` (줄 36): | ¹³⁰ᵐCe | 【2453.6(3) keV】 | 2453.6(3) keV | 2453.6(3) keV | 1984 | 100(8) ns | IT | ¹³⁰Ce | 7− |  |  |

### S068 (묶음 B, rare_earth, ko, 그룹 ko24)

- verdict: 있음, dim: 시간, base: 7.3e-06, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `7.3(15) µs` (줄 48, 뒤): | ¹⁴⁰ᵐCe | 2107.85(3) keV | 2107.85(3) keV | 2107.85(3) keV | 【7.3(15) µs】 |  |  | 6+ |  |  |
- found: [Isotopes of cerium] raw `7.3(15) μs` (줄 57): | ¹⁴⁰ᵐCe | 2107.854(24) keV | 2107.854(24) keV | 2107.854(24) keV | 1964 | 【7.3(15) μs】 | IT | ¹⁴⁰Ce | 6+ |  |  |

### S069 (묶음 B, exoplanets, ko, 그룹 ko24)

- verdict: 있음, dim: 길이, base: 4.23362e+11, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `2.83` (줄 11, 이름 칸): - 평균거리(AU): 【2.83】
  - [HD 23596 b] raw `2.83 천문단위` (줄 29, 뒤): …자리 방향으로 지구로부터 약 170광년 떨어진 곳에 있는 외계 행성이다. 이 행성은 매우 무거운데, 적어도 목성 질량의 약 7.8배는 되므로 슈퍼 목성으로 분류할 수 있다. 질량에 기초하면 이 행성은 아마도 단단한 표면이 없는, 가스 행성일 것이다. 항성으로부터 평균 【2.83 천문단위】 떨어져 있으며 1565일 걸려 초속 19.7 킬로미터 속도로 항성 주위를 1회 돈다. 다만 행성 궤도는 다소 찌그러져 있으며 항성에 가까워질 때는 2 천문단위, 멀어질 때 3.66 천문단위까지 물러난다.
- found: [HD 23596 b] raw `2.83 AU` (줄 20): …t as mid-superjovian. Based on its mass, the planet would probably be a gas giant with no solid surface. The planet orbits at the average distance of 【2.83 AU】, taking 1565 days to complete its orbit with average velocity of 19.7 km/s. The eccentricity of the planet's orbit is higher than all the planets in …

### S070 (묶음 B, rare_earth, ko, 그룹 ko21)

- verdict: 있음, dim: 시간, base: 1e-07, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `100(8) ns` (줄 28, 뒤): | ¹³⁰ᵐCe | 2453.6(3) keV | 2453.6(3) keV | 2453.6(3) keV | 【100(8) ns】 |  |  | (7-) |  |  |
- found: [Isotopes of cerium] raw `100(8) ns` (줄 36): | ¹³⁰ᵐCe | 2453.6(3) keV | 2453.6(3) keV | 2453.6(3) keV | 1984 | 【100(8) ns】 | IT | ¹³⁰Ce | 7− |  |  |

### S071 (묶음 B, rare_earth, ko, 그룹 ko46)

- verdict: 있음, dim: 시간, base: 5820, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `97(4) min` (줄 33, 뒤): | ¹³³Ce | 58 | 75 | 132.911515(18) | 【97(4) min】 | β⁺ | ¹³³La | 1/2+ |  |  |
- found: [Isotopes of cerium] raw `97(4) min` (줄 41): | ¹³³Ce | 58 | 75 | 132.911520(18) | 1951 | 【97(4) min】 | β⁺ | ¹³³La | 1/2+ |  |  |

### S072 (묶음 B, rare_earth, ko, 그룹 ko25)

- verdict: 있음, dim: 시간, base: 0.00865, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `8.65(20) ms` (줄 44, 뒤): | ¹³⁸ᵐCe | 2129.17(12) keV | 2129.17(12) keV | 2129.17(12) keV | 【8.65(20) ms】 | IT | ¹³⁸Ce | 7- |  |  |
- found: [Isotopes of cerium] raw `8.73(20) ms` (줄 53): | ¹³⁸ᵐCe | 2129.28(12) keV | 2129.28(12) keV | 2129.28(12) keV | 1960 | 【8.73(20) ms】 | IT | ¹³⁸Ce | 7- |  |  |

### S073 (묶음 B, exoplanets, ko, 그룹 ko72)

- verdict: 있음, dim: 시간, base: 1.36209e+06, 표 안: 아니오
- 언급:
  - [글리제 86 b] raw `15.76491 ± 0.00039 일` (줄 13, 뒤): - 공전주기: 【15.76491 ± 0.00039 일】
  - [글리제 86 b] raw `15.77일` (줄 23, 뒤): … 돌고 있기 때문이다. 글리제 86 b의 모항성 글리제 86은 K형 주계열성이다. 1998년 11월 24일, 마이클 메이어 연구진이 이 행성의 존재를 공식적으로 발표했다. 다른 뜨거운 목성들과 마찬가지로 이 행성 역시 항성으로부터 가까이 붙어 있다. 1회 공전에는 약 【15.77일】이 걸린다.
- found: [Gliese 86 b] raw `15.77 ± 0.01 d` (줄 10):   - Orbital period (sidereal): 【15.77 ± 0.01 d】

### S074 (묶음 B, rare_earth, ko, 그룹 ko37)

- verdict: 있음, dim: 시간, base: 51, 표 안: 예
- 언급:
  - [세륨 동위 원소] raw `51.0(3) s` (줄 23, 뒤): | ¹²⁶Ce | 58 | 68 | 125.92397(3) | 【51.0(3) s】 | β⁺ | ¹²⁶La | 0+ |  |  |
- found: [Isotopes of cerium] raw `51.0(3) s` (줄 29): | ¹²⁶Ce | 58 | 68 | 125.923971(30) | 1978 | 【51.0(3) s】 | β⁺ | ¹²⁶La | 0+ |  |  |

### S075 (묶음 B, exoplanets, ko, 그룹 ko17)

- verdict: 있음, dim: 길이, base: 1.97469e+11, 표 안: 예
- 언급:
  - [확인되지 않은 외계 행성 목록] raw `1.32` (줄 104, 머리글): | PSR B1828-10 | B | 12 ME | 1.35년 | 【1.32】 |  |  |
  - [HD 147513 b] raw `1.32` (줄 11, 이름 칸): - 평균거리(AU): 【1.32】
- found: [HD 147513 b] raw `1.32 AU` (줄 10):   - Semi-major axis: 【1.32 AU】 (197,000,000 km)

### S076 (묶음 A, rare_earth, en, 그룹 en370)

- verdict: 그 언어에만, dim: 온도, base: 143, 표 안: 아니오
- 언급:
  - [Melting point] raw `143 K` (줄 90, 뒤): …, for three structural isomers with molecular formula C5H12 the melting point increases in the series isopentane −160 °C (113 K) n-pentane −129.8 °C (【143 K】) and neopentane −16.4 °C (256.8 K). Likewise in xylenes and also dichlorobenzenes the melting point increases in the order meta, ortho and then para.…
  - [Melting point] raw `−129.8 °C` (줄 90, 뒤): …For example, for three structural isomers with molecular formula C5H12 the melting point increases in the series isopentane −160 °C (113 K) n-pentane 【−129.8 °C】 (143 K) and neopentane −16.4 °C (256.8 K). Likewise in xylenes and also dichlorobenzenes the melting point increases in the order meta, ortho and the…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [사마륨] `143`: - 산소족 원소들과의 화합물은 압력에 따라 전기 저항이 달라지는 특성이 있어 압력 감지기에 사용되기도 한다. 사마륨-147과 네오디뮴-【143】, 네오디뮴-144의 비율을 분석하면 방사능 연대 측정을 할 수도 있다.

### S077 (묶음 A, kr_satellites, en, 그룹 en17)

- verdict: 그 언어에만, dim: 각도, base: 124, 표 안: 아니오
- 언급:
  - [South Korea] raw `124°` (줄 140, 뒤): …hern tip lies on the Korea Strait and the East China Sea. The country, including all its islands, lies between latitudes 33° and 39°N, and longitudes 【124°】 and 130°E. Its total area is 100,472.4 square kilometers (38,792.61 sq mi). South Korea can be divided into four general regions: an eastern region o…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 126.977: [대한민국] raw `126° 58′ 36″` (줄 4):   - 수도: 서울 북위 37° 34′ 08″ 동경 【126° 58′ 36″】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S078 (묶음 A, probes, en, 그룹 en245)

- verdict: 그 언어에만, dim: 진동수, base: 38400, 표 안: 아니오
- 언급:
  - [Mariner 4] raw `38.4 kHz` (줄 54, 뒤): …words or three quantitative word commands for mid-course maneuvers. The central computer and sequencer operated stored time-sequence commands using a 【38.4 kHz】 synchronization frequency as a time reference. Temperature control was achieved through the use of adjustable louvers mounted on six of the electroni…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S079 (묶음 A, rare_earth, en, 그룹 en85)

- verdict: 그 언어에만, dim: 길이, base: 200000, 표 안: 아니오
- 언급:
  - [Rare-earth element] raw `200` (줄 163, 뒤): …ion zones. In a rift setting, the alkaline magma is produced by very small degrees of partial melting (<1%) of garnet peridotite in the upper mantle (【200】 to 600 km depth). This melt becomes enriched in incompatible elements, like the rare-earth elements, by leaching them out of the crystalline residue.…
  - [Rare-earth element] raw `200 km` (줄 165, 뒤): …ttings are carbonatites, and A- and M-Type granitoids. Near subduction zones, partial melting of the subducting plate within the asthenosphere (80 to 【200 km】 depth) produces a volatile-rich magma (high concentrations of CO2 and water), with high concentrations of alkaline elements, and high element mobilit…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [이트륨] `200`: 할로젠 원소들과는 플루오린화 이트륨(III), 염화 이트륨(III), 브로민화 이트륨(III)과 같은 삼할로젠화물을 약 【200】 °C 이상의 온도 환경에서 생성한다. 이와 비슷하게 이트륨은 고온에서 탄소(C), 인(P), 셀레늄(Se), 규소(Si)와 이원화물을 형성한다…
  - [란타넘족] `200`: …다. 결과적으로 란타넘족 이온의 스펙트럼은 다소 약하고 흡수 띠는 좁다. 산화 홀뮴을 포함하는 유리와 산화 홀뮴 용액(보통 과염소산에 녹임)은 【200】~900 nm 스펙트럼 범위에서 날카로운 광학 흡수 피크를 가지며 광학 분광광도계의 파장 교정 표준물질로 사용할 수 있고, 상업적으로 구할 수 …
  - [희토류 원소] `200`: …광물 내에 함유되어 있던 희토류 원소가 재농집되어 형성된 것으로 추정된다. 방사능 수치는 소근리층이 420 cps 이하, 화강편마암이 최대 2,【200】 cps이다.
  - [희토류 원소] `200`: | 팔라듐 | 20,【200】 |
  - [희토류 원소] `200`: | 붕소 | 109,【200】 |

### S080 (묶음 A, exoplanets, en, 그룹 en215)

- verdict: 그 언어에만, dim: 온도, base: 973, 표 안: 아니오
- 언급:
  - [Exoplanet] raw `973 K` (줄 254, 뒤): …ipsed by its parent star. For example, the planet HD 189733b has been estimated to have an average temperature of 1,205 K (932 °C) on its dayside and 【973 K】 (700 °C) on its nightside.
  - [Exoplanet] raw `700 °C` (줄 254, 뒤): …y its parent star. For example, the planet HD 189733b has been estimated to have an average temperature of 1,205 K (932 °C) on its dayside and 973 K (【700 °C】) on its nightside.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [센타우루스자리 프록시마 b] `700`: 센타우루스자리 프록시마 b는 어머니 별을 11.186 일에 1회 돌고 있으며 별과의 평균 거리는 약 0.05 천문단위(【700】만 km 또는 500만 마일)로 태양과 지구 사이 거리의 약 20분의 1 정도이다. 참고로 태양에서 가장 가까운 행성 수성의 평균 공전궤도 반지…
  - [센타우루스자리 프록시마 b] `700`: … 수준) 프록시마로부터 나오는 복사플럭스의 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~【700】 nm)의 3%에 불과하다.(목성은 3.7%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 2700 럭스이다. 참고로…

### S081 (묶음 A, rare_earth, en, 그룹 en519)

- verdict: 그 언어에만, dim: 질량, base: 3.0258e+07, 표 안: 아니오
- 언급:
  - [Rare-earth element] raw `30,258 tonnes` (줄 462, 뒤): … incident, The Economist reported that "China ... in July announced the latest in a series of annual export reductions, this time by 40% to precisely 【30,258 tonnes】." China has officially cited resource depletion and environmental concerns as the reasons for a nationwide crackdown on its rare-earth mineral produc…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S082 (묶음 A, probes, en, 그룹 en5)

- verdict: 그 언어에만, dim: 각도, base: 1.05, 표 안: 아니오
- 언급:
  - [Mariner 4] raw `1.05°` (줄 50, 뒤): …om center of the spacecraft, to obtain closeup pictures of the surface of Mars. This subsystem consisted of four parts: a Cassegrain telescope with a 【1.05°】 by 1.05° field of view, a shutter and red/green filter assembly with 0.08 and 0.20 second exposure times, a slow scan vidicon tube which translated t…
  - [Mariner 4] raw `1.05°` (줄 50, 뒤): … of the spacecraft, to obtain closeup pictures of the surface of Mars. This subsystem consisted of four parts: a Cassegrain telescope with a 1.05° by 【1.05°】 field of view, a shutter and red/green filter assembly with 0.08 and 0.20 second exposure times, a slow scan vidicon tube which translated the optica…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S083 (묶음 A, kr_satellites, en, 그룹 en62)

- verdict: 그 언어에만, dim: 길이, base: 1.09435e+06, 표 안: 아니오
- 언급:
  - [South Korea] raw `680 mi` (줄 140, 뒤): South Korea occupies the southern portion of the Korean Peninsula, which extends some 1,100 km (【680 mi】) from the Continental and East Asian mainland. This mountainous peninsula is flanked by the Yellow Sea to the west and the Sea of Japan to the east. …
  - [South Korea] raw `1,100 km` (줄 140, 뒤): South Korea occupies the southern portion of the Korean Peninsula, which extends some 【1,100 km】 (680 mi) from the Continental and East Asian mainland. This mountainous peninsula is flanked by the Yellow Sea to the west and the Sea of Japan to th…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1e+06: [지구 주회 궤도] raw `1,000km` (줄 44): …O)의 고도에 있고 원지점이 지구 동기 궤도의 고도에 있는 지구 중심 타원 궤도. 장타원 궤도 35,786km 이상의 원지점과 낮은 근지점(약 【1,000km】)이 있는 궤도. 원지점 근처에서 긴 체류 시간을 갖는다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [대한민국] `1100`: …50~60%가 이때 집중된다. 이를 장마라고 하며 특히 6월 말에서 7월 중순까지를 장마철이라 한다. 각 지역의 연 평균 강수량은 중부 지방이 【1100】~1400mm, 남부 지방이 1000~1800mm, 경북 지역이 1000~1200mm이다. 경상남도 해안 지역은 약 1800mm이며 제주도는 1…

### S084 (묶음 A, rare_earth, en, 그룹 en161)

- verdict: 그 언어에만, dim: 비열, base: 182.022, 표 안: 아니오
- 언급:
  - [Europium] raw `182.022 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【182.022 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S085 (묶음 A, rare_earth, en, 그룹 en509)

- verdict: 그 언어에만, dim: 질량, base: 422000, 표 안: 아니오
- 언급:
  - [Europium] raw `422 tonnes` (줄 217, 뒤): …f mixed rare-earth production rather than mined separately. European Commission estimates placed average global production of europium oxide at about 【422 tonnes】 per year in 2012–2016. China accounted for approximately 86% of this production, followed by Australia at 6%, the United States and Russia at about 2…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S086 (묶음 A, exoplanets, en, 그룹 en273)

- verdict: 그 언어에만, dim: 질량, base: 4.06707e+25, 표 안: 아니오
- 언급:
  - [Gliese 581c] raw `6.81+0.21 −1.16 M🜨` (줄 17, 뒤):   - Mass: 【6.81+0.21 −1.16 M🜨】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S087 (묶음 A, probes, en, 그룹 en87)

- verdict: 그 언어에만, dim: 길이, base: 135000, 표 안: 아니오
- 언급:
  - [Venus Express] raw `135 km` (줄 116, 뒤): …a final time until 2015. Between 18 June and 11 July 2014, the spacecraft performed successful aerobraking experiments with multiple passes at 131 to 【135 km】 altitude.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 147000: [잉훠 1호] raw `147 km` (줄 59): 2012년 1월 14일, 포보스 그룬트와 잉훠 1호는 【147 km】 궤도에서 초당 수백 미터의 속도로 궤도가 떨어지고 있었다. 두 탐사선은 1월 15일 태평양 방향으로 재진입하여 분해되었다.
  - base 150000: [베네라 8호] raw `150 km` (줄 24): …km 위에서 1 km/s 정도였고, 10 km 이하에서는 급격히 속도가 줄었다. 베네라 8호는 남경 10.70, 동경 335.25 좌표에서 약 【150 km】 정도의 범위 내 지역에서 협정 세계시 9시 32분에 착륙했는데, 이 지역은 바실리사 지역이라고 불린다. 아침에 햇빛은 명암 경계산 500 km…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [미국 항공 우주국] `135`: …2006년, 우주왕복선은 다시 비행을 시작하여 허블 우주망원경을 서비스하기 위한 여러 임무를 수행했지만, 2011년 국제우주정거장으로의 STS-【135】 보급 임무 이후 은퇴했다.

### S088 (묶음 A, kr_satellites, en, 그룹 en162)

- verdict: 그 언어에만, dim: 시간, base: 2.63506e+09, 표 안: 아니오
- 언급:
  - [South Korea] raw `83.5 years` (줄 382, 뒤): …of hospital beds per 1000 people at 9.56 beds. Life expectancy has been rising rapidly and South Korea ranked 6th in the world for life expectancy at 【83.5 years】 in 2023. It also has the third-highest health-adjusted life expectancy in the world. South Korea maintains the world's highest per capita rate of pla…
  - [South Korea] raw `83.53 years` (줄 329, 뒤): …oeconomic development, South Korea has experienced a dramatic increase in life expectancy, from 79.10 years in 2008 (which was 34th in the world), to 【83.53 years】 in 2024—the fifth-highest of any country or territory.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S089 (묶음 A, probes, en, 그룹 en53)

- verdict: 그 언어에만, dim: 길이, base: 0.457, 표 안: 아니오
- 언급:
  - [Mariner 4] raw `45.7 cm` (줄 40, 뒤): The Mariner 4 spacecraft consisted of an octagonal magnesium frame, 127 cm (50 in) across a diagonal and 【45.7 cm】 (18.0 in) high. Four solar panels were attached to the top of the frame with an end-to-end span of 6.88 meters (22.6 ft), including solar pressure va…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.5: [제22호 과학위성 히노데] raw `0.5미터` (줄 33): 구경 【0.5미터】, 각분해능 0.2 각초, 시야 400² 각초인 그레고리안식 광학 망원경으로, SOT의 초점면 패키지(FPP)에는 세 가지 광학 장비가 포함되어…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S090 (묶음 A, rare_earth, en, 그룹 en12)

- verdict: 그 언어에만, dim: 길이, base: 1.92e-10, 표 안: 아니오
- 언급:
  - [Dysprosium] raw `192±7 pm` (줄 31, 뒤):   - Covalent radius: 【192±7 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 1.95e-10: [란타넘] raw `195 pm` (줄 28):   - 원자 반지름: 【195 pm】 (실험값)
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29):   - 공유 반지름: 【187±8 pm】
  - base 1.85e-10: [유로퓸] raw `185 pm` (줄 28):   - 원자 반지름: 【185 pm】 (실험값) 231 pm (계산값)
  - base 1.8e-10: [이트륨] raw `180 pm` (줄 28):   - 원자 반지름: 【180 pm】 (실험값)
  - base 2.084e-10: [란타넘족] raw `208.4 pm` (줄 65): …것으로 추정된다. 란타넘족 금속은 무르며 경도는 계열을 따라 증가한다. 유로퓸은 밀도가 5.24 g/cm³로 계열에서 가장 낮고 금속 반지름이 【208.4 pm】로 가장 커서 두드러진다. 이는 금속 반지름이 222 pm인 바륨과 비교할 수 있다. 금속 내에 더 큰 Eu²⁺ 이온이 포함되어 있고 전도띠에 …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S091 (묶음 A, kr_satellites, en, 그룹 en72)

- verdict: 그 언어에만, dim: 길이, base: 8.4e+06, 표 안: 예
- 언급:
  - [Geocentric orbit] raw `8,400 km` (줄 140, 뒤): | Low Earth orbit | 6,600 – 【8,400 km】 | 200 – 2,000 km | Circular orbit: 7.7–6.9 km/s (27,720–24,840 km/h or 17,224–15,435 mph) respectively, Elliptic: 10.07–8.7 km/s respectively | 1 h 2…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S092 (묶음 A, probes, en, 그룹 en231)

- verdict: 그 언어에만, dim: 에너지, base: 5.60762e-15, 표 안: 아니오
- 언급:
  - [Mariner 2] raw `35 keV` (줄 91, 뒤): …ficiently, and was previously used in Injun 1, Explorer 12 and Explorer 14. It was able to detect protons above 500 keV in energy and electrons above 【35 keV】. The length of the basic telemetry frame was 887.04 seconds. During each frame, the counting rate of the detector was sampled twice at intervals sepa…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [베네라 8호] `35`: 베네라 8호는 하강할 때 자료를 보내 왔다. 바람 속도는 고도 【35】~30 km 위에서 1 km/s 정도였고, 10 km 이하에서는 급격히 속도가 줄었다. 베네라 8호는 남경 10.70, 동경 335.25 좌표에…

### S093 (묶음 A, rare_earth, en, 그룹 en286)

- verdict: 그 언어에만, dim: 압력, base: 7e+08, 표 안: 아니오
- 언급:
  - [Erbium] raw `700 MPa` (줄 45, 뒤):   - Vickers hardness: 430–【700 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [프라세오디뮴] `700`:   - 전기 저항도: (실온) (α, poly) 【700】 n Ω·m
  - [사마륨] `700`: …한 자성을 가지는 사마륨-코발트 자석으로 쓰인다. 그러나 네오디뮴 자석은 조금만 가열해도 자성이 쉽게 사라지는데 반해 사마륨-코발트 자석은 약 【700】°C의 고온에서도 자성을 잃지 않는 성질이 있다. 방사성 동위 원소인 사마륨-153은 암 치료제로 사용되며 사마륨-149는 중성자를 잘 흡수하는…
  - [사마륨] `700`: …한 자석은 철보다 1만배 이상 강력한 것이다. 또, 네오디뮴 자석은 300~400°C 가량의 온도에서 자성을 잃는데 비해 사마륨-코발트 자석은 【700】°C 이상의 고온에서도 자성을 잃지 않는다. 주로 소형 전동기, 헤드셋, 기타나 그와 비슷한 악기의 자석식 픽업 등에 사용된다.
  - [희토류 원소] `700`: | 플루토늄 | 4,【700】,000 |

### S094 (묶음 A, probes, en, 그룹 en196)

- verdict: 그 언어에만, dim: 시간, base: 2.4192e+06, 표 안: 아니오
- 언급:
  - [Hinode (satellite)] raw `28 days` (줄 7, 뒤): - Mission duration: 20 years, 【28 days】 (elapsed)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [제22호 과학위성 히노데] `28`: …V 로켓에 실려 발사된 마지막 인공위성이다. 히노데는 발사 이후 태양을 향시 관찰 가능한 명암 경계선 근처에 자리를 잡았으며, 같은 해 10월 【28】일 탐사선이 최초로 사진을 보내왔다.
  - [매리너 4호] `28`: - 발사일: 1964년 11월 【28】일 14:22:01 UTC
  - [매리너 4호] `28`: 1964년 11월 【28】일 14:22:01 UTC에 케이프커내버럴 공군 기지의 런치 컴플렉스 SLC-12 발사대에서 아틀라스 로켓에 실려 발사되었다. 7개월 반 동안 …
  - [매리너 4호] `28`: - 발사일 : 1964년 11월 【28】일 14:22:01 UTC
  - [매리너 4호] `28`: - 임무 기간 : 1964년 11월 【28】일 - 1967년 12월 21일

### S095 (묶음 A, exoplanets, en, 그룹 en179)

- verdict: 그 언어에만, dim: 시간, base: 4.29183e+12, 표 안: 아니오
- 언급:
  - [Orbital eccentricity] raw `136,000 years` (줄 140, 뒤): … of periodic components, including a long, stable cycle of about 405,000 years and several shorter components with periods between roughly 95,000 and 【136,000 years】, which together give rise to a prominent ~100,000-year modulation in eccentricity.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S096 (묶음 A, probes, en, 그룹 en92)

- verdict: 그 언어에만, dim: 길이, base: 273588, 표 안: 아니오
- 언급:
  - [Hinode (satellite)] raw `170 mi` (줄 28, 뒤): …V rocket from Uchinoura Space Center, Japan on 22 September 2006 at 21:36 UTC (23 September, 06:36 JST). Its initial orbit was perigee height 280 km (【170 mi】), apogee height 686 km (426 mi), inclination 98.3 degrees, after which the satellite maneuvered to the quasi-circular Sun-synchronous orbit over the …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 280000: [제22호 과학위성 히노데] raw `280 km` (줄 16): - 근지점: 【280 km】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [매리너 4호] `170`: - 전력: 【170】 W
  - [매리너 4호] `170`: - 출력 : 【170】 W

### S097 (묶음 A, exoplanets, en, 그룹 en166)

- verdict: 그 언어에만, dim: 시간, base: 2.592e+07, 표 안: 아니오
- 언급:
  - [Methods of detecting exoplanets] raw `300 days` (줄 108, 뒤): …as carried out with NASA's Kepler space telescope. The transiting planet Kepler-19b shows TTV with an amplitude of five minutes and a period of about 【300 days】, indicating the presence of a second planet, Kepler-19c, which has a period which is a near-rational multiple of the period of the transiting planet.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.50474e+07: [케플러-22b] raw `289.9 일` (줄 6): - 공전주기: 【289.9 일】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [질량] `300`: …력가속도를 측정하여 지구 반지름의 제곱을 곱해 지구의 능동적 중력질량을 측정할 수도 있다. 두 방법으로 계산한 결과 지구의 질량은 태양 질량의 【300】만분의 1로 일치한다.

### S098 (묶음 A, probes, en, 그룹 en8)

- verdict: 그 언어에만, dim: 각도, base: 35, 표 안: 아니오
- 언급:
  - [Mariner 4] raw `35°` (줄 89, 뒤): …reen filters, plus 21 lines of a 22nd picture were taken. The images covered a discontinuous swath of Mars starting near 40° N, 170° E, down to about 【35°】 S, 200° E, and then across to the terminator at 50° S, 255° E, representing about 1% of the planet's surface. The images taken during the flyby were …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [베네라 8호] `35`: 베네라 8호는 하강할 때 자료를 보내 왔다. 바람 속도는 고도 【35】~30 km 위에서 1 km/s 정도였고, 10 km 이하에서는 급격히 속도가 줄었다. 베네라 8호는 남경 10.70, 동경 335.25 좌표에…

### S099 (묶음 A, rare_earth, en, 그룹 en44)

- verdict: 그 언어에만, dim: 길이, base: 8.855e-10, 표 안: 예
- 언급:
  - [Samarium] raw `885.5` (줄 96, 머리글): | Sm2O3 |  | monoclinic | C2/m | 12 | mS30 | 1418 | 362.4 | 【885.5】 | 6 | 7.76 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.9834e-10: [사마륨] raw `0.89834 nm` (줄 30):   - 격자 상수: ar = 【0.89834 nm】 α = 23.307° ah = 0.36291 nm ch = 2.6207 nm (20 °C에서)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S100 (묶음 A, kr_satellites, en, 그룹 en0)

- verdict: 그 언어에만, dim: 가속도, base: 9.80665, 표 안: 아니오
- 언급:
  - [Weight] raw `9.80665 m/s²` (줄 59, 뒤): The gravitational acceleration varies from place to place. Sometimes, it is simply taken to have a standard value of 【9.80665 m/s²】, which gives the standard weight.
  - [Weight] raw `9.80665 m/s²` (줄 131, 뒤): …at different locations. To standardize weights, scales are always calibrated to read the weight an object would have at a nominal standard gravity of 【9.80665 m/s²】 (approx. 32.174 ft/s²). However, this calibration is done at the factory. When the scale is moved to another location on Earth, the force of gravity …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S101 (묶음 B, rare_earth, en, 그룹 en54)

- verdict: 그 언어에만, dim: 시간, base: 324, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `5.4(4) min` (줄 38, 뒤): | ¹³¹ᵐCe | 63.09(9) keV | 63.09(9) keV | 63.09(9) keV | 1966 | 【5.4(4) min】 | β⁺ | ¹³¹La | (1/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 300: [세륨 동위 원소] raw `5.0(10) min` (줄 30): | ¹³¹ᵐCe | 61.8(1) keV | 61.8(1) keV | 61.8(1) keV | 【5.0(10) min】 | β⁺ | ¹³¹La | (1/2+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S102 (묶음 B, rare_earth, en, 그룹 en59)

- verdict: 그 언어에만, dim: 시간, base: 1728, 표 안: 아니오
- 언급:
  - [Holmium] raw `28.8 min` (줄 52, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁶³Ho synth 4570 y ε ¹⁶³Dy ¹⁶⁴Ho synth 【28.8 min】 ε ¹⁶⁴Dy β⁻ ¹⁶⁴Er ¹⁶⁵Ho 100% stable ¹⁶⁶Ho synth 26.812 h β⁻ ¹⁶⁶Er ¹⁶⁶ᵐ¹Ho synth 1133 y β⁻ ¹⁶⁶Er ¹⁶⁷Ho synth 3.1 h β⁻ ¹⁶⁷Er
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S103 (묶음 B, rare_earth, en, 그룹 en33)

- verdict: 그 언어에만, dim: 시간, base: 0.313, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `313(7) ms` (줄 72, 뒤): | ¹⁵⁵Ce | 58 | 97 | 154.94871(32)# | 1994 | 【313(7) ms】 | β⁻ | ¹⁵⁵Pr | 5/2−# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S104 (묶음 B, exoplanets, en, 그룹 en14)

- verdict: 그 언어에만, dim: 각도, base: 148.95, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `+148.950°` (줄 12, 뒤):   - Longitude of ascending node: 16.684°【+148.950°】 −21.642°
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S105 (묶음 B, rare_earth, en, 그룹 en111)

- verdict: 그 언어에만, dim: 질량, base: 4e+08, 표 안: 아니오
- 언급:
  - [Holmium] raw `400,000 tonnes` (줄 142, 뒤): …ral has yet been found. The main mining areas are China, United States, Brazil, India, Sri Lanka, and Australia with reserves of holmium estimated as 【400,000 tonnes】. The annual production of holmium metal is of about 10 tonnes per year.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S106 (묶음 B, rare_earth, en, 그룹 en31)

- verdict: 그 언어에만, dim: 시간, base: 0.175, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `175(41) ms` (줄 74, 뒤): | ¹⁵⁷Ce | 58 | 99 | 156.95713(43)# | 2017 | 【175(41) ms】 | β⁻ | ¹⁵⁷Pr | 7/2+# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [홀뮴] `175`:   - 원자 반지름: 【175】 pm (실험값)

### S107 (묶음 B, exoplanets, en, 그룹 en5)

- verdict: 그 언어에만, dim: 각도, base: -0.11, 표 안: 아니오
- 언급:
  - [Gliese 86 b] raw `−0.11°` (줄 12, 뒤):   - Longitude of ascending node: 73.33°+0.10° 【−0.11°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S108 (묶음 B, rare_earth, en, 그룹 en24)

- verdict: 그 언어에만, dim: 시간, base: 3.08e-07, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `308(5) ns` (줄 44, 뒤): | ¹³⁴ᵐCe | 3208.6(4) keV | 3208.6(4) keV | 3208.6(4) keV | 1980 | 【308(5) ns】 | IT | ¹³⁴Ce | 10+ |  |  |
  - [Isotopes of cerium] raw `310 ns` (줄 18, 뒤): | ¹¹⁹Ce | 58 | 61 | 118.95296(54)# | 2025 | 200# ms [>【310 ns】] |  |  | 5/2+# |  |  |
  - [Isotopes of cerium] raw `310 ns` (줄 19, 뒤): | ¹²⁰Ce | 58 | 62 | 119.94661(54)# | 2025 | 250# ms [>【310 ns】] |  |  | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3e-07: [세륨 동위 원소] raw `300 ns` (줄 61): | ¹⁵³Ce | 58 | 95 | 152.94058(43)# | 500# ms [>【300 ns】] | β⁻ | ¹⁵³Pr | 3/2-# |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S109 (묶음 B, exoplanets, en, 그룹 en30)

- verdict: 그 언어에만, dim: 길이, base: 1.41911e+19, 표 안: 아니오
- 언급:
  - [HAT-P-9b] raw `1500 light years` (줄 18, 뒤): HAT-P-9b, formally named Alef, is an exoplanet approximately 【1500 light years】 away in the constellation Auriga. This planet was found by the transit method on June 26, 2008. It has a mass 78% that of Jupiter and a radius 140% t…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.47587e+19: [HAT-P-9 b] raw `1,560 광년` (줄 25): HAT-P-9b는 마차부자리에 있는, 지구에서 약 【1,560 광년】 떨어져 있는 외계 행성이다. 이 행성은 2008년 6월 26일 통과법을 통해 발견되었다. 질량은 목성의 78퍼센트, 반지름은 목성의 약 140…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S110 (묶음 B, rare_earth, en, 그룹 en37)

- verdict: 그 언어에만, dim: 시간, base: 1.42, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `1.42(2) s` (줄 69, 뒤): | ¹⁵²Ce | 58 | 94 | 151.93668(22)# | 1990 | 【1.42(2) s】 | β⁻ | ¹⁵²Pr | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.4: [세륨 동위 원소] raw `1.4(2) s` (줄 60): | ¹⁵²Ce | 58 | 94 | 151.93654(21)# | 【1.4(2) s】 | β⁻ | ¹⁵²Pr | 0+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S111 (묶음 B, exoplanets, en, 그룹 en37)

- verdict: 그 언어에만, dim: 시간, base: 1.32637e+08, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `4.203+0.021 −0.025 yr` (줄 10, 뒤):   - Orbital period (sidereal): 【4.203+0.021 −0.025 yr】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1.35216e+08: [HD 23596 b] raw `1565±21 일` (줄 15): - 공전주기: 【1565±21 일】(4.285년)
  - base 1.2623e+08: [확인되지 않은 외계 행성 목록] raw `4년` (줄 32): | 마차부자리 GM | b | 1.7 | 【4년】 | 2.5 |  |  |  |
  - base 1.4256e+08: [확인되지 않은 외계 행성 목록] raw `1650` (줄 29): | GD 66 | b | 2.11 | 【1650】 | 2.356 | 0 |  | 2007 |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S112 (묶음 B, exoplanets, en, 그룹 en32)

- verdict: 그 언어에만, dim: 속도, base: 128.315, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `128.315+2.480 −2.670 m/s` (줄 15, 뒤):   - Semi-amplitude: 【128.315+2.480 −2.670 m/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S113 (묶음 B, exoplanets, en, 그룹 en9)

- verdict: 그 언어에만, dim: 각도, base: 15.759, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `+15.759°` (줄 11, 뒤):   - Inclination: 38.898°【+15.759°】 −77.179°
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S114 (묶음 B, rare_earth, en, 그룹 en75)

- verdict: 그 언어에만, dim: 시간, base: 3.57548e+10, 표 안: 아니오
- 언급:
  - [Holmium] raw `1133 y` (줄 52, 뒤): …e (t1/2) mode pro­duct ¹⁶³Ho synth 4570 y ε ¹⁶³Dy ¹⁶⁴Ho synth 28.8 min ε ¹⁶⁴Dy β⁻ ¹⁶⁴Er ¹⁶⁵Ho 100% stable ¹⁶⁶Ho synth 26.812 h β⁻ ¹⁶⁶Er ¹⁶⁶ᵐ¹Ho synth 【1133 y】 β⁻ ¹⁶⁶Er ¹⁶⁷Ho synth 3.1 h β⁻ ¹⁶⁷Er
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S115 (묶음 B, exoplanets, en, 그룹 en13)

- verdict: 그 언어에만, dim: 각도, base: 73.33, 표 안: 아니오
- 언급:
  - [Gliese 86 b] raw `73.33°` (줄 12, 뒤):   - Longitude of ascending node: 【73.33°】+0.10° −0.11°
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S116 (묶음 B, exoplanets, en, 그룹 en1)

- verdict: 그 언어에만, dim: 각도, base: -77.179, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `−77.179°` (줄 11, 뒤):   - Inclination: 38.898°+15.759° 【−77.179°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S117 (묶음 B, rare_earth, en, 그룹 en87)

- verdict: 그 언어에만, dim: 에너지, base: 1.49964e-14, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `93.6(4) keV` (줄 28, 뒤): | ¹²⁵ᵐCe | 【93.6(4) keV】 | 93.6(4) keV | 93.6(4) keV | 2007 | 13(10) s | IT | ¹²⁵Ce | (1/2+) |  |  |
  - [Isotopes of cerium] raw `93.6(4) keV` (줄 28, 뒤): | ¹²⁵ᵐCe | 93.6(4) keV | 【93.6(4) keV】 | 93.6(4) keV | 2007 | 13(10) s | IT | ¹²⁵Ce | (1/2+) |  |  |
  - [Isotopes of cerium] raw `93.6(4) keV` (줄 28, 뒤): | ¹²⁵ᵐCe | 93.6(4) keV | 93.6(4) keV | 【93.6(4) keV】 | 2007 | 13(10) s | IT | ¹²⁵Ce | (1/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S118 (묶음 B, exoplanets, en, 그룹 en2)

- verdict: 그 언어에만, dim: 각도, base: -21.642, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `−21.642°` (줄 12, 뒤):   - Longitude of ascending node: 16.684°+148.950° 【−21.642°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S119 (묶음 B, exoplanets, en, 그룹 en16)

- verdict: 그 언어에만, dim: 각도, base: 264.57, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `264.570°` (줄 14, 뒤):   - Argument of periastron: 【264.570°】+3.372° −3.544°
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 246.005: [HD 147513 b] raw `16ʰ 24ᵐ 01.2899ˢ` (줄 6): - 적경: 【16ʰ 24ᵐ 01.2899ˢ】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S120 (묶음 B, exoplanets, en, 그룹 en39)

- verdict: 그 언어에만, dim: 질량, base: 0.00105, 표 안: 아니오
- 언급:
  - [HAT-P-9b] raw `1.05 g` (줄 16, 뒤):   - Surface gravity: 10.3 m/s² (34 ft/s²) 【1.05 g】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S121 (묶음 B, rare_earth, en, 그룹 en79)

- verdict: 그 언어에만, dim: 압력, base: 6e+08, 표 안: 아니오
- 언급:
  - [Holmium] raw `600 MPa` (줄 44, 뒤):   - Vickers hardness: 410–【600 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S122 (묶음 B, rare_earth, en, 그룹 en64)

- verdict: 그 언어에만, dim: 시간, base: 18360, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `5.1(3) h` (줄 42, 뒤): | ¹³³ᵐCe | 37.2(7) keV | 37.2(7) keV | 37.2(7) keV | 1967 | 【5.1(3) h】 | β⁺ | ¹³³La | 9/2− |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 17640: [세륨 동위 원소] raw `4.9(4) h` (줄 34): | ¹³³ᵐCe | 37.1(8) keV | 37.1(8) keV | 37.1(8) keV | 【4.9(4) h】 | β⁺ | ¹³³La | 9/2- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S123 (묶음 B, exoplanets, en, 그룹 en31)

- verdict: 그 언어에만, dim: 밀도, base: 380, 표 안: 아니오
- 언급:
  - [HAT-P-9b] raw `0.38 g/cm³` (줄 15, 뒤):   - Mean density: 【0.38 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S124 (묶음 B, rare_earth, en, 그룹 en46)

- verdict: 그 언어에만, dim: 시간, base: 28.6, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `28.6(7) s` (줄 31, 뒤): | ¹²⁷ᵐ¹Ce | 7.3(11) keV | 7.3(11) keV | 7.3(11) keV | 1996 | 【28.6(7) s】 | β⁺ | ¹²⁷La | (5/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 29: [세륨 동위 원소] raw `29(2) s` (줄 24): | ¹²⁷Ce | 58 | 69 | 126.92273(6) | 【29(2) s】 | β⁺ | ¹²⁷La | 5/2+# |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S125 (묶음 B, rare_earth, en, 그룹 en96)

- verdict: 그 언어에만, dim: 에너지, base: 5.14074e-13, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `3208.6(4) keV` (줄 44, 뒤): | ¹³⁴ᵐCe | 【3208.6(4) keV】 | 3208.6(4) keV | 3208.6(4) keV | 1980 | 308(5) ns | IT | ¹³⁴Ce | 10+ |  |  |
  - [Isotopes of cerium] raw `3208.6(4) keV` (줄 44, 뒤): | ¹³⁴ᵐCe | 3208.6(4) keV | 【3208.6(4) keV】 | 3208.6(4) keV | 1980 | 308(5) ns | IT | ¹³⁴Ce | 10+ |  |  |
  - [Isotopes of cerium] raw `3208.6(4) keV` (줄 44, 뒤): | ¹³⁴ᵐCe | 3208.6(4) keV | 3208.6(4) keV | 【3208.6(4) keV】 | 1980 | 308(5) ns | IT | ¹³⁴Ce | 10+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.95954e-13: [세륨 동위 원소] raw `3095.5(4) keV` (줄 39): | ¹³⁶ᵐCe | 【3095.5(4) keV】 | 3095.5(4) keV | 3095.5(4) keV | 2.2(2) µs |  |  | 10+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### S126 (묶음 A, rare_earth, en, 그룹 en358)

- verdict: 있을 수 있음, dim: 온도, base: 50, 표 안: 아니오
- 언급:
  - [Samarium] raw `50 K` (줄 149, 뒤): …alence compound where samarium is present both as Sm²⁺ and Sm³⁺ ions in a 3:7 ratio. It belongs to a class of Kondo insulators; at temperatures above 【50 K】, its properties are typical of a Kondo metal, with metallic electrical conductivity characterized by strong electron scattering, whereas at lower tem…
- found: [사마륨] 숫자 글자 `50` (줄 102): - 사마륨-149는 중성자를 잘 흡수하는 성질이 있으므로 원자로의 제어봉에 들어간다. X선 레이저의 제조에도 사용되는데, 이 경우 6.8~7.3나노미터의 파장을 가진 X선이 【50】피코초 동안 방출되므로 다양한 분야에 응용된다.

### S127 (묶음 A, probes, en, 그룹 en222)

- verdict: 있음, dim: 시간, base: 6.31152e+08, 표 안: 아니오
- 언급:
  - [Hinode (satellite)] raw `20 years` (줄 7, 뒤): - Mission duration: 【20 years】, 28 days (elapsed)
  - [NASA] raw `20 years` (줄 227, 뒤): …rger effort (see Discovery, New Frontiers, etc.). The James Webb Space Telescope is a strategic mission that was developed over a period of more than 【20 years】. Strategic missions are developed on an ad-hoc basis as program objectives and priorities are established. Missions like Voyager, had they been devel…
- found: [미국 항공 우주국] raw `20년` (줄 211): … 전략 임무(이전에는 플래그십 임무라고 불림)는 일반적으로 여러 NASA 센터에 걸쳐 있는 대규모 팀에 의해 개발되고 관리되는 전략적 임무이다. 개별 임무는 더 큰 노력의 일부(디스커버리, 뉴 프런티어 등 참조)가 아니라 프로그램 자체가 된다. 제임스 웹 우주망원경은 【20년】 이상에 걸쳐 개발된 전략적 임무이다. 전략적 임무는 프로그램 목표와 우선순위가 설정됨에 따라 임시적으로 개발된다. 보이저와 같은 임무가 오늘날 개발되었다면 전략적 임무였을 것이다. 그레이트 옵저버터리 중 세 개는 전략적 임무였다(찬드라 엑스선 천문대, 콤프턴 감마선 …

### S128 (묶음 A, rare_earth, en, 그룹 en89)

- verdict: 있음, dim: 몰 에너지, base: 6200, 표 안: 아니오
- 언급:
  - [Lanthanum] raw `6.20 kJ/mol` (줄 21, 뒤):   - Heat of fusion: 【6.20 kJ/mol】
- found: [란타넘] raw `6.20 kJ/mol` (줄 20):   - 융해열: 【6.20 kJ/mol】

### S129 (묶음 A, rare_earth, en, 그룹 en272)

- verdict: 있음, dim: 압력, base: 3.4e+08, 표 안: 아니오
- 언급:
  - [Ytterbium] raw `340` (줄 46, 뒤):   - Brinell hardness: 【340】–440 MPa
- found: [이터븀] raw `343 MPa` (줄 42):   - 브리넬 굳기: 【343 MPa】

### S130 (묶음 A, kr_satellites, en, 그룹 en156)

- verdict: 있을 수 있음, dim: 시간, base: 7.57382e+08, 표 안: 아니오
- 언급:
  - [South Korea] raw `24 years` (줄 134, 뒤): …tary alliance with the United States, and the successful hosting of the Winter Olympics in Pyeongchang. In April 2018, Park Geun-hye was sentenced to 【24 years】 in jail and convicted of abuse of power and corruption. The COVID-19 pandemic caused South Korea to record more deaths than births, resulting in a po…
- found: [무궁화 5호] 숫자 글자 `24` (줄 41): - 탑재체: 고출력 중계기 (민간용 【24】개, 군용 12개)

### S131 (묶음 A, kr_satellites, en, 그룹 en169)

- verdict: 있음, dim: 온도, base: 265.928, 표 안: 아니오
- 언급:
  - [South Korea] raw `19` (줄 146, 뒤): …ainy season called jangma, which begins end of June and lasts through the end of July. In Seoul, the average January temperature range is −7 to 1 °C (【19】 to 34 °F), and the average August temperature range is 22 to 30 °C (72 to 86 °F). Winter temperatures are higher along the southern coast and conside…
  - [South Korea] raw `−7` (줄 146, 뒤): …ng a short rainy season called jangma, which begins end of June and lasts through the end of July. In Seoul, the average January temperature range is 【−7】 to 1 °C (19 to 34 °F), and the average August temperature range is 22 to 30 °C (72 to 86 °F). Winter temperatures are higher along the southern coast…
- found: [대한민국] raw `-6` (줄 192): …기온과 습도가 점차 낮아지기 시작하여 12월에서 2월까지는 춥고 건조한 겨울 날씨를 보인다. 중부 산간 지방을 제외하고 대체로 연 평균 기온은 10~16℃이며, 가장 무더운 달인 8월은 23~36℃, 5월은 16~19℃, 10월은 11~19℃, 가장 추운 달인 1월은 【-6】~3℃이다.

### S132 (묶음 A, kr_satellites, en, 그룹 en145)

- verdict: 있음, dim: 시간, base: 6.912e+07, 표 안: 아니오
- 언급:
  - [Coordinated Universal Time] raw `800 days` (줄 204, 뒤): …d of the 20th century, with the LOD at 1.3 ms above the nominal value, UTC ran faster than UT by 1.3 ms per day, getting a second ahead roughly every 【800 days】. Thus, leap seconds were inserted at approximately this interval, retarding UTC to keep it synchronised in the long term. The actual rotational perio…
  - [Coordinated Universal Time] raw `800 days` (줄 206, 뒤): Just as adding a leap day every four years does not mean the year is getting longer by one day every four years, the insertion of a leap second every 【800 days】 does not indicate that the mean solar day is getting longer by a second every 800 days. It will take about 50,000 years for a mean solar day to lengt…
  - [Coordinated Universal Time] raw `800 days` (줄 206, 뒤): …one day every four years, the insertion of a leap second every 800 days does not indicate that the mean solar day is getting longer by a second every 【800 days】. It will take about 50,000 years for a mean solar day to lengthen by one second (at a rate of 2 ms per century). This rate fluctuates within the rang…
  - [Coordinated Universal Time] raw `800 days` (줄 206, 뒤): …his difference over a period of time: Near the end of the 20th century, this difference was about ⁠1/800⁠ of a second per day; therefore, after about 【800 days】, it accumulated to 1 second (and a leap second was then added).
- found: [협정 세계시] raw `800일` (줄 92): …가 공칭 86,400초를 초과하는 값은 시간이 지남에 따라 누적되어 처음에 평균 태양과 동기화되었던 UTC 날짜가 동기화 해제되어 앞서나가게 한다. 20세기 말, LOD가 공칭 값보다 1.3ms 높은 상태에서 UTC는 UT보다 하루에 1.3ms 더 빠르게 실행되어 약 【800일】마다 1초 앞서게 되었다. 따라서 UTC를 장기적으로 동기화된 상태로 유지하기 위해 대략 이 간격으로 윤초가 삽입되었다. 실제 자전 주기는 지각 변동과 같은 예측 불가능한 요인에 따라 조금씩 달라지며 단순 계산만으로는 파악할 수 없고 실제 관측을 통해 보정해야 한다.

### S133 (묶음 A, rare_earth, en, 그룹 en15)

- verdict: 있음, dim: 길이, base: 2.07e-10, 표 안: 아니오
- 언급:
  - [Lanthanum] raw `207±8 pm` (줄 31, 뒤):   - Covalent radius: 【207±8 pm】
  - [Lanthanide] raw `208.4 pm` (줄 67, 뒤): …ses across the series. Europium stands out, as it has the lowest density in the series at 5.24 g/cm³ and the largest metallic radius in the series at 【208.4 pm】. It can be compared to barium, which has a metallic radius of 222 pm. It is believed that the metal contains the larger Eu²⁺ ion and that there are o…
- found: [란타넘족] raw `208.4 pm` (줄 65): …인한다고 본다(란타넘(920 °C) – 루테튬(1622 °C)). 혼성은 녹는점이 795 °C로 가장 낮은 세륨에서 가장 큰 것으로 추정된다. 란타넘족 금속은 무르며 경도는 계열을 따라 증가한다. 유로퓸은 밀도가 5.24 g/cm³로 계열에서 가장 낮고 금속 반지름이 【208.4 pm】로 가장 커서 두드러진다. 이는 금속 반지름이 222 pm인 바륨과 비교할 수 있다. 금속 내에 더 큰 Eu²⁺ 이온이 포함되어 있고 전도띠에 전자가 두 개만 존재한다고 여겨진다. 이터븀 또한 금속 반지름이 크며 이를 앞과 비슷하게 설명할 수 있다. 란타넘족 금속의 비…

### S134 (묶음 A, rare_earth, en, 그룹 en211)

- verdict: 있음, dim: 시간, base: 230400, 표 안: 아니오
- 언급:
  - [Yttrium] raw `64 hours` (줄 98, 뒤): …clear reactors. In the context of nuclear waste management, the most important isotopes of yttrium are ⁹¹Y and ⁹⁰Y, with half-lives of 58.51 days and 【64 hours】, respectively. Though ⁹⁰Y has a short half-life, it exists in secular equilibrium with its long-lived parent isotope, strontium-90 (⁹⁰Sr) (half-life …
  - [Yttrium] raw `64 hours` (줄 104, 뒤): …lf-life of 25 ms and the most stable is ⁸⁸Y with half-life 106.629 days. Apart from ⁹¹Y, ⁸⁷Y, and ⁹⁰Y, with half-lives of 58.51 days, 79.8 hours, and 【64 hours】, respectively; all other isotopes have half-lives of less than a day and most of less than an hour.
  - [Yttrium] raw `64.05 h` (줄 52, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ⁸⁷Y synth 79.8 h ε ⁸⁷Sr ⁸⁸Y synth 106.63 d ε ⁸⁸Sr ⁸⁹Y 100% stable ⁹⁰Y synth 【64.05 h】 β⁻ ⁹⁰Zr ⁹¹Y synth 58.51 d β⁻ ⁹¹Zr
- found: [이트륨] raw `2.67d` (줄 47):   - 동위체 존재비 반감기 DM DE (MeV) DP ⁸⁷Y 합성 3.35d ε - ⁸⁷Sr γ 0.48 0.38D - ⁸⁸Y 합성 106.6d ε - ⁸⁸Sr γ 1.83 0.89 - ⁸⁹Y 100% 안정 ⁹⁰Y 합성 【2.67d】 β- 2.28 ⁹⁰Zr γ 2.18 - ⁹¹Y 합성 58.5d β- 1.54 ⁹¹Zr γ 1.20 -

### S135 (묶음 A, exoplanets, en, 그룹 en147)

- verdict: 있음, dim: 시간, base: 228433, 표 안: 아니오
- 언급:
  - [Gliese 436 b] raw `2.64389803(26) d` (줄 12, 뒤):   - Orbital period (sidereal): 【2.64389803(26) d】
- found: [글리제 436 b] raw `2.643904 일` (줄 13): - 공전주기: 【2.643904 일】

### S136 (묶음 A, rare_earth, en, 그룹 en170)

- verdict: 있음, dim: 비저항, base: 7e-07, 표 안: 아니오
- 언급:
  - [Praseodymium] raw `0.700 µΩ⋅m` (줄 37, 뒤):   - Electrical resistivity: poly: 【0.700 µΩ⋅m】 (at r.t.)
- found: [프라세오디뮴] raw `700 n Ω·m` (줄 33):   - 전기 저항도: (실온) (α, poly) 【700 n Ω·m】

### S137 (묶음 A, exoplanets, en, 그룹 en5)

- verdict: 있을 수 있음, dim: 각도, base: -13, 표 안: 아니오
- 언급:
  - [Gliese 581c] raw `−13°` (줄 11, 뒤):   - Inclination: 47°+15° 【−13°】
- found: [외계 행성] 숫자 글자 `13` (줄 102): 1. 중수소 열핵 융합 작용이 일어나는 수준보다 낮은 실제 질량(현재로서는 태양과 비슷한 중원소 함량을 지닌 천체의 경우 목성질량 【13】배 수준)을 지니며, 항성 또는 항성의 잔해 주위를 돌아야 한다(어떻게 형성되었는지는 중요하지 않다). 외계 행성으로 인정받기 위해 필요한 최소 질량/크기의 기준은 우리 태양계 천체들의 기준과 동일하다.

### S138 (묶음 A, rare_earth, en, 그룹 en389)

- verdict: 있음, dim: 온도, base: 350, 표 안: 예
- 언급:
  - [Lanthanide] raw `350 K` (줄 61, 뒤): | Magnetic susceptibility χmol /10⁻⁶(cm³·mol⁻¹) | +95.9 | +2500 (β) | +5530 (α) | +5930 (α) | —N/a | +1278 (α) | +30900 | +185000 (【350 K】) | +170000 (α) | +98000 | +72900 | +48000 | +24700 | +67 (β) | +183 |
- found: [란타넘족] raw `350 K` (줄 59): | 자기 감수율 χmol /10⁻⁶(cm³·mol⁻¹) | +95.9 | +2500 (β) | +5530 (α) | +5930 (α) | 빈칸 | +1278 (α) | +30900 | +185000 (【350 K】) | +170000 (α) | +98000 | +72900 | +48000 | +24700 | +67 (β) | +183 |

### S139 (묶음 B, rare_earth, en, 그룹 en104)

- verdict: 있음, dim: 온도, base: 1273.15, 표 안: 아니오
- 언급:
  - [Terbium(III,IV) oxide] raw `1000 °C` (줄 30, 뒤): Tb4O7 is most often produced by ignition of the oxalate or the sulfate in air. The oxalate (at 【1000 °C】) is generally preferred, since the sulfate requires a higher temperature, and it produces an almost black product contaminated with Tb6O11 or other o…
- found: [산화 터븀(III,IV)] raw `1000 °C` (줄 31): Tb4O7은 공기 중에서 옥살산 터븀이나 황산 터븀을 점화하여 가장 자주 생산된다. 황산염은 더 높은 온도를 필요로 하고 Tb6O11이나 다른 산소가 풍부한 산화물로 오염된 거의 검은색에 가까운 생성물을 만들기 때문에, 일반적으로 옥살산염(【1000 °C】에서)이 선호된다.

### S140 (묶음 B, rare_earth, en, 그룹 en82)

- verdict: 있음, dim: 압력, base: 4.02e+10, 표 안: 아니오
- 언급:
  - [Holmium] raw `40.2 GPa` (줄 41, 뒤):   - Bulk modulus: 【40.2 GPa】
- found: [홀뮴] raw `40.2 GPa` (줄 36):   - 부피 탄성 계수: 【40.2 GPa】

### S141 (묶음 B, rare_earth, en, 그룹 en89)

- verdict: 있음, dim: 에너지, base: 7.14266e-14, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `445.81(21) keV` (줄 46, 뒤): | ¹³⁵ᵐCe | 【445.81(21) keV】 | 445.81(21) keV | 445.81(21) keV | 1970 | 20(1) s | IT | ¹³⁵Ce | (11/2−) |  |  |
  - [Isotopes of cerium] raw `445.81(21) keV` (줄 46, 뒤): | ¹³⁵ᵐCe | 445.81(21) keV | 【445.81(21) keV】 | 445.81(21) keV | 1970 | 20(1) s | IT | ¹³⁵Ce | (11/2−) |  |  |
  - [Isotopes of cerium] raw `445.81(21) keV` (줄 46, 뒤): | ¹³⁵ᵐCe | 445.81(21) keV | 445.81(21) keV | 【445.81(21) keV】 | 1970 | 20(1) s | IT | ¹³⁵Ce | (11/2−) |  |  |
- found: [세륨 동위 원소] raw `445.8(2) keV` (줄 37): | ¹³⁵ᵐCe | 【445.8(2) keV】 | 445.8(2) keV | 445.8(2) keV | 20(1) s | IT | ¹³⁵Ce | (11/2-) |  |  |

### S142 (묶음 B, rare_earth, en, 그룹 en36)

- verdict: 있음, dim: 시간, base: 1.1, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `1.1(1) s` (줄 20, 뒤): | ¹²¹Ce | 58 | 63 | 120.94344(43)# | 1997 | 【1.1(1) s】 | β⁺ (99%) | ¹²¹La | 5/2(+#) |  |  |
  - [Isotopes of cerium] raw `1.1(1) s` (줄 21, 뒤): | ¹²¹Ce | 58 | 63 | 120.94344(43)# | 1997 | 【1.1(1) s】 | β⁺, p (1%) | ¹²⁰Ba | 5/2(+#) |  |  |
- found: [세륨 동위 원소] raw `1.1(1) s` (줄 15): | ¹²¹Ce | 58 | 63 | 120.94342(54)# | 【1.1(1) s】 | β⁺ | ¹²¹La | (5/2)(+#) |  |  |

### S143 (묶음 B, rare_earth, en, 그룹 en2)

- verdict: 있음, dim: 길이, base: 5.22e-10, 표 안: 아니오
- 언급:
  - [Scandium dodecaboride] raw `522pm` (줄 23, 뒤): ScB12 was originally reported as having a cubic structure, later studies showed it to have tetragonal structure (unit cell with a=【522pm】, c=735pm). More recently it has been shown that there is indeed a cubic form but that it requires stabilization.
- found: [십이붕소화 스칸듐] raw `522pm` (줄 23): ScB12는 처음에 등축정계 구조를 가진 것으로 보고되었으나, 이후의 연구에서는 정방정계 구조(단위 격자 a=【522pm】, c=735pm)를 가짐이 밝혀졌다. 보다 최근에는 실제로 등축정계 형태가 존재하지만 안정화가 필요하다는 사실이 밝혀졌다.

### S144 (묶음 B, exoplanets, en, 그룹 en23)

- verdict: 있음, dim: 길이, base: 2.99196e+11, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `2.00 AU` (줄 20, 뒤): …t with average velocity of 19.7 km/s. The eccentricity of the planet's orbit is higher than all the planets in the Solar System, bringing as close as 【2.00 AU】 to as far as 3.66 AU from the parent star.
- found: [확인되지 않은 외계 행성 목록] raw `2` (줄 90): | 알데바란 | b | ~11 | 653.8 | ~【2】 | 0.182 | 1997 |

### S145 (묶음 B, exoplanets, en, 그룹 en18)

- verdict: 있음, dim: 길이, base: 7.89877e+09, 표 안: 아니오
- 언급:
  - [HAT-P-9b] raw `0.0528 ± 0.002 AU` (줄 8, 뒤):   - Semi-major axis: 【0.0528 ± 0.002 AU】 (7,900,000 ± 300,000 km)
  - [HAT-P-9b] raw `7,900,000 ± 300,000 km` (줄 8, 뒤):   - Semi-major axis: 0.0528 ± 0.002 AU (【7,900,000 ± 300,000 km】)
- found: [HAT-P-9 b] raw `0.053` (줄 11): - 평균거리(AU): 【0.053】

### S146 (묶음 B, rare_earth, en, 그룹 en3)

- verdict: 있음, dim: 길이, base: 7.35e-10, 표 안: 아니오
- 언급:
  - [Scandium dodecaboride] raw `735pm` (줄 23, 뒤): ScB12 was originally reported as having a cubic structure, later studies showed it to have tetragonal structure (unit cell with a=522pm, c=【735pm】). More recently it has been shown that there is indeed a cubic form but that it requires stabilization.
- found: [십이붕소화 스칸듐] raw `735pm` (줄 23): ScB12는 처음에 등축정계 구조를 가진 것으로 보고되었으나, 이후의 연구에서는 정방정계 구조(단위 격자 a=522pm, c=【735pm】)를 가짐이 밝혀졌다. 보다 최근에는 실제로 등축정계 형태가 존재하지만 안정화가 필요하다는 사실이 밝혀졌다.

### S147 (묶음 B, exoplanets, en, 그룹 en28)

- verdict: 있음, dim: 길이, base: 3.97351e+17, 표 안: 아니오
- 언급:
  - [HD 147513 b] raw `42 light-years` (줄 18, 뒤): HD 147513 b is an exoplanet approximately 【42 light-years】 away in the constellation of Scorpius. It is at least 21% more massive than Jupiter. But unlike Jupiter, it orbits the star much closer, mean distanc…
- found: [HD 147513 b] raw `41.96 광년` (줄 8): - 거리: 【41.96 광년】(12.87 파섹)

### S148 (묶음 B, exoplanets, en, 그룹 en38)

- verdict: 있음, dim: 시간, base: 1.35216e+08, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `1565 days` (줄 20, 뒤): …vian. Based on its mass, the planet would probably be a gas giant with no solid surface. The planet orbits at the average distance of 2.83 AU, taking 【1565 days】 to complete its orbit with average velocity of 19.7 km/s. The eccentricity of the planet's orbit is higher than all the planets in the Solar System, …
- found: [HD 23596 b] raw `1565±21 일` (줄 15): - 공전주기: 【1565±21 일】(4.285년)

### S149 (묶음 B, exoplanets, en, 그룹 en26)

- verdict: 있음, dim: 길이, base: 5.47528e+11, 표 안: 아니오
- 언급:
  - [HD 23596 b] raw `3.66 AU` (줄 20, 뒤): …ty of 19.7 km/s. The eccentricity of the planet's orbit is higher than all the planets in the Solar System, bringing as close as 2.00 AU to as far as 【3.66 AU】 from the parent star.
- found: [HD 23596 b] raw `3.66` (줄 13): - 원일점(AU): 【3.66】

### S150 (묶음 B, rare_earth, en, 그룹 en90)

- verdict: 있음, dim: 에너지, base: 1.20843e-13, 표 안: 예
- 언급:
  - [Isotopes of cerium] raw `754.24(8) keV` (줄 55, 뒤): | ¹³⁹ᵐCe | 【754.24(8) keV】 | 754.24(8) keV | 754.24(8) keV | 1956 | 57.58(32) s | IT | ¹³⁹Ce | 11/2− |  |  |
  - [Isotopes of cerium] raw `754.24(8) keV` (줄 55, 뒤): | ¹³⁹ᵐCe | 754.24(8) keV | 【754.24(8) keV】 | 754.24(8) keV | 1956 | 57.58(32) s | IT | ¹³⁹Ce | 11/2− |  |  |
  - [Isotopes of cerium] raw `754.24(8) keV` (줄 55, 뒤): | ¹³⁹ᵐCe | 754.24(8) keV | 754.24(8) keV | 【754.24(8) keV】 | 1956 | 57.58(32) s | IT | ¹³⁹Ce | 11/2− |  |  |
- found: [세륨 동위 원소] raw `754.24(8) keV` (줄 46): | ¹³⁹ᵐCe | 【754.24(8) keV】 | 754.24(8) keV | 754.24(8) keV | 56.54(13) s | IT | ¹³⁹Ce | 11/2- |  |  |

### D1 (끝까지 읽는 문서: 묶음 A, exoplanets, ko, 목동자리 타우 b, 1877자)

줄 번호는 0부터 센다. 규칙이 읽은 양의 목록 뒤에 줄 번호를 붙인 글 전체가 있다.

규칙이 읽은 양(줄, raw, value, unit, dim):

- 6 | `13ʰ 47ᵐ 17ˢ` | 206.82083333333333 | ° | 각도
- 7 | `+17° 27′ 22″` | 17.45611111111111 | ° | 각도
- 8 | `15 파섹` | 15.0 | 파섹 | 길이
- 11 | `0.046` | 0.046 | AU | 길이
- 13 | `3.3135 일` | 3.3135 | 일 | 시간
- 15 | `0.003067 초각` | 0.003067 | 초각 | 각도
- 25 | `50광년` | 50.0 | 광년 | 길이
- 29 | `469 ± 5 미터` | 469.0 | 미터 | 길이
- 29 | `15년` | 15.0 | 년 | 시간
- 33 | `79.5시간` | 79.5 | 시간 | 시간
- 33 | `1621 켈빈` | 1621.0 | 켈빈 | 온도
- 41 | `1621 켈빈` | 1621.0 | 켈빈 | 온도

```
0: # 목동자리 타우 b
1: 
2: - 목동자리 타우 b
3: - 모항성
4: - 이름: 목동자리 타우
5: - 별자리: 목동자리
6: - 적경: 13ʰ 47ᵐ 17ˢ
7: - 적위: +17° 27′ 22″
8: - 거리: 15 파섹
9: - 겉보기 등급: 4.5
10: - 궤도요소
11: - 평균거리(AU): 0.046
12: - 이심률: 0.018
13: - 공전주기: 3.3135 일
14: - 궤도경사각: - 도
15: - 각거리: 0.003067 초각
16: - 물리적 특징
17: - 질량: 3.9 MJ
18: - 반지름: - RJ
19: - 중원소함량: 0.28 [Fe/H]
20: - 발견 정보
21: - 발견일: 1996 년
22: - 상태: 논문 심사 통과
23: - 외계 행성 목록
24: 
25: 목동자리 타우 b 또는 목동자리 타우 Ab는 지구에서 목동자리 방향으로 50광년 떨어진 곳에 있는 외계 행성이다. 1996년 제오프리 마시와 폴 버틀러 팀은 목동자리 타우별 근처에 행성이 있음을 공표했다. 1999년 이 행성에는 ‘밀레니엄 행성’이라는 이름이 붙었는데, 이는 목동자리 타우 b가 시각적으로 발견된 최초의 외계 행성이라는 의미였다. 그러나 이후 목동자리 타우 b를 시각적으로 관측했다는 것은 증거의 신빙성이 떨어져서 철회되었다.
26: 
27: ## 발견
28: 
29: 이 행성의 발견시기는 1996년으로, 외계 행성이 발견되기 시작하던 때에 알아낸 천체라고 볼 수 있다. 발견자는 샌프란시스코 행성탐사 프로젝트 소속이었던 폴 버틀러와 제오프리 마시로 시선속도법을 이용했다. 항성은 가시광선으로 볼 때 밝았으며 행성은 질량이 컸다. 항성의 시선속도는 초당 469 ± 5 미터였는데 이 수치의 신빙성은 마이클 메이어와 디디어 퀠로즈가 15년 동안 모은 자료를 통해, 신속하게 확인되었다. 타우 b의 존재는 이후 AFOE 행성탐사팀에 의해 검증되었다.
30: 
31: ## 공전궤도 및 질량
32: 
33: 목동자리 타우 b는 다소 질량이 큰 편으로 최소질량이 목성의 네 배 이상이다. 최근 캐나다 MOST 우주망원경을 이용하여 이 행성의 질량이 목성의 7 ~ 8배 수준일 것으로 추측하고 있다. 항성에서 매우 가까이 붙어 있는데 거리는 수성과 태양 간격의 7분의 1밖에 되지 않는다. 한 바퀴 항성을 도는 데 걸리는 시간은 79.5시간에 불과하다. 목동자리 타우는 태양보다 더 뜨겁고 밝기 때문에 타우 b는 알려져 있는 행성들 중 가장 뜨거운 존재에 포함된다. 구체적인 온도는 약 1621 켈빈이다. 직접 외관을 통해 증명한 것은 아니지만, 질량으로 미루어 보아 가스 행성으로 보인다.
34: 
35: 목동자리 타우 b는 생성 초기에는 갈색 왜성이었다가 어머니 항성의 열기 때문에 대기를 대부분 우주 공간으로 날려 지금의 행성급 질량만 남은 것으로 추측한 적도 있었으나, 현재는 그럴 가능성은 적은 것으로 알려졌다. 다만 HD 209458 b 같은 경우 대기가 우주 공간으로 달아나는 현상이 진행 중인 것으로 관측되고 있다.
36: 
37: 1999년 12월 앤드루 콜리어 카메론 연구진은 행성이 항성의 빛을 받아 빛나는 모습을 포착했다고 발표했다. 이들은 행성의 궤도경사각은 29도로 타우 b의 실제 질량이 목성의 8.5배라고 했다. 이들은 행성을 인간의 눈으로 보면 푸른 색으로 빛날 것이라고 추측했다. 불행하게도 이들의 관측 결과는 아직 검증되지 못했으며 이후 신빙성이 없는 것으로 결론지어졌다.
38: 
39: ## 특징
40: 
41: 목동자리 타우 b는 뜨거운 열기 때문에 반지름이 목성보다 20퍼센트 더 클 것으로 생각된다. 아직까지 이 행성이 내는 빛이 포착된 적은 없으므로, 행성의 반사율은 0.39보다 낮을 것으로 생각된다. 표면 온도가 1621 켈빈 정도일 경우 수다르스키가 추측했던 외계행성의 겉모습에 미루어 보아 작열형 V일 것으로 생각되며 이 경우 반사율은 0.55까지 올라갈 것이다.
42: 
43: 목동자리 타우 A를 보다 먼 거리에서 돌고 있는 행성이 더 있을 것이라는 증거들이 존재한다. 그러나 가상의 행성이 공전을 1회 마치는 시간이 차기 전까지는 그 존재를 확신할 수 없다.
44: 
```

### D2 (끝까지 읽는 문서: 묶음 B, exoplanets, ko, HD 23596 b, 1011자)

줄 번호는 0부터 센다. 규칙이 읽은 양의 목록 뒤에 줄 번호를 붙인 글 전체가 있다.

규칙이 읽은 양(줄, raw, value, unit, dim):

- 6 | `03ʰ 48ᵐ 00.3739ˢ` | 57.00155791666667 | ° | 각도
- 7 | `+40° 31′ 50.287″` | 40.530635277777776 | ° | 각도
- 8 | `170 광년` | 170.0 | 광년 | 길이
- 8 | `52 파섹` | 52.0 | 파섹 | 길이
- 11 | `2.83` | 2.83 | AU | 길이
- 12 | `2.00` | 2.0 | AU | 길이
- 13 | `3.66` | 3.66 | AU | 길이
- 15 | `1565±21 일` | 1565.0 | 일 | 시간
- 15 | `4.285년` | 4.285 | 년 | 시간
- 18 | `11400 g/cm³` | 11400.0 | g/cm³ | 밀도
- 19 | `216 g` | 216.0 | g | 질량
- 20 | `196 켈빈` | 196.0 | 켈빈 | 온도
- 29 | `170광년` | 170.0 | 광년 | 길이
- 29 | `2.83 천문단위` | 2.83 | 천문단위 | 길이
- 29 | `1565일` | 1565.0 | 일 | 시간
- 29 | `초속 19.7 킬로미터` | 19.7 | 킬로미터 | 속도
- 29 | `2 천문단위` | 2.0 | 천문단위 | 길이
- 29 | `3.66 천문단위` | 3.66 | 천문단위 | 길이

```
0: # HD 23596 b
1: 
2: - HD 23596 b
3: - 모항성
4: - 이름: HD 23596
5: - 별자리: 페르세우스자리
6: - 적경: 03ʰ 48ᵐ 00.3739ˢ
7: - 적위: +40° 31′ 50.287″
8: - 거리: 170 광년(52 파섹)
9: - 형태: F8
10: - 궤도요소
11: - 평균거리(AU): 2.83
12: - 근일점(AU): 2.00
13: - 원일점(AU): 3.66
14: - 이심률: 0.292±0.023
15: - 공전주기: 1565±21 일(4.285년)
16: - 물리적 특징
17: - 질량: >7.80±0.35 목성질량(2,480 지구질량)
18: - 밀도: ~11400 g/cm³
19: - 표면중력: ~216 g
20: - 온도: ~196 켈빈
21: - 발견 정보
22: - 발견일: 2002년 6월
23: - 발견자: Perrier 연구진
24: - 발견방법: 도플러 분광법
25: - 발견지역: Haute-Provence Observatory
26: - 상태: 논문 출판됨
27: - 외계 행성 목록
28: 
29: HD 23596 b는 페르세우스자리 방향으로 지구로부터 약 170광년 떨어진 곳에 있는 외계 행성이다. 이 행성은 매우 무거운데, 적어도 목성 질량의 약 7.8배는 되므로 슈퍼 목성으로 분류할 수 있다. 질량에 기초하면 이 행성은 아마도 단단한 표면이 없는, 가스 행성일 것이다. 항성으로부터 평균 2.83 천문단위 떨어져 있으며 1565일 걸려 초속 19.7 킬로미터 속도로 항성 주위를 1회 돈다. 다만 행성 궤도는 다소 찌그러져 있으며 항성에 가까워질 때는 2 천문단위, 멀어질 때 3.66 천문단위까지 물러난다.
30: 
31: Perrier 연구진이 2002년 도플러 분광법을 이용하여 발견했다. 도플러 분광법은 행성의 중력 때문에 항성이 흔들려 스펙트럼에 변화가 생기는 것을 찾아내는 것으로, 직접 행성을 관측하지 않아도 그 존재를 알아낼 수 있다는 점에서 외계 행성을 발견하는 가장 보편적인 방법으로 사용되어 왔다. 그러나 이 방법의 가장 큰 문제점은 행성의 정확한 질량을 알 수 없다는 것이다. HD 23596 b의 경우도 예외가 아니어서, 궤도경사각을 모르기 때문에 실제 질량은 훨씬 더 클 수 있다.
32: 
```

### D3 (끝까지 읽는 문서: 묶음 A, probes, en, Yinghuo-1, 6305자)

줄 번호는 0부터 센다. 규칙이 읽은 양의 목록 뒤에 줄 번호를 붙인 글 전체가 있다.

규칙이 읽은 양(줄, raw, value, unit, dim):

- 4 | `1 year` | 1.0 | year | 시간
- 6 | `254 lb` | 254.0 | lb | 질량
- 7 | `750mm` | 750.0 | mm | 길이
- 7 | `750mm` | 750.0 | mm | 길이
- 7 | `650mm` | 650.0 | mm | 길이
- 8 | `90 W` | 90.0 | W | 출력
- 19 | `500 mi` | 500.0 | mi | 길이
- 20 | `50,000 mi` | 50000.0 | mi | 길이
- 22 | `3 days` | 3.0 | days | 시간
- 50 | `200 m` | 200.0 | m | 길이
- 50 | `660 ft` | 660.0 | ft | 길이
- 54 | `8.8 hours` | 8.8 | hours | 시간
- 66 | `91 mi` | 91.0 | mi | 길이
- 70 | `2.5 ft` | 2.5 | ft | 길이
- 71 | `2.5 ft` | 2.5 | ft | 길이
- 72 | `2.0 ft` | 2.0 | ft | 길이
- 73 | `254 lb` | 254.0 | lb | 질량
- 74 | `18 ft` | 18.0 | ft | 길이
- 74 | `90 W` | 90.0 | W | 출력
- 74 | `180 W` | 180.0 | W | 출력
- 75 | `950 mm` | 950.0 | mm | 길이
- 75 | `12 W` | 12.0 | W | 출력
- 75 | `7.17 GHz` | 7.17 | GHz | 진동수

```
0: # Yinghuo-1
1: 
2: - Mission type: Mars orbiter
3: - Operator: CNSA
4: - Mission duration: 1 year in Mars orbit (planned) Never departed Earth orbit
5: - Spacecraft properties
6:   - Launch mass: 115 kilograms (254 lb)
7:   - Dimensions: 750mm x 750mm x 650mm (stowed)
8:   - Power: 90 W, solar array
9: - Start of mission
10:   - Launch date: 8 November 2011, 20:16:03 UTC
11:   - Rocket: Zenit-2M
12:   - Launch site: Baikonur 45/1
13:   - Deployed from: Fobos-Grunt (planned)
14: - End of mission
15:   - Decay date: 15 January 2012
16: - Orbital parameters
17:   - Reference system: Areocentric (planned) Geocentric (achieved)
18:   - Regime: Low Earth (achieved)
19:   - Perigee altitude: 800 kilometres (500 mi) (planned)
20:   - Apogee altitude: 80,000 kilometres (50,000 mi) (planned)
21:   - Inclination: 5 degrees (planned)
22:   - Period: 3 days (planned)
23: 
24: Yinghuo-1 (simplified Chinese: 萤火一号; traditional Chinese: 螢火一號; pinyin: Yínghuǒ yī hào) was a Chinese Mars-exploration space probe, intended to be the first Chinese planetary space probe and the first Chinese spacecraft to orbit Mars. It was launched from Baikonur Cosmodrome, Kazakhstan, on 8 November 2011, along with the Russian Fobos-Grunt sample return spacecraft, which was intended to visit Mars's moon Phobos. The 115-kg (250-lb) Yinghuo-1 probe was intended by the CNSA to orbit Mars for about two years, studying the planet's surface, atmosphere, ionosphere and magnetic field. Shortly after launch, Fobos-Grunt was expected to perform two burns to depart Earth orbit bound for Mars. However, these burns did not take place, leaving both probes stranded in orbit. On 17 November 2011, CNSA reported that Yinghuo-1 had been declared lost. After a period of orbital decay, Yinghuo-1 and Fobos-Grunt underwent destructive re-entry on 15 January 2012, finally disintegrating over the Pacific Ocean.
25: 
26: As a result, CNSA subsequently moved to embark on an independent Mars exploration program, which culminated in the Tianwen-1 orbiter-lander-rover mission that successfully landed the Zhurong rover on Mars on 22 May, 2021.
27: 
28: ## Name
29: 
30: Yinghuo-1's name (simplified Chinese: 萤火; traditional Chinese: 螢火; pinyin: yínghuǒ; lit. 'luminous fire'; trans. "firefly") was a tribute to the near-homophone yínghuò (荧惑; 熒惑). This word, a short form of "shimmering planet" (熒惑星; yínghuò xīng), is an ancient Chinese name for Mars.
31: 
32: ## Background
33: 
34: On 26 March 2007, the director of the China National Space Administration, Sun Laiyan, and the head of the Russian Space Agency, Anatoly Perminov, signed a landmark space co-operation accord, entitled the "Cooperative Agreement between the China National Space Administration and the Russian Space Agency on joint Chinese-Russian exploration of Mars". One stipulation of the agreement was the construction and launch of the Yinghuo Mars orbiter and its Russian counterpart, Fobos-Grunt.
35: 
36: ## Instruments and objectives
37: 
38: Yinghuo-1's primary scientific objectives were:
39: 
40: 1. To conduct detailed investigation of the plasma environment and magnetic field around Mars.
41: 2. To study Martian ion escape processes and their possible mechanisms
42: 3. To conduct ionosphere occultation measurements between Yinghuo-1 and Fobos-Grunt, focusing on the sub-solar and midnight regions.
43: 4. To observe sandstorms on the Martian surface.
44: 
45: The probe's science payload consisted of four instrument:
46: 
47: 1. A plasma package, consisting of an electron analyzer, ion analyzer and mass spectrometer.
48: 2. A fluxgate magnetometer.
49: 3. A radio-occultation sounder.
50: 4. An optical imaging system consisting of two cameras with 200 m (660 ft) resolution for high-quality images of the Martian surface to be captured from orbit.
51: 
52: ## Mission profile
53: 
54: Following its transit to Mars, Yinghuo-1 was planned to separate from Fobos-Grunt in October 2012 and enter a 72.8-hour equatorial Martian orbit, with an orbital inclination of approximately 5 degrees. Fobos-Grunt and Yinghuo-1 would have conducted Mars ionosphere occultation experiments together, although Fobos-Grunt's primary objective was to obtain surface samples from the Martian moon Phobos. Yinghuo-1 would have experienced periods of up to 8.8 hours in darkness when its orbit carried it over Mars's nightside; it would have run on battery power during these periods, as its solar panels would have been unusable without direct sunlight.
55: 
56: ### Launch processing
57: 
58: On 17 October 2011, the completed Yinghuo-1 satellite arrived at Baikonur Cosmodrome with Fobos-Grunt, beginning payload processing operations in preparation for its November launch.
59: 
60: ### Launch and orbital burn failure
61: 
62: China's Yinghuo-1 and the Russian Fobos-Grunt spacecraft were launched together aboard a Ukrainian Zenit rocket with a Fregat upper stage from Baikonur Cosmodrome, Kazakhstan, on 8 November 2011. Shortly after launch, Fobos-Grunt was expected to perform two burns to depart Earth orbit and begin its journey to Mars. However, these burns did not take place, stranding the two spacecraft in their parking orbit. Despite repeated efforts to contact the launcher and rectify the problem, the spacecraft continued to lose altitude. On 17 November, Chinese state media formally declared the Yinghuo-1 probe lost, and the launcher's orbit gradually began to decay.
63: 
64: ### Destructive re-entry
65: 
66: On 14 January 2012, it was reported that Fobos-Grunt and Yinghuo-1 were beginning their final descent into Earth's atmosphere, falling at a rate of several hundred metres per hour from their 147-kilometre (91 mi) orbital altitude. The two spacecraft completed their re-entry and disintegrated over the Pacific Ocean on 15 January 2012.
67: 
68: ## Specifications
69: 
70: - Length: 0.75 metres (2.5 ft) (excluding solar panels).
71: - Width: 0.75 metres (2.5 ft).
72: - Height: 0.6 metres (2.0 ft).
73: - Mass: 115 kilograms (254 lb).
74: - Power: 3-axis stabilised, 2×3 section solar array with a full-extended length of 5.6 metres (18 ft), providing average power of 90 W, and peak power of 180 W.
75: - HGA: 950 mm antenna dish (S-band) with a 12 W transmitter in two frequencies (8.4 and 7.17 GHz) and a data rate between 8 bit/s and 16 kbit/s.
76: - LGA: 80 bit/s data rate.
77: 
78: ## Further reading
79: 
80: - Zheng, Wei; Hsu, Houtse; Zhong, Min; Yun, Meijuan (2011). "China's first-phase Mars Exploration Program: Yinghuo-1 orbiter". Planetary and Space Science. 86: 155–159. Bibcode:2013P&SS...86..155Z. doi:10.1016/j.pss.2011.02.008.
81: 
```

### D4 (끝까지 읽는 문서: 묶음 B, rare_earth, en, Terbium(III,IV) oxide, 3447자)

줄 번호는 0부터 센다. 규칙이 읽은 양의 목록 뒤에 줄 번호를 붙인 글 전체가 있다.

규칙이 읽은 양(줄, raw, value, unit, dim):

- 14 | `747.6972 g/mol` | 747.6972 | g/mol | 몰 질량
- 16 | `7.3 g/cm³` | 7.3 | g/cm³ | 밀도
- 30 | `1000 °C` | 1000.0 | °C | 온도
- 34 | `350 °C` | 350.0 | °C | 온도
- 46 | `350` | 350.0 | °C | 온도
- 46 | `400 °C` | 400.0 | °C | 온도

```
0: # Terbium(III,IV) oxide
1: 
2: - Names
3: - IUPAC name Tetraterbium heptaoxide
4: - Other names Terbium(III,IV) oxide, Terbium peroxide
5: - Identifiers
6: - 3D model (JSmol) Interactive image
7: - ChemSpider 17339486
8: - EC Number 234-856-3
9: - PubChem CID 16211492
10: - InChI InChI=1S/7O.4Tb Key: UWZVBPNIJCKCMC-UHFFFAOYSA-N
11: - SMILES O=[Tb]O[Tb](=O)O[Tb](=O)O[Tb]=O
12: - Properties
13: - Chemical formula Tb4O7
14: - Molar mass 747.6972 g/mol
15: - Appearance Dark brown-black hygroscopic solid.
16: - Density 7.3 g/cm³
17: - Melting point Decomposes to Tb2O3
18: - Solubility in water Insoluble
19: - Hazards
20: - Occupational safety and health (OHS/OSH):
21: - Main hazards Oxidising agent.
22: - Related compounds
23: - Other cations Terbium(III) oxide Terbium(IV) oxide
24: - Related compounds Cerium(IV) oxide Praseodymium(III,IV) oxide
25: 
26: Terbium(III,IV) oxide, occasionally called tetraterbium heptaoxide, has the formula Tb4O7, though some texts refer to it as TbO1.75. There is some debate as to whether it is a discrete compound, or simply one phase in an interstitial oxide system. Tb4O7 is one of the main commercial terbium compounds, and the only such product containing at least some Tb(IV) (terbium in the +4 oxidation state), along with the more stable Tb(III). It is produced by heating the metal oxalate, and it is used in the preparation of other terbium compounds. It is also used in electronics and data storage, green energy technologies, medical imaging and diagnosis, and chemical processes. Terbium forms three other major oxides: Tb2O3, TbO2, and Tb6O11.
27: 
28: ## Synthesis
29: 
30: Tb4O7 is most often produced by ignition of the oxalate or the sulfate in air. The oxalate (at 1000 °C) is generally preferred, since the sulfate requires a higher temperature, and it produces an almost black product contaminated with Tb6O11 or other oxygen-rich oxides.
31: 
32: ## Chemical properties
33: 
34: Terbium(III,IV) oxide loses O2 when heated at high temperatures; at more moderate temperatures (ca. 350 °C) it reversibly loses oxygen, as shown by exchange with¹⁸O2. This property, also seen in Pr6O11 and V2O5, allows it to work like V2O5 as a redox catalyst in reactions involving oxygen. It was found as early as 1916 that hot Tb4O7 catalyses the reaction of coal gas (CO + H2) with air, leading to incandescence and often ignition.
35: 
36: Tb4O7 reacts with atomic oxygen to produce TbO2, but more convenient preparations are available.
37: 
38: Tb 4O 7 (s) + 6 HCl (aq) → 2 TbO 2 (s) + 2 TbCl 3 (aq) + 3 H 2O (l)
39: 
40: Tb4O7 reacts with other hot concentrated acids to produce terbium(III) salts. For example, reaction with sulfuric acid gives terbium(III) sulfate. Terbium oxide reacts slowly with hydrochloric acid to form terbium(III) chloride solution, and elemental chlorine. At ambient temperature, complete dissolution might require a month; in a hot water bath, about a week.
41: 
42: Anhydrous terbium(III) chloride can be produced by the ammonium chloride route. In the first step, terbium oxide is heated with ammonium chloride to produce the ammonium salt of the pentachloride:
43: 
44: Tb4O7 + 22 NH4Cl → 4 (NH4)2TbCl5 + 7 H2O + 14 NH3
45: 
46: In the second step, the ammonium chloride salt is converted to the trichlorides by heating in a vacuum at 350-400 °C:
47: 
48: (NH4)2TbCl5 → TbCl3 + 2 HCl + 2 NH3
49: 
50: ## Further reading
51: 
52: - CRC Handbook of Chemistry and Physics (71st ed.). Ann Arbor, Michigan: CRC Press. 1990. ISBN 978-0-8493-0471-2.
53: - Mellor, J.W. A Comprehensive Treatise on Inorganic and Theoretical Chemistry. London: Longmans, Green & Co. pp. 692–696.
54: 
```
