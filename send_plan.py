import requests
import datetime
import os
import re

# 환경 변수 설정
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
START_DATE_STR = os.environ.get('START_DATE')
PLAN_FILE = "plan.md"
CHEERUP_FILE = "mission.md"

def get_content_by_day(file_name, day_count):
    """파일에서 Day n에 해당하는 내용을 추출합니다."""
    if not os.path.exists(file_name):
        return None
        
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Day n 포맷 유연성 확보 (plan.md의 시간 포함 포맷 및 cheerup.md 지원)
    pattern = rf"\*\*Day {day_count}(?:\s*\(.*?\))?\*\*(.*?)(?=\*\*Day {day_count + 1}|###|$)"
    match = re.search(pattern, content, re.DOTALL)
    
    return match.group(1).strip() if match else None

def send_to_discord():
    print("--- 파이썬 실행 시작 ---")
    
    # 날짜 계산 (KST 기준)
    curr_utc = datetime.datetime.now(datetime.timezone.utc)
    curr_kst = curr_utc + datetime.timedelta(hours=9)
    today = curr_kst.date()
    
    start_date = datetime.date.fromisoformat(START_DATE_STR)
    day_count = (today - start_date).days + 1
    
    print(f"📌 오늘 날짜: {today} ({day_count}일차)")

    # 내용 가져오기
    plan_text = get_content_by_day(PLAN_FILE, day_count)
    mission_text = get_content_by_day(CHEERUP_FILE, day_count)
    
    if plan_text:
        # 미션 파일이 없거나 내용이 비어있으면 지정하신 기본 문구 사용
        final_mission = mission_text if mission_text else "열공하세요! 🔥"
        
        payload = {
            "embeds": [{
                "title": f"📅 DB 설계 학습 - {day_count}일차",
                "description": plan_text,
                "color": 3447003,
                "fields": [
                    {
                        "name": "🚀 오늘의 미션",
                        "value": final_mission,
                        "inline": False
                    }
                ]
                # footer 부분이 삭제되었습니다.
            }]
        }
        
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"✅ 전송 결과: {res.status_code}")
    else:
        print(f"⚠️ Day {day_count} 학습 내용을 찾을 수 없어 전송을 중단합니다.")

if __name__ == "__main__":
    send_to_discord()
