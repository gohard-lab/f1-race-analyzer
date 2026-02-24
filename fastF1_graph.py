import fastf1 as ff1
from fastf1 import plotting
import matplotlib.pyplot as plt

# 1. 맷플롯립 F1 공식 테마 적용 및 캐시 폴더 설정 (필수)
plotting.setup_mpl()
ff1.Cache.enable_cache('cache') # 작업 폴더에 'cache' 폴더 생성 필요

# 2. 2021년 아부다비 그랑프리 예선(Q) 데이터 긁어오기
print("FIA 서버에서 데이터를 긁어옵니다. 잠시만 기다려주세요...")
session = ff1.get_session(2021, 'Abu Dhabi', 'Q')
session.load()

# 3. 막스(VER)와 해밀턴(HAM)의 가장 빨랐던 랩(Fastest Lap) 쏙 뽑기
ver_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('HAM').pick_fastest()

# 4. 텔레메트리(원격 측정) 데이터에 '거리' 정보 추가해서 가져오기
ver_tel = ver_lap.get_telemetry().add_distance()
ham_tel = ham_lap.get_telemetry().add_distance()

# 5. 그래프로 화려하게 시각화하기
plt.figure(figsize=(14, 6))

# 막스는 레드불(파란색), 해밀턴은 메르세데스(청록색/은색 느낌)로 그리기
plt.plot(ver_tel['Distance'], ver_tel['Speed'], label='Verstappen (VER)', color='blue', linewidth=2)
plt.plot(ham_tel['Distance'], ham_tel['Speed'], label='Hamilton (HAM)', color='cyan', linewidth=2)

# 그래프 꾸미기
plt.title("2021 Abu Dhabi Q3: Verstappen vs Hamilton - Speed", fontsize=16, fontweight='bold')
plt.xlabel("Distance (m)", fontsize=12)
plt.ylabel("Speed (km/h)", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# 짠!
plt.show()