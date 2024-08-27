from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'image', 'email', 'uid')
    depth = 1

class UserView(ViewSet):
  def retrieve(self, request, pk=None):
    try:
      user = User.objects.get(pk=pk)
      serializer = UserSerializer(user)
      return Response(serializer.data)
    except User.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

  def create(self, request):
    user = User.objects.create(
      first_name = request.data["first_name"],
      last_name = request.data["last_name"],
      image = request.data["image"],
      email = request.data["email"],
      uid = request.data["uid"],
    )
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    user = User.objects.get(pk=pk)
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.image = request.data["image"]
    user.email = request.data["email"]
    user.uid = request.data["uid"]
    user.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)

  def delete(self, request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
