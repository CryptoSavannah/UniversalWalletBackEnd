import requests

def get_rates():
    binusu_url = 'https://staging.binusu.com/rates.php?json=1'
    rates_call = requests.get(binusu_url)
    return rates_call.json()