"""조사용: 희토류 원소 코퍼스의 마크다운 표를 원문 HTML 표와 짝지어 구조를 있는 그대로 적는다. 분류하지 않는다.

실행: .venv/bin/python research_notes/stage2_table_shapes_rare_earth/extract.py
결과: 같은 폴더의 tables.json, tables_dump.md
구조를 읽는 코드는 도시 코퍼스 때의 research_notes/stage2_table_shapes/extract.py를 그대로 불러 쓴다(어느 코퍼스에나 쓰는 부분).
그 파일의 main은 부르지 않는다(도시 코퍼스의 결과 파일을 덮어쓰지 않기 위해서다).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "stage2_table_shapes"))
import extract as ex  # noqa: E402


def main():
    tables, per_doc, kto_tables, problems = ex.run()
    (HERE / "tables.json").write_text(json.dumps(tables, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "tables_dump.md").write_text(ex.dump(tables, per_doc, kto_tables, problems), encoding="utf-8")
    print(f"표 호출 {len(tables)}개, 문제 {problems or '없음'}")


if __name__ == "__main__":
    main()
