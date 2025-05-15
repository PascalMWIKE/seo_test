import os
from datetime import datetime

REPORT_DIR = "reports"
TEMPLATE_PATH = "templates/index_template.html"
OUTPUT_PATH = "index.html"

# Alle PDFs im reports/-Verzeichnis sammeln
pdf_files = [f for f in os.listdir(REPORT_DIR) if f.endswith(".pdf")]

# Neuester Report nach Änderungsdatum
latest_pdf = max(pdf_files, key=lambda f: os.path.getmtime(os.path.join(REPORT_DIR, f)))

# HTML-Downloadliste
download_links = "\n".join(
    f'<li><a href="{REPORT_DIR}/{f}" download>{f}</a></li>' for f in sorted(pdf_files, reverse=True)
)

# HTML-Template einlesen
with open(TEMPLATE_PATH, "r") as f:
    template = f.read()

# Platzhalter ersetzen
html = template.replace("{{LATEST_PDF}}", f"{REPORT_DIR}/{latest_pdf}")
html = html.replace("{{PDF_LIST}}", download_links)

# Ausgabe speichern
with open(OUTPUT_PATH, "w") as f:
    f.write(html)

print(f"index.html erfolgreich erstellt. Neuester Bericht: {latest_pdf}")
