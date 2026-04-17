// ── API Helper ──────────────────────────────────────────
async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    credentials: 'include',
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw { status: res.status, detail: data.detail || 'Something went wrong' };
  return data;
}

// ── Auth State ──────────────────────────────────────────
let currentUser = null;

async function loadUser() {
  try {
    currentUser = await api('/api/auth/me');
  } catch {
    currentUser = null;
  }
  renderNav();
  return currentUser;
}

function renderNav() {
  const navUser = document.getElementById('nav-user');
  const navAuth = document.getElementById('nav-auth');
  const navCartWrap = document.getElementById('nav-cart-wrap');

  if (currentUser) {
    if (navUser) {
      navUser.innerHTML = `
        <span>Hi, <strong>${currentUser.name.split(' ')[0]}</strong></span>
        ${currentUser.role === 'admin' ? `<a href="/admin" class="btn btn-outline btn-sm">Admin</a>` : ''}
        <button class="btn-logout" onclick="logout()">Logout</button>
      `;
      navUser.style.display = 'flex';
    }
    if (navAuth) navAuth.style.display = 'none';
    if (navCartWrap) navCartWrap.style.display = 'flex';
    updateCartBadge();
  } else {
    if (navUser) navUser.style.display = 'none';
    if (navAuth) navAuth.style.display = 'flex';
    if (navCartWrap) navCartWrap.style.display = 'none';
  }
}

async function logout() {
  await api('/api/auth/logout', { method: 'POST' });
  currentUser = null;
  window.location.href = '/';
}

async function updateCartBadge() {
  try {
    const cart = await api('/api/cart/');
    const badge = document.getElementById('cart-badge');
    if (badge) {
      const count = cart.items.reduce((sum, i) => sum + i.quantity, 0);
      badge.textContent = count;
      badge.style.display = count > 0 ? 'flex' : 'none';
    }
  } catch {}
}

// ── Toast ──────────────────────────────────────────────
function showToast(msg, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✓', error: '✕', info: 'ℹ' };
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.innerHTML = `<span>${icons[type] || '✓'}</span>${msg}`;
  container.appendChild(t);
  setTimeout(() => {
    t.classList.add('toast-out');
    setTimeout(() => t.remove(), 300);
  }, 3000);
}

// ── Format price ───────────────────────────────────────
function fmt(n) { return '$' + Number(n).toFixed(2); }

// ── Format date ────────────────────────────────────────
function fmtDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

// ── Active nav link ────────────────────────────────────
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === path);
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadUser();
  setActiveNav();
});
