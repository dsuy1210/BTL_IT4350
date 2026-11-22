"""ArchiMate — tầng Business & Application (5 Core Services, 6 Data Objects). Chạy: python archimate_app_bus.py"""
from svgkit import Svg

W, H = 1780, 1120
s = Svg(W, H)
BUS, BUS_S = "#FFFFB5", "#A8A000"
APP, APP_S = "#B5FFFF", "#008C8C"
DAT, DAT_S = "#DDFBFF", "#008C8C"
EXTF, EXTS = "#E5E7EB", "#6B7280"

s.defs.append('<marker id="serve" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">'
              '<path d="M1,1 L9,5 L1,9" fill="none" stroke="#111" stroke-width="1.6"/></marker>'
              '<marker id="flowm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">'
              '<path d="M0,0 L10,5 L0,10 z" fill="#111"/></marker>'
              '<marker id="real" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto">'
              '<path d="M1,1 L11,6 L1,11 z" fill="#fff" stroke="#111" stroke-width="1.4"/></marker>')

s.text(30, 24, "ArchiMate — Tầng Business & Application của Student 360 & Data Hub (Biến thể B)", size=20, weight="700", anchor="start")
s.text(30, 50, "Dùng đúng 5 Core Services (SVC-01..05), 6 Data Objects (DO-01..06) và 4 nguồn ngoài (EXT-01..04) của Hợp đồng chung · Truy vết REQ-01, REQ-02, REQ-03",
       size=13, fill="#4b5563", anchor="start")

# ---- Bands
s.rect(20, 70, W - 40, 420, fill="#FFFFE6", stroke=BUS_S, sw=1.5, rx=8, dash="8 5")
s.text(36, 86, "BUSINESS LAYER", size=13, weight="700", fill="#7a7400", anchor="start")
s.rect(20, 510, W - 40, 590, fill="#EAFFFF", stroke=APP_S, sw=1.5, rx=8, dash="8 5")
s.text(36, 526, "APPLICATION LAYER", size=13, weight="700", fill="#006b6b", anchor="start")


def actor(cx, y, w, txt):
    s.rect(cx - w / 2, y, w, 50, fill=BUS, stroke=BUS_S, sw=1.6)
    ix, iy = cx - w / 2 + 16, y + 10
    s.add(f'<circle cx="{ix}" cy="{iy + 4}" r="4" fill="none" stroke="#555" stroke-width="1.3"/>')
    s.line([(ix, iy + 8), (ix, iy + 20)], stroke="#555", sw=1.3)
    s.line([(ix - 6, iy + 12), (ix + 6, iy + 12)], stroke="#555", sw=1.3)
    s.line([(ix, iy + 20), (ix - 5, iy + 28)], stroke="#555", sw=1.3)
    s.line([(ix, iy + 20), (ix + 5, iy + 28)], stroke="#555", sw=1.3)
    s.text(cx + 8, y + 25, txt, size=13, weight="600", max_chars=int(w / 8))


def bservice(cx, y, w, txt):
    s.rect(cx - w / 2, y, w, 60, fill=BUS, stroke=BUS_S, sw=1.6, rx=30)
    s.text(cx, y + 30, txt, size=13, weight="600", max_chars=int(w / 8.2))


def bprocess(cx, y, w, txt):
    s.rect(cx - w / 2, y, w, 70, fill=BUS, stroke=BUS_S, sw=1.6, rx=12)
    ix, iy = cx - w / 2 + 12, y + 10
    s.add(f'<polygon points="{ix},{iy} {ix + 10},{iy} {ix + 10},{iy - 4} {ix + 20},{iy + 4} {ix + 10},{iy + 12} {ix + 10},{iy + 8} {ix},{iy + 8}" fill="#fff" stroke="#555" stroke-width="1"/>')
    s.text(cx + 8, y + 38, txt, size=13, weight="600", max_chars=int(w / 8.2))


def comp(cx, y, w, h, code, name, desc):
    x = cx - w / 2
    s.rect(x, y, w, h, fill=APP, stroke=APP_S, sw=2)
    # icon
    s.rect(x + w - 34, y + 8, 22, 14, fill=APP, stroke="#444", sw=1.2)
    s.rect(x + w - 40, y + 11, 10, 4, fill=APP, stroke="#444", sw=1)
    s.rect(x + w - 40, y + 17, 10, 4, fill=APP, stroke="#444", sw=1)
    s.text(x + 12, y + 20, code, size=12, weight="700", fill="#006b6b", anchor="start")
    s.text(x + 12, y + 46, name, size=14, weight="700", anchor="start", max_chars=34, lh=17)
    s.text(x + 12, y + 86, desc, size=11, fill="#374151", anchor="start", max_chars=44)


def dobj(cx, y, w, code, name, read=False):
    s.rect(cx - w / 2, y, w, 40, fill=DAT, stroke=DAT_S, sw=1.4, dash="5 3" if read else None)
    s.rect(cx - w / 2, y, w, 10, fill="#C4F1FA", stroke=DAT_S, sw=1.4)
    s.text(cx, y + 26, f"{code} {name}" + (" (đọc)" if read else ""), size=12, weight="600")


def serving(pts):
    s.line(pts, marker="serve")


def realization(pts):
    s.line(pts, dash="3 4", marker="real")


def flow(pts, n):
    s.line(pts, dash="7 4", marker="flowm")
    # chấm số flow ở giữa đoạn dài nhất
    best = max(range(len(pts) - 1), key=lambda i: abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]))
    mx = (pts[best][0] + pts[best + 1][0]) / 2
    my = (pts[best][1] + pts[best + 1][1]) / 2
    s.add(f'<circle cx="{mx}" cy="{my}" r="11" fill="#fff" stroke="#111" stroke-width="1.4"/>')
    s.text(mx, my, str(n), size=12, weight="700")


# ---- Business: actors
Y_A, Y_S, Y_P = 100, 190, 330
actor(190, Y_A, 210, "Ban Giám hiệu")
actor(540, Y_A, 210, "Giảng viên")
actor(1100, Y_A, 260, "Cố vấn học tập")
actor(1550, Y_A, 210, "Sinh viên")
# services
bservice(190, Y_S, 280, "Dịch vụ Báo cáo Đào tạo")
bservice(960, Y_S, 260, "Dịch vụ Cảnh báo Tức thì")
bservice(1550, Y_S, 290, "Dịch vụ Tra cứu Hồ sơ Sinh viên 360")
# processes
bprocess(190, Y_P, 300, "Đồng bộ Dữ liệu Tuyển sinh & Cựu sinh viên")
bprocess(960, Y_P, 360, "Giám sát Học vụ & Cảnh báo Sớm (Early Warning)")
bprocess(1550, Y_P, 300, "Tư vấn Học tập & Can thiệp Cá nhân hóa")

# business relations
serving([(190, Y_S), (190, Y_A + 50)])                      # Báo cáo -> BGH
serving([(1030, Y_S), (1030, Y_A + 50)])                    # Cảnh báo -> Cố vấn
serving([(1550, Y_S), (1550, Y_A + 50)])                    # Tra cứu -> SV
serving([(1450, Y_S), (1450, 172), (1200, 172), (1200, Y_A + 50)])   # Tra cứu -> Cố vấn
realization([(190, Y_P), (190, Y_S + 60)])                  # P3 -> Báo cáo
realization([(960, Y_P), (960, Y_S + 60)])                  # P1 -> Cảnh báo
realization([(1550, Y_P), (1550, Y_S + 60)])                # P2 -> Tra cứu
s.line([(540, Y_A + 50), (540, Y_P + 35), (780, Y_P + 35)], marker="flowm")   # Giảng viên -> P1 (triggering)
s.text(560, 262, "nhập điểm / giao bài (kích hoạt sự kiện)", size=11, anchor="start", fill="#374151", italic=True)

# ---- Application components
Y_C, HC, WC = 620, 215, 300
cx = [190, 530, 870, 1210, 1550]
comp(cx[0], Y_C, WC, HC, "SVC-01", "Batch Ingestion Service", "Thu thập & chuẩn hóa dữ liệu lô từ Tuyển sinh, Việc làm")
comp(cx[1], Y_C, WC, HC, "SVC-02", "Stream Ingestion Gateway", "Nhận sự kiện điểm / LMS, lọc trùng, kiểm tra Idempotency")
comp(cx[2], Y_C, WC, HC, "SVC-03", "Student 360 Profile Service", "Tổng hợp 4 nguồn thành hồ sơ 360 duy nhất, API truy vấn")
comp(cx[3], Y_C, WC, HC, "SVC-04", "Fast Alerting Engine", "Đánh giá luật trên luồng sự kiện, phát cảnh báo < 30 s")
comp(cx[4], Y_C, WC, HC, "SVC-05", "Academic Portal & Notification Svc", "Dashboard cho Cố vấn / Sinh viên, đẩy thông báo")

dobj(cx[0], 725, 260, "DO-01", "Admission Record")
dobj(cx[0], 775, 260, "DO-04", "Employment Record")
dobj(cx[1], 725, 260, "DO-02", "LMS Activity Log")
dobj(cx[1], 775, 260, "DO-03", "Grade Event")
dobj(cx[2], 750, 260, "DO-05", "Student 360 Profile")
dobj(cx[3], 750, 260, "DO-06", "Academic Alert")
dobj(cx[4], 725, 260, "DO-05", "Student 360 Profile", read=True)
dobj(cx[4], 775, 260, "DO-06", "Academic Alert", read=True)

# ---- Application serves business
serving([(190, Y_C), (190, Y_P + 70)])                            # SVC-01 -> P3
serving([(900, Y_C), (900, Y_P + 70)])                            # SVC-03 -> P1
serving([(1075, Y_C), (1075, Y_P + 70)])                          # SVC-04 -> P1
serving([(1550, Y_C), (1550, Y_P + 70)])                          # SVC-05 -> P2
serving([(1430, Y_C), (1430, 480), (1125, 480), (1125, Y_P + 70)])  # SVC-05 -> P1

# ---- Application flows
flow([(250, Y_C), (250, 585), (810, 585), (810, Y_C)], 1)           # SVC-01 -> SVC-03
flow([(600, Y_C), (600, 560), (850, 560), (850, Y_C)], 2)           # SVC-02 -> SVC-03
flow([(1020, 735), (1060, 735)], 3)                                  # SVC-03 -> SVC-04
flow([(1360, 735), (1400, 735)], 4)                                  # SVC-04 -> SVC-05
flow([(530, Y_C + HC), (530, 900), (1180, 900), (1180, Y_C + HC)], 5)   # SVC-02 -> SVC-04
flow([(870, Y_C + HC), (870, 930), (1520, 930), (1520, Y_C + HC)], 6)   # SVC-03 -> SVC-05

# ---- External systems
def ext(cx_, code, name, mode):
    s.rect(cx_ - 70, 970, 140, 70, fill=EXTF, stroke=EXTS, sw=1.6)
    s.text(cx_, 988, code, size=11, weight="700", fill="#374151")
    s.text(cx_, 1010, name, size=12, weight="600", max_chars=17)
    s.text(cx_, 1030, mode, size=10, fill="#6b7280")


ext(120, "EXT-01", "Admission System", "Batch")
ext(280, "EXT-02", "Career & Alumni System", "Batch")
ext(450, "EXT-03", "LMS System", "Real-time Event")
ext(610, "EXT-04", "Grading System", "Real-time CDC")
for x_ in (120, 280):
    s.line([(x_, 970), (x_, Y_C + HC + 0)], dash="7 4", marker="flowm")
for x_ in (450, 610):
    s.line([(x_, 970), (x_, Y_C + HC + 0)], dash="7 4", marker="flowm")
# (EXT -> SVC-01/02 đi thẳng lên; riêng EXT-01,02 nằm dưới SVC-01 và EXT-03,04 nằm dưới SVC-02)

# ---- Legend flows
lx, ly = 800, 965
s.rect(lx - 20, ly - 12, 960, 140, fill="#ffffff", stroke="#9ca3af", sw=1, rx=6)
s.text(lx, ly + 6, "Chú giải luồng dữ liệu giữa các Core Services (Flow)", size=12, weight="700", anchor="start")
items = [
    "① SVC-01 → SVC-03: Admission/Employment Record đã chuẩn hóa (upsert)",
    "② SVC-02 → SVC-03: Grade Event / LMS Activity Log cập nhật hồ sơ",
    "③ SVC-03 → SVC-04: chỉ số hiện tại (CPA, ngày không hoạt động LMS)",
    "④ SVC-04 → SVC-05: Academic Alert (ACTIVE / REVOKED)",
    "⑤ SVC-02 → SVC-04: sự kiện thô để đánh giá luật tức thì",
    "⑥ SVC-03 → SVC-05: Student 360 Profile hiển thị trên Portal",
]
for i, t in enumerate(items):
    s.text(lx, ly + 30 + 17 * i, t.replace("①", "1.").replace("②", "2.").replace("③", "3.").replace("④", "4.").replace("⑤", "5.").replace("⑥", "6."),
           size=11, anchor="start", fill="#1f2937")
# notation
nx = lx + 560
s.text(nx, ly + 6, "Ký hiệu quan hệ", size=12, weight="700", anchor="start")
s.line([(nx, ly + 32), (nx + 60, ly + 32)], marker="serve"); s.text(nx + 72, ly + 32, "Serving (phục vụ)", size=11, anchor="start")
s.line([(nx, ly + 54), (nx + 60, ly + 54)], dash="3 4", marker="real"); s.text(nx + 72, ly + 54, "Realization (hiện thực hóa)", size=11, anchor="start")
s.line([(nx, ly + 76), (nx + 60, ly + 76)], dash="7 4", marker="flowm"); s.text(nx + 72, ly + 76, "Flow (luồng dữ liệu)", size=11, anchor="start")
s.line([(nx, ly + 98), (nx + 60, ly + 98)], marker="flowm"); s.text(nx + 72, ly + 98, "Triggering (kích hoạt)", size=11, anchor="start")
s.text(nx, ly + 120, "Data Object nằm trong Component = Component truy cập", size=10, anchor="start", fill="#6b7280")

s.save("../archimate_app_bus.svg")
print("ok")
