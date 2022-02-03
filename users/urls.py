from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.user_view, name='view_user'),
    path('all/', views.all_users, name='view_all_users'),
    path('my-profile/', views.my_profile, name='my_profile'),
]