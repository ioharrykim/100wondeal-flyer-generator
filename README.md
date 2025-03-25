# 🧾 100WONDEAL 전단 자동 생성 툴

마케팅/디자인 팀을 위한 **마트 전단 이미지 자동화 툴**입니다.  
Excel 파일 기반으로 HTML 전단을 자동 생성하고, 이미지(PNG)로 저장할 수 있습니다.

---

## 📁 프로젝트 구조

```
100wondeal/
├── assets/              # 로고, QR 등 이미지 리소스
├── data/                # Excel 업로드용 폴더 (100wondeal.xlsx)
├── output_html/         # 마트별 HTML 전단 저장
├── output_image/        # PNG 이미지 저장
├── templates/           # Jinja 기반 HTML 템플릿
├── generate.py          # HTML 생성 Python 스크립트
├── render.js            # PNG 생성 Puppeteer 스크립트
```

---

## 🚀 사용법

### 1. 엑셀 파일 업로드

`data/100wondeal.xlsx`에 최신 마트 데이터를 업로드합니다.

필요한 컬럼은 아래와 같습니다:

| 컬럼명     | 설명                     |
|------------|--------------------------|
| 마트       | 마트명 (예: 큐마켓 부평점) |
| 상품명     | 전단에 노출될 상품 이름     |
| 이미지     | 상품 이미지 URL           |
| 규격       | 상품 규격 (예: 500g, 2L 등) |
| 원가       | 정가                     |
| 실판매가   | 할인 적용 가격             |

---

### 2. HTML 전단 생성

```bash
python3 generate.py
```

실행 후:
- 포함 항목 선택 (상품명/이미지 등)
- 특정 마트 필터 입력 (예: `벨몽드마트` 입력 시 관련 지점만 생성)

📂 결과는 `output_html/` 폴더에 `.html`로 저장됩니다.

---

### 3. PNG 이미지 생성

```bash
node render.js
```

브라우저 기반 Puppeteer로 각 `.html`을 이미지로 변환  
📂 결과는 `output_image/` 폴더에 `.png`로 저장됩니다.

---

## ✏️ HTML 직접 수정 기능

- 생성된 HTML은 Chrome 브라우저로 열기만 하면 텍스트 직접 수정 가능  
- `contenteditable` 속성 적용 (상품명, 가격, 문구 등)  
- 우측 상단 `저장하기` 버튼 클릭 시 → 수정된 `.html` 재다운로드 가능

---

## ✅ 기능 요약

- Excel 기반 마트 전단 자동 생성
- HTML 전단 + PNG 이미지 생성
- 최대 10개 상품 자동 정렬 (짝수 유지)
- 항목 선택형 전단 제작
- 마트명 키워드 검색 지원
- HTML 직접 수정 및 저장 기능 포함
- 고해상도 PNG 추출

---

## ⚙️ 필요 의존성

- **Python 3.x**
  - `pandas`, `jinja2`, `openpyxl`
- **Node.js**
  - `puppeteer`

### 설치 예시

```bash
# Python
pip install pandas jinja2 openpyxl

# Node.js
npm install puppeteer
```

---

## ✨ 만든 사람

**김현민 (Hyunmin Kim)**  
브랜드/콘텐츠 디자이너 @ 애즈위메이크
