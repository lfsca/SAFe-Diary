document.addEventListener('DOMContentLoaded', function () {
  const hotspots = document.querySelectorAll('.hotspot');
  const modal = document.getElementById('modal');
  const modalTitle = document.getElementById('modal-title');
  const modalText = document.getElementById('modal-text');
  const modalClose = document.getElementById('modal-close');

  hotspots.forEach(hotspot => {
    hotspot.addEventListener('click', () => {
      modalTitle.textContent = hotspot.dataset.title;
      modalText.textContent = hotspot.dataset.content;
      modal.classList.remove('hidden');
    });
  });

  modalClose.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  window.addEventListener('click', e => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });
});
