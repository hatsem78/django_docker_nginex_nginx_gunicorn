from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from core.models import Meetup


class MeetupSerializers(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = Meetup
        fields = (
            "id",
            "name",
            "date",
            "description",
            "count_beer",
            "count_box_beer",
            "maximum_temperature",
            "count_participants",
            "direction"
        )

        read_only_fields = ('id',)

    def create(self, validated_data):
        """
            Create and return a new `Meetup` instance, given the validated data.
        """
        trans = Meetup.objects.create(**validated_data)

        return trans

    def update(self, instance, validated_data):
        """
            Update and return an existing `Meetup` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date.strftime('YYYY-MM-DDThh:mm'))
        instance.description = validated_data.get('description', instance.description)
        instance.count_beer = validated_data.get('count_beer', instance.count_beer)
        instance.maximum_temperature = validated_data.get('maximum_temperature', instance.maximum_temperature)
        instance.count_participants = validated_data.get('count_participants', instance.count_participants)
        instance.direction = validated_data.get('direction', instance.direction)

        instance.save()
        return instance
