from django.db import models


class Owner(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Hotel(models.Model):
    hotel_name=models.CharField(max_length=200)
    address=models.CharField(max_length=300)
    owner_id=models.ForeignKey(Owner,on_delete=models.CASCADE, related_name='hotel')
    
    def __str__(self):
        return self.hotel_name
    
class Room(models.Model):
    room_no=models.CharField(max_length=100)
    rent=models.IntegerField()
    is_occupied=models.BooleanField()
    hotel_id=models.ForeignKey(Hotel,on_delete=models.CASCADE, related_name='room')
    
    def __str__(self):
        return self.room_no