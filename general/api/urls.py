from django.urls import path
from .views import (
    UserListView,
    ProductListCreateView,
    ProductDetailView,
    CartDetailView,
    CartItemAddView,
    OrderListCreateView,
    RegisterView,
)


urlpatterns = [
    

    path('register/', RegisterView.as_view(), name='register'),

    path('users/', UserListView.as_view(), name='user-list'),

    
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', CartItemAddView.as_view(), name='cart-item-add'),

    
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),

    
]
