import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()


def migrate(database):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        ssl_ca=os.getenv("DB_SSL_CA"),
        ssl_verify_cert=True,
        use_pure=True,
        connect_timeout=10,
        database=database,
    )
    cur = conn.cursor()
    cur.execute("SHOW COLUMNS FROM orders LIKE 'daily_number'")
    if not cur.fetchone():
        cur.execute("ALTER TABLE orders ADD COLUMN daily_number INT NOT NULL DEFAULT 1")
        conn.commit()
        print(f"{database}: daily_number column added.")
    else:
        print(f"{database}: daily_number column already exists.")
    conn.close()


migrate("shongwe_ordering")
migrate("shongwe_ordering_test")
