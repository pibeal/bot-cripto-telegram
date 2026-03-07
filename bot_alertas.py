import os
import sqlite3
import asyncio
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
CallbackQueryHandler,
MessageHandler,
filters,
ContextTypes
)

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
# LISTA GRANDE DE CRIPTOS
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
"DOT":"DOT-USD",
"LTC":"LTC-USD",
"TRX":"TRX-USD",
"ATOM":"ATOM-USD",
"ETC":"ETC-USD",
"FIL":"FIL-USD",
"APT":"APT-USD",
"ARB":"ARB-USD",
"OP":"OP-USD",
"NEAR":"NEAR-USD",
"ICP":"ICP-USD",
"INJ":"INJ-USD",
"RNDR":"RNDR-USD",
"SUI":"SUI20947-USD",
"SEI":"SEI-USD"
}

# =========================
# MENU PRINCIPAL
# =========================

def menu():

    keyboard = [

    [InlineKeyboardButton("💰 Precio",callback_data="precio")],
    [InlineKeyboardButton("📊 Graficas",callback_data="grafica")],
    [InlineKeyboardButton("📉 Indicadores",callback_data="indicador")],
    [InlineKeyboardButton("🤖 Analisis IA",callback_data="analisis")],
    [InlineKeyboardButton("🚨 Crear alerta",callback_data="alerta")],
    [InlineKeyboardButton("🏆 Top mercado",callback_data="top")]

    ]

    return InlineKeyboardMarkup(keyboard)

# =========================
# START
# =========================

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

    "🏦 BOT CRYPTO EMPRESARIAL\n\n"
    "Sistema profesional de análisis crypto",

    reply_markup=menu()

    )

# =========================
# MENU CRIPTOS
# =========================

async def menu_criptos(query,tipo):

    keyboard=[]

    for c in cryptos:

        keyboard.append([InlineKeyboardButton(c,callback_data=f"{tipo}_{c}")])

    await query.message.reply_text(

    "Selecciona una criptomoneda",

    reply_markup=InlineKeyboardMarkup(keyboard)

    )

# =========================
# PRECIO
# =========================

async def precio(query,crypto):

    ticker=cryptos[crypto]

    data=yf.Ticker(ticker).history(period="1d")

    precio=data["Close"].iloc[-1]

    await query.message.reply_text(

    f"💰 {crypto}\n\nPrecio actual: ${precio:,.2f}"

    )

# =========================
# GRAFICA
# =========================

async def grafica(query,crypto):

    ticker=cryptos[crypto]

    data=yf.Ticker(ticker).history(period="1mo")

    plt.figure(figsize=(10,5))

    data["Close"].plot()

    plt.title(f"{crypto} precio")

    archivo=f"{crypto}.png"

    plt.savefig(archivo)

    plt.close()

    await query.message.reply_photo(photo=open(archivo,"rb"))

# =========================
# INDICADORES
# =========================

async def indicadores(query,crypto):

    ticker=cryptos[crypto]

    data=yf.Ticker(ticker).history(period="6mo")

    data["EMA20"]=data["Close"].ewm(span=20).mean()
    data["EMA50"]=data["Close"].ewm(span=50).mean()

    delta=data["Close"].diff()

    gain=(delta.where(delta>0,0)).rolling(14).mean()
    loss=(-delta.where(delta<0,0)).rolling(14).mean()

    rs=gain/loss

    data["RSI"]=100-(100/(1+rs))

    rsi=data["RSI"].iloc[-1]

    señal="NEUTRAL"

    if rsi>70:
        señal="SOBRECOMPRA 🔴"
    elif rsi<30:
        señal="SOBREVENTA 🟢"

    await query.message.reply_text(

    f"📉 Indicadores {crypto}\n\n"
    f"RSI: {rsi:.2f}\n"
    f"Señal: {señal}"

    )

# =========================
# ANALISIS AUTOMATICO
# =========================

async def analisis(query,crypto):

    ticker=cryptos[crypto]

    data=yf.Ticker(ticker).history(period="6mo")

    ema20=data["Close"].ewm(span=20).mean().iloc[-1]
    ema50=data["Close"].ewm(span=50).mean().iloc[-1]

    precio=data["Close"].iloc[-1]

    tendencia="BAJISTA"

    if ema20>ema50:
        tendencia="ALCISTA"

    await query.message.reply_text(

    f"🤖 Analisis {crypto}\n\n"
    f"Precio: {precio:.2f}\n"
    f"Tendencia: {tendencia}"

    )

# =========================
# ALERTAS
# =========================

async def alerta(update,context):

    await update.message.reply_text(

    "Formato:\n\nBTC 50000"

    )

    context.user_data["alerta"]=True

async def recibir(update,context):

    if context.user_data.get("alerta"):

        try:

            crypto,precio=update.message.text.upper().split()

            precio=float(precio)

        except:

            await update.message.reply_text("Formato incorrecto")

            return

        cursor.execute(

        "INSERT INTO alertas VALUES (?,?,?)",

        (update.message.chat_id,crypto,precio)

        )

        conn.commit()

        context.user_data["alerta"]=False

        await update.message.reply_text(

        f"🚨 Alerta creada {crypto} {precio}"

        )

# =========================
# ALERTAS AUTOMATICAS
# =========================

async def verificar_alertas(app):

    while True:

        cursor.execute("SELECT * FROM alertas")

        filas=cursor.fetchall()

        for chat_id,crypto,precio_alerta in filas:

            ticker=cryptos.get(crypto)

            if not ticker:
                continue

            precio=yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]

            if precio>=precio_alerta:

                await app.bot.send_message(

                chat_id=chat_id,

                text=f"🚨 ALERTA {crypto}\nPrecio: {precio}"

                )

        await asyncio.sleep(60)

# =========================
# TOP MERCADO
# =========================

async def top(query):

    cambios=[]

    for c,t in cryptos.items():

        data=yf.Ticker(t).history(period="2d")

        if len(data)<2:
            continue

        hoy=data["Close"].iloc[-1]
        ayer=data["Close"].iloc[-2]

        cambio=((hoy-ayer)/ayer)*100

        cambios.append((c,cambio))

    cambios.sort(key=lambda x:x[1],reverse=True)

    texto="🏆 TOP CRIPTOS\n\n"

    for c,p in cambios[:10]:

        texto+=f"{c} {p:.2f}%\n"

    await query.message.reply_text(texto)

# =========================
# BOTONES
# =========================

async def botones(update,context):

    query=update.callback_query

    await query.answer()

    data=query.data

    if data=="precio":
        await menu_criptos(query,"precio")

    elif data=="grafica":
        await menu_criptos(query,"grafica")

    elif data=="indicador":
        await menu_criptos(query,"indicador")

    elif data=="analisis":
        await menu_criptos(query,"analisis")

    elif data=="alerta":
        await query.message.reply_text("Usa /alerta")

    elif data=="top":
        await top(query)

    elif data.startswith("precio_"):

        crypto=data.split("_")[1]
        await precio(query,crypto)

    elif data.startswith("grafica_"):

        crypto=data.split("_")[1]
        await grafica(query,crypto)

    elif data.startswith("indicador_"):

        crypto=data.split("_")[1]
        await indicadores(query,crypto)

    elif data.startswith("analisis_"):

        crypto=data.split("_")[1]
        await analisis(query,crypto)

# =========================
# MAIN
# =========================

async def main():

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",start))

    app.add_handler(CommandHandler("alerta",alerta))

    app.add_handler(CallbackQueryHandler(botones))

    app.add_handler(MessageHandler(filters.TEXT,recibir))

    asyncio.create_task(verificar_alertas(app))

    print("BOT EMPRESARIAL CORRIENDO")

    await app.run_polling()

if __name__=="__main__":

    asyncio.run(main())
