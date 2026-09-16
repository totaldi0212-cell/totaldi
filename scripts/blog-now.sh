#!/usr/bin/env bash
# 클로드 코드를 "블로그 쓰라"는 명령과 함께 바로 띄운다.
#
#   ./scripts/blog-now.sh              대화창이 열리고 곧바로 3편 작성 시작
#   ./scripts/blog-now.sh --headless   창 없이 백그라운드로 작성만 하고 종료
#
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

if ! command -v claude >/dev/null 2>&1; then
  echo "클로드 코드(claude)가 설치되어 있지 않습니다."
  echo "설치: https://claude.com/claude-code"
  exit 1
fi

if [ "$1" = "--headless" ]; then
  LOG="$ROOT/posts/.last-run.log"
  echo "[$(date '+%F %T')] 무인 모드로 블로그 작성 시작" | tee "$LOG"
  claude -p "/blog-daily" --permission-mode acceptEdits >>"$LOG" 2>&1
  echo "[$(date '+%F %T')] 완료. 결과: posts/$(date +%F)/" | tee -a "$LOG"
  ls -1 "$ROOT/posts/$(date +%F)"/*.md 2>/dev/null | grep -v '_' | tee -a "$LOG"
else
  exec claude "/blog-daily"
fi
