/* search.js — homepage/navbar search bar behaviour */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form[data-search-form]').forEach(function (form) {
    var input = form.querySelector('input[type="search"], input[name="q"]');
    if (!input) return;
    // Keyboard shortcut: "/" focuses the search box
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== input && !/input|textarea/i.test(document.activeElement.tagName)) {
        e.preventDefault();
        input.focus();
      }
    });
  });
});
