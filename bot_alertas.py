import os
import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CallbackQueryHandler,
CommandHandler,
ContextTypes
)

TOKEN = os.getenv("TOKEN")

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
# CRIPTOS
# =========================

TOP50 = [
"BTC","ETH","BNB","XRP","ADA","SOL","DOGE","DOT","MATIC","LTC",
"LINK","UNI","AVAX","TRX","SHIB","XLM","ETC","ATOM","FIL","AAVE",
"NEAR","APT","ARB","OP","INJ","SUI","PEPE","RNDR","SEI","IMX",
"GRT","SAND","MANA","FLOW","EGLD","XTZ","ALGO","KAVA","HBAR","ICP",
"QNT","FTM","RUNE","AXS","THETA","EOS","MKR","SNX","CRV","CHZ"
]

GRAFICAS = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC"]

# =========================
# API BINANCE
# =========================

def precio(symbol):

    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

    data=requests.get(url).json()

    return float(data["price"])

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
# IA SIMPLE
# =========================

def ia_trading(symbol):

    df=historial(symbol)

    rsi=df["close"].pct_change().rolling(14).mean().iloc[-1]

    sma50=df["close"].rolling(50).mean().iloc[-1]

    precio_actual=df["close"].iloc[-1]

    if rsi<0 and precio_actual>sma50:

        return "🟢 Señal COMPRA"

    elif rsi>0:

        return "🔴 Señal VENTA"

    else:

        return "⚪ Mercado lateral"

# =========================
# MENU
# =========================

def menu():

    keyboard=[

        [InlineKeyboardButton("💰 Precio BTC",callback_data="btc"),
         InlineKeyboardButton("💰 Precio ETH",callback_data="eth")],

        [InlineKeyboardButton("📊 Top 10",callback_data="top10"),
         InlineKeyboardButton("💰 Top 50",callback_data="top50")],

        [InlineKeyboardButton("🚀 Ganadoras",callback_data="ganadoras"),
         InlineKeyboardButton("📉 Perdedoras",callback_data="perdedoras")],

        [InlineKeyboardButton("🤖 IA Trading BTC",callback_data="ia")],

        [InlineKeyboardButton("📊 Ver Gráficas",callback_data="graficas")],

        [InlineKeyboardButton("🔥 Scanner Mercado",callback_data="scanner")],

        [InlineKeyboardButton("💎 Activar Premium",callback_data="premium")]

    ]

    return InlineKeyboardMarkup(keyboard)

# =========================
# MENU GRAFICAS
# =========================

def menu_graficas():

    keyboard=[]

    fila=[]

    for c in GRAFICAS:

        fila.append(InlineKeyboardButton(c,callback_data=f"graf_{c}"))

        if len(fila)==3:

            keyboard.append(fila)

            fila=[]

    keyboard.append(fila)

    keyboard.append([InlineKeyboardButton("⬅️ Volver",callback_data="menu")])

    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.message.from_user.id

    cursor.execute("INSERT OR IGNORE INTO users VALUES(?,?)",(user,"free"))

    conn.commit()

    await update.message.reply_text(

        "🤖 BOT CRYPTO PREMIUM\n\nSelecciona opción:",

        reply_markup=menu()

    )

# =========================
# BOTONES
# =========================

async def botones(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query

    await query.answer()

    data=query.data

    if data=="menu":

        await query.edit_message_text(

        "Menú principal",

        reply_markup=menu()

        )

# PRECIO BTC

    elif data=="btc":

        p=precio("BTC")

        await query.edit_message_text(

        f"💰 BTC ${p:.2f}",

        reply_markup=menu()

        )

# PRECIO ETH

    elif data=="eth":

        p=precio("ETH")

        await query.edit_message_text(

        f"💰 ETH ${p:.2f}",

        reply_markup=menu()

        )

# TOP 10

    elif data=="top10":

        lista=["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC"]

        texto="📊 TOP 10\n\n"

        for c in lista:

            texto+=f"{c} ${precio(c):.2f}\n"

        await query.edit_message_text(

        texto,

        reply_markup=menu()

        )

# TOP 50

    elif data=="top50":

        texto="💰 TOP 50\n\n"

        for c in TOP50:

            try:

                texto+=f"{c} ${precio(c):.2f}\n"

            except:

                pass

        await query.edit_message_text(

        texto[:4000],

        reply_markup=menu()

        )

# GANADORAS

    elif data=="ganadoras":

        url="https://api.binance.com/api/v3/ticker/24hr"

        data=requests.get(url).json()

        top=sorted(data,key=lambda x:float(x["priceChangePercent"]),reverse=True)[:10]

        texto="🚀 GANADORAS\n\n"

        for c in top:

            texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

        await query.edit_message_text(

        texto,

        reply_markup=menu()

        )

# SCANNER

    elif data=="scanner":

        url="https://api.binance.com/api/v3/ticker/24hr"

        data=requests.get(url).json()

        vol=sorted(data,key=lambda x:abs(float(x["priceChangePercent"])),reverse=True)[:10]

        texto="🔥 MAYOR VOLATILIDAD\n\n"

        for c in vol:

            texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

        await query.edit_message_text(

        texto,

        reply_markup=menu()

        )

# IA

    elif data=="ia":

        señal=ia_trading("BTC")

        await query.edit_message_text(

        f"🤖 IA BTC\n\n{señal}",

        reply_markup=menu()

        )

# GRAFICAS

    elif data=="graficas":

        await query.edit_message_text(

        "Selecciona cripto:",

        reply_markup=menu_graficas()

        )

# GENERAR GRAFICA

    elif "graf_" in data:

        symbol=data.split("_")[1]

        df=historial(symbol)

        df["close"].plot(title=symbol)

        plt.savefig("graf.png")

        plt.close()

        await context.bot.send_photo(

        chat_id=query.message.chat_id,

        photo=open("graf.png","rb")

        )

# PREMIUM

    elif data=="premium":

        await query.edit_message_text(

        "💎 PLAN PREMIUM\n\n"

        "Acceso a IA avanzada y scanner completo.\n"

        "Precio: $9/mes",

        reply_markup=menu()

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

            if actual>=p:

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

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))

    app.add_handler(CallbackQueryHandler(botones))

    job_queue = app.job_queue

    job_queue.run_repeating(revisar_alertas,interval=60)

    print("🚀 BOT CRYPTO PREMIUM ACTIVO")

    app.run_polling()

if __name__=="__main__":

    main()
