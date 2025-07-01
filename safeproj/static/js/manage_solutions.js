document.addEventListener('DOMContentLoaded', function () {
  const challengeSelect = document.getElementById('challenge-select');
  const statusSelect = document.getElementById('status-select');
  const form = document.getElementById('filter-form');

  // Desabilita o select de status se não houver challenge selecionado
  if (!challengeSelect.value) {
    statusSelect.disabled = true;
  }

  function maybeSubmit() {
    if (challengeSelect.value && statusSelect.value) {
      form.submit();
    }
  }

  if (challengeSelect) {
    challengeSelect.addEventListener('change', function () {
      // Ativa o campo de status ao selecionar um challenge
      if (challengeSelect.value) {
        statusSelect.disabled = false;
      } else {
        statusSelect.disabled = true;
      }

      maybeSubmit();
    });
  }

  if (statusSelect) {
    statusSelect.addEventListener('change', maybeSubmit);
  }

  const cards = document.querySelectorAll('.solution-card');
  const detailCard = document.getElementById('solution-detail');
  const descEl = document.getElementById('detail-description');
  const authorEl = document.getElementById('detail-author');
  const challengeEl = document.getElementById('detail-challenge');
  const idInput = document.getElementById('solution-id-input');
  const acceptBtn = detailCard ? detailCard.querySelector('button[value="accept"]') : null;
  const rejectBtn = detailCard ? detailCard.querySelector('button[value="reject"]') : null;
  const pendBtn = detailCard ? detailCard.querySelector('button[value="pend"]') : null;

  cards.forEach(card => {
    card.addEventListener('click', () => {
      const desc = card.getAttribute('data-description');
      const author = card.getAttribute('data-author');
      const challenge = card.getAttribute('data-challenge');
      const status = card.getAttribute('data-status');
      const id = card.getAttribute('data-id');

      descEl.textContent = desc;
      authorEl.textContent = 'By ' + author;
      challengeEl.textContent = challenge;
      idInput.value = id;

      if (status === 'Pending') {
        acceptBtn.classList.remove('d-none');
        rejectBtn.classList.remove('d-none');
        pendBtn.classList.add('d-none');
      } else {
        acceptBtn.classList.add('d-none');
        rejectBtn.classList.add('d-none');
        pendBtn.classList.remove('d-none');
      }

      detailCard.classList.remove('d-none');
    });
  });
});
