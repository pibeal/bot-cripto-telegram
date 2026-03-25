import os
import json
import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

# 📂 DATA
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 📂 USERS
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
AVISO = "⚠️ Esto no es asesoría financiera. Toda inversión tiene riesgo."

# 💰 BTC
def precio():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        return requests.get(url).json()["bitcoin"]["usd"]
    except:
        return "N/A"

# 🏠 MENU PRINCIPAL
def menu_principal():
    texto = (
        "💸 *FINANCE BOT PRO*\n"
        "━━━━━━━━━━━━━━━\n\n"
        "Explora y compara inversiones.\n\n"
        "👇 Selecciona:"
    )

    keyboard = [
        [
            InlineKeyboardButton("💰 Ahorro", callback_data="ahorro"),
            InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")
        ],
        [
            InlineKeyboardButton("🪙 Cripto", callback_data="cripto")
        ],
        [
            InlineKeyboardButton("🏆 Ranking", callback_data="ranking"),
            InlineKeyboardButton("🆚 Comparar", callback_data="comparar")
        ]
    ]

    return texto, keyboard

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guardar_user(update.effective_chat.id)

    texto, keyboard = menu_principal()

    await update.message.reply_text(
        texto,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN
    )

# 📊 MOSTRAR
def generar_lista(tipo):
    resultados = [x for x in data if x["tipo"] == tipo]

    mensaje = f"*{tipo.upper()}*\n━━━━━━━━━━━━━━━\n\n"
    botones = []

    for r in resultados:
        mensaje += (
            f"🏦 *{r['nombre']}*\n"
            f"• Rendimiento: {r['rendimiento']}\n"
            f"• Liquidez: {r['liquidez']}\n"
            f"• Riesgo: {r['riesgo']}\n"
            f"• {r['descripcion']}\n\n"
        )

        botones.append([
            InlineKeyboardButton(f"Abrir {r['nombre']}", url=r["link"])
        ])

    botones.append([
        InlineKeyboardButton("⬅️ Volver", callback_data="menu")
    ])

    return mensaje, botones

# 🏆 RANKING
def generar_ranking():
    orden = sorted(data, key=lambda x: x["riesgo"])

    mensaje = "*🏆 TOP OPCIONES*\n━━━━━━━━━━━━━━━\n\n"
    for i, r in enumerate(orden[:5], 1):
        mensaje += f"{i}. {r['nombre']} ({r['tipo']})\n"

    botones = [[InlineKeyboardButton("⬅️ Volver", callback_data="menu")]]

    return mensaje, botones

# 🆚 COMPARAR
def generar_comparacion():
    a, b = data[0], data[1]

    mensaje = (
        "*🆚 COMPARACIÓN*\n━━━━━━━━━━━━━━━\n\n"
        f"{a['nombre']} vs {b['nombre']}\n\n"
        f"💰 {a['rendimiento']} vs {b['rendimiento']}\n"
        f"⚠️ {a['riesgo']} vs {b['riesgo']}\n"
        f"💧 {a['liquidez']} vs {b['liquidez']}\n"
    )

    botones = [[InlineKeyboardButton("⬅️ Volver", callback_data="menu")]]

    return mensaje, botones

# 🎯 BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    tipo = query.data

    if tipo == "menu":
        texto, keyboard = menu_principal()
        await query.message.edit_text(
            texto,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
        return

    if tipo in ["ahorro", "bolsa", "cripto"]:
        mensaje, botones = generar_lista(tipo)

        if tipo == "cripto":
            btc = precio()
            mensaje = f"💰 BTC: ${btc}\n\n" + mensaje

    elif tipo == "ranking":
        mensaje, botones = generar_ranking()

    elif tipo == "comparar":
        mensaje, botones = generar_comparacion()

    else:
        return

    await query.message.edit_text(
        mensaje,
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode=ParseMode.MARKDOWN
    )

# 🧠 MENSAJE
async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if "btc" in texto:
        tipo = "cripto"
    elif "bolsa" in texto:
        tipo = "bolsa"
    else:
        tipo = "ahorro"

    mensaje, botones = generar_lista(tipo)

    await update.message.reply_text(
        mensaje,
        reply_markup=InlineKeyboardMarkup(botones),
        parse_mode=ParseMode.MARKDOWN
    )

# 🚀 MAIN
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botones))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje))

    print("🔥 BOT APP PRO ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
    
