/* =============================================================================
   main.js — Frontend JavaScript
   Machine Learning-Based Disease Risk Prediction System
   ============================================================================= */

'use strict';

// =============================================================================
// 1. DARK / LIGHT THEME TOGGLE
// =============================================================================

(function initTheme() {
  const html      = document.documentElement;
  const toggleBtn = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');

  // Load saved preference (default: dark)
  const saved = localStorage.getItem('theme') || 'dark';
  applyTheme(saved);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      const current = html.getAttribute('data-theme') || 'dark';
      const next    = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('theme', next);
    });
  }

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'dark' ? 'bi bi-moon-stars-fill' : 'bi bi-sun-fill';
    }
  }
})();


// =============================================================================
// 2. NAVBAR SCROLL EFFECT
// =============================================================================

(function navbarScroll() {
  const nav = document.getElementById('mainNav');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      nav.style.padding = '0.4rem 0';
    } else {
      nav.style.padding = '0.75rem 0';
    }
  }, { passive: true });
})();


// =============================================================================
// 3. AUTO-DISMISS FLASH ALERTS
// =============================================================================

(function autoDismissAlerts() {
  const alerts = document.querySelectorAll('.flash-alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });
})();


// =============================================================================
// 4. ANIMATE ELEMENTS ON SCROLL (Intersection Observer)
// =============================================================================

(function scrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in-up');
        entry.target.style.opacity = '1';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  // Observe cards and sections
  const targets = document.querySelectorAll(
    '.feature-card, .model-card, .step-card, .algo-card, .dash-stat-card, .chart-card'
  );
  targets.forEach((el, i) => {
    el.style.opacity      = '0';
    el.style.animationDelay = `${i * 60}ms`;
    observer.observe(el);
  });
})();


// =============================================================================
// 5. ANIMATED COUNTER (Stats bar on home page)
// =============================================================================

(function animateCounters() {
  const counters = document.querySelectorAll('.stat-number, .dash-stat-num');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));

  function animateCounter(el) {
    const text   = el.textContent.trim();
    const hasPlus = text.includes('+');
    const hasPct  = text.includes('%');
    const num     = parseFloat(text.replace(/[^0-9.]/g, ''));
    if (isNaN(num)) return;

    const duration = 1500;
    const start    = performance.now();

    function update(now) {
      const elapsed  = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased    = 1 - Math.pow(1 - progress, 3);
      const current  = Math.round(eased * num * 10) / 10;
      el.textContent = current + (hasPct ? '%' : '') + (hasPlus ? '+' : '');
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  }
})();


// =============================================================================
// 6. FORM INPUT FLOATING LABEL ANIMATION
// =============================================================================

(function floatingInputs() {
  document.querySelectorAll('.form-control-custom').forEach(input => {
    input.addEventListener('focus', () => {
      input.closest('.input-group-custom')?.classList.add('focused');
    });
    input.addEventListener('blur', () => {
      input.closest('.input-group-custom')?.classList.remove('focused');
    });
  });
})();


// =============================================================================
// 7. TABLE SORT (click column headers)
// =============================================================================

(function tableSorter() {
  document.querySelectorAll('.metrics-table').forEach(table => {
    const headers = table.querySelectorAll('thead th');
    headers.forEach((th, colIdx) => {
      th.style.cursor = 'pointer';
      th.title = 'Click to sort';
      let asc = true;

      th.addEventListener('click', () => {
        const tbody = table.querySelector('tbody');
        const rows  = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
          const aVal = a.cells[colIdx]?.textContent.trim() || '';
          const bVal = b.cells[colIdx]?.textContent.trim() || '';
          const aNum = parseFloat(aVal);
          const bNum = parseFloat(bVal);

          if (!isNaN(aNum) && !isNaN(bNum)) {
            return asc ? aNum - bNum : bNum - aNum;
          }
          return asc
            ? aVal.localeCompare(bVal)
            : bVal.localeCompare(aVal);
        });

        rows.forEach(row => tbody.appendChild(row));
        asc = !asc;

        // Update sort icon
        headers.forEach(h => h.querySelector('.sort-icon')?.remove());
        const icon = document.createElement('span');
        icon.className = 'sort-icon ms-1';
        icon.textContent = asc ? ' ↑' : ' ↓';
        th.appendChild(icon);
      });
    });
  });
})();


// =============================================================================
// 8. TOOLTIP INITIALISATION
// =============================================================================

(function initTooltips() {
  const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(el => new bootstrap.Tooltip(el, { trigger: 'hover' }));
})();


// =============================================================================
// 9. SMOOTH PAGE TRANSITION
// =============================================================================

(function pageTransition() {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.35s ease';
  window.addEventListener('load', () => {
    document.body.style.opacity = '1';
  });

  document.querySelectorAll('a[href]').forEach(link => {
    // Only internal links, not hash/external
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('http') ||
        href.startsWith('mailto') || link.getAttribute('target') === '_blank') return;

    link.addEventListener('click', (e) => {
      e.preventDefault();
      document.body.style.opacity = '0';
      setTimeout(() => { window.location.href = href; }, 250);
    });
  });
})();


// =============================================================================
// 10. COPY CODE BUTTON (for any <code> blocks)
// =============================================================================

(function copyCode() {
  document.querySelectorAll('code').forEach(codeEl => {
    const parent = codeEl.parentElement;
    if (parent.tagName === 'PRE') {
      const btn = document.createElement('button');
      btn.className   = 'btn btn-sm btn-outline-accent copy-btn';
      btn.textContent = 'Copy';
      btn.style.cssText = 'position:absolute;top:8px;right:8px;font-size:0.7rem;opacity:0.7';
      parent.style.position = 'relative';
      parent.appendChild(btn);

      btn.addEventListener('click', () => {
        navigator.clipboard.writeText(codeEl.textContent).then(() => {
          btn.textContent = '✓ Copied!';
          setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
        });
      });
    }
  });
})();


// =============================================================================
// 11. PRINT / EXPORT
// =============================================================================

function printPage() {
  window.print();
}


// =============================================================================
// 12. HERO RING ANIMATION (home page stat ring)
// =============================================================================

(function heroRing() {
  const ringFill = document.querySelector('.ring-fill');
  if (!ringFill) return;

  setTimeout(() => {
    ringFill.style.transition = 'stroke-dasharray 1.8s cubic-bezier(0.4,0,0.2,1)';
    ringFill.setAttribute('stroke-dasharray', '220 283');
  }, 400);
})();


// =============================================================================
// 13. CONFIRM DANGEROUS ACTIONS
// =============================================================================

document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', (e) => {
    if (!confirm(el.dataset.confirm)) {
      e.preventDefault();
    }
  });
});


// =============================================================================
// 14. ACTIVE NAV HIGHLIGHT (for JS-driven pages)
// =============================================================================

(function activeNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && path === href) {
      link.classList.add('active');
    }
  });
})();
