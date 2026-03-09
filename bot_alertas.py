import os
import sqlite3
import asyncio
import logging
import requests
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# CONFIGURACION
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
# LIMITADOR API
# =========================

async def pausa_api():
    await asyncio.sleep(1)

# =========================
# OBTENER PRECIO SEGURO
# =========================

async def obtener_precio(cripto):

    try:

        ticker = yf.Ticker(f"{cripto}-USD")
        data = ticker.history(period="1d")

        if data.empty:
            return None

        precio = data["Close"].iloc[-1]

        await pausa_api()

        return precio

    except Exception as e:

        logging.error(f"Error precio {cripto}: {e}")
        return None

# =========================
# COMANDO PRECIO
# =========================

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Uso: /precio BTC")
        return

    cripto = context.args[0].upper()

    precio_actual = await obtener_precio(cripto)

    if precio_actual is None:
        await update.message.reply_text("No se pudo obtener precio")
        return

    await update.message.reply_text(
        f"💰 {cripto} = ${precio_actual:.2f}"
    )

# =========================
# GRAFICA
# =========================

async def grafica(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text("Uso: /grafica BTC")
        return

    cripto = context.args[0].upper()

    ticker = yf.Ticker(f"{cripto}-USD")
    data = ticker.history(period="7d")

    plt.figure()

    data["Close"].plot(title=f"{cripto} últimos 7 días")

    file = f"{cripto}.png"

    plt.savefig(file)

    await update.message.reply_photo(photo=open(file,"rb"))

# =========================
# ALERTA
# =========================

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text("Uso: /alerta BTC 65000")
        return

    user = update.effective_user.id
    cripto = context.args[0].upper()
    precio = float(context.args[1])

    cursor.execute(
        "INSERT INTO alertas VALUES (?,?,?)",
        (user, cripto, precio)
    )

    conn.commit()

    await update.message.reply_text(
        f"🔔 Alerta creada {cripto} ${precio}"
    )

# =========================
# MIS ALERTAS
# =========================

async def misalertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id

    cursor.execute(
        "SELECT cripto,precio FROM alertas WHERE user_id=?",
        (user,)
    )

    datos = cursor.fetchall()

    if not datos:
        await update.message.reply_text("No tienes alertas")
        return

    texto = "📊 Tus alertas\n\n"

    for c,p in datos:
        texto += f"{c} → ${p}\n"

    await update.message.reply_text(texto)

# =========================
# BORRAR ALERTAS
# =========================

async def borraralertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id

    cursor.execute(
        "DELETE FROM alertas WHERE user_id=?",
        (user,)
    )

    conn.commit()

    await update.message.reply_text("🗑 Alertas eliminadas")

# =========================
# TOP CRYPTO
# =========================

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lista = ["BTC","ETH","BNB","SOL","XRP","ADA","DOGE","AVAX","DOT","MATIC"]

    texto = "📊 Top criptos\n\n"

    for c in lista:

        precio = await obtener_precio(c)

        if precio:
            texto += f"{c} → ${precio:.2f}\n"

    await update.message.reply_text(texto)

# =========================
# FEAR GREED
# =========================

async def fear(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        data = requests.get("https://api.alternative.me/fng/").json()

        valor = data["data"][0]["value"]
        estado = data["data"][0]["value_classification"]

        await update.message.reply_text(
            f"😱 Fear & Greed\n\n{valor} → {estado}"
        )

    except:
        await update.message.reply_text("Error API Fear")

# =========================
# ANALISIS TECNICO
# =========================

async def analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cripto = context.args[0].upper()

    ticker = yf.Ticker(f"{cripto}-USD")

    data = ticker.history(period="3mo")

    close = data["Close"]

    sma50 = close.rolling(50).mean()
    sma200 = close.rolling(200).mean()

    delta = close.diff()

    gain = (delta.where(delta > 0,0)).rolling(14).mean()
    loss = (-delta.where(delta < 0,0)).rolling(14).mean()

    rs = gain/loss

    rsi = 100-(100/(1+rs))

    rsi_actual = rsi.iloc[-1]

    texto = f"📊 Analisis {cripto}\n\nRSI {rsi_actual:.2f}\n"

    if rsi_actual>70:
        texto+="⚠️ Sobrecompra\n"

    if rsi_actual<30:
        texto+="🟢 Sobreventa\n"

    if sma50.iloc[-1] > sma200.iloc[-1]:
        texto+="✨ Golden Cross\n"
    else:
        texto+="☠️ Death Cross\n"

    await update.message.reply_text(texto)

# =========================
# SEÑAL
# =========================

async def señal(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cripto=context.args[0].upper()

    ticker=yf.Ticker(f"{cripto}-USD")

    data=ticker.history(period="3mo")

    close=data["Close"]

    sma50=close.rolling(50).mean()
    sma200=close.rolling(200).mean()

    delta=close.diff()

    gain=(delta.where(delta>0,0)).rolling(14).mean()
    loss=(-delta.where(delta<0,0)).rolling(14).mean()

    rs=gain/loss

    rsi=100-(100/(1+rs))

    rsi_actual=rsi.iloc[-1]

    signal="NEUTRAL"

    if sma50.iloc[-1]>sma200.iloc[-1] and rsi_actual<70:
        signal="📈 LONG"

    if sma50.iloc[-1]<sma200.iloc[-1] and rsi_actual>30:
        signal="📉 SHORT"

    await update.message.reply_text(
        f"📊 Señal {cripto}\nRSI {rsi_actual:.2f}\n{signal}"
    )

# =========================
# LOOP ALERTAS
# =========================

async def revisar_alertas(app):

    while True:

        try:

            cursor.execute("SELECT user_id,cripto,precio FROM alertas")

            datos = cursor.fetchall()

            for user,cripto,precio_alerta in datos:

                precio_actual=await obtener_precio(cripto)

                if precio_actual and precio_actual>=precio_alerta:

                    await app.bot.send_message(
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

    app=ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("precio",precio))
    app.add_handler(CommandHandler("grafica",grafica))
    app.add_handler(CommandHandler("alerta",alerta))
    app.add_handler(CommandHandler("misalertas",misalertas))
    app.add_handler(CommandHandler("borraralertas",borraralertas))
    app.add_handler(CommandHandler("top",top))
    app.add_handler(CommandHandler("fear",fear))
    app.add_handler(CommandHandler("analisis",analisis))
    app.add_handler(CommandHandler("señal",señal))

    asyncio.create_task(revisar_alertas(app))

    print("BOT NIVEL DIOS ABSOLUTO ACTIVO")

    await app.run_polling()

if __name__=="__main__":
    asyncio.run(main())
