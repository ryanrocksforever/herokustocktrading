#Update 10-7

import stocker
import alpaca_trade_api as tradeapi
import time
import datetime
import requests
import re
import barthing
import json
import ast
import threading
import apikeys

API_KEY = apikeys.API_KEY
API_SECRET = apikeys.API_SECRET
APCA_API_BASE_URL = apikeys.APCA_API_BASE_URL
global prediction
prediction = 0
global anothernum
global tradablereal
anothernum = 0


class Actions:
    global prediction

    def __init__(self):
        self.tradablereal = True
        self.shortable = True
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
        #self.tradablereal
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
    def beststock(self, another, uponly):
        global anothernum
        skip=False
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"

        querystring = {"region": "US", "start": "0", "lang": "en-US", "count": "6"}

        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "714ff4f6eamsh9bc6892019abf3bp1df1b1jsn082fce7a6b7d"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # print(response.text)

        jsonfromit = json.loads(response.text)
        # print(jsonfromit['finance']['result'][0]['quotes'])
        try:
            quotes = jsonfromit['finance']['result'][0]["quotes"][anothernum]
        except:
            skip=True
            quotes = jsonfromit['finance']['result'][0]["quotes"][anothernum]
        print(quotes)

        stock = quotes["symbol"]
        print(stock)
        try:
            tradable = self.alpaca.get_asset(stock)
            print(tradable)
            self.shortable = tradable.shortable
            self.tradablereal = tradable.tradable
            print("Tradable: "+str(self.tradablereal))
            time.sleep(1)
            # tradable = tradable['tradable']

        except Exception as e:
            print(e)
            if skip is not True:
                anothernum = anothernum + 1
                self.beststock(anothernum, False)
            else:
                self.tradablereal = False
        if self.tradablereal is True and self.shortable is True:
            print("stock: " + stock)
            return stock
        else:
            print("Going TSLA")
            return "TSLA"

    def flatten(self, stock, qty, side):
        self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')
        print("Flattened: "+stock)

    def awaitMarketOpen(self):
        global prediction
        try:
            isOpen = self.alpaca.get_clock().is_open
        except:
            time.sleep(30)
            isOpen = self.alpaca.get_clock().is_open
        print("isOpen: " + str(isOpen))
        while not isOpen:
            clock = self.alpaca.get_clock()
            openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeToOpen = int((openingTime - currTime) / 60)
            print(str(timeToOpen) + " minutes til market open.")
            time.sleep(60)
            if (timeToOpen <= 10):
                print("predicting")
                stockfile = open("stockfile.txt", "r")
                stock = stockfile.readlines(1)[0]
                print("stock: " + stock)
                try:
                    prediction = self.project(stock)
                except:
                    time.sleep(2)
                    prediction = self.project(stock)
                print("prediction: " + str(prediction))
            try:
                isOpen = self.alpaca.get_clock().is_open
            except:
                print("error")
                self.awaitMarketOpen()

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
        try:
            clock = self.alpaca.get_clock()
        except:
            time.sleep(30)
            clock = self.alpaca.get_clock()
        closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        self.timeToClose = closingTime - currTime

        if self.timeToClose < (60 * 15):
            # Close all positions when 15 minutes til market close.
            print("Market closing soon.  Closing positions.")
            # side = 'sell'
            if start is not True:
                # self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')
                isOpen = self.alpaca.get_clock().is_open
                print("isOpen: " + str(isOpen))
                while isOpen:
                    clock = self.alpaca.get_clock()
                    closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
                    currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
                    timeToOpen = int((closingTime - currTime) / 60)
                    print(str(timeToOpen) + " minutes til market close.")
                    time.sleep(60)
                    try:
                        isOpen = self.alpaca.get_clock().is_open
                    except:
                        print("error")
                        self.awaitMarketClose(start=False)

    def isTradable(self, symbol):
        try:
            trad = self.alpaca.get_asset(symbol)
            if trad.tradable:
                return True
            else:
                return False
        except:
            return False

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
        print("Buying Power: " + str(buyingpower))
        if buyingpower == 0:
            print("0 is it, " + buyingpower)
            return 1000
        else:
            buyingminus = float(buyingpower)*0.005
            return float(buyingpower)-float(buyingminus)

    def getqty(self, stock):
        buybuy = Actions().getbuying()
        ga = barthing.get(stock)
        ga = float(ga)
        buybuy = float(buybuy)
        print(buybuy)
        safemon = buybuy - 100
        safega = ga
        amount = safemon / safega
        print(amount)
        amount = round(amount)
        print("amount: "+str(amount))
        return amount

    def decide(self, option):
        future = prediction
        print("future: " + str(future))
        try:
            realfuture = future[0]
        except:
            print("exception")
            realfuture = future
        symbol = option
        v = barthing.get(symbol=symbol)
        # real = future.asset
        current = v
        print("furture: "+str(future))
        print("realfuture: "+str(realfuture))
        print("current: "+str(current))

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
        betterorders = niceorders.replace("Order(", "").replace(")", "").replace("   ", "").replace("'", '"').replace(
            '":', '" :')
        bestorders = ast.literal_eval(betterorders)
        print(niceorders)
        print(betterorders)
        symbol = bestorders["symbol"]
        for key in bestorders.keys():
            print(key)

        print("FINAL ORDERS: " + repr(symbol))
        return bestorders

    def project(self, option):
        # stocker.predict
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
        previousprice = barthing.get(stock)
        while riseup is True:
            currentprice = barthing.get(stock)
            if previousprice >= currentprice <= previousprice - 0.5:
                self.submitOrder(stock=stock, qty=qty, side="sell")
                riseup = False

            time.sleep(30)
        else:
            self.ridedown(stock, startprice, qty)

    def ridedown(self, stock, startprice, qty):
        riseup = True
        previousprice = barthing.get(stock)
        while riseup is True:
            currentprice = barthing.get(stock)
            if previousprice <= currentprice >= previousprice + 0.5:
                self.submitOrder(stock=stock, qty=qty, side="buy")
                riseup = False

            time.sleep(30)
        else:
            self.rideup(stock, startprice, qty)


# Actions.saystock()

if __name__ == "__main__":
    Actions()
