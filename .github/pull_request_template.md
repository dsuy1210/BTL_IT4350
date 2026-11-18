## 📌 Thông Tin Pull Request

- **Người thực hiện:** <!-- Điền tên hoặc GitHub username -->
- **Vai trò:** [ ] Thành viên 1 (TV1 - TOGAF & Governance) | [ ] Thành viên 2 (TV2 - Luồng chính & Mock UI) | [ ] Thành viên 3 (TV3 - Realtime & Mock API)
- **Hạng mục thực hiện:** [ ] Giai đoạn 1 (Bối cảnh / Nghiệp vụ / NFR) | [ ] Giai đoạn 2 (Kiến trúc ArchiMate & Dữ liệu) | [ ] Giai đoạn 3 (ADR & Quản trị) | [ ] Giai đoạn 4 (Báo cáo, Slide & Prototype)
- **Nhánh nguồn (Source Branch):** `feature/...` <!-- TUYỆT ĐỐI KHÔNG PUSH TRỰC TIẾP LÊN MAIN -->

---

## 📝 Tóm Tắt Thay Đổi
<!-- Mô tả ngắn gọn nội dung đã làm trong PR này -->
- Thêm/Cập nhật tài liệu: ...
- Thêm/Cập nhật sơ đồ (BPMN / ArchiMate / C4): ...
- Thêm/Cập nhật prototype (Mock UI / Mock API / Schema): ...

---

## 🔒 Kiểm Tra Tuân Thủ "Hợp Đồng Chung" (Step 0 Contract)
Vui lòng tích chọn xác nhận nội dung của bạn tuân thủ đúng danh pháp quy định:
- [ ] **4 External Systems:** `Admission System`, `Career & Alumni System`, `LMS System`, `Grading System`
- [ ] **5 Core Services:** `Batch Ingestion Service`, `Stream Ingestion Gateway`, `Student 360 Profile Service`, `Fast Alerting Engine`, `Academic Portal & Notification Service`
- [ ] **6 Data Objects:** `Admission Record`, `LMS Activity Log`, `Grade Event`, `Employment Record`, `Student 360 Profile`, `Academic Alert`
- [ ] **3 Traceability IDs:** Đã ánh xạ đúng `REQ-01`, `REQ-02`, hoặc `REQ-03`

---

## 📸 Bằng Chứng / Demo / Sơ Đồ
<!-- Đính kèm ảnh chụp màn hình, ảnh sơ đồ render, hoặc kết quả chạy script kiểm tra -->

---

## ✅ Checklist Trước Khi Gửi PR
- [ ] Đã kéo code mới nhất từ nhánh `main` về trước khi push (`git pull origin main`).
- [ ] Đã kiểm tra không có xung đột (merge conflicts).
- [ ] Không sửa đổi file của thành viên khác trừ khi đã trao đổi thống nhất.
- [ ] Code/Script (nếu có) chạy thành công không có lỗi cú pháp.

---

## 👑 Phê Duyệt Của Nhóm Trưởng (Reviewer Approval)
*Chỉ nhóm trưởng mới có quyền tích chọn và merge vào `main`:*
- [ ] Nội dung đạt chất lượng và đáp ứng đầy đủ yêu cầu bài toán.
- [ ] Đúng quy chuẩn kiến trúc và danh pháp Hợp đồng chung.
- [ ] **APPROVED & MERGED**
