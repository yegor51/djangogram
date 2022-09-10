from django.urls import path
from . import views

urlpatterns = [
    path('<int:publication_id>/', views.publication_view, name='view_publication'),
    path('new/', views.create_publication, name='create_publication'),
    path('set-publication-mark/<int:publication_id>/', views.set_publication_mark, name='set_publication_mark'),
    path('delete/<int:publication_id>/', views.delete_publication, name='delete_publication'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('news-feed/', views.news_feed, name='news_feed'),
]