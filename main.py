from modules.config_loader import ConfigLoader

config_loader = ConfigLoader()

try:
    config = config_loader.load_config()
    if config_loader.is_config_file_filled_in(): print("Fill in details in config file.")

except (FileNotFoundError):
    config_loader.create_config_file()
    print("Fill in details in config file.")