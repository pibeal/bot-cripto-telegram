import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

def obtener_precio():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url, timeout=10)
    return response.json()["bitcoin"]["usd"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Bot funcionando")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    precio = obtener_precio()
    await update.message.reply_text(f"₿ BTC: ${precio}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))

    print("Bot iniciado correctamente")
    app.run_polling()

if __name__ == "__main__":
    main()
