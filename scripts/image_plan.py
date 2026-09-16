#!/usr/bin/env python3
"""원고의 [사진] 자리를 뽑아 이미지 프롬프트 시트 뼈대를 만든다.

클로드가 이 뼈대의 PROMPT 칸을 채우고(images/STYLE.md 규격), 크레딧이 있으면
그대로 생성까지 간다. 크레딧이 없으면 시트만 남아 제미나이 등에 붙여넣으면 된다.

  python3 scripts/image_plan.py posts/2026-09-16/01-*.md
  python3 scripts/image_plan.py posts/2026-09-16/*.md --check   # 자리 개수만 점검
"""
import argparse, pathlib, re, sys

SLOT_RE = re.compile(r"^\[사진\]\s*(.*)$", re.M)


def parse_post(path):
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    meta = dict(re.findall(r"^(\S+?):\s*(.+)$", raw.split("---")[1], re.M)) if raw.startswith("---") else {}
    title_m = re.search(r"^제목:\s*(.+)$", raw, re.M)
    title = title_m.group(1).strip() if title_m else pathlib.Path(path).stem

    # 본문만 (출처/점검 블록 제외)
    body = re.split(r"\n---\n\[출처\]", raw)[0]
    lines = body.split("\n")

    slots, heading = [], "(도입부)"
    for i, line in enumerate(lines):
        if line.startswith("## "):
            heading = line[3:].strip()
        m = SLOT_RE.match(line)
        if m:
            # 앞뒤 본문 문단을 문맥으로 붙인다
            before = next((l.strip() for l in reversed(lines[:i]) if l.strip() and not l.startswith(("#", "[", "-", "|"))), "")
            after = next((l.strip() for l in lines[i + 1:] if l.strip() and not l.startswith(("#", "[", "-", "|"))), "")
            slots.append({"n": len(slots) + 1, "heading": heading, "note": m.group(1).strip(),
                          "before": before[:120], "after": after[:120]})
    return meta, title, slots


def render(path, meta, title, slots):
    aud = meta.get("대상", "40~50대")
    age = "60대 후반~70대 초반" if "60" in aud else "40대 후반~50대 초반"
    stem = pathlib.Path(path).stem
    L = [f"# 이미지 프롬프트 시트 — {title}", "",
         f"- 원고: `{path}`",
         f"- 대상 독자: {aud} → 등장인물 나이대 **{age}**",
         f"- 규격: `images/STYLE.md` (실사 / 한국인 / 생활공간 / 골든아워 / 글자 없음)",
         f"- 모델: `nano_banana_pro`, 비율 16:9, 해상도 2k",
         f"- 저장 위치: `posts/{meta.get('날짜','')}/images/{stem}-01.png` … ", "",
         "---", ""]
    for s in slots:
        L += [f"## {s['n']}번 — {s['heading']}", "",
              f"**원고 메모**: {s['note'] or '(없음)'}",
              f"**앞 문맥**: {s['before'] or '—'}",
              f"**뒤 문맥**: {s['after'] or '—'}", "",
              "**PROMPT** (영문, STYLE.md 골격 순서대로 — 클로드가 채움)",
              "```", "(미작성)", "```", "",
              f"**ALT 텍스트** (네이버 업로드용, 한글 한 줄): (미작성)",
              f"**파일명**: `{stem}-{s['n']:02d}.png`", "", "---", ""]
    if not slots:
        L.append("⚠️ 이 원고에는 [사진] 자리가 없습니다. 3~5곳을 먼저 지정하세요.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--check", action="store_true", help="자리 개수만 점검하고 파일은 안 만듦")
    a = ap.parse_args()

    ok = True
    for f in a.files:
        if pathlib.Path(f).name.startswith("_"):
            continue
        meta, title, slots = parse_post(f)
        n = len(slots)
        good = 3 <= n <= 5
        ok = ok and good
        print(f"{'✅' if good else '❌'} {pathlib.Path(f).name}: [사진] 자리 {n}곳 (목표 3~5)")
        for s in slots:
            print(f"     {s['n']}. [{s['heading']}] {s['note'][:40] or '(설명 없음)'}")
        if not a.check:
            out = pathlib.Path(f).parent / f"_images-{pathlib.Path(f).stem}.md"
            out.write_text(render(f, meta, title, slots) + "\n", encoding="utf-8")
            print(f"     → 시트: {out}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
