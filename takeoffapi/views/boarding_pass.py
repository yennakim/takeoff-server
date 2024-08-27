from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import BoardingPass, Trip

class BoardingPassSerializer(serializers.ModelSerializer):
  class Meta:
    model = BoardingPass
    fields = ('id', 'trip_id', 'departing_from', 'arriving_to', 'airline', 'gate', 'seat', 'departure_time', 'arrival_time', 'flight_number')
    depth = 1

class BoardingPassView(ViewSet):
  def retrieve(self, request, pk=None):
    try:
      boarding_pass = BoardingPass.objects.get(pk=pk)
      serializer = BoardingPassSerializer(boarding_pass)
      return Response(serializer.data)
    except BoardingPass.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    boarding_passes = BoardingPass.objects.all()
    serializer = BoardingPassSerializer(boarding_passes, many=True)
    return Response(serializer.data)

  def create(self, request):
    trip = Trip.objects.get(pk=request.data["trip_id"])
    
    boarding_pass = BoardingPass.objects.create(    
      trip = trip,
      departing_from = request.data["departing_from"],
      arriving_to = request.data["arriving_to"],
      airline = request.data["airline"],
      gate = request.data["gate"],
      seat = request.data["seat"],
      departure_time = request.data["departure_time"],
      arrival_time = request.data["arrival_time"],
      flight_number = request.data["flight_number"],
    )
    serializer = BoardingPassSerializer(boarding_pass)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk):
    boarding_pass = BoardingPass.objects.get(pk=pk)
    trip = Trip.objects.get(pk=request.data["trip_id"])
    boarding_pass.trip = trip
    boarding_pass.departing_from = request.data["departing_from"]
    boarding_pass.arriving_to = request.data["arriving_to"]
    boarding_pass.airline = request.data["airline"]
    boarding_pass.gate = request.data["gate"]
    boarding_pass.seat = request.data["seat"]
    boarding_pass.departure_time = request.data["departure_time"]
    boarding_pass.arrival_time = request.data["arrival_time"]
    boarding_pass.flight_number = request.data["flight_number"]
    boarding_pass.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)

  def delete(self, request, pk):
    boarding_pass = BoardingPass.objects.get(pk=pk)
    boarding_pass.delete()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)
