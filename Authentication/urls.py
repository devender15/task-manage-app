
from django.urls import path
from .views import *


urlpatterns = [
    path('users', ListUsersView.as_view()),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('details', UserDetailsView.as_view()),
]