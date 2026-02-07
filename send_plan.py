print("--- 파이썬 실행 시작 ---")

import requests
import datetime
import os
import re

DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
START_DATE_STR = os.environ.get('START_DATE')
FILE_NAME = "plan.md"

def get_today_plan(day_count):
    if not os.path.exists(FILE_NAME):
        print(f"❌ 파일을 찾을 수 없음: {FILE_NAME}")
        return None
    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = rf"\*\*Day {day_count}\s*\(.*?\)\*\*(.*?)(?=\*\*Day {day_count + 1}|###|$)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None

def send_to_discord():
    print(f"--- 파이썬 실행 시작 ---")
    print(f"📌 설정된 시작일: {START_DATE_STR}")
    
    # 한국 시간(KST, UTC+9) 계산
    curr_utc = datetime.datetime.now(datetime.timezone.utc)
    curr_kst = curr_utc + datetime.timedelta(hours=9)
    today = curr_kst.date() # 한국의 오늘 날짜
    
    print(f"📌 한국 기준 오늘 날짜: {today}")
    
    start_date = datetime.date.fromisoformat(START_DATE_STR)
    day_count = (today - start_date).days + 1
    print(f"📌 오늘 계산된 일차: {day_count}일차")

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
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"✅ 전송 결과: {res.status_code}")
    else:
        print(f"⚠️ Day {day_count}에 해당하는 내용을 plan.md에서 찾지 못했습니다.")

if __name__ == "__main__":
    send_to_discord()