import os
import sqlite3
import asyncio
import time
import yfinance as yf
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# =========================
# TOKEN
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN no configurado")

# =========================
# BASE DE DATOS
# =========================

conn = sqlite3.connect("crypto.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alertas(
chat_id INTEGER,
crypto TEXT,
precio REAL
)
""")

conn.commit()

# =========================
# CRIPTOS
# =========================

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

# =========================
# CACHE DE PRECIOS
# =========================

price_cache = {}
cache_time = {}

CACHE_DURATION = 60

def get_price(symbol):

    now = time.time()

    if symbol in price_cache and now - cache_time[symbol] < CACHE_DURATION:
        return price_cache[symbol]

    data = yf.Ticker(symbol).history(period="1d")

    price = data["Close"].iloc[-1]

    price_cache[symbol] = price
    cache_time[symbol] = now

    return price


def get_history(symbol,period="3mo"):

    data = yf.Ticker(symbol).history(period=period)

    return data

# =========================
# MERCADO
# =========================

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

# =========================
# INDICADORES
# =========================

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

# =========================
# ANALISIS
# =========================

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

# =========================
# GRAFICA
# =========================

def create_chart(data,crypto):

    plt.figure(figsize=(10,5))

    data["Close"].plot()

    plt.title(f"{crypto} price")

    file=f"{crypto}.png"

    plt.savefig(file)

    plt.close()

    return file

# =========================
# ALERTAS
# =========================

async def check_alerts(app):

    while True:

        try:

            cursor.execute("SELECT chat_id,crypto,precio FROM alertas")

            alertas=cursor.fetchall()

            for chat_id,crypto,precio in alertas:

                current_price=get_price(cryptos[crypto])

                if current_price>=precio:

                    await app.bot.send_message(
                    chat_id=chat_id,
                    text=f"🚨 ALERTA\n{crypto} llegó a ${current_price:.2f}"
                    )

                    cursor.execute(
                    "DELETE FROM alertas WHERE chat_id=? AND crypto=?",
                    (chat_id,crypto)
                    )

                    conn.commit()

        except Exception as e:

            print("Error alertas:",e)

        await asyncio.sleep(60)

# =========================
# MENU
# =========================

def menu():

    keyboard=[
[InlineKeyboardButton("💰 Precio BTC",callback_data="price")],
[InlineKeyboardButton("📊 Grafica BTC",callback_data="chart")],
[InlineKeyboardButton("🤖 Analisis BTC",callback_data="analysis")],
[InlineKeyboardButton("🏆 Mercado",callback_data="market")]
]

    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
"🚀 CRYPTO BOT PROFESIONAL",
reply_markup=menu()
)

# =========================
# BOTONES
# =========================

async def buttons(update,context):

    query=update.callback_query

    await query.answer()

    data=query.data

    if data=="price":

        price=get_price("BTC-USD")

        await query.message.reply_text(f"BTC ${price:.2f}")

    if data=="chart":

        data=get_history("BTC-USD")

        file=create_chart(data,"BTC")

        await query.message.reply_photo(photo=open(file,"rb"))

    if data=="analysis":

        data=get_history("BTC-USD")

        trend,rsi,signal=analyze(data)

        await query.message.reply_text(
f"Tendencia: {trend}\nRSI: {rsi:.2f}\nSeñal: {signal}"
)

    if data=="market":

        top=market_scan()

        text="🏆 MERCADO\n\n"

        for c,p in top:

            text+=f"{c} {p:.2f}%\n"

        await query.message.reply_text(text)

# =========================
# ALERTA
# =========================

async def alerta(update:Update,context:ContextTypes.DEFAULT_TYPE):

    try:

        crypto=context.args[0].upper()
        precio=float(context.args[1])

        cursor.execute(
        "INSERT INTO alertas VALUES(?,?,?)",
        (update.message.chat_id,crypto,precio)
        )

        conn.commit()

        await update.message.reply_text(
        f"Alerta creada para {crypto} en ${precio}"
        )

    except:

        await update.message.reply_text(
        "Uso correcto:\n/alerta BTC 50000"
        )

# =========================
# MAIN
# =========================

async def main():

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("alerta",alerta))
    app.add_handler(CallbackQueryHandler(buttons))

    asyncio.create_task(check_alerts(app))

    print("BOT ACTIVO")

    await app.run_polling()

if __name__=="__main__":

    asyncio.run(main())
