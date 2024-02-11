import json


def create_config_file(config_fp="./config.json"):
    CONFIG_FILE_TEMPLATE = {
        "bot-token":"BOT-TOKEN"
    }

    with open(config_fp, "w") as config_file:
        json.dump(CONFIG_FILE_TEMPLATE, config_file, indent=4)
        print("Fill in details in config file.")

create_config_file()