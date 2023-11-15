from django.urls import path
from . import views

urlpatterns = [
    path('create_document/', views.create_document),
]