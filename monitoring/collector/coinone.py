from datetime import datetime
from common import fetch_push, add_random_time

def ticker(body):
    return [{
            "measurement": "ticker",
            "tags": {
                "xchg": "coinone",
                "currency": body['currency']
            },
            "timestamp": datetime.fromtimestamp(int(body['timestamp'])).strftime('%Y-%m-%dT%H:%M:%S%z'),
            "fields": {
                "last": int(body['last']),
            }
        }]

def orderbook(body):
    timestamp = datetime.fromtimestamp(int(body['timestamp'])).strftime('%Y-%m-%dT%H:%M:%S%z')
    data = []
    for item in body['bid']:
        data.append({
                "measurement": "orderbook",
                "tags": {
                    "xchg": "coinone",
                    "currency": body['currency'],
                    "type": "bid",
                },
                "timestamp": timestamp,
                "fields": {
                    "price": int(item['price']),
                    "qty": float(item['qty']),
                },
            })

    for item in body['ask']:
        data.append({
                "measurement": "orderbook",
                "tags": {
                    "xchg": "coinone",
                    "currency": body['currency'],
                    "type": "ask",
                },
                "timestamp": timestamp,
                "fields": {
                    "price": int(item['price']),
                    "qty": float(item['qty']),
                },
            })

    return data

lastTradeTime = datetime.utcnow()

def trade(body):
    data = []
    global lastTradeTime
    tempTime = lastTradeTime

    for item in body['completeOrders']:
        currentTradeTime = datetime.fromtimestamp(int(item['timestamp']))

        if currentTradeTime <= lastTradeTime:
            continue
        elif tempTime < currentTradeTime:
            tempTime = currentTradeTime
        
        currentTradeTime = add_random_time(currentTradeTime)

        data.append({
                "measurement": "trade",
                "tags": {
                    "xchg": "coinone",
                    "currency": body['currency'],
                },
                "timestamp": currentTradeTime.strftime('%Y-%m-%dT%H:%M:%S%z'),
                "fields": {
                    "price": int(item['price']),
                    "qty": float(item['qty']),
                },
            })

    lastTradeTime = tempTime

    return data

def run():
    currency = ['btc', 'eth', 'xrp', 'bch']

    for c in currency:
        fetch_push('https://api.coinone.co.kr/ticker?currency={}'.format(c), ticker, 5)
        # fetch_push('https://api.coinone.co.kr/orderbook?currency={}'.format(c), orderbook, 5)
        fetch_push('https://api.coinone.co.kr/trades?currency={}'.format(c), trade, 5)