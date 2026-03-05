import os
import sqlite3
import yfinance as yf
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("8718683908:AAFHR0BJ4mzRZw450TUciw_-jrxPb8VVMK4")

# =========================
# BASE DE DATOS
# =========================

conn = sqlite3.connect("alertas.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alertas(
user_id INTEGER,
crypto TEXT,
precio REAL
)
""")

conn.commit()

# =========================
# PRECIOS
# =========================

def obtener_precio(crypto):

    pares = {
        "btc": "BTC-USD",
        "eth": "ETH-USD",
        "sol": "SOL-USD"
    }

    ticker = pares.get(crypto.lower())

    if not ticker:
        return None

    data = yf.Ticker(ticker)
    precio = data.history(period="1d")["Close"].iloc[-1]

    return round(precio,2)

# =========================
# MENU
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("💰 Precio BTC", callback_data="btc")],
        [InlineKeyboardButton("💰 Precio ETH", callback_data="eth")],
        [InlineKeyboardButton("⚡ Precio SOL", callback_data="sol")],
        [InlineKeyboardButton("📊 Top Criptos", callback_data="top")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 Bot Cripto Ultra Pro\n\nSelecciona una opción:",
        reply_markup=reply_markup
    )

# =========================
# BOTONES
# =========================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    crypto = query.data

    if crypto in ["btc","eth","sol"]:

        precio = obtener_precio(crypto)

        await query.edit_message_text(
            f"💰 Precio de {crypto.upper()}:\n\n${precio}"
        )

    if crypto == "top":

        btc = obtener_precio("btc")
        eth = obtener_precio("eth")
        sol = obtener_precio("sol")

        mensaje = f"""
📊 TOP CRIPTOS

BTC: ${btc}
ETH: ${eth}
SOL: ${sol}
"""

        await query.edit_message_text(mensaje)

# =========================
# COMANDO PRECIO
# =========================

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text("Usa: /precio btc")
        return

    crypto = context.args[0]

    precio = obtener_precio(crypto)

    if precio is None:
        await update.message.reply_text("Cripto no soportada")
        return

    await update.message.reply_text(
        f"💰 Precio {crypto.upper()} = ${precio}"
    )

# =========================
# ALERTAS
# =========================

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /alerta btc 70000"
        )
        return

    crypto = context.args[0]
    precio = float(context.args[1])

    user = update.message.chat_id

    cursor.execute(
        "INSERT INTO alertas VALUES (?,?,?)",
        (user, crypto, precio)
    )

    conn.commit()

    await update.message.reply_text(
        f"🔔 Alerta creada para {crypto.upper()} en ${precio}"
    )

# =========================
# VER ALERTAS
# =========================

async def mis_alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.chat_id

    cursor.execute(
        "SELECT crypto,precio FROM alertas WHERE user_id=?",
        (user,)
    )

    datos = cursor.fetchall()

    if not datos:
        await update.message.reply_text("No tienes alertas")
        return

    mensaje = "🔔 Tus alertas:\n\n"

    for c,p in datos:
        mensaje += f"{c.upper()} → ${p}\n"

    await update.message.reply_text(mensaje)

# =========================
# GRAFICA
# =========================

async def grafica(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args)==0:
        await update.message.reply_text("Usa: /grafica btc")
        return

    crypto=context.args[0]

    pares={
        "btc":"BTC-USD",
        "eth":"ETH-USD",
        "sol":"SOL-USD"
    }

    ticker=pares.get(crypto)

    data=yf.download(ticker,period="7d")

    plt.figure()
    plt.plot(data["Close"])

    archivo="grafica.png"

    plt.savefig(archivo)

    await update.message.reply_photo(photo=open(archivo,"rb"))

# =========================
# HELP
# =========================

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje="""
📖 COMANDOS

/start → menú
/precio btc
/alerta btc 70000
/misalertas
/grafica btc
"""

    await update.message.reply_text(mensaje)

# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("misalertas", mis_alertas))
    app.add_handler(CommandHandler("grafica", grafica))
    app.add_handler(CommandHandler("help", help))

    app.add_handler(CallbackQueryHandler(botones))

    print("BOT ULTRA PRO INICIADO")

    app.run_polling()

if __name__ == "__main__":
    main()
