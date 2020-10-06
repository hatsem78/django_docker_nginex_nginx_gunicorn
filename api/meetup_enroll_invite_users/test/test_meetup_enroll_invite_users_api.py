from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import MeetupEnrollInviteUsers, Meetup

from api.meetup_enroll_invite_users.serializers import MeetupEnrollInviteUsersSerializers

MEETUP_ENRLL_INVITE_USER_URL_LIST = reverse("api:meetup_enroll_invite_users:list")
MEETUP_ENRLL_INVITE_USER_URL_PAGE_URL = reverse('api:meetup_enroll_invite_users:list_page')
MEETUP_ENRLL_INVITE_USER_URL_CREATE = reverse("api:meetup_enroll_invite_users:create")


def sample_user(email='test@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_meetup(name='Meetup Beer'):
    """Create a sample meetup"""
    meetup = Meetup.objects.create(
        user=sample_user(),
        date='2020-01-01',
        name=name,
        description='Description Meetup',
        count_beer=36,
        maximum_temperature=30.0,
        count_participants=10,
        direction="Avenida siempre viva 223"
    )
    return meetup


class PublicMeetupEnrollInviteUsersTest(TestCase):
    """Test publicly available meetup enroll or invite users """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to accss the endpint"""

        res = self.client.get(MEETUP_ENRLL_INVITE_USER_URL_LIST)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateMeetupEnrollInviteUsersTest(TestCase):
    """Test private meetup_enroll_invite_users api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test3@gmail.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_meetup_enroll_invite_users(self):
        """Test retrieving a list of meetup_enroll_invite_users"""
        meetup = Meetup.objects.create(
            user=self.user,
            date='2020-01-01',
            name='Meetup Beer',
            description='Description Meetup',
            count_beer=36,
            maximum_temperature=30.0,
            count_participants=10,
            direction="Avenida siempre viva 223"
        )

        meetup = MeetupEnrollInviteUsers(
            user=self.user,
            meetup=meetup,
        )

        res = self.client.get(MEETUP_ENRLL_INVITE_USER_URL_LIST)

        meetup_enroll_invite_users = MeetupEnrollInviteUsers.objects.all().order_by('-user')

        serializers = MeetupEnrollInviteUsersSerializers(meetup_enroll_invite_users, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.data)

    def test_enroll_invite_users_limited_to_user(self):
        """Test that enroll_invite_users for the authenticated user are returned"""
        user = sample_user(email='test4@gmail.com')

        meetup = sample_meetup()

        meetup = MeetupEnrollInviteUsers.objects.create(
            user=user,
            meetup=meetup,
        )

        res = self.client.get(MEETUP_ENRLL_INVITE_USER_URL_LIST)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['user_name'], meetup.user.name)

    def test_list_page_enroll_invite_users(self):
        """Test lsit page the meetup"""

        user = sample_user(email='test4@gmail.com')

        meetup = sample_meetup()

        meetup = MeetupEnrollInviteUsers.objects.create(
            user=user,
            meetup=meetup,
        )

        res = self.client.get(MEETUP_ENRLL_INVITE_USER_URL_PAGE_URL)
        obj = res

        self.assertEqual(obj.data['data'][0]['user'], meetup.user_id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def tests_create_enroll_invite_users(self):
        """Test that creating of enroll_invite_users """

        user = sample_user(email='test5@gmail.com')

        meetup = sample_meetup(name='Meetup Beer2')

        payload = {
            'user': user.pk,
            'meetup': meetup.pk,
        }

        res = self.client.post(MEETUP_ENRLL_INVITE_USER_URL_CREATE, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(res.data['user']), user.pk)

    def tests_update_enroll_invite_users(self):
        """Test that updateing of enroll_invite_users """

        user = sample_user(email='test7@gmail.com')

        meetup = sample_meetup(name='Meetup Beer7')

        meetup_user = MeetupEnrollInviteUsers.objects.create(
            user=user,
            meetup=meetup,
        )

        payload = {
            'user': user.pk,
            'meetup': meetup.pk,
            'user_check_in': True
        }

        MEETUP_ENRLL_INVITE_USER_URL_UPDATE = reverse(
            'api:meetup_enroll_invite_users:update', kwargs={'pk': meetup_user. pk}
        )

        res = self.client.put(MEETUP_ENRLL_INVITE_USER_URL_UPDATE, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(int(res.data['id']), meetup_user.pk)

    def test_delete_enroll_invite_users(self):
        """Test delete the update_enroll_invite_users"""

        user = sample_user(email='test7@gmail.com')

        meetup = sample_meetup(name='Meetup Beer7')

        meetup_user = MeetupEnrollInviteUsers.objects.create(
            user=user,
            meetup=meetup,
        )

        MEETUP_ENRLL_INVITE_USER_URL_DELETE = reverse('api:meetup_enroll_invite_users:update',
                                                      kwargs={'pk': meetup_user.pk})

        res = self.client.delete(MEETUP_ENRLL_INVITE_USER_URL_DELETE)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
