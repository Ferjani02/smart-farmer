import sqlite3

conn = sqlite3.connect('irrigation.db')
cursor = conn.cursor()

# Supprime les anciennes règles (optionnel)
cursor.execute('DELETE FROM age_rules')

rules = [
    (0, 2, 7),
    (3, 5, 20),
    (6, 10, 35),
    (11, 100, 50)
]

cursor.executemany('''
INSERT INTO age_rules (age_min, age_max, water_per_day)
VALUES (?, ?, ?)
''', rules)

conn.commit()
conn.close()
