# 질문 재료 후보 (materials.py)

부딪히는 값 목록: `/Users/seungchan/Workspace/MultilingualAgentRAG/data/questions/known_conflicts.json`. 후보는 정해진 순서로 낸 것이고 원문 확인은 AI(Claude)가 해 materials_check.md에 적는다.

- 한국어 적격 자리 539, 쌍 24, 단독 12(표 칸 7); 영어 적격 자리 339, 쌍 24, 단독 12(표 칸 6)

## 한국어

문서: wiki-ko-erbium, wiki-ko-isotopes-of-neodymium, wiki-ko-isotopes-of-terbium, wiki-ko-samarium, wiki-ko-yttrium

### A 여러 문서 연결 쌍 (24)

1. 양 atomic_number - 큰 쪽 Er (68)
- 가 `wiki-ko-erbium:7` `68` = 68 (정보 상자) 대상 Er, 양 atomic_number
  - 줄: `  - 원자 번호 (Z): 68`
  - 표시: 반대 언어에 같은 숫자 68: wiki-en-isotopes-of-yttrium:77, wiki-en-isotopes-of-yttrium:127, wiki-en-isotopes-of-yttrium:128, wiki-en-isotopes-of-yttrium:129
- 나 `wiki-ko-samarium:7` `62` = 62 (정보 상자) 대상 Sm, 양 atomic_number
  - 줄: `  - 원자 번호 (Z): 62`
  - 표시: 반대 언어에 같은 숫자 62: wiki-en-isotopes-of-yttrium:108, wiki-en-isotopes-of-yttrium:109, wiki-en-neutron-capture-therapy:212

2. 양 atomic_radius, 조건 empirical - 큰 쪽 Sm (185 pm)
- 가 `wiki-ko-erbium:34` `175 pm` = 175 pm (정보 상자) 대상 Er, 양 atomic_radius, 조건 empirical
  - 줄: `  - 원자 반지름: 175 pm (실험값) / 226 pm (계산값)`
  - 표시: 반대 언어에 같은 숫자 175: wiki-en-lutetium:92, wiki-en-lutetium:94
- 나 `wiki-ko-samarium:34` `185 pm` = 185 pm (정보 상자) 대상 Sm, 양 atomic_radius, 조건 empirical
  - 줄: `  - 원자 반지름: 185 pm (실험값) / 238 pm (계산값)`
  - 표시: 반대 언어에 같은 숫자 185: wiki-en-praseodymium:75

3. 양 boiling_point - 큰 쪽 Er (3141 K)
- 가 `wiki-ko-erbium:18` `3141 K` = 3141 K (정보 상자) 대상 Er, 양 boiling_point
  - 줄: `  - 끓는점: 3141 K`
- 나 `wiki-ko-samarium:18` `2067 K` = 2067 K (정보 상자) 대상 Sm, 양 boiling_point
  - 줄: `  - 끓는점: 2067 K`

4. 양 brinell_hardness - 큰 쪽 Er (814 MPa)
- 가 `wiki-ko-erbium:47` `814 MPa` = 814 MPa (정보 상자) 대상 Er, 양 brinell_hardness
  - 줄: `  - 브리넬 굳기: 814 MPa`
- 나 `wiki-ko-samarium:48` `441 MPa` = 441 MPa (정보 상자) 대상 Sm, 양 brinell_hardness
  - 줄: `  - 브리넬 굳기: 441 MPa`

5. 양 bulk_modulus - 큰 쪽 Er (44.4 GPa)
- 가 `wiki-ko-erbium:43` `44.4 GPa` = 44.4 GPa (정보 상자) 대상 Er, 양 bulk_modulus
  - 줄: `  - 부피 탄성 계수: 44.4 GPa`
- 나 `wiki-ko-samarium:44` `37.8 GPa` = 37.8 GPa (정보 상자) 대상 Sm, 양 bulk_modulus
  - 줄: `  - 부피 탄성 계수: (α form) 37.8 GPa`

6. 양 density - 큰 쪽 Er (9.066 g/cm³)
- 가 `wiki-ko-erbium:19` `9.066 g/cm³` = 9.066 g/cm³ (정보 상자) 대상 Er, 양 density
  - 줄: `  - 밀도 (상온 근처): 9.066 g/cm³`
- 나 `wiki-ko-samarium:19` `7.52 g/cm³` = 7.52 g/cm³ (정보 상자) 대상 Sm, 양 density
  - 줄: `  - 밀도 (상온 근처): 7.52 g/cm³`

7. 양 density_liquid_at_mp - 큰 쪽 Er (8.86 g/cm³)
- 가 `wiki-ko-erbium:20` `8.86 g/cm³` = 8.86 g/cm³ (정보 상자) 대상 Er, 양 density_liquid_at_mp
  - 줄: `  - 액체(녹는점)일 때: 8.86 g/cm³`
- 나 `wiki-ko-samarium:20` `7.16 g/cm³` = 7.16 g/cm³ (정보 상자) 대상 Sm, 양 density_liquid_at_mp
  - 줄: `  - 액체(녹는점)일 때: 7.16 g/cm³`

8. 양 electrical_resistivity - 큰 쪽 Sm (0.94 µΩ·m)
- 가 `wiki-ko-erbium:40` `0.860 μ Ω·m` = 0.86 µΩ·m (정보 상자) 대상 Er, 양 electrical_resistivity
  - 줄: `  - 전기 저항도: (실온) (poly) 0.860 μ Ω·m`
- 나 `wiki-ko-samarium:40` `0.940 μ Ω·m` = 0.94 µΩ·m (정보 상자) 대상 Sm, 양 electrical_resistivity
  - 줄: `  - 전기 저항도: (실온) (α, poly) 0.940 μ Ω·m`

9. 양 electronegativity - 큰 쪽 Er (1.24)
- 가 `wiki-ko-erbium:32` `1.24` = 1.24 (정보 상자) 대상 Er, 양 electronegativity
  - 줄: `  - 전기 음성도 (폴링 척도): 1.24`
- 나 `wiki-ko-samarium:32` `1.17` = 1.17 (정보 상자) 대상 Sm, 양 electronegativity
  - 줄: `  - 전기 음성도 (폴링 척도): 1.17`
  - 표시: 반대 언어에 같은 숫자 1.17: wiki-en-isotopes-of-yttrium:86, wiki-en-isotopes-of-yttrium:87, wiki-en-isotopes-of-yttrium:88

10. 양 excitation_energy - 큰 쪽 Tb-142m1 (280.2 keV)
- 가 `wiki-ko-isotopes-of-neodymium:28` `127.97(11) keV` = 127.97 keV (표) 대상 Nd-133m1, 양 excitation_energy
  - 줄: `| ¹³³ᵐ¹Nd | 127.97(11) keV | 127.97(11) keV | 127.97(11) keV | ~70 s | β⁺ | ¹³³Pr | (1/2)+ |  |  |`
- 나 `wiki-ko-isotopes-of-terbium:24` `280.2(10) keV` = 280.2 keV (표) 대상 Tb-142m1, 양 excitation_energy
  - 줄: `| ¹⁴²ᵐ¹Tb | 280.2(10) keV | 280.2(10) keV | 280.2(10) keV | 303(17) ms | IT (99.5%) | ¹⁴²Tb | (5-) |  |`

11. 양 half_life - 큰 쪽 Er-160 (28.58 h)
- 가 `wiki-ko-erbium:57` `28.58 h` = 28.58 h (표) 대상 Er-160, 양 half_life
  - 줄: `| ¹⁶⁰Er | 인공 | 28.58 h | ε | 0.330 | ¹⁶⁰Ho |`
- 나 `wiki-ko-isotopes-of-neodymium:15` `600(150) ms` = 600 ms (표) 대상 Nd-125, 양 half_life
  - 줄: `| ¹²⁵Nd | 60 | 65 | 124.94888(43)# | 600(150) ms |  |  | 5/2(+#) |  |  |`
  - 표시: 반대 언어에 같은 숫자 600: wiki-en-europium:146, wiki-en-europium:156

12. 양 heat_of_fusion - 큰 쪽 Er (19.9 kJ/mol)
- 가 `wiki-ko-erbium:21` `19.90 kJ/mol` = 19.9 kJ/mol (정보 상자) 대상 Er, 양 heat_of_fusion
  - 줄: `  - 융해열: 19.90 kJ/mol`
- 나 `wiki-ko-samarium:21` `8.62 kJ/mol` = 8.62 kJ/mol (정보 상자) 대상 Sm, 양 heat_of_fusion
  - 줄: `  - 융해열: 8.62 kJ/mol`

13. 양 heat_of_vaporization - 큰 쪽 Er (280 kJ/mol)
- 가 `wiki-ko-erbium:22` `280 kJ/mol` = 280 kJ/mol (정보 상자) 대상 Er, 양 heat_of_vaporization
  - 줄: `  - 기화열: 280 kJ/mol`
  - 표시: 반대 언어에 같은 숫자 280: wiki-en-dysprosium:22
- 나 `wiki-ko-samarium:22` `165 kJ/mol` = 165 kJ/mol (정보 상자) 대상 Sm, 양 heat_of_vaporization
  - 줄: `  - 기화열: 165 kJ/mol`
  - 표시: 반대 언어에 같은 숫자 165: wiki-en-thulium:113, wiki-en-dysprosium:126, wiki-en-europium:50

14. 양 ionization_energy, 조건 1st - 큰 쪽 Er (589.3 kJ/mol)
- 가 `wiki-ko-erbium:33` `589.3 kJ/mol` = 589.3 kJ/mol (정보 상자) 대상 Er, 양 ionization_energy, 조건 1st
  - 줄: `  - 이온화 에너지: 1차: 589.3 kJ/mol, 2차: 1150 kJ/mol, 3차: 2194 kJ/mol`
- 나 `wiki-ko-samarium:33` `544.5 kJ/mol` = 544.5 kJ/mol (정보 상자) 대상 Sm, 양 ionization_energy, 조건 1st
  - 줄: `  - 이온화 에너지: 1차: 544.5 kJ/mol, 2차: 1070 kJ/mol, 3차: 2260 kJ/mol`

15. 양 isotopic_mass - 큰 쪽 Tb-140 (139.94581 Da)
- 가 `wiki-ko-isotopes-of-neodymium:23` `129.92851(3)` = 129.92851 Da (표) 대상 Nd-130, 양 isotopic_mass
  - 줄: `| ¹³⁰Nd | 60 | 70 | 129.92851(3) | 21(3) s | β⁺ | ¹³⁰Pr | 0+ |  |  |`
- 나 `wiki-ko-isotopes-of-terbium:18` `139.94581(86)` = 139.94581 Da (표) 대상 Tb-140, 양 isotopic_mass
  - 줄: `| ¹⁴⁰Tb | 65 | 75 | 139.94581(86) | 2.4(2) s | β⁺ (99.74%) | ¹⁴⁰Gd | 5 |  |`

16. 양 lattice_constant, 조건 a - 큰 쪽 Y (364.83 pm)
- 가 `wiki-ko-erbium:37` `355.93 pm` = 355.93 pm (정보 상자) 대상 Er, 양 lattice_constant, 조건 a
  - 줄: `  - 격자 상수: a = 355.93 pm / c = 558.49 pm (20 °C에서)`
- 나 `wiki-ko-yttrium:37` `364.83 pm` = 364.83 pm (정보 상자) 대상 Y, 양 lattice_constant, 조건 a
  - 줄: `  - 격자 상수: a = 364.83 pm / c = 573.17 pm (20 °C에서)`

17. 양 melting_point - 큰 쪽 Er (1770 K)
- 가 `wiki-ko-erbium:17` `1770 K` = 1770 K (정보 상자) 대상 Er, 양 melting_point
  - 줄: `  - 녹는점: 1770 K`
- 나 `wiki-ko-samarium:17` `1345 K` = 1345 K (정보 상자) 대상 Sm, 양 melting_point
  - 줄: `  - 녹는점: 1345 K`

18. 양 molar_heat_capacity - 큰 쪽 Sm (29.54 J/(mol·K))
- 가 `wiki-ko-erbium:23` `28.12 J/(mol·K)` = 28.12 J/(mol·K) (정보 상자) 대상 Er, 양 molar_heat_capacity
  - 줄: `  - 몰열용량: 28.12 J/(mol·K)`
- 나 `wiki-ko-samarium:23` `29.54 J/(mol·K)` = 29.54 J/(mol·K) (정보 상자) 대상 Sm, 양 molar_heat_capacity
  - 줄: `  - 몰열용량: 29.54 J/(mol·K)`

19. 양 natural_abundance - 큰 쪽 Sm-144 (3.07 %)
- 가 `wiki-ko-erbium:58` `0.14%` = 0.14 % (표) 대상 Er-162, 양 natural_abundance
  - 줄: `| ¹⁶²Er | 0.14% | 안정 | 안정 | 안정 | 안정 |`
- 나 `wiki-ko-samarium:58` `3.07%` = 3.07 % (표) 대상 Sm-144, 양 natural_abundance
  - 줄: `| ¹⁴⁴Sm | 3.07% | 안정 | 안정 | 안정 | 안정 |`

20. 양 neutron_number - 큰 쪽 Tb-135 (70)
- 가 `wiki-ko-isotopes-of-neodymium:14` `64` = 64 (표) 대상 Nd-124, 양 neutron_number
  - 줄: `| ¹²⁴Nd | 60 | 64 | 123.95223(64)# | 500# ms |  |  | 0+ |  |  |`
  - 표시: 반대 언어에 같은 숫자 64: wiki-en-ytterbium:53, wiki-en-isotopes-of-yttrium:116, wiki-en-isotopes-of-yttrium:117, wiki-en-isotopes-of-yttrium:130, wiki-en-isotopes-of-yttrium:131 외 1곳
- 나 `wiki-ko-isotopes-of-terbium:12` `70` = 70 (표) 대상 Tb-135, 양 neutron_number
  - 줄: `| ¹³⁵Tb | 65 | 70 |  | 0.94(+33-22) ms |  |  | (7/2-) |  |`
  - 표시: 반대 언어에 같은 숫자 70: wiki-en-thulium:135, wiki-en-ytterbium:9, wiki-en-ytterbium:74, wiki-en-isotopes-of-yttrium:133, wiki-en-isotopes-of-yttrium:134 외 2곳

21. 양 poisson_ratio - 큰 쪽 Sm (0.274)
- 가 `wiki-ko-erbium:45` `0.237` = 0.237 (정보 상자) 대상 Er, 양 poisson_ratio
  - 줄: `  - 푸아송 비: 0.237`
- 나 `wiki-ko-samarium:46` `0.274` = 0.274 (정보 상자) 대상 Sm, 양 poisson_ratio
  - 줄: `  - 푸아송 비: (α form) 0.274`

22. 양 proton_number - 큰 쪽 Tb-135 (65)
- 가 `wiki-ko-isotopes-of-neodymium:14` `60` = 60 (표) 대상 Nd-124, 양 proton_number
  - 줄: `| ¹²⁴Nd | 60 | 64 | 123.95223(64)# | 500# ms |  |  | 0+ |  |  |`
  - 표시: 반대 언어에 같은 숫자 60: wiki-en-isotopes-of-yttrium:46, wiki-en-isotopes-of-yttrium:101, wiki-en-isotopes-of-yttrium:102, wiki-en-neutron-capture-therapy:28
- 나 `wiki-ko-isotopes-of-terbium:12` `65` = 65 (표) 대상 Tb-135, 양 proton_number
  - 줄: `| ¹³⁵Tb | 65 | 70 |  | 0.94(+33-22) ms |  |  | (7/2-) |  |`
  - 표시: 반대 언어에 같은 숫자 65: wiki-en-dysprosium:142, wiki-en-isotopes-of-yttrium:81, wiki-en-isotopes-of-yttrium:118, wiki-en-isotopes-of-yttrium:119, wiki-en-isotopes-of-yttrium:120

23. 양 shear_modulus - 큰 쪽 Er (28.3 GPa)
- 가 `wiki-ko-erbium:42` `28.3 GPa` = 28.3 GPa (정보 상자) 대상 Er, 양 shear_modulus
  - 줄: `  - 전단 탄성 계수: 28.3 GPa`
  - 표시: 반대 언어에 같은 숫자 28.3: wiki-en-dysprosium:71
- 나 `wiki-ko-samarium:43` `19.5 GPa` = 19.5 GPa (정보 상자) 대상 Sm, 양 shear_modulus
  - 줄: `  - 전단 탄성 계수: (α form) 19.5 GPa`

24. 양 speed_of_sound_thin_rod - 큰 쪽 Er (2830 m/s)
- 가 `wiki-ko-erbium:44` `2830 m/s` = 2830 m/s (정보 상자) 대상 Er, 양 speed_of_sound_thin_rod
  - 줄: `  - 음속 (얇은 막대): 2830 m/s (20 °C)`
- 나 `wiki-ko-samarium:45` `2130 m/s` = 2130 m/s (정보 상자) 대상 Sm, 양 speed_of_sound_thin_rod
  - 줄: `  - 음속 (얇은 막대): 2130 m/s (20 °C)`

### B 표·수치·조건 단독 (12)

1. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-ko-erbium:34` `226 pm` = 226 pm (정보 상자) 대상 Er, 양 atomic_radius, 조건 calculated
  - 줄: `  - 원자 반지름: 175 pm (실험값) / 226 pm (계산값)`

2. 표 칸
- `wiki-ko-isotopes-of-neodymium:29` `176.10(10) keV` = 176.1 keV (표) 대상 Nd-133m2, 양 excitation_energy
  - 줄: `| ¹³³ᵐ²Nd | 176.10(10) keV | 176.10(10) keV | 176.10(10) keV | ~300 ns |  |  | (9/2-) |  |  |`

3. 표 칸
- `wiki-ko-isotopes-of-terbium:25` `280.2(10) keV` = 280.2 keV (표) 대상 Tb-142m1, 양 excitation_energy
  - 줄: `| ¹⁴²ᵐ¹Tb | 280.2(10) keV | 280.2(10) keV | 280.2(10) keV | 303(17) ms | β⁺ (0.5%) | ¹⁴²Gd | (5-) |  |`

4. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-ko-samarium:34` `238 pm` = 238 pm (정보 상자) 대상 Sm, 양 atomic_radius, 조건 calculated
  - 줄: `  - 원자 반지름: 185 pm (실험값) / 238 pm (계산값)`

5. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-ko-yttrium:33` `600 kJ/mol` = 600 kJ/mol (정보 상자) 대상 Y, 양 ionization_energy, 조건 1st
  - 줄: `  - 이온화 에너지: 1차: 600 kJ/mol, 2차: 1180 kJ/mol, 3차: 1980 kJ/mol`
  - 표시: 반대 언어에 같은 숫자 600: wiki-en-europium:146, wiki-en-europium:156

6. 표 칸
- `wiki-ko-erbium:57` `0.330` = 0.33 MeV (표) 대상 Er-160, 양 decay_energy
  - 줄: `| ¹⁶⁰Er | 인공 | 28.58 h | ε | 0.330 | ¹⁶⁰Ho |`

7. 표 칸
- `wiki-ko-isotopes-of-neodymium:17` `1.8(4) s` = 1.8 s (표) 대상 Nd-127, 양 half_life
  - 줄: `| ¹²⁷Nd | 60 | 67 | 126.94050(43)# | 1.8(4) s | β⁺ | ¹²⁷Pr | 5/2+# |  |  |`
  - 표시: 반대 언어에 같은 숫자 1.8: wiki-en-praseodymium:89

8. 표 칸
- `wiki-ko-isotopes-of-terbium:12` `0.94(+33-22) ms` = 0.94 ms (표) 대상 Tb-135, 양 half_life
  - 줄: `| ¹³⁵Tb | 65 | 70 |  | 0.94(+33-22) ms |  |  | (7/2-) |  |`

9. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-ko-samarium:33` `1070 kJ/mol` = 1070 kJ/mol (정보 상자) 대상 Sm, 양 ionization_energy, 조건 2nd
  - 줄: `  - 이온화 에너지: 1차: 544.5 kJ/mol, 2차: 1070 kJ/mol, 3차: 2260 kJ/mol`
  - 표시: 반대 언어에 같은 숫자 1070: wiki-en-samarium-cobalt-magnet:14

10. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-ko-yttrium:37` `573.17 pm` = 573.17 pm (정보 상자) 대상 Y, 양 lattice_constant, 조건 c
  - 줄: `  - 격자 상수: a = 364.83 pm / c = 573.17 pm (20 °C에서)`

11. 표 칸
- `wiki-ko-erbium:60` `10.36 h` = 10.36 h (표) 대상 Er-165, 양 half_life
  - 줄: `| ¹⁶⁵Er | 인공 | 10.36 h | ε | 0.376 | ¹⁶⁵Ho |`

12. 표 칸
- `wiki-ko-isotopes-of-neodymium:24` `130.92725(3)` = 130.92725 Da (표) 대상 Nd-131, 양 isotopic_mass
  - 줄: `| ¹³¹Nd | 60 | 71 | 130.92725(3) | 33(3) s | β⁺ | ¹³¹Pr | (5/2)(+#) |  |  |`

## 영어

문서: wiki-en-europium, wiki-en-lanthanum, wiki-en-neutron-capture-therapy, wiki-en-praseodymium, wiki-en-samarium-cobalt-magnet

### A 여러 문서 연결 쌍 (24)

1. 양 atomic_number - 큰 쪽 Eu (63)
- 가 `wiki-en-europium:9` `63` = 63 (정보 상자) 대상 Eu, 양 atomic_number
  - 줄: `  - Atomic number (Z): 63`
  - 표시: 반대 언어에 같은 숫자 63: wiki-ko-isotopes-of-yttrium:13, wiki-ko-isotopes-of-yttrium:14, wiki-ko-isotopes-of-yttrium:82, wiki-ko-isotopes-of-yttrium:83
- 나 `wiki-en-lanthanum:9` `57` = 57 (정보 상자) 대상 La, 양 atomic_number
  - 줄: `  - Atomic number (Z): 57`
  - 표시: 반대 언어에 같은 숫자 57: wiki-ko-isotopes-of-yttrium:58

2. 양 atomic_radius, 조건 empirical - 큰 쪽 La (187 pm)
- 가 `wiki-en-europium:35` `180 pm` = 180 pm (정보 상자) 대상 Eu, 양 atomic_radius, 조건 empirical
  - 줄: `  - Atomic radius: empirical: 180 pm`
  - 표시: 반대 언어에 같은 숫자 180: wiki-ko-isotopes-of-yttrium:88, wiki-ko-yttrium:34, wiki-ko-isotopes-of-terbium:5, wiki-ko-isotopes-of-terbium:79, wiki-ko-isotopes-of-terbium:80
- 나 `wiki-en-lanthanum:35` `187 pm` = 187 pm (정보 상자) 대상 La, 양 atomic_radius, 조건 empirical
  - 줄: `  - Atomic radius: empirical: 187 pm`
  - 표시: 반대 언어에 같은 숫자 187: wiki-ko-ytterbium:35

3. 양 boiling_point - 큰 쪽 La (3737 K)
- 가 `wiki-en-europium:18` `1802 K ​(1529 °C, ​2784 °F)` = 1802 K (정보 상자) 대상 Eu, 양 boiling_point
  - 줄: `  - Boiling point: 1802 K ​(1529 °C, ​2784 °F)`
- 나 `wiki-en-lanthanum:18` `3737 K ​(3464 °C, ​6267 °F)` = 3737 K (정보 상자) 대상 La, 양 boiling_point
  - 줄: `  - Boiling point: 3737 K ​(3464 °C, ​6267 °F)`

4. 양 bulk_modulus - 큰 쪽 La (27.9 GPa)
- 가 `wiki-en-europium:48` `8.3 GPa` = 8.3 GPa (정보 상자) 대상 Eu, 양 bulk_modulus
  - 줄: `  - Bulk modulus: 8.3 GPa`
  - 표시: 반대 언어에 같은 숫자 8.3: wiki-ko-isotopes-of-yttrium:87
- 나 `wiki-en-lanthanum:48` `27.9 GPa` = 27.9 GPa (정보 상자) 대상 La, 양 bulk_modulus
  - 줄: `  - Bulk modulus: α form: 27.9 GPa`

5. 양 covalent_radius - 큰 쪽 La (207 pm)
- 가 `wiki-en-europium:36` `198±6 pm` = 198 pm (정보 상자) 대상 Eu, 양 covalent_radius
  - 줄: `  - Covalent radius: 198±6 pm`
- 나 `wiki-en-lanthanum:36` `207±8 pm` = 207 pm (정보 상자) 대상 La, 양 covalent_radius
  - 줄: `  - Covalent radius: 207±8 pm`

6. 양 density - 큰 쪽 Pr (6.773 g/cm³)
- 가 `wiki-en-lanthanum:19` `6.145 g/cm³` = 6.145 g/cm³ (정보 상자) 대상 La, 양 density
  - 줄: `  - Density (at 20° C): 6.145 g/cm³`
- 나 `wiki-en-praseodymium:19` `6.773 g/cm³` = 6.773 g/cm³ (정보 상자) 대상 Pr, 양 density
  - 줄: `  - Density (at 20° C): 6.773 g/cm³`

7. 양 density_liquid_at_mp - 큰 쪽 La (5.94 g/cm³)
- 가 `wiki-en-europium:20` `5.13 g/cm³` = 5.13 g/cm³ (정보 상자) 대상 Eu, 양 density_liquid_at_mp
  - 줄: `  - when liquid (at m.p.): 5.13 g/cm³`
- 나 `wiki-en-lanthanum:20` `5.94 g/cm³` = 5.94 g/cm³ (정보 상자) 대상 La, 양 density_liquid_at_mp
  - 줄: `  - when liquid (at m.p.): 5.94 g/cm³`

8. 양 discovery - 큰 쪽 neutron (1932)
- 가 `wiki-en-europium:188` `1803` = 1803 (본문) 대상 Ce, 양 discovery
  - 줄: `…longed separation of the rare-earth elements during the 19th century. Cerium had been discovered in 1803, and in the following decades apparently single rare-earth substances were repeatedly shown to cont…`
- 나 `wiki-en-neutron-capture-therapy:14` `in 1932` = 1932 (본문) 대상 neutron, 양 discovery
  - 줄: `James Chadwick discovered the neutron in 1932. Shortly thereafter, H. J. Taylor reported that boron-10 nuclei had a high propensity to capture lo…`

9. 양 electrical_resistivity - 큰 쪽 Eu (0.9 µΩ·m)
- 가 `wiki-en-europium:43` `0.900 µΩ⋅m` = 0.9 µΩ·m (정보 상자) 대상 Eu, 양 electrical_resistivity
  - 줄: `  - Electrical resistivity: poly: 0.900 µΩ⋅m (at r.t.)`
- 나 `wiki-en-lanthanum:43` `615 nΩ⋅m` = 615 nΩ·m (정보 상자) 대상 La, 양 electrical_resistivity
  - 줄: `  - Electrical resistivity: α, poly: 615 nΩ⋅m (at r.t.)`

10. 양 electronegativity - 큰 쪽 Eu (1.2)
- 가 `wiki-en-europium:33` `1.2` = 1.2 (정보 상자) 대상 Eu, 양 electronegativity
  - 줄: `  - Electronegativity: Pauling scale: 1.2`
- 나 `wiki-en-lanthanum:33` `1.10` = 1.1 (정보 상자) 대상 La, 양 electronegativity
  - 줄: `  - Electronegativity: Pauling scale: 1.10`

11. 양 first_isolation - 큰 쪽 La (1923)
- 가 `wiki-en-lanthanum:113` `in 1923` = 1923 (본문) 대상 La, 양 first_isolation
  - 줄: `…eek λανθάνειν [lanthanein] (lit. to lie hidden). Relatively pure lanthanum metal was first isolated in 1923.`
- 나 `wiki-en-praseodymium:122` `In 1803` = 1803 (본문) 대상 ceria, 양 first_isolation
  - 줄: `…ily owning the mine, sent a sample of it to Carl Scheele, who did not find any new elements within. In 1803, after Hisinger had become an ironmaster, he returned to the mineral with Jöns Jacob Berzelius and …`

12. 양 half_life - 큰 쪽 Eu-150 (36.9 y)
- 가 `wiki-en-europium:61` `36.9 y` = 36.9 y (표) 대상 Eu-150, 양 half_life
  - 줄: `| ¹⁵⁰Eu | synth | 36.9 y | β⁺ | ¹⁵⁰Sm |`
- 나 `wiki-en-lanthanum:67` `40.289 h` = 40.289 h (표) 대상 La-140, 양 half_life
  - 줄: `| ¹⁴⁰La | synth | 40.289 h | β⁻ | ¹⁴⁰Ce |`

13. 양 heat_of_fusion - 큰 쪽 Eu (9.21 kJ/mol)
- 가 `wiki-en-europium:21` `9.21 kJ/mol` = 9.21 kJ/mol (정보 상자) 대상 Eu, 양 heat_of_fusion
  - 줄: `  - Heat of fusion: 9.21 kJ/mol`
- 나 `wiki-en-lanthanum:21` `6.20 kJ/mol` = 6.2 kJ/mol (정보 상자) 대상 La, 양 heat_of_fusion
  - 줄: `  - Heat of fusion: 6.20 kJ/mol`

14. 양 heat_of_vaporization - 큰 쪽 La (400 kJ/mol)
- 가 `wiki-en-europium:22` `176 kJ/mol` = 176 kJ/mol (정보 상자) 대상 Eu, 양 heat_of_vaporization
  - 줄: `  - Heat of vaporization: 176 kJ/mol`
  - 표시: 반대 언어에 같은 숫자 176: wiki-ko-ytterbium:34, wiki-ko-lutetium:65
- 나 `wiki-en-lanthanum:22` `400 kJ/mol` = 400 kJ/mol (정보 상자) 대상 La, 양 heat_of_vaporization
  - 줄: `  - Heat of vaporization: 400 kJ/mol`
  - 표시: 반대 언어에 같은 숫자 400: wiki-ko-samarium:107, wiki-ko-yttrium:81

15. 양 ionization_energy, 조건 1st - 큰 쪽 Eu (547.1 kJ/mol)
- 가 `wiki-en-europium:34` `547.1 kJ/mol` = 547.1 kJ/mol (정보 상자) 대상 Eu, 양 ionization_energy, 조건 1st
  - 줄: `  - Ionization energies: 1st: 547.1 kJ/mol, 2nd: 1085 kJ/mol, 3rd: 2404 kJ/mol`
- 나 `wiki-en-lanthanum:34` `538.1 kJ/mol` = 538.1 kJ/mol (정보 상자) 대상 La, 양 ionization_energy, 조건 1st
  - 줄: `  - Ionization energies: 1st: 538.1 kJ/mol, 2nd: 1067 kJ/mol, 3rd: 1850.3 kJ/mol`

16. 양 lattice_constant, 조건 a - 큰 쪽 Eu (458.22 pm)
- 가 `wiki-en-europium:40` `458.22 pm` = 458.22 pm (정보 상자) 대상 Eu, 양 lattice_constant, 조건 a
  - 줄: `  - Lattice constant: a = 458.22 pm (at 20 °C)`
- 나 `wiki-en-lanthanum:40` `0.37742 nm` = 0.37742 nm (정보 상자) 대상 La, 양 lattice_constant, 조건 a
  - 줄: `  - Lattice constants: a = 0.37742 nm / c = 1.2171 nm (at 20 °C)`

17. 양 melting_point - 큰 쪽 Pr (1204 K)
- 가 `wiki-en-lanthanum:17` `1193 K ​(920 °C, ​1688 °F)` = 1193 K (정보 상자) 대상 La, 양 melting_point
  - 줄: `  - Melting point: 1193 K ​(920 °C, ​1688 °F)`
- 나 `wiki-en-praseodymium:17` `1204 K ​(931 °C, ​1708 °F)` = 1204 K (정보 상자) 대상 Pr, 양 melting_point
  - 줄: `  - Melting point: 1204 K ​(931 °C, ​1708 °F)`

18. 양 molar_heat_capacity - 큰 쪽 Eu (27.66 J/(mol·K))
- 가 `wiki-en-europium:23` `27.66 J/(mol·K)` = 27.66 J/(mol·K) (정보 상자) 대상 Eu, 양 molar_heat_capacity
  - 줄: `  - Molar heat capacity: 27.66 J/(mol·K)`
- 나 `wiki-en-lanthanum:23` `27.11 J/(mol·K)` = 27.11 J/(mol·K) (정보 상자) 대상 La, 양 molar_heat_capacity
  - 줄: `  - Molar heat capacity: 27.11 J/(mol·K)`

19. 양 natural_abundance - 큰 쪽 Pr-141 (100 %)
- 가 `wiki-en-lanthanum:66` `99.911%` = 99.911 % (표) 대상 La-139, 양 natural_abundance
  - 줄: `| ¹³⁹La | 99.911% | stable | stable | stable |`
- 나 `wiki-en-praseodymium:62` `100%` = 100 % (표) 대상 Pr-141, 양 natural_abundance
  - 줄: `| ¹⁴¹Pr | 100% | stable | stable | stable |`
  - 표시: 반대 언어에 같은 숫자 100: wiki-ko-thulium:26, wiki-ko-thulium:58, wiki-ko-dysprosium:26, wiki-ko-ytterbium:26, wiki-ko-lutetium:26 외 12곳

20. 양 number_of_electrons - 큰 쪽 Pr (59)
- 가 `wiki-en-lanthanum:79` `57 electrons` = 57 (본문) 대상 La, 양 number_of_electrons
  - 줄: `…um is generally considered the first of the f-block elements by authors writing on the subject. The 57 electrons of a lanthanum atom are arranged in the configuration [Xe]5d¹6s², with three valence electrons outs…`
  - 표시: 반대 언어에 같은 숫자 57: wiki-ko-isotopes-of-yttrium:58
- 나 `wiki-en-praseodymium:77` `59 electrons` = 59 (본문) 대상 Pr, 양 number_of_electrons
  - 줄: `Neutral praseodymium's 59 electrons are arranged in the configuration [Xe]4f³6s². Like most other lanthanides, praseodymium usually use…`
  - 표시: 반대 언어에 같은 숫자 59: wiki-ko-isotopes-of-yttrium:66, wiki-ko-isotopes-of-yttrium:67

21. 양 oxidation_states - 큰 쪽 Pr (4)
- 가 `wiki-en-lanthanum:69` `+3` = 3 (본문) 대상 La, 양 oxidation_states
  - 줄: `…ed among the rare-earth elements. Like most other rare-earth elements, its usual oxidation state is +3, although some compounds are known with an oxidation state of +2. Lanthanum has no biological role …`
- 나 `wiki-en-praseodymium:71` `+4` = 4 (본문) 대상 Pr, 양 oxidation_states
  - 줄: `…dily forms the +3 oxidation state, which is the only stable state in aqueous solution, although the +4 oxidation state is known in some solid compounds and, uniquely among the lanthanides, the +5 oxidat…`

22. 양 poisson_ratio - 큰 쪽 La (0.28)
- 가 `wiki-en-europium:49` `0.152` = 0.152 (정보 상자) 대상 Eu, 양 poisson_ratio
  - 줄: `  - Poisson ratio: 0.152`
- 나 `wiki-en-lanthanum:50` `0.280` = 0.28 (정보 상자) 대상 La, 양 poisson_ratio
  - 줄: `  - Poisson ratio: α form: 0.280`

23. 양 shear_modulus - 큰 쪽 La (14.3 GPa)
- 가 `wiki-en-europium:47` `7.9 GPa` = 7.9 GPa (정보 상자) 대상 Eu, 양 shear_modulus
  - 줄: `  - Shear modulus: 7.9 GPa`
  - 표시: 반대 언어에 같은 숫자 7.9: wiki-ko-isotopes-of-terbium:21
- 나 `wiki-en-lanthanum:47` `14.3 GPa` = 14.3 GPa (정보 상자) 대상 La, 양 shear_modulus
  - 줄: `  - Shear modulus: α form: 14.3 GPa`
  - 표시: 반대 언어에 같은 숫자 14.3: wiki-ko-ytterbium:63

24. 양 specific_heat_capacity - 큰 쪽 La (195.162 J/(kg·K))
- 가 `wiki-en-europium:24` `182.022 J/(kg·K)` = 182.022 J/(kg·K) (정보 상자) 대상 Eu, 양 specific_heat_capacity
  - 줄: `  - Specific heat capacity: 182.022 J/(kg·K)`
- 나 `wiki-en-lanthanum:24` `195.162 J/(kg·K)` = 195.162 J/(kg·K) (정보 상자) 대상 La, 양 specific_heat_capacity
  - 줄: `  - Specific heat capacity: 195.162 J/(kg·K)`

### B 표·수치·조건 단독 (12)

1. 표 칸
- `wiki-en-europium:63` `13.517 y` = 13.517 y (표) 대상 Eu-152, 양 half_life
  - 줄: `| ¹⁵²Eu | synth | 13.517 y | β⁺ | ¹⁵²Sm |`

2. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-en-lanthanum:34` `1067 kJ/mol` = 1067 kJ/mol (정보 상자) 대상 La, 양 ionization_energy, 조건 2nd
  - 줄: `  - Ionization energies: 1st: 538.1 kJ/mol, 2nd: 1067 kJ/mol, 3rd: 1850.3 kJ/mol`

3. 표 칸
- `wiki-en-neutron-capture-therapy:189` `2012` = 2012 (표) 대상 Particle Radiation Oncology Research Center, Kyoto University, Kumatori, Japan, 양 first_clinical_use_year
  - 줄: `…p,n)⁹B Cyclotron | Particle Radiation Oncology Research Center, Kyoto University, Kumatori, Japan | 2012 | Retired from clinical use |`

4. 표 칸
- `wiki-en-praseodymium:63` `19.12 h` = 19.12 h (표) 대상 Pr-142, 양 half_life
  - 줄: `| ¹⁴²Pr | synth | 19.12 h | β⁻ | ¹⁴²Nd |`

5. 표 칸
- `wiki-en-samarium-cobalt-magnet:25` `0.875–2.79` = 0.875–2.79 MA/m (표) 대상 sintered neodymium magnet, 양 coercivity
  - 줄: `| Coercivity (MA/m) | 0.875–2.79 | 0.493–2.79 |`

6. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-en-europium:34` `1085 kJ/mol` = 1085 kJ/mol (정보 상자) 대상 Eu, 양 ionization_energy, 조건 2nd
  - 줄: `  - Ionization energies: 1st: 547.1 kJ/mol, 2nd: 1085 kJ/mol, 3rd: 2404 kJ/mol`

7. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-en-lanthanum:40` `1.2171 nm` = 1.2171 nm (정보 상자) 대상 La, 양 lattice_constant, 조건 c
  - 줄: `  - Lattice constants: a = 0.37742 nm / c = 1.2171 nm (at 20 °C)`

8. 표 칸
- `wiki-en-neutron-capture-therapy:143` `12.8` = 12.8 months (표) 대상 BMRR, US, 양 median_survival_months
  - 줄: `| BMRR, US | 53 (1994–1999) | BPA 250–330 mg/kg | 12.8 |`

9. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-en-praseodymium:34` `527 kJ/mol` = 527 kJ/mol (정보 상자) 대상 Pr, 양 ionization_energy, 조건 1st
  - 줄: `  - Ionization energies: 1st: 527 kJ/mol, 2nd: 1020 kJ/mol, 3rd: 2086 kJ/mol`

10. 표 칸
- `wiki-en-samarium-cobalt-magnet:31` `(3–4)×10⁻⁶` = 0.000003–0.000004 1/K (표) 대상 sintered neodymium magnet, 양 cte,_magnetizing_direction
  - 줄: `| CTE, magnetizing direction (1/K) | (3–4)×10⁻⁶ | (5–9)×10⁻⁶ |`

11. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-en-europium:7` `151.964±0.001` = 151.964 (정보 상자) 대상 Eu, 양 standard_atomic_weight
  - 줄: `  - 151.964±0.001, 151.96±0.01 (abridged)`

12. 본문·정보 상자, 조건이 다른 같은 대상·양이 같은 문서에 있음
- `wiki-en-lanthanum:7` `138.90547±0.00007` = 138.90547 (정보 상자) 대상 La, 양 standard_atomic_weight
  - 줄: `  - 138.90547±0.00007, 138.91±0.01 (abridged)`

