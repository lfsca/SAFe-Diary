document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll('.cargo-box');

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('sidebar');
  const openBtn = document.querySelector('.sidebar-toggle');
  const closeBtn = document.getElementById('sidebarCloseBtn');

  // Evento: sidebar aberta -> esconder botão ">"
  sidebar.addEventListener('shown.bs.offcanvas', function () {
    openBtn.classList.add('d-none');
  });

  // Evento: sidebar fechada -> mostrar botão ">"
  sidebar.addEventListener('hidden.bs.offcanvas', function () {
    openBtn.classList.remove('d-none');
  });

  // Botão "<" para fechar a sidebar
  if (closeBtn && sidebar) {
    closeBtn.addEventListener('click', function () {
      const bsSidebar = bootstrap.Offcanvas.getInstance(sidebar);
      if (bsSidebar) {
        bsSidebar.hide();
      }
    });
  }

  console.log("Scripts carregados com sucesso!");
});

document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  form.addEventListener('submit', function () {
    const password = document.querySelector('input[name="password"]').value;
    const confirm = document.querySelector('input[name="confirm_password"]').value;
    if (password !== confirm) {
      alert("As senhas não coincidem.");
    }
  });
});
