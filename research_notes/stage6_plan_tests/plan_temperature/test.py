import json, sys
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal")
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/agent")
import generate, plan
qs = {q["id"]: q for q in json.load(open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json"))}
q = qs["q01-ko"]["question"]
out = []
for fmt in ("json", None):
    for seed in (1, 2, 3, 4, 5):
        body = generate.request_body(plan.PLAN_SYSTEM, q, seed)
        if fmt is None:
            body.pop("format")
        text, secs, *_ = generate.send(body)
        try:
            p = json.loads(text); kq = p.get("korean_question", "")
        except Exception:
            kq = "(JSON 아님) " + text[:200]
        ok = "유로퓸" in kq
        out.append((fmt, seed, ok, kq))
        print(fmt, seed, "유로퓸 그대로" if ok else "깨짐/다름", "|", kq[:90], flush=True)
