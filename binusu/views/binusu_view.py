import hashlib
from ..models import Kyc, Orders, EmailLogs, TelegramLogs, PasswordResets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers.serializers import KycSerializer, KycConfirmSerializer, OrdersSerializer, EmailLogsSerializer, TelegramLogsSerializer, OrderReceiverSerializer, KycUserSerializer, PasswordResetSerializer, PasswordResetCreateSerializer, PasswordConfirmSerializer

from ..helpers.helpers import get_random_alphanumeric_string
from ..helpers.email_handler import buy_email, client_email, sell_email, client_sell_email, sign_up_email, password_reset_email, password_reset_404_email
from ..helpers.telegram_handler import send_telegram, telegram_buy_message, telegram_sell_message
from ..helpers.baluwa import send_order_email

class KycListView(APIView):
    """
    List all kyc and create a new kyc object
    """
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = KycSerializer(data=request.data)
        if serializer.is_valid():
            try:
                existing_user = Kyc.objects.get(email_address=serializer.validated_data["email_address"])
                return Response({"status":400, "error": "User already exists proceed to login"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                password = hashlib.sha256(serializer.data["password"].encode('utf-8')).hexdigest()


                welcome_email = sign_up_email(serializer.data["first_name"])
                send_order_email("Welcome to Binusu", welcome_email, serializer.data["email_address"])

                return Response({"status":201, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ConfirmKyc(APIView):
    """
    Confirm KYC of an individual
    """
    def post(self, request, format=None):
        serializer = KycConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Kyc.objects.get(email_address=serializer.data["email_address"])
                if(str(user.password) == serializer.data["password"]):
                    user_serializer = KycUserSerializer(user)
                    return Response({"status":200, "data": user_serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status":404, "error":"Invalid username or password"})
            except:
                return Response({"status": 404, "error":"User with email not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrdersView(APIView):
    """
    List all and create a new order
    """
    def post(self, request, format=None):
        serializer = OrderReceiverSerializer(data=request.data)
        if serializer.is_valid():
            try: 
                user = Kyc.objects.get(id=int(serializer.data['related_kyc']))
                
                order_data = {
                    "order_number": "{}{}".format("BN", get_random_alphanumeric_string(10)),
                    "related_kyc": serializer.data['related_kyc'],
                    "order_type": serializer.data['order_type'],
                    "crypto_type": serializer.data['crypto_type'],
                    "fiat_type":    serializer.data['fiat_type'],
                    "order_amount_crypto": serializer.data['order_amount_crypto'],
                    "order_amount_fiat": serializer.data['order_amount_fiat'],
                    "order_status": "UNFULFILLED",
                    "crypto_unit_price": serializer.data['crypto_unit_price']
                }

                order_serializer = OrdersSerializer(data=order_data)
                order_serializer.is_valid(raise_exception=True)
                order_serializer.save()

                if(order_serializer.data["order_type"]=="BUY"):
                    message = buy_email(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

                    client_message = client_email(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

                    telegram_message = telegram_buy_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

                    send_order_email("Crypto Buy Order", message, "brian.t@savannah.ug")

                    send_order_email("Crypto Buy Order", message, "arinrony@gmail.com")

                    send_order_email("Cryptocurreny Purchase order from Binusu", client_message, user.email_address)

                    send_telegram(telegram_message)
                
                else:
                    message = sell_email(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

                    client_message = client_sell_email(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

                    telegram_message = telegram_buy_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

                    send_order_email("Crypto Sell Order", message, "brian.t@savannah.ug")

                    send_order_email("Crypto Sell Order", message, "arinrony@gmail.com")

                    send_order_email("Cryptocurreny Sell order from Binusu", client_message, user.email_address)

                    send_telegram(telegram_message)


                return Response({"status":201, "data":order_serializer.data}, status=status.HTTP_201_CREATED)
            except:
                return Response({"status":404, "error":"User doesnt have valid KYC"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
    Reset password of an individual
    """
    def post(self, request, format=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Kyc.objects.get(email_address=serializer.data["email_address"])
                user_serialized = KycUserSerializer(user)
                reset_token = hashlib.sha256(user.email_address.encode('utf-8')).hexdigest()
                reset_data = {
                    'related_account':user_serialized.data["id"],
                    'reset_token': reset_token
                }

                password_serializer = PasswordResetCreateSerializer(data=reset_data)
                password_serializer.is_valid(raise_exception=True)
                password_serializer.save()

                password_reset_message = password_reset_email(user.first_name, reset_token)

                send_order_email("Password Reset", password_reset_message, user.email_address)
                
                return Response({"status":200, "message":"Success, Reset Email dispatched"}, status=status.HTTP_200_OK)
            except:
                password_reset_message = password_reset_404_email(serializer.data["email_address"])
                send_order_email("Password Reset", password_reset_message, serializer.data["email_address"])
                return Response({"status":200, "message":"Success, Reset Email dispatched"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmPasswordReset(APIView):
    def post(self, request, format=None):
        serializer = PasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            reset_token = hashlib.sha256(serializer.data['email_address'].encode('utf-8')).hexdigest()
            if(str(reset_token)==str(serializer.data['token'])):
                try:
                    user = Kyc.objects.get(email_address=serializer.data["email_address"])

                    Kyc.objects.update_or_create(
                    id=user.id, defaults={'password':serializer.data['new_password']}
                    )

                    return Response({"status":200, "message":"Success, Password reset successfully"}, status=status.HTTP_200_OK)
                except:
                    return Response({"status":404, "error":"User doesnt have valid KYC"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)