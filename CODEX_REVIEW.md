# Codex 검토 기록 (2단계)

2차 검토 때 Codex가 1차 지적을 하나씩 대조하는 데 쓴다. 단계를 닫을 때 커밋한 뒤 지운다.

- 1차 검토: 2026-10-14 20:45:53~21:05:37, `gpt-6.1-sol`, `max` (세션 기록 `~/.codex/sessions/2026/10/14/rollout-2026-10-14T20-45-54-…jsonl`에서 확인)
- 1차 검토에 넘긴 "이번 검토" 부분은 아래 "1차 요청"에 그대로 옮겼다. 어느 `decisions/` 파일을 열라고는 적지 않았다(이슈 ⑦을 보려는 것)
- 2차 검토: 2026-10-14 22:27:49~22:43:18, `gpt-6.1-sol`, `max`. 결과 원문은 아래 "2차 지적 원문"

## 1차 지적의 처리

(지적마다 판정과 처리 내용을 사용자가 정하는 대로 적는다)

| 지적 | 판정 | 처리 |
|---|---|---|
| 1 머리글이 없는 표에서 첫 줄의 내용이 빈 열 지우기로 사라진다 | 맞음. 반영 | `build.py`의 `table_items`에서 첫 줄이 전부 `th`가 아니면 첫 줄도 내용 줄로 넣어 빈 열을 가린다. `check_build.py` 28번을 더하고 마크다운을 다시 만들었다(청주·춘천 한국어 두 파일만 바뀜). 원본 표의 칸 글자가 마크다운에 남았는지 표 전체에서 견줬다(`research_notes/stage2_markdown_rules/cell_loss_check.py`): 틀이 아닌 표 99개에서 사라진 칸은 빈 열의 머리글 10칸뿐, 틀로 풀린 표 24개는 0. `decisions/stage2.md` 2026-10-14 "머리글 줄을 가리는 기준" 줄 |
| 2 검색 낱말이 남지 않은 사실 9개가 대조 없이 통과한다 | 맞음. 반영 | `check.py`에서 찾을 낱말이 없는 사실은 저절로 통과하지 않게 했다. 9개는 AI가 반대 언어 마크다운 14개에서 그 도시 이름이 나오는 자리를 모두 읽어 "같은 사실 아님"으로 `cleared.json`에 적었다. `decisions/judgments.md` 2026-10-14 다시 센 줄 ⓐ |
| 3 질문에 쓰지 않기로 한 값 5개가 통과 수와 연결 재료 수에 들어간다 | 맞음. Codex가 든 5개보다 넓게 반영 | 정한 규칙 전부와, 통과한 사실 222개마다 같은 문서 안의 다른 값을 찾은 결과(문서 16개를 서브에이전트에 하나씩, `within_doc/`)를 대어 29개를 `excluded.json`에 적고 세기에서 뺐다. 합이 맞지 않는 표에서 한 번만 나오는 줄의 값은 쓴다(사용자). 다시 센 수: 한국어 93(표 34, 연결 후보 87), 영어 100(표 39, 연결 후보 64). 춘천 두 인구 표도 견줬다. `DECISIONS.md` 미정 목록 "질문을 만들 때 지킬 것" ⑦⑧ |
| 4 커밋 직전 검사가 stage된 파이썬·라이브러리 버전이 아니라 작업 폴더의 것으로 돈다 | 맞음. 반영 | 검사가 도는 조건일 때 `.python-version`, `uv.lock`, `pyproject.toml`의 stage본과 작업 폴더본이 다르면 막는다. 이미 올라간 커밋은 고칠 것이 없음을 확인했다. `decisions/stage2.md` 2026-10-14 커밋 직전 검사 줄 |
| 5 마지막 마크다운의 사용자 확인 기록이 없는데 ③을 채웠다고 했다 | 맞음(기록이 빠짐). 반영 | 사용자가 정보 상자를 고친 뒤 확인했다고 말해 판단 기록에 적었다. 지적 1과 그 뒤의 고침으로 바뀐 표 세 곳을 사용자가 위키백과 화면과 견줬다(판단 기록 2026-10-14) |
| 6 표 조사의 수 두 곳이 저장된 목록과 다르다 | 맞음. 반영 | 지적 1을 고친 뒤 표 모양을 다시 셌고 모양별 수는 그대로였다. `classify.py`가 원문 표를 위키백과 HTML 123과 통계 표 CSV 2로 나눠 적게 했다. 판단 기록 2026-10-14 ⑤ 줄의 19·3·1을 18·4·1로 고치고 고쳤다는 것을 그 자리에 남겼다 |

1차 지적 밖에서 고친 것(2차 검토의 "새로 생긴 문제"를 볼 때 함께 본다):

- 지적 5로 사용자가 바뀐 표를 열어 보다가 춘천 고등학교 표의 빈 첫 줄을 짚었다. 원본 줄의 칸이 전부 아래로 걸친 칸뿐이면 그 줄을 표에서 빼는 규칙을 더했다(`build.py` `table_items`, `check_build.py` 29번, `decisions/stage2.md` 2026-10-14 줄). 표 모양 분류에서 이 표를 "머리글 칸이 일부만 찬 표"에서 "머리글 줄이 없는 표"로 옮겼다
- 양이 많은 확인 작업은 나눠서 맡기고 빠진 항목을 세기로 했다(`decisions/common.md` 2026-10-14 줄)

## 2차 지적의 처리

2차에서는 심각한 지적만 반영하는 것이 규칙이나, 셋 다 "보통"이고 지금 고칠 수 있어 사용자가 지금 반영하기로 정했다. 2차 뒤에 고친 것은 다시 검토받지 않는다(닫는 절차 ④로 반례를 다시 따라간다).

| 지적 | 판정 | 처리 |
|---|---|---|
| 1 강릉 en 03: 서로 다른 사건을 충돌로 판정 | 절반 맞음. 반영 | 문서는 시 설치 1955년과 명주 지역 합병 1995년을 정보 상자에 따로 적고, 본문은 "1995년 합병하며 시가 설치되었다"고 적어 "시가 된 해"는 부딪히고 "합병한 해"는 부딪히지 않는다. 사실 문장을 "강릉과 명주 지역은 1995년에 합쳐졌다"로 고치고(종류 city_status_year → other) `excluded.json`에서 뺐다. "시가 된 해"는 알려진 부딪히는 값에 넣었다 |
| 2 천안 ko 02: 결측칸이 있는 부분합으로 충돌을 확정 | 지적한 근거는 맞음. 제외는 유지 | 서북구 아래 동들의 합은 불당1·2동이 `-`라 근거가 되지 못한다. 대신 빈칸 없이 적힌 서북구 400,566명 + 동남구 264,312명 = 664,878명이 총계 683,453명과 맞지 않는 것을 제외 근거로 바꿔 적었다 |
| 3 반올림 예외가 지시서에 빠짐 | 맞음. Codex의 제안과 반대로 반영 | 반올림·버림·"약"으로 적은 값도 다른 값으로 보아 질문에 쓰지 않기로 했다(사용자가 어드바이저 점검을 거쳐 정함). "다른 값 없음"이던 185개를 문서별로 다시 나눠 다른 모양으로 적힌 곳을 찾게 했고(`within_doc/form/`), 14개가 걸려 AI가 3개를 뺐다(전주 면적, 경주 연 강수량, 세종 2023년 인구). 나머지 10개는 값이 같거나 단위 병기라 빼지 않았고, 강릉 산림 사실은 원문에 없는 면적이 붙어 있어 문장을 고쳤다(`form/review.json`). 지시서 5·9번과 안내서에 규칙을 넣었다. 다시 센 수: 한국어 90(표 33, 연결 후보 70), 영어 101(표 39, 연결 후보 64) |

## 2차 요청

- 단계: 2단계 (문서). 2차 검토다. `CODEX_REVIEW.md`에 1차 요청, 1차 지적 원문, 지적마다의 처리, 1차 지적 밖에서 고친 것이 있다.
- 1차 지적 6개를 하나씩 해소됨 / 절반만 됨 / 안 됨으로 가르고, 고치면서 새로 생긴 문제만 추가로 써라.
- 1차 검토 뒤의 변경은 커밋 `0d56b77` 다음부터 `HEAD`까지다(`git log --oneline 0d56b77..HEAD`, `git diff 0d56b77 HEAD`).
- 1차 뒤에 새로 생기거나 크게 바뀐 산출물:
  - 변환 코드와 검사: `src/corpus/build.py`의 `table_items`(머리글 줄을 가리는 기준, 칸이 모두 아래로 걸친 줄 빼기), `src/corpus/check_build.py` 28·29번, `.githooks/pre-commit`(버전 파일의 stage본과 작업 폴더본 비교), 다시 만든 마크다운 `data/corpus/markdown/wiki-ko-cheongju.md`, `wiki-ko-chuncheon.md`
  - 표 글자 대조와 표 줄 찾기: `research_notes/stage2_markdown_rules/cell_loss_check.py`·`.txt`, `table_row_scans.py`·`.txt`
  - 사실 세기: `research_notes/stage2_fact_count/check.py`, `cleared.json`, `excluded.json`, `checked_markdown.json`, `counts_markdown.json`, `no_key_city_mentions.py`·`.txt`, `within_doc/`(문서 16개를 나눠 같은 문서 안의 다른 값을 찾은 지시문·답·검사), `known_conflicts.py`·`.md`
  - 표 모양: `research_notes/stage2_table_shapes/classify.py`, `shapes.md`
  - 최종 평가셋 지시서와 진행 안내: `data/questions/final_set_instructions.md`, `final_set_guide.md`(값이 부딪히는 사실의 규칙과 "알려진 부딪히는 값" 목록)
  - 일하는 방식의 결정 한 줄: `decisions/common.md`의 2026-10-14 줄
- 이슈 #4의 완료 기준은 `CODEX_REVIEW.md`의 "1차 요청"에 있다. ⑦은 이 검토 자체에 관한 항목이라 검토하지 않아도 된다.

## 1차 요청

- 단계: 2단계 (문서). 1차 검토다.
- 이슈: GitHub 이슈 #4 `[2단계] 문서`. 이슈의 하는 일과 완료 기준은 아래에 옮긴다. `STEPPER.md` 2단계 줄보다 이슈의 완료 기준이 자세하다(뒤에 더해진 ③-2, ④, ⑤, ⑥이 있다). ⑦은 이 검토 자체에 관한 항목이라 검토하지 않아도 된다.
- 산출물:
  - 문서 목록과 수집 기록: `data/corpus/documents.yaml`, `data/corpus/collected.yaml`
  - 원본과 마크다운: `data/corpus/raw/`, `data/corpus/markdown/` (28개씩)
  - 수집·변환·검사 코드: `src/corpus/` (`fetch.py`, `build.py`, `check_build.py`, `check_staged.py`), `.githooks/pre-commit`
  - 최종 평가셋 지시서와 진행 안내: `data/questions/final_set_instructions.md`, `data/questions/final_set_guide.md` (질문은 들어 있지 않다. 지시서의 예는 지어낸 것이다)
  - 조사와 계산의 기록: `research_notes/stage2_domain_survey/`, `research_notes/stage2_attraction_survey/`, `research_notes/stage2_fact_count/`, `research_notes/stage2_markdown_rules/`, `research_notes/stage2_table_shapes/`
- 이슈 #4의 하는 일과 완료 기준:
  - ① 도메인을 고른다. 완료 기준: 도메인과 고른 이유가 결정 기록에 있다. 아래 기준을 하나씩 대조한 결과가 함께 있다. 1단계의 질문 유형이 전부 나올 수 있다 / 언어별 최소 문서 수를 채운다 / 소스가 2개 이상이고 과제가 지정한 소스가 1개 이상이다 / 사용자가 내용을 판단할 수 있다 / 구체적 사실·표·여러 문서의 연결을 물을 수 있다 / 한쪽 언어 문서에만 있는 사실로 `EVALUATION.md` ② "코퍼스가 채워야 하는 수"의 표만큼 질문을 만들 수 있다(근거 문서 언어마다 36개, 그중 여러 문서 연결 12개, 표·수치·조건 6개) / 여러 문서 연결 질문을 위해 언어마다 문서가 2개 이상이다 / 한국어 문서와 영어 문서 각각에 질문을 만들 수 있는 표가 있다(표에서 나오는 서로 다른 사실이 언어마다 3개 이상)
  - ② 문서 20~30개의 목록을 만든다. 완료 기준: 문서마다 출처 주소, 식별자, 언어가 적힌 목록 파일이 있다.
  - ③ 수집 코드로 원문을 받고 마크다운으로 바꾼다. 완료 기준: 원본, 마크다운, 수집 시점이 저장되어 있다. 저장한 원본으로 변환 코드를 다시 실행하면 같은 코퍼스가 나온다(해시로 검사. 인터넷에서 다시 받는 것은 같은 바이트가 오지 않아 기준으로 삼지 않는다). 사용자가 열어 확인했다.
  - ③-2 만들어진 마크다운으로 한쪽 언어 문서에만 있는 사실을 다시 센다. 완료 기준: 정보 상자가 든 마크다운으로 겹침 검사를 다시 돌린 결과가 저장되어 있다. 문서 안에서 값이 서로 다른 곳도 다시 봤다. 근거 문서 언어마다 통과한 사실 36개 이상, 그중 표에서 나온 사실 6개 이상, 여러 문서 연결의 재료 12개 이상인지를 판단 기록에 적었다. 못 미치면 도시 구성으로 돌아간다.
  - ④ 수집을 다시 할 수 있는 조건을 정한다. 완료 기준: 처음 받는 것(최초 수집)과 저장해 둔 원본으로 다시 만드는 것(고정 원본 재처리)이 구분되어 있다. 해시로 같은 파일인지 검사한다.
  - ⑤ 마크다운으로 바꾼 뒤 표를 전부 본다. 완료 기준: 표가 어떤 모양으로 나왔는지 모양별로 적혀 있다. 한 칸에 줄바꿈으로 값이 둘 든 표와 칸을 합친 표가 있는지도 적혀 있다. 모양마다 어떻게 나눌지는 4단계에서 정한다.
  - ⑥ 최종 평가셋 지시서의 문서 목록 자리를 채운다. 완료 기준: `final_set_instructions.md`의 문서 목록 자리가 채워져 있다. 같은 파일과 `final_set_guide.md`에 있는 "`<...>`로 적은 곳은 3단계에서 채운다"는 문장을 문서 목록은 2단계에서 채웠다는 사실에 맞게 고쳤다. 저장할 곳과 검사 스크립트 명령의 자리는 3단계에서 채운다.
- 이 이슈에서 하지 않는 것: 질문·정답·근거 구절을 만드는 것(3단계), 청크와 표를 나누는 방법을 정하는 것(4단계), 정규화·청크·임베딩·인덱스(5단계).

## 1차 지적 원문

2단계를 완료로 보기 어렵습니다. **심각 1개, 보통 4개, 낮음 1개**를 찾았습니다. 파일은 수정하지 않았습니다.

1. **문제**: 머리글이 없는 표에서 실제 내용이 삭제됩니다. [build.py:315](/Users/seungchan/Workspace/MultilingualAgentRAG/src/corpus/build.py:315)의 빈 열 제거가 원인입니다.

   **근거**: 첫 내용 줄을 머리글로 취급하고, 그 아래가 빈 열을 삭제합니다. 그 결과 청주 원본의 **국도 36호선과 도로명**이 [마크다운:364](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-ko-cheongju.md:364)에서 빠졌습니다. 춘천 원본의 **한국방송통신대학교 강원지역대학**도 [마크다운:426](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-ko-chuncheon.md:426)에서 빠졌습니다. 원본 위치는 각각 `raw/wiki-ko-cheongju.html:897`, `raw/wiki-ko-chuncheon.html:1004`입니다. 이는 `decisions/stage2.md:29`의 빈 열 제거 규칙을 적용하면서 내용 줄을 잘못 구분한 것입니다. 기존 검사 27개는 이 누락을 잡지 못합니다.

   **심각도**: 심각

   **고칠 방법**: 실제 머리글과 내용 줄을 구분하십시오. 머리글이 없는 표에서는 첫 줄까지 포함해 빈 열인지 판단해야 합니다. 두 누락 사례를 검사에 추가하고, 변환 코드로 마크다운·해시·관련 조사 결과를 다시 만드십시오.

2. **문제**: 검색 키가 하나도 남지 않은 사실 9개가 겹침 검사에서 자동으로 통과합니다. [check.py:76](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/check.py:76).

   **근거**: 숫자는 세 글자 이상, 이름은 두 글자 이상만 남깁니다. 둘 다 비면 검색 결과도 비고, 98~99줄에서 바로 `통과`가 됩니다. 실제로 [강릉의 Cfa 기록:126](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/checked_markdown.json:126)은 두 키 목록이 비어 있습니다. [경주의 대학교 3곳 기록:524](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/checked_markdown.json:524)은 유일한 키 `3`이 제거됩니다. 이런 항목은 반대 언어에 같은 사실이 없는지 검사한 근거가 없습니다.

   **심각도**: 보통

   **고칠 방법**: 유효한 검색 키가 없으면 `미확인`으로 처리하고 통과 수에서 빼십시오. 필요한 키를 보충하거나 반대 언어 문서를 직접 대조한 기록을 남긴 뒤 통과시키십시오.

3. **문제**: 질문에 쓰지 않기로 한 충돌 값이 완료 판정에 사용하는 통과 수와 연결 후보 수에 포함됩니다. [check.py:111](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/check.py:111).

   **근거**: `DECISIONS.md:86`은 경주·광주의 면적, 세종의 행정 구역과 2025년 인구, 수원의 연 강수량 등을 제외하도록 기록했습니다. 그러나 `checked_markdown.json`의 `경주시_ko_03`, `광주광역시_ko_02`, `세종특별자치시_ko_01`, `세종특별자치시_ko_04`, `수원시_ko_05`는 모두 `통과`입니다. 이 항목들은 한국어 통과 110개와 연결 후보 197개에 들어갑니다. 저장된 숫자는 재현되지만, 질문에 사용할 수 있는 수와는 다릅니다.

   **심각도**: 보통

   **고칠 방법**: 겹침 검사 통과와 질문 사용 가능 여부를 따로 기록하십시오. 이미 정한 제외 조건을 적용한 사실 수·표 사실 수·연결 재료 수로 36·6·12 기준을 다시 대조하고 판단 기록을 갱신하십시오.

4. **문제**: 커밋 검사가 stage된 변환 환경을 사용하지 않습니다. [.githooks/pre-commit:23](/Users/seungchan/Workspace/MultilingualAgentRAG/.githooks/pre-commit:23), [check_staged.py:31](/Users/seungchan/Workspace/MultilingualAgentRAG/src/corpus/check_staged.py:31).

   **근거**: `uv.lock`과 `.python-version` 변경도 검사 조건에 넣었지만, 임시 폴더에는 stage된 `build.py`와 `data/corpus/`만 꺼냅니다. 실행은 현재 환경의 `sys.executable`로 합니다. 따라서 새 잠금 파일이나 Python 버전만 stage하고 작업 폴더에는 이전 판을 남긴 경우, 이전 환경으로 검사하게 됩니다. `decisions/stage2.md:36~37`에서 이 파일들을 검사 조건에 넣은 목적을 충족하지 못합니다.

   **심각도**: 보통

   **고칠 방법**: stage된 환경 파일에 맞는 Python·라이브러리로 재변환을 검사하십시오. 최소한 검사 환경과 stage된 환경이 다르면 거부해야 합니다. 환경 파일만 부분적으로 stage한 경우도 확인 항목에 넣으십시오.

5. **문제**: 최종 마크다운의 사용자 확인이 미확인인데 ③을 완료로 판정했습니다. [decisions/judgments.md:34](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/judgments.md:34).

   **근거**: 같은 줄에서 완료 기준 ①~⑥을 채웠다고 하면서, 마지막 마크다운을 사용자가 열어 확인했다는 기록은 없다고 명시합니다. 변환 규칙을 정할 때 이전 결과를 본 기록만으로 최종 결과의 확인까지 입증되지는 않습니다. 이번에 실제 누락도 발견되었습니다.

   **심각도**: 보통

   **고칠 방법**: 누락을 고친 최종 마크다운을 사용자가 확인한 뒤 대상 판과 확인 범위를 기록하십시오. 그 전에는 ③의 사용자 확인 부분을 미확인으로 두십시오.

6. **문제**: 표 조사 수량의 설명 두 곳이 저장된 목록과 다릅니다. [decisions/judgments.md:32](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/judgments.md:32), [shapes.md:34](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_table_shapes/shapes.md:34).

   **근거**: 줄바꿈 후보 23개의 실제 분류는 **기후 단위 변환 18개, 제목의 단위·구분 4개, 설명 줄바꿈 1개**입니다. 판단 기록은 19·3·1로 적었습니다. 또한 `table_items`가 받은 원문 표를 125개라고 썼지만 실제 HTML 표 호출은 **123개**이며, 125개는 CSV 표 기록 2개를 합친 수입니다.

   **심각도**: 낮음

   **고칠 방법**: 분류 설명을 18·4·1로 고치고, HTML 표 123개와 CSV 표 2개를 구분해 표기하십시오.

**문제없다고 판단한 부분**  
문서 목록·원본·마크다운·수집 기록은 28개로 일치하며, 한국어·영어 각 14개이고 출처 조건을 충족합니다. 현재 환경의 검사 27개는 통과했고, 저장된 사실·표 집계는 재계산과 일치하며 지시서의 문서 목록과 자리 안내도 맞습니다.  
실제 재수집과 커밋 훅의 환경 변경 실행은 확인하지 않았습니다. 최종 평가용 질문은 찾거나 열지 않았습니다.

## 2차 지적 원문

**1차 지적 6개는 모두 해소됐습니다. 고치는 과정에서 추가된 산출물에서 보통 문제 3개를 찾았습니다. 심각한 새 문제는 발견하지 못했습니다.**

| 1차 지적 | 판정 | 확인 근거 |
|---|---|---|
| 1. 표 첫 줄 내용 삭제 | 해소됨 | 두 누락이 복구됐고 검사 28·29번 통과. 표 글자 대조 결과도 저장본과 일치 |
| 2. 검색 키 없는 사실 자동 통과 | 해소됨 | 자동 통과를 차단했고, 9개에 대조 기록과 별도 판정을 남김 |
| 3. 제외할 값이 집계에 포함 | 해소됨 | 기존 5개를 포함한 29개 제외. 재계산도 한국어 93개·표 34개·연결 후보 87개, 영어 100개·표 39개·연결 후보 64개와 일치 |
| 4. stage와 검사 환경 불일치 | 해소됨 | 버전 파일 불일치를 거부하는 코드 확인. 거부 분기도 모의 실행으로 확인 |
| 5. 사용자 확인 기록 누락 | 해소됨 | [판단 기록 37·38번째 줄](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/judgments.md:37)에 대상과 확인 범위가 기록됨 |
| 6. 표 조사 수량 설명 오류 | 해소됨 | HTML 123개·CSV 2개로 구분됐고, 줄바꿈 후보 분류도 18·4·1로 일치 |

1. **문제**: 서로 다른 사건을 충돌로 판정해 사용 가능한 사실을 제외했습니다. [강릉 판정:12](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/within_doc/wiki-en-gangneung.answer.json:12), [excluded.json:7](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/excluded.json:7), [진행 안내:90](/Users/seungchan/Workspace/MultilingualAgentRAG/data/questions/final_set_guide.md:90).

   **근거**: [강릉 마크다운의 9·10번째 줄](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-en-gangneung.md:9)은 **시 설치 1955년**과 **명주 지역 합병 1995년**을 별도 항목으로 구분합니다. 본문 38번째 줄도 1995년 사건을 합병으로 설명합니다. 그런데 판정은 1955년만 인용해 두 사건을 같은 사실의 다른 값으로 묶었습니다. 이는 지시문의 “같은 대상의 같은 속성” 조건에 맞지 않습니다.

   **심각도**: 보통

   **고칠 방법**: `강릉시_en_03`을 합병 사건으로 구분해 판정을 고치고 제외 목록에서 빼십시오. 관련 집계·판단 기록·충돌 목록·진행 안내도 함께 다시 만드십시오.

2. **문제**: 결측값이 있는 부분합을 완전한 합처럼 사용해 충돌을 확정했습니다. [천안 판정:3](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/within_doc/wiki-ko-cheonan.answer.json:3), [excluded.json:9](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/excluded.json:9).

   **근거**: 서북구의 알려진 동별 인구 합은 330,499명이지만, [원문 표 91·92번째 줄](/Users/seungchan/Workspace/MultilingualAgentRAG/data/corpus/markdown/wiki-ko-cheonan.md:91)의 불당1·2동 인구는 `-`입니다. 따라서 이 합만으로 소계 400,566명이 틀렸다고 확정할 수 없습니다. [판단 기록:36](/Users/seungchan/Workspace/MultilingualAgentRAG/decisions/judgments.md:36)은 같은 두 결측칸 때문에 **면적 합은 대조할 수 없다**고 정정했지만, 인구에는 같은 처리를 적용하지 않았습니다.

   **심각도**: 보통

   **고칠 방법**: 결측칸이 있는 합계 대조는 검증 불가로 기록하십시오. 다른 독립적인 충돌 근거가 있다면 그 근거를 제외 사유로 쓰고, 없다면 현재의 부분합만으로 제외를 확정하지 마십시오. 충돌 목록과 안내서에도 같은 처리를 적용하십시오.

3. **문제**: 사실 검사에서 적용한 반올림 예외가 새 최종 평가셋 지시서에 빠졌습니다. [지시서:115](/Users/seungchan/Workspace/MultilingualAgentRAG/data/questions/final_set_instructions.md:115), [진행 안내:38](/Users/seungchan/Workspace/MultilingualAgentRAG/data/questions/final_set_guide.md:38).

   **근거**: 문서별 검사 지시문은 반올림·어림 표현을 충돌로 보지 않습니다. 실제 [경주 판정:40](/Users/seungchan/Workspace/MultilingualAgentRAG/research_notes/stage2_fact_count/within_doc/wiki-ko-gyeongju.answer.json:40)도 본문의 **1,091 mm**와 표의 **1,090.9 mm**를 같은 값으로 인정했습니다. 반면 새 지시서는 다른 값이면 제외하도록 하고 날짜가 다른 경우만 예외로 설명합니다. 그대로 따르면 사실 세기에서 허용한 값을 질문 생성에서는 잘못 제외할 수 있습니다.

   **심각도**: 보통

   **고칠 방법**: 지시서와 진행 안내에 “동일 단위에서 표시 자리수에 맞게 반올림하면 같은 값인 경우는 충돌로 보지 않는다”는 예외를 명시하십시오.

**문제없다고 판단한 부분**  
문서 28개·언어별 14개·출처 조건, 재현 및 해시 검사 29개, 저장된 사실·표 집계의 재계산은 일치했습니다.  
실제 부분 stage와 환경 변경을 동반한 훅 실행, 사용자 확인의 대화 원문은 확인하지 못했습니다. 파일은 수정하지 않았고 최종 평가용 질문은 찾거나 열지 않았습니다.
