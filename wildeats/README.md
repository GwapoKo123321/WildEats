# WildEats - Campus Cafeteria Management System
## Project Structure

## Requirements
- Python 3.x
- Django 6.0.4
- MySQL

## How to Run

### 1. Install dependencies
pip install django mysqlclient

### 2. Setup Database
Create a MySQL database called wildeats
CREATE DATABASE wildeats;

### 3. Apply Migrations
python manage.py migrate

### 4. Create Superuser
python manage.py createsuperuser

### 5. Run Server
python manage.py runserver 8080

### 6. Open Browser
http://127.0.0.1:8080/

## Pages
- http://127.0.0.1:8080/ → Index page
- http://127.0.0.1:8080/login/ → Login page
- http://127.0.0.1:8080/admin/ → Admin panel

## Apps
| App | Developer | Entities |
|-----|-----------|----------|
| foodcomposition | (your name) | FoodItem, NutritionInfo, Recipe |

## Models

### FoodItem
- FoodItemID, Name, Price, PortionSize

### NutritionInfo
- NutritionInfoID, FoodItem, Calories, Protein, Fat, Carbs, Sodium

### Recipe
- RecipeID, FoodItem, PreparationTime, Instructions