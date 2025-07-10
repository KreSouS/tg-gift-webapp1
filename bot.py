from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Filter
from aiogram.types import ContentType
from aiohttp import web
import asyncio
import aiosqlite
import json

BOT_TOKEN = "7661009860:AAHs7J0C-BHsFSa_cLK04yfv5lqlTG3lZ4E"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Кастомный фильтр для обработки данных из WebApp
class WebAppDataFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.content_type == ContentType.WEB_APP_DATA


@dp.message(Command("add"))
async def add_points(message: types.Message):
    await update_balance(message.from_user.id, 10)
    balance = await get_balance(message.from_user.id)
    await message.answer(f"Твой баланс пополнен. Сейчас у тебя {balance} очков.")


@dp.message(WebAppDataFilter())
async def handle_webapp_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)  # JSON строка → словарь
        reward = data.get("reward", 0)

        await update_balance(message.from_user.id, reward)
        balance = await get_balance(message.from_user.id)

        await message.answer(
            f"Ты получил {reward} монет! Текущий баланс: {balance} очков."
        )
    except Exception as e:
        await message.answer(f"Ошибка при обработке данных: {e}")


@dp.message()
async def handle_message(message: types.Message):
    await add_user_if_not_exists(message.from_user.id, message.from_user.username or "")
    balance = await get_balance(message.from_user.id)

    button = types.KeyboardButton(
        text="🎁 Открыть WebApp",
        web_app=types.WebAppInfo(url="https://KreSouS.github.io/tg-gift-webapp1/")
    )
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True
    )

    await message.answer(
        f"Привет, @{message.from_user.username or message.from_user.first_name}!\n"
        f"Твой баланс: {balance} очков.\n"
        f"Нажми кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


async def add_user_if_not_exists(user_id: int, username: str):
    async with aiosqlite.connect("bot_database.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

async def handle_get_balance(request):
    data = await request.json()
    user_id = data.get("user_id")
    if not user_id:
        return web.json_response({"error": "no user_id"}, status=400)
    
    balance = await get_balance(int(user_id))
    return web.json_response({"balance": balance})  

async def get_balance(user_id: int):
    async with aiosqlite.connect("bot_database.db") as db:
        async with db.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0


async def update_balance(user_id: int, amount: int):
    async with aiosqlite.connect("bot_database.db") as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()


async def main():
    # Удаляем старый вебхук
    await bot.delete_webhook(drop_pending_updates=True)

    # Создаём aiohttp-сервер
    app = web.Application()
    app.add_routes([web.post("/get_balance", handle_get_balance)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)  # 8080 — порт, можно поменять
    await site.start()

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
