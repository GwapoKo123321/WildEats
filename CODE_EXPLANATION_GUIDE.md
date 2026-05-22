# WildEats Code Explanation Guide

## Project Overview

WildEats is a Django web app for cafeteria ordering. It has three main user roles:

- Student
- Vendor
- Admin

Students can create orders, add menu items, submit payments, and view their own records.

Vendors can manage menu items, verify or fail payments, and update order progress.

Admins can view all orders, payments, users, vendors, and menu items.

## Main Apps

### `main`

Handles:

- Login
- Registration
- Profile editing
- Homepage

### `salesandtransactions`

Handles:

- Orders
- Order items
- Menu items
- Payment records
- Dashboards
- Role-based access

## Important Files

### `salesandtransactions/models.py`

Defines the database models:

- `Order`
- `OrderItem`
- `MenuItem`
- `PaymentRecord`

This file also contains important business rules, such as preventing orders from being cancelled or deleted once linked to payment records.

### `salesandtransactions/views.py`

Contains the main workflow logic:

- Creating orders
- Adding order items
- Recording payments
- Verifying payments
- Failing payments
- Updating order status
- Showing dashboards and list pages

### `salesandtransactions/forms.py`

Handles form validation.

Important validation includes:

- Payment must be cash.
- Payment must cover the full order total.
- Partial payments are not allowed.

### `salesandtransactions/urls.py`

Defines clean routes such as:

- `/sales/orders/new/`
- `/sales/orders/<order_id>/`
- `/sales/menu-items/`
- `/sales/payments/`
- `/sales/users/students/`
- `/sales/users/vendors/`

Old camelCase routes are kept as redirects so older links still work.

### `salesandtransactions/templates/`

Contains the HTML pages for:

- Dashboard
- Order details
- Menu items
- Payment records
- Registered students/vendors

## Order Flow

1. A student creates an order at `/sales/orders/new/`.
2. The student must select at least one menu item.
3. The order starts with status `Pending Payment`.
4. The student submits payment.
5. The payment must be cash and must match the full order total.
6. The order status becomes `Payment Submitted`.
7. A vendor verifies or fails the payment.
8. If verified, the order status becomes `Payment Verified`.
9. The vendor can update the order to `Processing` and then `Completed`.

## Payment Rules

Payments must:

- Be made in cash
- Cover the entire order total
- Not be partial payments

This rule is enforced in `PaymentRecordForm` in `salesandtransactions/forms.py`.

Even if a user edits the HTML form or sends a custom request, the server-side form validation blocks invalid payments.

## Cancel/Delete Rule

Orders cannot be cancelled or deleted once they have payment records.

This is enforced in the `Order` model:

- `can_cancel`
- `cancel()`
- `delete()`

This is important because model-level rules protect the database, not just the user interface.

## Payment Failed Status

The old wording `Rejected` was changed to `Failed`.

Current statuses:

- Payment status: `Failed`
- Order status: `Payment Failed`
- Vendor action button: `Fail`

The migration `0007_rename_failed_statuses.py` updates old database records to use the new wording.

## Dashboard

The dashboard focuses on orders.

Cards link to separate pages:

- Menu Items: `/sales/menu-items/`
- Payment Records: `/sales/payments/`
- Students: `/sales/users/students/`
- Vendors: `/sales/users/vendors/`

Payment Records are displayed as a table for easier scanning.

Registered Students and Registered Vendors pages show:

- Name
- Email

## Routing

The routing was cleaned from camelCase URLs to readable REST-style paths.

Examples:

| Old Route | New Route |
|---|---|
| `/sales/addNewOrder/` | `/sales/orders/new/` |
| `/sales/orderSummary/1/` | `/sales/orders/1/` |
| `/sales/addOrderItem/1/` | `/sales/orders/1/items/add/` |
| `/sales/recordPayment/1/` | `/sales/orders/1/payments/record/` |
| `/sales/paymentRecords/` | `/sales/payments/` |
| `/sales/menuItems/` | `/sales/menu-items/` |

Old routes redirect to the new routes to avoid breaking existing bookmarks.

## Common Q&A

### Q: What is this project?

It is a Django cafeteria ordering system where students order food, vendors manage items and payments, and admins monitor the system.

### Q: Why are there roles?

Roles control permissions. Students, vendors, and admins have different responsibilities, so they should not access the same actions.

### Q: What are the main models?

The main models are:

- `Order`
- `OrderItem`
- `MenuItem`
- `PaymentRecord`

### Q: Why must payment be full cash payment?

That is the business rule. The system does not allow partial payments or non-cash methods, so the payment must equal the full order total.

### Q: Where is payment validation handled?

Payment validation is handled in `PaymentRecordForm` inside `salesandtransactions/forms.py`.

### Q: Why also enforce cancellation rules in the model?

Because model-level validation protects the data even if the request does not come from the normal web form.

### Q: Why use migrations?

Migrations keep the database structure and stored data aligned with the code.

### Q: Why did you keep old URLs?

Old URLs redirect to the new clean URLs so existing links do not break.

### Q: Why is Payment Records a table?

Payment records are transactional data. A table is easier to scan than card-style summaries.

## Short Presentation Script

Use this order when explaining:

1. This is a Django ordering system for cafeteria transactions.
2. It uses role-based access for students, vendors, and admins.
3. The main models are `Order`, `OrderItem`, `MenuItem`, and `PaymentRecord`.
4. Students create orders and submit full cash payments.
5. Vendors verify or fail payments and update order progress.
6. Admins can view all orders, payments, registered users, and menu items.
7. Forms validate user input.
8. Models protect important business rules.
9. Templates show the role-specific interface.
10. Routes were cleaned to make the project easier to understand and maintain.
