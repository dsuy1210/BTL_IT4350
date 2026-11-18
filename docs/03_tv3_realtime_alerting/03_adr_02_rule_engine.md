# 📑 HẠNG MỤC 3 - TV3: KIẾN TRÚC QUYẾT ĐỊNH (ADR 02) & KIỂM CHỨNG TÌNH HUỐNG BẤT THƯỜNG
## ADR 02: Cơ Chế Xử Lý Luật Cảnh Báo Nhanh & Thu Hồi Ngoại Lệ

- **Mã định danh:** `ADR-02`
- **Trạng thái:** `ACCEPTED` (Đã phê duyệt)
- **Người đề xuất:** Thành viên 3 (Nhánh Biến thể B - Real-time & Hạ tầng)
- **Hạng mục:** Hạng mục 3 (Quyết định động cơ luật cảnh báo)
- **Yêu cầu liên quan:** `REQ-02` (Fast Alerting SLA < 30s), `REQ-03` (Biến thể B - Luồng ngoại lệ & Chống trùng lặp)

---

## 1. Bối Cảnh (Context)
Yêu cầu cốt lõi của Biến thể B đặt ra bài toán phát hiện sinh viên rơi vào tình trạng nguy hiểm học vụ (điểm kiểm tra kém, bỏ học LMS) và bắn thông báo tới Cố vấn học tập với độ trễ tối đa **30 giây**. Đồng thời, hệ thống phải xử lý mượt mà luồng ngoại lệ khi giảng viên sửa lại điểm số hoặc khi đường truyền mạng gây trùng lặp bản tin.

Cần lựa chọn mô hình kiến trúc tính toán luật (Rule Evaluation Architecture) phù hợp giữa tính đơn giản và hiệu năng thời gian thực.

---

## 2. So Sánh Các Phương Án (Options Comparison)

| Tiêu chí đánh giá | Phương án 1: Polling Database định kỳ (Scheduled Cronjob / Batch DB Queries) | Phương án 2: In-Memory Stream Rule Engine (Đánh giá trên Luồng Sự kiện) — **[CHỌN]** |
|---|---|---|
| **Cơ chế hoạt động** | Định kỳ (mỗi 1 phút, 5 phút hoặc 15 phút), một cronjob chạy các câu lệnh SQL SELECT nặng để quét toàn bộ bảng điểm tìm bản ghi có điểm < 3.0. | Mỗi sự kiện `Grade Event` hoặc `LMS Activity Log` khi đi qua Message Broker sẽ được đưa trực tiếp vào bộ nhớ RAM để Rule Engine so khớp tức thì. |
| **Độ trễ cảnh báo (Latency)** | **Cao & Dao động lớn (1 - 15 phút):** Phụ thuộc vào chu kỳ cronjob. Không thể đảm bảo SLA < 30 giây trong mọi thời điểm. | **Cực thấp (< 1 - 3 giây):** Sự kiện vừa sinh ra là luật được đánh giá ngay lập tức, thỏa mãn vượt trội SLA < 30s. |
| **Tải lên cơ sở dữ liệu** | **Rất nặng (I/O Bottleneck):** Quét bảng điểm hàng triệu dòng định kỳ gây nghẽn DB chính, làm chậm các thao tác nhập điểm của giảng viên. | **Rất nhẹ:** Chỉ đọc ghi các bản ghi cần thiết; trạng thái luật được cache trên Redis RAM. |
| **Khả năng xử lý Ngoại lệ & Thu hồi** | **Khó xử lý tức thì:** Phải so sánh diff giữa các lần quét để biết điểm nào vừa được sửa, dễ bỏ sót hoặc thu hồi trễ. | **Tự nhiên & Tức thì:** Sự kiện sửa điểm mang `version` cao hơn sẽ trigger luồng hủy cảnh báo cũ và phát sự kiện `REVOKED` ngay trong vài giây. |
| **Độ phức tạp hạ tầng** | Đơn giản, chỉ cần Cronjob / Celery worker. | Cần thêm Message Broker (Kafka/RabbitMQ) và In-Memory Cache (Redis). |

---

## 3. Quyết Định Kiến Trúc (Decision)
Nhóm quyết định chọn **Phương án 2: In-Memory Stream Rule Engine**.

- Sự kiện điểm số từ `Grading System` và LMS từ `LMS System` được stream trực tiếp qua `Stream Ingestion Gateway`.
- Động cơ luật `Fast Alerting Engine` sử dụng kỹ thuật State Cache (Redis) để:
  1. Kiểm tra mã băm bản tin chống trùng lặp (Idempotency).
  2. So khớp luật tức thì trong RAM.
  3. Quản lý trạng thái vòng đời của cảnh báo (`ACTIVE` $\rightarrow$ `REVOKED` khi có event sửa điểm mang version mới hơn).

---

## 4. Kiểm Chứng Tình Huống Bất Thường / Thay Đổi (Validation Scenario)

### Tình huống kiểm chứng:
> **"Giảng viên nhập nhầm điểm 2.0 cho sinh viên 20210001 môn IT4350 vào lúc 10:00:00, sau 45 giây (lúc 10:00:45) phát hiện ra và sửa lại thành 8.5."**

### Diễn biến hạ tầng & cách hệ thống xử lý:

1. **Lúc 10:00:00 - Nhập nhầm điểm:**
   - Giảng viên bấm lưu điểm 2.0. Hệ thống điểm phát `Grade Event` (event_id: `EVT-01`, student_id: `20210001`, course: `IT4350`, score: `2.0`, version: `1`).
   - `Stream Ingestion Gateway` nhận sự kiện lúc **10:00:01**, kiểm tra Redis thấy `EVT-01` chưa tồn tại $\rightarrow$ hợp lệ.
   - `Fast Alerting Engine` nhận sự kiện lúc **10:00:01.200**, thấy điểm 2.0 < 3.0 $\rightarrow$ sinh ngay bản ghi `Academic Alert` (id: `ALT-1001`, severity: `WARNING`, status: `ACTIVE`).
   - Lúc **10:00:02**, `Academic Portal` đẩy WebSocket tới Cố vấn học tập: Màn hình Cố vấn nhấp nháy cảnh báo đỏ. (Độ trễ thực tế: **2 giây** < 30s SLA).

2. **Lúc 10:00:45 - Giảng viên sửa điểm:**
   - Giảng viên nhập lại điểm 8.5. Hệ thống điểm phát `Grade Event` mới (event_id: `EVT-02`, student_id: `20210001`, course: `IT4350`, score: `8.5`, version: `2`, superseded_event_id: `EVT-01`).
   - `Stream Ingestion Gateway` nhận sự kiện lúc **10:00:46**, xác thực version 2 hợp lệ.
   - `Student 360 Profile Service` cập nhật lại điểm môn IT4350 thành 8.5 và tính lại CPA.
   - `Fast Alerting Engine` so khớp luật: Điểm 8.5 >= 3.0 (Không còn vi phạm).
   - Engine truy vấn Redis/DB thấy tồn tại alert `ALT-1001` đang `ACTIVE` gắn với môn IT4350 $\rightarrow$ Lập tức chuyển trạng thái `ALT-1001` thành **`REVOKED`** kèm lý do *"Điểm đã được giảng viên điều chỉnh từ 2.0 lên 8.5"*.
   - Lúc **10:00:47**, WebSocket push bản tin thu hồi xuống Portal. Màn hình Cố vấn tự động chuyển banner cảnh báo sang trạng thái gạch bỏ / màu xám đã thu hồi. (Thời gian xử lý thu hồi: **2 giây**).

> Chi tiết các payload JSON kiểm thử cho kịch bản này được định nghĩa tại `test_scenarios/exception_scenarios.json` và được thực thi bởi `mock-api/test_api.py`.
