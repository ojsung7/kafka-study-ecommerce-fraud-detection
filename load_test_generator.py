from confluent_kafka import Producer
import json
import time
import random
from datetime import datetime, timezone, timedelta
import sys

# KST 타임존 정의 (UTC+9)
KST = timezone(timedelta(hours=9))

# 부하 수준 설정 (커맨드 라인 인자로 받기)
if len(sys.argv) > 1:
    ORDERS_PER_SECOND = int(sys.argv[1])
else:
    ORDERS_PER_SECOND = 100  # 기본값: 초당 100건

SLEEP_TIME = 1.0 / ORDERS_PER_SECOND

# Kafka Producer 설정 (성능 최적화)
conf = {
    'bootstrap.servers': 'localhost:9092',
    'linger.ms': 10,  # 10ms 대기 후 배치 전송
    'batch.size': 16384,  # 배치 크기
    'compression.type': 'snappy',  # 압축
}

producer = Producer(conf)

# 상품 목록
products = [
    {"id": "P001", "name": "노트북", "price": 1500000},
    {"id": "P002", "name": "스마트폰", "price": 800000},
    {"id": "P003", "name": "이어폰", "price": 150000},
    {"id": "P004", "name": "마우스", "price": 30000},
    {"id": "P005", "name": "키보드", "price": 80000},
]

# 정상 사용자 IP 풀
normal_ips = [f"192.168.{random.randint(1,50)}.{random.randint(1,255)}" 
              for _ in range(100)]

# 의심스러운 IP (매크로 봇)
suspicious_ip = "192.168.99.99"

# 통계
total_sent = 0
failed_count = 0
start_time = time.time()

def delivery_report(err, msg):
    """메시지 전송 결과 콜백"""
    global failed_count
    if err is not None:
        failed_count += 1

def generate_order():
    """주문 생성 (90% 정상, 10% 의심)"""
    product = random.choice(products)
    
    if random.random() < 0.9:
        # 정상 주문
        return {
            "order_id": f"ORD{int(time.time() * 1000000)}",
            "timestamp": datetime.now(KST).isoformat(),
            "user_id": f"USER{random.randint(1000, 9999)}",
            "product_id": product["id"],
            "product_name": product["name"],
            "price": product["price"],
            "quantity": random.randint(1, 3),
            "ip_address": random.choice(normal_ips),
            "payment_method": random.choice(["card", "cash", "point"])
        }
    else:
        # 의심 주문
        return {
            "order_id": f"ORD{int(time.time() * 1000000)}",
            "timestamp": datetime.now(KST).isoformat(),
            "user_id": "USERBOT",
            "product_id": product["id"],
            "product_name": product["name"],
            "price": product["price"],
            "quantity": random.randint(5, 10),
            "ip_address": suspicious_ip,
            "payment_method": "card"
        }

print("🚀 고성능 주문 생성기 시작!")
print("=" * 60)
print(f"목표: 초당 {ORDERS_PER_SECOND:,}건")
print(f"대기 시간: {SLEEP_TIME * 1000:.2f}ms")
print("=" * 60)
print(f"{'경과시간':<12} {'전송건수':<12} {'초당처리':<12} {'실패':<8}")
print("-" * 60)

last_report_time = time.time()
last_report_count = 0

try:
    while True:
        order = generate_order()
        
        # Kafka로 전송
        producer.produce(
            'orders',
            key=order['order_id'],
            value=json.dumps(order).encode('utf-8'),
            callback=delivery_report
        )
        
        total_sent += 1
        
        # 비동기 전송 (버퍼에서 전송)
        producer.poll(0)
        
        # 1초마다 통계 출력
        current_time = time.time()
        if current_time - last_report_time >= 1.0:
            elapsed = current_time - start_time
            current_rate = (total_sent - last_report_count) / (current_time - last_report_time)
            avg_rate = total_sent / elapsed
            
            print(f"{elapsed:>10.1f}s  {total_sent:>10,}건  "
                  f"{current_rate:>9.1f}/s  {failed_count:>6}건")
            
            last_report_time = current_time
            last_report_count = total_sent
        
        # 부하 조절
        if SLEEP_TIME > 0:
            time.sleep(SLEEP_TIME)
        
except KeyboardInterrupt:
    print("\n" + "=" * 60)
    print("🛑 전송 중단")
    
    # 남은 메시지 전송
    print("📤 버퍼 비우는 중...")
    producer.flush()
    
    # 최종 통계
    total_time = time.time() - start_time
    avg_rate = total_sent / total_time
    
    print("\n📊 최종 통계:")
    print(f"  • 총 전송: {total_sent:,}건")
    print(f"  • 실패: {failed_count:,}건")
    print(f"  • 성공률: {(total_sent - failed_count) / total_sent * 100:.2f}%")
    print(f"  • 소요 시간: {total_time:.1f}초")
    print(f"  • 평균 처리율: {avg_rate:.1f}건/초")
    print("=" * 60)