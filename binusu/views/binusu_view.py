import hashlib
import jwt
from loyalty_api.settings import SECRET_KEY
from ..models import Kyc, Orders, EmailLogs, TelegramLogs, PasswordResets, AccountUser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers.serializers import KycSerializer, KycConfirmSerializer, OrdersSerializer, EmailLogsSerializer, TelegramLogsSerializer, OrderReceiverSerializer, KycUserSerializer, PasswordResetSerializer, PasswordResetCreateSerializer, PasswordConfirmSerializer, OrdersDetailSerializer, OrdersUpdateSerializer

from ..helpers.helpers import get_random_alphanumeric_string
from ..helpers.email_handler import EmailFormatter, PersonalEmailFormatter
from ..helpers.telegram_handler import send_telegram, telegram_buy_message, telegram_sell_message, send_error_telegram, telegram_error_message
from ..helpers.baluwa import send_order_email
from ..helpers.rates import get_rates

class KycListView(APIView):
    """
    List all kyc and create a new kyc object
    """
    # parser_classes = (MultiPartParser, FormParser)

    def get(self, request, format=None):
        serializer = KycUserSerializer(Kyc.objects.all(), many=True)
        return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        serializer = KycSerializer(data=request.data)
        if serializer.is_valid():
            try:
                existing_user = Kyc.objects.get(email_address=serializer.validated_data["email_address"])
                return Response({"status":400, "error": "User already exists proceed to login"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                try:
                    serializer.save()

                    PersonalEmail = PersonalEmailFormatter(serializer.data["first_name"])
                    welcome_email = PersonalEmail.sign_up_email()

                    send_order_email("Welcome to Binusu", welcome_email, serializer.data["email_address"])

                except Exception as e:
                    send_error_telegram(e)
                    return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)

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
    def get(self, request, format=None):
        try: 
            if(request.headers['Token']):
                decoded_jwt = jwt.decode(request.headers['Token'], SECRET_KEY, algorithms=["HS256"])
                if(decoded_jwt['id']):
                    serializer = OrdersDetailSerializer(Orders.objects.all(), many=True)
                    return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)
                return Response({"status":401, "error":"Unauthorized, Please provide token"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"status":401, "error":"Unauthorized, Please provide token"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"status":400, "error":"Bad Token, Go away with your bad token"}, status=status.HTTP_400_BAD_REQUEST)
                

    def post(self, request, format=None):
        serializer = OrderReceiverSerializer(data=request.data)
        if serializer.is_valid():
            try: 
                user = Kyc.objects.get(id=int(serializer.data['related_kyc']))
                
                order_data = {
                    "order_number": "{}".format(get_random_alphanumeric_string(10)),
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

                order_amount_formated = "{:0,.2f}".format(float(order_serializer.data["order_amount_fiat"]))
                crypto_unit_formated = "{:0,.2f}".format(float(order_serializer.data["crypto_unit_price"]))

                email_format = EmailFormatter(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated)


                if(order_serializer.data["order_type"]=="BUY"):
                    
                    message = email_format.buy_email(user.email_address, user.phone_number)

                    client_message = email_format.client_buy_email()

                    telegram_message = telegram_buy_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated)

                    try:
                        send_order_email("Crypto Buy Order", message, "twhy.brian@gmail.com")

                        send_order_email("Crypto Buy Order", message, "arinrony@gmail.com")

                        send_order_email("Cryptocurreny Purchase order from Binusu", client_message, user.email_address)

                        send_telegram(telegram_message)

                    except Exception as e:
                        send_error_telegram(e)
                        return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)
                
                else:
                    message = email_format.sell_email(user.email_address, user.phone_number)

                    client_message = email_format.client_sell_email()

                    telegram_message = telegram_buy_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated)

                    try:
                        send_order_email("Crypto Sell Order", message, "twhy.brian@gmail.com")

                        send_order_email("Crypto Sell Order", message, "arinrony@gmail.com")

                        send_order_email("Cryptocurreny Sell order from Binusu", client_message, user.email_address)

                        send_telegram(telegram_message)
                    except Exception as e:
                        send_error_telegram(e)
                        return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)

                return Response({"status":201, "data":order_serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                send_error_telegram(e)
                return Response({"status":404, "error":"User doesnt have valid KYC"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderDetails(APIView):

    def patch(self, request, format=None):
        if(request.headers['Token']):
            decoded_jwt = jwt.decode(request.headers['Token'], SECRET_KEY, algorithms=["HS256"])
            if(decoded_jwt['id']):
                serializer = OrdersUpdateSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        order_to_update = Orders.objects.get(order_number=serializer.data['order_number'])
                        user_updating   = AccountUser.objects.get(id=serializer.data['user_id'])

                        if(serializer.data["status"] == "FULFILLED" or serializer.data['status'] == "CANCELLED" ):
                            Orders.objects.update_or_create(id=order_to_update.id, defaults={'fullfilled_by':user_updating, 'order_status': serializer.data["status"]}
                            )
                            return Response({"status":200, "data":serializer.data}, status=status.HTTP_200_OK)
                        return Response({"status":400, "error":"Invalid status, Please use CANCELLED OR FULFILLED"}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        send_error_telegram(e)
                        return Response({"status":400, "error":"Invalid order number"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status":401, "error":"Unauthorized, Please provide token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"status":401, "error":"Unauthorized, Please provide token"}, status=status.HTTP_401_UNAUTHORIZED)
                

class OrdersStatistics(APIView):
    """
    Statistics on orders
    """
    def get(self, request, format=None):
        try: 
            if(request.headers['Token']):
                decoded_jwt = jwt.decode(request.headers['Token'], SECRET_KEY, algorithms=["HS256"])
                if(decoded_jwt['id']):
                    buy_orders          =   Orders.objects.filter(order_type="BUY").count()
                    sell_orders         =   Orders.objects.filter(order_type="SELL").count()
                    fullfilled_orders   =   Orders.objects.filter(order_status="FULFILLED").count()
                    unfullfilled_orders =   Orders.objects.filter(order_status="UNFULFILLED").count()
                    return Response({"status":200, "data":{"buy_orders":buy_orders, "sell_orders":sell_orders, "fulfilled_orders":fullfilled_orders, "unfulfilled_orders":unfullfilled_orders}})
                
                return Response({"status":400, "error":"Bad Token, Go away with your bad token"}, status=status.HTTP_400_BAD_REQUEST)    
            return Response({"status":401, "error":"Unauthorized, Please provide token"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"status":400, "error":"Bad Token, Go away with your bad token"}, status=status.HTTP_400_BAD_REQUEST)


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
                reset_token = hashlib.sha256(user.email_address.encode('utf-8')+get_random_alphanumeric_string(6).encode('utf-8')).hexdigest()
                reset_data = {
                    'related_account':user_serialized.data["id"],
                    'reset_token': reset_token
                }

                password_serializer = PasswordResetCreateSerializer(data=reset_data)
                password_serializer.is_valid(raise_exception=True)
                password_serializer.save()

                personal_email = PersonalEmailFormatter(user.first_name)

                password_reset_message = personal_email.password_reset_email(reset_token)

                send_order_email("Password Reset", password_reset_message, user.email_address)
                
                return Response({"status":200, "message":"Success, Reset Email dispatched"}, status=status.HTTP_200_OK)
            except:
                personal_email = PersonalEmailFormatter("first_name")
                password_reset_message = personal_email.password_reset_404_email(serializer.data["email_address"])
                send_order_email("Password Reset", password_reset_message, serializer.data["email_address"])
                return Response({"status":200, "message":"Success, Reset Email dispatched"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPasswordReset(APIView):
    def post(self, request, format=None):
        serializer = PasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                related_reset = PasswordResets.objects.get(reset_token=serializer.data["token"])
                if(related_reset.reset_used==False):
                
                    user = Kyc.objects.get(id=related_reset.related_account.id)

                    Kyc.objects.update_or_create(
                    id=user.id, defaults={'password':serializer.data['new_password']}
                    )

                    PasswordResets.objects.update_or_create(
                        id=related_reset.id, defaults={'reset_used':True}
                    )

                    return Response({"status":200, "message":"Success, Password reset successfully"}, status=status.HTTP_200_OK)
                return Response({"status":404, "error": "Reset token already used"})
            except:
                return Response({"status":404, "error":"User doesnt have valid KYC"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentRates(APIView):
    def get(self, request, format=None):
        try:
            rates_call = get_rates()
            rates_data = {
                "BTC":{
                    "BUY":rates_call[0]['Buy'],
                    "SELL":rates_call[0]['Sell'],
                    "TRANSFER_FEE_CRYPTO":rates_call[0]['transfer_fee_crypt'],
                    "TRANSFER_FEE_UGX":rates_call[0]['transfer_fee_ugx'],
                    "MINIMUM_CRYPTO_AMOUNT":rates_call[0]['minimum_crypt'],
                    "MINIMUM_UGX_AMOUNT":rates_call[0]['minimum_ugx']
                },
                "ETH":{
                    "BUY":rates_call[1]['Buy'],
                    "SELL":rates_call[1]['Sell'],
                    "TRANSFER_FEE_CRYPTO":rates_call[1]['transfer_fee_crypt'],
                    "TRANSFER_FEE_UGX":rates_call[1]['transfer_fee_ugx'],
                    "MINIMUM_CRYPTO_AMOUNT":rates_call[1]['minimum_crypt'],
                    "MINIMUM_UGX_AMOUNT":rates_call[1]['minimum_ugx']
                },
                "CELO":{
                    "BUY":rates_call[5]['Buy'],
                    "SELL":rates_call[5]['Sell'],
                    "TRANSFER_FEE_CRYPTO":rates_call[5]['transfer_fee_crypt'],
                    "TRANSFER_FEE_UGX":rates_call[5]['transfer_fee_ugx'],
                    "MINIMUM_CRYPTO_AMOUNT":rates_call[5]['minimum_crypt'],
                    "MINIMUM_UGX_AMOUNT":rates_call[5]['minimum_ugx']
                },
                "cUSD":{
                    "BUY":rates_call[3]['Buy'],
                    "SELL":rates_call[3]['Sell'],
                    "TRANSFER_FEE_CRYPTO":rates_call[3]['transfer_fee_crypt'],
                    "TRANSFER_FEE_UGX":rates_call[3]['transfer_fee_ugx'],
                    "MINIMUM_CRYPTO_AMOUNT":rates_call[3]['minimum_crypt'],
                    "MINIMUM_UGX_AMOUNT":rates_call[3]['minimum_ugx']
                },
                "BCH":{
                    "BUY":rates_call[4]['Buy'],
                    "SELL":rates_call[4]['Sell'],
                    "TRANSFER_FEE_CRYPTO":rates_call[4]['transfer_fee_crypt'],
                    "TRANSFER_FEE_UGX":rates_call[4]['transfer_fee_ugx'],
                    "MINIMUM_CRYPTO_AMOUNT":rates_call[4]['minimum_crypt'],
                    "MINIMUM_UGX_AMOUNT":rates_call[4]['minimum_ugx']
                },
                "LTC":{
                    "BUY":rates_call[2]['Buy'],
                    "SELL":rates_call[2]['Sell'],
                    "TRANSFER_FEE_CRYPTO":rates_call[2]['transfer_fee_crypt'],
                    "TRANSFER_FEE_UGX":rates_call[2]['transfer_fee_ugx'],
                    "MINIMUM_CRYPTO_AMOUNT":rates_call[2]['minimum_crypt'],
                    "MINIMUM_UGX_AMOUNT":rates_call[2]['minimum_ugx']
                }
            }
            return Response({"status":200, "data":rates_data})
        except:
             return Response({"status":404, "error":"Rates currently unavailable"}, status=status.HTTP_404_NOT_FOUND)