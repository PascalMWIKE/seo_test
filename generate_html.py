import os
from datetime import datetime

# Verzeichnis der Reports
reports_dir = 'reports'

# HTML-Datei für die Übersichtsseite
html_filename = 'index.html'

# HTML-Header
html_content = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Reports Übersicht</title>
    <style>
        body { font-family: monospace; background-color: #1e1e1e; color: #e0e0e0; padding: 20px; }
        h1 { text-align: center; color: #00ff99; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #2e2e2e; margin: 10px 0; padding: 10px; border-radius: 8px; }
        li a { text-decoration: none; color: #00ccff; font-weight: bold; }
        li:hover { background-color: #3e3e3e; }
        .footer { text-align: center; font-size: 12px; color: #888; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>SEO Reports Übersicht</h1>
    <p>Hier findest du automatisch generierte SEO-Reports zum Herunterladen.</p>
    <ul>
"""

# Loop durch das Verzeichnis und finde alle PDF-Berichte
for filename in sorted(os.listdir(reports_dir), reverse=True):
    if filename.endswith(".pdf"):
        report_date = filename.replace("seo_report_", "").replace(".pdf", "")
        html_content += f'<li><a href="{reports_dir}/{filename}" download>SEO Report vom {report_date} (Download)</a></li>\n'

# HTML-Footer
html_content += """
    </ul>
    <div class="footer">
        <p>Automatisch generiert am {}</p>
    </div>
</body>
</html>
""".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# HTML-Datei speichern
with open(html_filename, 'w') as file:
    file.write(html_content)

print("HTML-Übersichtsseite erfolgreich generiert!")
