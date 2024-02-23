from modules.config_loader import ConfigLoader
import discord
from discord.ext import commands
from typing import Literal

def load_config():
    config_loader = ConfigLoader()

    try:
        config = config_loader.load_config()
        if config_loader.is_config_file_filled_in(): return config

        return None

    except (FileNotFoundError):
        config_loader.create_config_file()
        return None

async def sync_app_commands(command_tree, guild = None):
    if guild: print(f"\nSyncing commands to [{guild}]")
    else: print(f"\nSyncing commands globally")

    if guild: command_tree.copy_global_to(guild=guild)
    commands_synced = await command_tree.sync(guild = guild)
    
    for command in commands_synced:
        print(f"[{command.name}] synced.")

    print(f"Total Commands Synced: {len(commands_synced)}\n")


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
        await sync_app_commands(bot.tree, discord.Object(config["dev-guild-id"]))
        print(f'We have logged in as {bot.user}')

    @bot.tree.command(name="ping", description="Replies with \"pong\".")
    async def ping(interaction:discord.Interaction):
        await interaction.response.send_message("pong", ephemeral=True)

    @bot.tree.command(name="sync", description="Syncs commands with discord", guild=discord.Object(config["dev-guild-id"]))
    async def sync(interaction:discord.Interaction, globally:Literal["True", "False"]):
        guild = await bot.fetch_guild(config["dev-guild-id"])
        commands_synced_message = ""

        if guild: commands_synced_message = f"**__Syncing commands to [{guild}]__**\n"
        else: commands_synced_message = f"**__Syncing commands globally__**\n"

        await interaction.response.send_message(content=commands_synced_message)

        if guild: bot.tree.copy_global_to(guild=guild)
        commands_synced = await bot.tree.sync(guild = guild)
        
        for command in commands_synced:
            commands_synced_message += f"[{command.name}] synced.\n"

        await interaction.edit_original_response(content=commands_synced_message)


    try:
        bot.run(config["bot-token"])
    except discord.errors.LoginFailure as error:
        print(error.args[0])

if __name__ == "__main__":
    main()