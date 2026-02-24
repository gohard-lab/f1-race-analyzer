import streamlit as st
import fastf1
import pandas as pd
import datetime

st.set_page_config(page_title="서킷 정보", layout="wide")
st.title("🗺️ F1 시즌 일정 및 서킷 정보")

# 1. 오늘 날짜 기준으로 '연도'만 숫자(예: 2026)로 쏙 빼옵니다.
current_year = datetime.datetime.now().year

# 2. range에 적용: 현재 연도부터 2018년까지 역순(-1)으로 목록을 만듭니다.
# (range는 두 번째 숫자 바로 앞까지만 만들어주기 때문에, 2018년까지 보려면 2017로 적어야 합니다)
year = st.selectbox("연도", range(current_year, 2017, -1))
# year = st.selectbox("📅 연도 (Year) 선택", [2024, 2023, 2022, 2021])

if st.button("일정 불러오기"):
    with st.spinner(f'{year}년 F1 시즌 일정을 불러오는 중입니다...'):
        schedule = fastf1.get_event_schedule(year)
        
        # 보기 좋게 필요한 데이터만 뽑아서 한글로 변경
        df = schedule[['RoundNumber', 'EventName', 'Country', 'Location', 'EventDate']]
        df.columns = ['라운드', '그랑프리 이름', '국가', '개최지', '결승전 날짜']
        
        # 시간 데이터 깔끔하게 자르기
        df['결승전 날짜'] = pd.to_datetime(df['결승전 날짜']).dt.strftime('%Y-%m-%d')

        st.dataframe(df, use_container_width=True, hide_index=True)