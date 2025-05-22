import os
from datetime import datetime

TEMPLATE_PATH = "templates/index_template.html"
OUTPUT_PATH = "index.html"
REPORTS_FOLDER = "reports"
FOOTER_GAME_PATH = "templates/footer_game.html"

def load_template(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def list_reports(folder):
    pdf_files = sorted(
        [f for f in os.listdir(folder) if f.endswith(".pdf")],
        reverse=True
    )
    links = ""
    for pdf in pdf_files:
        date_label = datetime.strptime(pdf.split("_")[-1].replace(".pdf", ""), "%Y-%m-%d").strftime("%d.%m.%Y")
        links += f'<li><a href="{folder}/{pdf}" download>{date_label}</a></li>\n'
    return links, f"{folder}/{pdf_files[0]}" if pdf_files else ""

def main():
    # Lade das Haupttemplate
    template = load_template(TEMPLATE_PATH)

    # Lade das Footer-Spiel
    footer_game = load_template(FOOTER_GAME_PATH) if os.path.exists(FOOTER_GAME_PATH) else ""

    # Berichte einlesen
    download_links, latest_pdf = list_reports(REPORTS_FOLDER)

    # Ersetze Platzhalter
    html_output = template.replace("{{LATEST_PDF_PATH}}", latest_pdf)
    html_output = html_output.replace("{{DOWNLOAD_LINKS}}", download_links)
    html_output = html_output.replace("{{FOOTER_GAME}}", footer_game)

    # Speichere finale index.html
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(html_output)

    print("✅ index.html wurde erfolgreich generiert.")

if __name__ == "__main__":
    main()
