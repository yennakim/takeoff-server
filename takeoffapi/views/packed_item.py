from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import PackedItem, Trip


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackedItem
        fields = ('id', 'trip_id', 'item_name', 'quantity')
        depth = 1


class PackedItemView(ViewSet):
    def retrieve(self, request, pk=None):
        try:
            item = PackedItem.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except PackedItem.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        trip_id = request.query_params.get('trip_id', None)
        if trip_id is not None:
            try:
                trip = Trip.objects.get(id=trip_id)
                items = PackedItem.objects.filter(trip=trip)
            except Trip.DoesNotExist:
                return Response({'message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = PackedItem.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        trip = Trip.objects.get(pk=request.data["trip_id"])

        packed_item = PackedItem.objects.create(
            trip=trip,
            item_name=request.data["item_name"],
            quantity=request.data["quantity"],
        )
        serializer = ItemSerializer(packed_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        packed_item = PackedItem.objects.get(pk=pk)
        trip = Trip.objects.get(pk=request.data["trip_id"])
        packed_item.trip = trip
        packed_item.item_name = request.data["item_name"]
        packed_item.quantity = request.data["quantity"]
        packed_item.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        packed_item = PackedItem.objects.get(pk=pk)
        packed_item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
