from __future__ import annotations

import bcrypt
import mysql.connector
from typing import Dict, List, Optional

from app.db import get_connection, reset_connection

EMPLOYEE_ROLE = "employee"
ADMIN_ROLE = "admin"


def _cursor(dictionary=False):
    try:
        return get_connection().cursor(dictionary=dictionary)
    except mysql.connector.OperationalError:
        return reset_connection().cursor(dictionary=dictionary)


def register_user(username: str, password: str, role: str) -> Dict[str, str]:
    username = username.strip()
    if not username:
        raise ValueError("Username cannot be empty.")
    if not password:
        raise ValueError("Password cannot be empty.")
    if role not in {EMPLOYEE_ROLE, ADMIN_ROLE}:
        raise ValueError("Invalid user role.")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = get_connection()
    cur = _cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed, role),
        )
        conn.commit()
        return {"username": username, "role": role, "active": "true"}
    except Exception as e:
        conn.rollback()
        if "Duplicate entry" in str(e):
            raise ValueError("Username already exists.")
        raise


def authenticate(username: str, password: str, role: Optional[str] = None) -> Optional[Dict[str, str]]:
    cur = _cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user is None or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return None
    if not user["active"]:
        return None
    if role is not None and user["role"] != role:
        return None
    return {"username": user["username"], "role": user["role"], "active": str(user["active"])}


def list_users() -> List[Dict[str, str]]:
    cur = _cursor(dictionary=True)
    cur.execute("SELECT username, role, active FROM users")
    rows = cur.fetchall()
    return [{"username": r["username"], "role": r["role"], "active": "true" if r["active"] else "false"} for r in rows]


def disable_user(username: str) -> Dict[str, str]:
    conn = get_connection()
    cur = _cursor()
    cur.execute("UPDATE users SET active = FALSE WHERE username = %s", (username,))
    if cur.rowcount == 0:
        raise ValueError("User not found.")
    conn.commit()
    return {"username": username, "active": "false"}


def delete_user(username: str) -> None:
    conn = get_connection()
    cur = _cursor()
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    if cur.rowcount == 0:
        raise ValueError("User not found.")
    conn.commit()


def clear_users() -> None:
    conn = get_connection()
    cur = _cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
