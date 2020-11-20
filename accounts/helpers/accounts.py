import random
from ..models import Otp
from ..serializers.user_serializer import OtpSerializer
from twilio.rest import Client 

account_sid = 'ACb8f3027fa07c3ffe6878e909433299b3' 
auth_token = '2f9e31d6ff434826baa59897deafd946' 
client = Client(account_sid, auth_token)

def generate_otp():
    return random.randint(0000, 9999)

def send_otp(user, phone_number, first_name):
    otp_code = generate_otp()
    otp_data = {
        "user": user,
        "otp_code": otp_code
    }
    try:
        message = client.messages.create( 
            from_='+12565968086', 
            messaging_service_sid='MG5148a7ac276a7476c43006229884be88', 
            body='Welcome {}, to Binusu Loyalty Wallet, Your One Time Password is {}'.format(first_name, otp_code),      
            to=phone_number
        ) 
        otp_save = OtpSerializer(data=otp_data)
        otp_save.is_valid(raise_exception=True)
        otp_save.save()
        return True
    except:
        return False


