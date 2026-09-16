#!/usr/bin/env python3
"""blog-writer 젬의 규칙을 기계적으로 검사한다.

  python3 scripts/style_check.py posts/2026-09-16/01-*.md
  python3 scripts/style_check.py --audience 60+ 파일.md
"""
import argparse, pathlib, re, statistics, sys

# 독자층별 리듬 기준. 실버는 문장을 짧게 끊는 게 원칙이므로
# "긴 문장" 기준과 편차 목표를 따로 둔다. (35자 상한과 충돌하지 않게)
PROFILE = {
    "40-50": dict(short_max=15, short_pct=20, long_min=40, long_pct=10,
                  avg=(22, 45), sd=12, cap=None),
    "60+":   dict(short_max=12, short_pct=22, long_min=25, long_pct=12,
                  avg=(15, 28), sd=7,  cap=35),
}

BLACKLIST = [
    "알아보겠습니다", "알아보도록", "소개해 드리려", "소개해드리려",
    "바쁘신 분들을 위해", "결론적으로", "종합해 보면", "종합해보면",
    "요약하자면", "도움이 되셨길", "하시기 바랍니다", "읽어주셔서 감사",
    "라고 할 수 있습니다", "인 것 같습니다", "라 할 수 있습니다",
]
HEDGE = ["매우", "굉장히", "대단히"]


def strip_meta(text):
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)      # frontmatter
    text = re.split(r"\n#해시태그|\n#\S+ #", text)[0]                # 해시태그 이후
    text = re.split(r"\n---\n\[출처\]", text)[0]
    text = re.sub(r"^\[사진\].*$", "", text, flags=re.M)
    text = re.sub(r"\[여기에[^\]]*\]", "", text)
    text = re.sub(r"^제목:.*$", "", text, flags=re.M)
    text = re.sub(r"^#+ .*$", "", text, flags=re.M)                # 소제목 제외
    return text


def sentences(body):
    # 구두점 기준으로만 자른다. "장비를 다 갖추고"의 '다'처럼
    # 어미로 보이는 부사에서 잘못 쪼개지는 것을 막기 위함.
    parts = re.split(r"(?<=[.!?…])\s+|\n+", body)
    out = []
    for s in parts:
        s = re.sub(r"^[-*]\s*", "", s.strip())   # 불릿 기호 제거
        if len(s) > 1:
            out.append(s)
    return out


def ending(s):
    s = s.rstrip(" .!?…")
    return s[-2:] if len(s) >= 2 else s


def check(path, audience):
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    body = strip_meta(raw)
    chars_ns = len(re.sub(r"\s", "", body))
    chars = len(body.strip())
    sents = sentences(body)
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]

    P = PROFILE[audience]
    lens = [len(s) for s in sents] or [0]
    short_pct = round(100 * sum(1 for x in lens if x < P["short_max"]) / len(lens), 1)
    long_pct = round(100 * sum(1 for x in lens if x >= P["long_min"]) / len(lens), 1)
    avg = round(sum(lens) / len(lens), 1)
    sd = round(statistics.pstdev(lens), 1) if len(lens) > 1 else 0.0
    one_line_paras = [p for p in paras if len(sentences(p)) == 1]

    # 어미 단조로움: 한국어 존댓말은 "-니다"가 많을 수밖에 없다.
    # 3연속이 아니라 (a) 5연속 (b) 어미 종류 부족 으로 본다.
    ends = [ending(s) for s in sents]
    streaks, run = [], 1
    for i in range(1, len(ends)):
        run = run + 1 if ends[i] == ends[i - 1] else 1
        if run == 5:
            streaks.append(sents[i][:24])
    distinct_ends = len({e for e in ends})

    hits = [w for w in BLACKLIST if w in raw]
    hedges = [w for w in HEDGE if w in body]
    numbers = re.findall(r"\d[\d,.]*\s*(?:원|만원|년|월|일|시간|분|개|번|퍼센트|%|℃|도|GB|kg)", body)
    reader = len(re.findall(r"여러분", body))
    exp_slots = len(re.findall(r"\[여기에 본인 경험", raw))
    photo_slots = len(re.findall(r"^\[사진\]", raw, re.M))

    # 실버 대상이면 문장 35자 상한
    over_cap = [s for s in sents if P["cap"] and len(s) > P["cap"]]

    ok = True
    def line(good, label, val):
        nonlocal ok
        if not good: ok = False
        print(f"  {'✅' if good else '❌'} {label}: {val}")

    print(f"\n── {pathlib.Path(path).name}  [{audience}]  ({chars}자 / 문장 {len(sents)}개 / 문단 {len(paras)}개)")
    line(1500 <= chars <= 2600, "본문 분량", f"{chars}자 (공백제외 {chars_ns}자) / 목표 1,500~2,500")
    line(short_pct >= P["short_pct"], f"짧은 문장({P['short_max']}자 미만)", f"{short_pct}% (목표 {P['short_pct']}%↑)")
    line(long_pct >= P["long_pct"], f"긴 문장({P['long_min']}자 이상)", f"{long_pct}% (목표 {P['long_pct']}%↑)")
    line(P["avg"][0] <= avg <= P["avg"][1], "평균 문장 길이", f"{avg}자 (목표 {P['avg'][0]}~{P['avg'][1]})")
    line(sd >= P["sd"], "문장 길이 편차(리듬)", f"표준편차 {sd} (목표 {P['sd']}↑)")
    line(len(one_line_paras) >= 2, "1문장 문단", f"{len(one_line_paras)}개 (목표 2개↑)")
    line(not streaks, "같은 어미 5연속", "없음" if not streaks else f"{len(streaks)}건 → {streaks}")
    line(distinct_ends >= 8, "어미 종류", f"{distinct_ends}가지 (목표 8가지↑)")
    line(not hits, "블랙리스트 표현", "0건" if not hits else f"{hits}")
    line(not hedges, "과장 부사", "0건" if not hedges else f"{hedges}")
    line(len(numbers) >= 5, "구체적 수치", f"{len(numbers)}개 (목표 5개↑)")
    line(reader <= 2, "'여러분' 사용", f"{reader}회 (상한 2)")
    line(1 <= exp_slots <= 2, "본인 경험 자리", f"{exp_slots}곳 (목표 1~2)")
    line(3 <= photo_slots <= 5, "[사진] 자리", f"{photo_slots}곳 (목표 3~5)")
    if P["cap"]:
        line(not over_cap, f"문장 {P['cap']}자 상한", "통과" if not over_cap else f"{len(over_cap)}문장 초과 → {[s[:22] for s in over_cap[:3]]}")
    return ok, dict(chars=chars, short_pct=short_pct, avg=avg, sd=sd, one=len(one_line_paras),
                    black=len(hits), nums=len(numbers), reader=reader, slots=exp_slots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--audience", default="40-50", choices=["40-50", "60+"])
    a = ap.parse_args()
    allok = True
    files = [f for f in a.files if not pathlib.Path(f).name.startswith("_")]
    for f in files:
        aud = a.audience
        try:
            head = pathlib.Path(f).read_text(encoding="utf-8")[:400]
            if "대상: 60대" in head: aud = "60+"
        except Exception:
            pass
        ok, _ = check(f, aud)
        allok = allok and ok
    if not files:
        print("검사할 원고가 없습니다."); sys.exit(0)
    print(f"\n{'전체 통과 ✅' if allok else '보완 필요 ❌'}")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
