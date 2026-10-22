# 본문 숫자에 대상·양 붙이기 지시서

이 지시서는 서브에이전트(Sonnet 5.5, effort high)가 읽는다. 맡은 문서의 본문 숫자마다 "무엇의 어떤 값인지"를 적는다. 결과는 같은 대상·같은 양의 값이 문서끼리 다르게 적힌 곳(부딪히는 값)을 찾는 데 쓴다. 결정은 `decisions/stage2.md` 2026-10-22 "희토류 원소의 사실 목록은 부딪히는 값을 찾는 데 쓴다", "희토류 원소 값 목록의 \"다른 값\" 기준", "희토류 원소 값 목록에 넣는 값" 줄에 있다.

## 하는 일

1. 맡은 문서마다 숫자 목록 `research_notes/stage2_values_rare_earth/body/items/<doc_id>.json`과 원문 `data/corpus/markdown/<doc_id>.md`를 읽는다. 숫자 목록의 항목 하나가 숫자 하나다. `id`는 `<doc_id>:<줄>:<시작>-<끝>`이고 줄은 1부터, 시작·끝은 그 줄 안의 글자 위치다. `context`는 앞뒤 글자 일부일 뿐이니 판단은 원문 줄 전체를 읽고 한다.
2. 항목마다 결과 한 줄을 `research_notes/stage2_values_rare_earth/body/<doc_id>.json`(JSON 목록)에 쓴다. 항목을 빠뜨리거나 두 번 쓰지 않는다. 다른 파일은 고치지 않는다. 커밋하지 않는다. 인터넷을 쓰지 않는다.
3. 다 쓴 뒤 아래 "스스로 확인"을 돌려 통과시킨다.

## 값인 숫자와 값이 아닌 숫자

- **값**: 무엇의 성질·양·수·때를 말하는 숫자. 질문의 정답이 될 수 있는 것. 예: 녹는점, 반감기, 지각 존재량, 생산량, 가격, 발견한 해, 환자 수, 생존 기간, 선량, 비율, 순서(13번째 원소).
- **값 아님**: 이름·기호·식의 일부(화학식, 반응식의 계수, 전자 배치 `4f`, 모델 이름 `RE-278`), 참고 문헌과 인용 안의 숫자(해, 권, 쪽, ISBN, DOI), 절·목록 번호. 까닭을 짧은 한국어로 적는다.
- 판단이 서지 않으면 가장 그럴듯한 쪽으로 적고 `"uncertain": true`와 까닭을 붙인다. 지어내지 않는다.

## 결과 한 줄의 꼴

값일 때:
```json
{"id": "<항목 id>", "value": true, "object": "Tm", "quantity": "melting_point", "condition": "", "note": ["(at 20 °C)"], "raw": "1545 °C"}
```
값이 아닐 때:
```json
{"id": "<항목 id>", "value": false, "reason": "화학식의 일부"}
```
다른 항목과 함께 한 값일 때(범위의 끝, 한 자리에 함께 적은 단위 환산 `1545 °C (2813 °F)`의 둘째 숫자 등):
```json
{"id": "<항목 id>", "value": true, "part_of": "<그 값의 첫 항목 id>"}
```

### 칸을 채우는 법

- `object`(대상 열쇠)
  - 원소는 원소 기호: `Tm`, `Dy`, `Yb`, `Lu`, `Er`, `Sm`, `Y`, `La`, `Eu`, `Pr`, `Gd`, `Ho`, `Nd`, `Tb`, `Ce`, `B` 등. 한국어 문서도 같다.
  - 동위 원소는 `원소 기호-질량수`: `Eu-151`, `Lu-177`, `Y-90`. 핵 이성질체는 뒤에 `m`(`Y-87m`).
  - 화합물은 문서에 적힌 화학식에서 빈칸을 뺀 꼴: `Eu2O3`, `SmCo5`, `Sm2Co17`, `Y2O3`.
  - 그 밖에는 짧은 영어 소문자 이름. 같은 문서의 표에 같은 대상이 줄 이름으로 있으면 그 글자를 그대로 쓴다(예: 중성자 포획 치료 문서의 시설 `BMRR, US`).
- `quantity`(양 열쇠)
  - `research_notes/stage2_values_rare_earth/vocab.json`의 `infobox_label`·`table_column`에 나오는 양 열쇠와 같은 성질이면 반드시 그 열쇠를 쓴다. 예: 녹는점은 `melting_point`, 반감기는 `half_life`, 밀도는 `density`, 원자 반지름은 `atomic_radius`, 붕괴 방식은 `decay_mode`, 자연 존재비는 `natural_abundance`.
  - 원소를 발견한 해와 처음 얻은(분리한) 해는 정보 상자와 같은 `discovery`, `first_isolation`을 쓴다. 금속 시료를 처음 얻은 해도 `first_isolation`이다.
  - 맞는 열쇠가 없으면 성질을 알 수 있는 짧은 영어 snake_case 열쇠를 새로 만든다(예: `crustal_abundance`, `annual_production`, `price`, `number_of_isotopes`, `neutron_cross_section`, `patients`, `median_survival`). 같은 성질에는 같은 열쇠를 쓴다. 새로 만든 열쇠는 보고에 뜻과 함께 적는다.
- `condition`(조건 열쇠): 한 줄에 여러 값을 나눠 적은 것 가운데 하나일 때만 쓴다. `vocab.json`의 `structural_condition` 값(`1st`, `2nd`, `3rd`, `empirical`, `calculated`, `a`, `c` 등)에서 고른다. 그 밖에는 `""`.
- `note`(덧붙인 말): 값에 붙은 조건이나 상황을 원문 글자 그대로(예: `"at room temperature"`, `"in seawater"`, `"2019년"`, `"for recurrent tumours"`). 없으면 `[]`.
- `raw`: 그 값을 원문에 적힌 그대로. 단위와 어림 말(`about`, `약`, `~`, `over`, `less than`)을 포함한다. 그 줄 안에 글자 그대로 있어야 하고 항목의 숫자를 포함해야 한다.
- `part_of`(2026-10-22 보탬): 그 숫자가 다른 숫자와 함께 값 하나를 이룰 때만 쓴다. 범위의 끝(`470–650 MPa`의 650), 한 자리에 함께 적은 단위 환산(`795 °C (1,463 °F)`의 1,463), 한 값 표현 안의 숫자(`two parts in 10¹⁸`의 18)가 그렇다. 이때 주 값의 `raw`는 그 숫자까지 덮도록 넓힌다(예: `795 °C (1,463 °F)`).
- 다른 값의 조건은 `part_of`가 아니다(2026-10-22 보탬). 가격·생산량·매장량의 기준 해, 순도, 압력 조건이 그렇다. 그 숫자는 `{"value": false, "reason": "다른 값의 조건"}`으로 둔다. 그리고 조건 글자를 주 값의 `note`에 원문 그대로 넣는다(예: 가격 `US$20 per gram`의 note에 `"in 1996"`).

## 스스로 확인

아래를 돌려 `문제 없음`이 나와야 끝난 것이다(`<doc_id>`를 바꿔 문서마다).

```
.venv/bin/python -I - <<'PY'
import json, pathlib
doc = "<doc_id>"
base = pathlib.Path("research_notes/stage2_values_rare_earth/body")
items = json.loads((base / "items" / f"{doc}.json").read_text(encoding="utf-8"))
out = json.loads((base / f"{doc}.json").read_text(encoding="utf-8"))
lines = pathlib.Path(f"data/corpus/markdown/{doc}.md").read_text(encoding="utf-8").split("\n")
ids = [x["id"] for x in items]; got = [x["id"] for x in out]; byid = {x["id"]: x for x in items}
bad = []
if sorted(ids) != sorted(got): bad.append(("빠지거나 겹친 id", sorted(set(ids) ^ set(got)), len(got) - len(set(got))))
for x in out:
    it = byid.get(x["id"])
    if it is None: continue
    if x.get("value") and "part_of" not in x:
        for k in ("object", "quantity", "condition", "note", "raw"):
            if k not in x: bad.append((x["id"], "칸 없음", k))
        line = lines[it["line"] - 1]
        if x.get("raw") and (x["raw"] not in line or it["raw"] not in x["raw"]): bad.append((x["id"], "raw가 줄에 없거나 숫자를 담지 않음", x.get("raw")))
    if x.get("value") and "part_of" in x:
        main = next((y for y in out if y["id"] == x["part_of"]), None)
        if main is None or "part_of" in main or not main.get("value"): bad.append((x["id"], "part_of가 값인 주 항목을 가리키지 않음"))
        else:
            line = lines[it["line"] - 1]
            a, b = (int(v) for v in x["id"].rsplit(":", 1)[1].split("-"))
            ma, mb = (int(v) for v in main["id"].rsplit(":", 1)[1].split("-"))
            s, ok = line.find(main["raw"]), False
            while s != -1:
                ok = ok or (s <= ma and mb <= s + len(main["raw"]) and s <= a and b <= s + len(main["raw"]))
                s = line.find(main["raw"], s + 1)
            if not ok or main["id"].split(":")[1] != x["id"].split(":")[1]: bad.append((x["id"], "part_of 숫자가 주 값의 raw 밖에 있음", main["raw"]))
    if x.get("value") is False and not x.get("reason"): bad.append((x["id"], "까닭 없음"))
print(bad or "문제 없음")
PY
```

## 보고(한국어, 짧게)

문서마다 값·값 아님·`uncertain` 수, 새로 만든 양 열쇠와 그 뜻, 숫자 목록에 없는데 값으로 보이는 숫자를 본 것(있으면 줄과 글자), 스스로 확인의 마지막 줄.
