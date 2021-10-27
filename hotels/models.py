from django.db import models
from django.contrib.auth import get_user_model
from model_utils import Choices
from model_utils.fields import StatusField

User = get_user_model()


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class Hotel(CreatedAtModel):
    STATUS = Choices("Available", "Not available")
    name = models.CharField(max_length=50, unique=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="hotel's_image", null=True, blank=True)
    status = StatusField()
    description = models.TextField()

    class Meta:
        ordering = ['name', 'rent']

    def __str__(self):
        return self.name


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
    rating = models.PositiveIntegerField(default=1)


class HotelLike(CreatedAtModel):
    username = models.ForeignKey(
        'account.User', on_delete=models.CASCADE,
        related_name='likes'
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="likes"
    )
