# 📑 TUẦN 2 - TV3: SƠ ĐỒ ARCHIMATE CÔNG NGHỆ & HẠ TẦNG LOW-LATENCY

## 1. Sơ Đồ ArchiMate Tầng Công Nghệ (Technology Layer)

Sơ đồ ArchiMate Technology mô tả chi tiết các **Node hạ tầng phần cứng / ảo hóa**, **Hệ thống phần mềm (System Software)**, **Mạng truyền thông (Communication Networks)** và cách chúng hiện thực hóa 5 Core Services:

### Các thành phần hạ tầng cốt lõi:
1. **API Gateway & Ingestion Cluster:**
   - Triển khai Kong API Gateway hoặc Envoy Proxy làm cửa ngõ tiếp nhận an toàn, rate-limiting, SSL termination.
   - Tiếp nhận Webhook từ LMS và API từ Grading System.
2. **Message Streaming Broker Cluster:**
   - Cụm **Apache Kafka** 3-node (hoặc RabbitMQ / Redpanda) quản lý các Topic:
     - `grades.events.raw`: Chứa toàn bộ sự kiện điểm thô.
     - `lms.activity.events`: Chứa nhật ký hành vi sinh viên.
     - `alerts.academic.events`: Chứa bản tin cảnh báo học vụ đã sinh ra.
     - `alerts.revocation.events`: Chứa bản tin thu hồi cảnh báo khi có sửa điểm.
3. **In-Memory Caching & State Store:**
   - **Redis Cluster** phục vụ 2 nhiệm vụ:
     - Lưu trữ Idempotency Keys (TTL = 24h) để chống trùng lặp bản tin.
     - Cache nhanh hồ sơ Student 360 để Rule Engine đọc với độ trễ micro-giây (< 2ms).
4. **Data Persistence Storage:**
   - **PostgreSQL Database:** Lưu trữ Master Profile, Bảng điểm chuẩn, Danh mục quy tắc học vụ, Lịch sử cảnh báo.
   - **MongoDB / MinIO:** Lưu trữ phi cấu trúc các payload nhật ký LMS raw và báo cáo khảo sát cựu sinh viên.
5. **Real-time Stream Engine Workers:**
   - Cụm Worker xử lý luồng (Python Stream Workers hoặc Apache Flink).

<!-- Vẽ trên phần mềm Archi hoặc Draw.io rồi lưu file ảnh vào diagrams/archimate_technology.png -->

---

## 2. Cơ Chế Kỹ Thuật Giúp Đạt Độ Trễ Thấp (SLA < 30 Giây)

Để đạt được cam kết độ trễ cực thấp trong Biến thể B, hệ thống áp dụng 4 kỹ thuật then chốt:

```
[Event Source]
     │ (CDC / Webhook < 500ms)
     ▼
[Kafka Streaming Broker]
     │ (Zero-copy network transfer < 100ms)
     ▼
[In-Memory Stream Rule Engine]  <───►  [Redis In-Memory State Cache] (< 2ms)
     │ (Đánh giá luật song song trong RAM < 50ms)
     ▼
[WebSocket Push Gateway]
     │ (Push thẳng tới UI Cố vấn < 200ms)
     ▼
[Cố Vấn Học Tập Nhìn Thấy Alert]  ===> TỔNG THỜI GIAN THỰC TẾ: ~ 1.5 - 3 GIÂY (Thỏa mãn xa SLA 30s)
```

1. **Kiến trúc Hướng sự kiện (Event-Driven Architecture) thay vì Quét định kỳ (Polling):**
   - Không dùng Cronjob quét database 5 phút hay 10 phút một lần.
   - Mỗi khi giảng viên nhấn "Lưu điểm", sự kiện được đẩy ngay lập tức qua hàng đợi streaming.
2. **Xử lý Luật trực tiếp trên Bộ nhớ RAM (In-Memory Processing):**
   - Động cơ luật tải trước danh sách sinh viên có nguy cơ và các ngưỡng điểm vào Redis Cache.
   - Khi sự kiện đến, việc so khớp ngưỡng thực hiện hoàn toàn trên RAM trong vòng < 5 mili-giây, không phải thực hiện các truy vấn SQL JOIN phức tạp vào ổ đĩa.
3. **Cơ chế Đẩy thời gian thực 2 chiều (Full-Duplex WebSocket Push):**
   - `Academic Portal` duy trì kết nối WebSocket thường trực với trình duyệt của Cố vấn học tập.
   - Khi có cảnh báo mới, máy chủ bắn trực tiếp (Push) dữ liệu xuống giao diện, không bắt trình duyệt phải gửi HTTP GET thăm dò định kỳ.
4. **Partitioning & Parallel Processing:**
   - Kafka Topic được phân mảnh (Partitions) theo `student_id % N_partitions`. Các worker xử lý song song độc lập, không gây nghẽn cổ chai ngay cả khi có hàng chục nghìn điểm thi được nhập cùng một lúc.
