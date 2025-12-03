from django.db import models

# Create your models here.
class Inventory(models.Model):
    name=models.CharField(max_length=200)
    category=models.CharField(max_length=200)
    price=models.IntegerField()
    quantity=models.IntegerField()
    barcode=models.IntegerField(unique=True)

    # def __str__(self):
    #     return self.name