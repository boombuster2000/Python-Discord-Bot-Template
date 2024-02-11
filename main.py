import json


def create_config_file(config_fp="./config.json"):
    CONFIG_FILE_TEMPLATE = {
        "bot-token":"BOT-TOKEN"
    }

    with open(config_fp, "w") as config_file:
        json.dump(CONFIG_FILE_TEMPLATE, config_file, indent=4)
        print("Fill in details in config file.")

def load_config(config_fp="./config.json"):
    try:
        with open(config_fp, "r") as config_file:
            config = json.load(config_file)
            return config
    except (json.decoder.JSONDecodeError):
        print("Invalid JSON in config file, resetting config file.")
        create_config_file()

def is_config_file_filled_in(config, config_fp="./config.json"):
    CONFIG_FILE_TEMPLATE = {
        "bot-token":"BOT-TOKEN"
    }

    for key in CONFIG_FILE_TEMPLATE.keys():
        if config[key] == CONFIG_FILE_TEMPLATE[key]: 
            return True
        
    return False

config = None

try:
    config = load_config()
    if is_config_file_filled_in(config): print("Fill in details in config file.")
    
except (FileNotFoundError):
    create_config_file()




