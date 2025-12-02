"""
Script để generate báo cáo kết quả test từ Locust CSV files.
Sử dụng: python generate_report.py [path_to_csv_file]
"""

import sys
import csv
from datetime import datetime
from pathlib import Path


def parse_locust_csv(csv_file_path):
    """
    Parse Locust CSV file và extract statistics.
    
    Args:
        csv_file_path: Đường dẫn đến file CSV từ Locust
        
    Returns:
        dict: Dictionary chứa statistics
    """
    stats = {
        'endpoints': [],
        'aggregated': {}
    }
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row['Type'] == 'Aggregated':
                    stats['aggregated'] = {
                        'name': row['Name'],
                        'requests': int(row['Request Count']),
                        'failures': int(row['Failure Count']),
                        'avg_response_time': float(row['Average Response Time']),
                        'min_response_time': float(row['Min Response Time']),
                        'max_response_time': float(row['Max Response Time']),
                        'median_response_time': float(row['Median Response Time']),
                        'p95_response_time': float(row['95%']),
                        'p99_response_time': float(row['99%']),
                        'rps': float(row['Requests/s'])
                    }
                else:
                    endpoint_stats = {
                        'type': row['Type'],
                        'name': row['Name'],
                        'requests': int(row['Request Count']),
                        'failures': int(row['Failure Count']),
                        'avg_response_time': float(row['Average Response Time']),
                        'min_response_time': float(row['Min Response Time']),
                        'max_response_time': float(row['Max Response Time']),
                        'median_response_time': float(row['Median Response Time']),
                        'p95_response_time': float(row['95%']),
                        'p99_response_time': float(row['99%']),
                        'rps': float(row['Requests/s'])
                    }
                    stats['endpoints'].append(endpoint_stats)
    
    except FileNotFoundError:
        print(f"Error: File {csv_file_path} not found!")
        return None
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return None
    
    return stats


def generate_markdown_report(stats, output_file='../results/result.md'):
    """
    Generate markdown report từ statistics.
    
    Args:
        stats: Dictionary chứa statistics
        output_file: Đường dẫn file output
    """
    if not stats:
        print("No statistics to generate report!")
        return
    
    report = f"""# 📊 Báo Cáo Kết Quả Stress Test - Context Handling Robot API

**Ngày test:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Test Tool:** Locust 2.42.6  
**Target Server:** http://103.253.20.30:30020

---

## 🎯 Tổng Quan Test

### Test Configuration
- **Số Users:** 10 concurrent users
- **Spawn Rate:** 2 users/second
- **Duration:** 60 giây
- **Wait Time:** 1-3 giây giữa các requests

### API Endpoints Tested
1. **POST /v1/conversations/end** - Kết thúc conversation
2. **POST /v1/activities/suggest** - Gợi ý activities cho user

---

## 📈 Kết Quả Test

### Screenshot 1: Statistics Overview
![Test Results Overview](image/result/1764646884789.png)

### Screenshot 2: Detailed Metrics
![Detailed Metrics](image/result/1764646907322.png)

---

## 📊 Phân Tích Chi Tiết

### 1. Performance Metrics

"""
    
    # Thêm thông tin cho từng endpoint
    for endpoint in stats['endpoints']:
        failure_rate = (endpoint['failures'] / endpoint['requests'] * 100) if endpoint['requests'] > 0 else 0
        
        report += f"""
#### **{endpoint['type']} {endpoint['name']}**
- **Total Requests:** {endpoint['requests']:,}
- **Failures:** {endpoint['failures']} ({failure_rate:.2f}%)
- **Average Response Time:** {endpoint['avg_response_time']:.2f} ms
- **Min Response Time:** {endpoint['min_response_time']:.2f} ms
- **Max Response Time:** {endpoint['max_response_time']:.2f} ms
- **Median (50th percentile):** {endpoint['median_response_time']:.2f} ms
- **95th percentile:** {endpoint['p95_response_time']:.2f} ms
- **99th percentile:** {endpoint['p99_response_time']:.2f} ms
- **Requests per Second (RPS):** {endpoint['rps']:.2f} req/s

"""
    
    # Thêm thông tin aggregated
    agg = stats['aggregated']
    failure_rate = (agg['failures'] / agg['requests'] * 100) if agg['requests'] > 0 else 0
    
    report += f"""
#### **Aggregated (Tổng Hợp)**
- **Total Requests:** {agg['requests']:,}
- **Total Failures:** {agg['failures']} ({failure_rate:.2f}%)
- **Average Response Time:** {agg['avg_response_time']:.2f} ms
- **Min Response Time:** {agg['min_response_time']:.2f} ms
- **Max Response Time:** {agg['max_response_time']:.2f} ms
- **Median (50th percentile):** {agg['median_response_time']:.2f} ms
- **95th percentile:** {agg['p95_response_time']:.2f} ms
- **99th percentile:** {agg['p99_response_time']:.2f} ms
- **Total RPS:** {agg['rps']:.2f} req/s

---

## ✅ Đánh Giá Kết Quả

### Performance Assessment

#### Response Time Analysis
"""
    
    # Phân tích response time
    avg_time = agg['avg_response_time']
    p95_time = agg['p95_response_time']
    
    if avg_time < 200:
        avg_status = "✅ Excellent"
    elif avg_time < 500:
        avg_status = "✅ Good"
    elif avg_time < 1000:
        avg_status = "⚠️ Acceptable"
    else:
        avg_status = "❌ Poor"
    
    if p95_time < 500:
        p95_status = "✅ Excellent"
    elif p95_time < 1000:
        p95_status = "✅ Good"
    elif p95_time < 2000:
        p95_status = "⚠️ Acceptable"
    else:
        p95_status = "❌ Poor"
    
    report += f"""
- **Average Response Time:** {avg_time:.2f} ms - {avg_status}
- **95th Percentile:** {p95_time:.2f} ms - {p95_status}

#### Failure Analysis
- **Total Failures:** {agg['failures']}
- **Failure Rate:** {failure_rate:.2f}%
"""
    
    if failure_rate == 0:
        report += "- **Status:** ✅ No failures - Perfect!\n"
    elif failure_rate < 1:
        report += "- **Status:** ✅ Good - Minimal failures\n"
    elif failure_rate < 5:
        report += "- **Status:** ⚠️ Acceptable - Some failures need investigation\n"
    else:
        report += "- **Status:** ❌ Poor - High failure rate, needs immediate attention\n"
    
    report += f"""
#### Throughput Analysis
- **Average RPS:** {agg['rps']:.2f} req/s
- **RPS Status:** {'✅ Stable' if agg['rps'] > 0 else '❌ No requests'}
- **Total Requests:** {agg['requests']:,} requests

---

## 🎯 Kết Luận

### ✅ Điểm Mạnh
"""
    
    strengths = []
    if failure_rate == 0:
        strengths.append("Không có failures - API hoạt động ổn định")
    if avg_time < 500:
        strengths.append(f"Response time tốt ({avg_time:.2f}ms)")
    if agg['rps'] >= 5:
        strengths.append(f"Throughput tốt ({agg['rps']:.2f} RPS)")
    
    if strengths:
        for i, strength in enumerate(strengths, 1):
            report += f"{i}. {strength}\n"
    else:
        report += "1. Test đã hoàn thành\n"
    
    report += """
### ⚠️ Điểm Cần Cải Thiện
"""
    
    improvements = []
    if failure_rate > 0:
        improvements.append(f"Giảm failure rate từ {failure_rate:.2f}% xuống < 1%")
    if avg_time > 500:
        improvements.append(f"Tối ưu response time (hiện tại {avg_time:.2f}ms)")
    if p95_time > 1000:
        improvements.append(f"Cải thiện 95th percentile (hiện tại {p95_time:.2f}ms)")
    
    if improvements:
        for i, improvement in enumerate(improvements, 1):
            report += f"{i}. {improvement}\n"
    else:
        report += "1. Không có điểm nào cần cải thiện - Kết quả tốt!\n"
    
    report += f"""
### 📋 Khuyến Nghị
1. **Ngắn hạn:**
   - {'Kiểm tra và fix các failures' if failure_rate > 0 else 'Tiếp tục monitor performance'}
   - {'Tối ưu response time cho endpoint chậm' if avg_time > 500 else 'Maintain current performance'}

2. **Dài hạn:**
   - Scale up server nếu cần xử lý nhiều users hơn
   - Implement caching để giảm response time
   - Consider load balancing nếu RPS tăng cao

---

## 📊 Performance Summary

| Metric | Value | Status |
|--------|-------|--------|
| Total Requests | {agg['requests']:,} | ✅ |
| Total Failures | {agg['failures']} ({failure_rate:.2f}%) | {'✅' if failure_rate < 1 else '⚠️' if failure_rate < 5 else '❌'} |
| Average Response Time | {avg_time:.2f} ms | {'✅' if avg_time < 500 else '⚠️' if avg_time < 1000 else '❌'} |
| 95th Percentile | {p95_time:.2f} ms | {'✅' if p95_time < 1000 else '⚠️' if p95_time < 2000 else '❌'} |
| 99th Percentile | {agg['p99_response_time']:.2f} ms | {'✅' if agg['p99_response_time'] < 2000 else '⚠️'} |
| RPS | {agg['rps']:.2f} req/s | ✅ |

---

## 🔍 Chi Tiết Kỹ Thuật

### Test Environment
- **Locust Version:** 2.42.6
- **Test Duration:** 60 seconds
- **Concurrent Users:** 10
- **Spawn Rate:** 2 users/second

### Status Codes Accepted
- ✅ **200 OK** - Success
- ✅ **201 Created** - Success
- ✅ **202 Accepted** - Success (Async processing)

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Generated By:** Locust Report Generator Script
"""
    
    # Write to file
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Report generated successfully: {output_path}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <path_to_csv_file>")
        print("Example: python generate_report.py ../results/stats_20251202_103000.csv")
        return
    
    csv_file = sys.argv[1]
    stats = parse_locust_csv(csv_file)
    
    if stats:
        generate_markdown_report(stats)


if __name__ == '__main__':
    main()

