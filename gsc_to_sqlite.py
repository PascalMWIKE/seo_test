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
# Quelle und Typ einfügen
quelle = 'google_search_console'
typ = 'date'  # Beispiel, kann erweitert werden

data = [{'date': r['keys'][0], 'clicks': r.get('clicks', 0), 'impressions': r.get('impressions', 0), 'quelle': quelle, 'typ': typ} for r in rows]

conn = sqlite3.connect('seo_data.db')
cursor = conn.cursor()

# Tabelle mit zusammengesetztem Primärschlüssel (date + quelle + typ)
cursor.execute('''
CREATE TABLE IF NOT EXISTS gsc_data (
    date TEXT,
    quelle TEXT,
    typ TEXT,
    clicks INTEGER,
    impressions INTEGER,
    PRIMARY KEY (date, quelle, typ)
)
''')

# Upsert für jede Zeile mit zusammengesetztem Schlüssel
for row in data:
    cursor.execute('''
    INSERT INTO gsc_data (date, quelle, typ, clicks, impressions) VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(date, quelle, typ) DO UPDATE SET
      clicks=excluded.clicks,
      impressions=excluded.impressions
    ''', (row['date'], row['quelle'], row['typ'], row['clicks'], row['impressions']))

conn.commit()
conn.close()

print(f"{len(data)} Zeilen erfolgreich upserted.")
