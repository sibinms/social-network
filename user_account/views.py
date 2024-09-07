from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .pagination import UserSearchPagination
from .serializers import EmailAuthTokenSerializer, EmailSignupSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class EmailLoginAPIView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer


class EmailSignupAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({
                'username': data['username'],
                'token': data['token']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserSearchPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '')
        if not keyword:
            return User.objects.none()  # Return empty queryset if no keyword provided

        # Search for users by email or name
        users_with_email_match = User.objects.filter(Q(username__iexact=keyword))
        if users_with_email_match.exists():
            return users_with_email_match

        return User.objects.filter(
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword)
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
