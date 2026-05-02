# WildEats



WildEats is a Django web app for managing cafeteria sales and transactions.
Users can create orders and add items to each order using a relational database.

---

## Structure

```
WildEats/
├── main/ (index & login)
├── salesandtransactions/ (orders & items)
├── wildeats/ (settings)
├── manage.py
```

---

## ⚙How to Run

```
python -m venv venv
venv\Scripts\activate
pip install django mysqlclient
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8080
```

---

## URLs

* `/` → Index
* `/login/` → Login
* `/sales/` → Sales page
* `/sales/addNewOrder/` → Add Order
* `/sales/addOrderItem/<id>/` → Add Item

---

## Features

* Login required for access
* Create Orders
* Add Order Items
* View Orders with items

---

## Author

Marishka Tuazon – Sales & Transactions
