#!/usr/bin/env python3
"""
Mock API Server - BTL IT4350: Student 360 & Fast Alerting (Biến thể B)
Phụ trách: Thành viên 3 (Hạng mục 4)

Triển khai bằng Python Standard Library (http.server) để chạy ngay lập tức
không cần cài đặt bất kỳ thư viện ngoài (pip) nào!
"""

import json
import time
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# In-Memory State Store (Giả lập Redis & Database của Data Hub)
PROCESSED_EVENT_IDS = set()  # Giả lập Redis Set để kiểm tra Idempotency
ACADEMIC_ALERTS = []         # Giả lập bảng Academic Alert trong PostgreSQL
STUDENT_PROFILES = {
    "20210001": {
        "student_id": "20210001",
        "full_name": "Nguyễn Văn An",
        "cohort": "K66",
        "major": "Công nghệ thông tin (IT1)",
        "admission_score": 28.5,
        "cpa": 2.15,
        "courses": {
            "IT4350": {"name": "Kiến trúc HTTT và Ứng dụng", "midterm": None, "final": None}
        },
        "lms": {"days_inactive": 17, "missed_assignments": 2}
    }
}

def reset_all_state():
    PROCESSED_EVENT_IDS.clear()
    ACADEMIC_ALERTS.clear()
    return {"message": "State reset successfully"}

def handle_grade_event(payload, start_time=None):
    if start_time is None:
        start_time = time.time()

    event_id = payload.get("event_id")
    event_type = payload.get("event_type", "GRADE_SUBMITTED")
    student_id = payload.get("student_id")
    course_id = payload.get("course_id")
    score = float(payload.get("score", 0.0))
    version = payload.get("version", 1)

    # BƯỚC 1: KIỂM TRA TÍNH CHỐNG TRÙNG LẶP (REQ-03A IDEMPOTENCY)
    if event_id in PROCESSED_EVENT_IDS:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "status": "DUPLICATE_IGNORED",
            "is_duplicate": True,
            "event_id": event_id,
            "message": f"Sự kiện {event_id} đã được xử lý trước đó. Chống lặp (Idempotent) thành công!",
            "latency_ms": round(elapsed_ms, 2)
        }

    PROCESSED_EVENT_IDS.add(event_id)

    # BƯỚC 2: CẬP NHẬT STUDENT 360 PROFILE SERVICE (SVC-03)
    if student_id in STUDENT_PROFILES:
        if course_id in STUDENT_PROFILES[student_id]["courses"]:
            STUDENT_PROFILES[student_id]["courses"][course_id]["midterm"] = score

    # BƯỚC 3: ĐÁNH GIÁ QUY TẮC CẢNH BÁO TỨC THÌ (FAST ALERTING ENGINE - SVC-04)
    # TÌNH HUỐNG A: GIẢNG VIÊN SỬA ĐIỂM (REQ-03B - THU HỒI CẢNH BÁO)
    if event_type == "GRADE_UPDATED" or version > 1:
        revoked_alerts = []
        for alert in ACADEMIC_ALERTS:
            if (alert["student_id"] == student_id and 
                alert["course_id"] == course_id and 
                alert["status"] == "ACTIVE"):
                alert["status"] = "REVOKED"
                alert["revoked_at"] = datetime.now(timezone.utc).isoformat()
                alert["revoked_reason"] = f"Điểm đã được giảng viên điều chỉnh lên {score} (version {version})"
                revoked_alerts.append(alert["alert_id"])

        elapsed_seconds = round(time.time() - start_time, 4)
        return {
            "status": "PROCESSED",
            "event_type": "GRADE_UPDATED",
            "event_id": event_id,
            "student_id": student_id,
            "new_score": score,
            "alert_revoked": len(revoked_alerts) > 0,
            "revoked_alert_ids": revoked_alerts,
            "message": f"Điểm đã cập nhật lên {score}. Đã thu hồi {len(revoked_alerts)} cảnh báo học vụ!",
            "processing_latency_seconds": elapsed_seconds
        }

    # TÌNH HUỐNG B: LUỒNG CHÍNH - PHÁT HIỆN ĐIỂM KÉM < 3.0 (REQ-02)
    alert_generated = False
    new_alert = None
    if score < 3.0:
        alert_id = f"ALT-{datetime.now().strftime('%Y%m%d')}-{len(ACADEMIC_ALERTS)+1:03d}"
        elapsed_seconds = round(time.time() - start_time + 1.2, 2)
        new_alert = {
            "alert_id": alert_id,
            "event_id": event_id,
            "student_id": student_id,
            "course_id": course_id,
            "severity": "CRITICAL" if score <= 2.0 else "WARNING",
            "trigger_reason": f"Điểm giữa kỳ môn {course_id} đạt {score}/10.0 (< 3.0)",
            "latency_seconds": f"{elapsed_seconds}s (SLA < 30s)",
            "status": "ACTIVE",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        ACADEMIC_ALERTS.insert(0, new_alert)
        alert_generated = True

    elapsed_total = round(time.time() - start_time, 4)
    return {
        "status": "PROCESSED",
        "event_id": event_id,
        "student_id": student_id,
        "score": score,
        "alert_generated": alert_generated,
        "alert_details": new_alert,
        "sla_satisfied": True,
        "latency_seconds": elapsed_total
    }

class FastAlertingHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/health":
            response = {
                "system": "Student 360 & Fast Alerting Data Hub",
                "course": "IT4350",
                "status": "UP",
                "core_services": {
                    "SVC-01: Batch Ingestion Service": "ONLINE",
                    "SVC-02: Stream Ingestion Gateway": "ONLINE",
                    "SVC-03: Student 360 Profile Service": "ONLINE",
                    "SVC-04: Fast Alerting Engine": "ACTIVE (< 30s SLA)",
                    "SVC-05: Academic Portal & Notification": "READY"
                },
                "alerts_count": len(ACADEMIC_ALERTS),
                "processed_events_count": len(PROCESSED_EVENT_IDS)
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))

        elif path == "/api/v1/alerts":
            self._set_headers(200)
            self.wfile.write(json.dumps({"alerts": ACADEMIC_ALERTS}, ensure_ascii=False, indent=2).encode("utf-8"))

        elif path.startswith("/api/v1/students/") and path.endswith("/profile"):
            student_id = path.split("/")[4]
            if student_id in STUDENT_PROFILES:
                self._set_headers(200)
                self.wfile.write(json.dumps(STUDENT_PROFILES[student_id], ensure_ascii=False, indent=2).encode("utf-8"))
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": f"Không tìm thấy sinh viên {student_id}"}, ensure_ascii=False).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint không tồn tại"}, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        start_time = time.time()
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except json.JSONDecodeError:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}, ensure_ascii=False).encode("utf-8"))
            return

        if path == "/api/v1/stream/grades":
            response = handle_grade_event(payload, start_time)
            self._set_headers(200)
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))

        elif path == "/api/v1/reset":
            res = reset_all_state()
            self._set_headers(200)
            self.wfile.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint không tồn tại"}, ensure_ascii=False).encode("utf-8"))

def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, FastAlertingHandler)
    print(f"🚀 [IT4350 Data Hub] Mock API Server đang chạy tại http://localhost:{port}")
    print("📌 Endpoints:")
    print(f"   - GET  http://localhost:{port}/health")
    print(f"   - GET  http://localhost:{port}/api/v1/alerts")
    print(f"   - GET  http://localhost:{port}/api/v1/students/20210001/profile")
    print(f"   - POST http://localhost:{port}/api/v1/stream/grades (Kèm payload JSON)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Dừng máy chủ Mock API.")
        httpd.server_close()

if __name__ == "__main__":
    run_server(8000)
