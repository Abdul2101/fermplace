from rest_framework import serializers
from general.models import User, Product, Cart, CartItem, Order, OrderItem


from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password_confirm', 'role']

    def validate(self, data):
        # Проверка, что пароли совпадают
        if data['password'] != data['password_confirm']:
            raise ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Удаляем 'password_confirm' перед созданием пользователя
        validated_data.pop('password_confirm')
        user = get_user_model().objects.create_user(**validated_data)  # Используем create_user для хэширования пароля
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email']  # Поля, которые нельзя менять


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)  # Показывает имя продавца

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'photo', 'seller']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Вложенный продукт

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Вложенные элементы корзины

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Вложенный продукт

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_time_of_order']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # Вложенные элементы заказа

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'user', 'total_price', 'created_at']
