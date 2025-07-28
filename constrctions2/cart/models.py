from django.conf import settings
from django.db import models
from project.models import ConstructionProject

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    project = models.ForeignKey(ConstructionProject, on_delete=models.CASCADE, related_name="cart_items")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"

    