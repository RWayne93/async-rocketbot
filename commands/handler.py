from commands.general import GeneralCommands
from commands.huggingchat import HuggingChatCommands

class MainCommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.general_commands = GeneralCommands(bot)
        self.huggingchat_commands = HuggingChatCommands(bot)

    def register_commands(self):
        self.bot.register_command(r'!echo (.*)', self.general_commands.echo, description="Echoes your input")
        self.bot.register_command(r'!askllama (.*)', self.huggingchat_commands.ask_huggingface, description="Ask the llama2 model a question. Model hosted by huggingface.")
        self.bot.register_command(r'!ping', self.general_commands.ping_command, description="Checks if bot is running")
        self.bot.register_command(r'!help', self.general_commands.list_commands, description="Lists all available commands")