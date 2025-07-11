from django.urls import path
from . import views

urlpatterns = [
    path('search/<str:isbn>/', views.search, name='search'),
]