# 🖥️ PROTOTYPE MOCK UI - STUDENT 360 & FAST ALERTING PORTAL
### Phụ trách: Thành viên 2 (Hạng mục 4)
### Môn học: Kiến trúc Hệ thống Thông tin và Ứng dụng (IT4350)

---

## 🌟 Giới Thiệu
Giao diện Web Prototype mô phỏng kịch bản End-to-End của hệ thống:
1. **Màn hình Dashboard Thống Kê:** Thống kê tổng quan sinh viên có nguy cơ, trạng thái hoạt động của 5 Core Services, tích hợp 4 nguồn dữ liệu (Admission, Grading, LMS, Career).
2. **Màn hình Hồ Sơ Student 360 Chi Tiết:** Gom toàn diện thông tin sinh viên từ 4 nguồn về một màn hình duy nhất (Single Pane of Glass). Bấm **Xem 360** ở Dashboard để mở đúng hồ sơ của từng sinh viên.
3. **Trung Tâm Cảnh Báo Nhanh (Fast Alerting Engine):** Hiển thị danh sách cảnh báo học vụ thời gian thực, minh họa độ trễ SLA < 30 giây. *Lưu ý: các con số độ trễ (~1.2s - 2.4s) và dữ liệu sinh viên trong prototype là **giá trị mô phỏng cố định**, không phải số đo thực; số đo thực do Mock API của TV3 kiểm chứng.*

---

## 🚀 Cách Mở & Chạy Demo
Giao diện được viết bằng **HTML5, CSS3 và Vanilla JavaScript thuần túy**, hoàn toàn không phụ thuộc vào `node_modules` hay cài đặt môi trường phức tạp:

### Cách 1: Mở trực tiếp bằng trình duyệt
- Nhấp đúp chuột trực tiếp vào file `mock-ui/index.html` trên máy tính để mở trên Chrome, Edge, Firefox hoặc Safari.

### Cách 2: Chạy qua Live Server hoặc Python Web Server
```bash
cd D:\BTL_IT4350\mock-ui
python -m http.server 8080
```
Sau đó mở trình duyệt truy cập: `http://localhost:8080`

---

## 🎬 Kịch Bản Demo Cho TV2 Khi Báo Cáo Thuyết Trình
1. **Demo Luồng Chính (REQ-02):**
   - Bấm vào nút màu xanh **"⚡ Giả Lập: Điểm Giữa Kỳ < 3.0 (REQ-02)"** ở thanh Header.
   - Quan sát pop-up Toast cảnh báo màu đỏ xuất hiện tức thì ở góc phải màn hình, số đếm cảnh báo tăng lên và một dòng mới xuất hiện trong bảng Fast Alert với độ trễ đo được 1.9s (< 30s SLA).
2. **Demo Xem Hồ Sơ 360 (REQ-01):**
   - Chuyển sang tab **"Hồ Sơ Student 360"** để thuyết minh cách 4 nguồn (Tuyển sinh, Điểm, LMS, Việc làm) được tổng hợp vào hồ sơ của sinh viên Nguyễn Văn An (20210001).
3. **Demo Xử Lý Ngoại Lệ & Thu Hồi (REQ-03):**
   - Bấm vào nút màu vàng **"🔄 Giả Lập: Sửa Điểm 8.5 & Thu Hồi (REQ-03)"**.
   - Quan sát thông báo Toast màu xanh: Điểm trong hồ sơ 360 được cập nhật lên 8.5, mức rủi ro chuyển về AN TOÀN, và bản ghi cảnh báo cũ tự động bị gạch bỏ và đổi trạng thái thành `REVOKED`.
