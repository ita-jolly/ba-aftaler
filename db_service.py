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
                    aftale_id INTEGER PRIMARY KEY,
                    cpr INTEGER,
                    nummerplade TEXT,
                    aftale_type TEXT,
                    start_dato DATE,
                    slut_dato DATE)
        ''')

        con.commit()

def create_aftale(aftale_id, cpr, nummerplade, aftale_type, start_dato, slut_dato):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            'INSERT INTO aftaler (aftale_id, cpr, nummerplade, aftale_type, start_dato, slut_dato) '
            'VALUES (?, ?, ?, ?, ?, ?)',
            (aftale_id, cpr, nummerplade, aftale_type, start_dato, slut_dato)
        )
        con.commit()

        cur.execute('SELECT * FROM aftaler WHERE aftale_id = ?', (aftale_id,))
        row = cur.fetchone()

        if row is None:
            return None
        return {'aftale_id': row[0], 'cpr': row[1], 'nummerplade': row[2], 
                'aftale_type': row[3], 'start_dato': row[4], 'slut_dato': row[5]}
