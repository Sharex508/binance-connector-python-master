import requests
import json

def get_response(url):
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()

def get_exchange_info():
  
    data = json.loads(requests.get(
        'https://api.binance.com/api/v3/ticker/price').text)

        

    #data =   get_response('https://api.binance.com/api/v3/ticker/price')
    print(data)
    filter='USDT'
    pd = data['symbols']
    full_data_dic = { s for s in pd if filter in s['symbol']}
    #resp = [d for d in data if d['quoteAsset'] == "inr"]
    return full_data_dic.keys()


def get_data():
     filter='USDT'
     data = json.loads(requests.get(
        'https://api.binance.com/api/v3/ticker/price').text)

     resp = [d for d in data if filter in d['symbol'] and 'price' in d]
     print(resp)
     rem_list = [
     'price']
     for obj in resp:
        for key in rem_list:
            obj.pop(key)
        lprice = obj.get('price', 0)

        #lprice = obj['price']
        marg=  float(lprice) + (float(lprice)/100)*3
        #mar = string(marg)
        obj.update({"intialPrice": lprice, "hightPrice": lprice,
                   "margin": marg, "purchasePrice": ""})
        print('completed')
     

     import requests

def getall_data(filter='USDT'):
    data = requests.get('https://api.binance.com/api/v3/ticker/price').json()

    # Filter data to include only symbols that contain the currency in the filter.
    resp = [d for d in data if filter in d['symbol'] and 'price' in d]
    
    # Update each dictionary in resp with additional keys.
    for obj in resp:
        lprice = float(obj['price'])
        marg = lprice * 1.03
        obj.update({
            "initialPrice": lprice,
            "highPrice": lprice,
            "margin": marg,
            "purchasePrice": ""
        })
        print('completed')
    
    return resp



    
getall_data()
