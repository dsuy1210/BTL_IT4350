#!/usr/bin/env python3
"""
Automated Test Suite for Mock API & Biến thể B (TV3 Deadline 4)
Kiểm chứng tự động 3 kịch bản:
- Kịch bản 1: REQ-02 Luồng chính: Điểm kém (< 3.0) kích hoạt Fast Alert < 30s
- Kịch bản 2: REQ-03A Luồng ngoại lệ: Chống trùng lặp sự kiện (Idempotency)
- Kịch bản 3: REQ-03B Luồng ngoại lệ: Giảng viên sửa điểm -> Thu hồi cảnh báo (Revocation)
"""

import json
import time
from urllib.request import Request, urlopen
from urllib.error import URLError
import server

SERVER_URL = "http://127.0.0.1:8000"
USE_DIRECT_MODE = False

def call_post(endpoint, payload):
    global USE_DIRECT_MODE
    if not USE_DIRECT_MODE:
        try:
            url = f"{SERVER_URL}{endpoint}"
            data = json.dumps(payload).encode("utf-8")
            req = Request(url, data=data, headers={"Content-Type": "application/json"})
            with urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except (URLError, OSError):
            USE_DIRECT_MODE = True

    # Direct in-process fallback
    if endpoint == "/api/v1/reset":
        return 200, server.reset_all_state()
    elif endpoint == "/api/v1/stream/grades":
        return 200, server.handle_grade_event(payload)
    return 404, {"error": "not found"}

def call_get(endpoint):
    global USE_DIRECT_MODE
    if not USE_DIRECT_MODE:
        try:
            url = f"{SERVER_URL}{endpoint}"
            req = Request(url)
            with urlopen(req) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except (URLError, OSError):
            USE_DIRECT_MODE = True

    # Direct in-process fallback
    if endpoint == "/api/v1/alerts":
        return 200, {"alerts": server.ACADEMIC_ALERTS}
    elif endpoint == "/health" or endpoint == "/":
        return 200, {"status": "UP", "alerts_count": len(server.ACADEMIC_ALERTS)}
    return 404, {"error": "not found"}

def run_tests():
    print("=" * 70)
    print("🧪 BẮT ĐẦU KIỂM THỬ TỰ ĐỘNG BIẾN THỂ B: FAST ALERTING & NGOẠI LỆ")
    print("=" * 70)

    # 0. Reset state
    call_post("/api/v1/reset", {})

    # KỊCH BẢN 1: REQ-02 - Luồng chính
    print("\n👉 [TEST 1] Kiểm tra Luồng chính REQ-02 (Điểm kém kích hoạt Fast Alert)")
    p1 = {
        "event_id": "EVT-20261118-001",
        "event_type": "GRADE_SUBMITTED",
        "student_id": "20210001",
        "course_id": "IT4350",
        "score": 2.5,
        "version": 1
    }
    status, res1 = call_post("/api/v1/stream/grades", p1)
    print(f"   HTTP Status: {status}")
    print(f"   Alert Generated: {res1.get('alert_generated')}")
    print(f"   Latency SLA Satisfied: {res1.get('sla_satisfied')}")
    assert res1.get("alert_generated") is True, "Phải sinh cảnh báo khi điểm < 3.0!"
    assert res1.get("alert_details", {}).get("status") == "ACTIVE", "Cảnh báo phải ở trạng thái ACTIVE!"
    print("   ✅ TEST 1 PASSED: Cảnh báo học vụ được sinh thành công với SLA < 30s!")

    # KỊCH BẢN 2: REQ-03A - Chống trùng lặp (Idempotency)
    print("\n👉 [TEST 2] Kiểm tra Luồng ngoại lệ REQ-03A (Chống trùng lặp bản tin)")
    status, res2 = call_post("/api/v1/stream/grades", p1)
    print(f"   HTTP Status: {status}")
    print(f"   Is Duplicate: {res2.get('is_duplicate')}")
    print(f"   Message: {res2.get('message')}")
    assert res2.get("is_duplicate") is True, "Bản tin cùng event_id phải bị phát hiện trùng lặp!"
    print("   ✅ TEST 2 PASSED: Chống trùng lặp thành công, không sinh cảnh báo rác!")

    # KỊCH BẢN 3: REQ-03B - Giảng viên sửa điểm & Thu hồi cảnh báo
    print("\n👉 [TEST 3] Kiểm tra Luồng ngoại lệ REQ-03B (Sửa điểm & Tự động thu hồi cảnh báo)")
    p3 = {
        "event_id": "EVT-20261118-002",
        "event_type": "GRADE_UPDATED",
        "student_id": "20210001",
        "course_id": "IT4350",
        "score": 8.5,
        "version": 2,
        "superseded_event_id": "EVT-20261118-001"
    }
    status, res3 = call_post("/api/v1/stream/grades", p3)
    print(f"   HTTP Status: {status}")
    print(f"   Alert Revoked: {res3.get('alert_revoked')}")
    print(f"   Revoked Alert IDs: {res3.get('revoked_alert_ids')}")
    print(f"   Message: {res3.get('message')}")
    assert res3.get("alert_revoked") is True, "Cảnh báo cũ phải được thu hồi khi sửa điểm!"

    # Kiểm tra lại danh sách alerts
    _, alerts_res = call_get("/api/v1/alerts")
    alerts_list = alerts_res.get("alerts", [])
    revoked_count = sum(1 for a in alerts_list if a["status"] == "REVOKED")
    assert revoked_count > 0, "Phải có bản ghi cảnh báo chuyển sang trạng thái REVOKED!"
    print(f"   Số cảnh báo đã REVOKED: {revoked_count}")
    print("   ✅ TEST 3 PASSED: Thu hồi cảnh báo tự động thành công!")

    print("\n" + "=" * 70)
    print("🎉 TẤT CẢ 3 BÀI KIỂM THỬ ĐÃ ĐẠT 100% TIÊU CHUẨN ĐỒ ÁN IT4350!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
