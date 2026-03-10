import os
import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("crypto.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
plan TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS alertas(
user_id INTEGER,
cripto TEXT,
precio REAL
)
""")

conn.commit()

# =========================
# LISTA CRIPTOS
# =========================

TOP10 = [
"BTC","ETH","BNB","SOL","XRP",
"ADA","DOGE","AVAX","DOT","MATIC"
]

# =========================
# PRECIO BINANCE
# =========================

def precio(symbol):

    try:

        url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

        data=requests.get(url,timeout=10).json()

        return float(data["price"])

    except:

        return None


# =========================
# HISTORIAL
# =========================

def historial(symbol):

    url=f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=200"

    data=requests.get(url).json()

    df=pd.DataFrame(data)

    df=df[[4]]

    df.columns=["close"]

    df["close"]=df["close"].astype(float)

    return df

# =========================
# IA TENDENCIA
# =========================

def ia_trading(symbol):

    df=historial(symbol)

    sma20=df["close"].rolling(20).mean().iloc[-1]

    sma50=df["close"].rolling(50).mean().iloc[-1]

    if sma20>sma50:

        return "🟢 Tendencia Alcista"

    elif sma20<sma50:

        return "🔴 Tendencia Bajista"

    else:

        return "⚪ Mercado lateral"


# =========================
# SCANNER MERCADO
# =========================

def scanner():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    top=sorted(data,key=lambda x:abs(float(x["priceChangePercent"])),reverse=True)[:10]

    texto="🔥 MOVIMIENTOS DEL MERCADO\n\n"

    for c in top:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto


# =========================
# DETECTOR PUMP
# =========================

def detectar_pump():

    url="https://api.binance.com/api/v3/ticker/24hr"

    data=requests.get(url).json()

    pumps=[c for c in data if float(c["priceChangePercent"])>8]

    texto="🚀 POSIBLE PUMP\n\n"

    for c in pumps[:10]:

        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto


# =========================
# GRAFICA
# =========================

def grafica(symbol):

    df=historial(symbol)

    df["close"].plot(title=symbol)

    plt.savefig("graf.png")

    plt.close()


# =========================
# MENU
# =========================

def menu():

    keyboard=[

        [InlineKeyboardButton("💰 Precio BTC",callback_data="btc"),
         InlineKeyboardButton("💰 Precio ETH",callback_data="eth")],

        [InlineKeyboardButton("📊 Top 10",callback_data="top10"),
         InlineKeyboardButton("🔥 Scanner Mercado",callback_data="scanner")],

        [InlineKeyboardButton("🚀 Detectar Pump",callback_data="pump"),
         InlineKeyboardButton("🤖 IA BTC",callback_data="ia")],

        [InlineKeyboardButton("📈 Gráfica BTC",callback_data="graf")]

    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.message.from_user.id

    cursor.execute("INSERT OR IGNORE INTO users VALUES(?,?)",(user,"free"))

    conn.commit()

    await update.message.reply_text(

        "🤖 BOT CRYPTO PRO V2\n\nSelecciona una opción:",

        reply_markup=menu()

    )


# =========================
# BOTONES
# =========================

async def botones(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query

    await query.answer()

    data=query.data

    if data=="btc":

        p=precio("BTC")

        await query.edit_message_text(f"BTC ${p}",reply_markup=menu())

    elif data=="eth":

        p=precio("ETH")

        await query.edit_message_text(f"ETH ${p}",reply_markup=menu())

    elif data=="top10":

        texto="📊 TOP 10\n\n"

        for c in TOP10:

            p=precio(c)

            texto+=f"{c} ${p}\n"

        await query.edit_message_text(texto,reply_markup=menu())

    elif data=="scanner":

        texto=scanner()

        await query.edit_message_text(texto,reply_markup=menu())

    elif data=="pump":

        texto=detectar_pump()

        await query.edit_message_text(texto,reply_markup=menu())

    elif data=="ia":

        señal=ia_trading("BTC")

        await query.edit_message_text(f"🤖 IA BTC\n\n{señal}",reply_markup=menu())

    elif data=="graf":

        grafica("BTC")

        await context.bot.send_photo(

            chat_id=query.message.chat_id,

            photo=open("graf.png","rb")

        )


# =========================
# ALERTAS
# =========================

async def revisar_alertas(context:ContextTypes.DEFAULT_TYPE):

    cursor.execute("SELECT user_id,cripto,precio FROM alertas")

    datos=cursor.fetchall()

    for user,cripto,p in datos:

        try:

            actual=precio(cripto)

            if actual and actual>=p:

                await context.bot.send_message(

                    chat_id=user,

                    text=f"🚨 {cripto} llegó a ${actual}"

                )

        except:

            pass


# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))

    # alertas cada minuto
    app.job_queue.run_repeating(revisar_alertas, interval=60)

    print("🚀 BOT CRYPTO PRO V2 ACTIVO")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__=="__main__":

    main()

