import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz  # Библиотека для работы с часовыми поясами

TOKEN = '7885324267:AAHFISc1gkB7BCLXllYhFNG3bZIUeU9g4a0'
FIXED_PRICE = '120₸'

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

def main():
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bus_info))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
