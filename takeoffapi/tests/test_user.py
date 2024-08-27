from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from takeoffapi.models import User
from takeoffapi.views import UserSerializer


class UserTests(APITestCase):

  fixtures = ['user']

  def setUp(self):
      # Create a sample User for testing
      self.user = User.objects.first()

  def test_create_user(self):
      """Create user test"""
      url = "/user"

      # Define the User properties
      user= {
          "first_name": "Tres",
          "last_name": "Leches",
          "image": "https://www.lemonblossoms.com/wp-content/uploads/2023/03/Tres-Leches-Cake-S2.jpg",
          "email": "tres@leches.com",
          "uid": "3333"
      }

      response = self.client.post(url, user, format='json')
      # Get the last user added to the database, it should be the one just created
      new_user = User.objects.last()

      # Use the serializer to serialize the "new_user"
      expected = UserSerializer(new_user)

      # Assert that the expected output matches the actual response
      self.assertEqual(expected.data, response.data)

  def test_get_user(self):
      """Get user test"""
      url = f'/user/{self.user.id}'

      response = self.client.get(url)

      self.assertEqual(status.HTTP_200_OK, response.status_code)

      # Run the user through the serializer that's being used in view
      expected = UserSerializer(self.user)

      # Assert that the response matches the expected return data
      self.assertEqual(expected.data, response.data)

  def test_list_users(self):
        """List users test"""
        url = '/user'

        response = self.client.get(url)
        
        # Get all the users in the database and serialize them to get the expected output
        all_users = User.objects.all()
        expected = UserSerializer(all_users, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected.data, response.data)

  def test_update_user(self):
      """Update user test"""
      url = f'/user/{self.user.id}'

      updated_user = {
          "first_name": "John Updated",
          "last_name": self.user.last_name,
          "image": self.user.image,
          "email": self.user.email,
          "uid": self.user.uid,
      }

      response = self.client.put(url, updated_user, format='json')

      self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

      # Refresh the user object to reflect any changes in the database
      self.user.refresh_from_db()

      # Assert that the updated value matches
      self.assertEqual(updated_user['first_name'], self.user.first_name)

  def test_delete_user(self):
      """Delete user test"""
      url = f'/user/{self.user.id}'
      response = self.client.delete(url)

      self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

      # Test that it was deleted by trying to get the user
      response = self.client.get(url)
      self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
