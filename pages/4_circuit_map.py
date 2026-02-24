import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="서킷 맵", page_icon="🗺️")
st.title("🗺️ F1 서킷 맵 (Track Map)")
st.write("선택한 그랑프리의 트랙 레이아웃을 확인합니다.")

# 💡 핵심: 2번 페이지에서 넘어온 데이터(session_state)가 있는지 확인하고 기본값으로 설정
current_year = datetime.datetime.now().year
default_year = st.session_state.get('selected_year', current_year)
default_event = st.session_state.get('selected_event', None)

# 조건바(사이드바) 설정
year = st.sidebar.selectbox("연도 선택", range(current_year, 2017, -1), index=current_year - default_year if default_year <= current_year else 0)

# 선택한 연도의 일정 불러오기
@st.cache_data
def load_schedule(year):
    return fastf1.get_event_schedule(year)

schedule = load_schedule(year)
events = schedule['EventName'].tolist()

# 2번 페이지에서 넘어온 서킷이 이번 연도 목록에 있다면 그 서킷을 기본으로 선택
try:
    event_idx = events.index(default_event) if default_event in events else 0
except:
    event_idx = 0

event = st.sidebar.selectbox("대회 (Event) 선택", events, index=event_idx)

# 맵 그리기 버튼
if st.button("🏁 서킷 맵 그리기"):
    with st.spinner(f"{year} {event} 서킷 데이터를 불러와 지도를 그리는 중입니다... (약 10~20초 소요)"):
        try:
            # 트랙의 형태를 가장 잘 보여주는 퀄리파잉(Q) 세션의 가장 빠른 랩 데이터를 가져옵니다.
            session = fastf1.get_session(year, event, 'Q')
            session.load(telemetry=True, weather=False, messages=False)
            
            fastest_lap = session.laps.pick_fastest()
            pos = fastest_lap.get_pos_data()

            # 그래프로 서킷 맵 그리기 (검은 배경에 흰색 트랙)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(pos['X'], pos['Y'], color='white', linewidth=3) # 트랙 선 그리기
            
            # 배경 및 축 디자인 설정
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')
            ax.axis('off') # x, y축 숫자 숨기기 (깔끔한 지도처럼 보이게)
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error("데이터를 불러오지 못했습니다. 아직 경기가 열리지 않았거나 FastF1 서버에 데이터가 없습니다.")