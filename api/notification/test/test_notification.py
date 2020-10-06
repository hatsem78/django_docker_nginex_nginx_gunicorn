from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from api.notification.serializers import NotificationSerializers
from core.models import Meetup, Notification
from api.meetup.serializers import MeetupSerializers


NOTIFICATION_URL_LIST = reverse("api:notification:list")
NOTFICATION_URL_CREATE = reverse("api:notification:create")


def sample_notification(user=None, text=None):
    """Create a sample meetup"""
    notirication = Notification.objects.create(
        user=user,
        text=text,
    )

    return notirication


def sample_user(email='test@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class PublicNotificationApiTest(TestCase):
    """Test that publicly available notification Api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving notification"""
        res = self.client.get(NOTIFICATION_URL_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateNotificationTest(TestCase):
    """Test private meetup_enroll_invite_users api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test3@gmail.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_notification(self):
        """Test retrieving a list of notification """

        sample_notification(user=self.user, text='ghjhgjkhgjfgfdgfdf')

        res = self.client.get(NOTIFICATION_URL_LIST)

        notification = Notification.objects.all().order_by('-user')

        serializers = NotificationSerializers(notification, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['data'], serializers.data)

    def test_create_notification(self):
        """Test creating a new notification"""

        payload = {
            'date': '2020-01-02 00:00:00',
            'user': self.user.pk,
            'text': 'Description Meetup2',
            'is_seen': True,
            'is_read': True,
        }

        self.client.post(NOTFICATION_URL_CREATE, payload)

        exists = Notification.objects.filter(
            user=self.user
        ).exists()

        self.assertTrue(exists)

    def test_notification_limited_to_user(self):
        """Test that notification for the authenticated user are returned"""
        user = sample_user(email='test4@gmail.com')

        notification = sample_notification(user=user, text='hhhhhhhhhh')

        res = self.client.get(NOTIFICATION_URL_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['data'][0]['user_name'], notification.user.name)

    def test_list_page_notification_users(self):
        """Test list page the notification"""

        user = sample_user(email='test4@gmail.com')

        sample_notification(user=user, text='hhhhhhhhhh')

        payload = {
            'sort': 'id|desc',
            'page': 1,
            'per_page': 3,
            'filter': "hhhhhhhhhh"
        }

        MEETUP_PAGE_URL = reverse('api:notification:list_page')

        res = self.client.get(MEETUP_PAGE_URL, payload)
        obj = res

        self.assertEqual(obj.data['data'][0]['text'], payload['filter'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def tests_update_notification_users(self):
        """Test that updating of notification """

        user = sample_user(email='test7@gmail.com')

        meetup_user = Notification.objects.create(
            user=user,
            text='kkkkkkkkkkkk',
        )

        payload = {
            'user': user.pk,
            'text': 'llllllllllllllllllllllll'
        }

        NOTIFICATION_URL_UPDATE = reverse(
            'api:notification:update', kwargs={'pk': meetup_user. pk}
        )

        res = self.client.put(NOTIFICATION_URL_UPDATE, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(int(res.data['id']), meetup_user.pk)

    def tests_update_notification_is_seen_users(self):
        """Test that updating of notification is seen user"""

        user = sample_user(email='test7@gmail.com')

        meetup_user = Notification.objects.create(
            user=user,
            date='2020-01-01',
            text='kkkkkkkkkkkk',
            is_seen=True
        )

        payload = {
            'user': user.pk,
            'text': 'llllllllllllllllllllllll',
            'is_seen': True,
            'is_read': False
        }

        NOTIFICATION_URL_UPDATE = reverse(
            'api:notification:update', kwargs={'pk': meetup_user. pk}
        )

        res = self.client.put(NOTIFICATION_URL_UPDATE, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(int(res.data['id']), meetup_user.pk)

    def tests_update_notification_is_read_users(self):
        """Test that updating of notification is read user"""

        user = sample_user(email='test7@gmail.com')

        meetup_user = Notification.objects.create(
            user=user,
            date='2020-01-01',
            text='kkkkkkkkkkkk',
            is_seen=True,
            is_read=True
        )

        payload = {
            'user': user.pk,
            'text': 'llllllllllllllllllllllll',
            'is_seen': True,
            'is_read': True
        }

        NOTIFICATION_URL_UPDATE = reverse(
            'api:notification:update', kwargs={'pk': meetup_user. pk}
        )

        res = self.client.put(NOTIFICATION_URL_UPDATE, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(int(res.data['id']), meetup_user.pk)


