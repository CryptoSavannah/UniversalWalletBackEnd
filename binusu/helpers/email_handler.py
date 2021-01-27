from django.core.mail import send_mail

# def send_order_email(subject, message, recepient):
#     return send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

def buy_email(order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
    return "Order No. {}, \n type: {}, \n of crypto {}{} using {}{} at market price of {} per {}".format(order_number, order_type, order_amount_crypto, crypto_type, order_amount_fiat, fiat_type, crypto_unit_price, crypto_type)

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

def password_reset_email(first_name, token):
    return "Hey {} Please use this link to reset your password https://binusu.com/new-password.html?token={}. \n Please Ignore this message if you did not request a password reset".format(first_name, token)

def password_reset_404_email(email):
    return "We received a request to reset the password to access Binusu OTC with your email address {} from a {{operating_system}} device using {{browser_name}}, but we were unable to find an account associated with this address. If you use Binusu OTC and were expecting this email, consider trying to request a password reset using the email address associated with your account.".format(email)