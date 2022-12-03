from django.urls import path
from .views import *


urlpatterns = [
    path('list', ListTasksView.as_view()),
    path('create-task', CreateTaskView.as_view()),
    path('edit-task', EditTaskView.as_view()),
    path('delete-task', DeleteTaskView.as_view()),
]