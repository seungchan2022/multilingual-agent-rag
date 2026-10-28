"""이슈 #15 판 1의 어븀 질문(q09-en)에서 근거 칸이 이웃 청크(10번 「이터븀」)를 고른 원인을 가르는 시험. 결과 숫자에 쓰지 않는다.

  .venv/bin/python research_notes/stage6_answer_tests/cause_probe/probe.py

판 0(⑧ 기록)의 q09-en 청크 목록 그대로, 씨앗 1~5로 판 넷을 돌린다. 판마다 판 1에서 한 가지씩만 다르다.
  v0-json   : 판 0 지시문(SYSTEM_EN) + format "json"     → 판 0이 재현되는지(대조)
  v1-schema : 판 1 지시문(cite-en-v1) + 틀              → 판 1이 재현되는지
  v1-json   : 판 1 지시문 + format "json"               → 틀 때문인지
  v1-nofact : 판 1 지시문의 언어 줄에서 fact를 뺌 + 틀   → "fact도 질문 언어로" 줄 때문인지
결과는 같은 폴더의 out.jsonl에 쓴다(이미 있으면 멈춘다).
2차(--round 2, out2.jsonl): 위에서 틀과 fact 언어 줄이 주된 까닭이 아니어서, 판 1의 남은 바뀐 줄을 하나씩 본다.
  v1-norefuse : 판 1에서 "근거가 없으면 답할 수 없다고 써라" 줄만 뺌 + 틀
  v0-citefield: 판 0 지시문의 답 꼴 줄에만 citations 칸을 더함(다른 줄은 판 0 그대로) + 틀
  v1-copy     : 판 1 + "fact는 참고 글의 말을 그대로 옮기고, 그 사실이 무엇의 값인지(참고 글 제목의 이름)를 함께 써라" 한 줄 + 틀
3차(--round 3, out3.jsonl): 사용자가 안 ㉠(확인 줄을 더함)을 골라, 확인 줄의 효과를 q09-en과 번호를 잘못 적은 q02-en에서 본다.
  v1-schema    : 판 1 그대로(q02-en의 대조)
  v1-titlecheck: 판 1의 근거 칸 줄 다음에 "값을 쓰기 전에 그 참고 글의 제목이 질문이 묻는 것과 같은지, 다른 언어여도 확인하라" 한 줄 + 틀
4차(--round 4, out4.jsonl): 3차의 확인 줄이 q09-en을 고치지 못해, 참고 글 머리의 문서 ID(wiki-ko-<영어 이름>)로 확인하게 하는 줄을 본다.
  v1-idcheck: 판 1의 근거 칸 줄 다음에 "참고 글은 문서 ID로 시작하고 ID에는 다룬 것의 영어 이름이 있다(예: wiki-ko-<영어 이름>). 값을 쓰기 전에 ID로 질문이 묻는 것과 같은지 확인하라" + 틀
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src" / "minimal"))
sys.path.insert(0, str(ROOT / "src" / "agent"))
import answer  # noqa: E402
import generate  # noqa: E402
import run_answer  # noqa: E402
from index import DSN, QUESTIONS  # noqa: E402

QID = "q09-en"
OUT = Path(__file__).resolve().parent / "out.jsonl"
OUT2 = Path(__file__).resolve().parent / "out2.jsonl"
REFUSE = ("If the reference passages do not contain the facts needed to answer, write in answer that the question cannot be answered from the passages, "
          "and write [] for citations.")
FORMAT_V0 = '{"reason": "Write the reasoning that leads to the answer, step by step", "answer": "Write only the final answer, briefly"}'
COPY = ("In fact, copy the words of the passage as they are, and include the name of the thing the fact is about, "
        "as written in the passage title.")
TITLE_CHECK = ("Before you use a value, check that the title of its passage names the same thing the question asks about, "
               "even if the passage is in a different language from the question.")
OUT3 = Path(__file__).resolve().parent / "out3.jsonl"
OUT4 = Path(__file__).resolve().parent / "out4.jsonl"
ID_CHECK = ("Each reference passage starts with its document ID, and the ID contains the English name of what the document is about "
            "(for example, wiki-ko-<English name>). Before you use a value, check with the ID that the passage is about the same thing the question asks about.")
assert REFUSE in answer.CITE_V1 and FORMAT_V0 in generate.SYSTEM_EN
LANG_V1 = ("Answer in the same language as the question. If the question is in Korean, write reason, answer, and fact in Korean; "
           "if it is in English, write them in English.")
LANG_V0 = ("Answer in the same language as the question. If the question is in Korean, write reason and answer in Korean; "
           "if it is in English, write them in English.")
assert LANG_V1 in answer.CITE_V1 and LANG_V0 in generate.SYSTEM_EN


def variants(found):
    context = generate.CONTEXT_EN.format(passages=generate.passages_of(found))
    n = len(found)
    nofact = answer.CITE_V1.replace(LANG_V1, LANG_V0)
    return {"v0-json": (generate.SYSTEM_EN + context, "json"),
            "v1-schema": (answer.CITE_V1 + context, answer.schema(n)),
            "v1-json": (answer.CITE_V1 + context, "json"),
            "v1-nofact": (nofact + context, answer.schema(n))}


def variants2(found):
    context = generate.CONTEXT_EN.format(passages=generate.passages_of(found))
    n = len(found)
    format_v1 = answer.CITE_V1.split("\n")[1]
    return {"v1-norefuse": (answer.CITE_V1.replace(REFUSE + "\n", "") + context, answer.schema(n)),
            "v0-citefield": (generate.SYSTEM_EN.replace(FORMAT_V0, format_v1) + context, answer.schema(n)),
            "v1-copy": (answer.CITE_V1.replace(REFUSE, REFUSE + "\n" + COPY) + context, answer.schema(n))}


def variants3(found):
    context = generate.CONTEXT_EN.format(passages=generate.passages_of(found))
    n = len(found)
    return {"v1-schema": (answer.CITE_V1 + context, answer.schema(n)),
            "v1-titlecheck": (answer.CITE_V1.replace(REFUSE, TITLE_CHECK + "\n" + REFUSE) + context, answer.schema(n))}


def variants4(found):
    context = generate.CONTEXT_EN.format(passages=generate.passages_of(found))
    return {"v1-idcheck": (answer.CITE_V1.replace(REFUSE, ID_CHECK + "\n" + REFUSE) + context, answer.schema(len(found)))}


def main():
    import psycopg
    round_ = sys.argv[sys.argv.index("--round") + 1] if "--round" in sys.argv else "1"
    out_path, make, names, qids = {"1": (OUT, variants, ("v0-json", "v1-schema", "v1-json", "v1-nofact"), (QID,)),
                                   "2": (OUT2, variants2, ("v1-norefuse", "v0-citefield", "v1-copy"), (QID,)),
                                   "3": (OUT3, variants3, ("v1-schema", "v1-titlecheck"), ("q09-en", "q02-en")),
                                   "4": (OUT4, variants4, ("v1-idcheck",), ("q09-en", "q02-en"))}[round_]
    generate.check_new(out_path)
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    base_rows = run_answer.read_jsonl(run_answer.BASE_RUNS)
    with psycopg.connect(DSN) as conn:
        items = [i for i in run_answer.prepare(conn, base_rows, questions) if i["row"]["question_id"] in qids]
    run_answer.warm_up()
    with open(out_path, "x", encoding="utf-8") as out:
        for name in names:
            for item in items:
                seed, found, question = item["row"]["seed"], item["found"], item["question"]
                system_message, fmt = make(found)[name]
                body = generate.request_body(system_message, question["question"], seed)
                body["format"] = fmt
                text, seconds, *_ = generate.send(body)
                graded = generate.graded(question, text)
                try:
                    citations = json.loads(text).get("citations")
                except (json.JSONDecodeError, AttributeError):
                    citations = None
                cited = answer.cited_of(citations, found) if isinstance(citations, list) and answer.shape_ok_of(json.loads(text)) else None
                wrong = None if cited is None else sum(bool(c["missing_numbers"]) for item in cited if item["numbers"] for c in item["checks"])
                row = {"variant": name, "question_id": item["row"]["question_id"], "wrong_attached": wrong, "seed": seed, "answer": graded["answer"], "correct": graded["correct"],
                       "citations": citations, "reason": graded["reason"], "seconds": seconds, "hit_ranks": item["search"]["hit_ranks"]}
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
                out.flush()
                print(name, item["row"]["question_id"], seed, "wrong_attached", wrong, graded["answer"], "맞음" if graded["correct"] else "틀림", citations, flush=True)


if __name__ == "__main__":
    main()
