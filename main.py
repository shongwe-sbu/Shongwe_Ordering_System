from app.auth import ADMIN_ROLE, EMPLOYEE_ROLE, authenticate, register_user
from app.menu import add_menu_item, list_menu_items


def show_menu():
    items = list_menu_items()
    if not items:
        print("No menu items available yet.")
        return

    print("\nMenu:")
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item['name']} - R{item['price']:.2f} ({item['category']})")


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
            show_menu()
        else:
            print("Admin dashboard: view reports, staff, customers, and sales.")
            show_menu()

        print("You are now signed in.")


if __name__ == "__main__":
    main()
