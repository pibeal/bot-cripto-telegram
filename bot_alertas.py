import os
import json
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes
)
import asyncio

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

# 📂 CARGAR DATA
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 📂 USUARIOS
def cargar_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return []

def guardar_user(user_id):
    users = cargar_users()
    if user_id not in users:
        users.append(user_id)
        with open("users.json", "w") as f:
            json.dump(users, f)

# ⚠️ AVISO
async def aviso(update):
    await update.message.reply_text(
        "⚠️ Esto no es asesoría financiera. Toda inversión tiene riesgo."
    )

# 💰 PRECIO CRIPTO
def precio(coin="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        return requests.get(url).json()[coin]["usd"]
    except:
        return None

# 🔔 ALERTAS AUTOMÁTICAS
async def enviar_alertas(app):
    ultimo_precio = 0

    while True:
        btc = precio("bitcoin")

        if btc and btc < 50000 and btc != ultimo_precio:
            users = cargar_users()

            for u in users:
                try:
                    await app.bot.send_message(
                        chat_id=u,
                        text=f"🚨 ALERTA BTC\nBitcoin bajó a ${btc}"
                    )
                except:
                    pass

            ultimo_precio = btc

        await asyncio.sleep(300)  # cada 5 min

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    guardar_user(user_id)

    texto = (
        "💸 *FINANCE BOT PRO*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "Plataforma para encontrar, comparar y monitorear inversiones.\n\n"
        "👇 Elige una opción:"
    )

    keyboard = [
        [
            InlineKeyboardButton("💰 Ahorro", callback_data="ahorro"),
            InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")
        ],
        [
            InlineKeyboardButton("🪙 Cripto", callback_data="cripto"),
            InlineKeyboardButton("🏆 Ranking", callback_data="ranking")
        ],
        [
            InlineKeyboardButton("🆚 Comparar", callback_data="comparar")
        ]
    ]

    await update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

    await aviso(update)

# 📊 MOSTRAR OPCIONES
async def mostrar(update, tipo):
    resultados = [x for x in data if x["tipo"] == tipo]

    mensaje = f"*{tipo.upper()}*\n━━━━━━━━━━━━━━━\n\n"
    botones = []

    for r in resultados:
        mensaje += (
            f"🏦 *{r['nombre']}*\n"
            f"• Rendimiento: {r.get('rendimiento','N/A')}\n"
            f"• Liquidez: {r.get('liquidez','N/A')}\n"
            f"• Riesgo: {r['riesgo']}\n"
            f"• {r.get('descripcion','')}\n\n"
        )

        botones.append([
            InlineKeyboardButton(f"Abrir {r['nombre']}", url=r["link"])
        ])

    await update.message.reply_text(
        mensaje,
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode=ParseMode.MARKDOWN
    )

# 🏆 RANKING
async def ranking(update):
    orden = sorted(data, key=lambda x: x["riesgo"])

    mensaje = "*🏆 TOP OPCIONES*\n━━━━━━━━━━━━━━━\n\n"

    for i, r in enumerate(orden[:5], 1):
        mensaje += f"{i}. {r['nombre']} ({r['tipo']})\n"

    await update.message.reply_text(mensaje, parse_mode=ParseMode.MARKDOWN)

# 🆚 COMPARAR
async def comparar(update):
    a, b = data[0], data[1]

    mensaje = (
        "*🆚 COMPARACIÓN*\n━━━━━━━━━━━━━━━\n\n"
        f"{a['nombre']} vs {b['nombre']}\n\n"
        f"Rendimiento:\n{a.get('rendimiento')} vs {b.get('rendimiento')}\n"
    )

    await update.message.reply_text(mensaje, parse_mode=ParseMode.MARKDOWN)

# 🎯 BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data

    if tipo == "cripto":
        btc = precio("bitcoin")
        await query.message.reply_text(f"💰 BTC: ${btc}")

    if tipo in ["ahorro", "bolsa", "cripto"]:
        await mostrar(query, tipo)

    elif tipo == "ranking":
        await ranking(query)

    elif tipo == "comparar":
        await comparar(query)

# MAIN
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))

    # ALERTAS EN BACKGROUND
    app.job_queue.run_once(lambda ctx: asyncio.create_task(enviar_alertas(app)), 1)

    print("🔥 BOT NEGOCIO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

