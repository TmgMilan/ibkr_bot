tickers = set()

def addTicker(arg):
    tickers.add(arg.upper())

def deleteTicker(arg):
    tickers.discard(arg.upper())

def getTicker():
    if not tickers:
        return "{}"
    return tickers
