import json, sys, urllib.request
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/minimal")
sys.path.insert(0, "/Users/seungchan/Workspace/MultilingualAgentRAG/src/agent")
import merge
from index import DSN, load_model
import generate
import psycopg

TOOLS = [{"type": "function", "function": {"name": "search_documents", "description": "Search the document index (Korean and English documents) and return the most relevant chunks for a query.",
          "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "the search query"}}, "required": ["query"]}}}]
SYSTEMS = {
 "free": "You find documents to answer the question. Do not answer the question. You are given the question and a search plan. Call search_documents as many times as you need, then reply DONE.",
 "plan": "You find documents to answer the question. Do not answer the question. You are given the question and a search plan. Call search_documents three times: with the original question, with korean_question, and with english_question from the plan. Then reply DONE.",
}
Q = {q["id"]: q for q in json.load(open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/minimal/questions.json"))}
rows = [json.loads(l) for l in open("/Users/seungchan/Workspace/MultilingualAgentRAG/data/agent/plan_search/runs.jsonl")]

def call(messages):
    body = {"model": "qwen3:8b", "messages": messages, "tools": TOOLS, "stream": False, "think": False,
            "options": {"temperature": 0, "top_p": 0.8, "top_k": 20, "min_p": 0, "num_ctx": 32768, "num_predict": 2048, "seed": 1}}
    req = urllib.request.Request("http://localhost:11434/api/chat", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=600).read())["message"]

model = load_model(generate.EMBED_MODEL)
with psycopg.connect(DSN) as conn:
    for variant in ("free", "plan"):
        for qid in ("q03-en", "q09-en", "q13-en", "q14-en", "q12-ko"):
            q = Q[qid]; p = next(r for r in rows if r["question_id"] == qid and r["seed"] == 1)["first_plan"]
            plan = {k: p[k] for k in ("targets", "korean_question", "english_question")}
            messages = [{"role": "system", "content": SYSTEMS[variant]},
                        {"role": "user", "content": "Question:\n" + q["question"] + "\n\nSearch plan:\n" + json.dumps(plan, ensure_ascii=False)}]
            queries = []
            for turn in range(6):
                m = call(messages)
                messages.append(m)
                tcs = m.get("tool_calls") or []
                if not tcs:
                    break
                for tc in tcs:
                    query = tc["function"]["arguments"].get("query", "")
                    found, rows_, _, _ = merge.fetch(conn, model, q, query, 4)
                    hit = any(r.get("evidence") for r in rows_)
                    queries.append({"query": query, "hit": hit})
                    content = "\n\n".join(f"[{i+1}] {f[4][:400]}" for i, f in enumerate(found))
                    messages.append({"role": "tool", "content": content, "tool_name": "search_documents"})
            kq = p["korean_question"].strip()
            print(json.dumps({"variant": variant, "q": qid, "n_calls": len(queries),
                              "used_korean_version": any(x["query"].strip() == kq for x in queries),
                              "any_korean_query": any(any("가" <= ch <= "힣" for ch in x["query"]) for x in queries),
                              "any_hit_top4": any(x["hit"] for x in queries), "queries": queries,
                              "final_text": (m.get("content") or "")[:120]}, ensure_ascii=False), flush=True)
