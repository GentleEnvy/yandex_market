import asyncio

from dotenv import dotenv_values

from bot import Bot

config = dotenv_values('.env')
TOKEN = config['TOKEN']
SECRET = config['SECRET']
LOG_LEVEL = config.get('LOG_LEVEL', 0)

bot = Bot(TOKEN, SECRET, LOG_LEVEL)


async def main():
    await asyncio.create_task(bot.listen())


asyncio.run(main())
