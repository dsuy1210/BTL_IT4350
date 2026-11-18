# 🎓 BÀI TẬP LỚN: KIẾN TRÚC HỆ THỐNG THÔNG TIN VÀ ỨNG DỤNG (IT4350)
## Chủ đề VIII: Student 360 & Data Hub — Biến thể B: Cảnh báo nhanh

[![PR Validation CI](https://github.com/dsuy1210/BTL_IT4350/actions/workflows/pr-check.yml/badge.svg)](https://github.com/dsuy1210/BTL_IT4350/actions)
[![Branch Protection: Enforced](https://img.shields.io/badge/Branch%20Protection-Strict%20PR%20Only-red.svg)](CONTRIBUTING.md)
[![Team Size](https://img.shields.io/badge/Quy%20mô-3%20Thành%20viên-blue.svg)](#-phân-công-trách-nhiệm-3-nhánh-độc-lập)
[![Duration](https://img.shields.io/badge/Thời%20gian-4%20Tuần%20(4%20Deadlines)-green.svg)](#-lộ-trình-4-mốc-deadline-chi-tiết)

---

## ⛔ QUY TẮC LÀM VIỆC BẮT BUỘC (GIT WORKFLOW)

> 🚨 **YÊU CẦU CỐT TỬ CỦA NHÓM TRƯỞNG:**
> 1. **TUYỆT ĐỐI KHÔNG PUSH TRỰC TIẾP LÊN NHÁNH `main`**.
> 2. Mọi thành viên khi thực hiện công việc **BẮT BUỘC PHẢI TẠO BRANCH RIÊNG** theo cú pháp:
>    - `feature/tv1-...` (Thành viên 1)
>    - `feature/tv2-...` (Thành viên 2)
>    - `feature/tv3-...` (Thành viên 3)
> 3. Sau khi hoàn thành, tạo **Pull Request (PR)** vào `main` và điền đầy đủ checklist.
> 4. **CHỈ KHI NHÓM TRƯỞNG REVIEW VÀ APPROVE THÌ CODE/DOC MỚI ĐƯỢC MERGE VÀO `main`**.
>
> 📖 *Xem hướng dẫn chi tiết quy trình Git và cấu hình bảo vệ nhánh tại:* [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 BƯỚC 0: "HỢP ĐỒNG CHUNG" (UNIVERSAL CONTRACT)

Để cả 3 thành viên làm việc song song độc lập **"Không ai phải đợi ai"**, tất cả tài liệu, sơ đồ BPMN, ArchiMate, ADR, Mock UI và Mock API phải dùng chính xác bộ danh pháp đã chốt cứng tại [docs/00_universal_contract.md](docs/00_universal_contract.md):

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            4 NGUỒN ĐẦU VÀO (EXTERNAL)                         │
│  1. Admission System (Batch)         │  2. Career & Alumni System (Batch)     │
│  3. LMS System (Real-time Stream)    │  4. Grading System (Real-time CDC)     │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    5 THÀNH PHẦN LÕI (CORE APPLICATION SERVICES)               │
│  [SVC-01] Batch Ingestion Service       ─► Thu thập dữ liệu lô (Tuyển sinh/VL)│
│  [SVC-02] Stream Ingestion Gateway      ─► Nhận sự kiện thời gian thực (LMS) │
│  [SVC-03] Student 360 Profile Service   ─► Kho dữ liệu hồ sơ 360 trung tâm   │
│  [SVC-04] Fast Alerting Engine          ─► Đánh giá luật cảnh báo nhanh < 30s│
│  [SVC-05] Academic Portal & Notification─► Dashboard cố vấn & gửi thông báo  │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                     6 ĐỐI TƯỢNG DỮ LIỆU CHUẨN (DATA OBJECTS)                 │
│  • Admission Record     • LMS Activity Log   • Grade Event                   │
│  • Employment Record    • Student 360 Profile• Academic Alert                │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3 Yêu Cầu Cốt Lõi Để Truy Vết (Traceability IDs):
- **`REQ-01`**: Tích hợp đa nguồn tạo hồ sơ Student 360 và hiển thị lên Dashboard.
- **`REQ-02` (Biến thể B - Luồng chính):** Phát hiện điểm kém / bỏ học LMS và phát cảnh báo học vụ thời gian thực (**SLA độ trễ < 30 giây**).
- **`REQ-03` (Biến thể B - Luồng ngoại lệ):** Chống trùng lặp sự kiện (Idempotency) và tự động thu hồi/hạ mức cảnh báo khi giảng viên điều chỉnh sửa lại điểm số.

---

## 👥 PHÂN CÔNG TRÁCH NHIỆM 3 NHÁNH ĐỘC LẬP

| Tiêu chí | 👤 Thành viên 1 (TV1)<br>**Quản trị, TOGAF & Chuyển đổi** | 👤 Thành viên 2 (TV2)<br>**Luồng Chính, Dữ liệu & Mock UI** | 👤 Thành viên 3 (TV3)<br>**Biến thể B, Hạ tầng & Mock API** |
|---|---|---|---|
| **Thư mục làm việc** | `docs/01_tv1_governance_togaf/` | `docs/02_tv2_core_student360/`<br>`mock-ui/` | `docs/03_tv3_realtime_alerting/`<br>`mock-api/` |
| **Phần Báo cáo phụ trách** | **Chương 1** (Bối cảnh, Motivation)<br>**Chương 5** (Gap, Roadmap, Rủi ro, Truy vết) | **Chương 2** (Nghiệp vụ, Ứng dụng & Dữ liệu Student 360 + ADR 01) | **Chương 3** (Công nghệ Real-time)<br>**Chương 4** (Ngoại lệ + ADR 02 + Kiểm chứng) |
| **Phần Slide phụ trách** | Trang 1-2 & Trang 11-12 | Trang 3-6 (Nghiệp vụ, C4, ADR 01, Demo UI) | Trang 7-10 (Công nghệ, ADR 02, Demo API) |
| **Prototype bàn giao** | Ghép file Word hoàn chỉnh (25-35 trang) & Khung Slide | Giao diện Web Prototype Dashboard & Student 360 (`mock-ui/`) | Mock API Server & Test Suite kiểm chứng ngoại lệ (`mock-api/`) |

---

## 📅 LỘ TRÌNH 4 MỐC DEADLINE CHI TIẾT

```mermaid
gantt
    title Lộ Trình 4 Mốc Deadline - BTL IT4350
    dateFormat  YYYY-MM-DD
    section TV1: Quản Trị & TOGAF
    Tuần 1: Bối cảnh, Stakeholder, Motivation, Baseline     :tv1_1, 2026-11-18, 7d
    Tuần 2: Gap Analysis, Roadmap 3 Phase, Migration        :tv1_2, after tv1_1, 7d
    Tuần 3: Danh mục 6-8 Rủi ro, Traceability Matrix        :tv1_3, after tv1_2, 7d
    Tuần 4: Ghép Báo cáo (25-35 trang), Khung Slide (12 trang):tv1_4, after tv1_3, 7d
    section TV2: Luồng Chính & UI
    Tuần 1: Yêu cầu chức năng FR, BPMN 1 Luồng chính        :tv2_1, 2026-11-18, 7d
    Tuần 2: ArchiMate Business/App, Cấu trúc Dữ liệu, C4    :tv2_2, after tv2_1, 7d
    Tuần 3: Quyết định ADR 01 (Batch ETL vs Hybrid)         :tv2_3, after tv2_2, 7d
    Tuần 4: Hoàn thiện Prototype Mock UI, 3 Slide           :tv2_4, after tv2_3, 7d
    section TV3: Real-time & API
    Tuần 1: Yêu cầu phi chức năng NFR, BPMN 2 Ngoại lệ      :tv3_1, 2026-11-18, 7d
    Tuần 2: ArchiMate Technology, Cơ chế Low-Latency        :tv3_2, after tv3_1, 7d
    Tuần 3: Quyết định ADR 02 (Cronjob vs Stream Engine)    :tv3_3, after tv3_2, 7d
    Tuần 4: Hoàn thiện Prototype Mock API, Test Suite, 3 Slide:tv3_4, after tv3_3, 7d
```

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```
BTL_IT4350/
├── .github/
│   ├── ISSUE_TEMPLATE/                 # Template giao task cho TV1, TV2, TV3
│   ├── workflows/pr-check.yml          # GitHub Actions CI tự động kiểm tra cú pháp PR
│   └── pull_request_template.md        # Mẫu PR bắt buộc có checklist Hợp đồng chung
├── docs/
│   ├── 00_universal_contract.md        # Bước 0: Hợp đồng chung (Quy chuẩn danh pháp bất biến)
│   ├── 01_tv1_governance_togaf/        # Thư mục làm việc của Thành viên 1
│   │   ├── README.md
│   │   ├── week1_vision_motivation.md
│   │   ├── week2_gap_roadmap.md
│   │   ├── week3_risks_traceability.md
│   │   └── diagrams/                   # Sơ đồ Motivation, Migration của TV1
│   ├── 02_tv2_core_student360/         # Thư mục làm việc của Thành viên 2
│   │   ├── README.md
│   │   ├── week1_fr_bpmn_core.md
│   │   ├── week2_archimate_c4_schema.md
│   │   ├── week3_adr_01_integration.md
│   │   ├── schemas/                    # JSON Schema hồ sơ Student 360
│   │   └── diagrams/                   # Sơ đồ BPMN 1, ArchiMate App, C4 Container
│   ├── 03_tv3_realtime_alerting/       # Thư mục làm việc của Thành viên 3
│   │   ├── README.md
│   │   ├── week1_nfr_bpmn_exception.md
│   │   ├── week2_archimate_tech_infra.md
│   │   ├── week3_adr_02_rule_engine.md
│   │   ├── test_scenarios/             # Các kịch bản JSON kiểm chứng ngoại lệ
│   │   └── diagrams/                   # Sơ đồ BPMN 2, ArchiMate Technology
│   ├── report/
│   │   └── REPORT_OUTLINE.md           # Dàn ý chi tiết ghép Báo cáo 5 Chương (25-35 trang)
│   └── slides/
│       └── SLIDE_OUTLINE.md            # Dàn ý khung Slide thuyết trình (10-12 trang)
├── mock-ui/                            # Prototype Web Dashboard & Fast Alerting (TV2)
│   ├── index.html                      # Mở trực tiếp bằng trình duyệt để demo
│   ├── style.css
│   ├── app.js                          # Xử lý tương tác, giả lập điểm kém & thu hồi
│   └── README.md
├── mock-api/                           # Prototype Mock API Server & Test Suite (TV3)
│   ├── server.py                       # HTTP Server thuần Python (không cần pip install)
│   ├── test_api.py                     # Kịch bản tự động test REQ-02, REQ-03A, REQ-03B
│   ├── test_requests.http              # HTTP Client payloads
│   └── README.md
├── .gitignore
├── CONTRIBUTING.md                     # Quy định nhánh Git, Pull Request & Phê duyệt
└── README.md                           # Tài liệu tổng quan dự án
```

---

## ⚡ HƯỚNG DẪN KHỞI CHẠY NHANH CÁC PROTOTYPE

### 1. Trải nghiệm Prototype Mock UI (TV2)
Không cần cài đặt bất cứ thư viện nào:
- Nhấp đúp chuột mở file [mock-ui/index.html](mock-ui/index.html) bằng bất kỳ trình duyệt nào.
- Hoặc chạy web server mini:
  ```bash
  cd mock-ui
  python -m http.server 8080
  ```
  Truy cập: `http://localhost:8080`

### 2. Khởi chạy & Kiểm thử Mock API (TV3)
Chạy bằng Python 3 thuần túy:
- **Khởi động server:**
  ```bash
  python mock-api/server.py
  ```
- **Chạy kiểm thử tự động 3 kịch bản:**
  ```bash
  python mock-api/test_api.py
  ```
  *(Kiểm chứng luồng chính phát cảnh báo SLA < 30s, chống trùng lặp sự kiện và tự động thu hồi khi giảng viên sửa điểm!)*
