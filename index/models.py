from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name            = models.CharField(max_length=100)
    shop_product_id = models.CharField(max_length=100)
    price           = models.FloatField()
    image_url       = models.URLField(null=True)
    product_url     = models.URLField(null=True)
    last_update     = models.DateTimeField(default=timezone.now, null=False)




    def __str__(self):
        return self.name