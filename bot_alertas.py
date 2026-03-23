import os
import json
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# LOGS (IMPORTANTE PARA RAILWAY)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# TOKEN
TOKEN = os.getenv("BOT_TOKEN")

# CARGAR DATA
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ⚠️ AVISO LEGAL
async def aviso(update: Update):
    await update.message.reply_text(
        "⚠️ Esto no es asesoría financiera. Toda inversión tiene riesgo."
    )

# 💰 PRECIO CRIPTO (GRATIS)
def obtener_precio(coin="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        res = requests.get(url, timeout=10)
        return res.json()[coin]["usd"]
    except:
        return "No disponible"

# 🧠 IA LOCAL (SIN API)
def interpretar(texto):
    texto = texto.lower()

    if any(p in texto for p in ["bitcoin", "btc", "crypto", "cripto", "ethereum"]):
        return "cripto"

    if any(p in texto for p in ["acciones", "bolsa", "invertir", "trading", "etf"]):
        return "bolsa"

    if any(p in texto for p in ["seguro", "ahorro", "rendimiento", "sin riesgo"]):
        return "ahorro"

    return "ahorro"

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("🧠 Recomiéndame", callback_data="ia")]
    ]

    await update.message.reply_text(
        "💸 Bot financiero PRO\n\nElige una opción:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await aviso(update)

# 🎯 BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data

    if tipo == "cripto":
        btc = obtener_precio("bitcoin")
        eth = obtener_precio("ethereum")

        await query.message.reply_text(
            f"💰 Precios actuales:\nBTC: ${btc}\nETH: ${eth}"
        )

    if tipo == "ia":
        await query.message.reply_text("Escríbeme qué buscas:")
        return

    resultados = [x for x in data if x["tipo"] == tipo]

    if not resultados:
        await query.message.reply_text("No hay opciones disponibles.")
        return

    botones = []
    for r in resultados:
        link = r.get("afiliado") or r["link"]
        botones.append([
            InlineKeyboardButton(
                f"{r['nombre']} ({r['riesgo']})",
                url=link
            )
        ])

    await query.message.reply_text(
        f"Opciones en {tipo}:",
        reply_markup=InlineKeyboardMarkup(botones)
    )

# 🧠 MENSAJES (IA LOCAL)
async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    categoria = interpretar(texto)

    resultados = [
        x for x in data
        if categoria in x["tipo"] or categoria in x["riesgo"]
    ]

    if not resultados:
        await update.message.reply_text("No encontré algo exacto.")
        return

    botones = []
    for r in resultados:
        link = r.get("afiliado") or r["link"]
        botones.append([
            InlineKeyboardButton(r["nombre"], url=link)
        ])

    await update.message.reply_text(
        "🔎 Te recomiendo:",
        reply_markup=InlineKeyboardMarkup(botones)
    )

    await aviso(update)

# MAIN
def main():
    if not TOKEN:
        raise ValueError("Falta BOT_TOKEN en variables de entorno")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))

    print("🔥 BOT ACTIVO 24/7")
    app.run_polling()

if __name__ == "__main__":
    main()
   

    
