from django.urls import path
from . import views

urlpatterns = [
    path('<int:publication_id>/', views.publication_view, name='view_publication'),
    path('new/', views.create_publication, name='create_publication'),
    path('like-publication/<int:publication_id>/', views.like_publication, name='like_publication'),
]