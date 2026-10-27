import json, sys
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal")
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/agent")
import generate, plan
qs = {q["id"]: q for q in json.load(open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json"))}
q = qs["q01-ko"]["question"]
for temp in (0, 0.7):
    for seed in range(1, 11):
        body = generate.request_body(plan.PLAN_SYSTEM, q, seed)
        body["options"]["temperature"] = temp
        text, *_ = generate.send(body)
        try: kq = json.loads(text).get("korean_question", "")
        except Exception: kq = "(JSON 아님)"
        print(temp, seed, "그대로" if "유로퓸" in kq else "깨짐/다름", "|", kq[30:50], flush=True)
