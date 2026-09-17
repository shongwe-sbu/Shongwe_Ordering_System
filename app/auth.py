from __future__ import annotations

import bcrypt
from typing import Dict, List, Optional


EMPLOYEE_ROLE = "employee"
ADMIN_ROLE = "admin"
users: Dict[str, Dict[str, str]] = {}


def register_user(username: str, password: str, role: str) -> Dict[str, str]:
    username = username.strip()
    if not username:
        raise ValueError("Username cannot be empty.")
    if username in users:
        raise ValueError("Username already exists.")
    if not password:
        raise ValueError("Password cannot be empty.")
    if role not in {EMPLOYEE_ROLE, ADMIN_ROLE}:
        raise ValueError("Invalid user role.")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = {"username": username, "password": hashed, "role": role, "active": "true"}
    users[username] = user
    return user


def authenticate(
    username: str, password: str, role: Optional[str] = None
) -> Optional[Dict[str, str]]:
    user = users.get(username)
    if user is None or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return None
    if user["active"] != "true":
        return None
    if role is not None and user["role"] != role:
        return None
    return user


def list_users() -> List[Dict[str, str]]:
    return list(users.values())


def disable_user(username: str) -> Dict[str, str]:
    user = users.get(username)
    if user is None:
        raise ValueError("User not found.")
    user["active"] = "false"
    return user


def delete_user(username: str) -> None:
    if username not in users:
        raise ValueError("User not found.")
    del users[username]


def clear_users() -> None:
    users.clear()
