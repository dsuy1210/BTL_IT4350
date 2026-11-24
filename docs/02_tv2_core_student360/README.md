# 📗 THÀNH VIÊN 2: NHÁNH LUỒNG CHÍNH (END-TO-END), DỮ LIỆU & MOCK UI

- **Phần Báo cáo phụ trách:** **Chương 2** (Nghiệp vụ & Kiến trúc Ứng dụng/Dữ liệu Student 360 + ADR 01) (~10 trang).
- **Phần Code/Prototype phụ trách:** Thư mục `mock-ui/` (Giao diện Web tương tác: Hồ sơ Student 360, Dashboard thống kê, Pop-up Cảnh báo học vụ).

---

## 📋 Danh Mục Các Hạng Mục Công Việc Của TV2

| Hạng mục | Nội dung công việc | File bàn giao |
|:---:|:---|:---|
| **Hạng mục 1** | Yêu cầu chức năng (FR-01..15, quy tắc BR-01..04); BPMN Quy trình 1 (Luồng chính End-to-End: Sự kiện → Gateway → Profile → Engine → Portal). | `01_fr_bpmn_core.md`<br>`diagrams/bpmn_core_flow.png` |
| **Hạng mục 2** | ArchiMate tầng Business & Application (5 Core Services & 6 Data Objects); cấu trúc dữ liệu Hồ sơ Student 360; sơ đồ C4 Container. | `02_archimate_c4_schema.md`<br>`schemas/student_360_profile_schema.json`<br>`schemas/student_360_profile_example.json`<br>`diagrams/archimate_app_bus.png`<br>`diagrams/c4_container.png`<br>`diagrams/student360_lineage.png` |
| **Hạng mục 3** | **ADR 01** (Batch ETL truyền thống vs Hybrid Batch + CDC/Stream): tiêu chí, ma trận điểm, quyết định, đánh đổi. | `03_adr_01_integration.md` |
| **Hạng mục 4** | Prototype Mock UI (HTML/CSS/JS) chạy trực tiếp trên trình duyệt + ảnh chụp 4 màn hình cho báo cáo / slide. | `../../mock-ui/`<br>`diagrams/ui/*.png` |

---

## 📁 Cấu Trúc Thư Mục
```
docs/02_tv2_core_student360/
├── README.md
├── 01_fr_bpmn_core.md
├── 02_archimate_c4_schema.md
├── 03_adr_01_integration.md
├── schemas/
│   ├── student_360_profile_schema.json
│   └── student_360_profile_example.json   # bản ghi mẫu hợp lệ
└── diagrams/
    ├── bpmn_core_flow.png / .svg
    ├── archimate_app_bus.png / .svg
    ├── c4_container.png / .svg
    ├── student360_lineage.png / .svg
    ├── ui/                  # ảnh chụp Mock UI (dashboard, hồ sơ 360, cảnh báo, thu hồi)
    └── src/                 # mã Python sinh sơ đồ: chạy `python <tên>.py` để vẽ lại
```

## 🔁 Vẽ lại sơ đồ
```bash
cd docs/02_tv2_core_student360/diagrams/src
python bpmn_core_flow.py && python archimate_app_bus.py && python c4_container.py && python student360_lineage.py
# Xuất PNG (cần rsvg-convert hoặc Inkscape):
for f in bpmn_core_flow archimate_app_bus c4_container student360_lineage; do rsvg-convert -w 2400 ../$f.svg -o ../$f.png; done
```
