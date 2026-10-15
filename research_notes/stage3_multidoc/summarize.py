"""answers/의 후보를 모아 바구니를 문서 이름으로 다시 붙이고, 자매도시 규칙을 대고, AI가 가른 모양을 붙여 sweep_result.json으로 쓴다."""
import json
from pathlib import Path
HERE = Path(__file__).parent
TWO = {"wiki-ko-jeonju", "wiki-ko-cheongju", "wiki-ko-chuncheon", "wiki-ko-cheonan", "kto-ko-jeonju-hanok-village",
       "kto-ko-cheongju-cheongnamdae", "kto-ko-chuncheon-samaksan-cable-car", "kto-ko-cheonan-samgeori-park", "portal-ko-jeonju-population"}
# AI(본 대화의 Claude)가 질문과 두 구절을 읽고 가른 것.
# 모양: 따라가기 = 한 문서의 사실이 다음 문서에서 찾을 대상을 정한다 / 나란히 = 같은 이름으로 두 문서에서 따로 찾는다
# 걸림: 규칙에 걸려 뺀다 / 약함: 고리가 억지스럽다(이유) / 겹침: 다른 후보와 같은 질문
SHAPE = {
 "나란히": ["한화", "이글스", "십이목", "FK리그", "대전지방고용노동청", "대전지방기상청", "충청지방통계청", "NC", "NC백화점", "롯데백화점", "롯데아울렛"],
}
BLOCK = {"저장성": "춘천의 우호도시 사실이다. 청주·춘천·천안은 두 언어 문서의 자매도시 목록이 서로 달라 자매도시 사실을 쓰지 않는다(DECISIONS.md 미정 목록 ⑦)"}
WEAK = {
 "천안아산역": "표에 적힌 역의 순서로 대상을 가리킨다",
 "한국국토정보공사": "열거 순서로 대상을 가리킨다",
 "남청주": "표에서 나들목의 위치(사이에 있는 시설)를 묻는다",
 "남풍세": "표에서 바로 다음 나들목을 묻는다",
 "국민의힘": "정당이 같다는 것만으로 잇는다",
 "KB국민은행": "구단 이름에 은행 이름이 들어 있다는 것으로 잇는다",
 "LG헬로비전": "같은 회사의 다른 지역 방송사로 잇는다",
 "대구광역시": "광주 문서는 '달빛 동맹'이라고 풀어 쓰지 않았다(표 이름만 있음)",
 "경부고속선": "노선 이름만으로 다른 도시의 역 개업일로 넘어간다",
 "후쿠이현": "두 문서의 도시가 서로 다르고 현 이름만 같다",
 "광둥성": "성 이름만 같고 두 도시는 다르다", "후베이성": "성 이름만 같고 두 도시는 다르다",
 "푸젠성": "성 이름만 같고 두 도시는 다르다", "허난성": "성 이름만 같고 두 도시는 다르다",
 "정동영": "두 문서의 사람이 같다는 근거가 이름뿐이다",
}
DUP = {"이글스": "한화", "국립청주박물관": "계유명전씨아미타불비상", "청남대": "이미 재료 목록의 K9", "한화": "이미 재료 목록의 K11", "이글스": "이미 재료 목록의 K11"}
out = []
for af in sorted((HERE / "answers").glob("*.json")):
    for a in json.loads(af.read_text(encoding="utf-8")):
        for c in [a] + (a.get("other_candidates") or []) if a.get("verdict") == "후보" else []:
            docs = [c["bridge"]["doc"], c["target"]["doc"]]
            name = a["name"]
            out.append({
                "batch": af.stem, "name": name, "question": c["question"], "answer": c["answer"],
                "bridge": c["bridge"], "target": c["target"],
                "bucket_by_docs": "두 언어 도시" if any(d in TWO for d in docs) else "한국어 도시",
                "bucket_by_agent": c.get("bucket"),
                "shape": "나란히" if name in SHAPE["나란히"] else "따라가기",
                "blocked": BLOCK.get(name), "weak": WEAK.get(name), "dup": DUP.get(name),
            })
(HERE / "sweep_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
print("후보", len(out), "| 바구니를 다시 붙여 바뀐 것", sum(o["bucket_by_docs"] != o["bucket_by_agent"] for o in out))
ok = [o for o in out if not o["blocked"] and not o["dup"]]
print("걸림·겹침 뺀 것", len(ok), Counter((o["shape"], "약함" if o["weak"] else "보통", o["bucket_by_docs"]) for o in ok))
for o in ok:
    if o["shape"] == "따라가기" and not o["weak"]: print(" ", o["name"], "|", o["bucket_by_docs"], "|", o["question"][:70])
