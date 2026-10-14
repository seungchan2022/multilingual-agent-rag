"""코퍼스 문서 28개의 원본을 받는 프로그램.

  uv run python src/corpus/fetch.py                       documents.yaml의 문서를 차례로 받는다
  uv run python src/corpus/fetch.py --only <doc_id> ...   그 문서만 받는다
  uv run python src/corpus/fetch.py --force               이미 받은 문서도 다시 받는다

원본은 data/corpus/raw/에 받은 그대로 쓰고, 받은 사실은 data/corpus/collected.yaml에 적는다.
마크다운으로 바꾸는 일은 여기서 하지 않는다. 요청은 한 번에 하나씩, 2초 간격으로 보낸다.
확인에 걸린 문서는 원본을 쓰지 않고(있던 파일도 덮어쓰지 않고) 끝에 모아 알린 뒤 종료 코드 1로 끝낸다.
"""
import argparse, csv, gzip, hashlib, io, json, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "corpus"
RAW = CORPUS / "raw"
DOCS = CORPUS / "documents.yaml"
COLLECTED = CORPUS / "collected.yaml"
UA = "MultilingualAgentRAG-corpus/1.0 (https://github.com/seungchan2022/multilingual-agent-rag)"
GAP = 2                    # 요청 사이에 쉬는 초
RETRY_WAIT = (5, 30, 60, 60)  # 다시 하는 횟수는 4번. Retry-After가 없을 때 쉬는 초
HEADER = "# 수집 기록. src/corpus/fetch.py가 원본을 받을 때 쓴다. 마크다운의 해시는 src/corpus/build.py가 채운다.\n"

# 출처마다 collected.yaml에 그대로 적는 글자. 다른 이름이나 주소를 지어 넣지 않는다.
MODIFIED = "규칙은 decisions/stage2.md의 2026-10-14 줄에 있다."
LICENSE = {
    "wiki": {
        "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "modified": "원문에서 이미지, 각주, 링크의 연결, 안내 줄 등을 지우고 마크다운으로 바꿨다. " + MODIFIED,
    },
    "kto": {
        "license": "한국관광공사 관광정보의 저작권 유형 Type1 (응답의 cpyrhtDivCd 값)",
        "modified": "소개 글에 제목과 주소 줄을 붙이고 <br>과 문자 참조를 글자로 바꿨다. " + MODIFIED,
    },
    "portal": {
        "license": "이용허락범위: 제한 없음 (자료 설명 페이지에 적힌 값)",
        "modified": "파일의 칸 이름과 값을 바꾸지 않고 마크다운 표로 옮기고 제목을 붙였다. " + MODIFIED,
    },
}


class Fail(Exception):
    """확인에 걸렸거나 요청이 끝내 실패했을 때. 메시지에 주소를 넣지 않는다(관광공사 주소에는 키가 있다)."""


def key():
    env = dict(l.strip().split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l)
    return env["DATA_GO_KR_KEY"]


def wait_from(headers, fallback):
    """Retry-After 헤더의 초. 없거나 숫자가 아니면 fallback."""
    v = headers.get("Retry-After") if headers else None
    return int(v) if v and v.strip().isdigit() else fallback


def get(url, headers, busy=None):
    """한 번 요청해 본문 바이트를 돌려준다. 429, 5xx, 연결 오류는 쉬었다가 4번까지 다시 한다.

    busy(본문, 헤더)가 초를 돌려주면 서버가 바쁘다는 뜻이니 그만큼 쉬고 다시 한다(위키백과 maxlag).
    """
    for n in range(len(RETRY_WAIT) + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
                body, h = r.read(), r.headers
                if h.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
            wait = busy(body, h) if busy else None
            reason = "서버가 바쁨(maxlag)"
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                raise Fail(f"HTTP {e.code}")
            wait, reason = wait_from(e.headers, None), f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            wait, reason = None, f"연결 오류({type(e).__name__})"
        else:
            if wait is None:
                return body
        if n == len(RETRY_WAIT):
            raise Fail(f"{reason}: 다시 {len(RETRY_WAIT)}번 해도 안 됨")
        time.sleep(RETRY_WAIT[n] if wait is None else wait)


def fetch_wiki(d):
    revid = int(d["version"].split()[-1])
    url = (f"https://{d['language']}.wikipedia.org/w/api.php?action=parse&oldid={revid}"
           "&prop=text%7Crevid&format=json&formatversion=2&maxlag=5")

    def busy(body, h):
        try:
            e = json.loads(body).get("error")
        except ValueError:
            return None  # JSON이 아니면 바쁜 것이 아니라 이상 응답이다. 아래에서 걸린다.
        return wait_from(h, 5) if e and e.get("code") == "maxlag" else None

    body = get(url, {"User-Agent": UA, "Accept-Encoding": "gzip"}, busy)
    try:
        r = json.loads(body)
    except ValueError:
        raise Fail("JSON이 아닌 응답")
    if "error" in r:
        raise Fail(f"API 오류: {r['error'].get('code')}")
    if r["parse"]["revid"] != revid:
        raise Fail(f"판이 다름: 기대 {revid}, 받은 {r['parse']['revid']}")
    return url, r["parse"]["text"].encode("utf-8"), ".html", d["url"]


def fetch_kto(d):
    svc = "KorService2" if d["language"] == "ko" else "EngService2"
    rest = f"MobileOS=ETC&MobileApp=MultilingualAgentRAG&_type=json&contentId={d['identifier'].split()[-1]}"
    base = f"https://apis.data.go.kr/B551011/{svc}/detailCommon2?"
    body = get(f"{base}serviceKey={urllib.parse.quote(key(), safe='%')}&{rest}", {"User-Agent": UA})
    try:
        r = json.loads(body)["response"]
    except (ValueError, KeyError):
        raise Fail("JSON이 아닌 응답(한도 초과 등)")
    code = r.get("header", {}).get("resultCode")
    if code != "0000":
        raise Fail(f"resultCode: 기대 0000, 받은 {code}")
    items = (r.get("body", {}).get("items") or {}).get("item") or []
    item = items[0] if isinstance(items, list) and items else items
    if not isinstance(item, dict) or not item:
        raise Fail("응답에 항목이 없음")
    want = d["version"].split()[-1]
    if item.get("modifiedtime") != want:
        raise Fail(f"modifiedtime: 기대 {want}, 받은 {item.get('modifiedtime')}")
    if item.get("cpyrhtDivCd") != "Type1":
        raise Fail(f"cpyrhtDivCd: 기대 Type1, 받은 {item.get('cpyrhtDivCd')}")
    return base + rest, body, ".json", d["url"]  # 기록하는 주소에는 serviceKey 부분이 없다


def fetch_portal(d):
    file_id = re.search(r"atchFileId (\S+)", d["identifier"]).group(1)
    url = f"https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId={file_id}&fileDetailSn=1&insertDataPrcus=N"
    body = get(url, {"User-Agent": UA, "Referer": d["url"]})
    try:
        rows = list(csv.reader(io.StringIO(body.decode("cp949"))))
    except UnicodeDecodeError:
        raise Fail("cp949로 풀 수 없음(파일이 아닌 응답)")
    if not rows or len(rows[0]) < 2 or rows[0][-1].strip() != "데이터기준일자":
        raise Fail("첫 줄이 쉼표로 나뉜 머리글이 아니거나 마지막 칸 이름이 데이터기준일자가 아님")
    data = [r for r in rows[1:] if r]
    want = d["version"].split()[-1]
    if not data:
        raise Fail("자료 줄이 없음")
    bad = sorted({r[-1].strip() for r in data if r[-1].strip() != want})
    if bad:
        raise Fail(f"데이터기준일자: 기대 {want}, 다른 값 {bad[:3]}")
    return url, body, ".csv", d["url"]


FETCH = {"wiki": fetch_wiki, "kto": fetch_kto, "portal": fetch_portal}


def load_collected():
    if not COLLECTED.exists():
        return []
    return (yaml.safe_load(COLLECTED.read_text(encoding="utf-8")) or {}).get("documents") or []


def save_collected(docs, rows):
    """documents.yaml의 순서로 쓴다. 목록에 없는 줄은 뒤에 둔다."""
    order = {d["doc_id"]: i for i, d in enumerate(docs)}
    rows = sorted(rows, key=lambda r: order.get(r["doc_id"], len(order)))
    text = yaml.safe_dump({"documents": rows}, allow_unicode=True, sort_keys=False)
    COLLECTED.write_text(HEADER + text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="코퍼스 문서의 원본을 받는다.")
    ap.add_argument("--only", nargs="+", metavar="DOC_ID", help="그 문서만 받는다")
    ap.add_argument("--force", action="store_true", help="이미 받은 문서도 다시 받는다")
    args = ap.parse_args()

    docs = yaml.safe_load(DOCS.read_text(encoding="utf-8"))["documents"]
    if args.only:
        unknown = set(args.only) - {d["doc_id"] for d in docs}
        if unknown:
            sys.exit(f"documents.yaml에 없는 doc_id: {sorted(unknown)}")
    rows = load_collected()
    done = {r["doc_id"]: r for r in rows}
    RAW.mkdir(parents=True, exist_ok=True)

    got, skipped, failed, sent = 0, 0, [], False
    for d in docs:
        doc_id = d["doc_id"]
        if args.only and doc_id not in args.only:
            continue
        kind = doc_id.split("-")[0]
        if kind not in FETCH:
            failed.append((doc_id, "doc_id 앞머리를 모름"))
            print(f"{doc_id}  실패: doc_id 앞머리를 모름")
            continue
        prev = done.get(doc_id)
        if not args.force and prev and (CORPUS / prev.get("raw_file", "")).is_file():
            skipped += 1
            print(f"{doc_id}  건너뜀")
            continue
        if sent:
            time.sleep(GAP)
        sent = True
        try:
            request_url, body, ext, source_url = FETCH[kind](d)
        except Fail as e:
            failed.append((doc_id, str(e)))
            print(f"{doc_id}  실패: {e}")
            continue
        raw_file = f"raw/{doc_id}{ext}"
        (CORPUS / raw_file).write_bytes(body)
        row = {
            "doc_id": doc_id,
            "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "request_url": request_url,
            "source": f"{d['source']} \"{d['title']}\" ({d['version']})",
            "source_url": source_url,
            **LICENSE[kind],
            "raw_file": raw_file,
            "raw_sha256": hashlib.sha256(body).hexdigest(),
        }
        if prev:
            prev.update(row)  # 다른 스크립트가 더한 칸(markdown_file 등)은 그대로 둔다
        else:
            rows.append(row)
            done[doc_id] = row
        save_collected(docs, rows)
        got += 1
        print(f"{doc_id}  받음  {len(body)}바이트")

    print(f"\n받음 {got}, 건너뜀 {skipped}, 실패 {len(failed)}")
    for doc_id, why in failed:
        print(f"  실패 {doc_id}: {why}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
