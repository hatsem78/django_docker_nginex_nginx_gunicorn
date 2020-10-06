from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


from rest_framework import status
from rest_framework.test import APIClient

from core.models import MeetupEnrollInviteUsers, Meetup





def sample_user(email='test@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_meetup(name='Meetup Beer', user=None):
    """Create a sample meetup"""
    meetup = Meetup.objects.create(
        user=user,
        date='2020-01-01',
        name=name,
        description='Description Meetup',
        count_beer=36,
        maximum_temperature=30.0,
        count_participants=10,
        direction="Avenida siempre viva 223"
    )
    return meetup


class TestRegistrationUserMeetup(TestCase):
    """Test registration user and check in meetup"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test3@gmail.com',
            password='testpass',
            name='fname',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_registration_user_meetup_successful(self):
        """Test registragion user in one meetup"""

        meetup = sample_meetup(name='Meetup Beer12', user=self.user)

        payload = {
            'user': self.user.pk,
            'meetup': meetup.pk,
            'user_check_in': True
        }

        REGISTRATION_USER_URL = reverse(
            'api:registration_check_in_user:registration'
        )

        res = self.client.post(REGISTRATION_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(int(res.data['user']), self.user.pk)

    def tests_check_in_meetup_successful(self):
        """Test that check in meetup """

        meetup = sample_meetup(name='Meetup Beer7', user=self.user)

        meetup_user = MeetupEnrollInviteUsers.objects.create(
            user=self.user,
            meetup=meetup,
        )

        payload = {
            'user': self.user.pk,
            'meetup': meetup.pk,
            'user_check_in': True
        }

        CHECK_IN_URL_UPDATE = reverse(
            'api:meetup_enroll_invite_users:update', kwargs={'pk': meetup_user. pk}
        )

        res = self.client.put(CHECK_IN_URL_UPDATE, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(int(res.data['id']), meetup_user.pk)
