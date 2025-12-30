# 🛒 실시간 전자상거래 이상거래 탐지 시스템

![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat-square&logo=python&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-3.5-231F20?style=flat-square&logo=apache-kafka&logoColor=white)
![Spark](https://img.shields.io/badge/Spark-3.5-E25A1C?style=flat-square&logo=apache-spark&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Latest-F46800?style=flat-square&logo=grafana&logoColor=white)

Kafka와 Spark Streaming을 활용한 **실시간 데이터 파이프라인**으로, 전자상거래 주문 데이터를 실시간으로 분석하여 이상 거래를 탐지하고 Grafana 대시보드로 시각화합니다.

## 📑 목차

- [프로젝트 개요](#-프로젝트-개요)
- [시스템 아키텍처](#-시스템-아키텍처)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [데이터베이스 스키마](#-데이터베이스-스키마)
- [설치 및 실행](#-설치-및-실행)
- [대시보드 스크린샷](#-대시보드-스크린샷)
- [프로젝트 구조](#-프로젝트-구조)
- [기술적 의사결정](#-기술적-의사결정)
- [트러블슈팅](#-트러블슈팅)

---

## 🎯 프로젝트 개요

### 배경
전자상거래 플랫폼에서는 매크로를 이용한 대량 구매, 이상 거래 패턴 등을 실시간으로 탐지하여 대응해야 합니다. 본 프로젝트는 **초당 수천 건의 주문 데이터를 실시간으로 처리**하고, 의심스러운 거래 패턴을 즉시 감지하는 시스템입니다.

### 목표
- ⚡ **실시간 처리**: 평균 500ms 이하의 지연시간으로 데이터 분석
- 🔍 **이상 탐지**: 매크로 의심 IP, 고액 거래 실시간 모니터링
- 📊 **시각화**: Grafana를 통한 실시간 대시보드 제공
- 🏗️ **확장성**: 분산 처리 가능한 아키텍처 설계

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐
│  주문 생성기     │ (Python)
│  Order Generator │
└────────┬────────┘
         │ JSON 메시지
         ↓
┌─────────────────┐
│     Kafka       │ (Message Queue)
│   Topic: orders │
└────────┬────────┘
         │ 스트리밍
         ↓
┌─────────────────┐
│ Spark Streaming │ (Real-time Processing)
│  - 윈도우 집계   │
│  - 이상 탐지     │
│  - 데이터 변환   │
└────────┬────────┘
         │ JDBC
         ↓
┌─────────────────┐
│  PostgreSQL     │ (Data Storage)
│  - 인기 상품     │
│  - 의심 IP       │
│  - 고액 거래     │
│  - 실시간 통계   │
└────────┬────────┘
         │ Query
         ↓
┌─────────────────┐
│    Grafana      │ (Visualization)
│  실시간 대시보드 │
└─────────────────┘
```

### 데이터 플로우
1. **주문 생성**: Python 스크립트가 초당 약 10-20건의 가상 주문 데이터 생성
2. **Kafka 전송**: JSON 형태로 `orders` 토픽에 발행
3. **Spark 처리**: 
   - 30초 윈도우로 인기 상품 집계
   - 1분 윈도우로 IP별 주문 패턴 분석
   - 50만원 이상 고액 거래 필터링
4. **DB 저장**: PostgreSQL에 분석 결과 저장
5. **대시보드**: Grafana가 5-10초마다 자동 갱신

---

## ✨ 주요 기능

### 1. 실시간 인기 상품 분석
- **Window**: 30초 슬라이딩 윈도우
- **집계**: 상품별 주문 건수, 총 매출
- **목적**: 재고 관리, 마케팅 전략 수립

### 2. 매크로 의심 IP 탐지
- **조건**: 1분 내 동일 IP에서 10건 이상 주문
- **Window**: 1분 슬라이딩 윈도우
- **알림**: 의심 IP, 주문 수, 총 금액 기록

### 3. 고액 거래 모니터링
- **기준**: 50만원 이상 단일 거래
- **처리**: 실시간 스트리밍 (배치 없음)
- **목적**: 사기 거래 방지, 결제 승인 검토

### 4. 실시간 통계 대시보드
- 전체 주문 수 추이
- 시간대별 매출 현황
- 평균 주문 금액
- 의심 IP 발생 추이

---

## 🛠️ 기술 스택

| 카테고리 | 기술 | 버전 | 용도 |
|---------|------|------|------|
| **메시지 큐** | Apache Kafka | 3.5.0 | 실시간 데이터 스트리밍 |
| **스트림 처리** | Apache Spark Streaming | 3.5.0 | 실시간 데이터 분석 및 집계 |
| **데이터베이스** | PostgreSQL | 15 | 분석 결과 저장 |
| **시각화** | Grafana | Latest | 실시간 대시보드 |
| **컨테이너** | Docker Compose | - | 인프라 관리 |
| **언어** | Python | 3.9 | 데이터 생성 및 파이프라인 |
| **라이브러리** | confluent-kafka, pyspark, psycopg2 | - | Kafka/Spark/DB 연동 |

### 왜 이 기술들을 선택했나?

**Kafka**
- ✅ 높은 처리량 (초당 수백만 메시지)
- ✅ 메시지 영속성 (디스크 저장)
- ✅ 여러 Consumer 동시 구독 가능

**Spark Streaming**
- ✅ 마이크로 배치 방식으로 안정적
- ✅ Window 함수로 시계열 분석 용이
- ✅ 확장성 (클러스터 모드 지원)

**PostgreSQL**
- ✅ 트랜잭션 지원
- ✅ 복잡한 쿼리 성능 우수
- ✅ Grafana와 네이티브 연동

---

## 📊 데이터베이스 스키마

### 1. popular_products (인기 상품 통계)
```sql
CREATE TABLE popular_products (
    id SERIAL PRIMARY KEY,
    window_start TIMESTAMP,      -- 윈도우 시작 시간
    window_end TIMESTAMP,        -- 윈도우 종료 시간
    product_name VARCHAR(100),   -- 상품명
    order_count INTEGER,         -- 주문 건수
    total_sales BIGINT,          -- 총 매출 (원)
    created_at TIMESTAMP DEFAULT NOW()  -- 레코드 생성 시간
);

-- 인덱스: 시간 기반 조회 최적화
CREATE INDEX idx_popular_created ON popular_products(created_at);
CREATE INDEX idx_popular_window ON popular_products(window_end);
```

**컬럼 설명:**
- `window_start/window_end`: Spark의 30초 윈도우 시작/종료 시간
- `product_name`: 집계 대상 상품명 (노트북, 스마트폰 등)
- `order_count`: 해당 윈도우 동안의 주문 건수
- `total_sales`: 해당 윈도우 동안의 총 매출액
- `created_at`: DB 삽입 시간 (디버깅 및 데이터 추적용)

**샘플 데이터:**
```
id | window_start        | window_end          | product_name | order_count | total_sales | created_at
---+---------------------+---------------------+--------------+-------------+-------------+-------------------
 1 | 2025-12-30 21:00:00 | 2025-12-30 21:00:30 | 노트북        |     23      | 34,500,000  | 2025-12-30 21:00:35
 2 | 2025-12-30 21:00:00 | 2025-12-30 21:00:30 | 스마트폰      |     18      | 14,400,000  | 2025-12-30 21:00:35
```

---

### 2. suspicious_ips (의심 IP 목록)
```sql
CREATE TABLE suspicious_ips (
    id SERIAL PRIMARY KEY,
    window_start TIMESTAMP,      -- 탐지 윈도우 시작
    ip_address VARCHAR(50),      -- 의심 IP 주소
    order_count INTEGER,         -- 주문 건수
    total_spent BIGINT,          -- 총 결제 금액 (원)
    created_at TIMESTAMP DEFAULT NOW()
);

-- 인덱스: IP 조회 최적화
CREATE INDEX idx_suspicious_ip ON suspicious_ips(ip_address);
CREATE INDEX idx_suspicious_created ON suspicious_ips(created_at);
```

**컬럼 설명:**
- `window_start`: 1분 윈도우 시작 시간 (의심 행동 발생 구간)
- `ip_address`: 의심스러운 행동을 한 IP 주소
- `order_count`: 1분 내 주문 건수 (10건 이상일 때만 기록)
- `total_spent`: 1분 내 해당 IP의 총 결제 금액
- `created_at`: 탐지 시간

**샘플 데이터:**
```
id | window_start        | ip_address     | order_count | total_spent  | created_at
---+---------------------+----------------+-------------+--------------+-------------------
 1 | 2025-12-30 21:05:00 | 192.168.99.99  |     87      | 130,500,000  | 2025-12-30 21:06:05
```

**비즈니스 룰:**
- `order_count >= 10`: 1분 내 10건 이상 주문 시 의심 IP로 기록
- 실제 운영 시에는 차단 또는 추가 인증 요구

---

### 3. high_value_orders (고액 거래)
```sql
CREATE TABLE high_value_orders (
    id SERIAL PRIMARY KEY,
    order_time TIMESTAMP,        -- 주문 시간
    order_id VARCHAR(100),       -- 주문 ID
    product_name VARCHAR(100),   -- 상품명
    quantity INTEGER,            -- 수량
    total_price BIGINT,          -- 총 금액 (원)
    ip_address VARCHAR(50),      -- 주문 IP
    created_at TIMESTAMP DEFAULT NOW()
);

-- 인덱스: 시간/금액 기반 조회
CREATE INDEX idx_high_value_time ON high_value_orders(order_time);
CREATE INDEX idx_high_value_price ON high_value_orders(total_price);
```

**컬럼 설명:**
- `order_time`: 주문이 발생한 실제 시간
- `order_id`: 주문 고유 식별자 (예: ORD1735567275123)
- `product_name`: 구매한 상품명
- `quantity`: 구매 수량
- `total_price`: 총 결제 금액 (가격 × 수량)
- `ip_address`: 주문한 사용자의 IP 주소
- `created_at`: DB 삽입 시간

**샘플 데이터:**
```
id | order_time          | order_id         | product_name | quantity | total_price  | ip_address
---+---------------------+------------------+--------------+----------+--------------+---------------
 1 | 2025-12-30 21:10:15 | ORD1735567275123 | 노트북        |    8     | 12,000,000   | 192.168.99.99
```

**비즈니스 룰:**
- `total_price >= 500,000`: 50만원 이상 거래는 별도 모니터링
- 실제 운영 시에는 추가 인증, 결제 승인 지연 등의 조치

---

### 4. realtime_stats (실시간 통계)
```sql
CREATE TABLE realtime_stats (
    id SERIAL PRIMARY KEY,
    stat_time TIMESTAMP,             -- 통계 시점
    total_orders INTEGER,            -- 총 주문 수
    total_sales BIGINT,              -- 총 매출 (원)
    avg_order_value BIGINT,          -- 평균 주문 금액 (원)
    suspicious_ip_count INTEGER,     -- 의심 IP 수 (현재 0, 향후 확장)
    created_at TIMESTAMP DEFAULT NOW()
);

-- 인덱스: 시간 기반 조회
CREATE INDEX idx_stats_time ON realtime_stats(stat_time);
```

**컬럼 설명:**
- `stat_time`: 통계 집계 시점 (30초 윈도우의 종료 시간)
- `total_orders`: 30초 동안의 총 주문 건수
- `total_sales`: 30초 동안의 총 매출액
- `avg_order_value`: 30초 동안의 평균 주문 금액
- `suspicious_ip_count`: 의심 IP 수 (현재는 0, 향후 조인으로 계산 가능)
- `created_at`: DB 삽입 시간

**샘플 데이터:**
```
id | stat_time           | total_orders | total_sales | avg_order_value | suspicious_ip_count | created_at
---+---------------------+--------------+-------------+-----------------+---------------------+-------------------
 1 | 2025-12-30 21:09:00 |      28      |  22,730,000 |      811,785    |          0          | 2025-12-30 21:09:05
 2 | 2025-12-30 21:09:30 |      50      |  67,990,000 |    1,359,800    |          0          | 2025-12-30 21:09:35
```

**활용:**
- Grafana 시계열 그래프 데이터 소스
- 시간대별 비즈니스 지표 추적
- 피크 타임 분석 및 리소스 계획

---


## 🚀 설치 및 실행

### 사전 요구사항
```bash
# 필수
- Docker Desktop 설치
- Python 3.9 이상
- Java 17 (Spark 실행용)

# 확인
docker --version
python3 --version
java -version
```

### 1단계: 프로젝트 클론
```bash
git clone https://github.com/your-username/ecommerce-fraud-detection.git
cd ecommerce-fraud-detection
```

### 2단계: Python 라이브러리 설치
```bash
pip install confluent-kafka pyspark psycopg2-binary
```

### 3단계: 인프라 시작
```bash
# Docker 컨테이너 시작 (Kafka, PostgreSQL, Grafana)
docker-compose up -d

# 컨테이너 확인
docker ps
# 4개 실행 중이어야 함: zookeeper, kafka, postgres, grafana
```

### 4단계: 데이터베이스 초기화
```bash
# 데이터베이스 생성
python3 create_database.py

# 테이블 생성
python3 create_tables.py
```

### 5단계: 데이터 파이프라인 실행

**터미널 1 - 주문 데이터 생성:**
```bash
python3 order_generator.py
```

**터미널 2 - Spark 스트리밍 (분석 & DB 저장):**
```bash
python3 spark_to_db.py
```

**터미널 3 - Spark 분석 (콘솔 출력, 선택사항):**
```bash
python3 spark_analyzer.py
```

### 6단계: Grafana 대시보드 설정

1. **브라우저에서 접속:**
   ```
   http://localhost:3000
   ```

2. **로그인:**
   - Username: `admin`
   - Password: `admin`

3. **PostgreSQL 데이터소스 추가:**
   - Configuration → Data sources → Add data source
   - PostgreSQL 선택
   - 설정:
     ```
     Host: host.docker.internal:5432
     Database: analytics_db
     User: admin
     Password: admin123
     SSL Mode: disable
     ```
   - "Save & test" 클릭

4. **대시보드 생성:**
   - 좌측 + 아이콘 → Create Dashboard
   - 패널 추가 (아래 쿼리 참고)

### Grafana 쿼리 예시

**실시간 주문 수:**
```sql
SELECT 
  stat_time as time,
  total_orders
FROM realtime_stats
WHERE stat_time > NOW() - INTERVAL '10 minutes'
ORDER BY stat_time
```

**실시간 매출:**
```sql
SELECT 
  stat_time as time,
  total_sales / 1000000.0 as "매출(백만원)"
FROM realtime_stats
WHERE stat_time > NOW() - INTERVAL '10 minutes'
ORDER BY stat_time
```

**인기 상품 Top 5:**
```sql
SELECT 
  product_name,
  SUM(order_count) as total_orders
FROM popular_products
WHERE created_at > NOW() - INTERVAL '5 minutes'
GROUP BY product_name
ORDER BY total_orders DESC
LIMIT 5
```

**의심 IP:**
```sql
SELECT 
  ip_address,
  order_count,
  total_spent / 1000000.0 as "금액(백만원)",
  window_start as "탐지시간"
FROM suspicious_ips
WHERE created_at > NOW() - INTERVAL '10 minutes'
ORDER BY order_count DESC
```

**고액 거래 건수:**
```sql
SELECT 
  COUNT(*) as count
FROM high_value_orders
WHERE created_at > NOW() - INTERVAL '5 minutes'
```

---

## 📸 대시보드 스크린샷

### 실시간 모니터링 대시보드
![Dashboard](screenshots/dashboard.png)

**포함 내용:**
- 📊 실시간 주문 수 (시계열 그래프)
- 💰 실시간 매출 (시계열 그래프)
- 🏆 인기 상품 Top 5 (바 차트)
- 🚨 의심 IP 탐지 (테이블)
- 💳 고액 거래 건수 (통계)

---

## 📁 프로젝트 구조

```
ecommerce-fraud-detection/
├── docker-compose.yml          # 인프라 정의 (Kafka, PostgreSQL, Grafana)
├── create_database.py          # DB 생성 스크립트
├── create_tables.py            # 테이블 스키마 생성
├── order_generator.py          # 가상 주문 데이터 생성기
├── spark_to_db.py              # Spark Streaming → PostgreSQL 저장
├── spark_analyzer.py           # Spark Streaming 콘솔 출력 (디버깅용)
├── README.md                   # 프로젝트 문서 (현재 파일)
├── requirements.txt            # Python 의존성
└── screenshots/                # 대시보드 스크린샷
    └── dashboard.png
```

### 주요 파일 설명

**order_generator.py**
- **역할**: 초당 10-20건의 가상 주문 생성
- **데이터**: 상품(노트북, 스마트폰 등), 가격, 수량, IP 주소
- **패턴**: 90% 정상 주문, 10% 의심 주문 (IP: 192.168.99.99)
- **JSON 포맷**:
  ```json
  {
    "order_id": "ORD1735567275123",
    "timestamp": "2025-12-30T21:10:15.123456",
    "user_id": "USER1234",
    "product_id": "P001",
    "product_name": "노트북",
    "price": 1500000,
    "quantity": 2,
    "ip_address": "192.168.1.100",
    "payment_method": "card"
  }
  ```

**spark_to_db.py**
- **역할**: Kafka 메시지 소비 → Spark 처리 → PostgreSQL 저장
- **Window 함수**:
  - 인기 상품: 30초 슬라이딩 윈도우
  - 의심 IP: 1분 슬라이딩 윈도우
  - 실시간 통계: 30초 슬라이딩 윈도우
- **배치 처리**: 30초마다 DB에 저장
- **타임존**: KST (Asia/Seoul) 변환 처리

**spark_analyzer.py**
- **역할**: Spark 분석 결과를 콘솔에 실시간 출력
- **용도**: 디버깅, 데이터 검증
- **출력**: 인기 상품, 의심 IP, 고액 거래를 터미널에 표시

---

## 💡 기술적 의사결정

### 1. 왜 Kafka를 사용했는가?

**기존 방식 (Apache NiFi):**
- GUI 기반 플로우 설계
- 주로 배치 처리에 적합
- 레거시 시스템 통합에 유리

**Kafka 선택 이유:**
- ✅ 높은 처리량 (초당 수백만 메시지)
- ✅ Publish-Subscribe 패턴으로 여러 Consumer 동시 처리
- ✅ 메시지 영속성 (디스크 저장, 장애 시 재처리 가능)
- ✅ 대기업/글로벌 기업의 사실상 표준

### 2. Spark Streaming

**Spark Streaming 선택 이유:**
- ✅ 마이크로 배치 방식으로 안정적
- ✅ 풍부한 Window 함수 (tumbling, sliding, session)
- ✅ 기존 배치 처리 경험 활용 가능
- ✅ 커뮤니티 크고 레퍼런스 많음

### 3. Window 설정 근거

**인기 상품 (30초):**
- 너무 짧으면: 데이터 불안정, DB 부하 증가
- 너무 길면: 실시간성 저하
- **30초**: 실시간성과 안정성 균형

**의심 IP (1분):**
- 매크로 탐지에는 충분한 시간
- 1분 내 10건 = 6초당 1건 = 명백히 비정상

**실시간 통계 (30초):**
- Grafana 대시보드 갱신 주기와 동기화
- 너무 짧으면 DB 부하, 너무 길면 실시간성 저하

### 4. PostgreSQL

**PostgreSQL 선택 이유:**
- ✅ 트랜잭션 지원 (데이터 일관성)
- ✅ 복잡한 집계 쿼리 성능 우수
- ✅ Grafana 네이티브 연동
- ✅ 인덱스를 통한 빠른 조회

---

## 🐛 트러블슈팅

### 문제 1: Kafka 연결 실패
```
Error: Connection to node -1 could not be established
```

**해결:**
```bash
# Docker 컨테이너 재시작
docker-compose down
docker-compose up -d

# 포트 확인
lsof -i :9092
```

---

### 문제 2: Spark Java Gateway 오류
```
Java gateway process exited before sending its port number
```

**해결:**
```bash
# Java 17 설치 (Mac)
brew install openjdk@17

# 환경변수 설정
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 확인
java -version
```

---

### 문제 3: DB 연결 오류
```
psycopg2.OperationalError: database "analytics_db" does not exist
```

**해결:**
```bash
# 데이터베이스 생성
python3 create_database.py

# 또는 수동 생성
docker exec -it <postgres-container> psql -U admin -d postgres
CREATE DATABASE analytics_db;
```

---

### 문제 4: 데이터가 Grafana에 안 보임

**체크리스트:**
1. ✅ Spark 실행 중인가? (`python3 spark_to_db.py`)
2. ✅ 주문 생성 중인가? (`python3 order_generator.py`)
3. ✅ DB에 데이터 있나?
   ```bash
   docker exec -it <postgres-container> psql -U admin -d analytics_db
   SELECT COUNT(*) FROM realtime_stats;
   ```
4. ✅ Grafana 쿼리 시간 범위 확인 (Last 10 minutes?)
5. ✅ Grafana 자동 새로고침 활성화 (5s 또는 10s)

---

### 문제 5: Docker 컨테이너가 시작 안 됨

**해결:**
```bash
# 기존 컨테이너 완전 삭제
docker-compose down -v

# 이미지 재다운로드
docker-compose pull

# 재시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

---

## 📚 참고 자료

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spark Structured Streaming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Grafana Tutorials](https://grafana.com/tutorials/)

---

## 🙏 핵심 역량

이 프로젝트는 공공기관에서의 빅데이터 플랫폼 경험을 바탕으로, 대기업/글로벌 기업에서 요구하는 실시간 데이터 파이프라인 역량을 증명하기 위해 제작되었습니다.

**핵심 역량:**
- ✅ Kafka를 활용한 실시간 메시징
- ✅ Spark Streaming 분산 처리
- ✅ PostgreSQL 스키마 설계 및 최적화
- ✅ Grafana 실시간 대시보드 구축
- ✅ Docker를 활용한 인프라 관리