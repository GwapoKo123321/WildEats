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

* `/` - Home
* `/login/` - Login
* `/register/` - Registration
* `/edit-profile/` - Profile
* `/sales/` - Orders dashboard
* `/sales/addNewOrder/` - Create order
* `/sales/orderSummary/<id>/` - Order details

---

## Features

* Login required for access
* Create Orders
* Add Order Items
* View Orders with items

---

## Author

Marishka Tuazon – Sales & Transactions
