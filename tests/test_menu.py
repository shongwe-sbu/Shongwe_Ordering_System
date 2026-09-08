import unittest

from app.menu import add_menu_item, clear_menu, get_menu_item, list_menu_items


class MenuTests(unittest.TestCase):
    def setUp(self):
        clear_menu()

    def test_add_menu_item_stores_item(self):
        item = add_menu_item("Burger", 35.0, "Main")
        self.assertEqual(item["name"], "Burger")
        self.assertEqual(item["price"], 35.0)
        self.assertEqual(item["category"], "Main")

    def test_duplicate_item_name_is_rejected(self):
        add_menu_item("Burger", 35.0)
        with self.assertRaises(ValueError):
            add_menu_item("Burger", 40.0)

    def test_list_menu_items_returns_all_items(self):
        add_menu_item("Burger", 35.0)
        add_menu_item("Fries", 18.0)
        items = list_menu_items()
        self.assertEqual(len(items), 2)

    def test_get_menu_item_returns_matching_item(self):
        add_menu_item("Pizza", 50.0)
        item = get_menu_item("Pizza")
        self.assertIsNotNone(item)
        self.assertEqual(item["price"], 50.0)


if __name__ == "__main__":
    unittest.main()
