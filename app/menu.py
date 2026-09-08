from typing import Dict, List, Optional

menu: Dict[str, Dict[str, object]] = {}


def add_menu_item(name: str, price: float, category: str = "General") -> Dict[str, object]:
    item_name = name.strip()
    if not item_name:
        raise ValueError("Item name cannot be empty.")
    if item_name in menu:
        raise ValueError("Menu item already exists.")
    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    item = {"name": item_name, "price": float(price), "category": category.strip() or "General"}
    menu[item_name] = item
    return item


def list_menu_items() -> List[Dict[str, object]]:
    return list(menu.values())


def get_menu_item(name: str) -> Optional[Dict[str, object]]:
    return menu.get(name.strip())


def clear_menu() -> None:
    menu.clear()
