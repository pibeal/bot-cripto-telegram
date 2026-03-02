import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

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
# VARIABLES GLOBALES
# ==============================

usuarios_suscritos = set()
ultimo_precio_btc = None

# ==============================
# FUNCIONES
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
        "🚀 *Bot Cripto con Alertas*\n\n"
        "/btc - Precio actual BTC\n"
        "/subscribe - Activar alertas\n"
        "/unsubscribe - Desactivar alertas"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        precio = obtener_precio("bitcoin")
        await update.message.reply_text(f"₿ Bitcoin: ${precio}")
    except:
        await update.message.reply_text("❌ Error obteniendo precio")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    usuarios_suscritos.add(user_id)
    await update.message.reply_text("✅ Te has suscrito a alertas automáticas.")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    usuarios_suscritos.discard(user_id)
    await update.message.reply_text("❌ Te has desuscrito de las alertas.")

# ==============================
# ALERTA AUTOMÁTICA
# ==============================

async def verificar_precio(context: ContextTypes.DEFAULT_TYPE):
    global ultimo_precio_btc

    try:
        precio_actual = obtener_precio("bitcoin")

        if ultimo_precio_btc is None:
            ultimo_precio_btc = precio_actual
            return

        variacion = ((precio_actual - ultimo_precio_btc) / ultimo_precio_btc) * 100

        # Solo alerta si cambia más de 0.5%
        if abs(variacion) >= 0.5:
            mensaje = (
                f"🚨 Alerta BTC 🚨\n\n"
                f"Precio actual: ${precio_actual}\n"
                f"Variación: {variacion:.2f}%"
            )

            for user_id in usuarios_suscritos:
                await context.bot.send_message(chat_id=user_id, text=mensaje)

            ultimo_precio_btc = precio_actual

    except Exception as e:
        logger.error(f"Error en verificación automática: {e}")

# ==============================
# MAIN
# ==============================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Ejecutar cada 5 minutos (300 segundos)
    job_queue = app.job_queue
    job_queue.run_repeating(verificar_precio, interval=300, first=10)

    logger.info("Bot con alertas automáticas iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
