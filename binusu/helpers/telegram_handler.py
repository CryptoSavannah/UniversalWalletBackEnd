from loyalty_api.settings import TELEGRAM_TOKEN, TELEGRAM_GROUP_ID, ENVIRONMENT
from ..constants.constants import TELEGRAM_ERROR_GROUP, TELEGRAM_ERROR_TOKEN
import requests


def send_telegram(text):
    if ENVIRONMENT=="TESTING":
        telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(TELEGRAM_ERROR_TOKEN, TELEGRAM_ERROR_GROUP, text)
    elif ENVIRONMENT=="PRODUCTION":
        telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(TELEGRAM_TOKEN, TELEGRAM_GROUP_ID, text)
    telegram_post = requests.post(telegram_url)
    return telegram_post.json()
    # except:
    #     return "error"

def send_error_telegram(text):
    telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(TELEGRAM_ERROR_TOKEN, TELEGRAM_ERROR_GROUP, text)
    
    telegram_post = requests.post(telegram_url)
    return telegram_post.json()


def telegram_buy_message(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price, crypto_fees, email_address, phone_number):
    return "Order No. {}, \n type: {}, \n of crypto {}{} \n using {}{} \n at market price of {} per {}. Crypto transfer fees are {}. Customer Email Address is {} and Phone number is {}".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type, crypto_fees, email_address, phone_number)


def telegram_sell_message(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price, email_address, phone_number):
    return "Order No. {}, \n type: {}, \n of crypto {}{} \n using {}{} \n at market price of {} per {}. Customer Email Address is {} and Phone number is {}. ".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type, email_address, phone_number)

def telegram_error_message(e):
    return "{}".format(e)