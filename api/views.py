from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import authentication,permissions
from rest_framework import serializers

from api.serializers import UserSerializer,TodoSerializer

from django.contrib.auth.models import User
from todo.models import Todos

# Create your views here.

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class TodosView(ViewSet):

    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    def list(self, request, *args, **kwargs):
        qs=Todos.objects.filter(user=request.user)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    

    def destroy(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        obj=Todos.objects.get(id=id)
        if obj.user != request.user:
            raise serializers.ValidationError('permission denied')
        else:
            obj.delete()
            return Response({'message':'Deleted'})
        

    def update(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        obj=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    