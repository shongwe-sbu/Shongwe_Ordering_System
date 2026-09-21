import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

_connection = None


def _connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=os.getenv("DB_SSL_CA"),
        ssl_verify_cert=True,
        use_pure=True,
        connect_timeout=10,
        autocommit=False,
    )


def get_connection():
    global _connection
    if _connection is None:
        _connection = _connect()
    return _connection


def reset_connection():
    global _connection
    try:
        if _connection is not None:
            _connection.close()
    except Exception:
        pass
    _connection = _connect()
    return _connection
