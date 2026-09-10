from app.auth import ADMIN_ROLE, EMPLOYEE_ROLE, authenticate, register_user
from app.menu import add_menu_item, list_menu_items
from app.orders import create_order, list_orders, update_order_status


def show_menu():
    items = list_menu_items()
    if not items:
        print("No menu items available yet.")
        return

    print("\nMenu:")
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item['name']} - R{item['price']:.2f} ({item['category']})")


def create_order_from_console():
    customer_name = input("Customer name: ").strip()
    order_type = input("Order type (dine-in/takeaway): ").strip().lower()
    items = []

    while True:
        show_menu()
        selection = input("Choose menu item number to add (or 'done'): ").strip().lower()
        if selection == "done":
            break
        try:
            index = int(selection) - 1
        except ValueError:
            print("Invalid menu number.")
            continue

        menu_items = list_menu_items()
        if index < 0 or index >= len(menu_items):
            print("Invalid menu number.")
            continue

        chosen_item = menu_items[index]
        quantity = input(f"Quantity for {chosen_item['name']}: ").strip()
        try:
            qty = int(quantity)
        except ValueError:
            print("Quantity must be a number.")
            continue

        if qty <= 0:
            print("Quantity must be greater than zero.")
            continue

        items.append({
            "name": chosen_item["name"],
            "quantity": qty,
            "price": chosen_item["price"],
        })
        print(f"Added {qty} x {chosen_item['name']}.")

    if not items:
        print("No items selected. Order cancelled.")
        return

    order = create_order(customer_name, order_type, items)
    print("\nOrder created successfully.")
    print(f"Order ID: {order['order_id']}")
    print(f"Customer: {order['customer_name']}")
    print(f"Total: R{order['total']:.2f}")
    print(f"Status: {order['status']}")

    print("\nCurrent queue:")
    for queued_order in list_orders():
        print(f"#{queued_order['order_id']} - {queued_order['customer_name']} - {queued_order['status']} - R{queued_order['total']:.2f}")


VALID_STATUSES = ["preparing", "ready", "collected", "cancelled"]


def show_orders():
    all_orders = list_orders()
    if not all_orders:
        print("No orders placed yet.")
        return
    print("\nAll orders:")
    for order in all_orders:
        print(f"#{order['order_id']} | {order['customer_name']} | {order['order_type']} | {order['status']} | R{order['total']:.2f}")
        for item in order["items"]:
            print(f"   - {item['quantity']}x {item['name']} @ R{item['price']:.2f}")


def update_order_status_from_console():
    active_orders = [o for o in list_orders() if o["status"] not in {"collected", "cancelled"}]
    if not active_orders:
        print("No active orders.")
        return

    print("\nActive orders:")
    for order in active_orders:
        print(f"#{order['order_id']} - {order['customer_name']} - {order['status']} - R{order['total']:.2f}")

    try:
        order_id = int(input("Enter order ID to update: ").strip())
    except ValueError:
        print("Invalid order ID.")
        return

    print("Statuses: " + ", ".join(f"{i+1}. {s}" for i, s in enumerate(VALID_STATUSES)))
    try:
        status_choice = int(input("Choose new status number: ").strip()) - 1
    except ValueError:
        print("Invalid choice.")
        return

    if status_choice < 0 or status_choice >= len(VALID_STATUSES):
        print("Invalid choice.")
        return

    new_status = VALID_STATUSES[status_choice]
    try:
        updated = update_order_status(order_id, new_status)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if updated is None:
        print("Order not found.")
    else:
        print(f"Order #{updated['order_id']} status updated to '{updated['status']}'.")


def seed_data():
    register_user("admin1", "admin123", ADMIN_ROLE)
    register_user("emp1", "emp123", EMPLOYEE_ROLE)
    add_menu_item("Burger", 35.0, "Main")
    add_menu_item("Fries", 18.50, "Side")
    add_menu_item("Coke", 12.00, "Drink")


def main():
    seed_data()

    print("========================================")
    print("Shongwe Restaurant Ordering System")
    print("========================================")

    while True:
        print("\nSelect sign-in type:")
        print("1. Employee login")
        print("2. Administrator login")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "3":
            print("Goodbye.")
            break

        if choice not in {"1", "2"}:
            print("Invalid choice. Please try again.")
            continue

        role = EMPLOYEE_ROLE if choice == "1" else ADMIN_ROLE
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        user = authenticate(username, password, role)

        if user is None:
            print("Invalid username, password, or role.")
            continue

        print(f"\nLogin successful! Welcome {user['username']} ({user['role']}).")

        if user["role"] == EMPLOYEE_ROLE:
            print("Employee dashboard: manage orders, queue, and menu items.")
            while True:
                print("\nEmployee actions:")
                print("1. View menu")
                print("2. Create order")
                print("3. View orders")
                print("4. Update order status")
                print("5. Logout")
                action = input("Choose an action: ").strip()

                if action == "1":
                    show_menu()
                elif action == "2":
                    create_order_from_console()
                elif action == "3":
                    show_orders()
                elif action == "4":
                    update_order_status_from_console()
                elif action == "5":
                    print("Logged out.")
                    break
                else:
                    print("Invalid action.")
        else:
            print("Admin dashboard: view reports, staff, customers, and sales.")
            show_menu()

        print("You are now signed in.")


if __name__ == "__main__":
    main()
