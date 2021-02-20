"""Serializers module"""
from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room Class converts Model into a JSON Object"""
    class Meta:
        """Define what fields can be sended and visible from Room Model"""
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause',
                  'votes_to_skip', 'created_at')


class CreateRoomSerializer(serializers.ModelSerializer):
    """"Create a Room Model and save it into DB"""
    class Meta:
        """Define what fields are requested to Create a Room """
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    """"Update a Room Model and save it into DB"""

    code = serializers.CharField(validators=[])

    class Meta:
        """Define what fields are requested to Create a Room """
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')
