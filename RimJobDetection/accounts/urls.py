from django.urls import path
from django.urls import include
from RimJobDetection.accounts import views


urlpatterns = [

    path('register', views.register_user, name='register user'),
    path('login', views.log_in_user, name='login user'),
    path('logout', views.logout_user, name='logout user'),
]