const select = document.getElementById('challenge-select');
const descriptions = document.querySelectorAll('.card-descricao');
const groups = document.querySelectorAll('[id^="group-"]');
const registrarBtn = document.getElementById('btn-registrar');
const registrarContainer = document.getElementById('registrar-container');

select.addEventListener('change', () => {
  descriptions.forEach(d => d.classList.add('hide'));
  groups.forEach(g => g.classList.add('hide'));

  const selectedId = select.value;
  const desc = document.getElementById(`desc-${selectedId}`);
  const group = document.getElementById(`group-${selectedId}`);

  if (desc) desc.classList.remove('hide');
  if (group) group.classList.remove('hide');

  // Exibir botão com URL atualizada
  if (selectedId) {
    registrarContainer.classList.remove('d-none');
    registrarBtn.href = `/registrar_ocorrencia/?challenge_id=${selectedId}`;
  } else {
    registrarContainer.classList.add('d-none');
    registrarBtn.href = '#';
  }
});
