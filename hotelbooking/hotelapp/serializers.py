from rest_framework import serializers
from .models import Hotel,Room,Owner


        
class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Room
        fields="__all__"
        
        
        
class HotelSerializer(serializers.ModelSerializer):
    rooms=RoomSerializer(read_only=True, many=True)
    class Meta:
        model=Hotel
        fields="__all__"
        
        
class OwnerSerializer(serializers.ModelSerializer):
    hotels=HotelSerializer(read_only=True, many=True)
    class Meta:
        model=Owner
        fields="__all__"