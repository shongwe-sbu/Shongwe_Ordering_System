# Shongwe Restaurant Ordering System

The Shongwe Restaurant Ordering System is a Python console application for managing in restaurant orders. Restaurant employees use it to record customer orders, manage the order queue and update order statuses. Administrators manage the menu, staff accounts, orders and sales reports.

## Combined Project Scope

This is one combined project that covers both the **CyberSecurity** and **Cloud Computing** requirements. The restaurant ordering system demonstrates how security controls protect users, administrators, accounts and order information, while cloud technologies provide reliable storage, access, backups and reporting for the application.

The CyberSecurity focus includes authentication, role-based access control, secure password storage, input validation, login attempt limiting, protected administrator functions, secure handling of customer information and prevention of unauthorized access. The Cloud Computing focus includes using AWS Free Tier services, storing orders and customer details in a managed cloud database, enabling backups and making sales information available to authorized administrators.

## Project Goals

- Allow employees to securely sign in and take customer orders.
- Allow employees to record optional customer details without requiring customers to create accounts.
- Save customer order information in a cloud-hosted database.
- Allow employees to manage the current restaurant order queue.
- Allow administrators to monitor customers and manage current and past orders.
- Provide sales information showing what was sold and how much revenue was generated.
- Keep historical order prices accurate, even when menu prices change later.

## Main User Areas

### Employee Side

- Log in with an authorized staff account (password input is masked).
- Record optional customer name and contact details.
- Browse available menu items and prices.
- Add items to an order and submit it to the restaurant queue.
- View and update active order statuses (preparing, ready, collected, cancelled).

Customers do not log in to the system. Their details are recorded by an employee when needed.

### Administrator Side

- Sign in through a protected administrator account.
- Create and manage employee accounts and permissions.
- Add, edit, disable and remove menu items.
- View all active, completed and cancelled orders.
- Review sales totals, popular menu items and revenue over a selected date range.
- Export sales data to a CSV file for further analysis.

## Architecture

```text
Employee or Administrator
        |
        v
 Python Console Application (main.py)
        |
        v
  Python Backend Logic
 /      |        \
Auth   Menu    Orders & Reports
        |
        v
  Amazon RDS MySQL Database
```

- **Application:** Python console application.
- **Database:** MySQL hosted on Amazon RDS using the AWS Free Tier.
- **Interface:** Text-based menus for employee and administrator workflows.
- **Authentication:** bcrypt password hashing, role-based access control (admin/employee).
- **Cloud provider:** Amazon Web Services (AWS).
- **AWS documentation:** See `AWS_SETUP.md` for full RDS setup, SSL, security groups and environment variable configuration.

## Core Data

The database contains the following main records:

- **Staff users:** Login details, contact information and account role.
- **Customers:** Optional name and contact details captured by employees.
- **Menu items:** Names, descriptions, categories, prices and availability.
- **Orders:** Customer, order type, table number where applicable, daily order number, total amount, status and order date.
- **Order items:** Menu item, quantity and the price at the time of ordering.

Order item prices are stored when an order is placed. This ensures that historical orders remain correct if the restaurant changes its menu prices later.

Payments are handled in person at the store and are not recorded by this application.

## Order Process

1. An employee signs in with an authorized staff account (login is limited to 3 attempts).
2. The employee records optional customer details and selects the order type: dine-in or takeaway.
3. The employee selects menu items and adds them to the order.
4. The system validates the items, quantities, prices and order total.
5. The order and its items are saved in the cloud database and added to the restaurant queue.
6. Each order is assigned a daily order number that resets to 1 at the start of each day.
7. Employees update the order status as it is prepared and handed to the customer.
8. Collected orders are included in sales reports.

## Order Numbering

Orders use a daily order number as the user-facing ID. This resets to 1 at the start of each day, making it easy for staff to reference orders during a shift. The internal database ID auto-increments and is used for database integrity and foreign key relationships.

## Sales Reports

Administrators can generate a sales report for any date range. The report shows:

- Total revenue from collected orders.
- Total number of collected orders.
- Top 5 menu items by quantity sold.

After viewing a report, the administrator is prompted to export the data to a CSV file named `sales_YYYY-MM-DD_to_YYYY-MM-DD.csv`.

## Security Controls

- Passwords are hashed with bcrypt and never stored as plain text.
- Password input is masked using `getpass` (requires a real CMD window — not the VS Code integrated terminal).
- Login is limited to 3 attempts before access is denied.
- Usernames must be alphanumeric and at least 3 characters long.
- Passwords must be at least 8 characters long.
- Employee and administrator permissions are separated by role.
- Staff users can only access the functions allowed by their role.
- Order totals are calculated and validated server-side.
- Payment card details are not stored by this application.
- Database credentials are stored in environment variables and never hard-coded.
- AWS database access is restricted via security group rules.
- SSL is enforced for all database connections.
- Cloud database backups are enabled on the RDS instance.

## Development Phases Completed

1. Set up the Python console application.
2. Configured a local MySQL database for development.
3. Created and configured an AWS RDS MySQL database using the AWS Free Tier.
4. Implemented administrator-managed staff accounts, login and user roles.
5. Implemented menu and category management.
6. Implemented the shopping cart and order creation process.
7. Implemented order status updates and daily order numbering.
8. Built the administrator console.
9. Added sales reports and CSV data export.
10. Added input validation and login attempt limiting.
11. Added automated tests, security checks, backups and AWS configuration documentation.

## Testing

The project includes 16 automated tests across three test files:

- `tests/test_auth.py` — 5 tests covering registration, authentication, listing, disabling and deleting users.
- `tests/test_menu.py` — 4 tests covering adding, editing, disabling and deleting menu items.
- `tests/test_orders.py` — 6 tests covering order creation, status updates, daily numbering, sales reports and CSV export.

Tests run against an isolated `shongwe_ordering_test` database. The production database is never touched by tests. Each test file sets `TEST_MODE=1` before any imports to ensure test isolation.

## Project Verification Codes

- CyberSecurity Verification Code: `WTC-LUS8YWD7`
- Cloud Computing Verification Code: `WTC-STGLUT43`
