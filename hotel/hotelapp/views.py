from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import ownermodel,hotelmodel,roommodel
from .serializers import ownerserializer,hotelserializer,roomserializer
# Create your views here.
@api_view(["POST"])
def ownerpost(request):
    if request.method=="POST":
        s1=ownerserializer(data=request.data)
        if s1.is_valid():
            s1.save()
            return Response(s1.data,status=status.HTTP_201_CREATED)
        return Response("email already exists",status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def hotelpost(request):
    if request.method=="POST":
        s1=hotelserializer(data=request.data)
        if s1.is_valid():
            s1.save()
            return Response(s1.data,status=status.HTTP_201_CREATED)
        return Response("This field is required",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def roompost(request):
    if request.method=="POST":
        s1=roomserializer(data=request.data)
        if s1.is_valid():
            s1.save()
            return Response(s1.data,status=status.HTTP_201_CREATED)
        return Response("This field is required",status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PATCH","DELETE"])
def roomget(request,id):
    if request.method=="GET":
        try:
            m1=roommodel.objects.get(id=id)
        except:
            return Response("Not found",status=status.HTTP_404_NOT_FOUND)
        s1=roomserializer(m1)
        return Response(s1.data)
    if request.method=="DELETE":
        try:
            m1=roommodel.objects.get(id=id)
        except:
            return Response("Not found",status=status.HTTP_404_NOT_FOUND)
        m1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method=="PATCH":
        try:
            m1=roommodel.objects.get(id=id)
        except:
            return Response("Not found",status=status.HTTP_404_NOT_FOUND)
        s1=roomserializer(data=request.data,instance=m1,partial=True)
        if s1.is_valid():
            s1.save()
            return Response(s1.data,status=status.HTTP_200_OK)
