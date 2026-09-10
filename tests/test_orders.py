import unittest

from app.orders import clear_orders, create_order, list_orders, update_order_status


class OrderTests(unittest.TestCase):
    def setUp(self):
        clear_orders()

    def test_create_order_calculates_total(self):
        order = create_order(
            "Alice",
            "dine-in",
            [
                {"name": "Burger", "quantity": 2, "price": 35.0},
                {"name": "Coke", "quantity": 1, "price": 12.0},
            ],
        )
        self.assertEqual(order["total"], 82.0)
        self.assertEqual(order["status"], "preparing")

    def test_order_is_added_to_queue(self):
        create_order("Bob", "takeaway", [{"name": "Fries", "quantity": 1, "price": 18.5}])
        orders = list_orders()
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]["customer_name"], "Bob")

    def test_status_can_be_updated(self):
        order = create_order("Carol", "dine-in", [{"name": "Burger", "quantity": 1, "price": 35.0}])
        updated = update_order_status(order["order_id"], "ready")
        self.assertEqual(updated["status"], "ready")

    def test_full_status_progression(self):
        order = create_order("Dave", "dine-in", [{"name": "Burger", "quantity": 1, "price": 35.0}])
        for status in ["ready", "collected"]:
            updated = update_order_status(order["order_id"], status)
            self.assertEqual(updated["status"], status)

    def test_invalid_status_raises_error(self):
        order = create_order("Eve", "takeaway", [{"name": "Fries", "quantity": 1, "price": 18.5}])
        with self.assertRaises(ValueError):
            update_order_status(order["order_id"], "pending")


if __name__ == "__main__":
    unittest.main()
