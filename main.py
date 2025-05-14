from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import httpx
import asyncio

# Token del bot de Telegram
TOKEN = "7407294284:AAGkVv6AlzOlgOVhDqrDhfcGtYhajtA7Amk"

# Configuración de la API
API_URL = "https://api.factiliza.com/v1/dni/info/{dni}"  # Endpoint para consultas DNI
API_AUTH = "7407294284:AAGkVv6AlzOlgOVhDqrDhfcGtYhajtA7Amk"  # Reemplaza con tu token de autorización

# Base de datos en memoria simulada para créditos de usuarios
users_credits = {}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    if user_id not in users_credits:
        users_credits[user_id] = 10  # Créditos iniciales para nuevos usuarios
    await update.message.reply_text(f"Hola {user.first_name}, bienvenido al bot. Usa /register para registrarte.")

# Comando /register
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users_credits:
        users_credits[user_id] = 10
        await update.message.reply_text("Registro exitoso. Se te han asignado 10 créditos.")
    else:
        await update.message.reply_text("Ya estás registrado. Usa /me para ver tus créditos.")

# Comando /me
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in users_credits:
        credits = users_credits[user_id]
        await update.message.reply_text(f"Tienes {credits} créditos disponibles.")
    else:
        await update.message.reply_text("No estás registrado. Usa /register para registrarte.")

# Comando /recargar
async def recargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in users_credits:
        users_credits[user_id] += 10  # Incrementar créditos
        await update.message.reply_text("Se han recargado 10 créditos a tu cuenta.")
    else:
        await update.message.reply_text("No estás registrado. Usa /register para registrarte.")

async def dni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Uso: /dni <DNI>")
        return
    
    dni = context.args[0]

    try:
        # Realizar la consulta a la API de forma asíncrona
        async with httpx.AsyncClient() as client:
            response = await client.get(
                API_URL.format(dni=dni),
                headers={"Authorization": API_AUTH}
            )
        
        if response.status_code == 200:
            data = response.json()
            # Formatear la respuesta
            response_text = (
                f"🔍 Consulta DNI:\n"
                f"Nombre: {data.get('nombre', 'N/A')}\n"
                f"Apellido: {data.get('apellido', 'N/A')}\n"
                f"Domicilio: {data.get('direccion', 'N/A')}\n"
                f"Fecha de Nacimiento: {data.get('fecha_nacimiento', 'N/A')}\n"
            )
            await update.message.reply_text(response_text)
        else:
            await update.message.reply_text(f"Error en la consulta. Código de estado: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Ocurrió un error al realizar la consulta: {e}")

 
# Ejecutar el bot
if __} # type: ignore


 name__ == "_main_":
    app = Application.builder().token(TOKEN).build()

    # Registro de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("me", me))
    app.add_handler(CommandHandler("recargar", recargar))
    app.add_handler(CommandHandler("dni", dni))

    # Ejecutar el bot
    app.run_polling()