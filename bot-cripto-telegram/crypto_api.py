import yfinance as yf

def get_price(symbol):

    data = yf.Ticker(symbol).history(period="1d")

    return data["Close"].iloc[-1]


def get_history(symbol,period="3mo"):

    data = yf.Ticker(symbol).history(period=period)

    return data
