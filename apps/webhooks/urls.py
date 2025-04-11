from django.urls import path
from . import views

urlpatterns = [
    path('', views.receber, name='webhooks_receber'),
]
