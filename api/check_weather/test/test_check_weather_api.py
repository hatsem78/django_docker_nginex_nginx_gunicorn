from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


WEATHER_FORECAST_URL_LIST = reverse("api:check_weather:list")


class PublicCheckWeatherApiTest(TestCase):
    """Test that the list Check Weather forecast 16th"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving Weather forecast for the city"""
        city = {'city': "buenos aires,ar"}

        res = self.client.get(WEATHER_FORECAST_URL_LIST, city)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateMeetupApiTest(TestCase):
    """Test the authorized user list Check Weather forecast 16th Api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_check_weather_city(self):
        """Test Weather forecast for the city"""
        city = {'city': "buenos aires,ar"}

        res = self.client.get(WEATHER_FORECAST_URL_LIST, city)

        dict_keys = ['date_day', 'date', 'temp', 'weather_description']

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(list(res.data[0].keys()), dict_keys)

    def test_check_weather_city_not_exist(self):
        """Test Weather forecast for the city"""
        city = {'city': "goodbye,ar"}

        res = self.client.get(WEATHER_FORECAST_URL_LIST, city)

        dict_keys = {'cod': '404', 'message': 'city not found'}

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, dict_keys)

