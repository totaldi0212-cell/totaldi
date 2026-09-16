# 블로그 이미지 스타일 헌장

사용자가 제시한 레퍼런스 5장(Nano Banana Pro 생성)을 분석해 규격화한 것.
**모든 블로그 이미지는 이 문서를 따른다.** 예외를 두려면 이 파일을 먼저 고친다.

---

## 한 줄 정의

> **"한국 사람이 실제 생활 공간에서 살아가는 순간을, 연출 없이 찍은 것 같은 사진."**

스톡 사진이 아니다. 광고 컷도 아니다. 누군가의 휴대폰 앨범에 있을 법한 사진이다.

---

## 레퍼런스에서 뽑아낸 공통 규격

### 1. 매체 — 실사 사진

- **photorealistic photograph**. 일러스트, 3D 렌더, 수채화, 벡터 전부 금지.
- 카메라 느낌을 명시한다: 자연광, 얕은 심도, 35mm 또는 50mm 화각.
- 후보정 티가 나면 안 된다. HDR, 과한 비네팅, 뽀샤시 필터 금지.

### 2. 인물 — 평범한 한국인

- **Korean** 을 반드시 명시한다. 안 쓰면 서양인 얼굴이 나온다.
- **모델 같지 않은 얼굴.** "ordinary-looking", "not a fashion model" 을 넣는다.
- 글의 대상 독자와 나이를 맞춘다. 40~50대 글이면 40~50대, 실버 글이면 60~70대.
- 인물이 화면을 꽉 채우지 않는다. **환경이 같이 보이는 미디엄~와이드 샷.**
- 카메라를 안 본다. 서로 보거나, 대상을 보거나, 걷고 있다.

### 3. 공간 — 진짜 한국 장소

레퍼런스가 강한 이유는 배경이 구체적이어서다.

| 레퍼런스 | 공간 |
|---|---|
| 1 | 동네 중국집 — 나무 벽, 벽에 붙은 메뉴판, 에어컨, 뒤쪽 손님들 |
| 2 | 항구도시 전망대 — 산 능선, 아파트 단지, 다리, 바다 |
| 3 | 어촌 한옥 골목 — 기와지붕, 벽에 걸린 어망과 부표 |
| 4 | 횟집 좌식 테이블 — 소주병, 반찬 열몇 접시, 나무 벽 |
| 5 | 해상 케이블카 캐빈 — 유리창 너머 바다 |

**"한국 식당"(X) → "동네 중국집, 나무 벽에 붙은 손글씨 메뉴판, 벽걸이 에어컨"(O)**

생활 소품이 진짜를 만든다: 메뉴판, 달력, 선풍기, 정수기, 화분, 전기 콘센트, 스테인리스 반찬 그릇.

### 4. 조명 — 따뜻하게, 부드럽게

- 실외: **골든아워** (해 뜨고 한 시간, 지기 전 한 시간). 역광 살짝.
- 실내: 창에서 들어오는 자연광 + 형광등. 플래시 금지.
- 색온도는 따뜻한 쪽(앰버/골드). 단, 채도를 과하게 올리지 않는다.

### 5. 구도와 순간

- **연출 안 한 순간을 잡는다.** 웃으며 서로 보기, 젓가락 드는 중, 손가락으로 가리키기, 걸어가는 뒷모습.
- 살짝 어수선한 게 자연스럽다. 테이블 위 접시가 딱 맞게 정렬되면 광고처럼 보인다.
- 배경 인물은 가볍게 블러 처리해 깊이를 만든다.

### 6. 비율

| 용도 | 비율 |
|---|---|
| 본문 삽입 기본 | **16:9** (네이버 본문 폭에 잘 맞음) |
| 대표 이미지 / 썸네일 | **1:1** 또는 4:3 |
| 세로 인물·절차 컷 | 4:5 |

해상도는 **2k**. 4k는 네이버 업로드 시 어차피 리사이즈되므로 크레딧 낭비.

---

## 절대 금지

- ❌ **이미지 안에 글자 넣기** — 한글은 거의 깨져 나오고, 깨진 글자는 AI 티의 1순위다.
- ❌ 서양인 얼굴 (Korean 명시 안 하면 기본값이 서양인)
- ❌ 하얀 배경 + 활짝 웃는 사람 = 전형적인 스톡 사진
- ❌ 과한 보정, 블룸, 렌즈 플레어 떡칠
- ❌ 실존 브랜드 로고, 실존 인물 얼굴
- ❌ 손·손가락이 중심에 크게 오는 구도 (AI가 가장 잘 망치는 부위)

## 납품 전 육안 검수 3초

1. **손가락 개수** — 가장 흔한 사고
2. **글자** — 간판·메뉴판에 깨진 한글이 크게 박혀 있지 않은지
3. **얼굴** — 눈동자 방향이 어긋나거나 이가 이상하지 않은지

하나라도 걸리면 재생성한다. 어설픈 이미지 한 장이 잘 쓴 글 전체를 깎아먹는다.

---

## 타임스탬프 워터마크에 대해

레퍼런스 2·3·5에는 `MON JAN 26 2026 12:22:58 PM KST` 같은 카메라 타임스탬프가 박혀 있다.
"진짜 찍은 사진"처럼 보이게 하는 장치다.

**기본값은 넣지 않는다.** 이유는 두 가지다.

1. 실제로 찍지 않은 사진에 촬영 시각을 박는 건 독자를 속이는 쪽에 가깝다.
2. 이미지 안 글자는 어차피 깨질 위험이 있다.

원하시면 넣을 수 있지만, 그때는 **"AI로 생성한 이미지"임을 글 하단에 한 줄 밝히는 것**을 같이 권한다.
구글 계열 모델은 우측 하단에 자체 워터마크(반짝이 표시)가 들어가는데, 이건 지우지 않는다.

---

## 프롬프트 골격 (이 순서로 쓴다)

```
Photorealistic candid photograph.
[누가] — Korean, [나이대], ordinary-looking, not a fashion model, [옷차림]
[무엇을 하는 중] — [구체적 동작], not looking at camera
[어디서] — [구체적 한국 공간] + [생활 소품 2~3개]
[조명] — [golden hour / warm indoor daylight from window], soft natural light
[카메라] — shot on 35mm, shallow depth of field, background slightly blurred
[톤] — warm amber tones, natural colors, no heavy editing
No text, no logos, no watermark in the image.
```

### 완성 예시 (레퍼런스 1 재현)

```
Photorealistic candid photograph. A Korean couple in their late 30s, ordinary-looking,
not fashion models, wearing plain navy t-shirts, sitting across a wooden table in a small
neighborhood Chinese restaurant in Korea. They are laughing and looking at each other while
holding steel chopsticks, not looking at the camera. Two bowls of jjajangmyeon topped with
fried eggs, a plate of tangsuyuk, and small side dishes of danmuji and pickled onion are on
the table. Wooden wall panels, a handwritten menu board on the wall, a wall-mounted air
conditioner, and other diners slightly blurred in the background. Warm indoor daylight
coming through a window on the left. Shot on 35mm, shallow depth of field, warm amber tones,
natural colors, no heavy editing. No text overlay, no logos.
```

---

## 주제별 소재 힌트

| 테마 | 잘 먹히는 장면 |
|---|---|
| 노후·연금 | 주민센터 창구, 은행 상담 데스크, 식탁에서 서류 펼쳐놓고 계산기 두드리기 |
| 재테크 | 노트북과 가계부, 통장 여러 권, 창가 카페에서 메모하는 손 |
| IT·디지털 | 식탁에서 스마트폰 들여다보는 어르신, 대리점 카운터, 유심 갈아 끼우는 손 |
| 건강·운동 | 동네 하천 산책로, 아파트 단지 헬스장, 병원 대기실 |
| 일상·취미 | 캠핑장 텐트 앞, 창고에 쌓인 장비, 등산로 쉼터 |
| 자기계발 | 새벽 식탁에 펼친 수험서, 도서관 열람실, 출근길 지하철에서 책 |
