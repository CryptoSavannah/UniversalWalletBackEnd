import random
import string
from loyalty_api.settings import ENVIRONMENT

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    if ENVIRONMENT=="TESTING":
        return "{}{}".format("TEST-", result_str)
    else:
        return "{}{}".format("BN", result_str)

def generate_otp():
    return random.randint(1000, 9999)