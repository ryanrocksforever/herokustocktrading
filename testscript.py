import alpaca_trade_api as tradeapi
import apikeys
API_KEY = apikeys.API_KEY
API_SECRET = apikeys.API_SECRET
APCA_API_BASE_URL = apikeys.APCA_API_BASE_URL
alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

stock = "TSLA"
tradable = alpaca.get_asset(stock)
print(tradable)