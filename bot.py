import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from flask import Flask

# === НАСТРОЙКИ === ЗАМЕНИТЕ НА СВОИ! ===
BOT_TOKEN = "8311718981:AAEWzb9VYJAcDshGcG7dQV_6pHnR21SpHbo"  # Токен из BotFather
ADMIN_CHAT_ID = "1247168929"  # Ваш Chat ID
# === КОНЕЦ НАСТРОЕК ===

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

class TelegramBot:
    def __init__(self):
        self.application = None
        self.setup_bot()
    
    def setup_bot(self):
        """Настраивает бота"""
        try:
            self.application = Application.builder().token(BOT_TOKEN).build()
            
            # Добавляем обработчики
            self.application.add_handler(MessageHandler(filters.COMMAND, self.start_command))
            self.application.add_handler(MessageHandler(filters.ALL, self.forward_to_admin))
            
            logger.info("✅ Бот настроен и готов к работе!")
            
        except Exception as e:
            logger.error(f"❌ Ошибка настройки бота: {e}")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🤖 Добро пожаловать в бот для предложений!

💡 Просто отправьте ваше предложение, вопрос или отзыв, и я сразу перешлю его администратору.

📝 Вы можете отправлять:
• Текстовые сообщения
• Фотографии с подписями
• Документы

⚡ Администратор получит ваше сообщение мгновенно!
        """
        await update.message.reply_text(welcome_text)
    
    async def forward_to_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Пересылает сообщение администратору"""
        try:
            user = update.message.from_user
            user_info = f"👤 Новое сообщение от: {user.first_name}"
            if user.last_name:
                user_info += f" {user.last_name}"
            if user.username:
                user_info += f" (@{user.username})"
            user_info += f"\n🆔 ID: {user.id}"
            
            if update.message.text:
                message_text = f"{user_info}\n\n💬 Сообщение:\n{update.message.text}"
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_text)
                await update.message.reply_text("✅ Ваше сообщение отправлено администратору!")
            
            elif update.message.photo:
                caption = update.message.caption or "📷 Фото без подписи"
                message_text = f"{user_info}\n\n📸 Фото с подписью:\n{caption}"
                await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message_text)
                await context.bot.send_photo(
                    chat_id=ADMIN_CHAT_ID,
                    photo=update.message.photo[-1].file_id,
                    caption=f"Фото от {user.first_name}"
                )
                await update.message.reply_text("✅ Ваше фото отправлено администратору!")
                
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            await update.message.reply_text("❌ Произошла ошибка при отправке сообщения")
    
    def start_polling(self):
        """Запускает бота в фоновом режиме"""
        if self.application:
            self.application.run_polling()

# Создаем экземпляр бота
bot = TelegramBot()

@app.route('/')
def home():
    return "🤖 Telegram Bot is running! Status: OK"

@app.route('/start_bot')
def start_bot():
    """Запускает бота"""
    try:
        bot.start_polling()
        return "✅ Бот запущен!"
    except Exception as e:
        return f"❌ Ошибка запуска: {e}"

@app.route('/health')
def health():
    return "🟢 Bot is healthy"

# Запускаем бота при импорте
if __name__ == "__main__":
    print("🚀 Запуск бота...")
    bot.start_polling()
