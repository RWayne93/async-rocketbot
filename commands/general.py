from .base import CommandHandler

class GeneralCommands(CommandHandler):
    async def echo(self, message, match_list):
        await self.bot.send_message(message['rid'], match_list[0])

    async def ping_command(self, message, match_list=None):
        await self.bot.send_message(message['rid'], 'pong')

    async def list_commands(self, message, match_list=None):
        commands_list = []
        for cmd, cmd_data in self.bot._commands.items():
            description = cmd_data.get('description', "")
            if '(.*)' in cmd:
                cmd = cmd.replace('(.*)', "<your_input>")
            commands_list.append("{} - {}".format(cmd, description))
        response_text = "Available commands:\n{}".format('\n'.join(commands_list))
        await self.bot.send_message(message['rid'], response_text)

# async def list_commands(bot, message, match_list=None):
#     commands_list = []
#     for cmd, cmd_data in bot._commands.items():
#         description = cmd_data.get('description', "")
#         if '(.*)' in cmd:
#             cmd = cmd.replace('(.*)', "<your_input>")
#         commands_list.append("{} - {}".format(cmd, description))
#     response_text = "Available commands:\n{}".format('\n'.join(commands_list))
#     await bot.send_message(message['rid'], response_text)

# async def echo(bot, message, match_list):
#     await bot.send_message(message['rid'], match_list[0])

# async def ping_command(bot, message, match_list=None):
#     await bot.send_message(message['rid'], 'pong')
