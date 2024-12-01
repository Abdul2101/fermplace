# admin.py
from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, User  # импортируем User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Создаем кастомный администратор для User
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Админка для модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'seller', 'description']
    search_fields = ['title', 'seller__username']
    list_filter = ['seller']

# Админка для модели CartItem (корзина)
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Устанавливаем минимальное количество пустых форм для добавления товаров в корзину

# Админка для модели OrderItem (покупка)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

# Админка для модели Order (заказ)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['user', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username']

# Админка для модели Cart (корзина)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']

# Регистрируем все модели
admin.site.register(User, UserAdmin)  # Регистрация кастомного администратора для User
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
