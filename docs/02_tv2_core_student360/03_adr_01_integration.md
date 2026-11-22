# 📑 HẠNG MỤC 3 - TV2: KIẾN TRÚC QUYẾT ĐỊNH (ADR 01)
## ADR 01: Kiến trúc tích hợp đa nguồn về Data Hub cho Student 360 & Cảnh báo nhanh

| Thuộc tính | Giá trị |
|:---|:---|
| **Mã định danh** | `ADR-01` |
| **Trạng thái** | `PROPOSED` — chờ Nhóm trưởng duyệt qua Pull Request (chuyển thành `ACCEPTED` sau khi merge) |
| **Người đề xuất** | Thành viên 2 (Nhánh Luồng chính & Dữ liệu) |
| **Yêu cầu liên quan** | `REQ-01` (tích hợp đa nguồn Student 360), `REQ-02` (Biến thể B — cảnh báo nhanh, SLA < 30 giây); ảnh hưởng gián tiếp `REQ-03` |
| **Quyết định liên quan** | `ADR-02` của TV3 (cơ chế Rule Engine) xây trên kết quả của ADR này |

---

## 1. Bối cảnh (Context)

Data Hub phải gom dữ liệu từ 4 hệ thống độc lập với đặc tính rất khác nhau:

| Nguồn | Đặc tính dữ liệu | Độ tươi cần thiết |
|:---|:---|:---|
| `Admission System` (EXT-01) | Gần như tĩnh, đổi theo kỳ tuyển sinh | Hằng ngày / đầu kỳ là đủ |
| `Career & Alumni System` (EXT-02) | Khảo sát theo đợt, tần suất thấp | Hằng tháng / cuối kỳ là đủ |
| `Grading System` (EXT-04) | Phát sinh khi giảng viên nhập / sửa điểm | **Tức thì** — nguồn kích hoạt cảnh báo điểm kém |
| `LMS System` (EXT-03) | Lưu lượng sự kiện lớn (đăng nhập, nộp bài, điểm danh) | **Tức thì** — nguồn kích hoạt cảnh báo bỏ học |

`REQ-02` yêu cầu `Academic Alert` đến Cố vấn học tập trong **dưới 30 giây** kể từ khi sự kiện phát sinh. `REQ-01` yêu cầu một hồ sơ 360 duy nhất, nhất quán giữa cả bốn nguồn.

**Câu hỏi quyết định:** tích hợp cả bốn nguồn theo một kiểu thống nhất, hay chọn kiểu tích hợp theo từng nguồn?

---

## 2. Các tiêu chí đánh giá

Trọng số do TV2 đề xuất, tổng 100%. Điểm 1 (kém) – 5 (tốt). Riêng tiêu chí **Độ trễ** là *điều kiện loại* (knockout): phương án không đáp ứng `REQ-02` bị loại bất kể tổng điểm.

| # | Tiêu chí | Trọng số | Ý nghĩa |
|:---:|:---|:---:|:---|
| C1 | Độ trễ đáp ứng `REQ-02` (< 30 s) | 30% | **Điều kiện loại** |
| C2 | Khả năng mở rộng nguồn mới (thẻ thư viện, KTX...) | 15% | Thêm nguồn không phải thiết kế lại |
| C3 | Nhất quán & khả năng đối soát dữ liệu | 15% | Một hồ sơ đúng, có thể kiểm tra lại |
| C4 | Độ phức tạp vận hành | 15% | Số thành phần phải vận hành, giám sát |
| C5 | Tác động lên hệ thống nguồn | 10% | Tải thêm, thay đổi bắt buộc ở hệ thống gốc |
| C6 | Chi phí hạ tầng | 10% | Máy chủ, broker, lưu trữ |
| C7 | Độ chín muồi / dễ tìm nhân lực | 5% | Công cụ phổ biến, tài liệu sẵn có |

---

## 3. Các phương án được xem xét

### Phương án 1 — Batch ETL truyền thống (Pure Batch ETL)
Một tiến trình ETL (Apache Airflow / script Python) chạy định kỳ (ví dụ mỗi đêm hoặc mỗi 4 giờ), quét cả 4 nguồn, làm sạch rồi nạp vào Data Hub.

- **Ưu điểm:** đơn giản, quen thuộc, ít thành phần; xử lý khối lượng lớn vào ban đêm, không làm chậm hệ thống tác nghiệp ban ngày; dễ đối soát vì mỗi lần chạy là một lô có thể chạy lại.
- **Nhược điểm:** độ tươi dữ liệu từ vài giờ đến 24 giờ → **không thể phát cảnh báo trong < 30 s** (điểm trượt sáng nay, Cố vấn chỉ biết sáng hôm sau). Quét lại toàn bộ 2 nguồn tần suất cao cũng tốn tải vô ích.

### Phương án 2 — Hybrid: Batch cho Tuyển sinh / Việc làm + Event-driven / CDC cho LMS / Điểm
- **Nhánh Batch** — `Batch Ingestion Service` (SVC-01) nạp `Admission System` và `Career & Alumni System` theo lô.
- **Nhánh Stream** — `Stream Ingestion Gateway` (SVC-02) nhận sự kiện từ `LMS System` (Webhook) và `Grading System` (CDC / API Event), đưa vào Message Broker.
- Hai nhánh hội tụ tại `Student 360 Profile Service` (SVC-03); `Fast Alerting Engine` (SVC-04) đọc trực tiếp luồng sự kiện.

- **Ưu điểm:** đáp ứng `REQ-02` vì chỉ hai nguồn cần tức thì mới đi đường stream; không lãng phí tài nguyên streaming cho nguồn đổi chậm; hệ thống Tuyển sinh không phải phát sự kiện; dễ gắn thêm nguồn sự kiện mới.
- **Nhược điểm:** phải vận hành hai đường ống (Batch + Stream) và một Message Broker; phải xử lý thứ tự sự kiện, trùng lặp và hợp nhất dữ liệu giữa hai đường.

---

## 4. Ma trận đánh giá

| Tiêu chí | Trọng số | PA1: Batch ETL | PA2: Hybrid | Nhận xét |
|:---|:---:|:---:|:---:|:---|
| C1. Độ trễ đáp ứng `REQ-02` | 30% | **1** ❌ | **5** ✅ | PA1 trễ hàng giờ → bị loại. PA2 trễ tính bằng giây. |
| C2. Mở rộng nguồn mới | 15% | 2 | 4 | PA2 chỉ cần thêm một producer / topic. |
| C3. Nhất quán & đối soát | 15% | 5 | 4 | PA1 dễ đối soát; PA2 cần Idempotency và đối soát định kỳ. |
| C4. Độ phức tạp vận hành | 15% | 5 | 3 | PA2 thêm Broker và nhánh stream. |
| C5. Tác động lên hệ thống nguồn | 10% | 3 | 4 | PA1 quét nặng giờ cao điểm; PA2 chỉ đọc log CDC / nhận Webhook. |
| C6. Chi phí hạ tầng | 10% | 5 | 3 | PA2 cần Kafka, Redis, node xử lý luồng. |
| C7. Độ chín muồi / nhân lực | 5% | 5 | 4 | Cả hai đều dùng công cụ phổ biến. |
| **Tổng điểm có trọng số** | 100% | **3.15** | **4.05** | PA2 cao hơn và là phương án duy nhất qua điều kiện loại C1. |

*(Tổng điểm = Σ trọng số × điểm; ví dụ PA2 = 0.30×5 + 0.15×4 + 0.15×4 + 0.15×3 + 0.10×4 + 0.10×3 + 0.05×4 = 4.05.)*

---

## 5. Quyết định (Decision)

Chọn **Phương án 2 — Hybrid Integration** làm kiến trúc tích hợp chính thức:

- `Batch Ingestion Service` (SVC-01): `Admission System` và `Career & Alumni System`, theo lô.
- `Stream Ingestion Gateway` (SVC-02): `LMS System` và `Grading System`, theo sự kiện.
- Hợp nhất tại `Student 360 Profile Service` (SVC-03) theo khóa `student_id`.

**Ngân sách độ trễ thiết kế (ước tính, chưa đo thực tế)** — dùng để chứng minh PA2 có đủ dư địa so với SLA 30 giây; số liệu thực do TV3 kiểm chứng bằng Mock API:

| Chặng | Ước tính |
|:---|:---:|
| Nguồn phát Webhook / CDC → Gateway nhận | ≈ 0.5 s |
| Validate schema + kiểm tra Idempotency Key | ≈ 0.2 s |
| Publish lên Kafka + consume bởi Engine | ≈ 0.6 s |
| Đánh giá luật + ghi `Academic Alert` | ≈ 0.4 s |
| Đẩy tới Portal (WebSocket) + vẽ pop-up | ≈ 1.0 s |
| **Tổng** | **≈ 3 s** (SLA cho phép 30 s) |

---

## 6. Hệ quả & đánh đổi (Consequences & Trade-offs)

**Tác động tích cực**
- Thỏa `REQ-02` với dư địa lớn; `REQ-01` được giữ nhất quán nhờ khóa `student_id` chung.
- Dễ mở rộng: thêm nguồn sự kiện mới (thẻ thư viện, cổng KTX) chỉ cần thêm producer / topic.

**Đánh đổi chấp nhận & cách giảm thiểu**

| Đánh đổi | Biện pháp |
|:---|:---|
| Vận hành hai đường ống và một Message Broker | Đóng gói bằng Docker Compose, giám sát độ trễ (lag) của topic; triển khai theo lộ trình 3 Phase của TV1 (Phase 1 Batch → Phase 2 Stream). |
| Sự kiện điểm / LMS đến **trước** bản ghi Tuyển sinh | `SVC-03` tạo hồ sơ tạm (placeholder), bổ sung khi lô Tuyển sinh về; sự kiện không tìm thấy hồ sơ vào hàng chờ thử lại có giới hạn. |
| Trùng lặp / sai thứ tự sự kiện giữa hai đường | Dùng `event_id` + `version` làm khóa Idempotency; chi tiết cơ chế do TV3 mô tả ở BPMN 2 và `REQ-03`. |
| Lệch dữ liệu giữa nhánh Batch và Stream | Đối soát định kỳ (reconciliation) hằng đêm so với nguồn gốc; lưu bản gốc ở Staging & Raw Store. |
| Chi phí hạ tầng cao hơn PA1 | Chỉ stream hai nguồn cần tức thì; hai nguồn còn lại giữ batch rẻ hơn. |

**Rủi ro còn lại:** nếu `LMS System` không hỗ trợ Webhook, cần một adapter đọc log hoặc API polling ngắn chu kỳ — vẫn nằm trong SVC-02 nên không đổi kiến trúc.

---

## 7. Liên kết

- Sơ đồ: `diagrams/c4_container.png`, `diagrams/archimate_app_bus.png`, `diagrams/bpmn_core_flow.png`.
- Quyết định kế tiếp: ADR 02 của TV3 (Polling Cronjob vs In-memory Stream Rule Engine) — thực hiện trên đường stream mà ADR này đã chọn.
