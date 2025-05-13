from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Lade Template
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report_template.html')

# Dummy-Daten
output = template.render(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Speichern als HTML (könnte auch PDF sein mit Erweiterung)
with open('report_output.html', 'w') as f:
    f.write(output)

print("Dummy SEO-Report erstellt.")