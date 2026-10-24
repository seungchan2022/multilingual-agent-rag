"""Baseline 실행과 같은 순서(몸풀기 → 씨앗 1~5 × 질문 순서)로 158번을 다시 보내고, 159번째(씨앗 5, q04-ko)만 stream으로 받아 끊기기 전까지의 글을 남긴다.
앞 158번의 글이 저장된 기록과 같은지도 센다. 저장소 파일은 쓰지 않는다."""
import sys, json, urllib.request
ROOT = "/Users/seungchan/Workspace/MultilingualAgentRAG"
sys.path.insert(0, ROOT + "/src/minimal")
import generate as g
OUT = sys.argv[1]
qs = json.loads(g.QUESTIONS.read_text(encoding="utf-8"))
saved = [json.loads(l)["output"] for l in open(ROOT + "/data/minimal/generation/runs_baseline.aborted-3.jsonl")]
urllib.request.urlopen(urllib.request.Request(g.URL.replace("/api/chat", "/api/generate"), data=json.dumps({"model": g.MODEL, "keep_alive": 0}).encode(), headers={"Content-Type": "application/json"})).read()  # 모델을 내려 실제 실행처럼 막 올린 상태에서 시작한다
g.chat(g.SYSTEM_EN, g.WARMUP_USER, 1)
n, same = 0, 0
for seed in g.SEEDS:
    for q in qs:
        s, u = g.messages_of("baseline", q)
        if n < 158:
            out = g.chat(s, u, seed)[0]
            same += out == saved[n]
            n += 1
            continue
        body = g.request_body(s, u, seed); body["stream"] = True
        req = urllib.request.Request(g.URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        parts, err = [], None
        with urllib.request.urlopen(req, timeout=600) as r:
            for line in r:
                d = json.loads(line)
                if "error" in d:
                    err = d["error"]; break
                parts.append(d.get("message", {}).get("content", ""))
        text = "".join(parts)
        json.dump({"replayed": n, "same_as_saved": same, "target": q["id"], "seed": seed, "error": err,
                   "chars": len(text), "pieces": len(parts), "text": text, "last_pieces": parts[-40:]},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("done", n, same, err, len(text))
        sys.exit(0)
