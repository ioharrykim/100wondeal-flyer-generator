import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AIRBRIDGE_API_TOKEN = os.getenv("AIRBRIDGE_API_TOKEN")
AIRBRIDGE_API_URL = "https://api.airbridge.io/v1/tracking-links"

def generate_tracking_link(mart_name: str) -> str:
    """
    마트명을 기반으로 Airbridge 트래킹 링크를 생성하고 shortUrl을 반환합니다.
    """
    today_str = datetime.now().strftime("%y%m%d")  # 예: 250326
    campaign_name = f"{today_str}_{mart_name}_flyer"

    headers = {
        "Authorization": f"Bearer {AIRBRIDGE_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept-Language": "ko"
    }

    data = {
        "channel": "offline",
        "campaignParams": {
            "campaign": campaign_name,
            "ad_group": "presswork",
            "ad_creative": "flyer"
        },
        "isReengagement": "OFF",
        "deeplinkUrl": "qmarket://home",
        "deeplinkOption": {
        "showAlertForInitialDeeplinkingIssue": False  # ✅ 스탑오버 비활성화
    },
        "fallbackPaths": {
            "android": "google-play",
            "ios": "itunes-appstore",
            "desktop": "https://qmarket.online"
        }
    }

    try:
        response = requests.post(AIRBRIDGE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        short_url = response.json()["data"]["trackingLink"]["shortUrl"]
        return short_url
    except Exception as e:
        print(f"[ERROR] 트래킹 링크 생성 실패: {mart_name} → {e}")
        return None

# 테스트 실행 (삭제해도 무방)
if __name__ == "__main__":
    print(generate_tracking_link("큐마켓"))
