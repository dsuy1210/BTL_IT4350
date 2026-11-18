# 📗 THÀNH VIÊN 2: NHÁNH LUỒNG CHÍNH (END-TO-END), DỮ LIỆU & MOCK UI

- **Phần Báo cáo phụ trách:** **Chương 2** (Nghiệp vụ & Kiến trúc Ứng dụng/Dữ liệu Student 360 + ADR 01) (~10 trang).
- **Phần Slide phụ trách:** Trang 3-4 (Kiến trúc Nghiệp vụ & Hồ sơ 360), Trang 5-6 (ADR 01 & Demo Mock UI).
- **Phần Code/Prototype phụ trách:** Thư mục `mock-ui/` (Giao diện Web tương tác: Hồ sơ Student 360, Dashboard thống kê, Pop-up Cảnh báo học vụ).

---

## 📋 Danh Mục Các Hạng Mục Công Việc Của TV2

| Hạng mục | Nội dung công việc | File bàn giao |
|:---:|:---|:---|
| **Hạng mục 1** | Viết chi tiết bộ Yêu cầu chức năng (FR); Vẽ sơ đồ BPMN Quy trình 1 (Luồng chính End-to-End: Sự kiện $\rightarrow$ Gateway $\rightarrow$ Profile $\rightarrow$ Engine $\rightarrow$ Portal). | `01_fr_bpmn_core.md`<br>`diagrams/bpmn_core_flow.png` |
| **Hạng mục 2** | Vẽ sơ đồ ArchiMate tầng Business & Application (dùng đúng 5 Core Services & 6 Data Objects); Thiết kế cấu trúc dữ liệu Hồ sơ Student 360; Vẽ sơ đồ C4 Container. | `02_archimate_c4_schema.md`<br>`schemas/student_360_profile_schema.json`<br>`diagrams/c4_container.png` |
| **Hạng mục 3** | Soạn thảo trọn vẹn **ADR 01** (Kiến trúc tích hợp dữ liệu về Data Hub: Batch ETL truyền thống vs Hybrid Batch + CDC/Stream). | `03_adr_01_integration.md` |
| **Hạng mục 4** | Xây dựng Prototype Mock UI hoàn chỉnh (HTML/CSS/JS) chạy trực tiếp trên trình duyệt; Điền 3 trang slide phần Nghiệp vụ, Dữ liệu và Demo UI. | `../../mock-ui/`<br>`../slides/SLIDE_OUTLINE.md` |

---

## 📁 Cấu Trúc Thư Mục
```
docs/02_tv2_core_student360/
├── README.md
├── 01_fr_bpmn_core.md
├── 02_archimate_c4_schema.md
├── 03_adr_01_integration.md
├── schemas/
│   └── student_360_profile_schema.json
└── diagrams/
    └── .gitkeep
```
