---
description: 새 GEM(맞춤 AI 역할)을 대화로 설계해서 만든다
argument-hint: [젬-이름]
---

새 GEM을 만든다. `gem` 스킬(.claude/skills/gem/SKILL.md)의 절차를 따를 것.

요청한 젬 이름: $1

이름이 비어 있으면 어떤 업무용 젬인지 먼저 물어보고 적절한 영소문자 이름을 제안해.
이름이 있으면 스킬에 적힌 4가지 질문을 하고, 답을 받아 `gems/$1.gem.md` 를 채운 뒤
`./scripts/gem.sh sync` 까지 실행해서 마무리해.
