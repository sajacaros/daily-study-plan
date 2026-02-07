import requests
import datetime
import os
import re

# 설정
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
START_DATE_STR = os.environ.get('START_DATE') # Secrets에서 가져옴
FILE_NAME = "plan.md"

def get_today_plan(day_count):
    if not os.path.exists(FILE_NAME): return None
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Day X 섹션 추출 정규식
    pattern = rf"\*\*Day {day_count}\s*\(.*?\)\*\*(.*?)(?=\*\*Day {day_count + 1}|###|$)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None

def send_to_discord():
    # 시작일 설정 (YYYY-MM-DD 형식)
    start_date = datetime.date.fromisoformat(START_DATE_STR)
    today = datetime.date.today()
    day_count = (today - start_date).days + 1

    plan_text = get_today_plan(day_count)
    
    if plan_text:
        payload = {
            "embeds": [{
                "title": f"📅 DB 설계 학습 - {day_count}일차",
                "description": plan_text,
                "color": 3447003,
                "footer": {"text": "열공하세요! 🔥"}
            }]
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

if __name__ == "__main__":
    send_to_discord()