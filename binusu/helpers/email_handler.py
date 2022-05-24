from django.core.mail import send_mail
import html

def email_structure(order_owner, order_type, order_number, crypto_type, order_amount_crypto, fiat_type, order_amount_fiat, crypto_fees, total_amount, email_address, phone_number, crypto_address):
    style = 'table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}'
    escaped_style = html.escape(style)

    if(order_owner=='client'):
        table = '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Crypto Transaction Fees</td><td>{}</td></tr><tr><td>Total Amount</td><td>{}</td></tr><tr><td>{} Address</td><td>{}</td></tr></table></body></html>'.format(escaped_style, order_type, order_number, crypto_type, order_amount_crypto, fiat_type, order_amount_fiat, crypto_fees, total_amount, crypto_type, crypto_address)
        return table

    table = '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Crypto Transaction Fees</td><td>{}</td></tr><tr><td>Total Amount</td><td>{}</td></tr><tr><td>Email Address</td><td>{}</td></tr><tr><td>Phone Number</td><td>{}</td></tr><tr><td>{} Address</td><td>{}</td></tr></table></body></html>'.format(escaped_style, order_type, order_number, crypto_type, order_amount_crypto, fiat_type, order_amount_fiat, crypto_fees, total_amount, email_address, phone_number, crypto_type, crypto_address)
    return table
    


class EmailFormatter:
    """
    Handle all transaction email dispatch logic
    """

    def __init__(self, order_number, order_type, crypto_type, fiat_type, order_amount_crypto, order_amount_fiat, crypto_unit_price):
        self.style = 'table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}'
        self.escaped_style = html.escape(self.style)
        self.order_number = order_number
        self.order_type = order_type
        self.crypto_type = crypto_type
        self.fiat_type = fiat_type
        self.order_amount_crypto = order_amount_crypto
        self.order_amount_fiat = order_amount_fiat
        self.crypto_unit_price = crypto_unit_price

    def buy_email(self, email_address, phone_number, crypto_fees, crypto_fees_type, total_amount, crypto_address):
        return '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Crypto Unit Price</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Crypto Transaction Speed</td><td>{}</td></tr><tr><td>Crypto Transaction Fees</td><td>{}</td></tr><tr><td>Total Amount</td><td>{}</td></tr><tr><td>Email Address</td><td>{}</td></tr><tr><td>Phone Number</td><td>{}</td></tr><tr><td>{} Address</td><td>{}</td></tr></table></body></html>'.format(self.escaped_style, self.order_type, self.order_number, self.crypto_type, self.order_amount_crypto, self.crypto_unit_price, self.fiat_type, self.order_amount_fiat, crypto_fees_type, crypto_fees, total_amount, email_address, phone_number, self.crypto_type, crypto_address)

    def client_buy_email(self, crypto_fees, crypto_fees_type, total_amount):
        if(crypto_fees_type=="SLOW"):
            return  '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Crypto Transaction Speed</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Crypto Transaction Fees</td><td>{}</td></tr><tr><td>Total Amount</td><td>{}</td></tr></table><br><br><h3>Please Note: The crypto could up to 7 days to arrive to your wallet with the transaction speed chosen</h3><br><br><h3>WARNING: Please be ware of investment schemes that promise returns which are too good to be true. This usually ends up being a CON. binusu.com is not responsible for where you invest your money</h3></body></html>'.format(self.escaped_style, self.order_type, self.order_number, self.crypto_type, self.order_amount_crypto, crypto_fees_type, self.fiat_type, self.order_amount_fiat, crypto_fees, total_amount)

        if(crypto_fees_type=="MEDIUM"):
            return  '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Crypto Transaction Speed</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Crypto Transaction Fees</td><td>{}</td></tr><tr><td>Total Amount</td><td>{}</td></tr></table><br><br><h3>Please Note: The crypto could up to 24 hours to arrive to your wallet with the transaction speed chosen</h3><br><br><h3>WARNING: Please be ware of investment schemes that promise returns which are too good to be true. This usually ends up being a CON. binusu.com is not responsible for where you invest your money</h3></body></html>'.format(self.escaped_style, self.order_type, self.order_number, self.crypto_type, self.order_amount_crypto, crypto_fees_type, self.fiat_type, self.order_amount_fiat, crypto_fees, total_amount)

        if(crypto_fees_type=="FAST"):
            return  '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Crypto Transaction Speed</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Crypto Transaction Fees</td><td>{}</td></tr><tr><td>Total Amount</td><td>{}</td></tr></table><br><br><h3>Please Note: The crypto could up to 1 hour to arrive to your wallet with the transaction speed chosen</h3><br><br><h3>WARNING: Please be ware of investment schemes that promise returns which are too good to be true. This usually ends up being a CON. binusu.com is not responsible for where you invest your money</h3></body></html>'.format(self.escaped_style, self.order_type, self.order_number, self.crypto_type, self.order_amount_crypto, crypto_fees_type, self.fiat_type, self.order_amount_fiat, crypto_fees, total_amount)

    def sell_email(self, email_address, phone_number):
        return '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr><tr><td>Email Address</td><td>{}</td></tr><tr><td>Phone Number</td><td>{}</td></tr></table></body></html>'.format(self.escaped_style, self.order_type, self.order_number, self.crypto_type, self.order_amount_crypto, self.fiat_type, self.order_amount_fiat, email_address, phone_number)


    def client_sell_email(self):
        return  '<!DOCTYPE html><html><head><style>{}</style></head><body><h2>  {} Order Number: {} </h2><table><tr><th>Order Detail</th><th>Order Amount</th></tr><tr><td>Crypto Type</td><td>{}</td></tr><tr><td>Crypto Amount</td><td>{}</td></tr><tr><td>Fiat Amount ({})</td><td>{}</td></tr></table><br><br><h1>WARNING: Please be ware of investment schemes that promise returns which are too good to be true. This usually ends up being a CON. binusu.com is not responsible for where you invest your money</h1></body></html>'.format(self.escaped_style, self.order_type, self.order_number, self.crypto_type, self.order_amount_crypto, self.fiat_type, self.order_amount_fiat)


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

class AdminEmailFormatter:
    """
    Handle all admin related emails
    """

    def __init__(self, first_name):
        self.first_name = first_name

    def activate_account_email(self, otp):
        return "Hey {}, Please use the otp {} provided to activate your account".format(self.first_name, otp)
