from typing import Dict, List, Optional

from app.db import get_connection

VALID_STATUSES = ["preparing", "ready", "collected", "cancelled"]


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
        item_total = round(quantity * price, 2)
        total += item_total
        order_items.append({"name": name, "quantity": quantity, "price": price, "item_total": item_total})

    total = round(total, 2)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COALESCE(MAX(daily_number), 0) + 1 FROM orders WHERE DATE(created_at) = CURDATE()"
    )
    daily_number = cursor.fetchone()[0]
    cursor.execute(
        "INSERT INTO orders (customer_name, order_type, total, daily_number) VALUES (%s, %s, %s, %s)",
        (customer, order_type, total, daily_number),
    )
    order_id = cursor.lastrowid
    for item in order_items:
        cursor.execute(
            "INSERT INTO order_items (order_id, item_name, quantity, price, item_total) VALUES (%s, %s, %s, %s, %s)",
            (order_id, item["name"], item["quantity"], item["price"], item["item_total"]),
        )
    conn.commit()
    return {
        "order_id": daily_number,
        "customer_name": customer,
        "order_type": order_type,
        "items": order_items,
        "total": total,
        "status": "preparing",
    }


def list_orders() -> List[Dict[str, object]]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = cursor.fetchall()
    for order in orders:
        cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order["id"],))
        order["order_id"] = order["daily_number"]
        order["items"] = cursor.fetchall()
    return orders


def update_order_status(order_id: int, new_status: str) -> Optional[Dict[str, object]]:
    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid order status.")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET status = %s WHERE daily_number = %s AND DATE(created_at) = CURDATE()",
        (new_status, order_id),
    )
    if cursor.rowcount == 0:
        return None
    conn.commit()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM orders WHERE daily_number = %s AND DATE(created_at) = CURDATE()",
        (order_id,),
    )
    order = cursor.fetchone()
    order["order_id"] = order["daily_number"]
    return order


def sales_report(from_date: str, to_date: str) -> Dict[str, object]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT COUNT(*) AS order_count, COALESCE(SUM(total), 0) AS revenue
        FROM orders
        WHERE status = 'collected' AND DATE(created_at) BETWEEN %s AND %s
        """,
        (from_date, to_date),
    )
    summary = cursor.fetchone()
    cursor.execute(
        """
        SELECT oi.item_name, SUM(oi.quantity) AS total_qty
        FROM order_items oi
        JOIN orders o ON o.id = oi.order_id
        WHERE o.status = 'collected' AND DATE(o.created_at) BETWEEN %s AND %s
        GROUP BY oi.item_name
        ORDER BY total_qty DESC
        LIMIT 5
        """,
        (from_date, to_date),
    )
    top_items = cursor.fetchall()
    return {
        "from_date": from_date,
        "to_date": to_date,
        "order_count": summary["order_count"],
        "revenue": float(summary["revenue"]),
        "top_items": [{ "name": r["item_name"], "quantity": r["total_qty"]} for r in top_items],
    }


def clear_orders() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    conn.commit()
