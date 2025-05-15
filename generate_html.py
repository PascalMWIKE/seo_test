import os
import re
from datetime import datetime

# Verzeichnis mit PDF-Berichten
report_dir = "reports"
pdf_files = [
    f for f in os.listdir(report_dir)
    if f.endswith(".pdf")
]

# Pfade + Änderungszeiten
full_paths = [
    (f, os.path.getmtime(os.path.join(report_dir, f)))
    for f in pdf_files
]

# Aktuellsten Bericht identifizieren
if full_paths:
    latest_file, latest_mtime = max(full_paths, key=lambda x: x[1])
    latest_path = os.path.join(report_dir, latest_file)
    # Datum aus Dateinamen extrahieren (Format: seo_report_YYYY-MM-DD.pdf)
    match = re.search(r"(\d{4}-\d{2}-\d{2})", latest_file)
    if match:
        report_date = datetime.strptime(match.group(1), "%Y-%m-%d").strftime("%d.%m.%Y")
    else:
        report_date = datetime.fromtimestamp(latest_mtime).strftime("%d.%m.%Y")
else:
    latest_file = None
    report_date = None

# HTML-Bestandteile
html_head = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>SEO Reports</title>
    <style>
        body {
            font-family: sans-serif;
            margin: 2rem;
            background-color: #f4f4f4;
            color: #333;
        }
        h1 {
            font-size: 2rem;
        }
        .pdf-viewer {
            width: 100%;
            height: 90vh;
            border: none;
            margin-bottom: 2rem;
        }
        .report-list a {
            display: block;
            margin: 0.5rem 0;
            text-decoration: none;
            color: #0066cc;
        }
        .footer {
            margin-top: 4rem;
            font-size: 0.8rem;
            color: #aaa;
            text-align: center;
            position: relative;
        }
        .crocodile {
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 50px;
            background: url('https://upload.wikimedia.org/wikipedia/commons/3/36/Google_Dino_Game_Offline.png') no-repeat center center;
            background-size: contain;
            opacity: 0.3;
        }
        .flying-letters {
            position: absolute;
            bottom: 20px;
            left: 0;
            width: 100%;
            overflow: hidden;
            pointer-events: none;
        }
        .flying-letters span {
            position: absolute;
            animation: fly 5s linear infinite;
            color: #000;
            font-weight: bold;
            font-size: 1.2rem;
        }
        @keyframes fly {
            0% { bottom: 0; left: 100%; transform: rotate(0deg); }
            100% { bottom: 100%; left: 0%; transform: rotate(720deg); }
        }
    </style>
</head>
<body>
    <h1>Aktueller SEO-Bericht</h1>
"""

html_footer = """
    <div class="footer">
        © 2025 SEO Dashboard
        <div class="crocodile"></div>
        <div class="flying-letters">
""" + "\n".join(
    f'<span style="left: {i * 5}%; animation-delay: {i * 0.7}s;">P</span>'
    for i in range(20)
) + """
        </div>
    </div>
</body>
</html>
"""

# Embed für aktuellsten Bericht + Datum
embed_html = ""
if latest_file:
    embed_html = f"""
    <p><strong>Datum des Berichts:</strong> {report_date}</p>
    <embed src="reports/{latest_file}" type="application/pdf" class="pdf-viewer">
    """
else:
    embed_html = "<p><em>Kein Bericht gefunden.</em></p>"

# Alle Download-Links
report_links = sorted(pdf_files, reverse=True)
links_html = "<h2>Alle SEO-Berichte (Download)</h2><div class='report-list'>\n"
for f in report_links:
    links_html += f'<a href="reports/{f}" download>{f}</a>\n'
links_html += "</div>"

# Schreiben
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_head + embed_html + links_html + html_footer)

print("index.html erfolgreich erstellt – neuester Bericht eingebunden:", latest_file)
