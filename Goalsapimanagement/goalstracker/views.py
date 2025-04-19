from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import DailyGoal
from .serializers import GoalS
from rest_framework.permissions import IsAuthenticated


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def goalsgetpost(request):
    if request.method=='GET':
        try:
            qs=DailyGoal.objects.all()
        except:
            return Response({'msg':'no data available'},status=status.HTTP_400_BAD_REQUEST )
        s1=GoalS(qs,many=True)
        return Response(s1.data, status=status.HTTP_200_OK)
    
    if request.method=='POST':
        s1=GoalS(data=request.data)
        if s1.is_valid():
            s1.save()
            return Response(s1.data,status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':s1.errors},status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def goalsedit(request,pk):
    if request.method=='GET':
        try:
            qs=DailyGoal.objects.get(pk=pk)
        except:
            return Response('Not found',status=status.HTTP_404_NOT_FOUND )
        s1=GoalS(qs)
        return Response(s1.data, status=status.HTTP_200_OK)
    
    if request.method=='PATCH':
        try:
            qs=DailyGoal.objects.get(pk=pk)
        except:
            return Response({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND )
        s1=GoalS(instance=qs,data=request.data,partial=True)
        if s1.is_valid():
            s1.save()
            return Response(s1.data,status=status.HTTP_200_OK)
        else:
            return Response({'msg':s1.errors},status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE':
        try:
            qs=DailyGoal.objects.get(pk=pk)
        except:
            return Response({'msg':'Not found'},status=status.HTTP_404_NOT_FOUND )
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)