import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect("seo_data.db")

# Hol die letzten 2 Monate
today = datetime.utcnow().date()
start = today.replace(day=1)
last_month = (start - timedelta(days=1)).replace(day=1)

# Alle Daten laden
df = pd.read_sql_query("SELECT * FROM gsc_data", conn, parse_dates=["date"])
conn.close()

# Gruppieren nach Keyword & Monat
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby(["month", "query"]).agg({
    "clicks": "sum",
    "impressions": "sum",
    "ctr": "mean",
    "position": "mean"
}).reset_index()

# Pivot: Aktueller Monat vs. Vormonat
pivot = monthly.pivot(index="query", columns="month")

# Daten berechnen
def safe_diff(current, previous):
    return current - previous if pd.notnull(current) and pd.notnull(previous) else None

kpi_data = []
for keyword in pivot.index:
    try:
        clicks_now = pivot["clicks"][start.to_period("M")][keyword]
        clicks_prev = pivot["clicks"][last_month.to_period("M")][keyword]
        impressions_now = pivot["impressions"][start.to_period("M")][keyword]
        impressions_prev = pivot["impressions"][last_month.to_period("M")][keyword]
        position_now = pivot["position"][start.to_period("M")][keyword]
        position_prev = pivot["position"][last_month.to_period("M")][keyword]

        delta_clicks = safe_diff(clicks_now, clicks_prev)
        delta_position = safe_diff(position_prev, position_now)  # niedriger = besser

        if delta_clicks and abs(delta_clicks) > 5:  # Filtere kleine Änderungen
            kpi_data.append({
                "Keyword": keyword,
                "Clicks Δ": int(delta_clicks),
                "Pos Δ": round(delta_position, 2),
                "CTR": f"{pivot['ctr'][start.to_period('M')][keyword]*100:.1f}%",
                "Impr→Click": f"{(clicks_now / impressions_now * 100):.2f}%" if impressions_now else "0.00%"
            })
    except Exception:
        continue

# Top-Veränderungen nach Klick-Gewinn
top_kpi = sorted(kpi_data, key=lambda x: -x["Clicks Δ"])[:10]

# Als HTML-Tabelle ausgeben
html_table = "<table><tr>" + "".join(f"<th>{k}</th>" for k in top_kpi[0].keys()) + "</tr>"
for row in top_kpi:
    html_table += "<tr>" + "".join(f"<td>{v}</td>" for v in row.values()) + "</tr>"
html_table += "</table>"

with open("templates/kpi_table.html", "w") as f:
    f.write(html_table)

print("KPIs erfolgreich extrahiert.")
