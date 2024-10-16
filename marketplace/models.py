from django.db import models
from accounts.models import User
from menu.models import Fooditem



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(Fooditem, on_delete=models.CASCADE, related_name="cart")
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user
