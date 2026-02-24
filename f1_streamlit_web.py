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

st.set_page_config(page_title="F1 텔레메트리 비교 뷰어", layout="wide")
st.title("🏎️ F1 드라이버 텔레메트리 비교 대시보드")

st.sidebar.header("📊 데이터 조회 조건")
year = st.sidebar.selectbox("연도 (Year)", [2024, 2023, 2022, 2021])
gp = st.sidebar.text_input("그랑프리 (예: Bahrain, Monza)", value="Bahrain")
session_type = st.sidebar.selectbox("세션 (Session)", ['FP1', 'FP2', 'FP3', 'Q', 'Sprint', 'R'])

# 🏁 드라이버 2명 입력받기
st.sidebar.subheader("🏁 비교할 드라이버 선택")
driver1 = st.sidebar.text_input("드라이버 1 (예: VER)", value="VER").upper()
driver2 = st.sidebar.text_input("드라이버 2 (예: HAM)", value="HAM").upper()

if st.sidebar.button("데이터 비교하기"):
    try:
        with st.spinner(f'{year}년 {gp} 그랑프리 데이터를 불러오는 중입니다...'):
            session = fastf1.get_session(year, gp, session_type)
            session.load()

            # 두 드라이버의 Fastest Lap 추출
            lap_d1 = session.laps.pick_driver(driver1).pick_fastest()
            lap_d2 = session.laps.pick_driver(driver2).pick_fastest()

            # 텔레메트리 데이터 추출
            tel_d1 = lap_d1.get_telemetry()
            tel_d2 = lap_d2.get_telemetry()

            st.subheader(f"🏁 {driver1} vs {driver2} - {year} {gp} ({session_type})")

            # 📊 속도, 스로틀, 브레이크 3단 그래프 생성
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
            fig.patch.set_facecolor('#121212') 

            color_d1 = 'cyan'    # 드라이버 1 색상
            color_d2 = 'magenta' # 드라이버 2 색상

            # 1. 속도 (Speed) 그래프
            ax1.plot(tel_d1['Distance'], tel_d1['Speed'], color=color_d1, label=driver1, linewidth=2)
            ax1.plot(tel_d2['Distance'], tel_d2['Speed'], color=color_d2, label=driver2, linewidth=2, alpha=0.8)
            ax1.set_ylabel("Speed (km/h)")
            ax1.set_title("Speed Comparison", fontsize=14, fontweight='bold')
            ax1.legend(loc="lower right")
            ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            # 2. 스로틀 (Throttle) 그래프
            ax2.plot(tel_d1['Distance'], tel_d1['Throttle'], color=color_d1, label=driver1, linewidth=2)
            ax2.plot(tel_d2['Distance'], tel_d2['Throttle'], color=color_d2, label=driver2, linewidth=2, alpha=0.8)
            ax2.set_ylabel("Throttle (%)")
            ax2.set_title("Throttle Comparison", fontsize=14, fontweight='bold')
            ax2.set_ylim(-5, 105)
            ax2.legend(loc="lower right")
            ax2.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            # 3. 브레이크 (Brake) 그래프
            brake_d1 = tel_d1['Brake'].astype(int)
            brake_d2 = tel_d2['Brake'].astype(int)
            
            # 팁: 브레이크 구간이 겹치면 그래프가 안 보일 수 있어서, 드라이버 2의 그래프 높이를 살짝(0.95) 낮췄어!
            ax3.plot(tel_d1['Distance'], brake_d1, color=color_d1, label=driver1, linewidth=2)
            ax3.plot(tel_d2['Distance'], brake_d2 * 0.95, color=color_d2, label=driver2, linewidth=2, alpha=0.8)
            ax3.set_ylabel("Brake (On/Off)")
            ax3.set_xlabel("Distance (m)")
            ax3.set_yticks([0, 1])
            ax3.set_yticklabels(['Off', 'On'])
            ax3.set_title("Brake Comparison", fontsize=14, fontweight='bold')
            ax3.legend(loc="center right")
            ax3.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

            plt.tight_layout()
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"데이터를 불러오는 데 실패했어. 드라이버 코드(예: VER, LEC)가 맞는지 확인해 봐!\n에러 상세: {e}")
else:
    st.info("👈 왼쪽 사이드바에서 두 명의 드라이버를 선택하고 '데이터 비교하기' 버튼을 눌러줘.")