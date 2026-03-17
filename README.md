# 🏎️ F1 Race Analyzer

F1 레이스 데이터를 수집, 분석하고 직관적으로 시각화하는 파이썬(Streamlit) 기반 애플리케이션입니다. 

## ✨ 주요 기능

* **레이스 데이터 조회:** 특정 시즌, 그랑프리, 세션의 랩타임 및 텔레메트리(Telemetry) 데이터 분석
* **드라이버 페이스 비교:** 선택한 두 드라이버 간의 랩 페이스 및 섹터별 기록 시각화
* **독립 실행 및 클라우드 지원:** 파이썬 환경 구축 없이 바로 실행 가능한 Windows용 `.exe` 파일 및 Google Colab 환경 제공
* **사용자 통계 분석:** Supabase 연동을 통한 애플리케이션 사용량 및 트래픽 모니터링

> **Notice:** 본 프로그램은 더 나은 서비스 제공과 에러 수정을 위해 데이터베이스(Supabase)를 활용하여 익명화된 최소한의 사용 통계(기능 클릭 수 등)를 수집합니다.

## 🛠 기술 스택

* **Language:** Python 3.10+
* **Framework:** Streamlit
* **Database:** Supabase (Usage Tracking)
* **Dependency Management:** `pyproject.toml`

## 🚀 설치 및 실행 방법

이 프로젝트는 레거시 방식인 `requirements.txt` 대신, 최신 파이썬 패키지 관리 표준인 `pyproject.toml`을 사용하여 의존성을 관리합니다.

### 1. 저장소 클론
```bash
git clone [https://github.com/gohard-lab/f1-race-analyzer.git](https://github.com/gohard-lab/f1-race-analyzer.git)
cd f1-race-analyzer

### 2. 의존성 설치 (Poetry 사용 시)
Bash
# Poetry가 설치되어 있지 않다면 먼저 설치해주세요 (pip install poetry)
poetry install
(참고: 일반 pip를 사용할 경우 pip install . 명령어로 설치 가능합니다.)

### 3. 환경 변수 설정
프로젝트 최상단에 .env 파일을 생성하고 Supabase 연결 정보를 입력합니다.

```Ini, TOML
SUPABASE_URL="your_supabase_url"
SUPABASE_KEY="your_supabase_anon_key"

### 4. 애플리케이션 실행
```Bash
poetry run streamlit run f1_telemetry_analyzer.py

📂 프로젝트 구조
보안 및 가독성을 위해 표준적인 형태의 변수명과 범용적인 주석 처리를 지향하여 코드를 작성했습니다.

👨‍💻 제작자 및 관련 링크
GitHub: @gohard-lab

YouTube: 잡학다식 개발자

바로 실행해보기: Google Colab 링크 삽입 예정 / Windows exe 다운로드 링크 삽입 예정