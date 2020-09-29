import stocker
import alpaca_trade_api as tradeapi
import threading
import time
import datetime
import requests
import re
import pandas as pd
import Main_backend as back
import barset as barget


# pooo = Main_backend.Actions().saystock()
# print(pooo)
class mainstuff:
    def __init__(self):
        # self.best = back.Actions().beststock()
        self.best = back.Actions().beststock(uponly=False)
        self.runthing = True

    def run(self):
        stock = self.best
        # qty = back.Actions().getqty(stock)
        qty = back.Actions().getqty(stock)
        print(qty)
        back.Actions().awaitMarketClose(qty=qty, stock=self.best, side="sell", start=True)
        back.Actions().awaitMarketOpen()
        if back.Actions().closingTime() is True:
            # time.sleep(96000)
            print("sleeping 15 min")
            back.Actions().awaitMarketOpen()

        else:
            print("market open")

        amount = qty
        # stock = back.best()

        print(stock)
        abcd = back.Actions().decide(option=stock)
        print(abcd)

        if abcd is True:
            print("going down")
            power = back.Actions().getbuying()
            power = float(power)
            print(power)
            symbol = stock
            v = barget.get(stock=symbol)
            real = float(v)
            project = back.Actions().project(option=stock)
            project = float(project)
            sideabc = "buy"
            goal = project - 0.5
            if power > real:

                while back.Actions().closingTime() is not True:
                    back.Actions().rideup(stock, 0, qty)


                else:
                    if back.Actions().closingTime() is True:
                        v = barget.get(stock=symbol)
                        real = float(v)
                        print("buying")
                        print(real)
                        print("<")
                        print(goal)
                        back.Actions().flatten(stock=symbol, qty=amount, side="buy")

            else:
                print("not enough power")
        else:
            print("going up")
            power = back.Actions().getbuying()
            power = float(power)
            print(power)
            symbol = stock
            v = barget.get(stock=symbol)
            real = float(v)
            project = back.Actions().project(option=stock)
            project = float(project)
            goal = project + 0.5
            sideabc = "sell"
            if power > real:

                while back.Actions().closingTime() is not True:
                    back.Actions().ridedown(stock, 0, qty)


                else:
                    if back.Actions().closingTime() is True:
                        v = barget.get(stock=symbol)
                        real = float(v)
                        print("buying")
                        print(real)
                        print("<")
                        print(goal)
                        back.Actions().flatten(stock=symbol, qty=amount, side="buy")
            else:
                print("not enough power")

        closdown = False
        while closdown is not True:
            closdown = back.Actions().closingTime()
            time.sleep(30)

        back.Actions().awaitMarketClose(stock=stock, qty=amount, side=sideabc, start=False)
        print(back.Actions().profit())
        back.Actions().awaitMarketOpen()
        mainstuff().run()

    def goodday(self, stock):
        future = back.Actions().project(option=stock)
        return future

    def stop(self):
        self.runthing = False

    def abcabc(self):
        #        qty = back.Actions().getqty()
        mainstuff().run()

        # else:
        #   print("badbad")


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    mainstuff()
