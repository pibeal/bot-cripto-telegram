import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN=os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

# ======================
# DATABASE
# ======================

conn=sqlite3.connect("crypto.db",check_same_thread=False)
cursor=conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY)")
conn.commit()

# ======================
# OBTENER CRIPTOS
# ======================

def obtener_criptos():

    url="https://api.binance.com/api/v3/exchangeInfo"

    data=requests.get(url).json()

    lista=[]

    for s in data["symbols"]:

        if "USDT" in s["symbol"]:

            coin=s["symbol"].replace("USDT","")

            if coin not in lista:

                lista.append(coin)

    return lista[:200]

CRIPTO_LIST=obtener_criptos()

# ======================
# PRECIO
# ======================

def precio(symbol):

    try:

        url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

        data=requests.get(url).json()

        return float(data["price"])

    except:

        return None

# ======================
# HISTORIAL
# ======================

def historial(symbol):

    url=f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=200"

    data=requests.get(url).json()

    df=pd.DataFrame(data)

    df=df[[4]]

    df.columns=["close"]

    df["close"]=df["close"].astype(float)

    return df

# ======================
# GRAFICA PRO
# ======================

def grafica(symbol):

    df=historial(symbol)

    df["SMA20"]=df["close"].rolling(20).mean()
    df["SMA50"]=df["close"].rolling(50).mean()

    delta=df["close"].diff()

    gain=(delta.where(delta>0,0)).rolling(14).mean()
    loss=(-delta.where(delta<0,0)).rolling(14).mean()

    rs=gain/loss

    df["RSI"]=100-(100/(1+rs))

    plt.figure(figsize=(10,6))

    plt.subplot(2,1,1)

    plt.plot(df["close"],label="Precio")
    plt.plot(df["SMA20"],label="SMA20")
    plt.plot(df["SMA50"],label="SMA50")

    plt.legend()
    plt.title(symbol)

    plt.subplot(2,1,2)

    plt.plot(df["RSI"],label="RSI")

    plt.axhline(70)
    plt.axhline(30)

    plt.legend()

    plt.savefig("graf.png")

    plt.close()

# ======================
# IA TRADING
# ======================

def ia(symbol):

    df=historial(symbol)

    sma20=df["close"].rolling(20).mean().iloc[-1]
    sma50=df["close"].rolling(50).mean().iloc[-1]

    if sma20>sma50:

        return "🟢 Tendencia Alcista"

    if sma20<sma50:

        return "🔴 Tendencia Bajista"

    return "⚪ Mercado lateral"

# ======================
# TOP
# ======================

def top(n=10):

    texto=f"📊 TOP {n} CRIPTOS\n\n"

    for c in CRIPTO_LIST[:n]:

        p=precio(c)

        if p:

            texto+=f"{c} ${round(p,2)}\n"

    return texto

# ======================
# GANADORAS
# ======================

def ganadoras():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    top=sorted(data,key=lambda x:float(x["priceChangePercent"]),reverse=True)[:10]

    texto="🚀 GANADORAS\n\n"

    for c in top:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# ======================
# PERDEDORAS
# ======================

def perdedoras():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    top=sorted(data,key=lambda x:float(x["priceChangePercent"]))[:10]

    texto="📉 PERDEDORAS\n\n"

    for c in top:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# ======================
# SCANNER
# ======================

def scanner():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    top=sorted(data,key=lambda x:abs(float(x["priceChangePercent"])),reverse=True)[:10]

    texto="🔥 VOLATILIDAD\n\n"

    for c in top:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# ======================
# PUMPS
# ======================

def pumps():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    pumps=[c for c in data if float(c["priceChangePercent"])>8]

    texto="🚀 POSIBLE PUMP\n\n"

    for c in pumps[:10]:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# ======================
# GEMS
# ======================

def gems():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    gems=[c for c in data if float(c["priceChangePercent"])>5]

    texto="💎 GEMS\n\n"

    for c in gems[:10]:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# ======================
# MENU
# ======================

def menu():

    keyboard=[

    [InlineKeyboardButton("💰 BTC","btc"),
     InlineKeyboardButton("💰 ETH","eth")],

    [InlineKeyboardButton("📊 Top 10","top10"),
     InlineKeyboardButton("📊 Top 50","top50")],

    [InlineKeyboardButton("📊 Top 100","top100"),
     InlineKeyboardButton("🚀 Ganadoras","ganadoras")],

    [InlineKeyboardButton("📉 Perdedoras","perdedoras"),
     InlineKeyboardButton("🔥 Scanner","scanner")],

    [InlineKeyboardButton("🚀 Pumps","pumps"),
     InlineKeyboardButton("💎 Gems","gems")],

    [InlineKeyboardButton("🤖 IA BTC","ia"),
     InlineKeyboardButton("📈 Grafica BTC","graf")]

    ]

    return InlineKeyboardMarkup(keyboard)

# ======================
# START
# ======================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "🤖 BOT CRYPTO PRO\nSelecciona una opción:",

        reply_markup=menu()

    )

# ======================
# BOTONES
# ======================

async def botones(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    data=query.data

    chat=query.message.chat_id

    if data=="btc":

        p=precio("BTC")

        await context.bot.send_message(chat_id=chat,text=f"BTC ${p}",reply_markup=menu())

    elif data=="eth":

        p=precio("ETH")

        await context.bot.send_message(chat_id=chat,text=f"ETH ${p}",reply_markup=menu())

    elif data=="top10":

        await context.bot.send_message(chat,text=top(10),reply_markup=menu())

    elif data=="top50":

        await context.bot.send_message(chat,text=top(50),reply_markup=menu())

    elif data=="top100":

        await context.bot.send_message(chat,text=top(100),reply_markup=menu())

    elif data=="ganadoras":

        await context.bot.send_message(chat,text=ganadoras(),reply_markup=menu())

    elif data=="perdedoras":

        await context.bot.send_message(chat,text=perdedoras(),reply_markup=menu())

    elif data=="scanner":

        await context.bot.send_message(chat,text=scanner(),reply_markup=menu())

    elif data=="pumps":

        await context.bot.send_message(chat,text=pumps(),reply_markup=menu())

    elif data=="gems":

        await context.bot.send_message(chat,text=gems(),reply_markup=menu())

    elif data=="ia":

        await context.bot.send_message(chat,text=ia("BTC"),reply_markup=menu())

    elif data=="graf":

        grafica("BTC")

        await context.bot.send_photo(chat,photo=open("graf.png","rb"))

# ======================
# MAIN
# ======================

def main():

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(botones))

    print("BOT CRYPTO PRO ACTIVO")

    app.run_polling()

if __name__=="__main__":

    main()
