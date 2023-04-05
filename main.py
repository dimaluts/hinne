from aiogram import Bot, Dispatcher, executor
from settings import token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from modules.register_module_handlers import register_module_handler
from modules import register_callback_handler

bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

async def send_logs(chat_id, text):
    await bot.send_message(chat_id, text)

async def register_handlers(dp):
    register_callback_handler(dp)
    register_module_handler(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=register_handlers)
