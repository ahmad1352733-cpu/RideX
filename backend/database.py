import sqlite3

db = sqlite3.connect("ridex.db")

cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS captains(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT UNIQUE,
    car TEXT,
    plate TEXT,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS passengers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT UNIQUE,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS rides(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_phone TEXT,
    captain_phone TEXT,
    from_location TEXT,
    to_location TEXT,
    status TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

db.commit()
db.close()

print("RideX Database Created Successfully")
