from django.core.mail import send_mail


class EmailFormatter:
    """
    Handle all transaction email dispatch logic
    """

    def __init__(self, order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
        self.order_number = order_number
        self.order_type = order_type
        self.crypto_type = crypto_type
        self.fiat_type = fiat_type
        self.order_amount_crypto = order_amount_crypto
        self.order_amount_fiat = order_amount_fiat
        self.crypto_unit_price = crypto_unit_price

    def buy_email(self, email_address, phone_number):
        return "Order No. {}, \n type: {}, \n of crypto {}{} using {}{} at market price of {} per {}. Client Email address is {} and Phone Number is {}".format(self.order_number, self.order_type, self.order_amount_crypto, self.crypto_type, self.order_amount_fiat, self.fiat_type, self.crypto_unit_price, self.crypto_type, email_address, phone_number)

    def client_buy_email(self):
        return "Order No. {}, \n type: {}, \n of crypto {}{} \n using {}{} at market price of {} per {} confirmed. Please hold on as one of our agents contacts you.".format(self.order_number, self.order_type, self.order_amount_crypto, self.crypto_type, self.order_amount_fiat, self.fiat_type, self.crypto_unit_price, self.crypto_type)

    def sell_email(self, email_address, phone_number):
        return "Order No. {}, type: {}, of crypto {}{} for {}{} at market price of {} per {}. Client Email address is {} and Phone Number is {}".format(self.order_number, self.order_type, self.order_amount_crypto, self.crypto_type, self.order_amount_fiat, self.fiat_type, self.crypto_unit_price, self.crypto_type, email_address, phone_number)

    def client_sell_email(self):
        return "Order No. {}, type: {}, of crypto {}{} for {}{} at market price of {} per {} confirmed. Please hold on as one of our agents contacts you.".format(self.order_number, self.order_type, self.order_amount_crypto, self.crypto_type, self.order_amount_fiat, self.fiat_type, self.crypto_unit_price, self.crypto_type)


class PersonalEmailFormatter:
    """
    Handle all personal email dispatch logic
    """

    def __init__(self, first_name):
        self.first_name = first_name

    def sign_up_email(self):
        return "Hey {} \n Welcome to binusu.com. You can now proceed to transact in crypto. Supported coins are BTC, ETH, CELO, cUSD. Please reach out to support@binusu.com for further details".format(self.first_name)

    def order_confirm_email(self):
        pass

    def password_reset_email(self, token):
        return "Hey {} Please use this link to reset your password https://binusu.com/new-password.html?token={}. \n Please Ignore this message if you did not request a password reset".format(self.first_name, token)

    def password_reset_404_email(self, email):
        return "We received a request to reset the password to access Binusu OTC with your email address {} from a {{operating_system}} device using {{browser_name}}, but we were unable to find an account associated with this address. If you use Binusu OTC and were expecting this email, consider trying to request a password reset using the email address associated with your account.".format(email)