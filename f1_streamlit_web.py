import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import os

# 1. 웹페이지 기본 설정 (스마트폰에 최적화)
st.set_page_config(page_title="F1 2021 아부다비 턴5 데이터", layout="centered")

# 2. UI 텍스트 구성
st.title("🏎️ 2021 아부다비 GP 마지막 랩")
st.subheader("막스 vs 해밀턴: 턴 5 브레이킹 타이밍")
st.write("아래 그래프를 손가락으로 확대하거나 스와이프해서 0.1초의 승부를 직접 확인해 보세요!")

# 3. 데이터 로드 함수 (Streamlit 메모리 캐시 적용 ★)
# 이 데코레이터가 있으면 유저 1000명이 접속해도 API 통신은 딱 1번만 합니다.
@st.cache_data 
def load_f1_data():
    cache_dir = './f1_cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)

    session = fastf1.get_session(2021, 'Abu Dhabi', 'R')
    session.load(telemetry=True)

    lap58 = session.laps[session.laps['LapNumber'] == 58]
    ver_tel = lap58.pick_driver('VER').iloc[0].get_telemetry()
    ham_tel = lap58.pick_driver('HAM').iloc[0].get_telemetry()
    return ver_tel, ham_tel

# 데이터 불러오기 (로딩 스피너 UI 제공)
with st.spinner('F1 공식 텔레메트리 데이터를 불러오는 중입니다...'):
    ver_data, ham_data = load_f1_data()

# 4. 그래프 그리기 (Matplotlib 활용)
fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#111827') # 다크모드 배경
ax.set_facecolor('#111827')

# 막스와 해밀턴 브레이크 데이터 플롯
ax.plot(ver_data['Distance'], ver_data['Brake'], color='#00ffff', lw=2.5, label='Max Verstappen')
ax.plot(ham_data['Distance'], ham_data['Brake'], color='#ff00ff', lw=2.5, label='Lewis Hamilton')

# 턴 5 진입 구간(1200m ~ 1500m)만 잘라서 보여주기
ax.set_xlim(1200, 1500)
ax.set_ylim(-0.1, 1.1)

# 디자인 세팅
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Distance (m)', color='white')
ax.set_ylabel('Brake Input (0 to 1)', color='white')
ax.legend(facecolor='#111827', labelcolor='white')

# 5. Streamlit 화면에 그래프 송출
st.pyplot(fig)

st.caption("제작: 잡학다식 개발자 | 데이터 출처: FastF1 API")