from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import RoleModel,UserModel,NewsModel
from .serializers import UserS, NewsS
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
class Login(APIView):
    #authentication_classes=[JWTAuthentication]
    def post(self,request,*args,**kwargs):
        email=request.data.get('email')
        password=request.data.get('password')
        if not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)

        #refresh = RefreshToken.for_user(user)
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    
class NewsListPost(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        if request.user.role.role_name!='reporter':
            return Response(status=403)
        s1=NewsS(data=request.data)
        if s1.is_valid():
            s1.save(author=request.user)
            return Response(s1.data,status=201)
        else:
            return Response(s1.errors,status=400)
    

    def get(self,request,*args,**kwargs):
        try:
            qs=NewsModel.objects.all()
        except:
            return Response(status=400)
        s1=NewsS(qs,many=True)
        return Response(s1.data,status=200)
    
class NewsRetrieve(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request,id):
        try:
            qs=NewsModel.objects.get(pk=id)
        except:
            return Response(status=404)
        s1=NewsS(qs)
        return Response(s1.data,status=200)
    


    def put(self,request,id,*args,**kwargs):
        if not request.data:
            return Response(status=400)
        try:
            qs=NewsModel.objects.get(pk=id)
        except:
            return Response(status=404)
        if qs.author!=request.user:
            return Response(status=403)
        s1=NewsS(qs,data=request.data)
        if s1.is_valid():
            s1.save()
        return Response(s1.data,status=200)
    
    def patch(self,request,id,*args,**kwargs):
        
        try:
            qs=NewsModel.objects.get(pk=id)
        except:
            return Response(status=404)
        if qs.author!=request.user:
            return Response(status=403)
        s1=NewsS(qs,data=request.data,partial=True)
        if s1.is_valid():
            s1.save()
        return Response(s1.data,status=200)
    


    def delete(self,request,id,*args,**kwargs):
        
        try:
            qs=NewsModel.objects.get(pk=id)
        except:
            return Response(status=404)
        if qs.author!=request.user:
            return Response(status=403)
        qs.delete()
        return Response(status=204)