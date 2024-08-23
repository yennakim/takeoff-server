from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from takeoffapi.models import PackedItem

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
    items = PackedItem.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
