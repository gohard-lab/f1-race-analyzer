import streamlit as st
import fastf1

st.set_page_config(page_title="드라이버 순위", layout="wide")
st.title("🏆 경기별 드라이버 최종 순위")

YEARS = [2024, 2023, 2022, 2021]
CIRCUITS = ['Bahrain', 'Saudi Arabia', 'Australia', 'Japan', 'China', 'Miami', 'Emilia Romagna', 'Monaco', 'Canada', 'Spain', 'Austria', 'Great Britain', 'Hungary', 'Belgium', 'Netherlands', 'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico', 'Sao Paulo', 'Las Vegas', 'Qatar', 'Abu Dhabi']

col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("📅 연도", YEARS)
with col2:
    gp = st.selectbox("🏁 그랑프리", CIRCUITS, index=0)

if st.button("순위 결과 보기"):
    try:
        with st.spinner(f'{year} {gp} 본선 레이스(R) 결과를 불러오는 중입니다...'):
            # 본선 레이스(R) 결과를 가져옵니다. 텔레메트리는 끄고 가져와서 속도가 빠릅니다.
            session = fastf1.get_session(year, gp, 'R')
            session.load(telemetry=False, weather=False) 

            results = session.results
            
            # 출력할 컬럼 정리
            df = results[['Position', 'DriverNumber', 'Abbreviation', 'FullName', 'TeamName', 'Points']]
            df.columns = ['최종 순위', '엔트리 넘버', '코드', '이름', '소속팀', '획득 포인트']
            
            st.success(f"🏁 {year} {gp} 그랑프리 레이스 결과")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"데이터를 불러올 수 없습니다. 레이스가 취소되었거나 아직 열리지 않았습니다. (에러: {e})")