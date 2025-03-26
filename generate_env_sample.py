import os
from shutil import copyfile

env_path = ".env"
sample_path = ".env.sample"

if os.path.exists(env_path):
    copyfile(env_path, sample_path)
    print(f"✅ '{env_path}' 파일을 기반으로 '{sample_path}' 파일을 생성했습니다.")
else:
    with open(sample_path, "w", encoding="utf-8") as f:
        f.write("AIRBRIDGE_API_TOKEN=your_airbridge_token_here\n")
    print(f"⚠️ '{env_path}' 파일이 없어 기본 템플릿으로 '{sample_path}' 파일을 생성했습니다.")
