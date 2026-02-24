import sys
import numpy as np
import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
# 🔥 [수정] QFrame이 추가되었습니다.
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings

import os
# 1. 프로젝트 폴더 내에 캐시 파일들을 저장할 폴더 경로 지정
cache_dir = './cache'

# 2. 폴더가 없으면 자동 생성
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# 3. FastF1 캐시 활성화 ★
ff1.Cache.enable_cache(cache_dir)

# ---------------------------------------------------------

warnings.simplefilter(action='ignore', category=FutureWarning)
ff1.Cache.enable_cache('cache')

class CustomToolbar(NavigationToolbar):
    toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Back', 'Forward', 'Save')]

class F1AnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1 Telemetry Director Board (Grouped UI)")
        self.setGeometry(100, 100, 1600, 900)

        self.app_bg_color = '#F0F4F8'   
        self.graph_bg_color = '#0B192C'
        self.graph_text_color = '#FFFFFF'
        self.graph_grid_color = '#1A365D'
        self.track_color = '#8892b0'
        self.highlight_color = '#FFD369' 
        self.color_d1 = '#00E5FF' 
        self.color_d2 = '#FF007F' 

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        self.main_widget.setStyleSheet(f"background-color: {self.app_bg_color};")

        self.setup_control_panel()

        self.fig = plt.figure(figsize=(16, 8))
        self.fig.patch.set_facecolor(self.graph_bg_color)
        self.canvas = FigureCanvas(self.fig)
        
        self.toolbar = CustomToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("background-color: #FFFFFF; spacing: 5px;")
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('scroll_event', self.on_scroll) 
        
        self.ver_tel = None
        self.highlight_line = None
        self.ax_map = None
        self.ax0 = None
        self.axes_list = []
        self.is_pressing = False
        self.press_x = None

    def setup_control_panel(self):
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(10, 10, 10, 10) 
        combo_style = "QComboBox { background-color: white; border: 2px solid #CBD5E1; border-radius: 6px; padding: 4px; color: black; font-weight: bold; }"

        # --- 데이터 셋업 ---
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(y) for y in range(2026, 2017, -1)])
        self.year_combo.setCurrentText("2021")
        self.year_combo.setStyleSheet(combo_style)
        self.year_combo.setFixedWidth(80) # 글자 수에 맞춰 너비 조정

        self.event_combo = QComboBox()
        events = ["Abu Dhabi", "Bahrain", "Saudi Arabia", "Australia", "Monaco", "Silverstone", "Monza", "Suzuka", "Interlagos", "Las Vegas"]
        self.event_combo.addItems(sorted(events))
        self.event_combo.setCurrentText("Abu Dhabi")
        self.event_combo.setStyleSheet(combo_style)
        self.event_combo.setFixedWidth(130)

        # self.session_combo = QComboBox()
        # self.session_combo.addItems(["R", "Q"]) 
        # self.session_combo.setStyleSheet(combo_style)
        # self.session_combo.setFixedWidth(60)

# 🔥 [핵심 수정] 세션 종류를 한글 설명과 함께 모두 추가!
        self.session_combo = QComboBox()
        sessions = [
            "R (본선 레이스)", 
            "Q (예선)", 
            "S (스프린트)", 
            "SQ (스프린트 예선)", 
            "FP1 (연습주행 1)", 
            "FP2 (연습주행 2)", 
            "FP3 (연습주행 3)"
        ]
        self.session_combo.addItems(sessions)
        self.session_combo.setStyleSheet(combo_style)
        self.session_combo.setFixedWidth(140) # 글자가 길어졌으니 너비를 넉넉하게

        self.driver1_combo = QComboBox()
        self.driver2_combo = QComboBox()
        drivers = sorted(["VER", "HAM", "LEC", "SAI", "NOR", "PIA", "RUS", "ALO", "PER", "STR", "GAS", "OCO", "ALB", "TSU"])
        self.driver1_combo.addItems(drivers)
        self.driver2_combo.addItems(drivers)
        self.driver1_combo.setCurrentText("VER")
        self.driver2_combo.setCurrentText("HAM")
        self.driver1_combo.setStyleSheet(combo_style)
        self.driver2_combo.setStyleSheet(combo_style)
        self.driver1_combo.setFixedWidth(80)
        self.driver2_combo.setFixedWidth(80)

        self.lap_combo = QComboBox()
        self.lap_combo.addItems([str(i) for i in range(1, 81)])
        self.lap_combo.setCurrentText("58")
        self.lap_combo.setStyleSheet(combo_style)
        self.lap_combo.setFixedWidth(60)

        # --- UI 그룹화 및 배치 ---
        def create_group(items):
            group_layout = QHBoxLayout()
            group_layout.setSpacing(5) # 라벨과 콤보박스를 바짝 붙임
            for label_text, widget in items:
                lbl = QLabel(label_text)
                lbl.setStyleSheet("font-weight: bold; color: #1E293B;")
                group_layout.addWidget(lbl)
                group_layout.addWidget(widget)
                group_layout.addSpacing(10) # 같은 그룹 내 요소 간 약간의 간격
            return group_layout

        def add_vertical_separator():
            line = QFrame()
            line.setFrameShape(QFrame.VLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #CBD5E1; margin-left: 5px; margin-right: 5px;")
            control_layout.addWidget(line)

        # 1. 경기 정보 그룹
        event_group = create_group([("Year:", self.year_combo), ("Event:", self.event_combo), ("Session:", self.session_combo)])
        control_layout.addLayout(event_group)
        
        add_vertical_separator()

        # 2. 드라이버 정보 그룹
        driver_group = create_group([("Driver 1:", self.driver1_combo), ("Driver 2:", self.driver2_combo)])
        control_layout.addLayout(driver_group)

        add_vertical_separator()

        # 3. 랩 정보 그룹
        lap_group = create_group([("Lap #:", self.lap_combo)])
        control_layout.addLayout(lap_group)

        # 오른쪽 남는 공간을 밀어주고 버튼 배치
        control_layout.addStretch()
        
        self.btn_analyze = QPushButton("🚀 분석 시작")
        self.btn_analyze.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; border-radius: 6px; padding: 8px 20px;")
        self.btn_analyze.clicked.connect(self.run_analysis)
        control_layout.addWidget(self.btn_analyze)

        self.layout.addLayout(control_layout)

    def run_analysis(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.setText("⏳ 로딩 중...")
        QApplication.processEvents()

        try:
            year = int(self.year_combo.currentText())
            event = self.event_combo.currentText()
            # session_type = self.session_combo.currentText()

            # --- 교체할 부분 ---
            # 띄어쓰기 기준으로 앞의 영문 코드만 가져옵니다.
            session_code = self.session_combo.currentText().split(" ")[0]

            d1 = self.driver1_combo.currentText()
            d2 = self.driver2_combo.currentText()
            target_lap = int(self.lap_combo.currentText())

            session = ff1.get_session(year, event, session_code)
            session.load()
            self.circuit_info = session.get_circuit_info()

            laps_d1 = session.laps.pick_drivers(d1)
            laps_d2 = session.laps.pick_drivers(d2)
            
            target_laps_d1 = laps_d1[laps_d1['LapNumber'] == target_lap]
            target_laps_d2 = laps_d2[laps_d2['LapNumber'] == target_lap]

            if target_laps_d1.empty or target_laps_d2.empty:
                raise ValueError(f"{d1} 혹은 {d2}의 {target_lap}번째 랩 데이터가 없습니다.")

            lap_d1 = target_laps_d1.iloc[0]
            lap_d2 = target_laps_d2.iloc[0]

            self.ver_tel = lap_d1.get_telemetry().add_distance()
            ham_tel = lap_d2.get_telemetry().add_distance()
            delta_time, ref_tel, _ = utils.delta_time(lap_d1, lap_d2)

            self.fig.clear()
            self.fig.suptitle(f"{year} {event} | {d1} vs {d2} (Lap {target_lap})", color='white', fontweight='bold', fontsize=16)
            gs = gridspec.GridSpec(4, 2, width_ratios=[3, 1])

            def create_ax(pos, title, share_ax=None):
                # ax = self.fig.add_subplot(pos, sharex=share_ax, facecolor=self.graph_bg_color)
                ax = self.fig.add_subplot(pos, sharex=share_ax, facecolor='#000000')
                ax.tick_params(colors=self.graph_text_color)
                ax.grid(True, color=self.graph_grid_color, linestyle='--', alpha=0.5)
                ax.set_ylabel(title, color='white', fontweight='bold')
                return ax

            self.ax0 = create_ax(gs[0, 0], "Time Delta (s)")
            ax1 = create_ax(gs[1, 0], "Speed (km/h)", share_ax=self.ax0)
            ax2 = create_ax(gs[2, 0], "Throttle (%)", share_ax=self.ax0)
            ax3 = create_ax(gs[3, 0], "Brake", share_ax=self.ax0)
            ax3.set_xlabel("Distance (m)", color='white', fontweight='bold')
            
            self.axes_list = [self.ax0, ax1, ax2, ax3]

            self.ax0.plot(ref_tel['Distance'], delta_time, color='white', linewidth=2, label=f'Gap ({d1} vs {d2})')
            self.ax0.axhline(0, color='gray', linestyle='--', label=f'{d1} (Base Line)')
            
            ax1.plot(self.ver_tel['Distance'], self.ver_tel['Speed'], label=d1, color=self.color_d1, linewidth=2)
            ax1.plot(ham_tel['Distance'], ham_tel['Speed'], label=d2, color=self.color_d2, linewidth=2)
            
            ax2.plot(self.ver_tel['Distance'], self.ver_tel['Throttle'], label=d1, color=self.color_d1, linewidth=2)
            ax2.plot(ham_tel['Distance'], ham_tel['Throttle'], label=d2, color=self.color_d2, linewidth=2)
            
            ax3.plot(self.ver_tel['Distance'], self.ver_tel['Brake'], label=d1, color=self.color_d1, linewidth=2)
            ax3.plot(ham_tel['Distance'], ham_tel['Brake'], label=d2, color=self.color_d2, linewidth=2)
            
            for ax in self.axes_list:
                ax.legend(loc='upper right', labelcolor='white', frameon=False, fontsize=9)

            self.ax_map = self.fig.add_subplot(gs[:, 1], facecolor="#363131FF")
            self.ax_map.plot(self.ver_tel['X'], self.ver_tel['Y'], color="#8EE42C", linewidth=2)

            # 3. 코너 번호도 글자는 검정색, 둥근 박스는 연한 회색으로 변경
            for _, corner in self.circuit_info.corners.iterrows():
                txt = f"{corner['Number']}{corner['Letter']}"
                self.ax_map.text(corner['X'], corner['Y'], txt, color='black', fontsize=8, ha='center', va='center',
                                 fontweight='bold', bbox=dict(boxstyle='circle,pad=0.2', facecolor='#F3F4F6', edgecolor='#9CA3AF', alpha=0.9))

            self.ax_map.set_aspect('equal', 'datalim')
            
            # 🔥 [수정] axis('off') 대신 눈금과 테두리 선만 감쪽같이 숨깁니다! (바탕색 유지됨)
            self.ax_map.set_xticks([])
            self.ax_map.set_yticks([])
            for spine in self.ax_map.spines.values():
                spine.set_visible(False)

            # 4. 하얀 바탕에서 가장 잘 튀는 F1 공식 레드(#E10600)로 줌 하이라이트 라인 변경
            self.highlight_line, = self.ax_map.plot([], [], color='#E10600', linewidth=5)
            self.fig.tight_layout()
            self.toolbar.update()
            self.update_view(500)

        except Exception as e:
            QMessageBox.warning(self, "오류", f"데이터 로드 실패: {str(e)} (특정 선수가 해당 경기에서 출전하지 않았거나 또는 lab이 없거나, 경기 중 사고를 당한 경우 등은 데이터가 없을 수 있습니다.)")
        finally:
            QApplication.restoreOverrideCursor()
            self.btn_analyze.setEnabled(True)
            self.btn_analyze.setText("🚀 분석 시작")

    def on_scroll(self, event):
        if event.inaxes in self.axes_list:
            base_scale = 0.7
            cur_xlim = self.ax0.get_xlim()
            scale = base_scale if event.button == 'up' else 1/base_scale
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale
            rel_x = (cur_xlim[1] - event.xdata) / (cur_xlim[1] - cur_xlim[0])
            new_xlim = [event.xdata - new_width * (1 - rel_x), event.xdata + new_width * rel_x]
            self.ax0.set_xlim(new_xlim)
            self.sync_map(new_xlim[0], new_xlim[1])
            self.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes in self.axes_list:
            self.is_pressing = True
            self.press_x = event.xdata
        elif event.inaxes == self.ax_map and self.ver_tel is not None:
            distances = np.sqrt((self.ver_tel['X'] - event.xdata)**2 + (self.ver_tel['Y'] - event.ydata)**2)
            closest_idx = distances.idxmin()
            self.update_view(self.ver_tel.loc[closest_idx, 'Distance'])

    def on_motion(self, event):
        if self.is_pressing and event.inaxes in self.axes_list:
            dx = self.press_x - event.xdata
            cur_xlim = self.ax0.get_xlim()
            new_xlim = [cur_xlim[0] + dx, cur_xlim[1] + dx]
            self.ax0.set_xlim(new_xlim)
            self.sync_map(new_xlim[0], new_xlim[1])
            self.canvas.draw_idle()

    def on_release(self, event):
        self.is_pressing = False

    def sync_map(self, z_start, z_end):
        if self.ver_tel is not None and self.highlight_line is not None:
            mask = (self.ver_tel['Distance'] >= z_start) & (self.ver_tel['Distance'] <= z_end)
            self.highlight_line.set_data(self.ver_tel['X'][mask], self.ver_tel['Y'][mask])

    def update_view(self, center_distance):
        if self.ver_tel is None: return
        self.ax0.set_xlim(center_distance - 350, center_distance + 350)
        self.sync_map(center_distance - 350, center_distance + 350)
        closest_corner_idx = (self.circuit_info.corners['Distance'] - center_distance).abs().argmin()
        corner = self.circuit_info.corners.iloc[closest_corner_idx]
        self.ax0.set_title(f"▶ Analysis: Turn {corner['Number']}", color=self.highlight_color, fontweight='bold', fontsize=12)
        self.canvas.draw_idle()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = F1AnalyzerApp()
    ex.show()
    sys.exit(app.exec_())