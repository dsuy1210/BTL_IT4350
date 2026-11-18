# 📙 THÀNH VIÊN 3: NHÁNH BIẾN THỂ B (REAL-TIME), CÔNG NGHỆ & MOCK API

- **Phần Báo cáo phụ trách:** **Chương 3** (Kiến trúc Công nghệ Real-time & Hạ tầng triển khai) và **Chương 4** (Xử lý Ngoại lệ, ADR 02 & Kiểm chứng Hệ thống) (~10 trang).
- **Phần Slide phụ trách:** Trang 7-8 (Kiến trúc Công nghệ & ADR 02), Trang 9-10 (Xử lý Ngoại lệ & Demo Mock API).
- **Phần Code/Prototype phụ trách:** Thư mục `mock-api/` (Mock API Server giả lập nhận Stream, kiểm tra Idempotency, đánh giá luật nhanh < 30s và thu hồi cảnh báo khi sửa điểm).

---

## 📋 Danh Mục Các Hạng Mục Công Việc Của TV3

| Hạng mục | Nội dung công việc | File bàn giao |
|:---:|:---|:---|
| **Hạng mục 1** | Viết bộ Yêu cầu phi chức năng (NFR) cho Biến thể B: Latency < 30s, Throughput, Idempotency; Sơ đồ BPMN Quy trình 2 (Luồng ngoại lệ: Giảng viên sửa điểm / LMS gửi trùng). | `01_nfr_bpmn_exception.md`<br>`diagrams/bpmn_exception_flow.png` |
| **Hạng mục 2** | Sơ đồ ArchiMate tầng Technology (Hạ tầng triển khai: Kafka/MQ, Stream Processing, PostgreSQL, Redis, API Gateway); Phân tích kỹ thuật đạt Low Latency. | `02_archimate_tech_infra.md`<br>`diagrams/archimate_technology.png` |
| **Hạng mục 3** | Soạn thảo trọn vẹn **ADR 02** (Cơ chế xử lý luật cảnh báo: Polling Cronjob vs In-Memory Stream Rule Engine); Soạn kịch bản kiểm chứng 01 tình huống bất thường (5k điểm / sửa điểm). | `03_adr_02_rule_engine.md`<br>`test_scenarios/exception_scenarios.json` |
| **Hạng mục 4** | Xây dựng Prototype Mock API hoàn chỉnh bằng Python (chạy test không cần cài lib ngoài); Viết kịch bản test curl/python kiểm chứng REQ-02 và REQ-03; Điền 3 slide. | `../../mock-api/`<br>`../slides/SLIDE_OUTLINE.md` |

---

## 📁 Cấu Trúc Thư Mục
```
docs/03_tv3_realtime_alerting/
├── README.md
├── 01_nfr_bpmn_exception.md
├── 02_archimate_tech_infra.md
├── 03_adr_02_rule_engine.md
├── test_scenarios/
│   └── exception_scenarios.json
└── diagrams/
    └── .gitkeep
```
