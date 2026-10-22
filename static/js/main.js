/**
 * FarmDirect - Frontend JavaScript
 * Handles cart interactions, payment option tab switching,
 * responsive mobile navigation, and demo quick-fill logins.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Navigation Toggle
  const navToggle = document.querySelector('.mobile-nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      const icon = navToggle.querySelector('i');
      if (icon) {
        if (navLinks.classList.contains('open')) {
          icon.className = 'fa-solid fa-xmark';
        } else {
          icon.className = 'fa-solid fa-bars';
        }
      }
    });
  }

  // 2. Alert Dismissal
  const alertCloses = document.querySelectorAll('.alert-close');
  alertCloses.forEach(btn => {
    btn.addEventListener('click', function () {
      const alert = this.closest('.alert');
      if (alert) {
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 250);
      }
    });
  });

  // 3. AJAX Add to Cart (Enhances buttons without page reload)
  const ajaxAddForms = document.querySelectorAll('.ajax-add-cart-form');
  ajaxAddForms.forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      const submitBtn = this.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : '';

      if (submitBtn) {
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Adding...';
        submitBtn.disabled = true;
      }

      fetch('/api/cart/add', {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Update navbar cart count
          const cartBadges = document.querySelectorAll('.cart-badge-count');
          cartBadges.forEach(badge => {
            badge.textContent = data.cart_count;
            badge.classList.add('pulse');
            setTimeout(() => badge.classList.remove('pulse'), 600);
          });

          showToast(data.message || 'Product added to cart!', 'success');
        } else {
          showToast(data.message || 'Could not add to cart', 'error');
        }
      })
      .catch(err => {
        console.error('Cart add error:', err);
        // Fallback: normal submit if fetch fails
        this.submit();
      })
      .finally(() => {
        if (submitBtn) {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }
      });
    });
  });

  // 4. Payment Method Tab Switcher (Checkout Page)
  const paymentTabs = document.querySelectorAll('.payment-tab-btn');
  const paymentPanels = document.querySelectorAll('.payment-panel');
  const hiddenPaymentInput = document.getElementById('selected-payment-method');

  if (paymentTabs.length && paymentPanels.length) {
    paymentTabs.forEach(tab => {
      tab.addEventListener('click', function () {
        const method = this.getAttribute('data-method');
        const targetPanelId = `panel-${method}`;

        // Toggle active tabs
        paymentTabs.forEach(t => t.classList.remove('active'));
        this.classList.add('active');

        // Toggle active panels
        paymentPanels.forEach(panel => {
          if (panel.id === targetPanelId) {
            panel.classList.add('active');
          } else {
            panel.classList.remove('active');
          }
        });

        // Update hidden field value for backend order processing
        if (hiddenPaymentInput) {
          let label = 'Cash on Delivery';
          if (method === 'upi') label = 'UPI (QR / Google Pay / PhonePe)';
          else if (method === 'card') label = 'Credit / Debit Card';
          else if (method === 'netbanking') label = 'Net Banking';
          hiddenPaymentInput.value = label;
        }
      });
    });
  }

  // 5. Demo Account Quick-Fill (Login Page)
  window.fillDemoAccount = function (role) {
    const emailInput = document.getElementById('login-email');
    const passwordInput = document.getElementById('login-password');

    if (!emailInput || !passwordInput) return;

    if (role === 'customer') {
      emailInput.value = 'priya@gmail.com';
      passwordInput.value = 'customer123';
      showToast('Loaded demo credentials for Customer (Priya Sharma)', 'info');
    } else if (role === 'farmer') {
      emailInput.value = 'ramesh@farmdirect.com';
      passwordInput.value = 'farmer123';
      showToast('Loaded demo credentials for Farmer (Ramesh Patel)', 'info');
    } else if (role === 'farmer2') {
      emailInput.value = 'sunita@farmdirect.com';
      passwordInput.value = 'farmer123';
      showToast('Loaded demo credentials for Farmer (Sunita Sharma)', 'info');
    } else if (role === 'admin') {
      emailInput.value = 'admin@farmdirect.com';
      passwordInput.value = 'admin123';
      showToast('Loaded demo credentials for Administrator', 'info');
    }
  };

  // 6. Toast Notification Helper
  function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.position = 'fixed';
      container.style.bottom = '24px';
      container.style.right = '24px';
      container.style.zIndex = '9999';
      container.style.display = 'flex';
      container.style.flexDirection = 'column';
      container.style.gap = '10px';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast-item toast-${type}`;
    toast.style.padding = '12px 20px';
    toast.style.borderRadius = '10px';
    toast.style.fontWeight = '600';
    toast.style.fontSize = '0.92rem';
    toast.style.boxShadow = '0 6px 20px rgba(0,0,0,0.15)';
    toast.style.display = 'flex';
    toast.style.alignItems = 'center';
    toast.style.gap = '10px';
    toast.style.transition = 'all 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(15px)';

    let icon = 'fa-circle-check';
    if (type === 'success') {
      toast.style.background = '#1b4332';
      toast.style.color = '#ffffff';
      toast.style.border = '1px solid #52b788';
      icon = 'fa-circle-check';
    } else if (type === 'info') {
      toast.style.background = '#1e3a8a';
      toast.style.color = '#ffffff';
      icon = 'fa-circle-info';
    } else {
      toast.style.background = '#991b1b';
      toast.style.color = '#ffffff';
      icon = 'fa-triangle-exclamation';
    }

    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateY(0)';
    });

    // Animate out & remove
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
});
