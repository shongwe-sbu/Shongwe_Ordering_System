from typing import Dict, List, Optional

orders: List[Dict[str, object]] = []
_order_id_counter = 1


def clear_orders() -> None:
    orders.clear()
    global _order_id_counter
    _order_id_counter = 1


def create_order(customer_name: str, order_type: str, items: List[Dict[str, object]]) -> Dict[str, object]:
    customer = customer_name.strip()
    if not customer:
        raise ValueError("Customer name cannot be empty.")
    if order_type not in {"dine-in", "takeaway"}:
        raise ValueError("Order type must be 'dine-in' or 'takeaway'.")
    if not items:
        raise ValueError("Order must contain at least one item.")

    order_items = []
    total = 0.0

    for item in items:
        name = str(item["name"]).strip()
        quantity = int(item["quantity"])
        price = float(item["price"])

        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        item_total = quantity * price
        total += item_total
        order_items.append(
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "item_total": round(item_total, 2),
            }
        )

    global _order_id_counter
    order = {
        "order_id": _order_id_counter,
        "customer_name": customer,
        "order_type": order_type,
        "items": order_items,
        "total": round(total, 2),
        "status": "preparing",
    }
    orders.append(order)
    _order_id_counter += 1
    return order


def list_orders() -> List[Dict[str, object]]:
    return list(orders)


def update_order_status(order_id: int, new_status: str) -> Optional[Dict[str, object]]:
    for order in orders:
        if int(order["order_id"]) == order_id:
            valid_statuses = {"preparing", "ready", "collected", "cancelled"}
            if new_status not in valid_statuses:
                raise ValueError("Invalid order status.")
            order["status"] = new_status
            return order
    return None
