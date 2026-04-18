from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import FoodItemForm


class HomePageView(View):
    template_name = 'foodcomposition/index.html'

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user
        })


class LoginView(View):
    template_name = 'foodcomposition/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, self.template_name, {
                'error': 'Invalid credentials'
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


class AddFoodItemView(View):
    template_name = 'foodcomposition/addNewFoodItem.html'

    def get(self, request):
        form = FoodItemForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FoodItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})