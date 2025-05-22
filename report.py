from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import datetime

# Beispieldaten
data = {
    'report_date': datetime.date.today().strftime("%d.%m.%Y"),
    'visitors': 1345,
    'keywords': 67,
    'clicks': 456,
    'impressions': 12000
}

# Lade Template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report_template.html')

# Lese CSS und bette es inline ein
with open('css/report_style.css') as css_file:
    css_content = f"<style>{css_file.read()}</style>"

# HTML generieren
html_content = template.render(**data)
html_with_style = html_content.replace("</head>", f"{css_content}</head>")

# PDF erstellen
HTML(string=html_with_style, base_url='.').write_pdf('reports/seo_report.pdf')
