import requests

def get_rates():
    binusu_url = 'https://binusu.com/rates.php?json=1'
    rates_call = requests.post(binusu_url)
    return rates_call.json()