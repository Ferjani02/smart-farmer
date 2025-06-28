import sqlite3

conn = sqlite3.connect('irrigation.db')
cursor = conn.cursor()

# Supprime les anciennes règles (optionnel)
cursor.execute('DELETE FROM irrigation_rules')

rules = [
    (20, 25, 40, 60, 30, 8.0),
    (25, 30, 30, 50, 40, 10.5),
    (30, 35, 20, 40, 50, 13.0),
    (15, 20, 50, 70, 20, 6.0),
    (10, 15, 60, 80, 15, 5.0)
]

cursor.executemany('''
INSERT INTO irrigation_rules (temperature_min, temperature_max, humidite_min, humidite_max, duree_irrigation, quantite_irrigation)
VALUES (?, ?, ?, ?, ?, ?)
''', rules)

conn.commit()
conn.close()
