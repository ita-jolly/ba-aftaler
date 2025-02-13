import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')


def init():
    """Initialize the "aftaler" table if it doesn't exist."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS aftaler(
                    aftale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cpr TEXT,
                    nummerplade TEXT,
                    aftale_type TEXT,
                    start_dato DATE,
                    slut_dato DATE)
        ''')

        con.commit()

def create_aftale(cpr, nummerplade, aftale_type, start_dato, slut_dato):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('''
            INSERT INTO aftaler (cpr, nummerplade, aftale_type, start_dato, slut_dato)
            VALUES (?, ?, ?, ?, ?)''',
            (cpr, nummerplade, aftale_type, start_dato, slut_dato)
            )

        con.commit()

        cur.execute('SELECT * FROM aftaler')
        row = cur.fetchone()

        if row is None:
            return None

        return {'aftale_id': row[0],
                'cpr': row[1],
                'nummerplade': row[2],
                'aftale_type': row[3],
                'start_dato': row[4],
                'slut_dato': row[5]}

def get_aftaler():
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM aftaler')
        rows = cur.fetchall()

        all_aftaler = [{'aftale_id': row[0],
                        'cpr': row[1],
                        'nummerplade': row[2],
                        'aftale_type': row[3],
                        'start_dato': row[4],
                        'slut_dato': row[5]}
                        for row in rows]
        if len(all_aftaler) == 0:
            return None

        return all_aftaler
