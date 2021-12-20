from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path(r'confirm-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         views.confirm_email_view,
         name='confirm_email'),
    path('email-not-confirmed/', views.email_not_confirmed_view, name='email_not_confirmed'),
    path('send-activation-link/', views.send_activation_link_view, name='send_activation_link'),
]
