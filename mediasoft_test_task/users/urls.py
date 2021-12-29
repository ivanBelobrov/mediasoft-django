from django.urls import path
from .views import UserLoginView, UserLogoutView, RegistrationUserView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', RegistrationUserView.as_view(), name='registration')
]