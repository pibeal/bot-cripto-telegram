import os
import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

usuarios_suscritos = set()
ultimo_precio_btc = None

def obtener_precio():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url, timeout=10)
    return response.json()["bitcoin"]["usd"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Bot activo\n\n/btc\n/subscribe")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    precio = obtener_precio()
    await update.message.reply_text(f"₿ BTC: ${precio}")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_suscritos.add(update.effective_chat.id)
    await update.message.reply_text("✅ Suscrito a alertas")

async def alerta_loop(app):
    global ultimo_precio_btc

    while True:
        try:
            precio_actual = obtener_precio()

            if ultimo_precio_btc is None:
                ultimo_precio_btc = precio_actual
            else:
                variacion = ((precio_actual - ultimo_precio_btc) / ultimo_precio_btc) * 100

                if abs(variacion) >= 0.5:
                    mensaje = f"🚨 BTC cambió {variacion:.2f}%\nPrecio: ${precio_actual}"

                    for user_id in usuarios_suscritos:
                        await app.bot.send_message(chat_id=user_id, text=mensaje)

                    ultimo_precio_btc = precio_actual

        except Exception as e:
            logger.error(e)

        await asyncio.sleep(300)  # 5 minutos

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("subscribe", subscribe))

    print("Bot con alertas iniciado")

    asyncio.create_task(alerta_loop(app))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
