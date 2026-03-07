from indicators import RSI,MACD,EMA,bollinger

def analyze(data):

    rsi = RSI(data)

    macd,signal = MACD(data)

    ema20 = EMA(data,20).iloc[-1]
    ema50 = EMA(data,50).iloc[-1]

    upper,lower = bollinger(data)

    price = data["Close"].iloc[-1]

    trend="BAJISTA"

    if ema20>ema50:
        trend="ALCISTA"

    signal_trade="NEUTRAL"

    if rsi<30 and price<lower:
        signal_trade="COMPRA"

    if rsi>70 and price>upper:
        signal_trade="VENTA"

    return trend,rsi,signal_trade
