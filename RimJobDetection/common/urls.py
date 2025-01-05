from django.urls import path
from RimJobDetection.common import views

urlpatterns = [

    path('', views.home_page, name='home page')

]