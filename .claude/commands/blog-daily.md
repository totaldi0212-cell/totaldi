---
description: 오늘 몫의 블로그 글(기본 3편)을 키워드 선정부터 자동으로 작성한다
---

`blog-autopilot` 스킬(.claude/skills/blog-autopilot/SKILL.md)의 1~7단계를 지금 실행해.

먼저 오늘 진행 상황부터 확인해:

```bash
ls posts/$(date +%F)/ 2>/dev/null
```

- 아직 키워드 브리프가 없으면 `python3 scripts/keyword_radar.py --count 3 --out posts/$(date +%F)/_keywords.md` 로 생성
- 이미 쓴 글이 있으면 **남은 편수만** 작성
- 시작할지 되묻지 말고 바로 진행

문체 규칙은 `gem-blog-writer` 스킬을 그대로 따른다.
