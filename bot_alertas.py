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
