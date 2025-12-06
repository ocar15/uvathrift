from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    CONDITIONS = [
        (1, "New"),
        (2, "Like New"),
        (3, "Good"),
        (4, "Fair"),
        (5, "Poor")
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="item_images/", blank=True, null=True)
    condition = models.PositiveSmallIntegerField(choices=CONDITIONS, default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (${self.price})"