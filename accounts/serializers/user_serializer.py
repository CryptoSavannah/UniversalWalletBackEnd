from rest_framework import serializers
from ..models import User, Otp


class UserSerializer(serializers.ModelSerializer):
    """
    Model serializer for the User Model
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'prefix', 'location')

    #validation at the serializer, This should be refactored later.
    def validate_username(self, user):
        if len(user) != 9:
            raise serializers.ValidationError("username should be 9 characters")
        return user

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_client=True
        user.save()
        return user


class UserCreateSerializer(serializers.Serializer):
    phone_prefix = serializers.CharField(max_length=4)
    phone_number = serializers.CharField(max_length=9)
    first_name   = serializers.CharField(max_length=250)
    last_name    = serializers.CharField(max_length=250)
    location     = serializers.CharField(max_length=250)
    email        = serializers.CharField(max_length=250)
    pin_code     = serializers.IntegerField()


class UserSaveSerializer(serializers.ModelSerializer):
    """
    Save serializer for User details
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'prefix', 'username', 'email', 'location')

class UserShortDetailsSerializer(serializers.ModelSerializer):
    """
    Short Detail serializer for User
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'location', 'prefix', 'username')

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class OtpSerializer(serializers.ModelSerializer):
    """
    Save serializer for the OTP
    """
    class Meta:
        model = Otp
        fields = ('id', 'user' ,'otp_code')

class OtpVerificationSerializer(serializers.Serializer):
    phone_number    = serializers.CharField(max_length=9)
    otp             = serializers.IntegerField()
