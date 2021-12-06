from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.user_view, name='view_user'),
    path('all/', views.all_users, name='view_all_users')
]