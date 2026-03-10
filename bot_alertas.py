import os
import sqlite3
import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

# =====================
# DATABASE
# =====================

conn = sqlite3.connect("crypto.db",check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,plan TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS alertas(user_id INTEGER,cripto TEXT,precio REAL)")
conn.commit()

# =====================
# LISTA CRIPTOS
# =====================

TOP50 = [
"BTC","ETH","BNB","XRP","ADA","SOL","DOGE","DOT","MATIC","LTC",
"LINK","UNI","AVAX","TRX","SHIB","XLM","ETC","ATOM","FIL","AAVE",
"NEAR","APT","ARB","OP","INJ","SUI","PEPE","RNDR","SEI","IMX",
"GRT","SAND","MANA","FLOW","EGLD","XTZ","ALGO","KAVA","HBAR","ICP",
"QNT","FTM","RUNE","AXS","THETA","EOS","MKR","SNX","CRV","CHZ"
]

TOP10 = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC"]

# =====================
# PRECIO
# =====================

def precio(symbol):

    try:
        url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data=requests.get(url,timeout=10).json()
        return float(data["price"])
    except:
        return None

# =====================
# HISTORIAL
# =====================

def historial(symbol):

    url=f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=200"
    data=requests.get(url).json()

    df=pd.DataFrame(data)
    df=df[[4]]
    df.columns=["close"]
    df["close"]=df["close"].astype(float)

    return df

# =====================
# IA TENDENCIA
# =====================

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

# =====================
# TOP50
# =====================

def top50():

    texto="💰 TOP 50 CRIPTOS\n\n"

    for c in TOP50:
        p=precio(c)
        if p:
            texto+=f"{c} ${round(p,2)}\n"

    return texto[:4000]

# =====================
# GANADORAS
# =====================

def ganadoras():

    url="https://api.binance.com/api/v3/ticker/24hr"
    data=requests.get(url).json()

    top=sorted(data,key=lambda x:float(x["priceChangePercent"]),reverse=True)[:10]

    texto="🚀 GANADORAS\n\n"

    for c in top:
        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# =====================
# PERDEDORAS
# =====================

def perdedoras():

    url="https://api.binance.com/api/v3/ticker/24hr"
    data=requests.get(url).json()

    top=sorted(data,key=lambda x:float(x["priceChangePercent"]))[:10]

    texto="📉 PERDEDORAS\n\n"

    for c in top:
        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# =====================
# SCANNER
# =====================

def scanner():

    url="https://api.binance.com/api/v3/ticker/24hr"
    data=requests.get(url).json()

    top=sorted(data,key=lambda x:abs(float(x["priceChangePercent"])),reverse=True)[:10]

    texto="🔥 VOLATILIDAD\n\n"

    for c in top:
        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# =====================
# PUMP
# =====================

def pump():

    url="https://api.binance.com/api/v3/ticker/24hr"
    data=requests.get(url).json()

    pumps=[c for c in data if float(c["priceChangePercent"])>8]

    texto="🚀 POSIBLE PUMP\n\n"

    for c in pumps[:10]:
        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# =====================
# RANKING OPORTUNIDADES
# =====================

def oportunidades():

    url="https://api.binance.com/api/v3/ticker/24hr"
    data=requests.get(url).json()

    ranking=sorted(data,key=lambda x:float(x["priceChangePercent"]),reverse=True)[:15]

    texto="📊 OPORTUNIDADES\n\n"

    for c in ranking:
        texto+=f'{c["symbol"]} {c["priceChangePercent"]}%\n'

    return texto

# =====================
# GRAFICA
# =====================

def grafica(symbol):

    df=historial(symbol)

    df["close"].plot(title=symbol)

    plt.savefig("graf.png")

    plt.close()

# =====================
# MENU
# =====================

def menu():

    keyboard=[

    [InlineKeyboardButton("💰 BTC",callback_data="btc"),
     InlineKeyboardButton("💰 ETH",callback_data="eth")],

    [InlineKeyboardButton("📊 Top 10",callback_data="top10"),
     InlineKeyboardButton("💰 Top 50",callback_data="top50")],

    [InlineKeyboardButton("🚀 Ganadoras",callback_data="ganadoras"),
     InlineKeyboardButton("📉 Perdedoras",callback_data="perdedoras")],

    [InlineKeyboardButton("🔥 Scanner",callback_data="scanner"),
     InlineKeyboardButton("🚀 Pump",callback_data="pump")],

    [InlineKeyboardButton("📊 Oportunidades",callback_data="oportunidades"),
     InlineKeyboardButton("🤖 IA BTC",callback_data="ia")],

    [InlineKeyboardButton("📈 Gráfica BTC",callback_data="graf")]

    ]

    return InlineKeyboardMarkup(keyboard)

# =====================
# START
# =====================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.message.from_user.id

    cursor.execute("INSERT OR IGNORE INTO users VALUES(?,?)",(user,"free"))
    conn.commit()

    await update.message.reply_text(

        "🤖 BOT CRYPTO PRO\n\nSelecciona una opción:",

        reply_markup=menu()

    )

# =====================
# BOTONES
# =====================

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
            texto+=f"{c} ${precio(c)}\n"

        await query.edit_message_text(texto,reply_markup=menu())

    elif data=="top50":
        await query.edit_message_text(top50(),reply_markup=menu())

    elif data=="ganadoras":
        await query.edit_message_text(ganadoras(),reply_markup=menu())

    elif data=="perdedoras":
        await query.edit_message_text(perdedoras(),reply_markup=menu())

    elif data=="scanner":
        await query.edit_message_text(scanner(),reply_markup=menu())

    elif data=="pump":
        await query.edit_message_text(pump(),reply_markup=menu())

    elif data=="oportunidades":
        await query.edit_message_text(oportunidades(),reply_markup=menu())

    elif data=="ia":
        await query.edit_message_text(ia_trading("BTC"),reply_markup=menu())

    elif data=="graf":

        grafica("BTC")

        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=open("graf.png","rb")
        )

# =====================
# MAIN
# =====================

def main():

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(CallbackQueryHandler(botones))

    print("BOT CRYPTO PRO ACTIVO")

    app.run_polling(drop_pending_updates=True)

if __name__=="__main__":
    main()
