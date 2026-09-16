#!/usr/bin/env bash
# 세션 시작 훅. 오늘 블로그 글이 아직 없으면 키워드를 뽑아 클로드에게 작업을 지시한다.
# 어떤 경우에도 세션을 깨뜨리지 않는다 (항상 exit 0).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" 2>/dev/null || exit 0

AUTO_MODE=auto
POSTS_PER_DAY=3
PLATFORM=naver
[ -f "$ROOT/blog.config" ] && . "$ROOT/blog.config" 2>/dev/null

[ "$AUTO_MODE" = "off" ] && exit 0

TODAY="$(date +%F)"
DIR="$ROOT/posts/$TODAY"
KW="$DIR/_keywords.md"

# 오늘 쓴 글 세기 (_로 시작하는 파일 제외)
written=0
if [ -d "$DIR" ]; then
  written=$(find "$DIR" -maxdepth 1 -name '*.md' ! -name '_*' 2>/dev/null | wc -l | tr -d ' ')
fi

# 할당량 채웠으면 조용히 종료
[ "$written" -ge "$POSTS_PER_DAY" ] && exit 0

# 키워드 브리프는 하루 한 번만 생성 (같은 날 재접속 시 재사용)
if [ ! -f "$KW" ]; then
  mkdir -p "$DIR"
  python3 "$ROOT/scripts/keyword_radar.py" --count "$POSTS_PER_DAY" --out "$KW" >/dev/null 2>&1 \
    || { echo "[블로그 자동화] 키워드 생성 실패 — scripts/keyword_radar.py 를 직접 실행해보세요."; exit 0; }
fi

remain=$((POSTS_PER_DAY - written))

cat <<MSG
════════════════════════════════════════════════════════
📝 블로그 자동화 — $TODAY (오늘 $written/$POSTS_PER_DAY 편 완료, $remain 편 남음)
════════════════════════════════════════════════════════

키워드 브리프: posts/$TODAY/_keywords.md
플랫폼: $PLATFORM   모드: $AUTO_MODE

MSG

if [ "$AUTO_MODE" = "auto" ]; then
  cat <<MSG
[클로드에게 지시]
지금 바로 blog-autopilot 스킬(.claude/skills/blog-autopilot/SKILL.md)의 절차를 따라
남은 $remain 편을 작성하라. 사용자에게 시작 여부를 되묻지 말 것.
글쓰기 규칙은 gem-blog-writer 스킬을 그대로 적용한다.
MSG
else
  cat <<MSG
[클로드에게 지시]
posts/$TODAY/_keywords.md 의 키워드 3개를 사용자에게 보여주고,
어떤 것부터 쓸지 물어본 뒤 blog-autopilot 스킬 절차로 작성하라.
MSG
fi
exit 0
