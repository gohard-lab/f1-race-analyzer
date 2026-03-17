import sys
import os
import fastf1
import streamlit as st
from tracker import log_app_usage
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from animation_canvas import TelemetryAnimationCanvas


# 1. 프로젝트 폴더 내에 캐시 파일들을 저장할 폴더 경로 지정
cache_dir = './f1_cache'

# 2. 폴더가 없으면 자동 생성
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# 3. FastF1 캐시 활성화 ★
fastf1.Cache.enable_cache(cache_dir)

# ---------------------------------------------------------

st.markdown("---")
st.write("🔍 [디버그] Supabase 돌직구 테스트 중...")

# tracker.py를 거치지 않고 여기서 직접 쏴봅니다.
try:
    url = "https://gkzbiacodysnrzbpvavm.supabase.co" # (진짜 주소로 살짝 바꿔주세요)
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdremJpYWNvZHlzbnJ6YnB2YXZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM1NzE2MTgsImV4cCI6MjA4OTE0NzYxOH0.Lv5uVeNZOyo21tgyl2jjGcESoLl_iQTJYp4jdCwuYDU" # (진짜 키로 살짝 바꿔주세요)
    
    client = create_client(url, key)
    res = client.table('usage_logs').insert({"app_name": "f1_test", "action": "test_직접연결"}).execute()
    
    st.success(f"✅ DB에 데이터 꽂힘! 응답 결과: {res.data}")
except Exception as e:
    st.error(f"❌ DB가 뱉어낸 진짜 에러: {e}")


# 앱 메인 파일 최상단에 작성
def run_tracker():
    if "is_tracked" not in st.session_state:
        log_app_usage("f1_telemetry_web", "f1_telemetry_started")
        st.session_state["is_tracked"] = True

# 함수 실행
run_tracker()

class F1DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 2021 Abu Dhabi - Turn 5 Recording Mode")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #111827;")

        self.ver_data, self.ham_data = self.load_f1_data()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 캔버스 추가
        self.canvas = TelemetryAnimationCanvas(self.ver_data, self.ham_data, self)
        main_layout.addWidget(self.canvas)

        # --- 버튼 UI 레이아웃 구성 ---
        button_layout = QHBoxLayout()
        
        self.btn_play = QPushButton("▶ 재생 (Resume)", self)
        self.btn_pause = QPushButton("⏸ 일시정지 (Pause)", self)
        self.btn_restart = QPushButton("🔄 처음부터 (Restart)", self)

        # 버튼 스타일 (어두운 테마)
        btn_style = "color: white; background-color: #374151; padding: 10px; font-weight: bold;"
        self.btn_play.setStyleSheet(btn_style)
        self.btn_pause.setStyleSheet(btn_style)
        self.btn_restart.setStyleSheet(btn_style)

        button_layout.addWidget(self.btn_play)
        button_layout.addWidget(self.btn_pause)
        button_layout.addWidget(self.btn_restart)
        
        main_layout.addLayout(button_layout)

        # 버튼 클릭 이벤트 연결
        self.btn_play.clicked.connect(self.canvas.resume_animation)
        self.btn_pause.clicked.connect(self.canvas.pause_animation)
        self.btn_restart.clicked.connect(self.canvas.restart_animation)
        
        # 시작하자마자 멈춰두고 싶다면 아래 주석을 해제하세요 (녹화 준비용)
        # self.canvas.pause_animation()

    def load_f1_data(self):
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

if __name__ == "__main__":
    log_app_usage("f1_telemetry_web", "f1_telemetry_started")
    app = QApplication(sys.argv)
    window = F1DashboardWindow()
    window.show()
    sys.exit(app.exec_())