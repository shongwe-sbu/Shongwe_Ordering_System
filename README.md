# Shongwe Restaurant Ordering System

The Shongwe Restaurant Ordering System is a Python console application for managing in-restaurant orders. Restaurant employees will use it to record customer orders, manage the order queue, update order statuses, and record sales. Managers or administrators will manage the menu, staff access, customers, orders, and reports.

## Combined Project Scope

This is one combined project that covers both the **Cyber Security** and **Cloud Computing** requirements. The restaurant ordering system will demonstrate how security controls protect users, administrators, accounts, and order information, while cloud technologies provide reliable storage, access, backups, and reporting for the application.

The Cyber Security focus includes authentication, role-based access control, secure password storage, input validation, protected administrator functions, secure handling of customer information, and prevention of unauthorized access. The Cloud Computing focus includes using AWS Free Tier services, storing orders and customer details in a managed cloud database, enabling backups where available, and making sales information available to authorized administrators.

## Project Goals

- Allow employees to securely sign in and take customer orders.
- Allow employees to record optional customer details without requiring customers to create accounts.
- Save customer, order, and payment-related information in a cloud-hosted database.
- Allow employees to manage the current restaurant order queue.
- Allow administrators to monitor customers and manage current and past orders.
- Provide sales information showing what was sold and how much revenue was generated.
- Keep historical order prices accurate, even when menu prices change later.

## Main User Areas

### Employee Side

- Log in with an authorized staff account.
- Record optional customer name and contact details.
- Browse available menu items and prices.
- Add items to an order and submit it to the restaurant queue.
- View and update active order statuses.

Customers do not log in to the system. Their details are recorded by an employee when needed.

### Administrator Side

- Sign in through a protected manager or administrator area.
- Create and manage employee accounts and permissions.
- Add, edit, disable, and remove menu items.
- View customer details and customer order history.
- View active, completed, and cancelled orders.
- Update order statuses, such as `Pending`, `Confirmed`, `Preparing`, `Ready`, and `Completed`.
- Review sales totals, popular menu items, and revenue over selected dates.
- Export sales data for further analysis.

## Planned Architecture

```text
Customer or Administrator
		|
	    v
	 Python Console Application
			|
			v
		  Python Backend Logic
	/       |       \
 Authentication Orders  Reports
		|
		v
	    Amazon RDS MySQL Database
```

The first version is planned around:

	- **Application:** Python console application.
	- **Database:** MySQL hosted on Amazon RDS using the AWS Free Tier where eligible.
	- **Interface:** Text-based menus for customer and administrator workflows.
	- **Authentication:** Secure Python authentication with customer and administrator roles.
	- **Cloud provider:** Amazon Web Services (AWS).
- **Source control:** Git and GitHub.

	The system can later be extended with a web interface if the project grows beyond the initial console application.

## Core Data

The database is expected to contain the following main records:

- **Staff users:** Login details, contact information, and account role.
- **Customers:** Optional name and contact details captured by employees.
- **Menu items:** Names, descriptions, categories, prices, and availability.
- **Orders:** Customer, order type, table number where applicable, total amount, status, payment status, and order date.
- **Order items:** Menu item, quantity, and the price at the time of ordering.
- **Payments:** Payment provider reference, amount, status, and payment date.

Order item prices will be stored when an order is placed. This ensures that historical orders remain correct if the restaurant changes its menu prices later.

## Order Process

1. An employee signs in with an authorized staff account.
2. The employee records optional customer details and selects the order type: dine-in or takeaway.
3. The employee selects menu items and adds them to the order.
4. The system validates the items, quantities, prices, and order total.
5. The order and its items are saved in the cloud database and added to the restaurant queue.
6. Employees update the order status as it is prepared and handed to the customer.
7. Completed and paid orders are included in sales reports.

## Security Expectations

- Passwords must be securely hashed and never stored as plain text.
- Employee and administrator permissions must be separated.
- Staff users must only access the functions allowed by their role.
- Order totals must be calculated and validated on the server.
- Payment card details must not be stored by this application.
- Secrets and database credentials must be stored in environment variables.
- Database credentials must be stored securely and not hard-coded in the application.
- AWS database access must be restricted to authorized users and services.
- Cloud database backups and application error logging should be enabled where available.

## Planned Development Phases

1. Set up the Python console application.
2. Configure a local MySQL database for development.
3. Create and configure an AWS RDS MySQL database using the AWS Free Tier where eligible.
4. Implement administrator-managed staff accounts, login, and user roles.
5. Implement menu and category management.
6. Implement the shopping cart and order creation process.
7. Implement order status updates and customer order history.
8. Build the administrator console.
9. Add sales reports and data export.
10. Add payment recording for cash or card payments if required.
11. Add automated tests, security checks, backups, and AWS configuration documentation.

## Project Verification Codes

- Cyber Security Verification Code: `WTC-LUS8YWD7`
- Cloud Computing Verification Code: `WTC-STGLUT43`
