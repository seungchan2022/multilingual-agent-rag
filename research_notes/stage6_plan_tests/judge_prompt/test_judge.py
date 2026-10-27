import json, sys
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal")
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/agent")
import generate, plan

DRAFT = "\n".join([
    "You check a search plan written for a question. Do not answer the question.",
    "The plan has targets (facts to look up, each with a condition and a unit), korean_question, and english_question.",
    "Check three things.",
    "targets_ok: targets include every fact needed to answer the question, and each condition and unit matches the question.",
    "korean_ok: korean_question is written in Korean and asks exactly the same thing as the question: "
    "the same numbers, names, symbols, conditions, and units, with nothing added or dropped.",
    "english_ok: english_question is written in English and asks exactly the same thing as the question.",
    "A check fails only when you can point to a word or value in the plan that differs from the question. "
    "Different wording with the same meaning is not a problem.",
    "A word in korean_question that is not Korean, or a word in english_question that is not English, is a problem, "
    "unless it is a number, symbol, abbreviation, unit, or name kept from the question.",
    "reason: before deciding, compare the plan with the question item by item and write what matches and what differs.",
    "For every check that fails, write one problem: quote the wrong text from the plan and the text it should match in the question.",
    "Answer only in the JSON format below.",
    '{"reason": "...", "targets_ok": true, "korean_ok": true, "english_ok": true, "problems": ["..."]}',
])

if __name__ == "__main__":
    qs = {q["id"]: q["question"] for q in json.load(open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json"))}
    rows = [json.loads(l) for l in open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/agent/plan_search/runs.jsonl")]
    for name, system in (("v2(지금)", plan.JUDGE_SYSTEM), ("고친 판", DRAFT)):
        for qid in ("q09-ko", "q14-ko"):
            for seed in range(1, 6):
                r = next(x for x in rows if x["question_id"] == qid and x["seed"] == seed)
                body = plan.judge_body(plan.judge_user_message(qs[qid], r["first_plan"]), seed)
                body["messages"][0]["content"] = system
                text, *_ = generate.send(body)
                j, errs = plan.check_judgment(text)
                print(json.dumps({"prompt": name, "q": qid, "seed": seed, "shape_errors": errs,
                                  "passed": plan.passed(j) if not errs else None,
                                  "checks": {c: j.get(c) for c in plan.CHECKS} if j else None,
                                  "problems": j.get("problems") if j else text[:300]}, ensure_ascii=False), flush=True)
