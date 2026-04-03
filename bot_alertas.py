import os, requests, sqlite3, tempfile, re, base64, time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

# =========================
# CONFIG
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TELEGRAM_TOKEN or not GROQ_API_KEY or not WEBHOOK_URL or not REPLICATE_API_TOKEN:
    raise ValueError("Faltan variables de entorno")

MODELO_TEXTO = "llama-3.3-70b-versatile"
MODELO_VISION = "llama-3.2-11b-vision-preview"
MAX_HISTORY = 10

# =========================
# DB
# =========================
def init_db():
    conn = sqlite3.connect("bot_pibeal.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mensajes 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       user_id TEXT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_to_db(user_id, role, content):
    try:
        conn = sqlite3.connect("bot_pibeal.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensajes (user_id, role, content) VALUES (?, ?, ?)",
                       (user_id, role, str(content)))
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB error:", e)

def get_history(user_id):
    try:
        conn = sqlite3.connect("bot_pibeal.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM mensajes WHERE user_id=? ORDER BY id DESC LIMIT ?",
                       (user_id, MAX_HISTORY))
        rows = cursor.fetchall()
        conn.close()
        return [{"role": r, "content": c} for r, c in reversed(rows)]
    except Exception as e:
        print("History error:", e)
        return []

def clear_history(user_id):
    try:
        conn = sqlite3.connect("bot_pibeal.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mensajes WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Clear error:", e)

init_db()

# =========================
# IA
# =========================
def preguntar_ia(user_id: str, pregunta: str, image_bytes: bytes = None) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}

    modelo = MODELO_TEXTO
    u_content = pregunta

    if image_bytes:
        modelo = MODELO_VISION
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        u_content = [
            {"type": "text", "text": pregunta},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]

    messages = [{"role": "system", "content": "Eres Pibeal IA PRO."}]
    messages += get_history(user_id)
    messages.append({"role": "user", "content": u_content})

    try:
        payload = {"model": modelo, "messages": messages, "temperature": 0.5}
        r = requests.post(url, headers=headers, json=payload, timeout=25)

        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            print("Groq error:", r.text)

    except Exception as e:
        print("IA error:", e)

    return "⚠️ Error con la IA."

# =========================
# IMÁGENES (REPLICATE)
# =========================
if img:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            f.write(img)
            temp_path = f.name

        with open(temp_path, "rb") as photo:
            await update.message.reply_photo(photo=photo)

    except Exception as e:
        print("Error enviando imagen:", e)
        await update.message.reply_text("⚠️ No se pudo enviar la imagen.")

    finally:
        try:
            os.remove(temp_path)
        except:
            pass
else:
    await update.message.reply_text("❌ Error generando imagen.")

# =========================
# AUDIO
# =========================
audio = texto_a_voz(res)

if audio:
    try:
        if os.path.exists(audio) and os.path.getsize(audio) > 0:
            with open(audio, "rb") as f:
                await update.message.reply_voice(voice=f)
        else:
            print("Audio vacío o no existe")

    except Exception as e:
        print("Error enviando audio:", e)

    finally:
        try:
            os.remove(audio)
        except:
            pass

# =========================
# TELEGRAM
# =========================
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = str(update.message.from_user.id)
    texto = update.message.text.strip() if update.message.text else ""

    # RESET
    if texto.lower() in ["/reset", "/start"]:
        clear_history(user_id)
        await update.message.reply_text("🧹 Memoria reiniciada.")
        return

    # FOTO
    if update.message.photo:
        await update.message.reply_text("👀 Analizando imagen...")

        file = await update.message.photo[-1].get_file()
        image_bytes = await file.download_as_bytearray()

        save_to_db(user_id, "user", "imagen enviada")

        res = preguntar_ia(user_id, "Analiza esta imagen.", image_bytes)

        save_to_db(user_id, "assistant", res)

        await update.message.reply_text(res)
        return

    # TEXTO
    if texto:
        if texto.startswith("/imagen "):
            prompt = texto.replace("/imagen ", "")
            await update.message.reply_text("🎨 Generando imagen...")

            img = generar_imagen(prompt)

            if img:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
                    f.write(img)
                    temp_path = f.name

                with open(temp_path, "rb") as photo:
                    await update.message.reply_photo(photo=photo)

                os.remove(temp_path)
            else:
                await update.message.reply_text("❌ Error generando imagen.")

            return

        # GUARDAR MEMORIA
        save_to_db(user_id, "user", texto)

        res = preguntar_ia(user_id, texto)

        save_to_db(user_id, "assistant", res)

        await update.message.reply_text(res)

        # AUDIO
        audio = texto_a_voz(res)
        if audio:
            try:
                with open(audio, "rb") as f:
                    await update.message.reply_voice(voice=f)
            except Exception as e:
                print("Audio error:", e)
            finally:
                try:
                    os.remove(audio)
                except:
                    pass

# =========================
# FASTAPI
# =========================
bot_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
bot_app.add_handler(MessageHandler(filters.ALL, responder))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print("✅ BOT PRO FINAL CON MEMORIA ACTIVA")
    yield
    await bot_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def webhook(req: Request):
    try:
        data = await req.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
    except Exception as e:
        print("Webhook error:", e)

    return {"ok": True}
