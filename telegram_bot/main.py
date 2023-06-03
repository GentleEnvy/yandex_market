import asyncio
import time

from bot import Bot

TOKEN = '5488378527:AAGRkM9oVjEftmShfy1JrXnYh6nbVhQl3TQ'

bot = Bot(TOKEN)


async def main():
    await asyncio.create_task(bot.listen())


print('run')
time.sleep(5)
asyncio.run(main())
