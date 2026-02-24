import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import os

# 🎨 다크 모드 스타일 적용
plt.style.use('dark_background')

# FastF1 캐시 설정
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

st.set_page_config(page_title="F1 텔레메트리 뷰어", layout="wide")
st.title("🏎️ 다이내믹 F1 텔레메트리 대시보드")

st.sidebar.header("📊 데이터 조회 조건")
year = st.sidebar.selectbox("연도 (Year)", [2024, 2023, 2022, 2021])
gp = st.sidebar.text_input("그랑프리 (예: Bahrain, Monza, Monaco)", value="Bahrain")
session_type = st.sidebar.selectbox("세션 (Session)", ['FP1', 'FP2', 'FP3', 'Q', 'Sprint', 'R'])
driver = st.sidebar.text_input("드라이버 코드 (예: VER, HAM, LEC)", value="VER").upper()

if st.sidebar.button("데이터 불러오기"):
    try:
        with st.spinner(f'{year}년 {gp} 그랑프리 ({session_type}) 데이터를 불러오는 중입니다...'):
            session = fastf1.get_session(year, gp, session_type)
            session.load()

            fastest_lap = session.laps.pick_driver(driver).pick_fastest()
            telemetry = fastest_lap.get_telemetry()

            st.subheader(f"🏁 {driver} - {year} {gp} ({session_type}) Fastest Lap")

            # 📊 그래프 3개로 나누기 (속도, 스로틀, 브레이크)
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
            
            # 도화지 배경색을 약간 짙은 회색으로 변경 (구분감을 위해)
            fig.patch.set_facecolor('#121212') 

            # 1. 속도 (Speed) 그래프
            ax1.plot(telemetry['Distance'], telemetry['Speed'], color='cyan', linewidth=2)
            ax1.set_ylabel("Speed (km/h)")
            ax1.set_title("Speed", fontsize=14, fontweight='bold')
            ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            # 2. 스로틀 (Throttle) 그래프 (0~100%)
            ax2.plot(telemetry['Distance'], telemetry['Throttle'], color='lime', linewidth=2)
            ax2.set_ylabel("Throttle (%)")
            ax2.set_title("Throttle", fontsize=14, fontweight='bold')
            ax2.set_ylim(-5, 105) # 보기 좋게 여백 추가
            ax2.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            # 3. 브레이크 (Brake) 그래프 (On/Off)
            # 브레이크는 True/False 값이므로 보기 쉽게 1과 0으로 변환하여 그립니다.
            brake_data = telemetry['Brake'].astype(int)
            ax3.plot(telemetry['Distance'], brake_data, color='red', linewidth=2)
            ax3.fill_between(telemetry['Distance'], brake_data, color='red', alpha=0.3) # 시각적으로 돋보이게 색칠
            ax3.set_ylabel("Brake (On/Off)")
            ax3.set_xlabel("Distance (m)")
            ax3.set_yticks([0, 1])
            ax3.set_yticklabels(['Off', 'On'])
            ax3.set_title("Brake", fontsize=14, fontweight='bold')
            ax3.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            # 그래프 간격 자동 조절
            plt.tight_layout()
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"데이터를 불러오는 데 실패했습니다. 에러 상세: {e}")
else:
    st.info("👈 왼쪽 사이드바에서 조건을 설정하고 '데이터 불러오기' 버튼을 눌러주세요.")