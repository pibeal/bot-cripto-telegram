from crypto_api import get_history

cryptos = {

"BTC":"BTC-USD",
"ETH":"ETH-USD",
"BNB":"BNB-USD",
"SOL":"SOL-USD",
"XRP":"XRP-USD",
"ADA":"ADA-USD",
"DOGE":"DOGE-USD",
"AVAX":"AVAX-USD",
"MATIC":"MATIC-USD",
"DOT":"DOT-USD"

}

def market_scan():

    results=[]

    for c,t in cryptos.items():

        data=get_history(t,"2d")

        today=data["Close"].iloc[-1]
        yesterday=data["Close"].iloc[-2]

        change=((today-yesterday)/yesterday)*100

        results.append((c,change))

    results.sort(key=lambda x:x[1],reverse=True)

    return results
