const select = document.getElementById('challenge-select');
const descriptions = document.querySelectorAll('.card-descricao');
const groups = document.querySelectorAll('[id^="group-"]');
const registrarBtn = document.getElementById('btn-registrar');

select.addEventListener('change', () => {
  descriptions.forEach(d => d.classList.add('hide'));
  groups.forEach(g => g.classList.add('hide'));

  const selectedId = select.value;
  const desc = document.getElementById(`desc-${selectedId}`);
  const group = document.getElementById(`group-${selectedId}`);

  if (desc) desc.classList.remove('hide');
  if (group) group.classList.remove('hide');

  // Atualiza o botão "Registrar Ocorrência"
  if (registrarBtn) {
    registrarBtn.href = `/registrar_ocorrencia/?challenge_id=${selectedId}`;
    registrarBtn.classList.remove('disabled');
  }
});
