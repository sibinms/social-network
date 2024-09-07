from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import EmailAuthTokenSerializer, EmailSignupSerializer
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
