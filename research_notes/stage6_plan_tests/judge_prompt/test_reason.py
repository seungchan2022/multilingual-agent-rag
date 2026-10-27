import json, sys
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal")
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/agent")
import generate, plan
from test_judge import DRAFT

REASON_LINE = ("The planner's reasoning is also given. Use it only to understand why the plan was written that way. "
               "Judge the plan by comparing it with the question.")

def with_reason(system):
    lines = system.split("\n")
    return "\n".join(lines[:2] + [REASON_LINE] + lines[2:])

def message(question, p, reason):
    if not reason:
        return plan.judge_user_message(question, p)
    return "Question:\n" + question + "\n\nPlanner's reasoning:\n" + p["reason"] + "\n\nSearch plan:\n" + plan.plan_json(p)

# 기대: Claude가 계획을 질문과 대조해 붙인 값
EXPECT = {"q09-ko": False, "q01-ko": False, "q18-ko": False, "q19-ko": False, "q02-ko": False,
          "q14-ko": True, "q13-ko": True, "q16-ko": True}
VARIANTS = [("v2", plan.JUDGE_SYSTEM, False), ("고친 판", DRAFT, False),
            ("v2+생각", with_reason(plan.JUDGE_SYSTEM), True), ("고친 판+생각", with_reason(DRAFT), True)]
qs = {q["id"]: q["question"] for q in json.load(open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json"))}
rows = [json.loads(l) for l in open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/agent/plan_search/runs.jsonl")]
for name, system, reason in VARIANTS:
    for qid, want in EXPECT.items():
        p = next(x for x in rows if x["question_id"] == qid and x["seed"] == 1)["first_plan"]
        body = plan.judge_body(message(qs[qid], p, reason), 1)
        body["messages"][0]["content"] = system
        text, *_ = generate.send(body)
        j, errs = plan.check_judgment(text)
        got = plan.passed(j) if not errs else None
        print(json.dumps({"variant": name, "q": qid, "expect_pass": want, "passed": got, "right": got == want,
                          "shape_errors": errs, "checks": {c: j.get(c) for c in plan.CHECKS} if j else None,
                          "problems": j.get("problems") if j else text[:300]}, ensure_ascii=False), flush=True)
