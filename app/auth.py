from __future__ import annotations

from typing import Dict, Optional


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

    user = {"username": username, "password": password, "role": role}
    users[username] = user
    return user


def authenticate(
    username: str, password: str, role: Optional[str] = None
) -> Optional[Dict[str, str]]:
    user = users.get(username)
    if user is None or user["password"] != password:
        return None
    if role is not None and user["role"] != role:
        return None
    return user


def clear_users() -> None:
    users.clear()
