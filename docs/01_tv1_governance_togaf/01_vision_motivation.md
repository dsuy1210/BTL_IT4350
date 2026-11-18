# 📑 HẠNG MỤC 1 - TV1: BỐI CẢNH, ĐỘNG LỰC & TẦM NHÌN KIẾN TRÚC (CHƯƠNG 1)

## 1. Bối Cảnh Tổ Chức & Bài Toán (Organizational Context)
- **Tên tổ chức giả định:** Trường Đại học Công nghệ / Đại học Bách Khoa Quốc gia.
- **Quy mô:** ~25.000 sinh viên chính quy, 1.200 giảng viên, 45 chuyên ngành đào tạo.
- **Thực trạng đau đầu (Pain Points):**
  - Dữ liệu sinh viên bị phân mảnh (Siloed Data) trên 4 hệ thống riêng biệt: Tuyển sinh, Điểm đào tạo, LMS học trực tuyến và Khảo sát việc làm.
  - Cố vấn học tập chỉ phát hiện sinh viên có nguy cơ thôi học/học lực yếu khi đã hết kỳ và có quyết định cảnh cáo học vụ chính thức (quá muộn để can thiệp hỗ trợ).
  - Tỷ lệ sinh viên bị buộc thôi học hoặc trễ hạn tốt nghiệp hàng năm dao động từ 4% - 6%, gây thiệt hại uy tín và doanh thu đào tạo.

## 2. Các Giả Định Của Bài Toán (Assumptions)
1. Các hệ thống hiện tại đều có khả năng cung cấp API hoặc xuất dữ liệu:
   - `Admission System` và `Career & Alumni System` sẵn sàng xuất dữ liệu định kỳ theo lô (CSV/JSON/Database dump).
   - `Grading System` và `LMS System` hỗ trợ bắn webhook hoặc ghi transaction log (CDC) theo thời gian thực.
2. Sinh viên và Cố vấn học tập có tài khoản định danh duy nhất (Single Identity / SSO qua Email trường hoặc MSSV).
3. Nhà trường có hạ tầng Cloud hoặc Trung tâm dữ liệu (On-premise Private Cloud) đủ điều kiện triển khai cụm Stream Processing và Data Hub tập trung.

## 3. Phân Tích Các Bên Liên Quan (Stakeholder Analysis)

| Bên liên quan (Stakeholder) | Mối quan tâm chính (Concerns) | Kỳ vọng vào hệ thống |
|---|---|---|
| **Ban Giám hiệu (Executive Board)** | Tỷ lệ tốt nghiệp đúng hạn, giảm tỷ lệ thôi học, nâng cao xếp hạng đại học. | Dashboard báo cáo trực quan, số liệu 360 toàn diện, cảnh báo sớm xu hướng. |
| **Cố vấn học tập (Academic Advisors)** | Khó theo dõi tiến độ từng sinh viên, thông tin đến quá trễ. | Nhận cảnh báo tức thì (< 30s) khi sinh viên có điểm bất thường hoặc bỏ LMS, có đủ dữ liệu để tư vấn kịp thời. |
| **Phòng Đào tạo (Registrar / Academic Affairs)** | Sai lệch dữ liệu giữa các phòng ban, công việc thủ công tổng hợp báo cáo cuối kỳ nặng nề. | Tự động hóa tích hợp dữ liệu, báo cáo tự động, giảm tải nhân sự. |
| **Sinh viên (Students)** | Không nắm rõ bức tranh học tập tổng thể, nguy cơ trượt môn bất ngờ. | Cổng thông tin xem hồ sơ 360 cá nhân, nhận thông báo nhắc nhở sớm để cải thiện kết quả. |

## 4. Sơ Đồ ArchiMate Tầng Motivation (Motivation Layer)
<!-- Vẽ trên Archi hoặc Draw.io rồi xuất ảnh lưu vào diagrams/archimate_motivation.png -->

### Thành phần cần có trong sơ đồ:
- **Stakeholders:** Ban Giám hiệu, Cố vấn học tập, Phòng Đào tạo, Sinh viên.
- **Drivers:** Nâng cao chất lượng đào tạo, Chuyển đổi số giáo dục đại học, Giảm tỷ lệ thôi học.
- **Goals:** Tích hợp dữ liệu tập trung toàn trường, Can thiệp học vụ chủ động trước kỳ thi, Nâng tỷ lệ tốt nghiệp đúng hạn lên 92%.
- **Outcomes:** Hồ sơ Student 360 tập trung, Hệ thống cảnh báo nhanh thời gian thực.
- **Requirements (Gắn trực tiếp với 3 mã quy chuẩn):**
  - `REQ-01`: Tích hợp đa nguồn dữ liệu tạo hồ sơ Student 360.
  - `REQ-02`: Phát hiện nguy cơ & phát Academic Alert tức thì (< 30s).
  - `REQ-03`: Xử lý ngoại lệ, chống trùng lặp và tự động thu hồi/cập nhật cảnh báo khi sửa điểm.

## 5. Tầm Nhìn Kiến Trúc (Architecture Vision) & Kiến Trúc Hiện Trạng (Baseline)

### Kiến trúc Hiện trạng (Baseline Architecture):
- 4 hệ thống hoạt động rời rạc (Point-to-Point hoặc hoàn toàn tách biệt).
- Dữ liệu đồng bộ thủ công bằng cách xuất file Excel vào cuối học kỳ.
- Không có cơ chế thông báo tự động; Cố vấn học tập nhận danh sách giấy hoặc file Excel sau khi kỳ thi kết thúc.

### Kiến trúc Mục tiêu (Target Architecture Vision):
- Xây dựng **Data Hub** trung tâm với 5 Core Application Services:
  1. `Batch Ingestion Service`
  2. `Stream Ingestion Gateway`
  3. `Student 360 Profile Service`
  4. `Fast Alerting Engine`
  5. `Academic Portal & Notification Service`
- Chuyển đổi từ mô hình *Passive Reactive* (Xử lý bị động cuối kỳ) sang mô hình *Active Real-time Proactive* (Chủ động cảnh báo theo thời gian thực).
