# 📑 TUẦN 3 - TV2: KIẾN TRÚC QUYẾT ĐỊNH (ADR 01)
## ADR 01: Kiến Trúc Tích Hợp Đa Nguồn Về Data Hub Cho Student 360 & Cảnh Báo Nhanh

- **Mã định danh:** `ADR-01`
- **Trạng thái:** `ACCEPTED` (Đã phê duyệt)
- **Người đề xuất:** Thành viên 2 (Nhánh Luồng Chính & Dữ liệu)
- **Ngày quyết định:** Tuần 3
- **Yêu cầu liên quan:** `REQ-01` (Tích hợp đa nguồn Student 360), `REQ-02` (Biến thể B - Cảnh báo nhanh SLA < 30s)

---

## 1. Bối Cảnh (Context)
Hệ thống quản lý dữ liệu sinh viên cần tích hợp từ 4 nguồn dữ liệu độc lập:
1. `Admission System` (Hệ thống Tuyển sinh): Dữ liệu tĩnh, khối lượng vừa, chỉ biến động theo kỳ tuyển sinh.
2. `Career & Alumni System` (Hệ thống Việc làm): Dữ liệu khảo sát theo đợt, tần suất thấp (theo tháng/quý).
3. `Grading System` (Hệ thống Điểm): Dữ liệu phát sinh điểm thi, cần phản ánh nhanh khi có điểm mới.
4. `LMS System` (Hệ thống Học trực tuyến): Lưu lượng sự kiện lớn (nộp bài, tương tác, điểm danh).

Đặc biệt, theo yêu cầu của **Chủ đề VIII - Biến thể B (Cảnh báo nhanh)**: Khi phát sinh điểm kém hoặc dấu hiệu bỏ học trên LMS, hệ thống phải phát Academic Alert đến Cố vấn học tập trong thời gian ngắn (**SLA độ trễ < 30 giây**).

---

## 2. Các Phương Án Được Xem Xét (Options Considered)

### Phương án 1: Batch ETL Truyền Thống (Pure Batch ETL)
- **Mô tả:** Định kỳ (ví dụ mỗi đêm lúc 00:00 hoặc mỗi 4 tiếng), một tiến trình ETL (Extract - Transform - Load) bằng Apache Airflow / Python Script sẽ quét toàn bộ 4 cơ sở dữ liệu nguồn, trích xuất dữ liệu mới/thay đổi, làm sạch và ghi vào cơ sở dữ liệu Data Hub `Student 360 Profile Service`.
- **Ưu điểm:**
  - Kiến trúc đơn giản, quen thuộc, dễ cài đặt và bảo trì.
  - Ít tốn tài nguyên máy chủ thời gian thực.
  - Xử lý nhất quán dữ liệu lớn vào ban đêm mà không làm chậm các hệ thống tác nghiệp ban ngày.
- **Nhược điểm chí mạng:**
  - **Độ trễ dữ liệu rất cao (High Latency):** Dữ liệu có thể trễ từ 4 tiếng đến 24 tiếng.
  - **KHÔNG THỂ ĐÁP ỨNG BIẾN THỂ B:** Không thể phát hiện điểm kém hay bỏ học để cảnh báo trong < 30 giây. Sinh viên thi trượt sáng nay nhưng cố vấn chỉ biết vào sáng hôm sau.

---

### Phương án 2: Kiến Trúc Lai - Hybrid Integration (Batch + Event-Driven / CDC) — **[ĐƯỢC CHỌN]**
- **Mô tả:** Phân loại nguồn dữ liệu theo tính chất nghiệp vụ để áp dụng cơ chế tối ưu:
  1. **Nhánh Batch Ingestion Service:** Dành cho `Admission System` và `Career & Alumni System` (chạy đồng bộ định kỳ theo lô vì dữ liệu không yêu cầu thời gian thực).
  2. **Nhánh Stream Ingestion Gateway:** Dành cho `Grading System` và `LMS System` sử dụng Change Data Capture (Debezium/Kafka) hoặc Webhooks/API Event để đẩy sự kiện tức thì vào hàng đợi Message Broker.
- **Ưu điểm:**
  - **Thỏa mãn 100% SLA Biến thể B:** Dữ liệu điểm và hoạt động LMS được đẩy ngay lập tức qua stream, cho phép `Fast Alerting Engine` xử lý trong < 30 giây.
  - **Tối ưu tài nguyên:** Không lãng phí tài nguyên streaming cho những nguồn dữ liệu chỉ cần cập nhật định kỳ (Tuyển sinh, Cựu sinh viên).
  - **Giảm tải cho hệ thống nguồn:** Hệ thống tuyển sinh không phải duy trì cơ chế streaming phức tạp; hệ thống điểm đào tạo chỉ cần emit event hoặc stream log.
- **Nhược điểm:**
  - Phức tạp hơn về mặt kiến trúc: Phải duy trì cả 2 pipeline (Batch + Stream).
  - Cần giải quyết bài toán đồng bộ dữ liệu và kiểm tra trùng lặp (Idempotency) khi kết hợp dữ liệu lô và luồng.

---

## 3. Quyết Định Kiến Trúc (Decision)
Nhóm quyết định chọn **Phương án 2 (Kiến trúc Lai - Hybrid Integration)** làm kiến trúc tích hợp chính thức cho Data Hub.

- Triển khai `Batch Ingestion Service` (SVC-01) chuyên trách lấy dữ liệu định kỳ từ `Admission System` và `Career & Alumni System`.
- Triển khai `Stream Ingestion Gateway` (SVC-02) tiếp nhận luồng sự kiện từ `LMS System` và `Grading System`.
- Hợp nhất dữ liệu tại `Student 360 Profile Service` (SVC-03).

---

## 4. Hậu Quả & Đánh Đổi (Consequences & Trade-offs)

### Tác động tích cực:
- Đảm bảo tính khả thi tuyệt đối cho yêu cầu `REQ-02` (Độ trễ cảnh báo < 30 giây).
- Kiến trúc mở rộng linh hoạt: Có thể dễ dàng gắn thêm các nguồn sự kiện mới trong tương lai (Ví dụ: Thẻ thư viện, Cổng ra vào KTX).

### Đánh đổi chấp nhận (Trade-offs) & Giải pháp:
- **Độ phức tạp vận hành:** Cần cài đặt Message Broker (Apache Kafka/RabbitMQ) bên cạnh RDBMS truyền thống $\rightarrow$ Giải quyết bằng cách đóng gói Docker Compose và định nghĩa kịch bản triển khai rõ ràng.
- **Khả năng lệch thứ tự sự kiện:** Sự kiện cập nhật điểm có thể đến trước khi bản ghi sinh viên được tạo trong Batch $\rightarrow$ Giải pháp: `Stream Ingestion Gateway` có cơ chế đệm (Retry buffer) hoặc fallback tạo placeholder profile tạm thời.
