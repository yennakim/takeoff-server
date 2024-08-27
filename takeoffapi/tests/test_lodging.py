from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from takeoffapi.models import Lodging, Trip
from takeoffapi.views.lodging import LodgingSerializer

class LodgingTests(APITestCase):
    fixtures = ['user','trip', 'lodging']

    def setUp(self):
        # Grab the first Trip object from the database
        self.trip = Trip.objects.first()

    def test_create_lodging(self):
        """Create lodging test"""
        url = "/lodging"

        lodging = {
            "trip_id": self.trip.id,
            "address": "123 Gordon Ramsay St",
            "city": "London",
            "length_of_stay": 4
        }

        response = self.client.post(url, lodging, format='json')

        new_lodging = Lodging.objects.last()

        expected = LodgingSerializer(new_lodging)

        self.assertEqual(expected.data, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_get_lodging(self):
        """Get Lodging Test"""
        lodging = Lodging.objects.first()

        url = f'/lodging/{lodging.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = LodgingSerializer(lodging)

        self.assertEqual(expected.data, response.data)

    def test_list_lodgings(self):
        """Test list lodgings"""
        url = '/lodging'

        response = self.client.get(url)
        
        all_lodgings = Lodging.objects.all()
        expected = LodgingSerializer(all_lodgings, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_lodging(self):
        """Test update lodging"""
        lodging = Lodging.objects.first()

        url = f'/lodging/{lodging.id}'

        updated_lodging = {
            "trip_id": lodging.trip.id,
            "address": "456 Fleet Street",
            "city": lodging.city,
            "length_of_stay": lodging.length_of_stay + 1
        }

        response = self.client.put(url, updated_lodging, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        lodging.refresh_from_db()

        self.assertEqual(updated_lodging['address'], lodging.address)
        self.assertEqual(updated_lodging['length_of_stay'], lodging.length_of_stay)

    def test_delete_lodging(self):
        """Test delete lodging"""
        lodging = Lodging.objects.first()

        url = f'/lodging/{lodging.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
