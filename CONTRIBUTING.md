# 🛡️ HƯỚNG DẪN ĐÓNG GÓP & QUY TRÌNH LÀM VIỆC NHÓM (GIT WORKFLOW)

Tài liệu này quy định **bắt buộc** cho toàn bộ 3 thành viên tham gia Bài tập lớn môn **Kiến trúc Hệ thống Thông tin và Ứng dụng (IT4350)**.

---

## ⛔ QUY TẮC BẤT BIẾN (GOLDEN RULES)

1. **TUYỆT ĐỐI KHÔNG COMMIT HOẶC PUSH TRỰC TIẾP LÊN NHÁNH `main`**.
2. **MỌI THAY ĐỔI ĐỀU PHẢI QUA PULL REQUEST (PR)**: Mỗi thành viên tạo branch riêng khi làm việc, sau đó mở PR vào `main`.
3. **CHỈ NHÓM TRƯỞNG MỚI ĐƯỢC PHÉP DUYỆT (APPROVE) VÀ MERGE VÀO `main`**.
4. **TUÂN THỦ DANH PHÁP CHUẨN**: Xem file `docs/00_universal_contract.md` trước khi viết tài liệu hay code.

---

## ⚙️ DÀNH CHO NHÓM TRƯỞNG: CẤU HÌNH BRANCH PROTECTION TRÊN GITHUB

Để GitHub tự động chặn mọi người push trực tiếp lên `main`, Nhóm trưởng cần thực hiện 5 bước sau trên giao diện GitHub:

1. Truy cập repo trên GitHub: `https://github.com/dsuy1210/BTL_IT4350`
2. Bấm vào tab **Settings** (ở thanh menu trên cùng).
3. Ở menu bên trái, chọn **Branches** (mục *Code and automation*).
4. Nhấn nút **Add branch ruleset** (hoặc **Add classic branch protection rule**):
   - **Branch name pattern**: Điền `main`
   - ✅ Tích chọn: **Require a pull request before merging**
   - ✅ Tích chọn: **Require approvals** -> Đặt số lượng là `1`
   - ✅ Tích chọn: **Dismiss stale pull request approvals when new commits are pushed**
   - ✅ Tích chọn: **Require status checks to pass before merging** (Chọn workflow `validate-pr`)
   - ✅ Tích chọn: **Do not allow bypassing the above settings** (để áp dụng cho toàn bộ thành viên)
   - ❌ Đảm bảo **BỎ TÍCH** mục *Allow force pushes* và *Allow deletions*.
5. Bấm **Create** / **Save changes**.

> *Sau khi bật tính năng này, nếu ai cố tình `git push origin main`, GitHub sẽ từ chối và báo lỗi ngay lập tức!*

---

## 🌿 QUY ƯỚC ĐẶT TÊN BRANCH

Mọi branch tạo mới phải tuân thủ định dạng:
```
<loại>/<mã_thành_viên>-<mô_tả_ngắn>
```

### Các tiền tố hợp lệ:
- `feature/tv1-togaf-vision`: Làm phần Bối cảnh & Motivation của TV1
- `feature/tv1-gap-roadmap`: Làm phần Gap Analysis & Roadmap của TV1
- `feature/tv2-bpmn-core`: Làm phần Sơ đồ BPMN luồng chính của TV2
- `feature/tv2-mock-ui`: Làm phần Web Prototype Mock UI của TV2
- `feature/tv3-tech-archimate`: Làm phần ArchiMate Technology của TV3
- `feature/tv3-mock-api`: Làm phần Mock API & Test ngoại lệ của TV3
- `docs/tv1-traceability-matrix`: Cập nhật tài liệu & ma trận truy vết
- `fix/tv3-api-idempotency`: Sửa lỗi kỹ thuật / API

---

## 🚀 QUY TRÌNH 6 BƯỚC LÀM VIỆC HÀNG NGÀY CHO THÀNH VIÊN

### Bước 1: Đồng bộ nhánh `main` mới nhất
Trước khi làm việc mới, luôn kéo code mới nhất từ GitHub:
```bash
git checkout main
git pull origin main
```

### Bước 2: Tạo branch riêng cho công việc của mình
```bash
# Ví dụ TV2 làm phần sơ đồ BPMN:
git checkout -b feature/tv2-bpmn-core
```

### Bước 3: Thực hiện công việc & Lưu commit
Viết tài liệu hoặc code trong thư mục được phân công (`docs/01_...`, `docs/02_...`, `docs/03_...`, `mock-ui/`, `mock-api/`).
Commit với thông điệp rõ ràng theo chuẩn Conventional Commits:
```bash
git add .
git commit -m "feat(tv2): hoàn thành sơ đồ BPMN luồng chính REQ-02"
```

*Quy ước tiền tố commit:*
- `feat(...)`: Tính năng mới, nội dung mới
- `docs(...)`: Thêm hoặc sửa tài liệu markdown
- `fix(...)`: Sửa lỗi sơ đồ, cú pháp, mã nguồn
- `refactor(...)`: Tái cấu trúc file/thư mục

### Bước 4: Push branch cá nhân lên GitHub
```bash
git push -u origin feature/tv2-bpmn-core
```

### Bước 5: Mở Pull Request (PR) trên GitHub
1. Vào trang GitHub của repo: `https://github.com/dsuy1210/BTL_IT4350`
2. Nhấn vào nút **Compare & pull request** màu vàng vừa hiện lên.
3. Base branch chọn: `main`, Compare branch chọn branch của bạn (ví dụ: `feature/tv2-bpmn-core`).
4. Điền đầy đủ thông tin theo mẫu **Pull Request Template** có sẵn:
   - Tích chọn vai trò TV1 / TV2 / TV3
   - Tích chọn hạng mục thực hiện tương ứng
   - Xác nhận đã tuân thủ 5 Core Services & Danh pháp trong Hợp đồng chung
   - Đính kèm ảnh demo/kết quả (nếu có)
5. Nhấn **Create Pull Request**.

### Bước 6: Nhóm trưởng Review & Duyệt
- Nhóm trưởng nhận thông báo, kiểm tra nội dung và sơ đồ.
- Nếu cần chỉnh sửa: Nhóm trưởng comment trong PR, thành viên commit thêm vào cùng branch đó rồi push tiếp (PR tự động cập nhật).
- Khi đạt yêu cầu: Nhóm trưởng bấm **Approve** -> Bấm **Confirm Merge** (khuyến khích chọn *Squash and merge* hoặc *Rebase and merge* để lịch sử git gọn gàng).
- Sau khi merge, xóa branch cũ trên GitHub.

---

## 🗂️ NGUYÊN TẮC KHÔNG XUNG ĐỘT (ZERO MERGE CONFLICT)

Dự án đã được phân chia thư mục độc lập tuyệt đối:
- TV1 chỉ làm việc trong: `docs/01_tv1_governance_togaf/`
- TV2 chỉ làm việc trong: `docs/02_tv2_core_student360/` và `mock-ui/`
- TV3 chỉ làm việc trong: `docs/03_tv3_realtime_alerting/` và `mock-api/`
- `docs/00_universal_contract.md`: File chung chốt cứng, **KHÔNG TỰ Ý CHỈNH SỬA** khi chưa họp cả nhóm!

Nếu tuân thủ đúng nguyên tắc này, dự án **100% không bao giờ gặp merge conflict**.
