from django.db import models

# Create your models here.
# Create your models here.
class ownermodel(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)

class hotelmodel(models.Model):
    hotel_name=models.CharField(max_length=100)
    address=models.TextField(max_length=200)
    owner_id=models.ForeignKey(ownermodel,on_delete=models.CASCADE,related_name="hotel")

class roommodel(models.Model):
    room_no=models.CharField(max_length=100)
    rent=models.IntegerField()
    is_occupied=models.BooleanField()
    hotel_id=models.ForeignKey(hotelmodel,on_delete=models.CASCADE,related_name="rooms")