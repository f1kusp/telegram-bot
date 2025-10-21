import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Получаем настройки из переменных окружения
BOT_TOKEN = os.environ['BOT_TOKEN']
ADMIN_CHAT_ID = os.environ['ADMIN_CHAT_ID']

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = "🤖 Бот для предложений! Отправьте сообщение."
    await update.message.reply_text(welcome_text)

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает сообщение администратору"""
    try:
        user = update.message.from_user
        
        if update.message.text:
            message_text = f"👤 {user.first_name}:\n{update.message.text}"
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_text)
            await update.message.reply_text("✅ Сообщение отправлено!")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text("❌ Ошибка отправки")

def main():
    """Основная функция"""
    print("🚀 Запуск бота на Railway...")
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.COMMAND, start_command))
    application.add_handler(MessageHandler(filters.ALL, forward_to_admin))
    
    print("✅ Бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
