document.addEventListener('DOMContentLoaded', function () {
  const typeSelect = document.getElementById('type-select');
  const challengeSelect = document.getElementById('challenge-select');
  const statusSelect = document.getElementById('status-select');
  const form = document.getElementById('filter-form');

  if (!typeSelect.value) {
    challengeSelect.disabled = true;
    statusSelect.disabled = true;
  } else if (!challengeSelect.value) {
    statusSelect.disabled = true;
  } else {
    statusSelect.disabled = false;
  }

  function maybeSubmit() {
    if (typeSelect.value && challengeSelect.value && statusSelect.value) {
      typeSelect.removeAttribute('disabled');
      challengeSelect.removeAttribute('disabled');
      statusSelect.removeAttribute('disabled');
      form.submit();
    }
  }

  if (typeSelect) {
    typeSelect.addEventListener('change', function () {
      if (typeSelect.value) {
        challengeSelect.disabled = false;
        if (challengeSelect.value) {
          statusSelect.disabled = false;
        }
      } else {
        challengeSelect.disabled = true;
        statusSelect.disabled = true;
      }
      maybeSubmit();
    });
  }

  if (challengeSelect) {
    challengeSelect.addEventListener('change', function () {
      if (typeSelect.value && challengeSelect.value) {
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

  const cards = document.querySelectorAll('.manage-card');
  const detailCard = document.getElementById('item-detail');
  const descEl = document.getElementById('detail-description');
  const authorEl = document.getElementById('detail-author');
  const challengeEl = document.getElementById('detail-challenge');
  const idInput = document.getElementById('item-id-input');
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
        acceptBtn?.classList.remove('hide');
        rejectBtn?.classList.remove('hide');
        pendBtn?.classList.add('hide');
      } else {
        acceptBtn?.classList.add('hide');
        rejectBtn?.classList.add('hide');
        pendBtn?.classList.remove('hide');
      }

      detailCard.classList.remove('hide');
    });
  });
});
