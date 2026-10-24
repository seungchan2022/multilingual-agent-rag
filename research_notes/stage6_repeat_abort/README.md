# Baseline이 되풀이로 끊긴 사례 (이슈 #12, 2026-10-24)

6단계 "모델의 한계"를 볼 때 쓰려고, 다시 만들기 어려운 것을 여기 모아 둔다. 판단은 `decisions/judgments.md` 2026-10-24, 처리 규칙은 `decisions/stage6.md` 2026-10-24 "되풀이로 끊긴 답" 줄.

## 무슨 일이었나

- Baseline(문서 없이 답) 실행에서 씨앗 5, 질문 q04-ko(툴륨 직육면체의 질량, 정답 0.5592 kg)에 모델 qwen3:8b가 answer에 "0.000…"을 끝없이 썼고, Ollama가 `prediction aborted, token repeat limit reached`로 생성을 끊었다.
- reason에서 계산을 하지 않고 방법만 말한 뒤 answer를 "0."으로 시작했다. 밀도도 9.90 g/cm³로 틀렸다(문서 값 9.32).
- 380번 본 실행(`data/minimal/generation/runs_baseline.jsonl`)에서도 같은 요청이 끊겼고, 그 줄에 끊기기 전 글(270자)이 `output`, 이유가 `abort_reason`으로 남아 있다. 최소판(청크를 넣음)에서는 끊긴 답이 없었다.

## 재현 조건 (다시 해 보려면)

- 같은 순서: 몸풀기 → 씨앗 1~5 × 질문 38개(파일 순서), 한 번에 하나씩. 159번째가 이 요청이다.
- **모델을 내렸다가 막 올린 상태에서 시작해야 한다.** 모델이 이미 올라 있는 채로 시작하면 앞 158개 가운데 155개만 같았고 이 요청은 정상으로 답했다(`target_warm.json`, 0.495 kg). 내렸다가 시작하면 158개가 글자까지 같고 같은 곳에서 끊겼다(`target_cold.json`).
- 같은 환경: `environment.txt`(Ollama 0.35.1, qwen3:8b digest `500a1f06…`, Apple M3 Pro). Ollama나 모델 파일이 바뀌면 재현되지 않을 수 있다. Ollama 앱은 스스로 업데이트할 수 있으므로, 다시 해 보려면 먼저 판을 확인한다.
- 생성 설정: `src/minimal/generate.py`(커밋 `c5a4ae0`)의 `request_body`.

## 파일

| 파일 | 내용 |
|---|---|
| `replay.py` | 모델이 올라 있는 채로 158번을 다시 보내고 159번째만 stream으로 받는 재현 스크립트 |
| `replay_cold.py` | 같은 것을 모델을 내린 뒤 시작하는 판 |
| `target_warm.json`, `replay_warm.log` | 위 첫 재현의 결과: 158개 중 155개 같음, 끊기지 않음 |
| `target_cold.json`, `replay_cold.log` | 둘째 재현의 결과: 158개 모두 같음, 끊김, 끊기기 전 글과 마지막 조각 40개 |
| `ollama_server_log_excerpt.txt` | Ollama 서버 로그에서 HTTP 500 줄과 2026-10-24 모델 올림 줄. 10-24의 500은 12:18(첫 실행이 끊김), 13:42(AI가 멈춘 실행), 13:57(셋째 실행이 끊김) |
| `environment.txt` | Ollama 판, 모델 digest, 컴퓨터 |

## 뒤에 볼 것 (모델의 한계에서)

- 로그에는 10-18과 10-20(도메인 고르기 실험)에도 HTTP 500이 여러 번 있다. 그때도 같은 되풀이였는지는 확인하지 않았다.
- 끊긴 답이 계산을 건너뛴 답에서 나왔다. 끊기지 않았지만 계산을 건너뛴 답이 얼마나 되는지는 380번 기록의 reason으로 볼 수 있다(판정 기준을 먼저 정해야 함).
