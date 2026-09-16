---
description: 등록된 GEM(맞춤 AI 역할) 목록을 보여주고 관리 메뉴를 안내한다
---

`./scripts/gem.sh list` 를 실행해 등록된 젬 목록을 보여줘.

그 다음 아래를 한 줄씩 간단히 안내해:
- 새로 만들기: `/gem-new <이름>` 또는 "젬 만들어줘"
- 고치기: `gems/<이름>.gem.md` 수정 후 `./scripts/gem.sh sync`
- 지우기: `./scripts/gem.sh remove <이름>`

이미 만들어진 젬은 별도 명령 없이도 대화 내용에 맞춰 자동으로 호출된다는 점을 알려줘.
