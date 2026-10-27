import json, sys
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal")
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/agent")
import generate, plan
qs = {q["id"]: q for q in json.load(open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json"))}
rows = [json.loads(l) for l in open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/agent/plan_search/runs.jsonl")]
for qid in ("q18-ko", "q09-ko", "q19-ko", "q16-ko", "q01-ko"):
    q = qs[qid]["question"]
    body = generate.request_body(plan.PLAN_SYSTEM, q, 1)
    body["options"]["temperature"] = 0
    text, *_ = generate.send(body)
    kq = json.loads(text).get("korean_question", "")
    print("==", qid, "온도 0:", "그대로" if kq.strip() == q.strip() else "다름")
    print("   원문 :", q)
    if kq.strip() != q.strip(): print("   온도0:", kq)
    bad = [r["first_plan"]["korean_question"] for r in rows if r["question_id"] == qid and r["first_plan"] and r["first_plan"]["korean_question"].strip() != q.strip()]
    for b in bad[:2]: print("   0.7 실패 예:", b)
