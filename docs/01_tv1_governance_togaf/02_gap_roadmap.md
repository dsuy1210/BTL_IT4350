# 📑 HẠNG MỤC 2 - TV1: PHÂN TÍCH KHOẢNG CÁCH (GAP ANALYSIS) & LỘ TRÌNH CHUYỂN ĐỔI (ROADMAP)

## 1. Phân Tích Khoảng Cách (Gap Analysis)

Bảng so sánh chi tiết giữa Kiến trúc Hiện trạng (Baseline) và Kiến trúc Mục tiêu (Target):

| Tiêu chí so sánh | Hiện trạng (Baseline) | Mục tiêu (Target Architecture) | Khoảng cách cần giải quyết (Gap) | Thành phần phụ trách (5 Core Services) |
|---|---|---|---|---|
| **Thu thập dữ liệu Tuyển sinh & Việc làm** | Xuất file Excel thủ công mỗi năm 1-2 lần, lưu trữ phân tán. | Tự động hóa trích xuất và đồng bộ theo lô định kỳ vào kho dữ liệu. | Thiếu module tự động hóa ingest dữ liệu lô và chuẩn hóa định dạng. | `Batch Ingestion Service` |
| **Thu thập dữ liệu LMS & Điểm số** | Dữ liệu nằm nguyên trong DB của LMS và Đào tạo; chỉ xem qua giao diện riêng. | Nhận sự kiện thời gian thực (CDC / Webhook) ngay khi có biến động điểm hoặc nộp bài. | Thiếu Gateway tiếp nhận luồng sự kiện tốc độ cao và lọc trùng. | `Stream Ingestion Gateway` |
| **Tổng hợp Hồ sơ Sinh viên** | Không có góc nhìn 360; tra cứu thông tin phải đăng nhập 4 hệ thống khác nhau. | Một hồ sơ thống nhất (Single Source of Truth) lưu lịch sử học tập, hoạt động, khảo sát. | Thiếu Data Hub & Service hợp nhất dữ liệu đa nguồn. | `Student 360 Profile Service` |
| **Cơ chế Cảnh báo học vụ** | Họp xét cảnh cáo học vụ sau khi kết thúc học kỳ (đã muộn). | Phát hiện nguy cơ tức thì (độ trễ < 30 giây) khi phát sinh điểm liệt hoặc bỏ LMS. | Thiếu động cơ đánh giá quy tắc luồng sự kiện (Rule Engine). | `Fast Alerting Engine` |
| **Giao diện tương tác & Thông báo** | Email thủ công hoặc thông báo giấy dán bảng tin. | Dashboard trực quan cho Cố vấn học tập, Cổng thông tin cho sinh viên, bắn Multi-channel Alert. | Thiếu Portal thống nhất và kênh Notification tự động. | `Academic Portal & Notification Service` |

---

## 2. Lộ Trình Chuyển Đổi (Implementation & Migration Roadmap)

Dự án được chia làm 3 giai đoạn (Phases) liên tục:

```
[Phase 1: Xây Dựng Nền Tảng & Batch Data Hub]
  └─► Thu thập Tuyển sinh + Xây dựng Student 360 Profile Service + Dashboard xem hồ sơ cơ bản
        │
        ▼
[Phase 2: Triển Khai Luồng Thời Gian Thực & Fast Alerting (Biến thể B)]
  └─► Xây dựng Stream Gateway + Tích hợp LMS, Điểm + Fast Alerting Engine (< 30s) + Xử lý Ngoại lệ
        │
        ▼
[Phase 3: Hoàn Thiện, Tối Ưu Hóa & Tích Hợp Việc Làm]
  └─► Tích hợp Career & Alumni System + Tối ưu hóa hiệu năng, bảo mật + Đánh giá mô hình dự báo AI
```

### Chi tiết 3 Giai đoạn:
1. **Giai đoạn 1 (Phase 1) - Tuần 1-12 (MVP Nền tảng):**
   - Triển khai `Batch Ingestion Service` và `Student 360 Profile Service`.
   - Kết nối nguồn dữ liệu `Admission System`.
   - Xây dựng giao diện cơ bản của `Academic Portal` để tra cứu hồ sơ sinh viên.
2. **Giai đoạn 2 (Phase 2) - Tuần 13-24 (Trọng tâm Biến thể B - Real-time & Cảnh báo nhanh):**
   - Triển khai `Stream Ingestion Gateway` (Apache Kafka/RabbitMQ) và `Fast Alerting Engine`.
   - Tích hợp luồng sự kiện tức thì từ `LMS System` và `Grading System`.
   - Hoàn thiện tính năng thông báo tức thì (< 30s) và xử lý ngoại lệ thu hồi/sửa điểm.
3. **Giai đoạn 3 (Phase 3) - Tuần 25-36 (Tích hợp Toàn diện & Mở rộng):**
   - Tích hợp `Career & Alumni System` để khép kín vòng đời sinh viên từ lúc vào trường đến khi đi làm.
   - Kiểm thử tải toàn diện (Stress Testing), hoàn thiện chính sách phân quyền bảo mật dữ liệu.

---

## 3. Sơ Đồ ArchiMate Implementation & Migration
<!-- Vẽ trên Archi hoặc Draw.io rồi xuất ảnh lưu vào diagrams/archimate_migration.png -->
- Biểu diễn mối quan hệ giữa các **Work Packages**, **Deliverables**, **Plateaus** (Baseline Plateau $\rightarrow$ Transition Plateau 1 $\rightarrow$ Transition Plateau 2 $\rightarrow$ Target Plateau), và các **Gaps**.
