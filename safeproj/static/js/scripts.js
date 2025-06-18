document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll('.cargo-box');

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
    });
  });
});
