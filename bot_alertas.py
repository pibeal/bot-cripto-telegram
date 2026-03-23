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
    filters,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ⚠️ AVISO
async def aviso(update):
    await update.message.reply_text(
        "⚠️ Esto no es asesoría financiera. Toda inversión tiene riesgo."
    )

# 🧠 IA LOCAL
def interpretar(texto):
    texto = texto.lower()

    if any(p in texto for p in ["bitcoin", "btc", "crypto", "cripto"]):
        return "cripto"
    if any(p in texto for p in ["bolsa", "acciones", "etf"]):
        return "bolsa"
    return "ahorro"

# 💰 PRECIO
def precio(coin="bitcoin"):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        return requests.get(url).json()[coin]["usd"]
    except:
        return "N/A"

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "💸 *FINANCE BOT PRO*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "Encuentra y compara opciones para hacer crecer tu dinero.\n\n"
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
            InlineKeyboardButton("🆚 Comparar", callback_data="comparar"),
            InlineKeyboardButton("🧠 Recomendar", callback_data="ia")
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
    orden = sorted(data, key=lambda x: x.get("riesgo", "z"))

    mensaje = "*🏆 TOP OPCIONES*\n━━━━━━━━━━━━━━━\n\n"

    for i, r in enumerate(orden[:5], 1):
        mensaje += f"{i}. {r['nombre']} ({r['tipo']})\n"

    await update.message.reply_text(
        mensaje,
        parse_mode=ParseMode.MARKDOWN
    )

# 🆚 COMPARADOR
async def comparar(update):
    if len(data) < 2:
        await update.message.reply_text("No hay suficientes opciones.")
        return

    a, b = data[0], data[1]

    mensaje = (
        "*🆚 COMPARACIÓN*\n━━━━━━━━━━━━━━━\n\n"
        f"*{a['nombre']} vs {b['nombre']}*\n\n"
        f"Rendimiento:\n{a.get('rendimiento')} vs {b.get('rendimiento')}\n\n"
        f"Riesgo:\n{a['riesgo']} vs {b['riesgo']}\n\n"
        f"Liquidez:\n{a.get('liquidez')} vs {b.get('liquidez')}\n"
    )

    await update.message.reply_text(
        mensaje,
        parse_mode=ParseMode.MARKDOWN
    )

# 🎯 BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data

    if tipo == "ahorro" or tipo == "bolsa" or tipo == "cripto":
        if tipo == "cripto":
            btc = precio("bitcoin")
            await query.message.reply_text(f"💰 BTC: ${btc}")

        await mostrar(query, tipo)

    elif tipo == "ranking":
        await ranking(query)

    elif tipo == "comparar":
        await comparar(query)

    elif tipo == "ia":
        await query.message.reply_text("Escribe lo que buscas:")

# 🧠 MENSAJES
async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    tipo = interpretar(texto)

    await mostrar(update, tipo)
    await aviso(update)

# MAIN
def main():
    if not TOKEN:
        raise ValueError("Falta BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))

    print("🔥 BOT PRO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
