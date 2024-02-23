from modules.config_loader import ConfigLoader
import discord
from discord.app_commands import CommandTree
from discord.ext import commands

def load_config():
    config_loader = ConfigLoader()

    try:
        config = config_loader.load_config()
        if config_loader.is_config_file_filled_in(): return config

        return None

    except (FileNotFoundError):
        config_loader.create_config_file()
        return None

def main():
    config = load_config()
    if not config: 
        print("Fill in the details in [./config.json].")
        return

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=config["bot-prefix"], intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user}')

    @bot.tree.command(name="ping", description="Replies with \"pong\".")
    async def ping(interaction:discord.Interaction):
        await interaction.response.send_message("pong", ephemeral=True)

    @bot.tree.command(name="sync", description="Syncs commands with discord", guild=discord.Object(config["dev-guild-id"]))
    async def sync(interaction:discord.Interaction):
        guild = discord.Object(config["dev-guild-id"])

        if guild: await interaction.response.send_message(f"\nSyncing commands to [{guild}]", ephemeral=True)
        else: await interaction.response.send_message(f"\nSyncing commands globally", ephemeral=True)

        if guild: bot.tree.copy_global_to(guild=guild)
        commands_synced = await bot.tree.sync(guild = guild)
        
        commands_synced_message = ""
        for command in commands_synced:
            commands_synced_message += f"[{command.name}] synced.\n"

        await interaction.response.edit_message(content=commands_synced_message)


    try:
        bot.run(config["bot-token"])
    except discord.errors.LoginFailure as error:
        print(error.args[0])

if __name__ == "__main__":
    main()