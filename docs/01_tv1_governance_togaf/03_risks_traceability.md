# 📑 HẠNG MỤC 3 - TV1: QUẢN TRỊ RỦI RO & BẢNG TRUY VẾT YÊU CẦU

## 1. Danh Mục Rủi Ro & Đối Sách Giảm Thiểu (Risk Catalog & Mitigation)

| Mã RR | Rủi ro tiềm ẩn (Risk) | Khả năng | Tác động | Mức độ | Đối sách giảm thiểu (Mitigation Strategy) | Thành phần liên quan |
|:---:|---|:---:|:---:|:---:|---|---|
| **RSK-01** | **Lệch định dạng dữ liệu (Data Drift / Inconsistency):** Dữ liệu mã SV, mã môn từ các hệ thống cũ không đồng nhất. | Cao | Cao | **Nghiêm trọng** | Xây dựng Schema Validation chuẩn trong `Batch Ingestion Service` & `Stream Ingestion Gateway`; sử dụng cơ chế Dead-Letter Queue (DLQ) cho bản tin lỗi. | Batch & Stream Ingestion |
| **RSK-02** | **Bão cảnh báo (Alert Fatigue / Storm):** Giảng viên nhập điểm 1.000 sinh viên cùng lúc kích hoạt hàng loạt cảnh báo gây quá tải cố vấn. | Trung bình | Cao | **Cao** | Thiết lập cơ chế gom nhóm (Throttling / Debouncing / Batch Notification) trong `Fast Alerting Engine`; chỉ gửi tổng hợp 1 thông báo tóm tắt cho cố vấn trong 5 phút. | Fast Alerting Engine |
| **RSK-03** | **Đứt gãy kết nối mạng với LMS:** Mạng trường bị nghẽn làm mất hoặc chậm trễ sự kiện nộp bài/điểm danh. | Trung bình | Cao | **Cao** | Sử dụng Message Broker phân tán (Kafka) có buffer bền vững (Persistence Log) trên đĩa; cơ chế Retry tự động với Exponential Backoff. | Stream Ingestion Gateway |
| **RSK-04** | **Lộ lọt dữ liệu nhạy cảm sinh viên (Data Privacy / Leak):** Điểm số hoặc thông tin cá nhân bị truy cập trái phép. | Thấp | Rất cao | **Cao** | Áp dụng RBAC (Role-Based Access Control), mã hóa dữ liệu khi lưu trữ (Encryption at Rest - AES256) và khi truyền tải (TLS 1.3), phân vùng truy cập cố vấn theo khoa/viện. | Academic Portal |
| **RSK-05** | **Xung đột khi giảng viên sửa điểm:** Giảng viên nhập nhầm điểm 0 rồi sửa lại điểm 10 ngay sau đó gây cảnh báo sai sự thật. | Cao | Trung bình | **Cao** | Hiện thực hóa yêu cầu `REQ-03`: cơ chế Event Versioning + Time-window Cancellation trong `Fast Alerting Engine` tự động thu hồi cảnh báo cũ. | Fast Alerting Engine |
| **RSK-06** | **Chậm trễ tiến độ do thiếu nhân sự:** Khối lượng công việc tích hợp lớn vượt quá thời hạn 4 tuần. | Trung bình | Trung bình | **Trung bình** | Chốt cứng "Hợp đồng chung" Bước 0 ngay từ Ngày 1 để 3 thành viên làm song song độc lập, không ai phải đợi ai. | Quy trình quản trị |
| **RSK-07** | **Quá tải bộ nhớ (OOM) của In-memory Rule Engine:** Lưu trữ quá nhiều trạng thái sự kiện trong RAM làm sập dịch vụ. | Thấp | Rất cao | **Cao** | Giới hạn sliding window (ví dụ: chỉ giữ trạng thái trong 15-30 phút), offload dữ liệu lịch sử sang Redis/PostgreSQL. | Fast Alerting Engine |

---

## 2. Bảng Ma Trận Truy Vết (Traceability Matrix)

Ma trận truy vết bảo đảm 100% các yêu cầu từ nghiệp vụ đến triển khai hạ tầng đều được kết nối chặt chẽ và không bị bỏ sót:

| Mã Yêu cầu (Traceability ID) | Tên Yêu cầu & Mục tiêu | Bên liên quan (Stakeholder) | Thành phần Core Service phụ trách | Đối tượng Dữ liệu (Data Objects) | Quyết định Kiến trúc (ADR) | Prototype kiểm chứng |
|:---:|---|---|---|---|:---:|:---:|
| **`REQ-01`** | **Tích hợp đa nguồn tạo hồ sơ Student 360 & Dashboard**<br>Tập trung hóa dữ liệu từ Tuyển sinh, LMS, Điểm và Việc làm thành một bản ghi duy nhất. | - Ban Giám hiệu<br>- Phòng Đào tạo<br>- Sinh viên | - `Batch Ingestion Service`<br>- `Student 360 Profile Service`<br>- `Academic Portal` | - `Admission Record`<br>- `Employment Record`<br>- `Student 360 Profile` | **ADR 01** (Data Hub Integration Pattern) | Giao diện Web Student 360 Profile & Analytics Dashboard (`mock-ui`) |
| **`REQ-02`** | **Luồng chính Biến thể B: Phát hiện nguy cơ & Cảnh báo nhanh < 30s**<br>Bắt sự kiện trắc nghiệm kém / bỏ học LMS và gửi thông báo tức thì cho Cố vấn học tập. | - Cố vấn học tập<br>- Sinh viên | - `Stream Ingestion Gateway`<br>- `Fast Alerting Engine`<br>- `Academic Portal & Notification Service` | - `Grade Event`<br>- `LMS Activity Log`<br>- `Academic Alert` | **ADR 02** (Real-time Rule Engine Pattern) | Pop-up Fast Alert trên UI (`mock-ui`) & Luồng API phát cảnh báo (`mock-api`) |
| **`REQ-03`** | **Luồng ngoại lệ Biến thể B: Xử lý trùng lặp & Sửa điểm**<br>Chống nhận sự kiện lặp (Idempotency) và tự động thu hồi/hạ mức cảnh báo khi giảng viên cập nhật điểm số. | - Cố vấn học tập<br>- Giảng viên | - `Stream Ingestion Gateway`<br>- `Fast Alerting Engine`<br>- `Student 360 Profile Service` | - `Grade Event`<br>- `Academic Alert` | **ADR 02** (Event Deduplication & Revocation) | Script giả lập gửi sự kiện trùng và API thu hồi cảnh báo (`mock-api`) |
