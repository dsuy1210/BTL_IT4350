# 📚 KHUNG BÁO CÁO TỔNG HỢP BÀI TẬP LỚN (FINAL REPORT OUTLINE)
### Môn học: Kiến trúc Hệ thống Thông tin và Ứng dụng (IT4350)
### Đề tài: Chủ đề VIII - Student 360 & Data Hub (Biến thể B: Cảnh báo nhanh)
**Dung lượng mục tiêu:** 25 - 35 trang | **Phụ trách ghép bài & format:** Thành viên 1 (Hạng mục 4)

---

## MỤC LỤC CHI TIẾT BÁO CÁO

### LỜI MỞ ĐẦU & DANH MỤC TỪ VIẾT TẮT (~1-2 trang)
- Danh mục thuật ngữ & 5 Core Services, 6 Data Objects (Trích từ `docs/00_universal_contract.md`).

---

### CHƯƠNG 1: BỐI CẢNH, ĐỘNG LỰC & TẦM NHÌN KIẾN TRÚC (~5-7 trang)
> **Thành viên phụ trách:** Thành viên 1
- **1.1 Bối cảnh bài toán & Khảo sát hiện trạng trường Đại học** (Từ `docs/01_tv1_governance_togaf/01_vision_motivation.md`)
  - Thực trạng 4 hệ thống dữ liệu phân mảnh (Siloed): Tuyển sinh, LMS, Điểm, Việc làm.
  - Các khó khăn trong việc phát hiện nguy cơ sinh viên bỏ học / trượt môn.
- **1.2 Các giả định của bài toán**
- **1.3 Phân tích các bên liên quan (Stakeholder Analysis)**
- **1.4 Tầng Động lực kiến trúc (TOGAF / ArchiMate Motivation Layer)**
  - Mục tiêu, động lực, kết quả mong đợi.
  - Ánh xạ 3 yêu cầu cốt lõi: `REQ-01`, `REQ-02`, `REQ-03`.
- **1.5 Tầm nhìn Kiến trúc mục tiêu (Architecture Vision) & Baseline**

---

### CHƯƠNG 2: KIẾN TRÚC NGHIỆP VỤ & ỨNG DỤNG/DỮ LIỆU STUDENT 360 (~8-10 trang)
> **Thành viên phụ trách:** Thành viên 2
- **2.1 Yêu cầu chức năng chi tiết (Functional Requirements - FR)** (Từ `docs/02_tv2_core_student360/01_fr_bpmn_core.md`)
- **2.2 Quy trình nghiệp vụ Luồng chính End-to-End (BPMN 1)**
  - Luồng tiếp nhận sự kiện $\rightarrow$ Cập nhật hồ sơ 360 $\rightarrow$ Đánh giá luật $\rightarrow$ Thông báo Cố vấn học tập.
- **2.3 Kiến trúc Ứng dụng & Nghiệp vụ (ArchiMate Business & Application Layer)** (Từ `docs/02_tv2_core_student360/02_archimate_c4_schema.md`)
  - Thể hiện rõ 5 Core Services và tương tác nghiệp vụ.
- **2.4 Kiến trúc Dữ liệu & Thiết kế Hồ sơ Student 360**
  - Cấu trúc dữ liệu tổng hợp từ 4 nguồn.
  - Sơ đồ C4 Container biểu diễn phân rã thành phần phần mềm.
- **2.5 Quyết định kiến trúc ADR 01** (Từ `docs/02_tv2_core_student360/03_adr_01_integration.md`)
  - So sánh Batch ETL truyền thống vs Hybrid Integration (Batch + CDC/Stream).
- **2.6 Thiết kế Giao diện Prototype Mock UI** (Từ `mock-ui/`)
  - Màn hình Dashboard phân tích, Hồ sơ Student 360 và Pop-up cảnh báo tức thì.

---

### CHƯƠNG 3: KIẾN TRÚC CÔNG NGHỆ & HẠ TẦNG REAL-TIME CẢNH BÁO NHANH (~6-8 trang)
> **Thành viên phụ trách:** Thành viên 3
- **3.1 Yêu cầu phi chức năng (NFR) cho Biến thể B** (Từ `docs/03_tv3_realtime_alerting/01_nfr_bpmn_exception.md`)
  - Cam kết độ trễ cảnh báo SLA < 30s, thông lượng chịu tải (Throughput), tính sẵn sàng (Availability).
- **3.2 Kiến trúc Hạ tầng Triển khai (ArchiMate Technology Layer)** (Từ `docs/03_tv3_realtime_alerting/02_archimate_tech_infra.md`)
  - Cụm Message Broker (Kafka/RabbitMQ), In-memory Cache (Redis), Cơ sở dữ liệu quan hệ & NoSQL.
- **3.3 Cơ chế Kỹ thuật Tối ưu Low-Latency**
  - Luồng truyền dữ liệu Zero-copy, Push WebSocket 2 chiều, xử lý RAM In-memory.
- **3.4 Quyết định kiến trúc ADR 02** (Từ `docs/03_tv3_realtime_alerting/03_adr_02_rule_engine.md`)
  - So sánh Polling Database định kỳ vs In-Memory Stream Rule Engine.

---

### CHƯƠNG 4: XỬ LÝ NGOẠI LỆ & KIỂM CHỨNG HỆ THỐNG (~5-6 trang)
> **Thành viên phụ trách:** Thành viên 3
- **4.1 Đặc tả Luồng Ngoại lệ Nghiệp vụ (BPMN 2)** (Từ `docs/03_tv3_realtime_alerting/01_nfr_bpmn_exception.md`)
  - Cơ chế chống trùng lặp sự kiện (Idempotency Key & Redis Hash).
  - Cơ chế đính chính / thu hồi cảnh báo học vụ khi giảng viên sửa điểm.
- **4.2 Kiểm chứng Tình huống Bất thường (Validation & Stress Test)**
  - Tình huống nhập 5.000 điểm đồng thời cuối kỳ.
  - Tình huống sửa điểm từ 2.0 lên 8.5 sau 45 giây.
- **4.3 Kết quả Thực nghiệm Prototype Mock API** (Từ `mock-api/`)
  - Log thực tế các request JSON, thời gian phản hồi API và trạng thái bản ghi cảnh báo.

---

### CHƯƠNG 5: PHÂN TÍCH KHOẢNG CÁCH, LỘ TRÌNH CHUYỂN ĐỔI & QUẢN TRỊ RỦI RO (~5-6 trang)
> **Thành viên phụ trách:** Thành viên 1
- **5.1 Phân tích khoảng cách (Gap Analysis)** (Từ `docs/01_tv1_governance_togaf/02_gap_roadmap.md`)
  - Đối chiếu hiện trạng rời rạc vs Kiến trúc mục tiêu 5 Core Services.
- **5.2 Lộ trình chuyển đổi (Implementation & Migration Roadmap)**
  - 3 Giai đoạn (Phase 1: Nền tảng Batch $\rightarrow$ Phase 2: Stream & Cảnh báo nhanh $\rightarrow$ Phase 3: Hoàn thiện việc làm).
  - Sơ đồ ArchiMate Implementation & Migration.
- **5.3 Danh mục Quản trị Rủi ro & Đối sách (Risk Management & Mitigation)** (Từ `docs/01_tv1_governance_togaf/03_risks_traceability.md`)
  - 7 rủi ro trọng yếu (Lệch dữ liệu, bão cảnh báo, đứt mạng LMS, lộ lọt thông tin...).
- **5.4 Ma trận Truy vết Yêu cầu (Traceability Matrix)**
  - Chứng minh sự liên kết xuyên suốt của `REQ-01`, `REQ-02`, `REQ-03`.

---

### KẾT LUẬN & HƯỚNG PHÁT TRIỂN (~1 trang)
- Tóm tắt kết quả đạt được của dự án.
- Đóng góp của từng thành viên trong nhóm.
- Tài liệu tham khảo.
