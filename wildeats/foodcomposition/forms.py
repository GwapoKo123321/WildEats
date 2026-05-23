# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser, AdminProfile, VendorProfile, FoodItem, NutritionInfo, Recipe, Ingredient, Cafeteria, CATEGORY_CHOICES
#
# ALLERGEN_KEYS = ['milk', 'eggs', 'wheat', 'soy', 'peanuts', 'tree nuts', 'fish', 'shellfish']
#
# COMMON_INGREDIENTS = [
#     'Milk', 'Eggs', 'Wheat', 'Soy', 'Peanuts', 'Tree Nuts', 'Fish', 'Shellfish',
#     'Garlic', 'Onion', 'Chicken', 'Beef', 'Pork', 'Rice', 'Flour',
#     'Sugar', 'Salt', 'Butter', 'Oil', 'Tomato',
# ]
#
#
# class StudentRegisterForm(UserCreationForm):
#     Fname = forms.CharField(max_length=100, label="First Name")
#     Lname = forms.CharField(max_length=100, label="Last Name")
#     email = forms.EmailField(required=True)
#
#     class Meta:
#         model = CustomUser
#         fields = ['Fname', 'Lname', 'username', 'email', 'password1', 'password2']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'student'
#         user.Fname = self.cleaned_data['Fname']
#         user.Lname = self.cleaned_data['Lname']
#         user.status = 'active'
#         if commit:
#             user.save()
#         return user
#
#
# class AdminRegisterForm(UserCreationForm):
#     Fname = forms.CharField(max_length=100, label="First Name")
#     Lname = forms.CharField(max_length=100, label="Last Name")
#     email = forms.EmailField(required=True)
#     AdminLevel = forms.CharField(max_length=50, label="Admin Level")
#     CafeteriaType = forms.ChoiceField(
#         choices=[('college', 'College'), ('highschool', 'High School')],
#         label="Cafeteria Type"
#     )
#
#     class Meta:
#         model = CustomUser
#         fields = ['Fname', 'Lname', 'username', 'email', 'password1', 'password2']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'admin'
#         user.Fname = self.cleaned_data['Fname']
#         user.Lname = self.cleaned_data['Lname']
#         user.status = 'active'
#         if commit:
#             user.save()
#             AdminProfile.objects.create(
#                 user=user,
#                 AdminLevel=self.cleaned_data['AdminLevel'],
#                 CafeteriaType=self.cleaned_data['CafeteriaType'],
#             )
#         return user
#
#
# class VendorRegisterForm(UserCreationForm):
#     Fname = forms.CharField(max_length=100, label="First Name")
#     Lname = forms.CharField(max_length=100, label="Last Name")
#     email = forms.EmailField(required=True)
#     ContactNumber = forms.CharField(max_length=20, label="Contact Number")
#     BusinessLicenseNumber = forms.CharField(max_length=100, label="Business License Number")
#
#     class Meta:
#         model = CustomUser
#         fields = ['Fname', 'Lname', 'username', 'email', 'password1', 'password2']
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'vendor'
#         user.Fname = self.cleaned_data['Fname']
#         user.Lname = self.cleaned_data['Lname']
#         user.status = 'active'
#         if commit:
#             user.save()
#             VendorProfile.objects.create(
#                 user=user,
#                 ContactNumber=self.cleaned_data['ContactNumber'],
#                 BusinessLicenseNumber=self.cleaned_data['BusinessLicenseNumber'],
#                 ContractStatus='pending',
#             )
#         return user
#
#
# class CafeteriaForm(forms.ModelForm):
#     class Meta:
#         model = Cafeteria
#         fields = ['Name', 'Location', 'OperatingHours', 'Capacity']
#         labels = {
#             'Name': 'Cafeteria Name',
#             'Location': 'Location',
#             'OperatingHours': 'Operating Hours',
#             'Capacity': 'Capacity',
#         }
#
#     def clean_Name(self):
#         name = self.cleaned_data.get('Name')
#         if Cafeteria.objects.filter(Name__iexact=name).exists():
#             raise forms.ValidationError("This cafeteria already exists.")
#         return name
#
#     def clean_Capacity(self):
#         capacity = self.cleaned_data.get('Capacity')
#         if capacity is not None and capacity <= 0:
#             raise forms.ValidationError("Capacity must be greater than zero.")
#         return capacity
#
#
# class FoodItemForm(forms.ModelForm):
#     class Meta:
#         model = FoodItem
#         fields = ['Name', 'Price', 'PortionSize', 'Category', 'Cafeteria']
#
#     def clean_Price(self):
#         price = self.cleaned_data.get('Price')
#         if price is not None and price <= 0:
#             raise forms.ValidationError("Price must be greater than zero.")
#         return price
#
#     def clean_Name(self):
#         name = self.cleaned_data.get('Name')
#         cafeteria = self.cleaned_data.get('Cafeteria')
#         qs = FoodItem.objects.filter(Name__iexact=name, Cafeteria=cafeteria)
#         if not self.instance.pk and qs.exists():
#             raise forms.ValidationError("A food item with this name already exists.")
#         return name
#
#     def clean_Cafeteria(self):
#         return self.cleaned_data.get('Cafeteria') or None
#
#
# class NutritionInfoForm(forms.ModelForm):
#     class Meta:
#         model = NutritionInfo
#         fields = ['Calories', 'Protein', 'Fat', 'Carbs', 'Sodium']
#         labels = {
#             'Calories': 'Calories (kcal)',
#             'Protein': 'Protein (g)',
#             'Fat': 'Fat (g)',
#             'Carbs': 'Carbohydrates (g)',
#             'Sodium': 'Sodium (mg)',
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         for field in ['Calories', 'Protein', 'Fat', 'Carbs', 'Sodium']:
#             val = cleaned_data.get(field)
#             if val is not None and val < 0:
#                 self.add_error(field, "Value must be 0 or greater.")
#         return cleaned_data
#
#
# class RecipeForm(forms.ModelForm):
#     class Meta:
#         model = Recipe
#         fields = ['PreparationTime', 'Instructions']
#
#     def clean_PreparationTime(self):
#         time = self.cleaned_data.get('PreparationTime')
#         if time is not None and time <= 0:
#             raise forms.ValidationError("Preparation time must be greater than zero.")
#         return time
#
#     def save_with_ingredients(self, food_item, selected_ids):
#         recipe = self.save(commit=False)
#         recipe.FoodItem = food_item
#         recipe.save()
#         recipe.Ingredients.clear()
#         for ing_id in selected_ids:
#             try:
#                 obj = Ingredient.objects.get(pk=ing_id)
#                 recipe.Ingredients.add(obj)
#             except Ingredient.DoesNotExist:
#                 pass
#         return recipe
#
# class CafeteriaForm(forms.ModelForm):
#     class Meta:
#         model = Cafeteria
#         fields = ['Name', 'Location', 'OperatingHours', 'Capacity']
#
#     def clean_Name(self):
#         name = self.cleaned_data.get('Name')
#         qs = Cafeteria.objects.filter(Name__iexact=name)
#         if self.instance.pk:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise forms.ValidationError("This cafeteria already exists.")
#         return name
#
#     def clean_Capacity(self):
#         capacity = self.cleaned_data.get('Capacity')
#         if capacity is not None and capacity <= 0:
#             raise forms.ValidationError("Capacity must be greater than zero.")
#         return capacity
#
#
# class IngredientForm(forms.ModelForm):
#     ExpiryDate = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         label='Expiry Date',
#         required=False
#     )
#
#     class Meta:
#         model = Ingredient
#         fields = ['Name', 'QuantityUnit', 'Threshold', 'StorageCondition', 'ExpiryDate', 'IsAllergen']
#
#     def clean_Name(self):
#         name = self.cleaned_data.get('Name')
#         qs = Ingredient.objects.filter(Name__iexact=name)
#         if self.instance.pk:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise forms.ValidationError("This ingredient already exists.")
#         return name
#
#     def clean_Threshold(self):
#         threshold = self.cleaned_data.get('Threshold')
#         if threshold is not None and threshold < 0:
#             raise forms.ValidationError("Threshold must be zero or positive.")
#         return threshold
#
#
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (CustomUser, AdminProfile, VendorProfile, FoodItem,
                     NutritionInfo, Recipe, Ingredient, Cafeteria, Discount, CATEGORY_CHOICES)

ALLERGEN_KEYS = ['milk', 'eggs', 'wheat', 'soy', 'peanuts', 'tree nuts', 'fish', 'shellfish']


class StudentRegisterForm(UserCreationForm):
    Fname = forms.CharField(max_length=100, label="First Name")
    Lname = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['Fname', 'Lname', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.Fname = self.cleaned_data['Fname']
        user.Lname = self.cleaned_data['Lname']
        user.status = 'active'
        if commit:
            user.save()
        return user


class AdminRegisterForm(UserCreationForm):
    Fname = forms.CharField(max_length=100, label="First Name")
    Lname = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(required=True)
    AdminLevel = forms.CharField(max_length=50, label="Admin Level")
    CafeteriaType = forms.ChoiceField(
        choices=[('college', 'College'), ('highschool', 'High School')],
        label="Cafeteria Type"
    )

    class Meta:
        model = CustomUser
        fields = ['Fname', 'Lname', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'admin'
        user.Fname = self.cleaned_data['Fname']
        user.Lname = self.cleaned_data['Lname']
        user.status = 'active'
        if commit:
            user.save()
            AdminProfile.objects.create(
                user=user,
                AdminLevel=self.cleaned_data['AdminLevel'],
                CafeteriaType=self.cleaned_data['CafeteriaType'],
            )
        return user


class VendorRegisterForm(UserCreationForm):
    Fname = forms.CharField(max_length=100, label="First Name")
    Lname = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(required=True)
    ContactNumber = forms.CharField(max_length=20, label="Contact Number")
    BusinessLicenseNumber = forms.CharField(max_length=100, label="Business License Number")

    class Meta:
        model = CustomUser
        fields = ['Fname', 'Lname', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'vendor'
        user.Fname = self.cleaned_data['Fname']
        user.Lname = self.cleaned_data['Lname']
        user.status = 'active'
        if commit:
            user.save()
            VendorProfile.objects.create(
                user=user,
                ContactNumber=self.cleaned_data['ContactNumber'],
                BusinessLicenseNumber=self.cleaned_data['BusinessLicenseNumber'],
                ContractStatus='pending',
            )
        return user


# class DiscountForm(forms.ModelForm):
#     StartDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     EndDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#
#     class Meta:
#         model = Discount
#         fields = ['Name', 'Description', 'StartDate', 'EndDate', 'Percentage']
#         labels = {
#             'Name': 'Discount Name',
#             'Description': 'Description',
#             'StartDate': 'Start Date',
#             'EndDate': 'End Date',
#             'Percentage': 'Discount Percentage (%)',
#         }
#
#     def clean_Percentage(self):
#         pct = self.cleaned_data.get('Percentage')
#         if pct is not None and (pct < 1 or pct > 100):
#             raise forms.ValidationError("Percentage must be between 1 and 100.")
#         return pct
#
#     def clean(self):
#         cleaned_data = super().clean()
#         start = cleaned_data.get('StartDate')
#         end = cleaned_data.get('EndDate')
#         if start and end and start >= end:
#             raise forms.ValidationError("Start date must be before end date.")
#         return cleaned_data

class DiscountForm(forms.ModelForm):
    StartDate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )
    EndDate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Discount
        fields = ['Name', 'Description', 'StartDate', 'EndDate', 'Percentage']

    def clean_Percentage(self):
        pct = self.cleaned_data.get('Percentage')
        if pct is None:
            raise forms.ValidationError("Percentage is required.")
        if pct < 1 or pct > 100:
            raise forms.ValidationError("Percentage must be between 1 and 100.")
        return pct

    def clean_StartDate(self):
        start = self.cleaned_data.get('StartDate')
        if not start:
            raise forms.ValidationError("Start date is required.")
        return start

    def clean_EndDate(self):
        end = self.cleaned_data.get('EndDate')
        if not end:
            raise forms.ValidationError("End date is required.")
        return end

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('StartDate')
        end = cleaned_data.get('EndDate')
        if start and end and start >= end:
            raise forms.ValidationError("Start date must be before end date.")
        return cleaned_data


# class FoodItemForm(forms.ModelForm):
#     class Meta:
#         model = FoodItem
#         fields = ['Name', 'Price', 'PortionSize', 'Category', 'Cafeteria', 'Discount']
#         labels = {
#             'Discount': 'Apply Discount (optional)',
#         }
#
#     def clean_Price(self):
#         price = self.cleaned_data.get('Price')
#         if price is not None and price <= 0:
#             raise forms.ValidationError("Price must be greater than zero.")
#         return price
#
#     def clean_Name(self):
#         name = self.cleaned_data.get('Name')
#         cafeteria = self.cleaned_data.get('Cafeteria')
#         qs = FoodItem.objects.filter(Name__iexact=name, Cafeteria=cafeteria)
#         if self.instance.pk:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise forms.ValidationError("A food item with this name already exists.")
#         return name
#
#     def clean_Cafeteria(self):
#         return self.cleaned_data.get('Cafeteria') or None

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['Name', 'Price', 'PortionSize', 'Category', 'Cafeteria', 'Discount']

    def clean_Price(self):
        price = self.cleaned_data.get('Price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_PortionSize(self):
        portion_size = self.cleaned_data.get('PortionSize')

        if portion_size is not None and portion_size < 1:
            raise forms.ValidationError(
                "Portion size must be greater than zero."
            )

        return portion_size

    def clean_Name(self):
        name = self.cleaned_data.get('Name')
        cafeteria = self.cleaned_data.get('Cafeteria')
        qs = FoodItem.objects.filter(Name__iexact=name, Cafeteria=cafeteria)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A food item with this name already exists.")
        return name

    def clean_Cafeteria(self):
        return self.cleaned_data.get('Cafeteria') or None


class NutritionInfoForm(forms.ModelForm):
    class Meta:
        model = NutritionInfo
        fields = ['Calories', 'Protein', 'Fat', 'Carbs', 'Sodium']
        labels = {
            'Calories': 'Calories (kcal)',
            'Protein': 'Protein (g)',
            'Fat': 'Fat (g)',
            'Carbs': 'Carbohydrates (g)',
            'Sodium': 'Sodium (mg)',
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['Calories', 'Protein', 'Fat', 'Carbs', 'Sodium']:
            val = cleaned_data.get(field)
            if val is not None and val < 0:
                self.add_error(field, "Value must be 0 or greater.")
        return cleaned_data


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['PreparationTime', 'Instructions']

    def clean_PreparationTime(self):
        time = self.cleaned_data.get('PreparationTime')
        if time is not None and time <= 0:
            raise forms.ValidationError("Preparation time must be greater than zero.")
        return time

    def save_with_ingredients(self, food_item, selected_ids):
        recipe = self.save(commit=False)
        recipe.FoodItem = food_item
        recipe.save()
        recipe.Ingredients.clear()
        for ing_id in selected_ids:
            try:
                obj = Ingredient.objects.get(pk=ing_id)
                recipe.Ingredients.add(obj)
            except Ingredient.DoesNotExist:
                pass
        return recipe


class CafeteriaForm(forms.ModelForm):
    class Meta:
        model = Cafeteria
        fields = ['Name', 'Location', 'OperatingHours', 'Capacity']

    def clean_Name(self):
        name = self.cleaned_data.get('Name')
        qs = Cafeteria.objects.filter(Name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This cafeteria already exists.")
        return name

    def clean_Capacity(self):
        capacity = self.cleaned_data.get('Capacity')
        if capacity is not None and capacity <= 0:
            raise forms.ValidationError("Capacity must be greater than zero.")
        return capacity


class IngredientForm(forms.ModelForm):
    ExpiryDate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Expiry Date',
        required=False
    )

    class Meta:
        model = Ingredient
        fields = ['Name', 'QuantityUnit', 'Threshold', 'StorageCondition', 'ExpiryDate', 'IsAllergen']

    def clean_Name(self):
        name = self.cleaned_data.get('Name')
        qs = Ingredient.objects.filter(Name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This ingredient already exists.")
        return name

    def clean_Threshold(self):
        threshold = self.cleaned_data.get('Threshold')
        if threshold is not None and threshold < 0:
            raise forms.ValidationError("Threshold must be zero or positive.")
        return threshold