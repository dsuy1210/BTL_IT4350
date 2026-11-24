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

  // Chi tiết hồ sơ Student 360 cho từng sinh viên (dữ liệu mô phỏng, gom từ DO-01..DO-04)
  const profiles = {
    '20210001': {
      name: 'Nguyễn Văn An', risk: 'NGUY CƠ CAO (CPA < 2.2)', riskClass: 'badge badge-danger', cohort: 'K66', major: 'Công nghệ Thông tin (IT1)',
      email: 'an.nv210001@sis.hust.edu.vn', phone: '0987.654.321',
      admScore: '28.5 / 30.0 (Khối A00)', school: 'THPT Chuyên Hà Nội - Amsterdam', rank: 'Top 5% Khóa',
      cpa: '2.15 / 4.0', gpa: '1.80', credits: '68 / 8 tín chỉ',
      courseLabel: 'Môn IT4350 (Kiến trúc HTTT):', course: 'Giữa kỳ: 2.5 (Nguy cơ)',
      lastLogin: '17 ngày trước', submitRate: '45% (Bỏ 2 bài gần nhất)', absent: '4 buổi (> 20% định mức)', forum: '0 bài viết',
      careerStatus: 'Chưa đi thực tập', target: 'Software Engineering / Cloud', soft: 'Khá (Cần cải thiện giao tiếp)', alumniRate: '96% có việc làm trong 6 tháng'
    },
    '20210045': {
      name: 'Trần Thị Bích', risk: 'NGUY CƠ BỎ HỌC (14 ngày không tương tác)', riskClass: 'badge badge-warning', cohort: 'K66', major: 'Khoa học Máy tính (IT2)',
      email: 'bich.tt210045@sis.hust.edu.vn', phone: '0912.345.678',
      admScore: '27.0 / 30.0 (Khối A01)', school: 'THPT Phan Đình Phùng, Hà Nội', rank: 'Top 20% Khóa',
      cpa: '2.28 / 4.0', gpa: '2.05', credits: '72 / 4 tín chỉ',
      courseLabel: 'Môn IT3040 (Kỹ thuật lập trình):', course: 'Giữa kỳ: 3.0 (Sát ngưỡng)',
      lastLogin: '14 ngày trước', submitRate: '48% (Bỏ 1 bài gần nhất)', absent: '3 buổi (= 15% định mức)', forum: '1 bài viết',
      careerStatus: 'Đang tìm nơi thực tập', target: 'Data Engineering', soft: 'Tốt', alumniRate: '94% có việc làm trong 6 tháng'
    },
    '20210112': {
      name: 'Lê Hoàng Cường', risk: 'CẢNH BÁO MÔN HỌC (điểm < 3.0)', riskClass: 'badge badge-warning', cohort: 'K66', major: 'Hệ thống Thông tin (IT-E10)',
      email: 'cuong.lh210112@sis.hust.edu.vn', phone: '0868.112.233',
      admScore: '26.25 / 30.0 (Khối A00)', school: 'THPT Chuyên Lam Sơn, Thanh Hóa', rank: 'Top 30% Khóa',
      cpa: '2.45 / 4.0', gpa: '2.10', credits: '75 / 6 tín chỉ',
      courseLabel: 'Môn IT4010 (Hệ thống thông tin quản lý):', course: 'Giữa kỳ: 2.0 (Nguy cơ)',
      lastLogin: '3 ngày trước', submitRate: '70% (Chưa nộp bài tập lớn)', absent: '1 buổi', forum: '4 bài viết',
      careerStatus: 'Đã thực tập tại FPT Software', target: 'Business Analyst', soft: 'Khá', alumniRate: '92% có việc làm trong 6 tháng'
    }
  };
  let currentProfileId = '20210001';

  function renderProfile(id) {
    const p = profiles[id];
    if (!p) return;
    currentProfileId = id;
    document.getElementById('profile-name').textContent = p.name;
    const tag = document.getElementById('profile-risk-tag');
    tag.textContent = p.risk;
    tag.className = p.riskClass;
    document.getElementById('profile-id').textContent = id;
    document.getElementById('profile-cpa').textContent = p.cpa;
    document.getElementById('profile-it4350-score').textContent = p.course;
    document.querySelectorAll('[data-f]').forEach(el => {
      const k = el.getAttribute('data-f');
      if (p[k] !== undefined) el.textContent = p[k];
    });
  }

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
        renderProfile(btn.getAttribute('data-id'));
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

      // Cập nhật dữ liệu hồ sơ 360 của SV 20210001 (để lần mở sau vẫn đúng)
      Object.assign(profiles['20210001'], {
        cpa: '2.85 / 4.0 (Đã phục hồi)', course: 'Giữa kỳ: 8.5 (Đã đính chính)',
        risk: 'BÌNH THƯỜNG (AN TOÀN)', riskClass: 'badge badge-success'
      });
      if (currentProfileId === '20210001') renderProfile('20210001');
      const showingAn = currentProfileId === '20210001';
      const profileCpa = showingAn ? document.getElementById('profile-cpa') : null;
      const profileScore = showingAn ? document.getElementById('profile-it4350-score') : null;
      const profileTag = showingAn ? document.getElementById('profile-risk-tag') : null;

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
