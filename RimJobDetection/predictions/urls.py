from django.urls import path
from RimJobDetection.predictions import views

urlpatterns = [

    path('prediction', views.prediction, name='user predict')
]