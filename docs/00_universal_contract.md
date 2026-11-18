# 📜 BƯỚC 0: "HỢP ĐỒNG CHUNG" (UNIVERSAL CONTRACT)
### Môn học: Kiến trúc Hệ thống Thông tin và Ứng dụng (IT4350)
### Chủ đề VIII: Student 360 & Data Hub — Biến thể B: Cảnh báo nhanh

> ⚠️ **LƯU Ý CỐT TỬ**: Đây là bộ từ điển danh pháp và thông số chuẩn được chốt cứng cho toàn bộ dự án. Cả 3 thành viên khi vẽ BPMN, vẽ ArchiMate, viết ADR, code Mock UI hay Mock API **BẮT BUỘC** sử dụng chính xác 100% các định danh dưới đây để đảm bảo tính nhất quán và không ai phải chờ ai.

---

## 1. 4 Nguồn Dữ Liệu Đầu Vào (External Systems)

| STT | Tên chuẩn tiếng Anh | Tên tiếng Việt | Phương thức tích hợp | Tần suất / Đặc tính |
|:---:|:---|:---|:---|:---|
| **EXT-01** | `Admission System` | Hệ thống Tuyển sinh | Batch Integration (File/API Lô) | Đồng bộ định kỳ (Đầu kỳ / Hàng ngày) |
| **EXT-02** | `Career & Alumni System` | Hệ thống Việc làm & Cựu sinh viên | Batch Integration (File/API Lô) | Đồng bộ định kỳ (Theo tháng / Cuối kỳ) |
| **EXT-03** | `LMS System` | Hệ thống Học trực tuyến (Moodle/Canvas) | Real-time Event Streaming (Webhook/Kafka) | Bắn sự kiện thời gian thực (Nộp bài, điểm danh, truy cập) |
| **EXT-04** | `Grading System` | Hệ thống Quản lý điểm số đào tạo | Real-time Event Streaming (CDC / API Event) | Bắn sự kiện thời gian thực ngay khi giảng viên nhập điểm |

---

## 2. 5 Thành Phần Lõi Hệ Thống (Core Application Services)

| STT | Tên chuẩn tiếng Anh | Chức năng chính | Vai trò trong kiến trúc |
|:---:|:---|:---|:---|
| **SVC-01** | `Batch Ingestion Service` | Thu thập, làm sạch và chuẩn hóa dữ liệu lô từ Tuyển sinh & Việc làm. | Data Ingestion Layer (Batch) |
| **SVC-02** | `Stream Ingestion Gateway` | Nhận sự kiện điểm/bài tập tức thì từ LMS và Hệ thống Điểm, lọc trùng & kiểm tra Idempotency. | Ingestion & Messaging Gateway |
| **SVC-03** | `Student 360 Profile Service` | Tổng hợp dữ liệu từ 4 nguồn thành hồ sơ 360 duy nhất, cung cấp API truy vấn hồ sơ toàn diện. | Core Data Hub & Master Profile |
| **SVC-04** | `Fast Alerting Engine` | Đánh giá quy tắc học vụ thời gian thực trên luồng sự kiện, phát hiện nguy cơ và phát cảnh báo nhanh. | Real-time Rule & Event Processing |
| **SVC-05** | `Academic Portal & Notification Service` | Cung cấp giao diện Web Dashboard cho Cố vấn học tập/Sinh viên và bắn thông báo tức thì (Email, Web Push, SMS). | Presentation & Notification Layer |

---

## 3. 6 Đối Tượng Dữ Liệu Chuẩn (Data Objects)

| STT | Tên Data Object | Mô tả & Thuộc tính cốt lõi | Nguồn phát sinh |
|:---:|:---|:---|:---|
| **DO-01** | `Admission Record` | Thông tin tuyển sinh ban đầu: `student_id`, `full_name`, `entry_year`, `major`, `admission_score`, `high_school`. | Admission System |
| **DO-02** | `LMS Activity Log` | Nhật ký hoạt động học tập: `activity_id`, `student_id`, `course_id`, `login_time`, `assignment_status`, `last_access`. | LMS System |
| **DO-03** | `Grade Event` | Sự kiện phát sinh điểm số: `event_id`, `student_id`, `course_id`, `exam_type`, `score`, `timestamp`, `version`. | Grading System |
| **DO-04** | `Employment Record` | Tình trạng việc làm sau tốt nghiệp: `alumni_id`, `company`, `role`, `salary_bracket`, `survey_year`. | Career & Alumni System |
| **DO-05** | `Student 360 Profile` | Bản ghi hồ sơ tổng hợp: chứa toàn bộ lịch sử điểm (GPA, CPA), tiến độ tín chỉ, cảnh cáo học vụ, hoạt động LMS và dự báo rủi ro. | Student 360 Profile Service |
| **DO-06** | `Academic Alert` | Bản ghi cảnh báo học vụ: `alert_id`, `student_id`, `severity` (INFO/WARNING/CRITICAL), `trigger_reason`, `latency_seconds`, `status` (ACTIVE/REVOKED/RESOLVED). | Fast Alerting Engine |

---

## 4. 3 Yêu Cầu Cốt Lõi Dùng Để Truy Vết (Traceability IDs)

```
[REQ-01: Tích hợp Đa nguồn Student 360] 
     │
     ├──► [REQ-02: Luồng chính Biến thể B - Cảnh báo nhanh < 30s]
     │
     └──► [REQ-03: Luồng ngoại lệ Biến thể B - Chống trùng lặp & Thu hồi khi sửa điểm]
```

- **`REQ-01` (Tích hợp đa nguồn tạo hồ sơ Student 360 & Dashboard):**
  - Hệ thống phải tích hợp thành công dữ liệu từ cả 4 nguồn (Tuyển sinh, LMS, Điểm, Việc làm).
  - Tổng hợp thành một hồ sơ duy nhất (Single Source of Truth) cho mỗi sinh viên.
  - Hiển thị trực quan trên Academic Portal Dashboard cho Cố vấn học tập và Ban Giám hiệu.

- **`REQ-02` (Biến thể B - Luồng chính: Phát hiện nguy cơ & Cảnh báo nhanh tức thì):**
  - Tự động phát hiện sinh viên có điểm kém (điểm trắc nghiệm/giữa kỳ < 3.0) hoặc bỏ học trên LMS (> 14 ngày không tương tác).
  - Đánh giá luật cảnh báo và phát Academic Alert đến Cố vấn học tập trong thời gian ngắn: **SLA Độ trễ < 30 giây** kể từ khi sự kiện phát sinh.

- **`REQ-03` (Biến thể B - Luồng ngoại lệ: Xử lý sự kiện trùng lặp & Sửa điểm):**
  - **Chống trùng lặp (Idempotency):** Xử lý an toàn khi LMS/Hệ thống điểm gửi nhiều lần cùng một bản tin do mạng chập chờn (Network Retry).
  - **Sửa điểm/Thu hồi:** Trường hợp giảng viên sửa lại điểm số ngay sau khi hệ thống vừa phát cảnh báo (ví dụ sửa từ 2.0 thành 8.0), hệ thống phải tự động cập nhật lại Student 360 Profile và chuyển trạng thái bản ghi `Academic Alert` sang `REVOKED` (Thu hồi) hoặc cập nhật hạ mức cảnh báo tức thì.

---

## 5. Ma Trận Phân Bổ Trách Nhiệm (RACI Matrix)

| Đầu mục công việc | TV1 (Governance) | TV2 (Core Flow & UI) | TV3 (Tech & API) |
|---|:---:|:---:|:---:|
| **Bối cảnh, Động lực, TOGAF Motivation** | **A / R** | C | I |
| **Architecture Baseline & Gap Analysis** | **A / R** | C | C |
| **Yêu cầu chức năng (FR) & BPMN Luồng chính** | I | **A / R** | C |
| **ArchiMate Business & Application Layer** | C | **A / R** | I |
| **Cấu trúc dữ liệu Student 360 & C4 Container** | I | **A / R** | C |
| **ADR 01: Kiến trúc Tích hợp Data Hub** | I | **A / R** | C |
| **Prototype Mock UI (Web Dashboard & Alert Popup)** | I | **A / R** | I |
| **Yêu cầu phi chức năng (NFR: Latency, Idempotency)** | I | C | **A / R** |
| **BPMN Luồng ngoại lệ (Sửa điểm, Trùng lặp)** | I | C | **A / R** |
| **ArchiMate Technology Layer & Hạ tầng Streaming** | C | I | **A / R** |
| **ADR 02: Cơ chế Luật Cảnh báo Nhanh (Rule Engine)** | I | C | **A / R** |
| **Prototype Mock API & Script Kiểm chứng Ngoại lệ** | I | I | **A / R** |
| **Roadmap Chuyển đổi & Quản trị Rủi ro** | **A / R** | I | C |
| **Ma trận truy vết (Traceability Matrix)** | **A / R** | C | C |
| **Tổng hợp Báo cáo 5 Chương & Ghép Slide hoàn chỉnh** | **A / R** | C | C |

*(Chú thích: R = Responsible - Người trực tiếp làm, A = Accountable - Người chịu trách nhiệm chính, C = Consulted - Người tham vấn góp ý, I = Informed - Người nhận thông tin)*
