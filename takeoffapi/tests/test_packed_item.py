from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from takeoffapi.models import Trip, PackedItem
from takeoffapi.views.packed_item import ItemSerializer


class PackedItemTests(APITestCase):

    fixtures = ['trip', 'user', 'packed_item']

    def setUp(self):
        self.trip = Trip.objects.first()

    def test_create_packed_item(self):
        """Create PackedItem test"""
        url = "/items"

        packed_item = {
            "trip_id": self.trip.id,
            "item_name": "Laptop",
            "quantity": 1
        }

        response = self.client.post(url, packed_item, format='json')

        new_packed_item = PackedItem.objects.last()

        expected = ItemSerializer(new_packed_item)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_get_packed_item(self):
        """Get PackedItem Test"""
        packed_item = PackedItem.objects.first()

        url = f'/items/{packed_item.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = ItemSerializer(packed_item)

        self.assertEqual(expected.data, response.data)

    def test_list_packed_items(self):
        """Test list PackedItems"""
        url = '/items'

        response = self.client.get(url)

        all_packed_items = PackedItem.objects.all()
        expected = ItemSerializer(all_packed_items, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_packed_item(self):
        """Test update PackedItem"""
        packed_item = PackedItem.objects.first()

        url = f'/items/{packed_item.id}'

        updated_packed_item = {
            "trip_id": self.trip.id,
            "item_name": "Updated Item",
            "quantity": 10
        }

        response = self.client.put(url, updated_packed_item, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        packed_item.refresh_from_db()

        self.assertEqual(
            updated_packed_item['item_name'], packed_item.item_name)
        self.assertEqual(updated_packed_item['quantity'], packed_item.quantity)

    def test_delete_packed_item(self):
        """Test delete PackedItem"""
        packed_item = PackedItem.objects.first()

        url = f'/items/{packed_item.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
