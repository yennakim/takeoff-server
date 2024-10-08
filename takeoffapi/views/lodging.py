from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import Lodging, Trip


class LodgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lodging
        fields = ('id', 'trip_id', 'address', 'city', 'length_of_stay')
        depth = 1


class LodgingView(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            lodging = Lodging.objects.get(pk=pk)
            serializer = LodgingSerializer(lodging)
            return Response(serializer.data)
        except Lodging.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        trip_id = request.query_params.get('trip_id', None)
        if trip_id is not None:
            try:
                trip = Trip.objects.get(id=trip_id)
                lodgings = Lodging.objects.filter(trip=trip)
            except Trip.DoesNotExist:
                return Response({'message': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            lodgings = Lodging.objects.all()
        serializer = LodgingSerializer(lodgings, many=True)
        return Response(serializer.data)

    def create(self, request):
        trip = Trip.objects.get(pk=request.data["trip_id"])
        lodging = Lodging.objects.create(
            trip=trip,
            address=request.data["address"],
            city=request.data["city"],
            length_of_stay=request.data["length_of_stay"],
        )
        serializer = LodgingSerializer(lodging)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        lodging = Lodging.objects.get(pk=pk)
        trip = Trip.objects.get(pk=request.data["trip_id"])
        lodging.trip = trip
        lodging.address = request.data["address"]
        lodging.city = request.data["city"]
        lodging.length_of_stay = request.data["length_of_stay"]
        lodging.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        lodging = Lodging.objects.get(pk=pk)
        lodging.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
