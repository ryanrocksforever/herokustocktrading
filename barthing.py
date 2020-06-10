import barset as barget
def get(symbol):
    symbol = "AAPL"
    v = barget.get(stock=symbol)
    print(v)
    return v