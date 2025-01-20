import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz
import os

# Токен Telegram-бота (указывается через переменные окружения для безопасности)
TOKEN = os.getenv("TOKEN")
FIXED_PRICE = '120₸'
PORT = int(os.getenv("PORT", "8443"))  # Порт по умолчанию 8443

# Генерация случайного гос. номера
def generate_random_license():
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
    digits = ''.join(random.choices('0123456789', k=3))
    return f"{digits}{letters}02"

# Генерация случайной ссылки на QR
def generate_random_qr():
    random_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    return f"http://qr.tha.kz/{random_code}"

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Добро пожаловать в нашу компанию! Теперь у вас пожизненный проездной билет на все автобусы Алматы. Введите номер автобуса, чтобы оплатить проезд:"
    )

# Обработка сообщения с номером автобуса
async def bus_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bus_number = update.message.text

    # Установка часового пояса Алматы
    almaty_tz = pytz.timezone("Asia/Almaty")
    now = datetime.now(almaty_tz)

    date_only = now.strftime("%d/%m")  # Только дата
    time_only = now.strftime("%H:%M")  # Только время
    license_plate = generate_random_license()
    qr_link = generate_random_qr()

    # Формирование ответа с подчеркнутым временем
    response = (
        f"ONAY! ALA\n"
        f"IZ {date_only} <u>{time_only}</u>\n"  # Подчеркиваем только время
        f"{bus_number},{license_plate},{FIXED_PRICE}\n"
        f"{qr_link}"
    )

    # Отправка сообщения с HTML-разметкой
    await update.message.reply_text(response, parse_mode="HTML")

    # Удаление сообщения пользователя
    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

# Основная функция
def main():
    # Создаем приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bus_info))

    # Настройка Webhook
    webhook_url = f"https://{os.getenv('RAILWAY_STATIC_URL')}/{TOKEN}"  # Используем Railway домен
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=webhook_url,
    )

if __name__ == "__main__":
    main()
