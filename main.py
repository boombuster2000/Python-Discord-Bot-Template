from modules.config_loader import ConfigLoader
import discord
from discord.app_commands import CommandTree
from discord.ext import commands

def load_config():
    try:
        config = config_loader.load_config()
        if config_loader.is_config_file_filled_in(): return config

        return None

    except (FileNotFoundError):
        config_loader.create_config_file()
        return None

async def sync_app_commands(command_tree:CommandTree, guild:discord.Guild = None):
    if guild: print(f"\nSyncing commands to [{guild.name}]")
    else: print(f"\nSyncing commands globally")

    commands_synced = []
    commands_synced = await command_tree.sync(guild = guild)
    
    for command in commands_synced:
        print(f"[{command.name}] synced.")

    print(f"Total Commands Synced: {len(commands_synced)}\n")

def run_bot(client:discord.Client, config:dict):
    try:
        client.run(config["bot-token"])
    except discord.errors.LoginFailure as error:
        print(error.args[0])

config_loader = ConfigLoader()
config = load_config()
if not config: print("Fill in the details in [./config.json].")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    guild = await bot.fetch_guild(config['dev-guild-id'])
    #await sync_app_commands(command_tree, guild) # Uncomment to sync commands
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name="ping", description="Replies with \"pong\".")
async def ping(interaction:discord.Interaction) -> None:
    await interaction.response.send_message("pong", ephemeral=True)

if config: run_bot(bot, config)

