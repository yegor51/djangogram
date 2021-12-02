from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/<int:id>/', views.profile),
    path('publication/<int:id>/', views.publication)
]