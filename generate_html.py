import os

TEMPLATE_PATH = "templates/index_template.html"
OUTPUT_PATH = "index.html"
REPORT_DIR = "reports"

# Aktuelle PDF-Dateien im Report-Ordner sammeln
pdf_files = [f for f in os.listdir(REPORT_DIR) if f.endswith(".pdf")]
pdf_files.sort(key=lambda f: os.path.getmtime(os.path.join(REPORT_DIR, f)), reverse=True)
latest_pdf = pdf_files[0] if pdf_files else ""

# Downloadliste erstellen
download_links = "\n".join(
    f'<li><a href="{REPORT_DIR}/{f}" download>{f}</a></li>' for f in pdf_files
)

# Dino-Spiel (ausgelagert oder inline)
with open("templates/footer_game_snippet.html", "r", encoding="utf-8") as f:
    footer_game = f.read()

# Template einlesen
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

# Platzhalter ersetzen
html = template.replace("{{LATEST_PDF_PATH}}", f"{REPORT_DIR}/{latest_pdf}")
html = html.replace("{{DOWNLOAD_LINKS}}", download_links)
html = html.replace("{{FOOTER_GAME}}", footer_game)

# Datei schreiben
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ index.html erstellt mit {latest_pdf} als neuestem Bericht.")
