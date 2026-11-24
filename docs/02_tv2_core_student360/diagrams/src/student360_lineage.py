"""Sơ đồ gom 4 nguồn vào Student 360 Profile (data lineage). Chạy: python student360_lineage.py"""
from svgkit import Svg

W, H = 1600, 760
s = Svg(W, H)
s.defs.append('<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#374151"/></marker>')
s.text(30, 24, "Gom 4 nguồn dữ liệu vào Student 360 Profile (DO-05) — Data lineage", size=20, weight="700", anchor="start")
s.text(30, 50, "Khóa gộp duy nhất: student_id · Batch (SVC-01) ghi Admission/Employment · Stream (SVC-02) ghi Grade/LMS · Fast Alerting Engine (SVC-04) ghi risk_assessment",
       size=13, fill="#4b5563", anchor="start")

# columns
src = [
    ("EXT-01 Admission System", "DO-01 Admission Record", "student_id, full_name, entry_year, major,\nadmission_score, high_school", "Batch · hằng ngày", "#E5E7EB"),
    ("EXT-04 Grading System", "DO-03 Grade Event", "event_id, student_id, course_id, exam_type,\nscore, timestamp, version", "Stream · CDC", "#E5E7EB"),
    ("EXT-03 LMS System", "DO-02 LMS Activity Log", "activity_id, student_id, course_id, login_time,\nassignment_status, last_access", "Stream · Webhook", "#E5E7EB"),
    ("EXT-02 Career & Alumni System", "DO-04 Employment Record", "alumni_id, company, role,\nsalary_bracket, survey_year", "Batch · theo tháng", "#E5E7EB"),
]
tgt = [
    ("personal_info + admission_record", "Họ tên, ngày sinh, email, khóa, ngành, điểm tuyển sinh, trường THPT", "REQ-01"),
    ("academic_progress", "CPA, GPA kỳ gần nhất, tín chỉ tích lũy / nợ, course_grades[] (giữa kỳ, cuối kỳ, version)", "REQ-01 · REQ-02"),
    ("lms_summary", "last_login_timestamp, days_inactive, assignment_completion_rate, missed_attendance_count", "REQ-01 · REQ-02"),
    ("career_alumni_info", "is_graduated, current_status, target_company, skills[]", "REQ-01"),
]
y0, h, gap = 110, 120, 30
for i, (ex, do, fields, mode, col) in enumerate(src):
    y = y0 + i * (h + gap)
    s.rect(30, y, 440, h, fill=col, stroke="#6B7280", sw=1.6, rx=8)
    s.text(46, y + 20, ex, size=13, weight="700", anchor="start")
    s.text(46, y + 44, do, size=13, weight="700", fill="#0e7490", anchor="start")
    s.text(46, y + 78, fields, size=11, anchor="start", fill="#374151", lh=15)
    s.text(46, y + 108, mode, size=10.5, anchor="start", fill="#6b7280", italic=True)
    # ingestion service chip
    svc = "SVC-01 Batch Ingestion" if "Batch" in mode else "SVC-02 Stream Gateway"
    s.rect(540, y + 30, 230, 56, fill="#438DD5", stroke="#2E6DB4", sw=1.5, rx=8)
    s.text(655, y + 52, svc, size=12.5, weight="700", fill="#fff")
    s.text(655, y + 72, "chuẩn hóa · khử trùng lặp" if "Batch" in mode else "validate · Idempotency Key", size=10.5, fill="#DBEAFE")
    s.line([(470, y + 58), (540, y + 58)], marker="a")
    # to profile
    s.rect(850, y, 420, h, fill="#B5FFFF", stroke="#008C8C", sw=1.6)
    t = tgt[i]
    s.text(866, y + 22, t[0], size=13, weight="700", fill="#006b6b", anchor="start")
    s.text(866, y + 62, t[1], size=11, anchor="start", max_chars=56, fill="#1f2937", lh=15)
    s.text(866, y + 106, "Truy vết: " + t[2], size=10.5, anchor="start", fill="#6b7280", italic=True)
    s.line([(770, y + 58), (850, y + 58)], marker="a")

# profile frame + risk box
s.rect(830, 90, 760, 4 * (h + gap) - 10 + 20, fill="none", stroke="#008C8C", sw=2, rx=10, dash="8 5")
s.text(850, 78, "DO-05 Student 360 Profile (SVC-03 Student 360 Profile Service)", size=13, weight="700", fill="#006b6b", anchor="start")
s.rect(1330, 110, 240, 270, fill="#FFE4E6", stroke="#BE123C", sw=1.6, rx=8)
s.text(1450, 132, "risk_assessment", size=13, weight="700", fill="#9f1239")
s.text(1450, 200, "current_risk_level (LOW → CRITICAL)\nactive_alerts[ ] — alert_id, severity,\ntrigger_reason, status\n(ACTIVE / REVOKED / RESOLVED)", size=11, lh=16, fill="#1f2937")
s.text(1450, 296, "Do SVC-04 Fast Alerting Engine\nghi lại sau mỗi lần đánh giá luật", size=10.5, fill="#6b7280", italic=True, lh=14)
s.text(1450, 352, "Truy vết: REQ-02 · REQ-03", size=10.5, fill="#6b7280", italic=True)
s.rect(1330, 420, 240, 150, fill="#FFE4E6", stroke="#BE123C", sw=1.6, rx=8)
s.text(1450, 445, "DO-06 Academic Alert", size=13, weight="700", fill="#9f1239")
s.text(1450, 500, "alert_id, student_id, severity,\ntrigger_reason, latency_seconds,\nstatus", size=11, lh=16)
s.line([(1450, 420), (1450, 380)], marker="a")
s.text(1462, 402, "tóm tắt", size=10, fill="#6b7280", anchor="start")
s.save("../student360_lineage.svg")
print("ok")
