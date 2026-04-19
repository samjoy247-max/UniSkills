// =============================================
// UniSkills — Shared JavaScript v3
// =============================================

// Hamburger nav toggle
function toggleNav() {
  const nav = document.getElementById('navLinks');
  if (nav) nav.classList.toggle('open');
}

// Role tab switcher (index.html)
function switchTab(role) {
  const roles = ['seeker', 'provider', 'alumni'];
  roles.forEach(r => {
    const tab   = document.getElementById('tab-' + r);
    const panel = document.getElementById('panel-' + r);
    if (tab)   tab.classList.toggle('active', r === role);
    if (panel) panel.classList.toggle('active', r === role);
  });
  document.querySelectorAll('.role-choice-btn').forEach((btn, i) => {
    btn.classList.toggle('selected', roles[i] === role);
  });
}

// Toggle register/login
function toggleRegister(role) {
  const loginDiv    = document.getElementById(role + '-login');
  const registerDiv = document.getElementById(role + '-register');
  if (!loginDiv || !registerDiv) return;
  const showingLogin = loginDiv.style.display !== 'none';
  loginDiv.style.display    = showingLogin ? 'none'  : '';
  registerDiv.style.display = showingLogin ? ''      : 'none';
}

// Close mobile nav on link click
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.navbar-links a').forEach(link => {
    link.addEventListener('click', () => {
      const nav = document.getElementById('navLinks');
      if (nav) nav.classList.remove('open');
    });
  });
});