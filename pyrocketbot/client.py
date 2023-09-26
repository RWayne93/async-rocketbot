import re
import asyncio
import collections
from rocketchat_API.rocketchat import RocketChat
from datetime import datetime, timezone


class RocketBot(RocketChat):
    _commands = {}
    
    def __init__(self, username, password, server_url, client, proxy_dict=None, threading_updates=False):
        super().__init__(user=username, password=password, server_url=server_url, session=client, proxies=proxy_dict)
        
        self.bot_username = username
        self._threading = threading_updates
        self.last_processed_timestamp = self.get_current_utc_timestamp()

    @staticmethod
    def get_current_utc_timestamp():
        """Get the current UTC timestamp in the same format as the messages."""
        return datetime.now(timezone.utc).isoformat()
        
    # @classmethod
    # def command(cls, regex, description=None):
    #     def decorator(func):
    #         cls._commands[regex] = {
    #             'function': func,
    #             'description': description
    #         }
    #         return func
    #     return decorator

    def register_command(self, pattern, func, description=""):
        self._commands[pattern] = {
            'function': func,
            'description': description
        }

    async def send_message(self, chat_id, text):
        return await self.chat_post_message(text, chat_id)

    async def get_updates(self):
        response = await self.subscriptions_get()
        data = response.json()
        return data.get('update')

    # async def run(self, chat_type='', sleep=0):
    #     #print(f"Registered commands: {self._commands.keys()}")
    #     ids = collections.deque(maxlen=10000)
    #     while True:
    #         updates = await self.get_updates()

    #         if updates:
    #             for result in updates:
    #                 try:
    #                     chat_type = result['t']
    #                     room_id = result['rid']
                        
    #                     if chat_type == "d":
    #                         response = await self.im_history(room_id)
    #                         messages = response.json().get('messages', [])
    #                     elif chat_type == "c":
    #                         response = await self.channels_history(room_id)
    #                         messages = response.json().get('messages', [])
    #                     elif chat_type == "p":
    #                         response = await self.groups_history(room_id)
    #                         messages = response.json().get('messages', [])
    #                     else:
    #                         continue

    #                     if result['t'] == chat_type:
    #                         for message in messages:
    #                             if message['_id'] in ids or message['u']['username'] == self.bot_username:
    #                                 continue
    #                             ids.append(message['_id'])

    #                             message_timestamp = message['ts']
    #                             if self.last_processed_timestamp and message_timestamp <= self.last_processed_timestamp:
    #                                 continue

    #                             for k, v in self._commands.items():
    #                                 regex = re.compile(k, flags=re.MULTILINE | re.DOTALL)
    #                                 m = regex.match(message['msg'])

    #                                 if m:
    #                                     match_list = []
    #                                     print(f"Matches for command {k}: {m.groups()}")
    #                                     for x in m.groups():
    #                                         match_list.append(x)
    #                                     try:
    #                                         await v(message, match_list)
    #                                     except TypeError as e:
    #                                         print(f"TypeError encountered: {e}")
    #                                         await v(message)

    #                 except Exception as e:
    #                     print(f'Error: {e} in {result}')

    #         await asyncio.sleep(sleep)

    async def run(self, chat_type='', sleep=0):
        ids = collections.deque(maxlen=10000)
        while True:
            updates = await self.get_updates()

            if updates:
                for result in updates:
                    try:
                        chat_type = result['t']
                        room_id = result['rid']
                        
                        if chat_type == "d":
                            response = await self.im_history(room_id)
                            messages = response.json().get('messages', [])
                        elif chat_type == "c":
                            response = await self.channels_history(room_id)
                            messages = response.json().get('messages', [])
                        elif chat_type == "p":
                            response = await self.groups_history(room_id)
                            messages = response.json().get('messages', [])
                        else:
                            continue

                        if result['t'] == chat_type:
                            for message in messages:
                                if message['_id'] in ids or message['u']['username'] == self.bot_username:
                                    continue
                                ids.append(message['_id'])

                                message_timestamp = message['ts']
                                if self.last_processed_timestamp and message_timestamp <= self.last_processed_timestamp:
                                    continue

                                for pattern, command_data in self._commands.items():
                                    regex = re.compile(pattern, flags=re.MULTILINE | re.DOTALL)
                                    m = regex.match(message['msg'])
                                    func = command_data['function']

                                    if m:
                                        match_list = m.groups()
                                        print(f"Matches for command {pattern}: {match_list}")
                                        try:
                                            await func(message, match_list)
                                        except TypeError as e:
                                            print(f"TypeError encountered: {e}")
                                            await func(message)

                    except Exception as e:
                        print(f'Error: {e} in {result}')

            await asyncio.sleep(sleep)
