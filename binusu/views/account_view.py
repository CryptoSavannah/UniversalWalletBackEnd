import hashlib
import jwt
from ..models import AccountUser, UserLogins, UserRefreshOtp
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.account_serializer import UserCreateSerializer, UserDetailSerializer, UserRefreshOtpCreateSerializer, UserDataSerializer, UserLoginSerializer, UserOtpConfirmSerializer, UserTokenSerializer

from ..helpers.helpers import get_random_alphanumeric_string
from ..helpers.email_handler import EmailFormatter, PersonalEmailFormatter
from ..helpers.telegram_handler import send_telegram, telegram_buy_message, telegram_sell_message, send_error_telegram, telegram_error_message
from ..helpers.baluwa import send_order_email

from loyalty_api.settings import SECRET_KEY


class UserListView(APIView):
    """
    List all users and create a new user object
    """

    def get(self, request, format=None):
        serializer = UserDetailSerializer(AccountUser.objects.filter(active=True), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = UserDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                existing_user = AccountUser.objects.get(email_address=serializer.validated_data["email_address"])
                return Response({"status":400, "error": "User already exists proceed to login"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                try:
                    password_hashed = hashlib.sha256(serializer.validated_data['password'].encode('utf-8')).hexdigest()

                    user_data = {
                    "first_name": serializer.data["first_name"],
                    "last_name": serializer.data["last_name"],
                    "email_address": serializer.data["email_address"],
                    "role": serializer.data["role"],
                    "password": password_hashed,
                    "account_status": 0
                    }

                    user_save_serializer = UserCreateSerializer(data=user_data)
                    user_save_serializer.is_valid(raise_exception=True)
                    user_save_serializer.save()

                except Exception as e:
                    send_error_telegram(e)
                    return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)

                return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    Login view for user
    """
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = AccountUser.objects.get(email_address=serializer.validated_data["email_address"])

                if(user.password==hashlib.sha256(serializer.validated_data['password'].encode('utf-8')).hexdigest()):
                    if(user.active==False):
                        print("send email")
                        return Response({"status":401, "error":"Please check otp in email to activate account"})
                    else:
                        encoded_jwt = jwt.encode({"id": user.id}, SECRET_KEY, algorithm="HS256").decode('ascii')

                        user_data = {
                            "user_id":user.id,
                            "email_address":user.email_address,
                            "first_name":user.first_name,
                            "last_name":user.last_name,
                            "token":encoded_jwt
                        }

                        user_serializer = UserTokenSerializer(user_data)
                        return Response({"status":200, "data":user_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":404, "error":"Invalid username or password"})
            except:
                return Response({"status":404, "error":"Invalid username or password"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)