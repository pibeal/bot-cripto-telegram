import random, time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '8718683908:AAFHR0BJ4mzRZw450TUciw_-jrxPb8VVMK4'
MAPA_SIZE = 7 # Un poco más pequeño para que quepa bien en el celular

# --- ICONOS PRO ---
PISO = "⬛"
PLAYER = "🏃‍♂️"
ZOMBI = "🧟"
CASA = "🏚️"
BALAS = "📦"

def generar_grid(px, py, zombis, casas, balas_pos):
    grid = ""
    for y in range(MAPA_SIZE):
        for x in range(MAPA_SIZE):
            if x == px and y == py: grid += PLAYER
            elif (x, y) in zombis: grid += ZOMBI
            elif (x, y) in casas: grid += CASA
            elif (x, y) in balas_pos: grid += BALAS
            else: grid += PISO
        grid += "\n"
    return grid

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inicializamos todo en memoria (User Data)
    context.user_data.update({
        'x': 3, 'y': 3, 'hp': 100, 'ammo': 10,
        'zombis': [(random.randint(0,6), random.randint(0,6)) for _ in range(4)],
        'casas': [(0,0), (6,6)],
        'balas_pos': [(random.randint(0,6), random.randint(0,6))]
    })
    
    u = context.user_data
    mapa = generar_grid(u['x'], u['y'], u['zombis'], u['casas'], u['balas_pos'])
    
    txt = f"🧟 **ZONA DE GUERRA**\n\n{mapa}\n❤️ Vida: {u['hp']}% | 🔫 Balas: {u['ammo']}"
    
    btns = [
        [InlineKeyboardButton("⬆️", callback_data='u')],
        [InlineKeyboardButton("⬅️", callback_data='l'), InlineKeyboardButton("➡️", callback_data='r')],
        [InlineKeyboardButton("⬇️", callback_data='d')]
    ]
    
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(btns), parse_mode='Markdown')

async def jugar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer()
    u = context.user_data
    if 'x' not in u: return # Por si el bot se reinicia

    # Movimiento rápido
    if query.data == 'u' and u['y'] > 0: u['y'] -= 1
    if query.data == 'd' and u['y'] < MAPA_SIZE -1: u['y'] += 1
    if query.data == 'l' and u['x'] > 0: u['x'] -= 1
    if query.data == 'r' and u['x'] < MAPA_SIZE -1: u['x'] += 1

    # IA: Los zombis se mueven hacia ti
    nuevos_z = []
    for zx, zy in u['zombis']:
        if random.random() < 0.4: # Solo 40% de probabilidad de que el zombi se mueva
            if zx < u['x']: zx += 1
            elif zx > u['x']: zx -= 1
            if zy < u['y']: zy += 1
            elif zy > u['y']: zy -= 1
        nuevos_z.append((zx, zy))
    u['zombis'] = nuevos_z

    # Eventos (Colisiones)
    pos = (u['x'], u['y'])
    status = ""
    if pos in u['zombis']:
        if u['ammo'] > 0:
            u['ammo'] -= 1; u['zombis'].remove(pos); status = "💥 ¡PUM! Mataste a uno."
        else:
            u['hp'] -= 20; status = "🩸 ¡TE MORDIDIERON!"
    
    if pos in u['balas_pos']:
        u['ammo'] += 5; u['balas_pos'].remove(pos); status = "📦 +5 Balas encontradas."

    # ACTUALIZACIÓN SIN PARPADEO (edit_message_text)
    mapa = generar_grid(u['x'], u['y'], u['zombis'], u['casas'], u['balas_pos'])
    nuevo_txt = f"🧟 **ZONA DE GUERRA**\n\n{mapa}\n❤️ Vida: {u['hp']}% | 🔫 Balas: {u['ammo']}\n_{status}_"
    
    btns = [[InlineKeyboardButton("⬆️", callback_data='u')],
            [InlineKeyboardButton("⬅️", callback_data='l'), InlineKeyboardButton("➡️", callback_data='r')],
            [InlineKeyboardButton("⬇️", callback_data='d')]]

    try:
        await query.edit_message_text(nuevo_txt, reply_markup=InlineKeyboardMarkup(btns), parse_mode='Markdown')
    except: pass # Evita error si el mensaje es idéntico

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(jugar))
    app.run_polling()
