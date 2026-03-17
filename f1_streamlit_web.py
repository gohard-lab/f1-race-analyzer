import streamlit as st
from tracker import log_app_usage



from supabase import create_client

# st.write("🔍 [디버그] RLS 완벽 돌파 테스트 중...")
# try:
#     url = "https://gkzbiacodysnrzbpvavm.supabase.co" # (진짜 주소)
#     key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdremJpYWNvZHlzbnJ6YnB2YXZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM1NzE2MTgsImV4cCI6MjA4OTE0NzYxOH0.Lv5uVeNZOyo21tgyl2jjGcESoLl_iQTJYp4jdCwuYDU" # (진짜 키)
#     client = create_client(url, key)
    
#     # 👇 끝에 returning='minimal'을 추가했습니다!
#     res = client.table('usage_logs').insert({"app_name": "f1_test_cheiri", "action": "test_직접연결"}, returning='minimal').execute()
    
#     st.success("✅ DB에 데이터 꽂힘! 문지기 통과 완료!")
# except Exception as e:
#     st.error(f"❌ DB가 뱉어낸 진짜 에러: {e}")

log_app_usage("f1_telemetry_cheiri", "f1_telemetry_started")





st.set_page_config(page_title="F1 데이터 대시보드", page_icon="🏎️", layout="wide")

st.title("🏎️ F1 데이터 분석 대시보드에 오신 것을 환영합니다!")
st.markdown("""
---
이 대시보드는 F1 경기 데이터를 다각도로 분석하기 위해 제작되었습니다.  
마치 피트월(Pit Wall)의 엔지니어처럼 데이터를 탐색해 보세요!

👈 **왼쪽 사이드바의 메뉴를 클릭해서 원하는 분석 페이지로 이동할 수 있습니다.**

* 🏎️ **1_텔레메트리_비교:** 두 드라이버의 코너링, 브레이킹, 스로틀 전개량을 그래프로 비교합니다.
* 🗺️ **2_서킷_정보:** 시즌별 F1 그랑프리 개최 일정과 서킷 기본 정보를 확인합니다.
* 🏆 **3_드라이버_순위:** 특정 그랑프리(본선 레이스)의 최종 순위와 획득 포인트를 확인합니다.
""")