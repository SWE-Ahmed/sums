from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('result', views.summary, name='result')
]