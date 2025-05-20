import os
from datetime import datetime

REPORT_DIR = "reports"
TEMPLATE_PATH = "templates/report_template.html"
OUTPUT_PATH = "index.html"

# Alle PDFs im reports/-Verzeichnis sammeln
pdf_files = [f for f in os.listdir(REPORT_DIR) if f.endswith(".pdf")]

# Neuester Report nach Änderungsdatum
latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(REPORT_DIR, f)))

# HTML-Downloadliste
download_links = "\n".join(
    f'<li><a href="{REPORT_DIR}/{f}" download>{f}</a></li>' for f in sorted(pdf_files, reverse=True)
)

# Dino-Spiel HTML + Script
footer_game = '''
<div style="text-align: center; margin-top: 50px;">
  <h3>Schnapp dir alle PP!</h3>
  <canvas id="dinoCanvas" width="600" height="150" style="border:1px solid #000"></canvas>
  <div>Punkte: <span id="score">0</span></div>
  <div id="gameOver" style="color:red; font-weight:bold; display:none; cursor:pointer;">Game Over! Klick zum Neustart.</div>
</div>
<script>
const canvas = document.getElementById('dinoCanvas');
const ctx = canvas.getContext('2d');
let dino = { x: 50, y: 100, width: 20, height: 30, vy: 0, gravity: 1, jumping: false };
let letters = [];
let score = 0;
let gameOver = false;
let mouthOpen = false;

function drawDino() {
  ctx.fillStyle = 'green';
  ctx.fillRect(dino.x, dino.y, dino.width, dino.height); // Körper
  ctx.fillRect(dino.x, dino.y + dino.height, 5, 5); // Bein links
  ctx.fillRect(dino.x + 15, dino.y + dino.height, 5, 5); // Bein rechts
  ctx.fillRect(dino.x - 5, dino.y + 10, 5, 5); // Arm links
  ctx.fillRect(dino.x + dino.width, dino.y + 10, 5, 5); // Arm rechts
  ctx.fillRect(dino.x - 10, dino.y + 15, 10, 5); // Langer Schwanz
  ctx.fillStyle = 'black';
  ctx.beginPath();
  ctx.arc(dino.x + dino.width - 5, dino.y + 5, 2, 0, Math.PI * 2); // Auge
  ctx.fill();
  if (mouthOpen) {
    ctx.fillStyle = 'red';
    ctx.fillRect(dino.x + dino.width, dino.y + 10, 10, 5); // Geöffneter Schnabel
  } else {
    ctx.fillStyle = 'red';
    ctx.fillRect(dino.x + dino.width, dino.y + 12, 8, 2); // Geschlossener Schnabel
  }
}

function drawLetters() {
  ctx.fillStyle = 'black';
  letters.forEach(l => {
    ctx.font = '20px monospace';
    ctx.fillText(l.char, l.x, l.y);
  });
}

function update() {
  if (gameOver) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (dino.jumping) {
    dino.vy += dino.gravity;
    dino.y += dino.vy;
    if (dino.y >= 100) {
      dino.y = 100;
      dino.vy = 0;
      dino.jumping = false;
    }
  }

  drawDino();
  drawLetters();

  letters.forEach(l => l.x -= 2);
  letters = letters.filter(l => l.x > 0);

  for (let i = 0; i < letters.length - 1; i++) {
    const l1 = letters[i];
    const l2 = letters[i + 1];
    if (
      l1.char === 'P' &&
      l2.char === 'P' &&
      Math.abs(l1.x - l2.x) < 20 &&
      Math.abs(l1.y - l2.y) < 10 &&
      l1.x < dino.x + dino.width &&
      l1.x + 10 > dino.x &&
      l1.y > dino.y &&
      l1.y < dino.y + dino.height
    ) {
      mouthOpen = true;
      setTimeout(() => mouthOpen = false, 200);
      score++;
      document.getElementById('score').textContent = score;
      letters.splice(i, 2);
      break;
    } else if (
      l1.x < dino.x + dino.width &&
      l1.x + 10 > dino.x &&
      l1.y > dino.y &&
      l1.y < dino.y + dino.height
    ) {
      gameOver = true;
      document.getElementById('gameOver').style.display = 'block';
    }
  }
}

function spawnLetter() {
  const options = ['PP', 'A', 'B', 'C', 'D', 'E', 'F'];
  const choice = options[Math.floor(Math.random() * options.length)];
  const y = 60 + Math.floor(Math.random() * 60);
  for (let i = 0; i < choice.length; i++) {
    letters.push({ x: canvas.width + i * 12, y: y, char: choice[i] });
  }
}

canvas.addEventListener('click', () => {
  if (gameOver) {
    letters = [];
    score = 0;
    dino.y = 100;
    dino.vy = 0;
    dino.jumping = false;
    gameOver = false;
    mouthOpen = false;
    document.getElementById('score').textContent = score;
    document.getElementById('gameOver').style.display = 'none';
  } else if (!dino.jumping) {
    dino.vy = -12;
    dino.jumping = true;
  }
});

setInterval(update, 30);
setInterval(spawnLetter, 1000);
</script>
'''

# HTML-Template einlesen
with open(TEMPLATE_PATH, "r") as f:
    template = f.read()

# Platzhalter ersetzen
html = template.replace("{{LATEST_PDF}}", f"{REPORT_DIR}/{latest_pdf}")
html = html.replace("{{PDF_LIST}}", download_links)
html = html.replace("{{FOOTER_GAME}}", footer_game)

# Ausgabe speichern
with open(OUTPUT_PATH, "w") as f:
    f.write(html)

print(f"index.html erfolgreich erstellt. Neuester Bericht: {latest_pdf}")
