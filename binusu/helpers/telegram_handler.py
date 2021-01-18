from loyalty_api.settings import TELEGRAM_TOKEN, TELEGRAM_GROUP_ID
import requests


def send_telegram(text):
    telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(TELEGRAM_TOKEN, TELEGRAM_GROUP_ID, text)
    
    telegram_post = requests.post(telegram_url)
    return telegram_post.json()
    # except:
    #     return "error"

def telegram_buy_message(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, \n type: {}, \n of crypto {}{} \n using {}{} \n at market price of {} per {}".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)


def telegram_sell_message(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, \n type: {}, \n of crypto {}{} \n using {}{} \n at market price of {} per {}".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)