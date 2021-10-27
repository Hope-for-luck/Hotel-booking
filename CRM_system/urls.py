from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from hotels.views import HotelViewSet, HotelLikesViewSet, HotelReviewViewSet
from account.views import UserViewSet

router = DefaultRouter()
router.register('reviews', HotelReviewViewSet)
router.register('hotels', HotelViewSet)
router.register('likes', HotelLikesViewSet)
router.register('users', UserViewSet,  basename='User')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    ]
