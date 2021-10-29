from django.contrib import admin
from .models import Hotel, HotelReview, HotelLike

admin.site.register(Hotel)
admin.site.register(HotelReview)
admin.site.register(HotelLike)
