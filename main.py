from modules.config_loader import ConfigLoader
import discord

def load_config():
    try:
        config = config_loader.load_config()
        if not config_loader.is_config_file_filled_in(): return config

        return None

    except (FileNotFoundError):
        config_loader.create_config_file()
        return None


config_loader = ConfigLoader()
config = load_config()
if not config: print("Fill in the detials in {./config.json}.")

intents = discord.Intents.default()
intents.message_content = True