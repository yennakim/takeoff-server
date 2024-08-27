from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from takeoffapi.models import Trip, User, Traveler, TripTraveler

class TripSerializer(serializers.ModelSerializer):
  class Meta:
    model = Trip
    fields = ('id', 'user_id', 'trip_name', 'origin', 'destination', 'start_date', 'end_date')
    depth = 2

class TripView(ViewSet):
  def retrieve(self, request, pk=None):
    try:
      trip = Trip.objects.get(pk=pk)
      serializer = TripSerializer(trip)
      return Response(serializer.data)
    except Trip.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    trips = Trip.objects.all()
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)

  def create(self, request):
    user = User.objects.get(id=request.data["user_id"])
    
    trip = Trip.objects.create(
      user = user,
      trip_name = request.data["trip_name"],
      origin = request.data["origin"],
      destination = request.data["destination"],
      start_date = request.data["start_date"],
      end_date = request.data["end_date"],
    )
    serializer = TripSerializer(trip)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
   
  def update(self, request, pk):
    trip = Trip.objects.get(pk=pk)
    user = User.objects.get(id=request.data["user_id"])
    
    trip.user = user
    trip.trip_name = request.data["trip_name"]
    trip.origin = request.data["origin"]
    trip.destination = request.data["destination"]
    trip.start_date = request.data["start_date"]
    trip.end_date = request.data["end_date"]
    trip.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)

  def delete(self, request, pk):
    trip = Trip.objects.get(pk=pk)
    trip.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

  @action(methods=['post'], detail=True)
  def add_traveler(self, request, pk):
    trip = Trip.objects.get(pk=pk)
    traveler = Traveler.objects.get(pk=pk)
    trip_traveler = TripTraveler.objects.create(
      trip = trip,
      traveler = traveler
    )
    
    return Response({'message': 'Traveler added to trip'}, status=status.HTTP_201_CREATED)

  @action(methods=['delete'], detail=True)
  def remove_traveler(self, request, pk):
    trip = Trip.objects.get(pk=pk)
    traveler = Traveler.objects.get(pk=pk)
    trip_traveler = TripTraveler.objects.filter(trip_id = trip.id, traveler_id = traveler.id)
    trip_traveler.delete()
    
    return Response({'message': 'Traveler removed'}, status=status.HTTP_204_NO_CONTENT)
