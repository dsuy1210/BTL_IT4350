# 📑 HẠNG MỤC 2 - TV2: SƠ ĐỒ ARCHIMATE (BUSINESS & APPLICATION), C4 CONTAINER & CẤU TRÚC DỮ LIỆU STUDENT 360

## 1. Sơ Đồ ArchiMate Tầng Nghiệp Vụ & Ứng Dụng (Business & Application Layer)

### 1.1 Tầng Nghiệp Vụ (Business Layer):
- **Business Actors:** Sinh viên, Giảng viên, Cố vấn học tập, Ban Giám hiệu.
- **Business Processes:** 
  - Quy trình Đồng bộ Dữ liệu Tuyển sinh & Cựu sinh viên định kỳ.
  - Quy trình Giám sát Học vụ & Cảnh báo Sớm (Early Warning Process).
  - Quy trình Tư vấn Học tập & Can thiệp Cá nhân hóa.
- **Business Services:** Dịch vụ Tra cứu Hồ sơ Sinh viên 360, Dịch vụ Cảnh báo Tức thì, Dịch vụ Báo cáo Đào tạo.

### 1.2 Tầng Ứng Dụng (Application Layer):
Ánh xạ trực tiếp **5 Core Services** và **6 Data Objects** đã chốt tại Bước 0:
1. `Batch Ingestion Service` truy cập và biến đổi: `Admission Record` và `Employment Record`.
2. `Stream Ingestion Gateway` tiếp nhận: `Grade Event` và `LMS Activity Log`.
3. `Student 360 Profile Service` lưu trữ, quản lý và phục vụ: `Student 360 Profile`.
4. `Fast Alerting Engine` xử lý luồng sự kiện và sinh ra: `Academic Alert`.
5. `Academic Portal & Notification Service` trình diễn dữ liệu và gửi thông báo cảnh báo đến Cố vấn học tập và Sinh viên.

<!-- Vẽ trên phần mềm Archi hoặc Draw.io rồi lưu file ảnh vào diagrams/archimate_app_bus.png -->

---

## 2. Sơ Đồ C4 Container (C4 Model - Level 2)

Sơ đồ C4 Container biểu diễn các khối kiến trúc phần mềm, công nghệ sử dụng và giao thức giao tiếp giữa các thành phần:

```mermaid
graph TD
    subgraph External_Systems ["Hệ Thống Bên Ngoài (External Systems)"]
        EXT1["Admission System<br/>[RDBMS / CSV API]"]
        EXT2["Career & Alumni System<br/>[REST API / Files]"]
        EXT3["LMS System (Moodle)<br/>[Webhook / Real-time Events]"]
        EXT4["Grading System<br/>[CDC / Debezium / Events]"]
    end

    subgraph Data_Hub ["Student 360 & Fast Alerting Platform"]
        SVC1["Batch Ingestion Service<br/>[Python / Apache Airflow / Spark]"]
        SVC2["Stream Ingestion Gateway<br/>[Apache Kafka Broker + Schema Registry]"]
        
        DB_STAGING[("Staging & Raw Store<br/>[PostgreSQL / MinIO]")]
        
        SVC3["Student 360 Profile Service<br/>[Spring Boot / Go / Node.js]"]
        DB_360[("Student 360 Master DB<br/>[PostgreSQL + MongoDB]")]
        CACHE_360[("In-Memory Cache<br/>[Redis]")]

        SVC4["Fast Alerting Engine<br/>[Apache Flink / In-memory Rule Engine]"]
        DB_ALERTS[("Alerts & Audit Store<br/>[PostgreSQL]")]

        SVC5["Academic Portal Backend<br/>[REST / GraphQL / WebSocket]"]
        UI_SPA["Academic Portal Frontend<br/>[React / HTML5 Dashboard]"]
    end

    actor Advisor as "Cố vấn học tập"
    actor Student as "Sinh viên"

    EXT1 -->|SFTP / Batch Job| SVC1
    EXT2 -->|REST API Lô| SVC1
    SVC1 -->|Write Raw| DB_STAGING
    SVC1 -->|Normalize & Upsert| SVC3

    EXT3 -->|HTTP POST Event| SVC2
    EXT4 -->|CDC Kafka Topic| SVC2

    SVC2 -->|Pub/Sub Grade/LMS Topic| SVC3
    SVC2 -->|Pub/Sub Event Stream| SVC4

    SVC3 -->|Read/Write Profile| DB_360
    SVC3 -->|Read Cache| CACHE_360

    SVC4 -->|Query Current Metrics| CACHE_360
    SVC4 -->|Emit Academic Alert| DB_ALERTS
    SVC4 -->|Push Realtime Alert < 30s| SVC5

    SVC5 -->|WebSocket Realtime Push| UI_SPA
    Advisor -->|Tra cứu & Nhận cảnh báo| UI_SPA
    Student -->|Xem hồ sơ cá nhân| UI_SPA
```

---

## 3. Cấu Trúc Dữ Liệu Hồ Sơ Student 360 (Data Object Design)

Hồ sơ **Student 360 Profile** được tổng hợp từ 4 nguồn:
1. **Từ `Admission System`:** Mã SV, Họ tên, Ngày sinh, Giới tính, Quê quán, Khóa tuyển sinh, Ngành học, Điểm thi đại học, Khối thi, Trường cấp 3.
2. **Từ `Grading System`:** Điểm trung bình học kỳ (GPA), Điểm tích lũy toàn khóa (CPA), Số tín chỉ đã đạt / còn nợ, Danh sách điểm từng môn học (Thường kỳ, Giữa kỳ, Cuối kỳ).
3. **Từ `LMS System`:** Thời gian đăng nhập gần nhất, Số giờ học trực tuyến trong tuần, Tỷ lệ nộp bài tập đúng hạn, Số buổi vắng học trên hệ thống điểm danh.
4. **Từ `Career & Alumni System`:** Tình trạng việc làm sau khi tốt nghiệp (Dành cho cựu sinh viên), Vị trí làm việc, Nhóm thu nhập, Kỹ năng thực tế được doanh nghiệp đánh giá cao.

> Chi tiết JSON Schema mẫu được định nghĩa đầy đủ tại file `schemas/student_360_profile_schema.json`.
