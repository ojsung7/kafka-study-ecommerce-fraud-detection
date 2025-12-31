import psutil
import time
import csv
from datetime import datetime

print("📊 시스템 모니터링 시작...")
print("=" * 60)

# CSV 파일 생성
csv_file = open('performance_metrics.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow([
    'timestamp', 
    'cpu_percent', 
    'memory_percent', 
    'memory_used_mb',
    'disk_read_mb',
    'disk_write_mb',
    'network_sent_mb',
    'network_recv_mb'
])

print(f"{'시간':<20} {'CPU':<10} {'메모리':<10} {'메모리(MB)':<12} {'디스크 R/W':<15}")
print("-" * 80)

# 초기 값
disk_io_prev = psutil.disk_io_counters()
net_io_prev = psutil.net_io_counters()

try:
    while True:
        # CPU, 메모리
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_mb = memory.used / (1024 * 1024)
        
        # 디스크 I/O
        disk_io = psutil.disk_io_counters()
        disk_read_mb = (disk_io.read_bytes - disk_io_prev.read_bytes) / (1024 * 1024)
        disk_write_mb = (disk_io.write_bytes - disk_io_prev.write_bytes) / (1024 * 1024)
        disk_io_prev = disk_io
        
        # 네트워크
        net_io = psutil.net_io_counters()
        net_sent_mb = (net_io.bytes_sent - net_io_prev.bytes_sent) / (1024 * 1024)
        net_recv_mb = (net_io.bytes_recv - net_io_prev.bytes_recv) / (1024 * 1024)
        net_io_prev = net_io
        
        # 현재 시간
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 콘솔 출력
        print(f"{now:<20} {cpu_percent:>6.1f}%  {memory_percent:>7.1f}%  "
              f"{memory_used_mb:>10.0f}  R:{disk_read_mb:>4.1f}/W:{disk_write_mb:>4.1f}")
        
        # CSV 저장
        csv_writer.writerow([
            now,
            cpu_percent,
            memory_percent,
            memory_used_mb,
            disk_read_mb,
            disk_write_mb,
            net_sent_mb,
            net_recv_mb
        ])
        csv_file.flush()
        
        time.sleep(5)  # 5초마다 측정
        
except KeyboardInterrupt:
    print("\n\n📊 모니터링 종료")
    csv_file.close()
    print(f"결과 저장: performance_metrics.csv")