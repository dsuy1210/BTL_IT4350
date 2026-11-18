/**
 * Student 360 & Fast Alerting Portal - Interactive Prototype (TV2 Prototype)
 * Course: IT4350 - Enterprise Architecture
 * Topic VIII: Student 360 & Data Hub (Biến thể B: Cảnh báo nhanh)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Tab Management
  const navItems = document.querySelectorAll('.nav-item');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const pageTitle = document.getElementById('page-title');
  const pageSubtitle = document.getElementById('page-subtitle');

  const tabTitles = {
    dashboard: {
      title: 'Dashboard Giám Sát Học Vụ & Cảnh Báo Sớm',
      subtitle: 'Hệ thống tích hợp dữ liệu tập trung Student 360 & Động cơ cảnh báo nhanh thời gian thực'
    },
    profile: {
      title: 'Hồ Sơ Toàn Diện Sinh Viên (Student 360 Profile)',
      subtitle: 'Hợp nhất từ 4 nguồn: Tuyển sinh, Quản lý điểm, LMS Học tập & Việc làm cựu sinh viên'
    },
    alerts: {
      title: 'Trung Tâm Cảnh Báo Nhanh (Fast Alerting Engine)',
      subtitle: 'Giám sát và đánh giá quy tắc thời gian thực theo Biến thể B (SLA < 30 giây & Xử lý ngoại lệ)'
    }
  };

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const targetTab = item.getAttribute('data-tab');
      navItems.forEach(nav => nav.classList.remove('active'));
      tabPanes.forEach(pane => pane.classList.remove('active'));

      item.classList.add('active');
      const activePane = document.getElementById(`tab-${targetTab}`);
      if (activePane) activePane.classList.add('active');

      if (tabTitles[targetTab]) {
        pageTitle.innerText = tabTitles[targetTab].title;
        pageSubtitle.innerText = tabTitles[targetTab].subtitle;
      }
    });
  });

  // Mock Students at Risk Data (Derived from Student 360 Profile)
  const students = [
    {
      id: '20210001',
      name: 'Nguyễn Văn An',
      classMajor: 'K66 - CNTT 01',
      cpa: 2.15,
      lms: '17 ngày không login, bỏ 2 bài tập',
      course: 'IT4350 (Điểm: 2.5)',
      riskLevel: 'CRITICAL',
      status: 'Cảnh báo cấp 1'
    },
    {
      id: '20210045',
      name: 'Trần Thị Bích',
      classMajor: 'K66 - KHMT 02',
      cpa: 2.28,
      lms: '14 ngày không tương tác, vắng 3 buổi',
      course: 'IT3040 (Điểm: 3.0)',
      riskLevel: 'HIGH',
      status: 'Nguy cơ bỏ học'
    },
    {
      id: '20210112',
      name: 'Lê Hoàng Cường',
      classMajor: 'K66 - HTTT 01',
      cpa: 2.45,
      lms: 'Không nộp bài tập lớn',
      course: 'IT4010 (Điểm: 2.0)',
      riskLevel: 'HIGH',
      status: 'Cảnh báo môn học'
    }
  ];

  // Mock Academic Alerts Data
  let alerts = [
    {
      id: 'ALT-20261118-001',
      timestamp: '2026-11-18 10:00:02',
      studentId: '20210001',
      studentName: 'Nguyễn Văn An',
      severity: 'CRITICAL',
      reason: 'Điểm giữa kỳ môn IT4350 = 2.5 (< 3.0) & vắng LMS 17 ngày',
      latency: '1.8 giây',
      status: 'ACTIVE'
    },
    {
      id: 'ALT-20261118-002',
      timestamp: '2026-11-18 09:42:15',
      studentId: '20210045',
      studentName: 'Trần Thị Bích',
      severity: 'WARNING',
      reason: 'Không tương tác LMS > 14 ngày, tỷ lệ nộp bài < 50%',
      latency: '2.4 giây',
      status: 'ACTIVE'
    },
    {
      id: 'ALT-20261117-009',
      timestamp: '2026-11-17 14:20:10',
      studentId: '20205562',
      studentName: 'Vũ Đức Duy',
      severity: 'WARNING',
      reason: 'Giảng viên sửa điểm kiểm tra từ 2.0 -> 8.0',
      latency: '1.2 giây',
      status: 'REVOKED'
    }
  ];

  // Render Risk Table
  function renderRiskTable() {
    const tbody = document.getElementById('risk-students-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    students.forEach(s => {
      const tr = document.createElement('tr');
      const badgeClass = s.riskLevel === 'CRITICAL' ? 'badge-danger' : 'badge-warning';
      tr.innerHTML = `
        <td><code>${s.id}</code></td>
        <td><strong>${s.name}</strong></td>
        <td>${s.classMajor}</td>
        <td><strong class="text-danger">${s.cpa.toFixed(2)}</strong></td>
        <td><small class="text-danger">${s.lms}</small></td>
        <td><span class="tag">${s.course}</span></td>
        <td><span class="badge ${badgeClass}">${s.status}</span></td>
        <td>
          <button class="btn btn-sm btn-secondary btn-view-profile" data-id="${s.id}">
            Xem 360
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    // Attach event for View 360 buttons
    document.querySelectorAll('.btn-view-profile').forEach(btn => {
      btn.addEventListener('click', () => {
        const profileTabBtn = document.querySelector('[data-tab="profile"]');
        if (profileTabBtn) profileTabBtn.click();
      });
    });
  }

  // Render Alerts Table
  function renderAlertsTable() {
    const tbody = document.getElementById('alerts-tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    let activeCount = 0;
    let revokedCount = 0;
    let resolvedCount = 0;

    alerts.forEach(a => {
      if (a.status === 'ACTIVE') activeCount++;
      else if (a.status === 'REVOKED') revokedCount++;
      else if (a.status === 'RESOLVED') resolvedCount++;

      let statusBadge = `<span class="badge badge-danger">ACTIVE</span>`;
      if (a.status === 'REVOKED') {
        statusBadge = `<span class="badge" style="background:#e2e8f0; color:#64748b; text-decoration:line-through;">REVOKED</span>`;
      } else if (a.status === 'RESOLVED') {
        statusBadge = `<span class="badge badge-success">RESOLVED</span>`;
      }

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><code>${a.id}</code></td>
        <td><small>${a.timestamp}</small></td>
        <td><strong>${a.studentName}</strong> (<code>${a.studentId}</code>)</td>
        <td><span class="badge ${a.severity === 'CRITICAL' ? 'badge-danger' : 'badge-warning'}">${a.severity}</span></td>
        <td>${a.reason}</td>
        <td><strong class="text-success">${a.latency}</strong></td>
        <td>${statusBadge}</td>
        <td>
          ${a.status === 'ACTIVE' ? `
            <button class="btn btn-sm btn-primary" onclick="alert('Đã mở quy trình hỗ trợ sinh viên ${a.studentName}')">
              Xử Lý Cảnh Báo
            </button>
          ` : `
            <small class="text-muted">Đã xử lý / Thu hồi</small>
          `}
        </td>
      `;
      tbody.appendChild(tr);
    });

    // Update counters
    document.getElementById('alert-counter').innerText = activeCount;
    document.getElementById('kpi-active-alerts').innerText = activeCount;
    document.getElementById('active-badge-count').innerText = activeCount;
    document.getElementById('revoked-badge-count').innerText = revokedCount;
    document.getElementById('resolved-badge-count').innerText = resolvedCount;
  }

  // Toast Notification Helper
  function showToast(title, message, sub, type = 'danger') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <div class="toast-icon">${type === 'danger' ? '🚨' : type === 'warning' ? '⚠️' : '✅'}</div>
      <div class="toast-body">
        <strong>${title}</strong>
        <p>${message}</p>
        <small>${sub}</small>
      </div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.5s ease';
      setTimeout(() => toast.remove(), 500);
    }, 6000);
  }

  // SIMULATION 1: Fast Alert Trigger (REQ-02)
  document.getElementById('btn-demo-trigger').addEventListener('click', () => {
    const now = new Date().toISOString().replace('T', ' ').substring(0, 19);
    const newAlert = {
      id: `ALT-LIVE-${Math.floor(Math.random() * 9000 + 1000)}`,
      timestamp: now,
      studentId: '20210001',
      studentName: 'Nguyễn Văn An',
      severity: 'CRITICAL',
      reason: 'Sự kiện điểm giữa kỳ IT4350 = 2.0 (< 3.0) vừa phát sinh từ Grading System',
      latency: '1.9 giây (SLA < 30s)',
      status: 'ACTIVE'
    };

    alerts.unshift(newAlert);
    renderAlertsTable();

    // Trigger visual toast
    showToast(
      'PHÁT HIỆN CẢNH BÁO HỌC VỤ MỚI (< 30s SLA)',
      'Sinh viên Nguyễn Văn An (20210001) vừa nhận điểm 2.0 môn IT4350. Fast Alerting Engine đã đánh giá quy tắc thành công!',
      '⏱️ Thời gian từ sự kiện đến UI: 1.9 giây (Đạt chuẩn Biến thể B)',
      'danger'
    );
  });

  // SIMULATION 2: Update Grade & Revoke Alert (REQ-03 Luồng Ngoại Lệ)
  document.getElementById('btn-demo-revoke').addEventListener('click', () => {
    let targetAlert = alerts.find(a => a.studentId === '20210001' && a.status === 'ACTIVE');
    if (targetAlert) {
      targetAlert.status = 'REVOKED';
      targetAlert.reason = 'ĐÃ THU HỒI: Giảng viên đã đính chính sửa điểm từ 2.0 -> 8.5';
      renderAlertsTable();

      // Update Student 360 Profile fields in DOM
      const profileCpa = document.getElementById('profile-cpa');
      const profileScore = document.getElementById('profile-it4350-score');
      const profileTag = document.getElementById('profile-risk-tag');

      if (profileCpa) profileCpa.innerText = '2.85 / 4.0 (Đã phục hồi)';
      if (profileScore) profileScore.innerText = 'Giữa kỳ: 8.5 (Đã đính chính)';
      if (profileTag) {
        profileTag.className = 'badge badge-success';
        profileTag.innerText = 'BÌNH THƯỜNG (AN TOÀN)';
      }

      showToast(
        'XỬ LÝ NGOẠI LỆ: THU HỒI CẢNH BÁO TỰ ĐỘNG (REQ-03)',
        'Giảng viên vừa sửa điểm môn IT4350 lên 8.5. Hồ sơ 360 đã cập nhật và Cảnh báo ALT-20261118 đã tự động chuyển sang REVOKED!',
        '⏱️ Thời gian thu hồi: 1.4 giây. Tránh gây hoang mang cho cố vấn.',
        'success'
      );
    } else {
      alert('Không có cảnh báo ACTIVE nào của sinh viên 20210001 để thu hồi. Hãy bấm nút giả lập màu xanh bên trái trước!');
    }
  });

  // Initial Render
  renderRiskTable();
  renderAlertsTable();
});
