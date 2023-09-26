import asyncio
import httpx
from pyrocketbot import RocketBot
from commands.handler import MainCommandHandler
from utils.credentials import load_env

creds = load_env()
username = creds['bot_user']
password = creds['bot_password']
server = creds['server_url']

async def main():
    async with httpx.AsyncClient() as client:
        bot = RocketBot(username, password, server_url=server, client=client)
        handler = MainCommandHandler(bot)
        handler.register_commands()

        if bot.login_task:
            await bot.login_task

        print('Logged in\n')
        await bot.run(chat_type='c', sleep=0.5)

if __name__ == '__main__':
    asyncio.run(main())
