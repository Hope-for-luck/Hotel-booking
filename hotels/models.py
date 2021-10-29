from django.db import models
from django.contrib.auth import get_user_model
from model_utils import Choices
from model_utils.fields import StatusField
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import notify_user_func

User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class Hotel(CreatedAtModel):
    STATUS = Choices("Available", "Not available")
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to="hotel's_image", null=True, blank=True)
    status = StatusField()
    description = models.TextField()
    stars = models.PositiveIntegerField(default=1)
    total_floors = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['name']


class HotelRoom(CreatedAtModel):
    STATUS = Choices("single", "double", "triple", "apartment", "suite")
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE,
        related_name='room'
    )
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    floor = models.PositiveIntegerField(default=1)
    room = StatusField()

    # class Meta:
    #     ordering = ['hotel', 'rent']


class HotelReview(CreatedAtModel):
    username = models.ForeignKey(
        'account.User', on_delete=models.CASCADE,
        related_name='reviews'
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    # rating = models.PositiveIntegerField(default=1)


class HotelLike(CreatedAtModel):
    username = models.ForeignKey(
        'account.User', on_delete=models.CASCADE,
        related_name='likes'
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="likes"
    )


class HotelFavorites(CreatedAtModel):
    username = models.ForeignKey(
        'account.User', on_delete=models.CASCADE,
        related_name='favorites'
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="favorites"
    )


@receiver(post_save, sender=HotelReview)
def notify_user(sender, instance, created, **kwargs):
    if created:
        email = instance.username.email
        notify_user_func.delay(email)
