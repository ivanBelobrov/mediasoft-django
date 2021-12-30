from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = '/base_of_films/films/'


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


class RegistrationUserView(View):
    @staticmethod
    def get(request):
        form = UserRegistrationForm()
        return render(request, 'users/registration.html', context={'form': form})

    @staticmethod
    def post(request):
        form = UserRegistrationForm(request.POST)
        if not form.is_valid():
            return render(request, 'users/registration.html', context={'form': form})
        else:
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/base_of_films/films/')


