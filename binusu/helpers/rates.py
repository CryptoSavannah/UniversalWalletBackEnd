import requests

def get_rates(baseCurrency):
    if(baseCurrency=="KES"):
        binusu_url = 'https://staging.binusu.com/rates.php?json=1&baseCurrency=KES'
    else:
        binusu_url = 'https://staging.binusu.com/rates.php?json=1'
    
    rates_call = requests.get(binusu_url)
    return rates_call.json()

def trigger_collection(data):
    try:
        url = "https://bnuaz3.binusu.com/node/api.php"
        trigger_call = requests.post(url, data)
        return trigger_call.json()
    except:
        return False