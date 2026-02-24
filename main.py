import sys
import os
import fastf1
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
    app = QApplication(sys.argv)
    window = F1DashboardWindow()
    window.show()
    sys.exit(app.exec_())