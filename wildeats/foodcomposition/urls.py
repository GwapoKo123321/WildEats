# # from django.urls import path
# # from . import views
# #
# # urlpatterns = [
# #     path('', views.HomePageView.as_view(), name='home'),
# #     path('login/', views.LoginView.as_view(), name='login'),
# #     path('logout/', views.LogoutView.as_view(), name='logout'),
# #     path('register/', views.RegisterView.as_view(), name='register'),
# #     path('add/', views.AddFoodItemView.as_view(), name='add-food'),
# #     path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
# # ]
#
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.HomePageView.as_view(), name='home'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', views.LogoutView.as_view(), name='logout'),
#     path('register/', views.RegisterView.as_view(), name='register'),
#     path('add/', views.AddFoodItemView.as_view(), name='add-food'),
#     path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
# ]

# from django.urls import path
# from . import views
#
# # urlpatterns = [
# #     path('', views.HomePageView.as_view(), name='home'),
# #     path('login/', views.LoginView.as_view(), name='login'),
# #     path('logout/', views.LogoutView.as_view(), name='logout'),
# #     path('register/', views.RegisterView.as_view(), name='register'),
# #     path('foods/', views.FoodListView.as_view(), name='food-list'),
# #     path('foods/<int:pk>/', views.FoodDetailView.as_view(), name='food-detail'),
# #     path('foods/add/', views.AddFoodItemView.as_view(), name='add-food'),
# #     path('foods/<int:pk>/edit/', views.EditFoodItemView.as_view(), name='edit-food'),
# #     path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
# # ]

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
#     path('cafeterias/', views.CafeteriaListView.as_view(), name='cafeteria-list'),
#     path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
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
    path('cafeterias/', views.CafeteriaListView.as_view(), name='cafeteria-list'),
    path('cafeterias/add/', views.AddCafeteriaView.as_view(), name='add-cafeteria'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
]