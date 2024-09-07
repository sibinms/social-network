from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class EmailAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Email"),
        write_only=True,
        validators=[EmailValidator(message=_("Enter a valid email address."))]
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class EmailSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        label=_("Email"),
        write_only=True,
        validators=[EmailValidator(message=_("Enter a valid email address."))]
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, attrs):
        # Check that passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        return attrs

    def create(self, validated_data):
        # Remove password2 as it's not needed for creating the user
        password = validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Create and return token
        token, _ = Token.objects.get_or_create(user=user)
        return {
            'username': user.username,
            'token': token.key
        }
