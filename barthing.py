import barset as barget
def get(symbol):

    v = barget.get(stock=symbol)
    print(v)
    return v