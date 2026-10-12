#!/bin/sh
# 대화가 압축되기 전에 대화 기록을 백업한다. 실패하면 실패를 알린다.
src="$(jq -r '.transcript_path // empty')"
dir="$HOME/.claude/backups"
if [ -z "$src" ] || [ ! -f "$src" ]; then
  echo '{"systemMessage": "대화 백업 실패: 대화 기록 파일을 찾지 못했습니다."}'
  exit 0
fi
dst="$dir/multilingual-agent-rag-$(date +%Y%m%d-%H%M%S).jsonl"
if mkdir -p "$dir" && cp "$src" "$dst"; then
  echo "{\"systemMessage\": \"대화 백업 완료: $dst\"}"
else
  echo '{"systemMessage": "대화 백업 실패: 복사하지 못했습니다."}'
fi
