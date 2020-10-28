import alpaca_trade_api as tradeapi
import time
import apikeys
import finnhub


finnhub_client = finnhub.Client(api_key=apikeys.FINN_API_KEY)

# Stock candles
print("hello")

API_KEY = apikeys.API_KEY
API_SECRET = apikeys.API_SECRET
APCA_API_BASE_URL = apikeys.APCA_API_BASE_URL

from datetime import datetime


def price(stock):
    api = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # Get daily price data for AAPL over the last 5 trading days.

    barset = api.get_barset(symbols=stock, timeframe='1Min', limit=1, start=dt_string)
    aapl_bars = barset[stock]
    print(barset)

    # See how much AAPL moved in that timeframe.
    # print(aapl_bars)
    current = aapl_bars[0].c

    return current

global counter
counter = 0
def get(stock):
    global counter
    #print("getting")
    print(counter)
    try:
        if counter >= 10:
            print("using finnhub")
            res = finnhub_client.quote('AAPL')

            print(res['c'])
            return res['c']
        else:
            first = price(stock)
    except Exception as e:
        print(e)
        time.sleep(0.5)
        first = get(stock)
        counter = counter + 1
        print(counter)
    return first
