# Generated by Django 3.1.2 on 2020-10-02 02:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetupenrollinviteusers',
            name='meetup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Meetup_MeetupEnrollInviteUsers', to='core.meetup'),
        ),
        migrations.AlterField(
            model_name='meetupenrollinviteusers',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='User_MeetupEnrollInviteUsers', to=settings.AUTH_USER_MODEL),
        ),
    ]
