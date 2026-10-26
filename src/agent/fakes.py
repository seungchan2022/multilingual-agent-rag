"""src/agent의 시험들이 같이 쓰는 가짜들(시험 파일이 아니다). Ollama와 실제 데이터베이스 없이 고리를 돌려 보게 한다.

FakeOllama는 urlopen을 대신해 요청 본문을 역할(생성 모델의 계획 쓰기 / 판정 모델 / 답 쓰기)로 나눠 정해 둔 글을 순서대로 돌려준다.
fake_search는 merge.embed_query와 merge.search를 대신한다. 검색어 글이 곧 가짜 벡터이고, 글마다 정해 둔 청크 줄 목록을 k개만큼 돌려준다.
"""
import json
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "minimal"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402
import merge  # noqa: E402
import plan  # noqa: E402

ANSWER = '{"reason": "읽는다", "answer": "17.7 kg"}'


def question(qid="q01-ko", lang="ko", text="반감기는 몇 시간인가?", pair_id="q01-en"):
    return {"id": qid, "lang": lang, "branch": "한국어만", "pair_id": pair_id, "question": text, "value": 17.7, "unit": "kg", "answer": "17.7 kg",
            "evidence": [{"doc_id": "doc-a", "line": 5, "value_text": "17.7"}]}


def found_row(chunk_id, text="무관한 글", evidence=False):
    """search가 돌려주는 한 줄 (chunk_id, distance, doc_id, lines, text, tokens, language, line_start, line_end). evidence가 참이면 질문 question()의 근거를 채운다."""
    if evidence:
        return (chunk_id, 0.1, "doc-a", [5], "반감기는 17.7 시간이다 " + text, 9, "en", 5, 5)
    return (chunk_id, 0.1, "doc-b", [1], text, 9, "en", 1, 1)


def plan_output(korean="한국어판", english="english version", reason="생각", targets=None):
    targets = [{"fact": "half-life", "condition": "", "unit": "h"}] if targets is None else targets
    return json.dumps({"reason": reason, "targets": targets, "korean_question": korean, "english_question": english}, ensure_ascii=False)


def judge_output(targets_ok=True, korean_ok=True, english_ok=True, problems=(), reason="견줌"):
    return json.dumps({"reason": reason, "targets_ok": targets_ok, "korean_ok": korean_ok, "english_ok": english_ok, "problems": list(problems)}, ensure_ascii=False)


class FakeResponse:
    """stream 응답 하나. 글은 두 조각으로 나눠 오고 끝에 done 줄이 온다. error를 주면 done 줄 대신 error 줄이 온다."""

    def __init__(self, content, error=None):
        cut = len(content) // 2
        lines = [{"message": {"role": "assistant", "content": piece}, "done": False} for piece in (content[:cut], content[cut:]) if piece]
        lines.append({"error": error} if error else {"message": {"role": "assistant", "content": ""}, "done": True, "eval_count": 12, "prompt_eval_count": 345})
        self.lines = [(json.dumps(line, ensure_ascii=False) + "\n").encode() for line in lines]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def __iter__(self):
        return iter(self.lines)

    def read(self):
        return b'{"done": true}'


class FakeOllama:
    """urlopen을 대신한다. 모든 요청을 순서대로 calls에, 채팅 요청은 (역할, 본문)으로 requests에 쌓는다.
    역할은 'warmup'(사용자 메시지가 몸풀기 글. 큐를 쓰지 않고 빈 객체를 돌려준다), 'plan'(생성 모델, 시스템 메시지가 PLAN_SYSTEM),
    'judge'(판정 모델), 'answer'(생성 모델, 그 밖)이다.
    plans와 judges는 그 역할의 요청이 올 때마다 앞에서부터 하나씩 꺼내 쓰는 글 목록이고, 모자라면 AssertionError다.
    plans나 judges의 항목이 FakeResponse면 그대로 돌려주고, 글이면 FakeResponse로 감싼다. 답 쓰기는 늘 answer 글이다."""

    def __init__(self, plans=(), judges=(), answer=ANSWER):
        self.plans, self.judges, self.answer = list(plans), list(judges), answer
        self.requests, self.calls = [], []

    def role_of(self, body):
        if body["messages"][1]["content"] == generate.WARMUP_USER:
            return "warmup"
        if body["model"] == plan.JUDGE_MODEL:
            return "judge"
        return "plan" if body["messages"][0]["content"] == plan.PLAN_SYSTEM else "answer"

    def __call__(self, req, timeout=None):
        body = json.loads(req.data)
        self.calls.append((req.full_url, body))
        if req.full_url == generate.GENERATE_URL:
            return FakeResponse("")
        assert req.full_url == generate.URL, req.full_url
        role = self.role_of(body)
        self.requests.append((role, body))
        if role == "warmup":
            return FakeResponse("{}")
        queue = {"plan": self.plans, "judge": self.judges}.get(role)
        content = self.answer if queue is None else queue.pop(0)
        return content if isinstance(content, FakeResponse) else FakeResponse(content)

    def roles(self):
        return [role for role, _ in self.requests]


@contextmanager
def patched(ollama, searches):
    """urlopen을 ollama로, merge의 임베딩과 검색을 가짜로 바꾼다. searches는 {검색어 글: search 결과 줄 목록}이다.
    검색 호출은 (검색어 글, k)로 merge_calls에 쌓아 돌려준다. 목록에 없는 검색어는 AssertionError다."""
    calls = []

    def fake_search(conn, chunk_set, model_name, vector, k):
        assert vector in searches, f"가짜 검색에 없는 검색어: {vector!r}"
        calls.append((vector, k))
        return searches[vector][:k]

    with mock.patch.object(generate.urllib.request, "urlopen", ollama), mock.patch.object(merge, "embed_query", lambda model, text: text), \
            mock.patch.object(merge, "search", fake_search):
        yield calls
