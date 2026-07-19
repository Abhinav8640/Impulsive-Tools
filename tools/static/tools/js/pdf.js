/* pdf.js — small UX helpers specific to the PDF tools category */
document.addEventListener('DOMContentLoaded', function () {
  // Rotate PDF: live-rotate a preview icon as the angle select changes
  var angleSelect = document.querySelector('[data-rotate-angle]');
  var previewIcon = document.querySelector('[data-rotate-preview]');
  if (angleSelect && previewIcon) {
    var applyAngle = function () {
      previewIcon.style.transform = 'rotate(' + angleSelect.value + 'deg)';
    };
    angleSelect.addEventListener('change', applyAngle);
    applyAngle();
  }

  // Split PDF: keep "end page" >= "start page"
  var startPage = document.querySelector('[data-split-start]');
  var endPage = document.querySelector('[data-split-end]');
  if (startPage && endPage) {
    startPage.addEventListener('change', function () {
      if (endPage.value && Number(endPage.value) < Number(startPage.value)) {
        endPage.value = startPage.value;
      }
    });
  }
});
