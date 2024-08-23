from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import TripTraveler, Trip, Traveler

class TripTravelerSerializer(serializers.ModelSerializer):
  class Meta:
    model = TripTraveler
    fields = ('id', 'trip_id', 'traveler_id')
    depth = 1

class TripTravelerView(ViewSet):
  def retrieve(self, request, pk=None):
    try:
      trip_traveler = TripTraveler.objects.get(pk=pk)
      serializer = TripTravelerSerializer(trip_traveler)
      return Response(serializer.data)
    except Trip.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    trip_travelers = Trip.objects.all()
    serializer = TripTravelerSerializer(trip_travelers, many=True)
    return Response(serializer.data)
