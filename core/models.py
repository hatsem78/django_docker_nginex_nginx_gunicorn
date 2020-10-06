import json
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.urls import reverse


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

        """Custom user model that supports using email instead of username"""
        email = models.EmailField(max_length=255, unique=True)
        name = models.CharField(max_length=255)
        department = models.CharField(max_length=255, blank=True)
        last_name = models.CharField(max_length=255, blank=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        objects = UserManager()

        USERNAME_FIELD = 'email'

        def save(self, *args, **kwargs):
            super().save(*args, **kwargs)


class Meetup(models.Model):

    """Meetup to be used for users"""

    class Meta:
        verbose_name_plural = "Meetup"

    user = models.ForeignKey('User', related_name='User_Meetup', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date start Meetup")
    description = models.TextField(blank=True)
    count_beer = models.IntegerField(default=0, help_text="quantity of beer expressed in boxes of 6 units")
    count_box_beer = models.IntegerField(default=0, help_text="Count Box beer")
    maximum_temperature = models.FloatField(default=0, blank=True, help_text="Maximum Temperature")
    count_participants = models.IntegerField(default=0, help_text="Count Participants")
    direction = models.CharField(max_length=380)

    def __str__(self):
        return self.name


class MeetupEnrollInviteUsers(models.Model):

    class Meta:
        verbose_name_plural = "Meetup Enroll InviteUsers"
        unique_together = ('user', 'meetup',)

    id = models.AutoField(primary_key=True, help_text="Unique id")

    user = models.ForeignKey('User', related_name='User_MeetupEnrollInviteUsers', on_delete=models.CASCADE, null=True)
    meetup = models.ForeignKey('Meetup', related_name='Meetup_MeetupEnrollInviteUsers', on_delete=models.CASCADE, null=True)
    user_check_in = models.BooleanField(default=False)

    def user_name(self):
        return self.user.name

    def user_email(self):
        return self.user.email

    def meetup_name(self):
        return self.meetup.name

    def meetup_date(self):
        return self.meetup.date

    def meetup_direction(self):
        return self.meetup.direction

    def meetup_description(self):
        return self.meetup.description


class Notification(models.Model):
    class Meta:
        verbose_name_plural = "Notification"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User_Notification', related_name='notifications')
    text = models.TextField(blank=False)
    date = models.DateTimeField(default=datetime.datetime.now, blank=False)
    is_seen = models.BooleanField(default=False)
    is_read = models.BooleanField( default=False)

    __data = None

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('notifications:notification_detail', kwargs={'pk': self.pk})

    def user_name(self):
        return self.user.name

    @property
    def data(self):
        if self.__data is None:
            self.__data = json.loads(self.text)
        return self.__data

