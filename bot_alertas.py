<<<<<<< HEAD
import os
import json
import requests
import yfinance as yf
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8771204299:AAF-H6RWaRqsR7Yr9lyHrfmPk6-YHS14F0U")

if not TOKEN:
    raise ValueError("TOKEN no configurado")

# ===============================
# ARCHIVOS
# ===============================

ALERT_FILE = "alertas.json"

if not os.path.exists(ALERT_FILE):
    with open(ALERT_FILE, "w") as f:
        json.dump([], f)

# ===============================
# TOP 20 CRYPTOS
# ===============================

cryptos = {
    "btc": "BTC-USD",
    "eth": "ETH-USD",
    "bnb": "BNB-USD",
    "xrp": "XRP-USD",
    "ada": "ADA-USD",
    "sol": "SOL-USD",
    "doge": "DOGE-USD",
    "dot": "DOT-USD",
    "matic": "MATIC-USD",
    "ltc": "LTC-USD",
    "trx": "TRX-USD",
    "avax": "AVAX-USD",
    "link": "LINK-USD",
    "atom": "ATOM-USD",
    "uni": "UNI-USD",
    "xlm": "XLM-USD",
    "etc": "ETC-USD",
    "hbar": "HBAR-USD",
    "fil": "FIL-USD",
    "apt": "APT-USD"
}

# ===============================
# PRECIO CRYPTO
# ===============================

def get_price(symbol):
    data = yf.Ticker(symbol)
    hist = data.history(period="1d")
    return float(hist["Close"].iloc[-1])

# ===============================
# START
# ===============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("📊 Mercado", callback_data="market")],
        [InlineKeyboardButton("📈 Ganadores", callback_data="top")],
        [InlineKeyboardButton("📉 Perdedores", callback_data="losers")],
        [InlineKeyboardButton("📊 Grafica BTC", callback_data="grafica")],
        [InlineKeyboardButton("💎 Premium", callback_data="premium")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 BOT CRIPTO PRO\n\nSelecciona una opción:",
        reply_markup=reply_markup
    )

# ===============================
# TOP 20
# ===============================

async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "📊 TOP 20 CRYPTO\n\n"

    for name, symbol in cryptos.items():

        try:
            price = get_price(symbol)
            text += f"{name.upper()} : ${price:.2f}\n"
        except:
            pass

    await update.message.reply_text(text)

# ===============================
# GANADORES
# ===============================

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = yf.download(list(cryptos.values()), period="2d")

    cambios = []

    for i, symbol in enumerate(cryptos.values()):

        try:
            close = data["Close"][symbol]
            change = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
            cambios.append((symbol, change))
        except:
            pass

    cambios.sort(key=lambda x: x[1], reverse=True)

    text = "📈 TOP GANADORES\n\n"

    for c in cambios[:5]:
        text += f"{c[0]} : {c[1]:.2f}%\n"

    await update.message.reply_text(text)

# ===============================
# PERDEDORES
# ===============================

async def losers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = yf.download(list(cryptos.values()), period="2d")

    cambios = []

    for i, symbol in enumerate(cryptos.values()):

        try:
            close = data["Close"][symbol]
            change = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
            cambios.append((symbol, change))
        except:
            pass

    cambios.sort(key=lambda x: x[1])

    text = "📉 TOP PERDEDORES\n\n"

    for c in cambios[:5]:
        text += f"{c[0]} : {c[1]:.2f}%\n"

    await update.message.reply_text(text)

# ===============================
# ALERTA
# ===============================

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        coin = context.args[0].lower()
        porcentaje = float(context.args[1])

        with open(ALERT_FILE) as f:
            alertas = json.load(f)

        alertas.append({
            "chat": update.effective_chat.id,
            "coin": coin,
            "porcentaje": porcentaje,
            "precio": get_price(cryptos[coin])
        })

        with open(ALERT_FILE, "w") as f:
            json.dump(alertas, f)

        await update.message.reply_text("🚨 Alerta creada")

    except:

        await update.message.reply_text("Uso: /alerta btc 3")

# ===============================
# VERIFICAR ALERTAS
# ===============================

async def verificar_alertas(context):

    with open(ALERT_FILE) as f:
        alertas = json.load(f)

    nuevas = []

    for alerta in alertas:

        try:

            coin = alerta["coin"]
            precio_actual = get_price(cryptos[coin])

            cambio = ((precio_actual - alerta["precio"]) / alerta["precio"]) * 100

            if abs(cambio) >= alerta["porcentaje"]:

                await context.bot.send_message(
                    alerta["chat"],
                    f"🚨 ALERTA {coin.upper()}\nCambio: {cambio:.2f}%"
                )

            else:

                nuevas.append(alerta)

        except:
            pass

    with open(ALERT_FILE, "w") as f:
        json.dump(nuevas, f)

# ===============================
# GRAFICA
# ===============================

async def grafica(update: Update, context: ContextTypes.DEFAULT_TYPE):

    data = yf.Ticker("BTC-USD")
    hist = data.history(period="7d")

    plt.figure()
    hist["Close"].plot()
    plt.title("BTC 7D")
    plt.savefig("grafica.png")
    plt.close()

    await update.message.reply_photo(photo=open("grafica.png", "rb"))

# ===============================
# PREMIUM
# ===============================

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

        "💎 CRYPTO PRO PREMIUM\n\n"
        "✔ Señales exclusivas\n"
        "✔ Alertas adelantadas\n"
        "✔ Estrategias de trading\n\n"
        "Precio: $5 USD / mes\n"
        "Contacto: @tuusuario"

    )

# ===============================
# MAIN
# ===============================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("market", market))
    app.add_handler(CommandHandler("top", top))
    app.add_handler(CommandHandler("perdedores", losers))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("grafica", grafica))
    app.add_handler(CommandHandler("premium", premium))

    app.job_queue.run_repeating(verificar_alertas, interval=60, first=10)

    print("BOT ONLINE 🚀")

    app.run_polling()

if __name__ == "__main__":
    main()
=======
import logging
import requests
import time
import json
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ==============================
# CONFIG
# ==============================

TOKEN = "8771204299:AAF-H6RWaRqsR7Yr9lyHrfmPk6-YHS14F0U"
ARCHIVO_ALERTAS = "alertas.json"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ==============================
# VARIABLES GLOBALES
# ==============================

cache_top20 = []
ultimo_update = 0
CACHE_TIEMPO = 60

alertas_usuarios = {}
precios_referencia = {}

# ==============================
# PERSISTENCIA
# ==============================

def guardar_alertas():
    with open(ARCHIVO_ALERTAS, "w") as f:
        json.dump(alertas_usuarios, f)


def cargar_alertas():
    global alertas_usuarios
    if os.path.exists(ARCHIVO_ALERTAS):
        with open(ARCHIVO_ALERTAS, "r") as f:
            alertas_usuarios = json.load(f)
            alertas_usuarios = {int(k): v for k, v in alertas_usuarios.items()}

# ==============================
# CACHE COINGECKO
# ==============================

def actualizar_cache():
    global cache_top20, ultimo_update

    ahora = time.time()

    if ahora - ultimo_update < CACHE_TIEMPO and cache_top20:
        return

    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 20,
            "page": 1,
            "price_change_percentage": "24h"
        }

        response = requests.get(url, params=params, timeout=10)
        cache_top20 = response.json()
        ultimo_update = ahora
        logger.info("Cache actualizado")

    except Exception as e:
        logger.error(f"Error cache: {e}")

# ==============================
# VERIFICAR ALERTAS
# ==============================

async def verificar_alertas(context: ContextTypes.DEFAULT_TYPE):
    actualizar_cache()

    for user_id, coins in alertas_usuarios.items():
        for coin_id, porcentaje_objetivo in coins.items():
            coin = next((c for c in cache_top20 if c["id"] == coin_id), None)

            if not coin:
                continue

            precio_actual = coin["current_price"]

            if user_id not in precios_referencia:
                precios_referencia[user_id] = {}

            if coin_id not in precios_referencia[user_id]:
                precios_referencia[user_id][coin_id] = precio_actual
                continue

            precio_base = precios_referencia[user_id][coin_id]
            variacion = ((precio_actual - precio_base) / precio_base) * 100

            if abs(variacion) >= porcentaje_objetivo:
                mensaje = (
                    f"🚨 ALERTA {coin['name']}\n\n"
                    f"Variación: {variacion:.2f}%\n"
                    f"Precio actual: ${precio_actual}"
                )

                await context.bot.send_message(chat_id=user_id, text=mensaje)

                precios_referencia[user_id][coin_id] = precio_actual

# ==============================
# COMANDOS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "📊 Bot Cripto PRO\n\n"
        "/top20\n"
        "/alerta bitcoin 3\n"
        "/misalertas\n"
        "/eliminar bitcoin\n"
        "/borraralertas\n"
    )
    await update.message.reply_text(mensaje)


async def top20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    actualizar_cache()

    mensaje = "🏆 TOP 20\n\n"

    for i, coin in enumerate(cache_top20, start=1):
        mensaje += (
            f"{i}. {coin['name']} ({coin['symbol'].upper()})\n"
            f"${coin['current_price']} | "
            f"{coin['price_change_percentage_24h']:.2f}%\n\n"
        )

    await update.message.reply_text(mensaje)


async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Uso: /alerta bitcoin 3")
        return

    coin_id = context.args[0].lower()

    try:
        porcentaje = float(context.args[1])
    except ValueError:
        await update.message.reply_text("El porcentaje debe ser número.")
        return

    user_id = update.effective_chat.id
    actualizar_cache()

    coin = next((c for c in cache_top20 if c["id"] == coin_id), None)

    if not coin:
        await update.message.reply_text("Cripto no está en el Top 20.")
        return

    if user_id not in alertas_usuarios:
        alertas_usuarios[user_id] = {}

    alertas_usuarios[user_id][coin_id] = porcentaje

    guardar_alertas()

    await update.message.reply_text(
        f"✅ Alerta activada para {coin['name']} al {porcentaje}%"
    )


async def misalertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in alertas_usuarios:
        await update.message.reply_text("No tienes alertas activas.")
        return

    mensaje = "🔔 Tus alertas:\n\n"

    for coin, porc in alertas_usuarios[user_id].items():
        mensaje += f"{coin} → {porc}%\n"

    await update.message.reply_text(mensaje)


async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Uso: /eliminar bitcoin")
        return

    coin_id = context.args[0].lower()
    user_id = update.effective_chat.id

    if user_id not in alertas_usuarios:
        await update.message.reply_text("No tienes alertas activas.")
        return

    if coin_id not in alertas_usuarios[user_id]:
        await update.message.reply_text("No tienes alerta para esa cripto.")
        return

    del alertas_usuarios[user_id][coin_id]

    if user_id in precios_referencia:
        precios_referencia[user_id].pop(coin_id, None)

    if not alertas_usuarios[user_id]:
        del alertas_usuarios[user_id]

    guardar_alertas()

    await update.message.reply_text(f"🗑 Alerta eliminada para {coin_id}")


async def borraralertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id not in alertas_usuarios:
        await update.message.reply_text("No tienes alertas activas.")
        return

    del alertas_usuarios[user_id]
    precios_referencia.pop(user_id, None)

    guardar_alertas()

    await update.message.reply_text("🗑 Todas tus alertas fueron eliminadas.")


# ==============================
# MAIN
# ==============================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    cargar_alertas()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top20", top20))
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("misalertas", misalertas))
    app.add_handler(CommandHandler("eliminar", eliminar))
    app.add_handler(CommandHandler("borraralertas", borraralertas))

    app.job_queue.run_repeating(verificar_alertas, interval=60, first=10)

    logger.info("Bot Trader PRO completo activo...")
    app.run_polling()


if __name__ == "__main__":
    main()
>>>>>>> 7daac31d359cde7bf59a7c9d58e9181704b2526a
