import sqlite3

try:
    conn = sqlite3.connect("seo_data.db")
    cursor = conn.cursor()

    print("🔍 Tabellen in der DB:")
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for table in tables:
        print(f"📄 Tabelle: {table[0]}")
        rows = cursor.execute(f"SELECT * FROM {table[0]} LIMIT 10;").fetchall()
        for row in rows:
            print(f"➡️  {row}")
    
    conn.close()
except Exception as e:
    print("❌ Fehler beim Auslesen der DB:", e)
