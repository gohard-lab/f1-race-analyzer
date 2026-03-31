import streamlit as st
from tracker_web import log_app_usage

log_app_usage("f1_telemetry_web", "f1_opened")

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


@st.dialog("⭐ Support Polymath Developer Automation Tool")
def show_star_popup_web():
    # 팝업 노출 트래커 기록
    log_app_usage("f1_telemetry_web", "star_prompt_displayed", details={"ui": "streamlit_dialog"})
    
    st.warning(
        "💡 유용하게 사용하셨나요? 소스코드만 날름 가져가는 분들이 많습니다. "
        "개발자의 땀과 노력에 대한 최소한의 예의로 깃허브 Star⭐를 부탁드립니다!\n\n"
        "Did you find this useful? Please show some basic courtesy for the developer's hard work by leaving a GitHub Star⭐."
    )
    
    # 깃허브 Star 유도 버튼
    st.link_button("👉 깃허브로 이동하여 Star 누르기", "https://github.com/gohard-lab/f1-race-analyzer")

show_star_popup_web()
