from django.db import models
from django.contrib.auth.models import User
from index.models import Product
# Create your models here.

class UserProfile(models.Model):
    user_model            = models.OneToOneField(User, on_delete=models.CASCADE)
    accepted_price        = models.FloatField()
    wanted_products       = models.ManyToManyField(Product)
    
    
    
    
    def __str__(self):
        return self.user_model.username