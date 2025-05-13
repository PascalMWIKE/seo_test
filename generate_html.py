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
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; padding: 20px; }
        h1 { text-align: center; color: #4CAF50; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #fff; margin: 10px 0; padding: 10px; border-radius: 5px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        li a { text-decoration: none; color: #2196F3; font-weight: bold; }
        li:hover { background-color: #e1f5fe; }
        .footer { text-align: center; font-size: 12px; color: #aaa; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>SEO Reports Übersicht</h1>
    <p>Automatisch generierte SEO-Berichte. Einfach auf einen Bericht klicken, um ihn herunterzuladen.</p>
    <ul>
"""

# Loop durch das Verzeichnis und finde alle PDF-Berichte
for filename in os.listdir(reports_dir):
    if filename.endswith(".pdf"):
        report_date = filename.replace("seo_report_", "").replace(".pdf", "")
        html_content += f'<li><a href="https://[DEIN-GITHUB-NAME].github.io/[DEIN-REPO]/{reports_dir}/{filename}">SEO Report vom {report_date}</a></li>\n'

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
