import random, os
from PIL import Image, ImageDraw
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURACIÓN ---
TOKEN = 'tu token aqui'  # <--- PEGA TU TOKEN AQUÍ
MAPA_SIZE = 8
TILE_SIZE = 60 

SPRITES = {}
ARCHIVOS = {
    'zombi': 'zombi.png',
    'humano': 'humano.png',
    'casa': 'casa.png',
    'piso': 'piso.png'
}

# --- MOTOR DE RECURSOS (LOCAL) ---
def cargar_recursos():
    print("Cargando gráficos desde tu carpeta...")
    for nombre, archivo in ARCHIVOS.items():
        if os.path.exists(archivo):
            img = Image.open(archivo).convert("RGBA")
            SPRITES[nombre] = img.resize((TILE_SIZE, TILE_SIZE))
            print(f"✅ {nombre} cargado correctamente.")
        else:
            print(f"❌ ERROR: No encontré '{archivo}' en la carpeta.")
            # Respaldo si no está la imagen
            SPRITES[nombre] = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), (255,0,0,255))

# --- MOTOR GRÁFICO ---
def renderizar_mapa(px, py, zombis, casas):
    mapa_img = Image.new('RGBA', (MAPA_SIZE * TILE_SIZE, MAPA_SIZE * TILE_SIZE), (30, 30, 30, 255))
    for y in range(MAPA_SIZE):
        for x in range(MAPA_SIZE):
            mapa_img.paste(SPRITES['piso'], (x * TILE_SIZE, y * TILE_SIZE))
    for (cx, cy) in casas:
        mapa_img.paste(SPRITES['casa'], (cx * TILE_SIZE, cy * TILE_SIZE), SPRITES['casa'])
    for (zx, zy) in zombis:
        mapa_img.paste(SPRITES['zombi'], (zx * TILE_SIZE, zy * TILE_SIZE), SPRITES['zombi'])
    mapa_img.paste(SPRITES['humano'], (px * TILE_SIZE, py * TILE_SIZE), SPRITES['humano'])
    mapa_img.save("render.png")
    return "render.png"

# --- LÓGICA DE JUEGO (IA ZOMBI) ---
def mover_horda(px, py, zombis):
    nuevos = []
    for (zx, zy) in zombis:
        if random.random() < 0.4:
            if zx < px: zx += 1
            elif zx > px: zx -= 1
            elif zy < py: zy += 1
            elif zy > py: zy -= 1
        nuevos.append((zx, zy))
    return nuevos

# --- COMANDOS Y CONTROLADOR ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'hp' not in context.user_data or context.user_data['hp'] <= 0:
        context.user_data.update({
            'x': 0, 'y': 7, 'hp': 100, 'balas': 15,
            'zombis': [(random.randint(2,7), random.randint(0,5)) for _ in range(6)],
            'casas': [(2,2), (5,5), (1,1), (6,6)]
        })
    u = context.user_data
    img_p = renderizar_mapa(u['x'], u['y'], u['zombis'], u['casas'])
    txt = f"🧟 **MODO SUPERVIVENCIA**\n❤️ HP: {u['hp']} | 🔫 Balas: {u['balas']}"
    btns = [[InlineKeyboardButton("⬆️", callback_data='up')],
            [InlineKeyboardButton("⬅️", callback_data='left'), InlineKeyboardButton("➡️", callback_data='right')],
            [InlineKeyboardButton("⬇️", callback_data='down')]]
    with open(img_p, 'rb') as f:
        if update.message: await update.message.reply_photo(f, caption=txt, reply_markup=InlineKeyboardMarkup(btns))
        else:
            try: await update.callback_query.message.delete()
            except: pass
            await context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=f, caption=txt, reply_markup=InlineKeyboardMarkup(btns))

async def controlador(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; await query.answer(); u = context.user_data
    old_x, old_y = u['x'], u['y']
    if query.data == 'up' and u['y'] > 0: u['y'] -= 1
    elif query.data == 'down' and u['y'] < MAPA_SIZE - 1: u['y'] += 1
    elif query.data == 'left' and u['x'] > 0: u['x'] -= 1
    elif query.data == 'right' and u['x'] < MAPA_SIZE - 1: u['x'] += 1
    u['zombis'] = mover_horda(u['x'], u['y'], u['zombis'])
    pos = (u['x'], u['y'])
    if pos in u['zombis']:
        if u['balas'] > 0:
            u['balas'] -= 1; u['zombis'].remove(pos); await query.answer("¡PUM! 💥")
        else:
            u['hp'] -= 30; u['x'], u['y'] = old_x, old_y; await query.answer("¡MORDIDA! 🩸", show_alert=True)
    if pos in u['casas']:
        u['balas'] += 5; u['casas'].remove(pos); await query.answer("Munición encontrada 🏚️🎁")
    if u['hp'] <= 0: await query.message.reply_text("💀 Has muerto.")
    else: await start(update, context)

if __name__ == '__main__':
    cargar_recursos()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(controlador))
    print("🧟 ¡A jugar!")
    app.run_polling()
