from rest_framework import viewsets, permissions
from .models import Cart, Order
from .serializers import CartSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
from account.models import User


class OrderViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Order.objects.filter(username=self.request.user)
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class CartViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Cart.objects.filter(username=self.request.user)
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
