from django.shortcuts import render
from .models import Inventory
from .serializers import InventorySerializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import api_view


@api_view(['GET','POST'])
def itemsgetpost(request):
    if request.method=='GET':
        qs=Inventory.objects.all()
        s1=InventorySerializer(qs,many=True)
        return Response(s1.data,status=status.HTTP_200_OK)
    
    if request.method=='POST':
        s1=InventorySerializer(data=request.data)
        if s1.is_valid():
            barcode=s1.validated_data['barcode']
            if Inventory.objects.filter(barcode=barcode).exists():
                return Response({'barcode':['inventory with this barcode already exists.']},status=status.HTTP_400_BAD_REQUEST)
            s1.save()
            return Response(s1.data,status=status.HTTP_201_CREATED)
        return Response(s1.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
@api_view(['DELETE', 'PUT'])
def itemedit(request,pk):
    if request.method=='DELETE':
        try:
            qs=Inventory.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    if request.method=='PUT':
        try:
            qs=Inventory.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        s1=InventorySerializer(qs,data=request.data)
        if s1.is_valid():
            s1.save()
            return Response(s1.data, status=status.HTTP_200_OK)
        

        
@api_view(['GET'])
def itemscategory(request,category):
    if request.method=='GET':
        try:
            qs=Inventory.objects.filter(category=category)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s1=InventorySerializer(qs,many=True)
        return Response(s1.data,status=status.HTTP_200_OK)
        
        
@api_view(['GET'])
def itemsort(request):
    if request.method=='GET':
        qs=Inventory.objects.all().order_by('-price')
        s1=InventorySerializer(qs,many=True)
        return Response(s1.data,status=status.HTTP_200_OK)