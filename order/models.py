from django.db import models
from hotels.models import CreatedAtModel
from model_utils import Choices
from model_utils.fields import StatusField
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    username = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='cart')
    # order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name='items')
    room = models.ForeignKey('hotels.HotelRoom', on_delete=models.RESTRICT, related_name='cart')
    days = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart'


class Order(CreatedAtModel):
    STATUS = Choices('In progress', 'Canceled', 'Finished')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    username = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='order')
    cart = models.ForeignKey(Cart, on_delete=models.RESTRICT, related_name='order')
    order_status = StatusField()

    class Meta:
        ordering = ['-created_at']
        db_table = 'order'

    def __str__(self):
        return f"Заказ № {self.id} от {self.created_at.strftime('%d%m%Y %H:%M')}"
