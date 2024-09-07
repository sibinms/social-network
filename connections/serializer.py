from django.contrib.auth.models import User
from rest_framework import serializers

from connections.models import FriendRequest
from user_account.serializers import UserSerializer


class CreateFriendRequestSerializer(serializers.Serializer):
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    def validate_to_user(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("Cannot send friend request to yourself.")
        return value

    def create(self, validated_data):
        from_user = self.context['request'].user
        to_user = validated_data['to_user']

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
            status='pending'
        )
        if not created:
            raise serializers.ValidationError("Friend request already sent.")
        return friend_request


class UpdateFriendRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'reject'], required=True)

    def update(self, instance, validated_data):
        action = validated_data['action']
        if action == 'accept':
            instance.status = 'accepted'
        elif action == 'reject':
            instance.status = 'rejected'
        else:
            raise serializers.ValidationError("Invalid action.")
        instance.save()
        return instance


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status']
        read_only_fields = ['from_user', 'status']
