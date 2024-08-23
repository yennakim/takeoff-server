from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import Trip, User

class TripSerializer(serializers.ModelSerializer):
  class Meta:
    model = Trip
    fields = ('id', 'user_id', 'trip_name', 'origin', 'destination', 'start_date', 'end_date')
    depth = 1

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
    return Response(serializer.data)
   
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
