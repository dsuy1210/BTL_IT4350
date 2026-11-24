"""C4 Container (Level 2). Chạy: python c4_container.py"""
from svgkit import Svg, wrap, FONT
from html import escape

W, H = 1780, 1020
s = Svg(W, H)
s.defs.append('<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
              '<path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker>')

s.text(30, 24, "C4 Container (Level 2) — Student 360 & Fast Alerting Platform", size=20, weight="700", anchor="start")
s.text(30, 50, "Phân rã 5 Core Services thành các Container (công nghệ đề xuất) và kho dữ liệu · REQ-01 (đường Batch + Stream về hồ sơ 360), REQ-02 (Broker → Engine → Portal < 30 s)",
       size=13, fill="#4b5563", anchor="start")

# boundary
s.rect(310, 90, 1440, 770, fill="#F4F9FE", stroke="#1168BD", sw=2, rx=10, dash="8 5")
s.text(330, 108, "Student 360 & Fast Alerting Platform  [Software System]", size=13, weight="700", fill="#1168BD", anchor="start")
s.rect(20, 90, 250, 560, fill="#F9FAFB", stroke="#9CA3AF", sw=1.5, rx=10, dash="8 5")
s.text(36, 108, "Hệ thống bên ngoài", size=13, weight="700", fill="#4B5563", anchor="start")


def box(x, y, w, h, title, tech, desc, fill, stroke="#2E6DB4", rx=6):
    s.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.5, rx=rx)
    s.text(x + w / 2, y + 20, title, size=13, weight="700", fill="#fff", max_chars=int(w / 7.4), lh=15)
    n = len(wrap(title, int(w / 7.4)))
    s.text(x + w / 2, y + 20 + 15 * (n - 1) + 22, tech, size=10.5, fill="#DBEAFE", italic=True)
    s.text(x + w / 2, y + h - 24, desc, size=10.5, fill="#fff", max_chars=int(w / 6.0), lh=13)


def cyl(x, y, w, h, title, tech, desc):
    f, st = "#2F6FB0", "#1E4F85"
    s.add(f'<path d="M{x},{y + 12} v{h - 24} a{w / 2},12 0 0 0 {w},0 v-{h - 24} a{w / 2},12 0 0 0 -{w},0 z" fill="{f}" stroke="{st}" stroke-width="1.5"/>')
    s.add(f'<ellipse cx="{x + w / 2}" cy="{y + 12}" rx="{w / 2}" ry="12" fill="#3F82C8" stroke="{st}" stroke-width="1.5"/>')
    s.text(x + w / 2, y + 34, title, size=12.5, weight="700", fill="#fff", max_chars=int(w / 7.4))
    s.text(x + w / 2, y + 52, tech, size=10.5, fill="#DBEAFE", italic=True)
    s.text(x + w / 2, y + h - 12, desc, size=10, fill="#fff", max_chars=int(w / 5.6))


def ext(x, y, w, h, title, tech, desc):
    s.rect(x, y, w, h, fill="#8A8A8A", stroke="#6B6B6B", sw=1.5, rx=6)
    s.text(x + w / 2, y + 17, title, size=12, weight="700", fill="#fff", max_chars=int(w / 7))
    s.text(x + w / 2, y + 40, tech, size=10, fill="#F3F4F6", italic=True, max_chars=int(w / 5.6))
    s.text(x + w / 2, y + h - 12, desc, size=10, fill="#fff")


def person(cx, y, w, name):
    s.rect(cx - w / 2, y, w, 70, fill="#08427B", stroke="#052E56", sw=1.5, rx=14)
    s.text(cx, y + 24, name, size=13, weight="700", fill="#fff")
    s.text(cx, y + 48, "[Person]", size=10.5, fill="#BFDBFE", italic=True)


def lab(x, y, t, anchor="middle"):
    ls = wrap(t, 26)
    w = max(len(l) for l in ls) * 5.6 + 8
    h = 13 * len(ls) + 4
    x0 = x - w / 2 if anchor == "middle" else x - 3
    s.rect(x0, y - h / 2, w, h, fill="#ffffff", stroke="none", sw=0, extra='opacity="0.92"')
    s.text(x0 + w / 2, y, t, size=10, fill="#111827", max_chars=26, lh=13)


def edge(pts):
    s.line(pts, stroke="#374151", sw=1.5, marker="a")


# ---- externals
ext(40, 125, 210, 70, "EXT-01 Admission System", "[Hệ thống ngoài: RDBMS / CSV]", "Batch")
ext(40, 215, 210, 70, "EXT-02 Career & Alumni", "[Hệ thống ngoài: REST API / File]", "Batch")
ext(40, 500, 210, 70, "EXT-03 LMS System", "[Hệ thống ngoài: Moodle Webhook]", "Real-time Event")
ext(40, 590, 210, 70, "EXT-04 Grading System", "[Hệ thống ngoài: DB + CDC]", "Real-time CDC")

# ---- batch
B, C, D, E = 340, 720, 1100, 1470
CW = 270
box(B, 130, CW, 130, "SVC-01 Batch Ingestion Service", "[Container: Python + Apache Airflow]", "Chuẩn hóa dữ liệu lô Tuyển sinh / Việc làm", "#438DD5")
cyl(B, 320, CW, 100, "Staging & Raw Store", "[Container: PostgreSQL / MinIO]", "Lưu bản gốc để đối soát")
box(B, 500, CW, 160, "SVC-02 Stream Ingestion Gateway", "[Container: API Gateway + Schema Registry]", "Validate schema, kiểm tra Idempotency Key, publish topic", "#438DD5")
cyl(B, 710, CW, 100, "Message Broker", "[Container: Apache Kafka]", "Topic grade-events, lms-events")
# ---- C
cyl(C, 130, CW, 100, "Student 360 Master DB", "[Container: PostgreSQL JSONB]", "DO-05 Student 360 Profile")
box(C, 300, CW, 120, "SVC-03 Student 360 Profile Service", "[Container: Spring Boot REST API]", "Tổng hợp & truy vấn hồ sơ 360", "#438DD5")
cyl(C, 520, CW, 100, "In-memory Cache", "[Container: Redis]", "Chỉ số hiện tại, Idempotency Key")
# ---- D
cyl(D, 330, CW, 100, "Alerts & Audit Store", "[Container: PostgreSQL]", "DO-06 Academic Alert")
box(D, 520, CW, 130, "SVC-04 Fast Alerting Engine", "[Container: Kafka Streams / Flink]", "Đánh giá luật in-memory, sinh Academic Alert", "#438DD5")
# ---- E
box(E, 300, CW, 120, "SVC-05 Academic Portal & Notification", "[Container: Node.js REST + WebSocket]", "Dashboard API, đẩy cảnh báo, gửi email", "#438DD5")
box(E, 520, CW, 110, "Academic Portal Frontend", "[Container: Web SPA - HTML5 / JS]", "Dashboard, Student 360, Alert Popup", "#6AA5E0")
person(1530, 910, 170, "Cố vấn học tập")
person(1700, 910, 150, "Sinh viên")

# ---- edges
edge([(250, 160), (340, 160)]); lab(295, 148, "SFTP / JDBC")
edge([(250, 250), (340, 250)]); lab(295, 238, "REST API (lô)")
edge([(475, 260), (475, 320)]); lab(485, 292, "ghi dữ liệu gốc", "start")
edge([(610, 190), (665, 190), (665, 360), (720, 360)]); lab(667, 222, "REST: upsert Admission / Employment")
edge([(250, 535), (340, 535)]); lab(295, 523, "HTTPS Webhook")
edge([(250, 625), (340, 625)]); lab(295, 613, "CDC (Debezium)")
edge([(475, 660), (475, 710)]); lab(540, 685, "publish", "start")
edge([(610, 770), (670, 770), (670, 400), (720, 400)]); lab(640, 440, "consume Grade / LMS")
edge([(610, 560), (720, 560)]); lab(665, 548, "Idempotency Key")
edge([(855, 300), (855, 230)]); lab(880, 265, "SQL", "start")
edge([(855, 420), (855, 520)]); lab(870, 470, "ghi chỉ số hiện tại", "start")
edge([(1100, 590), (990, 590)]); lab(1045, 606, "đọc chỉ số")
edge([(610, 790), (1235, 790), (1235, 650)]); lab(900, 790, "consume (< 1 s)")
edge([(1235, 520), (1235, 430)]); lab(1250, 475, "ghi Academic Alert", "start")
edge([(1370, 560), (1420, 560), (1420, 370), (1470, 370)]); lab(1420, 470, "push Alert (< 30 s)")
edge([(1605, 300), (1605, 268), (775, 268), (775, 300)]); lab(1190, 268, "REST: lấy hồ sơ 360")
edge([(1605, 420), (1605, 520)]); lab(1620, 470, "WebSocket + JSON/HTTPS", "start")
edge([(1530, 910), (1530, 630)]); lab(1530, 790, "xem & nhận cảnh báo")
edge([(1700, 910), (1700, 630)]); lab(1700, 740, "xem hồ sơ cá nhân")

# ---- legend
s.rect(30, 700, 250, 200, fill="#fff", stroke="#9CA3AF", sw=1, rx=6)
s.text(42, 718, "Chú giải C4", size=12, weight="700", anchor="start")
for i, (col, t) in enumerate([("#438DD5", "Container (ứng dụng / dịch vụ)"), ("#2F6FB0", "Container kho dữ liệu"),
                              ("#8A8A8A", "Hệ thống ngoài"), ("#08427B", "Người dùng")]):
    s.rect(42, 736 + i * 28, 30, 18, fill=col, stroke="#1f2937", sw=1, rx=3)
    s.text(82, 745 + i * 28, t, size=11, anchor="start")
s.text(42, 860, "Mũi tên: hướng dữ liệu / lời gọi,\nnhãn = giao thức hoặc nội dung.", size=10.5, anchor="start", fill="#4b5563")

s.save("../c4_container.svg")
print("ok")
