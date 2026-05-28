from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('add_coin/', views.add_new_coin, name='add_new_coin'),
    path('coins/<int:coin_id>/edit/', views.edit_coin, name='edit_coin'),
    path('coins/<int:coin_id>/delete/', views.delete_coin, name='delete_coin'),
    path('transactions/', views.admin_transactions, name='admin_transactions'),
    path('transactions/<int:tx_id>/delete/', views.delete_transaction, name='delete_transaction'),
]
