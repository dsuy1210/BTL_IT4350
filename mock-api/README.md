# ⚙️ PROTOTYPE MOCK API - FAST ALERTING & EXCEPTION ENGINE
### Phụ trách: Thành viên 3 (Mốc Deadline Tuần 4)
### Môn học: Kiến trúc Hệ thống Thông tin và Ứng dụng (IT4350)

---

## 🌟 Giới Thiệu
Mock API Server được thiết kế chuyên biệt để giả lập và kiểm chứng:
1. **`SVC-02: Stream Ingestion Gateway`:** Cửa ngõ tiếp nhận luồng sự kiện điểm (`Grade Event`) và LMS (`LMS Activity Log`).
2. **`SVC-04: Fast Alerting Engine`:** Động cơ đánh giá quy tắc thời gian thực trên RAM, cam kết SLA độ trễ < 30 giây.
3. **`REQ-02` (Luồng chính):** Tự động phát hiện điểm kém (< 3.0) và sinh ra `Academic Alert` với trạng thái `ACTIVE`.
4. **`REQ-03A` (Luồng ngoại lệ Idempotency):** Lọc trùng lặp bản tin khi cùng một `event_id` được gửi nhiều lần.
5. **`REQ-03B` (Luồng ngoại lệ Revocation):** Giảng viên sửa điểm (version 2) $\rightarrow$ Tự động thu hồi cảnh báo cũ (`ACTIVE` $\rightarrow$ `REVOKED`) và cập nhật lại điểm vào hồ sơ 360.

---

## 🚀 Cách Chạy Mock API Server
Server được viết hoàn toàn bằng **Python Standard Library (`http.server`)**, có thể chạy ngay trên bất kỳ máy nào có cài Python 3 mà **không cần chạy `pip install`**:

### Bước 1: Khởi động Server
```bash
cd D:\BTL_IT4350\mock-api
python server.py
```
Máy chủ sẽ lắng nghe tại: `http://localhost:8000`

### Bước 2: Chạy bộ kiểm thử tự động (Automated Test Suite)
Mở một cửa sổ Terminal mới:
```bash
python mock-api\test_api.py
```
Bộ test sẽ tự động thực thi 3 kịch bản kiểm chứng và in kết quả chi tiết từng bước.

---

## 📡 Danh Sách Endpoints REST API

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/health` | Kiểm tra trạng thái hoạt động của 5 Core Services. |
| `GET` | `/api/v1/alerts` | Lấy danh sách toàn bộ Academic Alert (ACTIVE, REVOKED, RESOLVED). |
| `GET` | `/api/v1/students/{id}/profile` | Lấy dữ liệu hồ sơ Student 360 của sinh viên. |
| `POST` | `/api/v1/stream/grades` | Đẩy sự kiện điểm số (Grade Event) vào luồng xử lý. |
| `POST` | `/api/v1/reset` | Xóa trắng dữ liệu state bộ nhớ tạm thời để test lại từ đầu. |

---

## 🧪 Kịch Bản Test Mẫu Bằng cURL

### 1. Luồng chính REQ-02: Bắn điểm 2.5 kích hoạt Fast Alert
```bash
curl -X POST http://localhost:8000/api/v1/stream/grades \
  -H "Content-Type: application/json" \
  -d "{\"event_id\":\"EVT-001\",\"event_type\":\"GRADE_SUBMITTED\",\"student_id\":\"20210001\",\"course_id\":\"IT4350\",\"score\":2.5,\"version\":1}"
```

### 2. Luồng ngoại lệ REQ-03A: Gửi lại đúng bản tin trên (Kiểm tra chống trùng lặp)
```bash
curl -X POST http://localhost:8000/api/v1/stream/grades \
  -H "Content-Type: application/json" \
  -d "{\"event_id\":\"EVT-001\",\"event_type\":\"GRADE_SUBMITTED\",\"student_id\":\"20210001\",\"course_id\":\"IT4350\",\"score\":2.5,\"version\":1}"
```
*Kết quả:* Trả về `"is_duplicate": true` và bỏ qua, không sinh cảnh báo lặp!

### 3. Luồng ngoại lệ REQ-03B: Giảng viên sửa điểm thành 8.5
```bash
curl -X POST http://localhost:8000/api/v1/stream/grades \
  -H "Content-Type: application/json" \
  -d "{\"event_id\":\"EVT-002\",\"event_type\":\"GRADE_UPDATED\",\"student_id\":\"20210001\",\"course_id\":\"IT4350\",\"score\":8.5,\"version\":2}"
```
*Kết quả:* Trả về `"alert_revoked": true`, cảnh báo cũ đổi trạng thái thành `REVOKED`!
