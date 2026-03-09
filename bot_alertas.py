import os
import sqlite3
import asyncio
import logging
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from threading import Thread
from web import app as web_app


# =========================
# WEB SERVER (KEEP ALIVE)
# =========================

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()


# =========================
# CONFIG
# =========================

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# =========================
# BASE DE DATOS
# =========================

conn = sqlite3.connect("alertas.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alertas(
user_id INTEGER,
cripto TEXT,
precio REAL
)
""")

conn.commit()


# =========================
# API BINANCE
# =========================

def precio_binance(symbol):

    url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"

    r=requests.get(url).json()

    return float(r["price"])


# =========================
# HISTORIAL BINANCE
# =========================

def historial_binance(symbol):

    url=f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=200"

    data=requests.get(url).json()

    df=pd.DataFrame(data)

    df=df[[4]]

    df.columns=["close"]

    df["close"]=df["close"].astype(float)

    return df


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 BOT CRYPTO ACTIVO\n\n"
        "Comandos:\n"
        "/precio BTC\n"
        "/top\n"
        "/alerta BTC 50000\n"
        "/misalertas\n"
        "/borraralertas\n"
        "/analisis BTC\n"
        "/senal BTC\n"
        "/test"
    )


# =========================
# TEST
# =========================

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✅ BOT ACTUALIZADO CORRECTAMENTE"
    )


# =========================
# PRECIO
# =========================

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text("Uso: /precio BTC")

        return

    cripto=context.args[0].upper()

    try:

        price=precio_binance(cripto)

        await update.message.reply_text(
            f"💰 {cripto} = ${price:.2f}"
        )

    except:

        await update.message.reply_text("Error obteniendo precio")


# =========================
# TOP CRIPTOS
# =========================

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lista=["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC"]

    texto="📊 TOP CRIPTOS\n\n"

    for c in lista:

        try:

            p=precio_binance(c)

            texto+=f"{c} → ${p:.2f}\n"

        except:

            pass

    await update.message.reply_text(texto)


# =========================
# ALERTA
# =========================

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args)<2:

        await update.message.reply_text("Uso: /alerta BTC 50000")

        return

    user=update.effective_user.id

    cripto=context.args[0].upper()

    precio=float(context.args[1])

    cursor.execute(
        "INSERT INTO alertas VALUES(?,?,?)",
        (user,cripto,precio)
    )

    conn.commit()

    await update.message.reply_text(
        f"🔔 Alerta creada {cripto} ${precio}"
    )


# =========================
# MIS ALERTAS
# =========================

async def misalertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user=update.effective_user.id

    cursor.execute(
        "SELECT cripto,precio FROM alertas WHERE user_id=?",
        (user,)
    )

    datos=cursor.fetchall()

    if not datos:

        await update.message.reply_text("No tienes alertas")

        return

    texto="📊 Tus alertas\n\n"

    for c,p in datos:

        texto+=f"{c} → ${p}\n"

    await update.message.reply_text(texto)


# =========================
# BORRAR ALERTAS
# =========================

async def borraralertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user=update.effective_user.id

    cursor.execute(
        "DELETE FROM alertas WHERE user_id=?",
        (user,)
    )

    conn.commit()

    await update.message.reply_text("Alertas borradas")


# =========================
# ANALISIS RSI
# =========================

async def analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text("Uso: /analisis BTC")

        return

    cripto=context.args[0].upper()

    df=historial_binance(cripto)

    close=df["close"]

    delta=close.diff()

    gain=(delta.where(delta>0,0)).rolling(14).mean()

    loss=(-delta.where(delta<0,0)).rolling(14).mean()

    rs=gain/loss

    rsi=100-(100/(1+rs))

    rsi_actual=rsi.iloc[-1]

    msg=f"📊 RSI {cripto}\n\n{rsi_actual:.2f}\n"

    if rsi_actual>70:
        msg+="⚠️ SOBRECOMPRA"

    elif rsi_actual<30:
        msg+="🟢 SOBREVENTA"

    await update.message.reply_text(msg)


# =========================
# SEÑAL
# =========================

async def senal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text("Uso: /senal BTC")

        return

    cripto=context.args[0].upper()

    df=historial_binance(cripto)

    close=df["close"]

    sma50=close.rolling(50).mean()

    sma200=close.rolling(200).mean()

    signal="NEUTRAL"

    if sma50.iloc[-1]>sma200.iloc[-1]:
        signal="📈 LONG"

    elif sma50.iloc[-1]<sma200.iloc[-1]:
        signal="📉 SHORT"

    await update.message.reply_text(
        f"📊 Señal {cripto}\n\n{signal}"
    )


# =========================
# LOOP ALERTAS
# =========================

async def revisar_alertas(application):

    while True:

        try:

            cursor.execute(
                "SELECT user_id,cripto,precio FROM alertas"
            )

            datos=cursor.fetchall()

            for user,cripto,precio_alerta in datos:

                precio_actual=precio_binance(cripto)

                if precio_actual>=precio_alerta:

                    await application.bot.send_message(
                        chat_id=user,
                        text=f"🚨 {cripto} llegó a ${precio_actual:.2f}"
                    )

            await asyncio.sleep(60)

        except Exception as e:

            logging.error(e)

            await asyncio.sleep(120)


# =========================
# MAIN
# =========================

async def main():

    application=ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start",start))
    application.add_handler(CommandHandler("test",test))
    application.add_handler(CommandHandler("precio",precio))
    application.add_handler(CommandHandler("top",top))
    application.add_handler(CommandHandler("alerta",alerta))
    application.add_handler(CommandHandler("misalertas",misalertas))
    application.add_handler(CommandHandler("borraralertas",borraralertas))
    application.add_handler(CommandHandler("analisis",analisis))
    application.add_handler(CommandHandler("senal",senal))

    asyncio.create_task(revisar_alertas(application))

    print("BOT CRYPTO BINANCE ACTIVO")

    await application.run_polling()


# =========================
# RUN
# =========================

if __name__ == "__main__":

    asyncio.run(main())
