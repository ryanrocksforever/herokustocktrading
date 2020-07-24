import stocker
import alpaca_trade_api as tradeapi
import time
import datetime
import requests
import re
import barthing
import json
import ast

poop = stocker.predict.tomorrow('SBUX')
print(poop)

API_KEY = "PKRFE6TC81RILOIZETPN"
API_SECRET = "DFP5raNeqjoBDBbj4DMsmBQqEVAXrwgLVvSGclJa"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"


class Actions:

    def __init__(self):
        self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, 'v2')

        self.found = "AAPL"
        self.long = []
        self.short = []
        self.qShort = None
        self.qLong = None
        self.adjustedQLong = None
        self.adjustedQShort = None
        self.blacklist = set()
        self.longAmount = 0
        self.shortAmount = 0
        self.timeToClose = None
        # stockUniverse = [found, found1, found2, found3, found4, found5, found6, found7, found8, found9, found10,
        #                found11, found12, found13, found14, found15, found16, found17, ]
        # self.stockuniverse = stockUniverse
        # Format the allStocks variable for use in the class.
        # self.allStocks = []
        # for stock in stockUniverse:
        #   self.allStocks.append([stock, 0])

    # def saystock(self):
    #   stonks = self.stockuniverse
    #  print(stonks)
    def beststock(self):
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-movers"

        querystring = {"region": "US", "lang": "en"}

        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "714ff4f6eamsh9bc6892019abf3bp1df1b1jsn082fce7a6b7d"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

        m = re.findall('symbol":"(.+?)"}', response.text)

        if m:
            found = m[0]
            print(found)
        if m:
            found1 = m[1]
            print(found1)
        if m:
            found2 = m[2]
            print(found2)
        if m:
            found3 = m[3]
            print(found3)
        if m:
            found4 = m[4]
            print(found4)
        if m:
            found5 = m[5]
            print(found5)
        if m:
            found6 = m[6]
            print(found6)
        if m:
            found7 = m[7]
            print(found7)
        if m:
            found8 = m[8]
            print(found8)
        if m:
            found9 = m[9]
            print(found9)
        if m:
            found10 = m[10]
            print(found10)
        if m:
            found11 = m[11]
            print(found2)
        if m:
            found12 = m[12]
            print(found3)
        if m:
            found13 = m[13]
            print(found4)
        if m:
            found14 = m[14]
            print(found5)
        if m:
            found15 = m[1]
            print(found6)
        if m:
            found16 = m[16]
            print(found7)
        if m:
            found17 = m[17]
            print(found8)
        best = found
        return best


    def flatten(self, stock, qty, side):
        self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')

    def awaitMarketOpen(self):
        isOpen = self.alpaca.get_clock().is_open
        print(isOpen)
        while (not isOpen):
            clock = self.alpaca.get_clock()
            openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeToOpen = int((openingTime - currTime) / 60)
            print(str(timeToOpen) + " minutes til market open.")
            time.sleep(60)
            isOpen = self.alpaca.get_clock().is_open
    def closingTime(self):
        clock = self.alpaca.get_clock()
        closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        self.timeToClose = closingTime - currTime

        if (self.timeToClose < (60 * 15)):
            # Close all positions when 15 minutes til market close.
            print("Market closing soon.")


            return True
        else:
            return False

    def submitOrder(self, qty, stock, side):
        self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')
    def awaitMarketClose(self, qty, stock, side, start):
        clock = self.alpaca.get_clock()
        closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        self.timeToClose = closingTime - currTime

        if (self.timeToClose < (60 * 15)):
            # Close all positions when 15 minutes til market close.
            print("Market closing soon.  Closing positions.")
            side = 'sell'
            if start is not True:

                self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')



    def submitOrder(self, qty, stock, side):
        self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')

    # def price(self, symbol):
    #     # price = self.alpaca.get_asset(symbol=stock)
    #
    #     price = barget.get(stock=symbol)
    #     #thing = self.alpaca.get_barset(symbols=symbol, timeframe='minute', limit=1)
    #     #real = thing
    #     print(price)
    #     return price
    def getbuying(self):
        acount = self.alpaca.get_account()
        buyingpower = acount.buying_power
        print(buyingpower)
        return buyingpower

    def getqty(self, stock):
        buybuy = Actions().getbuying()
        ga = barthing.get(stock)
        ga = float(ga)
        buybuy = float(buybuy)
        safemon = buybuy - 100
        safega = round(ga)
        amount = safemon/safega
        amount = round(amount)
        return amount
    def decide(self, option):
        future = stocker.predict.tomorrow(option, steps=2, training=0.99, period=20, years=1, error_method='mape')
        realfuture = future[0]
        symbol = option
        v = barthing.get(symbol=symbol)
        # real = future.asset
        current = v
        print(future)
        print(realfuture)
        print(current)

        if current <= realfuture:
            return False
        else:
            return True
    def getorders(self):

        orders = self.alpaca.list_orders(
            status='closed',
            limit=100,
            nested=True  # show nested multi-leg orders
        )
        niceorders = str(orders[0])
        betterorders = niceorders.replace("Order(", "").replace(")", "").replace("   ", "").replace("'", '"').replace('":', '" :')
        bestorders = ast.literal_eval(betterorders)
        print(niceorders)
        print(betterorders)
        symbol = bestorders["symbol"]
        for key in bestorders.keys():
            print(key)

        print("FINAL ORDERS: " + repr(symbol))
        return bestorders
    def project(self, option):
        future = stocker.predict.tomorrow(option, steps=2, training=0.99, period=20, years=1, error_method='mape')
        return future[0]

    def best(self):
        best = self.found

        return best

    def profit(self):
        account = self.alpaca.get_account()
        balance_change = float(account.equity) - float(account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')
        return round(balance_change, 2)

    def rideup(self, stock, startprice, qty):
        riseup = True
        previousprice = barthing.get
        while riseup is True:
            currentprice = barthing.get(stock)
            if previousprice >= currentprice <= previousprice - 0.5:
                self.submitOrder(qty, stock, "sell")
                riseup = False

            time.sleep(30)

    def ridedown(self, stock, startprice, qty):
        riseup = True
        previousprice = barthing.get
        while riseup is True:
            currentprice = barthing.get(stock)
            if previousprice <= currentprice >= previousprice + 0.5:
                self.submitOrder(qty, stock, "buy")
                riseup = False

            time.sleep(30)








# Actions.saystock()

if __name__ == "__main__":
    Actions()
