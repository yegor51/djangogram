from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>/', views.publication_view, name='view_publication'),
]