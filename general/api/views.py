from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from general.models import User, Product, Cart, CartItem, Order
from .serializers import (
    UserSerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        # Создаем экземпляр сериализатора с переданными данными
        serializer = RegisterSerializer(data=request.data)
        
        # Проверяем, что сериализатор валиден
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        
        # Если данные невалидны, возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Только администратор может видеть список пользователей


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'seller':
            raise PermissionDenied("Only sellers can create products.")
        serializer.save(seller=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.seller:
            raise PermissionDenied("You are not allowed to edit this product.")
        serializer.save()


class CartDetailView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Использование filter().first() вместо get() для предотвращения исключений
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart:
            raise PermissionDenied("Cart not found.")
        return cart


class CartItemAddView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        # Проверка на наличие товара в корзине, чтобы избежать дублирования
        if CartItem.objects.filter(cart=cart, product=product).exists():
            raise PermissionDenied("Product is already in the cart.")
        serializer.save(cart=cart)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart or not cart.items.exists():
            raise PermissionDenied("Your cart is empty, you cannot create an order.")
        serializer.save(user=self.request.user)
