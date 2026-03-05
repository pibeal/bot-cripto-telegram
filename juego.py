import sqlite3, random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8718683908:AAFHR0BJ4mzRZw450TUciw_-jrxPb8VVMK4'

# Imágenes estables
IMG_PUEBLO = "https://i.imgur.com"
IMG_CAMINO = "https://i.imgur.com" # Imagen para bifurcación

def conectar_db():
    conn = sqlite3.connect('rpg_pro.db')
    cursor = conn.cursor()
    # ID, Nombre, Oro, Nivel, HP_Act, HP_Max, ATK, MP (Mana)
    cursor.execute('''CREATE TABLE IF NOT EXISTS heroe 
                      (id INTEGER PRIMARY KEY, nombre TEXT, oro INTEGER, nivel INTEGER, 
                       hp_act INTEGER, hp_max INTEGER, atk INTEGER, mp INTEGER)''')
    conn.commit()
    return conn

async def refrescar(context, chat_id, foto, texto, botones, query=None):
    markup = InlineKeyboardMarkup(botones)
    if query: 
        try: await query.delete_message()
        except: pass
    try: await context.bot.send_photo(chat_id=chat_id, photo=foto, caption=texto, reply_markup=markup, parse_mode='Markdown')
    except: await context.bot.send_message(chat_id=chat_id, text=texto, reply_markup=markup, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = conectar_db(); c = conn.cursor()
    c.execute("SELECT * FROM heroe WHERE id = ?", (user.id,))
    h = c.fetchone()
    if not h:
        c.execute("INSERT INTO heroe VALUES (?, ?, 0, 1, 100, 100, 15, 50)", (user.id, user.first_name))
        conn.commit(); h = (user.id, user.first_name, 0, 1, 100, 100, 15, 50)
    conn.close()
    txt = f"🏰 **CIUDAD CENTRAL**\n❤️ HP: {h[4]}/{h[5]} | ✨ MP: {h[7]}\n💰 Oro: {h[2]}"
    btns = [[InlineKeyboardButton("🏰 Ir a la Mazmorra", callback_data='camino_inicial')],
            [InlineKeyboardButton("🏥 Curar (20 oro)", callback_data='curar_pueblo')]]
    await refrescar(context, update.message.chat_id, IMG_PUEBLO, txt, btns)

async def controlador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    user_id = query.from_user.id
    conn = conectar_db(); c = conn.cursor()
    c.execute("SELECT * FROM heroe WHERE id = ?", (user_id,))
    h = list(c.fetchone())

    # --- BIFURCACIÓN DE CAMINOS ---
    if query.data == 'camino_inicial':
        txt = "🛤️ Llegas a una división. ¿Qué camino tomas?\n\n⬅️ **Izquierda:** Bosque oscuro (Más monstruos).\n➡️ **Derecha:** Cuevas (Más tesoros)."
        btns = [[InlineKeyboardButton("🌲 Bosque", callback_data='explorar_facil')],
                [InlineKeyboardButton("🕳️ Cuevas", callback_data='explorar_dificil')]]
        await refrescar(context, query.message.chat_id, IMG_CAMINO, txt, btns, query)

    # --- EXPLORACIÓN ---
    elif 'explorar' in query.data:
        ev = random.choice(['m', 'm', 't']) if 'facil' in query.data else random.choice(['m', 't', 't'])
        if ev == 't':
            oro = random.randint(30, 80)
            c.execute("UPDATE heroe SET oro = oro + ? WHERE id = ?", (oro, user_id))
            conn.commit()
            await refrescar(context, query.message.chat_id, IMG_CAMINO, f"💎 ¡Tesoro! +{oro} oro.", [[InlineKeyboardButton("Volver", callback_data='volver')]], query)
        else:
            # Aparece enemigo
            m_hp = 60; context.user_data.update({'m_hp': m_hp, 'm_at': 12})
            txt = f"👾 **¡ENEMIGO APARECE!**\n❤️ HP Monstruo: {m_hp}"
            btns = [
                [InlineKeyboardButton("⚔️ Pelear", callback_data='atacar')],
                [InlineKeyboardButton("🔥 Habilidad (20 MP)", callback_data='especial')],
                [InlineKeyboardButton("🧪 Poción (15 oro)", callback_data='pocion')],
                [InlineKeyboardButton("🏃 Huir", callback_data='volver')]
            ]
            await refrescar(context, query.message.chat_id, "https://i.imgur.com", txt, btns, query)

    # --- COMBATE ---
    elif query.data in ['atacar', 'especial', 'pocion']:
        d_m = random.randint(8, 15)
        txt_accion = ""

        if query.data == 'atacar':
            d_h = random.randint(h[6]-5, h[6]+5)
            txt_accion = f"⚔️ Golpeaste por {d_h}."
            context.user_data['m_hp'] -= d_h
        elif query.data == 'especial':
            if h[7] >= 20:
                d_h = h[6] * 2
                h[7] -= 20
                txt_accion = f"🔥 ¡EXPLOSIÓN MÁGICA! Daño: {d_h}."
                context.user_data['m_hp'] -= d_h
            else:
                await query.answer("❌ Sin Maná", show_alert=True); conn.close(); return
        elif query.data == 'pocion':
            if h[2] >= 15:
                h[4] = min(h[5], h[4] + 40)
                h[2] -= 15
                txt_accion = "🧪 Usaste una poción. +40 HP."
                d_m = 0 # El enemigo no ataca si usas pocion (ventaja)
            else:
                await query.answer("❌ Sin oro", show_alert=True); conn.close(); return

        h[4] -= d_m
        c.execute("UPDATE heroe SET hp_act = ?, oro = ?, mp = ? WHERE id = ?", (max(0, h[4]), h[2], h[7], user_id))
        conn.commit()

        if context.user_data['m_hp'] <= 0:
            await refrescar(context, query.message.chat_id, IMG_PUEBLO, "🏆 ¡Victoria!", [[InlineKeyboardButton("Volver", callback_data='volver')]], query)
        elif h[4] <= 0:
            c.execute("UPDATE heroe SET hp_act = 0, oro = oro / 2 WHERE id = ?", (user_id,))
            conn.commit()
            await refrescar(context, query.message.chat_id, IMG_PUEBLO, "💀 Has muerto.", [[InlineKeyboardButton("Resucitar", callback_data='volver')]], query)
        else:
            txt = f"{txt_accion}\n💥 Recibiste {d_m} de daño.\n❤️ Tu HP: {h[4]} | 👾 Enemigo: {context.user_data['m_hp']}"
            btns = [[InlineKeyboardButton("⚔️ Seguir", callback_data='atacar')],
                    [InlineKeyboardButton("🔥 Especial", callback_data='especial')],
                    [InlineKeyboardButton("🏃 Huir", callback_data='volver')]]
            await refrescar(context, query.message.chat_id, "https://i.imgur.com", txt, btns, query)

    elif query.data == 'volver':
        await query.delete_message()
        await start(update, context)
    
    elif query.data == 'curar_pueblo':
        if h[2] >= 20:
            c.execute("UPDATE heroe SET hp_act = hp_max, mp = 50, oro = oro - 20 WHERE id = ?", (user_id,))
            conn.commit(); await query.answer("💖 Recuperado", show_alert=True)
            await start(update, context)
        else: await query.answer("❌ Sin oro", show_alert=True)

    conn.close()

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(controlador))
    app.run_polling()
