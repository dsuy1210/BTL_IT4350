"""BPMN 1 — Luồng chính End-to-End (REQ-01, REQ-02). Chạy: python bpmn_core_flow.py"""
from svgkit import Svg

W, H = 1900, 1010
TOP, LH, LX = 70, 150, 200
s = Svg(W, H)
s.defs.append('<marker id="seq" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">'
              '<path d="M0,0 L10,5 L0,10 z" fill="#111"/></marker>')

# --- tiêu đề ---
s.text(30, 24, "BPMN 1 — Luồng chính End-to-End: từ sự kiện điểm / hoạt động LMS đến cảnh báo cho Cố vấn học tập",
       size=20, weight="700", anchor="start")
s.text(30, 50, "Truy vết: REQ-01 (tích hợp Student 360) · REQ-02 (cảnh báo nhanh, SLA < 30 giây) · Ngoại lệ trùng lặp / sửa điểm xem BPMN 2 (REQ-03)",
       size=13, fill="#4b5563", anchor="start")

lanes = [
    ("Nguồn dữ liệu", "LMS System /\nGrading System", "#eef2ff"),
    ("Stream Ingestion Gateway", "SVC-02", "#f0fdf4"),
    ("Student 360 Profile Service", "SVC-03", "#fefce8"),
    ("Fast Alerting Engine", "SVC-04", "#fff1f2"),
    ("Academic Portal &\nNotification Service", "SVC-05", "#f0f9ff"),
    ("Cố vấn học tập /\nSinh viên", "Actor nghiệp vụ", "#faf5ff"),
]
for i, (n, sub, col) in enumerate(lanes):
    y = TOP + i * LH
    s.rect(40, y, W - 50, LH, fill=col, stroke="#6b7280", sw=1.2)
    s.rect(40, y, 160, LH, fill="#e5e7eb", stroke="#6b7280", sw=1.2)
    s.text(120, y + LH / 2 - 12, n, size=13, weight="700", max_chars=18)
    s.text(120, y + LH / 2 + 28, sub, size=11, fill="#4b5563", max_chars=20)
# pool
s.rect(10, TOP, 30, LH * 6, fill="#d1d5db", stroke="#6b7280", sw=1.2)
s.add(f'<text transform="translate(27,{TOP + LH * 3}) rotate(-90)" font-family="Inter, sans-serif" font-size="14" '
      f'font-weight="700" text-anchor="middle" dominant-baseline="central">Student 360 &amp; Data Hub (Biến thể B)</text>')


def cy(l):
    return TOP + l * LH + LH / 2


def task(x, l, txt, w=170, h=78, fill="#ffffff", dy=0):
    y = cy(l) - h / 2 + dy
    s.rect(x - w / 2, y, w, h, fill=fill, stroke="#111", sw=1.8, rx=10)
    s.text(x, y + h / 2, txt, size=12, max_chars=int(w / 6.6))
    return (x, y + h / 2 )


def event(x, l, kind, label, dy=0, lab_side="below", lab_w=18):
    y = cy(l) + dy
    if kind == "start":
        s.add(f'<circle cx="{x}" cy="{y}" r="17" fill="#dcfce7" stroke="#166534" stroke-width="2"/>')
    else:
        s.add(f'<circle cx="{x}" cy="{y}" r="17" fill="#fee2e2" stroke="#991b1b" stroke-width="4"/>')
    if lab_side == "below":
        s.text(x, y + 52, label, size=11, max_chars=lab_w, fill="#374151")
    else:
        s.text(x + 26, y, label, size=11, max_chars=lab_w, fill="#374151", anchor="start")


def gateway(x, l, kind, label, dy=0, lab_pos="top"):
    y = cy(l) + dy
    r = 26
    s.add(f'<polygon points="{x},{y - r} {x + r},{y} {x},{y + r} {x - r},{y}" fill="#fef9c3" stroke="#a16207" stroke-width="2"/>')
    if kind == "xor":
        s.line([(x - 10, y - 10), (x + 10, y + 10)], stroke="#a16207", sw=3)
        s.line([(x - 10, y + 10), (x + 10, y - 10)], stroke="#a16207", sw=3)
    else:
        s.line([(x - 12, y), (x + 12, y)], stroke="#a16207", sw=3)
        s.line([(x, y - 12), (x, y + 12)], stroke="#a16207", sw=3)
    if lab_pos == "top":
        s.text(x, y - r - 22, label, size=11, weight="600", max_chars=24, fill="#713f12")
    return (x, y)


def flow(pts, label=None, lpos=None):
    s.line(pts, marker="seq")
    if label:
        s.text(lpos[0], lpos[1], label, size=11, weight="700", fill="#0f172a")


# ---- Lane 0
event(260, 0, "start", "Có điểm mới / SV phát sinh hoạt động LMS", lab_w=20)
task(430, 0, "Phát sự kiện Grade Event / LMS Activity Log (Webhook / CDC)", w=190)
flow([(277, cy(0)), (335, cy(0))])
# ---- Lane 1
task(430, 1, "Tiếp nhận sự kiện, kiểm tra schema & Idempotency Key", w=190)
flow([(430, cy(0) + 39), (430, cy(1) - 39)])
g1 = gateway(660, 1, "xor", "Hợp lệ & chưa trùng lặp?")
flow([(525, cy(1)), (634, cy(1))])
event(660, 1, "end", "Loại bỏ / chuyển luồng ngoại lệ BPMN 2 (REQ-03)", dy=62, lab_side="right", lab_w=34)
flow([(660, cy(1) + 26), (660, cy(1) + 45)], "Không", (628, cy(1) + 36))
task(870, 1, "Phát sự kiện chuẩn hóa lên Message Broker (Kafka topic)", w=190)
flow([(686, cy(1)), (775, cy(1))], "Có", (730, cy(1) - 12))
g2 = gateway(1075, 1, "and", "Xử lý song song")
flow([(965, cy(1)), (1049, cy(1))])
# ---- Lane 2
task(1270, 2, "Cập nhật Student 360 Profile (DO-05) từ Grade Event / LMS Activity Log", w=200)
flow([(1075, cy(1) + 26), (1075, cy(2)), (1170, cy(2))])
event(1500, 2, "end", "Hồ sơ 360 đã đồng bộ", lab_w=20)
flow([(1370, cy(2)), (1483, cy(2))])
# ---- Lane 3
task(1270, 3, "Đánh giá luật: điểm < 3.0 hoặc > 14 ngày không tương tác LMS", w=200)
flow([(1075, cy(2)), (1075, cy(3)), (1170, cy(3))])
g3 = gateway(1465, 3, "xor", "Vi phạm ngưỡng?")
flow([(1370, cy(3)), (1439, cy(3))])
event(1465, 3, "end", "Không phát cảnh báo", dy=62, lab_side="right", lab_w=30)
flow([(1465, cy(3) + 26), (1465, cy(3) + 45)], "Không", (1433, cy(3) + 36))
task(1700, 3, "Tạo Academic Alert (DO-06) trạng thái ACTIVE trong ≤ 30 giây", w=190, fill="#ffe4e6")
flow([(1491, cy(3)), (1605, cy(3))], "Có", (1548, cy(3) - 12))
# ---- Lane 4
task(1700, 4, "Đẩy cảnh báo realtime lên Dashboard (WebSocket) & gửi email nhắc sinh viên", w=190)
flow([(1700, cy(3) + 39), (1700, cy(4) - 39)])
# ---- Lane 5
task(1700, 5, "Xem cảnh báo, mở Student 360 Profile & hẹn tư vấn", w=190)
flow([(1700, cy(4) + 39), (1700, cy(5) - 39)])
event(1500, 5, "end", "Alert → RESOLVED sau can thiệp", lab_w=22)
flow([(1605, cy(5)), (1517, cy(5))])

# --- SLA annotation
s.rect(870 - 110, TOP + 4 * LH + 20, 330, 100, fill="#fffbeb", stroke="#b45309", sw=1.5, rx=6, dash="6 4")
s.text(870 + 55, TOP + 4 * LH + 70,
       "SLA REQ-02: tổng thời gian từ khi Grade Event / LMS Activity Log phát sinh đến khi cảnh báo hiển thị trên Portal phải < 30 giây (ngân sách thiết kế ≈ 3 s, xem ADR 01 mục 5).",
       size=12, max_chars=44, fill="#78350f")

# --- Legend
ly = TOP + 5 * LH + 20
s.text(260, ly + 54, "Chú giải:", size=12, weight="700", anchor="start")
s.add(f'<circle cx="380" cy="{ly + 54}" r="10" fill="#dcfce7" stroke="#166534" stroke-width="2"/>')
s.text(398, ly + 54, "Start", size=11, anchor="start")
s.add(f'<circle cx="470" cy="{ly + 54}" r="10" fill="#fee2e2" stroke="#991b1b" stroke-width="3"/>')
s.text(488, ly + 54, "End", size=11, anchor="start")
s.add(f'<polygon points="560,{ly + 42} 576,{ly + 54} 560,{ly + 66} 544,{ly + 54}" fill="#fef9c3" stroke="#a16207" stroke-width="2"/>')
s.text(588, ly + 54, "Gateway (× XOR, + AND)", size=11, anchor="start")
s.rect(740, ly + 42, 40, 24, fill="#fff", stroke="#111", sw=1.6, rx=6)
s.text(790, ly + 54, "Task (Activity)", size=11, anchor="start")

s.save("../bpmn_core_flow.svg")
print("ok")
