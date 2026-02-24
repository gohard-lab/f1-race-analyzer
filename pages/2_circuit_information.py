import streamlit as st
import fastf1
import datetime

st.set_page_config(page_title="서킷 정보", page_icon="📅")
st.title("📅 시즌별 서킷 및 일정 정보")

current_year = datetime.datetime.now().year
year = st.sidebar.selectbox("연도 선택", range(current_year, 2017, -1))

with st.spinner(f"{year}년도 F1 경기 일정을 불러오는 중입니다..."):
    schedule = fastf1.get_event_schedule(year)
    
    # 1. 일정 표 보여주기
    st.dataframe(
        schedule[['RoundNumber', 'Country', 'Location', 'EventName', 'EventDate']],
        use_container_width=True
    )

    st.markdown("---")
    
    # 2. 서킷 맵으로 이동하는 특별 구역 만들기
    st.subheader("🗺️ 서킷 트랙 지도로 보기")
    st.write("위 일정표에서 확인한 대회의 트랙 모양을 확인하고 싶다면 아래에서 선택 후 이동하세요.")
    
    # 대회를 선택하는 콤보박스
    selected_event = st.selectbox("지도를 볼 대회를 선택하세요", schedule['EventName'].tolist())
    
    # 이동 버튼
    if st.button(f"🚀 '{selected_event}' 서킷 맵 보러가기"):
        # 핵심: 4번 페이지로 이동하기 전에, 현재 선택한 연도와 대회를 Streamlit의 '기억 장치(session_state)'에 저장합니다.
        st.session_state['selected_year'] = year
        st.session_state['selected_event'] = selected_event
        
        # 4번 페이지로 강제 순간이동!
        st.switch_page("pages/4_circuit_map.py")        