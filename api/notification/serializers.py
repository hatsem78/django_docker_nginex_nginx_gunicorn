from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from core.models import Notification
from datetime import datetime


class NotificationSerializers(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = Notification
        fields = ("id", "user", "user_name", "text", "date", "is_seen", "is_read")

        read_only_fields = ('id',)

    def create(self, validated_data):
        """
            Create and return a new `Meetup` instance, given the validated data.
        """
        trans = Notification.objects.create(**validated_data)

        return trans

    def update(self, instance, validated_data):
        """
            Update and return an existing `Meetup` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        if 'date' in validated_data:
            instance.date = validated_data.get('date', instance.date.strftime('YYYY-MM-DDThh:mm'))
        else:
            instance.date = datetime.strptime(str(datetime.now())[:19], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
        instance.text = validated_data.get('text', instance.text)
        instance.is_seen = validated_data.get('is_seen', instance.is_seen)
        instance.is_read = validated_data.get('is_read', instance.is_read)

        instance.save()
        return instance
