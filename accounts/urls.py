from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, register_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),
]
