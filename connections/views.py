from django.contrib.auth.models import User
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from connections.models import FriendRequest
from connections.serializer import (
    FriendRequestSerializer,
    CreateFriendRequestSerializer,
    UpdateFriendRequestSerializer,
)
from user_account.serializers import UserSerializer


class FriendRequestViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and managing friend requests.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Retrieve a specific friend request by its ID.
        """
        try:
            return FriendRequest.objects.get(id=pk)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CreateFriendRequestSerializer,
        responses={
            status.HTTP_201_CREATED: FriendRequestSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiParameter(name='error', type=str, description='Error message')
        },
        description="Send a new friend request."
    )
    def create(self, request, *args, **kwargs):
        """
        Send a new friend request.
        """
        serializer = CreateFriendRequestSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            friend_request = serializer.save()
            return Response(
                FriendRequestSerializer(friend_request).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=UpdateFriendRequestSerializer,
        responses={
            status.HTTP_201_CREATED: FriendRequestSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiParameter(name='error', type=str, description='Error message')
        },
        description="Send a new friend request."
    )
    def update(self, request, *args, **kwargs):
        """
        Accept or reject a pending friend request.
        """
        friend_request = self.get_object(kwargs.get('pk'))
        if isinstance(friend_request, Response):  # Handle the case where friend request is not found
            return friend_request

        serializer = UpdateFriendRequestSerializer(
            friend_request,
            data=request.data, partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            updated_friend_request = serializer.save()
            return Response(FriendRequestSerializer(updated_friend_request).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status='accepted') |
            Q(received_requests__from_user=user, received_requests__status='accepted')
        ).distinct()


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')
