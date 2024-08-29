from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from takeoffapi.models import TripTraveler, Trip, Traveler, User
from takeoffapi.views.trip_traveler import TripTravelerSerializer


class TripTravelerTests(APITestCase):

    fixtures = ['user', 'traveler', 'trip', 'trip_traveler']

    def setUp(self):
        self.user = User.objects.first()

    def test_get_trip_traveler(self):
        """Get Trip Traveler Test"""
        trip_traveler = TripTraveler.objects.first()

        url = f'/trip_traveler/{trip_traveler.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = TripTravelerSerializer(trip_traveler)

        self.assertEqual(expected.data, response.data)

    def test_list_trip_travelers(self):
        """Test list trip travelers"""
        url = '/trip_traveler'

        response = self.client.get(url)

        all_trip_travelers = TripTraveler.objects.all()
        expected = TripTravelerSerializer(all_trip_travelers, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_add_traveler(self):
        """Test add traveler to trip"""
        trip = Trip.objects.get(pk=1)
        traveler = Traveler.objects.get(pk=2)

        url = f'/trip/{trip.id}/add_traveler'

        data = {
            "trip_id": trip.id,
            "traveler_id": traveler.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        try:
            if response.status_code == status.HTTP_201_CREATED:
                trip_traveler = TripTraveler.objects.get(
                    trip=trip, traveler=traveler)
                self.assertIsNotNone(trip_traveler)
            else:
                print(f"Error response: {response.data}")

        except TripTraveler.DoesNotExist:
            print("TripTraveler object was not created.")

    def test_remove_traveler(self):
        """Test remove traveler from trip"""
        trip = Trip.objects.first()
        traveler = Traveler.objects.first()
        TripTraveler.objects.create(trip=trip, traveler=traveler)

        url = f'/trip/remove_traveler'

        data = {
            "trip_id": trip.id,
            "traveler_id": traveler.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Check if the TripTraveler object was deleted
        self.assertFalse(TripTraveler.objects.filter(
            trip=trip, traveler=traveler).exists())

    def test_remove_nonexistent_traveler(self):
        """Test removing a traveler that doesn't exist in the trip"""
        trip = Trip.objects.first()
        traveler = Traveler.objects.create(first_name="Test", last_name="User")

        url = '/trip/remove_traveler/'
        data = {
            "trip_id": trip.id,
            "traveler_id": traveler.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_display_travelers(self):
        """Test display travelers for a trip"""
        trip = Trip.objects.first()
        url = f'/trip/{trip.id}/display_travelers'

        response = self.client.post(url, data={}, format='json')
        trip_travelers = TripTraveler.objects.filter(trip=trip)

        expected_data = []
        for trip_traveler in trip_travelers:
            traveler_data = {
                'id': trip_traveler.id,  # Keep this for TripTraveler object
                'trip_id': trip_traveler.trip.id,  # Keep this for TripTraveler object
                'traveler': {
                    'id': trip_traveler.traveler.id,
                    'first_name': trip_traveler.traveler.first_name,
                    'last_name': trip_traveler.traveler.last_name,
                    'image': trip_traveler.traveler.image,
                }
            }
            expected_data.append(traveler_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
