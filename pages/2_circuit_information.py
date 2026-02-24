import streamlit as st
import fastf1
import pandas as pd

st.set_page_config(page_title="서킷 정보", layout="wide")
st.title("🗺️ F1 시즌 일정 및 서킷 정보")

year = st.selectbox("📅 연도 (Year) 선택", [2024, 2023, 2022, 2021])

if st.button("일정 불러오기"):
    with st.spinner(f'{year}년 F1 시즌 일정을 불러오는 중입니다...'):
        schedule = fastf1.get_event_schedule(year)
        
        # 보기 좋게 필요한 데이터만 뽑아서 한글로 변경
        df = schedule[['RoundNumber', 'EventName', 'Country', 'Location', 'EventDate']]
        df.columns = ['라운드', '그랑프리 이름', '국가', '개최지', '결승전 날짜']
        
        # #시간 데이터 깔끔하게 자르기
        df['결승전 날짜'] = pd.to_datetime(df['결승전 날짜']).dt.strftime('%Y-%m-%d')

        st.dataframe(df, use_container_width=True, hide_index=True)