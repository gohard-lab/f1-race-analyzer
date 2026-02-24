import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import os
import datetime

#
plt.style.use('dark_background')

if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

st.set_page_config(page_title="텔레메트리 비교", layout="wide")
st.title("🏎️ F1 드라이버 텔레메트리 비교")

# 1. 오늘 날짜 기준으로 '연도'만 숫자(예: 2026)로 쏙 빼옵니다.
current_year = datetime.datetime.now().year

# 2. range에 적용: 현재 연도부터 2018년까지 역순(-1)으로 목록을 만듭니다.
# (range는 두 번째 숫자 바로 앞까지만 만들어주기 때문에, 2018년까지 보려면 2017로 적어야 합니다)
YEARS = range(current_year, 2017, -1)
# YEARS = [2024, 2023, 2022, 2021]
CIRCUITS = ['Bahrain', 'Saudi Arabia', 'Australia', 'Japan', 'China', 'Miami', 'Emilia Romagna', 'Monaco', 'Canada', 'Spain', 'Austria', 'Great Britain', 'Hungary', 'Belgium', 'Netherlands', 'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico', 'Sao Paulo', 'Las Vegas', 'Qatar', 'Abu Dhabi']
SESSIONS = ['FP1', 'FP2', 'FP3', 'Q', 'Sprint', 'R']
DRIVERS = ['VER', 'PER', 'HAM', 'RUS', 'LEC', 'SAI', 'NOR', 'PIA', 'ALO', 'STR', 'GAS', 'OCO', 'ALB', 'SAR', 'TSU', 'RIC', 'BOT', 'ZHO', 'MAG', 'HUL']

st.sidebar.header("📊 조회 조건")
year = st.sidebar.selectbox("📅 연도", YEARS)
gp = st.sidebar.selectbox("🏁 그랑프리", CIRCUITS, index=0)
session_type = st.sidebar.selectbox("⏱️ 세션", SESSIONS, index=3)

st.sidebar.subheader("🏎️ 드라이버 선택")
driver1 = st.sidebar.selectbox("드라이버 1", DRIVERS, index=0)
driver2 = st.sidebar.selectbox("드라이버 2", DRIVERS, index=2)

if st.sidebar.button("비교하기"):
    try:
        with st.spinner('데이터를 불러오는 중...'):
            session = fastf1.get_session(year, gp, session_type)
            session.load()
            lap_d1 = session.laps.pick_driver(driver1).pick_fastest()
            lap_d2 = session.laps.pick_driver(driver2).pick_fastest()
            tel_d1 = lap_d1.get_telemetry()
            tel_d2 = lap_d2.get_telemetry()

            st.subheader(f"🏁 {driver1} vs {driver2} - {year} {gp} ({session_type})")
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
            fig.patch.set_facecolor('#121212') 

            ax1.plot(tel_d1['Distance'], tel_d1['Speed'], color='cyan', label=driver1, linewidth=2)
            ax1.plot(tel_d2['Distance'], tel_d2['Speed'], color='magenta', label=driver2, linewidth=2, alpha=0.8)
            ax1.set_ylabel("Speed (km/h)")
            ax1.legend(loc="lower right")
            ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            ax2.plot(tel_d1['Distance'], tel_d1['Throttle'], color='cyan', label=driver1, linewidth=2)
            ax2.plot(tel_d2['Distance'], tel_d2['Throttle'], color='magenta', label=driver2, linewidth=2, alpha=0.8)
            ax2.set_ylabel("Throttle (%)")
            ax2.set_ylim(-5, 105)
            ax2.legend(loc="lower right")
            ax2.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            brake_d1 = tel_d1['Brake'].astype(int)
            brake_d2 = tel_d2['Brake'].astype(int)
            ax3.plot(tel_d1['Distance'], brake_d1, color='cyan', label=driver1, linewidth=2)
            ax3.plot(tel_d2['Distance'], brake_d2 * 0.95, color='magenta', label=driver2, linewidth=2, alpha=0.8)
            ax3.set_ylabel("Brake (On/Off)")
            ax3.set_yticks([0, 1])
            ax3.set_yticklabels(['Off', 'On'])
            ax3.legend(loc="center right")
            ax3.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            plt.tight_layout()
            st.pyplot(fig)
    except Exception as e:
        st.error(f"데이터 로드 실패 : {e}")