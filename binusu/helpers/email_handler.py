from django.core.mail import send_mail
from loyalty_api.settings import EMAIL_HOST_USER

def send_order_email(subject, message, recepient):
    return send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

def buy_email(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, type: {}, of crypto {}{} using {}{} at market price of {} per {}".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)

def client_email(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, type: {}, of crypto {}{} using {}{} at market price of {} per {} confirmed. Please hold on as one of our agents contacts you.".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)

def sell_email(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, type: {}, of crypto {}{} for {}{} at market price of {} per {}".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)

def client_sell_email(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, type: {}, of crypto {}{} for {}{} at market price of {} per {} confirmed. Please hold on as one of our agents contacts you.".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)

def sign_up_email(first_name):
    return "Hey {} \n Welcome to binusu.com. You can now proceed to transact in crypto. Supported coins are BTC, ETH, LTC, XRP. Please reach out to support@binusu.com for further details"

def order_confirm_email():
    pass