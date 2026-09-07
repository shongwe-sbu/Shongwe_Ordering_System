from app.auth import ADMIN_ROLE, EMPLOYEE_ROLE, authenticate, register_user


def main():
    # Demo accounts for the first version.
    register_user("admin1", "admin123", ADMIN_ROLE)
    register_user("emp1", "emp123", EMPLOYEE_ROLE)

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
            print("Employee dashboard: \nMenu Items \nManage Orders \nView Queue")
        else:
            print("Admin dashboard: view reports, staff, customers, and sales.")

        print("You are now signed in.")


if __name__ == "__main__":
    main()
