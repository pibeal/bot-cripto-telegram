 import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==============================
# CONFIGURACIÓN
# ==============================

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("No se encontró el BOT_TOKEN en las variables de entorno")

# Logging para Railway
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ==============================
# COMANDOS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot de Alertas Cripto activo!\n\n"
        "Usa /price para ver el precio actual de BTC."
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()

        btc_price = data["bitcoin"]["usd"]

        await update.message.reply_text(
            f"💰 Precio actual de BTC: ${btc_price}"
        )

    except Exception as e:
        logger.error(f"Error obteniendo precio: {e}")
        await update.message.reply_text("❌ Error obteniendo el precio.")

# ==============================
# MAIN
# ==============================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    logger.info("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == "__main__":
    main() 
