from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_meetup():
    """Create a sample meetup"""
    meetup = models.Meetup.objects.create(
        date='2020-01-01',
        name='Meetup Beer',
        description='Description Meetup',
        count_beer=36,
        maximum_temperature=30.0,
        count_participants=10,
        direction="Avenida siempre viva 223"
    )
    return meetup


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = "Testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with not email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
            """Test creating a new superuser"""
            user = get_user_model().objects.create_superuser(
                'test@londonappdev.com',
                'test123'
            )

            self.assertTrue(user.is_superuser)
            self.assertTrue(user.is_staff)

    def test_new_meetup(self):
        """Test new meetup for group beer"""

        meetup = models.Meetup.objects.create(
            user=sample_user(),
            date='2020-01-01',
            name='Meetup Beer',
            description='Description Meetup',
            count_beer=36,
            maximum_temperature=30.0,
            count_participants=10,
            direction="Avenida siempre viva 223"
        )

        self.assertEqual(str(meetup), meetup.name)

    def test_meetup_enroll_invite_users(self):
        """Test create new meetup enrroll or invite users"""
        user = sample_user(email='test2@gmail.com')
        meetup = models.MeetupEnrollInviteUsers.objects.create(
            user=user,
            meetup=sample_meetup(),
        )

        self.assertEqual(meetup.user, user)

    def test_new_nofication(self):
        """Test new notification """
        user = sample_user(email='test2@gmail.com')

        notirication = models.Notification.objects.create(
            user=user,
            text='asdfasdfasd',
        )

        self.assertEqual(notirication.user, user)
