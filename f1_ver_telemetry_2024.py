import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import os

# 1. FastF1 캐시 설정 (API 호출을 줄이기 위해 데이터를 로컬에 저장)
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache')

st.title("🏎️ F1 텔레메트리 대시보드")

# 2. 데이터 로딩 (Streamlit 스피너로 로딩 상태 표시)
with st.spinner('F1 데이터를 불러오는 중입니다... (최초 실행 시 다운로드로 인해 시간이 걸립니다)'):
    # 2024년 바레인 그랑프리 퀄리파잉 세션 로드
    session = fastf1.get_session(2024, 'Bahrain', 'Q')
    session.load()

    # 막스 베르스타펜(VER)의 가장 빠른 랩 텔레메트리 추출
    fastest_lap = session.laps.pick_driver('VER').pick_fastest()
    telemetry = fastest_lap.get_telemetry()

# 3. 데이터 시각화 (Matplotlib)
st.subheader("Max Verstappen - 2024 Bahrain Q Fastest Lap")

# 위아래로 2개의 그래프 배치 (X축인 거리를 공유)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# 속도 그래프 (파란색)
ax1.plot(telemetry['Distance'], telemetry['Speed'], color='blue')
ax1.set_ylabel("Speed (km/h)")
ax1.set_title("Speed and Gear Shifting")
ax1.grid(True)

# 기어 변속 그래프 (빨간색)
ax2.plot(telemetry['Distance'], telemetry['nGear'], color='red')
ax2.set_ylabel("Gear")
ax2.set_xlabel("Distance (m)")
ax2.set_yticks(range(1, 9)) # F1은 8단 기어까지 있음
ax2.grid(True)

# 여백 조정 후 Streamlit에 출력
plt.tight_layout()
st.pyplot(fig)