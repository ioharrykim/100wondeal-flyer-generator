import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

# ===== 0-1. 특정 마트 키워드 입력 =====
target_keyword = input("전단을 생성할 마트명을 입력하세요 (엔터시 전체 생성): ").strip()
print("")

# ===== 0. 사용자 입력: 포함할 항목 선택 =====
print("✔️ 전단에 포함할 항목을 선택하세요 (y/n)")
include_product_name = input("상품명을 넣으시겠습니까? (y/n): ").lower() == "y"
include_image = input("이미지를 넣으시겠습니까? (y/n): ").lower() == "y"
include_standard = input("규격을 넣으시겠습니까? (y/n): ").lower() == "y"
include_original_price = input("원가를 넣으시겠습니까? (y/n): ").lower() == "y"
include_current_price = input("실판매가를 넣으시겠습니까? (y/n): ").lower() == "y"

# ===== 1. 데이터 로드 및 전처리 =====
EXCEL_PATH = "data/100wondeal.xlsx"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output_html"

df = pd.read_excel(EXCEL_PATH)

# 컬럼명 매핑 (ERP 기반 구조)
df = df.rename(columns={
    '마트': 'mart_name',
    '상품명': 'product_name',
    '이미지': 'product_image_url',
    '규격': 'standard',
    '원가': 'original_price',
    '실판매가': 'current_price'
})

# 결측 처리
df['product_image_url'] = df['product_image_url'].fillna('../assets/default-thumb.png')
# 규격 NaN 처리 + 문자열 변환
df['standard'] = df['standard'].fillna('').astype(str)
df['original_price'] = pd.to_numeric(df['original_price'], errors='coerce').fillna(0)
df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce').fillna(0)

# 템플릿 설정
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
template = env.get_template("flyer_template.html")

# 출력 폴더 생성
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== 2. 마트별 전단 생성 =====
for mart_name, group in df.groupby("mart_name"):
    if target_keyword and target_keyword not in mart_name:
        continue

    group_sorted = group.sort_values(by="original_price", ascending=False)
    top_items = group_sorted.head(10)

    if len(top_items) % 2 != 0:
        top_items = top_items.iloc[:-1]

    product_list = top_items.to_dict(orient="records")

    num_columns = min(max(len(product_list) // 2, 2), 5)
    grid_class = f"columns-{num_columns}"

    rendered_html = template.render(
        products=product_list,
        grid_class=grid_class,
        show_product_name=include_product_name,
        show_image=include_image,
        show_standard=include_standard,
        show_original_price=include_original_price,
        show_current_price=include_current_price,
        mart_name=mart_name  # ✅ 마트명을 title로 전달
    )

    safe_mart_name = "".join(c for c in mart_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    output_path = os.path.join(OUTPUT_DIR, f"{safe_mart_name}.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print(f"✅ Generated: {output_path}")
