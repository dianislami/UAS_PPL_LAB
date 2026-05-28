from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_dashboard, name='portfolio_dashboard'),
    path('add/', views.add_to_portfolio, name='add_to_portfolio'),
]
