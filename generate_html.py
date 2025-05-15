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
  <canvas id="dinoCanvas" width="600" height="150" style="border:1px solid #000"></canvas>
  <div>Punkte: <span id="score">0</span></div>
</div>
<script>
const canvas = document.getElementById('dinoCanvas');
const ctx = canvas.getContext('2d');
let dino = { x: 50, y: 100, width: 30, height: 30 };
let letters = [];
let score = 0;

function drawDino() {
  ctx.fillStyle = 'black';
  ctx.fillRect(dino.x, dino.y, dino.width, dino.height);
  ctx.fillStyle = 'white';
  ctx.fillRect(dino.x + 5, dino.y + 5, 20, 10); // Augen als Stilmittel
}

function drawLetters() {
  ctx.fillStyle = 'black';
  letters.forEach(l => {
    ctx.font = '20px monospace';
    ctx.fillText(l.char, l.x, l.y);
  });
}

function update() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawDino();
  drawLetters();

  letters.forEach(l => l.x -= 2);
  letters = letters.filter(l => l.x > 0);
}

function spawnLetter() {
  const char = Math.random() < 0.5 ? 'P' : String.fromCharCode(65 + Math.floor(Math.random() * 26));
  letters.push({ x: canvas.width, y: 110, char });
}

canvas.addEventListener('click', () => {
  letters.forEach(l => {
    if (l.x < dino.x + dino.width && l.x + 10 > dino.x && l.char === 'P') {
      score++;
      document.getElementById('score').textContent = score;
    }
  });
  letters = letters.filter(l => l.x >= dino.x + dino.width || l.char !== 'P');
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
