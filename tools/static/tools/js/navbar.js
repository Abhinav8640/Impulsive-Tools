/* navbar.js — mobile menu + dropdown behaviour */
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.getElementById('nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('mobile-open');
    });
  }

  var dropdown = document.querySelector('.nav-dropdown');
  if (dropdown && window.matchMedia('(max-width: 880px)').matches) {
    var trigger = dropdown.querySelector('.nav-dropdown-trigger');
    if (trigger) {
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        dropdown.classList.toggle('mobile-expanded');
      });
    }
  }
});
