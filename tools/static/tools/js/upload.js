/* upload.js — drag & drop upload zone, file list, validation, and an
   AJAX submit that shows a real upload-progress bar before swapping in
   the server-rendered result panel (no full page reload). */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.dropzone').forEach(function (zone) {
    var input = zone.querySelector('input[type="file"]');
    var listEl = zone.parentElement.querySelector('.file-list');
    if (!input) return;

    function renderList() {
      if (!listEl) return;
      listEl.innerHTML = '';
      Array.from(input.files).forEach(function (file, idx) {
        var li = document.createElement('li');
        var sizeKb = (file.size / 1024).toFixed(1);
        li.innerHTML = '<span>' + file.name + ' <span class="muted">(' + sizeKb + ' KB)</span></span>';
        listEl.appendChild(li);
      });
    }

    zone.addEventListener('click', function () { input.click(); });
    zone.addEventListener('dragover', function (e) { e.preventDefault(); zone.classList.add('dragover'); });
    zone.addEventListener('dragleave', function () { zone.classList.remove('dragover'); });
    zone.addEventListener('drop', function (e) {
      e.preventDefault();
      zone.classList.remove('dragover');
      if (e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        renderList();
      }
    });
    input.addEventListener('change', renderList);
  });

  document.querySelectorAll('form.tool-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      var progress = form.querySelector('#upload-progress');
      var bar = progress ? progress.querySelector('.bar') : null;
      var submitBtn = form.querySelector('button[type="submit"]');

      if (!progress) return; // no progress UI on this form (e.g. client-side tools) — let it submit normally

      e.preventDefault();
      var xhr = new XMLHttpRequest();
      xhr.open(form.method || 'POST', form.action || window.location.href, true);

      xhr.upload.addEventListener('progress', function (evt) {
        if (evt.lengthComputable && bar) {
          var pct = Math.round((evt.loaded / evt.total) * 100);
          bar.style.width = pct + '%';
        }
      });

      xhr.addEventListener('loadstart', function () {
        progress.style.display = 'block';
        if (submitBtn) { submitBtn.disabled = true; submitBtn.querySelector('.btn-label').textContent = 'Processing…'; }
      });

      xhr.addEventListener('load', function () {
        var parser = new DOMParser();
        var doc = parser.parseFromString(xhr.responseText, 'text/html');
        var newMount = doc.getElementById('tool-result-container');
        var oldMount = document.getElementById('tool-result-container');
        if (newMount && oldMount) {
          oldMount.innerHTML = newMount.innerHTML;
          oldMount.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
          // Fallback: full reload if structure wasn't found
          window.location.reload();
        }
        if (submitBtn) { submitBtn.disabled = false; submitBtn.querySelector('.btn-label').textContent = submitBtn.getAttribute('data-label') || 'Run'; }
        progress.style.display = 'none';
        if (bar) bar.style.width = '0%';
      });

      xhr.addEventListener('error', function () {
        if (submitBtn) { submitBtn.disabled = false; }
        progress.style.display = 'none';
        alert('Something went wrong submitting the form. Please try again.');
      });

      xhr.send(new FormData(form));
    });
  });
});
