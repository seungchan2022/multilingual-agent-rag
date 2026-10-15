# chat3 묶음 1(한국어 질문·한국어 문서) 사용자 판정

후보 파일: `research_notes/stage3_dev/chat3/batch1_ko-ko.yaml`(고친 뒤 검사를 통과한 것). 순서표(`data/questions/final_set_guide.md`)의 "대조할 것"을 따라 후보마다 확인하고 여기에 적는다.

Claude는 사용자의 판정이 끝난 뒤 같은 후보를 원문과 다시 대조해, 이 기록과 견줘 놓친 것을 센다(`decisions/common.md` 2026-10-15). 그래서 판정을 마칠 때까지 Claude에게 후보 내용의 맞고 틀림을 묻지 않는다. 절차를 묻는 것은 된다.

적는 법: 확인한 칸은 `[ ]`를 `[x]`로 바꾼다. 확인하지 않은 칸은 그대로 둔다(비워 둔 것도 기록이다). 판정은 채택·수정·폐기 가운데 하나만 남긴다. 근거 구절이 원문에 글자 그대로 있는지, 개수·형식, `opposite_check`가 원문과 맞는지는 후보 검사가 이미 봤다.

## c-001

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-002

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-003

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-004

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-005

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-006

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-007

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-008

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-009

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-010

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-011

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:

## c-012

- [ ] 1. 근거 구절만 읽고 정답이 나온다 (조건·단위 포함) — 볼 곳: 후보 YAML의 `question`, `answer`, `passage`
- [ ] 2. 정답이 하나로 정해진다 — 볼 곳: 후보 YAML의 `passage`
- [ ] 3. 같은 문서 안에 다른 값이 없다 — 볼 곳: 근거 `doc_id`의 원문(`Cmd+P`로 열고 `Cmd+F`)
- [ ] 4. 같은 언어의 다른 문서에 다른 값이 없다 — 볼 곳: 폴더 찾기(`Cmd+Shift+F`, 포함할 파일 `data/corpus/markdown/*-ko-*`)
- [ ] 5. 영어 문서: 걸린 곳을 번역기로 읽었다 — 볼 곳: 후보 YAML의 `opposite_check` → `hits` → `excerpt`
- [ ] 6. 영어 문서: 찾을 말에 그 사실의 이름·숫자가 들어 있다 (빠졌으면 번역기로 옮겨 폴더 찾기를 더 했다) — 볼 곳: 후보 YAML의 `opposite_check` → `term`, 폴더 찾기(포함할 파일 `data/corpus/markdown/*-en-*`)
- [ ] 7. 영어 문서: 두 언어 도시면 같은 도시의 영어 문서를 번역해 읽었다 (한국어 도시면 해당 없음) — 볼 곳: `wiki-en-<도시>.md`의 해당 절을 번역기로
- [ ] 8. `required_facts`가 빠짐없고 군더더기 없다 — 볼 곳: 후보 YAML의 `required_facts` → `fact`, `answer`
- [ ] 9. 유형이 맞다 — 볼 곳: 후보 YAML의 `type`, `question`, `passage`
- 판정: 채택 / 수정 / 폐기
- 이유:
- 찾아본 말과 걸린 곳:
