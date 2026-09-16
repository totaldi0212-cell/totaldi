#!/usr/bin/env python3
"""오늘의 블로그 키워드 후보를 뽑는다.

3단 폴백:
  1) 구글 트렌드 실시간 RSS (geo=KR)          — 네트워크 되면
  2) 네이버 데이터랩 API                       — NAVER_CLIENT_ID/SECRET 있으면
  3) keywords/bank.json 시드 뱅크 + 계절 키워드 — 항상 동작

출력은 마크다운 브리프. 클로드가 이걸 받아 웹 검색으로 최종 키워드를 확정한다.

사용:
  python3 scripts/keyword_radar.py                 # 3개
  python3 scripts/keyword_radar.py --count 5
  python3 scripts/keyword_radar.py --out posts/2026-09-16/_keywords.md
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import random
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANK = ROOT / "keywords" / "bank.json"
USED = ROOT / "keywords" / "used.log"
COOLDOWN_DAYS = 120          # 이 기간 안에 쓴 키워드는 다시 안 뽑는다
TIMEOUT = 6                  # 네트워크가 막혀 있어도 6초 안에 폴백


# --------------------------------------------------------------------------- 실시간 트렌드

def fetch_google_trends(geo="KR"):
    """구글 트렌드 실시간 인기 검색어. 실패하면 빈 리스트."""
    url = f"https://trends.google.com/trending/rss?geo={geo}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            xml = r.read().decode("utf-8", "replace")
    except Exception:
        return []
    import re
    items = re.findall(r"<item>(.*?)</item>", xml, re.S)
    out = []
    for it in items:
        m = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
        if m:
            out.append(m.group(1).strip())
    return out[:20]


def fetch_naver_datalab(keywords):
    """네이버 데이터랩 검색어 트렌드. API 키가 있어야 한다."""
    cid = os.environ.get("NAVER_CLIENT_ID")
    csec = os.environ.get("NAVER_CLIENT_SECRET")
    if not (cid and csec) or not keywords:
        return {}
    today = dt.date.today()
    body = {
        "startDate": (today - dt.timedelta(days=30)).isoformat(),
        "endDate": today.isoformat(),
        "timeUnit": "week",
        "keywordGroups": [{"groupName": k, "keywords": [k]} for k in keywords[:5]],
    }
    try:
        req = urllib.request.Request(
            "https://openapi.naver.com/v1/datalab/search",
            data=json.dumps(body).encode(),
            headers={
                "X-Naver-Client-Id": cid,
                "X-Naver-Client-Secret": csec,
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read().decode())
    except Exception:
        return {}
    scores = {}
    for res in data.get("results", []):
        pts = res.get("data", [])
        scores[res["title"]] = round(sum(p["ratio"] for p in pts) / len(pts), 1) if pts else 0.0
    return scores


# --------------------------------------------------------------------------- 사용 이력

def load_used():
    if not USED.exists():
        return set(), []
    cutoff = dt.date.today() - dt.timedelta(days=COOLDOWN_DAYS)
    recent_kw, rows = set(), []
    for line in USED.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        try:
            d = dt.date.fromisoformat(parts[0])
        except ValueError:
            continue
        rows.append(parts)
        if d >= cutoff:
            recent_kw.add(parts[3])
    return recent_kw, rows


def record(picks):
    USED.parent.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    with USED.open("a", encoding="utf-8") as f:
        for p in picks:
            f.write(f"{today}\t{p['theme']}\t{p['audience']}\t{p['seed']}\n")


# --------------------------------------------------------------------------- 선정

def pick_seeds(bank, count, used_kw, rows):
    """서로 다른 테마에서, 최근 안 쓴 키워드를, 독자층을 섞어 뽑는다."""
    today = dt.date.today()
    rnd = random.Random(today.toordinal())

    # 최근 14일간 쓴 테마는 뒤로 민다
    recent_themes = [r[1] for r in rows[-40:]]
    themes = list(bank["themes"].keys())
    themes.sort(key=lambda t: (recent_themes[::-1].index(t) if t in recent_themes else 999), reverse=True)
    head, tail = themes[: max(4, len(themes) // 2)], themes[max(4, len(themes) // 2):]
    rnd.shuffle(head)
    rnd.shuffle(tail)
    themes = head + tail

    # 독자층 배분: 40~50대 2, 실버 1 (요청 수에 비례해 반복)
    pattern = ["40-50", "60+", "40-50"]
    picks, seen_theme = [], set()

    for i in range(count):
        aud = pattern[i % len(pattern)]
        for t in themes:
            if t in seen_theme:
                continue
            pool = [k for k in bank["themes"][t][aud] if k not in used_kw]
            if not pool:
                continue
            seed = rnd.choice(pool)
            picks.append({
                "theme": t,
                "theme_label": bank["themes"][t]["label"],
                "audience": aud,
                "seed": seed,
            })
            seen_theme.add(t)
            used_kw.add(seed)
            break
    return picks


# --------------------------------------------------------------------------- 출력

def render(picks, trends, datalab, season):
    today = dt.date.today()
    L = []
    L.append(f"# 오늘의 블로그 키워드 브리프 — {today.isoformat()} ({'월화수목금토일'[today.weekday()]})")
    L.append("")

    if trends:
        L.append("## 실시간 구글 트렌드 (KR)")
        L.append(", ".join(trends[:12]))
        L.append("")
        L.append("> 위 중 우리 테마(IT·비즈니스·건강·라이프·자기계발·재테크·리뷰·취미·경제적자유·노후·연금)와")
        L.append("> 엮을 수 있는 게 있으면 아래 시드보다 **우선**한다. 없으면 무시.")
    else:
        L.append("## 실시간 트렌드")
        L.append("_조회 실패 (네트워크 차단 또는 오프라인). 시드 + 웹 검색으로 대체한다._")
    L.append("")

    if datalab:
        L.append("## 네이버 데이터랩 30일 평균 검색 지수")
        for k, v in sorted(datalab.items(), key=lambda x: -x[1]):
            L.append(f"- {k}: {v}")
        L.append("")

    L.append(f"## 계절 앵커 ({today.month}월)")
    L.append(", ".join(season))
    L.append("")

    L.append("## 오늘 쓸 글 3편 — 시드 키워드")
    L.append("")
    L.append("| # | 테마 | 대상 | 시드 키워드 |")
    L.append("|---|------|------|------------|")
    for i, p in enumerate(picks, 1):
        aud = "40~50대" if p["audience"] == "40-50" else "60대 이상"
        L.append(f"| {i} | {p['theme_label']} | {aud} | {p['seed']} |")
    L.append("")
    L.append("> 시드는 **출발점**이지 확정 제목이 아니다.")
    L.append("> 각 시드를 웹 검색으로 검증해 **지금 실제로 검색되는 롱테일 키워드**로 좁힌 뒤 쓸 것.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-record", action="store_true", help="used.log에 기록하지 않음")
    ap.add_argument("--no-network", action="store_true", help="트렌드 조회 건너뜀")
    a = ap.parse_args()

    if not BANK.exists():
        sys.exit(f"키워드 뱅크가 없습니다: {BANK}")
    bank = json.loads(BANK.read_text(encoding="utf-8"))

    used_kw, rows = load_used()
    picks = pick_seeds(bank, a.count, used_kw, rows)
    if not picks:
        sys.exit("뽑을 키워드가 없습니다. keywords/bank.json 을 늘리거나 used.log 를 비우세요.")

    trends = [] if a.no_network else fetch_google_trends()
    datalab = {} if a.no_network else fetch_naver_datalab([p["seed"] for p in picks])
    season = bank["seasonal"].get(f"{dt.date.today().month:02d}", [])

    text = render(picks, trends, datalab, season)

    if a.out:
        p = pathlib.Path(a.out)
        if not p.is_absolute():
            p = ROOT / p
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text + "\n", encoding="utf-8")
        print(f"저장됨: {p.relative_to(ROOT)}")
    print(text)

    if not a.no_record:
        record(picks)


if __name__ == "__main__":
    main()
