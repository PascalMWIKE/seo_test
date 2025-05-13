from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from weasyprint import HTML
import os

# Lade Template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report_template.html')

# Dummy-Daten
rendered = template.render(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Speichern als HTML (optional für Debugging)
with open('report_output.html', 'w') as f:
    f.write(rendered)

# Speichern als PDF im Unterordner "reports"
os.makedirs("reports", exist_ok=True)
pdf_filename = f'reports/seo_report_{datetime.now().strftime("%Y-%m-%d")}.pdf'
HTML(string=rendered).write_pdf(pdf_filename)

print(f"Report erstellt: {pdf_filename}")
