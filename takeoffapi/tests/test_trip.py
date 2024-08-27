from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from takeoffapi.models import Trip, User
from takeoffapi.views import TripSerializer

class TripTests(APITestCase):

    fixtures = ['user', 'trip', 'boarding_pass', 'lodging', 'packed_item', 'traveler', 'trip_traveler']

    def setUp(self):
        # Grab the first User object from the database
        self.user = User.objects.first()

    def test_create_trip(self):
        """Create trip test"""
        url = "/trip"

        # Define the Trip properties
        trip = {
            "user_id": self.user.id,
            "trip_name": "Paris",
            "origin": "BNA",
            "destination": "CDG",
            "start_date": "2024-10-01",
            "end_date": "2024-10-10"
        }

        response = self.client.post(url, trip, format='json')

        # Get the last trip added to the database
        new_trip = Trip.objects.last()

        expected = TripSerializer(new_trip)

        self.assertEqual(expected.data, response.data)

    def test_get_trip(self):
        """Get trip test"""
        trip = Trip.objects.first()

        url = f'/trip/{trip.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = TripSerializer(trip)

        self.assertEqual(expected.data, response.data)

    def test_list_trips(self):
        """List trips test"""
        url = '/trip'

        response = self.client.get(url)

        all_trips = Trip.objects.all()
        expected = TripSerializer(all_trips, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_update_trip(self):
        """Update trip test"""
        trip = Trip.objects.first()

        url = f'/trip/{trip.id}'

        updated_trip = {
            "user_id": self.user.id,
            "trip_name": f'{trip.trip_name} updated',
            "origin": trip.origin,
            "destination": trip.destination,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
        }

        response = self.client.put(url, updated_trip, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        trip.refresh_from_db()

        self.assertEqual(updated_trip['trip_name'], trip.trip_name)

    def test_delete_trip(self):
        """Delete trip test"""
        trip = Trip.objects.first()

        url = f'/trip/{trip.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
