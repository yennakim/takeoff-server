from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from takeoffapi.models import Traveler
from takeoffapi.views.traveler import TravelerSerializer

class TravelerTests(APITestCase):

    fixtures = ['traveler']

    def setUp(self):
        self.traveler = Traveler.objects.first()

    def test_create_traveler(self):
        """Create traveler test"""
        url = "/traveler"

        traveler = {
            "first_name": "Tres",
            "last_name": "Leches",
            "image": "https://www.lemonblossoms.com/wp-content/uploads/2023/03/Tres-Leches-Cake-S2.jpg"
        }

        response = self.client.post(url, traveler, format='json')

        new_traveler = Traveler.objects.last()

        expected = TravelerSerializer(new_traveler)

        self.assertEqual(expected.data, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
    def test_get_traveler(self):
        """Get Traveler Test"""
        # Grab a traveler object from the database
        traveler = Traveler.objects.first()

        url = f'/traveler/{traveler.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected = TravelerSerializer(traveler)

        self.assertEqual(expected.data, response.data)

    def test_list_travelers(self):
        """Test list travelers"""
        url = '/traveler'

        response = self.client.get(url)

        all_travelers = Traveler.objects.all()
        expected = TravelerSerializer(all_travelers, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

    def test_change_traveler(self):
        """Test update traveler"""
        traveler = Traveler.objects.first()

        url = f'/traveler/{traveler.id}'

        updated_traveler = {
            "first_name": f'{traveler.first_name} updated',
            "last_name": traveler.last_name,
            "image": traveler.image,
        }

        response = self.client.put(url, updated_traveler, format='json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        traveler.refresh_from_db()

        self.assertEqual(updated_traveler['first_name'], traveler.first_name)

    def test_delete_traveler(self):
        """Test delete traveler"""
        traveler = Traveler.objects.first()

        url = f'/traveler/{traveler.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
