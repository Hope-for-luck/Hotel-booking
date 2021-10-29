from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from hotels.views import HotelViewSet, HotelLikesViewSet, HotelReviewViewSet, HotelRoomViewSet, \
    HotelFavoritesViewSet
from account.views import UserViewSet, ProfileViewSet
from order.views import CartViewSet, OrderViewSet
from .yasg import urlpatterns as doc_urls

router = DefaultRouter()
router.register('reviews', HotelReviewViewSet)
router.register('hotels', HotelViewSet)
router.register('likes', HotelLikesViewSet)
router.register('users', UserViewSet, basename='User')
router.register('profile', ProfileViewSet, basename='User')
router.register('rooms', HotelRoomViewSet)
router.register('order', OrderViewSet, basename='Order')
router.register('cart', CartViewSet, basename='Cart')
router.register('favorites', HotelFavoritesViewSet, basename='HotelFavorites')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
]

urlpatterns += doc_urls
