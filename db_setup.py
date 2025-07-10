import aiosqlite
import asyncio

async def create_tables():
    async with aiosqlite.connect("bot_database.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS gifts (
                gift_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                is_limited BOOLEAN DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_gifts (
                user_id INTEGER,
                gift_id INTEGER,
                quantity INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, gift_id)
            )
        """)
        await db.commit()

asyncio.run(create_tables())
