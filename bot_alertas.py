import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# =========================
# SISTEMA DE CONTEO
# =========================
def registrar_usuario(user_id):
    try:
        usuarios = set()
        if os.path.exists("usuarios.txt"):
            with open("usuarios.txt", "r") as f:
                usuarios = set(line.strip() for line in f)
        usuarios.add(str(user_id))
        with open("usuarios.txt", "w") as f:
            for uid in usuarios:
                f.write(f"{uid}\n")
    except: pass

def obtener_conteo():
    if not os.path.exists("usuarios.txt"): return 0
    with open("usuarios.txt", "r") as f:
        return len(f.readlines())

# =========================
# LIMPIAR WEBHOOK
# =========================
async def limpiar():
    bot = Bot(TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.close()

asyncio.get_event_loop().run_until_complete(limpiar())

# =========================
# FORMATO PRO
# =========================
def formato_app(nombre, ganancia, riesgo, disponibilidad, ideal, extra=""):
    return (
        f"💰 *{nombre}*\n\n"
        f"📈 Cómo ganas: {ganancia}\n"
        f"⚠️ Riesgo: {riesgo}\n"
        f"🌎 Disponible en: {disponibilidad}\n"
        f"🎯 Ideal para: {ideal}\n\n"
        f"{extra}"
    )

# =========================
# MENÚ PRINCIPAL
# =========================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Recomendado", callback_data="top")],
        [InlineKeyboardButton("💰 Ahorro", callback_data="ahorro")],
        [InlineKeyboardButton("📈 Bolsa", callback_data="bolsa")],
        [InlineKeyboardButton("🪙 Cripto", callback_data="cripto")],
        [InlineKeyboardButton("💸 Ganar dinero", callback_data="ganar")],
        [InlineKeyboardButton("🧠 Asesor", callback_data="asesor")]
    ])

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Bienvenido a Investia Pro*\n\n"
        "💸 Descubre las mejores formas de ahorrar, invertir y generar ingresos.\n\n"
        "⚠️ *No somos asesores financieros.*\n\n"
        "Selecciona una opción 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =========================
# HANDLER
# =========================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ⭐ TOP
    if data == "top":
        await query.edit_message_text(
            "⭐ *Apps recomendadas*\n\nEmpieza aquí 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu", callback_data="app_nu")],
                [InlineKeyboardButton("CETES", callback_data="app_cetes")],
                [InlineKeyboardButton("GBM+", callback_data="app_gbm")],
                [InlineKeyboardButton("Binance", callback_data="app_binance")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    # ===== AHORRO =====
    elif data == "ahorro":
        await query.edit_message_text(
            "💰 *Ahorro (bajo riesgo)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Nu ⭐", callback_data="app_nu")],
                [InlineKeyboardButton("Klar", callback_data="app_klar")],
                [InlineKeyboardButton("Ualá", callback_data="app_uala")],
                [InlineKeyboardButton("MercadoPago", callback_data="app_mp")],
                [InlineKeyboardButton("Hey Banco", callback_data="app_hey")],
                [InlineKeyboardButton("CETES ⭐", callback_data="app_cetes")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_nu":
        await query.edit_message_text(
            formato_app("Nu Bank","Intereses diarios","Bajo","México","Empezar fácil","✔️ Sin comisiones"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://nu.com.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=nu+bank+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_klar":
        await query.edit_message_text(
            formato_app("Klar","Ahorro con rendimiento","Bajo","México","Usuarios nuevos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.klar.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=klar+app+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_uala":
        await query.edit_message_text(
            formato_app("Ualá","Cuenta digital","Bajo","México","Uso diario"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.uala.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=uala+app+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mp":
        await query.edit_message_text(
            formato_app("MercadoPago","Rendimiento automático","Bajo","México","Ahorro flexible"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.mercadopago.com.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=mercadopago+rendimiento")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_hey":
        await query.edit_message_text(
            formato_app("Hey Banco","Ahorro digital","Bajo","México","Usuarios bancarios"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.heybanco.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=hey+banco+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_cetes":
        await query.edit_message_text(
            formato_app("CETES","Intereses del gobierno","Muy bajo","México","Perfil conservador","✔️ Alta seguridad"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.cetesdirecto.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=cetes+directo+como+invertir")],
                [InlineKeyboardButton("🔙", callback_data="ahorro")]
            ]),
            parse_mode="Markdown"
        )

    # ===== BOLSA =====
    elif data == "bolsa":
        await query.edit_message_text(
            "📈 *Bolsa (riesgo medio)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("GBM+ ⭐", callback_data="app_gbm")],
                [InlineKeyboardButton("Kuspit", callback_data="app_kuspit")],
                [InlineKeyboardButton("Bursanet", callback_data="app_bursanet")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_gbm":
        await query.edit_message_text(
            formato_app("GBM+","Acciones y ETFs","Medio","México","Inversión a largo plazo"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://gbm.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=gbm+como+invertir")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_kuspit":
        await query.edit_message_text(
            formato_app("Kuspit","Acciones","Medio","México","Aprender"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.kuspit.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=kuspit+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bursanet":
        await query.edit_message_text(
            formato_app("Bursanet","Fondos y acciones","Medio","México","Avanzados"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.bursanet.mx")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=bursanet+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="bolsa")]
            ]),
            parse_mode="Markdown"
        )

    # ===== CRIPTO =====
    elif data == "cripto":
        await query.edit_message_text(
            "🪙 *Cripto (alto riesgo)*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Binance ⭐", callback_data="app_binance")],
                [InlineKeyboardButton("Bitso", callback_data="app_bitso")],
                [InlineKeyboardButton("Bybit", callback_data="app_bybit")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_binance":
        await query.edit_message_text(
            formato_app("Binance","Trading y staking","Alto","Global","Avanzados","⚠️ Volátil"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.binance.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=binance+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bitso":
        await query.edit_message_text(
            formato_app("Bitso","Compra sencilla","Medio","México","Principiantes"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://bitso.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=bitso+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_bybit":
        await query.edit_message_text(
            formato_app("Bybit","Trading avanzado","Alto","Global","Expertos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.bybit.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=bybit+como+usar")],
                [InlineKeyboardButton("🔙", callback_data="cripto")]
            ]),
            parse_mode="Markdown"
        )

    # ===== GANAR DINERO =====
    elif data == "ganar":
        await query.edit_message_text(
            "💸 *Ganar dinero*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Google Rewards ⭐", callback_data="app_google")],
                [InlineKeyboardButton("Viewpoints", callback_data="app_view")],
                [InlineKeyboardButton("Nicequest", callback_data="app_nice")],
                [InlineKeyboardButton("Mode", callback_data="app_mode")],
                [InlineKeyboardButton("Atlas Earth", callback_data="app_atlas")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_google":
        await query.edit_message_text(
            formato_app("Google Rewards","Encuestas","Muy bajo","Global","Cualquiera"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com/store/apps/details?id=com.google.android.apps.paidtasks")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=google+rewards+como+funciona")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_view":
        await query.edit_message_text(
            formato_app("Viewpoints","Encuestas","Muy bajo","Global","Casual"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://viewpoints.fb.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=viewpoints+meta")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_nice":
        await query.edit_message_text(
            formato_app("Nicequest","Encuestas","Muy bajo","Global","Pacientes"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://www.nicequest.com")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=nicequest+como+funciona")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_mode":
        await query.edit_message_text(
            formato_app("Mode","Escuchar música","Bajo","Global","Ingresos pasivos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com/store/apps/details?id=us.current.android")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=mode+earn+app")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "app_atlas":
        await query.edit_message_text(
            formato_app("Atlas Earth","Renta virtual","Medio","Global","Curiosos"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📲 Ir", url="https://play.google.com/store/search?q=atlas+earth&c=apps")],
                [InlineKeyboardButton("🎥 Ver tutorial", url="https://www.youtube.com/results?search_query=atlas+earth+como+funciona")],
                [InlineKeyboardButton("🔙", callback_data="ganar")]
            ]),
            parse_mode="Markdown"
        )

    # ===== ASESOR =====
    elif data == "asesor":
        await query.edit_message_text(
            "🧠 *Asesor Investia*\n\nSelecciona tu nivel 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("👶 Nuevo", callback_data="nivel_nuevo")],
                [InlineKeyboardButton("📈 Intermedio", callback_data="nivel_intermedio")],
                [InlineKeyboardButton("🔥 Avanzado", callback_data="nivel_avanzado")],
                [InlineKeyboardButton("🔙 Menú", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )

    elif data == "nivel_nuevo":
        await query.edit_message_text(
            "👶 Empieza con bajo riesgo 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a ahorro", callback_data="ahorro")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ])
        )

    elif data == "nivel_intermedio":
        await query.edit_message_text(
            "📈 Nivel intermedio 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a bolsa", callback_data="bolsa")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ])
        )

    elif data == "nivel_avanzado":
        await query.edit_message_text(
            "🔥 Nivel avanzado 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Ir a cripto", callback_data="cripto")],
                [InlineKeyboardButton("🔙", callback_data="asesor")]
            ])
        )

    elif data == "menu":
        await query.edit_message_text("📌 Menú principal 👇", reply_markup=main_menu())

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🔥 INVESTIA PRO MAX ACTIVO")
    app.run_polling()

if __name__ == "__main__":
    main()
