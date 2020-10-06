from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from core.models import  Meetup
from api.meetup.serializers import MeetupSerializers


MEETUP_URL_LIST = reverse("api:meetup:list")
MEETUP_URL_CREATE = reverse("api:meetup:create")


class PublicMeetupApiTest(TestCase):
    """Test that publicly available Meetups Api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving Meetups"""
        res = self.client.get(MEETUP_URL_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateMeetupApiTest(TestCase):
    """Test the authorized user Meetups Api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_meetup(self):
        """Test retrieve meetups"""

        Meetup.objects.create(
            date='2020-01-01 00:00:00',
            name='Meetup Beer',
            description='Description Meetup',
            count_beer=36,
            maximum_temperature=30.0,
            count_participants=10,
            direction="Avenida siempre viva 223"
        )

        res = self.client.get(MEETUP_URL_LIST)

        meettup = Meetup.objects.all().order_by("-name")

        serializers = MeetupSerializers(meettup, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        obj = serializers.data

        self.assertEqual(res.data[0]['date'], obj[0]['date'])

    def test_create_meetup(self):
        """Test creating a new meetup"""

        payload = {
            'user': self.user.pk,
            'date': '2020-01-02 00:00:00',
            'name': 'Meetup Beer2',
            'description': 'Description Meetup2',
            'count_beer': 36,
            'maximum_temperature': 30.0,
            'count_participants': 10,
            'direction': "Avenida siempre viva 225"
        }

        self.client.post(MEETUP_URL_CREATE, payload)

        exists = Meetup.objects.filter(
            name='Meetup Beer2'
        ).exists()

        self.assertTrue(exists)

    def test_create_meetup_invalid(self):
        """Test creating a new meetup with invalid payload"""
        payload = {
            'date': '2020-01-02 00:00:00',
            'name': '',
            'description': 'Description Meetup2',
            'count_beer': 36,
            'maximum_temperature': 30.0,
            'count_participants': 10,
            'direction': "Avenida siempre viva 225"
        }

        res = self.client.post(MEETUP_URL_CREATE, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_meetup(self):
        """Test updating the meetup"""
        meetup = Meetup.objects.create(
            date='2020-01-01 00:00:00',
            name='Meetup Beer 3',
            description='Description Meetup',
            count_beer=36,
            maximum_temperature=30.0,
            count_participants=10,
            direction="Avenida siempre viva 223"
        )

        MEETUP_URL_UPDATE = reverse('api:meetup:update', kwargs={'pk': meetup.pk})

        payload = {
            'name': 'new name',
            'description': 'New Description Meetup2',
            'date': '2020-01-01 00:00:00',
            'direction': "Avenida siempre viva 223"
        }

        res = self.client.put(MEETUP_URL_UPDATE, payload)
        obj = res

        self.assertEqual(obj.data['name'], payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_meetup(self):
        """Test delete the meetup"""
        meetup = Meetup.objects.create(
            date='2020-01-01 00:00:00',
            name='Meetup Beer 3',
            description='Description Meetup',
            count_beer=36,
            maximum_temperature=30.0,
            count_participants=10,
            direction="Avenida siempre viva 223"
        )

        MEETUP_URL_DELETE = reverse('api:meetup:delete', kwargs={'pk': meetup.pk})

        res = self.client.delete(MEETUP_URL_DELETE)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_page_meetup(self):
        """Test lsit page the meetup"""
        meetup = Meetup.objects.create(
            date='2020-01-01 00:00:00',
            name='Meetup Beer 3',
            description='Description Meetup',
            count_beer=36,
            maximum_temperature=30.0,
            count_participants=10,
            direction="Avenida siempre viva 223"
        )
        payload = {
            'sort': 'id|desc',
            'page': 1,
            'per_page': 3,
            'filter': "Avenida siempre viva 223"
        }

        MEETUP_PAGE_URL = reverse('api:meetup:list_page')

        res = self.client.get(MEETUP_PAGE_URL, payload)
        obj = res

        self.assertEqual(obj.data['data'][0]['direction'], payload['filter'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)










