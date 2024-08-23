from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import BoardingPass

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
