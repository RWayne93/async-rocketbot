### Installation
- From GitHub:
Clone our repository and `https://github.com/RWayne93/async-rocketbot.git`

### Requirements
- TODO

### Info. 
This rocket chat bot framework is based on an async implementation of rocketchat_API below you can find usage examples. 

### Usage
```python
import asyncio
from rocketchat_API.rocketchat import RocketChat

async def main():
    rocket = RocketChat('user', 'pass', server_url='server_url')
    if rocket.login_task:
        await rocket.login_task
        print('Login successful!')

    # Use the methods to test
    response = await rocket.chat_post_message('test message using asynchronous library!', room_id='room_id')
    print(response.json())
    
asyncio.run(main())
```

*note*: every method returns a [requests](https://github.com/kennethreitz/requests) Response object.

#### Connection pooling
If you are going to make a couple of request, you can user connection pooling provided by `requests`. This will save significant time by avoiding re-negotiation of TLS (SSL) with the chat server on each call.

```python
import asyncio
import httpx
from rocketchat_API.rocketchat import RocketChat

async def main():
    async with httpx.AsyncClient() as client:
    rocket = RocketChat('user', 'pass', server_url='server_url', client=client)
    if rocket.login_task:
        await rocket.login_task
    
    print(rocket.channels_list().json())
    print(rocket.channels_history('GENERAL', count=5).json())

asyncio.run(main())
```

### Simple bot usage
```python
import asyncio
import httpx
from pyrocketbot import RocketBot
from commands.handler import MainCommandHandler

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
```