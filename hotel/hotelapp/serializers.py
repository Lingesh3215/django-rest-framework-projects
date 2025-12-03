from .models import ownermodel,hotelmodel,roommodel
from rest_framework import serializers

class roomserializer(serializers.ModelSerializer):
    class Meta:
        model=roommodel
        fields="__all__"
    
class hotelserializer(serializers.ModelSerializer):
    rooms=roomserializer(read_only=True, many=True)
    class Meta:
        model=hotelmodel
        fields="__all__"

class ownerserializer(serializers.ModelSerializer):
    hotels=hotelserializer(read_only=True,many=True)
    class Meta:
        model=ownermodel
        fields="__all__"

