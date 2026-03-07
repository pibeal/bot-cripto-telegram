import sqlite3

conn = sqlite3.connect("crypto.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alertas(
chat_id INTEGER,
crypto TEXT,
precio REAL
)
""")

conn.commit()
