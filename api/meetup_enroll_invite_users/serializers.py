from rest_framework import serializers

from api.common import CalculateBeer
from core.models import Meetup, MeetupEnrollInviteUsers, Notification, User


class MeetupEnrollInviteUsersSerializers(serializers.ModelSerializer):
    """Serializer for the MeetupEnrollInviteUsers object"""

    class Meta:
        model = MeetupEnrollInviteUsers
        fields = (
            'id',
            "user",
            "user_name",
            "user_email",
            "meetup",
            "meetup_name",
            "meetup_date",
            "meetup_direction",
            "meetup_description",
        )

        read_only_fields = ('id',)

    def create(self, validated_data):
        """
            Create and return a new `Meetup` instance, given the validated data.
        """
        trans = MeetupEnrollInviteUsers.objects.create(**validated_data)
        calcule_beer = CalculateBeer(validated_data['meetup'].id)
        trans.meetup = calcule_beer.calculate_count_beer()

        return trans

    def update(self, instance, validated_data):
        """
            Update and return an existing `Meetup` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.meetup = validated_data.get('meetup', instance.meetup)
        instance.user_check_in = validated_data.get('user_check_in', instance.user_check_in)

        instance.save()
        return instance

    def __registre_notification(self, request, trans):
        if not request['user'].is_superuser:

            user = User.objects.filter(id=trans.meetup.user_id)

            Notification.objects.create(
                user=user,
                date='2020-01-01',
                text=f"El usuario {request['user'].email} se registro en la  meetup {trans.meetup.name}",
                is_seen=True,
                is_read=True
            )

        else:

            Notification.objects.create(
                user=request['user'],
                date='2020-01-01',
                text=f"El usuario {request['user'].email} se registro en la  meetup {trans.meetup.name}",
                is_seen=True,
                is_read=True
            )