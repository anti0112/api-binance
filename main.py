import requests
import json
import time
from const import headers

banks = ['Tinkoff', 'RosBank', 'QIWI', 'YandexMoney', 'RaiffeisenBankRussia',
         'PostBankRussia', 'MTSBank', 'HomeCreditBank', 'ABank', 'RUBfiatbalance',
         'Payeer', 'Advcash', 'Mobiletopup']

coins = ['USDT', 'BTC', 'BUSD', "BNB",'ETH', "RUB"]
all_page = {}
start = time.time()
for coin in coins:
    for page in range(1, 5):

        data = {
        "asset": coin,
        "fiat": "RUB",
        "merchantCheck": False,
        "page": page,
        "payTypes": [],
        "publisherType": None,
        "rows": 50,
        "tradeType": "BUY"
    }
        count = 0
        while True:   
            response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=data)
            obj = json.loads(response.text)
            
            if obj["code"] == "000000":
                for data in obj['data']:
                    price =  data['adv']['price']
                    coin = data['adv']['asset']
                    limit = data['adv']['minSingleTransAmount']
                    for pay in data['adv']['tradeMethods']:
                        bank = pay['payType']
                        if not all_page.get(limit):
                            all_page[limit]={}
                        else:
                            if bank in banks:
                                all_page[limit][bank]={coin:price}
                            continue
                        all_page[limit][bank]={coin:price}
                        if not all_page[limit].get(bank):
                            all_page[limit][bank] = {}
                        if not all_page[limit][bank].get(coin) or all_page[limit][bank][coin] > price:
                            all_page[limit][bank][coin]=price
                print(page)
                time.sleep(1)                     
                break
            time.sleep(1)
            print(f'Неудачный запрос:{obj}')
            continue

end = time.time()
with open('api.json', 'w') as f:
    json.dump(all_page, f)
    print(end - start)    