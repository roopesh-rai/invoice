from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

