from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import (FoodItemForm, NutritionInfoForm, RecipeForm,
                    StudentRegisterForm, AdminRegisterForm, VendorRegisterForm,
                    CafeteriaForm, IngredientForm, DiscountForm)
from .models import CustomUser, FoodItem, Ingredient, Cafeteria, Recipe, NutritionInfo
from .models import FoodItem, NutritionInfo, Recipe, CATEGORY_CHOICES, Cafeteria, Ingredient, Discount


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
        foods = list(FoodItem.objects.all())
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        sort = request.GET.get('sort', '')

        if query:
            foods = [f for f in foods if query.lower() in f.Name.lower()]
        if category:
            foods = [f for f in foods if f.Category == category]

        def effective_price(food):
            dp = food.discounted_price()
            return float(dp) if dp is not None else float(food.Price)

        if sort == 'az':
            foods.sort(key=lambda f: f.Name.lower())
        elif sort == 'za':
            foods.sort(key=lambda f: f.Name.lower(), reverse=True)
        elif sort == 'low':
            foods.sort(key=effective_price)
        elif sort == 'high':
            foods.sort(key=effective_price, reverse=True)

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
        elif request.user.role == 'admin':
            template = 'foodcomposition/foodDetailAdmin.html'
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
        if request.user.role == 'vendor':
            template = 'foodcomposition/cafeteriaDetail.html'
        elif request.user.role == 'admin':
            template = 'foodcomposition/cafeteriaDetailAdmin.html'
        else:
            template = 'foodcomposition/cafeteriaDetailStudent.html'
        return render(request, template, {
            'cafeteria': cafeteria,
            'foods': foods,
            'user': request.user,
        })


class IngredientDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk)
        if request.user.role == 'vendor':
            template = 'foodcomposition/ingredientDetail.html'
        elif request.user.role == 'admin':
            template = 'foodcomposition/ingredientDetailAdmin.html'
        else:
            template = 'foodcomposition/ingredientDetailStudent.html'
        return render(request, template, {
            'ingredient': ingredient,
            'user': request.user,
        })

class DiscountDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/discountDetail.html'

    def get(self, request, pk):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('home')
        discount = get_object_or_404(Discount, pk=pk)
        food_items = FoodItem.objects.filter(Discount=discount)
        return render(request, self.template_name, {
            'discount': discount,
            'food_items': food_items,
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
            'discounts': Discount.objects.all().order_by('Name'),
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
            'discounts': Discount.objects.all().order_by('Name'),
        })

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
        return render(request, self.template_name, {
            'form': form,
            'cafeteria': cafeteria,
            'discounts': Discount.objects.all().order_by('Name'),
        })

    def post(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('cafeteria-list')
        cafeteria = get_object_or_404(Cafeteria, pk=pk)
        form = CafeteriaForm(request.POST, instance=cafeteria)
        if form.is_valid():
            form.save()
            return redirect('cafeteria-detail', pk=pk)
        return render(request, self.template_name, {
            'form': form,
            'cafeteria': cafeteria,
            'discounts': Discount.objects.all().order_by('Name'),
        })

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

class AdminDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/adminDashboard.html'

    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')

        total_users = CustomUser.objects.count()
        total_students = CustomUser.objects.filter(role='student').count()
        total_vendors = CustomUser.objects.filter(role='vendor').count()
        total_admins = CustomUser.objects.filter(role='admin').count()
        active_users = CustomUser.objects.filter(status='active').count()
        total_foods = FoodItem.objects.count()
        total_ingredients = Ingredient.objects.count()
        total_allergens = Ingredient.objects.filter(IsAllergen=True).count()
        total_cafeterias = Cafeteria.objects.count()
        total_recipes = Recipe.objects.count()
        total_nutrition = NutritionInfo.objects.count()
        total_discounts = Discount.objects.count()
        import datetime
        active_discounts = sum(1 for d in Discount.objects.all() if d.is_active())

        recent_foods = FoodItem.objects.all().order_by('-id')[:5]
        recent_users = CustomUser.objects.all().order_by('-date_joined')[:5]
        recent_ingredients = Ingredient.objects.all().order_by('-id')[:5]
        recent_discounts = Discount.objects.all().order_by('-id')[:5]

        category_counts = []
        for val, label in CATEGORY_CHOICES:
            count = FoodItem.objects.filter(Category=val).count()
            category_counts.append({'label': label, 'count': count})

        return render(request, self.template_name, {
            'total_users': total_users,
            'total_students': total_students,
            'total_vendors': total_vendors,
            'total_admins': total_admins,
            'active_users': active_users,
            'total_foods': total_foods,
            'total_ingredients': total_ingredients,
            'total_allergens': total_allergens,
            'total_cafeterias': total_cafeterias,
            'total_recipes': total_recipes,
            'total_nutrition': total_nutrition,
            'total_discounts': total_discounts,
            'active_discounts': active_discounts,
            'recent_foods': recent_foods,
            'recent_users': recent_users,
            'recent_ingredients': recent_ingredients,
            'recent_discounts': recent_discounts,
            'category_counts': category_counts,
        })


class AdminUserListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/adminUserList.html'

    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')
        role_filter = request.GET.get('role', '')
        status_filter = request.GET.get('status', '')
        query = request.GET.get('q', '')
        users = CustomUser.objects.all().order_by('-date_joined')
        if role_filter:
            users = users.filter(role=role_filter)
        if status_filter:
            users = users.filter(status=status_filter)
        if query:
            users = users.filter(username__icontains=query)
        return render(request, self.template_name, {
            'users': users,
            'role_filter': role_filter,
            'status_filter': status_filter,
            'query': query,
        })


class AdminFoodListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/adminFoodList.html'

    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        foods = FoodItem.objects.all().order_by('-id')
        if query:
            foods = foods.filter(Name__icontains=query)
        if category:
            foods = foods.filter(Category=category)
        from .models import CATEGORY_CHOICES
        return render(request, self.template_name, {
            'foods': foods,
            'query': query,
            'category': category,
            'categories': CATEGORY_CHOICES,
        })


class AdminIngredientListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/adminIngredientList.html'

    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')
        query = request.GET.get('q', '')
        allergen = request.GET.get('allergen', '')
        ingredients = Ingredient.objects.all().order_by('Name')
        if query:
            ingredients = ingredients.filter(Name__icontains=query)
        if allergen == 'yes':
            ingredients = ingredients.filter(IsAllergen=True)
        elif allergen == 'no':
            ingredients = ingredients.filter(IsAllergen=False)
        return render(request, self.template_name, {
            'ingredients': ingredients,
            'query': query,
            'allergen': allergen,
        })


class AdminCafeteriaListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/adminCafeteriaList.html'

    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')
        query = request.GET.get('q', '')
        cafeterias = Cafeteria.objects.all().order_by('Name')
        if query:
            cafeterias = cafeterias.filter(Name__icontains=query)
        return render(request, self.template_name, {
            'cafeterias': cafeterias,
            'query': query,
        })

class DiscountListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/discountList.html'

    def get(self, request):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('home')
        discounts = Discount.objects.all().order_by('Name')
        query = request.GET.get('q', '')
        if query:
            discounts = discounts.filter(Name__icontains=query)
        return render(request, self.template_name, {
            'discounts': discounts,
            'query': query,
            'user': request.user,
        })


class AddDiscountView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/addDiscount.html'

    def get(self, request):
        if request.user.role != 'vendor':
            return redirect('home')
        return render(request, self.template_name, {'form': DiscountForm()})

    def post(self, request):
        if request.user.role != 'vendor':
            return redirect('home')
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('discount-list')
        return render(request, self.template_name, {'form': form})


class EditDiscountView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/editDiscount.html'

    def get(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('home')
        discount = get_object_or_404(Discount, pk=pk)
        form = DiscountForm(instance=discount)
        return render(request, self.template_name, {'form': form, 'discount': discount})

    def post(self, request, pk):
        if request.user.role != 'vendor':
            return redirect('home')
        discount = get_object_or_404(Discount, pk=pk)
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            return redirect('discount-list')
        return render(request, self.template_name, {'form': form, 'discount': discount})


class AdminDiscountListView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'foodcomposition/adminDiscountList.html'

    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')
        discounts = Discount.objects.all().order_by('Name')
        query = request.GET.get('q', '')
        if query:
            discounts = discounts.filter(Name__icontains=query)
        return render(request, self.template_name, {
            'discounts': discounts,
            'query': query,
        })

class DiscountDetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        if request.user.role not in ['vendor', 'admin']:
            return redirect('home')
        discount = get_object_or_404(Discount, pk=pk)
        food_items = FoodItem.objects.filter(Discount=discount)
        if request.user.role == 'vendor':
            template = 'foodcomposition/discountDetail.html'
        else:
            template = 'foodcomposition/discountDetailAdmin.html'
        return render(request, template, {
            'discount': discount,
            'food_items': food_items,
            'user': request.user,
        })