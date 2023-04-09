from django.shortcuts import render
from rest_framework.response import Response
from api.serializers import PostSerializer,UserSerializer
from api.models import Post
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework import authentication,permissions

class SocialAppView(ModelViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=PostSerializer
    queryset=Post.objects.all()

    def perform_create(self, serializer):
       serializer.save(user=self.request.user)

    def list(self,request,*args,**kwargs):
        qs=Post.objects.filter(User=request.user)
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)

class UsersView(ModelViewSet):

    serializer_class=UserSerializer
    queryset=User.objects.all()   
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(): 
            usr=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerializer(usr,many=False)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors) 

