import os
import logging
import requests
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==============================
# CONFIG
# ==============================

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

if not TOKEN:
    raise ValueError("No se encontró BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

usuarios_suscritos = set()
ultimo_precio_btc = None

# ==============================
# FLASK SERVER (para Railway)
# ==============================

app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot funcionando 🚀"

def run_flask():
    app_flask.run(host="0.0.0.0", port=PORT)

# ==============================
# FUNCIONES CRIPTO
# ==============================

def obtener_precio():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    return response.json()["bitcoin"]["usd"]

# ==============================
# COMANDOS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bot Cripto con Alertas\n\n"
        "/btc\n"
        "/subscribe\n"
        "/unsubscribe"
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    precio = obtener_precio()
    await update.message.reply_text(f"₿ Bitcoin: ${precio}")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_suscritos.add(update.effective_chat.id)
    await update.message.reply_text("✅ Suscrito a alertas")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_suscritos.discard(update.effective_chat.id)
    await update.message.reply_text("❌ Desuscrito")

async def verificar_precio(context: ContextTypes.DEFAULT_TYPE):
    global ultimo_precio_btc

    precio_actual = obtener_precio()

    if ultimo_precio_btc is None:
        ultimo_precio_btc = precio_actual
        return

    variacion = ((precio_actual - ultimo_precio_btc) / ultimo_precio_btc) * 100

    if abs(variacion) >= 0.5:
        mensaje = f"🚨 BTC cambió {variacion:.2f}%\nPrecio: ${precio_actual}"
        for user_id in usuarios_suscritos:
            await context.bot.send_message(chat_id=user_id, text=mensaje)

        ultimo_precio_btc = precio_actual

# ==============================
# MAIN
# ==============================

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))

    app.job_queue.run_repeating(verificar_precio, interval=300, first=10)

    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_flask()
