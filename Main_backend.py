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

API_KEY = "PKW2FI9P4854V34RX698"
API_SECRET = "BIyasVLegtVpSq5ug2zilpIuGAeMFUaeqZZPd06R"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
global prediction
prediction = 0

class Actions:
    global prediction

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
    def beststock(self, uponly):
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"

        querystring = {"region": "US", "start": "0", "lang": "en-US", "count": "6"}

        headers = {
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
            'x-rapidapi-key': "714ff4f6eamsh9bc6892019abf3bp1df1b1jsn082fce7a6b7d"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        #print(response.text)

        jsonfromit = json.loads(response.text)
        # print(jsonfromit['finance']['result'][0]['quotes'])
        quotes = jsonfromit['finance']['result'][0]["quotes"][0]


        stock = quotes["symbol"]
        try:
            tradable = self.alpaca.get_asset(stock)
            tradable = json.loads(tradable)
            tradable = tradable["tradable"]
        except:
            tradable = False    
        if tradable:
            print(stock)
            return stock
        else:
            print("Going TSLA")
            return "TSLA"
        

    def flatten(self, stock, qty, side):
        self.alpaca.submit_order(symbol=stock, qty=qty, side=side, type='market', time_in_force='gtc')

    def awaitMarketOpen(self):
        global prediction
        isOpen = self.alpaca.get_clock().is_open
        print(isOpen)
        while (not isOpen):
            clock = self.alpaca.get_clock()
            openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            timeToOpen = int((openingTime - currTime) / 60)
            print(str(timeToOpen) + " minutes til market open.")
            time.sleep(60)
            if(timeToOpen <=10):
                print("predicting")
                stockfile = open("stockfile.txt", "r")
                stock = stockfile.readlines(1)[0]
                print(stock)
                try:
                    prediction = self.project(stock)
                except:
                    time.sleep(2)
                    prediction = self.project(stock)
                print(prediction)
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
                print(isOpen)
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
        print(buyingpower)
        if buyingpower == 0 or "0" in buyingpower:
            print("0 is it")
            return 1000
        else:
            return buyingpower

    def getqty(self, stock):
        buybuy = Actions().getbuying()
        ga = barthing.get(stock)
        ga = float(ga)
        buybuy = float(buybuy)
        safemon = buybuy - 100
        safega = round(ga)
        amount = safemon / safega
        amount = round(amount)
        return amount

    def decide(self, option):
        future = prediction
        print(future)
        try:
        	realfuture=future[0]
        except:
        	print("exception")
        	realfuture=future
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
        stocker.predict
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
                self.submitOrder(qty, stock, "sell")
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
                self.submitOrder(qty, stock, "buy")
                riseup = False

            time.sleep(30)
        else:
            self.rideup(stock, startprice, qty)


# Actions.saystock()

if __name__ == "__main__":
    Actions()
