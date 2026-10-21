# 3 세기: 후보 대조 종이 (sheet)

## 판정 기준 (이 종이를 읽는 AI가 지킨다)

- read_ok: 값과 단위를 문서대로 읽었는가(true/false).
- truth(셋 가운데 하나): "그 언어에만" = 코퍼스 안의 반대 언어 문서에 같은 값도, 같은 대상의 같은 양이 다른 값으로 적힌 것(서로 어긋남)도 없다.
  "반대 언어에 있음" = 둘 가운데 하나가 있다. "세는 범위의 수가 아님" = 연도·이름·오차 폭 등.
- 같은 값: ±1% 안이거나, 더 정밀한 값을 덜 정밀한 값의 마지막 자리로 반올림해 같은 것(괄호 안의 환산과 낱말 숫자도 견준다. 정수 끝의 0은 유효 자릿수로 보지 않는다).
- 묶음에 언급이 여럿이면, 바르게 읽은 "그 언어에만"인 사실이 하나라도 있으면 그 묶음은 맞은 것(read_ok true, truth "그 언어에만")이다.
- 견주는 문서는 코퍼스 안의 반대 언어 문서뿐이다.
- 판정은 차례의 앞에서부터 빈틈없이 채운다. 그 쪽 차례로 맞은 것이 18개가 되면 그 쪽은 멈춘다(`status`가 알려 준다).
- 칸은 confirm.json에 채운다: read_ok(true/false), truth, note(글).

## 차례별 목록 (번호만)

### exoplanets ko
- 두 언어 쪽 차례 (18개): E-ko-001, E-ko-002, E-ko-003, E-ko-004, E-ko-005, E-ko-006, E-ko-007, E-ko-008, E-ko-009, E-ko-010, E-ko-011, E-ko-012, E-ko-013, E-ko-014, E-ko-015, E-ko-016, E-ko-017, E-ko-018
- 한쪽 언어 쪽 차례 (54개): E-ko-019, E-ko-020, E-ko-021, E-ko-022, E-ko-023, E-ko-024, E-ko-025, E-ko-026, E-ko-027, E-ko-028, E-ko-029, E-ko-030, E-ko-031, E-ko-032, E-ko-033, E-ko-034, E-ko-035, E-ko-036, E-ko-037, E-ko-038, E-ko-039, E-ko-040, E-ko-041, E-ko-042, E-ko-043, E-ko-044, E-ko-045, E-ko-046, E-ko-047, E-ko-048, E-ko-049, E-ko-050, E-ko-051, E-ko-052, E-ko-053, E-ko-054, E-ko-055, E-ko-056, E-ko-057, E-ko-058, E-ko-059, E-ko-060, E-ko-061, E-ko-062, E-ko-063, E-ko-064, E-ko-065, E-ko-066, E-ko-067, E-ko-068, E-ko-069, E-ko-070, E-ko-071, E-ko-072
- 표 차례 (11개): E-ko-058, E-ko-028, E-ko-023, E-ko-042, E-ko-056, E-ko-059, E-ko-049, E-ko-070, E-ko-034, E-ko-027, E-ko-054
- 모델 시험 차례(결정 ⑥) (21개): E-ko-063, E-ko-049, E-ko-023, E-ko-069, E-ko-054, E-ko-070, E-ko-042, E-ko-059, E-ko-061, E-ko-056, E-ko-047, E-ko-052, E-ko-060, E-ko-034, E-ko-053, E-ko-015, E-ko-027, E-ko-031, E-ko-036, E-ko-028, E-ko-058

### exoplanets en
- 두 언어 쪽 차례 (54개): E-en-001, E-en-002, E-en-003, E-en-004, E-en-005, E-en-006, E-en-007, E-en-008, E-en-009, E-en-010, E-en-011, E-en-012, E-en-013, E-en-014, E-en-015, E-en-016, E-en-017, E-en-018, E-en-019, E-en-020, E-en-021, E-en-022, E-en-023, E-en-024, E-en-025, E-en-026, E-en-027, E-en-028, E-en-029, E-en-030, E-en-031, E-en-032, E-en-033, E-en-034, E-en-035, E-en-036, E-en-037, E-en-038, E-en-039, E-en-040, E-en-041, E-en-042, E-en-043, E-en-044, E-en-045, E-en-046, E-en-047, E-en-048, E-en-049, E-en-050, E-en-051, E-en-052, E-en-053, E-en-054
- 한쪽 언어 쪽 차례 (84개): E-en-055, E-en-056, E-en-057, E-en-058, E-en-059, E-en-060, E-en-061, E-en-062, E-en-063, E-en-064, E-en-065, E-en-066, E-en-067, E-en-068, E-en-069, E-en-070, E-en-071, E-en-072, E-en-073, E-en-074, E-en-075, E-en-076, E-en-077, E-en-078, E-en-079, E-en-080, E-en-081, E-en-082, E-en-083, E-en-084, E-en-085, E-en-086, E-en-087, E-en-088, E-en-089, E-en-090, E-en-091, E-en-092, E-en-093, E-en-094, E-en-095, E-en-096, E-en-097, E-en-098, E-en-099, E-en-100, E-en-101, E-en-102, E-en-103, E-en-104, E-en-105, E-en-106, E-en-107, E-en-108, E-en-109, E-en-110, E-en-111, E-en-112, E-en-113, E-en-114, E-en-115, E-en-116, E-en-117, E-en-118, E-en-119, E-en-120, E-en-121, E-en-122, E-en-123, E-en-124, E-en-125, E-en-126, E-en-127, E-en-128, E-en-129, E-en-130, E-en-131, E-en-132, E-en-133, E-en-134, E-en-135, E-en-136, E-en-137, E-en-138
- 표 차례 (9개): E-en-082, E-en-069, E-en-064, E-en-104, E-en-065, E-en-134, E-en-063, E-en-124, E-en-055
- 모델 시험 차례(결정 ⑥) (50개): E-en-134, E-en-119, E-en-080, E-en-061, E-en-058, E-en-063, E-en-067, E-en-133, E-en-048, E-en-088, E-en-098, E-en-092, E-en-091, E-en-105, E-en-104, E-en-002, E-en-109, E-en-065, E-en-075, E-en-084, E-en-060, E-en-129, E-en-064, E-en-028, E-en-126, E-en-070, E-en-082, E-en-096, E-en-073, E-en-078, E-en-049, E-en-012, E-en-062, E-en-138, E-en-055, E-en-123, E-en-125, E-en-039, E-en-007, E-en-124, E-en-015, E-en-085, E-en-072, E-en-090, E-en-074, E-en-086, E-en-037, E-en-081, E-en-112, E-en-106

### rare_earth ko
- 두 언어 쪽 차례 (22개): R-ko-001, R-ko-002, R-ko-003, R-ko-004, R-ko-005, R-ko-006, R-ko-007, R-ko-008, R-ko-009, R-ko-010, R-ko-011, R-ko-012, R-ko-013, R-ko-014, R-ko-015, R-ko-016, R-ko-017, R-ko-018, R-ko-019, R-ko-020, R-ko-021, R-ko-022
- 한쪽 언어 쪽 차례 (145개): R-ko-023, R-ko-024, R-ko-025, R-ko-026, R-ko-027, R-ko-028, R-ko-029, R-ko-030, R-ko-031, R-ko-032, R-ko-033, R-ko-034, R-ko-035, R-ko-036, R-ko-037, R-ko-038, R-ko-039, R-ko-040, R-ko-041, R-ko-042, R-ko-043, R-ko-044, R-ko-045, R-ko-046, R-ko-047, R-ko-048, R-ko-049, R-ko-050, R-ko-051, R-ko-052, R-ko-053, R-ko-054, R-ko-055, R-ko-056, R-ko-057, R-ko-058, R-ko-059, R-ko-060, R-ko-061, R-ko-062, R-ko-063, R-ko-064, R-ko-065, R-ko-066, R-ko-067, R-ko-068, R-ko-069, R-ko-070, R-ko-071, R-ko-072, R-ko-073, R-ko-074, R-ko-075, R-ko-076, R-ko-077, R-ko-078, R-ko-079, R-ko-080, R-ko-081, R-ko-082, R-ko-083, R-ko-084, R-ko-085, R-ko-086, R-ko-087, R-ko-088, R-ko-089, R-ko-090, R-ko-091, R-ko-092, R-ko-093, R-ko-094, R-ko-095, R-ko-096, R-ko-097, R-ko-098, R-ko-099, R-ko-100, R-ko-101, R-ko-102, R-ko-103, R-ko-104, R-ko-105, R-ko-106, R-ko-107, R-ko-108, R-ko-109, R-ko-110, R-ko-111, R-ko-112, R-ko-113, R-ko-114, R-ko-115, R-ko-116, R-ko-117, R-ko-118, R-ko-119, R-ko-120, R-ko-121, R-ko-122, R-ko-123, R-ko-124, R-ko-125, R-ko-126, R-ko-127, R-ko-128, R-ko-129, R-ko-130, R-ko-131, R-ko-132, R-ko-133, R-ko-134, R-ko-135, R-ko-136, R-ko-137, R-ko-138, R-ko-139, R-ko-140, R-ko-141, R-ko-142, R-ko-143, R-ko-144, R-ko-145, R-ko-146, R-ko-147, R-ko-148, R-ko-149, R-ko-150, R-ko-151, R-ko-152, R-ko-153, R-ko-154, R-ko-155, R-ko-156, R-ko-157, R-ko-158, R-ko-159, R-ko-160, R-ko-161, R-ko-162, R-ko-163, R-ko-164, R-ko-165, R-ko-166, R-ko-167
- 표 차례 (94개): R-ko-043, R-ko-079, R-ko-116, R-ko-095, R-ko-087, R-ko-011, R-ko-051, R-ko-048, R-ko-102, R-ko-015, R-ko-057, R-ko-036, R-ko-072, R-ko-121, R-ko-142, R-ko-128, R-ko-138, R-ko-091, R-ko-115, R-ko-024, R-ko-042, R-ko-114, R-ko-039, R-ko-075, R-ko-160, R-ko-049, R-ko-149, R-ko-155, R-ko-088, R-ko-157, R-ko-129, R-ko-108, R-ko-045, R-ko-125, R-ko-166, R-ko-086, R-ko-103, R-ko-136, R-ko-005, R-ko-067, R-ko-150, R-ko-152, R-ko-030, R-ko-029, R-ko-060, R-ko-132, R-ko-017, R-ko-151, R-ko-028, R-ko-071, R-ko-131, R-ko-064, R-ko-065, R-ko-113, R-ko-089, R-ko-010, R-ko-059, R-ko-038, R-ko-026, R-ko-099, R-ko-006, R-ko-046, R-ko-094, R-ko-080, R-ko-066, R-ko-139, R-ko-052, R-ko-083, R-ko-144, R-ko-110, R-ko-141, R-ko-147, R-ko-021, R-ko-093, R-ko-145, R-ko-056, R-ko-022, R-ko-073, R-ko-047, R-ko-077, R-ko-163, R-ko-124, R-ko-122, R-ko-106, R-ko-111, R-ko-063, R-ko-007, R-ko-018, R-ko-164, R-ko-023, R-ko-101, R-ko-053, R-ko-044, R-ko-033
- 모델 시험 차례(결정 ⑥) (94개): R-ko-043, R-ko-079, R-ko-116, R-ko-095, R-ko-087, R-ko-011, R-ko-051, R-ko-048, R-ko-102, R-ko-015, R-ko-057, R-ko-036, R-ko-072, R-ko-121, R-ko-142, R-ko-128, R-ko-138, R-ko-091, R-ko-115, R-ko-024, R-ko-042, R-ko-114, R-ko-039, R-ko-075, R-ko-160, R-ko-049, R-ko-149, R-ko-155, R-ko-088, R-ko-157, R-ko-129, R-ko-108, R-ko-045, R-ko-125, R-ko-166, R-ko-086, R-ko-103, R-ko-136, R-ko-005, R-ko-067, R-ko-150, R-ko-152, R-ko-030, R-ko-029, R-ko-060, R-ko-132, R-ko-017, R-ko-151, R-ko-028, R-ko-071, R-ko-131, R-ko-064, R-ko-065, R-ko-113, R-ko-089, R-ko-010, R-ko-059, R-ko-038, R-ko-026, R-ko-099, R-ko-006, R-ko-046, R-ko-094, R-ko-080, R-ko-066, R-ko-139, R-ko-052, R-ko-083, R-ko-144, R-ko-110, R-ko-141, R-ko-147, R-ko-021, R-ko-093, R-ko-145, R-ko-056, R-ko-022, R-ko-073, R-ko-047, R-ko-077, R-ko-163, R-ko-124, R-ko-122, R-ko-106, R-ko-111, R-ko-063, R-ko-007, R-ko-018, R-ko-164, R-ko-023, R-ko-101, R-ko-053, R-ko-044, R-ko-033

### rare_earth en
- 두 언어 쪽 차례 (92개): R-en-001, R-en-002, R-en-003, R-en-004, R-en-005, R-en-006, R-en-007, R-en-008, R-en-009, R-en-010, R-en-011, R-en-012, R-en-013, R-en-014, R-en-015, R-en-016, R-en-017, R-en-018, R-en-019, R-en-020, R-en-021, R-en-022, R-en-023, R-en-024, R-en-025, R-en-026, R-en-027, R-en-028, R-en-029, R-en-030, R-en-031, R-en-032, R-en-033, R-en-034, R-en-035, R-en-036, R-en-037, R-en-038, R-en-039, R-en-040, R-en-041, R-en-042, R-en-043, R-en-044, R-en-045, R-en-046, R-en-047, R-en-048, R-en-049, R-en-050, R-en-051, R-en-052, R-en-053, R-en-054, R-en-055, R-en-056, R-en-057, R-en-058, R-en-059, R-en-060, R-en-061, R-en-062, R-en-063, R-en-064, R-en-065, R-en-066, R-en-067, R-en-068, R-en-069, R-en-070, R-en-071, R-en-072, R-en-073, R-en-074, R-en-075, R-en-076, R-en-077, R-en-078, R-en-079, R-en-080, R-en-081, R-en-082, R-en-083, R-en-084, R-en-085, R-en-086, R-en-087, R-en-088, R-en-089, R-en-090, R-en-091, R-en-092
- 한쪽 언어 쪽 차례 (106개): R-en-093, R-en-094, R-en-095, R-en-096, R-en-097, R-en-098, R-en-099, R-en-100, R-en-101, R-en-102, R-en-103, R-en-104, R-en-105, R-en-106, R-en-107, R-en-108, R-en-109, R-en-110, R-en-111, R-en-112, R-en-113, R-en-114, R-en-115, R-en-116, R-en-117, R-en-118, R-en-119, R-en-120, R-en-121, R-en-122, R-en-123, R-en-124, R-en-125, R-en-126, R-en-127, R-en-128, R-en-129, R-en-130, R-en-131, R-en-132, R-en-133, R-en-134, R-en-135, R-en-136, R-en-137, R-en-138, R-en-139, R-en-140, R-en-141, R-en-142, R-en-143, R-en-144, R-en-145, R-en-146, R-en-147, R-en-148, R-en-149, R-en-150, R-en-151, R-en-152, R-en-153, R-en-154, R-en-155, R-en-156, R-en-157, R-en-158, R-en-159, R-en-160, R-en-161, R-en-162, R-en-163, R-en-164, R-en-165, R-en-166, R-en-167, R-en-168, R-en-169, R-en-170, R-en-171, R-en-172, R-en-173, R-en-174, R-en-175, R-en-176, R-en-177, R-en-178, R-en-179, R-en-180, R-en-181, R-en-182, R-en-183, R-en-184, R-en-185, R-en-186, R-en-187, R-en-188, R-en-189, R-en-190, R-en-191, R-en-192, R-en-193, R-en-194, R-en-195, R-en-196, R-en-197, R-en-198
- 표 차례 (64개): R-en-078, R-en-044, R-en-075, R-en-018, R-en-066, R-en-070, R-en-037, R-en-030, R-en-010, R-en-056, R-en-063, R-en-067, R-en-099, R-en-086, R-en-103, R-en-059, R-en-142, R-en-022, R-en-051, R-en-009, R-en-042, R-en-082, R-en-026, R-en-029, R-en-038, R-en-047, R-en-015, R-en-065, R-en-069, R-en-091, R-en-049, R-en-062, R-en-050, R-en-006, R-en-001, R-en-016, R-en-013, R-en-033, R-en-005, R-en-039, R-en-024, R-en-085, R-en-072, R-en-008, R-en-104, R-en-060, R-en-123, R-en-106, R-en-140, R-en-002, R-en-045, R-en-054, R-en-090, R-en-034, R-en-043, R-en-071, R-en-011, R-en-083, R-en-089, R-en-058, R-en-094, R-en-088, R-en-093, R-en-061
- 모델 시험 차례(결정 ⑥) (83개): R-en-163, R-en-075, R-en-045, R-en-140, R-en-071, R-en-097, R-en-103, R-en-094, R-en-172, R-en-010, R-en-123, R-en-083, R-en-051, R-en-089, R-en-065, R-en-029, R-en-042, R-en-133, R-en-099, R-en-026, R-en-016, R-en-022, R-en-018, R-en-034, R-en-058, R-en-069, R-en-110, R-en-134, R-en-024, R-en-145, R-en-038, R-en-088, R-en-193, R-en-056, R-en-009, R-en-093, R-en-142, R-en-015, R-en-085, R-en-054, R-en-166, R-en-005, R-en-192, R-en-037, R-en-001, R-en-086, R-en-044, R-en-030, R-en-182, R-en-179, R-en-114, R-en-078, R-en-072, R-en-090, R-en-062, R-en-008, R-en-050, R-en-006, R-en-039, R-en-060, R-en-013, R-en-033, R-en-096, R-en-049, R-en-047, R-en-067, R-en-063, R-en-108, R-en-127, R-en-198, R-en-128, R-en-002, R-en-043, R-en-059, R-en-082, R-en-011, R-en-066, R-en-104, R-en-106, R-en-091, R-en-070, R-en-061, R-en-131

## 후보

### E-ko-001

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 밀도, base 1870, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `1870 ± 400 kg/m³` (줄 17, 뒤): - 밀도: 【1870 ± 400 kg/m³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-002

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 각도, base -1.06278, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `−01° 03′ 46.0″` (줄 7, 여러 칸): - 적위: 【−01° 03′ 46.0″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [CoRoT-7b] `01`: …od.) The space mission CoRoT observed the star CoRoT-7, in the stellar field LRa【01】, from October 15, 2007, to March 3, 2008. During this period, 153 periodic tran…
  - [KOI-4878.01] `01`: # KOI-4878.【01】
  - [KOI-4878.01] `01`: KOI-4878.【01】 is an exoplanet candidate that orbits the G-type main-sequence star KOI-4878. I…
  - [KOI-4878.01] `01`: KOI-4878.【01】 has a slightly larger radius than the Earth: 1.02 Earth radii. Its mass has not…
  - [KOI-4878.01] `01`: …tes an orbit around its host star every 449 Earth days. Based on this, KOI-4878.【01】 should be in the habitable zone of the star.

### E-ko-003

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 각도, base 8.51944e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [목동자리 타우 b] (같은 주제의 반대 언어 문서: Tau Boötis b) raw `0.003067 초각` (줄 15, 뒤): - 각거리: 【0.003067 초각】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-004

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 4.73037e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [목동자리 타우 b] (같은 주제의 반대 언어 문서: Tau Boötis b) raw `50광년` (줄 25, 뒤): 목동자리 타우 b 또는 목동자리 타우 Ab는 지구에서 목동자리 방향으로 【50광년】 떨어진 곳에 있는 외계 행성이다. 1996년 제오프리 마시와 폴 버틀러 팀은 목동자리 타우별 근처에 행성이 있음을 공표했다. 1999년 이 행성에는 ‘밀레니엄 행성’이라는 이름이 붙었는데, 이는 목동자리 타우 b가 시각적으로 발견된 최초의 외계 행성이라는 의미였다. …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 4.82497e+17: [Tau Boötis b] raw `51 light-years` (줄 21, 두 언어 쪽): …oötis b, or more precisely Tau Boötis Ab, is an extrasolar planet approximately 【51 light-years】 away, around the primary star of the Tau Boötis system in the constellation of …
  - base 4.62852e+17: [GJ 1214 b] raw `15 pc` (줄 25, 두 언어 쪽): …e star GJ 1214, discovered in December 2009. Its parent star is 48 light-years (【15 pc】) from the Sun, in the constellation Ophiuchus. At the time of its discovery, GJ…
  - base 4.54115e+17: [GJ 1214 b] raw `48 light-years` (줄 25, 두 언어 쪽): …e that orbits the star GJ 1214, discovered in December 2009. Its parent star is 【48 light-years】 (15 pc) from the Sun, in the constellation Ophiuchus. At the time of its discov…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Zeta Leporis] `50`: … young, probably around 231 million years in age, but the margin of error spans 【50】–347 million years old.

### E-ko-005

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 질량, base 3.91179e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `6.55 ± 0.98 지구질량` (줄 16, 뒤): - 질량: 【6.55 ± 0.98 지구질량】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.12082e+25: [CoRoT-7b] raw `6.9 Earth masses` (줄 34, 두 언어 쪽): … paper, by Hatzes et al., employing Fourier analysis, reported a likely mass of 【6.9 Earth masses】 for CoRoT-7b, and found hints for the presence of a third planet in the system,…
  - base 3.61915e+25: [CoRoT-7b] raw `6.06±0.65 M🜨` (줄 15, 두 언어 쪽):   - Mass: 【6.06±0.65 M🜨】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-006

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 4.01138e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `13 파섹` (줄 8, 뒤): - 거리: 40 광년(【13 파섹】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [KOI-4878.01] `13`:   - Mean radius: 1.02+0.04 −0.【13】 R🜨
  - [Ross 128 b] `13`:   - Mass: ≥1.40±0.【13】 M🜨; 1.8+0.56 −0.43 M🜨 (predicted)
  - [TOI-2109 b] `13`: | c (unconfirmed) | — | — | >1.【13】; 1.57, 2.67, 88 or 117 | — | — | — |

### E-ko-007

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 각도, base 4.96381, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `+04° 57′ 49.7″` (줄 7, 여러 칸): - 적위: 【+04° 57′ 49.7″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [GJ 1214 b] `57`:   - Semi-amplitude: 14.38+0.【57】 −0.56 m/s
  - [KOI-4878.01] `04`:   - Mean radius: 1.02+0.【04】 −0.13 R🜨
  - [Zeta Leporis] `57`: - Right ascension: 05ʰ 46ᵐ 【57】.34096ˢ
  - [TOI-2109 b] `57`: | c (unconfirmed) | — | — | >1.13; 1.【57】, 2.67, 88 or 117 | — | — | — |

### E-ko-008

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 온도, base 1621, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [목동자리 타우 b] (같은 주제의 반대 언어 문서: Tau Boötis b) raw `1621 켈빈` (줄 33, 뒤): …이 붙어 있는데 거리는 수성과 태양 간격의 7분의 1밖에 되지 않는다. 한 바퀴 항성을 도는 데 걸리는 시간은 79.5시간에 불과하다. 목동자리 타우는 태양보다 더 뜨겁고 밝기 때문에 타우 b는 알려져 있는 행성들 중 가장 뜨거운 존재에 포함된다. 구체적인 온도는 약 【1621 켈빈】이다. 직접 외관을 통해 증명한 것은 아니지만, 질량으로 미루어 보아 가스 행성으로 보인다.
  - [목동자리 타우 b] (같은 주제의 반대 언어 문서: Tau Boötis b) raw `1621 켈빈` (줄 41, 뒤): 목동자리 타우 b는 뜨거운 열기 때문에 반지름이 목성보다 20퍼센트 더 클 것으로 생각된다. 아직까지 이 행성이 내는 빛이 포착된 적은 없으므로, 행성의 반사율은 0.39보다 낮을 것으로 생각된다. 표면 온도가 【1621 켈빈】 정도일 경우 수다르스키가 추측했던 외계행성의 겉모습에 미루어 보아 작열형 V일 것으로 생각되며 이 경우 반사율은 0.55까지 올라갈 것이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1600: [Tau Boötis b] raw `1600 K` (줄 31, 두 언어 쪽): …t or tidal effects, and a Bond albedo of 0.1, the temperature would be close to 【1600 K】. Although it has not been detected directly, it is certain that the planet is a…
  - base 1699.82: [Tau Boötis b] raw `2,600 °F` (줄 19, 두 언어 쪽):   - Temperature: 1,700 K (1,430 °C; 【2,600 °F】)
  - base 1540: [Tau Boötis b] raw `1540 K` (줄 41, 두 언어 쪽): …n HD 209458 b (formerly predicted 1392K) and possibly even Smertrios (predicted 【1540 K】 from higher albedo 0.3, then actually measured at 2300 K). Tau Boötis b's predi…
  - base 1799.82: [CoRoT-7b] raw `2,780 °F` (줄 16, 두 언어 쪽):   - Temperature: 1,300–1,800 K (1,030–1,530 °C; 1,880–【2,780 °F】)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-009

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 4.6263e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `489 광년` (줄 8, 뒤): - 거리: 【489 광년】(150 파섹)
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `150 파섹` (줄 8, 뒤): - 거리: 489 광년(【150 파섹】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.90623e+18: [CoRoT-7b] raw `159 parsecs` (줄 18, 두 언어 쪽): …t orbiting the star CoRoT-7 in the constellation of Monoceros, 520 light-years (【159 parsecs】) from the Earth. It was first detected photometrically by the French-led CoRoT …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [Kepler-16b] `150`: …e zone, but it is a gas giant with surface temperatures around −100 to −70 °C (−【150】 to −94 °F).
  - [TOI-2109 b] `150`: - Temperature 6,530+160 −【150】 K

### E-ko-010

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 온도, base 1773, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `1773 켈빈` (줄 17, 뒤): - 온도: 1273-【1773 켈빈】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1799.82: [CoRoT-7b] raw `2,780 °F` (줄 16, 두 언어 쪽):   - Temperature: 1,300–1,800 K (1,030–1,530 °C; 1,880–【2,780 °F】)
  - base 1699.82: [Tau Boötis b] raw `2,600 °F` (줄 19, 두 언어 쪽):   - Temperature: 1,700 K (1,430 °C; 【2,600 °F】)
  - base 1600: [Tau Boötis b] raw `1600 K` (줄 31, 두 언어 쪽): …t or tidal effects, and a Bond albedo of 0.1, the temperature would be close to 【1600 K】. Although it has not been detected directly, it is certain that the planet is a…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-011

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 각도, base 100.954, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `06ʰ 43ᵐ 49.0ˢ` (줄 6, 여러 칸): - 적경: 【06ʰ 43ᵐ 49.0ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [CoRoT-7b] `06`:   - Mass: 6.【06】±0.65 M🜨
  - [CoRoT-7b] `06`: CoRoT-7b's mass is somewhat uncertain at 6.【06】±0.65M🜨, while its radius and orbital period are well known from CoRoT photometr…
  - [GJ 1214 b] `06`:   - Albedo: 0.51±0.【06】 (Bond)
  - [Ross 128 b] `06`: … mass. The planet is at least 1.35 M🜨, or 1.35 times the mass of Earth (about 8.【06】×10²⁴ kg). This is slightly more massive than the similar and nearby Proxima Cen…
  - [Ross 128 b] `43`:   - Mass: ≥1.40±0.13 M🜨; 1.8+0.56 −0.【43】 M🜨 (predicted)

### E-ko-012

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 2.13925e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `0.0143 ± 0.0019` (줄 11, 이름 칸): - 평균거리(AU): 【0.0143 ± 0.0019】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-013

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 온도, base 1273, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `1273` (줄 17, 뒤): - 온도: 【1273】-1773 켈빈
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1299.82: [CoRoT-7b] raw `1,880` (줄 16, 두 언어 쪽):   - Temperature: 1,300–1,800 K (1,030–1,530 °C; 【1,880】–2,780 °F)
  - base 1392: [Tau Boötis b] raw `1392K` (줄 41, 두 언어 쪽): …it is (like Mastika) supposed to be hotter than HD 209458 b (formerly predicted 【1392K】) and possibly even Smertrios (predicted 1540 K from higher albedo 0.3, then act…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-014

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 각도, base 258.829, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `17ʰ 15ᵐ 18.94ˢ` (줄 6, 여러 칸): - 적경: 【17ʰ 15ᵐ 18.94ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 253.186: [TOI-2109 b] raw `16ʰ 52ᵐ 44.72027ˢ` (줄 4, 한쪽 언어 쪽): - Right ascension: 【16ʰ 52ᵐ 44.72027ˢ】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Kepler-16b] `15`:   - Discovery date: 【15】 September 2011
  - [CoRoT-7b] `15`: …ssion CoRoT observed the star CoRoT-7, in the stellar field LRa01, from October 【15】, 2007, to March 3, 2008. During this period, 153 periodic transit signals of 1.…
  - [CoRoT-7b] `15`: …as modeled to have convection in the mantle with a small core with no more than 【15】% the mass of the planet, or 0.75 M🜨. The lower mantle above the core-mantle bou…
  - [Tau Boötis b] `17`:   - Mass: 6.24+0.【17】 −0.18 MJ
  - [Tau Boötis b] `15`: …as quickly confirmed by Michel Mayor and Didier Queloz from data collected over 【15】 years. It was later confirmed also by the AFOE Planet Search Team.

### E-ko-015

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 1.01703e+19, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1075광년` (줄 6, 뒤): KOI-4878.01은 지구에서 【1075광년】 떨어진 곳에 위치하고 있으며 지구와 매우 유사한 환경을 가진 행성이 된다. 공전 주기도 449일로 지구와 크게 차이없는 양호한 공전 주기를 가지며 골디락스 존에 위치하여 잠재적으로 사람이 거주 가능한 행성 중에 하나로 꼽히는 슈퍼지구에 속하는 행성이다. 모항성인 KO…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.0596e+19: [KOI-4878.01] raw `1,120 light-years` (줄 16, 두 언어 쪽): …n exoplanet candidate that orbits the G-type main-sequence star KOI-4878. It is 【1,120 light-years】 (344 pc) distant from Earth. The features of the planet are very similar to tha…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-016

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 4.25733e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `450 광년` (줄 30, 뒤): 모항성 COROT-7은 외뿔소자리 방향으로 지구로부터 약 【450 광년】 떨어져 있고, 태양보다 약간 더 차갑고 덜 밝다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Kepler-16b] `450`: …radii of 0.64 R☉ and 0.22 R☉, respectively. They have surface temperatures of 4,【450】 K and 3,311 K and luminosities about 14% and 0.5% that of the Sun, respectively…

### E-ko-017

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 2.54316e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [COROT-7b] (같은 주제의 반대 언어 문서: CoRoT-7b) raw `0.017` (줄 11, 이름 칸): - 평균거리(AU): 【0.017】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.57308e+09: [CoRoT-7b] raw `0.0172 ± 0.00029 AU` (줄 8, 두 언어 쪽):   - Semi-major axis: 【0.0172 ± 0.00029 AU】 (2.573 ± 0.043 million km; 1.599 ± 0.027 million mi)
  - base 2.679e+09: [TOI-2109 b] raw `2,679,000 km` (줄 41, 한쪽 언어 쪽): … just 0.67 days (16 hours), being separated by only 0.01791 astronomical units (【2,679,000 km】) from its host star. The extreme proximity also means TOI-2109 b is strongly ir…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-018

- 분야 exoplanets, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 3.78429e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `40 광년` (줄 8, 뒤): - 거리: 【40 광년】(13 파섹)
  - [글리제 1214 b] (같은 주제의 반대 언어 문서: GJ 1214 b) raw `40 광년` (줄 26, 뒤): 글리제 1214 b는 지구로부터 뱀주인자리 방향으로 약 【40 광년】 떨어진 곳에 있는 글리제 1214 주위를 돌고 있는 외계 행성이다. 글리제 1214 b는 그 질량과 반지름이 태양계 내 가스 행성들보다 작은 것으로 검증된 두 번째 외계 행성이다(첫 번째로 검증된 행성은 CoRoT-7b이다). b의 직경은 지구의 약 2.7배, 질량은…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [CoRoT-7b] `40`: …sit signals of 1.3 h duration with a depth of 3.4 × 10⁻⁴ were registered. After 【40】 days of data acquisition, the Alarm mode pipeline algorithm detected the shallo…
  - [CoRoT-7b] `40`: … Earth. It could belong to a class of planets that are thought to contain up to 【40】% water (in the form of ice and/or vapor) in addition to rock. However, the fact…
  - [Tau Boötis b] `40`: …estimate came from the assumption of tidal lock with the star, which rotates at 【40】 degrees; fixing the planet's mass between 6 and 7 Jupiter masses. In 2007, magn…
  - [Ross 128 b] `40`:   - Mass: ≥1.【40】±0.13 M🜨; 1.8+0.56 −0.43 M🜨 (predicted)

### E-ko-019

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 5e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `5,000 킬로미터` (줄 31, 뒤): …. 통과 현상을 통하여 글리제 436 b의 반지름과 질량을 알 수 있었는데, 두 물리적 수치 모두 해왕성의 그것과 유사했다. 글리제 436 b는 통과 현상을 보이는 외계 행성들 중 가장 질량이 작기도 하다. 이 행성의 지름은 천왕성보다 4,000 킬로미터, 해왕성보다 【5,000 킬로미터】 더 크며 질량은 근소하게 더 크다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-020

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 7e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `700 nm` (줄 44, 뒤): …름은 0.39 AU이다. 프록시마 b가 모성으로부터 받는 복사플럭스는 태양의 65% 수준이다.(화성이 받는 양은 태양의 43% 수준) 프록시마로부터 나오는 복사플럭스의 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~【700 nm】)의 3%에 불과하다.(목성은 3.7%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 2700 럭스이다. 참고로 지구에서 태양이 떠오를 때 수평으로 받는 최대 조도는 대략 400 럭스이다. 프록시마에서는 종종 플레어가 발생한다. 2016년 발…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 7.5e-07: [GJ 1214 b] raw `750` (줄 43, 두 언어 쪽): …hed showing the spectrum to be largely featureless over the wavelength range of 【750】–1000 nm. Because a thick and cloud-free hydrogen-rich atmosphere would have pro…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Tau Boötis b] `700`:   - Temperature: 1,【700】 K (1,430 °C; 2,600 °F)

### E-ko-021

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 966470, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `11.186+0.001 −0.002 일` (줄 8, 뒤): - 공전주기: 【11.186+0.001 −0.002 일】
  - [센타우루스자리 프록시마 b] raw `11.186 일` (줄 44, 뒤): 센타우루스자리 프록시마 b는 어머니 별을 【11.186 일】에 1회 돌고 있으며 별과의 평균 거리는 약 0.05 천문단위(700만 km 또는 500만 마일)로 태양과 지구 사이 거리의 약 20분의 1 정도이다. 참고로 태양에서 가장 가까운 행성 수성의 평균 공전궤도 반지름은 0.39 AU이다. 프록시마 b가 모성으로부터 받는 …
  - [센타우루스자리 프록시마 b] raw `11.2 일` (줄 20, 뒤): 모항성에서 프록시마 b까지의 거리는 0.05 AU(750만 km 또는 460만 마일)로 가깝다. b는 【11.2 일】을 1 주기로 프록시마를 공전하고 있으며 예상되는 b의 질량은 지구의 최소 1.3 배이다. 이 행성은 지구가 받는 태양풍 강도의 약 2000 배에 해당되는 항성풍 압력을 받고 있으나 b의 생명체 거주 가능성 여부는 아직까지 명확하게 정립되지 않았다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-022

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 7.1712e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `83 일` (줄 36, 뒤): …센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 14%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 【83 일】이며 광도는 태양의 0.0015 배이다. 삼중성계의 나머지 두 항성들과 마찬가지로 프록시마는 태양과 비교할 때 중원소가 더 풍부한데 이는 보통 프록시마처럼 질량이 작은 별에서는 흔히 볼 수 없는 특징이다. b의 금속함량([Fe/H])은 0.21로 태양 대기 내 중원소 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 7.6032e+06: [TOI-2109 b] raw `88` (줄 50, 한쪽 언어 쪽): | c (unconfirmed) | — | — | >1.13; 1.57, 2.67, 【88】 or 117 | — | — | — |
  - base 7.776e+06: [Kepler-16b] raw `90 days` (줄 54, 두 언어 쪽): …imary around its star Pp must be less than 1:9 – for example, if a planet takes 【90 days】 to orbit its star, the maximum stable orbit for a moon of that planet is less t…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-023

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 5.6742e+06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `56 기압` (줄 51, 뒤): | 케플러-452b | 0.83 | 표면 온도와 기압은 288 K, 16~【56 기압】으로 추정. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [Tau Boötis b] `56`:   - Time of periastron: MJD 【56】,401.8797±0.0036
  - [GJ 1214 b] `56`:   - Semi-amplitude: 14.38+0.57 −0.【56】 m/s
  - [Ross 128 b] `56`:   - Mass: ≥1.40±0.13 M🜨; 1.8+0.【56】 −0.43 M🜨 (predicted)

### E-ko-024

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1.93536e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `22.4 일` (줄 52, 뒤): …률은 0.35 아래라는 것만 알려져 있을 뿐 확실하게 밝혀지지 않았고 이심률이 0.35라면 수성과 유사한 3:2 자전-공전 공명비에 b가 고정될 가능성이 충분하다. 이 경우 b가 1회 자전하는 데에는 대략 7.5 일이, 프록시마가 b의 지평선에서 떠올라 지기까지는 약 【22.4 일】이 걸릴 것이다. 궤도공명비는 최고 2:1까지도 가능하다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-025

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 1.22072e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `0.0816 AU` (줄 50, 뒤): … 별인 적색왜성이기 때문이다. 즉, 모항성인 프록시마의 온도가 낮기 때문에(표면온도 약 3000 °C) 이렇게 가까움에도 프록시마 b가 생명체 거주 가능 영역에 있을 수 있는 것이다. 태양 질량의 8분의 1 수준인 프록시마 주변의 생물권은 항성으로부터 0.0423 ~ 【0.0816 AU】 범위에 걸쳐 있다. 2016년 10월 프랑스 CNRS 연구재단의 천문학자들은 b에 지구 비슷한 바다와 미약한 대기가 존재할 가능성이 매우 높다고 주장했다. 그러나 b는 지구에서 봤을 때 항성 앞을 지나가지 않기 때문에 이 가설을 검증하기는 어렵다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-026

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base -449280, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `−5.2일` (줄 62, 뒤): …있는 밝은 별 둘처럼 보일 것이다. A와 B의 공전 위치에 따라 맨눈으로 본 두 별은 확실하게 별개의 천체로 보이거나, 또는 가끔씩, 그러나 단순하게, 분리되지 않은 홑별처럼 보일 것이다. 절대등급에 기초하면 센타우루스자리 알파 A와 B의 겉보기등급은 각각 −6.5와 【−5.2일】 것이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Kepler-22b] `5.2`:   - Mean density: <【5.2】 g/cm³

### E-ko-027

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 288, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `288 K` (줄 51, 뒤): | 케플러-452b | 0.83 | 표면 온도와 기압은 【288 K】, 16~56 기압으로 추정. |
  - [지구 유사도 지수] raw `288 K` (줄 52, 뒤): | 케플러-62e | 0.83 | 표면 온도와 기압은 【288 K】, 35 기압으로 추정. |
  - [지구 유사도 지수] raw `288 K` (줄 69, 뒤): | 케플러-62f | 0.69 | 표면 온도와 기압은 【288 K】, 10 기압으로 추정. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 294: [Ross 128 b] raw `294 K` (줄 29, 한쪽 언어 쪽): …ject. With these three albedo parameters, Ross 128 b would have a Teq of either 【294 K】 (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-l…
  - base 279: [Kepler-22b] raw `279±4 K` (줄 19, 한쪽 언어 쪽):   - Temperature: 【279±4 K】 (6 °C; 43 °F, equilibrium)
  - base 300.928: [Ross 128 b] raw `82 °F` (줄 15, 한쪽 언어 쪽):   - Temperature: 213–301 K (−60–28 °C; −76–【82 °F】) (equilibrium)
  - base 269: [Ross 128 b] raw `269 K` (줄 29, 한쪽 언어 쪽): … albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 【269 K】 (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-028

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 1.01325e+06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `10 기압` (줄 38, 뒤): | KOI-4878.01* | 0.98 | 확인되지 않았으나, 표면 온도와 기압이 292 K, 【10 기압】으로 추정됨. |
  - [지구 유사도 지수] raw `10 기압` (줄 69, 뒤): | 케플러-62f | 0.69 | 표면 온도와 기압은 288 K, 【10 기압】으로 추정. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Kepler-16b] `10`: …orbit its star, the maximum stable orbit for a moon of that planet is less than 【10】 days. Simulations suggest that a moon with an orbital period less than about 45…
  - [CoRoT-7b] `10`: …d CoRoT mission and reported in February 2009. Until the announcement of Kepler-【10】b in January 2011, it was the smallest exoplanet to have its diameter measured, …
  - [CoRoT-7b] `10`: …is period, 153 periodic transit signals of 1.3 h duration with a depth of 3.4 × 【10】⁻⁴ were registered. After 40 days of data acquisition, the Alarm mode pipeline a…
  - [CoRoT-7b] `10`: …ght. The planet is weighed at 7.42 Earth masses, yielding an average density of 【10】.4 ± 1.8 g cm⁻³, far higher than the Earth's and similar to that of the second r…
  - [CoRoT-7b] `10`: …r than the Earth's and similar to that of the second rocky planet found, Kepler-【10】b.

### E-ko-029

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1.11732e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 581 c] raw `12.932 일` (줄 13, 뒤): - 공전주기: 【12.932 일】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-030

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 조도, base 2700, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `2700 럭스` (줄 44, 뒤): …% 수준) 프록시마로부터 나오는 복사플럭스의 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~700 nm)의 3%에 불과하다.(목성은 3.7%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 【2700 럭스】이다. 참고로 지구에서 태양이 떠오를 때 수평으로 받는 최대 조도는 대략 400 럭스이다. 프록시마에서는 종종 플레어가 발생한다. 2016년 발생한 관측사상 가장 밝은 플레어는 프록시마의 광도를 약 8 배 높여놓았는데 이는 종전 수준에 비하면 커다란 변화량이었으나 태양…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-031

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 4.05648e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `469.5 ± 9.3 일` (줄 15, 뒤): - 공전주기: 【469.5 ± 9.3 일】(1.29년)
  - [HD 20367 b] raw `470일` (줄 26, 뒤): HD 20367 b는 양자리 방향으로 지구로부터 약 88광년 떨어진 곳에 있는 외계 행성이다. 최소 질량은 목성과 거의 비슷하다. 공전 궤도 평균 거리는 지구~태양 거리의 1.3배 수준이다. 공전 주기는 【470일】(1.3년)이며 궤도는 다소 찌그러져 있다. 거리를 고려할 때 이 행성이 받는 열의 양은 지구가 태양으로부터 받는 것과 비슷하다(다만 근일점일 때는 금성과, 원일점에서는 화성과 비슷한 열을 받는다). 만약 b 주변에 질량이 충분히 큰 위성이 존재한다면 외계 생명체가 살…
  - [HD 20367 b] raw `1.29년` (줄 15, 뒤): - 공전주기: 469.5 ± 9.3 일(【1.29년】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.87936e+07: [KOI-4878.01] raw `449 days` (줄 16, 두 언어 쪽): …he most Earth-like planets found. The orbital period of the exoplanet is around 【449 days】. It is located within the habitable zone of its parent star – a region where wa…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-032

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 175.546, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `11ʰ 42ᵐ 11ˢ` (줄 6, 여러 칸): - 적경: 【11ʰ 42ᵐ 11ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 171.4: [Tau Boötis b] raw `171.4°+5.7° −6.9°` (줄 13, 두 언어 쪽):   - Argument of periastron: 【171.4°+5.7° −6.9°】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [CoRoT-7b] `42`: …h multiple measurements were taken in a given night. The planet is weighed at 7.【42】 Earth masses, yielding an average density of 10.4 ± 1.8 g cm⁻³, far higher than…
  - [KELT-9b] `11`: The thermosphere layer of KELT-9b is expected to heat up to 10,000–【11】,000 K (9,727–10,727 °C; 17,540–19,340 °F), driven by ionization of heavy metals…
  - [KELT-9b] `11`: The thermosphere layer of KELT-9b is expected to heat up to 10,000–【11】,000 K (9,727–10,727 °C; 17,540–19,340 °F), driven by ionization of heavy metals…
  - [Ross 128 b] `11`: …ner edge of the habitable zone of the red dwarf star Ross 128, at a distance of 【11】.007 light-years (3.375 parsecs) from Earth in the constellation of Virgo. The e…
  - [Ross 128 b] `11`: …, making Ross 128 half the temperature and over twice the age. The star is only 【11】.03 light-years away, making it one of the 20 closest stars known.

### E-ko-033

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 5.83432e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `0.39 AU` (줄 44, 뒤): …우루스자리 프록시마 b는 어머니 별을 11.186 일에 1회 돌고 있으며 별과의 평균 거리는 약 0.05 천문단위(700만 km 또는 500만 마일)로 태양과 지구 사이 거리의 약 20분의 1 정도이다. 참고로 태양에서 가장 가까운 행성 수성의 평균 공전궤도 반지름은 【0.39 AU】이다. 프록시마 b가 모성으로부터 받는 복사플럭스는 태양의 65% 수준이다.(화성이 받는 양은 태양의 43% 수준) 프록시마로부터 나오는 복사플럭스의 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~700 nm)의 3…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5.5e+10: [Kepler-16b] raw `55` (줄 52, 두 언어 쪽): The habitable zone of the Kepler-16 system extends from approximately 【55】 to 106 million kilometers away from the binary system. Kepler-16b, with an orbi…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-034

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 284, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `284 K` (줄 41, 뒤): | 글리제 581 g* | 0.92 | 확인되지 않음. 조석 고정되었으며, 표면 온도와 기압은 【284 K】, 18 기압으로 추정. |
  - [지구 유사도 지수] raw `285 K` (줄 39, 뒤): | TRAPPIST-1e | 0.95 | 조석 고정되었으리라 추정됨. 표면 온도와 기압은 【285 K】, 6 기압으로, 현재까지 발견된 외계 행성 중 거주가능성 최상위에 속함. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 279: [Kepler-22b] raw `279±4 K` (줄 19, 한쪽 언어 쪽):   - Temperature: 【279±4 K】 (6 °C; 43 °F, equilibrium)
  - base 294: [Ross 128 b] raw `294 K` (줄 29, 한쪽 언어 쪽): …ject. With these three albedo parameters, Ross 128 b would have a Teq of either 【294 K】 (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-l…
  - base 269: [Ross 128 b] raw `269 K` (줄 29, 한쪽 언어 쪽): … albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 【269 K】 (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the…
  - base 300.928: [Ross 128 b] raw `82 °F` (줄 15, 한쪽 언어 쪽):   - Temperature: 213–301 K (−60–28 °C; −76–【82 °F】) (equilibrium)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-035

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 4.29645e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `0.02872` (줄 11, 이름 칸): - 평균거리(AU): 【0.02872】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-036

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 1.86399e+11, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `1.246 ± 0.075` (줄 11, 이름 칸): - 평균거리(AU): 【1.246 ± 0.075】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.70422e+11: [KOI-4878.01] raw `1.1392+0.0265 −0.0268 AU` (줄 7, 두 언어 쪽):   - Semi-major axis: 【1.1392+0.0265 −0.0268 AU】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-037

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 60.8333, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `+60° 50′` (줄 60, 여러 칸): …타우루스자리 알파 계의 근처에 있기 때문에 프록시마 b에서 바라본 하늘은 지구에서 봤을 때와 거의 비슷하지만 센타우루스자리에서 가장 밝게 빛나던 별은 보이지 않을 것이다. 태양은 센타우루스자리 알파 계의 현재 적경 및 적위의 대척점인 적경 02ʰ 39ᵐ 35ˢ, 적위 【+60° 50′】(2000년 기준)에서 겉보기등급 +0.5의 노란색 별로 보일 것이다. 이 위치는 3.4 등성 카시오페이아자리 엡실론의 근처이며 심장 성운의 바로 앞 근처이다. 이 위치 때문에 외계 관측자 눈에는 카시오페이아자리의 ＼/＼/ 모양이 /＼/＼/ 모양으로 바뀐 것처럼 보일 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Kepler-16b] `60`: …s. Simulations suggest that a moon with an orbital period less than about 45 to 【60】 days will remain safely bound to a massive giant planet or brown dwarf that orb…
  - [Ross 128 b] `60`:   - Temperature: 213–301 K (−【60】–28 °C; −76–82 °F) (equilibrium)
  - [Ross 128 b] `60`: …uld have a Teq of either 294 K (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (−【60】 °C; −76 °F). For an Earth-like albedo of 0.3, the planet would have an equilibr…
  - [Ross 128 b] `60`: …t has a temperature of 3192 K, a luminosity of 0.00362 L☉, and an age of 9.45±0.【60】 billion years. For comparison, the Sun has a temperature of 5772 K and age of 4…
  - [Zeta Leporis] `50`: … young, probably around 231 million years in age, but the margin of error spans 【50】–347 million years old.

### E-ko-038

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 7e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `700만 km` (줄 44, 뒤): 센타우루스자리 프록시마 b는 어머니 별을 11.186 일에 1회 돌고 있으며 별과의 평균 거리는 약 0.05 천문단위(【700만 km】 또는 500만 마일)로 태양과 지구 사이 거리의 약 20분의 1 정도이다. 참고로 태양에서 가장 가까운 행성 수성의 평균 공전궤도 반지름은 0.39 AU이다. 프록시마 b가 모성으로부터 받는 복사플럭스는 태양의 65% 수준이다.(화성이 받는 양은 태양의 43% 수준)…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 6.8815e+09: [CoRoT-7b] raw `0.046 AU` (줄 20, 두 언어 쪽): … times that of Earth and orbits every 3.7 days at a distance of 6.9 million km (【0.046 AU】; 4.3 million mi).
  - base 7.28392e+09: [Tau Boötis b] raw `0.04869+0.00039 −0.00040 AU` (줄 8, 두 언어 쪽):   - Semi-major axis: 【0.04869+0.00039 −0.00040 AU】
  - base 7.42e+09: [Ross 128 b] raw `7.42 million km` (줄 39, 한쪽 언어 쪽): …year (orbital period) lasting about 9.9 days. Its semi-major axis is 0.0496 AU (【7.42 million km】). According to some models of the planet's orbit, its orbit is quite circular, …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Tau Boötis b] `700`:   - Temperature: 1,【700】 K (1,430 °C; 2,600 °F)

### E-ko-039

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1.2623e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `4년` (줄 80, 뒤): … Breakthrough Initiatives가 주도하고 있으며 소형 무인 우주선 스타칩스를 개발 / 발사하는 것을 기획하고 있다. 이 우주선은 광속의 20% 속도로 날 수 있고 알파 계에 도착하는 데에는 약 20년이 걸리며 현장에서 수집한 정보가 지구에 닿는 데에는 【4년】이 조금 넘게 걸릴 것이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Kepler-16b] `4`: …d radii of 0.64 R☉ and 0.22 R☉, respectively. They have surface temperatures of 【4】,450 K and 3,311 K and luminosities about 14% and 0.5% that of the Sun, respecti…
  - [Kepler-16b] `4`: … of 2 billion years for the system is possible. In comparison, the Sun is about 【4】.6 billion years old and has a surface temperature of 5,778 K.
  - [Kepler-16b] `4`: To support an Earth-like atmosphere for about 【4】.6 billion years (the age of the Earth), the moon would have to have a Mars-like…
  - [CoRoT-7b] `4`: …ons of CoRoT-7 also detected a second super-Earth, CoRoT-7c, which has a mass 8.【4】 times that of Earth and orbits every 3.7 days at a distance of 6.9 million km (…
  - [CoRoT-7b] `4`: …t of Earth and orbits every 3.7 days at a distance of 6.9 million km (0.046 AU; 【4】.3 million mi).

### E-ko-040

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 3042, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `3042 켈빈` (줄 36, 뒤): 프록시마 b는 적색왜성 센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 14%이다. 표면 온도는 【3042 켈빈】이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 83 일이며 광도는 태양의 0.0015 배이다. 삼중성계의 나머지 두 항성들과 마찬가지로 프록시마는 태양과 비교할 때 중원소가…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3192: [Ross 128 b] raw `3192 K` (줄 33, 한쪽 언어 쪽): … is 17% the mass and 20% the radius of that of the Sun. It has a temperature of 【3192 K】, a luminosity of 0.00362 L☉, and an age of 9.45±0.60 billion years. For compari…
  - base 3311: [Kepler-16b] raw `3,311 K` (줄 44, 두 언어 쪽): ….64 R☉ and 0.22 R☉, respectively. They have surface temperatures of 4,450 K and 【3,311 K】 and luminosities about 14% and 0.5% that of the Sun, respectively. Based on the…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-041

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 1.92999e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 581 c] raw `20.4광년` (줄 27, 뒤): 천문학적 규모로 볼 때 글리제 581 c는 다른 외계행성들에 비하여 상대적으로 지구에서 가까운데, 천칭자리 방향으로 【20.4광년】 떨어진 거리에 위치한다. 이 정도 거리라면 위도와 경도 방위를 통해 별이 우리 은하 내에 자리잡은 위치를 정확하게 파악할 수 있다. 글리제 581은 글리제 인접 항성 목록에 최초로 수록되었으며, 항성계 중 지구에서 87번째로 가깝다.
  - [글리제 581 c] raw `6.26 파섹` (줄 8, 뒤): - 거리: 【6.26 파섹】 (20.55 광년)
  - [글리제 581 c] raw `20.55 광년` (줄 8, 뒤): - 거리: 6.26 파섹 (【20.55 광년】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-042

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 230, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `230 K` (줄 67, 뒤): | TRAPPIST-1 f | 0.70 | 온도 【230 K】, 지구형 행성일 확률이 약간 존재. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 213: [Ross 128 b] raw `213` (줄 15, 한쪽 언어 쪽):   - Temperature: 【213】–301 K (−60–28 °C; −76–82 °F) (equilibrium)
  - base 254.817: [KOI-4878.01] raw `−1 °F` (줄 30, 두 언어 쪽): … °F). For reference, the equilibrium temperature of the Earth is 255 K (−18 °C; 【−1 °F】).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [CoRoT-7b] `230`: …tenuous atmosphere (with a pressure approaching 1 Pa or 10⁻² mbar at 2,500 K [2,【230】 °C; 4,040 °F]) consisting predominantly of sodium, O2, O and silicon monoxide, …
  - [TOI-2109 b] `230`: …F), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (2,【230】 °C; 4,040 °F). Only 55 Cancri e and KELT-9b have hotter dayside temperatures. T…

### E-ko-043

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 6e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `1000만 분` (줄 72, 뒤): 측정에 사용된 분광기는 라 시야 천문대의 ESO 3.6미터 망원경 내 HARPS와 8 미터 VLT였다. 공전주기와 조합한 어머니 항성의 시선속도 극대점으로부터 외계 행성의 최소질량을 계산했다. 1종 오류가 발생할 가능성은 【1000만 분】의 1로 나왔다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [GJ 1214 b] `1000`: …showing the spectrum to be largely featureless over the wavelength range of 750–【1000】 nm. Because a thick and cloud-free hydrogen-rich atmosphere would have produced…

### E-ko-044

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 26.7064, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `+26° 42′ 23″` (줄 7, 여러 칸): - 적위: 【+26° 42′ 23″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 29: [Tau Boötis b] raw `29°` (줄 33, 두 언어 쪽): … the planet. They calculated that the orbit of the planet has an inclination of 【29°】 and thus the absolute mass of the planet would be about 8.5 times that of Jupit…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [CoRoT-7b] `42`: …h multiple measurements were taken in a given night. The planet is weighed at 7.【42】 Earth masses, yielding an average density of 10.4 ± 1.8 g cm⁻³, far higher than…
  - [CoRoT-7b] `23`: …eriod are well known from CoRoT photometry: it orbits very close to its star (1/【23】rd the distance from the Sun to Mercury) with an orbital period of 20 hours, 29 …
  - [Ross 128 b] `42`: …ar (orbital period) lasting about 9.9 days. Its semi-major axis is 0.0496 AU (7.【42】 million km). According to some models of the planet's orbit, its orbit is quite…
  - [TOI-2109 b] `23`: - Radial velocity (Rv) −22.28±1.【23】 km/s

### E-ko-045

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 7.82222e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `0.002816 초각` (줄 15, 뒤): - 각거리: 【0.002816 초각】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-046

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 조도, base 400, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `400 럭스` (줄 44, 뒤): … 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~700 nm)의 3%에 불과하다.(목성은 3.7%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 2700 럭스이다. 참고로 지구에서 태양이 떠오를 때 수평으로 받는 최대 조도는 대략 【400 럭스】이다. 프록시마에서는 종종 플레어가 발생한다. 2016년 발생한 관측사상 가장 밝은 플레어는 프록시마의 광도를 약 8 배 높여놓았는데 이는 종전 수준에 비하면 커다란 변화량이었으나 태양빛으로 환산하면 지구에 조사되는 양의 약 17%로 그리 강력한 수준은 아니다. 그러나…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [KELT-9b] `400`:   - Temperature: 4,579±120 K (dayside) 2,【400】+400 −300 K (nightside)
  - [KELT-9b] `400`:   - Temperature: 4,579±120 K (dayside) 2,400+【400】 −300 K (nightside)

### E-ko-047

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 8.32544e+17, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `88 ± 3 광년` (줄 8, 뒤): - 거리: 【88 ± 3 광년】(27.1 ± 0.8 파섹)
  - [HD 20367 b] raw `88광년` (줄 26, 뒤): HD 20367 b는 양자리 방향으로 지구로부터 약 【88광년】 떨어진 곳에 있는 외계 행성이다. 최소 질량은 목성과 거의 비슷하다. 공전 궤도 평균 거리는 지구~태양 거리의 1.3배 수준이다. 공전 주기는 470일(1.3년)이며 궤도는 다소 찌그러져 있다. 거리를 고려할 때 이 행성이 받는 열의 양은 지구가 태양으로부터 받는 것…
  - [HD 20367 b] raw `27.1 ± 0.8 파섹` (줄 8, 뒤): - 거리: 88 ± 3 광년(【27.1 ± 0.8 파섹】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [GJ 1214 b] `88`:   - Inclination: 【88】.980°+0.094° −0.085°
  - [Zeta Leporis] `88`: - Absolute magnitude (MV) +1.【88】
  - [TOI-2109 b] `88`: - Age 1.77+0.【88】 −0.68 Gyr
  - [TOI-2109 b] `88`: | c (unconfirmed) | — | — | >1.13; 1.57, 2.67, 【88】 or 117 | — | — | — |

### E-ko-048

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 4e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `4,000 킬로미터` (줄 31, 뒤): …표면 위를 지나가는 것을 발견했다. 통과 현상을 통하여 글리제 436 b의 반지름과 질량을 알 수 있었는데, 두 물리적 수치 모두 해왕성의 그것과 유사했다. 글리제 436 b는 통과 현상을 보이는 외계 행성들 중 가장 질량이 작기도 하다. 이 행성의 지름은 천왕성보다 【4,000 킬로미터】, 해왕성보다 5,000 킬로미터 더 크며 질량은 근소하게 더 크다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-049

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 3.54638e+06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `35 기압` (줄 52, 뒤): | 케플러-62e | 0.83 | 표면 온도와 기압은 288 K, 【35 기압】으로 추정. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Tau Boötis b] `35`: …ulted in measured carbon abundance similar to that of Jupiter, in the form of 0.【35】% carbon monoxide volume admixture to hydrogen-helium atmosphere. The upper limi…
  - [GJ 1214 b] `35`:   - Mass: 8.41+0.36 −0.【35】 M🜨
  - [GJ 1214 b] `35`: …ellar spectral lines due to the Doppler effect, yielding a mass of 8.41+0.36 −0.【35】 M🜨. Given the planet's mass and radius, its density can be calculated. Through …
  - [Ross 128 b] `35`: …d is considered one of the best candidates for habitability. The planet is only 【35】% more massive than Earth, receives only 38% more starlight, and is expected to …
  - [Ross 128 b] `35`: …parameter for Ross 128 b is its minimum possible mass. The planet is at least 1.【35】 M🜨, or 1.35 times the mass of Earth (about 8.06×10²⁴ kg). This is slightly more…

### E-ko-050

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 712.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `섭씨 439도` (줄 35, 앞): b가 어머니 항성 주위를 한 바퀴 도는 데에는 불과 39.5시간밖에 걸리지 않는다. 이 행성의 표면 온도는 대략 【섭씨 439도】이다. 이심률이 큰 궤도 때문에 받는 기조력으로 인해, 이 행성의 온도는 산술적인 계산치보다 더 높다. b의 주요 조성물은 높은 압력 하에서 존재하는, 다양한 형태의 뜨거운 ‘얼음’일 것으로 생각되며, 막대한 행성 자체의 내부 압력 덕분에 높은 온도에도 불구하고 고체 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 733: [Kepler-22b] raw `733 K` (줄 57, 한쪽 언어 쪽): … magnitude to the one on Venus, it would have an average surface temperature of 【733 K】 (460 °C).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-051

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 4.01138e+16, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `1.3 파섹` (줄 18, 뒤): …리 프록시마 b(프록시마 b 또는 센타우루스자리 알파 Cb)는 태양에서 가장 가까우면서 센타우루스자리 알파 삼중성계의 일원인 적색왜성 센타우루스자리 프록시마의 생명체 거주가능 영역 내를 돌고 있는 외계 행성이다. b는 센타우루스자리 방향으로 지구로부터 약 4.2 광년(【1.3 파섹】, 40조 km, 25조 마일, 26만 5천 AU) 떨어져 있어서 지구에서 가장 가까운 외계 행성이기도 하다.
  - [센타우루스자리 프록시마 b] raw `25조 마일` (줄 18, 뒤): …또는 센타우루스자리 알파 Cb)는 태양에서 가장 가까우면서 센타우루스자리 알파 삼중성계의 일원인 적색왜성 센타우루스자리 프록시마의 생명체 거주가능 영역 내를 돌고 있는 외계 행성이다. b는 센타우루스자리 방향으로 지구로부터 약 4.2 광년(1.3 파섹, 40조 km, 【25조 마일】, 26만 5천 AU) 떨어져 있어서 지구에서 가장 가까운 외계 행성이기도 하다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.94512e+16: [Zeta Leporis] raw `4.17 light-years` (줄 62, 한쪽 언어 쪽): … calculations from 2010 suggest that this star passed as close as 1.28 parsecs (【4.17 light-years】) from the Sun about 861,000 years ago. García-Sánchez 2001 suggested that the s…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [CoRoT-7b] `1.3`: …15, 2007, to March 3, 2008. During this period, 153 periodic transit signals of 【1.3】 h duration with a depth of 3.4 × 10⁻⁴ were registered. After 40 days of data ac…
  - [CoRoT-7b] `1.3`: …al., weighed the planet at about 4.8 Earth masses, giving it a density of 5.6 ± 【1.3】 g cm⁻³, similar to Earth's. The value was obtained using a pre-whitening proced…
  - [GJ 1214 b] `25`: …er, proportions of the total mass consistent with the mass and radius are about 【25】% rock and 75% water, covered by a thick envelope of gases such as hydrogen and …
  - [KELT-9b] `25`:   - Inclination: 86.79°±0.【25】°
  - [Ross 128 b] `25`: …ters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 269 K (−4 °C; 【25】 °F), or 213 K (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the planet wou…

### E-ko-052

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 2.46088e+11, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `1.645` (줄 13, 이름 칸): - 원일점(AU): 【1.645】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-053

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 1.26709e+11, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `0.847` (줄 12, 이름 칸): - 근일점(AU): 【0.847】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.21473e+11: [Kepler-22b] raw `0.812+0.011 −0.013 AU` (줄 8, 한쪽 언어 쪽):   - Semi-major axis: 【0.812+0.011 −0.013 AU】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-054

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 273, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `273 K` (줄 58, 뒤): | 케플러-440b | 0.75 | 궤도가 타원형, 표면 온도 【273 K】 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 269: [Ross 128 b] raw `269 K` (줄 29, 한쪽 언어 쪽): … albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 【269 K】 (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the…
  - base 279: [Kepler-22b] raw `279±4 K` (줄 19, 한쪽 언어 쪽):   - Temperature: 【279±4 K】 (6 °C; 43 °F, equilibrium)
  - base 254.817: [KOI-4878.01] raw `−1 °F` (줄 30, 두 언어 쪽): … °F). For reference, the equilibrium temperature of the Earth is 255 K (−18 °C; 【−1 °F】).
  - base 294: [Ross 128 b] raw `294 K` (줄 29, 한쪽 언어 쪽): …ject. With these three albedo parameters, Ross 128 b would have a Teq of either 【294 K】 (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-l…
  - base 300.928: [Ross 128 b] raw `82 °F` (줄 15, 한쪽 언어 쪽):   - Temperature: 213–301 K (−60–28 °C; −76–【82 °F】) (equilibrium)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-055

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 6.32799e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `0.0423` (줄 50, 뒤): … 스펙트럼상 M형 별인 적색왜성이기 때문이다. 즉, 모항성인 프록시마의 온도가 낮기 때문에(표면온도 약 3000 °C) 이렇게 가까움에도 프록시마 b가 생명체 거주 가능 영역에 있을 수 있는 것이다. 태양 질량의 8분의 1 수준인 프록시마 주변의 생물권은 항성으로부터 【0.0423】 ~ 0.0816 AU 범위에 걸쳐 있다. 2016년 10월 프랑스 CNRS 연구재단의 천문학자들은 b에 지구 비슷한 바다와 미약한 대기가 존재할 가능성이 매우 높다고 주장했다. 그러나 b는 지구에서 봤을 때 항성 앞을 지나가지 않기 때문에 이 가설을 검증하기는 어렵다…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.8815e+09: [CoRoT-7b] raw `0.046 AU` (줄 20, 두 언어 쪽): … times that of Earth and orbits every 3.7 days at a distance of 6.9 million km (【0.046 AU】; 4.3 million mi).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-056

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 2.53312e+06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `25 기압` (줄 42, 뒤): | 루이텐 b | 0.91 | 조석 고정됨. 표면 온도와 기압은 294 K, 【25 기압】으로 추정. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [GJ 1214 b] `25`: …er, proportions of the total mass consistent with the mass and radius are about 【25】% rock and 75% water, covered by a thick envelope of gases such as hydrogen and …
  - [KELT-9b] `25`:   - Inclination: 86.79°±0.【25】°
  - [Ross 128 b] `25`: …ters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 269 K (−4 °C; 【25】 °F), or 213 K (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the planet wou…
  - [Kepler-22b] `25`: …e from Earth to the Sun but the luminosity (light output) of Kepler-22 is about 【25】% less than that of the Sun. This combination of a shorter average distance from…
  - [TOI-2109 b] `25`: …years. The rotation period of this star is 14% longer than Earth's day, about 1/【25】th that of the Sun.

### E-ko-057

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 8.04672e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `500만 마일` (줄 44, 뒤): 센타우루스자리 프록시마 b는 어머니 별을 11.186 일에 1회 돌고 있으며 별과의 평균 거리는 약 0.05 천문단위(700만 km 또는 【500만 마일】)로 태양과 지구 사이 거리의 약 20분의 1 정도이다. 참고로 태양에서 가장 가까운 행성 수성의 평균 공전궤도 반지름은 0.39 AU이다. 프록시마 b가 모성으로부터 받는 복사플럭스는 태양의 65% 수준이다.(화성이 받는 양은 태양의 43% 수준) 프록시마로부터 나오…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 7.42e+09: [Ross 128 b] raw `7.42 million km` (줄 39, 한쪽 언어 쪽): …year (orbital period) lasting about 9.9 days. Its semi-major axis is 0.0496 AU (【7.42 million km】). According to some models of the planet's orbit, its orbit is quite circular, …
  - base 7.28392e+09: [Tau Boötis b] raw `0.04869+0.00039 −0.00040 AU` (줄 8, 두 언어 쪽):   - Semi-major axis: 【0.04869+0.00039 −0.00040 AU】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [CoRoT-7b] `500`: …oduced a tenuous atmosphere (with a pressure approaching 1 Pa or 10⁻² mbar at 2,【500】 K [2,230 °C; 4,040 °F]) consisting predominantly of sodium, O2, O and silicon m…
  - [TOI-2109 b] `500`: …; 6,070 °F), while the nightside is around 1,000 degrees cooler, at less than 2,【500】 K (2,230 °C; 4,040 °F). Only 55 Cancri e and KELT-9b have hotter dayside temper…

### E-ko-058

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 238.5, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `238.5 K` (줄 54, 뒤): | 케플러-283c | 0.79 | 표면 온도 【238.5 K】. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 254.817: [KOI-4878.01] raw `−1 °F` (줄 30, 두 언어 쪽): … °F). For reference, the equilibrium temperature of the Earth is 255 K (−18 °C; 【−1 °F】).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-059

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 233, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `233 K` (줄 50, 뒤): | 케플러-442b | 0.84 | 거주가능 구역의 정중앙에 위치. 온도 【233 K】. |
  - [센타우루스자리 프록시마 b] raw `234 K` (줄 32, 뒤): …구보다 낮거나 실제 질량이 최소질량보다 크다면 반지름은 지구보다 클 것이다. 수많은 슈퍼지구 크기 행성들처럼 센타우루스자리 프록시마 b는 해왕성 비슷하게 표면에는 두꺼운 수소층이, 내부에는 얼음층이 존재할 수도 있는데 이럴 가능성은 10% 이상이다. b의 균형 온도는 【234 K】 (−39 °C; −38 °F)이다.
  - [센타우루스자리 프록시마 b] raw `−39 °C` (줄 32, 뒤): … 실제 질량이 최소질량보다 크다면 반지름은 지구보다 클 것이다. 수많은 슈퍼지구 크기 행성들처럼 센타우루스자리 프록시마 b는 해왕성 비슷하게 표면에는 두꺼운 수소층이, 내부에는 얼음층이 존재할 수도 있는데 이럴 가능성은 10% 이상이다. b의 균형 온도는 234 K (【−39 °C】; −38 °F)이다.
  - [센타우루스자리 프록시마 b] raw `−38 °F` (줄 32, 뒤): …최소질량보다 크다면 반지름은 지구보다 클 것이다. 수많은 슈퍼지구 크기 행성들처럼 센타우루스자리 프록시마 b는 해왕성 비슷하게 표면에는 두꺼운 수소층이, 내부에는 얼음층이 존재할 수도 있는데 이럴 가능성은 10% 이상이다. b의 균형 온도는 234 K (−39 °C; 【−38 °F】)이다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 254.817: [KOI-4878.01] raw `−1 °F` (줄 30, 두 언어 쪽): … °F). For reference, the equilibrium temperature of the Earth is 255 K (−18 °C; 【−1 °F】).
  - base 213: [Ross 128 b] raw `213` (줄 15, 한쪽 언어 쪽):   - Temperature: 【213】–301 K (−60–28 °C; −76–82 °F) (equilibrium)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [GJ 1214 b] `38`:   - Semi-amplitude: 14.【38】+0.57 −0.56 m/s
  - [Ross 128 b] `38`: …for habitability. The planet is only 35% more massive than Earth, receives only 【38】% more starlight, and is expected to be a temperature suitable for liquid water …
  - [Ross 128 b] `38`: … zone. It appears to reside within the inner edge, as it receives approximately 【38】% more sunlight than Earth. The habitable zone is defined as the region around a…
  - [TOI-2109 b] `38`: - Luminosity 4.71+0.【38】 −0.27 L☉

### E-ko-060

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 49.4169, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `03ʰ 17ᵐ 40.0461ˢ` (줄 6, 여러 칸): - 적경: 【03ʰ 17ᵐ 40.0461ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 44.5: [Tau Boötis b] raw `44.5±1.5 degrees` (줄 37, 두 언어 쪽): …he planet's orbit and hence the planet's mass. One team found an inclination of 【44.5±1.5 degrees】 and a mass of 5.95±0.28 MJ. The other team found an inclination of 47−6⁺⁷ and a…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Tau Boötis b] `17`:   - Mass: 6.24+0.【17】 −0.18 MJ
  - [GJ 1214 b] `17`:   - Orbital period (sidereal): 1.580404531+18 −【17】 d
  - [GJ 1214 b] `17`:   - Mean density: 2.20+0.【17】 −0.16 g/cm³
  - [KELT-9b] `03`:   - Mean radius: 1.82±0.【03】 RJ
  - [KELT-9b] `17`: …times more massive than the sun. The surface temperature is 10,170 K (9,897 °C; 【17】,846 °F), unusually hot for a star with a transiting planet. Prior to the discov…

### E-ko-061

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 4.10249e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `1.3년` (줄 26, 뒤): HD 20367 b는 양자리 방향으로 지구로부터 약 88광년 떨어진 곳에 있는 외계 행성이다. 최소 질량은 목성과 거의 비슷하다. 공전 궤도 평균 거리는 지구~태양 거리의 1.3배 수준이다. 공전 주기는 470일(【1.3년】)이며 궤도는 다소 찌그러져 있다. 거리를 고려할 때 이 행성이 받는 열의 양은 지구가 태양으로부터 받는 것과 비슷하다(다만 근일점일 때는 금성과, 원일점에서는 화성과 비슷한 열을 받는다). 만약 b 주변에 질량이 충분히 큰 위성이 존재한다면 외계 생명체가 살 수 있는…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.87936e+07: [KOI-4878.01] raw `449 days` (줄 16, 두 언어 쪽): …he most Earth-like planets found. The orbital period of the exoplanet is around 【449 days】. It is located within the habitable zone of its parent star – a region where wa…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [CoRoT-7b] `1.3`: …15, 2007, to March 3, 2008. During this period, 153 periodic transit signals of 【1.3】 h duration with a depth of 3.4 × 10⁻⁴ were registered. After 40 days of data ac…
  - [CoRoT-7b] `1.3`: …al., weighed the planet at about 4.8 Earth masses, giving it a density of 5.6 ± 【1.3】 g cm⁻³, similar to Earth's. The value was obtained using a pre-whitening proced…

### E-ko-062

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 3.73995e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 581 c] raw `0.25 천문단위` (줄 33, 뒤): 우드리 팀은 2007년 4월 27일 자신들의 관측 사실을 논문으로 발표했으며 같은 해 7월 《천문학과 천체물리학》 저널에 게재했다. 논문을 통해 우드리 팀은 또다른 행성 글리제 581 d의 존재를 함께 발표했는데, d의 최소 질량은 지구의 7.7배에 행성으로부터 【0.25 천문단위】 떨어져 있었다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [KELT-9b] `0.25`:   - Inclination: 86.79°±【0.25】°

### E-ko-063

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 31.127, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `+31° 07′ 37.372″` (줄 7, 여러 칸): - 적위: 【+31° 07′ 37.372″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 29: [Tau Boötis b] raw `29°` (줄 33, 두 언어 쪽): … the planet. They calculated that the orbit of the planet has an inclination of 【29°】 and thus the absolute mass of the planet would be about 8.5 times that of Jupit…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [Kepler-16b] `07`: …arth), the moon would have to have a Mars-like density and at least a mass of 0.【07】 M🜨. One way to decrease loss from sputtering is for the moon to have a strong m…
  - [GJ 1214 b] `31`:   - Escape velocity: 19.【31】+0.53 −0.54 km/s
  - [Zeta Leporis] `07`: - Proper motion (μ) RA: −14.54 mas/yr Dec.: −1.【07】 mas/yr
  - [Zeta Leporis] `07`: - Distance 70.5 ± 0.2 ly (21.61 ± 0.【07】 pc)

### E-ko-064

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 229.858, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 581 c] raw `15ʰ 19ᵐ 26ˢ` (줄 6, 여러 칸): - 적경: 【15ʰ 19ᵐ 26ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 253.186: [TOI-2109 b] raw `16ʰ 52ᵐ 44.72027ˢ` (줄 4, 한쪽 언어 쪽): - Right ascension: 【16ʰ 52ᵐ 44.72027ˢ】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Kepler-16b] `15`:   - Discovery date: 【15】 September 2011
  - [CoRoT-7b] `15`: …ssion CoRoT observed the star CoRoT-7, in the stellar field LRa01, from October 【15】, 2007, to March 3, 2008. During this period, 153 periodic transit signals of 1.…
  - [CoRoT-7b] `15`: …as modeled to have convection in the mantle with a small core with no more than 【15】% the mass of the planet, or 0.75 M🜨. The lower mantle above the core-mantle bou…
  - [Tau Boötis b] `15`: …as quickly confirmed by Michel Mayor and Didier Queloz from data collected over 【15】 years. It was later confirmed also by the AFOE Planet Search Team.
  - [GJ 1214 b] `15`: …e star GJ 1214, discovered in December 2009. Its parent star is 48 light-years (【15】 pc) from the Sun, in the constellation Ophiuchus. At the time of its discovery,…

### E-ko-065

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 1.09206e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 581 c] raw `0.073` (줄 11, 이름 칸): - 평균거리(AU): 【0.073】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-066

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 3273.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `3000 °C` (줄 50, 뒤): …면에 존재할 수 있는 영역) 안을 돌고 있다. b가 모항성과 불과 750만 km밖에 떨어져 있지 않은데도 생명체 거주 가능 영역 안에 있을 수 있는 까닭은 프록시마가 스펙트럼상 M형 별인 적색왜성이기 때문이다. 즉, 모항성인 프록시마의 온도가 낮기 때문에(표면온도 약 【3000 °C】) 이렇게 가까움에도 프록시마 b가 생명체 거주 가능 영역에 있을 수 있는 것이다. 태양 질량의 8분의 1 수준인 프록시마 주변의 생물권은 항성으로부터 0.0423 ~ 0.0816 AU 범위에 걸쳐 있다. 2016년 10월 프랑스 CNRS 연구재단의 천문학자들은 b에 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3311: [Kepler-16b] raw `3,311 K` (줄 44, 두 언어 쪽): ….64 R☉ and 0.22 R☉, respectively. They have surface temperatures of 4,450 K and 【3,311 K】 and luminosities about 14% and 0.5% that of the Sun, respectively. Based on the…
  - base 3192: [Ross 128 b] raw `3192 K` (줄 33, 한쪽 언어 쪽): … is 17% the mass and 20% the radius of that of the Sun. It has a temperature of 【3192 K】, a luminosity of 0.00362 L☉, and an age of 9.45±0.60 billion years. For compari…
  - base 3627.59: [TOI-2109 b] raw `6,070 °F` (줄 41, 한쪽 언어 쪽): …9 b is strongly irradiated. The dayside temperature measures 3,630 K (3,360 °C; 【6,070 °F】), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (2,2…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-067

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 4e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `400` (줄 44, 뒤): …도 반지름은 0.39 AU이다. 프록시마 b가 모성으로부터 받는 복사플럭스는 태양의 65% 수준이다.(화성이 받는 양은 태양의 43% 수준) 프록시마로부터 나오는 복사플럭스의 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(【400】~700 nm)의 3%에 불과하다.(목성은 3.7%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 2700 럭스이다. 참고로 지구에서 태양이 떠오를 때 수평으로 받는 최대 조도는 대략 400 럭스이다. 프록시마에서는 종종 플레어가 발생한다. …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [KELT-9b] `400`:   - Temperature: 4,579±120 K (dayside) 2,【400】+400 −300 K (nightside)
  - [KELT-9b] `400`:   - Temperature: 4,579±120 K (dayside) 2,400+【400】 −300 K (nightside)

### E-ko-068

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 3.13135e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 436 b] raw `0.438 RJ` (줄 18, 뒤): - 반지름: 【0.438 RJ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-069

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 질량, base 2.20971e+27, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [HD 20367 b] raw `370 ± 70 지구질량` (줄 17, 뒤): - 질량: 1.17 ± 0.23 목성질량(>【370 ± 70 지구질량】)
  - [HD 20367 b] raw `1.17 ± 0.23 목성질량` (줄 17, 뒤): - 질량: 【1.17 ± 0.23 목성질량】(>370 ± 70 지구질량)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-070

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 276, 표 안 예, 시험 대상 밖 예
- 언급:
  - [지구 유사도 지수] raw `276 K` (줄 44, 뒤): | 케플러-438b | 0.88 | 온도는 【276 K】이며, 조석 고정되었으리라 추정됨. 거주가능성은 확실하지 않음. |
  - [지구 유사도 지수] raw `277 K` (줄 49, 뒤): | 글리제 667 Cc | 0.85 | 조석 고정되었으리라 추정됨. 온도는 【277 K】로 추정. |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 279: [Kepler-22b] raw `279±4 K` (줄 19, 한쪽 언어 쪽):   - Temperature: 【279±4 K】 (6 °C; 43 °F, equilibrium)
  - base 269: [Ross 128 b] raw `269 K` (줄 29, 한쪽 언어 쪽): … albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 【269 K】 (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the…
  - base 294: [Ross 128 b] raw `294 K` (줄 29, 한쪽 언어 쪽): …ject. With these three albedo parameters, Ross 128 b would have a Teq of either 【294 K】 (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (−60 °C; −76 °F). For an Earth-l…
  - base 254.817: [KOI-4878.01] raw `−1 °F` (줄 30, 두 언어 쪽): … °F). For reference, the equilibrium temperature of the Earth is 255 K (−18 °C; 【−1 °F】).
  - base 300.928: [Ross 128 b] raw `82 °F` (줄 15, 한쪽 언어 쪽):   - Temperature: 213–301 K (−60–28 °C; −76–【82 °F】) (equilibrium)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-071

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 3.23917e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [글리제 581 c] raw `0.011661 초각` (줄 15, 뒤): - 각거리: 【0.011661 초각】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-ko-072

- 분야 exoplanets, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 648000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [센타우루스자리 프록시마 b] raw `7.5 일` (줄 52, 뒤): …얼어붙는 추위가 지속될 것이다. 그러나 프록시마 b의 공전 이심률은 0.35 아래라는 것만 알려져 있을 뿐 확실하게 밝혀지지 않았고 이심률이 0.35라면 수성과 유사한 3:2 자전-공전 공명비에 b가 고정될 가능성이 충분하다. 이 경우 b가 1회 자전하는 데에는 대략 【7.5 일】이, 프록시마가 b의 지평선에서 떠올라 지기까지는 약 22.4 일이 걸릴 것이다. 궤도공명비는 최고 2:1까지도 가능하다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Tau Boötis b] `7.5`: …eventh that of Mercury's from the Sun. One orbital revolution takes only 3 days 【7.5】 hours to complete. Because τ Boo is hotter and larger than the Sun and the plan…

### E-en-001

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 2499.82, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `4,040 °F` (줄 64, 뒤): …been depleted, silicate rock vaporization may have produced a tenuous atmosphere (with a pressure approaching 1 Pa or 10⁻² mbar at 2,500 K [2,230 °C; 【4,040 °F】]) consisting predominantly of sodium, O2, O and silicon monoxide, as well as smaller amounts of potassium and other metals. Magnesium (Mg), aluminium…
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `2,500 K` (줄 64, 뒤): …ace volatiles have been depleted, silicate rock vaporization may have produced a tenuous atmosphere (with a pressure approaching 1 Pa or 10⁻² mbar at 【2,500 K】 [2,230 °C; 4,040 °F]) consisting predominantly of sodium, O2, O and silicon monoxide, as well as smaller amounts of potassium and other metals. Magne…
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `2,230 °C` (줄 64, 뒤): …iles have been depleted, silicate rock vaporization may have produced a tenuous atmosphere (with a pressure approaching 1 Pa or 10⁻² mbar at 2,500 K [【2,230 °C】; 4,040 °F]) consisting predominantly of sodium, O2, O and silicon monoxide, as well as smaller amounts of potassium and other metals. Magnesium (Mg),…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-002

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.0596e+19, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1,120 light-years` (줄 16, 뒤): KOI-4878.01 is an exoplanet candidate that orbits the G-type main-sequence star KOI-4878. It is 【1,120 light-years】 (344 pc) distant from Earth. The features of the planet are very similar to that of Earth, and if it is confirmed, it would be one of the most Earth-…
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `344 pc` (줄 16, 뒤): KOI-4878.01 is an exoplanet candidate that orbits the G-type main-sequence star KOI-4878. It is 1,120 light-years (【344 pc】) distant from Earth. The features of the planet are very similar to that of Earth, and if it is confirmed, it would be one of the most Earth-like pla…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.01703e+19: [KOI-4878.01] raw `1075광년` (줄 6, 두 언어 쪽): KOI-4878.01은 지구에서 【1075광년】 떨어진 곳에 위치하고 있으며 지구와 매우 유사한 환경을 가진 행성이 된다. 공전 주기도 449일로 지구와 크게 차이없는 양호한 공전 주기를 가…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-003

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 속도, base 19310, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `19.31+0.53 −0.54 km/s` (줄 21, 뒤):   - Escape velocity: 【19.31+0.53 −0.54 km/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-004

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 7.5e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `750` (줄 43, 뒤): …etary atmosphere can be inferred. In December 2010, a study was published showing the spectrum to be largely featureless over the wavelength range of 【750】–1000 nm. Because a thick and cloud-free hydrogen-rich atmosphere would have produced detectable spectral features, such an atmosphere appears to be r…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 7e-07: [센타우루스자리 프록시마 b] raw `700 nm` (줄 44, 한쪽 언어 쪽): … 수준) 프록시마로부터 나오는 복사플럭스의 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~【700 nm】)의 3%에 불과하다.(목성은 3.7%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 2700 럭스이다. 참고로 지구…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [센타우루스자리 프록시마 b] `750`: 모항성에서 프록시마 b까지의 거리는 0.05 AU(【750】만 km 또는 460만 마일)로 가깝다. b는 11.2 일을 1 주기로 프록시마를 공전하고 있으며 예상되는 b의 질량은 지구의 최소 1.3 배이…
  - [센타우루스자리 프록시마 b] `750`: … 거주가능 영역(행성의 조건 및 대기의 성질이 적절할 경우 액체 물이 행성 표면에 존재할 수 있는 영역) 안을 돌고 있다. b가 모항성과 불과 【750】만 km밖에 떨어져 있지 않은데도 생명체 거주 가능 영역 안에 있을 수 있는 까닭은 프록시마가 스펙트럼상 M형 별인 적색왜성이기 때문이다. 즉,…

### E-en-005

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 1392, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `1392K` (줄 41, 뒤): …albedo constraint was tightened to less than 0.12 by 2021. At 1600 K, it is (like Mastika) supposed to be hotter than HD 209458 b (formerly predicted 【1392K】) and possibly even Smertrios (predicted 1540 K from higher albedo 0.3, then actually measured at 2300 K). Tau Boötis b's predicted Sudarsky class is …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1273: [COROT-7b] raw `1273` (줄 17, 두 언어 쪽): - 온도: 【1273】-1773 켈빈
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-006

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 7.776e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-16b] (같은 주제의 반대 언어 문서: 케플러-16b) raw `90 days` (줄 54, 뒤): …een the moon's orbital period Ps around its primary and that of the primary around its star Pp must be less than 1:9 – for example, if a planet takes 【90 days】 to orbit its star, the maximum stable orbit for a moon of that planet is less than 10 days. Simulations suggest that a moon with an orbital period le…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 7.1712e+06: [센타우루스자리 프록시마 b] raw `83 일` (줄 36, 한쪽 언어 쪽): …이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 【83 일】이며 광도는 태양의 0.0015 배이다. 삼중성계의 나머지 두 항성들과 마찬가지로 프록시마는 태양과 비교할 때 중원소가 더 풍부한데 이는 보통 …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [케플러-16b] `90`: - 궤도경사각: 【90】.0322 ± 0.0023
  - [센타우루스자리 프록시마 b] `90`: …약 b의 궤도면이 관측자의 시선 방향과 거의 일치한다면 질량값은 지구의 1.27+0.19 −0.17 배일 것이다. 통계적으로 b의 질량은 대략 【90】%의 확률로 지구의 3배 미만일 것이다.
  - [센타우루스자리 프록시마 b] `90`: …진다면 질량을 계산할 수 있을 것이다. 만약 궤도가 보다 기울어져 있으면 실제 질량은 더 커질 것이며 질량값이 지구의 3 배 미만일 확률은 약 【90】%이다. b의 정확한 반지름은 알려지지 않았다. 만약 b가 암석으로 조성되어 있고 밀도를 지구와 같다고 가정하면 반지름은 최소 지구의 1.1 배…

### E-en-007

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 5.91248e+24, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `0.99 Earth masses` (줄 30, 뒤): …n the Earth: 1.02 Earth radii. Its mass has not been measured, but it is estimated to be somewhere between 0.4 - 3.0 Earth masses; most likely around 【0.99 Earth masses】. The planet has an equilibrium temperature of 257 K (−16 °C; 3 °F). For reference, the equilibrium temperature of the Earth is 255 K (−18 °C; −1 °F).
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-008

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 5.184e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-16b] (같은 주제의 반대 언어 문서: 케플러-16b) raw `60 days` (줄 54, 뒤): …the maximum stable orbit for a moon of that planet is less than 10 days. Simulations suggest that a moon with an orbital period less than about 45 to 【60 days】 will remain safely bound to a massive giant planet or brown dwarf that orbits 1 AU from a Sun-like star.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [센타우루스자리 프록시마 b] `60`: …가장 밝게 빛나던 별은 보이지 않을 것이다. 태양은 센타우루스자리 알파 계의 현재 적경 및 적위의 대척점인 적경 02ʰ 39ᵐ 35ˢ, 적위 +【60】° 50′(2000년 기준)에서 겉보기등급 +0.5의 노란색 별로 보일 것이다. 이 위치는 3.4 등성 카시오페이아자리 엡실론의 근처이며 심장 …
  - [지구 유사도 지수] `60`: | 케플러-296f | 0.【60】 |  |
  - [지구 유사도 지수] `60`: | 글리제 667 Ce* | 0.【60】 | 존재에 대한 논란이 있음. |
  - [지구 유사도 지수] `60`: | HD 69830 d | 0.【60】 | 행성의 밀도나 대기권 정보가 부족. |

### E-en-009

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 각도, base 44.5, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `44.5±1.5 degrees` (줄 37, 뒤): …s of carbon monoxide. This enabled calculation of the inclination of the planet's orbit and hence the planet's mass. One team found an inclination of 【44.5±1.5 degrees】 and a mass of 5.95±0.28 MJ. The other team found an inclination of 47−6⁺⁷ and a mass of 5.6±0.7 MJ.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 49.4169: [HD 20367 b] raw `03ʰ 17ᵐ 40.0461ˢ` (줄 6, 한쪽 언어 쪽): - 적경: 【03ʰ 17ᵐ 40.0461ˢ】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-010

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 속도, base 106210, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `106.21+1.76 −1.71 km/s` (줄 14, 뒤):   - Semi-amplitude: 【106.21+1.76 −1.71 km/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-011

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 5.02262e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `8.41+0.36 −0.35 M🜨` (줄 18, 뒤):   - Mass: 【8.41+0.36 −0.35 M🜨】
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `8.41+0.36 −0.35 M🜨` (줄 37, 뒤): …ervations of the parent star's radial velocity, measured through small shifts in stellar spectral lines due to the Doppler effect, yielding a mass of 【8.41+0.36 −0.35 M🜨】. Given the planet's mass and radius, its density can be calculated. Through a comparison with theoretical models, the density in turn provides limite…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-012

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 2.00637e+30, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1.009±0.129 M☉` (줄 20, 뒤): …tar, more precisely of spectral class G4V. It has an apparent magnitude of 12.37 and is located in the constellation of Draco. The star has a mass of 【1.009±0.129 M☉】, a radius of 1.131±0.059 R☉ and an effective temperature of 5674±125 K. Its age is estimated at 6.1±2.5 billion years, older than the Solar System.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-013

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 319680, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `3.7 days` (줄 20, 뒤): …. The radial velocity observations of CoRoT-7 also detected a second super-Earth, CoRoT-7c, which has a mass 8.4 times that of Earth and orbits every 【3.7 days】 at a distance of 6.9 million km (0.046 AU; 4.3 million mi).
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `3.7-day` (줄 32, 뒤): …re-whitening procedure and harmonic decomposition. It was also inferred that there was a second non-transiting planet in the system, CoRoT-7c, with a 【3.7-day】 orbital period.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [센타우루스자리 프록시마 b] `3.7`: … 대부분은 적외선 스펙트럼에 있다. 가시광선 스펙트럼에서 b가 받는 에너지는 지구 조도 PAR(400~700 nm)의 3%에 불과하다.(목성은 【3.7】%, 토성은 1.1%임) 조용한 프록시마로부터 프록시마 b가 받는 조도는 약 2700 럭스이다. 참고로 지구에서 태양이 떠오를 때 수평으로 받는…

### E-en-014

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 4.12082e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `6.9 Earth masses` (줄 34, 뒤): A second paper, by Hatzes et al., employing Fourier analysis, reported a likely mass of 【6.9 Earth masses】 for CoRoT-7b, and found hints for the presence of a third planet in the system, CoRoT-7d, with mass similar to Neptune's and a 9-day orbital period.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.91179e+25: [글리제 1214 b] raw `6.55 ± 0.98 지구질량` (줄 16, 두 언어 쪽): - 질량: 【6.55 ± 0.98 지구질량】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-015

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 각도, base 89.95, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `89.95 °` (줄 10, 뒤):   - Inclination: 【89.95 °】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-016

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 1699.82, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `2,600 °F` (줄 19, 뒤):   - Temperature: 1,700 K (1,430 °C; 【2,600 °F】)
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `1,700 K` (줄 19, 뒤):   - Temperature: 【1,700 K】 (1,430 °C; 2,600 °F)
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `1,430 °C` (줄 19, 뒤):   - Temperature: 1,700 K (【1,430 °C】; 2,600 °F)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1773: [COROT-7b] raw `1773 켈빈` (줄 17, 두 언어 쪽): - 온도: 1273-【1773 켈빈】
  - base 1621: [목동자리 타우 b] raw `1621 켈빈` (줄 33, 두 언어 쪽): …불과하다. 목동자리 타우는 태양보다 더 뜨겁고 밝기 때문에 타우 b는 알려져 있는 행성들 중 가장 뜨거운 존재에 포함된다. 구체적인 온도는 약 【1621 켈빈】이다. 직접 외관을 통해 증명한 것은 아니지만, 질량으로 미루어 보아 가스 행성으로 보인다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-017

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 3.40415e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `5.7 Earth masses` (줄 38, 뒤): Boisse et al., employing simultaneous fitting of stellar activity and planetary signals in the radial velocity data, calculate for CoRoT-7b a mass of 【5.7 Earth masses】, though with a very large uncertainty.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-018

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 1299.82, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1,880` (줄 16, 뒤):   - Temperature: 1,300–1,800 K (1,030–1,530 °C; 【1,880】–2,780 °F)
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1,300` (줄 16, 뒤):   - Temperature: 【1,300】–1,800 K (1,030–1,530 °C; 1,880–2,780 °F)
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1,030` (줄 16, 뒤):   - Temperature: 1,300–1,800 K (【1,030】–1,530 °C; 1,880–2,780 °F)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1273: [COROT-7b] raw `1273` (줄 17, 두 언어 쪽): - 온도: 【1273】-1773 켈빈
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-019

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 3.888e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-16b] (같은 주제의 반대 언어 문서: 케플러-16b) raw `45` (줄 54, 뒤): …star, the maximum stable orbit for a moon of that planet is less than 10 days. Simulations suggest that a moon with an orbital period less than about 【45】 to 60 days will remain safely bound to a massive giant planet or brown dwarf that orbits 1 AU from a Sun-like star.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3.6288e+06: [글리제 581 c] raw `6주` (줄 31, 한쪽 언어 쪽): …행성을 발견했다. 발견에는 칠레 소재 라 실라 천문대의 유럽 남방 천문대 3.6미터 망원경에 설치된 HARPS 기구가 사용되었다. 첫 발견 후 【6주】 동안 검토 작업에는 MOST 우주 망원경이 사용되었다. 검토 기간 중 행성이 항성 앞을 지나가는 사건은 발생하지 않았기 때문에 행성 크기를 직…
  - base 3.5424e+06: [케플러-16b] raw `41일` (줄 48, 두 언어 쪽): 케플러-16b는 쌍성주위 궤도를 돌고 있다. 케플러-16은 K형 및 M형 주계열성으로 이루어진 쌍성계로, 두 항성은 서로를 【41일】에 걸쳐 공전한다. 항성의 질량은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [HD 20367 b] `45`: | 화성 근일점 플럭스 | 718.545 | 52.【45】% |

### E-en-020

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 900000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `900 tonnes` (줄 43, 뒤): …ry system and the calculated hydrodynamic escape (loss of gasses that tends to deplete an atmosphere of higher molecular-weight constituents) rate of 【900 tonnes】 per second, scientists conclude that there has been a significant atmospheric loss during the lifetime of the planet and any current atmosphere canno…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-021

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 각도, base 171.4, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `171.4°+5.7° −6.9°` (줄 13, 뒤):   - Argument of periastron: 【171.4°+5.7° −6.9°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 175.546: [글리제 436 b] raw `11ʰ 42ᵐ 11ˢ` (줄 6, 한쪽 언어 쪽): - 적경: 【11ʰ 42ᵐ 11ˢ】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-022

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 4.54115e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `48 light-years` (줄 25, 뒤): …amed Enaiposha since 2023) is an exoplanet with a very high temperature that orbits the star GJ 1214, discovered in December 2009. Its parent star is 【48 light-years】 (15 pc) from the Sun, in the constellation Ophiuchus. At the time of its discovery, GJ 1214 b was the most likely known candidate for being an ocean …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.62852e+17: [목동자리 타우 b] raw `15 파섹` (줄 8, 두 언어 쪽): - 거리: 【15 파섹】
  - base 4.73037e+17: [목동자리 타우 b] raw `50광년` (줄 25, 두 언어 쪽): 목동자리 타우 b 또는 목동자리 타우 Ab는 지구에서 목동자리 방향으로 【50광년】 떨어진 곳에 있는 외계 행성이다. 1996년 제오프리 마시와 폴 버틀러 팀은 목동자리 타우별 근처에 행성이 있음을 공표했다. 1999년 이 행…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [센타우루스자리 프록시마 b] `48`: …왜성 센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 14%이다. 표면 온도는 3042 켈빈이며 나이는 【48】억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 83 일이며 광도…
  - [지구 유사도 지수] `48`: | 글리제 581b | 0.【48】 | 거주가능 구역의 안쪽 끝에 위치. |

### E-en-023

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 가속도, base 10.65, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `10.65+0.71 −0.67 m/s²` (줄 20, 뒤):   - Surface gravity: 【10.65+0.71 −0.67 m/s²】 (1.09 g)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-024

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 진동수, base 3e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `30 MHz` (줄 45, 뒤): In 2020, a radio emission in the 14-【30 MHz】 band was detected from the Tau Boötis system, likely associated with cyclotron radiation from the poles of Tau Boötis b. This could be a signature of…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [센타우루스자리 프록시마 b] `30`: - 반지름: 1.07+0.38 −0.31RE, 1.【30】+1.20 −0.62RE
  - [지구 유사도 지수] `30`: | 케플러-11b | 0.【30】 |  |
  - [HD 20367 b] `30`: | 금성 평균 플럭스 | 2,620.693 | 191.【30】% |

### E-en-025

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 각도, base 41.6, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `41.6°+1.0° −0.9°` (줄 11, 뒤):   - Inclination: 【41.6°+1.0° −0.9°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 39.8958: [센타우루스자리 프록시마 b] raw `02ʰ 39ᵐ 35ˢ` (줄 60, 한쪽 언어 쪽): … 비슷하지만 센타우루스자리에서 가장 밝게 빛나던 별은 보이지 않을 것이다. 태양은 센타우루스자리 알파 계의 현재 적경 및 적위의 대척점인 적경 【02ʰ 39ᵐ 35ˢ】, 적위 +60° 50′(2000년 기준)에서 겉보기등급 +0.5의 노란색 별로 보일 것이다. 이 위치는 3.4 등성 카시오페이아자리 엡실론의 …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-026

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 777600, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `9-day` (줄 34, 뒤): …ss of 6.9 Earth masses for CoRoT-7b, and found hints for the presence of a third planet in the system, CoRoT-7d, with mass similar to Neptune's and a 【9-day】 orbital period.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [케플러-16b] `9`: - 발견일: 2011년 【9】월 15일
  - [케플러-16b] `9`: … 바깥 행성 중 가장 측정이 잘 된 행성이라고 믿는다"고 밝혔다. 대표적으로 케플러-16b의 반지름 오차는 0.3% 정도인데, 이는 2011년 【9】월 당시 기준 발견된 외계행성 중 가장 정확한 수치였다.
  - [COROT-7b] `9`: - 형태: G【9】 V
  - [목동자리 타우 b] `9`: - 질량: 3.【9】 MJ
  - [글리제 581 c] `9`: …계열성 주위를 도는 외계 천체 중에서는 가장 작은 존재였다. 그러나 2009년 4월 21일 같은 별을 도는 글리제 581 e(지구질량의 약 1.【9】배)가 발견됨으로써 가장 질량이 작은 외계 행성의 자리를 넘겨 주었다. 581c는 지금까지 발견된 외계행성들 중 액체 물이 존재 가능한 궤도를 …

### E-en-027

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 4.43137e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `7.42 Earth masses` (줄 40, 뒤): … stellar activity through analysis only of radial velocity data for which multiple measurements were taken in a given night. The planet is weighed at 【7.42 Earth masses】, yielding an average density of 10.4 ± 1.8 g cm⁻³, far higher than the Earth's and similar to that of the second rocky planet found, Kepler-10b.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-028

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 7.86837e+08, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1.131±0.059 R☉` (줄 20, 뒤): …ral class G4V. It has an apparent magnitude of 12.37 and is located in the constellation of Draco. The star has a mass of 1.009±0.129 M☉, a radius of 【1.131±0.059 R☉】 and an effective temperature of 5674±125 K. Its age is estimated at 6.1±2.5 billion years, older than the Solar System.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-029

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 3.61915e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `6.06±0.65 M🜨` (줄 15, 뒤):   - Mass: 【6.06±0.65 M🜨】
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `6.06±0.65M🜨` (줄 50, 뒤): CoRoT-7b's mass is somewhat uncertain at 【6.06±0.65M🜨】, while its radius and orbital period are well known from CoRoT photometry: it orbits very close to its star (1/23rd the distance from the Sun to Merc…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.91179e+25: [글리제 1214 b] raw `6.55 ± 0.98 지구질량` (줄 16, 두 언어 쪽): - 질량: 【6.55 ± 0.98 지구질량】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-030

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.00774e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1.58 Earth radii` (줄 50, 뒤): …y close to its star (1/23rd the distance from the Sun to Mercury) with an orbital period of 20 hours, 29 minutes, and 9.7 seconds and has a radius of 【1.58 Earth radii】. CoRoT-7b had the shortest orbit of any planet known at the time of its discovery.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-031

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 1540, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `1540 K` (줄 41, 뒤): ….12 by 2021. At 1600 K, it is (like Mastika) supposed to be hotter than HD 209458 b (formerly predicted 1392K) and possibly even Smertrios (predicted 【1540 K】 from higher albedo 0.3, then actually measured at 2300 K). Tau Boötis b's predicted Sudarsky class is V; which is supposed to yield a highly reflecti…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1621: [목동자리 타우 b] raw `1621 켈빈` (줄 33, 두 언어 쪽): …불과하다. 목동자리 타우는 태양보다 더 뜨겁고 밝기 때문에 타우 b는 알려져 있는 행성들 중 가장 뜨거운 존재에 포함된다. 구체적인 온도는 약 【1621 켈빈】이다. 직접 외관을 통해 증명한 것은 아니지만, 질량으로 미루어 보아 가스 행성으로 보인다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-032

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 각도, base 88.98, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `88.980°+0.094° −0.085°` (줄 13, 뒤):   - Inclination: 【88.980°+0.094° −0.085°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-033

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 437, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `437±19 K` (줄 23, 뒤):   - Temperature: 553±9 K (280 °C; 536 °F, dayside) 【437±19 K】 (164 °C; 327 °F, nightside)
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `327 °F` (줄 23, 뒤):   - Temperature: 553±9 K (280 °C; 536 °F, dayside) 437±19 K (164 °C; 【327 °F】, nightside)
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `164 °C` (줄 23, 뒤):   - Temperature: 553±9 K (280 °C; 536 °F, dayside) 437±19 K (【164 °C】; 327 °F, nightside)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-034

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 4.90623e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `159 parsecs` (줄 18, 뒤): CoRoT-7b (previously named CoRoT-Exo-7b) is an exoplanet orbiting the star CoRoT-7 in the constellation of Monoceros, 520 light-years (【159 parsecs】) from the Earth. It was first detected photometrically by the French-led CoRoT mission and reported in February 2009. Until the announcement of Keple…
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `520 light-years` (줄 18, 뒤): CoRoT-7b (previously named CoRoT-Exo-7b) is an exoplanet orbiting the star CoRoT-7 in the constellation of Monoceros, 【520 light-years】 (159 parsecs) from the Earth. It was first detected photometrically by the French-led CoRoT mission and reported in February 2009. Until the announce…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.6263e+18: [COROT-7b] raw `489 광년` (줄 8, 두 언어 쪽): - 거리: 【489 광년】(150 파섹)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-035

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 1799.82, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `2,780 °F` (줄 16, 뒤):   - Temperature: 1,300–1,800 K (1,030–1,530 °C; 1,880–【2,780 °F】)
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1,800 K` (줄 16, 뒤):   - Temperature: 1,300–【1,800 K】 (1,030–1,530 °C; 1,880–2,780 °F)
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1,530 °C` (줄 16, 뒤):   - Temperature: 1,300–1,800 K (1,030–【1,530 °C】; 1,880–2,780 °F)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1773: [COROT-7b] raw `1773 켈빈` (줄 17, 두 언어 쪽): - 온도: 1273-【1773 켈빈】
  - base 1621: [목동자리 타우 b] raw `1621 켈빈` (줄 33, 두 언어 쪽): …불과하다. 목동자리 타우는 태양보다 더 뜨겁고 밝기 때문에 타우 b는 알려져 있는 행성들 중 가장 뜨거운 존재에 포함된다. 구체적인 온도는 약 【1621 켈빈】이다. 직접 외관을 통해 증명한 것은 아니지만, 질량으로 미루어 보아 가스 행성으로 보인다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-036

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 진동수, base 1.4e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `14` (줄 45, 뒤): In 2020, a radio emission in the 【14】-30 MHz band was detected from the Tau Boötis system, likely associated with cyclotron radiation from the poles of Tau Boötis b. This could be a signa…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [케플러-16b] `14`: - 표면중력: 【14】.52 (± 0.7) m/s²
  - [케플러-16b] `14`: …은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및 3311 K, 광도는 태양의 【14】% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
  - [센타우루스자리 프록시마 b] `14`: 프록시마 b는 적색왜성 센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 【14】%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우…

### E-en-037

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.79166e+25, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `3.0 Earth masses` (줄 30, 뒤): …8.01 has a slightly larger radius than the Earth: 1.02 Earth radii. Its mass has not been measured, but it is estimated to be somewhere between 0.4 - 【3.0 Earth masses】; most likely around 0.99 Earth masses. The planet has an equilibrium temperature of 257 K (−16 °C; 3 °F). For reference, the equilibrium temperature …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-038

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 4.82497e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `51 light-years` (줄 21, 뒤): Tau Boötis b, or more precisely Tau Boötis Ab, is an extrasolar planet approximately 【51 light-years】 away, around the primary star of the Tau Boötis system in the constellation of Boötes. It was one of the first exoplanets to be discovered. It is a h…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.73037e+17: [목동자리 타우 b] raw `50광년` (줄 25, 두 언어 쪽): 목동자리 타우 b 또는 목동자리 타우 Ab는 지구에서 목동자리 방향으로 【50광년】 떨어진 곳에 있는 외계 행성이다. 1996년 제오프리 마시와 폴 버틀러 팀은 목동자리 타우별 근처에 행성이 있음을 공표했다. 1999년 이 행…
  - base 4.62852e+17: [목동자리 타우 b] raw `15 파섹` (줄 8, 두 언어 쪽): - 거리: 【15 파섹】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-039

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.70422e+11, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1.1392+0.0265 −0.0268 AU` (줄 7, 뒤):   - Semi-major axis: 【1.1392+0.0265 −0.0268 AU】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.86399e+11: [HD 20367 b] raw `1.246 ± 0.075` (줄 11, 한쪽 언어 쪽): - 평균거리(AU): 【1.246 ± 0.075】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-040

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 2300, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `2300 K` (줄 41, 뒤): …be hotter than HD 209458 b (formerly predicted 1392K) and possibly even Smertrios (predicted 1540 K from higher albedo 0.3, then actually measured at 【2300 K】). Tau Boötis b's predicted Sudarsky class is V; which is supposed to yield a highly reflective albedo of 0.55.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-041

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.13888e+28, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `6` (줄 35, 뒤): A better estimate came from the assumption of tidal lock with the star, which rotates at 40 degrees; fixing the planet's mass between 【6】 and 7 Jupiter masses. In 2007, magnetic field detection confirmed this estimate.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [COROT-7b] `6`: …는 외계 행성이다. 2009년 프랑스 주도의 COROT 계획 중 발견되었다. 이 행성은 반지름이 지구의 1.7배에 불과하고, 질량은 지구의 5.【6】 ~ 11배 사이일 것으로 보인다. 질량을 고려하면 가스 행성이 아니라 암석 행성일 것이다. 항성에서 매우 가까운 거리에 있기 때문에 1회 공전…
  - [글리제 1214 b] `6`: - 질량: 【6】.55 ± 0.98 지구질량
  - [글리제 1214 b] `6`: …작은 것으로 검증된 두 번째 외계 행성이다(첫 번째로 검증된 행성은 CoRoT-7b이다). b의 직경은 지구의 약 2.7배, 질량은 지구의 약 【6】.5배 즈음으로 밝혀졌고, 모항성이 태양보다 훨씬 어두운 적색 왜성이어서 행성 대기를 현재 기술로 분석 가능하다는 점에서 더욱 돋보이는 존재이다…
  - [글리제 581 c] `6`: - 거리: 【6】.26 파섹 (20.55 광년)
  - [글리제 581 c] `6`: …일 스위스 제네바 천문대 소속 스테판 우드리가 이끄는 연구팀이 이 행성을 발견했다. 발견에는 칠레 소재 라 실라 천문대의 유럽 남방 천문대 3.【6】미터 망원경에 설치된 HARPS 기구가 사용되었다. 첫 발견 후 6주 동안 검토 작업에는 MOST 우주 망원경이 사용되었다. 검토 기간 중 행성…

### E-en-042

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 2.57308e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `0.0172 ± 0.00029 AU` (줄 8, 뒤):   - Semi-major axis: 【0.0172 ± 0.00029 AU】 (2.573 ± 0.043 million km; 1.599 ± 0.027 million mi)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.54316e+09: [COROT-7b] raw `0.017` (줄 11, 두 언어 쪽): - 평균거리(AU): 【0.017】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-043

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 2.86666e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `4.8 Earth masses` (줄 32, 뒤): The discovery paper, by Queloz et al., weighed the planet at about 【4.8 Earth masses】, giving it a density of 5.6 ± 1.3 g cm⁻³, similar to Earth's. The value was obtained using a pre-whitening procedure and harmonic decomposition. It w…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-044

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 질량, base 0.00109, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `1.09 g` (줄 20, 뒤):   - Surface gravity: 10.65+0.71 −0.67 m/s² (【1.09 g】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-045

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 9.74574e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `1.528±0.065 R🜨` (줄 14, 뒤):   - Mean radius: 【1.528±0.065 R🜨】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-046

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 속도, base 14.38, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `14.38+0.57 −0.56 m/s` (줄 14, 뒤):   - Semi-amplitude: 【14.38+0.57 −0.56 m/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-047

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.74313e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `2.733+0.033 −0.031 R🜨` (줄 17, 뒤):   - Mean radius: 【2.733+0.033 −0.031 R🜨】
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `2.733+0.033 −0.031 R🜨` (줄 37, 뒤): …1214 b can be inferred from the amount of dimming seen when the planet crosses in front of its parent star as viewed from Earth, yielding a radius of 【2.733+0.033 −0.031 R🜨】. The mass of the planet can be inferred from sensitive observations of the parent star's radial velocity, measured through small shifts in stellar sp…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-048

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 5674, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `5674±125 K` (줄 20, 뒤): …12.37 and is located in the constellation of Draco. The star has a mass of 1.009±0.129 M☉, a radius of 1.131±0.059 R☉ and an effective temperature of 【5674±125 K】. Its age is estimated at 6.1±2.5 billion years, older than the Solar System.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5778: [센타우루스자리 프록시마 b] raw `5778 켈빈` (줄 36, 한쪽 언어 쪽): … 12%이며 반지름은 14%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 【5778 켈빈】이다. 센타우루스자리 프록시마의 1 자전주기는 83 일이며 광도는 태양의 0.0015 배이다. 삼중성계의 나머지 두 항성들과 마찬가지로 프록시마…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-049

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 6.50566e+06, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1.02+0.04 −0.13 R🜨` (줄 13, 뒤):   - Mean radius: 【1.02+0.04 −0.13 R🜨】
  - [KOI-4878.01] (같은 주제의 반대 언어 문서: KOI-4878.01) raw `1.02 Earth radii` (줄 30, 뒤): KOI-4878.01 has a slightly larger radius than the Earth: 【1.02 Earth radii】. Its mass has not been measured, but it is estimated to be somewhere between 0.4 - 3.0 Earth masses; most likely around 0.99 Earth masses. The planet…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-050

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 9.7, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `9.7 seconds` (줄 50, 뒤): … CoRoT photometry: it orbits very close to its star (1/23rd the distance from the Sun to Mercury) with an orbital period of 20 hours, 29 minutes, and 【9.7 seconds】 and has a radius of 1.58 Earth radii. CoRoT-7b had the shortest orbit of any planet known at the time of its discovery.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-051

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 시간, base 3.456e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [CoRoT-7b] (같은 주제의 반대 언어 문서: COROT-7b) raw `40 days` (줄 24, 뒤): …ober 15, 2007, to March 3, 2008. During this period, 153 periodic transit signals of 1.3 h duration with a depth of 3.4 × 10⁻⁴ were registered. After 【40 days】 of data acquisition, the Alarm mode pipeline algorithm detected the shallow signal of CoRoT-7b, starting the follow-up observations from the ground t…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3.5424e+06: [케플러-16b] raw `41일` (줄 48, 두 언어 쪽): 케플러-16b는 쌍성주위 궤도를 돌고 있다. 케플러-16은 K형 및 M형 주계열성으로 이루어진 쌍성계로, 두 항성은 서로를 【41일】에 걸쳐 공전한다. 항성의 질량은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및…
  - base 3.6288e+06: [글리제 581 c] raw `6주` (줄 31, 한쪽 언어 쪽): …행성을 발견했다. 발견에는 칠레 소재 라 실라 천문대의 유럽 남방 천문대 3.6미터 망원경에 설치된 HARPS 기구가 사용되었다. 첫 발견 후 【6주】 동안 검토 작업에는 MOST 우주 망원경이 사용되었다. 검토 기간 중 행성이 항성 앞을 지나가는 사건은 발생하지 않았기 때문에 행성 크기를 직…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [글리제 1214 b] `40`: - 거리: 【40】 광년(13 파섹)
  - [글리제 1214 b] `40`: 글리제 1214 b는 지구로부터 뱀주인자리 방향으로 약 【40】 광년 떨어진 곳에 있는 글리제 1214 주위를 돌고 있는 외계 행성이다. 글리제 1214 b는 그 질량과 반지름이 태양계 내 가스 행성들보다 …
  - [센타우루스자리 프록시마 b] `40`: …루스자리 프록시마의 생명체 거주가능 영역 내를 돌고 있는 외계 행성이다. b는 센타우루스자리 방향으로 지구로부터 약 4.2 광년(1.3 파섹, 【40】조 km, 25조 마일, 26만 5천 AU) 떨어져 있어서 지구에서 가장 가까운 외계 행성이기도 하다.
  - [HD 20367 b] `40`: - 적경: 03ʰ 17ᵐ 【40】.0461ˢ

### E-en-052

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 온도, base 1600, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `1600 K` (줄 31, 뒤): …be hot. Assuming the planet is perfectly grey with no Greenhouse effect or tidal effects, and a Bond albedo of 0.1, the temperature would be close to 【1600 K】. Although it has not been detected directly, it is certain that the planet is a gas giant. As Tau Boötis b is more massive than most known "hot Jupit…
  - [Tau Boötis b] (같은 주제의 반대 언어 문서: 목동자리 타우 b) raw `1600 K` (줄 41, 뒤): …e no reflected light has been detected, the planet's albedo must be less than 0.37. The albedo constraint was tightened to less than 0.12 by 2021. At 【1600 K】, it is (like Mastika) supposed to be hotter than HD 209458 b (formerly predicted 1392K) and possibly even Smertrios (predicted 1540 K from higher alb…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1621: [목동자리 타우 b] raw `1621 켈빈` (줄 33, 두 언어 쪽): …불과하다. 목동자리 타우는 태양보다 더 뜨겁고 밝기 때문에 타우 b는 알려져 있는 행성들 중 가장 뜨거운 존재에 포함된다. 구체적인 온도는 약 【1621 켈빈】이다. 직접 외관을 통해 증명한 것은 아니지만, 질량으로 미루어 보아 가스 행성으로 보인다.
  - base 1773: [COROT-7b] raw `1773 켈빈` (줄 17, 두 언어 쪽): - 온도: 1273-【1773 켈빈】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-053

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 밀도, base 2200, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [GJ 1214 b] (같은 주제의 반대 언어 문서: 글리제 1214 b) raw `2.20+0.17 −0.16 g/cm³` (줄 19, 뒤):   - Mean density: 【2.20+0.17 −0.16 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-054

- 분야 exoplanets, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.5259e+11, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-16b] (같은 주제의 반대 언어 문서: 케플러-16b) raw `1.02 AU` (줄 52, 뒤): …ler-16b to capture it as its moon. Furthermore, the researchers considered the possibility of a habitable planet orbiting at a distance of about 0.95–【1.02 AU】, which could retain the thermal energy required to keep water in a liquid state via a strong greenhouse effect.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.49598e+11: [센타우루스자리 프록시마 b] raw `1 천문단위` (줄 66, 한쪽 언어 쪽): 센타우루스자리 프록시마처럼 작은 별들의 항성탄생 원반 모형에 따르면 별이 태어날 당시 항성으로부터 【1 천문단위】 이내에 있는 물질을 다 합쳐도 지구 질량 하나를 넘지 않는다 한다. 이 모형에 따르면 센타우루스자리 프록시마 b는 현재의 위치에서 태어난 것 …
  - base 1.4e+11: [케플러-16b] raw `1억 4000만 킬로미터` (줄 56, 두 언어 쪽): …주가능 영역 중심에 위치하던 지구형 행성이 섭동으로 바깥으로 이동하는 과정에서 케플러-16b에 위성으로 포획되었을 가능성이 있다. 이에 더해, 【1억 4000만 킬로미터】 거리에서 공전하는 행성이 존재할 가능성도 제기되었으며, 이 경우 이산화 탄소나 메테인 등 온실 기체가 충분할 경우 표면에 물이 액체 상태로 존…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-055

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 7.6032e+06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `88` (줄 50, 머리글): | c (unconfirmed) | — | — | >1.13; 1.57, 2.67, 【88】 or 117 | — | — | — |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 7.1712e+06: [센타우루스자리 프록시마 b] raw `83 일` (줄 36, 한쪽 언어 쪽): …이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 【83 일】이며 광도는 태양의 0.0015 배이다. 삼중성계의 나머지 두 항성들과 마찬가지로 프록시마는 태양과 비교할 때 중원소가 더 풍부한데 이는 보통 …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [글리제 1214 b] `88`: - 궤도경사각: 【88】.62(+0.36, -0.28)
  - [지구 유사도 지수] `88`: | 케플러-438b | 0.【88】 | 온도는 276 K이며, 조석 고정되었으리라 추정됨. 거주가능성은 확실하지 않음. |
  - [HD 20367 b] `88`: - 거리: 【88】 ± 3 광년(27.1 ± 0.8 파섹)
  - [HD 20367 b] `88`: HD 20367 b는 양자리 방향으로 지구로부터 약 【88】광년 떨어진 곳에 있는 외계 행성이다. 최소 질량은 목성과 거의 비슷하다. 공전 궤도 평균 거리는 지구~태양 거리의 1.3배 수준이다. 공전 주…

### E-en-056

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 5518, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `5,518 K` (줄 37, 뒤): The host star, Kepler-22, is a G-type star that is 3% less massive than the Sun and 2% smaller in volume. It has a surface temperature of 【5,518 K】 (5,245 °C; 9,473 °F) compared with the Sun, which has a surface temperature of 5,778 K (5,505 °C; 9,941 °F). The star is about 4 billion years old. I…
  - [Kepler-22b] raw `5,245 °C` (줄 37, 뒤): The host star, Kepler-22, is a G-type star that is 3% less massive than the Sun and 2% smaller in volume. It has a surface temperature of 5,518 K (【5,245 °C】; 9,473 °F) compared with the Sun, which has a surface temperature of 5,778 K (5,505 °C; 9,941 °F). The star is about 4 billion years old. In comparis…
  - [Kepler-22b] raw `9,473 °F` (줄 37, 뒤): …t star, Kepler-22, is a G-type star that is 3% less massive than the Sun and 2% smaller in volume. It has a surface temperature of 5,518 K (5,245 °C; 【9,473 °F】) compared with the Sun, which has a surface temperature of 5,778 K (5,505 °C; 9,941 °F). The star is about 4 billion years old. In comparison, the Su…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5778: [센타우루스자리 프록시마 b] raw `5778 켈빈` (줄 36, 한쪽 언어 쪽): … 12%이며 반지름은 14%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 【5778 켈빈】이다. 센타우루스자리 프록시마의 1 자전주기는 83 일이며 광도는 태양의 0.0015 배이다. 삼중성계의 나머지 두 항성들과 마찬가지로 프록시마…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-057

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 10169.8, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `17,846 °F` (줄 27, 뒤): … star, KELT-9, also designated HD 195689, is 2.3 times larger and 2.4 times more massive than the sun. The surface temperature is 10,170 K (9,897 °C; 【17,846 °F】), unusually hot for a star with a transiting planet. Prior to the discovery of KELT-9b, only six A-type stars were known to have planets, of which th…
  - [KELT-9b] raw `10,170 K` (줄 27, 뒤): The host star, KELT-9, also designated HD 195689, is 2.3 times larger and 2.4 times more massive than the sun. The surface temperature is 【10,170 K】 (9,897 °C; 17,846 °F), unusually hot for a star with a transiting planet. Prior to the discovery of KELT-9b, only six A-type stars were known to have…
  - [KELT-9b] raw `9,897 °C` (줄 27, 뒤): The host star, KELT-9, also designated HD 195689, is 2.3 times larger and 2.4 times more massive than the sun. The surface temperature is 10,170 K (【9,897 °C】; 17,846 °F), unusually hot for a star with a transiting planet. Prior to the discovery of KELT-9b, only six A-type stars were known to have planets, …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-058

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 2499.82, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `4,040 °F` (줄 41, 뒤): …d. The dayside temperature measures 3,630 K (3,360 °C; 6,070 °F), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (2,230 °C; 【4,040 °F】). Only 55 Cancri e and KELT-9b have hotter dayside temperatures. This planet is around 30% larger than Jupiter and five times more massive. Its orbit…
  - [TOI-2109 b] raw `2,500 K` (줄 41, 뒤): … strongly irradiated. The dayside temperature measures 3,630 K (3,360 °C; 6,070 °F), while the nightside is around 1,000 degrees cooler, at less than 【2,500 K】 (2,230 °C; 4,040 °F). Only 55 Cancri e and KELT-9b have hotter dayside temperatures. This planet is around 30% larger than Jupiter and five times mor…
  - [TOI-2109 b] raw `2,230 °C` (줄 41, 뒤): … irradiated. The dayside temperature measures 3,630 K (3,360 °C; 6,070 °F), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (【2,230 °C】; 4,040 °F). Only 55 Cancri e and KELT-9b have hotter dayside temperatures. This planet is around 30% larger than Jupiter and five times more massive.…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-059

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.3394e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `2.10±0.12 R🜨` (줄 16, 뒤):   - Mean radius: 【2.10±0.12 R🜨】
  - [Kepler-22b] raw `2.1 R🜨` (줄 29, 뒤): Kepler-22b's radius was initially thought to be 2.4 times that of Earth, but has since been revised to 【2.1 R🜨】 as of 2023. Its mass and surface composition remain unknown, with only some rough estimates established: at the time of the discovery announcement, i…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-060

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 5.05203e+16, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `5.34 light-years` (줄 62, 뒤): …ed as close as 1.28 parsecs (4.17 light-years) from the Sun about 861,000 years ago. García-Sánchez 2001 suggested that the star passed 1.64 parsecs (【5.34 light-years】) from the Sun about 1 million years ago. It was the brightest star in the night sky over 1 million years ago, peaking with an apparent magnitude of -…
  - [Zeta Leporis] raw `1.64 parsecs` (줄 62, 뒤): …this star passed as close as 1.28 parsecs (4.17 light-years) from the Sun about 861,000 years ago. García-Sánchez 2001 suggested that the star passed 【1.64 parsecs】 (5.34 light-years) from the Sun about 1 million years ago. It was the brightest star in the night sky over 1 million years ago, peaking with an appar…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-061

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base -14.8219, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `−14° 49′ 19.0199″` (줄 5, 여러 칸): - Declination: 【−14° 49′ 19.0199″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [케플러-16b] `14`: - 표면중력: 【14】.52 (± 0.7) m/s²
  - [케플러-16b] `14`: …은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및 3311 K, 광도는 태양의 【14】% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
  - [COROT-7b] `49`: - 적경: 06ʰ 43ᵐ 【49】.0ˢ
  - [글리제 1214 b] `49`: - 적위: +04° 57′ 【49】.7″
  - [센타우루스자리 프록시마 b] `14`: 프록시마 b는 적색왜성 센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 【14】%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우…

### E-en-062

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.71711e+13, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `861,000 years` (줄 62, 뒤): Bobylev's calculations from 2010 suggest that this star passed as close as 1.28 parsecs (4.17 light-years) from the Sun about 【861,000 years】 ago. García-Sánchez 2001 suggested that the star passed 1.64 parsecs (5.34 light-years) from the Sun about 1 million years ago. It was the brightest …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-063

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 3.73995e+11, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `2.5 AU` (줄 50, 뒤): …in a 5.4 AU radius. The temperature of the dust was estimated as about 340 K. Based on heating from the star, this could place the grains as close as 【2.5 AU】 from Zeta Leporis.
  - [Zeta Leporis] raw `2.5` (줄 58, 뒤): | Asteroid belt | 【2.5】–6.1 AU | 2.5–6.1 AU | 2.5–6.1 AU | 2.5–6.1 AU | — | — |
  - [Zeta Leporis] raw `2.5` (줄 58, 뒤): | Asteroid belt | 2.5–6.1 AU | 【2.5】–6.1 AU | 2.5–6.1 AU | 2.5–6.1 AU | — | — |
  - [Zeta Leporis] raw `2.5` (줄 58, 뒤): | Asteroid belt | 2.5–6.1 AU | 2.5–6.1 AU | 【2.5】–6.1 AU | 2.5–6.1 AU | — | — |
  - [Zeta Leporis] raw `2.5` (줄 58, 뒤): | Asteroid belt | 2.5–6.1 AU | 2.5–6.1 AU | 2.5–6.1 AU | 【2.5】–6.1 AU | — | — |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-064

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.01088e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `117` (줄 50, 머리글): | c (unconfirmed) | — | — | >1.13; 1.57, 2.67, 88 or 【117】 | — | — | — |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-065

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 9.62997e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.347±0.047 RJ` (줄 49, 뒤): | b | 5.02±0.75 MJ | 0.01791±0.00065 | 0.67247414(28) | 0 | 70.74±0.37 | 【1.347±0.047 RJ】 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-066

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 851524, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `9.8556+0.0012 −0.0011 d` (줄 9, 뒤):   - Orbital period (sidereal): 【9.8556+0.0012 −0.0011 d】
  - [Ross 128 b] raw `9.9 days` (줄 39, 뒤): Ross 128 b is a closely orbiting planet, with a year (orbital period) lasting about 【9.9 days】. Its semi-major axis is 0.0496 AU (7.42 million km). According to some models of the planet's orbit, its orbit is quite circular, with an eccentricit…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-067

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 8.23084e+18, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `870 ly` (줄 31, 뒤): TOI-2109 is a magnitude 10.2 star in the constellation of Hercules. It is located 【870 ly】 (268 pc) from Earth based on parallax measurements. This star is host to one confirmed exoplanet.
  - [TOI-2109 b] raw `873 ± 5 ly` (줄 14, 뒤): - Distance 【873 ± 5 ly】 (268 ± 1 pc)
  - [TOI-2109 b] raw `268 ± 1 pc` (줄 14, 뒤): - Distance 873 ± 5 ly (【268 ± 1 pc】)
  - [TOI-2109 b] raw `268 pc` (줄 31, 뒤): TOI-2109 is a magnitude 10.2 star in the constellation of Hercules. It is located 870 ly (【268 pc】) from Earth based on parallax measurements. This star is host to one confirmed exoplanet.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-068

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 10999.8, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `19,340 °F` (줄 37, 뒤): The thermosphere layer of KELT-9b is expected to heat up to 10,000–11,000 K (9,727–10,727 °C; 17,540–【19,340 °F】), driven by ionization of heavy metals atoms like iron.
  - [KELT-9b] raw `11,000 K` (줄 37, 뒤): The thermosphere layer of KELT-9b is expected to heat up to 10,000–【11,000 K】 (9,727–10,727 °C; 17,540–19,340 °F), driven by ionization of heavy metals atoms like iron.
  - [KELT-9b] raw `10,727 °C` (줄 37, 뒤): The thermosphere layer of KELT-9b is expected to heat up to 10,000–11,000 K (9,727–【10,727 °C】; 17,540–19,340 °F), driven by ionization of heavy metals atoms like iron.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-069

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 26640, 표 안 예, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `7.4 hour` (줄 79, 뒤): | 1 October 2011 |  |  |  | 【7.4 hour】 transit observed by Spitzer space telescope, confirming the planet |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-070

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.1813e+09, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.698+0.062 −0.057 R☉` (줄 17, 뒤): - Radius 【1.698+0.062 −0.057 R☉】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-071

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 1.075e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `1.8+0.56 −0.43 M🜨` (줄 14, 뒤):   - Mass: ≥1.40±0.13 M🜨; 【1.8+0.56 −0.43 M🜨】 (predicted)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-072

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 5.5857e+16, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.77+0.88 −0.68 Gyr` (줄 24, 뒤): - Age 【1.77+0.88 −0.68 Gyr】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-073

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 20000, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `20.0` (줄 12, 뒤): - Radial velocity (Rv) 【20.0】–24.7 km/s
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-074

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 86.7389, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `05ʰ 46ᵐ 57.34096ˢ` (줄 4, 여러 칸): - Right ascension: 【05ʰ 46ᵐ 57.34096ˢ】
  - [KELT-9b] raw `86.79°±0.25°` (줄 13, 뒤):   - Inclination: 【86.79°±0.25°】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [COROT-7b] `46`: - 적위: −01° 03′ 【46】.0″
  - [글리제 1214 b] `05`: …과 질량값으로부터 b는 질량의 약 4분의 3이 물과 얼음이며, 나머지는 암석으로 이루어져 있는 바다 행성일 가능성이 있다. 행성 질량의 약 0.【05】퍼센트에 해당하는 수소와 헬륨 대기가 표면을 둘러싸고 있을 가능성이 있다. 가설이 맞다면 충분한 대기압 때문에 액체 상태의 물이 행성 전체에 가…
  - [센타우루스자리 프록시마 b] `05`: 모항성에서 프록시마 b까지의 거리는 0.【05】 AU(750만 km 또는 460만 마일)로 가깝다. b는 11.2 일을 1 주기로 프록시마를 공전하고 있으며 예상되는 b의 질량은 지구의 최소…
  - [센타우루스자리 프록시마 b] `05`: 센타우루스자리 프록시마 b는 어머니 별을 11.186 일에 1회 돌고 있으며 별과의 평균 거리는 약 0.【05】 천문단위(700만 km 또는 500만 마일)로 태양과 지구 사이 거리의 약 20분의 1 정도이다. 참고로 태양에서 가장 가까운 행성 수성의 평…
  - [센타우루스자리 프록시마 b] `46`: …록시마 항성의 질량은 태양의 12%이며 반지름은 14%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 【46】억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 83 일이며 광도는 태양의 0.0015 배이다. 삼중성계의 나…

### E-en-075

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 5.68037e+16, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.8 billion years` (줄 35, 뒤): …0 °C; 11,290 °F), which is 10% hotter than the Sun, whose temperature measures 5,772 K (5,499 °C; 9,930 °F). The age of TOI-2109 is uncertain, around 【1.8 billion years】. The rotation period of this star is 14% longer than Earth's day, about 1/25th that of the Sun.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.31152e+16: [케플러-16b] raw `20억 년` (줄 48, 두 언어 쪽): …온도는 4450 K 및 3311 K, 광도는 태양의 14% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 【20억 년】이다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-076

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 9999.82, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `17,540` (줄 37, 뒤): The thermosphere layer of KELT-9b is expected to heat up to 10,000–11,000 K (9,727–10,727 °C; 【17,540】–19,340 °F), driven by ionization of heavy metals atoms like iron.
  - [KELT-9b] raw `10,000` (줄 37, 뒤): The thermosphere layer of KELT-9b is expected to heat up to 【10,000】–11,000 K (9,727–10,727 °C; 17,540–19,340 °F), driven by ionization of heavy metals atoms like iron.
  - [KELT-9b] raw `9,727` (줄 37, 뒤): The thermosphere layer of KELT-9b is expected to heat up to 10,000–11,000 K (【9,727】–10,727 °C; 17,540–19,340 °F), driven by ionization of heavy metals atoms like iron.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-077

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.91343e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `3.0 R🜨` (줄 25, 뒤): … its density, is not known as no transits of this planet have been observed. Ross 128 b would be 0.5 R🜨 (Earth radii) for a pure-iron composition and 【3.0 R🜨】 for a pure hydrogen-helium composition, both implausible extremes. For a more plausible Earth-like composition, the planet would need to be about 1.1…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-078

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 1.03797e-06, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `3.7367±0.0197 mas` (줄 13, 뒤): - Parallax (π) 【3.7367±0.0197 mas】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-079

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 6.33869e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `670 light-years` (줄 23, 뒤): …b, also designated HD 195689 b, is an exoplanet and ultra-hot Jupiter in a polar orbit around the late B-type/early A-type star KELT-9, located about 【670 light-years】 from Earth. Detected using the Kilodegree Extremely Little Telescope, the discovery of KELT-9b was announced in 2016. As of June 2017, it is the hott…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-080

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 6.66506e+17, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `21.6 parsecs` (줄 32, 뒤): Zeta Leporis, Latinized from ζ Leporis formally named Darlugal, is a star approximately 70.5 light-years (【21.6 parsecs】) away in the southern constellation of Lepus. It has an apparent visual magnitude of 3.5, which is bright enough to be seen with the naked eye. In 20…
  - [Zeta Leporis] raw `21.61 ± 0.07 pc` (줄 15, 뒤): - Distance 70.5 ± 0.2 ly (【21.61 ± 0.07 pc】)
  - [Zeta Leporis] raw `70.5 ± 0.2 ly` (줄 15, 뒤): - Distance 【70.5 ± 0.2 ly】 (21.61 ± 0.07 pc)
  - [Zeta Leporis] raw `70.5 light-years` (줄 32, 뒤): Zeta Leporis, Latinized from ζ Leporis formally named Darlugal, is a star approximately 【70.5 light-years】 (21.6 parsecs) away in the southern constellation of Lepus. It has an apparent visual magnitude of 3.5, which is bright enough to be seen with the na…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-081

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 6.31152e+11, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `20,000 years` (줄 52, 뒤): …he Moon. Astronomers Christine Chen and professor Michael Jura found that the dust contained within this belt should have fallen into the star within 【20,000 years】, a time period much shorter than Zeta Leporis's estimated age, suggesting that some mechanism must be replenishing the belt. The belt's age is estima…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-082

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 9.12547e+11, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `6.1 AU` (줄 58, 뒤): | Asteroid belt | 2.5–【6.1 AU】 | 2.5–6.1 AU | 2.5–6.1 AU | 2.5–6.1 AU | — | — |
  - [Zeta Leporis] raw `6.1 AU` (줄 58, 뒤): | Asteroid belt | 2.5–6.1 AU | 2.5–【6.1 AU】 | 2.5–6.1 AU | 2.5–6.1 AU | — | — |
  - [Zeta Leporis] raw `6.1 AU` (줄 58, 뒤): | Asteroid belt | 2.5–6.1 AU | 2.5–6.1 AU | 2.5–【6.1 AU】 | 2.5–6.1 AU | — | — |
  - [Zeta Leporis] raw `6.1 AU` (줄 58, 뒤): | Asteroid belt | 2.5–6.1 AU | 2.5–6.1 AU | 2.5–6.1 AU | 2.5–【6.1 AU】 | — | — |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-083

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 491, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `0.491+0.072 −0.066 g/cm³` (줄 19, 뒤):   - Mean density: 【0.491+0.072 −0.066 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-084

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 24700, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `24.7 km/s` (줄 12, 뒤): - Radial velocity (Rv) 20.0–【24.7 km/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-085

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 81900, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `81.9±1.7 km/s` (줄 23, 뒤): - Rotational velocity (v sin i) 【81.9±1.7 km/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-086

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 2.87732e+30, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.447+0.075 −0.078 M☉` (줄 16, 뒤): - Mass 【1.447+0.075 −0.078 M☉】
  - [Zeta Leporis] raw `1.46 M☉` (줄 18, 뒤): - Mass 【1.46 M☉】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-087

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.50442e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `289.863876±0.000013 d` (줄 10, 뒤):   - Orbital period (sidereal): 【289.863876±0.000013 d】
  - [Kepler-22b] raw `290 days` (줄 23, 뒤): … planet or have a volatile-rich composition with a liquid or gaseous outer layer. The planet's known orbital parameters are its orbital period, about 【290 days】, and its inclination, approximately 90°. Its surface temperature may be moderate if it does not experience extreme greenhouse heating. In the absence…
  - [Kepler-22b] raw `290 days` (줄 43, 뒤): The only parameters of the planet's orbit that are currently available are its orbital period, which is about 【290 days】, and its inclination, which is approximately 90°. From Earth, the planet appears to make a transit across the disk of its host star. In order to obta…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-088

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base -22280, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `−22.28±1.23 km/s` (줄 11, 뒤): - Radial velocity (Rv) 【−22.28±1.23 km/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-089

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 5.4347e+25, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `9.1 M🜨` (줄 17, 뒤):   - Mass: <【9.1 M🜨】
  - [Kepler-22b] raw `9.1 M🜨` (줄 29, 뒤): … in Kipping et al. (2013) does not reliably detect the mass (the upper limit is 52.8 M🜨). As of 2023, the upper limit has been constrained to at most 【9.1 M🜨】.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-090

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 1.28556e-05, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `46.28±0.16 mas` (줄 14, 뒤): - Parallax (π) 【46.28±0.16 mas】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-091

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 98496, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.14 days` (줄 22, 뒤): - Rotation 【1.14 days】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-092

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 253.186, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `16ʰ 52ᵐ 44.72027ˢ` (줄 4, 여러 칸): - Right ascension: 【16ʰ 52ᵐ 44.72027ˢ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 258.829: [글리제 1214 b] raw `17ʰ 15ᵐ 18.94ˢ` (줄 6, 두 언어 쪽): - 적경: 【17ʰ 15ᵐ 18.94ˢ】
  - base 229.858: [글리제 581 c] raw `15ʰ 19ᵐ 26ˢ` (줄 6, 한쪽 언어 쪽): - 적경: 【15ʰ 19ᵐ 26ˢ】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [케플러-16b] `16`: # 케플러-【16】b
  - [케플러-16b] `16`: - 케플러-【16】b
  - [케플러-16b] `16`: - 이름: 케플러-【16】 (KOI-1611)
  - [케플러-16b] `16`: 케플러-【16】b(Kepler-16b)는 229일 주기로 케플러-16 쌍성계를 공전하는 외계 행성으로, 크기는 대략 토성 정도이며 암석과 얼음의 구성 비율이 …
  - [케플러-16b] `16`: 케플러-16b(Kepler-【16】b)는 229일 주기로 케플러-16 쌍성계를 공전하는 외계 행성으로, 크기는 대략 토성 정도이며 암석과 얼음의 구성 비율이 각각 절반 정도이다.…

### E-en-093

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 1.41, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `1.41±0.14 m/s` (줄 10, 뒤):   - Semi-amplitude: 【1.41±0.14 m/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-094

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 5200, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `5.2 g/cm³` (줄 18, 뒤):   - Mean density: <【5.2 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [센타우루스자리 프록시마 b] `5.2`: …끔씩, 그러나 단순하게, 분리되지 않은 홑별처럼 보일 것이다. 절대등급에 기초하면 센타우루스자리 알파 A와 B의 겉보기등급은 각각 −6.5와 −【5.2】일 것이다.

### E-en-095

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 6.17136e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `200 parsecs` (줄 21, 뒤): …interest designation KOI-087.01) is an exoplanet orbiting the Sun-like star Kepler-22 within its habitable zone. It is located about 640 light-years (【200 parsecs】) from Earth in the constellation Cygnus. Discovered by NASA's Kepler space telescope, it was announced on 5 December 2011 as the first known transiti…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-096

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 245000, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `245 km/s` (줄 24, 뒤): - Rotational velocity (v sin i) 【245 km/s】
  - [Zeta Leporis] raw `245 km/s` (줄 42, 뒤): …trum appear nebulous because it is spinning rapidly, causing the lines to broaden because of the Doppler effect. The projected rotational velocity is 【245 km/s】, giving a lower limit on the star's actual equatorial azimuthal velocity.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-097

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 2.14999e+26, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `36 Earth masses` (줄 29, 뒤): …ablished: at the time of the discovery announcement, it was known to have fewer than 124 Earth masses at the 3-sigma confidence limit, and fewer than 【36 Earth masses】 at 1-sigma confidence. The adopted model in Kipping et al. (2013) does not reliably detect the mass (the upper limit is 52.8 M🜨). As of 2023, the upp…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 4개:
  - [글리제 1214 b] `36`: - 궤도경사각: 88.62(+0.【36】, -0.28)
  - [글리제 581 c] `36`: …적색왜성 글리제 581을 공전하는 행성으로, 다른 이름으로 Wolf 562 c, HIP 74995 c로 불리기도 한다. 최소 질량은 지구의 5.【36】배로, 질량이 지구의 10배 미만이라는 점에서 슈퍼지구로 분류할 수 있다. 이 행성의 질량은 발견 당시 기술력으로 감지할 수 있는 질량 하한선 …
  - [글리제 581 c] `36`: …기적인 움직임을 보여주는 것을 통해 계산이 가능하다. 네 행성 모두 케플러의 행성운동 법칙을 따른다고 가정하면 c의 최소 질량은 지구질량의 5.【36】배이다. 시선 속도법 하나만으로는 실제 질량을 잴 수 없으나 최소 질량보다 월등히 크지는 않을 것으로 보인다(지나치게 질량이 클 경우 행성계는 …
  - [HD 20367 b] `36`: | 화성 원일점 플럭스 | 494.00 | 【36】.06% |

### E-en-098

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 출력, base 5.3592e+27, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `14 L☉` (줄 20, 뒤): - Luminosity 【14 L☉】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [케플러-16b] `14`: - 표면중력: 【14】.52 (± 0.7) m/s²
  - [케플러-16b] `14`: …은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및 3311 K, 광도는 태양의 【14】% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
  - [센타우루스자리 프록시마 b] `14`: 프록시마 b는 적색왜성 센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 【14】%이다. 표면 온도는 3042 켈빈이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우…

### E-en-099

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 293, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `293±32 m/s` (줄 14, 뒤):   - Semi-amplitude: 【293±32 m/s】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-100

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 7.008e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `7008 km` (줄 25, 뒤): …extremes. For a more plausible Earth-like composition, the planet would need to be about 1.10 R🜨 - i.e., 1.1 times the radius of Earth (approximately 【7008 km】). With that radius, Ross 128 b would be slightly denser than Earth, due to how a rocky planet would become more compact as it increases in size. It w…
  - [Ross 128 b] raw `1.10 R🜨` (줄 25, 뒤): … R🜨 for a pure hydrogen-helium composition, both implausible extremes. For a more plausible Earth-like composition, the planet would need to be about 【1.10 R🜨】 - i.e., 1.1 times the radius of Earth (approximately 7008 km). With that radius, Ross 128 b would be slightly denser than Earth, due to how a rocky p…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-101

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 7.40553e+26, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `124 Earth masses` (줄 29, 뒤): …ce composition remain unknown, with only some rough estimates established: at the time of the discovery announcement, it was known to have fewer than 【124 Earth masses】 at the 3-sigma confidence limit, and fewer than 36 Earth masses at 1-sigma confidence. The adopted model in Kipping et al. (2013) does not reliably d…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-102

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 2400, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `2,400+400 −300 K` (줄 21, 뒤):   - Temperature: 4,579±120 K (dayside) 【2,400+400 −300 K】 (nightside)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-103

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.04134e+17, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `11.007 light-years` (줄 17, 뒤): …rmed Earth-sized exoplanet, likely rocky, that is orbiting near the inner edge of the habitable zone of the red dwarf star Ross 128, at a distance of 【11.007 light-years】 (3.375 parsecs) from Earth in the constellation of Virgo. The exoplanet was found using a decade's worth of radial velocity data using the European S…
  - [Ross 128 b] raw `3.375 parsecs` (줄 17, 뒤): …planet, likely rocky, that is orbiting near the inner edge of the habitable zone of the red dwarf star Ross 128, at a distance of 11.007 light-years (【3.375 parsecs】) from Earth in the constellation of Virgo. The exoplanet was found using a decade's worth of radial velocity data using the European Southern Observa…
  - [Ross 128 b] raw `11.03 light-years` (줄 33, 뒤): …ison, the Sun has a temperature of 5772 K and age of 4.5 billion years, making Ross 128 half the temperature and over twice the age. The star is only 【11.03 light-years】 away, making it one of the 20 closest stars known.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-104

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 97200, 표 안 예, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `1.125 days` (줄 43, 뒤): …sing the CHEOPS space telescope, which could be attributed to a yet unseen exoplanet. This putative planet should have an orbital period greater than 【1.125 days】 and its other characteristics remain unconstrained.
  - [TOI-2109 b] raw `1.13` (줄 50, 머리글): | c (unconfirmed) | — | — | >【1.13】; 1.57, 2.67, 88 or 117 | — | — | — |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-105

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 7.28981e+15, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `231+126 −181 Myr` (줄 25, 뒤): - Age 【231+126 −181 Myr】
  - [Zeta Leporis] raw `231 million years` (줄 44, 뒤): …ogen and helium, what astronomers term the star's metallicity, is only 17% of the abundance in the Sun. The star appears to be young, probably around 【231 million years】 in age, but the margin of error spans 50–347 million years old.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-106

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 9772, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `9,772 K` (줄 22, 뒤): - Temperature 【9,772 K】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-107

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 출력, base 1.38574e+24, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `0.00362 L☉` (줄 33, 뒤): …all red dwarf star known as Ross 128. The star is 17% the mass and 20% the radius of that of the Sun. It has a temperature of 3192 K, a luminosity of 【0.00362 L☉】, and an age of 9.45±0.60 billion years. For comparison, the Sun has a temperature of 5772 K and age of 4.5 billion years, making Ross 128 half the te…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-108

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 300.928, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `82 °F` (줄 15, 뒤):   - Temperature: 213–301 K (−60–28 °C; −76–【82 °F】) (equilibrium)
  - [Ross 128 b] raw `301 K` (줄 15, 뒤):   - Temperature: 213–【301 K】 (−60–28 °C; −76–82 °F) (equilibrium)
  - [Ross 128 b] raw `28 °C` (줄 15, 뒤):   - Temperature: 213–301 K (−60–【28 °C】; −76–82 °F) (equilibrium)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 292: [지구 유사도 지수] raw `292 K` (줄 38, 한쪽 언어 쪽): | KOI-4878.01* | 0.98 | 확인되지 않았으나, 표면 온도와 기압이 【292 K】, 10 기압으로 추정됨. |
  - base 288: [지구 유사도 지수] raw `288 K` (줄 51, 한쪽 언어 쪽): | 케플러-452b | 0.83 | 표면 온도와 기압은 【288 K】, 16~56 기압으로 추정. |
  - base 284: [지구 유사도 지수] raw `284 K` (줄 41, 한쪽 언어 쪽): | 글리제 581 g* | 0.92 | 확인되지 않음. 조석 고정되었으며, 표면 온도와 기압은 【284 K】, 18 기압으로 추정. |
  - base 276: [지구 유사도 지수] raw `276 K` (줄 44, 한쪽 언어 쪽): | 케플러-438b | 0.88 | 온도는 【276 K】이며, 조석 고정되었으리라 추정됨. 거주가능성은 확실하지 않음. |
  - base 273: [지구 유사도 지수] raw `273 K` (줄 58, 한쪽 언어 쪽): | 케플러-440b | 0.75 | 궤도가 타원형, 표면 온도 【273 K】 |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [목동자리 타우 b] `28`: - 중원소함량: 0.【28】 [Fe/H]
  - [글리제 1214 b] `28`: - 궤도경사각: 88.62(+0.36, -0.【28】)

### E-en-109

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 3627.59, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `6,070 °F` (줄 41, 뒤): …9,000 km) from its host star. The extreme proximity also means TOI-2109 b is strongly irradiated. The dayside temperature measures 3,630 K (3,360 °C; 【6,070 °F】), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (2,230 °C; 4,040 °F). Only 55 Cancri e and KELT-9b have hotter dayside tem…
  - [TOI-2109 b] raw `3,630 K` (줄 41, 뒤): …nomical units (2,679,000 km) from its host star. The extreme proximity also means TOI-2109 b is strongly irradiated. The dayside temperature measures 【3,630 K】 (3,360 °C; 6,070 °F), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (2,230 °C; 4,040 °F). Only 55 Cancri e and KELT-9b hav…
  - [TOI-2109 b] raw `3,360 °C` (줄 41, 뒤): …nits (2,679,000 km) from its host star. The extreme proximity also means TOI-2109 b is strongly irradiated. The dayside temperature measures 3,630 K (【3,360 °C】; 6,070 °F), while the nightside is around 1,000 degrees cooler, at less than 2,500 K (2,230 °C; 4,040 °F). Only 55 Cancri e and KELT-9b have hotter d…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3311: [케플러-16b] raw `3311 K` (줄 48, 두 언어 쪽): … 걸쳐 공전한다. 항성의 질량은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및 【3311 K】, 광도는 태양의 14% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
  - base 3273.15: [센타우루스자리 프록시마 b] raw `3000 °C` (줄 50, 한쪽 언어 쪽): …역 안에 있을 수 있는 까닭은 프록시마가 스펙트럼상 M형 별인 적색왜성이기 때문이다. 즉, 모항성인 프록시마의 온도가 낮기 때문에(표면온도 약 【3000 °C】) 이렇게 가까움에도 프록시마 b가 생명체 거주 가능 영역에 있을 수 있는 것이다. 태양 질량의 8분의 1 수준인 프록시마 주변의 생물권은 항성…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-110

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 127969, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `1.4811235±0.0000011 d` (줄 12, 뒤):   - Orbital period (sidereal): 【1.4811235±0.0000011 d】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 136546: [글리제 1214 b] raw `1.5803925 ± 0.0000117 일` (줄 13, 두 언어 쪽): - 공전주기: 【1.5803925 ± 0.0000117 일】(37.92942 시간)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-111

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 6.05487e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `640 light-years` (줄 21, 뒤): …Kepler object of interest designation KOI-087.01) is an exoplanet orbiting the Sun-like star Kepler-22 within its habitable zone. It is located about 【640 light-years】 (200 parsecs) from Earth in the constellation Cygnus. Discovered by NASA's Kepler space telescope, it was announced on 5 December 2011 as the first k…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-112

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 6527.59, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `11,290 °F` (줄 35, 뒤): …he Sun, comparable to Sirius A, 1.4 times more massive and nearly five times brighter. The effective temperature of its surface is 6,530 K (6,260 °C; 【11,290 °F】), which is 10% hotter than the Sun, whose temperature measures 5,772 K (5,499 °C; 9,930 °F). The age of TOI-2109 is uncertain, around 1.8 billion yea…
  - [TOI-2109 b] raw `6,530+160 −150 K` (줄 20, 뒤): - Temperature 【6,530+160 −150 K】
  - [TOI-2109 b] raw `6,530 K` (줄 35, 뒤): …times larger than the Sun, comparable to Sirius A, 1.4 times more massive and nearly five times brighter. The effective temperature of its surface is 【6,530 K】 (6,260 °C; 11,290 °F), which is 10% hotter than the Sun, whose temperature measures 5,772 K (5,499 °C; 9,930 °F). The age of TOI-2109 is uncertain, a…
  - [TOI-2109 b] raw `6,260 °C` (줄 35, 뒤): …ger than the Sun, comparable to Sirius A, 1.4 times more massive and nearly five times brighter. The effective temperature of its surface is 6,530 K (【6,260 °C】; 11,290 °F), which is 10% hotter than the Sun, whose temperature measures 5,772 K (5,499 °C; 9,930 °F). The age of TOI-2109 is uncertain, around 1.8 …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-113

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 3.15332e+26, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `52.8 M🜨` (줄 29, 뒤): …nd fewer than 36 Earth masses at 1-sigma confidence. The adopted model in Kipping et al. (2013) does not reliably detect the mass (the upper limit is 【52.8 M🜨】). As of 2023, the upper limit has been constrained to at most 9.1 M🜨.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-114

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 129600, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `1.5 days` (줄 27, 뒤): …tar known to have a planet. KELT-9b occupies a circular but strongly inclined orbit a mere 0.03462 AU from KELT-9 with an orbital period of less than 【1.5 days】.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 136546: [글리제 1214 b] raw `1.5803925 ± 0.0000117 일` (줄 13, 두 언어 쪽): - 공전주기: 【1.5803925 ± 0.0000117 일】(37.92942 시간)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-115

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 4579, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `4,579±120 K` (줄 21, 뒤):   - Temperature: 【4,579±120 K】 (dayside) 2,400+400 −300 K (nightside)
  - [KELT-9b] raw `7,820 °F` (줄 35, 뒤): As of 2022, KELT-9b is the hottest known exoplanet, with dayside temperatures approaching 4,600 K (4,327 °C; 【7,820 °F】) — warmer than some K-type stars. Molecules on the day side are broken into their component atoms, so that normally sequestered refractory elements c…
  - [KELT-9b] raw `4,600 K` (줄 35, 뒤): As of 2022, KELT-9b is the hottest known exoplanet, with dayside temperatures approaching 【4,600 K】 (4,327 °C; 7,820 °F) — warmer than some K-type stars. Molecules on the day side are broken into their component atoms, so that normally sequestered r…
  - [KELT-9b] raw `4,327 °C` (줄 35, 뒤): As of 2022, KELT-9b is the hottest known exoplanet, with dayside temperatures approaching 4,600 K (【4,327 °C】; 7,820 °F) — warmer than some K-type stars. Molecules on the day side are broken into their component atoms, so that normally sequestered refractory …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4450: [케플러-16b] raw `4450 K` (줄 48, 두 언어 쪽): … 서로를 41일에 걸쳐 공전한다. 항성의 질량은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 【4450 K】 및 3311 K, 광도는 태양의 14% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-116

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 3.22499e+24, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `0.54 Earth masses` (줄 63, 뒤): …be caused by an orbiting satellite. Such variations were not found, ruling out the existence of any satellites of Kepler-22b with a mass greater than 【0.54 Earth masses】.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-117

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 5000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `5 km/s` (줄 39, 뒤): … the upper atmosphere KELT-9b. Due to this, it is suspected that the planet is losing 10¹³ grams per second and has a vertical outflow wind speed of ~【5 km/s】. Another 2026 study potentially detected magnetic field for the planet, via observation of the Zeeman effect with the SPIRou spectrograph.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [케플러-16b] `5`: …8 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및 3311 K, 광도는 태양의 14% 및 0.【5】%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
  - [COROT-7b] `5`: - 질량: 0.035(+0, -0.017) 목성질량[11(+0, -【5】.4) 지구질량]
  - [COROT-7b] `5`: … 있는 외계 행성이다. 2009년 프랑스 주도의 COROT 계획 중 발견되었다. 이 행성은 반지름이 지구의 1.7배에 불과하고, 질량은 지구의 【5】.6 ~ 11배 사이일 것으로 보인다. 질량을 고려하면 가스 행성이 아니라 암석 행성일 것이다. 항성에서 매우 가까운 거리에 있기 때문에 1회 …
  - [COROT-7b] `5`: COROT 계획은 2009년 【5】월 12일 기준으로 COROT-7b의 천구 좌표를 아직 발표하지 않았다. 이 계획은 HARPS 분광사진기를 써서 b의 존재를 검증하려고 시도했으…
  - [목동자리 타우 b] `5`: - 겉보기 등급: 4.【5】

### E-en-118

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 8.36108e+24, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `1.40±0.13 M🜨` (줄 14, 뒤):   - Mass: ≥【1.40±0.13 M🜨】; 1.8+0.56 −0.43 M🜨 (predicted)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-119

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 출력, base 1.80299e+27, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `4.71+0.38 −0.27 L☉` (줄 18, 뒤): - Luminosity 【4.71+0.38 −0.27 L☉】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-120

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 5.17908e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `0.03462 AU` (줄 27, 뒤): …. KELT-9, classified as B9.5-A0 could be the first B-type star known to have a planet. KELT-9b occupies a circular but strongly inclined orbit a mere 【0.03462 AU】 from KELT-9 with an orbital period of less than 1.5 days.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-121

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 7429.82, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `12,914 °F` (줄 27, 뒤): … discovery of KELT-9b, only six A-type stars were known to have planets, of which the warmest, WASP-33, is significantly cooler at 7,430 K (7,157 °C; 【12,914 °F】); no B-type stars were previously known to host planets. KELT-9, classified as B9.5-A0 could be the first B-type star known to have a planet. KELT-9b…
  - [KELT-9b] raw `7,430 K` (줄 27, 뒤): …lanet. Prior to the discovery of KELT-9b, only six A-type stars were known to have planets, of which the warmest, WASP-33, is significantly cooler at 【7,430 K】 (7,157 °C; 12,914 °F); no B-type stars were previously known to host planets. KELT-9, classified as B9.5-A0 could be the first B-type star known to h…
  - [KELT-9b] raw `7,157 °C` (줄 27, 뒤): …ior to the discovery of KELT-9b, only six A-type stars were known to have planets, of which the warmest, WASP-33, is significantly cooler at 7,430 K (【7,157 °C】; 12,914 °F); no B-type stars were previously known to host planets. KELT-9, classified as B9.5-A0 could be the first B-type star known to have a plan…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-122

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 가속도, base 10.945, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `10.945 m/s²` (줄 25, 뒤): … denser than Earth, due to how a rocky planet would become more compact as it increases in size. It would give the planet a gravitational pull around 【10.945 m/s²】, or about 1.12 times that of Earth.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-123

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.09505e+16, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `347 million years` (줄 44, 뒤): …ty, is only 17% of the abundance in the Sun. The star appears to be young, probably around 231 million years in age, but the margin of error spans 50–【347 million years】 old.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-124

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 2.679e+09, 표 안 예, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `2,679,000 km` (줄 41, 뒤): …ith the shortest orbital period of its class. It completes an orbit in just 0.67 days (16 hours), being separated by only 0.01791 astronomical units (【2,679,000 km】) from its host star. The extreme proximity also means TOI-2109 b is strongly irradiated. The dayside temperature measures 3,630 K (3,360 °C; 6,070 °F…
  - [TOI-2109 b] raw `0.01791 astronomical units` (줄 41, 뒤): …I-2109 b is a hot Jupiter, with the shortest orbital period of its class. It completes an orbit in just 0.67 days (16 hours), being separated by only 【0.01791 astronomical units】 (2,679,000 km) from its host star. The extreme proximity also means TOI-2109 b is strongly irradiated. The dayside temperature measures 3,630 K (3,36…
  - [TOI-2109 b] raw `0.01791±0.00065` (줄 49, 머리글): | b | 5.02±0.75 MJ | 【0.01791±0.00065】 | 0.67247414(28) | 0 | 70.74±0.37 | 1.347±0.047 RJ |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.54316e+09: [COROT-7b] raw `0.017` (줄 11, 두 언어 쪽): - 평균거리(AU): 【0.017】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-125

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.82509e+12, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `12.2 AU` (줄 48, 뒤): …magnetic spectrum, the InfraRed Astronomical Satellite was used to identify dust orbiting this star. This debris disk is constrained to a diameter of 【12.2 AU】.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-126

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 340, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `340 K` (줄 50, 뒤): …d more accurately to constrain the radius of the dust. It was found to lie within a 5.4 AU radius. The temperature of the dust was estimated as about 【340 K】. Based on heating from the star, this could place the grains as close as 2.5 AU from Zeta Leporis.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-127

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 5.03846e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `0.03368±0.00078 AU` (줄 10, 뒤):   - Semi-major axis: 【0.03368±0.00078 AU】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-128

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 89.764, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `89.764°+0.025° −0.042°` (줄 11, 뒤):   - Inclination: 【89.764°+0.025° −0.042°】
  - [Kepler-22b] raw `90°` (줄 23, 뒤): …ith a liquid or gaseous outer layer. The planet's known orbital parameters are its orbital period, about 290 days, and its inclination, approximately 【90°】. Its surface temperature may be moderate if it does not experience extreme greenhouse heating. In the absence of an atmosphere, its equilibrium tempe…
  - [Kepler-22b] raw `90°` (줄 43, 뒤): …eters of the planet's orbit that are currently available are its orbital period, which is about 290 days, and its inclination, which is approximately 【90°】. From Earth, the planet appears to make a transit across the disk of its host star. In order to obtain further information about the details of the p…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [케플러-16b] `90`: - 궤도경사각: 【90】.0322 ± 0.0023
  - [센타우루스자리 프록시마 b] `90`: …약 b의 궤도면이 관측자의 시선 방향과 거의 일치한다면 질량값은 지구의 1.27+0.19 −0.17 배일 것이다. 통계적으로 b의 질량은 대략 【90】%의 확률로 지구의 3배 미만일 것이다.
  - [센타우루스자리 프록시마 b] `90`: …진다면 질량을 계산할 수 있을 것이다. 만약 궤도가 보다 기울어져 있으면 실제 질량은 더 커질 것이며 질량값이 지구의 3 배 미만일 확률은 약 【90】%이다. b의 정확한 반지름은 알려지지 않았다. 만약 b가 암석으로 조성되어 있고 밀도를 지구와 같다고 가정하면 반지름은 최소 지구의 1.1 배…

### E-en-129

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 16.58, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `+16° 34′ 47.8400″` (줄 5, 여러 칸): - Declination: 【+16° 34′ 47.8400″】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 17.4561: [목동자리 타우 b] raw `+17° 27′ 22″` (줄 7, 두 언어 쪽): - 적위: 【+17° 27′ 22″】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [케플러-16b] `16`: # 케플러-【16】b
  - [케플러-16b] `16`: - 케플러-【16】b
  - [케플러-16b] `16`: - 이름: 케플러-【16】 (KOI-1611)
  - [케플러-16b] `16`: 케플러-【16】b(Kepler-16b)는 229일 주기로 케플러-16 쌍성계를 공전하는 외계 행성으로, 크기는 대략 토성 정도이며 암석과 얼음의 구성 비율이 …
  - [케플러-16b] `16`: 케플러-16b(Kepler-【16】b)는 229일 주기로 케플러-16 쌍성계를 공전하는 외계 행성으로, 크기는 대략 토성 정도이며 암석과 얼음의 구성 비율이 각각 절반 정도이다.…

### E-en-130

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.30115e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [KELT-9b] raw `1.82±0.03 RJ` (줄 17, 뒤):   - Mean radius: 【1.82±0.03 RJ】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-131

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 213, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `213` (줄 15, 뒤):   - Temperature: 【213】–301 K (−60–28 °C; −76–82 °F) (equilibrium)
  - [Ross 128 b] raw `213 K` (줄 29, 뒤): …orbed by a celestial object. With these three albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 【213 K】 (−60 °C; −76 °F). For an Earth-like albedo of 0.3, the planet would have an equilibrium temperature of 280 K (7 °C; 44 °F), about 8 Kelvins lower tha…
  - [Ross 128 b] raw `−60` (줄 15, 뒤):   - Temperature: 213–301 K (【−60】–28 °C; −76–82 °F) (equilibrium)
  - [Ross 128 b] raw `−76` (줄 15, 뒤):   - Temperature: 213–301 K (−60–28 °C; 【−76】–82 °F) (equilibrium)
  - [Ross 128 b] raw `−60 °C` (줄 29, 뒤): …y a celestial object. With these three albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (【−60 °C】; −76 °F). For an Earth-like albedo of 0.3, the planet would have an equilibrium temperature of 280 K (7 °C; 44 °F), about 8 Kelvins lower than Earth'…
  - [Ross 128 b] raw `−76 °F` (줄 29, 뒤): …stial object. With these three albedo parameters, Ross 128 b would have a Teq of either 294 K (21 °C; 70 °F), 269 K (−4 °C; 25 °F), or 213 K (−60 °C; 【−76 °F】). For an Earth-like albedo of 0.3, the planet would have an equilibrium temperature of 280 K (7 °C; 44 °F), about 8 Kelvins lower than Earth's averag…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 203.15: [케플러-16b] raw `−70 °C` (줄 26, 두 언어 쪽): 케플러-16b의 궤도는 생명체 거주가능 영역의 바깥쪽 끄트머리에 걸쳐 있긴 하나, 거대 기체 행성으로서 표면 온도는 −100 ~ 【−70 °C】 정도이다.
  - base 230: [지구 유사도 지수] raw `230 K` (줄 67, 한쪽 언어 쪽): | TRAPPIST-1 f | 0.70 | 온도 【230 K】, 지구형 행성일 확률이 약간 존재. |
  - base 233: [지구 유사도 지수] raw `233 K` (줄 50, 한쪽 언어 쪽): | 케플러-442b | 0.84 | 거주가능 구역의 정중앙에 위치. 온도 【233 K】. |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [센타우루스자리 프록시마 b] `60`: …가장 밝게 빛나던 별은 보이지 않을 것이다. 태양은 센타우루스자리 알파 계의 현재 적경 및 적위의 대척점인 적경 02ʰ 39ᵐ 35ˢ, 적위 +【60】° 50′(2000년 기준)에서 겉보기등급 +0.5의 노란색 별로 보일 것이다. 이 위치는 3.4 등성 카시오페이아자리 엡실론의 근처이며 심장 …
  - [지구 유사도 지수] `60`: | 케플러-296f | 0.【60】 |  |
  - [지구 유사도 지수] `60`: | 글리제 667 Ce* | 0.【60】 | 존재에 대한 논란이 있음. |
  - [지구 유사도 지수] `60`: | HD 69830 d | 0.【60】 | 행성의 밀도나 대기권 정보가 부족. |
  - [지구 유사도 지수] `76`: | 볼프 1061c | 0.【76】 |  |

### E-en-132

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 8.06e+24, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `8.06×10²⁴ kg` (줄 25, 뒤): …the only known physical parameter for Ross 128 b is its minimum possible mass. The planet is at least 1.35 M🜨, or 1.35 times the mass of Earth (about 【8.06×10²⁴ kg】). This is slightly more massive than the similar and nearby Proxima Centauri b, with a minimum mass of 1.27 M🜨. The low mass of Ross 128 b implies th…
  - [Ross 128 b] raw `1.35 M🜨` (줄 25, 뒤): …being discovered by the radial velocity method, the only known physical parameter for Ross 128 b is its minimum possible mass. The planet is at least 【1.35 M🜨】, or 1.35 times the mass of Earth (about 8.06×10²⁴ kg). This is slightly more massive than the similar and nearby Proxima Centauri b, with a minimum m…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-133

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.04355e+09, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `1.5 R☉` (줄 19, 뒤): - Radius 【1.5 R☉】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-134

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 각도, base 70.74, 표 안 예, 시험 대상 밖 예
- 언급:
  - [TOI-2109 b] raw `70.74±0.37` (줄 49, 머리글): | b | 5.02±0.75 MJ | 0.01791±0.00065 | 0.67247414(28) | 0 | 【70.74±0.37】 | 1.347±0.047 RJ |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-135

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 733, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `733 K` (줄 57, 뒤): - If the atmosphere has a greenhouse effect similar in magnitude to the one on Venus, it would have an average surface temperature of 【733 K】 (460 °C).
  - [Kepler-22b] raw `460 °C` (줄 57, 뒤): - If the atmosphere has a greenhouse effect similar in magnitude to the one on Venus, it would have an average surface temperature of 733 K (【460 °C】).
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 712.15: [글리제 436 b] raw `섭씨 439도` (줄 35, 한쪽 언어 쪽): b가 어머니 항성 주위를 한 바퀴 도는 데에는 불과 39.5시간밖에 걸리지 않는다. 이 행성의 표면 온도는 대략 【섭씨 439도】이다. 이심률이 큰 궤도 때문에 받는 기조력으로 인해, 이 행성의 온도는 산술적인 계산치보다 더 높다. b의 주요 조성물은 높은 압력 하에서 존…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [센타우루스자리 프록시마 b] `460`: 모항성에서 프록시마 b까지의 거리는 0.05 AU(750만 km 또는 【460】만 마일)로 가깝다. b는 11.2 일을 1 주기로 프록시마를 공전하고 있으며 예상되는 b의 질량은 지구의 최소 1.3 배이다. 이 행성은 지구…

### E-en-136

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.21473e+11, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Kepler-22b] raw `0.812+0.011 −0.013 AU` (줄 8, 뒤):   - Semi-major axis: 【0.812+0.011 −0.013 AU】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.26709e+11: [HD 20367 b] raw `0.847` (줄 12, 한쪽 언어 쪽): - 근일점(AU): 【0.847】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-137

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 3192, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ross 128 b] raw `3192 K` (줄 33, 뒤): Ross 128 b orbits the small red dwarf star known as Ross 128. The star is 17% the mass and 20% the radius of that of the Sun. It has a temperature of 【3192 K】, a luminosity of 0.00362 L☉, and an age of 9.45±0.60 billion years. For comparison, the Sun has a temperature of 5772 K and age of 4.5 billion years,…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3273.15: [센타우루스자리 프록시마 b] raw `3000 °C` (줄 50, 한쪽 언어 쪽): …역 안에 있을 수 있는 까닭은 프록시마가 스펙트럼상 M형 별인 적색왜성이기 때문이다. 즉, 모항성인 프록시마의 온도가 낮기 때문에(표면온도 약 【3000 °C】) 이렇게 가까움에도 프록시마 b가 생명체 거주 가능 영역에 있을 수 있는 것이다. 태양 질량의 8분의 1 수준인 프록시마 주변의 생물권은 항성…
  - base 3311: [케플러-16b] raw `3311 K` (줄 48, 두 언어 쪽): … 걸쳐 공전한다. 항성의 질량은 각각 0.68 M☉ 및 0.20 M☉, 반지름은 0.64 R☉ 및 0.22 R☉, 표면 온도는 4450 K 및 【3311 K】, 광도는 태양의 14% 및 0.5%이다. 항성의 물리적 성질과 궤도 형태를 통해 추정한 항성계의 나이는 약 20억 년이다.
  - base 3042: [센타우루스자리 프록시마 b] raw `3042 켈빈` (줄 36, 한쪽 언어 쪽): 프록시마 b는 적색왜성 센타우루스자리 프록시마를 돌고 있다. 프록시마 항성의 질량은 태양의 12%이며 반지름은 14%이다. 표면 온도는 【3042 켈빈】이며 나이는 48억 5천만 년이다. 참고로 태양의 나이는 46억 년이며 표면 온도는 5778 켈빈이다. 센타우루스자리 프록시마의 1 자전주기는 …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### E-en-138

- 분야 exoplanets, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.57788e+15, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Zeta Leporis] raw `50` (줄 44, 뒤): …icity, is only 17% of the abundance in the Sun. The star appears to be young, probably around 231 million years in age, but the margin of error spans 【50】–347 million years old.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [목동자리 타우 b] `50`: 목동자리 타우 b 또는 목동자리 타우 Ab는 지구에서 목동자리 방향으로 【50】광년 떨어진 곳에 있는 외계 행성이다. 1996년 제오프리 마시와 폴 버틀러 팀은 목동자리 타우별 근처에 행성이 있음을 공표했다. 1999년 이…
  - [센타우루스자리 프록시마 b] `50`: …게 빛나던 별은 보이지 않을 것이다. 태양은 센타우루스자리 알파 계의 현재 적경 및 적위의 대척점인 적경 02ʰ 39ᵐ 35ˢ, 적위 +60° 【50】′(2000년 기준)에서 겉보기등급 +0.5의 노란색 별로 보일 것이다. 이 위치는 3.4 등성 카시오페이아자리 엡실론의 근처이며 심장 성운의 …

### R-ko-001

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 3.5916e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [디스프로슘] (같은 주제의 반대 언어 문서: Dysprosium) raw `359.16 pm` (줄 30, 뒤):   - 격자 상수: a = 【359.16 pm】 c = 565.01 pm (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-002

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 몰 에너지, base 247000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [툴륨] (같은 주제의 반대 언어 문서: Thulium) raw `247 kJ/mol` (줄 21, 뒤):   - 기화열: 【247 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [Dysprosium] `247`:   - Poisson ratio: 0.【247】
  - [Praseodymium] `247`: …Praseodymium is calculated to have a very large atomic radius; with a radius of 【247】 pm, barium, rubidium and caesium are larger. However, observationally, it is us…

### R-ko-003

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 2.22e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [툴륨] (같은 주제의 반대 언어 문서: Thulium) raw `222 pm` (줄 28, 뒤):   - 원자 반지름: 175 pm (실험값) 【222 pm】 (계산값)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.07e-10: [Lanthanum] raw `207±8 pm` (줄 31, 한쪽 언어 쪽):   - Covalent radius: 【207±8 pm】
  - base 2.03e-10: [Praseodymium] raw `203±7 pm` (줄 31, 한쪽 언어 쪽):   - Covalent radius: 【203±7 pm】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-004

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 압력, base 5.2e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [툴륨] (같은 주제의 반대 언어 문서: Thulium) raw `520 MPa` (줄 38, 뒤):   - 비커스 굳기: 【520 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 5e+08: [Dysprosium] raw `500` (줄 46, 두 언어 쪽):   - Brinell hardness: 【500】–1050 MPa
  - base 5.5e+08: [Dysprosium] raw `550 MPa` (줄 45, 두 언어 쪽):   - Vickers hardness: 410–【550 MPa】
  - base 4.7e+08: [Thulium] raw `470` (줄 44, 두 언어 쪽):   - Vickers hardness: 【470】–650 MPa
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-005

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 8.6e-06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `8.6(8) µs` (줄 75, 뒤): | ⁹⁹ᵐY | 2141.65(19) keV | 2141.65(19) keV | 2141.65(19) keV | 【8.6(8) µs】 |  |  | (17/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.2e-06: [Isotopes of yttrium] raw `8.2(4) μs` (줄 95, 두 언어 쪽): | ⁹⁹ᵐY | 2141.65(19) keV | 2141.65(19) keV | 2141.65(19) keV | 1985 | 【8.2(4) μs】 | IT | ⁹⁹Y | (17/2+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-006

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 7.6e-06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `7.6(4) µs` (줄 71, 뒤): | ⁹⁸ᵐ³Y | 496.19(15) keV | 496.19(15) keV | 496.19(15) keV | 【7.6(4) µs】 |  |  | (2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 8.2e-06: [Isotopes of yttrium] raw `8.2(4) μs` (줄 95, 두 언어 쪽): | ⁹⁹ᵐY | 2141.65(19) keV | 2141.65(19) keV | 2141.65(19) keV | 1985 | 【8.2(4) μs】 | IT | ⁹⁹Y | (17/2+) |  |
  - base 6.9e-06: [Isotopes of yttrium] raw `6.90(54) μs` (줄 89, 두 언어 쪽): | ⁹⁸ᵐ³Y | 496.10(11) keV | 496.10(11) keV | 496.10(11) keV | 2017 | 【6.90(54) μs】 | IT | ⁹⁸Y | (4)− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-007

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 에너지, base 6.56892e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 68, 뒤): | ⁹⁸ᵐ²Y | 【410(30) keV】 | 410(30) keV | 410(30) keV | 2.0(2) s | β⁻ (86.6%) | ⁹⁸Zr | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 68, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 【410(30) keV】 | 410(30) keV | 2.0(2) s | β⁻ (86.6%) | ⁹⁸Zr | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 68, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 410(30) keV | 【410(30) keV】 | 2.0(2) s | β⁻ (86.6%) | ⁹⁸Zr | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 69, 뒤): | ⁹⁸ᵐ²Y | 【410(30) keV】 | 410(30) keV | 410(30) keV | 2.0(2) s | IT (10%) | ⁹⁸Y | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 69, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 【410(30) keV】 | 410(30) keV | 2.0(2) s | IT (10%) | ⁹⁸Y | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 69, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 410(30) keV | 【410(30) keV】 | 2.0(2) s | IT (10%) | ⁹⁸Y | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 70, 뒤): | ⁹⁸ᵐ²Y | 【410(30) keV】 | 410(30) keV | 410(30) keV | 2.0(2) s | β⁻, n (3.4%) | ⁹⁷Zr | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 70, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 【410(30) keV】 | 410(30) keV | 2.0(2) s | β⁻, n (3.4%) | ⁹⁷Zr | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `410(30) keV` (줄 70, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 410(30) keV | 【410(30) keV】 | 2.0(2) s | β⁻, n (3.4%) | ⁹⁷Zr | (5+,4-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 6.45084e-14: [Isotopes of yttrium] raw `402.63(14) keV` (줄 35, 두 언어 쪽): | ⁸²ᵐ¹Y | 【402.63(14) keV】 | 402.63(14) keV | 402.63(14) keV | 1993 | 258(22) ns | IT | ⁸²Y | 4− |  |
  - base 6.29431e-14: [Isotopes of yttrium] raw `392.86(9) keV` (줄 55, 두 언어 쪽): | ⁸⁸ᵐ¹Y | 【392.86(9) keV】 | 392.86(9) keV | 392.86(9) keV | 1955 | 301(3) μs | IT | ⁸⁸Y | 1+ |  |
  - base 6.10141e-14: [Isotopes of yttrium] raw `380.82(7) keV` (줄 52, 두 언어 쪽): | ⁸⁷ᵐY | 【380.82(7) keV】 | 380.82(7) keV | 380.82(7) keV | 1940 | 13.37(3) h | IT (98.43%) | ⁸⁷Y | 9/2+ …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Dysprosium] `410`:   - Vickers hardness: 【410】–550 MPa

### R-ko-008

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 5.4846e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이터븀] (같은 주제의 반대 언어 문서: Ytterbium) raw `548.46 pm` (줄 31, 뒤):   - 격자 상수: a = 【548.46 pm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-009

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 3.5053e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [루테튬] (같은 주제의 반대 언어 문서: Lutetium) raw `350.53 pm` (줄 29, 뒤):   - 격자 상수: a = 【350.53 pm】 c = 554.93 pm (20 °C에서)
  - [툴륨] (같은 주제의 반대 언어 문서: Thulium) raw `353.77 pm` (줄 30, 뒤):   - 격자 상수: a = 【353.77 pm】 c = 555.39 pm (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-010

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 0.735, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `735(7) ms` (줄 76, 뒤): | ¹⁰⁰Y | 39 | 61 | 99.92776(8) | 【735(7) ms】 | β⁻ (98.98%) | ¹⁰⁰Zr | 1-,2- |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `735(7) ms` (줄 77, 뒤): | ¹⁰⁰Y | 39 | 61 | 99.92776(8) | 【735(7) ms】 | β⁻, n (1.02%) | ⁹⁹Zr | 1-,2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.727: [Isotopes of yttrium] raw `727(6) ms` (줄 98, 두 언어 쪽): | ¹⁰⁰ᵐY | 144(16) keV | 144(16) keV | 144(16) keV | 1977 | 【727(6) ms】 | β⁻ (98.92%) | ¹⁰⁰Zr | 1+# |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-011

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 2, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `2.0(2) s` (줄 68, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 410(30) keV | 410(30) keV | 【2.0(2) s】 | β⁻ (86.6%) | ⁹⁸Zr | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `2.0(2) s` (줄 69, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 410(30) keV | 410(30) keV | 【2.0(2) s】 | IT (10%) | ⁹⁸Y | (5+,4-) |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `2.0(2) s` (줄 70, 뒤): | ⁹⁸ᵐ²Y | 410(30) keV | 410(30) keV | 410(30) keV | 【2.0(2) s】 | β⁻, n (3.4%) | ⁹⁷Zr | (5+,4-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-012

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 5.6501e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [디스프로슘] (같은 주제의 반대 언어 문서: Dysprosium) raw `565.01 pm` (줄 30, 뒤):   - 격자 상수: a = 359.16 pm c = 【565.01 pm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-013

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 5.5493e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [루테튬] (같은 주제의 반대 언어 문서: Lutetium) raw `554.93 pm` (줄 29, 뒤):   - 격자 상수: a = 350.53 pm c = 【554.93 pm】 (20 °C에서)
  - [툴륨] (같은 주제의 반대 언어 문서: Thulium) raw `555.39 pm` (줄 30, 뒤):   - 격자 상수: a = 353.77 pm c = 【555.39 pm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-014

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 길이, base 2.28e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [디스프로슘] (같은 주제의 반대 언어 문서: Dysprosium) raw `228 pm` (줄 28, 뒤):   - 원자 반지름: 175 pm (실험값) 【228 pm】 (계산값)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.47e-10: [Praseodymium] raw `247 pm` (줄 62, 한쪽 언어 쪽): …Praseodymium is calculated to have a very large atomic radius; with a radius of 【247 pm】, barium, rubidium and caesium are larger. However, observationally, it is usual…
  - base 2.07e-10: [Lanthanum] raw `207±8 pm` (줄 31, 한쪽 언어 쪽):   - Covalent radius: 【207±8 pm】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [Isotopes of yttrium] `228`: | ⁸⁰ᵐ¹Y | 【228】.5(1) keV | 228.5(1) keV | 228.5(1) keV | 1998 | 4.8(3) s | IT (81%) | ⁸⁰Y | 1− …
  - [Isotopes of yttrium] `228`: | ⁸⁰ᵐ¹Y | 228.5(1) keV | 【228】.5(1) keV | 228.5(1) keV | 1998 | 4.8(3) s | IT (81%) | ⁸⁰Y | 1− |  |
  - [Isotopes of yttrium] `228`: | ⁸⁰ᵐ¹Y | 228.5(1) keV | 228.5(1) keV | 【228】.5(1) keV | 1998 | 4.8(3) s | IT (81%) | ⁸⁰Y | 1− |  |
  - [Isotopes of yttrium] `228`: | ⁸⁰ᵐ¹Y | 【228】.5(1) keV | 228.5(1) keV | 228.5(1) keV | 1998 | 4.8(3) s | β⁺ (19%) | ⁸⁰Sr | 1−…
  - [Isotopes of yttrium] `228`: | ⁸⁰ᵐ¹Y | 228.5(1) keV | 【228】.5(1) keV | 228.5(1) keV | 1998 | 4.8(3) s | β⁺ (19%) | ⁸⁰Sr | 1− |  |

### R-ko-015

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 에너지, base 1.82648e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `1140(30) keV` (줄 58, 뒤): | ⁹⁶ᵐY | 【1140(30) keV】 | 1140(30) keV | 1140(30) keV | 9.6(2) s | β⁻ | ⁹⁶Zr | (8)+ |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `1140(30) keV` (줄 58, 뒤): | ⁹⁶ᵐY | 1140(30) keV | 【1140(30) keV】 | 1140(30) keV | 9.6(2) s | β⁻ | ⁹⁶Zr | (8)+ |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `1140(30) keV` (줄 58, 뒤): | ⁹⁶ᵐY | 1140(30) keV | 1140(30) keV | 【1140(30) keV】 | 9.6(2) s | β⁻ | ⁹⁶Zr | (8)+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1.89297e-13: [Isotopes of yttrium] raw `1181.50(18) keV` (줄 92, 두 언어 쪽): | ⁹⁸ᵐ⁶Y | 【1181.50(18) keV】 | 1181.50(18) keV | 1181.50(18) keV | 2017 | 762(14) ns | IT | ⁹⁸Y | (10−) |  |
  - base 1.74253e-13: [Isotopes of yttrium] raw `1087.6(6) keV` (줄 72, 두 언어 쪽): | ⁹⁵ᵐY | 【1087.6(6) keV】 | 1087.6(6) keV | 1087.6(6) keV | 1982 | 48.6(5) μs | IT | ⁹⁵Y | 9/2+ |  |
  - base 1.9263e-13: [Isotopes of yttrium] raw `1202.3(10) keV` (줄 70, 두 언어 쪽): | ⁹⁴ᵐY | 【1202.3(10) keV】 | 1202.3(10) keV | 1202.3(10) keV | 1999 | 1.304(12) μs | IT | ⁹⁴Y | (5+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-016

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 6879.6, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이터븀] (같은 주제의 반대 언어 문서: Ytterbium) raw `1.911 h` (줄 49, 뒤): …6 d ε 0.909 ¹⁶⁹Tm ¹⁷⁰Yb 3.05% 안정 ¹⁷¹Yb 14.3% 안정 ¹⁷²Yb 21.9% 안정 ¹⁷³Yb 16.12% 안정 ¹⁷⁴Yb 31.8% 안정 ¹⁷⁵Yb 인공 4.185 d β⁻ 0.470 ¹⁷⁵Lu ¹⁷⁶Yb 12.7% 안정 ¹⁷⁷Yb 인공 【1.911 h】 β⁻ 1.399 ¹⁷⁷Lu
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 7200: [Ytterbium] raw `2 hours` (줄 100, 두 언어 쪽): …s. All of the remaining radioactive isotopes have half-lives that are less than 【2 hours】, with the majority of them being less than 20 minutes. This element also has 18…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-017

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 2.68e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `268(25) ns` (줄 23, 뒤): | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 【268(25) ns】 |  |  | 4- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.58e-07: [Isotopes of yttrium] raw `258(22) ns` (줄 35, 두 언어 쪽): | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 1993 | 【258(22) ns】 | IT | ⁸²Y | 4− |  |
  - base 2.92e-07: [Isotopes of yttrium] raw `292(10) ns` (줄 42, 두 언어 쪽): | ⁸⁴ᵐ²Y | 210.42(16) keV | 210.42(16) keV | 210.42(16) keV | 2005 | 【292(10) ns】 | IT | ⁸⁴Y | 4− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-018

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 8.3e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `0.83(10) µs` (줄 72, 뒤): | ⁹⁸ᵐ⁴Y | 1181.1(4) keV | 1181.1(4) keV | 1181.1(4) keV | 【0.83(10) µs】 |  |  | (8-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 8.7e-07: [Isotopes of yttrium] raw `870(90) ns` (줄 102, 두 언어 쪽): | ¹⁰¹ᵐY | 1205.0(10) keV | 1205.0(10) keV | 1205.0(10) keV | 2009 | 【870(90) ns】 | IT | ¹⁰¹Y | 13/2−# |  |
  - base 7.62e-07: [Isotopes of yttrium] raw `762(14) ns` (줄 92, 두 언어 쪽): | ⁹⁸ᵐ⁶Y | 1181.50(18) keV | 1181.50(18) keV | 1181.50(18) keV | 2017 | 【762(14) ns】 | IT | ⁹⁸Y | (10−) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-019

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 몰 에너지, base 159000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이터븀] (같은 주제의 반대 언어 문서: Ytterbium) raw `159 kJ/mol` (줄 21, 뒤):   - 기화열: 【159 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 176000: [Europium] raw `176 kJ/mol` (줄 22, 한쪽 언어 쪽):   - Heat of vaporization: 【176 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-020

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 압력, base 5.4e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [디스프로슘] (같은 주제의 반대 언어 문서: Dysprosium) raw `540 MPa` (줄 40, 뒤):   - 비커스 굳기: 【540 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 5.5e+08: [Dysprosium] raw `550 MPa` (줄 45, 두 언어 쪽):   - Vickers hardness: 410–【550 MPa】
  - base 5e+08: [Dysprosium] raw `500` (줄 46, 두 언어 쪽):   - Brinell hardness: 【500】–1050 MPa
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-021

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 11484, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `3.19(6) h` (줄 47, 뒤): | ⁹⁰ᵐY | 681.67(10) keV | 681.67(10) keV | 681.67(10) keV | 【3.19(6) h】 | IT (99.99%) | ⁹⁰Y | 7+ |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `3.19(6) h` (줄 48, 뒤): | ⁹⁰ᵐY | 681.67(10) keV | 681.67(10) keV | 681.67(10) keV | 【3.19(6) h】 | β⁻ (.0018%) | ⁹⁰Zr | 7+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 11613.6: [Isotopes of yttrium] raw `3.226(11) h` (줄 60, 두 언어 쪽): | ⁹⁰ᵐY | 682.01(5) keV | 682.01(5) keV | 682.01(5) keV | 1961 | 【3.226(11) h】 | IT | ⁹⁰Y | 7+ |  |
  - base 12744: [Isotopes of yttrium] raw `3.54(1) h` (줄 65, 두 언어 쪽): | ⁹²Y | 39 | 53 | 91.9089458(98) | 1940 | 【3.54(1) h】 | β⁻ | ⁹²Zr | 2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-022

- 분야 rare_earth, 언어 ko, 쪽 두 언어 쪽, dim 시간, base 0.224, 표 안 예, 시험 대상 밖 예
- 언급:
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `224(19) ms` (줄 85, 뒤): | ¹⁰³Y | 39 | 64 | 102.93673(32)# | 【224(19) ms】 | β⁻ (91.7%) | ¹⁰³Zr | 5/2+# |  |  |
  - [이트륨 동위 원소] (같은 주제의 반대 언어 문서: Isotopes of yttrium) raw `224(19) ms` (줄 86, 뒤): | ¹⁰³Y | 39 | 64 | 102.93673(32)# | 【224(19) ms】 | β⁻, n (8.3%) | ¹⁰²Zr | 5/2+# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.239: [Isotopes of yttrium] raw `239(12) ms` (줄 108, 두 언어 쪽): | ¹⁰³Y | 39 | 64 | 102.937244(12) | 1994 | 【239(12) ms】 | β⁻ (92.0%) | ¹⁰³Zr | 5/2+# |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-023

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 8.10701e-15, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `50.6(9) keV` (줄 42, 뒤): | ¹⁴⁷ᵐTb | 【50.6(9) keV】 | 50.6(9) keV | 50.6(9) keV | 1.87(5) min | β⁺ | ¹⁴⁷Gd | (11/2)- |  |  |
  - [터븀 동위 원소] raw `50.6(9) keV` (줄 42, 뒤): | ¹⁴⁷ᵐTb | 50.6(9) keV | 【50.6(9) keV】 | 50.6(9) keV | 1.87(5) min | β⁺ | ¹⁴⁷Gd | (11/2)- |  |  |
  - [터븀 동위 원소] raw `50.6(9) keV` (줄 42, 뒤): | ¹⁴⁷ᵐTb | 50.6(9) keV | 50.6(9) keV | 【50.6(9) keV】 | 1.87(5) min | β⁺ | ¹⁴⁷Gd | (11/2)- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-024

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1170, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `19.5(3) min` (줄 88, 뒤): | ¹⁶³Tb | 65 | 98 | 162.930648(5) | 【19.5(3) min】 | β⁻ | ¹⁶³Dy | 3/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1200: [Ytterbium] raw `20 minutes` (줄 100, 두 언어 쪽): …alf-lives that are less than 2 hours, with the majority of them being less than 【20 minutes】. This element also has 18 meta states, with the most stable being ¹⁶⁹ᵐYb (half-…
  - base 1122: [Isotopes of yttrium] raw `18.7(1) min` (줄 69, 두 언어 쪽): | ⁹⁴Y | 39 | 55 | 93.9115921(68) | 1948 | 【18.7(1) min】 | β⁻ | ⁹⁴Zr | 2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-025

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 2.56e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `25.6 GPa` (줄 36, 뒤):   - 전단 탄성 계수: 【25.6 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 2.47e+10: [Dysprosium] raw `24.7 GPa` (줄 41, 두 언어 쪽):   - Shear modulus: 【24.7 GPa】
  - base 2.72e+10: [Lutetium] raw `27.2 GPa` (줄 40, 두 언어 쪽):   - Shear modulus: 【27.2 GPa】
  - base 2.39e+10: [Ytterbium] raw `23.9 GPa` (줄 40, 두 언어 쪽):   - Young's modulus: β form: 【23.9 GPa】
  - base 2.79e+10: [Lanthanum] raw `27.9 GPa` (줄 42, 한쪽 언어 쪽):   - Bulk modulus: α form: 【27.9 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-026

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 0.00118, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `1.18(2) ms` (줄 40, 뒤): | ¹⁴⁶ᵐ²Tb | 930(100)# keV | 930(100)# keV | 930(100)# keV | 【1.18(2) ms】 |  |  | (10+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-027

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 3.34511e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `1.06×10¹¹y` (줄 48, 뒤):   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁴⁴Sm 3.07% 안정 ¹⁴⁶Sm 인공 1.03×10⁸y α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 【1.06×10¹¹y】 α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α 1.986 ¹⁴⁴Nd ¹⁴⁹Sm 13.82% >2×10¹⁵ y α 1.870 ¹⁴⁵Nd ¹⁵⁰Sm 7.38% 안정 ¹⁵²Sm 26.75% 안정 ¹⁵⁴Sm 22.75% 안정
  - [사마륨] raw `1.06×10¹¹년` (줄 73, 뒤): … 동위 원소(¹⁴⁴Sm, ¹⁵⁰Sm, ¹⁵²Sm, ¹⁵⁴Sm)와 세 개의 방사성 동위 원소(¹⁴⁷Sm, ¹⁴⁸Sm, ¹⁴⁹Sm)가 존재하며, 이 중 가장 많이 존재하는 것은 ¹⁵²Sm이다. 방사성 동위 원소 세 가지는 모두 반감기가 매우 긴 편이며(¹⁴⁷Sm은 반감기 【1.06×10¹¹년】, ¹⁴⁸Sm은 반감기 7×10¹⁵년)이며, 이들 중 ¹⁴⁹Sm은 자료에 따라 반감기 2×10¹⁵년 이상인 방사성 동위 원소로 분류되기도 하고 안정한 동위 원소로 분류되기도 한다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.25043e+18: [Lanthanum] raw `1.03×10¹¹ y` (줄 53, 한쪽 언어 쪽): … half-life (t1/2) mode pro­duct ¹³⁷La synth 6×10⁴ y ε ¹³⁷Ba ¹³⁸La 0.0889999999% 【1.03×10¹¹ y】 β⁺ ¹³⁸Ba β⁻ ¹³⁸Ce ¹³⁹La 99.911% stable ¹⁴⁰La synth 40.289 h β⁻ ¹⁴⁰Ce
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-028

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 6220.8, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `1.728(1) h` (줄 54, 뒤): | ¹⁴⁹Nd | 60 | 89 | 148.920149(3) | 【1.728(1) h】 | β⁻ | ¹⁴⁸Pm | 5/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5760: [Europium] raw `96 minutes` (줄 163, 한쪽 언어 쪽): … of 9.3116 hours; another isomer of ¹⁵²Eu at 147.9 keV has a half-life of about 【96 minutes】. Most neutron-deficient europium isotopes decay towards isotopes of samarium by…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-029

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 19080, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `5.3(2) h` (줄 76, 뒤): | ¹⁵⁶ᵐ²Tb | 88.4(2) keV | 88.4(2) keV | 88.4(2) keV | 【5.3(2) h】 |  |  | (0+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 17496: [Isotopes of yttrium] raw `4.86(20) h` (줄 44, 두 언어 쪽): | ⁸⁵ᵐ¹Y | 19.68(17) keV | 19.68(17) keV | 19.68(17) keV | 1963 | 【4.86(20) h】 | β⁺ | ⁸⁵Sr | (9/2)+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-030

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 132, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `2.20(5) min` (줄 44, 뒤): | ¹⁴⁸ᵐ¹Tb | 90.1(3) keV | 90.1(3) keV | 90.1(3) keV | 【2.20(5) min】 | β⁺ | ¹⁴⁸Gd | (9)+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-031

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 밀도, base 8860, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `8.86 g/cm³` (줄 19, 뒤):   - 액체(녹는점)일 때: 【8.86 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 8550: [Dysprosium] raw `8.550 g/cm³` (줄 19, 두 언어 쪽):   - Density (at 20° C): 【8.550 g/cm³】
  - base 9300: [Lutetium] raw `9.3 g/cm³` (줄 20, 두 언어 쪽):   - when liquid (at m.p.): 【9.3 g/cm³】
  - base 8370: [Dysprosium] raw `8.37 g/cm³` (줄 20, 두 언어 쪽):   - when liquid (at m.p.): 【8.37 g/cm³】
  - base 9810: [Lutetium] raw `9.81 g/cm³` (줄 116, 두 언어 쪽): Lutetium tantalate (LuTaO4) is the densest known stable white material (density 【9.81 g/cm³】) and therefore is an ideal host for X-ray phosphors. The only denser white mate…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-032

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 5.89e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `589 MPa` (줄 39, 뒤):   - 비커스 굳기: 【589 MPa】
  - [이트륨] raw `589 MPa` (줄 40, 뒤):   - 브리넬 굳기: 【589 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 5.5e+08: [Dysprosium] raw `550 MPa` (줄 45, 두 언어 쪽):   - Vickers hardness: 410–【550 MPa】
  - base 6.4e+08: [Praseodymium] raw `640 MPa` (줄 46, 한쪽 언어 쪽):   - Brinell hardness: 250–【640 MPa】
  - base 6.5e+08: [Thulium] raw `650 MPa` (줄 44, 두 언어 쪽):   - Vickers hardness: 470–【650 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-033

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 2.61435e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `163.175(5) keV` (줄 64, 뒤): | ¹⁵³ᵐTb | 【163.175(5) keV】 | 163.175(5) keV | 163.175(5) keV | 186(4) µs |  |  | 11/2- |  |  |
  - [터븀 동위 원소] raw `163.175(5) keV` (줄 64, 뒤): | ¹⁵³ᵐTb | 163.175(5) keV | 【163.175(5) keV】 | 163.175(5) keV | 186(4) µs |  |  | 11/2- |  |  |
  - [터븀 동위 원소] raw `163.175(5) keV` (줄 64, 뒤): | ¹⁵³ᵐTb | 163.175(5) keV | 163.175(5) keV | 【163.175(5) keV】 | 186(4) µs |  |  | 11/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.7362e-14: [Isotopes of yttrium] raw `170.78(5) keV` (줄 85, 두 언어 쪽): | ⁹⁸ᵐ¹Y | 【170.78(5) keV】 | 170.78(5) keV | 170.78(5) keV | 2017 | 615(8) ns | IT | ⁹⁸Y | 2− |  |
  - base 2.36962e-14: [Europium] raw `147.9 keV` (줄 163, 한쪽 언어 쪽): …ours, and ¹⁵²ᵐ¹Eu, with a half-life of 9.3116 hours; another isomer of ¹⁵²Eu at 【147.9 keV】 has a half-life of about 96 minutes. Most neutron-deficient europium isotopes d…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-034

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 1.95e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `19.5 GPa` (줄 36, 뒤):   - 전단 탄성 계수: (α form) 【19.5 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.82e+10: [Europium] raw `18.2 GPa` (줄 40, 한쪽 언어 쪽):   - Young's modulus: 【18.2 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-035

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 5.7317e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `573.17 pm` (줄 30, 뒤):   - 격자 상수: a = 364.83 pm c = 【573.17 pm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-036

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 2.16134e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `1349(10) keV` (줄 61, 뒤): | ¹⁵⁴ᵐ²Nd | 【1349(10) keV】 | 1349(10) keV | 1349(10) keV | >1 µs |  |  | (5-) |  |  |
  - [네오디뮴 동위 원소] raw `1349(10) keV` (줄 61, 뒤): | ¹⁵⁴ᵐ²Nd | 1349(10) keV | 【1349(10) keV】 | 1349(10) keV | >1 µs |  |  | (5-) |  |  |
  - [네오디뮴 동위 원소] raw `1349(10) keV` (줄 61, 뒤): | ¹⁵⁴ᵐ²Nd | 1349(10) keV | 1349(10) keV | 【1349(10) keV】 | >1 µs |  |  | (5-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-037

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 비저항, base 5.96e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `596 n Ω·m` (줄 33, 뒤):   - 전기 저항도: (실온) (α, poly) 【596 n Ω·m】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 5.82e-07: [Lutetium] raw `582 nΩ⋅m` (줄 37, 두 언어 쪽):   - Electrical resistivity: poly: 【582 nΩ⋅m】 (at r.t.)
  - base 6.15e-07: [Lanthanum] raw `615 nΩ⋅m` (줄 37, 한쪽 언어 쪽):   - Electrical resistivity: α, poly: 【615 nΩ⋅m】 (at r.t.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Thulium] `596`:   - Ionization energies: 1st: 【596】.7 kJ/mol, 2nd: 1160 kJ/mol, 3rd: 2285 kJ/mol

### R-ko-038

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 9.6e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `0.96 µs` (줄 60, 뒤): | ¹⁵²ᵐ¹Tb | 342.15(16) keV | 342.15(16) keV | 342.15(16) keV | 【0.96 µs】 |  |  | 5- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.7e-07: [Isotopes of yttrium] raw `870(90) ns` (줄 102, 두 언어 쪽): | ¹⁰¹ᵐY | 1205.0(10) keV | 1205.0(10) keV | 1205.0(10) keV | 2009 | 【870(90) ns】 | IT | ¹⁰¹Y | 13/2−# |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-039

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 25.9, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `25.9(2) s` (줄 59, 뒤): | ¹⁵⁴Nd | 60 | 94 | 153.92948(12) | 【25.9(2) s】 | β⁻ | ¹⁵⁴Pm | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-040

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 열팽창, base 1.22e-05, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `12.2 µm/(m·K)` (줄 31, 뒤):   - 열팽창: (실온) (poly) 【12.2 µm/(m·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.33e-05: [Thulium] raw `13.3 µm/(m⋅K)` (줄 35, 두 언어 쪽):   - Thermal expansion: poly: 【13.3 µm/(m⋅K)】 (at r.t.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-041

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 11420, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `11.42 kJ/mol` (줄 20, 뒤):   - 융해열: 【11.42 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 11060: [Dysprosium] raw `11.06 kJ/mol` (줄 21, 두 언어 쪽):   - Heat of fusion: 【11.06 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-042

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 1.38085e-12, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `8618.6(10) keV` (줄 45, 뒤): | ¹⁴⁸ᵐ²Tb | 【8618.6(10) keV】 | 8618.6(10) keV | 8618.6(10) keV | 1.310(7) µs |  |  | (27+) |  |  |
  - [터븀 동위 원소] raw `8618.6(10) keV` (줄 45, 뒤): | ¹⁴⁸ᵐ²Tb | 8618.6(10) keV | 【8618.6(10) keV】 | 8618.6(10) keV | 1.310(7) µs |  |  | (27+) |  |  |
  - [터븀 동위 원소] raw `8618.6(10) keV` (줄 45, 뒤): | ¹⁴⁸ᵐ²Tb | 8618.6(10) keV | 8618.6(10) keV | 【8618.6(10) keV】 | 1.310(7) µs |  |  | (27+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.27213e-12: [Neutron capture therapy of cancer] raw `7.94 MeV` (줄 75, 한쪽 언어 쪽): …¹⁵⁷Gd(n,γ)¹⁵⁸Gd capture reaction (¹⁵⁷Gd + nth (0.025eV) → [¹⁵⁸Gd] → ¹⁵⁸Gd + γ + 【7.94 MeV】). Though the gamma rays have longer pathlengths, orders of magnitude greater de…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-043

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 9.95593e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `621.4(11) keV` (줄 25, 뒤): | ¹⁴²ᵐ²Tb | 【621.4(11) keV】 | 621.4(11) keV | 621.4(11) keV | 15(4) µs |  |  |  |  |  |
  - [터븀 동위 원소] raw `621.4(11) keV` (줄 25, 뒤): | ¹⁴²ᵐ²Tb | 621.4(11) keV | 【621.4(11) keV】 | 621.4(11) keV | 15(4) µs |  |  |  |  |  |
  - [터븀 동위 원소] raw `621.4(11) keV` (줄 25, 뒤): | ¹⁴²ᵐ²Tb | 621.4(11) keV | 621.4(11) keV | 【621.4(11) keV】 | 15(4) µs |  |  |  |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 9.51693e-14: [Isotopes of yttrium] raw `594(10) keV` (줄 90, 두 언어 쪽): | ⁹⁸ᵐ⁴Y | 【594(10) keV】 | 594(10) keV | 594(10) keV | 2017 | 180(7) ns | IT | ⁹⁸Y | (3−,4−) |  |
  - base 1.06948e-13: [Isotopes of yttrium] raw `667.52(23) keV` (줄 78, 두 언어 쪽): | ⁹⁷ᵐ¹Y | 【667.52(23) keV】 | 667.52(23) keV | 667.52(23) keV | 1978 | 1.17(3) s | β⁻ (>99.2%) | ⁹⁷Zr | 9/2…
  - base 1.08075e-13: [Isotopes of yttrium] raw `674.55(4) keV` (줄 56, 두 언어 쪽): | ⁸⁸ᵐ²Y | 【674.55(4) keV】 | 674.55(4) keV | 674.55(4) keV | 1962 | 13.98(17) ms | IT | ⁸⁸Y | 8+ |  |
  - base 1.0927e-13: [Isotopes of yttrium] raw `682.01(5) keV` (줄 60, 두 언어 쪽): | ⁹⁰ᵐY | 【682.01(5) keV】 | 682.01(5) keV | 682.01(5) keV | 1961 | 3.226(11) h | IT | ⁹⁰Y | 7+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-044

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 596160, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `6.9일` (줄 2, 뒤): 자연계에 존재하는 터븀 혹은 테르븀의 동위 원소는 1종으로 ¹⁵⁹Tb이 100% 존재한다. 우라늄과 토륨의 자발 핵분열로 생성되는 생성되는 ¹⁶¹Tb은 반감기가 【6.9일】로 자연계에 미량 존재한다.
  - [터븀 동위 원소] raw `6.906(19) d` (줄 86, 뒤): | ¹⁶¹Tb | 65 | 96 | 160.9275699(28) | 【6.906(19) d】 | β⁻ | ¹⁶¹Dy | 3/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 604800: [Lutetium] raw `7 days` (줄 126, 두 언어 쪽): …¹⁷⁷Lu emits low-energy beta particles and gamma rays and has a half-life around 【7 days】, positive characteristics for commercial applications, especially in therapeuti…
  - base 574068: [Lutetium] raw `6.6443 d` (줄 52, 두 언어 쪽): …⁷⁴Yb ¹⁷⁵Lu 97.4009999999% stable ¹⁷⁶Lu 2.599% 3.701×10¹⁰ y β⁻ ¹⁷⁶Hf ¹⁷⁷Lu synth 【6.6443 d】 β⁻ ¹⁷⁷Hf
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-045

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 126.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `2.11(10) min` (줄 90, 뒤): | ¹⁶⁵Tb | 65 | 100 | 164.93488(21)# | 【2.11(10) min】 | β⁻ | ¹⁶⁵ᵐDy | 3/2+# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-046

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 5.08675e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `3174.9(4) keV` (줄 37, 뒤): | ¹³⁸ᵐNd | 【3174.9(4) keV】 | 3174.9(4) keV | 3174.9(4) keV | 410(50) ns |  |  | (10+) |  |  |
  - [네오디뮴 동위 원소] raw `3174.9(4) keV` (줄 37, 뒤): | ¹³⁸ᵐNd | 3174.9(4) keV | 【3174.9(4) keV】 | 3174.9(4) keV | 410(50) ns |  |  | (10+) |  |  |
  - [네오디뮴 동위 원소] raw `3174.9(4) keV` (줄 37, 뒤): | ¹³⁸ᵐNd | 3174.9(4) keV | 3174.9(4) keV | 【3174.9(4) keV】 | 410(50) ns |  |  | (10+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.80653e-13: [Neutron capture therapy of cancer] raw `3.0 MeV` (줄 180, 한쪽 언어 쪽): … lithium-7 reaction requires a proton accelerator with energies between 1.9 and 【3.0 MeV】, while the beryllium-9 reaction typically uses accelerators with energies betwe…
  - base 5.64383e-13: [Isotopes of yttrium] raw `3522.6(4) keV` (줄 81, 두 언어 쪽): | ⁹⁷ᵐ²Y | 【3522.6(4) keV】 | 3522.6(4) keV | 3522.6(4) keV | 1986 | 142(8) ms | IT (94.8%) | ⁹⁷Y | (27/2−)…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-047

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 6.22237e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `388.37(15) keV` (줄 83, 뒤): | ¹⁵⁸ᵐ²Tb | 【388.37(15) keV】 | 388.37(15) keV | 388.37(15) keV | 0.40(4) ms |  |  | 7- |  |  |
  - [터븀 동위 원소] raw `388.37(15) keV` (줄 83, 뒤): | ¹⁵⁸ᵐ²Tb | 388.37(15) keV | 【388.37(15) keV】 | 388.37(15) keV | 0.40(4) ms |  |  | 7- |  |  |
  - [터븀 동위 원소] raw `388.37(15) keV` (줄 83, 뒤): | ¹⁵⁸ᵐ²Tb | 388.37(15) keV | 388.37(15) keV | 【388.37(15) keV】 | 0.40(4) ms |  |  | 7- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 6.29431e-14: [Isotopes of yttrium] raw `392.86(9) keV` (줄 55, 두 언어 쪽): | ⁸⁸ᵐ¹Y | 【392.86(9) keV】 | 392.86(9) keV | 392.86(9) keV | 1955 | 301(3) μs | IT | ⁸⁸Y | 1+ |  |
  - base 6.10141e-14: [Isotopes of yttrium] raw `380.82(7) keV` (줄 52, 두 언어 쪽): | ⁸⁷ᵐY | 【380.82(7) keV】 | 380.82(7) keV | 380.82(7) keV | 1940 | 13.37(3) h | IT (98.43%) | ⁸⁷Y | 9/2+ …
  - base 6.45084e-14: [Isotopes of yttrium] raw `402.63(14) keV` (줄 35, 두 언어 쪽): | ⁸²ᵐ¹Y | 【402.63(14) keV】 | 402.63(14) keV | 402.63(14) keV | 1993 | 258(22) ns | IT | ⁸²Y | 4− |  |
  - base 5.60762e-14: [Ytterbium] raw `350 keV` (줄 154, 두 언어 쪽): …e roughly equivalent to those taken with X-rays having energies between 250 and 【350 keV】. ¹⁶⁹Yb is also used in nuclear medicine.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-048

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 5.13e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `513(42) ns` (줄 71, 뒤): | ¹⁵⁴ᵐ³Tb | 0+Z keV | 0+Z keV | 0+Z keV | 【513(42) ns】 |  |  |  |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-049

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 0.0006, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `600(50) µs` (줄 43, 뒤): | ¹⁴⁰ᵐNd | 2221.4(1) keV | 2221.4(1) keV | 2221.4(1) keV | 【600(50) µs】 |  |  | 7- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [Thulium] `600`: …rades of 99 % and 99.9 % purity. The price per kilogram oscillated between US$4,【600】 and $13,300 in the period from 1959 to 1998 for 99.9 % purity, and it was the s…
  - [Europium] `600`: …ide, EuN, can be prepared by direct reaction of the metal with ammonia at about 【600】 °C and crystallizes in the cubic rock-salt structure. Europium phosphide, EuP, …
  - [Europium] `600`: … hexagonal rhabdophane structure; after dehydration at temperatures above about 【600】 °C it transforms to monoclinic anhydrous EuPO4, which is isostructural with mon…

### R-ko-050

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 166680, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `46.3시간` (줄 101, 뒤): - 방사성 동위 원소인 사마륨-153은 반감기 【46.3시간】을 거쳐 베타 붕괴하므로 화합물의 형태로 만들어져 각종 암의 치료제로 쓰이기도 한다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-051

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 3.70343e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 39, 뒤): | ¹³⁹ᵐ¹Nd | 【231.15(5) keV】 | 231.15(5) keV | 231.15(5) keV | 5.50(20) h | β⁺ (88.2%) | ¹³⁹Pr | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 39, 뒤): | ¹³⁹ᵐ¹Nd | 231.15(5) keV | 【231.15(5) keV】 | 231.15(5) keV | 5.50(20) h | β⁺ (88.2%) | ¹³⁹Pr | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 39, 뒤): | ¹³⁹ᵐ¹Nd | 231.15(5) keV | 231.15(5) keV | 【231.15(5) keV】 | 5.50(20) h | β⁺ (88.2%) | ¹³⁹Pr | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 40, 뒤): | ¹³⁹ᵐ¹Nd | 【231.15(5) keV】 | 231.15(5) keV | 231.15(5) keV | 5.50(20) h | IT (11.8%) | ¹³⁹Nd | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 40, 뒤): | ¹³⁹ᵐ¹Nd | 231.15(5) keV | 【231.15(5) keV】 | 231.15(5) keV | 5.50(20) h | IT (11.8%) | ¹³⁹Nd | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 40, 뒤): | ¹³⁹ᵐ¹Nd | 231.15(5) keV | 231.15(5) keV | 【231.15(5) keV】 | 5.50(20) h | IT (11.8%) | ¹³⁹Nd | 11/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 3.66097e-14: [Isotopes of yttrium] raw `228.5(1) keV` (줄 30, 두 언어 쪽): | ⁸⁰ᵐ¹Y | 【228.5(1) keV】 | 228.5(1) keV | 228.5(1) keV | 1998 | 4.8(3) s | IT (81%) | ⁸⁰Y | 1− |  |
  - base 3.49611e-14: [Isotopes of yttrium] raw `218.21(9) keV` (줄 48, 두 언어 쪽): | ⁸⁶ᵐ¹Y | 【218.21(9) keV】 | 218.21(9) keV | 218.21(9) keV | 1961 | 47.4(4) min | IT (99.31%) | ⁸⁶Y | (8+)…
  - base 4.00544e-14: [Ytterbium] raw `250` (줄 154, 두 언어 쪽): …ource are roughly equivalent to those taken with X-rays having energies between 【250】 and 350 keV. ¹⁶⁹Yb is also used in nuclear medicine.
  - base 3.3713e-14: [Isotopes of yttrium] raw `210.42(16) keV` (줄 42, 두 언어 쪽): | ⁸⁴ᵐ²Y | 【210.42(16) keV】 | 210.42(16) keV | 210.42(16) keV | 2005 | 292(10) ns | IT | ⁸⁴Y | 4− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-052

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 2.4, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `2.4(2) s` (줄 17, 뒤): | ¹⁴⁰Tb | 65 | 75 | 139.94581(86) | 【2.4(2) s】 | β⁺ (99.74%) | ¹⁴⁰Gd | 5 |  |  |
  - [터븀 동위 원소] raw `2.4(2) s` (줄 18, 뒤): | ¹⁴⁰Tb | 65 | 75 | 139.94581(86) | 【2.4(2) s】 | β⁺, p (0.26%) | ¹³⁹Eu | 5 |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.32: [Isotopes of yttrium] raw `2.32(8) s` (줄 86, 두 언어 쪽): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 465.7(7) keV | 1977 | 【2.32(8) s】 | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-053

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 19800, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `5.50(20) h` (줄 39, 뒤): | ¹³⁹ᵐ¹Nd | 231.15(5) keV | 231.15(5) keV | 231.15(5) keV | 【5.50(20) h】 | β⁺ (88.2%) | ¹³⁹Pr | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `5.50(20) h` (줄 40, 뒤): | ¹³⁹ᵐ¹Nd | 231.15(5) keV | 231.15(5) keV | 231.15(5) keV | 【5.50(20) h】 | IT (11.8%) | ¹³⁹Nd | 11/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 21600: [Neutron capture therapy of cancer] raw `6 hours` (줄 158, 한쪽 언어 쪽): …unt of BPA administered was increased (900 mg/kg), and it was infused i.v. over 【6 hours】. This was based on experimental animal studies in glioma-bearing rats demonstra…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-054

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 3609, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `3609 K` (줄 17, 뒤):   - 끓는점: 【3609 K】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3675: [Lutetium] raw `3675 K` (줄 18, 두 언어 쪽):   - Boiling point: 【3675 K】 ​(3402 °C, ​6156 °F)
  - base 3737: [Lanthanum] raw `3737 K` (줄 18, 한쪽 언어 쪽):   - Boiling point: 【3737 K】 ​(3464 °C, ​6267 °F)
  - base 3403: [Praseodymium] raw `3403 K` (줄 18, 한쪽 언어 쪽):   - Boiling point: 【3403 K】 ​(3130 °C, ​5666 °F)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-055

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 8.14e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `814 MPa` (줄 40, 뒤):   - 브리넬 굳기: 【814 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 7.55e+08: [Lutetium] raw `755` (줄 43, 두 언어 쪽):   - Vickers hardness: 【755】–1160 MPa
  - base 7.45e+08: [Praseodymium] raw `745 MPa` (줄 45, 한쪽 언어 쪽):   - Vickers hardness: 250–【745 MPa】
  - base 8.9e+08: [Lutetium] raw `890` (줄 44, 두 언어 쪽):   - Brinell hardness: 【890】–1300 MPa
  - base 9e+08: [Thulium] raw `900 MPa` (줄 45, 두 언어 쪽):   - Brinell hardness: 470–【900 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-056

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 2310, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `38.5(15) min` (줄 34, 뒤): | ¹³⁷Nd | 60 | 77 | 136.914567(12) | 【38.5(15) min】 | β⁺ | ¹³⁷Pr | 1/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2370: [Isotopes of yttrium] raw `39.5(8) min` (줄 40, 두 언어 쪽): | ⁸⁴Y | 39 | 45 | 83.9206711(46) | 1962 | 【39.5(8) min】 | β⁺ | ⁸⁴Sr | (6+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Ytterbium] `38.5`:   - Thermal conductivity: 【38.5】 W/(m⋅K)

### R-ko-057

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 5.49, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `5.49(7) s` (줄 63, 뒤): | ¹⁵⁶Nd | 60 | 96 | 155.93502(22) | 【5.49(7) s】 | β⁻ | ¹⁵⁶Pm | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 5.34: [Isotopes of yttrium] raw `5.34(5) s` (줄 73, 두 언어 쪽): | ⁹⁶Y | 39 | 57 | 95.9159093(65) | 1975 | 【5.34(5) s】 | β⁻ | ⁹⁶Zr | 0− |  |
  - base 5.8: [Isotopes of yttrium] raw `5.8(6) s` (줄 26, 두 언어 쪽): | ⁷⁸ᵐY | ~300 keV | ~300 keV | ~300 keV | 1998 | 【5.8(6) s】 | β⁺ | ⁷⁸Sr | (5+) |  |
  - base 6: [Lutetium] raw `6s` (줄 64, 두 언어 쪽): … generally encountered in the +3 oxidation state, having lost its two outermost 【6s】 and the single 5d-electron. The lutetium atom is the smallest among the lanthan…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-058

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 2.26e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `2260 kJ/mol` (줄 27, 뒤):   - 이온화 에너지: 1차: 544.5 kJ/mol, 2차: 1070 kJ/mol, 3차: 【2260 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 2.285e+06: [Thulium] raw `2285 kJ/mol` (줄 29, 두 언어 쪽):   - Ionization energies: 1st: 596.7 kJ/mol, 2nd: 1160 kJ/mol, 3rd: 【2285 kJ/mol】
  - base 2.2e+06: [Dysprosium] raw `2200 kJ/mol` (줄 29, 두 언어 쪽):   - Ionization energies: 1st: 573.0 kJ/mol, 2nd: 1130 kJ/mol, 3rd: 【2200 kJ/mol】
  - base 2.404e+06: [Europium] raw `2404 kJ/mol` (줄 29, 한쪽 언어 쪽):   - Ionization energies: 1st: 547.1 kJ/mol, 2nd: 1085 kJ/mol, 3rd: 【2404 kJ/mol】
  - base 2.086e+06: [Praseodymium] raw `2086 kJ/mol` (줄 29, 한쪽 언어 쪽):   - Ionization energies: 1st: 527 kJ/mol, 2nd: 1020 kJ/mol, 3rd: 【2086 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-059

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 12528, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `3.48(16) h` (줄 50, 뒤): | ¹⁵⁰Tb | 65 | 85 | 149.923660(8) | 【3.48(16) h】 | β⁺ (99.95%) | ¹⁵⁰Gd | (2-) |  |  |
  - [터븀 동위 원소] raw `3.48(16) h` (줄 51, 뒤): | ¹⁵⁰Tb | 65 | 85 | 149.923660(8) | 【3.48(16) h】 | α (0.05%) | ¹⁴⁶Eu | (2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 12744: [Isotopes of yttrium] raw `3.54(1) h` (줄 65, 두 언어 쪽): | ⁹²Y | 39 | 53 | 91.9089458(98) | 1940 | 【3.54(1) h】 | β⁻ | ⁹²Zr | 2− |  |
  - base 11613.6: [Isotopes of yttrium] raw `3.226(11) h` (줄 60, 두 언어 쪽): | ⁹⁰ᵐY | 682.01(5) keV | 682.01(5) keV | 682.01(5) keV | 1961 | 【3.226(11) h】 | IT | ⁹⁰Y | 7+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-060

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 1.7672e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 80, 뒤): | ¹⁵⁸ᵐ¹Tb | 【110.3(12) keV】 | 110.3(12) keV | 110.3(12) keV | 10.70(17) s | IT (99.39%) | ¹⁵⁸Tb | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 80, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 【110.3(12) keV】 | 110.3(12) keV | 10.70(17) s | IT (99.39%) | ¹⁵⁸Tb | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 80, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 110.3(12) keV | 【110.3(12) keV】 | 10.70(17) s | IT (99.39%) | ¹⁵⁸Tb | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 81, 뒤): | ¹⁵⁸ᵐ¹Tb | 【110.3(12) keV】 | 110.3(12) keV | 110.3(12) keV | 10.70(17) s | β⁻ (0.6%) | ¹⁵⁸Dy | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 81, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 【110.3(12) keV】 | 110.3(12) keV | 10.70(17) s | β⁻ (0.6%) | ¹⁵⁸Dy | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 81, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 110.3(12) keV | 【110.3(12) keV】 | 10.70(17) s | β⁻ (0.6%) | ¹⁵⁸Dy | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 82, 뒤): | ¹⁵⁸ᵐ¹Tb | 【110.3(12) keV】 | 110.3(12) keV | 110.3(12) keV | 10.70(17) s | β⁺ (0.01%) | ¹⁵⁸Gd | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 82, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 【110.3(12) keV】 | 110.3(12) keV | 10.70(17) s | β⁺ (0.01%) | ¹⁵⁸Gd | 0- |  |  |
  - [터븀 동위 원소] raw `110.3(12) keV` (줄 82, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 110.3(12) keV | 【110.3(12) keV】 | 10.70(17) s | β⁺ (0.01%) | ¹⁵⁸Gd | 0- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.60218e-14: [Neutron capture therapy of cancer] raw `100keV` (줄 182, 한쪽 언어 쪽): …t area. Since the nuclear reactions yield neutrons with energies ranging from < 【100keV】 to tens of MeV, a beam-shaping assembly (BSA) must be used to moderate, filter,…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-061

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 열전도율, base 14.5, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `14.5 W/(m·K)` (줄 32, 뒤):   - 열전도율: 【14.5 W/(m·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 13.9: [Europium] raw `13.9 W/(m⋅K)` (줄 36, 한쪽 언어 쪽):   - Thermal conductivity: est. 【13.9 W/(m⋅K)】
  - base 13.4: [Lanthanum] raw `13.4 W/(m⋅K)` (줄 36, 한쪽 언어 쪽):   - Thermal conductivity: 【13.4 W/(m⋅K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-062

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 14.8, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `14.8K` (줄 61, 뒤): … 일반적인 조건에서는 삼방정계 구조(α 구조)를 가지며, 731°C 이상의 고온으로 가열하면 육방정계 구조로 전환된다. 전환 온도는 불순물에 따라 달라지기도 한다. 922°C 이상으로 가열하면 다시 결정 구조가 바뀌어 체심 입방정계 구조가 된다. 실온에서는 상자성이며 【14.8K】 이하로 냉각시키면 반강자성을 띤다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 15: [Europium] raw `15 K` (줄 125, 한쪽 언어 쪽): …sforming to a cubic high-temperature phase. EuC2 becomes ferromagnetic at about 【15 K】 and is semiconducting above the transition; near the Curie temperature its elec…
  - base 15.5: [Europium] raw `15.5` (줄 123, 한쪽 언어 쪽): …metal and undergoes two closely spaced electronic and magnetic transitions near 【15.5】 and 12.6 K. Its unusual transport properties, including large magnetoresistance…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [Isotopes of yttrium] `14.8`: | ⁷⁹Y | 39 | 40 | 78.937752(14) | 1992 | 【14.8】(6) s | β⁺ | ⁷⁹Sr | 5/2+# |  |
  - [Praseodymium] `14.8`:   - Shear modulus: 【14.8】 GPa

### R-ko-063

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 2.82143e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `176.10(10) keV` (줄 28, 뒤): | ¹³³ᵐ²Nd | 【176.10(10) keV】 | 176.10(10) keV | 176.10(10) keV | ~300 ns |  |  | (9/2-) |  |  |
  - [네오디뮴 동위 원소] raw `176.10(10) keV` (줄 28, 뒤): | ¹³³ᵐ²Nd | 176.10(10) keV | 【176.10(10) keV】 | 176.10(10) keV | ~300 ns |  |  | (9/2-) |  |  |
  - [네오디뮴 동위 원소] raw `176.10(10) keV` (줄 28, 뒤): | ¹³³ᵐ²Nd | 176.10(10) keV | 176.10(10) keV | 【176.10(10) keV】 | ~300 ns |  |  | (9/2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.7362e-14: [Isotopes of yttrium] raw `170.78(5) keV` (줄 85, 두 언어 쪽): | ⁹⁸ᵐ¹Y | 【170.78(5) keV】 | 170.78(5) keV | 170.78(5) keV | 2017 | 615(8) ns | IT | ⁹⁸Y | 2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-064

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 1.41632e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `88.4(2) keV` (줄 76, 뒤): | ¹⁵⁶ᵐ²Tb | 【88.4(2) keV】 | 88.4(2) keV | 88.4(2) keV | 5.3(2) h |  |  | (0+) |  |  |
  - [터븀 동위 원소] raw `88.4(2) keV` (줄 76, 뒤): | ¹⁵⁶ᵐ²Tb | 88.4(2) keV | 【88.4(2) keV】 | 88.4(2) keV | 5.3(2) h |  |  | (0+) |  |  |
  - [터븀 동위 원소] raw `88.4(2) keV` (줄 76, 뒤): | ¹⁵⁶ᵐ²Tb | 88.4(2) keV | 88.4(2) keV | 【88.4(2) keV】 | 5.3(2) h |  |  | (0+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.34988e-14: [Thulium] raw `84.253 keV` (줄 131, 두 언어 쪽): … major emission lines of comparable intensity (at 7.4, 51.354, 52.389, 59.4 and 【84.253 keV】). These radioactive sources have a useful life of about one year, as tools in m…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-065

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 31.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `31.6(10) s` (줄 58, 뒤): | ¹⁵³Nd | 60 | 93 | 152.927698(29) | 【31.6(10) s】 | β⁻ | ¹⁵³Pm | (3/2)- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 30.1: [Isotopes of yttrium] raw `30.1(5) s` (줄 29, 두 언어 쪽): | ⁸⁰Y | 39 | 41 | 79.9343548(67) | 1981 | 【30.1(5) s】 | β⁺ | ⁸⁰Sr | 4− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-066

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `1.6(2) s` (줄 16, 뒤): | ¹³⁹Tb | 65 | 74 | 138.94829(32)# | 【1.6(2) s】 | β⁺ | ¹³⁹Gd | 11/2-# |  |  |
  - [네오디뮴 동위 원소] raw `1.60(15) s` (줄 35, 뒤): | ¹³⁷ᵐNd | 519.43(17) keV | 519.43(17) keV | 519.43(17) keV | 【1.60(15) s】 | IT | ¹³⁷Nd | (11/2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.484: [Isotopes of yttrium] raw `1.484(7) s` (줄 93, 두 언어 쪽): | ⁹⁹Y | 39 | 60 | 98.9241608(71) | 1975 | 【1.484(7) s】 | β⁻ (98.23%) | ⁹⁹Zr | 5/2+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Ytterbium] `1.6`: …becomes a semiconductor when exposed to a pressure of about 16,000 atmospheres (【1.6】 GPa). Its electrical resistivity increases ten times upon compression to 39,000…

### R-ko-067

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 2.768e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `276.8(18) ns` (줄 41, 뒤): | ¹³⁹ᵐ²Nd | 2570.9+X keV | 2570.9+X keV | 2570.9+X keV | 【276.8(18) ns】 |  |  |  |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.92e-07: [Isotopes of yttrium] raw `292(10) ns` (줄 42, 두 언어 쪽): | ⁸⁴ᵐ²Y | 210.42(16) keV | 210.42(16) keV | 210.42(16) keV | 2005 | 【292(10) ns】 | IT | ⁸⁴Y | 4− |  |
  - base 2.58e-07: [Isotopes of yttrium] raw `258(22) ns` (줄 35, 두 언어 쪽): | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 1993 | 【258(22) ns】 | IT | ⁸²Y | 4− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-068

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 589300, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `589.3 kJ/mol` (줄 27, 뒤):   - 이온화 에너지: 1차: 【589.3 kJ/mol】, 2차: 1150 kJ/mol, 3차: 2194 kJ/mol
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 596700: [Thulium] raw `596.7 kJ/mol` (줄 29, 두 언어 쪽):   - Ionization energies: 1st: 【596.7 kJ/mol】, 2nd: 1160 kJ/mol, 3rd: 2285 kJ/mol
  - base 603400: [Ytterbium] raw `603.4 kJ/mol` (줄 29, 두 언어 쪽):   - Ionization energies: 1st: 【603.4 kJ/mol】, 2nd: 1174.8 kJ/mol, 3rd: 2417 kJ/mol
  - base 573000: [Dysprosium] raw `573.0 kJ/mol` (줄 29, 두 언어 쪽):   - Ionization energies: 1st: 【573.0 kJ/mol】, 2nd: 1130 kJ/mol, 3rd: 2200 kJ/mol
  - base 547100: [Europium] raw `547.1 kJ/mol` (줄 29, 한쪽 언어 쪽):   - Ionization energies: 1st: 【547.1 kJ/mol】, 2nd: 1085 kJ/mol, 3rd: 2404 kJ/mol
  - base 538100: [Lanthanum] raw `538.1 kJ/mol` (줄 29, 한쪽 언어 쪽):   - Ionization energies: 1st: 【538.1 kJ/mol】, 2nd: 1067 kJ/mol, 3rd: 1850.3 kJ/mol
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-069

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 1770, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `1770 K` (줄 16, 뒤):   - 녹는점: 【1770 K】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1802: [Europium] raw `1802 K` (줄 18, 한쪽 언어 쪽):   - Boiling point: 【1802 K】 ​(1529 °C, ​2784 °F)
  - base 1680: [Dysprosium] raw `1680 K` (줄 17, 두 언어 쪽):   - Melting point: 【1680 K】 ​(1407 °C, ​2565 °F)
  - base 1654: [Dysprosium] raw `1,654 K` (줄 65, 두 언어 쪽): … (−94 °C). It transforms from the hcp phase to the body-centered cubic phase at 【1,654 K】 (1,381 °C).
  - base 1925: [Lutetium] raw `1925 K` (줄 17, 두 언어 쪽):   - Melting point: 【1925 K】 ​(1652 °C, ​3006 °F)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-070

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 열용량, base 29.54, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `29.54 J/(mol·K)` (줄 22, 뒤):   - 몰열용량: 【29.54 J/(mol·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 27.7: [Dysprosium] raw `27.7 J/(mol·K)` (줄 23, 두 언어 쪽):   - Molar heat capacity: 【27.7 J/(mol·K)】
  - base 27.11: [Lanthanum] raw `27.11 J/(mol·K)` (줄 23, 한쪽 언어 쪽):   - Molar heat capacity: 【27.11 J/(mol·K)】
  - base 26.74: [Ytterbium] raw `26.74 J/(mol·K)` (줄 23, 두 언어 쪽):   - Molar heat capacity: 【26.74 J/(mol·K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-071

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 7.9, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `7.9(6) s` (줄 20, 뒤): | ¹⁴¹ᵐTb | 0(200)# keV | 0(200)# keV | 0(200)# keV | 【7.9(6) s】 | β⁺ | ¹⁴¹Gd | 11/2-# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.3: [Isotopes of yttrium] raw `8.30(20) s` (줄 34, 두 언어 쪽): | ⁸²Y | 39 | 43 | 81.9269302(59) | 1980 | 【8.30(20) s】 | β⁺ | ⁸²Sr | 1+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Europium] `7.9`:   - Shear modulus: 【7.9】 GPa

### R-ko-072

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 5.48185e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `342.15(16) keV` (줄 60, 뒤): | ¹⁵²ᵐ¹Tb | 【342.15(16) keV】 | 342.15(16) keV | 342.15(16) keV | 0.96 µs |  |  | 5- |  |  |
  - [터븀 동위 원소] raw `342.15(16) keV` (줄 60, 뒤): | ¹⁵²ᵐ¹Tb | 342.15(16) keV | 【342.15(16) keV】 | 342.15(16) keV | 0.96 µs |  |  | 5- |  |  |
  - [터븀 동위 원소] raw `342.15(16) keV` (줄 60, 뒤): | ¹⁵²ᵐ¹Tb | 342.15(16) keV | 342.15(16) keV | 【342.15(16) keV】 | 0.96 µs |  |  | 5- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 5.60762e-14: [Ytterbium] raw `350 keV` (줄 154, 두 언어 쪽): …e roughly equivalent to those taken with X-rays having energies between 250 and 【350 keV】. ¹⁶⁹Yb is also used in nuclear medicine.
  - base 5.0084e-14: [Isotopes of yttrium] raw `312.6(9) keV` (줄 32, 두 언어 쪽): | ⁸⁰ᵐ²Y | 【312.6(9) keV】 | 312.6(9) keV | 312.6(9) keV | 1997 | 4.7(3) μs | IT | ⁸⁰Y | (2+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-073

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 63000, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `17.5(1) h` (줄 58, 뒤): | ¹⁵²Tb | 65 | 87 | 151.92407(4) | 【17.5(1) h】 | β⁺ | ¹⁵²Gd | 2- |  |  |
  - [터븀 동위 원소] raw `17.5(1) h` (줄 59, 뒤): | ¹⁵²Tb | 65 | 87 | 151.92407(4) | 【17.5(1) h】 | α (7×10⁻⁷%) | ¹⁴⁸Eu | 2- |  |  |
  - [터븀 동위 원소] raw `17.609(1) h` (줄 54, 뒤): | ¹⁵¹Tb | 65 | 86 | 150.923103(5) | 【17.609(1) h】 | β⁺ (99.99%) | ¹⁵¹Gd | 1/2(+) |  |  |
  - [터븀 동위 원소] raw `17.609(1) h` (줄 55, 뒤): | ¹⁵¹Tb | 65 | 86 | 150.923103(5) | 【17.609(1) h】 | α (0.0095%) | ¹⁴⁷Eu | 1/2(+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 61200: [Dysprosium] raw `17 hours` (줄 149, 두 언어 쪽): …duced by heating an aqueous solution of DyBr3 and NaF to 450 °C at 450 bars for 【17 hours】. This material is remarkably robust, surviving over 100 hours in various aqueou…
  - base 68832: [Praseodymium] raw `19.12 h` (줄 52, 한쪽 언어 쪽): …Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁴¹Pr 100% stable ¹⁴²Pr synth 【19.12 h】 β⁻ ¹⁴²Nd ε ¹⁴²Ce ¹⁴³Pr synth 13.57 d β⁻ ¹⁴³Nd
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-074

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 비저항, base 8.6e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `0.860 μ Ω·m` (줄 33, 뒤):   - 전기 저항도: (실온) (poly) 【0.860 μ Ω·m】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 9e-07: [Europium] raw `0.900 µΩ⋅m` (줄 37, 한쪽 언어 쪽):   - Electrical resistivity: poly: 【0.900 µΩ⋅m】 (at r.t.)
  - base 9.26e-07: [Dysprosium] raw `926 nΩ⋅m` (줄 37, 두 언어 쪽):   - Electrical resistivity: α, poly: 【926 nΩ⋅m】 (r.t.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-075

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 77400, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `21.5(4) h` (줄 65, 뒤): | ¹⁵⁴Tb | 65 | 89 | 153.92468(5) | 【21.5(4) h】 | β⁺ (99.9%) | ¹⁵⁴Gd | 0(+#) |  |  |
  - [터븀 동위 원소] raw `21.5(4) h` (줄 66, 뒤): | ¹⁵⁴Tb | 65 | 89 | 153.92468(5) | 【21.5(4) h】 | β⁻ (0.1%) | ¹⁵⁴Dy | 0(+#) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-076

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 27057.6, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `7.516 h` (줄 47, 뒤): … 안정 ¹⁶⁴Er 1.61% 안정 ¹⁶⁵Er 인공 10.36 h ε 0.376 ¹⁶⁵Ho ¹⁶⁶Er 33.6% 안정 ¹⁶⁷Er 22.95% 안정 ¹⁶⁸Er 26.8% 안정 ¹⁶⁹Er 인공 9.4 d β⁻ 0.351 ¹⁶⁹Tm ¹⁷⁰Er 14.9% 안정 ¹⁷¹Er 인공 【7.516 h】 β⁻ 1.490 ¹⁷¹Tm ¹⁷²Er 인공 49.3 h β⁻ 0.891 ¹⁷²Tm
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-077

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 30.9, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `30.9(7) s` (줄 37, 뒤): | ¹⁴⁵ᵐTb | 0(100)# keV | 0(100)# keV | 0(100)# keV | 【30.9(7) s】 | β⁺ | ¹⁴⁵Gd | (11/2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 30.1: [Isotopes of yttrium] raw `30.1(5) s` (줄 29, 두 언어 쪽): | ⁸⁰Y | 39 | 41 | 79.9343548(67) | 1981 | 【30.1(5) s】 | β⁺ | ⁸⁰Sr | 4− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-078

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 5.5849e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `558.49 pm` (줄 30, 뒤):   - 격자 상수: a = 355.93 pm c = 【558.49 pm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-079

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 8.72385e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `544.5(6) keV` (줄 35, 뒤): | ¹⁴⁴ᵐ⁴Tb | 【544.5(6) keV】 | 544.5(6) keV | 544.5(6) keV | <300 ns |  |  | (10+) |  |  |
  - [터븀 동위 원소] raw `544.5(6) keV` (줄 35, 뒤): | ¹⁴⁴ᵐ⁴Tb | 544.5(6) keV | 【544.5(6) keV】 | 544.5(6) keV | <300 ns |  |  | (10+) |  |  |
  - [터븀 동위 원소] raw `544.5(6) keV` (줄 35, 뒤): | ¹⁴⁴ᵐ⁴Tb | 544.5(6) keV | 544.5(6) keV | 【544.5(6) keV】 | <300 ns |  |  | (10+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 8.90137e-14: [Isotopes of yttrium] raw `555.58(5) keV` (줄 63, 두 언어 쪽): | ⁹¹ᵐY | 【555.58(5) keV】 | 555.58(5) keV | 555.58(5) keV | 1943 | 49.71(4) min | IT | ⁹¹Y | 9/2+ |  |
  - base 8.13105e-14: [Isotopes of yttrium] raw `507.50(13) keV` (줄 36, 두 언어 쪽): | ⁸²ᵐ²Y | 【507.50(13) keV】 | 507.50(13) keV | 507.50(13) keV | 1993 | 148(6) ns | IT | ⁸²Y | 6+ |  |
  - base 9.51693e-14: [Isotopes of yttrium] raw `594(10) keV` (줄 90, 두 언어 쪽): | ⁹⁸ᵐ⁴Y | 【594(10) keV】 | 594(10) keV | 594(10) keV | 2017 | 180(7) ns | IT | ⁹⁸Y | (3−,4−) |  |
  - base 7.9484e-14: [Isotopes of yttrium] raw `496.10(11) keV` (줄 89, 두 언어 쪽): | ⁹⁸ᵐ³Y | 【496.10(11) keV】 | 496.10(11) keV | 496.10(11) keV | 2017 | 6.90(54) μs | IT | ⁹⁸Y | (4)− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-080

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 81720, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `22.7(5) h` (줄 70, 뒤): | ¹⁵⁴ᵐ²Tb | 200(150)# keV | 200(150)# keV | 200(150)# keV | 【22.7(5) h】 |  |  | 7- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 86400: [Neutron capture therapy of cancer] raw `24-hour` (줄 182, 한쪽 언어 쪽): …mmobilization and to increase the number of patients that could be treated in a 【24-hour】 period. Increasing the neutron beam intensity for the same proton current by ad…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-081

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 속도, base 3300, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `3300 m/s` (줄 38, 뒤):   - 음속 (얇은 막대): 【3300 m/s】 (20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-082

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 19900, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `19.90 kJ/mol` (줄 20, 뒤):   - 융해열: 【19.90 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 22000: [Lutetium] raw `22 kJ/mol` (줄 21, 두 언어 쪽):   - Heat of fusion: ca. 【22 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-083

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 7.62957e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `476.2(5) keV` (줄 33, 뒤): | ¹⁴⁴ᵐ²Tb | 【476.2(5) keV】 | 476.2(5) keV | 476.2(5) keV | 2.8(3) µs |  |  | (8-) |  |  |
  - [터븀 동위 원소] raw `476.2(5) keV` (줄 33, 뒤): | ¹⁴⁴ᵐ²Tb | 476.2(5) keV | 【476.2(5) keV】 | 476.2(5) keV | 2.8(3) µs |  |  | (8-) |  |  |
  - [터븀 동위 원소] raw `476.2(5) keV` (줄 33, 뒤): | ¹⁴⁴ᵐ²Tb | 476.2(5) keV | 476.2(5) keV | 【476.2(5) keV】 | 2.8(3) µs |  |  | (8-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 7.46134e-14: [Isotopes of yttrium] raw `465.7(7) keV` (줄 86, 두 언어 쪽): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ …
  - base 7.9484e-14: [Isotopes of yttrium] raw `496.10(11) keV` (줄 89, 두 언어 쪽): | ⁹⁸ᵐ³Y | 【496.10(11) keV】 | 496.10(11) keV | 496.10(11) keV | 2017 | 6.90(54) μs | IT | ⁹⁸Y | (4)− |  |
  - base 8.13105e-14: [Isotopes of yttrium] raw `507.50(13) keV` (줄 36, 두 언어 쪽): | ⁸²ᵐ²Y | 【507.50(13) keV】 | 507.50(13) keV | 507.50(13) keV | 1993 | 148(6) ns | IT | ⁸²Y | 6+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-084

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 3141, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `3141 K` (줄 17, 뒤):   - 끓는점: 【3141 K】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 2928: [Ytterbium] raw `2928 K` (줄 39, 두 언어 쪽):   - Molar magnetic susceptibility: +249.0×10⁻⁶ cm³/mol (【2928 K】)
  - base 3403: [Praseodymium] raw `3403 K` (줄 18, 한쪽 언어 쪽):   - Boiling point: 【3403 K】 ​(3130 °C, ​5666 °F)
  - base 2835.15: [Dysprosium] raw `2562 °C` (줄 18, 두 언어 쪽):   - Boiling point: 2840 K ​(【2562 °C】, ​4653 °F)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-085

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 밀도, base 7520, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `7.52 g/cm³` (줄 18, 뒤):   - 밀도 (상온 근처): 【7.52 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 6973: [Ytterbium] raw `6.973 g/cm³` (줄 73, 두 언어 쪽): …bium crystallizes in the face-centered cubic system. Ytterbium has a density of 【6.973 g/cm³】, which is significantly lower than those of the neighboring lanthanides, thuliu…
  - base 6903: [Ytterbium] raw `6.903 g/cm³` (줄 67, 두 언어 쪽): …z/cu in]) has a body-centered cubic crystalline structure. The alpha allotrope (【6.903 g/cm³】 [3.990 oz/cu in]) has a hexagonal crystalline structure and is stable at low te…
  - base 6773: [Praseodymium] raw `6.773 g/cm³` (줄 19, 한쪽 언어 쪽):   - Density (at 20° C): 【6.773 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-086

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 0.597, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `597(17) ms` (줄 21, 뒤): | ¹⁴²Tb | 65 | 77 | 141.93874(32)# | 【597(17) ms】 | β⁺ | ¹⁴²Gd | 1+ |  |  |
  - [터븀 동위 원소] raw `597(17) ms` (줄 22, 뒤): | ¹⁴²Tb | 65 | 77 | 141.93874(32)# | 【597(17) ms】 | β⁺, p | ¹⁴¹Eu | 1+ |  |  |
  - [네오디뮴 동위 원소] raw `600(150) ms` (줄 14, 뒤): | ¹²⁵Nd | 60 | 65 | 124.94888(43)# | 【600(150) ms】 |  |  | 5/2(+#) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.548: [Isotopes of yttrium] raw `548(2) ms` (줄 83, 두 언어 쪽): | ⁹⁸Y | 39 | 59 | 97.9223948(85) | 1970 | 【548(2) ms】 | β⁻ (99.67%) | ⁹⁸Zr | 0− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [Thulium] `600`: …rades of 99 % and 99.9 % purity. The price per kilogram oscillated between US$4,【600】 and $13,300 in the period from 1959 to 1998 for 99.9 % purity, and it was the s…
  - [Europium] `600`: …ide, EuN, can be prepared by direct reaction of the metal with ammonia at about 【600】 °C and crystallizes in the cubic rock-salt structure. Europium phosphide, EuP, …
  - [Europium] `600`: … hexagonal rhabdophane structure; after dehydration at temperatures above about 【600】 °C it transforms to monoclinic anhydrous EuPO4, which is isostructural with mon…

### R-ko-087

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 948672, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `10.98(1) d` (줄 52, 뒤): | ¹⁴⁷Nd | 60 | 87 | 146.9161004(25) | 【10.98(1) d】 | β⁻ | ¹⁴⁷Pm | 5/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-088

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 180, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `3.0(1) min` (줄 89, 뒤): | ¹⁶⁴Tb | 65 | 99 | 163.93335(11) | 【3.0(1) min】 | β⁻ | ¹⁶⁴Dy | (5+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 171: [Isotopes of yttrium] raw `2.85(2) min` (줄 38, 두 언어 쪽): | ⁸³ᵐY | 62.04(10) keV | 62.04(10) keV | 62.04(10) keV | 1973 | 【2.85(2) min】 | β⁺ (60%) | ⁸³Sr | (3/2−) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Neutron capture therapy of cancer] `3.0`: … lithium-7 reaction requires a proton accelerator with energies between 1.9 and 【3.0】 MeV, while the beryllium-9 reaction typically uses accelerators with energies b…

### R-ko-089

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 14824.8, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `4.118(25) h` (줄 46, 뒤): | ¹⁴⁹Tb | 65 | 84 | 148.923246(5) | 【4.118(25) h】 | β⁺ (83.3%) | ¹⁴⁹Gd | 1/2+ |  |  |
  - [터븀 동위 원소] raw `4.118(25) h` (줄 47, 뒤): | ¹⁴⁹Tb | 65 | 84 | 148.923246(5) | 【4.118(25) h】 | α (16.7%) | ¹⁴⁵Eu | 1/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-090

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 각도, base 23.307, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `23.307°` (줄 30, 뒤):   - 격자 상수: ar = 0.89834 nm α = 【23.307°】 ah = 0.36291 nm ch = 2.6207 nm (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-091

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 87840, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `24.4(10) h` (줄 75, 뒤): | ¹⁵⁶ᵐ¹Tb | 54(3) keV | 54(3) keV | 54(3) keV | 【24.4(10) h】 | IT | ¹⁵⁶Tb | (7-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 86400: [Neutron capture therapy of cancer] raw `24-hour` (줄 182, 한쪽 언어 쪽): …mmobilization and to increase the number of patients that could be treated in a 【24-hour】 period. Increasing the neutron beam intensity for the same proton current by ad…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-092

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 6.35e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `63.5 GPa` (줄 35, 뒤):   - 영률: 【63.5 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 6.14e+10: [Dysprosium] raw `61.4 GPa` (줄 40, 두 언어 쪽):   - Young's modulus: 【61.4 GPa】
  - base 6.86e+10: [Lutetium] raw `68.6 GPa` (줄 39, 두 언어 쪽):   - Young's modulus: 【68.6 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-093

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 6.35904e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 30, 뒤): | ¹⁴⁴ᵐ¹Tb | 【396.9(5) keV】 | 396.9(5) keV | 396.9(5) keV | 4.25(15) s | IT (66%) | ¹⁴⁴Tb | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 30, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 【396.9(5) keV】 | 396.9(5) keV | 4.25(15) s | IT (66%) | ¹⁴⁴Tb | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 30, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 396.9(5) keV | 【396.9(5) keV】 | 4.25(15) s | IT (66%) | ¹⁴⁴Tb | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 31, 뒤): | ¹⁴⁴ᵐ¹Tb | 【396.9(5) keV】 | 396.9(5) keV | 396.9(5) keV | 4.25(15) s | β⁺ (34%) | ¹⁴⁴Gd | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 31, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 【396.9(5) keV】 | 396.9(5) keV | 4.25(15) s | β⁺ (34%) | ¹⁴⁴Gd | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 31, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 396.9(5) keV | 【396.9(5) keV】 | 4.25(15) s | β⁺ (34%) | ¹⁴⁴Gd | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 32, 뒤): | ¹⁴⁴ᵐ¹Tb | 【396.9(5) keV】 | 396.9(5) keV | 396.9(5) keV | 4.25(15) s | β⁺, p (<1%) | ¹⁴³Eu | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 32, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 【396.9(5) keV】 | 396.9(5) keV | 4.25(15) s | β⁺, p (<1%) | ¹⁴³Eu | (6-) |  |  |
  - [터븀 동위 원소] raw `396.9(5) keV` (줄 32, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 396.9(5) keV | 【396.9(5) keV】 | 4.25(15) s | β⁺, p (<1%) | ¹⁴³Eu | (6-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 6.29431e-14: [Isotopes of yttrium] raw `392.86(9) keV` (줄 55, 두 언어 쪽): | ⁸⁸ᵐ¹Y | 【392.86(9) keV】 | 392.86(9) keV | 392.86(9) keV | 1955 | 301(3) μs | IT | ⁸⁸Y | 1+ |  |
  - base 6.45084e-14: [Isotopes of yttrium] raw `402.63(14) keV` (줄 35, 두 언어 쪽): | ⁸²ᵐ¹Y | 【402.63(14) keV】 | 402.63(14) keV | 402.63(14) keV | 1993 | 258(22) ns | IT | ⁸²Y | 4− |  |
  - base 6.10141e-14: [Isotopes of yttrium] raw `380.82(7) keV` (줄 52, 두 언어 쪽): | ⁸⁷ᵐY | 【380.82(7) keV】 | 380.82(7) keV | 380.82(7) keV | 1940 | 13.37(3) h | IT (98.43%) | ⁸⁷Y | 9/2+ …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-094

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 2.8e-06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `2.8(3) µs` (줄 33, 뒤): | ¹⁴⁴ᵐ²Tb | 476.2(5) keV | 476.2(5) keV | 476.2(5) keV | 【2.8(3) µs】 |  |  | (8-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-095

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 744, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `12.4(6) min` (줄 31, 뒤): | ¹³⁵Nd | 60 | 75 | 134.918181(21) | 【12.4(6) min】 | β⁺ | ¹³⁵Pr | 9/2(-) |  |  |
  - [네오디뮴 동위 원소] raw `12.44(7) min` (줄 56, 뒤): | ¹⁵¹Nd | 60 | 91 | 150.923829(3) | 【12.44(7) min】 | β⁻ | ¹⁵¹Pm | 3/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-096

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 1345, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `1345 K` (줄 16, 뒤):   - 녹는점: 【1345 K】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1373.15: [Europium] raw `1100` (줄 223, 한쪽 언어 쪽): … carried out in refractory apparatus, commonly using tantalum, at approximately 【1100】–1200 °C. The europium produced is considerably more volatile than the lanthanum…
  - base 1273.15: [Praseodymium] raw `1000 °C` (줄 76, 한쪽 언어 쪽): …c trends, as it is one of the first and thus one of the largest lanthanides. At 【1000 °C】, many praseodymium oxides with composition PrO2−x exist as disordered, nonstoic…
  - base 1469: [Ytterbium] raw `1469 K` (줄 18, 두 언어 쪽):   - Boiling point: 【1469 K】 ​(1196 °C, ​2185 °F)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-097

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 8.9834e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `0.89834 nm` (줄 30, 뒤):   - 격자 상수: ar = 【0.89834 nm】 α = 23.307° ah = 0.36291 nm ch = 2.6207 nm (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-098

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 비저항, base 9.4e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `0.940 μ Ω·m` (줄 33, 뒤):   - 전기 저항도: (실온) (α, poly) 【0.940 μ Ω·m】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 9.26e-07: [Dysprosium] raw `926 nΩ⋅m` (줄 37, 두 언어 쪽):   - Electrical resistivity: α, poly: 【926 nΩ⋅m】 (r.t.)
  - base 9e-07: [Europium] raw `0.900 µΩ⋅m` (줄 37, 한쪽 언어 쪽):   - Electrical resistivity: poly: 【0.900 µΩ⋅m】 (at r.t.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-099

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 1.04141e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `65.0(2) keV` (줄 32, 뒤): | ¹³⁵ᵐNd | 【65.0(2) keV】 | 65.0(2) keV | 65.0(2) keV | 5.5(5) min | β⁺ | ¹³⁵Pr | (1/2+) |  |  |
  - [네오디뮴 동위 원소] raw `65.0(2) keV` (줄 32, 뒤): | ¹³⁵ᵐNd | 65.0(2) keV | 【65.0(2) keV】 | 65.0(2) keV | 5.5(5) min | β⁺ | ¹³⁵Pr | (1/2+) |  |  |
  - [네오디뮴 동위 원소] raw `65.0(2) keV` (줄 32, 뒤): | ¹³⁵ᵐNd | 65.0(2) keV | 65.0(2) keV | 【65.0(2) keV】 | 5.5(5) min | β⁺ | ¹³⁵Pr | (1/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1.07346e-14: [Isotopes of yttrium] raw `67.0(2) keV` (줄 41, 두 언어 쪽): | ⁸⁴ᵐ¹Y | 【67.0(2) keV】 | 67.0(2) keV | 67.0(2) keV | 1976 | 4.6(2) s | β⁺ | ⁸⁴Sr | 1+ |  |
  - base 9.9399e-15: [Isotopes of yttrium] raw `62.04(10) keV` (줄 38, 두 언어 쪽): | ⁸³ᵐY | 【62.04(10) keV】 | 62.04(10) keV | 62.04(10) keV | 1973 | 2.85(2) min | β⁺ (60%) | ⁸³Sr | (3/2−)…
  - base 9.51693e-15: [Thulium] raw `59.4` (줄 131, 두 언어 쪽): … and five major emission lines of comparable intensity (at 7.4, 51.354, 52.389, 【59.4】 and 84.253 keV). These radioactive sources have a useful life of about one year…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-100

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 속도, base 2130, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `2130 m/s` (줄 38, 뒤):   - 음속 (얇은 막대): 【2130 m/s】 (20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2280: [Praseodymium] raw `2280 m/s` (줄 43, 한쪽 언어 쪽):   - Speed of sound thin rod: 【2280 m/s】 (at 20 °C)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-101

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 8.9, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `8.9(2) s` (줄 62, 뒤): | ¹⁵⁵Nd | 60 | 95 | 154.93293(16)# | 【8.9(2) s】 | β⁻ | ¹⁵⁵Pm | 3/2-# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 8.3: [Isotopes of yttrium] raw `8.30(20) s` (줄 34, 두 언어 쪽): | ⁸²Y | 39 | 43 | 81.9269302(59) | 1980 | 【8.30(20) s】 | β⁺ | ⁸²Sr | 1+ |  |
  - base 9.6: [Isotopes of yttrium] raw `9.6(2) s` (줄 74, 두 언어 쪽): | ⁹⁶ᵐ¹Y | 1540(9) keV | 1540(9) keV | 1540(9) keV | 1975 | 【9.6(2) s】 | β⁻ | ⁹⁶Zr | 8+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-102

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 25.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `25.6(22) s` (줄 91, 뒤): | ¹⁶⁶Tb | 65 | 101 | 165.93799(11) | 【25.6(22) s】 | β⁻ | ¹⁶⁶Dy |  |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-103

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 3039, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `50.65(33) min` (줄 33, 뒤): | ¹³⁶Nd | 60 | 76 | 135.914976(13) | 【50.65(33) min】 | β⁺ | ¹³⁶Pr | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2982.6: [Isotopes of yttrium] raw `49.71(4) min` (줄 63, 두 언어 쪽): | ⁹¹ᵐY | 555.58(5) keV | 555.58(5) keV | 555.58(5) keV | 1943 | 【49.71(4) min】 | IT | ⁹¹Y | 9/2+ |  |
  - base 2844: [Isotopes of yttrium] raw `47.4(4) min` (줄 48, 두 언어 쪽): | ⁸⁶ᵐ¹Y | 218.21(9) keV | 218.21(9) keV | 218.21(9) keV | 1961 | 【47.4(4) min】 | IT (99.31%) | ⁸⁶Y | (8+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-104

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 열용량, base 28.12, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `28.12 J/(mol·K)` (줄 22, 뒤):   - 몰열용량: 【28.12 J/(mol·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 27.7: [Dysprosium] raw `27.7 J/(mol·K)` (줄 23, 두 언어 쪽):   - Molar heat capacity: 【27.7 J/(mol·K)】
  - base 27.11: [Lanthanum] raw `27.11 J/(mol·K)` (줄 23, 한쪽 언어 쪽):   - Molar heat capacity: 【27.11 J/(mol·K)】
  - base 26.74: [Ytterbium] raw `26.74 J/(mol·K)` (줄 23, 두 언어 쪽):   - Molar heat capacity: 【26.74 J/(mol·K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-105

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 3.5593e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `355.93 pm` (줄 30, 뒤):   - 격자 상수: a = 【355.93 pm】 c = 558.49 pm (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-106

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 3.55908e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `2221.4(1) keV` (줄 43, 뒤): | ¹⁴⁰ᵐNd | 【2221.4(1) keV】 | 2221.4(1) keV | 2221.4(1) keV | 600(50) µs |  |  | 7- |  |  |
  - [네오디뮴 동위 원소] raw `2221.4(1) keV` (줄 43, 뒤): | ¹⁴⁰ᵐNd | 2221.4(1) keV | 【2221.4(1) keV】 | 2221.4(1) keV | 600(50) µs |  |  | 7- |  |  |
  - [네오디뮴 동위 원소] raw `2221.4(1) keV` (줄 43, 뒤): | ¹⁴⁰ᵐNd | 2221.4(1) keV | 2221.4(1) keV | 【2221.4(1) keV】 | 600(50) µs |  |  | 7- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3.4313e-13: [Isotopes of yttrium] raw `2141.65(19) keV` (줄 95, 두 언어 쪽): | ⁹⁹ᵐY | 【2141.65(19) keV】 | 2141.65(19) keV | 2141.65(19) keV | 1985 | 8.2(4) μs | IT | ⁹⁹Y | (17/2+) |  …
  - base 3.70103e-13: [Neutron capture therapy of cancer] raw `2.31 MeV` (줄 23, 한쪽 언어 쪽): ¹⁰B + nth → [¹¹B] *→ α + ⁷Li + 【2.31 MeV】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-107

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 열팽창, base 1.06e-05, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `10.6 µm/(m·K)` (줄 31, 뒤):   - 열팽창: (실온) (α, poly) 【10.6 µm/(m·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 9.9e-06: [Dysprosium] raw `9.9 µm/(m⋅K)` (줄 35, 두 언어 쪽):   - Thermal expansion: poly: 【9.9 µm/(m⋅K)】 (r.t.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-108

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1782, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `29.7(5) min` (줄 38, 뒤): | ¹³⁹Nd | 60 | 79 | 138.911978(28) | 【29.7(5) min】 | β⁺ | ¹³⁹Pr | 3/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-109

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 177480, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `49.3 h` (줄 47, 뒤): …6 h ε 0.376 ¹⁶⁵Ho ¹⁶⁶Er 33.6% 안정 ¹⁶⁷Er 22.95% 안정 ¹⁶⁸Er 26.8% 안정 ¹⁶⁹Er 인공 9.4 d β⁻ 0.351 ¹⁶⁹Tm ¹⁷⁰Er 14.9% 안정 ¹⁷¹Er 인공 7.516 h β⁻ 1.490 ¹⁷¹Tm ¹⁷²Er 인공 【49.3 h】 β⁻ 0.891 ¹⁷²Tm
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-110

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 8.03876e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `501.74(19) keV` (줄 61, 뒤): | ¹⁵²ᵐ²Tb | 【501.74(19) keV】 | 501.74(19) keV | 501.74(19) keV | 4.2(1) min | IT (78.8%) | ¹⁵²Tb | 8+ |  |  |
  - [터븀 동위 원소] raw `501.74(19) keV` (줄 61, 뒤): | ¹⁵²ᵐ²Tb | 501.74(19) keV | 【501.74(19) keV】 | 501.74(19) keV | 4.2(1) min | IT (78.8%) | ¹⁵²Tb | 8+ |  |  |
  - [터븀 동위 원소] raw `501.74(19) keV` (줄 61, 뒤): | ¹⁵²ᵐ²Tb | 501.74(19) keV | 501.74(19) keV | 【501.74(19) keV】 | 4.2(1) min | IT (78.8%) | ¹⁵²Tb | 8+ |  |  |
  - [터븀 동위 원소] raw `501.74(19) keV` (줄 62, 뒤): | ¹⁵²ᵐ²Tb | 【501.74(19) keV】 | 501.74(19) keV | 501.74(19) keV | 4.2(1) min | β⁺ (21.2%) | ¹⁵²Gd | 8+ |  |  |
  - [터븀 동위 원소] raw `501.74(19) keV` (줄 62, 뒤): | ¹⁵²ᵐ²Tb | 501.74(19) keV | 【501.74(19) keV】 | 501.74(19) keV | 4.2(1) min | β⁺ (21.2%) | ¹⁵²Gd | 8+ |  |  |
  - [터븀 동위 원소] raw `501.74(19) keV` (줄 62, 뒤): | ¹⁵²ᵐ²Tb | 501.74(19) keV | 501.74(19) keV | 【501.74(19) keV】 | 4.2(1) min | β⁺ (21.2%) | ¹⁵²Gd | 8+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 7.9484e-14: [Isotopes of yttrium] raw `496.10(11) keV` (줄 89, 두 언어 쪽): | ⁹⁸ᵐ³Y | 【496.10(11) keV】 | 496.10(11) keV | 496.10(11) keV | 2017 | 6.90(54) μs | IT | ⁹⁸Y | (4)− |  |
  - base 8.13105e-14: [Isotopes of yttrium] raw `507.50(13) keV` (줄 36, 두 언어 쪽): | ⁸²ᵐ²Y | 【507.50(13) keV】 | 507.50(13) keV | 507.50(13) keV | 1993 | 148(6) ns | IT | ⁸²Y | 6+ |  |
  - base 7.46134e-14: [Isotopes of yttrium] raw `465.7(7) keV` (줄 86, 두 언어 쪽): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ …
  - base 8.90137e-14: [Isotopes of yttrium] raw `555.58(5) keV` (줄 63, 두 언어 쪽): | ⁹¹ᵐY | 【555.58(5) keV】 | 555.58(5) keV | 555.58(5) keV | 1943 | 49.71(4) min | IT | ⁹¹Y | 9/2+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-111

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 3.5, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `3.5(2) s` (줄 19, 뒤): | ¹⁴¹Tb | 65 | 76 | 140.94145(11) | 【3.5(2) s】 | β⁺ | ¹⁴¹Gd | (5/2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.75: [Isotopes of yttrium] raw `3.75(3) s` (줄 76, 두 언어 쪽): | ⁹⁷Y | 39 | 58 | 96.9182867(72) | 1970 | 【3.75(3) s】 | β⁻ (99.945%) | ⁹⁷Zr | 1/2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-112

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 2.38e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `238 pm` (줄 28, 뒤):   - 원자 반지름: 185 pm (실험값) 【238 pm】 (계산값)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.47e-10: [Praseodymium] raw `247 pm` (줄 62, 한쪽 언어 쪽): …Praseodymium is calculated to have a very large atomic radius; with a radius of 【247 pm】, barium, rubidium and caesium are larger. However, observationally, it is usual…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-113

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 459648, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `5.32(6) d` (줄 72, 뒤): | ¹⁵⁵Tb | 65 | 90 | 154.923505(13) | 【5.32(6) d】 | ε | ¹⁵⁵Gd | 3/2+ |  |  |
  - [터븀 동위 원소] raw `5.35(10) d` (줄 73, 뒤): | ¹⁵⁶Tb | 65 | 91 | 155.924747(5) | 【5.35(10) d】 | β⁺ | ¹⁵⁶Gd | 3- |  |  |
  - [터븀 동위 원소] raw `5.35(10) d` (줄 74, 뒤): | ¹⁵⁶Tb | 65 | 91 | 155.924747(5) | 【5.35(10) d】 | β⁻ (드묾) | ¹⁵⁶Dy | 3- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 432000: [Lutetium] raw `5d` (줄 64, 두 언어 쪽): …ered in the +3 oxidation state, having lost its two outermost 6s and the single 【5d】-electron. The lutetium atom is the smallest among the lanthanide atoms, due to …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-114

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 1.44356e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `90.1(3) keV` (줄 44, 뒤): | ¹⁴⁸ᵐ¹Tb | 【90.1(3) keV】 | 90.1(3) keV | 90.1(3) keV | 2.20(5) min | β⁺ | ¹⁴⁸Gd | (9)+ |  |  |
  - [터븀 동위 원소] raw `90.1(3) keV` (줄 44, 뒤): | ¹⁴⁸ᵐ¹Tb | 90.1(3) keV | 【90.1(3) keV】 | 90.1(3) keV | 2.20(5) min | β⁺ | ¹⁴⁸Gd | (9)+ |  |  |
  - [터븀 동위 원소] raw `90.1(3) keV` (줄 44, 뒤): | ¹⁴⁸ᵐ¹Tb | 90.1(3) keV | 90.1(3) keV | 【90.1(3) keV】 | 2.20(5) min | β⁺ | ¹⁴⁸Gd | (9)+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.34988e-14: [Thulium] raw `84.253 keV` (줄 131, 두 언어 쪽): … major emission lines of comparable intensity (at 7.4, 51.354, 52.389, 59.4 and 【84.253 keV】). These radioactive sources have a useful life of about one year, as tools in m…
  - base 1.60218e-14: [Neutron capture therapy of cancer] raw `100keV` (줄 182, 한쪽 언어 쪽): …t area. Since the nuclear reactions yield neutrons with energies ranging from < 【100keV】 to tens of MeV, a beam-shaping assembly (BSA) must be used to moderate, filter,…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-115

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 10.7, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `10.70(17) s` (줄 80, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 110.3(12) keV | 110.3(12) keV | 【10.70(17) s】 | IT (99.39%) | ¹⁵⁸Tb | 0- |  |  |
  - [터븀 동위 원소] raw `10.70(17) s` (줄 81, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 110.3(12) keV | 110.3(12) keV | 【10.70(17) s】 | β⁻ (0.6%) | ¹⁵⁸Dy | 0- |  |  |
  - [터븀 동위 원소] raw `10.70(17) s` (줄 82, 뒤): | ¹⁵⁸ᵐ¹Tb | 110.3(12) keV | 110.3(12) keV | 110.3(12) keV | 【10.70(17) s】 | β⁺ (0.01%) | ¹⁵⁸Gd | 0- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-116

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 4.25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `4.25(15) s` (줄 30, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 396.9(5) keV | 396.9(5) keV | 【4.25(15) s】 | IT (66%) | ¹⁴⁴Tb | (6-) |  |  |
  - [터븀 동위 원소] raw `4.25(15) s` (줄 31, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 396.9(5) keV | 396.9(5) keV | 【4.25(15) s】 | β⁺ (34%) | ¹⁴⁴Gd | (6-) |  |  |
  - [터븀 동위 원소] raw `4.25(15) s` (줄 32, 뒤): | ¹⁴⁴ᵐ¹Tb | 396.9(5) keV | 396.9(5) keV | 396.9(5) keV | 【4.25(15) s】 | β⁺, p (<1%) | ¹⁴³Eu | (6-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.6: [Isotopes of yttrium] raw `4.6(2) s` (줄 41, 두 언어 쪽): | ⁸⁴ᵐ¹Y | 67.0(2) keV | 67.0(2) keV | 67.0(2) keV | 1976 | 【4.6(2) s】 | β⁺ | ⁸⁴Sr | 1+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-117

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 2.26e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `226 pm` (줄 28, 뒤):   - 원자 반지름: 175 pm (실험값) 【226 pm】 (계산값)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.07e-10: [Lanthanum] raw `207±8 pm` (줄 31, 한쪽 언어 쪽):   - Covalent radius: 【207±8 pm】
  - base 2.47e-10: [Praseodymium] raw `247 pm` (줄 62, 한쪽 언어 쪽): …Praseodymium is calculated to have a very large atomic radius; with a radius of 【247 pm】, barium, rubidium and caesium are larger. However, observationally, it is usual…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [Isotopes of yttrium] `226`: | ⁹⁰ᵐY | 682.01(5) keV | 682.01(5) keV | 682.01(5) keV | 1961 | 3.【226】(11) h | IT | ⁹⁰Y | 7+ |  |
  - [Isotopes of yttrium] `226`: | ⁹⁰ᵐY | 682.01(5) keV | 682.01(5) keV | 682.01(5) keV | 1961 | 3.【226】(11) h | β⁻ (0.0018%) | ⁹⁰Zr | 7+ |  |

### R-ko-118

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 3.6291e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `0.36291 nm` (줄 30, 뒤):   - 격자 상수: ar = 0.89834 nm α = 23.307° ah = 【0.36291 nm】 ch = 2.6207 nm (20 °C에서)
  - [이트륨] raw `364.83 pm` (줄 30, 뒤):   - 격자 상수: a = 【364.83 pm】 c = 573.17 pm (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-119

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 4.97e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `49.7 GPa` (줄 35, 뒤):   - 영률: (α form) 【49.7 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.76e+10: [Lutetium] raw `47.6 GPa` (줄 41, 두 언어 쪽):   - Bulk modulus: 【47.6 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-120

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 1023.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `750 °C` (줄 64, 뒤): 순수한 원소 상태로는 표면에 더 이상의 산화를 막는 산화피막(산화이트륨 Y2O3로 이루어진)을 생성하기 때문에 비교적 안정한 편이다. 이 산화피막은 이트륨 금속이 수증기 안에서 【750 °C】 로 가열될 때 1 μm의 두께를 가질 수 있다. 잘게 나눠졌을 때, 이트륨은 공기 중에서 불안정하다. 작은 이트륨 조각은 400 °C 이상의 온도에서 불이 붙을 수 있다. 질화 이트륨(YN)은 이트륨이 질소(N) 기체 안에서 1000 °C 로 가열될 때 생성된다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1068: [Praseodymium] raw `1,068 K` (줄 66, 한쪽 언어 쪽): …rystal structure at room temperature, called the alpha phase (α-Pr). At 795 °C (【1,068 K】) it transforms to a different allotrope that has a body-centered cubic structur…
  - base 973: [Samarium–cobalt magnet] raw `973 K` (줄 13, 한쪽 언어 쪽): …tures from 250 °C (523 K) to 550 °C (823 K) and Curie temperatures from 700 °C (【973 K】) to 800 °C (1,070 K).
  - base 1095: [Europium] raw `1,095 K` (줄 63, 한쪽 언어 쪽): …temperature it has a density of about 5.24 g/cm³ and a melting point of 822 °C (【1,095 K】).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-121

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 6.7e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `670(60) ns` (줄 34, 뒤): | ¹⁴⁴ᵐ³Tb | 517.1(5) keV | 517.1(5) keV | 517.1(5) keV | 【670(60) ns】 |  |  | (9+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.15e-07: [Isotopes of yttrium] raw `615(8) ns` (줄 85, 두 언어 쪽): | ⁹⁸ᵐ¹Y | 170.78(5) keV | 170.78(5) keV | 170.78(5) keV | 2017 | 【615(8) ns】 | IT | ⁹⁸Y | 2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-122

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 4.9, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `4.9(2) s` (줄 20, 뒤): | ¹²⁹Nd | 60 | 69 | 128.93319(22)# | 【4.9(2) s】 | β⁺ | ¹²⁹Pr | 5/2+# |  |  |
  - [네오디뮴 동위 원소] raw `4.9(2) s` (줄 21, 뒤): | ¹²⁹Nd | 60 | 69 | 128.93319(22)# | 【4.9(2) s】 | β⁺, p (드묾) | ¹²⁸Ce | 5/2+# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 4.8: [Isotopes of yttrium] raw `4.8(3) s` (줄 30, 두 언어 쪽): | ⁸⁰ᵐ¹Y | 228.5(1) keV | 228.5(1) keV | 228.5(1) keV | 1998 | 【4.8(3) s】 | IT (81%) | ⁸⁰Y | 1− |  |
  - base 4.6: [Isotopes of yttrium] raw `4.6(2) s` (줄 41, 두 언어 쪽): | ⁸⁴ᵐ¹Y | 67.0(2) keV | 67.0(2) keV | 67.0(2) keV | 1976 | 【4.6(2) s】 | β⁺ | ⁸⁴Sr | 1+ |  |
  - base 5.34: [Isotopes of yttrium] raw `5.34(5) s` (줄 73, 두 언어 쪽): | ⁹⁶Y | 39 | 57 | 95.9159093(65) | 1975 | 【5.34(5) s】 | β⁻ | ⁹⁶Zr | 0− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-123

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 3.25043e+15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `1.03×10⁸y` (줄 48, 뒤):   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁴⁴Sm 3.07% 안정 ¹⁴⁶Sm 인공 【1.03×10⁸y】 α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 1.06×10¹¹y α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α 1.986 ¹⁴⁴Nd ¹⁴⁹Sm 13.82% >2×10¹⁵ y α 1.870 ¹⁴⁵Nd ¹⁵⁰Sm 7.38% 안정 ¹⁵²Sm 26.7…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [Ytterbium] `1.03`: …o the material used to make the laser. Ytterbium lasers commonly radiate in the 【1.03】–1.12 μm band being optically pumped at wavelength 900 nm–1 μm, dependently on t…
  - [Lanthanum] `1.03`: … half-life (t1/2) mode pro­duct ¹³⁷La synth 6×10⁴ y ε ¹³⁷Ba ¹³⁸La 0.0889999999% 【1.03】×10¹¹ y β⁺ ¹³⁸Ba β⁻ ¹³⁸Ce ¹³⁹La 99.911% stable ¹⁴⁰La synth 40.289 h β⁻ ¹⁴⁰Ce
  - [Lanthanum] `1.03`: …pe ¹³⁸ La is one of the few primordial odd–odd nuclei, with a long half-life of 【1.03】×10¹¹ years. It is one of the proton-rich p-nuclei which cannot be produced in t…

### R-ko-124

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 456, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `7.60(15) min` (줄 87, 뒤): | ¹⁶²Tb | 65 | 97 | 161.92949(4) | 【7.60(15) min】 | β⁻ | ¹⁶²Dy | 1- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 424.8: [Isotopes of yttrium] raw `7.08(8) min` (줄 37, 두 언어 쪽): | ⁸³Y | 39 | 44 | 82.922484(20) | 1962 | 【7.08(8) min】 | β⁺ | ⁸³Sr | (9/2+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-125

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 0.00041, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `410(30) µs` (줄 30, 뒤): | ¹³⁴ᵐNd | 2293.1(4) keV | 2293.1(4) keV | 2293.1(4) keV | 【410(30) µs】 |  |  | (8)- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Dysprosium] `410`:   - Vickers hardness: 【410】–550 MPa

### R-ko-126

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 밀도, base 4472, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `4.472 g/cm³` (줄 18, 뒤):   - 밀도 (상온 근처): 【4.472 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-127

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 3.78e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `37.8 GPa` (줄 37, 뒤):   - 부피 탄성 계수: (α form) 【37.8 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3.7e+10: [Europium] raw `37 GPa` (줄 67, 한쪽 언어 쪽): …rately modulated monoclinic structure, known as Eu-IV, which is stable to about 【37 GPa】; another structural transition occurs at higher pressure.
  - base 3.66e+10: [Lanthanum] raw `36.6 GPa` (줄 40, 한쪽 언어 쪽):   - Young's modulus: α form: 【36.6 GPa】
  - base 4.05e+10: [Dysprosium] raw `40.5 GPa` (줄 42, 두 언어 쪽):   - Bulk modulus: 【40.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-128

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 0.000186, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `186(4) µs` (줄 64, 뒤): | ¹⁵³ᵐTb | 163.175(5) keV | 163.175(5) keV | 163.175(5) keV | 【186(4) µs】 |  |  | 11/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-129

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 4.1e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `410(50) ns` (줄 37, 뒤): | ¹³⁸ᵐNd | 3174.9(4) keV | 3174.9(4) keV | 3174.9(4) keV | 【410(50) ns】 |  |  | (10+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.5e-07: [Isotopes of yttrium] raw `450(150) ns` (줄 91, 두 언어 쪽): | ⁹⁸ᵐ⁵Y | 972.17(20) keV | 972.17(20) keV | 972.17(20) keV | 1970 | 【450(150) ns】 | IT | ⁹⁸Y | (8+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Dysprosium] `410`:   - Vickers hardness: 【410】–550 MPa

### R-ko-130

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 102888, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `28.58 h` (줄 47, 뒤):   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁶⁰Er 인공 【28.58 h】 ε 0.330 ¹⁶⁰Ho ¹⁶²Er 0.14% 안정 ¹⁶⁴Er 1.61% 안정 ¹⁶⁵Er 인공 10.36 h ε 0.376 ¹⁶⁵Ho ¹⁶⁶Er 33.6% 안정 ¹⁶⁷Er 22.95% 안정 ¹⁶⁸Er 26.8% 안정 ¹⁶⁹Er 인공 9.4 d β⁻ 0.351 ¹⁶⁹T…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-131

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 348, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `5.8(2) min` (줄 52, 뒤): | ¹⁵⁰ᵐTb | 457(29) keV | 457(29) keV | 457(29) keV | 【5.8(2) min】 | β⁺ | ¹⁵⁰Gd | 9+ |  |  |
  - [터븀 동위 원소] raw `5.8(2) min` (줄 53, 뒤): | ¹⁵⁰ᵐTb | 457(29) keV | 457(29) keV | 457(29) keV | 【5.8(2) min】 | IT (드묾) | ¹⁵⁰Tb | 9+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [Isotopes of yttrium] `5.8`: | ⁷⁸ᵐY | ~300 keV | ~300 keV | ~300 keV | 1998 | 【5.8】(6) s | β⁺ | ⁷⁸Sr | (5+) |  |
  - [Isotopes of yttrium] `5.8`: | ⁷⁸ᵐY | ~300 keV | ~300 keV | ~300 keV | 1998 | 【5.8】(6) s | β⁺, p? | ⁷⁷Rb | (5+) |  |
  - [Neutron capture therapy of cancer] `5.8`: …ata, the MeST was reported as 14.2 months and the time to tumor progression was 【5.8】 months. However, more careful examination of the complete survival data reveale…

### R-ko-132

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 8.28486e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `517.1(5) keV` (줄 34, 뒤): | ¹⁴⁴ᵐ³Tb | 【517.1(5) keV】 | 517.1(5) keV | 517.1(5) keV | 670(60) ns |  |  | (9+) |  |  |
  - [터븀 동위 원소] raw `517.1(5) keV` (줄 34, 뒤): | ¹⁴⁴ᵐ³Tb | 517.1(5) keV | 【517.1(5) keV】 | 517.1(5) keV | 670(60) ns |  |  | (9+) |  |  |
  - [터븀 동위 원소] raw `517.1(5) keV` (줄 34, 뒤): | ¹⁴⁴ᵐ³Tb | 517.1(5) keV | 517.1(5) keV | 【517.1(5) keV】 | 670(60) ns |  |  | (9+) |  |  |
  - [네오디뮴 동위 원소] raw `519.43(17) keV` (줄 35, 뒤): | ¹³⁷ᵐNd | 【519.43(17) keV】 | 519.43(17) keV | 519.43(17) keV | 1.60(15) s | IT | ¹³⁷Nd | (11/2-) |  |  |
  - [네오디뮴 동위 원소] raw `519.43(17) keV` (줄 35, 뒤): | ¹³⁷ᵐNd | 519.43(17) keV | 【519.43(17) keV】 | 519.43(17) keV | 1.60(15) s | IT | ¹³⁷Nd | (11/2-) |  |  |
  - [네오디뮴 동위 원소] raw `519.43(17) keV` (줄 35, 뒤): | ¹³⁷ᵐNd | 519.43(17) keV | 519.43(17) keV | 【519.43(17) keV】 | 1.60(15) s | IT | ¹³⁷Nd | (11/2-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 8.13105e-14: [Isotopes of yttrium] raw `507.50(13) keV` (줄 36, 두 언어 쪽): | ⁸²ᵐ²Y | 【507.50(13) keV】 | 507.50(13) keV | 507.50(13) keV | 1993 | 148(6) ns | IT | ⁸²Y | 6+ |  |
  - base 7.9484e-14: [Isotopes of yttrium] raw `496.10(11) keV` (줄 89, 두 언어 쪽): | ⁹⁸ᵐ³Y | 【496.10(11) keV】 | 496.10(11) keV | 496.10(11) keV | 2017 | 6.90(54) μs | IT | ⁹⁸Y | (4)− |  |
  - base 8.90137e-14: [Isotopes of yttrium] raw `555.58(5) keV` (줄 63, 두 언어 쪽): | ⁹¹ᵐY | 【555.58(5) keV】 | 555.58(5) keV | 555.58(5) keV | 1943 | 49.71(4) min | IT | ⁹¹Y | 9/2+ |  |
  - base 7.46134e-14: [Isotopes of yttrium] raw `465.7(7) keV` (줄 86, 두 언어 쪽): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-133

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 밀도, base 7160, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `7.16 g/cm³` (줄 19, 뒤):   - 액체(녹는점)일 때: 【7.16 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 6973: [Ytterbium] raw `6.973 g/cm³` (줄 73, 두 언어 쪽): …bium crystallizes in the face-centered cubic system. Ytterbium has a density of 【6.973 g/cm³】, which is significantly lower than those of the neighboring lanthanides, thuliu…
  - base 6903: [Ytterbium] raw `6.903 g/cm³` (줄 67, 두 언어 쪽): …z/cu in]) has a body-centered cubic crystalline structure. The alpha allotrope (【6.903 g/cm³】 [3.990 oz/cu in]) has a hexagonal crystalline structure and is stable at low te…
  - base 6773: [Praseodymium] raw `6.773 g/cm³` (줄 19, 한쪽 언어 쪽):   - Density (at 20° C): 【6.773 g/cm³】
  - base 6570: [Ytterbium] raw `6.57 g/cm³` (줄 67, 두 언어 쪽): … a face-centered cubic crystal structure. The high-temperature gamma allotrope (【6.57 g/cm³】 [3.80 oz/cu in]) has a body-centered cubic crystalline structure. The alpha all…
  - base 6500: [Praseodymium] raw `6.50 g/cm³` (줄 20, 한쪽 언어 쪽):   - when liquid (at m.p.): 【6.50 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-134

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 2.6207e-09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `2.6207 nm` (줄 30, 뒤):   - 격자 상수: ar = 0.89834 nm α = 23.307° ah = 0.36291 nm ch = 【2.6207 nm】 (20 °C에서)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-135

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 열전도율, base 17.2, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `17.2 W/(m·K)` (줄 32, 뒤):   - 열전도율: 【17.2 W/(m·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 16.9: [Thulium] raw `16.9 W/(m⋅K)` (줄 36, 두 언어 쪽):   - Thermal conductivity: 【16.9 W/(m⋅K)】
  - base 16.4: [Lutetium] raw `16.4 W/(m⋅K)` (줄 36, 두 언어 쪽):   - Thermal conductivity: 【16.4 W/(m⋅K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-136

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 5904, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `1.64(3) h` (줄 41, 뒤): | ¹⁴⁷Tb | 65 | 82 | 146.924045(13) | 【1.64(3) h】 | β⁺ | ¹⁴⁷Gd | 1/2+# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5760: [Europium] raw `96 minutes` (줄 163, 한쪽 언어 쪽): … of 9.3116 hours; another isomer of ¹⁵²Eu at 147.9 keV has a half-life of about 【96 minutes】. Most neutron-deficient europium isotopes decay towards isotopes of samarium by…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-137

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 속도, base 2830, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `2830 m/s` (줄 37, 뒤):   - 음속 (얇은 막대): 【2830 m/s】 (20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2710: [Dysprosium] raw `2710 m/s` (줄 43, 두 언어 쪽):   - Speed of sound thin rod: 【2710 m/s】 (at 20 °C)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-138

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 249.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `4.16(4) min` (줄 48, 뒤): | ¹⁴⁹ᵐTb | 35.78(13) keV | 35.78(13) keV | 35.78(13) keV | 【4.16(4) min】 | β⁺ (99.97%) | ¹⁴⁹Gd | 11/2- |  |  |
  - [터븀 동위 원소] raw `4.16(4) min` (줄 49, 뒤): | ¹⁴⁹ᵐTb | 35.78(13) keV | 35.78(13) keV | 35.78(13) keV | 【4.16(4) min】 | α (0.022%) | ¹⁴⁵Eu | 11/2- |  |  |
  - [터븀 동위 원소] raw `4.2(1) min` (줄 61, 뒤): | ¹⁵²ᵐ²Tb | 501.74(19) keV | 501.74(19) keV | 501.74(19) keV | 【4.2(1) min】 | IT (78.8%) | ¹⁵²Tb | 8+ |  |  |
  - [터븀 동위 원소] raw `4.2(1) min` (줄 62, 뒤): | ¹⁵²ᵐ²Tb | 501.74(19) keV | 501.74(19) keV | 501.74(19) keV | 【4.2(1) min】 | β⁺ (21.2%) | ¹⁵²Gd | 8+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [Ytterbium] `4.2`: … 32 days), which is created along with the short-lived ¹⁷⁵Yb isotope (half-life 【4.2】 days) by neutron activation during the irradiation of ytterbium in nuclear reac…

### R-ko-139

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 2.05031e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `127.97(11) keV` (줄 27, 뒤): | ¹³³ᵐ¹Nd | 【127.97(11) keV】 | 127.97(11) keV | 127.97(11) keV | ~70 s | β⁺ | ¹³³Pr | (1/2)+ |  |  |
  - [네오디뮴 동위 원소] raw `127.97(11) keV` (줄 27, 뒤): | ¹³³ᵐ¹Nd | 127.97(11) keV | 【127.97(11) keV】 | 127.97(11) keV | ~70 s | β⁺ | ¹³³Pr | (1/2)+ |  |  |
  - [네오디뮴 동위 원소] raw `127.97(11) keV` (줄 27, 뒤): | ¹³³ᵐ¹Nd | 127.97(11) keV | 127.97(11) keV | 【127.97(11) keV】 | ~70 s | β⁺ | ¹³³Pr | (1/2)+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-140

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 열팽창, base 1.27e-05, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `12.7 µm/(m·K)` (줄 31, 뒤):   - 열팽창: (실온) (α, poly) 【12.7 µm/(m·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.33e-05: [Thulium] raw `13.3 µm/(m⋅K)` (줄 35, 두 언어 쪽):   - Thermal expansion: poly: 【13.3 µm/(m⋅K)】 (at r.t.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-141

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 24.1, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `24.1(5) s` (줄 39, 뒤): | ¹⁴⁶ᵐ¹Tb | 150(100)# keV | 150(100)# keV | 150(100)# keV | 【24.1(5) s】 | β⁺ | ¹⁴⁶Gd | 5- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-142

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 5.73259e-15, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `35.78(13) keV` (줄 48, 뒤): | ¹⁴⁹ᵐTb | 【35.78(13) keV】 | 35.78(13) keV | 35.78(13) keV | 4.16(4) min | β⁺ (99.97%) | ¹⁴⁹Gd | 11/2- |  |  |
  - [터븀 동위 원소] raw `35.78(13) keV` (줄 48, 뒤): | ¹⁴⁹ᵐTb | 35.78(13) keV | 【35.78(13) keV】 | 35.78(13) keV | 4.16(4) min | β⁺ (99.97%) | ¹⁴⁹Gd | 11/2- |  |  |
  - [터븀 동위 원소] raw `35.78(13) keV` (줄 48, 뒤): | ¹⁴⁹ᵐTb | 35.78(13) keV | 35.78(13) keV | 【35.78(13) keV】 | 4.16(4) min | β⁺ (99.97%) | ¹⁴⁹Gd | 11/2- |  |  |
  - [터븀 동위 원소] raw `35.78(13) keV` (줄 49, 뒤): | ¹⁴⁹ᵐTb | 【35.78(13) keV】 | 35.78(13) keV | 35.78(13) keV | 4.16(4) min | α (0.022%) | ¹⁴⁵Eu | 11/2- |  |  |
  - [터븀 동위 원소] raw `35.78(13) keV` (줄 49, 뒤): | ¹⁴⁹ᵐTb | 35.78(13) keV | 【35.78(13) keV】 | 35.78(13) keV | 4.16(4) min | α (0.022%) | ¹⁴⁵Eu | 11/2- |  |  |
  - [터븀 동위 원소] raw `35.78(13) keV` (줄 49, 뒤): | ¹⁴⁹ᵐTb | 35.78(13) keV | 35.78(13) keV | 【35.78(13) keV】 | 4.16(4) min | α (0.022%) | ¹⁴⁵Eu | 11/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-143

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 1004.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `731°C` (줄 61, 뒤): 사마륨은 희토류에 속하는 원소로, 그 단단함이나 밀도가 아연과 비슷하다. 란타넘족 원소 중에서는 이터븀과 유로퓸에 이어 반응성이 세 번째로 크며, 이는 광석에서 사마륨을 분리하기가 쉬운 원인이기도 하다. 일반적인 조건에서는 삼방정계 구조(α 구조)를 가지며, 【731°C】 이상의 고온으로 가열하면 육방정계 구조로 전환된다. 전환 온도는 불순물에 따라 달라지기도 한다. 922°C 이상으로 가열하면 다시 결정 구조가 바뀌어 체심 입방정계 구조가 된다. 실온에서는 상자성이며 14.8K 이하로 냉각시키면 반강자성을 띤다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 973: [Samarium–cobalt magnet] raw `973 K` (줄 13, 한쪽 언어 쪽): …tures from 250 °C (523 K) to 550 °C (823 K) and Curie temperatures from 700 °C (【973 K】) to 800 °C (1,070 K).
  - base 1068: [Praseodymium] raw `1,068 K` (줄 66, 한쪽 언어 쪽): …rystal structure at room temperature, called the alpha phase (α-Pr). At 795 °C (【1,068 K】) it transforms to a different allotrope that has a body-centered cubic structur…
  - base 1095: [Europium] raw `1,095 K` (줄 63, 한쪽 언어 쪽): …temperature it has a density of about 5.24 g/cm³ and a melting point of 822 °C (【1,095 K】).
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-144

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 684, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `11.4(2) min` (줄 57, 뒤): | ¹⁵²Nd | 60 | 92 | 151.924682(26) | 【11.4(2) min】 | β⁻ | ¹⁵²Pm | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 618: [Isotopes of yttrium] raw `10.3(1) min` (줄 71, 두 언어 쪽): | ⁹⁵Y | 39 | 56 | 94.9128197(73) | 1959 | 【10.3(1) min】 | β⁻ | ⁹⁵Zr | 1/2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-145

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 18144, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `5.04(9) h` (줄 36, 뒤): | ¹³⁸Nd | 60 | 78 | 137.911950(13) | 【5.04(9) h】 | β⁺ | ¹³⁸Pr | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 17496: [Isotopes of yttrium] raw `4.86(20) h` (줄 44, 두 언어 쪽): | ⁸⁵ᵐ¹Y | 19.68(17) keV | 19.68(17) keV | 19.68(17) keV | 1963 | 【4.86(20) h】 | β⁺ | ⁸⁵Sr | (9/2)+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-146

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 밀도, base 9066, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `9.066 g/cm³` (줄 18, 뒤):   - 밀도 (상온 근처): 【9.066 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 9300: [Lutetium] raw `9.3 g/cm³` (줄 20, 두 언어 쪽):   - when liquid (at m.p.): 【9.3 g/cm³】
  - base 8550: [Dysprosium] raw `8.550 g/cm³` (줄 19, 두 언어 쪽):   - Density (at 20° C): 【8.550 g/cm³】
  - base 9810: [Lutetium] raw `9.81 g/cm³` (줄 116, 두 언어 쪽): Lutetium tantalate (LuTaO4) is the densest known stable white material (density 【9.81 g/cm³】) and therefore is an ideal host for X-ray phosphors. The only denser white mate…
  - base 8370: [Dysprosium] raw `8.37 g/cm³` (줄 20, 두 언어 쪽):   - when liquid (at m.p.): 【8.37 g/cm³】
  - base 10000: [Lutetium] raw `10 g/cm³` (줄 116, 두 언어 쪽): …y phosphors. The only denser white material is thorium dioxide, with density of 【10 g/cm³】, but the thorium it contains is radioactive.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-147

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 2.29432e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `1432(5) keV` (줄 64, 뒤): | ¹⁵⁶ᵐNd | 【1432(5) keV】 | 1432(5) keV | 1432(5) keV | 135 ns |  |  | 5- |  |  |
  - [네오디뮴 동위 원소] raw `1432(5) keV` (줄 64, 뒤): | ¹⁵⁶ᵐNd | 1432(5) keV | 【1432(5) keV】 | 1432(5) keV | 135 ns |  |  | 5- |  |  |
  - [네오디뮴 동위 원소] raw `1432(5) keV` (줄 64, 뒤): | ¹⁵⁶ᵐNd | 1432(5) keV | 1432(5) keV | 【1432(5) keV】 | 135 ns |  |  | 5- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.46735e-13: [Isotopes of yttrium] raw `1540(9) keV` (줄 74, 두 언어 쪽): | ⁹⁶ᵐ¹Y | 【1540(9) keV】 | 1540(9) keV | 1540(9) keV | 1975 | 9.6(2) s | β⁻ | ⁹⁶Zr | 8+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-148

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 온도, base 2067, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `2067 K` (줄 17, 뒤):   - 끓는점: 【2067 K】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1925: [Lutetium] raw `1925 K` (줄 17, 두 언어 쪽):   - Melting point: 【1925 K】 ​(1652 °C, ​3006 °F)
  - base 2223: [Thulium] raw `2223 K` (줄 18, 두 언어 쪽):   - Boiling point: 【2223 K】 ​(1950 °C, ​3542 °F)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-149

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 19.4, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `19.4(27) s` (줄 92, 뒤): | ¹⁶⁷Tb | 65 | 102 | 166.94005(43)# | 【19.4(27) s】 | β⁻ | ¹⁶⁷Dy | 3/2+# |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-150

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 4.4893e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `280.2(10) keV` (줄 23, 뒤): | ¹⁴²ᵐ¹Tb | 【280.2(10) keV】 | 280.2(10) keV | 280.2(10) keV | 303(17) ms | IT (99.5%) | ¹⁴²Tb | (5-) |  |  |
  - [터븀 동위 원소] raw `280.2(10) keV` (줄 23, 뒤): | ¹⁴²ᵐ¹Tb | 280.2(10) keV | 【280.2(10) keV】 | 280.2(10) keV | 303(17) ms | IT (99.5%) | ¹⁴²Tb | (5-) |  |  |
  - [터븀 동위 원소] raw `280.2(10) keV` (줄 23, 뒤): | ¹⁴²ᵐ¹Tb | 280.2(10) keV | 280.2(10) keV | 【280.2(10) keV】 | 303(17) ms | IT (99.5%) | ¹⁴²Tb | (5-) |  |  |
  - [터븀 동위 원소] raw `280.2(10) keV` (줄 24, 뒤): | ¹⁴²ᵐ¹Tb | 【280.2(10) keV】 | 280.2(10) keV | 280.2(10) keV | 303(17) ms | β⁺ (0.5%) | ¹⁴²Gd | (5-) |  |  |
  - [터븀 동위 원소] raw `280.2(10) keV` (줄 24, 뒤): | ¹⁴²ᵐ¹Tb | 280.2(10) keV | 【280.2(10) keV】 | 280.2(10) keV | 303(17) ms | β⁺ (0.5%) | ¹⁴²Gd | (5-) |  |  |
  - [터븀 동위 원소] raw `280.2(10) keV` (줄 24, 뒤): | ¹⁴²ᵐ¹Tb | 280.2(10) keV | 280.2(10) keV | 【280.2(10) keV】 | 303(17) ms | β⁺ (0.5%) | ¹⁴²Gd | (5-) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.26467e-14: [Isotopes of yttrium] raw `266.18(10) keV` (줄 46, 두 언어 쪽): | ⁸⁵ᵐ²Y | 【266.18(10) keV】 | 266.18(10) keV | 266.18(10) keV | 1977 | 178(7) ns | IT | ⁸⁵Y | (5/2)− |  |
  - base 4.80653e-14: [Isotopes of yttrium] raw `300 keV` (줄 26, 두 언어 쪽): | ⁷⁸ᵐY | ~【300 keV】 | ~300 keV | ~300 keV | 1998 | 5.8(6) s | β⁺ | ⁷⁸Sr | (5+) |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-151

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 62, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `62.0(8) s` (줄 45, 뒤): | ¹⁴¹ᵐNd | 756.51(5) keV | 756.51(5) keV | 756.51(5) keV | 【62.0(8) s】 | IT (99.95%) | ¹⁴¹Nd | 11/2- |  |  |
  - [네오디뮴 동위 원소] raw `62.0(8) s` (줄 46, 뒤): | ¹⁴¹ᵐNd | 756.51(5) keV | 756.51(5) keV | 756.51(5) keV | 【62.0(8) s】 | β⁺ (0.05%) | ¹⁴¹Pr | 11/2- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-152

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 8964, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `2.49(3) h` (줄 44, 뒤): | ¹⁴¹Nd | 60 | 81 | 140.909610(4) | 【2.49(3) h】 | β⁺ | ¹⁴¹Pr | 3/2+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 8395.2: [Dysprosium] raw `2.332 h` (줄 53, 두 언어 쪽): …table ¹⁶²Dy 25.475% stable ¹⁶³Dy 24.896% stable ¹⁶⁴Dy 28.26% stable ¹⁶⁵Dy synth 【2.332 h】 β⁻ ¹⁶⁵Ho ¹⁶⁶Dy synth 3.40 d β⁻ ¹⁶⁶Ho
  - base 9648: [Isotopes of yttrium] raw `2.68(5) h` (줄 43, 두 언어 쪽): | ⁸⁵Y | 39 | 46 | 84.916433(20) | 1952 | 【2.68(5) h】 | β⁺ | ⁸⁵Sr | (1/2)− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-153

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 밀도, base 4240, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `4.24 g/cm³` (줄 19, 뒤):   - 액체(녹는점)일 때: 【4.24 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-154

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 2.83e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `28.3 GPa` (줄 35, 뒤):   - 전단 탄성 계수: 【28.3 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 2.79e+10: [Lanthanum] raw `27.9 GPa` (줄 42, 한쪽 언어 쪽):   - Bulk modulus: α form: 【27.9 GPa】
  - base 2.88e+10: [Praseodymium] raw `28.8 GPa` (줄 42, 한쪽 언어 쪽):   - Bulk modulus: 【28.8 GPa】
  - base 2.72e+10: [Lutetium] raw `27.2 GPa` (줄 40, 두 언어 쪽):   - Shear modulus: 【27.2 GPa】
  - base 3.05e+10: [Thulium] raw `30.5 GPa` (줄 41, 두 언어 쪽):   - Shear modulus: 【30.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-155

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 112.2, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `1.87(5) min` (줄 42, 뒤): | ¹⁴⁷ᵐTb | 50.6(9) keV | 50.6(9) keV | 50.6(9) keV | 【1.87(5) min】 | β⁺ | ¹⁴⁷Gd | (11/2)- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-156

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 812160, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `9.4 d` (줄 47, 뒤): …DP ¹⁶⁰Er 인공 28.58 h ε 0.330 ¹⁶⁰Ho ¹⁶²Er 0.14% 안정 ¹⁶⁴Er 1.61% 안정 ¹⁶⁵Er 인공 10.36 h ε 0.376 ¹⁶⁵Ho ¹⁶⁶Er 33.6% 안정 ¹⁶⁷Er 22.95% 안정 ¹⁶⁸Er 26.8% 안정 ¹⁶⁹Er 인공 【9.4 d】 β⁻ 0.351 ¹⁶⁹Tm ¹⁷⁰Er 14.9% 안정 ¹⁷¹Er 인공 7.516 h β⁻ 1.490 ¹⁷¹Tm ¹⁷²Er 인공 49.3 h β⁻ 0.891 ¹⁷²Tm
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 799200: [Thulium] raw `9.25 d` (줄 52, 두 언어 쪽): …in isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁶⁷Tm synth 【9.25 d】 ε ¹⁶⁷Er ¹⁶⁸Tm synth 93.1 d β⁺ ¹⁶⁸Er ¹⁶⁹Tm 100% stable ¹⁷⁰Tm synth 128.6 d β⁻ ¹⁷…
  - base 777600: [Lutetium] raw `9 days` (줄 80, 두 언어 쪽): …s. All of the remaining radioactive isotopes have half-lives that are less than 【9 days】, and the majority of these have half-lives that are less than half an hour. Iso…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-157

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 93.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `1.56(10) min` (줄 25, 뒤): | ¹³²Nd | 60 | 72 | 131.923321(26) | 【1.56(10) min】 | β⁺ | ¹³²Pr | 0+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-158

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 8620, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `8.62 kJ/mol` (줄 20, 뒤):   - 융해열: 【8.62 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 9210: [Europium] raw `9.21 kJ/mol` (줄 21, 한쪽 언어 쪽):   - Heat of fusion: 【9.21 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-159

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 4.12e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `41.2 GPa` (줄 37, 뒤):   - 부피 탄성 계수: 【41.2 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.05e+10: [Dysprosium] raw `40.5 GPa` (줄 42, 두 언어 쪽):   - Bulk modulus: 【40.5 GPa】
  - base 4.45e+10: [Thulium] raw `44.5 GPa` (줄 42, 두 언어 쪽):   - Bulk modulus: 【44.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-160

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 330, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `5.5(5) min` (줄 32, 뒤): | ¹³⁵ᵐNd | 65.0(2) keV | 65.0(2) keV | 65.0(2) keV | 【5.5(5) min】 | β⁺ | ¹³⁵Pr | (1/2+) |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-161

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 압력, base 6.99e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `69.9 GPa` (줄 34, 뒤):   - 영률: 【69.9 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 6.86e+10: [Lutetium] raw `68.6 GPa` (줄 39, 두 언어 쪽):   - Young's modulus: 【68.6 GPa】
  - base 7.4e+10: [Thulium] raw `74.0 GPa` (줄 40, 두 언어 쪽):   - Young's modulus: 【74.0 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-162

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 37296, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [어븀] raw `10.36 h` (줄 47, 뒤):   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁶⁰Er 인공 28.58 h ε 0.330 ¹⁶⁰Ho ¹⁶²Er 0.14% 안정 ¹⁶⁴Er 1.61% 안정 ¹⁶⁵Er 인공 【10.36 h】 ε 0.376 ¹⁶⁵Ho ¹⁶⁶Er 33.6% 안정 ¹⁶⁷Er 22.95% 안정 ¹⁶⁸Er 26.8% 안정 ¹⁶⁹Er 인공 9.4 d β⁻ 0.351 ¹⁶⁹Tm ¹⁷⁰Er 14.9% 안정 ¹⁷¹Er 인공 7.516 h β⁻ 1.490 ¹⁷¹Tm ¹⁷²Er 인공 49.…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 36648: [Isotopes of yttrium] raw `10.18(8) h` (줄 67, 두 언어 쪽): | ⁹³Y | 39 | 54 | 92.909578(11) | 1948 | 【10.18(8) h】 | β⁻ | ⁹³Zr | 1/2− |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-163

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 6.24672e+06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `72.3(2) d` (줄 85, 뒤): | ¹⁶⁰Tb | 65 | 95 | 159.9271676(27) | 【72.3(2) d】 | β⁻ | ¹⁶⁰Dy | 3- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-164

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 에너지, base 7.32195e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [터븀 동위 원소] raw `457(29) keV` (줄 52, 뒤): | ¹⁵⁰ᵐTb | 【457(29) keV】 | 457(29) keV | 457(29) keV | 5.8(2) min | β⁺ | ¹⁵⁰Gd | 9+ |  |  |
  - [터븀 동위 원소] raw `457(29) keV` (줄 52, 뒤): | ¹⁵⁰ᵐTb | 457(29) keV | 【457(29) keV】 | 457(29) keV | 5.8(2) min | β⁺ | ¹⁵⁰Gd | 9+ |  |  |
  - [터븀 동위 원소] raw `457(29) keV` (줄 52, 뒤): | ¹⁵⁰ᵐTb | 457(29) keV | 457(29) keV | 【457(29) keV】 | 5.8(2) min | β⁺ | ¹⁵⁰Gd | 9+ |  |  |
  - [터븀 동위 원소] raw `457(29) keV` (줄 53, 뒤): | ¹⁵⁰ᵐTb | 【457(29) keV】 | 457(29) keV | 457(29) keV | 5.8(2) min | IT (드묾) | ¹⁵⁰Tb | 9+ |  |  |
  - [터븀 동위 원소] raw `457(29) keV` (줄 53, 뒤): | ¹⁵⁰ᵐTb | 457(29) keV | 【457(29) keV】 | 457(29) keV | 5.8(2) min | IT (드묾) | ¹⁵⁰Tb | 9+ |  |  |
  - [터븀 동위 원소] raw `457(29) keV` (줄 53, 뒤): | ¹⁵⁰ᵐTb | 457(29) keV | 457(29) keV | 【457(29) keV】 | 5.8(2) min | IT (드묾) | ¹⁵⁰Tb | 9+ |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 7.46134e-14: [Isotopes of yttrium] raw `465.7(7) keV` (줄 86, 두 언어 쪽): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ …
  - base 7.9484e-14: [Isotopes of yttrium] raw `496.10(11) keV` (줄 89, 두 언어 쪽): | ⁹⁸ᵐ³Y | 【496.10(11) keV】 | 496.10(11) keV | 496.10(11) keV | 2017 | 6.90(54) μs | IT | ⁹⁸Y | (4)− |  |
  - base 8.13105e-14: [Isotopes of yttrium] raw `507.50(13) keV` (줄 36, 두 언어 쪽): | ⁸²ᵐ²Y | 【507.50(13) keV】 | 507.50(13) keV | 507.50(13) keV | 1993 | 148(6) ns | IT | ⁸²Y | 6+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-165

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 길이, base 6.8e-09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [사마륨] raw `6.8` (줄 102, 뒤): - 사마륨-149는 중성자를 잘 흡수하는 성질이 있으므로 원자로의 제어봉에 들어간다. X선 레이저의 제조에도 사용되는데, 이 경우 【6.8】~7.3나노미터의 파장을 가진 X선이 50피코초 동안 방출되므로 다양한 분야에 응용된다.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-166

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 시간, base 1.35e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [네오디뮴 동위 원소] raw `135 ns` (줄 64, 뒤): | ¹⁵⁶ᵐNd | 1432(5) keV | 1432(5) keV | 1432(5) keV | 【135 ns】 |  |  | 5- |  |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.253e-07: [Isotopes of yttrium] raw `125.3(55) ns` (줄 50, 두 언어 쪽): | ⁸⁶ᵐ²Y | 302.18(9) keV | 302.18(9) keV | 302.18(9) keV | 2000 | 【125.3(55) ns】 | IT | ⁸⁶Y | 6+ |  |
  - base 1.48e-07: [Isotopes of yttrium] raw `148(6) ns` (줄 36, 두 언어 쪽): | ⁸²ᵐ²Y | 507.50(13) keV | 507.50(13) keV | 507.50(13) keV | 1993 | 【148(6) ns】 | IT | ⁸²Y | 6+ |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-ko-167

- 분야 rare_earth, 언어 ko, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 365000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [이트륨] raw `365 kJ/mol` (줄 21, 뒤):   - 기화열: 【365 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 400000: [Lanthanum] raw `400 kJ/mol` (줄 22, 한쪽 언어 쪽):   - Heat of vaporization: 【400 kJ/mol】
  - base 331000: [Praseodymium] raw `331 kJ/mol` (줄 22, 한쪽 언어 쪽):   - Heat of vaporization: 【331 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-001

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 1.55759e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `972.17(20) keV` (줄 91, 뒤): | ⁹⁸ᵐ⁵Y | 【972.17(20) keV】 | 972.17(20) keV | 972.17(20) keV | 1970 | 450(150) ns | IT | ⁹⁸Y | (8+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `972.17(20) keV` (줄 91, 뒤): | ⁹⁸ᵐ⁵Y | 972.17(20) keV | 【972.17(20) keV】 | 972.17(20) keV | 1970 | 450(150) ns | IT | ⁹⁸Y | (8+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `972.17(20) keV` (줄 91, 뒤): | ⁹⁸ᵐ⁵Y | 972.17(20) keV | 972.17(20) keV | 【972.17(20) keV】 | 1970 | 450(150) ns | IT | ⁹⁸Y | (8+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.45633e-13: [이트륨 동위 원소] raw `908.97(3) keV` (줄 45, 두 언어 쪽): | ⁸⁹ᵐY | 【908.97(3) keV】 | 908.97(3) keV | 908.97(3) keV | 15.663(5) s | IT | ⁸⁹Y | 9/2+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-002

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.26133e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `75.95894(32)` (줄 18, 머리글): | ⁷⁶Y | 39 | 37 | 【75.95894(32)】# | 2001 | 28(9) ms | β⁺? | ⁷⁶Sr | 1−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `75.95894(32)` (줄 19, 머리글): | ⁷⁶Y | 39 | 37 | 【75.95894(32)】# | 2001 | 28(9) ms | p? | ⁷⁵Sr | 1−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `75.95894(32)` (줄 20, 머리글): | ⁷⁶Y | 39 | 37 | 【75.95894(32)】# | 2001 | 28(9) ms | β⁺, p? | ⁷⁵Rb | 1−# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-003

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 출력, base 1500, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `1.5 kW` (줄 174, 뒤): …l as the Yb-doped fibers. Fabrication of Low NA, Large Mode Area fibers enable achievement of near perfect beam qualities (M2<1.1) at power levels of 【1.5 kW】 to greater than 2 kW at ~1064 nm in a broadband configuration. Ytterbium-doped LMA fibers also have the advantages of a larger mode field diameter, w…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `1.5`: | ⁹¹ᵐY | 555.58(5) keV | 555.58(5) keV | 555.58(5) keV | 49.71(4) min | β⁻ (【1.5】%) | ⁹¹Zr | 9/2+ |  |  |

### R-en-004

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 4.41806e+13, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `1.40×10⁶ y` (줄 53, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁵⁴Dy synth 【1.40×10⁶ y】 α ¹⁵⁰Gd ¹⁵⁶Dy 0.056% stable ¹⁵⁸Dy 0.095% stable ¹⁵⁹Dy synth 144.4 d ε ¹⁵⁹Tb ¹⁶⁰Dy 2.329% stable ¹⁶¹Dy 18.8889999999% stable ¹⁶²Dy 25.475% stable ¹⁶³D…
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `1.40×10⁶ years` (줄 106, 뒤): Twenty-nine radioisotopes have been synthesized, ranging in atomic mass from 138 to 173. The most stable of these is ¹⁵⁴Dy, with a half-life of 【1.40×10⁶ years】, followed by ¹⁵⁹Dy with a half-life of 144.4 days. As a general rule, isotopes that are lighter than the stable isotopes tend to decay primarily by β…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-005

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.5428e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `92.909578(11)` (줄 67, 머리글): | ⁹³Y | 39 | 54 | 【92.909578(11)】 | 1948 | 10.18(8) h | β⁻ | ⁹³Zr | 1/2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-006

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 1.07346e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `67.0(2) keV` (줄 41, 뒤): | ⁸⁴ᵐ¹Y | 【67.0(2) keV】 | 67.0(2) keV | 67.0(2) keV | 1976 | 4.6(2) s | β⁺ | ⁸⁴Sr | 1+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `67.0(2) keV` (줄 41, 뒤): | ⁸⁴ᵐ¹Y | 67.0(2) keV | 【67.0(2) keV】 | 67.0(2) keV | 1976 | 4.6(2) s | β⁺ | ⁸⁴Sr | 1+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `67.0(2) keV` (줄 41, 뒤): | ⁸⁴ᵐ¹Y | 67.0(2) keV | 67.0(2) keV | 【67.0(2) keV】 | 1976 | 4.6(2) s | β⁺ | ⁸⁴Sr | 1+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.04141e-14: [네오디뮴 동위 원소] raw `65.0(2) keV` (줄 32, 한쪽 언어 쪽): | ¹³⁵ᵐNd | 【65.0(2) keV】 | 65.0(2) keV | 65.0(2) keV | 5.5(5) min | β⁺ | ¹³⁵Pr | (1/2+) |  |  |
  - base 9.93029e-15: [이트륨 동위 원소] raw `61.98(11) keV` (줄 26, 두 언어 쪽): | ⁸³ᵐY | 【61.98(11) keV】 | 61.98(11) keV | 61.98(11) keV | 2.85(2) min | β⁺ (60%) | ⁸³Sr | (3/2-) |  |  …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-007

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 압력, base 4.5e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `450 bars` (줄 149, 뒤): …her materials and act as a catalyst. Fibers of dysprosium oxide fluoride can be produced by heating an aqueous solution of DyBr3 and NaF to 450 °C at 【450 bars】 for 17 hours. This material is remarkably robust, surviving over 100 hours in various aqueous solutions at temperatures exceeding 400 °C without redi…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-008

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 0.025, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `25(5) ms` (줄 125, 뒤): | ¹⁰⁹Y | 39 | 70 | 108.96513(75)# | 2010 | 【25(5) ms】 | β⁻ | ¹⁰⁹Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `25(5) ms` (줄 126, 뒤): | ¹⁰⁹Y | 39 | 70 | 108.96513(75)# | 2010 | 【25(5) ms】 | β⁻, n? | ¹⁰⁸Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `25(5) ms` (줄 127, 뒤): | ¹⁰⁹Y | 39 | 70 | 108.96513(75)# | 2010 | 【25(5) ms】 | β⁻, 2n? | ¹⁰⁷Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [툴륨] `25`:   - 전기 음성도 (폴링 척도): 1.【25】
  - [툴륨] `25`:   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁶⁷Tm 인공 9.【25】 d ε 0.748 ¹⁶⁷Er ¹⁶⁸Tm 인공 93.1 d ε 1.679 ¹⁶⁸Er ¹⁶⁹Tm 100% 안정 ¹⁷⁰Tm 인공 128.6 d β⁻…
  - [디스프로슘] `25`: … 2.947 ¹⁵⁰Gd ¹⁵⁶Dy 0.06% 안정 ¹⁵⁸Dy 0.10% 안정 ¹⁶⁰Dy 2.34% 안정 ¹⁶¹Dy 18.91% 안정 ¹⁶²Dy 【25】.51% 안정 ¹⁶³Dy 24.90% 안정 ¹⁶⁴Dy 28.18% 안정
  - [이트륨 동위 원소] `25`: | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 268(【25】) ns |  |  | 4- |  |  |
  - [이트륨 동위 원소] `25`: | ⁹⁶Y | 39 | 57 | 95.915891(【25】) | 5.34(5) s | β⁻ | ⁹⁶Zr | 0- |  |  |

### R-en-009

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 11613.6, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `3.226(11) h` (줄 60, 뒤): | ⁹⁰ᵐY | 682.01(5) keV | 682.01(5) keV | 682.01(5) keV | 1961 | 【3.226(11) h】 | IT | ⁹⁰Y | 7+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `3.226(11) h` (줄 61, 뒤): | ⁹⁰ᵐY | 682.01(5) keV | 682.01(5) keV | 682.01(5) keV | 1961 | 【3.226(11) h】 | β⁻ (0.0018%) | ⁹⁰Zr | 7+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 11484: [이트륨 동위 원소] raw `3.19(6) h` (줄 47, 두 언어 쪽): | ⁹⁰ᵐY | 681.67(10) keV | 681.67(10) keV | 681.67(10) keV | 【3.19(6) h】 | IT (99.99%) | ⁹⁰Y | 7+ |  |  |
  - base 12528: [터븀 동위 원소] raw `3.48(16) h` (줄 50, 한쪽 언어 쪽): | ¹⁵⁰Tb | 65 | 85 | 149.923660(8) | 【3.48(16) h】 | β⁺ (99.95%) | ¹⁵⁰Gd | (2-) |  |  |
  - base 12744: [이트륨 동위 원소] raw `3.54(1) h` (줄 52, 두 언어 쪽): | ⁹²Y | 39 | 53 | 91.908949(10) | 【3.54(1) h】 | β⁻ | ⁹²Zr | 2- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-010

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 2.6516e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1655.0(11) keV` (줄 75, 뒤): | ⁹⁶ᵐ²Y | 【1655.0(11) keV】 | 1655.0(11) keV | 1655.0(11) keV | 2017 | 181(9) ns | IT | ⁹⁶Y | (6+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1655.0(11) keV` (줄 75, 뒤): | ⁹⁶ᵐ²Y | 1655.0(11) keV | 【1655.0(11) keV】 | 1655.0(11) keV | 2017 | 181(9) ns | IT | ⁹⁶Y | (6+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1655.0(11) keV` (줄 75, 뒤): | ⁹⁶ᵐ²Y | 1655.0(11) keV | 1655.0(11) keV | 【1655.0(11) keV】 | 2017 | 181(9) ns | IT | ⁹⁶Y | (6+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-011

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.62604e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `97.9223948(85)` (줄 83, 머리글): | ⁹⁸Y | 39 | 59 | 【97.9223948(85)】 | 1970 | 548(2) ms | β⁻ (99.67%) | ⁹⁸Zr | 0− |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `97.9223948(85)` (줄 84, 머리글): | ⁹⁸Y | 39 | 59 | 【97.9223948(85)】 | 1970 | 548(2) ms | β⁻, n (0.33%) | ⁹⁷Zr | 0− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-012

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.03e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `1.03` (줄 168, 뒤): …n generate short pulses; ytterbium can also easily be incorporated into the material used to make the laser. Ytterbium lasers commonly radiate in the 【1.03】–1.12 μm band being optically pumped at wavelength 900 nm–1 μm, dependently on the host and application. The small quantum defect makes ytterbium a pr…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1e-06: [이터븀] raw `1 마이크로미터` (줄 136, 두 언어 쪽): …다. 이로 인해 이터븀은 레이저 재료에 많이 포함된다. 이터븀 레이저는 일반적으로 1.06 - 1.12 마이크로미터의 선에서 파장 900 nm~【1 마이크로미터】의 빛을 발생시킨다. (광섬유 레이저의 도핑 재료로 사용된다.)
  - base 1.12e-06: [이터븀] raw `1.12 마이크로미터` (줄 136, 두 언어 쪽): …율이고 수명이 길며 짧은 펄스광을 발생시킬 수 있다. 이로 인해 이터븀은 레이저 재료에 많이 포함된다. 이터븀 레이저는 일반적으로 1.06 - 【1.12 마이크로미터】의 선에서 파장 900 nm~1 마이크로미터의 빛을 발생시킨다. (광섬유 레이저의 도핑 재료로 사용된다.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [사마륨] `1.03`:   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁴⁴Sm 3.07% 안정 ¹⁴⁶Sm 인공 【1.03】×10⁸y α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 1.06×10¹¹y α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α…

### R-en-013

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 2844, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `47.4(4) min` (줄 48, 뒤): | ⁸⁶ᵐ¹Y | 218.21(9) keV | 218.21(9) keV | 218.21(9) keV | 1961 | 【47.4(4) min】 | IT (99.31%) | ⁸⁶Y | (8+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `47.4(4) min` (줄 49, 뒤): | ⁸⁶ᵐ¹Y | 218.21(9) keV | 218.21(9) keV | 218.21(9) keV | 1961 | 【47.4(4) min】 | β⁺ (0.69%) | ⁸⁶Sr | (8+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 2880: [이트륨 동위 원소] raw `48(1) min` (줄 35, 두 언어 쪽): | ⁸⁶ᵐ¹Y | 218.30(20) keV | 218.30(20) keV | 218.30(20) keV | 【48(1) min】 | IT (99.31%) | ⁸⁶Y | (8+) |  |  |
  - base 2982.6: [이트륨 동위 원소] raw `49.71(4) min` (줄 50, 두 언어 쪽): | ⁹¹ᵐY | 555.58(5) keV | 555.58(5) keV | 555.58(5) keV | 【49.71(4) min】 | IT (98.5%) | ⁹¹Y | 9/2+ |  |  |
  - base 3039: [네오디뮴 동위 원소] raw `50.65(33) min` (줄 33, 한쪽 언어 쪽): | ¹³⁶Nd | 60 | 76 | 135.914976(13) | 【50.65(33) min】 | β⁺ | ¹³⁶Pr | 0+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-014

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 1.22688e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `142 days` (줄 82, 뒤): … 43 known nuclear isomers, of which the most stable of them are lutetium-177m3, with a half-life of 160.4 days, and lutetium-174m with a half-life of 【142 days】; longer than the ground states of all lutetium isotopes except 173-176.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.1111e+07: [툴륨] raw `128.6 d` (줄 46, 두 언어 쪽): …Tm 인공 9.25 d ε 0.748 ¹⁶⁷Er ¹⁶⁸Tm 인공 93.1 d ε 1.679 ¹⁶⁸Er ¹⁶⁹Tm 100% 안정 ¹⁷⁰Tm 인공 【128.6 d】 β⁻ 0.968 ¹⁷⁰Yb ¹⁷¹Tm 인공 1.92 y β⁻ 0.096 ¹⁷¹Yb
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [이트륨 동위 원소] `142`: | ⁹⁷ᵐ²Y | 3523.3(4) keV | 3523.3(4) keV | 3523.3(4) keV | 【142】(8) ms |  |  | (27/2-) |  |  |
  - [터븀 동위 원소] `142`: | ¹⁴³Tb | 65 | 78 | 【142】.93512(6) | 12(1) s | β⁺ | ¹⁴³Gd | (11/2-) |  |  |
  - [네오디뮴 동위 원소] `142`: | ¹⁴³Nd | 60 | 83 | 【142】.9098143(25) | 안정 | 안정 | 안정 | 7/2- | 0.122(2) | 0.1212-0.1232 |

### R-en-015

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 2.46735e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1540(9) keV` (줄 74, 뒤): | ⁹⁶ᵐ¹Y | 【1540(9) keV】 | 1540(9) keV | 1540(9) keV | 1975 | 9.6(2) s | β⁻ | ⁹⁶Zr | 8+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1540(9) keV` (줄 74, 뒤): | ⁹⁶ᵐ¹Y | 1540(9) keV | 【1540(9) keV】 | 1540(9) keV | 1975 | 9.6(2) s | β⁻ | ⁹⁶Zr | 8+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1540(9) keV` (줄 74, 뒤): | ⁹⁶ᵐ¹Y | 1540(9) keV | 1540(9) keV | 【1540(9) keV】 | 1975 | 9.6(2) s | β⁻ | ⁹⁶Zr | 8+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.29432e-13: [네오디뮴 동위 원소] raw `1432(5) keV` (줄 64, 한쪽 언어 쪽): | ¹⁵⁶ᵐNd | 【1432(5) keV】 | 1432(5) keV | 1432(5) keV | 135 ns |  |  | 5- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-016

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.79273e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `107.96052(64)` (줄 122, 머리글): | ¹⁰⁸Y | 39 | 69 | 【107.96052(64)】# | 2010 | 30(5) ms | β⁻ | ¹⁰⁸Zr | 6−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `107.96052(64)` (줄 123, 머리글): | ¹⁰⁸Y | 39 | 69 | 【107.96052(64)】# | 2010 | 30(5) ms | β⁻, n? | ¹⁰⁷Zr | 6−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `107.96052(64)` (줄 124, 머리글): | ¹⁰⁸Y | 39 | 69 | 【107.96052(64)】# | 2010 | 30(5) ms | β⁻, 2n? | ¹⁰⁶Zr | 6−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `108.96513(75)` (줄 125, 머리글): | ¹⁰⁹Y | 39 | 70 | 【108.96513(75)】# | 2010 | 25(5) ms | β⁻ | ¹⁰⁹Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `108.96513(75)` (줄 126, 머리글): | ¹⁰⁹Y | 39 | 70 | 【108.96513(75)】# | 2010 | 25(5) ms | β⁻, n? | ¹⁰⁸Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `108.96513(75)` (줄 127, 머리글): | ¹⁰⁹Y | 39 | 70 | 【108.96513(75)】# | 2010 | 25(5) ms | β⁻, 2n? | ¹⁰⁷Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-017

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 9.51693e-15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `59.4` (줄 131, 뒤): …r to produce the isotope thulium-170, having a half-life of 128.6 days and five major emission lines of comparable intensity (at 7.4, 51.354, 52.389, 【59.4】 and 84.253 keV). These radioactive sources have a useful life of about one year, as tools in medical and dental diagnosis, as well as to detect defec…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 9.93029e-15: [이트륨 동위 원소] raw `61.98(11) keV` (줄 26, 두 언어 쪽): | ⁸³ᵐY | 【61.98(11) keV】 | 61.98(11) keV | 61.98(11) keV | 2.85(2) min | β⁺ (60%) | ⁸³Sr | (3/2-) |  |  …
  - base 1.04141e-14: [네오디뮴 동위 원소] raw `65.0(2) keV` (줄 32, 한쪽 언어 쪽): | ¹³⁵ᵐNd | 【65.0(2) keV】 | 65.0(2) keV | 65.0(2) keV | 5.5(5) min | β⁺ | ¹³⁵Pr | (1/2+) |  |  |
  - base 8.65175e-15: [터븀 동위 원소] raw `54(3) keV` (줄 75, 한쪽 언어 쪽): | ¹⁵⁶ᵐ¹Tb | 【54(3) keV】 | 54(3) keV | 54(3) keV | 24.4(10) h | IT | ¹⁵⁶Tb | (7-) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-018

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.75936e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `105.95084(54)` (줄 116, 머리글): | ¹⁰⁶Y | 39 | 67 | 【105.95084(54)】# | 1997 | 75(6) ms | β⁻ | ¹⁰⁶Zr | 2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `105.95084(54)` (줄 117, 머리글): | ¹⁰⁶Y | 39 | 67 | 【105.95084(54)】# | 1997 | 75(6) ms | β⁻, n? | ¹⁰⁵Zr | 2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `105.95084(54)` (줄 118, 머리글): | ¹⁰⁶Y | 39 | 67 | 【105.95084(54)】# | 1997 | 75(6) ms | β⁻, 2n? | ¹⁰⁴Zr | 2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `106.95494(54)` (줄 119, 머리글): | ¹⁰⁷Y | 39 | 68 | 【106.95494(54)】# | 1997 | 33.5(3) ms | β⁻ | ¹⁰⁷Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `106.95494(54)` (줄 120, 머리글): | ¹⁰⁷Y | 39 | 68 | 【106.95494(54)】# | 1997 | 33.5(3) ms | β⁻, n? | ¹⁰⁶Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `106.95494(54)` (줄 121, 머리글): | ¹⁰⁷Y | 39 | 68 | 【106.95494(54)】# | 1997 | 33.5(3) ms | β⁻, 2n? | ¹⁰⁵Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-019

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 밀도, base 6570, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `6.57 g/cm³` (줄 67, 뒤): … (6.966 g/cm³ [4.027 oz/cu in]) exists at room temperature, and it has a face-centered cubic crystal structure. The high-temperature gamma allotrope (【6.57 g/cm³】 [3.80 oz/cu in]) has a body-centered cubic crystalline structure. The alpha allotrope (6.903 g/cm³ [3.990 oz/cu in]) has a hexagonal crystalline stru…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 6900: [이터븀] raw `6.90 g/cm³` (줄 18, 두 언어 쪽):   - 밀도 (상온 근처): 【6.90 g/cm³】
  - base 6210: [이터븀] raw `6.21 g/cm³` (줄 19, 두 언어 쪽):   - 액체(녹는점)일 때: 【6.21 g/cm³】
  - base 7160: [사마륨] raw `7.16 g/cm³` (줄 19, 한쪽 언어 쪽):   - 액체(녹는점)일 때: 【7.16 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-020

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 2.01e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `2010 nm` (줄 127, 뒤): …m in the infrared and is widely used in military applications, medicine, and meteorology. Single-element thulium-doped YAG (Tm:YAG) lasers operate at 【2010 nm】. The wavelength of thulium-based lasers is very efficient for superficial ablation of tissue, with minimal coagulation depth in air or in water. This…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-021

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 온도, base 32, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `32 K` (줄 64, 뒤): … exposure to air. The metal can be cut with a knife, as it has a Mohs hardness of 2 to 3; it is malleable and ductile. Thulium is ferromagnetic below 【32 K】, antiferromagnetic between 32 and 56 K, and paramagnetic above 56 K.
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `32` (줄 64, 뒤): …be cut with a knife, as it has a Mohs hardness of 2 to 3; it is malleable and ductile. Thulium is ferromagnetic below 32 K, antiferromagnetic between 【32】 and 56 K, and paramagnetic above 56 K.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [툴륨] `32`:   - 밀도 (상온 근처): 9.【32】 g/cm³
  - [이터븀] `32`: …위체 존재비 반감기 DM DE (MeV) DP ¹⁶⁶Yb 인공 56.7 h ε 0.304 ¹⁶⁶Tm ¹⁶⁸Yb 0.13% 안정 ¹⁶⁹Yb 인공 【32】.026 d ε 0.909 ¹⁶⁹Tm ¹⁷⁰Yb 3.05% 안정 ¹⁷¹Yb 14.3% 안정 ¹⁷²Yb 21.9% 안정 ¹⁷³Yb 16.12% 안…
  - [이터븀] `32`: …를 가지는 대부분의 란타넘족 원소들과 달리 이터븀은 면심입방격자 구조를 갖는다. 이터븀의 밀도는 6.973 g/cm^(3)로 이웃한 툴륨 (9.【32】 g/cm^(3))과 루테튬 (9.841 g/cm^(3))에 비해 상당히 낮다. 밀도 뿐만 아니라 녹는점과 끓는점도 이들에 비해 상당히 낮다. …
  - [이터븀] `32`: …한다. 이들 중 ¹⁷⁴Yb가 31.8 %로 가장 존재비가 높다. 27개의 방사성 동위원소도 알려져 있으며 가장 반감기가 긴 것들은 ¹⁶⁹Yb (【32】.0 일), ¹⁷⁵Yb (4.18 일), 그리고 ¹⁶⁶Yb (56.7 시간)이다. 나머지 방사성 동위원소들은 반감기가 2시간을 넘지 않으며 대부…
  - [이터븀] `32`: 【32】일의 반감기를 가지는 ¹⁶⁹Yb는 감마선을 방출하기 때문에 방사선 촬영에 사용된다. 이 방사성 동위원소는 ¹⁷⁵Yb와 함께 원자로에서 이터븀에 …

### R-en-022

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 3.3713e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `210.42(16) keV` (줄 42, 뒤): | ⁸⁴ᵐ²Y | 【210.42(16) keV】 | 210.42(16) keV | 210.42(16) keV | 2005 | 292(10) ns | IT | ⁸⁴Y | 4− |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `210.42(16) keV` (줄 42, 뒤): | ⁸⁴ᵐ²Y | 210.42(16) keV | 【210.42(16) keV】 | 210.42(16) keV | 2005 | 292(10) ns | IT | ⁸⁴Y | 4− |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `210.42(16) keV` (줄 42, 뒤): | ⁸⁴ᵐ²Y | 210.42(16) keV | 210.42(16) keV | 【210.42(16) keV】 | 2005 | 292(10) ns | IT | ⁸⁴Y | 4− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3.49755e-14: [이트륨 동위 원소] raw `218.30(20) keV` (줄 35, 두 언어 쪽): | ⁸⁶ᵐ¹Y | 【218.30(20) keV】 | 218.30(20) keV | 218.30(20) keV | 48(1) min | IT (99.31%) | ⁸⁶Y | (8+) |  |  …
  - base 3.66097e-14: [이트륨 동위 원소] raw `228.5(1) keV` (줄 19, 두 언어 쪽): | ⁸⁰ᵐ¹Y | 【228.5(1) keV】 | 228.5(1) keV | 228.5(1) keV | 4.8(3) s |  |  | (1-) |  |  |
  - base 3.70343e-14: [네오디뮴 동위 원소] raw `231.15(5) keV` (줄 39, 한쪽 언어 쪽): | ¹³⁹ᵐ¹Nd | 【231.15(5) keV】 | 231.15(5) keV | 231.15(5) keV | 5.50(20) h | β⁺ (88.2%) | ¹³⁹Pr | 11/2- |  | …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-023

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 압력, base 7.55e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `755` (줄 43, 뒤):   - Vickers hardness: 【755】–1160 MPa
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.14e+08: [어븀] raw `814 MPa` (줄 40, 한쪽 언어 쪽):   - 브리넬 굳기: 【814 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-024

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.31079e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `78.937752(14)` (줄 28, 머리글): | ⁷⁹Y | 39 | 40 | 【78.937752(14)】 | 1992 | 14.8(6) s | β⁺ | ⁷⁹Sr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-025

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 1.38586e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `160.4 days` (줄 82, 뒤): The element also has 43 known nuclear isomers, of which the most stable of them are lutetium-177m3, with a half-life of 【160.4 days】, and lutetium-174m with a half-life of 142 days; longer than the ground states of all lutetium isotopes except 173-176.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-026

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 0.239, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `239(12) ms` (줄 108, 뒤): | ¹⁰³Y | 39 | 64 | 102.937244(12) | 1994 | 【239(12) ms】 | β⁻ (92.0%) | ¹⁰³Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `239(12) ms` (줄 109, 뒤): | ¹⁰³Y | 39 | 64 | 102.937244(12) | 1994 | 【239(12) ms】 | β⁻, n (8.0%) | ¹⁰²Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.224: [이트륨 동위 원소] raw `224(19) ms` (줄 85, 두 언어 쪽): | ¹⁰³Y | 39 | 64 | 102.93673(32)# | 【224(19) ms】 | β⁻ (91.7%) | ¹⁰³Zr | 5/2+# |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-027

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.78e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `178 pm` (줄 30, 뒤):   - Atomic radius: empirical: 【178 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1.8e-10: [이트륨] raw `180 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【180 pm】 (실험값)
  - base 1.75e-10: [툴륨] raw `175 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 【175 pm】 (실험값) 222 pm (계산값)
  - base 1.85e-10: [사마륨] raw `185 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【185 pm】 (실험값) 238 pm (계산값)
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `178`: | ⁸⁵ᵐ²Y | 266.30(20) keV | 266.30(20) keV | 266.30(20) keV | 【178】(6) ns |  |  | 5/2- |  |  |

### R-en-028

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 온도, base 723.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `450 °C` (줄 149, 뒤): …inforce other materials and act as a catalyst. Fibers of dysprosium oxide fluoride can be produced by heating an aqueous solution of DyBr3 and NaF to 【450 °C】 at 450 bars for 17 hours. This material is remarkably robust, surviving over 100 hours in various aqueous solutions at temperatures exceeding 400 °C …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 673.15: [사마륨] raw `400°C` (줄 91, 한쪽 언어 쪽): … 사마륨과 코발트의 비율은 1:5이거나 2:17인 경우가 많다. 이러한 자석은 철보다 1만배 이상 강력한 것이다. 또, 네오디뮴 자석은 300~【400°C】 가량의 온도에서 자성을 잃는데 비해 사마륨-코발트 자석은 700°C 이상의 고온에서도 자성을 잃지 않는다. 주로 소형 전동기, 헤드셋, 기타나…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-029

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.69266e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `101.9343285(44)` (줄 103, 머리글): | ¹⁰²Y | 39 | 63 | 【101.9343285(44)】 | 1983 | 360(40) ms | β⁻ (>97.4%) | ¹⁰²Zr | (5−) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `101.9343285(44)` (줄 104, 머리글): | ¹⁰²Y | 39 | 63 | 【101.9343285(44)】 | 1983 | 360(40) ms | β⁻, n (<2.6%) | ¹⁰¹Zr | (5−) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `102.937244(12)` (줄 108, 머리글): | ¹⁰³Y | 39 | 64 | 【102.937244(12)】 | 1994 | 239(12) ms | β⁻ (92.0%) | ¹⁰³Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `102.937244(12)` (줄 109, 머리글): | ¹⁰³Y | 39 | 64 | 【102.937244(12)】 | 1994 | 239(12) ms | β⁻, n (8.0%) | ¹⁰²Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-030

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 2.32, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `2.32(8) s` (줄 86, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 465.7(7) keV | 1977 | 【2.32(8) s】 | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `2.32(8) s` (줄 87, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 465.7(7) keV | 1977 | 【2.32(8) s】 | β⁻, n (3.44%) | ⁹⁷Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `2.32(8) s` (줄 88, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 465.7(7) keV | 1977 | 【2.32(8) s】 | IT? | ⁹⁸Y | (6,7)+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.4: [터븀 동위 원소] raw `2.4(2) s` (줄 17, 한쪽 언어 쪽): | ¹⁴⁰Tb | 65 | 75 | 139.94581(86) | 【2.4(2) s】 | β⁺ (99.74%) | ¹⁴⁰Gd | 5 |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-031

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 8395.2, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `2.332 h` (줄 53, 뒤): …¹⁵⁹Dy synth 144.4 d ε ¹⁵⁹Tb ¹⁶⁰Dy 2.329% stable ¹⁶¹Dy 18.8889999999% stable ¹⁶²Dy 25.475% stable ¹⁶³Dy 24.896% stable ¹⁶⁴Dy 28.26% stable ¹⁶⁵Dy synth 【2.332 h】 β⁻ ¹⁶⁵Ho ¹⁶⁶Dy synth 3.40 d β⁻ ¹⁶⁶Ho
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8964: [네오디뮴 동위 원소] raw `2.49(3) h` (줄 44, 한쪽 언어 쪽): | ¹⁴¹Nd | 60 | 81 | 140.909610(4) | 【2.49(3) h】 | β⁺ | ¹⁴¹Pr | 3/2+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-032

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 압력, base 1.05e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `1050 MPa` (줄 46, 뒤):   - Brinell hardness: 500–【1050 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.16e+09: [루테튬] raw `1160 MPa` (줄 37, 두 언어 쪽):   - 비커스 굳기: 【1160 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-033

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.45977e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `87.9095013(16)` (줄 54, 머리글): | ⁸⁸Y | 39 | 49 | 【87.9095013(16)】 | 1948 | 106.629(24) d | β⁺ | ⁸⁸Sr | 4− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-034

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 0.727, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `727(6) ms` (줄 98, 뒤): | ¹⁰⁰ᵐY | 144(16) keV | 144(16) keV | 144(16) keV | 1977 | 【727(6) ms】 | β⁻ (98.92%) | ¹⁰⁰Zr | 1+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `727(6) ms` (줄 99, 뒤): | ¹⁰⁰ᵐY | 144(16) keV | 144(16) keV | 144(16) keV | 1977 | 【727(6) ms】 | β⁻, n (1.08%) | ⁹⁹Zr | 1+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.735: [이트륨 동위 원소] raw `735(7) ms` (줄 76, 두 언어 쪽): | ¹⁰⁰Y | 39 | 61 | 99.92776(8) | 【735(7) ms】 | β⁻ (98.98%) | ¹⁰⁰Zr | 1-,2- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-035

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 온도, base 90.45, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `−182.7 °C` (줄 65, 뒤): …f the elements, especially at low temperatures. Dysprosium has a simple ferromagnetic ordering at temperatures below its Curie temperature of 90.5 K (【−182.7 °C】), at which point it undergoes a first-order phase transition from the orthorhombic crystal structure to hexagonal close-packed (hcp). It then has a h…
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `90.5 K` (줄 65, 뒤): …engths of the elements, especially at low temperatures. Dysprosium has a simple ferromagnetic ordering at temperatures below its Curie temperature of 【90.5 K】 (−182.7 °C), at which point it undergoes a first-order phase transition from the orthorhombic crystal structure to hexagonal close-packed (hcp). It t…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-036

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 온도, base 2928, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `2928 K` (줄 39, 뒤):   - Molar magnetic susceptibility: +249.0×10⁻⁶ cm³/mol (【2928 K】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2840: [디스프로슘] raw `2840 K` (줄 17, 두 언어 쪽):   - 끓는점: 【2840 K】
  - base 3141: [어븀] raw `3141 K` (줄 17, 한쪽 언어 쪽):   - 끓는점: 【3141 K】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-037

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.27779e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `76.95015(22)` (줄 21, 머리글): | ⁷⁷Y | 39 | 38 | 【76.95015(22)】# | 1999 | 63(17) ms | β⁺ | ⁷⁷Sr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `76.95015(22)` (줄 22, 머리글): | ⁷⁷Y | 39 | 38 | 【76.95015(22)】# | 1999 | 63(17) ms | p? | ⁷⁶Sr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `76.95015(22)` (줄 23, 머리글): | ⁷⁷Y | 39 | 38 | 【76.95015(22)】# | 1999 | 63(17) ms | β⁺, p? | ⁷⁶Rb | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-038

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 0.197, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `197(4) ms` (줄 110, 뒤): | ¹⁰⁴Y | 39 | 65 | 103.94194(22)# | 1994 | 【197(4) ms】 | β⁻ (66%) | ¹⁰⁴Zr | (0+,1+)# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `197(4) ms` (줄 111, 뒤): | ¹⁰⁴Y | 39 | 65 | 103.94194(22)# | 1994 | 【197(4) ms】 | β⁻, n (34%) | ¹⁰³Zr | (0+,1+)# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `197(4) ms` (줄 112, 뒤): | ¹⁰⁴Y | 39 | 65 | 103.94194(22)# | 1994 | 【197(4) ms】 | β⁻, 2n? | ¹⁰²Zr | (0+,1+)# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.18: [이트륨 동위 원소] raw `180(60) ms` (줄 87, 두 언어 쪽): | ¹⁰⁴Y | 39 | 65 | 103.94105(43)# | 【180(60) ms】 | β⁻ | ¹⁰⁴Zr |  |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-039

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.32734e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `79.9343548(67)` (줄 29, 머리글): | ⁸⁰Y | 39 | 41 | 【79.9343548(67)】 | 1981 | 30.1(5) s | β⁺ | ⁸⁰Sr | 4− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-040

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 비열, base 160.007, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `160.007 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【160.007 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-041

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.9e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `190±10 pm` (줄 31, 뒤):   - Covalent radius: 【190±10 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
  - base 1.85e-10: [사마륨] raw `185 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【185 pm】 (실험값) 238 pm (계산값)
  - base 1.8e-10: [이트륨] raw `180 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【180 pm】 (실험값)
  - base 1.75e-10: [툴륨] raw `175 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 【175 pm】 (실험값) 222 pm (계산값)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [이트륨 동위 원소] `190`: | ⁸⁴ᵐY | -80(【190】) keV | -80(190) keV | -80(190) keV | 39.5(8) min | β⁺ | ⁸⁴Sr | (5-) |  |  |
  - [이트륨 동위 원소] `190`: | ⁸⁴ᵐY | -80(190) keV | -80(【190】) keV | -80(190) keV | 39.5(8) min | β⁺ | ⁸⁴Sr | (5-) |  |  |
  - [이트륨 동위 원소] `190`: | ⁸⁴ᵐY | -80(190) keV | -80(190) keV | -80(【190】) keV | 39.5(8) min | β⁺ | ⁸⁴Sr | (5-) |  |  |

### R-en-042

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.60937e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `96.9182867(72)` (줄 76, 머리글): | ⁹⁷Y | 39 | 58 | 【96.9182867(72)】 | 1970 | 3.75(3) s | β⁻ (99.945%) | ⁹⁷Zr | 1/2− |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `96.9182867(72)` (줄 77, 머리글): | ⁹⁷Y | 39 | 58 | 【96.9182867(72)】 | 1970 | 3.75(3) s | β⁻, n (0.055%) | ⁹⁶Zr | 1/2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-043

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.47632e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `88.90583816(36)` (줄 57, 머리글): | ⁸⁹Y | 39 | 50 | 【88.90583816(36)】 | 1923 | Stable | Stable | Stable | 1/2− | 1.0000 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-044

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.34387e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `80.9294459(30)` (줄 33, 머리글): | ⁸¹Y | 39 | 42 | 【80.9294459(30)】 | 1981 | 70.4(10) s | β⁺ | ⁸¹Sr | (5/2+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-045

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 2.58e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `258(22) ns` (줄 35, 뒤): | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 1993 | 【258(22) ns】 | IT | ⁸²Y | 4− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.68e-07: [이트륨 동위 원소] raw `268(25) ns` (줄 23, 두 언어 쪽): | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 【268(25) ns】 |  |  | 4- |  |  |
  - base 2.768e-07: [네오디뮴 동위 원소] raw `276.8(18) ns` (줄 41, 한쪽 언어 쪽): | ¹³⁹ᵐ²Nd | 2570.9+X keV | 2570.9+X keV | 2570.9+X keV | 【276.8(18) ns】 |  |  |  |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-046

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `100,000 tonnes` (줄 115, 뒤): …reenland, India, Tanzania, and the United States also have large reserves of thulium. In 2001, the total world reserves of thulium were approximately 【100,000 tonnes】. Thulium is the least abundant lanthanide on Earth except for the radioactive promethium.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-047

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.39354e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `83.9206711(46)` (줄 40, 머리글): | ⁸⁴Y | 39 | 45 | 【83.9206711(46)】 | 1962 | 39.5(8) min | β⁺ | ⁸⁴Sr | (6+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-048

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 압력, base 6.5e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `650 MPa` (줄 44, 뒤):   - Vickers hardness: 470–【650 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5.89e+08: [어븀] raw `589 MPa` (줄 39, 한쪽 언어 쪽):   - 비커스 굳기: 【589 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-049

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.726e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `103.94194(22)` (줄 110, 머리글): | ¹⁰⁴Y | 39 | 65 | 【103.94194(22)】# | 1994 | 197(4) ms | β⁻ (66%) | ¹⁰⁴Zr | (0+,1+)# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `103.94194(22)` (줄 111, 머리글): | ¹⁰⁴Y | 39 | 65 | 【103.94194(22)】# | 1994 | 197(4) ms | β⁻, n (34%) | ¹⁰³Zr | (0+,1+)# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `103.94194(22)` (줄 112, 머리글): | ¹⁰⁴Y | 39 | 65 | 【103.94194(22)】# | 1994 | 197(4) ms | β⁻, 2n? | ¹⁰²Zr | (0+,1+)# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `104.94571(43)` (줄 113, 머리글): | ¹⁰⁵Y | 39 | 66 | 【104.94571(43)】# | 1994 | 95(9) ms | β⁻ | ¹⁰⁵Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `104.94571(43)` (줄 114, 머리글): | ¹⁰⁵Y | 39 | 66 | 【104.94571(43)】# | 1994 | 95(9) ms | β⁻, n (<82%) | ¹⁰⁴Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `104.94571(43)` (줄 115, 머리글): | ¹⁰⁵Y | 39 | 66 | 【104.94571(43)】# | 1994 | 95(9) ms | β⁻, 2n? | ¹⁰³Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-050

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.55944e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `93.9115921(68)` (줄 69, 머리글): | ⁹⁴Y | 39 | 55 | 【93.9115921(68)】 | 1948 | 18.7(1) min | β⁻ | ⁹⁴Zr | 2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-051

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 0.0335, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `33.5(3) ms` (줄 119, 뒤): | ¹⁰⁷Y | 39 | 68 | 106.95494(54)# | 1997 | 【33.5(3) ms】 | β⁻ | ¹⁰⁷Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `33.5(3) ms` (줄 120, 뒤): | ¹⁰⁷Y | 39 | 68 | 106.95494(54)# | 1997 | 【33.5(3) ms】 | β⁻, n? | ¹⁰⁶Zr | 5/2+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `33.5(3) ms` (줄 121, 뒤): | ¹⁰⁷Y | 39 | 68 | 106.95494(54)# | 1997 | 【33.5(3) ms】 | β⁻, 2n? | ¹⁰⁵Zr | 5/2+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-052

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.064e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `1064 nm` (줄 174, 뒤): …ation of Low NA, Large Mode Area fibers enable achievement of near perfect beam qualities (M2<1.1) at power levels of 1.5 kW to greater than 2 kW at ~【1064 nm】 in a broadband configuration. Ytterbium-doped LMA fibers also have the advantages of a larger mode field diameter, which negates the impacts of nonli…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.12e-06: [이터븀] raw `1.12 마이크로미터` (줄 136, 두 언어 쪽): …율이고 수명이 길며 짧은 펄스광을 발생시킬 수 있다. 이로 인해 이터븀은 레이저 재료에 많이 포함된다. 이터븀 레이저는 일반적으로 1.06 - 【1.12 마이크로미터】의 선에서 파장 900 nm~1 마이크로미터의 빛을 발생시킨다. (광섬유 레이저의 도핑 재료로 사용된다.)
  - base 1e-06: [이터븀] raw `1 마이크로미터` (줄 136, 두 언어 쪽): …다. 이로 인해 이터븀은 레이저 재료에 많이 포함된다. 이터븀 레이저는 일반적으로 1.06 - 1.12 마이크로미터의 선에서 파장 900 nm~【1 마이크로미터】의 빛을 발생시킨다. (광섬유 레이저의 도핑 재료로 사용된다.)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-053

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 1.24762e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `144.4 d` (줄 53, 뒤): …n isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁵⁴Dy synth 1.40×10⁶ y α ¹⁵⁰Gd ¹⁵⁶Dy 0.056% stable ¹⁵⁸Dy 0.095% stable ¹⁵⁹Dy synth 【144.4 d】 ε ¹⁵⁹Tb ¹⁶⁰Dy 2.329% stable ¹⁶¹Dy 18.8889999999% stable ¹⁶²Dy 25.475% stable ¹⁶³Dy 24.896% stable ¹⁶⁴Dy 28.26% stable ¹⁶⁵Dy synth 2.332 h β⁻ ¹⁶⁵Ho ¹⁶…
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `144.4 days` (줄 106, 뒤): … ranging in atomic mass from 138 to 173. The most stable of these is ¹⁵⁴Dy, with a half-life of 1.40×10⁶ years, followed by ¹⁵⁹Dy with a half-life of 【144.4 days】. As a general rule, isotopes that are lighter than the stable isotopes tend to decay primarily by β⁺ decay, though ¹⁵⁴Dy decays by alpha emission and…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-054

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.34006e-24, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `807(50)` (줄 66, 머리글): | ⁹²ᵐY | 807(50)# keV | 807(50)# keV | 【807(50)】# keV | 2009 | 3.7(5) μs | IT | ⁹²Y | 7+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-055

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 160000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `160 km` (줄 135, 뒤): …tly, most dysprosium is being obtained from the ion-adsorption clay ores of southern China. As of November 2018 the Browns Range Project pilot plant, 【160 km】 south east of Halls Creek, Western Australia, is producing 50 tonnes (49 long tons) per annum.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [터븀 동위 원소] `160`: | ¹⁶¹Tb | 65 | 96 | 【160】.9275699(28) | 6.906(19) d | β⁻ | ¹⁶¹Dy | 3/2+ |  |  |
  - [네오디뮴 동위 원소] `160`: | ¹⁶¹Nd | 60 | 101 | 【160】.95388(75)# | 200# ms | β⁻ | ¹⁶¹Pm | 1/2-# |  |  |

### R-en-056

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 9.51693e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `594(10) keV` (줄 90, 뒤): | ⁹⁸ᵐ⁴Y | 【594(10) keV】 | 594(10) keV | 594(10) keV | 2017 | 180(7) ns | IT | ⁹⁸Y | (3−,4−) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `594(10) keV` (줄 90, 뒤): | ⁹⁸ᵐ⁴Y | 594(10) keV | 【594(10) keV】 | 594(10) keV | 2017 | 180(7) ns | IT | ⁹⁸Y | (3−,4−) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `594(10) keV` (줄 90, 뒤): | ⁹⁸ᵐ⁴Y | 594(10) keV | 594(10) keV | 【594(10) keV】 | 2017 | 180(7) ns | IT | ⁹⁸Y | (3−,4−) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 9.95593e-14: [터븀 동위 원소] raw `621.4(11) keV` (줄 25, 한쪽 언어 쪽): | ¹⁴²ᵐ²Tb | 【621.4(11) keV】 | 621.4(11) keV | 621.4(11) keV | 15(4) µs |  |  |  |  |  |
  - base 8.90137e-14: [이트륨 동위 원소] raw `555.58(5) keV` (줄 50, 두 언어 쪽): | ⁹¹ᵐY | 【555.58(5) keV】 | 555.58(5) keV | 555.58(5) keV | 49.71(4) min | IT (98.5%) | ⁹¹Y | 9/2+ |  |  …
  - base 8.72385e-14: [터븀 동위 원소] raw `544.5(6) keV` (줄 35, 한쪽 언어 쪽): | ¹⁴⁴ᵐ⁴Tb | 【544.5(6) keV】 | 544.5(6) keV | 544.5(6) keV | <300 ns |  |  | (10+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-057

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 2.08e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `2080 nm` (줄 127, 뒤): …um-thulium triple-doped yttrium aluminium garnet (Ho:Cr:Tm:YAG, or Ho,Cr,Tm:YAG) is an active laser medium material with high efficiency. It lases at 【2080 nm】 in the infrared and is widely used in military applications, medicine, and meteorology. Single-element thulium-doped YAG (Tm:YAG) lasers operate at 2…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-058

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.36043e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `81.9269302(59)` (줄 34, 머리글): | ⁸²Y | 39 | 43 | 【81.9269302(59)】 | 1980 | 8.30(20) s | β⁺ | ⁸²Sr | 1+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-059

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 2.30713e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `144(16) keV` (줄 98, 뒤): | ¹⁰⁰ᵐY | 【144(16) keV】 | 144(16) keV | 144(16) keV | 1977 | 727(6) ms | β⁻ (98.92%) | ¹⁰⁰Zr | 1+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `144(16) keV` (줄 98, 뒤): | ¹⁰⁰ᵐY | 144(16) keV | 【144(16) keV】 | 144(16) keV | 1977 | 727(6) ms | β⁻ (98.92%) | ¹⁰⁰Zr | 1+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `144(16) keV` (줄 98, 뒤): | ¹⁰⁰ᵐY | 144(16) keV | 144(16) keV | 【144(16) keV】 | 1977 | 727(6) ms | β⁻ (98.92%) | ¹⁰⁰Zr | 1+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `144(16) keV` (줄 99, 뒤): | ¹⁰⁰ᵐY | 【144(16) keV】 | 144(16) keV | 144(16) keV | 1977 | 727(6) ms | β⁻, n (1.08%) | ⁹⁹Zr | 1+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `144(16) keV` (줄 99, 뒤): | ¹⁰⁰ᵐY | 144(16) keV | 【144(16) keV】 | 144(16) keV | 1977 | 727(6) ms | β⁻, n (1.08%) | ⁹⁹Zr | 1+# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `144(16) keV` (줄 99, 뒤): | ¹⁰⁰ᵐY | 144(16) keV | 144(16) keV | 【144(16) keV】 | 1977 | 727(6) ms | β⁻, n (1.08%) | ⁹⁹Zr | 1+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [사마륨] `144`: … 원소들과의 화합물은 압력에 따라 전기 저항이 달라지는 특성이 있어 압력 감지기에 사용되기도 한다. 사마륨-147과 네오디뮴-143, 네오디뮴-【144】의 비율을 분석하면 방사능 연대 측정을 할 수도 있다.
  - [터븀 동위 원소] `144`: | ¹⁴⁵Tb | 65 | 80 | 【144】.92927(6) | 20# min | β⁺ | ¹⁴⁵Gd | (3/2+) |  |  |
  - [네오디뮴 동위 원소] `144`: | ¹⁴⁵Nd | 60 | 85 | 【144】.9125736(25) | 관찰 안정 | 관찰 안정 | 관찰 안정 | 7/2- | 0.083(1) | 0.0823-0.0835 |

### R-en-060

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 1.74253e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1087.6(6) keV` (줄 72, 뒤): | ⁹⁵ᵐY | 【1087.6(6) keV】 | 1087.6(6) keV | 1087.6(6) keV | 1982 | 48.6(5) μs | IT | ⁹⁵Y | 9/2+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1087.6(6) keV` (줄 72, 뒤): | ⁹⁵ᵐY | 1087.6(6) keV | 【1087.6(6) keV】 | 1087.6(6) keV | 1982 | 48.6(5) μs | IT | ⁹⁵Y | 9/2+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1087.6(6) keV` (줄 72, 뒤): | ⁹⁵ᵐY | 1087.6(6) keV | 1087.6(6) keV | 【1087.6(6) keV】 | 1982 | 48.6(5) μs | IT | ⁹⁵Y | 9/2+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.82648e-13: [이트륨 동위 원소] raw `1140(30) keV` (줄 58, 두 언어 쪽): | ⁹⁶ᵐY | 【1140(30) keV】 | 1140(30) keV | 1140(30) keV | 9.6(2) s | β⁻ | ⁹⁶Zr | (8)+ |  |  |
  - base 1.89233e-13: [이트륨 동위 원소] raw `1181.1(4) keV` (줄 72, 두 언어 쪽): | ⁹⁸ᵐ⁴Y | 【1181.1(4) keV】 | 1181.1(4) keV | 1181.1(4) keV | 0.83(10) µs |  |  | (8-) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-061

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 7.62e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `762(14) ns` (줄 92, 뒤): | ⁹⁸ᵐ⁶Y | 1181.50(18) keV | 1181.50(18) keV | 1181.50(18) keV | 2017 | 【762(14) ns】 | IT | ⁹⁸Y | (10−) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.3e-07: [이트륨 동위 원소] raw `0.83(10) µs` (줄 72, 두 언어 쪽): | ⁹⁸ᵐ⁴Y | 1181.1(4) keV | 1181.1(4) keV | 1181.1(4) keV | 【0.83(10) µs】 |  |  | (8-) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-062

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.52618e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `91.9089458(98)` (줄 65, 머리글): | ⁹²Y | 39 | 53 | 【91.9089458(98)】 | 1940 | 3.54(1) h | β⁻ | ⁹²Zr | 2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-063

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 4.5e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `450(150) ns` (줄 91, 뒤): | ⁹⁸ᵐ⁵Y | 972.17(20) keV | 972.17(20) keV | 972.17(20) keV | 1970 | 【450(150) ns】 | IT | ⁹⁸Y | (8+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.1e-07: [네오디뮴 동위 원소] raw `410(50) ns` (줄 37, 한쪽 언어 쪽): | ¹³⁸ᵐNd | 3174.9(4) keV | 3174.9(4) keV | 3174.9(4) keV | 【410(50) ns】 |  |  | (10+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-064

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 길이, base 1.92e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `192±7 pm` (줄 31, 뒤):   - Covalent radius: 【192±7 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
  - base 1.85e-10: [사마륨] raw `185 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【185 pm】 (실험값) 238 pm (계산값)
  - base 1.8e-10: [이트륨] raw `180 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【180 pm】 (실험값)
  - base 1.75e-10: [툴륨] raw `175 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 【175 pm】 (실험값) 222 pm (계산값)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-065

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 4.86e-05, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `48.6(5) μs` (줄 72, 뒤): | ⁹⁵ᵐY | 1087.6(6) keV | 1087.6(6) keV | 1087.6(6) keV | 1982 | 【48.6(5) μs】 | IT | ⁹⁵Y | 9/2+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-066

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 6.9e-06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `6.90(54) μs` (줄 89, 뒤): | ⁹⁸ᵐ³Y | 496.10(11) keV | 496.10(11) keV | 496.10(11) keV | 2017 | 【6.90(54) μs】 | IT | ⁹⁸Y | (4)− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 7.6e-06: [이트륨 동위 원소] raw `7.6(4) µs` (줄 71, 두 언어 쪽): | ⁹⁸ᵐ³Y | 496.19(15) keV | 496.19(15) keV | 496.19(15) keV | 【7.6(4) µs】 |  |  | (2-) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이터븀] `6.90`:   - 밀도 (상온 근처): 【6.90】 g/cm³

### R-en-067

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.37696e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `82.922484(20)` (줄 37, 머리글): | ⁸³Y | 39 | 44 | 【82.922484(20)】 | 1962 | 7.08(8) min | β⁺ | ⁸³Sr | (9/2+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-068

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 1.16763e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `3.70×10¹⁰ years` (줄 78, 뒤): …Out of these two, only the former is stable, making the element monoisotopic. The latter one, lutetium-176, decays via beta decay with a half-life of 【3.70×10¹⁰ years】; it makes up about 2.6% of natural lutetium.
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `3.701×10¹⁰ y` (줄 52, 뒤): …cay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁷³Lu synth 1.37 y ε ¹⁷³Yb ¹⁷⁴Lu synth 3.31 y β⁺ ¹⁷⁴Yb ¹⁷⁵Lu 97.4009999999% stable ¹⁷⁶Lu 2.599% 【3.701×10¹⁰ y】 β⁻ ¹⁷⁶Hf ¹⁷⁷Lu synth 6.6443 d β⁻ ¹⁷⁷Hf
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.19288e+18: [루테튬] raw `3.78×10¹⁰y` (줄 46, 두 언어 쪽): … 1.37 y ε 0.671 ¹⁷³Yb ¹⁷⁴Lu 인공 3.31 y ε 1.374 ¹⁷⁴Yb ¹⁷⁵Lu 97.41% 안정 ¹⁷⁶Lu 2.59% 【3.78×10¹⁰y】 β⁻ 1.193 ¹⁷⁶Hf
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-069

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 8.2e-06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `8.2(4) μs` (줄 95, 뒤): | ⁹⁹ᵐY | 2141.65(19) keV | 2141.65(19) keV | 2141.65(19) keV | 1985 | 【8.2(4) μs】 | IT | ⁹⁹Y | (17/2+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 8.6e-06: [이트륨 동위 원소] raw `8.6(8) µs` (줄 75, 두 언어 쪽): | ⁹⁹ᵐY | 2141.65(19) keV | 2141.65(19) keV | 2141.65(19) keV | 【8.6(8) µs】 |  |  | (17/2+) |  |  |
  - base 7.6e-06: [이트륨 동위 원소] raw `7.6(4) µs` (줄 71, 두 언어 쪽): | ⁹⁸ᵐ³Y | 496.19(15) keV | 496.19(15) keV | 496.19(15) keV | 【7.6(4) µs】 |  |  | (2-) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [터븀 동위 원소] `8.2`: | ¹⁶⁸Tb | 65 | 103 | 167.94364(54)# | 【8.2】(13) s | β⁻ | ¹⁶⁸Dy | 4-# |  |  |

### R-en-070

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.44319e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `86.9108761(12)` (줄 51, 머리글): | ⁸⁷Y | 39 | 48 | 【86.9108761(12)】 | 1940 | 79.8(3) h | β⁺ | ⁸⁷Sr | 1/2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-071

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.49294e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `89.90714175(38)` (줄 59, 머리글): | ⁹⁰Y | 39 | 51 | 【89.90714175(38)】 | 1937 | 64.05(5) h | β⁻ | ⁹⁰Zr | 2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-072

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 7.46134e-14, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 86, 뒤): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 86, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 【465.7(7) keV】 | 465.7(7) keV | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 86, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 【465.7(7) keV】 | 1977 | 2.32(8) s | β⁻ (96.56%) | ⁹⁸Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 87, 뒤): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | β⁻, n (3.44%) | ⁹⁷Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 87, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 【465.7(7) keV】 | 465.7(7) keV | 1977 | 2.32(8) s | β⁻, n (3.44%) | ⁹⁷Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 87, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 【465.7(7) keV】 | 1977 | 2.32(8) s | β⁻, n (3.44%) | ⁹⁷Zr | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 88, 뒤): | ⁹⁸ᵐ²Y | 【465.7(7) keV】 | 465.7(7) keV | 465.7(7) keV | 1977 | 2.32(8) s | IT? | ⁹⁸Y | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 88, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 【465.7(7) keV】 | 465.7(7) keV | 1977 | 2.32(8) s | IT? | ⁹⁸Y | (6,7)+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `465.7(7) keV` (줄 88, 뒤): | ⁹⁸ᵐ²Y | 465.7(7) keV | 465.7(7) keV | 【465.7(7) keV】 | 1977 | 2.32(8) s | IT? | ⁹⁸Y | (6,7)+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 7.32195e-14: [터븀 동위 원소] raw `457(29) keV` (줄 52, 한쪽 언어 쪽): | ¹⁵⁰ᵐTb | 【457(29) keV】 | 457(29) keV | 457(29) keV | 5.8(2) min | β⁺ | ¹⁵⁰Gd | 9+ |  |  |
  - base 7.62957e-14: [터븀 동위 원소] raw `476.2(5) keV` (줄 33, 한쪽 언어 쪽): | ¹⁴⁴ᵐ²Tb | 【476.2(5) keV】 | 476.2(5) keV | 476.2(5) keV | 2.8(3) µs |  |  | (8-) |  |  |
  - base 7.94984e-14: [이트륨 동위 원소] raw `496.19(15) keV` (줄 71, 두 언어 쪽): | ⁹⁸ᵐ³Y | 【496.19(15) keV】 | 496.19(15) keV | 496.19(15) keV | 7.6(4) µs |  |  | (2-) |  |  |
  - base 8.03876e-14: [터븀 동위 원소] raw `501.74(19) keV` (줄 61, 한쪽 언어 쪽): | ¹⁵²ᵐ²Tb | 【501.74(19) keV】 | 501.74(19) keV | 501.74(19) keV | 4.2(1) min | IT (78.8%) | ¹⁵²Tb | 8+ |  |  …
  - base 8.13105e-14: [이트륨 동위 원소] raw `507.50(13) keV` (줄 24, 두 언어 쪽): | ⁸²ᵐ²Y | 【507.50(13) keV】 | 507.50(13) keV | 507.50(13) keV | 147(7) ns |  |  | 6+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-073

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 3.1e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `3100 tonnes` (줄 133, 뒤): About 【3100 tonnes】 of dysprosium were produced worldwide in 2021, with 40% of that total produced in China, 31% in Myanmar, and 20% in Australia. Dysprosium prices have…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-074

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 75.42, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `1.257 minutes` (줄 106, 뒤): …prosium also has at least 11 metastable isomers, ranging in atomic mass from 140 to 165. The most stable of these is ¹⁶⁵ᵐDy, which has a half-life of 【1.257 minutes】.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 70.4: [이트륨 동위 원소] raw `70.4(10) s` (줄 21, 두 언어 쪽): | ⁸¹Y | 39 | 42 | 80.92913(7) | 【70.4(10) s】 | β⁺ | ⁸¹Sr | (5/2+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-075

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 1.9263e-13, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1202.3(10) keV` (줄 70, 뒤): | ⁹⁴ᵐY | 【1202.3(10) keV】 | 1202.3(10) keV | 1202.3(10) keV | 1999 | 1.304(12) μs | IT | ⁹⁴Y | (5+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1202.3(10) keV` (줄 70, 뒤): | ⁹⁴ᵐY | 1202.3(10) keV | 【1202.3(10) keV】 | 1202.3(10) keV | 1999 | 1.304(12) μs | IT | ⁹⁴Y | (5+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1202.3(10) keV` (줄 70, 뒤): | ⁹⁴ᵐY | 1202.3(10) keV | 1202.3(10) keV | 【1202.3(10) keV】 | 1999 | 1.304(12) μs | IT | ⁹⁴Y | (5+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1205.0(10) keV` (줄 102, 뒤): | ¹⁰¹ᵐY | 【1205.0(10) keV】 | 1205.0(10) keV | 1205.0(10) keV | 2009 | 870(90) ns | IT | ¹⁰¹Y | 13/2−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1205.0(10) keV` (줄 102, 뒤): | ¹⁰¹ᵐY | 1205.0(10) keV | 【1205.0(10) keV】 | 1205.0(10) keV | 2009 | 870(90) ns | IT | ¹⁰¹Y | 13/2−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `1205.0(10) keV` (줄 102, 뒤): | ¹⁰¹ᵐY | 1205.0(10) keV | 1205.0(10) keV | 【1205.0(10) keV】 | 2009 | 870(90) ns | IT | ¹⁰¹Y | 13/2−# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.89233e-13: [이트륨 동위 원소] raw `1181.1(4) keV` (줄 72, 두 언어 쪽): | ⁹⁸ᵐ⁴Y | 【1181.1(4) keV】 | 1181.1(4) keV | 1181.1(4) keV | 0.83(10) µs |  |  | (8-) |  |  |
  - base 1.82648e-13: [이트륨 동위 원소] raw `1140(30) keV` (줄 58, 두 언어 쪽): | ⁹⁶ᵐY | 【1140(30) keV】 | 1140(30) keV | 1140(30) keV | 9.6(2) s | β⁻ | ⁹⁶Zr | (8)+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-076

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 574068, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `6.6443 d` (줄 52, 뒤): …t1/2) mode pro­duct ¹⁷³Lu synth 1.37 y ε ¹⁷³Yb ¹⁷⁴Lu synth 3.31 y β⁺ ¹⁷⁴Yb ¹⁷⁵Lu 97.4009999999% stable ¹⁷⁶Lu 2.599% 3.701×10¹⁰ y β⁻ ¹⁷⁶Hf ¹⁷⁷Lu synth 【6.6443 d】 β⁻ ¹⁷⁷Hf
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `6.693-day` (줄 104, 뒤): ¹⁷⁷Lu is produced by neutron activation of ¹⁷⁶Lu or by indirectly by neutron activation of ¹⁷⁶Yb followed by beta decay. The 【6.693-day】 half-life allows transport from the production reactor to the point of use without significant loss in activity.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 596160: [터븀 동위 원소] raw `6.9일` (줄 2, 한쪽 언어 쪽): …터븀 혹은 테르븀의 동위 원소는 1종으로 ¹⁵⁹Tb이 100% 존재한다. 우라늄과 토륨의 자발 핵분열로 생성되는 생성되는 ¹⁶¹Tb은 반감기가 【6.9일】로 자연계에 미량 존재한다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-077

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 에너지, base 1.34988e-14, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `84.253 keV` (줄 131, 뒤): …uce the isotope thulium-170, having a half-life of 128.6 days and five major emission lines of comparable intensity (at 7.4, 51.354, 52.389, 59.4 and 【84.253 keV】). These radioactive sources have a useful life of about one year, as tools in medical and dental diagnosis, as well as to detect defects in inaccessi…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.41632e-14: [터븀 동위 원소] raw `88.4(2) keV` (줄 76, 한쪽 언어 쪽): | ¹⁵⁶ᵐ²Tb | 【88.4(2) keV】 | 88.4(2) keV | 88.4(2) keV | 5.3(2) h |  |  | (0+) |  |  |
  - base 1.44356e-14: [터븀 동위 원소] raw `90.1(3) keV` (줄 44, 한쪽 언어 쪽): | ¹⁴⁸ᵐ¹Tb | 【90.1(3) keV】 | 90.1(3) keV | 90.1(3) keV | 2.20(5) min | β⁺ | ¹⁴⁸Gd | (9)+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-078

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.64267e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `98.9241608(71)` (줄 93, 머리글): | ⁹⁹Y | 39 | 60 | 【98.9241608(71)】 | 1975 | 1.484(7) s | β⁻ (98.23%) | ⁹⁹Zr | 5/2+ |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `98.9241608(71)` (줄 94, 머리글): | ⁹⁹Y | 39 | 60 | 【98.9241608(71)】 | 1975 | 1.484(7) s | β⁻, n (1.77%) | ⁹⁸Zr | 5/2+ |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-079

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 몰 에너지, base 129000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `129 kJ/mol` (줄 22, 뒤):   - Heat of vaporization: 【129 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [네오디뮴 동위 원소] `129`: | ¹³⁰Nd | 60 | 70 | 【129】.92851(3) | 21(3) s | β⁺ | ¹³⁰Pr | 0+ |  |  |

### R-en-080

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 열팽창, base 2.431e-05, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `24.31×10⁻⁶/K` (줄 35, 뒤):   - Thermal expansion: 【24.31×10⁻⁶/K】 (at 20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.63e-05: [이터븀] raw `26.3 µm/(m·K)` (줄 32, 두 언어 쪽):   - 열팽창: (실온) (β, poly) 【26.3 µm/(m·K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-081

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 비열, base 170.462, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `170.462 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【170.462 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-082

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.29429e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `77.94399(32)` (줄 24, 머리글): | ⁷⁸Y | 39 | 39 | 【77.94399(32)】# | 1992 | 54(5) ms | β⁺ | ⁷⁸Sr | (0+) |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `77.94399(32)` (줄 25, 머리글): | ⁷⁸Y | 39 | 39 | 【77.94399(32)】# | 1992 | 54(5) ms | β⁺, p? | ⁷⁷Rb | (0+) |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-083

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.59272e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `95.9159093(65)` (줄 73, 머리글): | ⁹⁶Y | 39 | 57 | 【95.9159093(65)】 | 1975 | 5.34(5) s | β⁻ | ⁹⁶Zr | 0− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-084

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 압력, base 5.5e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Dysprosium] (같은 주제의 반대 언어 문서: 디스프로슘) raw `550 MPa` (줄 45, 뒤):   - Vickers hardness: 410–【550 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 5.4e+08: [디스프로슘] raw `540 MPa` (줄 40, 두 언어 쪽):   - 비커스 굳기: 【540 MPa】
  - base 5.2e+08: [툴륨] raw `520 MPa` (줄 38, 두 언어 쪽):   - 비커스 굳기: 【520 MPa】
  - base 5.89e+08: [어븀] raw `589 MPa` (줄 39, 한쪽 언어 쪽):   - 비커스 굳기: 【589 MPa】
  - base 5e+08: [디스프로슘] raw `500 MPa` (줄 41, 두 언어 쪽):   - 브리넬 굳기: 【500 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-085

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.50955e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `90.9072980(20)` (줄 62, 머리글): | ⁹¹Y | 39 | 52 | 【90.9072980(20)】 | 1943 | 58.51(6) d | β⁻ | ⁹¹Zr | 1/2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-086

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 3.7e-06, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `3.7(5) μs` (줄 66, 뒤): | ⁹²ᵐY | 807(50)# keV | 807(50)# keV | 807(50)# keV | 2009 | 【3.7(5) μs】 | IT | ⁹²Y | 7+# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-087

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 비열, base 153.512, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lutetium] (같은 주제의 반대 언어 문서: 루테튬) raw `153.512 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【153.512 J/(kg·K)】
  - [Ytterbium] (같은 주제의 반대 언어 문서: 이터븀) raw `154.522 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【154.522 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-088

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 8.7e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `870(90) ns` (줄 102, 뒤): | ¹⁰¹ᵐY | 1205.0(10) keV | 1205.0(10) keV | 1205.0(10) keV | 2009 | 【870(90) ns】 | IT | ¹⁰¹Y | 13/2−# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 8.3e-07: [이트륨 동위 원소] raw `0.83(10) µs` (줄 72, 두 언어 쪽): | ⁹⁸ᵐ⁴Y | 1181.1(4) keV | 1181.1(4) keV | 1181.1(4) keV | 【0.83(10) µs】 |  |  | (8-) |  |  |
  - base 9.6e-07: [터븀 동위 원소] raw `0.96 µs` (줄 60, 한쪽 언어 쪽): | ¹⁵²ᵐ¹Tb | 342.15(16) keV | 342.15(16) keV | 342.15(16) keV | 【0.96 µs】 |  |  | 5- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [사마륨] `870`: …¹¹y α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α 1.986 ¹⁴⁴Nd ¹⁴⁹Sm 13.82% >2×10¹⁵ y α 1.【870】 ¹⁴⁵Nd ¹⁵⁰Sm 7.38% 안정 ¹⁵²Sm 26.75% 안정 ¹⁵⁴Sm 22.75% 안정

### R-en-089

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 2.92e-07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `292(10) ns` (줄 42, 뒤): | ⁸⁴ᵐ²Y | 210.42(16) keV | 210.42(16) keV | 210.42(16) keV | 2005 | 【292(10) ns】 | IT | ⁸⁴Y | 4− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3e-07: [이트륨 동위 원소] raw `300 ns` (줄 88, 두 언어 쪽): | ¹⁰⁵Y | 39 | 66 | 104.94487(54)# | 60# ms [>【300 ns】] | β⁻ | ¹⁰⁵Zr | 5/2+# |  |  |
  - base 2.768e-07: [네오디뮴 동위 원소] raw `276.8(18) ns` (줄 41, 한쪽 언어 쪽): | ¹³⁹ᵐ²Nd | 2570.9+X keV | 2570.9+X keV | 2570.9+X keV | 【276.8(18) ns】 |  |  |  |  |  |
  - base 2.68e-07: [이트륨 동위 원소] raw `268(25) ns` (줄 23, 두 언어 쪽): | ⁸²ᵐ¹Y | 402.63(14) keV | 402.63(14) keV | 402.63(14) keV | 【268(25) ns】 |  |  | 4- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-090

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 시간, base 0.028, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `28(9) ms` (줄 18, 뒤): | ⁷⁶Y | 39 | 37 | 75.95894(32)# | 2001 | 【28(9) ms】 | β⁺? | ⁷⁶Sr | 1−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `28(9) ms` (줄 19, 뒤): | ⁷⁶Y | 39 | 37 | 75.95894(32)# | 2001 | 【28(9) ms】 | p? | ⁷⁵Sr | 1−# |  |
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `28(9) ms` (줄 20, 뒤): | ⁷⁶Y | 39 | 37 | 75.95894(32)# | 2001 | 【28(9) ms】 | β⁺, p? | ⁷⁵Rb | 1−# |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [디스프로슘] `28`: …y 0.10% 안정 ¹⁶⁰Dy 2.34% 안정 ¹⁶¹Dy 18.91% 안정 ¹⁶²Dy 25.51% 안정 ¹⁶³Dy 24.90% 안정 ¹⁶⁴Dy 【28】.18% 안정
  - [어븀] `28`:   - 몰열용량: 【28】.12 J/(mol·K)
  - [어븀] `28`:   - 전단 탄성 계수: 【28】.3 GPa
  - [어븀] `28`:   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁶⁰Er 인공 【28】.58 h ε 0.330 ¹⁶⁰Ho ¹⁶²Er 0.14% 안정 ¹⁶⁴Er 1.61% 안정 ¹⁶⁵Er 인공 10.36 h ε 0.376 ¹⁶⁵Ho…
  - [이트륨] `28`: …0.48 0.38D - ⁸⁸Y 합성 106.6d ε - ⁸⁸Sr γ 1.83 0.89 - ⁸⁹Y 100% 안정 ⁹⁰Y 합성 2.67d β- 2.【28】 ⁹⁰Zr γ 2.18 - ⁹¹Y 합성 58.5d β- 1.54 ⁹¹Zr γ 1.20 -

### R-en-091

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 질량, base 1.57606e-25, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Isotopes of yttrium] (같은 주제의 반대 언어 문서: 이트륨 동위 원소) raw `94.9128197(73)` (줄 71, 머리글): | ⁹⁵Y | 39 | 56 | 【94.9128197(73)】 | 1959 | 10.3(1) min | β⁻ | ⁹⁵Zr | 1/2− |  |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-092

- 분야 rare_earth, 언어 en, 쪽 두 언어 쪽, dim 몰 에너지, base 191000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Thulium] (같은 주제의 반대 언어 문서: 툴륨) raw `191 kJ/mol` (줄 22, 뒤):   - Heat of vaporization: 【191 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-093

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 5.75914e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `21.9` (줄 147, 머리글): | FiR1, Finland | 50 (1999–2012) | BPA 290–400 mg/kg | 11.0 – 【21.9】 (primary), 7.0 (recurrent) |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.05906e+07: [툴륨] raw `1.92 y` (줄 46, 두 언어 쪽): … 인공 93.1 d ε 1.679 ¹⁶⁸Er ¹⁶⁹Tm 100% 안정 ¹⁷⁰Tm 인공 128.6 d β⁻ 0.968 ¹⁷⁰Yb ¹⁷¹Tm 인공 【1.92 y】 β⁻ 0.096 ¹⁷¹Yb
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이터븀] `21.9`: …Yb 0.13% 안정 ¹⁶⁹Yb 인공 32.026 d ε 0.909 ¹⁶⁹Tm ¹⁷⁰Yb 3.05% 안정 ¹⁷¹Yb 14.3% 안정 ¹⁷²Yb 【21.9】% 안정 ¹⁷³Yb 16.12% 안정 ¹⁷⁴Yb 31.8% 안정 ¹⁷⁵Yb 인공 4.185 d β⁻ 0.470 ¹⁷⁵Lu ¹⁷⁶Yb 12.7% …

### R-en-094

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.89272e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `11.0` (줄 147, 머리글): | FiR1, Finland | 50 (1999–2012) | BPA 290–400 mg/kg | 【11.0】 – 21.9 (primary), 7.0 (recurrent) |
  - [Neutron capture therapy of cancer] raw `11.1` (줄 143, 머리글): | MITR, MIT, US | 20 (1996–1999) | BPA 250 or 350 mg/kg | 【11.1】 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-095

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 비열, base 195.162, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `195.162 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【195.162 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-096

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 4.97022e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `18.9 months` (줄 207, 뒤): …on irradiation. The primary endpoint of this study was the 1-year survival rate after BNCT, which was 79.2%, and the median overall survival rate was 【18.9 months】. Based on these results, it was concluded that c-BNS BNCT was safe and resulted in increased survival of patients with recurrent gliomas. Although th…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-097

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 3.73424e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `14.2 months` (줄 158, 뒤): …ome disagreement among the Swedish investigators regarding the evaluation of the results. Based on incomplete survival data, the MeST was reported as 【14.2 months】 and the time to tumor progression was 5.8 months. However, more careful examination of the complete survival data revealed that the MeST was 17.7 mon…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-098

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 비저항, base 9e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `0.900 µΩ⋅m` (줄 37, 뒤):   - Electrical resistivity: poly: 【0.900 µΩ⋅m】 (at r.t.)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 9.26e-07: [디스프로슘] raw `926 n Ω·m` (줄 33, 두 언어 쪽):   - 전기 저항도: (실온) (α, poly) 【926 n Ω·m】
  - base 9.4e-07: [사마륨] raw `0.940 μ Ω·m` (줄 33, 한쪽 언어 쪽):   - 전기 저항도: (실온) (α, poly) 【0.940 μ Ω·m】
  - base 8.6e-07: [어븀] raw `0.860 μ Ω·m` (줄 33, 한쪽 언어 쪽):   - 전기 저항도: (실온) (poly) 【0.860 μ Ω·m】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-099

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 4.65465e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `17.7` (줄 146, 머리글): | R2-0, Studsvik Medical AB, Sweden | 30 (2001–2007) | BPA 900 mg/kg | 【17.7】 (primary) |
  - [Neutron capture therapy of cancer] raw `17.7 months` (줄 158, 뒤): …2 months and the time to tumor progression was 5.8 months. However, more careful examination of the complete survival data revealed that the MeST was 【17.7 months】 compared to 15.5 months that has been reported for patients who received standard therapy of surgery, followed by radiotherapy (RT) and the drug temo…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.32339e+07: [루테튬] raw `1.37 y` (줄 46, 두 언어 쪽):   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁷³Lu 인공 【1.37 y】 ε 0.671 ¹⁷³Yb ¹⁷⁴Lu 인공 3.31 y ε 1.374 ¹⁷⁴Yb ¹⁷⁵Lu 97.41% 안정 ¹⁷⁶Lu 2.59% 3.78×10…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-100

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 1.65e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `165` (줄 44, 뒤):   - Vickers hardness: 【165】–200 MPa
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [사마륨] `165`:   - 기화열: 【165】 kJ/mol
  - [터븀 동위 원소] `165`: | ¹⁶⁶Tb | 65 | 101 | 【165】.93799(11) | 25.6(22) s | β⁻ | ¹⁶⁶Dy |  |  |  |

### R-en-101

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 3403, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `3403 K` (줄 18, 뒤):   - Boiling point: 【3403 K】 ​(3130 °C, ​5666 °F)
  - [Praseodymium] raw `3130 °C` (줄 18, 뒤):   - Boiling point: 3403 K ​(【3130 °C】, ​5666 °F)
  - [Praseodymium] raw `5666 °F` (줄 18, 뒤):   - Boiling point: 3403 K ​(3130 °C, ​【5666 °F】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 3609: [이트륨] raw `3609 K` (줄 17, 한쪽 언어 쪽):   - 끓는점: 【3609 K】
  - base 3675: [루테튬] raw `3675 K` (줄 17, 두 언어 쪽):   - 끓는점: 【3675 K】
  - base 3141: [어븀] raw `3141 K` (줄 17, 한쪽 언어 쪽):   - 끓는점: 【3141 K】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-102

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 4.26564e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `13.517 y` (줄 51, 뒤): …Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁵⁰Eu synth 36.9 y β⁺ ¹⁵⁰Sm ¹⁵¹Eu 47.7999999999% 4.6×10¹⁸ y α ¹⁴⁷Pm ¹⁵²Eu synth 【13.517 y】 β⁺ ¹⁵²Sm β⁻ ¹⁵²Gd ¹⁵³Eu 52.2% stable ¹⁵⁴Eu synth 8.592 y β⁻ ¹⁵⁴Gd ε ¹⁵⁴Sm ¹⁵⁵Eu synth 4.742 y β⁻ ¹⁵⁵Gd
  - [Europium] raw `13.517 years` (줄 161, 뒤): …e of 197+74 −71 ms. The longest-lived artificial isotope is ¹⁵⁰Eu, with a half-life of 36.9 years. Other comparatively long-lived isotopes are ¹⁵²Eu (【13.517 years】), ¹⁵⁴Eu (8.592 years) and ¹⁵⁵Eu (4.742 years); all other known ground-state europium radioisotopes have half-lives shorter than 100 days.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-103

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.84013e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `10.8` (줄 145, 머리글): | JRR4, Japan | 15 (1998–2007) | BPA 250 mg/kg + BSH 5 g | 【10.8】 (recurrent), 27.1 (+ X-ray) |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-104

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 3.47126e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `13.2` (줄 148, 머리글): | HFR, Netherlands | 26 (1997–2002) | BSH 100 mg/kg | 10.4 – 【13.2】 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-105

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 6.12e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `612 nm` (줄 243, 뒤): …ly been investigated as red emitters in organic light-emitting diodes. Their narrow emission bands, particularly the strong ⁵D0 → ⁷F2 transition near 【612 nm】, can produce highly saturated red electroluminescence. Device performance is influenced by the efficiency of charge transport and energy transfer to …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-106

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 7.12661e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `27.1 months` (줄 128, 뒤): …Research Reactor (JRR)-4 reactor. Patients subsequently received an X-ray boost after completion of BNCT. The overall median survival time (MeST) was 【27.1 months】, and the 1-year and 2-year survival rates were 87.5% and 62.5%, respectively.
  - [Neutron capture therapy of cancer] raw `27.1` (줄 145, 머리글): | JRR4, Japan | 15 (1998–2007) | BPA 250 mg/kg + BSH 5 g | 10.8 (recurrent), 【27.1】 (+ X-ray) |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-107

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 2.47e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `247 pm` (줄 62, 뒤): …. It is a ductile metal with a hardness comparable to that of silver. Praseodymium is calculated to have a very large atomic radius; with a radius of 【247 pm】, barium, rubidium and caesium are larger. However, observationally, it is usually 185 pm.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 2.38e-10: [사마륨] raw `238 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 185 pm (실험값) 【238 pm】 (계산값)
  - base 2.28e-10: [디스프로슘] raw `228 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 175 pm (실험값) 【228 pm】 (계산값)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [툴륨] `247`:   - 기화열: 【247】 kJ/mol
  - [디스프로슘] `247`:   - 푸아송 비: (α form) 0.【247】

### R-en-108

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 823, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Samarium–cobalt magnet] raw `823 K` (줄 13, 뒤): - These magnets have good temperature stability, maximum use temperatures from 250 °C (523 K) to 550 °C (【823 K】) and Curie temperatures from 700 °C (973 K) to 800 °C (1,070 K).
  - [Samarium–cobalt magnet] raw `550 °C` (줄 13, 뒤): - These magnets have good temperature stability, maximum use temperatures from 250 °C (523 K) to 【550 °C】 (823 K) and Curie temperatures from 700 °C (973 K) to 800 °C (1,070 K).
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-109

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 538100, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `538.1 kJ/mol` (줄 29, 뒤):   - Ionization energies: 1st: 【538.1 kJ/mol】, 2nd: 1067 kJ/mol, 3rd: 1850.3 kJ/mol
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 544500: [사마륨] raw `544.5 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 【544.5 kJ/mol】, 2차: 1070 kJ/mol, 3차: 2260 kJ/mol
  - base 523500: [루테튬] raw `523.5 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 【523.5 kJ/mol】, 2차: 1340 kJ/mol, 3차: 2022.3 kJ/mol
  - base 573000: [디스프로슘] raw `573.0 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 【573.0 kJ/mol】, 2차: 1130 kJ/mol, 3차: 2200 kJ/mol
  - base 589300: [어븀] raw `589.3 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 【589.3 kJ/mol】, 2차: 1150 kJ/mol, 3차: 2194 kJ/mol
  - base 596700: [툴륨] raw `596.7 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 【596.7 kJ/mol】, 2차: 1160 kJ/mol, 3차: 2285 kJ/mol
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-110

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 에너지, base 4.80653e-13, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `3.0 MeV` (줄 180, 뒤): …eutrons, though other nuclear reactions also have been considered. The lithium-7 reaction requires a proton accelerator with energies between 1.9 and 【3.0 MeV】, while the beryllium-9 reaction typically uses accelerators with energies between 5 and 30 MeV. Aside from the lower proton energy that the lithium-7…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5.08675e-13: [네오디뮴 동위 원소] raw `3174.9(4) keV` (줄 37, 한쪽 언어 쪽): | ¹³⁸ᵐNd | 【3174.9(4) keV】 | 3174.9(4) keV | 3174.9(4) keV | 410(50) ns |  |  | (10+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [디스프로슘] `3.0`:   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁵⁴Dy 인공 【3.0】E+6 y α 2.947 ¹⁵⁰Gd ¹⁵⁶Dy 0.06% 안정 ¹⁵⁸Dy 0.10% 안정 ¹⁶⁰Dy 2.34% 안정 ¹⁶¹Dy 18.91% 안정…
  - [터븀 동위 원소] `3.0`: | ¹⁶⁴Tb | 65 | 99 | 163.93335(11) | 【3.0】(1) min | β⁻ | ¹⁶⁴Dy | (5+) |  |  |

### R-en-111

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 6200, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `6.20 kJ/mol` (줄 21, 뒤):   - Heat of fusion: 【6.20 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-112

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 6890, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `6.89 kJ/mol` (줄 21, 뒤):   - Heat of fusion: 【6.89 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-113

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 1138.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `865 °C` (줄 69, 뒤): …anthanum has a hexagonal crystal structure at room temperature (α-La). At 310 °C, lanthanum changes to a face-centered cubic structure (β-La), and at 【865 °C】, it changes to a body-centered cubic structure (γ-La).
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1097: [이터븀] raw `1097 K` (줄 16, 두 언어 쪽):   - 녹는점: 【1097 K】
  - base 1195.15: [사마륨] raw `922°C` (줄 61, 한쪽 언어 쪽): …삼방정계 구조(α 구조)를 가지며, 731°C 이상의 고온으로 가열하면 육방정계 구조로 전환된다. 전환 온도는 불순물에 따라 달라지기도 한다. 【922°C】 이상으로 가열하면 다시 결정 구조가 바뀌어 체심 입방정계 구조가 된다. 실온에서는 상자성이며 14.8K 이하로 냉각시키면 반강자성을 띤다.
  - base 1068.15: [이터븀] raw `795 °C` (줄 62, 두 언어 쪽): …정 구조를 가지는데 알파 결정 구조는 -13 °C이하에서 존재하고 낮은 온도에서 안정하며 육방정계 결정 구조를 가지고 있고, 감마 결정 구조는 【795 °C】이상에서 존재하고 체심입방격자 구조를 갖는다. 베타 결정 구조는 상온에서 존재하며 면심입방격자 구조를 가지고 있다. 베타 결정 구조는 금속적인 …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-114

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 에너지, base 8.01088e-20, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `0.5 eV` (줄 27, 뒤): …eutrons, the source of which, until recently, has been specially designed nuclear reactors and now is neutron accelerators. Until 1994, low-energy (< 【0.5 eV】) thermal neutron beams were used in Japan and the United States, but since they have a limited depth of penetration in tissues, higher-energy (0.5–10…
  - [Neutron capture therapy of cancer] raw `0.5` (줄 27, 뒤): …0.5 eV) thermal neutron beams were used in Japan and the United States, but since they have a limited depth of penetration in tissues, higher-energy (【0.5】–10,000 eV) epithermal neutron beams, which have a greater depth of penetration, were used in clinical trials in the United States, Europe, Japan, Arg…
  - [Neutron capture therapy of cancer] raw `0.5 eV` (줄 81, 뒤): … 2014, neutron sources for NCT were limited to nuclear reactors. Reactor-derived neutrons are classified according to their energies as thermal (En < 【0.5 eV】), epithermal (0.5–10,000 eV), or fast (En >10 keV). Thermal neutrons are the most important for BNCT, since they usually initiate the ¹⁰B(n,α)⁷Li cap…
  - [Neutron capture therapy of cancer] raw `0.5` (줄 81, 뒤): …s for NCT were limited to nuclear reactors. Reactor-derived neutrons are classified according to their energies as thermal (En < 0.5 eV), epithermal (【0.5】–10,000 eV), or fast (En >10 keV). Thermal neutrons are the most important for BNCT, since they usually initiate the ¹⁰B(n,α)⁷Li capture reaction. How…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [터븀 동위 원소] `0.5`: | ¹⁴²ᵐ¹Tb | 280.2(10) keV | 280.2(10) keV | 280.2(10) keV | 303(17) ms | β⁺ (【0.5】%) | ¹⁴²Gd | (5-) |  |  |

### R-en-115

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 4e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `400 MPa` (줄 47, 뒤):   - Brinell hardness: 350–【400 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 4.12e+08: [사마륨] raw `412 MPa` (줄 40, 한쪽 언어 쪽):   - 비커스 굳기: 【412 MPa】
  - base 4.41e+08: [사마륨] raw `441 MPa` (줄 41, 한쪽 언어 쪽):   - 브리넬 굳기: 【441 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [사마륨] `400`: … 사마륨과 코발트의 비율은 1:5이거나 2:17인 경우가 많다. 이러한 자석은 철보다 1만배 이상 강력한 것이다. 또, 네오디뮴 자석은 300~【400】°C 가량의 온도에서 자성을 잃는데 비해 사마륨-코발트 자석은 700°C 이상의 고온에서도 자성을 잃지 않는다. 주로 소형 전동기, 헤드셋, 기…
  - [이트륨] `400`: … 안에서 750 °C 로 가열될 때 1 μm의 두께를 가질 수 있다. 잘게 나눠졌을 때, 이트륨은 공기 중에서 불안정하다. 작은 이트륨 조각은 【400】 °C 이상의 온도에서 불이 붙을 수 있다. 질화 이트륨(YN)은 이트륨이 질소(N) 기체 안에서 1000 °C 로 가열될 때 생성된다.

### R-en-116

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 145040, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `40.289 h` (줄 53, 뒤): …n­dance half-life (t1/2) mode pro­duct ¹³⁷La synth 6×10⁴ y ε ¹³⁷Ba ¹³⁸La 0.0889999999% 1.03×10¹¹ y β⁺ ¹³⁸Ba β⁻ ¹³⁸Ce ¹³⁹La 99.911% stable ¹⁴⁰La synth 【40.289 h】 β⁻ ¹⁴⁰Ce
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-117

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 1373.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `1100` (줄 223, 뒤): The reaction is carried out in refractory apparatus, commonly using tantalum, at approximately 【1100】–1200 °C. The europium produced is considerably more volatile than the lanthanum reductant and lanthanum oxide product, so it distils from the reactio…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1345: [사마륨] raw `1345 K` (줄 16, 한쪽 언어 쪽):   - 녹는점: 【1345 K】
  - base 1469: [이터븀] raw `1469 K` (줄 17, 두 언어 쪽):   - 끓는점: 【1469 K】
  - base 1273.15: [이트륨] raw `1000 °C` (줄 64, 한쪽 언어 쪽): …중에서 불안정하다. 작은 이트륨 조각은 400 °C 이상의 온도에서 불이 붙을 수 있다. 질화 이트륨(YN)은 이트륨이 질소(N) 기체 안에서 【1000 °C】 로 가열될 때 생성된다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-118

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 1.25e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `12.5 GPa` (줄 67, 뒤): …e. Under pressure, europium undergoes a series of structural transformations. The bcc phase transforms to a hexagonal close-packed structure at about 【12.5 GPa】, which remains stable to about 31.5 GPa. Above this pressure europium adopts an incommensurately modulated monoclinic structure, known as Eu-IV, whic…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-119

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 422000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `422 tonnes` (줄 217, 뒤): …f mixed rare-earth production rather than mined separately. European Commission estimates placed average global production of europium oxide at about 【422 tonnes】 per year in 2012–2016. China accounted for approximately 86% of this production, followed by Australia at 6%, the United States and Russia at about 2…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-120

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.98e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `198±6 pm` (줄 31, 뒤):   - Covalent radius: 【198±6 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
  - base 1.85e-10: [사마륨] raw `185 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【185 pm】 (실험값) 238 pm (계산값)
  - base 1.8e-10: [이트륨] raw `180 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【180 pm】 (실험값)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-121

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 12.6, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `12.6 K` (줄 123, 뒤): …s, europium is divalent in EuB6. EuB6 is a ferromagnetic semimetal and undergoes two closely spaced electronic and magnetic transitions near 15.5 and 【12.6 K】. Its unusual transport properties, including large magnetoresistance, have been associated with the formation and subsequent overlap of magnetic pola…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-122

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 2280, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `2280 m/s` (줄 43, 뒤):   - Speed of sound thin rod: 【2280 m/s】 (at 20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2130: [사마륨] raw `2130 m/s` (줄 38, 한쪽 언어 쪽):   - 음속 (얇은 막대): 【2130 m/s】 (20 °C)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-123

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 6.1799e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `23.5 months` (줄 124, 뒤): …l dose of 20 to 30 Gy was administered, divided into 2 Gy daily fractions. The MST of this group of patients (with newly diagnosed glioblastomas) was 【23.5 months】 and no significant toxicity was observed, other than hair loss (alopecia). However, a significant subset of these patients, a high proportion of whic…
  - [Neutron capture therapy of cancer] raw `23.5` (줄 144, 머리글): | KURRI, Japan | 40 (1998–2008) | BPA 500 mg/kg | 【23.5】 (primary + X-ray) |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.05906e+07: [툴륨] raw `1.92 y` (줄 46, 두 언어 쪽): … 인공 93.1 d ε 1.679 ¹⁶⁸Er ¹⁶⁹Tm 100% 안정 ¹⁷⁰Tm 인공 128.6 d β⁻ 0.968 ¹⁷⁰Yb ¹⁷¹Tm 인공 【1.92 y】 β⁻ 0.096 ¹⁷¹Yb
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-124

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 9210, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `9.21 kJ/mol` (줄 21, 뒤):   - Heat of fusion: 【9.21 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8620: [사마륨] raw `8.62 kJ/mol` (줄 20, 한쪽 언어 쪽):   - 융해열: 【8.62 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-125

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 1.82e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `182 pm` (줄 30, 뒤):   - Atomic radius: empirical: 【182 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1.8e-10: [이트륨] raw `180 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【180 pm】 (실험값)
  - base 1.85e-10: [사마륨] raw `185 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【185 pm】 (실험값) 238 pm (계산값)
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
  - base 1.75e-10: [툴륨] raw `175 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 【175 pm】 (실험값) 222 pm (계산값)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이터븀] `182`: 이터븀의 동위원소들은 ¹⁴⁸Yb의 경우인 147.9674 u에서부터 ¹⁸¹Yb의 경우인 【182】.9562 u의 원자량 범위를 가진다. 이터븀의 가장 안정한 동위원소 ¹⁷⁴Yb보다 중성자수가 적은 방사성 동위원소들의 일반적인 방사성 붕괴 형…

### R-en-126

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 1000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `1000 kg` (줄 158, 뒤): The price for a (metric) ton [【1000 kg】] of Lanthanum oxide 99% (FOB China in USD/Mt) is given by the Institute of Rare Earths Elements and Strategic Metals (IREESM) as below $2,000 for mos…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨] `1000`: …중에서 불안정하다. 작은 이트륨 조각은 400 °C 이상의 온도에서 불이 붙을 수 있다. 질화 이트륨(YN)은 이트륨이 질소(N) 기체 안에서 【1000】 °C 로 가열될 때 생성된다.

### R-en-127

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 에너지, base 4.00544e-21, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `0.025eV` (줄 75, 뒤): … culture (in vitro). Third, gamma rays and internal conversion and Auger electrons are products of the ¹⁵⁷Gd(n,γ)¹⁵⁸Gd capture reaction (¹⁵⁷Gd + nth (【0.025eV】) → [¹⁵⁸Gd] → ¹⁵⁸Gd + γ + 7.94 MeV). Though the gamma rays have longer pathlengths, orders of magnitude greater depths of penetration compared with al…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-128

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 3.57645e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `13.6 months` (줄 164, 뒤): …sing an epithermal beam. In this series, there were complete regressions in 12 cases, 10 partial regressions, and progression in 3 cases. The MST was 【13.6 months】, and the 6-year survival was 24%. Significant treatment related complications ("adverse" events) included transient mucositis, alopecia, and, rarely,…
  - [Neutron capture therapy of cancer] raw `13.7 months` (줄 136, 뒤): …es were seen in patients with lower-grade tumors. In 35 of 36 patients, there was tumor shrinkage, and the median progression-free survival (PFS) was 【13.7 months】. There was good local control of the patients' tumors, as evidenced by the fact that only 22.2% of them experienced local recurrence of their tumors.…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-129

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 열팽창, base 5.1e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `5.1×10⁻⁶/K` (줄 35, 뒤):   - Thermal expansion: 【5.1×10⁻⁶/K】 (at 20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-130

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 331000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `331 kJ/mol` (줄 22, 뒤):   - Heat of vaporization: 【331 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 365000: [이트륨] raw `365 kJ/mol` (줄 21, 한쪽 언어 쪽):   - 기화열: 【365 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `331`: | ⁹⁸Y | 39 | 59 | 97.922203(26) | 0.548(2) s | β⁻, n (.【331】%) | ⁹⁷Zr | (0)- |  |  |

### R-en-131

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.52525e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `5.8 months` (줄 158, 뒤): …egarding the evaluation of the results. Based on incomplete survival data, the MeST was reported as 14.2 months and the time to tumor progression was 【5.8 months】. However, more careful examination of the complete survival data revealed that the MeST was 17.7 months compared to 15.5 months that has been reporte…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [이트륨 동위 원소] `5.8`: | ⁷⁸ᵐY | 0(500)# keV | 0(500)# keV | 0(500)# keV | 【5.8】(5) s |  |  | 5+# |  |  |
  - [터븀 동위 원소] `5.8`: | ¹⁵⁰ᵐTb | 457(29) keV | 457(29) keV | 457(29) keV | 【5.8】(2) min | β⁺ | ¹⁵⁰Gd | 9+ |  |  |
  - [터븀 동위 원소] `5.8`: | ¹⁵⁰ᵐTb | 457(29) keV | 457(29) keV | 457(29) keV | 【5.8】(2) min | IT (드묾) | ¹⁵⁰Tb | 9+ |  |  |

### R-en-132

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 3.6e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `360` (줄 46, 뒤):   - Vickers hardness: 【360】–1750 MPa
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.43e+08: [이터븀] raw `343 MPa` (줄 42, 두 언어 쪽):   - 브리넬 굳기: 【343 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [이트륨 동위 원소] `360`: | ¹⁰²ᵐY | 200(200)# keV | 200(200)# keV | 200(200)# keV | 【360】(40) ms | β⁻ (94%) | ¹⁰²Zr | high |  |  |
  - [이트륨 동위 원소] `360`: | ¹⁰²ᵐY | 200(200)# keV | 200(200)# keV | 200(200)# keV | 【360】(40) ms | β⁻, n (6%) | ¹⁰¹Zr | high |  |  |

### R-en-133

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.58767e+08, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `98.4 months` (줄 136, 뒤): The median OS after BNCT was 29.6 months and 【98.4 months】 after diagnosis. Better responses were seen in patients with lower-grade tumors. In 35 of 36 patients, there was tumor shrinkage, and the median prog…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-134

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 86400, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `24-hour` (줄 182, 뒤): …sirable to reduce the treatment time both for patient comfort during immobilization and to increase the number of patients that could be treated in a 【24-hour】 period. Increasing the neutron beam intensity for the same proton current by adjusting the BSA is often achieved at the cost of reduced beam quality …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 87840: [터븀 동위 원소] raw `24.4(10) h` (줄 75, 한쪽 언어 쪽): | ¹⁵⁶ᵐ¹Tb | 54(3) keV | 54(3) keV | 54(3) keV | 【24.4(10) h】 | IT | ¹⁵⁶Tb | (7-) |  |  |
  - base 81720: [터븀 동위 원소] raw `22.7(5) h` (줄 70, 한쪽 언어 쪽): | ¹⁵⁴ᵐ²Tb | 200(150)# keV | 200(150)# keV | 200(150)# keV | 【22.7(5) h】 |  |  | 7- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [디스프로슘] `24`:   - 전단 탄성 계수: (α form) 【24】.7 GPa
  - [디스프로슘] `24`: …Dy 0.06% 안정 ¹⁵⁸Dy 0.10% 안정 ¹⁶⁰Dy 2.34% 안정 ¹⁶¹Dy 18.91% 안정 ¹⁶²Dy 25.51% 안정 ¹⁶³Dy 【24】.90% 안정 ¹⁶⁴Dy 28.18% 안정
  - [어븀] `24`:   - 전기 음성도 (폴링 척도): 1.【24】
  - [사마륨] `24`: …¹⁴⁶Sm 인공 1.03×10⁸y α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 1.06×10¹¹y α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.【24】% 7×10¹⁵y α 1.986 ¹⁴⁴Nd ¹⁴⁹Sm 13.82% >2×10¹⁵ y α 1.870 ¹⁴⁵Nd ¹⁵⁰Sm 7.38% 안정 ¹⁵²S…
  - [이트륨] `24`:   - 액체(녹는점)일 때: 4.【24】 g/cm³

### R-en-135

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 0.197, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `197+74 −71 ms` (줄 161, 뒤): …he neutron-rich isotope ¹⁷⁰Eu, at the upper end of this range, was first experimentally characterised in 2022 and was measured to have a half-life of 【197+74 −71 ms】. The longest-lived artificial isotope is ¹⁵⁰Eu, with a half-life of 36.9 years. Other comparatively long-lived isotopes are ¹⁵²Eu (13.517 years), ¹⁵⁴…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 0.18: [이트륨 동위 원소] raw `180(60) ms` (줄 87, 두 언어 쪽): | ¹⁰⁴Y | 39 | 65 | 103.94105(43)# | 【180(60) ms】 | β⁻ | ¹⁰⁴Zr |  |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-136

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 2.88e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `28.8 GPa` (줄 42, 뒤):   - Bulk modulus: 【28.8 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 2.83e+10: [어븀] raw `28.3 GPa` (줄 35, 한쪽 언어 쪽):   - 전단 탄성 계수: 【28.3 GPa】
  - base 2.72e+10: [루테튬] raw `27.2 GPa` (줄 34, 두 언어 쪽):   - 전단 탄성 계수: 【27.2 GPa】
  - base 3.05e+10: [툴륨] raw `30.5 GPa` (줄 35, 두 언어 쪽):   - 전단 탄성 계수: 【30.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-137

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 에너지, base 2.36962e-14, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `147.9 keV` (줄 163, 뒤): … known. Among the longest-lived are ¹⁵⁰ᵐEu, with a half-life of 12.8 hours, and ¹⁵²ᵐ¹Eu, with a half-life of 9.3116 hours; another isomer of ¹⁵²Eu at 【147.9 keV】 has a half-life of about 96 minutes. Most neutron-deficient europium isotopes decay towards isotopes of samarium by electron capture or positron emis…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2.61435e-14: [터븀 동위 원소] raw `163.175(5) keV` (줄 64, 한쪽 언어 쪽): | ¹⁵³ᵐTb | 【163.175(5) keV】 | 163.175(5) keV | 163.175(5) keV | 186(4) µs |  |  | 11/2- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-138

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.45165e+26, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `4.6×10¹⁸ y` (줄 51, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁵⁰Eu synth 36.9 y β⁺ ¹⁵⁰Sm ¹⁵¹Eu 47.7999999999% 【4.6×10¹⁸ y】 α ¹⁴⁷Pm ¹⁵²Eu synth 13.517 y β⁺ ¹⁵²Sm β⁻ ¹⁵²Gd ¹⁵³Eu 52.2% stable ¹⁵⁴Eu synth 8.592 y β⁻ ¹⁵⁴Gd ε ¹⁵⁴Sm ¹⁵⁵Eu synth 4.742 y β⁻ ¹⁵⁵Gd
  - [Europium] raw `4.6×10¹⁸ years` (줄 55, 뒤): … nearly equal proportions, ¹⁵¹Eu and ¹⁵³Eu. ¹⁵³Eu is observationally stable, while ¹⁵¹Eu is a very long-lived alpha emitter with a half-life of about 【4.6×10¹⁸ years】.
  - [Europium] raw `4.62×10¹⁸ years` (줄 159, 뒤): …ectively. ¹⁵³Eu is observationally stable, whereas ¹⁵¹Eu is a primordial radioisotope. It undergoes alpha decay to ¹⁴⁷Pm with a measured half-life of 【4.62×10¹⁸ years】. This half-life is about 300 million times the age of the Universe, so the decay has a negligible effect on the natural isotopic composition of europ…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `4.6`: | ⁸⁴Y | 39 | 45 | 83.92039(10) | 【4.6】(2) s | β⁺ | ⁸⁴Sr | 1+ |  |  |

### R-en-139

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 2.82e+07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `282 bar` (줄 76, 뒤): …e most oxidised product of the combustion of praseodymium and can be obtained by either reaction of praseodymium metal with pure oxygen at 400 °C and 【282 bar】 or by disproportionation of Pr6O11 in boiling acetic acid. The reactivity of praseodymium conforms to periodic trends, as it is one of the first and …
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-140

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.73494e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `10.4` (줄 148, 머리글): | HFR, Netherlands | 26 (1997–2002) | BSH 100 mg/kg | 【10.4】 – 13.2 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-141

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 3737, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `3737 K` (줄 18, 뒤):   - Boiling point: 【3737 K】 ​(3464 °C, ​6267 °F)
  - [Lanthanum] raw `6267 °F` (줄 18, 뒤):   - Boiling point: 3737 K ​(3464 °C, ​【6267 °F】)
  - [Lanthanum] raw `3464 °C` (줄 18, 뒤):   - Boiling point: 3737 K ​(【3464 °C】, ​6267 °F)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3675: [루테튬] raw `3675 K` (줄 17, 두 언어 쪽):   - 끓는점: 【3675 K】
  - base 3609: [이트륨] raw `3609 K` (줄 17, 한쪽 언어 쪽):   - 끓는점: 【3609 K】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-142

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 3.36607e+07, 표 안 예, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `12.8` (줄 142, 머리글): | BMRR, US | 53 (1994–1999) | BPA 250–330 mg/kg | 【12.8】 |
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-143

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 1.82e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `18.2 GPa` (줄 40, 뒤):   - Young's modulus: 【18.2 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.95e+10: [사마륨] raw `19.5 GPa` (줄 36, 한쪽 언어 쪽):   - 전단 탄성 계수: (α form) 【19.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-144

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.17245e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `13.57 d` (줄 52, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁴¹Pr 100% stable ¹⁴²Pr synth 19.12 h β⁻ ¹⁴²Nd ε ¹⁴²Ce ¹⁴³Pr synth 【13.57 d】 β⁻ ¹⁴³Nd
  - [Praseodymium] raw `13.57 days` (줄 105, 뒤): …been synthesized. All of these isotopes have half-lives under a day (and most under a minute), with the single exception of ¹⁴³Pr with a half-life of 【13.57 days】. Both ¹⁴¹Pr and ¹⁴³Pr occur as fission products of uranium (as do heavier isotopes). The primary decay mode of isotopes lighter than ¹⁴¹Pr is positro…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-145

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 흡수선량, base 54.3, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `54.3 Gy` (줄 158, 뒤): …dy. All were treated with 2 fields, and the average whole-brain dose was 3.2–6.1 Gy (weighted), and the minimum dose to the tumor ranged from 15.4 to 【54.3 Gy】 (w). There has been some disagreement among the Swedish investigators regarding the evaluation of the results. Based on incomplete survival data, the…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-146

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 열전도율, base 13.9, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `13.9 W/(m⋅K)` (줄 36, 뒤):   - Thermal conductivity: est. 【13.9 W/(m⋅K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 14.5: [어븀] raw `14.5 W/(m·K)` (줄 32, 한쪽 언어 쪽):   - 열전도율: 【14.5 W/(m·K)】
  - base 13.3: [사마륨] raw `13.3 W/(m·K)` (줄 32, 한쪽 언어 쪽):   - 열전도율: 【13.3 W/(m·K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `13.9`: | ⁸⁸ᵐ¹Y | 674.55(4) keV | 674.55(4) keV | 674.55(4) keV | 【13.9】(2) ms | IT | ⁸⁸Y | (8)+ |  |  |

### R-en-147

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 2.07e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `207±8 pm` (줄 31, 뒤):   - Covalent radius: 【207±8 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 2.22e-10: [툴륨] raw `222 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 175 pm (실험값) 【222 pm】 (계산값)
  - base 2.26e-10: [어븀] raw `226 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 175 pm (실험값) 【226 pm】 (계산값)
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이터븀] `207`:   - 푸아송 비: (β form) 0.【207】

### R-en-148

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.49646e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `4.742 y` (줄 51, 뒤): …Sm ¹⁵¹Eu 47.7999999999% 4.6×10¹⁸ y α ¹⁴⁷Pm ¹⁵²Eu synth 13.517 y β⁺ ¹⁵²Sm β⁻ ¹⁵²Gd ¹⁵³Eu 52.2% stable ¹⁵⁴Eu synth 8.592 y β⁻ ¹⁵⁴Gd ε ¹⁵⁴Sm ¹⁵⁵Eu synth 【4.742 y】 β⁻ ¹⁵⁵Gd
  - [Europium] raw `4.742 years` (줄 161, 뒤): …al isotope is ¹⁵⁰Eu, with a half-life of 36.9 years. Other comparatively long-lived isotopes are ¹⁵²Eu (13.517 years), ¹⁵⁴Eu (8.592 years) and ¹⁵⁵Eu (【4.742 years】); all other known ground-state europium radioisotopes have half-lives shorter than 100 days.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-149

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 15.5, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `15.5` (줄 123, 뒤): …exaborides, europium is divalent in EuB6. EuB6 is a ferromagnetic semimetal and undergoes two closely spaced electronic and magnetic transitions near 【15.5】 and 12.6 K. Its unusual transport properties, including large magnetoresistance, have been associated with the formation and subsequent overlap of ma…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 14.8: [사마륨] raw `14.8K` (줄 61, 한쪽 언어 쪽): …온도는 불순물에 따라 달라지기도 한다. 922°C 이상으로 가열하면 다시 결정 구조가 바뀌어 체심 입방정계 구조가 된다. 실온에서는 상자성이며 【14.8K】 이하로 냉각시키면 반강자성을 띤다.
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-150

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 3.15e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `31.5 GPa` (줄 67, 뒤): …series of structural transformations. The bcc phase transforms to a hexagonal close-packed structure at about 12.5 GPa, which remains stable to about 【31.5 GPa】. Above this pressure europium adopts an incommensurately modulated monoclinic structure, known as Eu-IV, which is stable to about 37 GPa; another str…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.05e+10: [툴륨] raw `30.5 GPa` (줄 35, 두 언어 쪽):   - 전단 탄성 계수: 【30.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-151

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 비열, base 193.031, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `193.031 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【193.031 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-152

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 비저항, base 7e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `0.700 µΩ⋅m` (줄 37, 뒤):   - Electrical resistivity: poly: 【0.700 µΩ⋅m】 (at r.t.)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6.76e-07: [툴륨] raw `676 n Ω·m` (줄 33, 두 언어 쪽):   - 전기 저항도: (실온) (poly) 【676 n Ω·m】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-153

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 1.48e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `14.8 GPa` (줄 41, 뒤):   - Shear modulus: 【14.8 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 3개:
  - [이트륨 동위 원소] `14.8`: | ⁷⁹Y | 39 | 40 | 78.93735(48) | 【14.8】(6) s | β⁺ (>99.9%) | ⁷⁹Sr | (5/2+)# |  |  |
  - [이트륨 동위 원소] `14.8`: | ⁷⁹Y | 39 | 40 | 78.93735(48) | 【14.8】(6) s | β⁺, p (<0.1%) | ⁷⁸Rb | (5/2+)# |  |  |
  - [사마륨] `14.8`: …온도는 불순물에 따라 달라지기도 한다. 922°C 이상으로 가열하면 다시 결정 구조가 바뀌어 체심 입방정계 구조가 된다. 실온에서는 상자성이며 【14.8】K 이하로 냉각시키면 반강자성을 띤다.

### R-en-154

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 길이, base 2.03e-10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `203±7 pm` (줄 31, 뒤):   - Covalent radius: 【203±7 pm】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 1.87e-10: [이터븀] raw `187±8 pm` (줄 29, 두 언어 쪽):   - 공유 반지름: 【187±8 pm】
  - base 2.22e-10: [툴륨] raw `222 pm` (줄 28, 두 언어 쪽):   - 원자 반지름: 175 pm (실험값) 【222 pm】 (계산값)
  - base 1.85e-10: [사마륨] raw `185 pm` (줄 28, 한쪽 언어 쪽):   - 원자 반지름: 【185 pm】 (실험값) 238 pm (계산값)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-155

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 6145, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `6.145 g/cm³` (줄 19, 뒤):   - Density (at 20° C): 【6.145 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6210: [이터븀] raw `6.21 g/cm³` (줄 19, 두 언어 쪽):   - 액체(녹는점)일 때: 【6.21 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-156

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 3.7e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `3,700 tonnes` (줄 127, 뒤): …is based on data from the U.S. Geological Survey, worldwide production of praseodymium was estimated at 2,000 tonnes in 2020 and increased to roughly 【3,700 tonnes】 in 2022.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-157

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 속도, base 2475, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `2475 m/s` (줄 43, 뒤):   - Speed of sound thin rod: 【2475 m/s】 (at 20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 2710: [디스프로슘] raw `2710 m/s` (줄 38, 두 언어 쪽):   - 음속 (얇은 막대): 【2710 m/s】 (20 °C)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-158

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 2e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `2,000 tonnes` (줄 127, 뒤): …s of lanthanides. According to industry analysis based on data from the U.S. Geological Survey, worldwide production of praseodymium was estimated at 【2,000 tonnes】 in 2020 and increased to roughly 3,700 tonnes in 2022.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-159

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 2.086e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `2086 kJ/mol` (줄 29, 뒤):   - Ionization energies: 1st: 527 kJ/mol, 2nd: 1020 kJ/mol, 3rd: 【2086 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 5개(가까운 차례):
  - base 2.0223e+06: [루테튬] raw `2022.3 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 523.5 kJ/mol, 2차: 1340 kJ/mol, 3차: 【2022.3 kJ/mol】
  - base 2.194e+06: [어븀] raw `2194 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 589.3 kJ/mol, 2차: 1150 kJ/mol, 3차: 【2194 kJ/mol】
  - base 1.98e+06: [이트륨] raw `1980 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 600 kJ/mol, 2차: 1180 kJ/mol, 3차: 【1980 kJ/mol】
  - base 2.26e+06: [사마륨] raw `2260 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 544.5 kJ/mol, 2차: 1070 kJ/mol, 3차: 【2260 kJ/mol】
  - base 2.285e+06: [툴륨] raw `2285 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 596.7 kJ/mol, 2차: 1160 kJ/mol, 3차: 【2285 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-160

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 1.085e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `1085 kJ/mol` (줄 29, 뒤):   - Ionization energies: 1st: 547.1 kJ/mol, 2nd: 【1085 kJ/mol】, 3rd: 2404 kJ/mol
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 1.07e+06: [사마륨] raw `1070 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 544.5 kJ/mol, 2차: 【1070 kJ/mol】, 3차: 2260 kJ/mol
  - base 1.13e+06: [디스프로슘] raw `1130 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 573.0 kJ/mol, 2차: 【1130 kJ/mol】, 3차: 2200 kJ/mol
  - base 1.15e+06: [어븀] raw `1150 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 589.3 kJ/mol, 2차: 【1150 kJ/mol】, 3차: 2194 kJ/mol
  - base 1.1748e+06: [이터븀] raw `1174.8 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 603.4 kJ/mol, 2차: 【1174.8 kJ/mol】, 3차: 2417 kJ/mol
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-161

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 1.75e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `1750 MPa` (줄 46, 뒤):   - Vickers hardness: 360–【1750 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.6212e+09: [이터븀] raw `16000 기압` (줄 62, 두 언어 쪽): …심입방격자 구조를 갖는다. 베타 결정 구조는 상온에서 존재하며 면심입방격자 구조를 가지고 있다. 베타 결정 구조는 금속적인 전기전도도를 갖는데 【16000 기압】(1.6 GPa)에서는 반도체가 되고 39000기압(3.9 GPa)에서는 10배나 전기저항이 상승한다. 하지만 신기하게도 40000기압에서는(4…
  - base 1.6e+09: [이터븀] raw `1.6 GPa` (줄 62, 두 언어 쪽): … 갖는다. 베타 결정 구조는 상온에서 존재하며 면심입방격자 구조를 가지고 있다. 베타 결정 구조는 금속적인 전기전도도를 갖는데 16000 기압(【1.6 GPa】)에서는 반도체가 되고 39000기압(3.9 GPa)에서는 10배나 전기저항이 상승한다. 하지만 신기하게도 40000기압에서는(4.0 GPa) …
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-162

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 1.16448e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `36.9 y` (줄 51, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁵⁰Eu synth 【36.9 y】 β⁺ ¹⁵⁰Sm ¹⁵¹Eu 47.7999999999% 4.6×10¹⁸ y α ¹⁴⁷Pm ¹⁵²Eu synth 13.517 y β⁺ ¹⁵²Sm β⁻ ¹⁵²Gd ¹⁵³Eu 52.2% stable ¹⁵⁴Eu synth 8.592 y β⁻ ¹⁵⁴Gd ε ¹⁵⁴Sm ¹⁵⁵Eu…
  - [Europium] raw `36.9 years` (줄 161, 뒤): …tally characterised in 2022 and was measured to have a half-life of 197+74 −71 ms. The longest-lived artificial isotope is ¹⁵⁰Eu, with a half-life of 【36.9 years】. Other comparatively long-lived isotopes are ¹⁵²Eu (13.517 years), ¹⁵⁴Eu (8.592 years) and ¹⁵⁵Eu (4.742 years); all other known ground-state europium…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-163

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 에너지, base 3.04414e-13, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `1.9` (줄 180, 뒤): …nerate neutrons, though other nuclear reactions also have been considered. The lithium-7 reaction requires a proton accelerator with energies between 【1.9】 and 3.0 MeV, while the beryllium-9 reaction typically uses accelerators with energies between 5 and 30 MeV. Aside from the lower proton energy that t…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `1.9`: | ⁹⁹Y | 39 | 60 | 98.924636(26) | 1.470(7) s | β⁻, n (【1.9】%) | ⁹⁸Zr | (5/2+) |  |  |

### R-en-164

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 1.02e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `1020 kJ/mol` (줄 29, 뒤):   - Ionization energies: 1st: 527 kJ/mol, 2nd: 【1020 kJ/mol】, 3rd: 2086 kJ/mol
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.07e+06: [사마륨] raw `1070 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 544.5 kJ/mol, 2차: 【1070 kJ/mol】, 3차: 2260 kJ/mol
  - base 1.13e+06: [디스프로슘] raw `1130 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 573.0 kJ/mol, 2차: 【1130 kJ/mol】, 3차: 2200 kJ/mol
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-165

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 3.66e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `36.6 GPa` (줄 40, 뒤):   - Young's modulus: α form: 【36.6 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 3.78e+10: [사마륨] raw `37.8 GPa` (줄 37, 한쪽 언어 쪽):   - 부피 탄성 계수: (α form) 【37.8 GPa】
  - base 4.05e+10: [디스프로슘] raw `40.5 GPa` (줄 37, 두 언어 쪽):   - 부피 탄성 계수: (α form) 【40.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-166

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 흡수선량, base 6.1, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `6.1 Gy` (줄 158, 뒤): …e BPA was well-tolerated by the 30 patients who were enrolled in this study. All were treated with 2 fields, and the average whole-brain dose was 3.2–【6.1 Gy】 (weighted), and the minimum dose to the tumor ranged from 15.4 to 54.3 Gy (w). There has been some disagreement among the Swedish investigators regar…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-167

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 176000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `176 kJ/mol` (줄 22, 뒤):   - Heat of vaporization: 【176 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 165000: [사마륨] raw `165 kJ/mol` (줄 21, 한쪽 언어 쪽):   - 기화열: 【165 kJ/mol】
  - base 159000: [이터븀] raw `159 kJ/mol` (줄 21, 두 언어 쪽):   - 기화열: 【159 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [이터븀] `176`:   - 원자 반지름: 【176】 pm (실험값)
  - [루테튬] `176`: 루테튬은 지각에서 은보다 훨씬 더 흔하지만 특별히 풍부한 원소는 아니다. 구체적으로 이용된 사례는 거의 없다. 루테튬-【176】은 상대적으로 풍부한(2.5%) 방사성 동위원소로 반감기가 약 380억년으로 광물과 운석의 나이를 결정하는 데 사용된다. 루테튬은 일반적으로 이…
  - [네오디뮴 동위 원소] `176`: | ¹³³ᵐ²Nd | 【176】.10(10) keV | 176.10(10) keV | 176.10(10) keV | ~300 ns |  |  | (9/2-) |  |  |
  - [네오디뮴 동위 원소] `176`: | ¹³³ᵐ²Nd | 176.10(10) keV | 【176】.10(10) keV | 176.10(10) keV | ~300 ns |  |  | (9/2-) |  |  |
  - [네오디뮴 동위 원소] `176`: | ¹³³ᵐ²Nd | 176.10(10) keV | 176.10(10) keV | 【176】.10(10) keV | ~300 ns |  |  | (9/2-) |  |  |

### R-en-168

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 1.43e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `14.3 GPa` (줄 41, 뒤):   - Shear modulus: α form: 【14.3 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이터븀] `14.3`: …0.304 ¹⁶⁶Tm ¹⁶⁸Yb 0.13% 안정 ¹⁶⁹Yb 인공 32.026 d ε 0.909 ¹⁶⁹Tm ¹⁷⁰Yb 3.05% 안정 ¹⁷¹Yb 【14.3】% 안정 ¹⁷²Yb 21.9% 안정 ¹⁷³Yb 16.12% 안정 ¹⁷⁴Yb 31.8% 안정 ¹⁷⁵Yb 인공 4.185 d β⁻ 0.470 ¹⁷⁵…

### R-en-169

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 583.15, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `310 °C` (줄 69, 뒤): …um is the least volatile of the lanthanides. Like most of the lanthanides, lanthanum has a hexagonal crystal structure at room temperature (α-La). At 【310 °C】, lanthanum changes to a face-centered cubic structure (β-La), and at 865 °C, it changes to a body-centered cubic structure (γ-La).
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 573.15: [사마륨] raw `300` (줄 91, 한쪽 언어 쪽): …이 때, 사마륨과 코발트의 비율은 1:5이거나 2:17인 경우가 많다. 이러한 자석은 철보다 1만배 이상 강력한 것이다. 또, 네오디뮴 자석은 【300】~400°C 가량의 온도에서 자성을 잃는데 비해 사마륨-코발트 자석은 700°C 이상의 고온에서도 자성을 잃지 않는다. 주로 소형 전동기, 헤드…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [사마륨] `310`: … DP ¹⁴⁴Sm 3.07% 안정 ¹⁴⁶Sm 인공 1.03×10⁸y α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 1.06×10¹¹y α 2.【310】 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α 1.986 ¹⁴⁴Nd ¹⁴⁹Sm 13.82% >2×10¹⁵ y α 1.870 ¹⁴⁵Nd ¹…
  - [터븀 동위 원소] `310`: | ¹⁴⁸ᵐ²Tb | 8618.6(10) keV | 8618.6(10) keV | 8618.6(10) keV | 1.【310】(7) µs |  |  | (27+) |  |  |

### R-en-170

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 46080, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `12.8 hours` (줄 163, 뒤): Numerous nuclear isomers are also known. Among the longest-lived are ¹⁵⁰ᵐEu, with a half-life of 【12.8 hours】, and ¹⁵²ᵐ¹Eu, with a half-life of 9.3116 hours; another isomer of ¹⁵²Eu at 147.9 keV has a half-life of about 96 minutes. Most neutron-deficient euro…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 48132: [이트륨 동위 원소] raw `13.37(3) h` (줄 39, 두 언어 쪽): | ⁸⁷ᵐY | 380.82(7) keV | 380.82(7) keV | 380.82(7) keV | 【13.37(3) h】 | IT (98.43%) | ⁸⁷Y | 9/2+ |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-171

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 6500, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `6.50 g/cm³` (줄 20, 뒤):   - when liquid (at m.p.): 【6.50 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 6210: [이터븀] raw `6.21 g/cm³` (줄 19, 두 언어 쪽):   - 액체(녹는점)일 때: 【6.21 g/cm³】
  - base 6900: [이터븀] raw `6.90 g/cm³` (줄 18, 두 언어 쪽):   - 밀도 (상온 근처): 【6.90 g/cm³】
  - base 7160: [사마륨] raw `7.16 g/cm³` (줄 19, 한쪽 언어 쪽):   - 액체(녹는점)일 때: 【7.16 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-172

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 50400, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `14 hours` (줄 102, 뒤): …ted ("debulking"), and at some time thereafter, BSH was administered by a slow infusion, usually intra-arterially, but later intravenously. Twelve to 【14 hours】 later, BNCT was carried out at one or another of several different nuclear reactors using low-energy thermal neutron beams. The poor tissue-penetrati…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 48132: [이트륨 동위 원소] raw `13.37(3) h` (줄 39, 두 언어 쪽): | ⁸⁷ᵐY | 380.82(7) keV | 380.82(7) keV | 380.82(7) keV | 【13.37(3) h】 | IT (98.43%) | ⁸⁷Y | 9/2+ |  |  |
  - base 53064: [이트륨 동위 원소] raw `14.74(2) h` (줄 34, 두 언어 쪽): | ⁸⁶Y | 39 | 47 | 85.914886(15) | 【14.74(2) h】 | β⁺ | ⁸⁶Sr | 4- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [이터븀] `14`: …0.304 ¹⁶⁶Tm ¹⁶⁸Yb 0.13% 안정 ¹⁶⁹Yb 인공 32.026 d ε 0.909 ¹⁶⁹Tm ¹⁷⁰Yb 3.05% 안정 ¹⁷¹Yb 【14】.3% 안정 ¹⁷²Yb 21.9% 안정 ¹⁷³Yb 16.12% 안정 ¹⁷⁴Yb 31.8% 안정 ¹⁷⁵Yb 인공 4.185 d β⁻ 0.470 ¹…
  - [이터븀] `14`: 주기율표상으로 란타넘족 원소 중 【14】번째이며 끝에서 두 번째에 위치해 있다. 이는 이터븀이 다른 란타넘족 원소들과 다르게 비교적 안정한 +2의 산화수를 가질 수 있는 이유이다. 하…
  - [이트륨 동위 원소] `14`: | ⁷⁹Y | 39 | 40 | 78.93735(48) | 【14】.8(6) s | β⁺ (>99.9%) | ⁷⁹Sr | (5/2+)# |  |  |
  - [이트륨 동위 원소] `14`: | ⁷⁹Y | 39 | 40 | 78.93735(48) | 【14】.8(6) s | β⁺, p (<0.1%) | ⁷⁸Rb | (5/2+)# |  |  |
  - [이트륨 동위 원소] `14`: | ⁸²ᵐ¹Y | 402.63(【14】) keV | 402.63(14) keV | 402.63(14) keV | 268(25) ns |  |  | 4- |  |  |

### R-en-173

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.4192e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `28-day` (줄 259, 뒤): …low systemic availability following oral administration of europium(III) chloride, although sufficiently high doses can produce adverse effects. In a 【28-day】 study, rats were given europium(III) chloride hexahydrate at doses of up to 1000 mg/kg of body weight per day. At the highest dose, gastric irritatio…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 5개:
  - [디스프로슘] `28`: …y 0.10% 안정 ¹⁶⁰Dy 2.34% 안정 ¹⁶¹Dy 18.91% 안정 ¹⁶²Dy 25.51% 안정 ¹⁶³Dy 24.90% 안정 ¹⁶⁴Dy 【28】.18% 안정
  - [어븀] `28`:   - 몰열용량: 【28】.12 J/(mol·K)
  - [어븀] `28`:   - 전단 탄성 계수: 【28】.3 GPa
  - [어븀] `28`:   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁶⁰Er 인공 【28】.58 h ε 0.330 ¹⁶⁰Ho ¹⁶²Er 0.14% 안정 ¹⁶⁴Er 1.61% 안정 ¹⁶⁵Er 인공 10.36 h ε 0.376 ¹⁶⁵Ho…
  - [이트륨] `28`: …0.48 0.38D - ⁸⁸Y 합성 106.6d ε - ⁸⁸Sr γ 1.83 0.89 - ⁸⁹Y 100% 안정 ⁹⁰Y 합성 2.67d β- 2.【28】 ⁹⁰Zr γ 2.18 - ⁹¹Y 합성 58.5d β- 1.54 ⁹¹Zr γ 1.20 -

### R-en-174

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 5940, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `5.94 g/cm³` (줄 20, 뒤):   - when liquid (at m.p.): 【5.94 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 6210: [이터븀] raw `6.21 g/cm³` (줄 19, 두 언어 쪽):   - 액체(녹는점)일 때: 【6.21 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-175

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 3.25043e+18, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `1.03×10¹¹ y` (줄 53, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹³⁷La synth 6×10⁴ y ε ¹³⁷Ba ¹³⁸La 0.0889999999% 【1.03×10¹¹ y】 β⁺ ¹³⁸Ba β⁻ ¹³⁸Ce ¹³⁹La 99.911% stable ¹⁴⁰La synth 40.289 h β⁻ ¹⁴⁰Ce
  - [Lanthanum] raw `1.03×10¹¹ years` (줄 79, 뒤): …ovae). It is the only stable isotope of lanthanum. The very rare isotope ¹³⁸ La is one of the few primordial odd–odd nuclei, with a long half-life of 【1.03×10¹¹ years】. It is one of the proton-rich p-nuclei which cannot be produced in the s- or r-processes. ¹³⁸ La, along with the even rarer ¹⁸⁰ᵐ Ta, is produced in t…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 3.34511e+18: [사마륨] raw `1.06×10¹¹y` (줄 48, 한쪽 언어 쪽): …반감기 DM DE (MeV) DP ¹⁴⁴Sm 3.07% 안정 ¹⁴⁶Sm 인공 1.03×10⁸y α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 【1.06×10¹¹y】 α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α 1.986 ¹⁴⁴Nd ¹⁴⁹Sm 13.82% >2×10¹⁵ y α 1.870…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [사마륨] `1.03`:   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁴⁴Sm 3.07% 안정 ¹⁴⁶Sm 인공 【1.03】×10⁸y α 2.529 ¹⁴²Nd ¹⁴⁷Sm 14.99% 1.06×10¹¹y α 2.310 ¹⁴³Nd ¹⁴⁸Sm 11.24% 7×10¹⁵y α…

### R-en-176

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 8.3e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `8.3 GPa` (줄 42, 뒤):   - Bulk modulus: 【8.3 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `8.3`: | ¹⁰³Y | 39 | 64 | 102.93673(32)# | 224(19) ms | β⁻, n (【8.3】%) | ¹⁰²Zr | 5/2+# |  |  |

### R-en-177

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 7.9e+09, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `7.9 GPa` (줄 41, 뒤):   - Shear modulus: 【7.9 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [터븀 동위 원소] `7.9`: | ¹⁴¹ᵐTb | 0(200)# keV | 0(200)# keV | 0(200)# keV | 【7.9】(6) s | β⁺ | ¹⁴¹Gd | 11/2-# |  |  |

### R-en-178

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 비저항, base 6.15e-07, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `615 nΩ⋅m` (줄 37, 뒤):   - Electrical resistivity: α, poly: 【615 nΩ⋅m】 (at r.t.)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 3개(가까운 차례):
  - base 5.96e-07: [이트륨] raw `596 n Ω·m` (줄 33, 한쪽 언어 쪽):   - 전기 저항도: (실온) (α, poly) 【596 n Ω·m】
  - base 5.82e-07: [루테튬] raw `582 n Ω·m` (줄 32, 두 언어 쪽):   - 전기 저항도: (실온) (poly) 【582 n Ω·m】
  - base 6.76e-07: [툴륨] raw `676 n Ω·m` (줄 33, 두 언어 쪽):   - 전기 저항도: (실온) (poly) 【676 n Ω·m】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-179

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 흡수선량, base 15.4, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `15.4` (줄 158, 뒤): …this study. All were treated with 2 fields, and the average whole-brain dose was 3.2–6.1 Gy (weighted), and the minimum dose to the tumor ranged from 【15.4】 to 54.3 Gy (w). There has been some disagreement among the Swedish investigators regarding the evaluation of the results. Based on incomplete surviva…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-180

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 7.45e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `745 MPa` (줄 45, 뒤):   - Vickers hardness: 250–【745 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 8.14e+08: [어븀] raw `814 MPa` (줄 40, 한쪽 언어 쪽):   - 브리넬 굳기: 【814 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-181

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 6773, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `6.773 g/cm³` (줄 19, 뒤):   - Density (at 20° C): 【6.773 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 6900: [이터븀] raw `6.90 g/cm³` (줄 18, 두 언어 쪽):   - 밀도 (상온 근처): 【6.90 g/cm³】
  - base 7160: [사마륨] raw `7.16 g/cm³` (줄 19, 한쪽 언어 쪽):   - 액체(녹는점)일 때: 【7.16 g/cm³】
  - base 6210: [이터븀] raw `6.21 g/cm³` (줄 19, 두 언어 쪽):   - 액체(녹는점)일 때: 【6.21 g/cm³】
  - base 7520: [사마륨] raw `7.52 g/cm³` (줄 18, 한쪽 언어 쪽):   - 밀도 (상온 근처): 【7.52 g/cm³】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-182

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 에너지, base 1.27213e-12, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `7.94 MeV` (줄 75, 뒤): … rays and internal conversion and Auger electrons are products of the ¹⁵⁷Gd(n,γ)¹⁵⁸Gd capture reaction (¹⁵⁷Gd + nth (0.025eV) → [¹⁵⁸Gd] → ¹⁵⁸Gd + γ + 【7.94 MeV】). Though the gamma rays have longer pathlengths, orders of magnitude greater depths of penetration compared with alpha particles, the other radiation…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 1.38085e-12: [터븀 동위 원소] raw `8618.6(10) keV` (줄 45, 한쪽 언어 쪽): | ¹⁴⁸ᵐ²Tb | 【8618.6(10) keV】 | 8618.6(10) keV | 8618.6(10) keV | 1.310(7) µs |  |  | (27+) |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-183

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 6.4e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `640 MPa` (줄 46, 뒤):   - Brinell hardness: 250–【640 MPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 5.89e+08: [어븀] raw `589 MPa` (줄 39, 한쪽 언어 쪽):   - 비커스 굳기: 【589 MPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-184

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 68832, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `19.12 h` (줄 52, 뒤):   - Main isotopes Decay Isotope abun­dance half-life (t1/2) mode pro­duct ¹⁴¹Pr 100% stable ¹⁴²Pr synth 【19.12 h】 β⁻ ¹⁴²Nd ε ¹⁴²Ce ¹⁴³Pr synth 13.57 d β⁻ ¹⁴³Nd
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 63000: [터븀 동위 원소] raw `17.5(1) h` (줄 58, 한쪽 언어 쪽): | ¹⁵²Tb | 65 | 87 | 151.92407(4) | 【17.5(1) h】 | β⁺ | ¹⁵²Gd | 2- |  |  |
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-185

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 5130, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `5.13 g/cm³` (줄 20, 뒤):   - when liquid (at m.p.): 【5.13 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-186

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 밀도, base 5240, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `5.24 g/cm³` (줄 63, 뒤): Europium is a soft, silvery-white, ductile rare-earth metal. Its hardness is similar to that of lead. At room temperature it has a density of about 【5.24 g/cm³】 and a melting point of 822 °C (1,095 K).
  - [Europium] raw `5.246 g/cm³` (줄 19, 뒤):   - Density (at 20° C): 【5.246 g/cm³】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-187

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 압력, base 2.79e+10, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `27.9 GPa` (줄 42, 뒤):   - Bulk modulus: α form: 【27.9 GPa】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 4개(가까운 차례):
  - base 2.83e+10: [어븀] raw `28.3 GPa` (줄 35, 한쪽 언어 쪽):   - 전단 탄성 계수: 【28.3 GPa】
  - base 2.72e+10: [루테튬] raw `27.2 GPa` (줄 34, 두 언어 쪽):   - 전단 탄성 계수: 【27.2 GPa】
  - base 2.56e+10: [이트륨] raw `25.6 GPa` (줄 36, 한쪽 언어 쪽):   - 전단 탄성 계수: 【25.6 GPa】
  - base 3.05e+10: [툴륨] raw `30.5 GPa` (줄 35, 두 언어 쪽):   - 전단 탄성 계수: 【30.5 GPa】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-188

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 비열, base 182.022, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `182.022 J/(kg·K)` (줄 24, 뒤):   - Specific heat capacity: 【182.022 J/(kg·K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-189

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 열팽창, base 4.5e-06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `4.5×10⁻⁶/K` (줄 35, 뒤):   - Thermal expansion: 【4.5×10⁻⁶/K】 (at 20 °C)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-190

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 400000, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `400 kJ/mol` (줄 22, 뒤):   - Heat of vaporization: 【400 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 414000: [루테튬] raw `414 kJ/mol` (줄 21, 두 언어 쪽):   - 기화열: 【414 kJ/mol】
  - base 365000: [이트륨] raw `365 kJ/mol` (줄 21, 한쪽 언어 쪽):   - 기화열: 【365 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 2개:
  - [사마륨] `400`: … 사마륨과 코발트의 비율은 1:5이거나 2:17인 경우가 많다. 이러한 자석은 철보다 1만배 이상 강력한 것이다. 또, 네오디뮴 자석은 300~【400】°C 가량의 온도에서 자성을 잃는데 비해 사마륨-코발트 자석은 700°C 이상의 고온에서도 자성을 잃지 않는다. 주로 소형 전동기, 헤드셋, 기…
  - [이트륨] `400`: … 안에서 750 °C 로 가열될 때 1 μm의 두께를 가질 수 있다. 잘게 나눠졌을 때, 이트륨은 공기 중에서 불안정하다. 작은 이트륨 조각은 【400】 °C 이상의 온도에서 불이 붙을 수 있다. 질화 이트륨(YN)은 이트륨이 질소(N) 기체 안에서 1000 °C 로 가열될 때 생성된다.

### R-en-191

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 몰 에너지, base 1.8503e+06, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `1850.3 kJ/mol` (줄 29, 뒤):   - Ionization energies: 1st: 538.1 kJ/mol, 2nd: 1067 kJ/mol, 3rd: 【1850.3 kJ/mol】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 2개(가까운 차례):
  - base 1.98e+06: [이트륨] raw `1980 kJ/mol` (줄 27, 한쪽 언어 쪽):   - 이온화 에너지: 1차: 600 kJ/mol, 2차: 1180 kJ/mol, 3차: 【1980 kJ/mol】
  - base 2.0223e+06: [루테튬] raw `2022.3 kJ/mol` (줄 27, 두 언어 쪽):   - 이온화 에너지: 1차: 523.5 kJ/mol, 2차: 1340 kJ/mol, 3차: 【2022.3 kJ/mol】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-192

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 흡수선량, base 3.2, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `3.2` (줄 158, 뒤): …f the BPA was well-tolerated by the 30 patients who were enrolled in this study. All were treated with 2 fields, and the average whole-brain dose was 【3.2】–6.1 Gy (weighted), and the minimum dose to the tumor ranged from 15.4 to 54.3 Gy (w). There has been some disagreement among the Swedish investigator…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-193

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 7.78405e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `29.6 months` (줄 136, 뒤): The median OS after BNCT was 【29.6 months】 and 98.4 months after diagnosis. Better responses were seen in patients with lower-grade tumors. In 35 of 36 patients, there was tumor shrinkage, and…
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-194

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 질량, base 0.0704, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `70.4 g` (줄 223, 뒤): …simultaneously, helping to separate europium from less volatile contaminants. In 1958, Frank Spedding, J. J. Hanak and A. H. Daane reported preparing 【70.4 g】 of high-purity europium by heating europium oxide with lanthanum in vacuum at about 1200 °C.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 1개:
  - [이트륨 동위 원소] `70.4`: | ⁸¹Y | 39 | 42 | 80.92913(7) | 【70.4】(10) s | β⁺ | ⁸¹Sr | (5/2+) |  |  |

### R-en-195

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 2.71143e+08, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Europium] raw `8.592 y` (줄 51, 뒤): …de pro­duct ¹⁵⁰Eu synth 36.9 y β⁺ ¹⁵⁰Sm ¹⁵¹Eu 47.7999999999% 4.6×10¹⁸ y α ¹⁴⁷Pm ¹⁵²Eu synth 13.517 y β⁺ ¹⁵²Sm β⁻ ¹⁵²Gd ¹⁵³Eu 52.2% stable ¹⁵⁴Eu synth 【8.592 y】 β⁻ ¹⁵⁴Gd ε ¹⁵⁴Sm ¹⁵⁵Eu synth 4.742 y β⁻ ¹⁵⁵Gd
  - [Europium] raw `8.592 years` (줄 161, 뒤): …e longest-lived artificial isotope is ¹⁵⁰Eu, with a half-life of 36.9 years. Other comparatively long-lived isotopes are ¹⁵²Eu (13.517 years), ¹⁵⁴Eu (【8.592 years】) and ¹⁵⁵Eu (4.742 years); all other known ground-state europium radioisotopes have half-lives shorter than 100 days.
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 0개(가까운 차례):
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-196

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 열전도율, base 12.5, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Praseodymium] raw `12.5 W/(m⋅K)` (줄 36, 뒤):   - Thermal conductivity: 【12.5 W/(m⋅K)】
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 13.3: [사마륨] raw `13.3 W/(m·K)` (줄 32, 한쪽 언어 쪽):   - 열전도율: 【13.3 W/(m·K)】
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-197

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 온도, base 298, 표 안 아니오, 시험 대상 밖 아니오
- 언급:
  - [Lanthanum] raw `298 K` (줄 39, 뒤):   - Molar magnetic susceptibility: +118.0×10⁻⁶ cm³/mol (【298 K】)
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 293.15: [툴륨] raw `20 °C` (줄 30, 두 언어 쪽):   - 격자 상수: a = 353.77 pm c = 555.39 pm (【20 °C】에서)
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:

### R-en-198

- 분야 rare_earth, 언어 en, 쪽 한쪽 언어 쪽, dim 시간, base 4.07611e+07, 표 안 아니오, 시험 대상 밖 예
- 언급:
  - [Neutron capture therapy of cancer] raw `15.5 months` (줄 158, 뒤): … tumor progression was 5.8 months. However, more careful examination of the complete survival data revealed that the MeST was 17.7 months compared to 【15.5 months】 that has been reported for patients who received standard therapy of surgery, followed by radiotherapy (RT) and the drug temozolomide (TMZ). Furtherm…
  - [Neutron capture therapy of cancer] raw `15.6 months` (줄 122, 뒤): The mean survival time (MST) of 10 patients with recurrent high-grade gliomas in the first of their trials was 【15.6 months】, with one long-term survivor (>5 years).
- (가) 반대 언어의 같은 dim이고 기준 값이 10% 안인 양 1개(가까운 차례):
  - base 4.32339e+07: [루테튬] raw `1.37 y` (줄 46, 두 언어 쪽):   - 동위체 존재비 반감기 DM DE (MeV) DP ¹⁷³Lu 인공 【1.37 y】 ε 0.671 ¹⁷³Yb ¹⁷⁴Lu 인공 3.31 y ε 1.374 ¹⁷⁴Yb ¹⁷⁵Lu 97.41% 안정 ¹⁷⁶Lu 2.59% 3.78×10…
- (나) 반대 언어 문서에서 언급의 숫자 글자가 나오는 자리 0개:
