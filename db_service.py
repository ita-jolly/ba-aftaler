import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_PATH')


def init():
    """Initialize the 'aftaler' table if it doesn't exist."""
    try:
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
        print("Table 'aftaler' initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing the table: {e}")


def create_aftale(aftale_id, cpr, nummerplade, aftale_type, start_dato, slut_dato):
    """Insert a new aftale into the database."""
    try:
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
                print("Failed to retrieve the aftale after insertion.")
                return None

            print("Aftale created successfully.")
            return {
                'aftale_id': row[0],
                'cpr': row[1],
                'nummerplade': row[2],
                'aftale_type': row[3],
                'start_dato': row[4],
                'slut_dato': row[5]
            }

    except sqlite3.IntegrityError:
        print(f"Error: A record with aftale_id {aftale_id} already exists.")
        return None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
