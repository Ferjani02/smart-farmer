import sqlite3

conn = sqlite3.connect('irrigation.db')
cursor = conn.cursor()

# Table des règles d'irrigation météo
cursor.execute('''
CREATE TABLE IF NOT EXISTS irrigation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature_min REAL,
    temperature_max REAL,
    humidite_min REAL,
    humidite_max REAL,
    duree_irrigation INTEGER,  -- en minutes
    quantite_irrigation REAL   -- en litres
)
''')

# Table des règles d'âge
cursor.execute('''
CREATE TABLE IF NOT EXISTS age_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age_min INTEGER,
    age_max INTEGER,
    water_per_day REAL         -- en litres par jour
)
''')

conn.commit()
conn.close()
