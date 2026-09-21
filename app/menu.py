from typing import Dict, List, Optional

from app.db import get_connection


def add_menu_item(name: str, price: float, category: str = "General") -> Dict[str, object]:
    item_name = name.strip()
    if not item_name:
        raise ValueError("Item name cannot be empty.")
    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO menu_items (name, price, category) VALUES (%s, %s, %s)",
            (item_name, float(price), category.strip() or "General"),
        )
        conn.commit()
        return {"name": item_name, "price": float(price), "category": category.strip() or "General", "available": True}
    except Exception as e:
        conn.rollback()
        if "Duplicate entry" in str(e):
            raise ValueError("Menu item already exists.")
        raise


def edit_menu_item(name: str, price: float = None, category: str = None) -> Dict[str, object]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items WHERE name = %s", (name.strip(),))
    item = cursor.fetchone()
    if item is None:
        raise ValueError("Menu item not found.")
    new_price = float(price) if price is not None else item["price"]
    new_category = category.strip() if category else item["category"]
    if price is not None and price <= 0:
        raise ValueError("Price must be greater than zero.")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE menu_items SET price = %s, category = %s WHERE name = %s",
        (new_price, new_category, name.strip()),
    )
    conn.commit()
    return {"name": name.strip(), "price": new_price, "category": new_category}


def disable_menu_item(name: str) -> Dict[str, object]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE menu_items SET available = FALSE WHERE name = %s", (name.strip(),))
    if cursor.rowcount == 0:
        raise ValueError("Menu item not found.")
    conn.commit()
    return {"name": name.strip(), "available": False}


def delete_menu_item(name: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items WHERE name = %s", (name.strip(),))
    if cursor.rowcount == 0:
        raise ValueError("Menu item not found.")
    conn.commit()


def list_menu_items(available_only: bool = False) -> List[Dict[str, object]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if available_only:
        cursor.execute("SELECT * FROM menu_items WHERE available = TRUE")
    else:
        cursor.execute("SELECT * FROM menu_items")
    return cursor.fetchall()


def get_menu_item(name: str) -> Optional[Dict[str, object]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items WHERE name = %s", (name.strip(),))
    return cursor.fetchone()


def clear_menu() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items")
    conn.commit()
