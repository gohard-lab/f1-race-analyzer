import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class TelemetryAnimationCanvas(FigureCanvas):
    def __init__(self, ver_data, ham_data, parent=None):
        # 1. 피규어 초기화 (기존 대시보드처럼 어두운 배경 적용)
        self.fig = Figure(facecolor='#111827', dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.ax = self.fig.add_subplot(111, facecolor='#111827')
        
        # 그리드 및 축 색상 세팅
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')

        # 2. 데이터 준비 (Pandas DataFrame에서 Numpy 배열로 추출)
        # 예: x축은 Distance, y축은 Brake 데이터
        self.x_ver = ver_data['Distance'].values
        self.y_ver_brake = ver_data['Brake'].values
        
        self.x_ham = ham_data['Distance'].values
        self.y_ham_brake = ham_data['Brake'].values

        # 3. 빈 선(Line) 객체 생성 (여기에 프레임마다 데이터를 채워 넣음)
        self.line_ver, = self.ax.plot([], [], color='#00ffff', lw=2, label='VER Brake')
        self.line_ham, = self.ax.plot([], [], color='#ff00ff', lw=2, label='HAM Brake')
        
        self.ax.legend(loc='upper right', facecolor='#111827', edgecolor='white', labelcolor='white')

        # 4. 축 한계값(Limit) 고정 (매우 중요★)
        # 애니메이션 도중 축이 자동으로 늘어나는 것을 방지합니다.
        # 아부다비 턴 5 진입 구간(예: 1200m ~ 1500m)으로 고정
        self.ax.set_xlim(1200, 1500)
        self.ax.set_ylim(-0.1, 1.1) # 브레이크는 0~100% (0.0 ~ 1.0)

        # 5. 애니메이션 객체 생성
        # 프레임 수는 데이터 배열의 길이 중 짧은 것에 맞춥니다.
        total_frames = min(len(self.x_ver), len(self.x_ham))
        
        self.ani = FuncAnimation(
            self.fig,
            self.update_frame,
            frames=total_frames,
            interval=20,     # 프레임 갱신 간격 (20ms = 초당 약 50프레임)
            blit=True,       # 성능 최적화: 변경된 픽셀(선)만 다시 그림
            repeat=False     # 1회 재생 후 정지
        )

    # 6. 실시간 업데이트 함수 (프레임마다 호출됨)
    def update_frame(self, frame):
        # 0부터 현재 프레임(frame) 인덱스까지만 데이터를 슬라이싱하여 주입
        self.line_ver.set_data(self.x_ver[:frame], self.y_ver_brake[:frame])
        self.line_ham.set_data(self.x_ham[:frame], self.y_ham_brake[:frame])
        
        # blit=True를 사용하려면 반드시 업데이트된 아티스트(선 객체)들을 튜플로 반환해야 함
        return self.line_ver, self.line_ham
    
    # --- 녹화 제어를 위한 추가 메서드 ---
    def pause_animation(self):
        """애니메이션 일시정지"""
        self.ani.pause()

    def resume_animation(self):
        """애니메이션 다시 재생"""
        self.ani.resume()

    def restart_animation(self):
        """처음부터 다시 그리기"""
        self.ani.frame_seq = self.ani.new_frame_seq() # 프레임 카운터 초기화
        self.line_ver.set_data([], [])
        self.line_ham.set_data([], [])
        self.ani.resume()