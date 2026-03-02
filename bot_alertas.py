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
    raise ValueError("No se encontró BOT_TOKEN en las variables de entorno")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# ==============================
# FUNCION PARA OBTENER PRECIO
# ==============================

def obtener_precio(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[coin_id]["usd"]

# ==============================
# COMANDOS
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "🚀 *Bot de Alertas Cripto Activo*\n\n"
        "Consulta precios en tiempo real:\n"
        "/btc - Precio de Bitcoin\n"
        "/eth - Precio de Ethereum\n"
        "/sol - Precio de Solana\n"
        "/help - Ver comandos"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "📌 *Comandos disponibles:*\n\n"
        "/btc → Precio actual de Bitcoin\n"
        "/eth → Precio actual de Ethereum\n"
        "/sol → Precio actual de Solana"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        precio = obtener_precio("bitcoin")
        await update.message.reply_text(f"₿ *Bitcoin*: ${precio}", parse_mode="Markdown")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("❌ Error obteniendo precio de BTC")

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        precio = obtener_precio("ethereum")
        await update.message.reply_text(f"Ξ *Ethereum*: ${precio}", parse_mode="Markdown")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("❌ Error obteniendo precio de ETH")

async def sol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        precio = obtener_precio("solana")
        await update.message.reply_text(f"◎ *Solana*: ${precio}", parse_mode="Markdown")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("❌ Error obteniendo precio de SOL")

# ==============================
# MAIN
# ==============================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("eth", eth))
    app.add_handler(CommandHandler("sol", sol))

    logger.info("Bot iniciado correctamente...")
    app.run_polling()

if __name__ == "__main__":
    main()
