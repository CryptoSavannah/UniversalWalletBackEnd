from ..models import Kyc, Orders, EmailLogs, TelegramLogs
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers.serializers import KycSerializer, KycConfirmSerializer, OrdersSerializer, EmailLogsSerializer, TelegramLogsSerializer, OrderReceiverSerializer, KycUserSerializer

from ..helpers.helpers import get_random_alphanumeric_string
from ..helpers.email_handler import send_order_email, buy_email

class KycListView(APIView):
    """
    List all kyc and create a new kyc object
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = KycSerializer(data=request.data)
        if serializer.is_valid():
            try:
                existing_user = Kyc.objects.get(email_address=serializer.validated_data["email_address"])
                return Response({"status":400, "error": "User already exists proceed to login"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                serializer.save()
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
            # try: 
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

            message = buy_email(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_serializer.data["order_amount_fiat"], order_serializer.data["crypto_unit_price"])

            send_order_email("Crypto Buy Order", message, "kapson65536@gmail.com")

            return Response({"status":201, "data":order_serializer.data}, status=status.HTTP_201_CREATED)
            # except:
            #     return Response({"status":404, "error":"User doesnt have valid KYC"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)