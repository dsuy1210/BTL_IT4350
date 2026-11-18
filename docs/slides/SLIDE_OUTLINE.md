# 🖥️ KHUNG SLIDE BẢO VỆ ĐỒ ÁN (10 - 12 SLIDES)
### Môn học: Kiến trúc Hệ thống Thông tin và Ứng dụng (IT4350)
### Đề tài: Student 360 & Data Hub — Biến thể B: Cảnh báo nhanh

---

## PHÂN BỔ TRANG SLIDE THEO THÀNH VIÊN

```
[TV1: Trang 1-2] ──► [TV2: Trang 3-6] ──► [TV3: Trang 7-10] ──► [TV1: Trang 11-12]
 (Bối cảnh/TOGAF)     (Nghiệp vụ & UI)     (Công nghệ & API)    (Lộ trình & Rủi ro)
```

---

### 🟢 PHẦN 1: TỔNG QUAN, BỐI CẢNH & TẦM NHÌN (TV1 phụ trách)
- **Slide 1: Trang tiêu đề & Giới thiệu nhóm**
  - Tên đề tài: Chủ đề VIII - Student 360 & Data Hub (Biến thể B: Cảnh báo nhanh).
  - Tên nhóm, danh sách 3 thành viên và phân công vai trò (TV1, TV2, TV3).
  - Giáo viên hướng dẫn.
- **Slide 2: Bối cảnh, Động lực & Tầm nhìn Kiến trúc (TOGAF Motivation)**
  - Nỗi đau của trường: Dữ liệu phân mảnh 4 hệ thống, phát hiện nguy cơ học vụ quá muộn.
  - Sơ đồ ArchiMate tầng Motivation (Stakeholders $\rightarrow$ Drivers $\rightarrow$ Goals $\rightarrow$ REQ-01, REQ-02, REQ-03).
  - Mục tiêu chuyển đổi từ *Bị động cuối kỳ* sang *Chủ động cảnh báo tức thì*.

---

### 🔵 PHẦN 2: KIẾN TRÚC NGHIỆP VỤ, DỮ LIỆU & MOCK UI (TV2 phụ trách)
- **Slide 3: Quy trình Nghiệp vụ Luồng chính End-to-End (BPMN 1)**
  - Hình ảnh sơ đồ BPMN: Giảng viên nhập điểm $\rightarrow$ Gateway $\rightarrow$ Cập nhật 360 Profile $\rightarrow$ Phát hiện cảnh báo $\rightarrow$ Cố vấn học tập can thiệp.
  - Sự kết hợp giữa 5 Core Services và 6 Data Objects đã chốt ở Hợp đồng chung.
- **Slide 4: Kiến trúc Ứng dụng & Cấu trúc Dữ liệu Student 360**
  - Sơ đồ ArchiMate Business & Application Layer.
  - Sơ đồ C4 Container: Cách 4 nguồn (Tuyển sinh, LMS, Điểm, Việc làm) được tích hợp về Data Hub.
- **Slide 5: Quyết định Kiến trúc ADR 01 (Tích hợp Data Hub)**
  - Bảng so sánh Phương án 1 (Batch ETL truyền thống) vs Phương án 2 (Hybrid Integration: Batch + CDC/Stream).
  - Lý do chọn Phương án 2: Thỏa mãn yêu cầu thời gian thực của Biến thể B.
- **Slide 6: Demo Prototype Mock UI (Giao diện Web)**
  - Ảnh chụp màn hình Dashboard phân tích nguy cơ sinh viên.
  - Ảnh chụp chi tiết Hồ sơ Student 360 tổng hợp.
  - Pop-up hiển thị thông báo cảnh báo tức thì (< 30s) trên Portal của Cố vấn.

---

### 🟠 PHẦN 3: KIẾN TRÚC CÔNG NGHỆ, NGOẠI LỆ & MOCK API (TV3 phụ trách)
- **Slide 7: Kiến trúc Công nghệ & Hạ tầng Low-Latency**
  - Sơ đồ ArchiMate Technology Layer: Kafka Streaming Cluster, Redis Cache, Postgres/Mongo, Webhook Gateway.
  - Cơ chế kỹ thuật đảm bảo SLA độ trễ < 30 giây (Thực tế đạt ~1.5 - 3 giây).
- **Slide 8: Quyết định Kiến trúc ADR 02 (Cơ chế Đánh giá Luật Cảnh báo)**
  - Bảng so sánh Cronjob Polling Database vs In-Memory Stream Rule Engine.
  - Phân tích hiệu năng, tải CPU/RAM và khả năng mở rộng.
- **Slide 9: Luồng Ngoại lệ Nghiệp vụ (BPMN 2) & Idempotency**
  - Xử lý bản tin trùng lặp bằng Redis SETNX Hash Key.
  - Luồng tự động thu hồi/hạ mức cảnh báo khi giảng viên điều chỉnh sửa điểm.
- **Slide 10: Demo Prototype Mock API & Kiểm chứng Tình huống Bất thường**
  - Kịch bản kiểm chứng: Giảng viên nhập nhầm điểm 2.0 $\rightarrow$ Phát cảnh báo trong 2 giây $\rightarrow$ Giảng viên sửa lại 8.5 $\rightarrow$ Cảnh báo tự động chuyển sang `REVOKED`.
  - Kết quả log API và Swagger / Terminal test.

---

### 🟢 PHẦN 4: LỘ TRÌNH CHUYỂN ĐỔI, QUẢN TRỊ RỦI RO & TỔNG KẾT (TV1 phụ trách)
- **Slide 11: Gap Analysis & Lộ trình Chuyển đổi 3 Giai đoạn**
  - Bảng Gap Analysis giữa Hiện trạng và Mục tiêu.
  - Roadmap 3 Phase (Phase 1: Nền tảng Batch $\rightarrow$ Phase 2: Stream & Fast Alerting $\rightarrow$ Phase 3: Hoàn thiện việc làm).
  - Sơ đồ ArchiMate Implementation & Migration.
- **Slide 12: Ma trận Truy vết (Traceability), Rủi ro & Kết luận**
  - Bảng Traceability Matrix chứng minh đáp ứng trọn vẹn `REQ-01`, `REQ-02`, `REQ-03`.
  - 06-08 rủi ro và giải pháp đối sách.
  - Lời cảm ơn và hỏi đáp (Q&A).
