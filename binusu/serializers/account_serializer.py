from rest_framework import serializers
from ..models import AccountUser, UserLogins, UserRefreshOtp


class UserDataSerializer(serializers.Serializer):
    first_name             =   serializers.CharField(max_length=250)
    last_name              =   serializers.CharField(max_length=250)
    email_address          =   serializers.CharField(max_length=250)
    password               =   serializers.CharField(max_length=250)
    role                   =   serializers.IntegerField()

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for user creation
    """
    class Meta:
        model = AccountUser
        fields = ('first_name', 'last_name', 'email_address', 'password', 'role', 'account_status')

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Model serializer for user details
    """
    class Meta:
        model = AccountUser
        fields = ('first_name', 'last_name', 'email_address', 'role')

class UserLoginsCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for user logins creation
    """
    class Meta:
        model = UserLogins
        fields = ('related_user', 'last_login', 'last_token')

class UserRefreshOtpCreateSerializer(serializers.ModelSerializer):
    """
    Model serializer for user refresh otps
    """
    class Meta:
        model = UserRefreshOtp
        fields = ('related_user', 'refresh_otp', 'token_expiry')

class UserLoginSerializer(serializers.Serializer):
    email_address        =   serializers.CharField(max_length=250)
    password             =   serializers.CharField(max_length=250)

class UserOtpConfirmSerializer(serializers.Serializer):
    email_address        =   serializers.CharField(max_length=250)
    password             =   serializers.CharField(max_length=250)
    otp                  =   serializers.CharField(max_length=4)

class UserTokenSerializer(serializers.Serializer):
    user_id             = serializers.IntegerField()
    email_address       =   serializers.CharField(max_length=250)
    first_name          =   serializers.CharField(max_length=250)
    last_name           =   serializers.CharField(max_length=250)
    token               =   serializers.CharField(max_length=250)
