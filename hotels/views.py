from .serializers import HotelLikesSerializer, HotelCreateSerializer, HotelListSerializer, HotelDetailSerializer, \
    HotelReviewSerializer
from .models import HotelReview, HotelLike, Hotel
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters


class HotelReviewViewSet(viewsets.ModelViewSet):
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class HotelLikesViewSet(viewsets.ModelViewSet):
    queryset = HotelLike.objects.all()
    serializer_class = HotelLikesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter]
    # filterset_fields = ['rent', 'name', 'status']
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'delete':
            return HotelListSerializer
        elif self.action == 'retrieve':
            return HotelDetailSerializer
        return HotelCreateSerializer
