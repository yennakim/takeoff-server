from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import Traveler

class TravelerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Traveler
    fields = ('id', 'first_name', 'last_name', 'image')
    depth = 1

class TravelerView(ViewSet):
  def retrieve(self, request, pk=None):
    try:
      traveler = Traveler.objects.get(pk=pk)
      serializer = TravelerSerializer(traveler)
      return Response(serializer.data)
    except Traveler.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    travelers = Traveler.objects.all()
    serializer = TravelerSerializer(travelers, many=True)
    return Response(serializer.data)

  def create(self, request):
    traveler = Traveler.objects.create(
      first_name = request.data["first_name"],
      last_name = request.data["last_name"],
      image = request.data["image"],
    )
    serializer = TravelerSerializer(traveler)
    return Response(serializer.data)

  def update(self, request, pk):
    traveler = Traveler.objects.get(pk=pk)
    traveler.first_name = request.data["first_name"]
    traveler.last_name = request.data["last_name"]
    traveler.image = request.data["image"]
    traveler.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
