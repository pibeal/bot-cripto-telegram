import pandas as pd

def EMA(data,period):

    return data["Close"].ewm(span=period).mean()


def RSI(data):

    delta = data["Close"].diff()

    gain = (delta.where(delta>0,0)).rolling(14).mean()
    loss = (-delta.where(delta<0,0)).rolling(14).mean()

    rs = gain/loss

    rsi = 100-(100/(1+rs))

    return rsi.iloc[-1]


def MACD(data):

    ema12 = data["Close"].ewm(span=12).mean()
    ema26 = data["Close"].ewm(span=26).mean()

    macd = ema12-ema26

    signal = macd.ewm(span=9).mean()

    return macd.iloc[-1],signal.iloc[-1]


def bollinger(data):

    ma = data["Close"].rolling(20).mean()

    std = data["Close"].rolling(20).std()

    upper = ma + (2*std)
    lower = ma - (2*std)

    return upper.iloc[-1],lower.iloc[-1]
