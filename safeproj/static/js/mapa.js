const canvas = document.getElementById("safeCanvas");
const ctx = canvas.getContext("2d");
const image = new Image();
image.src = "/static/img/safe2.png";

// [x, y, width, height, title, content]
const areas = [
  [10, 20, 120, 60, "Business Owner", "Responsável por definir a direção do negócio e a visão estratégica para direcionar as estratégias do trem. Responsável pelo patrocínio e engajamento estratégico."],
  [250, 20, 120, 60, "Product Manager", "Responsável por definir a direção do negócio e a visão estratégica para direcionar as estratégias do trem. Responsável pelo patrocínio e engajamento estratégico."],
  [380, 20, 120, 60, "Solution Architect", "Responsável pela visão técnica e arquitetural do trem."],
  [510, 20, 120, 60, "Release Train Engineer", "Atua como líder e “coach” dos times, responsável por facilitar os processos e assegurar a integração entre os times ágeis."],

  [10, 250, 120, 60, "Scrum Master", "Responsável por garantir a metodologia ágil dentro da equipe e solucionar qualquer impedimento encontrado pela equipe."],
  [150, 250, 120, 60, "Product Owner", "Responsável por definir a direção do negócio e a visão estratégica para direcionar as estratégias do trem. Responsável pelo patrocínio e engajamento estratégico."],
  [10, 320, 260, 30, "Agile Team", "Prioriza funcionalidades no nível de ART."],


  [310, 250, 120, 60, "Scrum Master", "Fornece direção técnica."],
  [450, 250, 120, 60, "Product Owner", "Fornece direção técnica."],
  [310, 320, 260, 30, "Agile Team", "Prioriza funcionalidades no nível de ART."],

  [610, 250, 120, 60, "Scrum Master", "Fornece direção técnica."],
  [750, 250, 120, 60, "Product Owner", "Fornece direção técnica."],
  [610, 320, 260, 30, "Agile Team", "Prioriza funcionalidades no nível de ART."],

  [10, 120, 100, 60, "PI Plannning", "Fornece direção técnica."],
  [540, 120, 100, 60, "PI Plannning", "Fornece direção técnica."],
  [1070, 120, 100, 60, "PI Plannning", "Fornece direção técnica."],
];  

image.onload = () => {
  ctx.drawImage(image, 0, 0);
  // drawHotspots();
};

function drawHotspots() {
  ctx.fillStyle = "rgba(0, 123, 255, 0.3)"; // azul claro
  ctx.strokeStyle = "rgba(0, 123, 255, 0.8)";
  ctx.lineWidth = 2;

  for (let area of areas) {
    const [x, y, w, h] = area;
    ctx.fillRect(x, y, w, h);
    ctx.strokeRect(x, y, w, h);
  }
}

canvas.addEventListener("click", function (e) {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  for (let area of areas) {
    const [ax, ay, aw, ah, title, content] = area;
    if (x >= ax && x <= ax + aw && y >= ay && y <= ay + ah) {
      showModal(title, content);
      break;
    }
  }
});

function showModal(title, text) {
  document.getElementById("modalTitle").textContent = title;
  document.getElementById("modalText").textContent = text;
  document.getElementById("infoModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("infoModal").style.display = "none";
}

// Fecha ao clicar no fundo escuro do modal
document.getElementById("infoModal").addEventListener("click", function (e) {
  const modalContent = document.querySelector(".modal-content");
  if (!modalContent.contains(e.target)) {
    closeModal();
  }
});