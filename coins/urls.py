from django.urls import path
from . import views

urlpatterns = [
    path('', views.explore_coins, name='explore_coins'),
    path('coin/<int:pk>/', views.coin_detail, name='coin_detail'),
]
