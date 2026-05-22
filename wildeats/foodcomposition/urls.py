# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.HomePageView.as_view(), name='home'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', views.LogoutView.as_view(), name='logout'),
#     path('register/', views.RegisterView.as_view(), name='register'),
#     path('foods/', views.FoodListView.as_view(), name='food-list'),
#     path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
#     path('foods/add/', views.AddFoodItemView.as_view(), name='add-food'),
#     path('foods/<int:pk>/edit/', views.EditFoodItemView.as_view(), name='edit-food'),
#     path('ingredients/', views.IngredientListView.as_view(), name='ingredient-list'),
#     path('ingredients/add/', views.AddIngredientView.as_view(), name='add-ingredient'),
#     path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),
#     path('ingredients/<int:pk>/edit/', views.EditIngredientView.as_view(), name='edit-ingredient'),
#     path('cafeterias/', views.CafeteriaListView.as_view(), name='cafeteria-list'),
#     path('cafeterias/add/', views.AddCafeteriaView.as_view(), name='add-cafeteria'),
#     path('cafeterias/<int:pk>/', views.CafeteriaDetailView.as_view(), name='cafeteria-detail'),
#     path('cafeterias/<int:pk>/edit/', views.EditCafeteriaView.as_view(), name='edit-cafeteria'),
#     path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
#     path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
#     path('admin-dashboard/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
#     path('admin-dashboard/foods/', views.AdminFoodListView.as_view(), name='admin-food-list'),
#     path('admin-dashboard/ingredients/', views.AdminIngredientListView.as_view(), name='admin-ingredient-list'),
#     path('admin-dashboard/cafeterias/', views.AdminCafeteriaListView.as_view(), name='admin-cafeteria-list'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('foods/', views.FoodListView.as_view(), name='food-list'),
    path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
    path('foods/add/', views.AddFoodItemView.as_view(), name='add-food'),
    path('foods/<int:pk>/edit/', views.EditFoodItemView.as_view(), name='edit-food'),
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient-list'),
    path('ingredients/add/', views.AddIngredientView.as_view(), name='add-ingredient'),
    path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),
    path('ingredients/<int:pk>/edit/', views.EditIngredientView.as_view(), name='edit-ingredient'),
    path('cafeterias/', views.CafeteriaListView.as_view(), name='cafeteria-list'),
    path('cafeterias/add/', views.AddCafeteriaView.as_view(), name='add-cafeteria'),
    path('cafeterias/<int:pk>/', views.CafeteriaDetailView.as_view(), name='cafeteria-detail'),
    path('cafeterias/<int:pk>/edit/', views.EditCafeteriaView.as_view(), name='edit-cafeteria'),
    path('discounts/', views.DiscountListView.as_view(), name='discount-list'),
    path('discounts/add/', views.AddDiscountView.as_view(), name='add-discount'),
    path('discounts/<int:pk>/', views.DiscountDetailView.as_view(), name='discount-detail'),
    path('discounts/<int:pk>/edit/', views.EditDiscountView.as_view(), name='edit-discount'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin-dashboard/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin-dashboard/foods/', views.AdminFoodListView.as_view(), name='admin-food-list'),
    path('admin-dashboard/ingredients/', views.AdminIngredientListView.as_view(), name='admin-ingredient-list'),
    path('admin-dashboard/cafeterias/', views.AdminCafeteriaListView.as_view(), name='admin-cafeteria-list'),
    path('admin-dashboard/discounts/', views.AdminDiscountListView.as_view(), name='admin-discount-list'),

]