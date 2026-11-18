# 🎓 BÀI TẬP LỚN: KIẾN TRÚC HỆ THỐNG THÔNG TIN VÀ ỨNG DỤNG (IT4350)
## Chủ đề VIII: Student 360 & Data Hub — Biến thể B: Cảnh báo nhanh

[![PR Validation CI](https://github.com/dsuy1210/BTL_IT4350/actions/workflows/pr-check.yml/badge.svg)](https://github.com/dsuy1210/BTL_IT4350/actions)
[![Branch Protection: Enforced](https://img.shields.io/badge/Branch%20Protection-Strict%20PR%20Only-red.svg)](CONTRIBUTING.md)
[![Team Size](https://img.shields.io/badge/Quy%20mô-3%20Thành%20viên-blue.svg)](#-phân-công-trách-nhiệm-3-nhánh-độc-lập)
[![Architecture](https://img.shields.io/badge/Kiến%20trúc-TOGAF%20%7C%20ArchiMate%20%7C%20C4-purple.svg)](#-cấu-trúc-thư-mục-dự-án)

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

## 📋 CÁC GIAI ĐOẠN TRIỂN KHAI DỰ ÁN

| Giai đoạn | 👤 TV1: Quản Trị & TOGAF | 👤 TV2: Luồng Chính & UI | 👤 TV3: Real-time & API |
|:---:|---|---|---|
| **Giai đoạn 1** | Bối cảnh tổ chức, Giả định, Stakeholders, ArchiMate Motivation, Baseline Architecture. | Đặc tả Functional Requirements (FR), Vẽ BPMN 1 Luồng chính End-to-End. | Đặc tả Non-Functional Requirements (NFR), Vẽ BPMN 2 Luồng ngoại lệ (sửa điểm/lặp). |
| **Giai đoạn 2** | Gap Analysis (Baseline vs Target), Roadmap 3 Phase, ArchiMate Migration. | ArchiMate Business & Application Layer, Thiết kế cấu trúc Hồ sơ 360, Sơ đồ C4. | ArchiMate Technology Layer, Kiến trúc Message Broker/Redis/DB, Kỹ thuật Low-Latency. |
| **Giai đoạn 3** | Danh mục 06-08 Rủi ro & Mitigation, Bảng ma trận truy vết (Traceability Matrix). | Soạn thảo trọn vẹn ADR 01 (Batch ETL vs Hybrid Integration cho Data Hub). | Soạn thảo trọn vẹn ADR 02 (Cronjob Polling vs Stream Rule Engine) & Kịch bản kiểm chứng. |
| **Giai đoạn 4** | Ghép hoàn chỉnh Báo cáo 5 Chương (25-35 trang), Tạo khung Slide bảo vệ (10-12 trang). | Hoàn thiện Web Prototype Mock UI (Dashboard, Hồ sơ 360, Pop-up Alert), Điền 3 Slide UI. | Hoàn thiện Prototype Mock API (Python Server, Test Suite kiểm chứng ngoại lệ), Điền 3 Slide API. |

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```
BTL_IT4350/
├── .github/
│   ├── ISSUE_TEMPLATE/                 # Template giao việc cho TV1, TV2, TV3
│   ├── workflows/pr-check.yml          # GitHub Actions CI tự động kiểm tra cú pháp PR
│   └── pull_request_template.md        # Mẫu PR bắt buộc có checklist Hợp đồng chung
├── docs/
│   ├── 00_universal_contract.md        # Bước 0: Hợp đồng chung (Quy chuẩn danh pháp bất biến)
│   ├── 01_tv1_governance_togaf/        # Thư mục làm việc của Thành viên 1
│   │   ├── README.md
│   │   ├── 01_vision_motivation.md
│   │   ├── 02_gap_roadmap.md
│   │   ├── 03_risks_traceability.md
│   │   └── diagrams/                   # Sơ đồ Motivation, Migration của TV1
│   ├── 02_tv2_core_student360/         # Thư mục làm việc của Thành viên 2
│   │   ├── README.md
│   │   ├── 01_fr_bpmn_core.md
│   │   ├── 02_archimate_c4_schema.md
│   │   ├── 03_adr_01_integration.md
│   │   ├── schemas/                    # JSON Schema hồ sơ Student 360
│   │   └── diagrams/                   # Sơ đồ BPMN 1, ArchiMate App, C4 Container
│   ├── 03_tv3_realtime_alerting/       # Thư mục làm việc của Thành viên 3
│   │   ├── README.md
│   │   ├── 01_nfr_bpmn_exception.md
│   │   ├── 02_archimate_tech_infra.md
│   │   ├── 03_adr_02_rule_engine.md
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
