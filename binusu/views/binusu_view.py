import hashlib
import jwt
import json
from loyalty_api.settings import SECRET_KEY
from ..models import Kyc, Orders, EmailLogs, TelegramLogs, PasswordResets, AccountUser, OrderCompletions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from ..serializers.serializers import KycSerializer, KycConfirmSerializer, OrdersSerializer, EmailLogsSerializer, TelegramLogsSerializer, OrderReceiverSerializer, KycUserSerializer, PasswordResetSerializer, PasswordResetCreateSerializer, PasswordConfirmSerializer, OrdersDetailSerializer, OrdersUpdateSerializer, ClientOrderSerializer, OrderCompletionsCreateSerializer, OrderCompletionsDetailSerializer, OrderCompletionSerializer, OrderCompletionUpdateSerializer, TenantOrderReceiverSerializer

from ..helpers.helpers import get_random_alphanumeric_string
from ..helpers.email_handler import EmailFormatter, PersonalEmailFormatter, email_structure
from ..helpers.telegram_handler import send_telegram, telegram_buy_message, telegram_sell_message, send_error_telegram, telegram_error_message
from ..helpers.baluwa import send_order_email
from ..helpers.rates import get_rates, trigger_collection

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


class ClientOrdersView(APIView):
    def post(self, request, format=None):
        serializer = ClientOrderSerializer(data=request.data)
        if serializer.is_valid():
            orders_serializer = OrdersDetailSerializer(Orders.objects.filter(related_kyc=serializer.data["related_kyc"]), many=True)
            return Response({"status":200, "data": orders_serializer.data}, status=status.HTTP_200_OK)
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
                    "crypto_unit_price": serializer.data['crypto_unit_price'],
                    "crypto_address": serializer.data['crypto_address'],
                    "crypto_fees": serializer.data['crypto_fees'],
                    "crypto_fees_type": serializer.data['crypto_fees_type'],
                    "total_payable_amount_fiat": serializer.data['total_payable_amount_fiat'],
                    "warning": serializer.data['warning'],
                    "tenant_id": 0
                }

                order_serializer = OrdersSerializer(data=order_data)
                order_serializer.is_valid(raise_exception=True)
                order_serializer.save()

                order_amount_formated = "{:0,.2f}".format(float(order_serializer.data["order_amount_fiat"]))
                crypto_unit_formated = "{:0,.2f}".format(float(order_serializer.data["crypto_unit_price"]))

                email_format = EmailFormatter(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated)


                if(order_serializer.data["order_type"]=="BUY"):
                    
                    message = email_format.buy_email(user.email_address, user.phone_number, serializer.data['crypto_fees'], serializer.data['crypto_fees_type'], serializer.data['total_payable_amount_fiat'], serializer.data['crypto_address'])

                    client_message = email_format.client_buy_email(serializer.data['crypto_fees'], serializer.data['crypto_fees_type'], serializer.data['total_payable_amount_fiat'])

                    telegram_message = telegram_buy_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated, serializer.data['crypto_fees'], user.email_address, user.phone_number)

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

                    telegram_message = telegram_sell_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated, user.email_address, user.phone_number)

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


class TenantsOrdersView(APIView):
    """
    List all and create a new order
    """

    def post(self, request, format=None):
        serializer = TenantOrderReceiverSerializer(data=request.data)
        if serializer.is_valid():

            order_number = "{}".format(get_random_alphanumeric_string(10))

            rates_call = get_rates("UGX")
            rates_json = {}
            for currency in rates_call:
                if currency["currencyName"] == "Bitcoin":
                    rates_json["BTC"]=currency
                if currency["currencyName"] == "Binusu":
                    rates_json["BNU"]=currency
                if currency["currencyName"] == "Ether":
                    rates_json["ETH"]=currency
                if currency["currencyName"] == "Litecoin":
                    rates_json["LTC"]=currency
                if currency["currencyName"] == "Celo Dollar":
                    rates_json["CUSD"]=currency
                if currency["currencyName"] == "Bitcoin Cash":
                    rates_json["BCH"]=currency
                if currency["currencyName"] == "CELO":
                    rates_json["CELO"]=currency
                if currency["currencyName"] == "Binance Coin":
                    rates_json["BNB"]=currency
                if currency["currencyName"] == "Starsharks SEA":
                    rates_json["SEA"]=currency

            try: 
                user = Kyc.objects.get(id=int(serializer.data['related_kyc']))

                if(serializer.data["order_type"]=="BUY"):

                    crypto_unit_price = rates_json[serializer.data['crypto_type']]['Sell']

                    crypto_fees = rates_json[serializer.data['crypto_type']]['fast']

                    order_amount_minus_fees = float(serializer.data['order_amount']) - float(crypto_fees)

                    order_amount_crypto = order_amount_minus_fees/float(crypto_unit_price)


                    order_data = {
                    "order_number": order_number,
                    "related_kyc": serializer.data['related_kyc'],
                    "order_type": serializer.data['order_type'],
                    "crypto_type": serializer.data['crypto_type'],
                    "fiat_type":    serializer.data['fiat_type'],
                    "order_amount_crypto": round(order_amount_crypto, 10),
                    "order_amount_fiat": round(float(serializer.data['order_amount']), 2),
                    "order_status": "UNFULFILLED",
                    "crypto_address": serializer.data['crypto_address'],
                    "crypto_fees": round(float(crypto_fees), 2),
                    "crypto_fees_type": 'FAST',
                    "total_payable_amount_fiat": order_amount_minus_fees,
                    "warning": 0,
                    }

                    order_serializer = OrdersSerializer(data=order_data)
                    order_serializer.is_valid(raise_exception=True)
                    order_serializer.save()

                    order_amount_formated = "{:0,.2f}".format(float(order_serializer.data["total_payable_amount_fiat"]))

                    crypto_unit_formated = "{:0,.2f}".format(float(order_serializer.data["crypto_unit_price"]))

                    email_format = EmailFormatter(order_number, serializer.data["order_type"], serializer.data["crypto_type"], serializer.data["fiat_type"], order_serializer.data['order_amount_crypto'], order_amount_formated, crypto_unit_formated)
                    
                    message = email_format.buy_email(user.email_address, user.phone_number, crypto_fees, 'FAST', order_amount_minus_fees, serializer.data['crypto_address'])

                    client_message = email_format.client_buy_email(crypto_fees, 'FAST', order_amount_minus_fees)

                    telegram_message = telegram_buy_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_amount_crypto, order_amount_formated, crypto_unit_formated, 'FAST', user.email_address, user.phone_number)

                    try:
                        send_order_email("Crypto Buy Order", message, "twhy.brian@gmail.com")

                        send_order_email("Crypto Buy Order", message, "arinrony@gmail.com")

                        send_order_email("Cryptocurreny Purchase order from Binusu", client_message, user.email_address)

                        send_telegram(telegram_message)

                    except Exception as e:
                        send_error_telegram(e)
                        return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)

                
                else:
                    
                    crypto_unit_price = rates_json[serializer.data['crypto_type']]['Buy']

                    order_amount_fiat = float(serializer.data['order_amount'])*float(crypto_unit_price)

                    order_data = {
                    "order_number": order_number,
                    "related_kyc": serializer.data['related_kyc'],
                    "order_type": serializer.data['order_type'],
                    "crypto_type": serializer.data['crypto_type'],
                    "fiat_type":    serializer.data['fiat_type'],
                    "order_amount_crypto": round(float((serializer.data['order_amount'])), 10),
                    "order_amount_fiat": round(float(order_amount_fiat), 2),
                    "order_status": "UNFULFILLED",
                    "crypto_unit_price": round(float(crypto_unit_price), 2),
                    "crypto_address": serializer.data['crypto_address'],
                    "crypto_fees": 0,
                    "crypto_fees_type": 'FAST',
                    "total_payable_amount_fiat": round(order_amount_fiat,2),
                    "warning": 0,
                    }

                    order_serializer = OrdersSerializer(data=order_data)
                    order_serializer.is_valid(raise_exception=True)
                    order_serializer.save()

                    order_amount_formated = "{:0,.2f}".format(float(order_serializer.data["total_payable_amount_fiat"]))

                    crypto_unit_formated = "{:0,.2f}".format(float(order_serializer.data["crypto_unit_price"]))

                    email_format = EmailFormatter(order_number, serializer.data["order_type"], serializer.data["crypto_type"], serializer.data["fiat_type"], order_serializer.data['order_amount_crypto'], order_amount_formated, crypto_unit_formated)

                    message = email_format.sell_email(user.email_address, user.phone_number)

                    client_message = email_format.client_sell_email()

                    telegram_message = telegram_sell_message(order_serializer.data["order_number"], order_serializer.data["order_type"], order_serializer.data["crypto_type"], order_serializer.data["fiat_type"], order_serializer.data["order_amount_crypto"], order_amount_formated, crypto_unit_formated, user.email_address, user.phone_number)

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
        currency = request.GET.get('currencySymbol', '')
        # try:
        if(currency=="KES"):
            rates_call = get_rates("KES")
        else:
            rates_call = get_rates("UGX")
        rates_json = {}
        for currency in rates_call:
            if currency["currencyName"] == "Bitcoin":
                rates_json["BTC"]=currency
            if currency["currencyName"] == "Binusu":
                rates_json["BNU"]=currency
            if currency["currencyName"] == "Ether":
                rates_json["ETH"]=currency
            if currency["currencyName"] == "Litecoin":
                rates_json["LTC"]=currency
            if currency["currencyName"] == "Celo Dollar":
                rates_json["CUSD"]=currency
            if currency["currencyName"] == "Bitcoin Cash":
                rates_json["BCH"]=currency
            if currency["currencyName"] == "CELO":
                rates_json["CELO"]=currency
            if currency["currencyName"] == "MYST":
                rates_json["MYST"]=currency
            if currency["currencyName"] == "Chainlink":
                rates_json["LINK"]=currency
            if currency["currencyName"] == "Binance Coin":
                rates_json["BNB"]=currency
            if currency["currencyName"] == "Starsharks SEA":
                rates_json["SEA"]=currency

        rates_data = {
            "BTC":{
                "BUY":rates_json['BTC']['Buy'],
                "SELL":rates_json['BTC']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['BTC']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['BTC']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['BTC']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['BTC']['minimum_ugx'],
                "SLOW":rates_json['BTC']['slow'],
                "NORMAL":rates_json['BTC']['normal'],
                "FAST":rates_json['BTC']['fast']
            },
            "ETH":{
                "BUY":rates_json['ETH']['Buy'],
                "SELL":rates_json['ETH']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['ETH']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['ETH']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['ETH']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['ETH']['minimum_ugx'],
                "SLOW":rates_json['ETH']['slow'],
                "NORMAL":rates_json['ETH']['normal'],
                "FAST":rates_json['ETH']['fast']
            },
            "CELO":{
                "BUY":rates_json['CELO']['Buy'],
                "SELL":rates_json['CELO']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['CELO']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['CELO']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['CELO']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['CELO']['minimum_ugx'],
                "SLOW":rates_json['CELO']['slow'],
                "NORMAL":rates_json['CELO']['normal'],
                "FAST":rates_json['CELO']['fast']
            },
            "cUSD":{
                "BUY":rates_json['CUSD']['Buy'],
                "SELL":rates_json['CUSD']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['CUSD']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['CUSD']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['CUSD']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['CUSD']['minimum_ugx'],
                "SLOW":rates_json['CUSD']['slow'],
                "NORMAL":rates_json['CUSD']['normal'],
                "FAST":rates_json['CUSD']['fast']
            },
            "BCH":{
                "BUY":rates_json['BCH']['Buy'],
                "SELL":rates_json['BCH']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['BCH']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['BCH']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['BCH']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['BCH']['minimum_ugx'],
                "SLOW":rates_json['BCH']['slow'],
                "NORMAL":rates_json['BCH']['normal'],
                "FAST":rates_json['BCH']['fast']
            },
            "LTC":{
                "BUY":rates_json['LTC']['Buy'],
                "SELL":rates_json['LTC']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['LTC']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['LTC']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['LTC']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['LTC']['minimum_ugx'],
                "SLOW":rates_json['LTC']['slow'],
                "NORMAL":rates_json['LTC']['normal'],
                "FAST":rates_json['LTC']['fast']
            },
            # "LINK":{
            #     "BUY":rates_json['LINK']['Buy'],
            #     "SELL":rates_json['LINK']['Sell'],
            #     "TRANSFER_FEE_CRYPTO":rates_json['LINK']['transfer_fee_crypt'],
            #     "TRANSFER_FEE_UGX":rates_json['LINK']['transfer_fee_ugx'],
            #     "MINIMUM_CRYPTO_AMOUNT":rates_json['LINK']['minimum_crypt'],
            #     "MINIMUM_UGX_AMOUNT":rates_json['LINK']['minimum_ugx'],
            #     "SLOW":rates_json['MYST']['slow'],
            #     "NORMAL":rates_json['MYST']['normal'],
            #     "FAST":rates_json['MYST']['fast']
            # },
            "USDT":{
                "BUY":rates_json['CUSD']['Buy'],
                "SELL":rates_json['CUSD']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['CUSD']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['CUSD']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['CUSD']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['CUSD']['minimum_ugx'],
                "SLOW":rates_json['CUSD']['slow'],
                "NORMAL":rates_json['CUSD']['normal'],
                "FAST":rates_json['CUSD']['fast']
            },
            "BNB":{
                "BUY":rates_json['BNB']['Buy'],
                "SELL":rates_json['BNB']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['BNB']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['BNB']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['BNB']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['BNB']['minimum_ugx'],
                "SLOW":rates_json['BNB']['slow'],
                "NORMAL":rates_json['BNB']['normal'],
                "FAST":rates_json['BNB']['fast']
            },
            "SEA":{
                "BUY":rates_json['SEA']['Buy'],
                "SELL":rates_json['SEA']['Sell'],
                "TRANSFER_FEE_CRYPTO":rates_json['SEA']['transfer_fee_crypt'],
                "TRANSFER_FEE_UGX":rates_json['SEA']['transfer_fee_ugx'],
                "MINIMUM_CRYPTO_AMOUNT":rates_json['SEA']['minimum_crypt'],
                "MINIMUM_UGX_AMOUNT":rates_json['SEA']['minimum_ugx'],
                "SLOW":rates_json['SEA']['slow'],
                "NORMAL":rates_json['SEA']['normal'],
                "FAST":rates_json['SEA']['fast']
            }
        }
        return Response({"status":200, "data":rates_data})
        # except Exception as e:
        #     return Response({"status":404, "error":"Rates currently unavailable"}, status=status.HTTP_404_NOT_FOUND)

class GetSpecificOrderDetails(APIView):
    def post(self, request, format=None):
        serializer = OrderCompletionSerializer(data=request.data)
        if serializer.is_valid():
            order = Orders.objects.get(id=serializer.data["related_order"])

            return Response({"status":200, "data": OrdersDetailSerializer(order).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderCompletionCollection(APIView):
    def post(self, request, format=None):
        serializer = OrderCompletionSerializer(data=request.data)
        if serializer.is_valid():
            order = Orders.objects.get(id=serializer.data["related_order"])
            kyc = Kyc.objects.get(id=order.related_kyc.id)
            formated_number = kyc.phone_number[1:]
            reconstructed_number = "{}{}".format("256", formated_number)
            if(order.order_status == "UNFULFILLED"):
                data = {
                    "wal_api_key": "fd9c876846b89736a8c3ecde15931c24fed9a10b4e3767af04361913ee671c09",
                    "method": "bms_deposit",
                    "payid": order.order_number,
                    "currency": "UG-MM",
                    "amount": float(order.total_payable_amount_fiat),
                    "format": "JSON-POPUP",
                    "email": kyc.email_address,
                    "notes": reconstructed_number
                }
                
                try:
                    call = trigger_collection(data)
                    order_completion_data = {
                        'related_order':order.id,
                        'currency':call["Response"]["currency"],
                        'amount':call["Response"]["amount_to_transfer"],
                        'invoice_number':call["Response"]["invoiceNo"],
                        'pay_id':call["Response"]["payment_id"],
                    }

                    order_completion_serializer = OrderCompletionsCreateSerializer(data=order_completion_data)
                    order_completion_serializer.is_valid(raise_exception=True)
                    order_completion_serializer.save()
                    return Response({"status":200, "data": order_completion_serializer.data, "popup": call["Response"]["data"]["popup"]}, status=status.HTTP_200_OK)
                except Exception as e:
                    send_error_telegram(e)
                    return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)
            return Response({"status":404, "error":"OPEN OPRDER NOT FOUND"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCompletionCollectionCrypto(APIView):
    def post(self, request, format=None):
        serializer = OrderCompletionSerializer(data=request.data)
        if serializer.is_valid():
            order = Orders.objects.get(id=serializer.data["related_order"])
            kyc = Kyc.objects.get(id=order.related_kyc.id)
            formated_number = kyc.phone_number[1:]
            reconstructed_number = "{}{}".format("256", formated_number)
            
            if(order.order_status == "UNFULFILLED"):
                data = ({
                    "wal_api_key":           "a8637118f1fedbaa33317ab5e4458f03e0e24885f20b2b2d6b1cfe110ea9640f",
                    "method": "bms_deposit",
                    "payid": order.order_number,
                    "currency": "BTC",
                    "amount": float(order.order_amount_fiat),
                    "format": "JSON-POPUP",
                    "notes": reconstructed_number,
                    "email": kyc.email_address,
                    "auto_exchange": 0
                })
                
                try:
                    call = trigger_collection(data)
                    order_completion_data = {
                        'related_order':order.id,
                        'currency':call["Response"]["data"]["currency"],
                        'amount':call["Response"]["data"]["amount_to_transfer"],
                        'invoice_number':call["Response"]["data"]["invoiceNo"],
                        'pay_id':call["Response"]["data"]["payment_id"],
                    }

                    order_completion_serializer = OrderCompletionsCreateSerializer(data=order_completion_data)
                    order_completion_serializer.is_valid(raise_exception=True)
                    order_completion_serializer.save()

                    return Response({"status":200, "data": order_completion_serializer.data, "popup": call["Response"]["data"]["popup"]}, status=status.HTTP_200_OK)
                except Exception as e:
                    send_error_telegram(e)
                    return Response({"status":424, "error":"Service Unavailable due to failed dependency"}, status=status.HTTP_424_FAILED_DEPENDENCY)
            return Response({"status":404, "error":"OPEN ORDER NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientOrderCompletionView(APIView):
    def post(self, request, format=None):
        serializer = OrderCompletionSerializer(data=request.data)
        if serializer.is_valid():
            order_completion_serializer = OrderCompletionsDetailSerializer(OrderCompletions.objects.filter(related_order=serializer.data["related_order"]), many=True)
            return Response({"status":200, "data": order_completion_serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderCompletionStatus(APIView):
    def post(self, request, format=None):
        serializer = OrderCompletionUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                related_completion = OrderCompletions.objects.get(pay_id=serializer.data["pay_id"])
                if(related_completion.completion_status==False and serializer.data["status"] == 0):

                    OrderCompletions.objects.update_or_create(
                    id=related_completion.id, defaults={'completion_status':True}
                    )

                    return Response({"status":200, "message":"Successfully Updated"}, status=status.HTTP_200_OK)
                if(related_completion.completion_status==False and serializer.data["status"] == 1):

                    OrderCompletions.objects.update_or_create(
                    id=related_completion.id, defaults={'callback_response':False}
                    )

                    return Response({"status":200, "message":"Successfully Updated"}, status=status.HTTP_200_OK)
                return Response({"status":404, "error": "Transaction Already Updated"})
            except:
                return Response({"status":404, "error":"User doesnt have valid KYC"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)