from modules.config_loader import ConfigLoader
import discord
from discord.app_commands import CommandTree

def load_config():
    try:
        config = config_loader.load_config()
        if not config_loader.is_config_file_filled_in(): return config

        return None

    except (FileNotFoundError):
        config_loader.create_config_file()
        return None

async def sync_app_commands(client, globally=True):
    pass


def run_bot(client):
    @client.event
    async def on_ready():
        

        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    try:
        client.run(config["bot-token"])
    except discord.errors.LoginFailure as error:
        print(error.args[0])


config_loader = ConfigLoader()
config = load_config()
if not config: print("Fill in the detials in {./config.json}.")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
command_tree = CommandTree(client)

if config: run_bot(client)

