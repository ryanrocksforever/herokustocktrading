import alpaca_trade_api as tradeapi
import time
import apikeys

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


def get(stock):
    try:
        first = price(stock)
    except:
        first = get(stock)
    return first
