from datetime import datetime
from common import fetch_push, convert_to_utc, add_random_time

def ticker(body, **kargs):
    body = body['data']
    return [{
            "measurement": "ticker",
            "tags": {
                "xchg": "bithumb",
                "currency": kargs['currency']
            },
            "timestamp": datetime.fromtimestamp(int(body['date'])/1000).strftime('%Y-%m-%dT%H:%M:%S%z'),
            "fields": {
                "last": int(float(body['closing_price'])),
            }
        }]

lastBidTime = 0
lastAskTime = 0

def orderbook(body, **kargs):
    body = body['data']
    timestamp = datetime.fromtimestamp(int(body['timestamp'])).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    data = []
    for item in body['bids']:
        data.append({
                "measurement": "orderbook",
                "tags": {
                    "xchg": "bithumb",
                    "currency": kargs['currency'],
                    "type": "bid",
                },
                "timestamp": timestamp,
                "fields": {
                    "price": int(float(item['price'])),
                    "qty": float(item['quantity']),
                },
            })

    for item in body['asks']:
        data.append({
                "measurement": "orderbook",
                "tags": {
                    "xchg": "bithumb",
                    "currency": kargs['currency'],
                    "type": "ask",
                },
                "time": timestamp,
                "fields": {
                    "price": int(item['price']),
                    "qty": float(item['quantity']),
                },
            })

    return data

# datetime.strptime('2015-04-20 11:17:21','%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S%z')
lastTradeTime = convert_to_utc('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

def trade(body, **kargs):
    data = []
    global lastTradeTime
    tempTime = lastTradeTime

    # print("data{} size is {}".format(kargs['currency'], len(body['data'])))
    # print("lt: {}".format(lastTradeTime))
    
    for item in body['data']:
        currentTradeTime = convert_to_utc(item['transaction_date'], '%Y-%m-%d %H:%M:%S')

        if currentTradeTime <= lastTradeTime:
            # print("skip ct < lt: {}".format(currentTradeTime))
            continue
        elif tempTime < currentTradeTime:
            # print("ct > lt: {}".format(currentTradeTime))
            tempTime = currentTradeTime

        currentTradeTime = add_random_time(currentTradeTime)
        # print("insert {}".format(currentTradeTime))

        data.append({
                "measurement": "trade",
                "tags": {
                    "xchg": "bithumb",
                    "currency": kargs['currency'],
                    "type": item['type'],
                },
                "time": currentTradeTime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "fields": {
                    "price": int(float(item['price'])),
                    "qty": float(item['units_traded']),
                    "total": float(item['total'])
                },
            })

    # print(data)

    lastTradeTime = tempTime

    return data

def run():
    currency = ['btc', 'eth', 'xrp', 'bch']

    for c in currency:
        fetch_push('https://api.bithumb.com/public/ticker/{}'.format(c), ticker, 5, currency=c)
        # fetch_push('https://api.bithumb.com/public/orderbook/{}'.format(c), orderbook, 5, currency=c)
        fetch_push('https://api.bithumb.com/public/recent_transactions/{}'.format(c), trade, 5, currency=c)