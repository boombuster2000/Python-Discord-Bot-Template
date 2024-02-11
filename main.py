from modules.config_loader import ConfigLoader
import discord
from discord.app_commands import CommandTree

def load_config():
    try:
        config = config_loader.load_config()
        if config_loader.is_config_file_filled_in(): return config

        return None

    except (FileNotFoundError):
        config_loader.create_config_file()
        return None

async def sync_app_commands(command_tree:CommandTree, guild:discord.Guild = None):
    commands_synced = []
    commands_synced = await command_tree.sync(guild = guild)
    
    for command in commands_synced:
        print(f"{command.name} synced.")


def run_bot(client:discord.Client, command_tree:CommandTree, config:dict):
    @client.event
    async def on_ready():
        guild = client.get_guild(config['dev-guild-id'])
        await sync_app_commands(command_tree, guild)
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
if not config: print("Fill in the details in [./config.json].")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
command_tree = CommandTree(client)

if config: run_bot(client, command_tree, config)

