from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='principal_home'),
]
