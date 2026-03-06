import os
import json
import requests
import yfinance as yf
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

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
