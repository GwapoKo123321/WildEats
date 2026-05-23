# WildEats Supply Module

This project is a Django-based module for the WildEats system. It implements the assigned ERD scope for the supply side of the system only.

## Project Structure

```text
WildEats_Betito/
├── README.md
└── PythonProject/
    ├── .venv/
    └── myproject/
        ├── manage.py
        ├── db.sqlite3
        ├── myproject/
        │   ├── settings.py
        │   ├── urls.py
        │   ├── asgi.py
        │   └── wsgi.py
        └── supply/
            ├── admin.py
            ├── apps.py
            ├── models.py
            ├── urls.py
            ├── views.py
            ├── migrations/
            └── templates/
                └── supply/
                    ├── index.html
                    └── login.html
```

## ERD-Based Scope

This module is based on the assigned ERD parts below:

- Ingredients and their storage details
- Inventory quantity, expiry, and location
- Supplier contact and delivery details

## Implemented Models

The `supply` app contains the following models based on the assigned ERD scope:

- `Supplier`
- `Ingredient`
- `Inventory`

### Model Coverage

- `Ingredient`
  Stores ingredient records and storage-related details such as `name`, `quantity_unit`, `reorder_threshold`, `storage_condition`, and `storage_area`.
- `Inventory`
  Stores stock monitoring details such as `quantity_available`, `expiry_date`, and `location`.
- `Supplier`
  Stores supplier details such as `name`, `contact_info`, and `delivery_details`.

### Relationships

- One `Supplier` can be linked to many `Ingredient` records.
- One `Ingredient` is linked to one `Inventory` record.

## Pages Included

- `Login Page`
- `Index Page / Dashboard`

The dashboard displays only the assigned module data:

- Ingredients
- Inventory
- Suppliers

## How To Run

1. Open a terminal in:

```powershell
C:\Users\James Ruby Betito\Downloads\WildEats_Betito\PythonProject\myproject
```

2. Run migrations:

```powershell
..\.venv\Scripts\python.exe manage.py migrate
```

3. Start the Django server on the required address:

```powershell
..\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8080
```

4. Open the browser and go to:

```text
http://127.0.0.1:8080/
```

or

```text
http://127.0.0.1:8080/login/
```

## Notes

- The project is configured to run locally using SQLite for this submission.
- The app included in this submission is `supply`.
- The implementation is intentionally limited to the assigned ERD scope only and does not include other group members' modules.

## Submission Note

Make sure to submit your project files along with any necessary documentation that explains your project structure and how to run it.
