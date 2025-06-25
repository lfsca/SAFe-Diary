const select = document.getElementById('challenge-select');
const descriptions = document.querySelectorAll('.card-descricao');
const groups = document.querySelectorAll('[id^="group-"]');

select.addEventListener('change', () => {
  descriptions.forEach(d => d.classList.add('hide'));
  groups.forEach(g => g.classList.add('hide'));

  const selectedId = select.value;
  const desc = document.getElementById(`desc-${selectedId}`);
  const group = document.getElementById(`group-${selectedId}`);

  if (desc) desc.classList.remove('hide');
  if (group) group.classList.remove('hide');
});
