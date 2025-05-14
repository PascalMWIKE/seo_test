import os
import json
import sqlite3
import datetime
import pandas as pd

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Verwende die Datei direkt
creds = service_account.Credentials.from_service_account_file("creds.json")

# --- Search Console API vorbereiten
service = build('searchconsole', 'v1', credentials=creds)
site_url = 'https://service.wirtschaft.nrw/'  # 🔁 Anpassen!

# --- Zeitraum: aktueller Monat
end_date = datetime.date.today()
start_date = end_date.replace(day=1)

request = {
    'startDate': str(start_date),
    'endDate': str(end_date),
    'dimensions': ['date'],
    'rowLimit': 1000
}

response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()

# --- In DataFrame umwandeln
rows = response.get('rows', [])
data = [{'date': r['keys'][0], 'clicks': r.get('clicks', 0), 'impressions': r.get('impressions', 0)} for r in rows]
df = pd.DataFrame(data)

# --- SQLite DB speichern
conn = sqlite3.connect('seo_data.db')
df.to_sql('gsc_data', conn, if_exists='replace', index=False)
conn.close()

print(f"{len(df)} Zeilen erfolgreich gespeichert.")
