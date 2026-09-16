#!/usr/bin/env bash
# gem.sh - 클로드용 GEM(맞춤 AI 역할) 관리 도구
#
#   ./scripts/gem.sh list              등록된 젬 목록
#   ./scripts/gem.sh show <이름>        젬 정의 보기
#   ./scripts/gem.sh new <이름>         템플릿으로 새 젬 만들기
#   ./scripts/gem.sh sync              젬 -> .claude/skills 로 빌드 (자동 호출 활성화)
#   ./scripts/gem.sh remove <이름>      젬과 빌드된 스킬 삭제
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM_DIR="$ROOT/gems"
SKILL_DIR="$ROOT/.claude/skills"
TEMPLATE="$GEM_DIR/_template.gem.md"

die() { echo "오류: $*" >&2; exit 1; }

gem_path() { echo "$GEM_DIR/$1.gem.md"; }

cmd_list() {
  echo "등록된 GEM (${GEM_DIR#$ROOT/}/)"
  echo
  local found=0
  for f in "$GEM_DIR"/*.gem.md; do
    [ -e "$f" ] || continue
    case "$(basename "$f")" in _*) continue ;; esac
    found=1
    python3 - "$f" <<'PY'
import sys, pathlib, re
p = pathlib.Path(sys.argv[1])
text = p.read_text(encoding="utf-8")
m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
meta = {}
if m:
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
name = meta.get("name", p.name.replace(".gem.md", ""))
title = meta.get("title", "")
desc = meta.get("description", "")
if len(desc) > 90:
    desc = desc[:87] + "..."
print(f"  - {name:<18} {title}")
if desc:
    print(f"    {desc}")
PY
  done
  [ "$found" = 1 ] || echo "  (아직 없음 — ./scripts/gem.sh new <이름> 으로 만들어보세요)"
}

cmd_show() {
  local name="${1:-}"; [ -n "$name" ] || die "젬 이름을 입력하세요."
  local f; f="$(gem_path "$name")"
  [ -f "$f" ] || die "'$name' 젬이 없습니다. ./scripts/gem.sh list 로 확인하세요."
  cat "$f"
}

cmd_new() {
  local name="${1:-}"; [ -n "$name" ] || die "젬 이름을 입력하세요. 예) ./scripts/gem.sh new report-writer"
  case "$name" in
    *[!a-z0-9-]*) die "이름은 영소문자/숫자/하이픈만 사용하세요: $name" ;;
  esac
  local f; f="$(gem_path "$name")"
  [ -f "$f" ] && die "'$name' 젬이 이미 있습니다."
  [ -f "$TEMPLATE" ] || die "템플릿이 없습니다: $TEMPLATE"
  sed "s/^name: .*/name: $name/" "$TEMPLATE" > "$f"
  echo "생성됨: ${f#$ROOT/}"
  echo "내용을 채운 뒤 ./scripts/gem.sh sync 를 실행하세요."
}

cmd_sync() {
  python3 - "$GEM_DIR" "$SKILL_DIR" <<'PY'
import sys, pathlib, re, shutil

gem_dir = pathlib.Path(sys.argv[1])
skill_dir = pathlib.Path(sys.argv[2])
skill_dir.mkdir(parents=True, exist_ok=True)

def parse(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise SystemExit(f"오류: {path.name} 에 frontmatter(--- 블록)가 없습니다.")
    meta, body = {}, m.group(2)
    for line in m.group(1).splitlines():
        if line.strip() and ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body

built, stale = [], []

# 이전에 빌드된 gem-* 스킬을 먼저 수집 (삭제된 젬 정리용)
existing = {d.name for d in skill_dir.glob("gem-*") if d.is_dir()}

for f in sorted(gem_dir.glob("*.gem.md")):
    if f.name.startswith("_"):
        continue
    meta, body = parse(f)
    name = meta.get("name") or f.name.replace(".gem.md", "")
    title = meta.get("title", name)
    desc = meta.get("description", "").strip()
    if not desc:
        raise SystemExit(f"오류: {f.name} 의 description 이 비어 있습니다. 언제 이 젬을 써야 하는지 적어주세요.")

    slug = f"gem-{name}"
    out = skill_dir / slug
    out.mkdir(parents=True, exist_ok=True)

    fm = [f"name: {slug}", f"description: {desc}"]
    for key in ("model", "allowed-tools"):
        if meta.get(key):
            fm.append(f"{key}: {meta[key]}")

    header = "---\n" + "\n".join(fm) + "\n---\n\n"
    note = (
        f"> 이 파일은 `gems/{f.name}` 에서 자동 생성되었습니다.\n"
        f"> 직접 고치지 말고 젬 파일을 수정한 뒤 `./scripts/gem.sh sync` 를 실행하세요.\n\n"
        f"# {title}\n\n"
    )
    (out / "SKILL.md").write_text(header + note + body.lstrip("\n"), encoding="utf-8")
    built.append(slug)
    existing.discard(slug)

for slug in sorted(existing):
    shutil.rmtree(skill_dir / slug)
    stale.append(slug)

print(f"빌드 완료: {len(built)}개")
for s in built:
    print(f"  ✓ .claude/skills/{s}/SKILL.md")
for s in stale:
    print(f"  ✗ 제거됨: .claude/skills/{s} (젬 파일 없음)")
PY
}

cmd_remove() {
  local name="${1:-}"; [ -n "$name" ] || die "젬 이름을 입력하세요."
  local f; f="$(gem_path "$name")"
  [ -f "$f" ] || die "'$name' 젬이 없습니다."
  rm -f "$f"
  rm -rf "$SKILL_DIR/gem-$name"
  echo "삭제됨: $name"
}

case "${1:-list}" in
  list)   cmd_list ;;
  show)   shift; cmd_show "$@" ;;
  new)    shift; cmd_new "$@" ;;
  sync)   cmd_sync ;;
  remove) shift; cmd_remove "$@" ;;
  -h|--help|help)
    sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  *) die "알 수 없는 명령: $1 (list | show | new | sync | remove)" ;;
esac
