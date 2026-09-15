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

    item = {"name": item_name, "price": float(price), "category": category.strip() or "General", "available": True}
    menu[item_name] = item
    return item


def edit_menu_item(name: str, price: float = None, category: str = None) -> Dict[str, object]:
    item = menu.get(name.strip())
    if item is None:
        raise ValueError("Menu item not found.")
    if price is not None:
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        item["price"] = float(price)
    if category is not None:
        item["category"] = category.strip() or "General"
    return item


def disable_menu_item(name: str) -> Dict[str, object]:
    item = menu.get(name.strip())
    if item is None:
        raise ValueError("Menu item not found.")
    item["available"] = False
    return item


def delete_menu_item(name: str) -> None:
    if name.strip() not in menu:
        raise ValueError("Menu item not found.")
    del menu[name.strip()]


def list_menu_items(available_only: bool = False) -> List[Dict[str, object]]:
    if available_only:
        return [i for i in menu.values() if i["available"]]
    return list(menu.values())


def get_menu_item(name: str) -> Optional[Dict[str, object]]:
    return menu.get(name.strip())


def clear_menu() -> None:
    menu.clear()
