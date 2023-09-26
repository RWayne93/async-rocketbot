import time
from commands.base import CommandHandler
from llms.llama2 import chatbot_instance
import asyncio


class HuggingChatCommands(CommandHandler):
    async def ask_huggingface(self, message, match_list):
        user_message = match_list[0]
        loop = asyncio.get_event_loop()
        start_time = time.time()
        response = await loop.run_in_executor(None, lambda: chatbot_instance.chat(user_message))

        await self.bot.send_message(message['rid'], response)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Time taken for response: {duration:.2f} seconds")


# async def ask_huggingface(bot, message, match_list):
#     user_message = match_list[0]
    
#     # Run the synchronous method in a thread
#     loop = asyncio.get_event_loop()
#     response = await loop.run_in_executor(None, lambda: chatbot.chat(user_message))
    
#     await bot.send_message(message['rid'], response)