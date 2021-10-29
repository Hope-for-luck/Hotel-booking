from django.contrib.auth.admin import admin
from .models import Cart, Order

admin.site.register(Order)
admin.site.register(Cart)
