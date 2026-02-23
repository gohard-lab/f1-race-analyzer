import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import os

# 0. 화면 테마
plt.style.use('dark_background')

# 1. FastF1 캐시 설정
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

# 웹페이지 기본 설정 (가로로 넓게 쓰기)
st.set_page_config(page_title="F1 텔레메트리 뷰어", layout="wide")
st.title("🏎️ 다이내믹 F1 텔레메트리 대시보드")

# 2. 사이드바(Sidebar)에 검색 조건 위젯 배치
st.sidebar.header("📊 데이터 조회 조건")

year = st.sidebar.selectbox("연도 (Year)", [2024, 2023, 2022, 2021])
gp = st.sidebar.text_input("그랑프리 (예: Bahrain, Monza, Monaco)", value="Bahrain")
session_type = st.sidebar.selectbox("세션 (Session)", ['FP1', 'FP2', 'FP3', 'Q', 'Sprint', 'R'])
driver = st.sidebar.text_input("드라이버 코드 (예: VER, HAM, LEC)", value="VER").upper()

# 3. 데이터 조회 버튼
if st.sidebar.button("데이터 불러오기"):
    try:
        with st.spinner(f'{year}년 {gp} 그랑프리 ({session_type}) 데이터를 불러오는 중입니다...'):
            # 세션 로드
            session = fastf1.get_session(year, gp, session_type)
            session.load()

            # 선택한 드라이버의 가장 빠른 랩 텔레메트리 추출
            fastest_lap = session.laps.pick_driver(driver).pick_fastest()
            telemetry = fastest_lap.get_telemetry()

            # 4. 데이터 시각화
            st.subheader(f"🏁 {driver} - {year} {gp} ({session_type}) Fastest Lap")

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

            # 속도 그래프
            ax1.plot(telemetry['Distance'], telemetry['Speed'], color='blue', linewidth=2)
            ax1.set_ylabel("Speed (km/h)")
            ax1.set_title("Speed & Gear Shifting")
            ax1.grid(True)

            # 기어 변속 그래프
            ax2.plot(telemetry['Distance'], telemetry['nGear'], color='red', linewidth=2)
            ax2.set_ylabel("Gear")
            ax2.set_xlabel("Distance (m)")
            ax2.set_yticks(range(1, 9))
            ax2.grid(True)

            plt.tight_layout()
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"데이터를 불러오는 데 실패했습니다. 입력하신 그랑프리 이름이나 드라이버 코드가 맞는지 확인해 주세요!\n(에러 상세: {e})")
else:
    # 처음 접속했을 때 메인 화면에 띄울 안내 문구
    st.info("👈 왼쪽 사이드바에서 조건을 설정하고 '데이터 불러오기' 버튼을 눌러주세요.")