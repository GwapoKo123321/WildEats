# # # # from django.contrib.auth import authenticate, login, logout
# # # # from django.contrib.auth.mixins import LoginRequiredMixin
# # # # from django.shortcuts import render, redirect
# # # # from django.views import View
# # # # from .forms import FoodItemForm, NutritionInfoForm, RecipeForm, RegisterForm
# # # # from .models import FoodItem
# # # #
# # # #
# # # # class HomePageView(View):
# # # #     template_name = 'foodcomposition/index.html'
# # # #
# # # #     def get(self, request):
# # # #         food_items = FoodItem.objects.all() if request.user.is_authenticated else []
# # # #         return render(request, self.template_name, {
# # # #             'user': request.user,
# # # #             'food_items': food_items,
# # # #         })
# # # #
# # # #
# # # # class LoginView(View):
# # # #     template_name = 'foodcomposition/login.html'
# # # #
# # # #     def get(self, request):
# # # #         if request.user.is_authenticated:
# # # #             return redirect('home')
# # # #         return render(request, self.template_name)
# # # #
# # # #     def post(self, request):
# # # #         username = request.POST['username']
# # # #         password = request.POST['password']
# # # #         user = authenticate(request, username=username, password=password)
# # # #         if user is not None:
# # # #             login(request, user)
# # # #             return redirect('home')
# # # #         return render(request, self.template_name, {'error': 'Invalid credentials'})
# # # #
# # # #
# # # # class RegisterView(View):
# # # #     template_name = 'foodcomposition/register.html'
# # # #
# # # #     def get(self, request):
# # # #         if request.user.is_authenticated:
# # # #             return redirect('home')
# # # #         form = RegisterForm()
# # # #         return render(request, self.template_name, {'form': form})
# # # #
# # # #     def post(self, request):
# # # #         form = RegisterForm(request.POST)
# # # #         if form.is_valid():
# # # #             user = form.save()
# # # #             login(request, user)
# # # #             return redirect('home')
# # # #         return render(request, self.template_name, {'form': form})
# # # #
# # # #
# # # # class LogoutView(View):
# # # #     def get(self, request):
# # # #         logout(request)
# # # #         return redirect('login')
# # # #
# # # #
# # # # class AddFoodItemView(LoginRequiredMixin, View):
# # # #     login_url = '/login/'
# # # #     template_name = 'foodcomposition/addNewFoodItem.html'
# # # #
# # # #     def get(self, request):
# # # #         food_form = FoodItemForm()
# # # #         nutrition_form = NutritionInfoForm()
# # # #         recipe_form = RecipeForm()
# # # #         return render(request, self.template_name, {
# # # #             'food_form': food_form,
# # # #             'nutrition_form': nutrition_form,
# # # #             'recipe_form': recipe_form,
# # # #         })
# # # #
# # # #     def post(self, request):
# # # #         food_form = FoodItemForm(request.POST)
# # # #         nutrition_form = NutritionInfoForm(request.POST)
# # # #         recipe_form = RecipeForm(request.POST)
# # # #
# # # #         if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
# # # #             food_item = food_form.save()
# # # #
# # # #             nutrition = nutrition_form.save(commit=False)
# # # #             nutrition.FoodItem = food_item
# # # #             nutrition.save()
# # # #
# # # #             recipe = recipe_form.save(commit=False)
# # # #             recipe.FoodItem = food_item
# # # #             recipe.save()
# # # #             recipe_form.save_m2m()
# # # #
# # # #             return redirect('home')
# # # #
# # # #         return render(request, self.template_name, {
# # # #             'food_form': food_form,
# # # #             'nutrition_form': nutrition_form,
# # # #             'recipe_form': recipe_form,
# # # #         })
# # # #
# # # #
# # # # class EditProfileView(LoginRequiredMixin, View):
# # # #     login_url = '/login/'
# # # #     template_name = 'foodcomposition/editProfile.html'
# # # #
# # # #     def get(self, request):
# # # #         return render(request, self.template_name, {'user': request.user})
# # # #
# # # #     def post(self, request):
# # # #         user = request.user
# # # #         user.username = request.POST.get('username')
# # # #         user.email = request.POST.get('email')
# # # #         user.save()
# # # #         return redirect('home')
# # #
# # # from django.contrib.auth import authenticate, login, logout
# # # from django.contrib.auth.mixins import LoginRequiredMixin
# # # from django.shortcuts import render, redirect
# # # from django.views import View
# # # from .forms import FoodItemForm, NutritionInfoForm, RecipeForm, RegisterForm
# # # from .models import FoodItem
# # #
# # #
# # # class HomePageView(View):
# # #     template_name = 'foodcomposition/index.html'
# # #
# # #     def get(self, request):
# # #         food_items = FoodItem.objects.all() if request.user.is_authenticated else []
# # #         return render(request, self.template_name, {
# # #             'user': request.user,
# # #             'food_items': food_items,
# # #         })
# # #
# # #
# # # class LoginView(View):
# # #     template_name = 'foodcomposition/login.html'
# # #
# # #     def get(self, request):
# # #         if request.user.is_authenticated:
# # #             return redirect('home')
# # #         return render(request, self.template_name)
# # #
# # #     def post(self, request):
# # #         username = request.POST['username']
# # #         password = request.POST['password']
# # #         user = authenticate(request, username=username, password=password)
# # #         if user is not None:
# # #             login(request, user)
# # #             return redirect('home')
# # #         return render(request, self.template_name, {'error': 'Invalid credentials'})
# # #
# # #
# # # class RegisterView(View):
# # #     template_name = 'foodcomposition/register.html'
# # #
# # #     def get(self, request):
# # #         if request.user.is_authenticated:
# # #             return redirect('home')
# # #         form = RegisterForm()
# # #         return render(request, self.template_name, {'form': form})
# # #
# # #     def post(self, request):
# # #         form = RegisterForm(request.POST)
# # #         if form.is_valid():
# # #             user = form.save()
# # #             login(request, user)
# # #             return redirect('home')
# # #         return render(request, self.template_name, {'form': form})
# # #
# # #
# # # class LogoutView(View):
# # #     def get(self, request):
# # #         logout(request)
# # #         return redirect('login')
# # #
# # #
# # # class AddFoodItemView(LoginRequiredMixin, View):
# # #     login_url = '/login/'
# # #     template_name = 'foodcomposition/addNewFoodItem.html'
# # #
# # #     def get(self, request):
# # #         food_form = FoodItemForm()
# # #         nutrition_form = NutritionInfoForm()
# # #         recipe_form = RecipeForm()
# # #         return render(request, self.template_name, {
# # #             'food_form': food_form,
# # #             'nutrition_form': nutrition_form,
# # #             'recipe_form': recipe_form,
# # #         })
# # #
# # #     def post(self, request):
# # #         food_form = FoodItemForm(request.POST)
# # #         nutrition_form = NutritionInfoForm(request.POST)
# # #         recipe_form = RecipeForm(request.POST)
# # #
# # #         if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
# # #             food_item = food_form.save()
# # #
# # #             nutrition = nutrition_form.save(commit=False)
# # #             nutrition.FoodItem = food_item
# # #             nutrition.save()
# # #
# # #             recipe = recipe_form.save(commit=False)
# # #             recipe.FoodItem = food_item
# # #             recipe.save()
# # #             recipe_form.save_m2m()
# # #
# # #             return redirect('home')
# # #
# # #         return render(request, self.template_name, {
# # #             'food_form': food_form,
# # #             'nutrition_form': nutrition_form,
# # #             'recipe_form': recipe_form,
# # #         })
# # #
# # #
# # # class EditProfileView(LoginRequiredMixin, View):
# # #     login_url = '/login/'
# # #     template_name = 'foodcomposition/editProfile.html'
# # #
# # #     def get(self, request):
# # #         return render(request, self.template_name, {'user': request.user})
# # #
# # #     def post(self, request):
# # #         user = request.user
# # #         user.username = request.POST.get('username')
# # #         user.email = request.POST.get('email')
# # #         user.save()
# # #         return redirect('home')
# #
# # from django.contrib.auth import authenticate, login, logout
# # from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.shortcuts import render, redirect, get_object_or_404
# # from django.views import View
# # from .forms import FoodItemForm, NutritionInfoForm, RecipeForm, StudentRegisterForm, AdminRegisterForm, VendorRegisterForm
# # from .models import FoodItem, NutritionInfo, Recipe, CATEGORY_CHOICES
# #
# #
# # class HomePageView(View):
# #     template_name = 'foodcomposition/index.html'
# #
# #     def get(self, request):
# #         return render(request, self.template_name, {'user': request.user})
# #
# #
# # class LoginView(View):
# #     template_name = 'foodcomposition/login.html'
# #
# #     def get(self, request):
# #         if request.user.is_authenticated:
# #             return redirect('home')
# #         return render(request, self.template_name)
# #
# #     def post(self, request):
# #         username = request.POST['username']
# #         password = request.POST['password']
# #         user = authenticate(request, username=username, password=password)
# #         if user is not None:
# #             login(request, user)
# #             return redirect('home')
# #         return render(request, self.template_name, {'error': 'Invalid username or password.'})
# #
# #
# # class RegisterView(View):
# #     template_name = 'foodcomposition/register.html'
# #
# #     def get(self, request):
# #         if request.user.is_authenticated:
# #             return redirect('home')
# #         role = request.GET.get('role', '')
# #         form = self._get_form(role)
# #         return render(request, self.template_name, {'form': form, 'role': role})
# #
# #     def post(self, request):
# #         role = request.POST.get('role', '')
# #         form = self._get_form(role, request.POST)
# #         if form.is_valid():
# #             user = form.save()
# #             login(request, user)
# #             return redirect('home')
# #         return render(request, self.template_name, {'form': form, 'role': role})
# #
# #     def _get_form(self, role, data=None):
# #         if role == 'admin':
# #             return AdminRegisterForm(data) if data else AdminRegisterForm()
# #         elif role == 'vendor':
# #             return VendorRegisterForm(data) if data else VendorRegisterForm()
# #         else:
# #             return StudentRegisterForm(data) if data else StudentRegisterForm()
# #
# #
# # class LogoutView(View):
# #     def get(self, request):
# #         logout(request)
# #         return redirect('login')
# #
# #
# # class FoodListView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #     template_name = 'foodcomposition/foodList.html'
# #
# #     def get(self, request):
# #         foods = FoodItem.objects.all()
# #         query = request.GET.get('q', '')
# #         category = request.GET.get('category', '')
# #         sort = request.GET.get('sort', '')
# #
# #         if query:
# #             foods = foods.filter(Name__icontains=query)
# #         if category:
# #             foods = foods.filter(Category=category)
# #         if sort == 'az':
# #             foods = foods.order_by('Name')
# #         elif sort == 'za':
# #             foods = foods.order_by('-Name')
# #         elif sort == 'low':
# #             foods = foods.order_by('Price')
# #         elif sort == 'high':
# #             foods = foods.order_by('-Price')
# #
# #         return render(request, self.template_name, {
# #             'foods': foods,
# #             'query': query,
# #             'category': category,
# #             'sort': sort,
# #             'categories': CATEGORY_CHOICES,
# #             'user': request.user,
# #         })
# #
# #
# # class FoodDetailView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #
# #     def get(self, request, pk):
# #         food = get_object_or_404(FoodItem, pk=pk)
# #         nutrition = getattr(food, 'nutritioninfo', None)
# #         recipe = getattr(food, 'recipe', None)
# #         allergens = []
# #         if recipe:
# #             allergens = [i for i in recipe.Ingredients.all() if i.IsAllergen]
# #
# #         if request.user.role == 'vendor':
# #             template = 'foodcomposition/foodDetailVendor.html'
# #         else:
# #             template = 'foodcomposition/foodDetailStudent.html'
# #
# #         return render(request, template, {
# #             'food': food,
# #             'nutrition': nutrition,
# #             'recipe': recipe,
# #             'allergens': allergens,
# #         })
# #
# #
# # class AddFoodItemView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #     template_name = 'foodcomposition/addNewFoodItem.html'
# #
# #     def get(self, request):
# #         if request.user.role not in ['vendor', 'admin']:
# #             return redirect('food-list')
# #         return render(request, self.template_name, {
# #             'food_form': FoodItemForm(),
# #             'nutrition_form': NutritionInfoForm(),
# #             'recipe_form': RecipeForm(),
# #         })
# #
# #     def post(self, request):
# #         if request.user.role not in ['vendor', 'admin']:
# #             return redirect('food-list')
# #         food_form = FoodItemForm(request.POST)
# #         nutrition_form = NutritionInfoForm(request.POST)
# #         recipe_form = RecipeForm(request.POST)
# #
# #         if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
# #             food_item = food_form.save()
# #             nutrition = nutrition_form.save(commit=False)
# #             nutrition.FoodItem = food_item
# #             nutrition.save()
# #             recipe = recipe_form.save(commit=False)
# #             recipe.FoodItem = food_item
# #             recipe.save()
# #             recipe_form.save_m2m()
# #             return redirect('food-list')
# #
# #         return render(request, self.template_name, {
# #             'food_form': food_form,
# #             'nutrition_form': nutrition_form,
# #             'recipe_form': recipe_form,
# #         })
# #
# #
# # class EditFoodItemView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #     template_name = 'foodcomposition/editFoodItem.html'
# #
# #     def get(self, request, pk):
# #         if request.user.role != 'vendor':
# #             return redirect('food-list')
# #         food = get_object_or_404(FoodItem, pk=pk)
# #         form = FoodItemForm(instance=food)
# #         return render(request, self.template_name, {'form': form, 'food': food})
# #
# #     def post(self, request, pk):
# #         if request.user.role != 'vendor':
# #             return redirect('food-list')
# #         food = get_object_or_404(FoodItem, pk=pk)
# #         form = FoodItemForm(request.POST, instance=food)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('food-detail', pk=pk)
# #         return render(request, self.template_name, {'form': form, 'food': food})
# #
# #
# # class EditProfileView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #     template_name = 'foodcomposition/editProfile.html'
# #
# #     def get(self, request):
# #         return render(request, self.template_name, {'user': request.user})
# #
# #     def post(self, request):
# #         user = request.user
# #         user.username = request.POST.get('username')
# #         user.email = request.POST.get('email')
# #         user.Fname = request.POST.get('Fname')
# #         user.Lname = request.POST.get('Lname')
# #         user.save()
# #         return redirect('home')
#
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from .forms import FoodItemForm, NutritionInfoForm, RecipeForm, StudentRegisterForm, AdminRegisterForm, VendorRegisterForm, CafeteriaForm
# from .models import FoodItem, NutritionInfo, Recipe, CATEGORY_CHOICES, Cafeteria
#
#
# class HomePageView(View):
#     template_name = 'foodcomposition/index.html'
#
#     def get(self, request):
#         return render(request, self.template_name, {'user': request.user})
#
#
# class LoginView(View):
#     template_name = 'foodcomposition/login.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         return render(request, self.template_name)
#
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         return render(request, self.template_name, {'error': 'Invalid username or password.'})
#
#
# class RegisterView(View):
#     template_name = 'foodcomposition/register.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         role = request.GET.get('role', '')
#         form = self._get_form(role)
#         return render(request, self.template_name, {'form': form, 'role': role})
#
#     def post(self, request):
#         role = request.POST.get('role', '')
#         form = self._get_form(role, request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#         return render(request, self.template_name, {'form': form, 'role': role})
#
#     def _get_form(self, role, data=None):
#         if role == 'admin':
#             return AdminRegisterForm(data) if data else AdminRegisterForm()
#         elif role == 'vendor':
#             return VendorRegisterForm(data) if data else VendorRegisterForm()
#         else:
#             return StudentRegisterForm(data) if data else StudentRegisterForm()
#
#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('login')
#
#
# class FoodListView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/foodList.html'
#
#     def get(self, request):
#         foods = FoodItem.objects.all()
#         query = request.GET.get('q', '')
#         category = request.GET.get('category', '')
#         sort = request.GET.get('sort', '')
#
#         if query:
#             foods = foods.filter(Name__icontains=query)
#         if category:
#             foods = foods.filter(Category=category)
#         if sort == 'az':
#             foods = foods.order_by('Name')
#         elif sort == 'za':
#             foods = foods.order_by('-Name')
#         elif sort == 'low':
#             foods = foods.order_by('Price')
#         elif sort == 'high':
#             foods = foods.order_by('-Price')
#
#         return render(request, self.template_name, {
#             'foods': foods,
#             'query': query,
#             'category': category,
#             'sort': sort,
#             'categories': CATEGORY_CHOICES,
#             'user': request.user,
#         })
#
#
# class FoodDetailView(LoginRequiredMixin, View):
#     login_url = '/login/'
#
#     def get(self, request, pk):
#         food = get_object_or_404(FoodItem, pk=pk)
#         nutrition = getattr(food, 'nutritioninfo', None)
#         recipe = getattr(food, 'recipe', None)
#         allergens = []
#         if recipe:
#             allergens = [i for i in recipe.Ingredients.all() if i.IsAllergen]
#
#         if request.user.role == 'vendor':
#             template = 'foodcomposition/foodDetailVendor.html'
#         else:
#             template = 'foodcomposition/foodDetailStudent.html'
#
#         return render(request, template, {
#             'food': food,
#             'nutrition': nutrition,
#             'recipe': recipe,
#             'allergens': allergens,
#         })
#
#
# class AddFoodItemView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/addNewFoodItem.html'
#
#     def get(self, request):
#         if request.user.role not in ['vendor', 'admin']:
#             return redirect('food-list')
#         return render(request, self.template_name, {
#             'food_form': FoodItemForm(),
#             'nutrition_form': NutritionInfoForm(),
#             'recipe_form': RecipeForm(),
#             'cafeteria_form': CafeteriaForm(),
#         })
#
#     def post(self, request):
#         if request.user.role not in ['vendor', 'admin']:
#             return redirect('food-list')
#
#         # Handle new cafeteria creation
#         if request.POST.get('new_cafeteria_name'):
#             Cafeteria.objects.get_or_create(Name=request.POST.get('new_cafeteria_name'))
#
#         food_form = FoodItemForm(request.POST)
#         nutrition_form = NutritionInfoForm(request.POST)
#         recipe_form = RecipeForm(request.POST)
# #
# #         if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
# #             food_item = food_form.save()
# #
# #             nutrition = nutrition_form.save(commit=False)
# #             nutrition.FoodItem = food_item
# #             nutrition.save()
# #
# #             recipe_form.save_with_ingredients(food_item)
# #
# #             return redirect('food-list')
# #
# #         return render(request, self.template_name, {
# #             'food_form': food_form,
# #             'nutrition_form': nutrition_form,
# #             'recipe_form': recipe_form,
# #             'cafeteria_form': CafeteriaForm(),
# #         })
# #
# #
# # class EditFoodItemView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #     template_name = 'foodcomposition/editFoodItem.html'
# #
# #     def get(self, request, pk):
# #         if request.user.role != 'vendor':
# #             return redirect('food-list')
# #         food = get_object_or_404(FoodItem, pk=pk)
# #         form = FoodItemForm(instance=food)
# #         return render(request, self.template_name, {'form': form, 'food': food})
# #
# #     def post(self, request, pk):
# #         if request.user.role != 'vendor':
# #             return redirect('food-list')
# #         food = get_object_or_404(FoodItem, pk=pk)
# #         form = FoodItemForm(request.POST, instance=food)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('food-detail', pk=pk)
# #         return render(request, self.template_name, {'form': form, 'food': food})
# #
# #
# # class EditProfileView(LoginRequiredMixin, View):
# #     login_url = '/login/'
# #     template_name = 'foodcomposition/editProfile.html'
# #
# #     def get(self, request):
# #         return render(request, self.template_name, {'user': request.user})
# #
# #     def post(self, request):
# #         user = request.user
# #         user.username = request.POST.get('username')
# #         user.email = request.POST.get('email')
# #         user.Fname = request.POST.get('Fname')
# #         user.Lname = request.POST.get('Lname')
# #         user.save()
# #         return redirect('home')
#
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from .forms import (FoodItemForm, NutritionInfoForm, RecipeForm,
#                     StudentRegisterForm, AdminRegisterForm, VendorRegisterForm,
#                     CafeteriaForm, IngredientForm)
# from .models import FoodItem, NutritionInfo, Recipe, CATEGORY_CHOICES, Cafeteria, Ingredient
#
#
# class HomePageView(View):
#     template_name = 'foodcomposition/index.html'
#
#     def get(self, request):
#         return render(request, self.template_name, {'user': request.user})
#
#
# class LoginView(View):
#     template_name = 'foodcomposition/login.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         return render(request, self.template_name)
#
#     def post(self, request):
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         return render(request, self.template_name, {'error': 'Invalid username or password.'})
#
#
# class RegisterView(View):
#     template_name = 'foodcomposition/register.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         role = request.GET.get('role', '')
#         form = self._get_form(role)
#         return render(request, self.template_name, {'form': form, 'role': role})
#
#     def post(self, request):
#         role = request.POST.get('role', '')
#         form = self._get_form(role, request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')
#         return render(request, self.template_name, {'form': form, 'role': role})
#
#     def _get_form(self, role, data=None):
#         if role == 'admin':
#             return AdminRegisterForm(data) if data else AdminRegisterForm()
#         elif role == 'vendor':
#             return VendorRegisterForm(data) if data else VendorRegisterForm()
#         else:
#             return StudentRegisterForm(data) if data else StudentRegisterForm()
#
#
# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('login')
#
#
# class FoodListView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/foodList.html'
#
#     def get(self, request):
#         foods = FoodItem.objects.all()
#         query = request.GET.get('q', '')
#         category = request.GET.get('category', '')
#         sort = request.GET.get('sort', '')
#
#         if query:
#             foods = foods.filter(Name__icontains=query)
#         if category:
#             foods = foods.filter(Category=category)
#         if sort == 'az':
#             foods = foods.order_by('Name')
#         elif sort == 'za':
#             foods = foods.order_by('-Name')
#         elif sort == 'low':
#             foods = foods.order_by('Price')
#         elif sort == 'high':
#             foods = foods.order_by('-Price')
#
#         return render(request, self.template_name, {
#             'foods': foods,
#             'query': query,
#             'category': category,
#             'sort': sort,
#             'categories': CATEGORY_CHOICES,
#             'user': request.user,
#         })
#
#
# class FoodDetailView(LoginRequiredMixin, View):
#     login_url = '/login/'
#
#     def get(self, request, pk):
#         food = get_object_or_404(FoodItem, pk=pk)
#         nutrition = getattr(food, 'nutritioninfo', None)
#         recipe = getattr(food, 'recipe', None)
#         allergens = []
#         if recipe:
#             allergens = [i for i in recipe.Ingredients.all() if i.IsAllergen]
#         if request.user.role == 'vendor':
#             template = 'foodcomposition/foodDetailVendor.html'
#         else:
#             template = 'foodcomposition/foodDetailStudent.html'
#         return render(request, template, {
#             'food': food,
#             'nutrition': nutrition,
#             'recipe': recipe,
#             'allergens': allergens,
#         })
#
#
# class AddFoodItemView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/addNewFoodItem.html'
#
#     def get(self, request):
#         if request.user.role not in ['vendor', 'admin']:
#             return redirect('food-list')
#         return render(request, self.template_name, {
#             'food_form': FoodItemForm(),
#             'nutrition_form': NutritionInfoForm(),
#             'recipe_form': RecipeForm(),
#         })
#
#     def post(self, request):
#         if request.user.role not in ['vendor', 'admin']:
#             return redirect('food-list')
#
#         food_form = FoodItemForm(request.POST)
#         nutrition_form = NutritionInfoForm(request.POST)
#         recipe_form = RecipeForm(request.POST)
#
#         if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
#             food_item = food_form.save()
#             nutrition = nutrition_form.save(commit=False)
#             nutrition.FoodItem = food_item
#             nutrition.save()
#             recipe_form.save_with_ingredients(food_item)
#             return redirect('food-list')
#
#         return render(request, self.template_name, {
#             'food_form': food_form,
#             'nutrition_form': nutrition_form,
#             'recipe_form': recipe_form,
#         })
#
#
# class EditFoodItemView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/editFoodItem.html'
#
#     def get(self, request, pk):
#         if request.user.role != 'vendor':
#             return redirect('food-list')
#         food = get_object_or_404(FoodItem, pk=pk)
#         form = FoodItemForm(instance=food)
#         return render(request, self.template_name, {'form': form, 'food': food})
#
#     def post(self, request, pk):
#         if request.user.role != 'vendor':
#             return redirect('food-list')
#         food = get_object_or_404(FoodItem, pk=pk)
#         form = FoodItemForm(request.POST, instance=food)
#         if form.is_valid():
#             form.save()
#             return redirect('food-detail', pk=pk)
#         return render(request, self.template_name, {'form': form, 'food': food})
#
#
# class IngredientListView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/ingredientList.html'
#
#     def get(self, request):
#         ingredients = Ingredient.objects.all()
#         query = request.GET.get('q', '')
#         filter_allergen = request.GET.get('allergen', '')
#         sort = request.GET.get('sort', '')
#
#         if query:
#             ingredients = ingredients.filter(Name__icontains=query)
#         if filter_allergen == 'yes':
#             ingredients = ingredients.filter(IsAllergen=True)
#         elif filter_allergen == 'no':
#             ingredients = ingredients.filter(IsAllergen=False)
#         if sort == 'az':
#             ingredients = ingredients.order_by('Name')
#         elif sort == 'za':
#             ingredients = ingredients.order_by('-Name')
#
#         form = IngredientForm() if request.user.role in ['vendor', 'admin'] else None
#
#         return render(request, self.template_name, {
#             'ingredients': ingredients,
#             'query': query,
#             'filter_allergen': filter_allergen,
#             'sort': sort,
#             'form': form,
#             'user': request.user,
#         })
#
#     def post(self, request):
#         if request.user.role not in ['vendor', 'admin']:
#             return redirect('ingredient-list')
#         form = IngredientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('ingredient-list')
#         ingredients = Ingredient.objects.all()
#         return render(request, self.template_name, {
#             'ingredients': ingredients,
#             'form': form,
#             'user': request.user,
#             'show_modal': True,
#         })
#
#
# class CafeteriaListView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/cafeteriaList.html'
#
#     def get(self, request):
#         cafeterias = Cafeteria.objects.all()
#         query = request.GET.get('q', '')
#         sort = request.GET.get('sort', '')
#
#         if query:
#             cafeterias = cafeterias.filter(Name__icontains=query)
#         if sort == 'az':
#             cafeterias = cafeterias.order_by('Name')
#         elif sort == 'za':
#             cafeterias = cafeterias.order_by('-Name')
#
#         form = CafeteriaForm() if request.user.role in ['vendor', 'admin'] else None
#
#         return render(request, self.template_name, {
#             'cafeterias': cafeterias,
#             'query': query,
#             'sort': sort,
#             'form': form,
#             'user': request.user,
#         })
#
#     def post(self, request):
#         if request.user.role not in ['vendor', 'admin']:
#             return redirect('cafeteria-list')
#         form = CafeteriaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('cafeteria-list')
#         cafeterias = Cafeteria.objects.all()
#         return render(request, self.template_name, {
#             'cafeterias': cafeterias,
#             'form': form,
#             'user': request.user,
#             'show_modal': True,
#         })
#
#
# class EditProfileView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/editProfile.html'
#
#     def get(self, request):
#         return render(request, self.template_name, {'user': request.user})
#
#     def post(self, request):
#         user = request.user
#         user.username = request.POST.get('username')
#         user.email = request.POST.get('email')
#         user.Fname = request.POST.get('Fname')
#         user.Lname = request.POST.get('Lname')
#         user.save()
#         return redirect('home')

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (FoodItemForm, NutritionInfoForm, RecipeForm,
                    StudentRegisterForm, AdminRegisterForm, VendorRegisterForm,
                    CafeteriaForm, IngredientForm)
from .models import FoodItem, NutritionInfo, Recipe, CATEGORY_CHOICES, Cafeteria, Ingredient


class HomePageView(View):
    template_name = 'foodcomposition/index.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})


class LoginView(View):
    template_name = 'foodcomposition/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'error': 'Invalid username or password.'})


class RegisterView(View):
    template_name = 'foodcomposition/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        role = request.GET.get('role', '')
        form = self._get_form(role)
        return render(request, self.template_name, {'form': form, 'role': role})

    def post(self, request):
        role = request.POST.get('role', '')
        form = self._get_form(role, request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form, 'role': role})

    def _get_form(self, role, data=None):
        if role == 'admin':
            return AdminRegisterForm(data) if data else AdminRegisterForm()
        elif role == 'vendor':
            return VendorRegisterForm(data) if data else VendorRegisterForm()
        else:
            return StudentRegisterForm(data) if data else StudentRegisterForm()


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class FoodListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/foodList.html'

    def get(self, request):
        foods = FoodItem.objects.all()
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        sort = request.GET.get('sort', '')

        if query:
            foods = foods.filter(Name__icontains=query)
        if category:
            foods = foods.filter(Category=category)
        if sort == 'az':
            foods = foods.order_by('Name')
        elif sort == 'za':
            foods = foods.order_by('-Name')
        elif sort == 'low':
            foods = foods.order_by('Price')
        elif sort == 'high':
            foods = foods.order_by('-Price')

        return render(request, self.template_name, {
            'foods': foods,
            'query': query,
            'category': category,
            'sort': sort,
            'categories': CATEGORY_CHOICES,
            'user': request.user,
        })


class FoodDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        food = get_object_or_404(FoodItem, pk=pk)
        nutrition = getattr(food, 'nutritioninfo', None)
        recipe = getattr(food, 'recipe', None)
        allergens = []
        if recipe:
            allergens = [i for i in recipe.Ingredients.all() if i.IsAllergen]
        if request.user.role == 'vendor':
            template = 'foodcomposition/foodDetailVendor.html'
        else:
            template = 'foodcomposition/foodDetailStudent.html'
        return render(request, template, {
            'food': food,
            'nutrition': nutrition,
            'recipe': recipe,
            'allergens': allergens,
        })

class CafeteriaDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/cafeteriaDetail.html'

    def get(self, request, pk):
        cafeteria = get_object_or_404(Cafeteria, pk=pk)
        foods = FoodItem.objects.filter(Cafeteria=cafeteria)
        return render(request, self.template_name, {
            'cafeteria': cafeteria,
            'foods': foods,
            'user': request.user,
        })


class IngredientDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/ingredientDetail.html'

    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        return render(request, self.template_name, {
            'ingredient': ingredient,
            'user': request.user,
        })

class AddFoodItemView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/addNewFoodItem.html'

    def get(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('food-list')
        return render(request, self.template_name, {
            'food_form': FoodItemForm(),
            'nutrition_form': NutritionInfoForm(),
            'recipe_form': RecipeForm(),
            'ingredients': Ingredient.objects.all().order_by('Name'),
            'cafeterias': Cafeteria.objects.all().order_by('Name'),
        })

    def post(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('food-list')

        food_form = FoodItemForm(request.POST)
        nutrition_form = NutritionInfoForm(request.POST)
        recipe_form = RecipeForm(request.POST)

        if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
            food_item = food_form.save()
            nutrition = nutrition_form.save(commit=False)
            nutrition.FoodItem = food_item
            nutrition.save()
            selected_ids = request.POST.getlist('ingredients')
            recipe_form.save_with_ingredients(food_item, selected_ids)
            return redirect('food-list')

        return render(request, self.template_name, {
            'food_form': food_form,
            'nutrition_form': nutrition_form,
            'recipe_form': recipe_form,
            'ingredients': Ingredient.objects.all().order_by('Name'),
            'cafeterias': Cafeteria.objects.all().order_by('Name'),
        })


# class EditFoodItemView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     template_name = 'foodcomposition/editFoodItem.html'
#
#     def get(self, request, pk):
#         if request.user.role != 'vendor':
#             return redirect('food-list')
#         food = get_object_or_404(FoodItem, pk=pk)
#         form = FoodItemForm(instance=food)
#         return render(request, self.template_name, {'form': form, 'food': food})
#
#     def post(self, request, pk):
#         if request.user.role != 'vendor':
#             return redirect('food-list')
#         food = get_object_or_404(FoodItem, pk=pk)
#         form = FoodItemForm(request.POST, instance=food)
#         if form.is_valid():
#             form.save()
#             return redirect('food-detail', pk=pk)
#         return render(request, self.template_name, {'form': form, 'food': food})

class EditFoodItemView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/editFoodItem.html'

    def get(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('food-list')
        food = get_object_or_404(FoodItem, pk=pk)
        food_form = FoodItemForm(instance=food)
        nutrition = getattr(food, 'nutritioninfo', None)
        recipe = getattr(food, 'recipe', None)
        nutrition_form = NutritionInfoForm(instance=nutrition) if nutrition else NutritionInfoForm()
        recipe_form = RecipeForm(instance=recipe) if recipe else RecipeForm()
        return render(request, self.template_name, {
            'form': food_form,
            'nutrition_form': nutrition_form,
            'recipe_form': recipe_form,
            'food': food,
            'ingredients': Ingredient.objects.all().order_by('Name'),
            'selected_ingredients': list(recipe.Ingredients.values_list('pk', flat=True)) if recipe else [],
        })

    def post(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('food-list')
        food = get_object_or_404(FoodItem, pk=pk)
        nutrition = getattr(food, 'nutritioninfo', None)
        recipe = getattr(food, 'recipe', None)

        food_form = FoodItemForm(request.POST, instance=food)
        nutrition_form = NutritionInfoForm(request.POST, instance=nutrition)
        recipe_form = RecipeForm(request.POST, instance=recipe)

        if food_form.is_valid() and nutrition_form.is_valid() and recipe_form.is_valid():
            food_form.save()

            nutrition_obj = nutrition_form.save(commit=False)
            nutrition_obj.FoodItem = food
            nutrition_obj.save()

            recipe_obj = recipe_form.save(commit=False)
            recipe_obj.FoodItem = food
            recipe_obj.save()

            selected_ids = request.POST.getlist('ingredients')
            recipe_obj.Ingredients.clear()
            for ing_id in selected_ids:
                try:
                    obj = Ingredient.objects.get(pk=ing_id)
                    recipe_obj.Ingredients.add(obj)
                except Ingredient.DoesNotExist:
                    pass

            return redirect('food-detail', pk=pk)

        return render(request, self.template_name, {
            'form': food_form,
            'nutrition_form': nutrition_form,
            'recipe_form': recipe_form,
            'food': food,
            'ingredients': Ingredient.objects.all().order_by('Name'),
            'selected_ingredients': list(recipe.Ingredients.values_list('pk', flat=True)) if recipe else [],
        })

class AddIngredientView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/addIngredient.html'

    def get(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('ingredient-list')
        return render(request, self.template_name, {
            'form': IngredientForm(),
        })

    def post(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('ingredient-list')
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient-list')
        return render(request, self.template_name, {'form': form})


class AddCafeteriaView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/addCafeteria.html'

    def get(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('cafeteria-list')
        return render(request, self.template_name, {
            'form': CafeteriaForm(),
        })

    def post(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('cafeteria-list')
        form = CafeteriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cafeteria-list')
        return render(request, self.template_name, {'form': form})


class IngredientListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/ingredientList.html'

    def get(self, request):
        ingredients = Ingredient.objects.all()
        query = request.GET.get('q', '')
        filter_allergen = request.GET.get('allergen', '')
        sort = request.GET.get('sort', '')

        if query:
            ingredients = ingredients.filter(Name__icontains=query)
        if filter_allergen == 'yes':
            ingredients = ingredients.filter(IsAllergen=True)
        elif filter_allergen == 'no':
            ingredients = ingredients.filter(IsAllergen=False)
        if sort == 'az':
            ingredients = ingredients.order_by('Name')
        elif sort == 'za':
            ingredients = ingredients.order_by('-Name')

        return render(request, self.template_name, {
            'ingredients': ingredients,
            'query': query,
            'filter_allergen': filter_allergen,
            'sort': sort,
            'user': request.user,
        })


class CafeteriaListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/cafeteriaList.html'

    def get(self, request):
        cafeterias = Cafeteria.objects.all()
        query = request.GET.get('q', '')
        sort = request.GET.get('sort', '')

        if query:
            cafeterias = cafeterias.filter(Name__icontains=query)
        if sort == 'az':
            cafeterias = cafeterias.order_by('Name')
        elif sort == 'za':
            cafeterias = cafeterias.order_by('-Name')

        return render(request, self.template_name, {
            'cafeterias': cafeterias,
            'query': query,
            'sort': sort,
            'user': request.user,
        })


class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/editProfile.html'

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

    def post(self, request):
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.Fname = request.POST.get('Fname')
        user.Lname = request.POST.get('Lname')
        user.save()
        return redirect('home')

class EditCafeteriaView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/editCafeteria.html'

    def get(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('cafeteria-list')
        cafeteria = get_object_or_404(Cafeteria, pk=pk)
        form = CafeteriaForm(instance=cafeteria)
        return render(request, self.template_name, {'form': form, 'cafeteria': cafeteria})

    def post(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('cafeteria-list')
        cafeteria = get_object_or_404(Cafeteria, pk=pk)
        form = CafeteriaForm(request.POST, instance=cafeteria)
        if form.is_valid():
            form.save()
            return redirect('cafeteria-list')
        return render(request, self.template_name, {'form': form, 'cafeteria': cafeteria})


class EditIngredientView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/editIngredient.html'

    def get(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('ingredient-list')
        ingredient = get_object_or_404(Ingredient, pk=pk)
        form = IngredientForm(instance=ingredient)
        return render(request, self.template_name, {'form': form, 'ingredient': ingredient})

    def post(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('ingredient-list')
        ingredient = get_object_or_404(Ingredient, pk=pk)
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient-list')
        return render(request, self.template_name, {'form': form, 'ingredient': ingredient})