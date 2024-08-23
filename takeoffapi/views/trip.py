from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import Trip

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
