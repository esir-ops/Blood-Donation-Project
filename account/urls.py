
from django.urls import path
from .views import register
from .views import login_view, complete_profile, profile_view, UpdateProfileView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('profile/', profile_view, name='profile'),
]